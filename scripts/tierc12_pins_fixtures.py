#!/usr/bin/env python
"""TIER-C12 · TC12-REG · THE PINS SUITE [LEANS L-0.17, L-0.18, L-0.23; CANON-25] — three blocks.

  F-PINS       the contract pin door, its map, its derived file, the register and the totality
  F-VETO       the veto map: each token of the VETOES line -> its register rows (VETO_ROWS_T)
  F-FAM-PINS   the families parsed at the REGISTRATION stage against the typed referee
               (a reading's addition — never one of F-FAM's blocks, L-0.19)

Production is scripts/tierc12_pins.py and the four filed files under pins/.  Every BREAK plant is
a mutation INSIDE production — a scratch copy of the map, the register, the derived file, the
classed tokens, the contract prefix (with a scratch STEP Q record, so the plant reaches the law it
names and not the prefix pin) or the door's own source — judged one at a time by the detector the
plant names.  The referees below are this suite's own typed commission, a second object: no value
is read back from the door to judge the door.

PRE-SUBSTRATE: no bar is read, no book exists, no env is imported, no network is touched.  The
registry (registrations/REGISTRATIONS.json) is filed after the pin files in the same record; its
two clauses assert on the filed payloads when it is on file and say so in one line when it is not.

Run (stdlib only; the transcript is pins/FIXTURES_PINS.txt):
  ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_pins_fixtures.py
      [--root=DIR] [--refile-transcript] [<leg filter> ...]
Exit 0 = every leg GREEN, every break RED, the transcript byte-identical to the record.
"""
from __future__ import annotations

import ast
import importlib.util
import json
import shutil
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import tierc12_fx as FX          # noqa: E402
import tierc12_pins as PINS      # noqa: E402

ROOT = PINS.ROOT
MAIN = PINS.main_tree(ROOT)
T12 = ROOT / "research_outputs" / "tierc12"
TRANSCRIPT = "FIXTURES_PINS.txt"
REGISTRY = T12 / "registrations" / "REGISTRATIONS.json"
VENUE_PROBE = "research_outputs/tierc10/data/VENUE_PROBE.json"      # TC10's Stage D probe [L-D.10]
BANNER = ("TIER-C12 TC12-REG PINS FIXTURES — L-0.17 the contract pin door, the pin map, the pin "
          "register, the totality · L-0.23 the veto map · L-0.18 the families — break leg first, "
          "RED or void")

# ═══════════════════════════════════════════════ THE TYPED COMMISSION (second objects)
SEED_T = 20261008
KINDS_T = ("contract", "x_record", "stage_d", "fitted", "lineage", "ruling")
TYPES_T = ("int", "fraction", "word", "iso", "str")
STAGE_LETTERS_T = ("G", "R", "S")
VA_LENSES_T = ("1h", "4h", "12h", "1d", "1w")
TRAVERSE_LENSES_T = ("1h", "4h", "12h", "1d")
# the pin NAMES OF RECORD [L-0.17 / CANON-25 point 3] -> the register kind of each
NAMES_T = {
    "seed": "contract", "fam.q": "contract", "fam.<stage letter>": "contract",
    "ctrl.sum_net_r": "contract", "va.accept_n": "contract", "va.accept_margin_atr": "contract",
    "va.sfp_k": "contract", "va.nest_frac": "contract", "va.value_area_pct": "contract",
    "va.mirror_words": "contract", "va.licence_set": "contract", "va.lookback.<lens>": "x_record",
    "adm.old_quantile": "contract", "adm.lag_cut": "contract", "adm.preseen_cell": "contract",
    "adm.abs_cut": "contract", "brd.cut": "contract", "rr_min": "contract",
    "sfp.rail_atr": "contract", "sfp.t1_fraction": "contract", "sfp.t2_offset_atr": "contract",
    "chop.n_bands": "contract", "tp1d.approach_atr": "contract", "two_trades.horizons": "contract",
    "book.trg912_periods": "contract", "grid.x16_shape": "contract", "grid.brd_levels": "contract",
    "scalp.third_long_max": "contract", "scalp.third_short_min": "contract",
    "scalp.ema_fast": "contract", "scalp.ema_slow": "contract",
    "scalp.trigger_prox_atr": "contract", "scalp.validity_bars": "contract",
    "scalp.fill_ticks": "contract", "scalp.deep_atr": "contract",
    "scalp.stop_beyond_atr": "contract", "scalp.rail_atr": "contract",
    "scalp.t1_fraction": "contract", "scalp.t2_offset_atr": "contract", "scalp.era": "contract",
    "loao.line": "contract", "ledger.opening": "contract", "ledger.n_min": "contract",
    "ferry.bus_dir": "contract", "ferry.cap_mb": "contract",
    "fee.maker_bps_side.<VENUE>": "stage_d", "traverse.<lens>": "fitted",
    "traverse.1h.in_5m_bars": "fitted", "ruling.tc11_stamp": "ruling", "ruling.1w": "ruling",
}
# rows the DOOR names (no name of record exists): seam 35's literals of scripts/tierc11_score.py,
# L-0.17's lineage door, and the constants L-V.4's table lists with a kind and no name
SCORE_LITERALS_T = ("REQUIRED", "INT_COLS", "FLOAT_COLS", "STR_COLS", "SORT_KEY", "HAIRCUT_TOL",
                    "SUM_TOL", "NET_LAW_TOL", "EXIT_FLAGS")
DOOR_NAMED_T = {
    **{f"lineage.tierc11_score.{n}": "lineage" for n in SCORE_LITERALS_T},
    "lineage.tierc2_rules.ATR_LEN": "lineage", "lineage.tierc5_rules.WARMUP_BARS": "lineage",
    "lineage.tierc5_rules.PROVISIONAL_MIN_N": "lineage", "lineage.tierc10_panel.N_BOOT": "lineage",
    "lineage.tierc10_panel.LENS_MS": "lineage", "lineage.tierc10_panel.ERA_CUT_MS": "lineage",
    "lineage.analytics_profile.PROFILE_ROWS": "lineage",
    "lineage.analytics_profile.VALUE_AREA": "lineage",
    "lineage.tierc2_baseline._round_floats.nd": "lineage",
    "x.va.laws.k_draws": "x_record", "x.va.laws.dev_return_bars": "x_record",
}
# the referee of every contract pin, in the door's exact form (a fraction is "num/den")
MIRROR_T = ["4h", "taker", "PASS", "1d", "taker", "PASS", "1h", "maker", "PASS", "12h", "", "FAIL",
            "1h", "taker", "FAIL"]
