#!/usr/bin/env python
"""TIER-C10 · STAGE B · THE SCORING DRIVER (B-CORE, then B-5M).

RATIFIED operator 2026-09-21 (contract TIER-C10) + 2026-09-22 (RESUME-AND-
FINISH, exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md).  Drafted APOLLO,
executed HEPHAESTUS; seed 20260921.  The six registrations were FILED at
371123f (registry of record: 6 lines, head 7621a857…, pinned TRACKED in
research_outputs/tierc10/REGISTRY_PIN.json).  THE FILED TEXTS ARE LAW.

WHAT THIS FILE DOES
  For each of the six registrations, IN FILED ORDER, and for every FILED arm
  of each, IN FILED ORDER, it rides the arm to its Book through exactly the
  door the registration names, and then (by mode):

    --dry-run  (the DEFAULT)   prints, per arm, the registration, the arm, the
               scored slot, the panel, the era and its window, the ruler, the
               base, the campaign count PER DECLARED ASSET (zeros printed), the
               book sha (`TP._book_sha`) and the base sha — and runs the
               binding checks `TP.score` runs AHEAD OF ITS RESULT MARKER
               (`TP._bind_arm` itself, the two-sample premise on campaign KEYS,
               stray symbols, finiteness, the era against every campaign) —
               WITHOUT calling `TP.score`, WITHOUT writing a .scored.json and
               WITHOUT computing any outcome.  Beside each registration it
               prints the outcome-free facts its filed text requires on the
               row (see BESIDE, below).  A HALT from any door is printed
               VERBATIM and the next arm is ridden.
    --score --only REG...      calls `TP.score` on every arm of each named
               registration (the scored arm and every Tier-E arm), files the
               rows at research_outputs/tierc10/scores/<REG>.rows.json and
               prints them.  Re-running reproduces: `TP.score` binds the
               inputs of an arm's FIRST score (`.scored.json`) and HALTs on a
               different book or seed — that is its law, and this driver does
               not guard around it.  A rows file that already exists and
               differs from the re-score's bytes is REFUSED (never
               overwritten): a re-score must reproduce the first.  A SCORED
               arm's HALT is recorded verbatim with what the filed text
               prescribes for it, and stops that registration unless
               --continue-after-scored-halt (the operator's word).
    --finish                   only when ALL SIX registrations carry exactly
               one canonical scored row, calls `TP.finish_family` (one fixed
               bar q/m at the DECLARED m = 6) and files scores/FAMILY.json.
               A registration whose SCORED arm HALTed (recorded verbatim in
               its rows file) finishes without a row ONLY when the operator
               names it: --allow-halted-slot REG.
    --stage B-CORE             = --score --only the five non-S1 registrations
                                 (P-GEN-1, P-SPR-2, P-BE-1, P-TRG-2, P-BRK-I1).
    --stage B-5M               = --score --only P-BRK-S1, then --finish.
    --expect D.json            (score) refuse any Book whose sha is not the
                               one a reviewed dry-run (--json-out) printed.

WHERE EVERY ARM COMES FROM
  The arms are read from the FILED registration JSON
  (research_outputs/tierc10/registrations/<REG>.json · book_spec.arms) —
  arm name, panel, ruler, base, era, scored_in_family, runner, lanes,
  loao_line, and for a `run_cell_n` arm the `ride` (card + roles, every
  field) — and held against the same record read THROUGH the door
  (`TP.require_registered` with the text of record from
  REGISTRATION_TEXTS.json and the head pinned in REGISTRY_PIN.json).  No arm
  parameter is typed here.  What the filed book spec does NOT carry is named
  and derived by rule, each rule checked against the filed TEXT:
    · a `run_cell_n` arm's card and roles are REBUILT from the filed `ride`
      and must round-trip `TP.ride_spec` to the filed dict byte for byte;
    · an external arm on lanes {card} (P-BE-1) rides `tierc10_lanes.CARD_BE1`
      with `be_floor_after_r` read from the ARM NAME ("be-floor-<pin>R") and
      that pin must be quoted in the filed text ("be_floor_after_r = <pin>");
      on lanes {spring} it rides `CARD_SPR2` (P-SPR-2 §5 names it); on lanes
      {card, spring} it rides CARD_SPR2 with lane "union" (P-SPR-2 §6 ARM 4:
      "lane union (card + spring)");
    · a BRK arm rides `tierc10_brk.ready_run(lane, role)`, the role found by
      the arm's filed NAME in `tierc10_brk.FILED_ARMS` (which that module
      itself holds against the filing on every call);
    · a "card-v6" base is `TP.run_cell_n(CONTROL_CARD, V6_ROLES, panel,
      lo, hi)` over the arm's OWN era window (P-BE-1 §8(9)) — never a
      full-corridor control filtered afterwards.

THE DOOR BEFORE THE BARS
  Every arm's door opens before one bar of it is read: `TP.require_arm`
  (external) or `TP.require_registered` + the arm lookup (`run_cell_n`) is
  called FIRST, then `corridor_era`, then any signal is built, then the
  runner — whose own first statement is the same door again.

BESIDE THE ROW — never inside the verdict
  P-GEN-1   the LOAO line printed twice (arm 1 all admitted · arm 3
            never-touched), raw + equal-risk co-headlines (TP.score), the
            per-asset rows (TP.headline_n, zeros included), the HAIRCUT TWIN
            (tierc10_data.haircut_twin_net_r, as filed) on every row with a
            sign-disagreement flag; the §5 assertion that arm 3 is exactly
            the three-symbol subset of arm 1 (checked in the dry-run, on keys
            and on the book sha).
  P-SPR-2   the signals handed in per asset and the refusals COUNTED
            (position_open / degenerate_R / no_struct_anchor) [§5].
  P-BE-1    F-C10-BE's status, RE-DERIVED from the scored arm's own ridden
            Book by `tierc10_lanes.be_latch_census` and held byte-for-byte
            against the filed lanes/BE_LATCH_CENSUS.json (NOT RUN per §9);
            every external arm prints the card fields it rode (§11: "the card
            fields the runner must print on the row").
  P-TRG-2   the ride differs from CONTROL_RIDE in EXACTLY the two trigger
            fields (§2), and the roles are a member of tierc9.SWEEP_CELLS.
  P-BRK-*   the SEALED `tierc10_brk.brk_rows` block: its own-era
            height-vs-toll verdict (READ from [Q-R3]), the Tier-E other
            anchor, the 17-asset view, the toll print and TOLL_ACCOUNTING —
            and every Book's two shas held against BRK_READY_BOOKS.json.
  EVERY ROW the haircut twin and the per-asset rows (score mode only).

WHAT THIS FILE NEVER DOES
  It never files, amends or re-files a registration, never writes
  REGISTRY.jsonl or REGISTRY_PIN.json, never refits a pin, and in --dry-run
  never calls TP.score / TP.finish_family / TP._mark_scored, never writes a
  .scored.json and never computes an outcome sum.  It reads the frozen
  snapshot only (NAIAD_CACHE_DIR exported BEFORE python starts; the live
  cache is refused by `TP.substrate`).

Run:
  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 \\
         PYTHONDONTWRITEBYTECODE=1
  ~/venvs/naiad/bin/python scripts/tierc10_score.py            # --dry-run
  ~/venvs/naiad/bin/python scripts/tierc10_score.py --dry-run --out T.txt \\
          --json-out D.json
  ~/venvs/naiad/bin/python scripts/tierc10_score.py --stage B-CORE \\
          --expect D.json                                      # IRREVERSIBLE
"""
from __future__ import annotations

import argparse
import ast
import dataclasses
import hashlib
import io
import json
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc10_panel as TP                                         # noqa: E402
import tierc10_lanes as LN                                         # noqa: E402
import tierc10_brk as B                                            # noqa: E402
import tierc10_data as D                                           # noqa: E402
import tierc9 as T9                                                # noqa: E402
import tierc8 as T8                                                # noqa: E402
import tierc7 as T7                                                # noqa: E402

iso = TP.iso

# ══════════════════════════════════════════════════════ THE RECORD'S PATHS
OUT = TP.OUT
REG_DIR = TP.REG_DIR
SCORES = OUT / "scores"
REGISTRY_PIN_PATH = OUT / "REGISTRY_PIN.json"
REGISTRATION_TEXTS_PATH = OUT / "REGISTRATION_TEXTS.json"
BE_LATCH_CENSUS_PATH = OUT / "lanes" / "BE_LATCH_CENSUS.json"
BRK_READY_BOOKS_PATH = OUT / "brk" / "BRK_READY_BOOKS.json"
FAMILY_NAME = "FAMILY.json"
ROWS_SUFFIX = ".rows.json"

S1_REG = "P-BRK-S1"
STAGE_B_5M = (S1_REG,)
STAGE_NAMES = ("B-CORE", "B-5M")

# the lanes a runner EMITS -> the module whose door rides it (read off the
# filed arm's `lanes`, never off the registration id)
LANES_MODULE_LANES = {"card", "spring"}
BRK_LANES = {B.LANE_S1, B.LANE_I1}

# the tokens an outcome-free printout may never carry (F-SC-NOSCORE scans
# the dry-run transcript for them; a sabotage printing a sum goes RED)
OUTCOME_TOKENS = ("net_r_sum", "net_r:", "expectancy", "ci_lo", "ci_hi",
                  "p_one_sided", "verdict:", "gross_r_sum", "net_r_twin",
                  "mean net", "twin_mean")

DRYRUN_LAW = (
    "DRY-RUN — NOT A RESULT. Every arm is ridden to its Book through the "
    "door its registration names and bound as TP.score would bind it AHEAD "
    "of its result marker; TP.score, TP.finish_family and TP._mark_scored "
    "are never called, no .scored.json is written, and no outcome (no sum, "
    "no mean, no CI, no p) is computed or printed. The campaign counts are "
    "a SCHEDULE, not an outcome — but one campaign rides per asset at a "
    "time, so a count is a function of the exits, and it is printed as such "
    "[tierc10_brk B12].")


