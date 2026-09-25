#!/usr/bin/env python
"""TIER-C11 · STAGE T-brk — P-BRK-4H, the 4h breakout-retest lane [LEANS L-T.1,
L-R.6(a), L-R.2 (SCALE-IN-SAMPLE), L-1.4 (selection_hazard), L-1.3, AM-1, AM-7].

Contract of record: exchange/queue/2026-09-24_TC11_APOLLO.md (sha256 bb38e016…,
STEP Q b9ed953).  Executor HEPHAESTUS; seed 20260924 (this stage draws nothing).
Readings of record: research_outputs/tierc11/LEANS.md (frozen) and
LEANS_AMENDMENTS.md (AM-1..AM-7, binding).  Registration of record:
research_outputs/tierc11/registrations/REGISTRATIONS.json, P-BRK-4H (seq 4),
verified here by payload sha before one bar is read.

THIS IS A RUNNER [L-F.2]: it imports tierc11_nest (N), the only TC11 module that
reaches the range machine, and calls ONE adapter, `N.range_facts(stem, '4h',
scale_kind)` — a plain dict of numpy arrays.  Everything that DECIDES (the
candidates, the stop, the tide permission, the ride, the accounting) lives in
the DECISION section below and receives plain arrays and the estate's frames
only: no Range object, no event dict, no N call (`DECISION_FUNCS` is the list;
the fixtures AST-scan them).

THE SCORED ARM (L-T.1, the registration's operative spec, built as written)
  4h macro death at the calibrated 4h pick (N.scale_of, tuning-era pick) ->
  the FIRST retest that HOLDS on tap-89 (N's scan: EMA-89 of 4h close, census
  RETEST_PINS margin 1.0 ATR / hold 3 / ttl 400; every qualifying touch in bar
  order inside the candidacy window; the first 'hold' is the event, known at
  touch + 3) -> entry at the close of the touch + hold bar, direction = the
  death direction (top death -> long) -> tide aligned AT THE ENTRY BAR'S CLOSE
  on the 4h frame (BK.tide_state(e89, e316, close)[entry_i] == direction; NOT
  BK.tide_4h_for_exec, which on a 4h exec frame reads the PREVIOUS 4h bar) ->
  stop BK.brk_stop (farther of retest extreme -/+ 0.5 ATR(4h) and entry -/+ 1.0
  ATR(4h), the extreme = min low / max high over touch..entry) -> ride
  BK.ride_leg_l(..., ribbon=None) (pure v6: tierc10_brk.py:1093 transcribes
  tierc9._ride_leg9; with ribbon None the 12/25 bell is never tested — do_br is
  False — so the bells are v6's counter 12/89 and counter 89/316 only) -> one
  position per asset (BK.brk_campaigns' open_until law) -> accounting
  BK.account_l (net = gross - taker fee 5.0 bps/side on every fill - funding by
  interval sum, D12 ceiling once) -> haircut twin per AM-7.  CLASSIC5, full
  corridor, vs zero.

TIER-E ARMS (each the scored rule with ONE named substitution; "a SELECTION, not
a result"; no verdict word):
  tierE__panel17               the 17-asset view (CLASSIC5 + UNSEEN12; LOAO bar 9/17)
  tierE__memline_first_hold    the memory-line first-that-holds lane (N's scan_mem:
                               the broken-side line, 1.0 ATR / 6 bars, known touch + 6)
  tierE__memline_oneshot_flip  its twin: the engine's one-shot memory flip
  tierE__frozen3               the frozen-3.0 twin (fully causal scale)
  tierE__oneshot_first_touch   the one-shot first-touch twin (C.retest_holds, TC10's law)
  tierE__tuning / __holdout    the scored book sliced by era of the entry CLOSE (L-1.3)

OUTPUTS
  research_outputs/tierc11/regbooks/P-BRK-4H/{scored,tierE__*}.parquet + .json,
  STATUS.json — the REGBOOK INTERFACE the scorer reads.
  research_outputs/tierc11/stage_t_brk/: STAGE_T_BRK.md (every table whole: the
  grids in §1-§11, and Appendices A-C = every candidate, every evaluated retest and
  every Tier-E regbook row), T_BRK_*.parquet (collared Tier-E tables; each row also
  carries row_kind — the scored arm's rows 'registered book (reference)', every
  other arm's 'Tier-E arm'), build_manifest.json.

REPAIR (verifier report on stage_t_brk; no rule changed, no regbook byte moved):
  row_kind on every stage table; T_BRK_INSAMPLE gains, per ridden arm, the
  disclosure cell of holdout rows acting on a death closed <= the era cut (F-6);
  the bar-316 floor disclosure (F-7); the report prints every table whole.

REPAIR 2 (final review 2026-09-25, task G4; no rule changed, no book_sha256 moved —
it covers the 16 required columns only):
  trading D-1: finding F-1 prints BOTH harvest medians — over every harvest and over
  the negative ones (it printed the all-harvest median beside the negative count);
  causality MINOR-2: every regbook row carries the EXTRA column
  anchor_scale_in_sample (R-TBRK-11: the label keyed to the death read as well as
  the known instant), counted per arm in T_BRK_ARMS (all rows and holdout rows,
  beside scale_in_sample's counts), by era in T_BRK_INSAMPLE, and printed in §11 /
  Appendix C / F-6; the sidecars are unchanged byte for byte;
  reproducibility MINOR-1: the fixtures re-derive all six STAT_COLS of every grid row.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_t_brk.py [--out-root=DIR]
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tierc11_nest as N                                             # noqa: E402  (guards first)

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

E = N.E
TP, T9, BK, TB = E.TP, E.T9, E.BK, E.TB
RC = BK.RC
iso = TP.iso

# ══════════════════════════════════════════════════════ 0 · CONSTANTS OF RECORD
ROOT = E.ROOT
REG_ID = "P-BRK-4H"
LENS = "4h"
LANE = "brk-4h"
PIN_MS = E.PIN_MS                           # 2026-09-25T00:00:00Z [L-0.1]
PIN_ISO = "2026-09-25T00:00:00Z"
ERA_CUT_MS = E.ERA_CUT_MS                   # 2024-06-30T23:59:59Z, era by CLOSE [L-1.3]
SEED = E.SEED
CARD = TP.CONTROL_CARD                      # v6 management [L-T.1]
ROLES = T9.V6_ROLES                         # tide 89/316 · window 12/89 · trigger 12/26
RIBBON = None                               # pure v6: no 12/25 bell [L-T.1]
RAIL_ATR = float(BK.MIN_STOP_ATR)           # 1.0 ATR(4h): R >= 1.0 ATR [L-T.1]
STOP_BUF_ATR = float(BK.STOP_BUF_ATR)       # 0.5 ATR(4h): "beyond" [L-T.1]
FLOOR_BARS = int(ROLES.floor_bars)          # 316: the warm-up floor per asset [L-0.1]
TAKER_BPS_SIDE = float(BK.FEE_BPS_SIDE)     # 5.0 [L-1.1]
RETEST_OF_RECORD = {"margin_atr": 1.0, "hold_bars": 3, "ttl_bars": 400}   # [L-T.1 / L-R.6]
MEM_HOLD_BARS = int(N.RC.PINS_V2["FLIP_HOLD_BARS"])                      # 6 [L-R.6(a)]
CLASSIC5 = tuple(E.CLASSIC5)
UNSEEN12 = tuple(E.UNSEEN12)
PANEL17 = tuple(E.PANEL17)
PANELS = {"CLASSIC5": CLASSIC5, "PANEL17": PANEL17}
COLLAR = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
          "gates": "nothing"}
# row_kind [repair, verifier MINOR]: the collar stays on every row of every stage
# table (the task law: every non-registered table carries it); row_kind says WHICH
# rows are cut from the registered book, so a reader filtering on the collar alone
# cannot mistake the scored arm's reference rows for a Tier-E arm.
ROW_KIND_REG = "registered book (reference)"
ROW_KIND_E = "Tier-E arm"
ROW_KIND_HAZ = "TC10 census cell (the selection hazard's source)"
ROW_KIND_PICK = "scale pick of record (SCALE_PICKS.json)"
BOOK_LABEL = "book, not a verdict"
HONESTY_LABEL = ("IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (selection_hazard: the best of 7,920 TC10 "
                 "census cells; SCALE-IN-SAMPLE: tuning-calibrated 4h scale) [L-1.4, L-R.2]")
OUT_ROOT = E.OUT                            # research_outputs/tierc11
STAGE_DIR = "stage_t_brk"
REGBOOK_DIR = ("regbooks", REG_ID)
DET_NAME = "_det_t_brk"
REPORT = "STAGE_T_BRK.md"
MANIFEST = "build_manifest.json"
SOURCE_SCRIPT = "scripts/tierc11_stage_t_brk.py"
REGS_PATH = E.OUT / "registrations" / "REGISTRATIONS.json"
REGS_SHA_OF_RECORD = "648834bf30e20e92713bddef2374ddef1aae843f4d8ba152fc50166c8cc6f1ee"
REG_SHA_OF_RECORD = "120939d9d4a2092958fcc72c25db5036e981ca5ad4f1be0b4da4f0edb9ba1655"
PICKS_PATH = N.PICKS_PATH
GRID_REL = "research_outputs/tierc10/census/outcome_grid.parquet"     # AM-1 allow-list

# the regbook interface (binding for every stage; the scorer reads ONLY this)
REQUIRED = ("symbol", "entry_ms", "entry_close_ms", "direction", "entry_px", "stop_px",
            "r_dist", "exit_close_ms", "exit_reason", "net_r", "gross_r", "fee_r",
            "funding_r", "haircut_net_r", "era", "lane")
REQ_INT = ("entry_ms", "entry_close_ms", "exit_close_ms")
REQ_I8 = ("direction",)
REQ_FLOAT = ("entry_px", "stop_px", "r_dist", "net_r", "gross_r", "fee_r", "funding_r",
             "haircut_net_r")
REQ_STR = ("symbol", "exit_reason", "era", "lane")
BOOK_KEY = ["symbol", "entry_ms"]
BOOK_SHA_LAW = ("sha256 over UTF-8 bytes of a canonical CSV: header = the 16 required columns "
                "in interface order joined by ','; rows sorted by (symbol, entry_close_ms) "
                "(mergesort); ints as str(int), direction as str(int), floats as repr(float) "
                "(full precision), strings as str; fields joined by ',', lines by '\\n', a "
                "trailing '\\n'")


@dataclasses.dataclass(frozen=True)
class Arm:
    name: str                # scored | tierE__<slug>
    kind: str                # scored | tierE
    panel: str               # CLASSIC5 | PANEL17
    scale_kind: str          # calibrated | frozen3.0
    source: str              # the range_facts prefix, or 'slice:<era>'
    era_scope: str           # full | tuning | holdout
    lane: str
    description: str


SOURCES = {                  # range_facts prefix -> (anchor, law, known_at - touch_i)
    "scan_tap89": ("tap89", "first retest that HOLDS (every qualifying touch, in bar order)", 3),
    "scan_mem": ("memory-line", "first retest that HOLDS on the broken-side memory line", 6),
    "oneshot_tap89": ("tap89", "one-shot first touch (C.retest_holds, TC10's law)", 3),
    "oneshot_mem": ("memory-line", "the engine's one-shot memory flip (leash)", 6),
}
ARMS = (
    Arm("scored", "scored", "CLASSIC5", "calibrated", "scan_tap89", "full", LANE,
        "P-BRK-4H scored arm: 4h macro death (calibrated 4h pick) -> the FIRST retest that "
        "HOLDS on tap-89 (1.0 ATR / 3 bars / ttl 400) -> entry at the touch+hold close, "
        "direction = the death direction; tide aligned at the entry bar's close; stop "
        "BK.brk_stop (retest extreme touch..entry -/+ 0.5 ATR, railed R >= 1.0 ATR(4h)); "
        "BK.ride_leg_l(ribbon=None) pure v6; one position per asset; CLASSIC5, full "
        "corridor, vs zero [L-T.1]"),
    Arm("tierE__panel17", "tierE", "PANEL17", "calibrated", "scan_tap89", "full", LANE,
        "the 17-asset view (CLASSIC5 + UNSEEN12), the scored rule unchanged; LOAO bar 9/17 "
        "(printed by the scorer, deciding nothing)"),
    Arm("tierE__memline_first_hold", "tierE", "CLASSIC5", "calibrated", "scan_mem", "full",
        "brk-4h-memline",
        "the memory-line first-that-holds lane: the dead range's broken-side memory line "
        "(as-of boundary at die_i-1), same candidacy window, hold = no close through by 1.0 "
        "ATR over touch..touch+6, entry at the touch+6 close; everything else the scored rule"),
    Arm("tierE__memline_oneshot_flip", "tierE", "CLASSIC5", "calibrated", "oneshot_mem",
        "full", "brk-4h-memflip",
        "the memory-line lane's twin: the engine's ONE-SHOT memory flip (the leash's single "
        "evaluation of the broken-side line; flip = hold), entry at the touch+6 close"),
    Arm("tierE__frozen3", "tierE", "CLASSIC5", "frozen3.0", "scan_tap89", "full",
        "brk-4h-frozen3",
        "the frozen-3.0 twin: the scored rule with the macro scale at the frozen 3.0 "
        "(fully causal scale)"),
    Arm("tierE__oneshot_first_touch", "tierE", "CLASSIC5", "calibrated", "oneshot_tap89",
        "full", "brk-4h-oneshot",
        "the one-shot first-touch twin: C.retest_holds' law (the FIRST qualifying touch gets "
        "the only evaluation; a failed first touch spends the death)"),
    Arm("tierE__tuning", "tierE", "CLASSIC5", "calibrated", "slice:tuning", "tuning", LANE,
        "the scored book's TUNING slice (entry close <= 2024-06-30T23:59:59Z) [L-1.3]"),
    Arm("tierE__holdout", "tierE", "CLASSIC5", "calibrated", "slice:holdout", "holdout", LANE,
        "the scored book's HOLDOUT slice (entry close > 2024-06-30T23:59:59Z) — the only "
        "slice whose calibrated scale is causal [L-R.2]"),
)
ARM_NAMES = tuple(a.name for a in ARMS)
RIDDEN = tuple(a for a in ARMS if not a.source.startswith("slice:"))
DISPOSITIONS = ("out_of_window", "out_of_tape", "no_atr", "tide", "no_stop", "position_open",
                "entered")
_REFUSED_KEY = {"permission": "tide", "no_atr": "no_atr", "no_stop": "no_stop",
                "out_of_tape": "out_of_tape"}
EXIT_REASONS = ("stop", "bell_12_89", "bell_89_316", "corridor_end")
ERAS = ("tuning", "holdout")
DIRS = ((1, "long"), (-1, "short"))

READINGS = (
    "R-TBRK-1 THE EVENT = N's first-retest-that-holds scan on tap89 at the calibrated 4h "
    "pick (range_facts 'scan_tap89_*' rows with verdict hold = is_first_hold), direction = "
    "the row's dir = the death's dir (top death -> +1 long), asserted against the death "
    "table; entry bar = the row's known_at (touch_i + 3), asserted.",
    "R-TBRK-2 WINDOW: TP.corridor_era(panel, 'full') (lo = the panel's first bar, hi = the "
    "pin), and per asset replay9's floor law lo_i = max(idx_range lo, 316) — L-0.1's "
    "'316-bar warm-up' (tide EMA316 unreadable before it); a hold known before the floor is "
    "'out_of_window', counted.",
    "R-TBRK-3 TIDE: BK.tide_state(EMA89, EMA316, close) of the 4h frame read AT entry_i "
    "(the entry bar's own close; three-state; aligned iff == direction). The rival (the "
    "previous 4h bar, BK.tide_4h_for_exec on a 4h exec frame) is printed per candidate as "
    "tide_prev_bar, never used.",
    "R-TBRK-4 STOP: BK.brk_stop(direction, extreme, touch_i, close[entry_i], ATR[entry_i], "
    "rail 1.0); extreme = min(low[touch_i..entry_i]) long / max(high[...]) short — "
    "band_hold_candidates' own segment; a None / non-positive R is 'no_stop', counted.",
    "R-TBRK-5 RIDE + ACCOUNTING: BK.brk_campaigns(frame, legs, TP.CONTROL_CARD, "
    "T9.V6_ROLES, lane, lo_i, hi_i, ribbon=None, era=None) = BK.ride_leg_l + BK.account_l; "
    "one position per asset (a leg whose entry bar <= the open campaign's exit bar is "
    "'position_open', counted); legs ordered (entry_i, -direction).",
    "R-TBRK-6 DISPOSITIONS: each candidate is passed ALONE through BK.legs_from_candidates "
    "(its own refusal key: permission -> 'tide', no_atr, no_stop, out_of_tape) and the "
    "per-candidate legs are asserted equal to one call over all in-window candidates.",
    "R-TBRK-7 STAMPS: entry_ms = the entry bar's OPEN (the pairing key), entry_close_ms = "
    "its close (the entry instant); exit_close_ms = the exit bar's close (BK's stamp; a "
    "stop is intrabar, so exit_event_ms = the exit bar's OPEN beside it [L-R.5]); era = "
    "E.era_of(entry_close_ms) [L-1.3].",
    "R-TBRK-8 HAIRCUT [AM-7]: haircut_net_r = net_r - fee_r x (slip_bps_side / "
    "taker_bps_side), slip = the stem's charter tier from E.fees() (A 2 / B 5 / C 10), "
    "taker = 5.0; fee_r is account_l's taker fee over every fill (entry, harvest, exit).",
    "R-TBRK-9 TIER-E ARMS each substitute ONE named element of the scored rule (panel, "
    "anchor law, scale, one-shot law) or slice the scored book by era; the 17-asset view's "
    "CLASSIC5 rows are asserted IDENTICAL to the scored book (same rule, same bars).",
    "R-TBRK-10 SCALE-IN-SAMPLE per row = range_facts' '<source>_scale_in_sample' of the "
    "row (a calibrated read at a known instant <= the era cut, or any read of a fallback "
    "pick) [L-R.2, R-LABEL]; stability_changed = the 4h pick's first-half-vs-tuning flag.",
    "R-TBRK-11 ANCHOR-SCALE-IN-SAMPLE per row (an EXTRA column; decides nothing; the "
    "interface's 16 columns and book_sha256 are untouched) = at the calibrated scale, "
    "(death close <= the era cut) OR (known close <= the era cut) OR the row's own "
    "scale_in_sample (a fallback pick's read is in-sample everywhere); False at frozen "
    "3.0 (fully causal). The row depends on the death read as well as the known-instant "
    "read, so a holdout entry acting on a death closed in the tuning era reads True here "
    "while its scale_in_sample (R-TBRK-10, keyed to the known instant) reads False; both "
    "labels and their holdout counts are printed side by side [causality MINOR-2].",
)


def _halt(msg: str) -> None:
    raise SystemExit(f"HALT: {msg}")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha_bytes(Path(p).read_bytes())


# ══════════════════════════════════════════════ 1 · THE REGISTRATION, VERIFIED
def registration() -> dict:
    """P-BRK-4H from REGISTRATIONS.json, verified: the file sha of record, the
    payload sha (the filer's law), the chain entry, the typed payload sha."""
    raw = REGS_PATH.read_bytes()
    if sha_bytes(raw) != REGS_SHA_OF_RECORD:
        _halt(f"REGISTRATIONS.json sha {sha_bytes(raw)} != of record {REGS_SHA_OF_RECORD}")
    doc = json.loads(raw)
    hit = [r for r in doc["registrations"] if r["registration"] == REG_ID]
    if len(hit) != 1:
        _halt(f"{REG_ID} appears {len(hit)} times in REGISTRATIONS.json")
    r = hit[0]
    body = {k: v for k, v in r.items() if k not in ("sha256", "text_sha256")}
    got = sha_bytes(json.dumps(body, sort_keys=True, ensure_ascii=False).encode())
    chain = [c for c in doc["chain"] if c["registration"] == REG_ID]
    if got != r["sha256"] or got != REG_SHA_OF_RECORD or len(chain) != 1 \
            or chain[0]["sha256"] != got:
        _halt(f"{REG_ID} payload sha {got} does not verify (filed {r['sha256']}, of record "
              f"{REG_SHA_OF_RECORD})")
    if sha_bytes(r["text_of_record"].encode()) != r["text_sha256"]:
        _halt(f"{REG_ID} text sha does not verify")
    spec = r["operative_spec"]
    if spec["panel"] != "CLASSIC5" or spec["era"] != "full corridor" or spec["ruler"] != "vs zero":
        _halt(f"{REG_ID} operative spec is not CLASSIC5 / full corridor / vs zero: {spec}")
    return r


# ═══════════════════════════════════════════ 2 · THE RANGE ADAPTER (runner only)
_FACTS: dict = {}


def facts(sym: str, scale_kind: str) -> dict:
    """THE ONE RANGE DOORWAY: N.range_facts(sym, '4h', scale_kind), a plain dict of
    numpy arrays (L-F.2).  Memoised per (sym, scale_kind)."""
    key = (sym, scale_kind)
    if key not in _FACTS:
        fx = N.range_facts(sym, LENS, scale_kind)
        if str(fx["lens"]) != LENS or str(fx["scale_kind"]) != scale_kind:
            _halt(f"range_facts({sym}) returned lens {fx['lens']} scale {fx['scale_kind']}")
        _FACTS[key] = fx
    return _FACTS[key]


def pins_check() -> dict:
    rp = dict(N.C.RETEST_PINS)
    got = {k: rp[k] for k in RETEST_OF_RECORD}
    if got != RETEST_OF_RECORD:
        _halt(f"C.RETEST_PINS {got} != {RETEST_OF_RECORD} [L-T.1]")
    return rp


def frame(sym: str):
    """BK's 4h LensFrame; its bars must BE the range tape's bars (index sharing is
    legal only then) — asserted once per asset against range_facts' own clock."""
    lf = BK.frame_l(sym, LENS)
    fx = facts(sym, "calibrated")
    if not (np.array_equal(lf.open_ms, fx["open_ms"]) and np.array_equal(lf.atr, fx["atr"])):
        _halt(f"{sym}: BK.frame_l 4h bars are not the range tape's bars — no index may be "
              f"shared")
    return lf


def window(sym: str, panel: str) -> tuple[int, int, dict]:
    """[R-TBRK-2] (lo_i, hi_i) on the asset's 4h frame and the panel's corridor meta."""
    lo_ms, hi_ms, meta = TP.corridor_era(PANELS[panel], "full")
    if hi_ms + 1 != PIN_MS:
        _halt(f"{panel} corridor end {iso(hi_ms + 1)} != the pin {PIN_ISO}")
    lf = frame(sym)
    lo_i, hi_i = BK.idx_range(lf.open_ms, lo_ms, hi_ms)
    lo_i = max(int(lo_i), FLOOR_BARS)
    if int(lf.close_ms[hi_i]) != PIN_MS:
        _halt(f"{sym}: last ridden bar closes {iso(int(lf.close_ms[hi_i]))}, not the pin")
    return int(lo_i), int(hi_i), meta


# ══════════════════════════════════════════════ 3 · DECISION (range-blind)
def scan_rows(fx: dict, source: str) -> pd.DataFrame:
    """Every evaluated row of one source, from the plain arrays (no N call)."""
    p = source
    n = len(fx[f"{p}_die_i"])
    seq = fx.get(f"{p}_seq", np.zeros(n, np.int64))
    return pd.DataFrame({
        "die_i": fx[f"{p}_die_i"].astype(np.int64), "rid": fx[f"{p}_rid"].astype(np.int64),
        "dir": fx[f"{p}_dir"].astype(np.int64), "seq": np.asarray(seq, np.int64),
        "touch_i": fx[f"{p}_touch_i"].astype(np.int64),
        "known_at": fx[f"{p}_known_at"].astype(np.int64),
        "retest_outcome": pd.Series(fx[f"{p}_verdict"]).map(
            {1: "hold", 0: "failed", -1: "truncated"}).to_numpy(object),
        "scale_in_sample": np.asarray(fx[f"{p}_scale_in_sample"], bool)})


def candidates(lf, fx: dict, source: str) -> list:
    """The HOLD rows of one source as BK.Candidates [R-TBRK-1, R-TBRK-4].  The
    direction is the row's (= the death's, asserted); the extreme is read from the
    RAW frame over touch_i..known_at; known_at - touch_i is the law's hold length."""
    anchor, _, H = SOURCES[source]
    rows = scan_rows(fx, source)
    die_dir = dict(zip(fx["die_i"].astype(np.int64).tolist(), fx["die_dir"].astype(np.int64).tolist()))
    out = []
    for r in rows[rows["retest_outcome"] == "hold"].itertuples(index=False):
        d, j, k = int(r.dir), int(r.touch_i), int(r.known_at)
        if die_dir.get(int(r.die_i)) != d:
            _halt(f"{lf.sym} {source}: hold at touch {j} carries dir {d}, its death "
                  f"{r.die_i} dir {die_dir.get(int(r.die_i))}")
        if k - j != H:
            _halt(f"{lf.sym} {source}: known_at {k} != touch {j} + {H}")
        if not (0 <= j <= k < lf.n):
            ext = float("nan")
        else:
            seg = slice(j, k + 1)
            ext = float(np.min(lf.l[seg])) if d == 1 else float(np.max(lf.h[seg]))
        out.append(BK.Candidate(direction=d, anchor=anchor, die_i=int(r.die_i), touch_i=j,
                                known_i=k, extreme=ext, rid=int(r.rid), verdict="hold",
                                note=f"{source} seq {int(r.seq)}"))
    return out


def tide_series(lf) -> np.ndarray:
    """[R-TBRK-3] the three-state tide of the 4h frame, per bar, read AT the bar."""
    ra = BK.roles_l(lf, ROLES)
    return BK.tide_state(ra["tide_f"], ra["tide_s"], lf.c)


def permit_of(tide: np.ndarray):
    """The permission BK.legs_from_candidates applies at the entry bar."""
    return lambda i, d: {"ok": int(tide[int(i)]) == int(d)}


def dispose(lf, cands: list, lane: str, lo_i: int, hi_i: int, tide: np.ndarray
            ) -> tuple[list, list]:
    """[R-TBRK-6] -> (legs, dispositions) — one disposition per candidate."""
    permit = permit_of(tide)
    legs, disp, inwin = [], [], []
    for cd in cands:
        if not (lo_i <= int(cd.known_i) <= hi_i):
            disp.append("out_of_window")
            continue
        inwin.append(cd)
        lg, ref = BK.legs_from_candidates(lf, [cd], lane, permit=permit, rail_atr=RAIL_ATR)
        if lg:
            legs.append(lg[0])
            disp.append("leg")
        else:
            why = [k for k, v in ref.items() if v]
            if len(why) != 1:
                _halt(f"{lf.sym}: candidate {cd} refused {ref}")
            disp.append(_REFUSED_KEY[why[0]])
    all_legs, _ = BK.legs_from_candidates(lf, inwin, lane, permit=permit, rail_atr=RAIL_ATR)
    if [dataclasses.astuple(x) for x in all_legs] != [dataclasses.astuple(x) for x in legs]:
        _halt(f"{lf.sym}: per-candidate legs differ from one legs_from_candidates call")
    return legs, disp


def ride(lf, legs: list, lo_i: int, hi_i: int, lane: str) -> list:
    """[R-TBRK-5] BK.brk_campaigns — ride_leg_l(ribbon=RIBBON) + account_l, one
    position per asset."""
    return BK.brk_campaigns(lf, legs, CARD, ROLES, lane, lo_i, hi_i, ribbon=RIBBON,
                            active=BK.COMPONENTS, era=None, account=True)


def haircut(net_r: float, fee_r: float, slip_bps_side: float) -> float:
    """[AM-7] net_r - fee_r x (slip / taker)."""
    return float(net_r) - float(fee_r) * (float(slip_bps_side) / TAKER_BPS_SIDE)


DECISION_FUNCS = ("scan_rows", "candidates", "tide_series", "permit_of", "dispose", "ride",
                  "haircut")


# ══════════════════════════════════════════════ 4 · ONE ARM
def anchor_in_sample(scale_kind: str, row_in_sample: bool, die_close_ms: int,
                     known_close_ms: int) -> bool:
    """[R-TBRK-11] the row's anchor label: at the calibrated scale, (death close <= the
    era cut) OR (known close <= the era cut) OR the row's own flag (a fallback pick);
    False at frozen 3.0.  A label, never a decision."""
    if scale_kind != "calibrated":
        return False
    return bool(row_in_sample) or int(die_close_ms) <= ERA_CUT_MS \
        or int(known_close_ms) <= ERA_CUT_MS


def trade_rows(trades: list, lf, arm: Arm, cand_info: dict, fees: dict) -> pd.DataFrame:
    rows = []
    fe = fees[lf.sym]
    for t in trades:
        ti, xi = int(t.entry_i), int(t.exit_i)
        ci = cand_info[(ti, int(t.direction), int(t.die_i))]
        d = int(t.direction)
        die_close = int(lf.close_ms[int(ci["die_i"])])
        rows.append({
            "symbol": t.symbol, "entry_ms": int(lf.open_ms[ti]),
            "entry_close_ms": int(lf.close_ms[ti]), "direction": d,
            "entry_px": float(t.entry_px), "stop_px": float(t.stop_px), "r_dist": float(t.r_dist),
            "exit_close_ms": int(lf.close_ms[xi]), "exit_reason": str(t.exit_reason),
            "net_r": float(t.net_r), "gross_r": float(t.gross_r), "fee_r": float(t.fee_r),
            "funding_r": float(t.funding_r),
            "haircut_net_r": haircut(t.net_r, t.fee_r, fe["slippage_bps_side"]),
            "era": str(E.era_of(int(lf.close_ms[ti]))), "lane": arm.lane,
            # ── extras ──
            "arm": arm.name, "anchor": ci["anchor"], "source": arm.source,
            "scale_kind": arm.scale_kind, "scale_mult": ci["scale_mult"],
            "pick_window": ci["pick_window"], "scale_in_sample": bool(ci["scale_in_sample"]),
            "anchor_scale_in_sample": anchor_in_sample(arm.scale_kind, ci["scale_in_sample"],
                                                       die_close, int(lf.close_ms[ti])),
            "stability_changed": ci["stability_changed"],
            "die_i": int(ci["die_i"]), "die_close_ms": die_close,
            "rid": int(ci["rid"]), "scan_seq": int(ci["seq"]), "touch_i": int(ci["touch_i"]),
            "touch_close_ms": int(lf.close_ms[int(ci["touch_i"])]),
            "entry_i": ti, "exit_i": xi, "exit_ms": int(lf.open_ms[xi]),
            "exit_event_ms": int(lf.open_ms[xi] if t.exit_reason == "stop" else lf.close_ms[xi]),
            "exit_event_stamp": "intrabar_open" if t.exit_reason == "stop" else "close",
            "exit_px": float(t.exit_px), "bars_held": int(t.bars_held),
            "retest_extreme": float(ci["extreme"]), "rail_binding": bool(ci["rail_binding"]),
            "atr_at_entry": float(t.atr_at_entry),
            "r_over_atr": float(t.r_dist) / float(t.atr_at_entry),
            "tide_at_entry": int(ci["tide"]), "tide_prev_bar": int(ci["tide_prev"]),
            "mfe_r": float(t.mfe_r), "mae_r": float(t.mae_r), "reached_1r": bool(t.reached_1r),
            "harvested": bool(t.harvested),
            "harvest_i": (-1 if t.harvest_i is None else int(t.harvest_i)),
            "harvest_px": (float("nan") if t.harvest_px is None else float(t.harvest_px)),
            "harvest_unit_move_r": (float("nan") if t.harvest_unit_move_r is None
                                    else float(t.harvest_unit_move_r)),
            "n_advances": int(len(t.advances)), "final_stop_px": float(t.final_stop_px),
            "funding_r_uncapped": float(t.funding_r_uncapped),
            "funding_ceiling_bound": bool(t.funding_ceiling_bound),
            "n_inactive_components": int(t.n_inactive_components),
            "slip_bps_side": float(fe["slippage_bps_side"]),
            "slippage_tier": str(fe["slippage_tier"]),
            "taker_bps_side": float(fe["taker_bps_side"]),
        })
    return pd.DataFrame(rows)


def run_arm(arm: Arm, fees: dict) -> dict:
    """Ride one arm over its panel: {book, cands, scan, tally, trades}."""
    if arm.source.startswith("slice:"):
        _halt(f"{arm.name} is a slice, not a ridden arm")
    books, cands_rows, scans, tallies, trades_all = [], [], [], [], {}
    anchor, law, H = SOURCES[arm.source]
    for sym in PANELS[arm.panel]:
        lf = frame(sym)
        fx = facts(sym, arm.scale_kind)
        lo_i, hi_i, meta = window(sym, arm.panel)
        tide = tide_series(lf)
        rows = scan_rows(fx, arm.source)
        cands = candidates(lf, fx, arm.source)
        legs, disp = dispose(lf, cands, arm.lane, lo_i, hi_i, tide)
        trades = ride(lf, legs, lo_i, hi_i, arm.lane)
        entered = {(int(t.entry_i), int(t.direction), int(t.die_i)) for t in trades}
        leg_of = {(int(L.entry_i), int(L.direction), int(L.die_i)): L for L in legs}
        if len(entered) != len(trades) or len(leg_of) != len(legs):
            _halt(f"{sym} {arm.name}: (entry_i, direction, die_i) is not a unique leg key")
        disp = [("entered" if (int(c.known_i), int(c.direction), int(c.die_i)) in entered
                 else "position_open") if x == "leg" else x for c, x in zip(cands, disp)]
        hold = rows[rows["retest_outcome"] == "hold"].reset_index(drop=True)
        if len(hold) != len(cands):
            _halt(f"{sym} {arm.name}: {len(hold)} hold rows vs {len(cands)} candidates")
        lab = N.scale_label(sym, LENS, arm.scale_kind)
        info = {}
        for c, x, hr in zip(cands, disp, hold.itertuples(index=False)):
            ti, d = int(c.known_i), int(c.direction)
            L = leg_of.get((ti, d, int(c.die_i)))
            rec = {"arm": arm.name, "symbol": sym, "die_i": int(c.die_i), "rid": int(c.rid),
                   "direction": d, "seq": int(hr.seq), "touch_i": int(c.touch_i),
                   "entry_i": ti, "entry_close_ms": (int(lf.close_ms[ti]) if ti < lf.n else -1),
                   "extreme": float(c.extreme), "disposition": x,
                   "tide": int(tide[ti]) if ti < lf.n else 0,
                   "tide_prev": int(tide[ti - 1]) if 0 < ti <= lf.n else 0,
                   "scale_in_sample": bool(hr.scale_in_sample),
                   "stop_px": (float(L.stop_px) if L is not None else float("nan")),
                   "r_dist": (float(L.r_dist) if L is not None else float("nan")),
                   "rail_binding": (bool(L.rail_binding) if L is not None else False),
                   "anchor": anchor, "scale_mult": float(np.asarray(fx["scale_mult"])),
                   "pick_window": str(lab["pick_window"]),
                   "stability_changed": (None if lab["stability_changed"] is None
                                         else bool(lab["stability_changed"]))}
            cands_rows.append(rec)
            if x == "entered":
                info[(ti, d, int(c.die_i))] = rec
        bk = trade_rows(trades, lf, arm, info, fees)
        if len(bk):
            books.append(bk)
        trades_all[sym] = trades
        sr = rows.copy()
        sr.insert(0, "symbol", sym)
        sr.insert(0, "arm", arm.name)
        sr["known_close_ms"] = np.where(sr["known_at"] < lf.n,
                                        lf.close_ms[np.minimum(sr["known_at"], lf.n - 1)], -1)
        scans.append(sr)
        cnt = {k: int(sum(1 for x in disp if x == k)) for k in DISPOSITIONS}
        tallies.append({"arm": arm.name, "symbol": sym, "lo_i": lo_i, "hi_i": hi_i,
                        "floor_open_ms": int(lf.open_ms[lo_i]),
                        "n_deaths": int(len(fx["die_i"])),
                        "n_rows_evaluated": int(len(rows)),
                        "n_hold": int((rows["retest_outcome"] == "hold").sum()),
                        "n_failed": int((rows["retest_outcome"] == "failed").sum()),
                        "n_truncated": int((rows["retest_outcome"] == "truncated").sum()),
                        "n_hold_after_failed_touch": int(((rows["retest_outcome"] == "hold")
                                                          & (rows["seq"] > 0)).sum()),
                        "n_candidates": len(cands), **{f"n_{k}": v for k, v in cnt.items()},
                        "n_trades": len(trades)})
        if cnt["entered"] != len(trades):
            _halt(f"{sym} {arm.name}: entered {cnt['entered']} != trades {len(trades)}")
    book = (pd.concat(books, ignore_index=True) if books else trade_rows([], None, arm, {}, fees))
    book = sort_book(book)
    return {"arm": arm, "book": book, "cands": pd.DataFrame(cands_rows),
            "scan": pd.concat(scans, ignore_index=True), "tally": pd.DataFrame(tallies),
            "trades": trades_all}


def sort_book(df: pd.DataFrame) -> pd.DataFrame:
    if not len(df):
        return df
    return df.sort_values(["symbol", "entry_close_ms"], kind="mergesort").reset_index(drop=True)


def typed_book(df: pd.DataFrame) -> pd.DataFrame:
    """The regbook dtypes of the interface."""
    d = df.copy()
    for c in REQ_INT:
        d[c] = d[c].astype(np.int64)
    d["direction"] = d["direction"].astype(np.int8)
    for c in REQ_FLOAT:
        d[c] = d[c].astype(np.float64)
    for c in REQ_STR:
        d[c] = d[c].astype(str)
    return d


# ══════════════════════════════════════════════ 5 · THE REGBOOK INTERFACE
def canonical_csv(df: pd.DataFrame) -> bytes:
    """[BOOK_SHA_LAW] the bytes book_sha256 is taken over."""
    d = df.sort_values(["symbol", "entry_close_ms"], kind="mergesort")
    lines = [",".join(REQUIRED)]
    cols = [d[c].tolist() for c in REQUIRED]
    for vals in zip(*cols):
        out = []
        for c, v in zip(REQUIRED, vals):
            if c in REQ_FLOAT:
                out.append(repr(float(v)))
            elif c in REQ_INT or c in REQ_I8:
                out.append(str(int(v)))
            else:
                out.append(str(v))
        lines.append(",".join(out))
    return ("\n".join(lines) + "\n").encode("utf-8")


def book_sha256(df: pd.DataFrame) -> str:
    return sha_bytes(canonical_csv(df))


def fsum(x) -> float:
    return float(math.fsum(float(v) for v in x))


def sidecar(arm: Arm, df: pd.DataFrame) -> dict:
    """The sidecar JSON of the interface (+ an 'extra' block)."""
    kind = arm.kind
    out = {"registration": REG_ID, "arm": arm.name, "kind": kind, "ruler": "vs_zero",
           "panel": list(PANELS[arm.panel]), "era_scope": arm.era_scope, "n": int(len(df)),
           "sum_net_r": fsum(df["net_r"]) if len(df) else 0.0,
           "book_sha256": book_sha256(df), "description": arm.description,
           "source_script": SOURCE_SCRIPT}
    if kind == "tierE":
        out.update(COLLAR)
        out["tier"] = "TIER-E"
    out["extra"] = {
        "as_of_last_closed_4h": PIN_ISO, "lens": LENS, "lane": arm.lane,
        "scale_kind": arm.scale_kind, "source": arm.source,
        "panel_name": arm.panel, "loao_bar_above_half": ("9/17" if arm.panel == "PANEL17"
                                                         else "3/5"),
        "book_sha_law": BOOK_SHA_LAW, "key": BOOK_KEY,
        "haircut_law": "AM-7: haircut_net_r = net_r - fee_r x (slip_bps_side / 5.0)",
        "sum_haircut_net_r": fsum(df["haircut_net_r"]) if len(df) else 0.0,
        "label": (BOOK_LABEL if kind == "scored" else COLLAR["selection_not_a_result"]),
    }
    if kind == "scored":
        out["extra"]["honesty_label_required"] = HONESTY_LABEL
    return out


# ══════════════════════════════════════════════ 6 · TABLES (Tier-E, collared)
def stats(df: pd.DataFrame) -> dict:
    n = int(len(df))
    if not n:
        return {"n": 0, "sum_net_r": 0.0, "mean_net_r": float("nan"), "p_win": float("nan"),
                "sum_haircut_net_r": 0.0, "mean_haircut_net_r": float("nan")}
    s = fsum(df["net_r"])
    sh = fsum(df["haircut_net_r"])
    return {"n": n, "sum_net_r": s, "mean_net_r": s / n,
            "p_win": float((df["net_r"] > 0).mean()), "sum_haircut_net_r": sh,
            "mean_haircut_net_r": sh / n}


def collar(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    for k, v in COLLAR.items():
        d[k] = v
    return d


def asof(df: pd.DataFrame, panel: str) -> pd.DataFrame:
    """TP.stamp_n: the as-of warranty columns of the panel's corridor."""
    _, _, meta = TP.corridor_era(PANELS[panel], "full")
    return TP.stamp_n(df, meta, LENS)


def arm_books(runs: dict) -> dict:
    """{arm name: book} — the ridden arms plus the two era slices of the scored."""
    out = {a.name: runs[a.name]["book"] for a in RIDDEN}
    sc = runs["scored"]["book"]
    for a in ARMS:
        if a.source.startswith("slice:"):
            era = a.source.split(":", 1)[1]
            b = sc[sc["era"] == era].copy()
            b["arm"] = a.name
            out[a.name] = b.reset_index(drop=True)
    return out


def grid_tables(books: dict) -> dict:
    """The whole grids: arm summary; arm x asset; arm x era; arm x exit reason;
    arm x direction — every declared cell present, n = 0 included."""
    summ = []
    for a in ARMS:
        b = books[a.name]
        summ.append({"cell": a.name, "arm": a.name, "kind": a.kind, "panel": a.panel,
                     "scale_kind": a.scale_kind, "source": a.source, "era_scope": a.era_scope,
                     "lane": a.lane, **stats(b),
                     "n_long": int((b["direction"] == 1).sum()) if len(b) else 0,
                     "n_short": int((b["direction"] == -1).sum()) if len(b) else 0,
                     "n_scale_in_sample": int(b["scale_in_sample"].sum()) if len(b) else 0,
                     "n_anchor_scale_in_sample": (int(b["anchor_scale_in_sample"].sum())
                                                  if len(b) else 0),
                     "n_holdout_scale_in_sample": (int((b["scale_in_sample"]
                                                        & (b["era"] == "holdout")).sum())
                                                   if len(b) else 0),
                     "n_holdout_anchor_scale_in_sample": (
                         int((b["anchor_scale_in_sample"] & (b["era"] == "holdout")).sum())
                         if len(b) else 0),
                     "book_sha256": book_sha256(b)})
    asset, era, exitg, dirg = [], [], [], []
    for a in RIDDEN:
        b = books[a.name]
        for s in PANELS[a.panel]:
            asset.append({"cell": f"{a.name}|{s}", "arm": a.name, "symbol": s,
                          **stats(b[b["symbol"] == s] if len(b) else b)})
        for e in ERAS:
            era.append({"cell": f"{a.name}|{e}", "arm": a.name, "era": e,
                        **stats(b[b["era"] == e] if len(b) else b)})
        for x in EXIT_REASONS:
            exitg.append({"cell": f"{a.name}|{x}", "arm": a.name, "exit_reason": x,
                          **stats(b[b["exit_reason"] == x] if len(b) else b)})
        for d, nm in DIRS:
            dirg.append({"cell": f"{a.name}|{nm}", "arm": a.name, "side": nm,
                         **stats(b[b["direction"] == d] if len(b) else b)})
    return {"T_BRK_ARMS": pd.DataFrame(summ), "T_BRK_ASSET_GRID": pd.DataFrame(asset),
            "T_BRK_ERA_GRID": pd.DataFrame(era), "T_BRK_EXIT_GRID": pd.DataFrame(exitg),
            "T_BRK_DIR_GRID": pd.DataFrame(dirg)}


def declared_cells() -> dict:
    """The declared cell lists (the fixture types its own; this is the builder's)."""
    return {
        "T_BRK_ARMS": list(ARM_NAMES),
        "T_BRK_ASSET_GRID": [f"{a.name}|{s}" for a in RIDDEN for s in PANELS[a.panel]],
        "T_BRK_ERA_GRID": [f"{a.name}|{e}" for a in RIDDEN for e in ERAS],
        "T_BRK_EXIT_GRID": [f"{a.name}|{x}" for a in RIDDEN for x in EXIT_REASONS],
        "T_BRK_DIR_GRID": [f"{a.name}|{nm}" for a in RIDDEN for _, nm in DIRS],
        "T_BRK_TALLY": [f"{a.name}|{s}" for a in RIDDEN for s in PANELS[a.panel]],
    }


def hazard_rows() -> pd.DataFrame:
    """The selection hazard's figures, re-read from TC10's outcome grid (AM-1: the
    source of P-BRK-4H's selection-hazard figures): 4h retest-hold-tap89, frozen
    3.0, H20, POOLED:CLASSIC5 / POOLED:UNSEEN12 x ALL / tuning / holdout."""
    g = pd.read_parquet(str(E.tc10_record(GRID_REL)))
    sel = g[(g["lens"] == "4h") & (g["cls"] == "retest-hold-tap89")
            & (g["scale_kind"] == "frozen3.0") & (g["horizon"] == "H20")
            & (g["asset"].isin(["POOLED:CLASSIC5", "POOLED:UNSEEN12"]))]
    cols = ["asset", "lens", "cls", "scale_kind", "era", "horizon", "n", "median_term",
            "toll_atr", "net"] + list(TP.AS_OF_COLUMNS)     # TC10's OWN as-of warranty
    d = sel[cols].copy()
    d["era"] = pd.Categorical(d["era"], ["ALL", "tuning", "holdout"], ordered=True)
    d = d.sort_values(["asset", "era"]).reset_index(drop=True)
    d["era"] = d["era"].astype(str)
    d["n_cells_in_grid"] = int(len(g))
    d["cell"] = d["asset"] + "|" + d["era"]
    d["source"] = GRID_REL + " (TC10, AM-1 allow-list)"
    return d


def picks_rows() -> pd.DataFrame:
    """The 4h scale picks of the 17 (SCALE_PICKS.json, the pins) [L-R.2]."""
    rec = N.picks()
    by = {(c["asset"], c["lens"]): c for c in rec["cells"]}
    rows = []
    for s in PANEL17:
        c = by[(s, LENS)]
        rows.append({"cell": s, "symbol": s, "panel": "CLASSIC5" if s in CLASSIC5 else "UNSEEN12",
                     "pick_of_record": float(c["pick_of_record"]),
                     "pick_window": c["pick_window"], "tuning_pick": c.get("tuning_pick"),
                     "whole_tape_pick": float(c["whole_tape_pick"]),
                     "first_half_pick": c.get("first_half_pick"),
                     "frozen_scale": float(c["frozen_scale"]),
                     "stable_first_half_vs_tuning": c.get("stable_first_half_vs_tuning"),
                     "in_sample_tuning": bool(c["in_sample_tuning"]),
                     "in_sample_holdout": bool(c["in_sample_holdout"]),
                     "label": c["label"],
                     "scale_of_calibrated": N.scale_of(s, LENS, "calibrated")})
    d = pd.DataFrame(rows)
    for k in ("tuning_pick", "first_half_pick"):
        d[k] = pd.to_numeric(d[k], errors="coerce").astype(float)
    d["stable_first_half_vs_tuning"] = d["stable_first_half_vs_tuning"].astype("boolean")
    return d


def insample_rows(books: dict) -> pd.DataFrame:
    """SCALE-IN-SAMPLE [L-R.2]: the scored book by the row's in-sample flag and era,
    then by its anchor label (R-TBRK-11) and era beside it, with the holdout slice and
    the frozen-3.0 twin beside; then, per ridden arm, the
    DISCLOSURE cell of holdout rows (era by the entry close) whose death closed at
    or before the era cut — the per-row flag is read at the entry instant
    (R-TBRK-10), so these rows read False while acting on a death the calibrated
    machine detected inside the tuning era.  Era membership [L-1.3] is unchanged."""
    sc = books["scored"]
    rows = []
    for flag in (True, False):
        for e in ERAS:
            b = sc[(sc["scale_in_sample"] == flag) & (sc["era"] == e)]
            rows.append({"cell": f"scored|in_sample={flag}|{e}", "arm": "scored",
                         "slice": "in-sample flag x era", "scale_in_sample": flag,
                         "anchor_scale_in_sample": None, "era": e, **stats(b)})
    # [R-TBRK-11, causality MINOR-2] the anchor label's cells, beside the flag's
    for flag in (True, False):
        for e in ERAS:
            b = sc[(sc["anchor_scale_in_sample"] == flag) & (sc["era"] == e)]
            rows.append({"cell": f"scored|anchor_in_sample={flag}|{e}", "arm": "scored",
                         "slice": "anchor in-sample label (R-TBRK-11) x era",
                         "scale_in_sample": None, "anchor_scale_in_sample": flag, "era": e,
                         **stats(b)})
    for nm in ("tierE__holdout", "tierE__frozen3"):
        rows.append({"cell": f"{nm}|beside", "arm": nm, "slice": "beside",
                     "scale_in_sample": None, "anchor_scale_in_sample": None, "era": "all",
                     **stats(books[nm])})
    for a in RIDDEN:
        b = books[a.name]
        m = (b["era"] == "holdout") & (b["die_close_ms"] <= ERA_CUT_MS)
        rows.append({"cell": f"{a.name}|holdout|death_close<=cut", "arm": a.name,
                     "slice": "holdout entry acting on a death closed <= the era cut "
                              "(disclosure)",
                     "scale_in_sample": None, "anchor_scale_in_sample": None, "era": "holdout",
                     **stats(b[m])})
    d = pd.DataFrame(rows)
    d["scale_in_sample"] = d["scale_in_sample"].astype("boolean")
    d["anchor_scale_in_sample"] = d["anchor_scale_in_sample"].astype("boolean")
    return d


def row_kind(df: pd.DataFrame, table: str) -> pd.DataFrame:
    """[ROW_KIND_*] the row's kind: the scored arm's rows are the registered book's
    reference rows; every other arm's row is a Tier-E arm's."""
    d = df.copy()
    if table == "T_BRK_HAZARD":
        d["row_kind"] = ROW_KIND_HAZ
    elif table == "T_BRK_PICKS":
        d["row_kind"] = ROW_KIND_PICK
    else:
        d["row_kind"] = np.where(d["arm"].to_numpy(object) == "scored", ROW_KIND_REG,
                                 ROW_KIND_E).astype(object)
    return d


# ══════════════════════════════════════════════ 7 · BUILD
DET_ROOT = OUT_ROOT / STAGE_DIR / DET_NAME
STAGE_TABLES = ("T_BRK_ARMS", "T_BRK_ASSET_GRID", "T_BRK_ERA_GRID", "T_BRK_EXIT_GRID",
                "T_BRK_DIR_GRID", "T_BRK_TALLY", "T_BRK_CANDIDATES", "T_BRK_SCAN",
                "T_BRK_HAZARD", "T_BRK_PICKS", "T_BRK_INSAMPLE")
TABLE_KEYS = {"T_BRK_ARMS": ["cell"], "T_BRK_ASSET_GRID": ["cell"], "T_BRK_ERA_GRID": ["cell"],
              "T_BRK_EXIT_GRID": ["cell"], "T_BRK_DIR_GRID": ["cell"], "T_BRK_TALLY": ["cell"],
              "T_BRK_CANDIDATES": ["arm", "symbol", "die_i", "touch_i"],
              "T_BRK_SCAN": ["arm", "symbol", "die_i", "seq"],
              "T_BRK_HAZARD": ["cell"], "T_BRK_PICKS": ["cell"], "T_BRK_INSAMPLE": ["cell"]}
REGBOOK_FILES = tuple(f"{a.name}.{x}" for a in ARMS for x in ("parquet", "json")) + ("STATUS.json",)
STAGE_FILES = tuple(f"{t}.parquet" for t in STAGE_TABLES) + (REPORT, MANIFEST)


def compute() -> dict:
    reg = registration()
    rp = pins_check()
    fees = E.fees()
    for s in PANEL17:
        if float(fees[s]["taker_bps_side"]) != TAKER_BPS_SIDE:
            _halt(f"{s}: taker {fees[s]['taker_bps_side']} != BK.FEE_BPS_SIDE {TAKER_BPS_SIDE}")
    runs = {a.name: run_arm(a, fees) for a in RIDDEN}
    # R-TBRK-9: the 17-asset view's CLASSIC5 rows ARE the scored book
    p17 = runs["tierE__panel17"]["book"]
    c5 = p17[p17["symbol"].isin(CLASSIC5)].reset_index(drop=True)
    if book_sha256(c5) != book_sha256(runs["scored"]["book"]):
        _halt("the 17-asset view's CLASSIC5 rows differ from the scored book")
    for a in RIDDEN:                    # R-TBRK-11: the anchor label never narrows the flag
        b = runs[a.name]["book"]
        if bool((b["scale_in_sample"] & ~b["anchor_scale_in_sample"]).any()):
            _halt(f"{a.name}: a row is scale_in_sample but not anchor_scale_in_sample")
        if a.scale_kind != "calibrated" and bool(b["anchor_scale_in_sample"].any()):
            _halt(f"{a.name}: an anchor in-sample row at {a.scale_kind}")
    books = arm_books(runs)
    tables = grid_tables(books)
    tables["T_BRK_TALLY"] = pd.concat([runs[a.name]["tally"] for a in RIDDEN], ignore_index=True)
    tables["T_BRK_TALLY"].insert(0, "cell", tables["T_BRK_TALLY"]["arm"] + "|"
                                 + tables["T_BRK_TALLY"]["symbol"])
    tables["T_BRK_CANDIDATES"] = pd.concat([runs[a.name]["cands"] for a in RIDDEN],
                                           ignore_index=True)
    tables["T_BRK_SCAN"] = pd.concat([runs[a.name]["scan"] for a in RIDDEN], ignore_index=True)
    tables["T_BRK_HAZARD"] = hazard_rows()
    tables["T_BRK_PICKS"] = picks_rows()
    tables["T_BRK_INSAMPLE"] = insample_rows(books)
    return {"reg": reg, "retest_pins": rp, "fees": fees, "runs": runs, "books": books,
            "tables": tables}


def _inside(p: Path, root: Path) -> bool:
    return p == root or root in p.parents


def guard_out_root(out_root: Path) -> Path:
    """E.OUT (the record); a direct child of DET_ROOT; or a direct child of a
    `_det_t_brk/` directory OUTSIDE the repo tree (a fixture scratch)."""
    o = Path(out_root).resolve()
    if o == OUT_ROOT.resolve() or o.parent == DET_ROOT.resolve():
        return o
    trees = {ROOT.resolve(), Path(E.MAIN_TREE).resolve()}
    if o.parent.name == DET_NAME and not any(_inside(o, t) for t in trees):
        return o
    _halt(f"output root {o} is neither {OUT_ROOT}, a run dir under {DET_ROOT}, nor one under "
          f"a {DET_NAME}/ scratch outside the repo")
    return o


def write_parquet(df: pd.DataFrame, path: Path) -> str:
    """pandas on a path STRING (AM-2), atomically; returns the content sha."""
    path.parent.mkdir(parents=True, exist_ok=True)
    d = df.reset_index(drop=True).copy()
    d.attrs = {}
    d.columns = [str(c) for c in d.columns]
    tmp = path.with_name(path.name + ".tmp")
    d.to_parquet(str(tmp), index=False)
    os.replace(str(tmp), str(path))
    return TB._content_sha(d)


def write_json(obj, path: Path) -> bytes:
    b = (json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, default=str)
         + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b)
    return b


def assert_key(df: pd.DataFrame, key: list, label: str) -> None:
    dup = int(df.duplicated(subset=key).sum()) if len(df) else 0
    if dup:
        _halt(f"{label}: key {key} has {dup} duplicate row(s)")
    if len(df) and df[key].isna().any().any():
        _halt(f"{label}: a null in key {key}")


def regbook_frame(arm: Arm, book: pd.DataFrame) -> pd.DataFrame:
    d = typed_book(book) if len(book) else book
    d = asof(d, arm.panel) if len(d) else d
    if arm.kind == "tierE" and len(d):
        d = collar(d)
    return d


def build(out_root: Path = OUT_ROOT) -> dict:
    out_root = guard_out_root(out_root)
    R = compute()
    sdir = out_root / STAGE_DIR
    rdir = out_root.joinpath(*REGBOOK_DIR)
    sdir.mkdir(parents=True, exist_ok=True)
    rdir.mkdir(parents=True, exist_ok=True)
    content, sides = {}, {}
    for a in ARMS:
        b = R["books"][a.name]
        if not len(b):
            _halt(f"{a.name}: an empty book")
        assert_key(b, BOOK_KEY, a.name)
        d = regbook_frame(a, b)
        if d[list(REQUIRED)].isna().any().any():
            _halt(f"{a.name}: a null in a required column")
        content[f"regbooks/{REG_ID}/{a.name}.parquet"] = write_parquet(d, rdir / f"{a.name}.parquet")
        sc = sidecar(a, d)
        sides[a.name] = sc
        write_json(sc, rdir / f"{a.name}.json")
    status = {"registration": REG_ID, "status": "BUILT",
              "reason": ("P-BRK-4H's scored arm and seven Tier-E books (the registration's "
                         "six tier_e_arms; the memory-line lane carries its engine one-shot "
                         "twin as its own book) built over the TC11 corridor; no precondition "
                         "or condition applies (vs zero, full corridor) [L-T.1]"),
              "arms": list(ARM_NAMES)}
    write_json(status, rdir / "STATUS.json")
    R["written"] = {}
    for t in STAGE_TABLES:
        df = R["tables"][t]
        assert_key(df, TABLE_KEYS[t], t)
        if t == "T_BRK_HAZARD":
            d = df.copy()               # TC10's figures keep TC10's as-of (2026-09-21T16:00Z)
        elif t == "T_BRK_PICKS":
            d = asof(df, "PANEL17")
        elif t == "T_BRK_TALLY" or t == "T_BRK_CANDIDATES" or t == "T_BRK_SCAN":
            parts = []
            for a in RIDDEN:
                g = df[df["arm"] == a.name]
                if len(g):
                    parts.append(asof(g, a.panel))
            d = pd.concat(parts, ignore_index=True)
        else:
            d = asof(df, "CLASSIC5")
        d = collar(row_kind(d, t))
        R["written"][t] = d
        content[f"{STAGE_DIR}/{t}.parquet"] = write_parquet(d, sdir / f"{t}.parquet")
    man = manifest(R, content, sides)
    write_json(man, sdir / MANIFEST)
    (sdir / REPORT).write_bytes(render_md(R, sides, man).encode("utf-8"))
    R["manifest"], R["sidecars"], R["content"] = man, sides, content
    return R


def manifest(R: dict, content: dict, sides: dict) -> dict:
    inputs = {"research_outputs/tierc11/registrations/REGISTRATIONS.json": sha_file(REGS_PATH),
              "research_outputs/tierc11/ranges/SCALE_PICKS.json": sha_file(PICKS_PATH),
              "research_outputs/tierc11/data/fee_schedule.json":
                  sha_file(E.OUT / "data" / "fee_schedule.json"),
              SOURCE_SCRIPT: sha_file(ROOT / SOURCE_SCRIPT),
              "scripts/tierc11_nest.py": sha_file(ROOT / "scripts" / "tierc11_nest.py"),
              "scripts/tierc11_env.py": sha_file(ROOT / "scripts" / "tierc11_env.py"),
              "scripts/tierc10_brk.py": sha_file(ROOT / "scripts" / "tierc10_brk.py")}
    return {
        "tier": "TIER-C11", "stage": "TC11-T (T-brk)", "registration": REG_ID,
        "registration_sha256": R["reg"]["sha256"], "seed": SEED,
        "as_of": PIN_ISO, "as_of_close_ms": PIN_MS, "substrate": E.SNAPSHOT.name,
        "retest_pins": {k: R["retest_pins"][k] for k in sorted(R["retest_pins"])},
        "arms": {a.name: {"n": sides[a.name]["n"], "sum_net_r": sides[a.name]["sum_net_r"],
                          "book_sha256": sides[a.name]["book_sha256"], "kind": a.kind,
                          "panel": a.panel, "era_scope": a.era_scope} for a in ARMS},
        "content_sha": dict(sorted(content.items())),
        "keys": {**{f"regbooks/{REG_ID}/{a.name}.parquet": BOOK_KEY for a in ARMS},
                 **{f"{STAGE_DIR}/{t}.parquet": TABLE_KEYS[t] for t in STAGE_TABLES}},
        "files": {"regbooks": list(REGBOOK_FILES), "stage": list(STAGE_FILES)},
        "input_sha": inputs,
        "book_sha_law": BOOK_SHA_LAW,
        "collar": COLLAR,
        "readings": list(READINGS),
    }


# ══════════════════════════════════════════════ 8 · THE REPORT (every table whole)
def _f(x, nd: int = 6) -> str:
    if x is None or x is pd.NA or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    if isinstance(x, (bool, np.bool_)):
        return str(bool(x))
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if isinstance(x, (float, np.floating)):
        return f"{float(x):+.{nd}f}"
    return str(x)


def md_table(df: pd.DataFrame, cols: list, collared: bool = True) -> str:
    cols = list(cols) + (list(COLLAR) if collared else [])
    L = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in df.itertuples(index=False):
        rd = r._asdict()
        L.append("| " + " | ".join(_f(rd[c]) if c not in COLLAR else COLLAR[c]
                                   for c in cols) + " |")
    return "\n".join(L)


STAT_COLS = ["n", "sum_net_r", "mean_net_r", "p_win", "sum_haircut_net_r", "mean_haircut_net_r"]


def render_md(R: dict, sides: dict, man: dict) -> str:
    reg, T, books = R["reg"], R["tables"], R["books"]
    W = R["written"]                    # the stage tables AS WRITTEN (row_kind + collar)
    spec = reg["operative_spec"]
    sc = sides["scored"]
    L = ["as_of_last_closed_4h: 2026-09-25T00:00:00Z", "",
         "# TIER-C11 · STAGE T-brk — P-BRK-4H, the 4h breakout-retest lane", "",
         f"Registration {REG_ID} (seq {reg['seq']}, prior {reg['prior_pct']}%), payload sha "
         f"`{reg['sha256']}` verified. Contract `exchange/queue/2026-09-24_TC11_APOLLO.md` "
         f"(sha bb38e016…). Readings: L-T.1, L-R.6(a), L-R.2, L-1.4, L-1.3, AM-1, AM-7. Seed "
         f"{SEED} (nothing drawn here). Substrate {E.SNAPSHOT.name}; corridor CLASSIC5 "
         f"2019-09-08T16:00Z → {PIN_ISO}, per-asset floor bar 316.", "",
         "Text of record (the contract's own lines):", "", "```",
         reg["text_of_record"], "```", "",
         "## 1 · The registered book (scored arm) — " + BOOK_LABEL, "",
         "No CI, no p, no verdict word here: the scorer (`scripts/tierc11_score.py`) reads the "
         "regbook. These are the book's own sums.", ""]
    s0 = stats(books["scored"])
    L.append("| registration | arm | ruler | panel | era_scope | n | sum_net_r | mean_net_r | "
             "p_win | sum_haircut_net_r | mean_haircut_net_r | book_sha256 | label |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    L.append(f"| {REG_ID} | scored | vs_zero | CLASSIC5 | full | {s0['n']} | "
             f"{_f(s0['sum_net_r'])} | {_f(s0['mean_net_r'])} | {_f(s0['p_win'])} | "
             f"{_f(s0['sum_haircut_net_r'])} | {_f(s0['mean_haircut_net_r'])} | "
             f"`{sc['book_sha256']}` | {BOOK_LABEL} |")
    L += ["", f"Per L-1.4 the §0 cell of {REG_ID} carries the honesty label: \"<scorer's word> — "
          f"{HONESTY_LABEL}\"; the family bar applies unchanged and the row is never cited as "
          f"confirmation.", "",
          "## 2 · SELECTION HAZARD [L-1.4] — printed with the book", "",
          f"> selection_hazard (registration text): {spec['selection_hazard']}", "",
          "The hazard's figures re-read from TC10's filed census grid (AM-1 allow-list; TC10's "
          "own as-of 2026-09-21T16:00Z, carried on the rows; frozen 3.0, one-shot "
          "retest-hold-tap89, H20 event outcomes — not a trade book; NET = median term − toll, "
          "ATR units). "
          "The scored event differs from the cell that was selected (first-HOLD scan, "
          "tuning-calibrated scale).", "",
          md_table(W["T_BRK_HAZARD"], ["asset", "era", "horizon", "n", "median_term",
                                       "toll_atr", "net", "n_cells_in_grid",
                                       "as_of_last_closed_4h", "row_kind"]), "",
          "## 3 · SCALE-IN-SAMPLE [L-R.2] — printed with the book", "",
          f"> scale_in_sample (registration text): {spec['scale_in_sample']}", "",
          "4h scale picks (SCALE_PICKS.json, the pins; CLASSIC5 of record, UNSEEN12 for the "
          "17-asset view):", "",
          md_table(W["T_BRK_PICKS"], ["symbol", "panel", "pick_of_record", "pick_window",
                                      "tuning_pick", "whole_tape_pick", "first_half_pick",
                                      "frozen_scale", "stable_first_half_vs_tuning",
                                      "in_sample_holdout", "row_kind"]), "",
          "The scored book by the row's in-sample flag (a calibrated range read at an instant "
          "≤ the era cut is structurally in-sample) and era; then by the row's ANCHOR label "
          "(anchor_scale_in_sample, R-TBRK-11: the death read's instant as well as the known "
          "instant) and era, beside it; with the holdout slice (the only slice with a causal "
          "scale) and the frozen-3.0 twin (fully causal) beside; then, per ridden arm, the "
          "DISCLOSURE cell of holdout rows whose death closed at or before the era cut (the "
          "per-row flag is read at the entry instant, R-TBRK-10, so these rows read False "
          "there and True on the anchor label; era by the entry close is unchanged, L-1.3 — "
          "see F-6):", "",
          md_table(W["T_BRK_INSAMPLE"], ["cell", "slice", "scale_in_sample",
                                         "anchor_scale_in_sample", "era"] + STAT_COLS
                   + ["row_kind"]), "",
          "## 4 · Tier-E arms — a SELECTION, not a result (no verdict word)", "",
          "The scored arm's row is the reference row of this Tier-E table (row_kind "
          f"'{ROW_KIND_REG}'); its registered form is §1 and its result is the scorer's. The "
          "collar is the table's: a split or a side-by-side of the registered book is a "
          "selection view, not the registered result.", "",
          md_table(W["T_BRK_ARMS"], ["arm", "panel", "scale_kind", "source", "era_scope", "lane"]
                   + STAT_COLS + ["n_long", "n_short", "n_scale_in_sample",
                                  "n_anchor_scale_in_sample", "n_holdout_scale_in_sample",
                                  "n_holdout_anchor_scale_in_sample", "row_kind"]), "",
          "Arm descriptions:", ""]
    for a in ARMS:
        L.append(f"- `{a.name}` ({a.kind}): {a.description}")
    L += ["", "## 5 · Grids, whole (every declared cell, n = 0 included)", "",
          "### 5a · arm × asset", "",
          md_table(W["T_BRK_ASSET_GRID"], ["arm", "symbol"] + STAT_COLS + ["row_kind"]), "",
          "### 5b · arm × era (era of the entry CLOSE; the slice arms are the scored arm's "
          "two era cells)", "",
          md_table(W["T_BRK_ERA_GRID"], ["arm", "era"] + STAT_COLS + ["row_kind"]), "",
          "### 5c · arm × exit reason", "",
          md_table(W["T_BRK_EXIT_GRID"], ["arm", "exit_reason"] + STAT_COLS + ["row_kind"]), "",
          "### 5d · arm × side", "",
          md_table(W["T_BRK_DIR_GRID"], ["arm", "side"] + STAT_COLS + ["row_kind"]), "",
          "## 6 · The scan and the dispositions (arm × asset, whole)", "",
          "deaths = macro deaths on the asset's 4h tape at the arm's scale; rows = evaluated "
          "retests; hold_after_failed = first holds found after a failed touch (the first-"
          "that-holds scan's own rescues); candidates = holds; then each candidate's single "
          "disposition.", "",
          md_table(W["T_BRK_TALLY"], ["arm", "symbol", "n_deaths", "n_rows_evaluated", "n_hold",
                                      "n_failed", "n_truncated", "n_hold_after_failed_touch",
                                      "n_candidates", "n_out_of_window", "n_out_of_tape",
                                      "n_no_atr", "n_tide", "n_no_stop", "n_position_open",
                                      "n_entered", "n_trades", "row_kind"]), "",
          "## 7 · Regbooks written (the scorer's interface)", "",
          "| arm | kind | n | sum_net_r | book_sha256 |", "|---|---|---|---|---|"]
    for a in ARMS:
        s = sides[a.name]
        L.append(f"| {a.name} | {a.kind} | {s['n']} | {_f(s['sum_net_r'])} | "
                 f"`{s['book_sha256']}` |")
    L += ["", f"book_sha256 law: {BOOK_SHA_LAW}.", "",
          "## 8 · Readings built (sub-readings where the frozen text is silent)", ""]
    L += [f"- {x}" for x in READINGS]
    L += ["", "## 9 · Content shas (build_manifest.json)", "", "| file | content sha256 |",
          "|---|---|"]
    for k, v in man["content_sha"].items():
        L.append(f"| {k} | `{v}` |")
    sb = books["scored"]
    L += ["", "## 10 · Findings (disclosures, not fixed; no rule was changed after a number "
          "was seen)", ""]
    hv = sb[sb["harvested"]]
    lag = (hv["harvest_i"] - hv["entry_i"]).to_numpy()
    hu = hv["harvest_unit_move_r"].to_numpy(float)
    hneg = hu[hu < 0]
    # [trading D-1] both medians: the all-harvest one and the negative harvests' own
    L.append(f"- F-1 THE v6 HARVEST FIRES EARLY ON THIS LANE. v6's harvest (50% at the 89/316 "
             f"band edge, harvest_min_unit_r = -inf) fired on {len(hv)}/{len(sb)} scored "
             f"campaigns; {len(hneg)} of those harvests were at a NEGATIVE unit move (median "
             f"over all {len(hv)} harvests {float(np.median(hu)):+.4f} R; over the {len(hneg)} "
             f"negative ones {float(np.median(hneg)):+.4f} R), a "
             f"median {float(np.median(lag)):.0f} bars after entry "
             f"({int((lag == 1).sum())} on the very next bar). The lane enters AT the EMA-89 tap, "
             f"next to the harvest band. This is the registered 'v6 management', built as "
             f"written; it is the operator's to judge.")
    cs = T["T_BRK_CANDIDATES"]
    cs = cs[cs["arm"] == "scored"]
    fl = cs[(cs["tide"] != cs["tide_prev"]) & (cs["disposition"] != "out_of_window")]
    L.append(f"- F-2 THE TIDE BAR MATTERS ON {len(fl)} SCORED CANDIDATES: the entry bar's tide "
             f"differs from the previous bar's ({int((fl['disposition'] == 'entered').sum())} "
             f"entered, {int((fl['disposition'] == 'tide').sum())} refused by the tide). "
             f"BK.tide_4h_for_exec on a 4h frame reads the previous bar (F-BRK-TIDE proves it); "
             f"the reading of record (the entry bar's own close) is used.")
    pk = T["T_BRK_PICKS"]
    fb = pk[pk["pick_window"] != "tuning"]["symbol"].tolist()
    ch = pk[(pk["panel"] == "CLASSIC5") & (pk["stable_first_half_vs_tuning"] == False)]  # noqa: E712
    L.append(f"- F-3 SCALE LABELS: 4h fallback (whole-tape, IN-SAMPLE everywhere) picks in the "
             f"17-asset view: {fb}; CLASSIC5 4h picks whose first-half-of-tuning pick differs "
             f"(stability_changed, flagged on every row): {ch['symbol'].tolist()}. Every scored "
             f"tuning-era row is scale-in-sample ({int(sb['scale_in_sample'].sum())}/{len(sb)}); "
             f"the holdout slice and the frozen-3.0 twin are printed beside (§3).")
    eg = T["T_BRK_EXIT_GRID"]
    ce = int(eg[eg["exit_reason"] == "corridor_end"]["n"].sum())
    L.append(f"- F-4 No campaign of any ridden arm is open at the pin (corridor_end exits: {ce}); "
             f"rail-bound stops: {int(sb['rail_binding'].sum())}/{len(sb)} scored campaigns "
             f"(a rail-bound R = |entry - (entry - ATR)| carries float rounding against ATR; the "
             f"law, not a bound, is what F-BRK-ENTRY holds).")
    L.append("- F-5 The 17-asset view's CLASSIC5 rows are byte-identical to the scored book "
             "(asserted in the build); the engine one-shot memory flip twin is the leash's own "
             "evaluation, not bounded by the next death (the engine's law), so its candidacy "
             "differs from the scan's window by construction.")
    pre = sb[(sb["era"] == "holdout") & (sb["die_close_ms"] <= ERA_CUT_MS)]
    per = {a.name: int(((books[a.name]["era"] == "holdout")
                        & (books[a.name]["die_close_ms"] <= ERA_CUT_MS)).sum()) for a in RIDDEN}
    L.append(f"- F-6 HOLDOUT ROWS ACTING ON A TUNING-ERA DEATH (disclosure): {len(pre)} scored "
             f"holdout campaign(s) act on a death whose bar closed at or before the era cut "
             + ("(" + "; ".join(f"{r.symbol} death close {iso(int(r.die_close_ms))}, entry close "
                                f"{iso(int(r.entry_close_ms))}, net {float(r.net_r):+.6f} R"
                                for r in pre.itertuples(index=False)) + ")" if len(pre) else "")
             + f". The per-row scale_in_sample flag is read at the entry instant (R-TBRK-10; "
             f"L-R.2 'read at an instant'), so these rows read False; era membership is by the "
             f"entry close [L-1.3] and is unchanged. Per ridden arm: {per}. Printed beside the "
             f"holdout slice in §3. The EXTRA column anchor_scale_in_sample (R-TBRK-11: death "
             f"close <= cut OR known close <= cut at the calibrated scale, OR the row's flag; "
             f"False at frozen 3.0) labels these rows True. Holdout rows labelled in-sample per "
             f"ridden arm, (scale_in_sample, anchor_scale_in_sample): "
             + str({a.name: (int((books[a.name]["scale_in_sample"]
                                  & (books[a.name]["era"] == "holdout")).sum()),
                             int((books[a.name]["anchor_scale_in_sample"]
                                  & (books[a.name]["era"] == "holdout")).sum()))
                    for a in RIDDEN})
             + " (T_BRK_ARMS n_holdout_scale_in_sample / n_holdout_anchor_scale_in_sample).")
    fl_d = {a.name: (int((books[a.name]["die_i"] < FLOOR_BARS).sum()),
                     round(fsum(books[a.name].loc[books[a.name]["die_i"] < FLOOR_BARS, "net_r"]), 6))
            for a in RIDDEN}
    fl_t = {a.name: int((books[a.name]["touch_i"] < FLOOR_BARS).sum()) for a in RIDDEN}
    L.append(f"- F-7 THE BAR-316 FLOOR IS APPLIED AT THE ENTRY BAR (R-TBRK-2; disclosure): "
             f"campaigns whose DEATH bar is below {FLOOR_BARS} (a floor on the death would not "
             f"admit them), per ridden arm (n, ΣR): {fl_d}; campaigns whose TOUCH bar is below "
             f"{FLOOR_BARS}: {fl_t}. The reading is unchanged.")
    L += ["", f"## 11 · The registered book, every campaign ({len(sb)} rows) — {BOOK_LABEL}", "",
          "Entry = the close of the touch + 3 bar (UTC); exit = the exit bar's close (a stop "
          "fills intrabar at the stop). The Tier-E books' rows, every candidate with its "
          "disposition and every evaluated retest are printed whole in Appendices A-C (row "
          "counts: "
          + ", ".join(f"{t} {len(T[t])}" for t in ("T_BRK_CANDIDATES", "T_BRK_SCAN"))
          + ", " + ", ".join(f"{a.name} {len(books[a.name])}" for a in ARMS if a.kind == "tierE")
          + ").", "",
          "| # | symbol | entry | side | entry_px | stop_px | r_dist | r_over_atr | exit | "
          "exit_reason | net_r | haircut_net_r | era | scale_in_sample | "
          "anchor_scale_in_sample |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, r in enumerate(sb.itertuples(index=False), 1):
        L.append(f"| {k} | {r.symbol} | {iso(int(r.entry_close_ms))} | "
                 f"{'long' if int(r.direction) == 1 else 'short'} | {r.entry_px!r} | "
                 f"{float(r.stop_px):.10g} | {float(r.r_dist):.10g} | {float(r.r_over_atr):.4f} | "
                 f"{iso(int(r.exit_close_ms))} | {r.exit_reason} | {float(r.net_r):+.6f} | "
                 f"{float(r.haircut_net_r):+.6f} | {r.era} | {bool(r.scale_in_sample)} | "
                 f"{bool(r.anchor_scale_in_sample)} |")
    L += appendices(W, books)
    return "\n".join(L) + "\n"


def _iso_or_dash(ms) -> str:
    return iso(int(ms)) if int(ms) >= 0 else "—"


def _g(x) -> str:
    return "—" if not np.isfinite(float(x)) else f"{float(x):.10g}"


APPX_A_COLS = ("arm", "symbol", "die_i", "touch_i", "entry_i", "entry_close", "side",
               "disposition", "tide", "tide_prev", "stop_px", "r_dist", "rail_binding",
               "scale_in_sample", "row_kind")
APPX_B_COLS = ("arm", "symbol", "die_i", "seq", "touch_i", "known_at", "known_close",
               "retest_outcome", "scale_in_sample", "row_kind")
APPX_C_COLS = ("arm", "symbol", "entry_close", "side", "entry_px", "stop_px", "r_dist",
               "exit_close", "exit_reason", "net_r", "gross_r", "fee_r", "funding_r",
               "haircut_net_r", "era", "scale_in_sample", "anchor_scale_in_sample")


def _appx(tag: str, cols: tuple, rows: list) -> list:
    hdr = ["row"] + list(cols) + list(COLLAR)
    L = ["| " + " | ".join(hdr) + " |", "|" + "|".join("---" for _ in hdr) + "|"]
    for k, vals in enumerate(rows, 1):
        L.append("| " + " | ".join([f"{tag}.{k}"] + [str(v) for v in vals]
                                   + [COLLAR[c] for c in COLLAR]) + " |")
    return L


def appendices(W: dict, books: dict) -> list:
    """[repair, verifier MINOR 'every table WHOLE'] the row-level stage tables and
    the Tier-E regbooks, printed whole: A = T_BRK_CANDIDATES, B = T_BRK_SCAN,
    C = every Tier-E regbook row (per arm).  Rows carry a tag (A.k / B.k / C.k) the
    fixtures count against the tables."""
    ca, sc = W["T_BRK_CANDIDATES"], W["T_BRK_SCAN"]
    L = ["", "## Appendix A · every candidate (hold) with its single disposition — "
         f"T_BRK_CANDIDATES, whole ({len(ca)} rows)", "",
         "entry_close = the close of the known_at bar (— past the tape); tide / tide_prev = "
         "the three-state tide at the entry bar / the bar before; stop_px / r_dist are the "
         "leg's (— when no leg was cut).", ""]
    L += _appx("A", APPX_A_COLS, [
        (r.arm, r.symbol, int(r.die_i), int(r.touch_i), int(r.entry_i),
         _iso_or_dash(r.entry_close_ms), "long" if int(r.direction) == 1 else "short",
         r.disposition, int(r.tide), int(r.tide_prev), _g(r.stop_px), _g(r.r_dist),
         bool(r.rail_binding), bool(r.scale_in_sample), r.row_kind)
        for r in ca.itertuples(index=False)])
    L += ["", "## Appendix B · every evaluated retest — T_BRK_SCAN, whole "
          f"({len(sc)} rows)", "",
          "seq = the touch's order within its death's candidacy window; known_at = touch + the "
          "law's hold length; known_close = that bar's close (— past the tape).", ""]
    L += _appx("B", APPX_B_COLS, [
        (r.arm, r.symbol, int(r.die_i), int(r.seq), int(r.touch_i), int(r.known_at),
         _iso_or_dash(r.known_close_ms), r.retest_outcome, bool(r.scale_in_sample), r.row_kind)
        for r in sc.itertuples(index=False)])
    tot = sum(len(books[a.name]) for a in ARMS if a.kind == "tierE")
    L += ["", f"## Appendix C · every Tier-E regbook row — a SELECTION, not a result ({tot} "
          f"rows over {sum(1 for a in ARMS if a.kind == 'tierE')} books)", "",
          "entry_close / exit_close = the entry / exit bar's close (UTC); the slice books "
          "(tierE__tuning, tierE__holdout) are the §11 rows cut by era and are printed again "
          "here as books of their own.", ""]
    rows = []
    for a in ARMS:
        if a.kind != "tierE":
            continue
        for r in books[a.name].itertuples(index=False):
            rows.append((a.name, r.symbol, iso(int(r.entry_close_ms)),
                         "long" if int(r.direction) == 1 else "short", repr(float(r.entry_px)),
                         _g(r.stop_px), _g(r.r_dist), iso(int(r.exit_close_ms)), r.exit_reason,
                         f"{float(r.net_r):+.6f}", f"{float(r.gross_r):+.6f}",
                         f"{float(r.fee_r):+.6f}", f"{float(r.funding_r):+.6f}",
                         f"{float(r.haircut_net_r):+.6f}", r.era, bool(r.scale_in_sample),
                         bool(r.anchor_scale_in_sample)))
    L += _appx("C", APPX_C_COLS, rows)
    return L


# ══════════════════════════════════════════════ 9 · MAIN
def lean_block() -> str:
    L = [f"{E.LEAN_TAG} STAGE T-brk (P-BRK-4H) · substrate {E.SNAPSHOT.name} · pin {PIN_ISO} "
         f"· seed {SEED}"]
    L += [f"{E.LEAN_TAG} {x}" for x in READINGS]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    od = next((a.split("=", 1)[1] for a in args if a.startswith("--out-root=")), None)
    R = build(Path(od) if od else OUT_ROOT)
    for a in ARMS:
        s = R["sidecars"][a.name]
        print(f"{a.name:30} n {s['n']:4d} · ΣR {s['sum_net_r']:+.6f} · sha {s['book_sha256'][:16]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