VALUES_T = {
    "seed": 20261008, "fam.q": "1/10", "fam.G": ["G", "ADMISSION", 2, "1/20"],
    "fam.R": ["R", "RANGE-STATE", 2, "1/20"], "fam.S": ["S", "SCALPER", 1, "1/10"],
    "ctrl.sum_net_r": "20403783/500000", "va.accept_n": 8, "va.accept_margin_atr": "3/2",
    "va.sfp_k": 3, "va.nest_frac": "1/4", "va.value_area_pct": 70, "va.mirror_words": MIRROR_T,
    "va.licence_set": ["4h", "taker", "1d", "taker", "1h", "maker"], "adm.old_quantile": 75,
    "adm.lag_cut": 16, "adm.preseen_cell": [110, "103/200"], "adm.abs_cut": 206,
    "brd.cut": [2, 5], "rr_min": "3/2", "sfp.rail_atr": "1/1", "sfp.t1_fraction": "1/2",
    "sfp.t2_offset_atr": "1/4", "chop.n_bands": 10, "tp1d.approach_atr": "1/4",
    "two_trades.horizons": [20, 100], "book.trg912_periods": [9, 12],
    "grid.x16_shape": [2, 2, 2, 2], "grid.brd_levels": [0, 5], "scalp.third_long_max": 33,
    "scalp.third_short_min": 67, "scalp.ema_fast": 12, "scalp.ema_slow": 89,
    "scalp.trigger_prox_atr": "1/4", "scalp.validity_bars": 12, "scalp.fill_ticks": 1,
    "scalp.deep_atr": "1/20", "scalp.stop_beyond_atr": "1/2", "scalp.rail_atr": "1/1",
    "scalp.t1_fraction": "1/2", "scalp.t2_offset_atr": "1/4", "scalp.era": "holdout",
    "loao.line": [3, 5], "ledger.opening": "2026-09-21T16:00Z", "ledger.n_min": 30,
    "ferry.bus_dir": "exchange/rows/tierc12/", "ferry.cap_mb": 2,
}
# the families [L-0.18]: (stage, family, m, bar exact, registration ids) and q
Q_T = "1/10"
FAMILIES_T = (("G", "ADMISSION", 2, "1/20", ("P-ADM-1", "P-BRD-1")),
              ("R", "RANGE-STATE", 2, "1/20", ("P-DIR-1", "P-SFP-VA-1")),
              ("S", "SCALPER", 1, "1/10", ("P-SCALP-3",)))
# the VETOES line [contract :135-137]: token -> does the line give a parenthesised value
VETO_TOKENS_T = (("va-lookback", False), ("sfp-k", True), ("nest", True), ("breadth", True),
                 ("rr-min", True), ("outer-third", True), ("validity", True), ("fill", True),
                 ("maker-bps", False), ("era", True), ("tc11-stamp", False), ("1w", False))
VETO_ROWS_T = {
    "va-lookback": ("va.lookback.<lens>",), "sfp-k": ("va.sfp_k",), "nest": ("va.nest_frac",),
    "breadth": ("brd.cut",), "rr-min": ("rr_min",),
    "outer-third": ("scalp.third_long_max", "scalp.third_short_min"),
    "validity": ("scalp.validity_bars",), "fill": ("scalp.fill_ticks",),
    "maker-bps": ("fee.maker_bps_side.<VENUE>",), "era": ("scalp.era",),
    "tc11-stamp": ("ruling.tc11_stamp",), "1w": ("ruling.1w",),
}
FIXTURE_NAMES_T = ("F-CTRL", "F-D-2", "F-D-3", "F-VA-ASOF", "F-VA-RAW", "F-VA-MIRROR", "F-STATE",
                   "F-TRAV", "F-GATE", "F-BRD", "F-DIR", "F-SFP", "F-SCALP", "F-TOLL",
                   "F-NEST-ASOF", "F-LEDGER", "F-FAM", "F-DET", "F-GRID", "F-KEY",
                   "import-closure", "worktree attestation")
# the totality: the classed tokens of the prefix, counted by class
CLASS_COUNTS_T = {"date": 4, "hand_sample_count": 8, "history_figure": 3, "id": 32,
                  "index_offset": 2, "lens_name": 61, "print_format": 2, "prior": 5,
                  "ruling_or_section_id": 19, "tier_id": 16}
N_LINES_T = 137
# the record ids a register row may name as a consumer [L-0.10: ORDER and SUBSTAGES_T]
RECORDS_T = ("TC12-REG", "TC12-REG.ledger-spec", "TC12-D", "TC12-D.mirror", "TC12-ENV.vendor",
             "TC12-ENV", "TC12-ENV.score-build", "TC12-V", "TC12-V.trades", "TC12-C.tide",
             "TC12-C", "TC12-V.stamps.c", "TC12-G", "TC12-R.dir", "TC12-R.sfp", "TC12-R.tables",
             "TC12-R", "TC12-V.stamps.r", "TC12-S", "TC12-V.stamps.s", "TC12-L", "TC12-SCORE",
             "TC12-FIX", "TC12-REVIEW", "TC12-CLOSE")
# seam 63: the consumers these rows must name
SEAM63_T = {"ledger.opening": ("TC12-REG.ledger-spec", "TC12-L"),
            "ledger.n_min": ("TC12-REG.ledger-spec", "TC12-L"),
            "adm.lag_cut": ("TC12-REG.ledger-spec", "TC12-L"),
            "seed": ("TC12-REG.ledger-spec", "TC12-L"),
            "ferry.bus_dir": ("TC12-L", "TC12-CLOSE"), "ferry.cap_mb": ("TC12-L", "TC12-CLOSE")}
# L-0.24's sets (a)-(f), the members a path names at filing (sets (d) and (e) are closed by the
# stamp proof at TC12-CLOSE): no TC12 pin may be the whole-file sha of one of these
STAMP_SETS_T = ("research_outputs/tierc11/registrations/REGISTRATIONS.json",
                "research_outputs/tierc11/registrations/REGISTRY_PIN.json",
                "scripts/tierc11_registrations.py", "scripts/tierc11_score.py",
                "scripts/tierc11_score_fixtures.py", "scripts/tierc11_stage_g.py",
                "scripts/tierc11_stage_t_brk.py",
                "research_outputs/tierc11/scores/REGISTRY_CHECK.json",
                "research_outputs/tierc11/PROGRESS.json")