# WHAT A FILED TEXT PRESCRIBES WHEN A DOOR HALTS — quoted, and each quote is
# VERIFIED against the text of record (whitespace-normalised) every time it
# is printed; a quote the text does not carry HALTS the print.  Keyed by
# (registration, the HALT's own words).
TEXT_PRESCRIBES = {
    ("P-BE-1", "the commissioned two-sample ruler's premise failed"): (
        "If it does not move, this registration does NOT quietly become the "
        "narrower paired row — it HALTs. That HALT is part of the claim, and "
        "it is why the ruler is registered rather than left to the scorer.",
        "If A1's two-sample premise fails and A1 HALTs, there is no "
        "report-only row on the same population to read instead; a new id "
        "must be filed under `set_change` and the reason disclosed."),
}


def _norm(s: str) -> str:
    return " ".join((s or "").split())


def prescribed(rid: str, halt: str, text: str) -> list:
    """The filed text's own words for this HALT — [] when it names none.
    HALTS if a quote on file here is NOT in the text of record."""
    out = []
    for (r, words), quotes in TEXT_PRESCRIBES.items():
        if r != rid or words not in (halt or ""):
            continue
        for q in quotes:
            if _norm(q) not in _norm(text):
                raise SystemExit(f"HALT: the quote {q[:60]!r}… is not in "
                                 f"{rid}'s text of record.")
            out.append(q)
    return out


def _halt_text(e: BaseException) -> str:
    c = getattr(e, "code", None)
    return str(c if c is not None else e)


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    return sha256_bytes(Path(p).read_bytes())


# ══════════════════════════════════════════════ 1 · THE RECORD, READ WHOLE
def load_record(reg_dir: Path | None = None,
                pin_path: Path | None = None,
                texts_path: Path | None = None) -> dict:
    """THE REGISTRY OF RECORD, READ AND HELD AGAINST ITS WITNESS.

    The six filings are read THROUGH the door (`TP.require_registered`, text
    of record, pinned head) AND raw from their JSON files, and the two must
    carry the identical book spec.  The registry's length, head and order
    must equal REGISTRY_PIN.json's; every registration's seq, payload sha and
    text sha must equal its pin.  Reads no bar.

    HALTS IF: the chain is broken; the registry is not the pinned one (length,
    head, order); a filing does not verify, is not the pinned bytes, or its
    raw arms differ from the door's; a text of record is missing."""
    reg_dir = Path(reg_dir) if reg_dir else REG_DIR
    pin = json.loads(Path(pin_path or REGISTRY_PIN_PATH).read_text("utf-8"))
    texts = json.loads(Path(texts_path or REGISTRATION_TEXTS_PATH)
                       .read_text("utf-8"))
    lines = TP._registry_lines(reg_dir)
    ok, why = TP._chain_ok(lines)
    if not ok:
        raise SystemExit(f"HALT: {reg_dir / TP.REGISTRY} — {why}.")
    order = [ln["registration"] for ln in lines]
    bad = pin_disagreements(lines, pin)
    if bad:
        raise SystemExit("HALT: the registry under " + str(reg_dir)
                         + " is NOT the registry of record: "
                         + " | ".join(bad))
    regs = {}
    for ln in lines:
        rid = ln["registration"]
        pr = pin["registrations"].get(rid) or {}
        t = (texts.get(rid) or {}).get("text")
        if not isinstance(t, str) or not t.strip():
            raise SystemExit(f"HALT: no text of record for {rid}.")
        head = (int(pr["registry_len"]), str(pr["registry_head"]))
        rec = TP.require_registered(rid, t, root=reg_dir,
                                    head_of_record=head)
        raw = json.loads((reg_dir / f"{rid}.json").read_text("utf-8"))
        chk = filing_disagreements(rec, raw, pr)
        if chk:
            raise SystemExit(f"HALT: {rid} is not the pinned filing: "
                             + " | ".join(chk))
        regs[rid] = {"rec": rec, "text": t, "head": head,
                     "arms": list(raw["book_spec"]["arms"]),
                     "arm_spec_calls": list((texts.get(rid) or {})
                                            .get("arm_spec_calls") or []),
                     "path": reg_dir / f"{rid}.json"}
    return {"pin": pin, "order": order, "regs": regs, "reg_dir": reg_dir,
            "registry_len": len(lines),
            "registry_head": lines[-1]["line_sha256"] if lines else None}


def pin_disagreements(lines: list, pin: dict) -> list:
    """Where the registry's lines disagree with REGISTRY_PIN.json: length,
    head, order of filing, family m.  [] when they agree."""
    order = [ln["registration"] for ln in lines]
    bad = []
    if len(lines) != int(pin["registry_len"]):
        bad.append(f"registry_len {len(lines)} != pinned {pin['registry_len']}")
    if (lines[-1]["line_sha256"] if lines else "GENESIS") \
            != pin["registry_head"]:
        bad.append("registry head != pinned head")
    if order != list(pin["order_of_filing"]):
        bad.append(f"order {order} != pinned {pin['order_of_filing']}")
    if int(pin["family_m"]) != TP.FAMILY_M:
        bad.append(f"pinned m {pin['family_m']} != TP.FAMILY_M {TP.FAMILY_M}")
    return bad


def filing_disagreements(rec: dict, raw: dict, pr: dict) -> list:
    """Where one filing (read through the door, and raw) disagrees with its
    pin: seq, payload sha, text sha, and the raw book spec vs the door's."""
    chk = []
    if rec["seq"] != int(pr.get("seq", -1)):
        chk.append(f"seq {rec['seq']} != pinned {pr.get('seq')}")
    if rec["sha256"] != pr.get("sha256"):
        chk.append("payload sha != pinned")
    if rec["text_sha256"] != pr.get("text_sha256"):
        chk.append("text sha != pinned")
    if json.dumps(raw.get("book_spec"), sort_keys=True) \
            != json.dumps(rec["book_spec"], sort_keys=True):
        chk.append("raw book_spec != the door's")
    return chk


def scored_json_on_file(reg_dir: Path | None = None) -> list:
    reg_dir = Path(reg_dir) if reg_dir else REG_DIR
    return sorted(p.name for p in reg_dir.glob("*.scored.json"))


# ══════════════════════════════ 2 · THE CARD OF AN ARM — REBUILT, NOT TYPED
def _parse_field(v: str):
    """A `ride_spec` field value (a repr string) back to its value."""
    if v in ("inf", "-inf", "nan"):
        return float(v)
    return ast.literal_eval(v)


_CLASS_OF = {"tierc8.Card": T8.Card, "tierc9.Roles": T9.Roles}


def _name_in_call(call: str, kind: str) -> str | None:
    """The FREE `name` a text's arm_spec call gave its card / roles — free
    because `ride_spec` drops it; cosmetic, never compared."""
    m = re.search(kind + r"\(name=\"([^\"]+)\"", call or "")
    if m:
        return m.group(1)
    if kind.endswith("Card") and "CONTROL_CARD" in (call or ""):
        return TP.CONTROL_CARD.name
    if kind.endswith("Roles") and "V6_ROLES" in (call or ""):
        return T9.V6_ROLES.name
    return None


def card_roles_of_ride(ride: dict, arm_call: str = "") -> tuple:
    """REBUILD a `run_cell_n` arm's card and roles FROM ITS FILED `ride` —
    class and every field — and prove the rebuild: `TP.ride_spec` of what was
    built must equal the filed dict byte for byte, so nothing but the filing
    decides what rides.  HALTS on an unknown class or any difference."""
    cc, rc = ride.get("card_class"), ride.get("roles_class")
    if cc not in _CLASS_OF or rc not in _CLASS_OF or cc == rc:
        raise SystemExit(f"HALT: a filed ride names classes {cc!r} / {rc!r}; "
                         f"this driver rebuilds {sorted(_CLASS_OF)} only.")
    try:
        cf = {k: _parse_field(v) for k, v in ride["card_fields"].items()}
        rf = {k: _parse_field(v) for k, v in ride["roles_fields"].items()}
        card = _CLASS_OF[cc](name=_name_in_call(arm_call, "Card")
                             or "tc10-score-card", **cf)
        roles = _CLASS_OF[rc](name=_name_in_call(arm_call, "Roles")
                              or "tc10-score-roles", **rf)
    except (TypeError, ValueError, SyntaxError) as e:
        raise SystemExit(f"HALT: the filed ride does not rebuild into "
                         f"{cc} / {rc}: {e!r}")
    got = TP.ride_spec(card, roles)
    if json.dumps(got, sort_keys=True) != json.dumps(ride, sort_keys=True):
        raise SystemExit(
            "HALT: the card/roles rebuilt from the filed ride do NOT "
            "round-trip it: " + "; ".join(TP._spec_diff(ride, got)[:4]))
    return card, roles


BE_PIN_RE = re.compile(r"be-floor-(\d+(?:\.\d+)?)R\b")


def be_pin_of_arm(arm: str, text: str) -> float:
    """P-BE-1's floor pin, READ FROM THE FILED ARM NAME and HELD AGAINST THE
    FILED TEXT: "be-floor-2R …" -> 2.0, and the text must quote
    "be_floor_after_r = 2.0" (the external book spec carries no card — §11
    says the pin is witnessed by the arm's name and the text).  HALTS if the
    name carries no pin or the text does not quote it."""
    m = BE_PIN_RE.search(arm or "")
    if not m:
        raise SystemExit(f"HALT: external card-lane arm {arm!r} names no "
                         f"'be-floor-<pin>R' — this driver will not guess "
                         f"its card.")
    pin = float(m.group(1))
    quote = f"be_floor_after_r = {pin:.1f}"
    if quote not in (text or ""):
        raise SystemExit(f"HALT: arm {arm!r} names the pin {pin}, and the "
                         f"filed text does not quote {quote!r}.")
    return pin


def lanes_card(arm: dict, text: str):
    """The tierc10_lanes card an EXTERNAL lanes arm rides, by rule off its
    FILED lanes (and, for the card lane, its filed name):
        {spring}         -> CARD_SPR2 (P-SPR-2 §5)
        {card, spring}   -> CARD_SPR2 with lane "union" (P-SPR-2 §6 ARM 4)
        {card}           -> CARD_BE1 at the arm's own floor pin (P-BE-1 §11)
    HALTS on any other lane set."""
    ls = tuple(sorted(arm["lanes"]))
    if ls == ("spring",):
        return LN.CARD_SPR2
    if ls == ("card", "spring"):
        return dataclasses.replace(LN.CARD_SPR2, name="tc10-spring-union",
                                   lane="union")
    if ls == ("card",):
        pin = be_pin_of_arm(arm["arm"], text)
        if float(LN.CARD_BE1.be_floor_after_r) == pin:
            return LN.CARD_BE1
        return dataclasses.replace(LN.CARD_BE1,
                                   name=f"tc10-be-floor-{pin:g}R",
                                   be_floor_after_r=pin)
    raise SystemExit(f"HALT: no lanes card for lanes {list(ls)}.")