ABBREV_MIN_T = 8                 # "whole or abbreviated": a hex run of at least this many chars
FLOW_PINS_T = ("fam.q", "fam.G", "fam.R", "fam.S")
SHADOW_OLD_T = "        q = values[FAM_Q]\n"
SHADOW_NEW_T = "        q = Fraction(1, 10)\n"

DATA_FILES = (PINS.MAP_NAME, PINS.PINS_NAME, PINS.REGISTER_NAME, PINS.UNPINNED_NAME)
_TMP: list = []
_N = [0]


# ═══════════════════════════════════════════════ SCRATCH COPIES OF PRODUCTION
def venues() -> list:
    """The venue names of TC10's Stage D table, READ from its probe — never typed [L-D.21]."""
    doc = json.loads((MAIN / VENUE_PROBE).read_text(encoding="utf-8"))
    return sorted({r["venue"] for k in ("classic5", "unseen12") for r in doc[k]})


def expand(names) -> list:
    out = []
    for n in names:
        if n.endswith("<stage letter>"):
            out += [n.replace("<stage letter>", x) for x in STAGE_LETTERS_T]
        elif n == "va.lookback.<lens>":
            out += [n.replace("<lens>", x) for x in VA_LENSES_T]
        elif n == "traverse.<lens>":
            out += [n.replace("<lens>", x) for x in TRAVERSE_LENSES_T]
        elif n.endswith("<VENUE>"):
            out += [n.replace("<VENUE>", x) for x in venues()]
        else:
            out.append(n)
    return out


def real() -> PINS.Door:
    """A fresh door over the filed files (nothing memoised between legs)."""
    return PINS.Door()


def scratch(*, edit=None, contract=None, amendment=None, refile=False) -> PINS.Door:
    """A door over a scratch copy of pins/.  `edit` = {file name: doc -> doc}; `contract` = a
    function over the prefix text, filed with a scratch STEP Q record of its own bytes and sha;
    `amendment` = text appended to a copy of LEANS_AMENDMENTS.md; `refile` re-derives the scratch
    CONTRACT_PINS.json, for a plant that must stay consistent up to the law it names."""
    _N[0] += 1
    d = Path(_TMP[0]) / f"s{_N[0]}"
    (d / "pins").mkdir(parents=True)
    for name in DATA_FILES:
        doc = PINS.read_json(T12 / "pins" / name)
        if edit and name in edit:
            doc = edit[name](doc)
        (d / "pins" / name).write_bytes(PINS.render(doc))
    kw = {"root": ROOT, "pins_dir": d / "pins", "main": MAIN}
    if contract is not None:
        text = contract("\n".join(real().prefix()["lines"]))
        raw = text.encode("utf-8")
        (d / "contract.md").write_bytes(raw)
        (d / "STEP_Q.json").write_text(json.dumps({"artifact_shas": {PINS.CONTRACT_REL: {
            "bytes": len(raw), "sha256": PINS.sha_bytes(raw)}}}), encoding="utf-8")
        kw.update(contract=d / "contract.md", step_q=d / "STEP_Q.json")
    if amendment is not None:
        (d / "AM.md").write_text((T12 / "LEANS_AMENDMENTS.md").read_text(encoding="utf-8")
                                 + amendment, encoding="utf-8")
        kw["amendments"] = d / "AM.md"
    door = PINS.Door(**kw)
    if refile:
        door.file(refile=True)
    return door


def rows_edit(name: str, fn):
    """An edit of one file's `rows` (the map or the register) or `tokens` (the classed tokens)."""
    key = "tokens" if name == PINS.UNPINNED_NAME else "rows"

    def edit(doc):
        doc[key] = fn(doc[key])
        return doc
    return {name: edit}


def one(pin: str, **change):
    """rows -> rows with the row `pin` changed (a key set to None is dropped)."""
    def fn(rows):
        out = []
        for r in rows:
            if r["pin"] == pin:
                r = {k: v for k, v in {**r, **change}.items() if v is not None or k == "veto"}
            out.append(r)
        return out
    return fn


def swap(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"the plant's anchor {old!r} stands {text.count(old)} times")
    return text.replace(old, new)


def line_swap(n: int, new: str):
    """prefix text -> the same text with line n replaced (the line count unchanged)."""
    def fn(text):
        lines = text.split("\n")
        lines[n - 1] = new
        return "\n".join(lines)
    return fn


# ═══════════════════════════════════════════════ DETECTORS
def guarded(thunk) -> list:
    """A door law is a HALT: carry its text as a finding."""
    try:
        return list(thunk())
    except SystemExit as e:
        return [str(e)]


def names_findings(d: PINS.Door) -> list:
    """PIN-NAME: the map and the register against the typed names of record."""
    out = []
    want = {n: NAMES_T[k] for k in NAMES_T for n in expand([k])}
    extra = dict(DOOR_NAMED_T)
    m = [r.get("pin") for r in PINS.read_json(d.pins_dir / PINS.MAP_NAME)["rows"]]
    reg = {}
    for r in PINS.read_json(d.pins_dir / PINS.REGISTER_NAME)["rows"]:
        reg.setdefault(r.get("pin"), r.get("kind"))
    for p in sorted(set(m) - set(want)):
        out.append(f"PIN-NAME {p}: a map row whose pin is not a name of record")
    for p in sorted(want):
        if p not in reg:
            out.append(f"PIN-NAME {p}: a name of record with no register row")
        elif reg[p] != want[p]:
            out.append(f"PIN-NAME {p}: the register files kind {reg[p]!r}; the name of record is "
                       f"of kind {want[p]!r}")
        if (want[p] == "contract") != (p in m):
            out.append(f"PIN-NAME {p}: a name of kind {want[p]!r} "
                       f"{'has no' if want[p] == 'contract' else 'has a'} map row")
    for p in sorted(set(reg) - set(want)):
        if extra.get(p) != reg[p]:
            out.append(f"PIN-NAME {p}: a register row ({reg[p]}) that is neither a name of record "
                       f"nor a row the door names (DOOR_NAMED_T)")
    for p in sorted(set(extra) - set(reg)):
        out.append(f"PIN-NAME {p}: a row the door names (DOOR_NAMED_T) is not in the register")
    return out