def card_fields_printable(card) -> dict:
    return {f.name: repr(getattr(card, f.name))
            for f in dataclasses.fields(card)}


def brk_role_of(arm: dict) -> tuple:
    """(lane, role) of a filed BRK arm — the role found by the arm's FILED
    NAME in tierc10_brk.FILED_ARMS.  HALTS if the filed name is not there."""
    ls = list(arm["lanes"])
    if len(ls) != 1 or ls[0] not in BRK_LANES:
        raise SystemExit(f"HALT: BRK arm {arm['arm']!r} lanes {ls}.")
    lane = ls[0]
    hit = [r for r, n in B.FILED_ARMS[lane].items() if n == arm["arm"]]
    if len(hit) != 1:
        raise SystemExit(f"HALT: filed BRK arm {arm['arm']!r} is not in "
                         f"tierc10_brk.FILED_ARMS[{lane!r}].")
    return lane, hit[0]


def door_kind(arm: dict) -> str:
    """run_cell_n | lanes | brk — from the FILED runner and lanes."""
    if arm["runner"] == "run_cell_n":
        return "run_cell_n"
    ls = set(arm["lanes"])
    if ls <= LANES_MODULE_LANES:
        return "lanes"
    if ls <= BRK_LANES:
        return "brk"
    raise SystemExit(f"HALT: no door for external arm {arm['arm']!r} lanes "
                     f"{sorted(ls)}.")


# ════════════════════════════════════════ 3 · THE RIDE — DOOR, THEN BARS
def open_door(reg: dict, rid: str, arm: dict) -> dict:
    """THE ARM'S DOOR, BEFORE ONE OF ITS BARS IS READ.  External arms walk
    `TP.require_arm` (text of record, pinned head, the arm, the panel, the
    lanes); a `run_cell_n` arm walks `TP.require_registered` and must be
    filed for `run_cell_n` on exactly its panel — `require_arm` itself
    refuses a run_cell_n arm, which is ridden by `run_cell_n`'s own door."""
    if arm["runner"] == "external":
        return TP.require_arm(rid, reg["text"], arm["arm"], arm["panel"],
                              lanes=tuple(arm["lanes"]),
                              head_of_record=reg["head"])
    rec = TP.require_registered(rid, reg["text"],
                                head_of_record=reg["head"])
    hit = [a for a in rec["book_spec"]["arms"]
           if a["arm"] == arm["arm"] and a["runner"] == "run_cell_n"
           and list(a["panel"]) == list(arm["panel"])]
    if len(hit) != 1:
        raise SystemExit(f"HALT: {rid} files no run_cell_n arm "
                         f"{arm['arm']!r} on {arm.get('panel_name')}.")
    return {"runner": "run_cell_n", "registration": rid, "arm": arm["arm"],
            "era": hit[0]["era"], "registration_sha256": rec["sha256"],
            **rec["_head"]}


_BASES: dict = {}


def control_base(panel: tuple, lo: int, hi: int):
    """THE "card-v6" BASE — the known control, ridden by `TP.run_cell_n` on
    the arm's panel over the arm's OWN window (P-BE-1 §8(9)).  Memoised on
    (panel, window): the same Book object is the same base."""
    k = (tuple(panel), int(lo), int(hi))
    if k not in _BASES:
        _BASES[k] = TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, panel, lo, hi)
    return _BASES[k]


_SPRINGS: dict = {}


def spring_window(sym: str, lo_ms: int, hi_ms: int, roles) -> tuple:
    """replay10's own window law, re-pointed: the 4h frame's index range of
    [lo_ms, hi_ms], its start raised to the roles' warm-up floor."""
    f = T9.frame(sym)["f"]
    lo_i, hi_i = T7._idx_range(f.open_ms, lo_ms, hi_ms)
    return max(lo_i, roles.floor_bars), hi_i


def springs_for(sym: str, lo_ms: int, hi_ms: int, roles) -> list:
    """THE SPRING SIGNALS HANDED IN for one asset and one ride window — the
    census's deviation-confirms at the FROZEN scale, re-indexed onto the
    ride's frame BY STAMP (`signals_on_frame`), kept iff their harden bar
    (`reclaim_i`) is inside replay10's own window.  Called only AFTER the
    arm's door has opened.  Memoised per asset (the whole-tape list)."""
    if sym not in _SPRINGS:
        raw = LN.spring_signals_from_census(sym, "4h", LN.FROZEN_SCALE)
        _SPRINGS[sym] = LN.signals_on_frame(T9.frame(sym)["f"], raw)
    lo_i, hi_i = spring_window(sym, lo_ms, hi_ms, roles)
    return [s for s in _SPRINGS[sym] if lo_i <= int(s.reclaim_i) <= hi_i]


def ride_arm(reg: dict, rid: str, arm: dict, brk_cache: dict) -> dict:
    """ONE FILED ARM, RIDDEN TO ITS BOOK THROUGH ITS REGISTRATION'S DOOR.
    Returns {book, base, window, era_meta, door, card, run, springs}."""
    kind = door_kind(arm)
    gate = open_door(reg, rid, arm)                  # THE DOOR — FIRST
    panel = tuple(arm["panel"])
    out = {"door": kind, "gate": gate, "card": None, "run": None,
           "springs": None, "base": None}
    if kind == "brk":
        lane, role = brk_role_of(arm)
        run = B.ready_run(lane, role, signals=brk_cache.setdefault(lane, {}))
        book = run["book"]
        if book.spec.get("arm") != arm["arm"] \
                or book.spec.get("registration") != rid:
            raise SystemExit(f"HALT: ready_run({lane}, {role}) rode arm "
                             f"{book.spec.get('arm')!r}, not the filed "
                             f"{arm['arm']!r}.")
        lo, hi = int(run["window"][0]), int(run["window"][1])
        _lo, _hi, meta = TP.corridor_era(panel, arm["era"])
        if (lo, hi) != (_lo, _hi):
            raise SystemExit(f"HALT: {rid} {arm['arm']!r} rode window "
                             f"[{iso(lo)}, {iso(hi + 1)}), not its era's "
                             f"[{iso(_lo)}, {iso(_hi + 1)}).")
        out.update(book=book, run=run, window=(lo, hi), era_meta=meta,
                   brk=(lane, role))
    else:
        lo, hi, meta = TP.corridor_era(panel, arm["era"])
        if kind == "run_cell_n":
            call = next((c for c in reg["arm_spec_calls"]
                         if f'"{arm["arm"]}"' in c), "")
            card, roles = card_roles_of_ride(arm["ride"], call)
            book = TP.run_cell_n(card, roles, panel, lo, hi, reg_id=rid,
                                 text=reg["text"], arm=arm["arm"],
                                 head_of_record=reg["head"])
            out.update(card=card, roles=roles)
        else:
            card = lanes_card(arm, reg["text"])
            roles = T9.V6_ROLES
            spr = None
            if card.lane in ("spring", "union"):
                spr = {s: springs_for(s, lo, hi, roles) for s in panel}
            book = LN.run_lane(card, roles, panel, lo, hi, reg_id=rid,
                               text=reg["text"], arm=arm["arm"],
                               lanes=tuple(arm["lanes"]),
                               head_of_record=reg["head"],
                               springs_by_sym=spr)
            out.update(card=card, roles=roles, springs=spr)
        out.update(book=book, window=(int(lo), int(hi)), era_meta=meta)
    if not isinstance(out["book"], TP.Book) or not out["book"].spec:
        raise SystemExit(f"HALT: {rid} {arm['arm']!r} — the door returned "
                         f"no Book.")
    if arm["base"] == "card-v6":
        out["base"] = control_base(panel, *out["window"])
    return out


# ═══════════════════════ 4 · THE BINDING — score()'s CHECKS, BEFORE ITS MARKER
def _key(t) -> tuple:
    return (str(t.symbol), str(t.lane), int(t.entry_ms))


def key_sets(book, base) -> dict:
    """The campaign-KEY relation of a book and its base — (symbol, lane,
    entry_ms), keys only: no outcome is read.  `moved` is decided by
    TP.score's OWN arithmetic (and `_rule`'s): n_pair = the book campaigns
    whose key the base holds; the set moved iff len(base) > n_pair or
    len(book) > n_pair.  The three set counts ride beside it for the eye."""
    bk = {_key(t) for t in book}
    ba = {_key(t) for t in (base or [])}
    n_pair = sum(1 for t in book if _key(t) in ba)
    return {"n_paired": len(bk & ba), "n_book_only": len(bk - ba),
            "n_base_only": len(ba - bk), "n_pair_score_law": n_pair,
            "moved": bool(len(base or []) > n_pair or len(book) > n_pair)}


def bind_check(rec: dict, arm: dict, book, base) -> dict:
    """EVERY CHECK `TP.score` RUNS AHEAD OF ITS RESULT MARKER, in its order,
    WITHOUT the marker: the ruler/base pairing, the panel, `TP._bind_arm`
    ITSELF (panel, ruler, scored slot, lanes, provenance, the base's ride,
    panel and window), the commissioned two-sample premise on campaign KEYS,
    stray symbols, non-finite net_r (a finiteness test, not a sum), and the
    era — offered, ridden and held against every campaign of book and base.
    Nothing is computed from an outcome and nothing is written.

    Returns {"ok", "halt" (verbatim or None), "checks": [...], "keys"}."""
    checks, ruler = [], arm["ruler"]
    panel = tuple(arm["panel"])

    def fail(msg):
        return {"ok": False, "halt": msg, "checks": checks,
                "keys": key_sets(book, base) if base is not None else None}
    try:
        if ruler not in TP.RULERS:
            return fail(f"HALT: unknown ruler {ruler!r}")
        if not book:
            return fail(f"HALT: {rec['registration']} — an empty book cannot "
                        f"be scored.")
        if (ruler == "vs_zero") != (base is None):
            return fail(f"HALT: ruler {ruler!r} and base "
                        f"{'None' if base is None else 'book'} disagree.")
        TP._check_panel(panel)
        filed = TP._bind_arm(rec, arm["arm"], panel, ruler,
                             bool(arm["scored_in_family"]), book, base)
        checks.append("TP._bind_arm: the offered book IS the filed arm "
                      "(panel, ruler, scored slot, lanes, provenance"
                      + (", base ride/panel/window" if base is not None
                         else "") + ")")
    except SystemExit as e:
        return fail(_halt_text(e))
    ks = key_sets(book, base) if base is not None else None
    if ruler == "two_sample":
        if not ks["moved"]:
            return fail(f"HALT: {rec['registration']} — the arm shares the "
                        f"WHOLE campaign set with its base; the commissioned "
                        f"two-sample ruler's premise failed.")
        checks.append(f"two-sample PREMISE holds on keys: paired "
                      f"{ks['n_paired']} · book-only {ks['n_book_only']} · "
                      f"base-only {ks['n_base_only']}")
    elif ruler == "set_change":
        moved = ks["moved"]
        checks.append(f"set_change law on keys: the set "
                      f"{'MOVED' if moved else 'did NOT move'} -> the "
                      f"{'TWO-SAMPLE' if moved else 'PAIRED'} interval "
                      f"(paired {ks['n_paired']} · book-only "
                      f"{ks['n_book_only']} · base-only {ks['n_base_only']})")
    stray = sorted(({t.symbol for t in book}
                    | {t.symbol for t in (base or [])}) - set(panel))
    if stray:
        return fail(f"HALT: the book holds {stray}, outside the declared "
                    f"panel {TP.panel_name(panel)}.")
    checks.append("no symbol outside the declared panel (book + base)")
    n_bad = sum(1 for t in list(book) + list(base or [])
                if t.net_r is None or not np.isfinite(float(t.net_r)))
    if n_bad:
        return fail(f"HALT: {n_bad} campaign(s) carry a non-finite net_r.")
    checks.append("every campaign's net_r is finite (a finiteness test; "
                  "nothing is summed)")
    fe = filed["era"]
    if fe != arm["era"]:
        return fail(f"HALT: filed era {fe!r} != the arm's {arm['era']!r}")
    sp_era = (getattr(book, "spec", None) or {}).get("era")
    if sp_era is not None and sp_era != fe:
        return fail(f"HALT: the book was ridden on the {sp_era!r} era, the "
                    f"arm is filed for {fe!r}.")
    out_e = [t for t in list(book) + list(base or [])
             if not TP.in_era(t.entry_ms, fe)]
    if out_e:
        return fail(f"HALT: {len(out_e)} campaigns ENTER outside the filed "
                    f"{fe!r} era.")
    checks.append(f"era {fe!r}: every entry of book"
                  + (" and base" if base is not None else "")
                  + " inside it; the book was ridden on it")
    return {"ok": True, "halt": None, "checks": checks, "keys": ks}


# ════════════════════════════ 5 · BESIDE THE ROW — OUTCOME-FREE (dry-run too)
def per_asset_counts(book, panel) -> dict:
    c = Counter(str(t.symbol) for t in book)
    return {s: int(c.get(s, 0)) for s in panel}


def per_lane_counts(book) -> dict:
    c = Counter(str(t.lane) for t in book)
    return dict(sorted(c.items()))


def gen1_subset(books: dict, arms: list) -> dict:
    """P-GEN-1 §5 ARM 3: "arm 3's campaigns must be exactly the three-symbol
    subset of arm 1's book. That is an assertion … if the two books disagree
    on any campaign of those three symbols, the disagreement is printed and
    the arm is reported as broken."  Held on the campaign KEYS and on the
    whole-trade content sha — no outcome is computed."""
    sc = [a for a in arms if a["scored_in_family"]]
    nt = [a for a in arms if sc and not a["scored_in_family"]
          and set(a["panel"]) < set(sc[0]["panel"])]
    if len(sc) != 1 or len(nt) != 1 or sc[0]["arm"] not in books \
            or nt[0]["arm"] not in books:
        return {"checked": False, "why": "arm 1 or arm 3 has no Book"}
    b1, b3 = books[sc[0]["arm"]], books[nt[0]["arm"]]
    three = set(nt[0]["panel"])
    sub = [t for t in b1 if t.symbol in three]
    k1 = sorted(_key(t) for t in sub)
    k3 = sorted(_key(t) for t in b3)
    s1 = TP._book_sha(sub)
    s3 = TP._book_sha(b3)
    c1 = B.book_content_sha(sub)
    c3 = B.book_content_sha(b3)
    return {"checked": True, "arm1": sc[0]["arm"], "arm3": nt[0]["arm"],
            "n_subset_of_arm1": len(sub), "n_arm3": len(b3),
            "keys_equal": k1 == k3,
            "keys_only_in_arm1": [list(k) for k in sorted(set(k1) - set(k3))],
            "keys_only_in_arm3": [list(k) for k in sorted(set(k3) - set(k1))],
            "book_sha_equal": s1 == s3, "content_sha_equal": c1 == c3,
            "broken": not (k1 == k3 and s1 == s3 and c1 == c3)}


def spring_refusals(book, springs: dict, card) -> dict:
    """P-SPR-2 §5: "Those refusals are counted, not hidden."  replay10
    tallies no refusal of a SPRING candidate, so the count is RECONSTRUCTED
    from the signals handed in and the Book's own schedule, in replay10's
    order: entered -> position_open (a campaign of the asset is open at the
    harden bar: entry_i <= reclaim_i <= exit_i) -> degenerate_R (the ATR at
    the harden bar is not finite and positive) -> no_struct_anchor
    (`spring_stop` gives no positive R).  A signal none of these explains is
    counted UNEXPLAINED — it must be zero, or the reconstruction is wrong.
    Reads entry geometry and the exit BAR; no outcome."""
    per, tot = {}, Counter()
    for sym, sigs in sorted(springs.items()):
        f = T9.frame(sym)["f"]
        camps = [t for t in book if t.symbol == sym]
        entered = Counter((int(t.entry_i), int(t.direction)) for t in camps
                          if t.lane == "spring")
        c = Counter()
        for s in sigs:
            ti, d = int(s.reclaim_i), int(s.direction)
            if entered.get((ti, d), 0) > 0:
                entered[(ti, d)] -= 1
                c["entered"] += 1
                continue
            if any(int(t.entry_i) <= ti <= int(t.exit_i) for t in camps):
                c["position_open"] += 1
                continue
            atr = float(f.atr[ti])
            if not (np.isfinite(atr) and atr > 0):
                c["degenerate_R"] += 1
                continue
            stp = LN.RC.spring_stop(s, float(f.c[ti]), atr,
                                    card.entry_rail_atr)
            if stp is None or not (np.isfinite(stp.r_dist)
                                   and stp.r_dist > 0):
                c["no_struct_anchor"] += 1
                continue
            c["UNEXPLAINED"] += 1
        c["signals"] = len(sigs)
        c["long"] = sum(1 for s in sigs if int(s.direction) == 1)
        c["short"] = len(sigs) - c["long"]
        per[sym] = {k: int(c.get(k, 0)) for k in
                    ("signals", "long", "short", "entered", "position_open",
                     "degenerate_R", "no_struct_anchor", "UNEXPLAINED")}
        tot.update(per[sym])
    n_spring = sum(1 for t in book if t.lane == "spring")
    tot = {k: int(v) for k, v in tot.items()}
    return {"per_asset": per, "total": tot,
            "spring_campaigns_in_book": n_spring,
            "consistent": bool(tot.get("entered", 0) == n_spring
                               and tot.get("UNEXPLAINED", 0) == 0)}


def trg2_ride_diff(arm: dict) -> dict:
    """P-TRG-2 §2: the filed ride differs from CONTROL_RIDE in EXACTLY the
    two trigger fields; §2 also names the roles a member of SWEEP_CELLS."""
    diff = TP._spec_diff(TP.CONTROL_RIDE, arm["ride"])
    rf = arm["ride"]["roles_fields"]
    cell = [r.name for r in T9.SWEEP_CELLS
            if {k: repr(getattr(r, k)) for k in rf} == rf]
    return {"diff": diff, "exactly_two_trigger_fields": diff == [
        "roles_fields.trg_f: filed 12 / offered 9",
        "roles_fields.trg_s: filed 26 / offered 12"],
        "sweep_cell": cell}


def be1_census(book) -> dict:
    """F-C10-BE's STATUS, RE-DERIVED FROM THE SCORED ARM'S OWN RIDDEN BOOK:
    `tierc10_lanes.be_latch_census` (identity, class and agreement flags —
    no exit, no outcome) and `be_c10_decision_of`, held byte-for-byte against
    the census the lanes suite filed.  P-BE-1 §9 governs the decision."""
    cen = LN.be_latch_census(book, be_r=float(LN.CARD_BE1.be_floor_after_r))
    b = LN.be_census_json(cen).encode("utf-8")
    filed = BE_LATCH_CENSUS_PATH.read_bytes() \
        if BE_LATCH_CENSUS_PATH.exists() else None
    dec = cen["f_c10_be"]
    return {"decision": dec.get("decision"),
            "governed_by": dec.get("governed_by"),
            "reason": dec.get("reason"), "missing": dec.get("missing"),
            "operator_question": dec.get("operator_question"),
            "counts": cen["counts"],
            "census_sha_rederived": sha256_bytes(b),
            "census_sha_filed": (sha256_bytes(filed) if filed is not None
                                 else None),
            "byte_identical_to_filed": bool(filed is not None
                                            and filed == b)}


def brk_ready_books() -> dict:
    if not BRK_READY_BOOKS_PATH.exists():
        return {}
    return json.loads(BRK_READY_BOOKS_PATH.read_text("utf-8")).get("books") \
        or {}