def door_findings(d: PINS.Door) -> list:
    """Every law of the door over one set of files, each run on its own so that one HALT hides
    no other finding."""
    out = names_findings(d)
    for thunk in (d.filed_findings, d.register_findings, d.totality_findings, d.equal_findings,
                  d.amendment_findings, lambda: [] if d.families() else []):
        out += guarded(thunk)
    return sorted(set(out), key=out.index)


def stdlib_findings(name: str, src: str) -> list:
    """PIN-STDLIB: the pin door imports a module outside the standard library."""
    mods = set()
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Import):
            mods |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom):
            mods.add((n.module or "").split(".")[0] if not n.level else ".")
    return [f"PIN-STDLIB {name}: imports {x!r}, which is not a standard-library module"
            for x in sorted(mods - set(sys.stdlib_module_names))]


def stamp_shas() -> dict:
    """{path: sha256} of L-0.24's nameable stamp-set members, read from the frozen files (the
    census sha of a byte-frozen path is the sha of its bytes)."""
    return {p: PINS.sha_bytes((MAIN / p).read_bytes()) for p in STAMP_SETS_T}


def census_findings(d: PINS.Door, registry_text) -> list:
    shas, out = stamp_shas(), []
    for r in PINS.read_json(d.pins_dir / PINS.REGISTER_NAME)["rows"]:
        out += PINS.census_sha_findings(f"register row {r.get('pin')}",
                                        json.dumps(r, sort_keys=True), shas, ABBREV_MIN_T)
    if registry_text is not None:
        out += PINS.census_sha_findings("the filed registry", registry_text, shas, ABBREV_MIN_T)
    return out


def referee_findings(d: PINS.Door) -> list:
    """PIN-REFEREE: the door's derivation against this suite's typed commission."""
    out = []
    doc = d.derive()
    got = {p: rec["value"] for p, rec in doc["pins"].items()}
    for p in sorted(set(got) | set(VALUES_T)):
        if got.get(p) != VALUES_T.get(p):
            out.append(f"PIN-REFEREE {p}: the door derives {got.get(p)!r}; the typed referee "
                       f"reads {VALUES_T.get(p)!r}")
    if tuple(doc["fixture_names"]) != FIXTURE_NAMES_T:
        out.append(f"PIN-REFEREE fixture names: the door parses {doc['fixture_names']}")
    if doc["contract"]["n_lines"] != N_LINES_T:
        out.append(f"PIN-REFEREE the prefix holds {doc['contract']['n_lines']} lines, typed "
                   f"{N_LINES_T}")
    counts = {}
    for t in d.unpinned().get("tokens", ()):
        counts[t.get("class")] = counts.get(t.get("class"), 0) + 1
    if counts != CLASS_COUNTS_T or sorted(d.unpinned().get("classes", {})) != sorted(CLASS_COUNTS_T):
        out.append(f"PIN-REFEREE classed tokens: {dict(sorted(counts.items()))} over classes "
                   f"{sorted(d.unpinned().get('classes', {}))}; typed {CLASS_COUNTS_T}")
    if tuple(d.register_doc().get("kinds", ())) != KINDS_T or tuple(d.map().get("types", ())) != TYPES_T:
        out.append("PIN-REFEREE the files' kinds or types are not the typed six and five")
    for r in d.register():
        bad = sorted(set(r["consumers"]) - set(RECORDS_T))
        if bad:
            out.append(f"PIN-REFEREE {r['pin']}: consumer(s) {bad} are not record ids")
        need = SEAM63_T.get(r["pin"], ())
        if not set(need) <= set(r["consumers"]):
            out.append(f"PIN-REFEREE {r['pin']}: consumers {r['consumers']} lack {list(need)} "
                       f"[seam 63]")
        if r["kind"] == "lineage" and r["pin"].startswith("lineage.tierc11_score.") \
                and "node_sha256" not in r:
            out.append(f"PIN-REFEREE {r['pin']}: a literal of scripts/tierc11_score.py with no "
                       f"node sha [seam 35]")
        if r["kind"] in ("fitted", "stage_d", "ruling") and "value" in r:
            out.append(f"PIN-REFEREE {r['pin']}: a {r['kind']} row carries a value at TC12-REG")
    if d.pin("seed") != SEED_T:
        out.append(f"PIN-REFEREE seed: the door reads {d.pin('seed')}, typed {SEED_T}")
    return out


def veto_findings(d: PINS.Door) -> list:
    """VETO-TOKENS / VETO-ROWS / VETO-NO-ROW / VETO-VALUE, then the door's own laws on the same
    files (VETO-AMENDMENT; the HALT PIN-ALSO of a value that differs from its stage line)."""
    out = []
    toks = guarded(d.veto_tokens)
    if toks and isinstance(toks[0], str):
        return toks
    got = tuple((t["token"], t["value_text"] is not None) for t in toks)
    if got != VETO_TOKENS_T:
        out.append(f"VETO-TOKENS the VETOES line parses to {got}; typed {VETO_TOKENS_T}")
    reg = PINS.read_json(d.pins_dir / PINS.REGISTER_NAME)["rows"]
    carry = {}
    for r in reg:
        if r.get("veto") is not None:
            carry.setdefault(r["veto"], []).append(r["pin"])
    maps = {r["pin"]: r for r in PINS.read_json(d.pins_dir / PINS.MAP_NAME)["rows"]}
    v_lines = PINS.read_json(d.pins_dir / PINS.MAP_NAME)["slices"]["vetoes"]["lines"]
    for token, has_value in VETO_TOKENS_T:
        want, have = sorted(expand(VETO_ROWS_T[token])), sorted(carry.get(token, []))
        if not have:
            out.append(f"VETO-NO-ROW \"{token}\": a token of the VETOES line names no register row")
        if have != want:
            out.append(f"VETO-ROWS \"{token}\": the register rows carrying it are {have}; "
                       f"VETO_ROWS_T names {want}")
        for p in want if has_value else ():
            cites = [c for c in maps.get(p, {}).get("also", ())
                     if v_lines[0] <= c["lines"][0] and c["lines"][1] <= v_lines[1]
                     and c["regex"].startswith(f'"{token}"')]
            if not cites:
                out.append(f"VETO-VALUE \"{token}\": the line gives a value in parentheses and "
                           f"the map row {p} holds no second citation of it — nothing parses it "
                           f"equal to its stage-text citation")
    for token in sorted(set(carry) - set(VETO_ROWS_T)):
        out.append(f"VETO-ROWS \"{token}\": carried by {sorted(carry[token])}; not a token of "
                   f"VETO_ROWS_T")
    out += guarded(d.amendment_findings)
    out += guarded(lambda: [] if d.load() else [])
    return out