def brk_sealed_row(runs_by_role: dict, lane: str) -> dict:
    """The SEALED tierc10_brk row [B12]: own-era height-vs-toll verdict
    (READ), the Tier-E other anchor, the 17-asset view, the toll print and
    TOLL_ACCOUNTING — no outcome sum."""
    rows = B.brk_rows({lane: {
        "scored": runs_by_role["scored"],
        "tier_e": runs_by_role.get("tier_e_other"),
        "panel_tier_e": runs_by_role.get("tier_e_panel17")}}, sealed=True)
    r = rows[0]
    hv = r["height_vs_toll"]
    o = r["tier_e_other_anchor"]
    p17 = r["tier_e_panel17"]
    t = r["toll"]
    return {
        "form": r["form"], "lens": r["lens"], "era": r["era"],
        "anchor_scored": r["anchor_scored"],
        "anchor_tier_e": r["anchor_tier_e"],
        "height_vs_toll": {k: hv.get(k) for k in (
            "asset", "lens", "scale_kind", "era", "verdict_pass", "reason",
            "provisional", "n_ranges", "ratio_median", "height_atr_median",
            "toll_atr_median")},
        "height_vs_toll_asset": {k: r["height_vs_toll_asset"].get(k)
                                 for k in ("asset", "source", "derived_how",
                                           "override")},
        "tier_e_other_anchor": None if o is None else {
            k: o.get(k) for k in ("tier", "anchor", "n_campaigns",
                                  "per_asset_n_campaigns",
                                  "book_sha256_score_binding")},
        "tier_e_panel17": None if p17 is None else {
            k: p17.get(k) for k in ("tier", "anchor", "n_campaigns",
                                    "n_assets_with_campaigns",
                                    "book_sha256_score_binding")},
        "toll": ({"cls": t.get("cls"), "lens": t.get("lens"),
                  "per_asset": t.get("per_asset")} if t.get("cls")
                 else {"stamped": False, "why": t.get("why")}),
        "toll_pct_of_1r_median": r["scored_figures"].get(
            "toll_pct_of_1r_median"),
        "toll_accounting_status": B.TOLL_ACCOUNTING.get("status"),
        "toll_accounting": B.TOLL_ACCOUNTING,
        "tuned": r["tuned"], "flip_hold_pins": r["flip_hold_pins"],
        "as_of_last_closed_4h": r["as_of_last_closed_4h"],
    }


def twin_tiers(panel) -> dict:
    """The haircut twin's tier and charter round trip per panel stem — read
    through tierc10_data (never typed); HALTS on an untiered asset."""
    m = D.load_manifest()
    by = {v["stem"]: v["asset"] for v in m["venues"] if v["stem"]}
    out = {}
    for s in panel:
        if s not in by:
            raise SystemExit(f"HALT: the Stage D manifest names no stem {s}.")
        a = by[s]
        out[s] = {"asset": a, "tier": D.tier_of(a),
                  "charter_round_trip_bps": D.charter_round_trip_bps(a)}
    return out


# ═════════════════════════════════════════════ 6 · THE DRY-RUN, PRINTED
class Printer:
    def __init__(self, echo: bool = True):
        self.buf = io.StringIO()
        self.echo = echo

    def __call__(self, s: str = "") -> None:
        self.buf.write(s + "\n")
        if self.echo:
            print(s, flush=True)

    def text(self) -> str:
        return self.buf.getvalue()


def _fmt_counts(d: dict) -> str:
    return " · ".join(f"{k} {v}" for k, v in d.items())


def _card_line(card) -> str:
    return ", ".join(f"{k}={v}" for k, v in card_fields_printable(card).items())


def arm_record(rid: str, reg: dict, k: int, arm: dict, ride: dict | None,
               bind: dict | None, halt: str | None) -> dict:
    """What the dry-run files per arm (machine-readable; `--expect` reads
    it back at --score)."""
    panel = list(arm["panel"])
    r = {"registration": rid, "seq": reg["rec"]["seq"], "arm_index": k,
         "arm": arm["arm"], "scored_in_family": bool(arm["scored_in_family"]),
         "panel_name": arm["panel_name"], "n_panel": len(panel),
         "loao_line": arm.get("loao_line"),
         "loao_bar": TP.above_half_bar(len(panel)), "era": arm["era"],
         "ruler": arm["ruler"], "base": arm["base"], "runner": arm["runner"],
         "lanes": list(arm["lanes"]), "halt": halt}
    if ride is not None:
        book, base = ride["book"], ride["base"]
        r.update(door=ride["door"],
                 window=[iso(ride["window"][0]), iso(ride["window"][1] + 1)],
                 window_ms=[int(ride["window"][0]), int(ride["window"][1])],
                 n_campaigns=len(book),
                 per_asset=per_asset_counts(book, panel),
                 per_lane=per_lane_counts(book),
                 zero_campaign_assets=[s for s in panel if not any(
                     t.symbol == s for t in book)],
                 book_sha=TP._book_sha(book),
                 book_content_sha=B.book_content_sha(book),
                 book_spec={k_: book.spec.get(k_) for k_ in (
                     "runner", "registration", "arm", "era", "lo_ms",
                     "hi_ms")},
                 base_n=(None if base is None else len(base)),
                 base_per_asset=(None if base is None
                                 else per_asset_counts(base, panel)),
                 base_sha=TP._book_sha(base),
                 base_content_sha=(None if base is None
                                   else B.book_content_sha(base)),
                 card=(None if ride["card"] is None
                       else {"class": f"{type(ride['card']).__module__}."
                                      f"{type(ride['card']).__qualname__}",
                             "fields": card_fields_printable(ride["card"])}))
    if bind is not None:
        r.update(bind_ok=bind["ok"], bind_halt=bind["halt"],
                 bind_checks=list(bind["checks"]), keys=bind["keys"])
    return r