def exact(x) -> Fraction:
    """A filed m, q or bar in any of the forms a registry may carry — "0.05", "1/20", 0.05."""
    return Fraction(x) if isinstance(x, (str, int)) else Fraction(repr(x))


def fam_referee_findings(fam: dict) -> list:
    """FAM-REFEREE: the door's parsed (stage, family, m, bar, ids) and q against the typed table."""
    got = tuple((f["stage"], f["family"], f["m"], f["bar_exact"], tuple(f["registrations"]))
                for f in fam["families"])
    out = []
    if got != FAMILIES_T:
        out.append(f"FAM-REFEREE the door parses {got}; the typed referee reads {FAMILIES_T}")
    if fam["q_exact"] != Q_T:
        out.append(f"FAM-REFEREE the door parses q = {fam['q_exact']}; typed {Q_T}")
    for f in fam["families"]:
        if f["bar_fraction"] != Fraction(Q_T) / f["m"] or exact(f["bar"]) != f["bar_fraction"]:
            out.append(f"FAM-BAR {f['family']}: the header's bar {f['bar']} is not q ÷ m = "
                       f"{Q_T} ÷ {f['m']}")
    return out


def registry_doc(fam: dict) -> dict:
    """A registry document in the keys of L-X.19, built from the door's parse — the base of the
    registry plants when no registry is on file yet."""
    return {"families": [{k: f[k] for k in ("family", "stage", "header_line", "m", "q", "bar",
                                            "bar_exact", "n_registrations")}
                         for f in fam["families"]],
            "registrations": [{"registration": r["registration"], "seq": i + 1,
                               "family": r["family"], "family_m": r["m"], "family_bar": r["bar"],
                               "prior_pct": r["prior_pct"],
                               "operative_spec": {"mechanism": "(a scratch body of the plant)"}}
                              for i, r in enumerate(sorted(fam["by_registration"].values(),
                                                           key=lambda r: r["line"]))]}


def registry_family_findings(doc: dict, fam: dict) -> list:
    """FAM-REGISTRY: a payload of the registry carries a family, m or bar other than the parse
    gives its id; or the registry's families are not the parse's."""
    out, by = [], fam["by_registration"]
    ids = [b.get("registration") for b in doc.get("registrations", ())]
    if sorted(ids) != sorted(by):
        out.append(f"FAM-REGISTRY the registry files {ids}; the contract registers {sorted(by)}")
    for b in doc.get("registrations", ()):
        want = by.get(b.get("registration"))
        if want is None:
            continue
        got = (b.get("family"), b.get("family_m"), exact(b.get("family_bar")))
        if got != (want["family"], want["m"], want["bar_fraction"]):
            out.append(f"FAM-REGISTRY {b['registration']}: the payload carries family "
                       f"{got[0]!r}, m {got[1]!r}, bar {b.get('family_bar')!r}; the parse gives "
                       f"{want['family']!r}, m {want['m']}, bar {want['bar']} "
                       f"({want['bar_exact']})")
    parsed = {f["family"]: f for f in fam["families"]}
    for f in doc.get("families", ()):
        want = parsed.get(f.get("family"))
        if want is None or f.get("m") != want["m"] or exact(f.get("bar")) != want["bar_fraction"] \
                or f.get("bar_exact") != want["bar_exact"] or exact(f.get("q")) != fam["q"]:
            out.append(f"FAM-REGISTRY families[]: {f.get('family')!r} is filed m {f.get('m')!r}, "
                       f"bar {f.get('bar')!r} ({f.get('bar_exact')!r}), q {f.get('q')!r}; not the "
                       f"parse's")
    if sorted(x.get("family") for x in doc.get("families", ())) != sorted(parsed):
        out.append("FAM-REGISTRY families[] does not hold the contract's three families")
    return out


def flow_findings(d, pin: str, bent) -> list:
    """The flow leg [L-0.17]: the pin bent AT ITS DOOR; `families()` — the smallest production
    function that reads it — must HALT FAMILY-BAR.  A bend that moves nothing is PIN-NOT-READ."""
    try:
        with d.bend(pin, bent):
            d.families()
    except SystemExit as e:
        return [] if "FAMILY-BAR" in str(e) else [f"PIN-FLOW-WRONG {pin}: bent at its door, the "
                                                  f"wrong thing moved — {e}"]
    return [f"PIN-NOT-READ {pin}: bent at its door, `families()` moved nothing — the function "
            f"holds a copy of the value"]


def bent_value(d, pin: str):
    v = d.pin(pin)
    if pin == PINS.FAM_Q:
        return v + v
    return (v[0], v[1], v[2] + 1, v[3])


def shadow_door():
    """A SHADOW COPY of the pin door whose `families()` holds a typed literal of EQUAL value in
    place of the pin fam.q — the planted mutation of the flow leg."""
    src = swap((ROOT / "scripts" / "tierc12_pins.py").read_text(encoding="utf-8"),
               SHADOW_OLD_T, SHADOW_NEW_T)
    p = Path(_TMP[0]) / "shadow_tierc12_pins.py"
    p.write_text(src, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("shadow_tierc12_pins", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Door(root=ROOT, main=MAIN)


def judged(real_leg):
    """A HALT of the door inside a REAL leg is that leg's FAIL, with the HALT's own text."""
    def leg():
        try:
            return real_leg()
        except SystemExit as e:
            return False, f"the pin door HALTed — {e}"
    return leg


def registry_on_file():
    return REGISTRY.read_text(encoding="utf-8") if REGISTRY.exists() else None


# ═══════════════════════════════════════════════ F-PINS
def pins_break():
    reg_sha = stamp_shas()[STAMP_SETS_T[0]]
    score_sha = stamp_shas()["scripts/tierc11_score.py"]
    nine = line_swap(35, real().prefix()["lines"][34].replace("8 consecutive", "9 consecutive"))
    return FX.plants([
        ("a map row deleted (scalp.deep_atr)", "PIN-TOTALITY",
         lambda: door_findings(scratch(edit=rows_edit(
             PINS.MAP_NAME, lambda rows: [r for r in rows if r["pin"] != "scalp.deep_atr"])))),
        ("a regex changed to capture the neighbouring number (adm.lag_cut reads q75)",
         "HALT PIN-FILED",
         lambda: [] if scratch(edit=rows_edit(PINS.MAP_NAME, one(
             "adm.lag_cut", regex=r"trailing q(\d+)"))).load() else []),
        ("a two-group row typed with a one-member type (brd.cut)", "PIN-ARITY",
         lambda: door_findings(scratch(edit=rows_edit(PINS.MAP_NAME, one(
             "brd.cut", type=["int"]))))),
        ("a map row renamed scalp.rr_min", "PIN-NAME",
         lambda: door_findings(scratch(edit=rows_edit(PINS.MAP_NAME, lambda rows: [
             {**r, "pin": "scalp.rr_min"} if r["pin"] == "rr_min" else r for r in rows])))),
        ("a registry copy whose spec text cites the file sha of TC11's REGISTRATIONS.json",
         "PIN-CENSUS-SHA",
         lambda: census_findings(real(), json.dumps(registry_doc(real().families()), default=str)
                                 + f" law_source sha256 {reg_sha}")),
        ("a registry copy citing that sha abbreviated", "PIN-CENSUS-SHA",
         lambda: census_findings(real(), f"REGISTRATIONS.json (sha `{reg_sha[:8]}…{reg_sha[60:]}`)")),
        ("a register copy pinning scripts/tierc11_score.py by its file sha", "PIN-CENSUS-SHA",
         lambda: census_findings(scratch(edit=rows_edit(PINS.REGISTER_NAME, one(
             "lineage.tierc11_score.HAIRCUT_TOL", node_sha256=score_sha))), None)),
        ("a second citation re-pointed at another number (rr_min's :100 citation reads :97)",
         "HALT PIN-ALSO",
         lambda: [] if scratch(edit=rows_edit(PINS.MAP_NAME, one("rr_min", also=[
             {"lines": [97, 97], "regex": r"else (\d+\.\d+) ATR_1h beyond"}]))).load() else []),
        ("a map row's lines moved (seed :4 -> :3-4; the value still parses)", "PIN-SLICE-SHA",
         lambda: door_findings(scratch(edit=rows_edit(PINS.MAP_NAME, one("seed", lines=[3, 4]))))),
        ("a CONTRACT_PINS.json copy with one value changed (rr_min 3/2 -> 2/1)", "HALT PIN-FILED",
         lambda: [] if scratch(edit={PINS.PINS_NAME: lambda doc: {**doc, "pins": {
             **doc["pins"], "rr_min": {**doc["pins"]["rr_min"], "value": "2/1"}}}}).load() else []),
        ("a name of record's register row deleted (traverse.4h)", "PIN-NAME",
         lambda: door_findings(scratch(edit=rows_edit(
             PINS.REGISTER_NAME, lambda rows: [r for r in rows if r["pin"] != "traverse.4h"])))),
        ("a register row of a seventh kind (brd.cut: typed)", "REGISTER-KIND",
         lambda: door_findings(scratch(edit=rows_edit(PINS.REGISTER_NAME, one(
             "brd.cut", kind="typed"))))),
        ("one classed token deleted (the prior of P-BRD-1)", "PIN-TOTALITY",
         lambda: door_findings(scratch(edit=rows_edit(
             PINS.UNPINNED_NAME, lambda toks: [t for t in toks if t["token"] != "40%"])))),
        ("a classed token of no class (0.000e+00 classed `number`)", "PIN-TOTALITY",
         lambda: door_findings(scratch(edit=rows_edit(PINS.UNPINNED_NAME, lambda toks: [
             {**t, "class": "number"} if t["token"] == "0.000e+00" else t for t in toks])))),
        ("a lineage row whose node sha is another literal's (HAIRCUT_TOL carries SUM_TOL's)",
         "LINEAGE-NODE",
         lambda: door_findings(scratch(edit=rows_edit(PINS.REGISTER_NAME, one(
             "lineage.tierc11_score.HAIRCUT_TOL",
             node_sha256=real().row("lineage.tierc11_score.SUM_TOL")["node_sha256"]))))),
        ("a contract copy reading `9 consecutive closes`, its derived file re-filed (the frozen "
         "literal still reads 8)", "PIN-EQUAL va.accept_n",
         lambda: door_findings(scratch(contract=nine, refile=True))),
        ("`import numpy` added to a copy of the pin door", "PIN-STDLIB",
         lambda: stdlib_findings("a copy of scripts/tierc12_pins.py", (
             ROOT / "scripts" / "tierc12_pins.py").read_text(encoding="utf-8") + "\nimport numpy\n")),
        ("one byte of a contract copy flipped, the STEP Q record left alone", "HALT CONTRACT-PREFIX",
         lambda: [] if PINS.Door(contract=scratch(contract=line_swap(
             1, real().prefix()["lines"][0].replace("TIER-C12", "TIER-C13"))).contract).load()
         else []),
    ])


def pins_real():
    d = real()
    reg_text = registry_on_file()
    found = (door_findings(d) + referee_findings(d) + census_findings(d, reg_text)
             + stdlib_findings("scripts/tierc12_pins.py",
                               (ROOT / "scripts" / "tierc12_pins.py").read_text(encoding="utf-8")))
    kinds = [r["kind"] for r in d.register()]
    by_door = sum(1 for r in d.register() for x in r.get("equal_to", ()) if x["by"] == "door")
    by_cons = sum(1 for r in d.register() for x in r.get("equal_to", ()) if x["by"] == "consumer")
    runs = d.digit_runs()
    n_cap = sum(1 for (line, s, e, _) in runs
                if any(cl == line and cs <= s and e <= ce
                       for rec in d.parsed().values() for _, (cl, cs, ce) in rec["spans"]))
    why = (f"{len(d.map()['rows'])} map rows re-derived from the {d.prefix()['prefix_bytes']}-byte "
           f"prefix == CONTRACT_PINS.json == the typed referee of {len(VALUES_T)} values; "
           f"{sum(len(r.get('also', ())) for r in d.map()['rows'])} second citations agree; "
           f"register {len(kinds)} rows ("
           + " · ".join(f"{k} {kinds.count(k)}" for k in KINDS_T)
           + f") == the names of record + DOOR_NAMED_T; {by_door} equalities made by the door "
             f"(node or manifest sha asserted), {by_cons} left to a consumer's gate [seam 6]; "
             f"totality: {len(runs)} digit runs over {N_LINES_T} lines = {n_cap} inside a "
             f"capture + {len(runs) - n_cap} inside the {sum(CLASS_COUNTS_T.values())} classed "
             f"tokens, none twice, none unaccounted; census shas of {len(STAMP_SETS_T)} stamp-set "
             f"paths in no register row; registry text: "
           + ("on file, carries none" if reg_text is not None
              else "NOT ON FILE — the registry clause asserts nothing at this run")
           + "; the door imports the standard library only")
    return (not found), (why if not found else f"{len(found)} finding(s): " + " | ".join(found))


# ═══════════════════════════════════════════════ F-VETO
AM_PLANT_T = ("\n---\n\n## AM-2 · 2026-10-10 (~12:00Z) · L-G.12 · operator veto \"breadth\"\n\n"
              "**Text amended.** The breadth cut.\n\n**Amended to.**\nPIN brd.cut := 3 5\n\n"
              "**Reason.** A veto.\n\n**Redone.** Stage G.\n")
AM_QUOTED_T = AM_PLANT_T.replace("**Reason.** A veto.",
                                 "**Reason.** operator, 2026-10-10: \"breadth — make it 3 of 5\"")


def veto_break():
    return FX.plants([
        ("a register copy with the va.sfp_k row's veto cleared", "VETO-ROWS \"sfp-k\"",
         lambda: veto_findings(scratch(edit=rows_edit(PINS.REGISTER_NAME, one(
             "va.sfp_k", veto=None))))),
        ("a register copy with rr-min on a second row (scalp.deep_atr)", "VETO-ROWS \"rr-min\"",
         lambda: veto_findings(scratch(edit=rows_edit(PINS.REGISTER_NAME, one(
             "scalp.deep_atr", veto="rr-min"))))),
        ("a register copy lacking the ruling.1w row", "VETO-NO-ROW \"1w\"",
         lambda: veto_findings(scratch(edit=rows_edit(
             PINS.REGISTER_NAME, lambda rows: [r for r in rows if r["pin"] != "ruling.1w"])))),
        ("a scratch amendment changing brd.cut with no quoted operator words", "VETO-AMENDMENT",
         lambda: veto_findings(scratch(amendment=AM_PLANT_T))),
        ("a scratch amendment changing scalp.deep_atr (a pin no veto token names)",
         "VETO-AMENDMENT",
         lambda: veto_findings(scratch(amendment=AM_QUOTED_T.replace(
             "PIN brd.cut := 3 5", "PIN scalp.deep_atr := 0.10")))),
        ("a contract copy whose VETOES line reads \"sfp-k\" (4) while the stage line reads K=3",
         "HALT PIN-ALSO",
         lambda: veto_findings(scratch(contract=lambda t: swap(t, '"sfp-k" (3)', '"sfp-k" (4)')))),
        ("a map copy whose va.nest_frac row holds no second citation", "VETO-VALUE \"nest\"",
         lambda: veto_findings(scratch(edit=rows_edit(PINS.MAP_NAME, one(
             "va.nest_frac", also=None))))),
    ])


def veto_real():
    d = real()
    found = veto_findings(d)
    rows = d.veto_rows()
    ctl = scratch(amendment=AM_QUOTED_T)
    ctl_found = veto_findings(ctl)
    if ctl_found or ctl.pin("brd.cut") != (3, 5) or d.pin("brd.cut") != tuple(VALUES_T["brd.cut"]):
        found.append(f"VETO-CONTROL a scratch amendment with the basis `operator veto "
                     f"\"breadth\"` and a quoted operator line must be GREEN and be READ by the "
                     f"door: findings {ctl_found}, brd.cut {ctl.pin('brd.cut')!r}")
    why = (f"{len(VETO_TOKENS_T)} tokens parsed from the VETOES line, each naming exactly "
           f"VETO_ROWS_T's register rows: "
           + " · ".join(f"\"{t}\" -> {', '.join(rows[t])}" for t, _ in VETO_TOKENS_T)
           + f"; the {sum(1 for _, v in VETO_TOKENS_T if v)} parenthesised values each parse "
             f"equal to their stage-text citation (second citations of the map); "
             f"{len(d.amendment_sections())} amendment(s) on file, "
             f"{sum(len(s['pins']) for s in d.amendment_sections())} changing a pin; control "
             f"GREEN: a quoted operator veto \"breadth\" is read by the door as brd.cut = (3, 5), "
             f"the filed contract value {d.pin('brd.cut')} untouched")
    return (not found), (why if not found else f"{len(found)} finding(s): " + " | ".join(found))


# ═══════════════════════════════════════════════ F-FAM-PINS
def fam_break():
    lines = real().prefix()["lines"]
    base = json.loads(registry_on_file()) if REGISTRY.exists() else registry_doc(real().families())

    def scalper_at_admission_bar():
        doc = json.loads(json.dumps(base, default=str))
        for b in doc["registrations"]:
            if b["registration"] == "P-SCALP-3":
                b["family_bar"] = "0.05"
        return registry_family_findings(doc, real().families())

    return FX.plants([
        ("a header copy reading a different bar (STAGE G: bar 0.10)", "HALT FAMILY-BAR",
         lambda: [] if scratch(contract=line_swap(52, lines[51].replace(
             "bar 0.05", "bar 0.10"))).families() else []),
        ("a header copy with a second registration id under SCALPER (:84 reads P-SCALP-4 [10%])",
         "HALT FAMILY-M-COUNT",
         lambda: [] if scratch(contract=line_swap(
             84, " P-SCALP-4 [10%] A SECOND REGISTRATION ID UNDER THE SCALPER HEADER")).families()
         else []),
        ("a registry copy whose SCALPER payload carries the ADMISSION bar", "FAM-REGISTRY P-SCALP-3",
         scalper_at_admission_bar),
        ("a contract copy whose third family is renamed SCALPING, its derived file re-filed",
         "FAM-REFEREE",
         lambda: fam_referee_findings(scratch(contract=line_swap(82, lines[81].replace(
             "SCALPER FAMILY", "SCALPING FAMILY")), refile=True).families())),
        ("a shadow copy of the pin door whose families() holds a typed 1/10 in place of the pin "
         "fam.q (equal value)", "PIN-NOT-READ fam.q",
         lambda: (lambda sd: flow_findings(sd, "fam.q", bent_value(sd, "fam.q")))(shadow_door())),
    ])


def fam_real():
    d = real()
    fam = d.families()
    found = fam_referee_findings(fam)
    reg_text = registry_on_file()
    if reg_text is not None:
        found += registry_family_findings(json.loads(reg_text), fam)
    for pin in FLOW_PINS_T:
        f = flow_findings(d, pin, bent_value(d, pin))
        found += f
        if not f:
            FX.say(d.flow_line(pin))
    if d.families()["q"] != fam["q"] or d.pin("fam.q") != Fraction(Q_T):
        found.append("FAM-REFEREE a bend outlived its block")
    why = ("q = " + fam["q_text"] + f" ({fam['q_exact']}) from contract :{fam['q_line']}; "
           + " · ".join(f"STAGE {f['stage']} {f['family']} (:{f['header_line']}) m = {f['m']}, "
                        f"bar {f['bar']} = {f['bar_exact']} == q ÷ m, ids "
                        f"{' '.join(f['registrations'])}" for f in fam["families"])
           + f" == the typed referee; {len(FLOW_PINS_T)} pins bent at the door, each HALTs "
             f"FAMILY-BAR; registry: "
           + (f"on file — {len(json.loads(reg_text).get('registrations', ()))} payloads carry "
              f"the parse's family, m and bar" if reg_text is not None
              else "NOT ON FILE — the registry clause asserts nothing at this run"))
    return (not found), (why if not found else f"{len(found)} finding(s): " + " | ".join(found))


FIXTURES = [
    ("F-PINS", "the contract pin door, its map, its derived file, the register and the totality",
     "the door's re-derivation differs from CONTRACT_PINS.json; an `also` citation disagrees; a "
     "row's type arity differs from its regex's group count; a map row's slice sha moved; a map "
     "row's pin is not a name of record, a name of record has no register row, or a register "
     "row's kind is outside the six; a digit run of the prefix is unaccounted; a register row or "
     "the registry's text carries the census sha, whole or abbreviated, of a path the tc11-stamp "
     "moves; a lineage node sha or a door-held equality fails; the contract is not the STEP Q "
     "prefix; the door imports anything outside the stdlib — each planted in a scratch copy of "
     "production and caught by its named detector",
     "any of those conditions holds on the filed files (CONTRACT_PIN_MAP.json, CONTRACT_PINS.json, "
     "PIN_REGISTER.json, CONTRACT_TOKENS_UNPINNED.json, scripts/tierc12_pins.py), or the door's "
     "derivation differs from this suite's typed referee",
     pins_break, judged(pins_real)),
    ("F-VETO", "the veto map: each token of the VETOES line and its register rows",
     "the set of register rows carrying a token differs from VETO_ROWS_T[token]; a token of the "
     "VETOES line has no row; a token's parenthesised value does not parse equal to its "
     "stage-text citation; an amendment that changes a pin names no operator quote",
     "any of those conditions holds on the filed register, map and LEANS_AMENDMENTS.md; or a "
     "quoted operator veto filed in a scratch amendment is not read by the door (the control)",
     veto_break, judged(veto_real)),
    ("F-FAM-PINS", "the families parsed at the registration stage (not one of F-FAM's blocks)",
     "the door's parsed (family, m, bar, ids) differs from the typed referee table; a header's "
     "bar is not q ÷ m; the ids under a header do not number m; a payload of the registry "
     "carries a family, m or bar other than the parse gives its id; a family pin bent at the "
     "door moves nothing (PIN-NOT-READ)",
     "any of those conditions holds on the contract prefix, the filed registry (when on file) "
     "or the door's families(); each family pin's bend prints its [FLOW] line",
     fam_break, judged(fam_real)),
]


def main(argv) -> int:
    root = Path(FX.opt(argv, "--root=", str(T12 / "pins")))
    tmp = tempfile.mkdtemp(prefix="tierc12_pins_fx_")
    _TMP[:] = [tmp]
    typed = [
        f"SEED_T {SEED_T} · N_LINES_T {N_LINES_T} · KINDS_T {list(KINDS_T)} · TYPES_T {list(TYPES_T)}",
        f"NAMES_T {len(NAMES_T)} names of record ({sum(1 for v in NAMES_T.values() if v == 'contract')} "
        f"of kind contract; <stage letter> {list(STAGE_LETTERS_T)}, va.lookback.<lens> "
        f"{list(VA_LENSES_T)}, traverse.<lens> {list(TRAVERSE_LENSES_T)}, <VENUE> read from "
        f"{VENUE_PROBE}) · DOOR_NAMED_T {len(DOOR_NAMED_T)} rows the door names",
        f"VALUES_T {len(VALUES_T)} contract pins · Q_T {Q_T} · FAMILIES_T "
        + "; ".join(f"{s} {n} m={m} bar {b} {' '.join(i)}" for s, n, m, b, i in FAMILIES_T),
        "VETO_ROWS_T " + "; ".join(f"\"{t}\" -> {', '.join(VETO_ROWS_T[t])}" for t, _ in VETO_TOKENS_T),
        "CLASS_COUNTS_T " + " · ".join(f"{k} {v}" for k, v in sorted(CLASS_COUNTS_T.items())),
        f"STAMP_SETS_T {list(STAMP_SETS_T)} · ABBREV_MIN_T {ABBREV_MIN_T}",
        f"FLOW_PINS_T {list(FLOW_PINS_T)} · n = 1 bend per pin (no seeded sample: the function "
        f"read is `families()` over the whole prefix)",
        f"FIXTURE_NAMES_T {len(FIXTURE_NAMES_T)} names · RECORDS_T {len(RECORDS_T)} record ids",
    ]
    try:
        return FX.run_suite(args=argv, root=root, transcript=TRANSCRIPT, banner=BANNER,
                            seed=SEED_T, fixtures=FIXTURES, typed=typed)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