def dry_run(ctx: dict, only: list | None, P: Printer) -> dict:
    """RIDE EVERY FILED ARM TO ITS BOOK AND BIND IT — PRINT, SCORE NOTHING."""
    regs, order = ctx["regs"], ctx["order"]
    sub = TP.substrate()
    P("TIER-C10 · STAGE B · SCORING DRIVER · --dry-run")
    P(DRYRUN_LAW)
    P(f"substrate {sub['substrate']} · as_of_last_closed_4h "
      f"{B.as_of_of_record()} · seed {TP.SEED} · n_boot {TP.N_BOOT} · "
      f"family m {TP.FAMILY_M}")
    P(f"registry of record {ctx['reg_dir']} · len {ctx['registry_len']} · "
      f"head {ctx['registry_head']} (== REGISTRY_PIN.json) · order "
      f"{' > '.join(order)}")
    for rid in order:
        rr = regs[rid]["rec"]
        P(f"  {rid}: seq {rr['seq']} · payload sha {rr['sha256'][:16]} · "
          f"text sha {rr['text_sha256'][:16]} · prior {rr['prior_pct']}% · "
          f"{len(regs[rid]['arms'])} arm(s) · text of record verified at "
          f"the door with the pinned head")
    sj = scored_json_on_file(ctx["reg_dir"])
    P(f"  .scored.json on file: {sj or 'NONE'}")
    arms_out, halts, besides = [], [], {}
    brk_cache: dict = {}
    brk_runs: dict = {}
    books_by_reg: dict = {}
    ready_books = brk_ready_books()
    for rid in order:
        if only and rid not in only:
            continue
        reg = regs[rid]
        arms = reg["arms"]
        P("")
        P("=" * 78)
        P(f"{rid} · seq {reg['rec']['seq']} · {len(arms)} filed arm(s), in "
          f"filed order")
        P("=" * 78)
        books_by_reg[rid] = {}
        for k, arm in enumerate(arms, 1):
            panel = list(arm["panel"])
            P(f"── {rid} · arm {k}/{len(arms)} · {arm['arm']!r}")
            P(f"   scored_in_family {bool(arm['scored_in_family'])} · panel "
              f"{arm['panel_name']} (N={len(panel)}) · era {arm['era']} · "
              f"ruler {arm['ruler']} · base {arm['base']} · runner "
              f"{arm['runner']} · lanes {list(arm['lanes'])} · LOAO line "
              f"{arm.get('loao_line')} (bar {TP.above_half_bar(len(panel))}"
              f"/{len(panel)})")
            ride = bind = halt = None
            try:
                ride = ride_arm(reg, rid, arm, brk_cache)
            except SystemExit as e:
                halt = _halt_text(e)
            if ride is None:
                P(f"   *** THE DOOR HALTED — NO BOOK. Verbatim: {halt}")
                halts.append((rid, arm["arm"], halt))
                arms_out.append(arm_record(rid, reg, k, arm, None, None,
                                           halt))
                continue
            book, base = ride["book"], ride["base"]
            books_by_reg[rid][arm["arm"]] = book
            if ride["door"] == "brk":
                brk_runs.setdefault(rid, {})[ride["brk"][1]] = ride["run"]
            bind = bind_check(reg["rec"], arm, book, base)
            rec_ = arm_record(rid, reg, k, arm, ride, bind, None)
            arms_out.append(rec_)
            P(f"   door {ride['door']} → Book · spec registration "
              f"{book.spec.get('registration')!r} · arm "
              f"{book.spec.get('arm')!r} · era {book.spec.get('era')!r}")
            P(f"   window [{rec_['window'][0]}, {rec_['window'][1]}) "
              f"({arm['era']}: {TP.era_note(arm['era'])[:60]}…)")
            if ride["card"] is not None and ride["door"] == "lanes":
                P(f"   card {type(ride['card']).__qualname__}"
                  f"({_card_line(ride['card'])})")
            if ride["door"] == "run_cell_n":
                P(f"   card/roles REBUILT from the filed ride and "
                  f"round-tripped: card {ride['card'].name!r}, roles "
                  f"{ride['roles'].name!r} {ride['roles'].periods}")
            P(f"   n_campaigns {len(book)} · per lane "
              f"{rec_['per_lane']} · per asset: "
              f"{_fmt_counts(rec_['per_asset'])}")
            P(f"   zero-campaign assets: "
              f"{rec_['zero_campaign_assets'] or 'none'}")
            P(f"   book sha (TP._book_sha) {rec_['book_sha']} · content sha "
              f"{rec_['book_content_sha'][:16]}")
            if base is None:
                P("   base: zero — no base book (vs_zero)")
            else:
                P(f"   base card-v6: TP.run_cell_n(CONTROL_CARD, V6_ROLES, "
                  f"{arm['panel_name']}, same window) · n {len(base)} · per "
                  f"asset: {_fmt_counts(rec_['base_per_asset'])}")
                P(f"   base sha (TP._book_sha) {rec_['base_sha']} · content "
                  f"sha {rec_['base_content_sha'][:16]}")
            if bind["ok"]:
                P("   BINDING OK — " + " | ".join(bind["checks"]))
            else:
                P(f"   *** BINDING WOULD HALT at TP.score — verbatim: "
                  f"{bind['halt']}")
                if bind["checks"]:
                    P("       (passed before it: "
                      + " | ".join(bind["checks"]) + ")")
                pq = prescribed(rid, bind["halt"], reg["text"])
                rec_["text_prescribes"] = pq
                for q in pq:
                    P(f"       THE FILED TEXT PRESCRIBES THIS (verified "
                      f"verbatim in {rid}'s text of record): \"{q}\"")
                halts.append((rid, arm["arm"], bind["halt"]))
            if ride["door"] == "brk":
                rb = ready_books.get(f"{rid} :: {arm['arm']}")
                if rb is None:
                    P("   BRK_READY_BOOKS.json: no filed record for this arm")
                else:
                    m1 = rb.get("book_sha256_score_binding") == rec_["book_sha"]
                    m2 = rb.get("book_content_sha256") \
                        == rec_["book_content_sha"]
                    rec_["brk_ready_books_match"] = bool(m1 and m2)
                    P(f"   held against BRK_READY_BOOKS.json: score-binding "
                      f"sha {'MATCH' if m1 else 'DIFFERS'} · content sha "
                      f"{'MATCH' if m2 else 'DIFFERS'} (filed n "
                      f"{rb.get('n_campaigns')})")
            if ride["springs"] is not None:
                sr = spring_refusals(book, ride["springs"], ride["card"])
                rec_["spring_refusals"] = sr
                P(f"   spring signals handed in / refusals COUNTED [P-SPR-2 "
                  f"§5] (reconstructed from the signals and the Book's "
                  f"schedule; consistent={sr['consistent']}):")
                for sym, c in sr["per_asset"].items():
                    P(f"     {sym}: {_fmt_counts(c)}")
                P(f"     TOTAL: {_fmt_counts(sr['total'])} · spring "
                  f"campaigns in book {sr['spring_campaigns_in_book']}")
            if ride["door"] == "run_cell_n" and rid == "P-TRG-2":
                td = trg2_ride_diff(arm)
                rec_["trg2_ride_diff"] = td
                P(f"   ride vs CONTROL_RIDE: {td['diff']} · exactly the two "
                  f"trigger fields: {td['exactly_two_trigger_fields']} · "
                  f"tierc9.SWEEP_CELLS member: {td['sweep_cell']}")
        # ── BESIDE THE REGISTRATION (outcome-free) ────────────────────────
        beside = {}
        if rid == "P-GEN-1":
            g = gen1_subset(books_by_reg[rid], arms)
            beside["arm3_is_subset_of_arm1"] = g
            P(f"── BESIDE {rid} · §5 ARM 3 ASSERTION (arm 3 == the "
              f"three-symbol subset of arm 1): "
              + ("NOT CHECKED — " + g["why"] if not g["checked"] else
                 f"keys equal {g['keys_equal']} · book sha equal "
                 f"{g['book_sha_equal']} · content sha equal "
                 f"{g['content_sha_equal']} (arm-1 subset n "
                 f"{g['n_subset_of_arm1']} / arm 3 n {g['n_arm3']}) → "
                 + ("*** ARM 3 IS BROKEN — disagreement printed: only in "
                    f"arm 1 {g['keys_only_in_arm1'][:6]}, only in arm 3 "
                    f"{g['keys_only_in_arm3'][:6]}" if g["broken"]
                    else "HOLDS")))
            P(f"   LOAO will print TWICE at --score: arm 1 (all admitted, "
              f"bar {TP.above_half_bar(12)}/12) and arm 3 (never-touched "
              f"only, bar {TP.above_half_bar(3)}/3); the 17-asset arm's "
              f"bar is {TP.above_half_bar(17)}/17.")
        # the haircut twin rides EVERY row [contract: "every row gets the
        # charter model as a HAIRCUT TWIN"] — wired here, computed at --score
        panel_u: list = []
        for a in arms:
            panel_u += [s for s in a["panel"] if s not in panel_u]
        try:
            tt = twin_tiers(panel_u)
            beside["haircut_twin_tiers"] = tt
            P(f"── BESIDE {rid} · HAIRCUT TWIN wired "
              f"(tierc10_data.haircut_twin_net_r, charter round trip bps "
              f"per asset; computed at --score only): "
              + " · ".join(f"{s} {v['tier']}/{v['charter_round_trip_bps']:g}"
                           for s, v in tt.items()))
        except SystemExit as e:
            beside["haircut_twin_tiers"] = {"halt": _halt_text(e)}
            P(f"── BESIDE {rid} · HAIRCUT TWIN HALT: {_halt_text(e)}")
        if rid == "P-BE-1":
            a1 = next((a for a in arms if a["scored_in_family"]), None)
            if a1 is not None and a1["arm"] in books_by_reg[rid]:
                try:
                    be = be1_census(books_by_reg[rid][a1["arm"]])
                except SystemExit as e:
                    be = {"decision": "HALT", "reason": _halt_text(e)}
                beside["f_c10_be"] = be
                P(f"── BESIDE {rid} · F-C10-BE (re-derived from arm "
                  f"{a1['arm']!r}'s ridden Book): {be.get('decision')} "
                  f"[{be.get('governed_by')}] · census re-derived "
                  f"{str(be.get('census_sha_rederived'))[:16]} vs filed "
                  f"{str(be.get('census_sha_filed'))[:16]} · byte-identical "
                  f"{be.get('byte_identical_to_filed')}")
                P(f"   reason (verbatim): {be.get('reason')}")
            else:
                beside["f_c10_be"] = {"decision": "NOT DERIVED",
                                      "reason": "arm A1 has no Book"}
                P(f"── BESIDE {rid} · F-C10-BE NOT DERIVED — A1 has no Book")
        if rid in brk_runs:
            lane = next(iter({tuple(a["lanes"])[0] for a in arms}))
            runs = brk_runs[rid]
            if "scored" in runs:
                try:
                    sr = brk_sealed_row(runs, lane)
                except SystemExit as e:
                    sr = {"halt": _halt_text(e)}
                beside["brk_sealed_row"] = sr
                if "halt" in sr:
                    P(f"── BESIDE {rid} · SEALED BRK ROW HALT: {sr['halt']}")
                else:
                    hv = sr["height_vs_toll"]
                    P(f"── BESIDE {rid} · SEALED BRK ROW [B12] · lens "
                      f"{sr['lens']} · era {sr['era']} · scored anchor "
                      f"{sr['anchor_scored']!r} · Tier-E other anchor "
                      f"{sr['anchor_tier_e']!r}")
                    P(f"   HEIGHT-vs-TOLL [Q-R3], READ at the form's own era "
                      f"({hv['era']}), {hv['asset']} / {hv['lens']} / "
                      f"{hv['scale_kind']}: verdict_pass {hv['verdict_pass']}"
                      f" — {hv['reason']!r} · provisional {hv['provisional']}"
                      f" · n_ranges {hv['n_ranges']}")
                    o = sr["tier_e_other_anchor"]
                    p17 = sr["tier_e_panel17"]
                    P(f"   Tier-E other anchor: "
                      + (f"{o['n_campaigns']} campaigns "
                         f"{o['per_asset_n_campaigns']}" if o else "ABSENT")
                      + " · Tier-E 17-asset view: "
                      + (f"{p17['n_campaigns']} campaigns on "
                         f"{p17['n_assets_with_campaigns']} assets"
                         if p17 else "ABSENT"))
                    P(f"   TOLL: {sr['toll']} · toll_pct_of_1r median "
                      f"{sr['toll_pct_of_1r_median']}")
                    P(f"   TOLL_ACCOUNTING: {sr['toll_accounting_status']}")
        besides[rid] = beside
    # ── SUMMARY ──────────────────────────────────────────────────────────
    P("")
    P("=" * 78)
    P("SUMMARY — per arm: registration · arm · scored · n · book sha · base "
      "sha · binding")
    P("=" * 78)
    for r_ in arms_out:
        P(f"  {r_['registration']:<9} {r_['arm'][:52]:<52} "
          f"{'SCORED' if r_['scored_in_family'] else 'tier-E':<6} "
          + (f"n={r_['n_campaigns']:<5} {r_['book_sha'][:16]} "
             f"{(r_['base_sha'] or 'zero')[:16]:<16} "
             f"{'BIND-OK' if r_['bind_ok'] else 'BIND-HALT'}"
             if r_.get("halt") is None else "DOOR-HALT"))
    P(f"HALTS: {len(halts)}")
    for rid, an, h in halts:
        P(f"  {rid} {an!r}: {h}")
    P(f".scored.json on file after the dry-run: "
      f"{scored_json_on_file(ctx['reg_dir']) or 'NONE'}")
    return {"arms": arms_out, "halts": halts, "beside": besides}


# ═══════════════════════════════════ 7 · --score — THE ONE IRREVERSIBLE ACT
def _jsonable(v):
    """Plain JSON: numpy scalars to python, non-finite floats to null (the
    rows file says so), DataFrames to records, tuples to lists."""
    if isinstance(v, dict):
        return {str(k): _jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_jsonable(x) for x in v]
    if isinstance(v, (bool, np.bool_)):
        return bool(v)
    if isinstance(v, (int, np.integer)):
        return int(v)
    if isinstance(v, (float, np.floating)):
        x = float(v)
        return x if math.isfinite(x) else None
    if v is None or isinstance(v, str):
        return v
    if hasattr(v, "to_dict"):
        return _jsonable(v.to_dict("records"))
    return repr(v)


def rows_bytes(doc: dict) -> bytes:
    return (json.dumps(_jsonable(doc), indent=1, sort_keys=True,
                       ensure_ascii=False, allow_nan=False) + "\n").encode()


def haircut_twin_block(book, base=None) -> dict:
    """THE HAIRCUT TWIN, BESIDE THE ROW [VETO "tiers"] — per campaign
    `tierc10_data.haircut_twin_net_r(asset, gross_r, entry_px, exit_px,
    risk_px = r_dist)`, AS FILED (net_r_twin = gross_r − cost_r).  The
    TC-series net_r stays the accounting of record and carries the verdict;
    the twin gates nothing.  FILED FUNCTION, NAMED LIMIT: it charges fee +
    charter slippage and NO funding, while the TC-series net_r charges
    funding — so a companion `net_r_twin − funding_r` rides beside it,
    labelled a companion.  A sign disagreement with the TC-series point is
    FLAGGED for both."""
    m = D.load_manifest()
    by = {v["stem"]: v["asset"] for v in m["venues"] if v["stem"]}

    def one(bk):
        tw, twf, per = [], [], {}
        for t in bk:
            h = D.haircut_twin_net_r(by[str(t.symbol)], float(t.gross_r),
                                     float(t.entry_px), float(t.exit_px),
                                     float(t.r_dist))
            tw.append(h["net_r_twin"])
            twf.append(h["net_r_twin"] - float(t.funding_r or 0.0))
            per.setdefault(str(t.symbol), []).append(h["net_r_twin"])
        return tw, twf, per
    tw, twf, per = one(book)
    tc = [float(t.net_r) for t in book]
    out = {"law": ("HAIRCUT TWIN — an ADDED column beside the TC-series toll, "
                   "never a replacement; the verdict, CI, p and LOAO are the "
                   "TC-series row's [VETO 'tiers']"),
           "function": "tierc10_data.haircut_twin_net_r (as filed)",
           "funding_note": ("the filed twin charges fee + charter slippage "
                            "and NO funding; the companion column subtracts "
                            "the campaign's funding_r and is NOT the filed "
                            "twin"),
           "n": len(tc),
           "tc_expectancy_r": float(np.mean(tc)) if tc else None,
           "twin_expectancy_r": float(np.mean(tw)) if tw else None,
           "twin_with_funding_companion_expectancy_r":
               float(np.mean(twf)) if twf else None,
           "twin_per_asset_expectancy_r": {
               s: float(np.mean(v)) for s, v in sorted(per.items())}}
    if base is not None:
        btw, btwf, _ = one(base)
        btc = [float(t.net_r) for t in base]
        out.update(
            base_n=len(btc),
            tc_difference_r=float(np.mean(tc) - np.mean(btc)),
            twin_difference_r=float(np.mean(tw) - np.mean(btw)),
            twin_with_funding_companion_difference_r=float(
                np.mean(twf) - np.mean(btwf)))
        a, b_, c_ = (out["tc_difference_r"], out["twin_difference_r"],
                     out["twin_with_funding_companion_difference_r"])
    else:
        a, b_, c_ = (out["tc_expectancy_r"], out["twin_expectancy_r"],
                     out["twin_with_funding_companion_expectancy_r"])
    out["sign_disagrees_with_tc"] = bool(np.sign(a) != np.sign(b_))
    out["companion_sign_disagrees_with_tc"] = bool(np.sign(a) != np.sign(c_))
    return out


def per_asset_rows(book, rid: str, arm: dict) -> list:
    """The per-asset rows beside the row — `TP.headline_n` (every DECLARED
    asset, n = 0 included), the asset and direction slices, both
    aggregations.  Printed beside; gates nothing."""
    df = TP.headline_n(book, f"{rid} :: {arm['arm']}", tuple(arm["panel"]))
    keep = df[df["group"].isin(["asset", "direction"])]
    return _jsonable(keep.to_dict("records"))


def expect_check(expect: dict, rid: str, arm: str, book, base) -> None:
    """`--expect`: the Book (and base) about to be scored must carry the shas
    a REVIEWED dry-run printed for this arm — else HALT, before TP.score."""
    want = expect.get((rid, arm))
    got = (TP._book_sha(book), TP._book_sha(base))
    if want is None or tuple(want) != got:
        raise SystemExit(
            f"HALT: --expect — {rid} {arm!r} re-rode to book {got[0]} / base "
            f"{got[1]}, the reviewed dry-run says {want}. Nothing is scored "
            f"on a Book nobody reviewed.")


def score_registration(ctx: dict, rid: str, expect: dict | None,
                       P: Printer, scores_dir: Path | None = None,
                       continue_after_scored_halt: bool = False) -> int:
    """SCORE EVERY FILED ARM OF ONE REGISTRATION — `TP.score`, arm by arm,
    in filed order; file scores/<REG>.rows.json.  A Tier-E arm that HALTs
    is recorded verbatim and the next arm is scored.  A SCORED arm that
    HALTs is recorded verbatim (with what the filed text prescribes for that
    HALT) and, by default, STOPS the registration: no Tier-E arm is scored
    behind a failed slot unless `continue_after_scored_halt` — the
    operator's word, because a Tier-E score is as irreversible as any.
    Returns 0 (all rows), 3 (a Tier-E HALT), 2 (the scored arm HALTed)."""
    scores_dir = Path(scores_dir) if scores_dir else SCORES
    reg = ctx["regs"][rid]
    rows, rc = [], 0
    brk_cache: dict = {}
    brk_runs: dict = {}
    books: dict = {}
    # PASS 1 — RIDE EVERY ARM AND CHECK EVERY BOOK BEFORE ANYTHING IS SCORED.
    # `TP.score` is irreversible (`_mark_scored`), so a Book that is not the
    # reviewed one — or a BRK arm on the wrong anchor — must HALT the
    # registration before its FIRST arm is scored, not after arm k-1.
    rides: dict = {}
    for k, arm in enumerate(reg["arms"], 1):
        try:
            rides[k] = ride_arm(reg, rid, arm, brk_cache)
        except SystemExit as e:
            rides[k] = e
            continue
        ride = rides[k]
        if ride["door"] == "brk":
            lane, role = ride["brk"]
            want = B.role_anchor(lane, role)
            if str(ride["run"]["anchor"]) != want:
                raise SystemExit(
                    f"HALT: {rid} {arm['arm']!r} rode anchor "
                    f"{ride['run']['anchor']!r}, not the filed role's "
                    f"{want!r}. Nothing in {rid} is scored.")
        if expect is not None:
            expect_check(expect, rid, arm["arm"], ride["book"], ride["base"])
    # PASS 2 — SCORE, arm by arm, in filed order.
    for k, arm in enumerate(reg["arms"], 1):
        try:
            if isinstance(rides[k], SystemExit):
                raise rides[k]
            ride = rides[k]
        except SystemExit as e:
            h = _halt_text(e)
            P(f"*** {rid} arm {arm['arm']!r}: THE DOOR HALTED — {h}")
            rows.append({"arm": arm["arm"], "halt": h, "at": "door",
                         "scored_in_family": bool(arm["scored_in_family"]),
                         "text_prescribes": prescribed(rid, h, reg["text"])})
            if arm["scored_in_family"]:
                rc = 2
                if not continue_after_scored_halt:
                    break
                continue
            rc = max(rc, 3)
            continue
        book, base = ride["book"], ride["base"]
        books[arm["arm"]] = book
        if ride["door"] == "brk":
            brk_runs[ride["brk"][1]] = ride["run"]
        # OUTCOME-FREE beside-columns first: they ride the entry whether or
        # not TP.score HALTs (P-BE-1's F-C10-BE status belongs on its row
        # even when its premise HALT leaves no row).
        pre = {"per_asset_n": per_asset_counts(book, arm["panel"])}
        if ride["card"] is not None and ride["door"] == "lanes":
            pre["card_fields_ridden"] = card_fields_printable(ride["card"])
        if ride["springs"] is not None:
            pre["spring_refusals"] = spring_refusals(
                book, ride["springs"], ride["card"])
        if rid == "P-BE-1" and arm["scored_in_family"]:
            pre["f_c10_be"] = be1_census(book)
        try:
            row = TP.score(rid, reg["text"], book, tuple(arm["panel"]),
                           base=base, ruler=arm["ruler"], seed=TP.SEED,
                           arm=arm["arm"],
                           scored_in_family=bool(arm["scored_in_family"]),
                           note=f"tierc10_score.py · {rid} arm {k}",
                           head_of_record=reg["head"], era=arm["era"])
        except SystemExit as e:
            h = _halt_text(e)
            pq = prescribed(rid, h, reg["text"])
            P(f"*** {rid} arm {arm['arm']!r}: TP.score HALTED — {h}")
            for q in pq:
                P(f"    THE FILED TEXT PRESCRIBES THIS: \"{q}\"")
            rows.append({"arm": arm["arm"], "halt": h, "at": "TP.score",
                         "scored_in_family": bool(arm["scored_in_family"]),
                         "text_prescribes": pq, "beside": pre})
            if arm["scored_in_family"]:
                rc = 2
                if not continue_after_scored_halt:
                    break
                continue
            rc = max(rc, 3)
            continue
        beside = dict(pre, per_asset_rows=per_asset_rows(book, rid, arm),
                      haircut_twin=haircut_twin_block(book, base))
        rows.append({"arm": arm["arm"], "score_row": row, "beside": beside,
                     "scored_in_family": bool(arm["scored_in_family"])})
        P(f"  SCORED {rid} · {arm['arm']!r} · "
          f"{'SCORED' if arm['scored_in_family'] else 'Tier-E'} · n "
          f"{row['n']} · expectancy {row['expectancy_r']} · CI "
          f"[{row['ci_lo']}, {row['ci_hi']}] · p {row['p_one_sided']} · "
          f"verdict: {row['verdict']} · LOAO {row['loao_line']} (line of "
          f"record {row['loao_line_of_record']}: "
          f"{row['loao_above_of_record']}/{row['loao_panels']}, bar "
          f"{row['loao_bar_above_half']}, clears "
          f"{row['loao_clears_line_of_record']}) · EAR "
          f"{row['ear_expectancy_r']} [{row['ear_ci_lo']}, "
          f"{row['ear_ci_hi']}] · twin sign flag "
          f"{beside['haircut_twin']['sign_disagrees_with_tc']}")
    reg_beside: dict = {}
    if rid == "P-GEN-1":
        reg_beside["arm3_is_subset_of_arm1"] = gen1_subset(books,
                                                           reg["arms"])
        lo = {r["arm"]: (r["score_row"]["loao_line"],
                         r["score_row"]["loao_clears_line_of_record"])
              for r in rows if "score_row" in r}
        reg_beside["loao_printed_twice"] = lo
        P(f"  LOAO, PRINTED TWICE [P-GEN-1]: {lo}")
    if brk_runs.get("scored") is not None:
        lane = next(iter({tuple(a["lanes"])[0] for a in reg["arms"]}))
        sr = brk_sealed_row(brk_runs, lane)
        reg_beside["brk_sealed_row"] = sr
        for r_ in rows:                # ON the scored row [contract l.112]
            if r_.get("scored_in_family") and "beside" in r_:
                r_["beside"]["brk_sealed_row"] = sr
        P(f"  BRK ROW [{rid}]: height-vs-toll ({sr['height_vs_toll']['era']}"
          f") verdict_pass {sr['height_vs_toll']['verdict_pass']} — "
          f"{sr['height_vs_toll']['reason']!r} · Tier-E other anchor "
          f"{sr['anchor_tier_e']!r} · TOLL_ACCOUNTING: "
          f"{sr['toll_accounting_status']}")
    if rid == "P-BE-1":
        be = next((r_["beside"].get("f_c10_be") for r_ in rows
                   if r_.get("scored_in_family") and r_.get("beside")), None)
        if be:
            P(f"  F-C10-BE [P-BE-1]: {be.get('decision')} "
              f"[{be.get('governed_by')}] · census byte-identical to the "
              f"filed one: {be.get('byte_identical_to_filed')}")
    doc = {"registration": rid, "seq": reg["rec"]["seq"],
           "registration_sha256": reg["rec"]["sha256"],
           "registry_head_of_record": list(reg["head"]),
           "as_of_last_closed_4h": B.as_of_of_record(),
           "seed": TP.SEED, "n_boot": TP.N_BOOT,
           "law": ("each score_row is TP.score's row, verbatim; `beside` "
                   "carries what the filed text requires ON the row and "
                   "gates nothing; non-finite floats are written as null"),
           "rows": rows, "beside_registration": reg_beside}
    b = rows_bytes(doc)
    scores_dir.mkdir(parents=True, exist_ok=True)
    p = scores_dir / f"{rid}{ROWS_SUFFIX}"
    if p.exists() and p.read_bytes() != b:
        raise SystemExit(
            f"HALT: {p} exists and the re-score's bytes DIFFER (filed "
            f"{sha256_file(p)[:16]} / now {sha256_bytes(b)[:16]}). A re-score "
            f"must reproduce the first; the filed rows are kept.")
    tmp = p.with_suffix(".json.tmp")
    tmp.write_bytes(b)
    os.replace(tmp, p)
    P(f"  FILED {p} · sha {sha256_bytes(b)} · rc {rc}")
    return rc


def finish(ctx: dict, P: Printer, scores_dir: Path | None = None,
           allow_halted: tuple = ()) -> int:
    """THE BAR, ONCE THE FAMILY IS WHOLE: every one of the six must carry
    EXACTLY ONE canonical scored row — or, for a registration the operator
    NAMES in `allow_halted`, a rows file recording its SCORED arm's HALT
    verbatim (P-TRG-2 §5: the bar applies "to EVERY scored row it is
    handed, whatever number of the declared six actually run"; P-BE-1 §7:
    "if a sibling registration HALTs … this row still reads clears_bh_bar").
    Only then does `TP.finish_family` run (one fixed bar q/m, m = 6
    DECLARED, fewer run never loosens it).  Files scores/FAMILY.json."""
    scores_dir = Path(scores_dir) if scores_dir else SCORES
    all_rows, srcs, halted = finish_gate(ctx["order"], scores_dir,
                                         allow_halted)
    for rid, h in halted.items():
        P(f"  *** {rid}: NO SCORED ROW — its scored arm HALTED (named by "
          f"--allow-halted-slot): {h}")
    fam = TP.finish_family(all_rows, family_m=TP.FAMILY_M)
    recs = _jsonable(fam.to_dict("records"))
    doc = {"family_m_declared": TP.FAMILY_M,
           "fdr_bar_q_over_m": TP.FDR_Q / TP.FAMILY_M,
           "rows_files_sha256": srcs, "rows": recs,
           "scored_slots_halted": halted,
           "law": "TP.finish_family over every row of the six rows files; "
                  "clears_bh_bar is a SEPARATE column beside the CI verdict"}
    b = rows_bytes(doc)
    p = scores_dir / FAMILY_NAME
    if p.exists() and p.read_bytes() != b:
        raise SystemExit(f"HALT: {p} exists and differs from this finish; "
                         f"the filed family is kept.")
    p.write_bytes(b)
    for r in recs:
        if r.get("scored_in_family"):
            P(f"  {r['registration']:<9} verdict {r['verdict']} · p "
              f"{r['p_one_sided']} · clears_bh_bar {r['clears_bh_bar']} "
              f"(bar {r['fdr_bar_q_over_m']}) · LOAO line of record clears "
              f"{r['loao_clears_line_of_record']}")
    P(f"  FILED {p} · sha {sha256_bytes(b)}")
    return 0


def finish_gate(order: list, scores_dir: Path, allow_halted=()) -> tuple:
    """(rows, rows-file shas, halted slots) — or HALT.  THE GATE `finish`
    stands behind: every registration of `order` has a rows file carrying
    EXACTLY ONE canonical scored row and no scored-arm HALT, or — only when
    the operator NAMES it in `allow_halted` — no scored row and exactly one
    recorded scored-arm HALT.  Reads files; calls nothing."""
    unk = sorted(set(allow_halted) - set(order))
    if unk:
        raise SystemExit(f"HALT: --allow-halted-slot names {unk}.")
    all_rows, srcs, bad, halted = [], {}, [], {}
    for rid in order:
        p = scores_dir / f"{rid}{ROWS_SUFFIX}"
        if not p.exists():
            bad.append(f"{rid}: no rows file")
            continue
        doc = json.loads(p.read_text("utf-8"))
        ent = list(doc.get("rows", []))
        rs = [r["score_row"] for r in ent if "score_row" in r]
        sc = [r for r in rs if r.get("scored_in_family")]
        sh = [r for r in ent if "halt" in r and r.get("scored_in_family")]
        if len(sc) == 1 and not sh and sc[0].get("registration") == rid \
                and sc[0].get("registration_root_is_canonical") is True:
            srcs[rid] = sha256_file(p)
            all_rows += rs
        elif not sc and len(sh) == 1 and rid in allow_halted:
            srcs[rid] = sha256_file(p)
            halted[rid] = sh[0]["halt"]
            all_rows += rs
        else:
            bad.append(f"{rid}: {len(sc)} canonical scored row(s), "
                       f"{len(sh)} recorded scored-arm HALT(s)"
                       + (" — name it with --allow-halted-slot to finish "
                          "without it" if sh and not sc else ""))
    if bad:
        raise SystemExit("HALT: --finish needs ALL SIX registrations with "
                         "exactly one canonical scored row (or a scored-arm "
                         "HALT the operator names): " + " | ".join(bad))
    return all_rows, srcs, halted


# ═════════════════════════════════════════════════════════════════ 8 · CLI
def load_expect(path: Path) -> dict:
    d = json.loads(Path(path).read_text("utf-8"))
    return {(a["registration"], a["arm"]): (a.get("book_sha"),
                                            a.get("base_sha"))
            for a in d["arms"] if a.get("halt") is None}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true",
                   help="ride + bind every filed arm; score nothing (default)")
    g.add_argument("--score", action="store_true",
                   help="TP.score the arms of --only registrations")
    g.add_argument("--finish", action="store_true",
                   help="TP.finish_family once all six are scored")
    g.add_argument("--stage", choices=STAGE_NAMES,
                   help="B-CORE = score the five non-S1; B-5M = score "
                        "P-BRK-S1 then --finish")
    ap.add_argument("--only", nargs="+", default=None)
    ap.add_argument("--out", default=None, help="write the printout here")
    ap.add_argument("--json-out", default=None,
                    help="dry-run: write the per-arm record here")
    ap.add_argument("--expect", default=None,
                    help="score: a dry-run --json-out; refuse any Book whose "
                         "sha differs from it")
    ap.add_argument("--continue-after-scored-halt", action="store_true",
                    help="score: after a registration's SCORED arm HALTs, "
                         "still score its Tier-E arms (operator's word)")
    ap.add_argument("--allow-halted-slot", nargs="+", default=(),
                    help="finish: registrations whose SCORED arm HALTed "
                         "(recorded verbatim) and that finish without a row "
                         "(operator's word)")
    a = ap.parse_args(argv)
    TP.substrate()                           # the frozen snapshot, or HALT
    ctx = load_record()
    only = a.only
    if only:
        unk = sorted(set(only) - set(ctx["order"]))
        if unk:
            raise SystemExit(f"HALT: --only names {unk}; the filed six are "
                             f"{ctx['order']}.")
    P = Printer()
    rc = 0
    if a.score or a.stage:
        if a.stage == "B-CORE":
            todo = [r for r in ctx["order"] if r not in STAGE_B_5M]
        elif a.stage == "B-5M":
            todo = list(STAGE_B_5M)
        else:
            if not only:
                raise SystemExit("HALT: --score needs --only <REG_ID...>.")
            todo = [r for r in ctx["order"] if r in only]
        expect = load_expect(Path(a.expect)) if a.expect else None
        P(f"TIER-C10 · STAGE B · --score {todo} — IRREVERSIBLE: TP.score "
          f"binds each arm's first score in <REG>.scored.json")
        if expect is None:
            P("  (no --expect: the Books are NOT held against a reviewed "
              "dry-run)")
        for rid in todo:
            rc = max(rc, score_registration(
                ctx, rid, expect, P, continue_after_scored_halt=bool(
                    a.continue_after_scored_halt)))
        if a.stage == "B-5M":
            rc = max(rc, finish(ctx, P,
                                allow_halted=tuple(a.allow_halted_slot)))
    elif a.finish:
        rc = finish(ctx, P, allow_halted=tuple(a.allow_halted_slot))
    else:
        res = dry_run(ctx, only, P)
        if a.json_out:
            Path(a.json_out).write_bytes(rows_bytes(
                {"law": DRYRUN_LAW, "arms": res["arms"],
                 "beside_registration": res["beside"],
                 "halts": [list(h) for h in res["halts"]]}))
        rc = 2 if res["halts"] else 0
    if a.out:
        Path(a.out).write_text(P.text(), encoding="utf-8")
    return rc


if __name__ == "__main__":
    sys.exit(main())
