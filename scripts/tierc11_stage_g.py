#!/usr/bin/env python
"""TIER-C11 · STAGE G — the admission gates [LEANS L-G.1, L-G.2, L-G.3, L-1.4,
L-1.5, AM-7].

Contract of record: exchange/queue/2026-09-24_TC11_APOLLO.md (sha256 bb38e016…,
STEP Q b9ed953), STAGE G lines 44-49.  Executor HEPHAESTUS; seed 20260924.
Readings of record: research_outputs/tierc11/LEANS.md (frozen, sha 655e1605…) and
LEANS_AMENDMENTS.md (AM-1..AM-7).  Registrations of record: P-AGE-1 and P-WIN-1
in research_outputs/tierc11/registrations/REGISTRATIONS.json (text + payload shas
verified here before anything is built).

A RUNNER, RANGE-FREE.  It imports tierc11_books (-> tierc11_env, the range-free
shim) and tierc11_ride; never tierc11_nest or any range module (Stage G reads no
range).  Parquet is read and written only through pandas on path strings (AM-2).
It draws nothing (no bootstrap: the scorer, scripts/tierc11_score.py, reads the
regbooks this writes and computes every interval); it prints no verdict word.

WHAT IT BUILDS
  research_outputs/tierc11/regbooks/P-AGE-1/   (REGBOOK INTERFACE)
    scored               v6 minus the campaigns whose ENTRY-bar tide streak
                         (tierc7_lab_regime.tide_streak) >= the trailing q75 edge
                         (B4 OLD; tierc9._trailing_edges over CLASSIC5 4h bars
                         with open <= the entry bar, >= 30 bars) [L-G.1]
    base                 the v6 book [L-1.6] (two-sample ruler, L-1.4)
    tierE__shadow_abs206 v6 minus streak > 206 (the ABSOLUTE shadow, as written:
                         206 is the whole-corridor MEDIAN edge, not the OLD edge,
                         and it reads the corridor ahead)
    tierE__tuning / tierE__holdout   the scored arm's era slices (era by the
                         entry bar's CLOSE, L-1.3); compare with `base` sliced
                         to the same era
    tierE__refused_cohort            the refused campaigns (L-1.5 gate row)
  research_outputs/tierc11/regbooks/P-WIN-1/
    scored               v6 minus lag = entry_i - arm_i >= 16 (4h bars) [L-G.2]
    base                 the v6 book
    tierE__shadow_lag7_15            v6 minus lag 7..15
    tierE__tuning / tierE__holdout / tierE__refused_cohort
    tierE__ratr_admission            v6 minus r_over_atr > 2.2 [L-G.3]
    tierE__ratr_priority             the within-window PRIORITY book [L-G.3]
  research_outputs/tierc11/stage_g/
    g_*.parquet          every non-registered table (collared, L-1.4) + the
                         registered-book descriptor table (no collar: book
                         arithmetic, not a verdict)
    build_manifest.json  content shas, keys, regbook shas, readings
    STAGE_G.md           the stage report, every table WHOLE

GATES ARE POST-FILTERS [L-1.5].  A gated book is the v6 book minus exactly the
refused campaigns — the same Trade objects, row-identical on every column.  The
re-ride rival (a refusal INSIDE the replay frees the slot and can admit a
trigger v6 rejected as position_open) is printed as a DISCLOSURE:
  · the count of record is taken from the v6 ride's REJECTION LOG
    (T9.replay9's Arming.reject == 'position_open'): the triggers whose blocking
    campaign (the one v6 campaign of that asset holding the slot at the trigger
    bar) is refused.  First order: a rival admitted into a freed slot could
    itself block a later rival; the log does not re-ride.
  · beside it, a RE-RIDE with a refusal hook (`replay_g(refuse=...)`, the gate's
    rule evaluated on each candidate at its own trigger bar; a refused trigger
    does not occupy the slot) — a Tier-E book, n / ΣR / admitted-not-in-v6.

THE PRIORITY BOOK [L-G.3; executor sub-reading, stated here and in STAGE_G.md].
`replay_g(priority_cut=2.2)` is replay9's candidate loop (arms, tide -> d ->
trigger gates, one position per asset, windows in time order) with ONE change:
a window whose FIRST 12/26 trigger c0 has r_over_atr = r_dist / ATR14_4h(c0) >
2.2 is PASSED (it never occupies the slot), and the window's entry becomes the
first LATER same-direction 12/26 cross c in (c0, min(window_end_i, hi_i + 1))
at which the asset is FLAT (c > the open campaign's exit bar) and the v6 stop
at c exists with r_over_atr(c) <= 2.2.  A window whose first trigger has
r_over_atr <= 2.2 (or has no stop / no ATR) follows v6's law exactly (the first
trigger only; position_open kills the window).  Every entry is ridden with
tierc11_ride.ride11 from its 4h close (walk / warn / tp off == _ride_leg9) and
booked by tierc11_ride.trade11 (tierc7._account_chain).  v6's windows of one
asset are disjoint in time (a window ends at the counter 12/89 cross, which is
the next window's arm), so windows never interleave; the one-position rule acts
across windows through open campaigns.  Every substitution is counted and
listed; so are windows passed with no substitute and v6 campaigns the priority
book did not take.

THE CROSS-ASSET SAME-CLOSE COLLISION COUNT [L-G.3] is a disclosure: 4h closes at
which two or more assets' campaigns enter in the same book.  It cannot bind:
one position per ASSET, and no portfolio cap exists.

THE THREE GATES CROSSED 2 x 2 x 2 [L-G.3], printed whole two ways:
  (a) the crossing: the v6 book partitioned by the three refusal flags
      (A = P-AGE-1 OLD, W = P-WIN-1 lag >= 16, S = r_over_atr > 2.2), 8 cells;
  (b) the eight gate books: v6 minus the union of the refused sets of the
      gates switched on.
  Each cell: n, E[net R], ΣR (n = 0 cells carry NaN stats and a nan_reason).

HAIRCUT TWIN [AM-7]: haircut_net_r = net_r - fee_r x slip_bps_side /
taker_bps_side (5.0), slip = the stem's charter tier (E.fees(): A 2 / B 5 /
C 10 bps/side).  fee_r is the ride's own taker fee over every fill.

REGBOOK book_sha256 (the canonical CSV law, stated once): the 16 REQUIRED columns
in the interface order, a header line of their names, one line per row sorted by
(symbol, entry_close_ms), fields joined by ',' and lines ended by '\\n'; floats
as repr(float(x)), ints as decimal, strings verbatim (a ',' or newline in a
string HALTs); sha256 of the UTF-8 bytes.

REPAIR 2026-09-25 (the Stage G verifier's MINOR findings; no rule, cut or book changed —
every regbook parquet is byte-identical to the first build):
  · one era seam `era_of_entry` (E.era_of of the entry bar's CLOSE) used by the facts,
    the regbook frames and the era-slice rows (`era_slice_rows`) [L-1.3];
  · the one-position sentence of STAGE_G.md is printed from the computed counts
    (`flat_claim`), never hard-coded;
  · the >206 label (ABS_LABEL) rides as a `caveat` column on the shadow's gate row and
    on every >206 row of g_tide_bands [L-G.1]; the >206 rows carry their real
    left-censored counts (no -1);
  · placeholder rows ('(none)') carry an explicit `placeholder` flag, sentinels only
    in their key fields and nulls elsewhere; the priority window log's entry_i /
    entry_ms are null (not -1) for a window with no entry;
  · every non-registered table STAGE_G.md prints carries the collar [L-1.4]; the
    header and the manifest print the latest close at fetch time beside the pin
    (AS_OF_PIN.json latest_closed_4h_at_pin_run) [L-0.1]; the manifest carries each
    regbook file's sha256.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_g.py            # canonical build
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_g.py --out-dir=DIR  # F-DET twin
      (DIR must be a direct child of research_outputs/tierc11/stage_g/_det_stage_g/,
       or of a `_det_stage_g/` directory OUTSIDE the repo tree)
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_books as B                   # noqa: E402  (-> tierc11_env: guard, shim, hook)
import tierc11_ride as RD                   # noqa: E402

import numpy as np                          # noqa: E402
import pandas as pd                         # noqa: E402

E = B.E
TP, T9, T7, TB, LR = E.TP, E.T9, E.T7, E.TB, E.LAB
RC = T9.RC
iso = TB.iso
CARD = TP.CONTROL_CARD
ROLES = T9.V6_ROLES
MS_4H = int(TP.MS_4H)

# ═══════════════════════════════════════════════════════ CONSTANTS OF RECORD
PIN_MS = E.PIN_MS                           # 2026-09-25T00:00:00Z [L-0.1]
PIN_ISO = "2026-09-25T00:00:00Z"
TC10_PIN_MS = B.TC10_PIN_MS                 # 2026-09-21T16:00:00Z
SEED = E.SEED                               # nothing here draws; printed
ERA_CUT_MS = E.ERA_CUT_MS
AGE_OLD_BAND = 3                            # LR._streak_band 3 = B4 OLD (run >= q75) [L-G.1]
ABS_TIDE_CUT = 206                          # L-G.1 shadow: refuse streak > 206, as written
LAG_CUT = 16                                # L-G.2: P-WIN-1 refuses lag >= 16
SHADOW_LAG = (7, 15)                        # L-G.2: the shadow cut refuses lag 7..15
RATR_CUT = 2.2                              # L-G.3: refuse r_over_atr > 2.2
TAKER_BPS_SIDE = 5.0                        # L-1.1 / AM-7 divisor
V6_BOOK_SHA = "f3c68f544bcda52c909374105dabbdc773c9bffa4b66b2ef7e0f35ac9b369132"   # books/ manifest
V6_N = 200
REGISTRATIONS_REL = "research_outputs/tierc11/registrations/REGISTRATIONS.json"
REGISTRATIONS_SHA = "648834bf30e20e92713bddef2374ddef1aae843f4d8ba152fc50166c8cc6f1ee"  # PROGRESS
REG_AGE, REG_WIN = "P-AGE-1", "P-WIN-1"
SOURCE_SCRIPT = "scripts/tierc11_stage_g.py"
COLLAR = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
          "gates": "nothing"}
BOOK_NOTE = "book, not a verdict"
ABS_LABEL = ("206 is the whole-corridor MEDIAN edge of the pooled CLASSIC5 streak, not the "
             "OLD edge, and it reads the corridor ahead (look-ahead); the OLD cut of record "
             "is the trailing q75 (B4)")

REQUIRED = ("symbol", "entry_ms", "entry_close_ms", "direction", "entry_px", "stop_px",
            "r_dist", "exit_close_ms", "exit_reason", "net_r", "gross_r", "fee_r",
            "funding_r", "haircut_net_r", "era", "lane")
REQ_INT = ("entry_ms", "entry_close_ms", "exit_close_ms")
REQ_FLOAT = ("entry_px", "stop_px", "r_dist", "net_r", "gross_r", "fee_r", "funding_r",
             "haircut_net_r")
REQ_STR = ("symbol", "exit_reason", "era", "lane")
SIDECAR_KEYS = ("registration", "arm", "kind", "ruler", "panel", "era_scope", "n",
                "sum_net_r", "book_sha256", "description", "source_script",
                "book_sha256_law", "haircut_law", "as_of", "seed")
BOOK_SHA_LAW = ("sha256 of the UTF-8 canonical CSV of the 16 required columns in interface "
                "order, rows sorted by (symbol, entry_close_ms) (mergesort), header = the "
                "column names joined by ',', one row per line joined by ',', '\\n' after every "
                "line (the last included); int columns and direction as str(int), floats as "
                "repr(float), strings verbatim (no ',' or newline allowed)")
HAIRCUT_LAW = ("AM-7: haircut_net_r = net_r - fee_r x (slip_bps_side / taker_bps_side); fee_r = "
               "the ride's taker fee over every fill / r_dist; slip_bps_side = the stem's charter "
               "tier (A 2 / B 5 / C 10) from E.fees(); taker 5.0 bps/side")
TIERE_KEYS = ("tier", "selection_not_a_result", "gates")

OUT_ROOT = E.OUT                            # research_outputs/tierc11
STAGE_DIR = "stage_g"
REGBOOK_DIR = "regbooks"
DET_NAME = "_det_stage_g"
DET_ROOT = OUT_ROOT / STAGE_DIR / DET_NAME
MANIFEST = "build_manifest.json"
REPORT = "STAGE_G.md"

# the gates of this stage: id -> (registration, the rule as text, the facts column)
GATES = {
    "P-AGE-1": (REG_AGE, "refuse ENTRY-bar tide streak >= trailing q75 (B4 OLD)",
                "age_old_refused"),
    "P-AGE-1/shadow_abs206": (REG_AGE, "refuse ENTRY-bar tide streak > 206 (ABSOLUTE "
                              "shadow, as written)", "age_abs206_refused"),
    "P-WIN-1": (REG_WIN, "refuse lag = entry_i - arm_i >= 16", "win_refused"),
    "P-WIN-1/shadow_lag7_15": (REG_WIN, "refuse lag 7..15 (shadow cut)", "lag7_15_refused"),
    "L-G.3/ratr_admission": (REG_WIN, "refuse r_over_atr = r_dist / ATR14_4h(entry) > 2.2",
                             "ratr_refused"),
}
GATE_ORDER = tuple(GATES)
GRID_FLAGS = (("A", "age_old_refused"), ("W", "win_refused"), ("S", "ratr_refused"))

READINGS = (
    "[LEAN-HEPHAESTUS] L-G.1 tide age of record = tierc7_lab_regime.tide_streak (run length "
    "of sign(e89 - e316) on 4h, counted from warm bar 316) read at the campaign's ENTRY bar; "
    "trailing CLASSIC5 quartile edges over bars with open <= the entry bar "
    "(tierc9._trailing_edges, >= 30 bars; pool = tierc9._trailing_pool over the TC11 "
    "corridor); OLD = B4 = streak >= trailing q75; P-AGE-1 refuses OLD.",
    "[LEAN-HEPHAESTUS] L-G.1 shadow: refuse streak > 206 exactly as written (206 = the "
    "whole-corridor median edge, not the OLD edge; it reads the corridor ahead).  "
    "Disclosure: tierc9.tide_streak_age (arm bar, three-state tide), banded on the SAME "
    "trailing edges as the campaign's entry-bar band.",
    "[LEAN-HEPHAESTUS] L-G.2 lag = entry_i - arm_i (4h bars); P-WIN-1 refuses lag >= 16; the "
    "shadow refuses 7..15.",
    "[LEAN-HEPHAESTUS] L-G.3 r_over_atr = r_dist / ATR14_4h(entry); admission refuses > 2.2; "
    "the PRIORITY book is replay9's loop with the first-trigger pass and the in-window "
    "substitute (first later same-direction 12/26 cross with the asset flat and r_over_atr "
    "<= 2.2), ridden by tierc11_ride.ride11 from its 4h close; the cross-asset same-close "
    "collision count is a disclosure; the three gates crossed 2 x 2 x 2 (partition + gate "
    "books), whole.",
    "[LEAN-HEPHAESTUS] L-1.5 gates are POST-FILTERS: gated = v6 minus exactly the refused "
    "set, row-identical; the re-ride rival count is taken from the v6 ride's rejection log "
    "(first order), the re-ride book with a refusal hook printed beside (Tier-E).",
    "[LEAN-HEPHAESTUS] L-1.3 era = the entry bar's CLOSE (E.era_of); L-1.4 no verdict word "
    "here, every non-registered table collared; AM-7 haircut_net_r = net_r - fee_r x "
    "slip_bps_side / 5.0 (charter tier).",
)


def _halt(msg: str) -> None:
    raise SystemExit(f"HALT: {msg}")


# ═══════════════════════════════════════════════════ THE REGISTRATIONS OF RECORD
def registrations() -> dict:
    """{reg id: record} for P-AGE-1 and P-WIN-1 — the file's sha, each text's sha and
    each payload's sha verified (tierc11_registrations' law) before anything is
    built.  HALTs on any mismatch."""
    p = ROOT / REGISTRATIONS_REL
    raw = p.read_bytes()
    if hashlib.sha256(raw).hexdigest() != REGISTRATIONS_SHA:
        _halt(f"{REGISTRATIONS_REL} is not the registrations of record ({REGISTRATIONS_SHA[:16]}…)")
    d = json.loads(raw.decode("utf-8"))
    out = {}
    for r in d["registrations"]:
        if r["registration"] not in (REG_AGE, REG_WIN):
            continue
        if hashlib.sha256(r["text_of_record"].encode("utf-8")).hexdigest() != r["text_sha256"]:
            _halt(f"{r['registration']}: text_sha256 does not verify")
        body = {k: v for k, v in r.items() if k not in ("sha256", "text_sha256")}
        if hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False)
                          .encode("utf-8")).hexdigest() != r["sha256"]:
            _halt(f"{r['registration']}: payload sha256 does not verify")
        out[r["registration"]] = r
    if sorted(out) != sorted((REG_AGE, REG_WIN)):
        _halt(f"registrations missing: {sorted(out)}")
    return out


# ═══════════════════════════════════════════════════════════ THE v6 BOOK + LOG
def v6_replay(lo: int, hi: int) -> tuple[list, dict]:
    """The v6 book and its REJECTION LOG: T9.replay9 per CLASSIC5 asset (exactly
    what TP.run_cell_n rides), held to B.v6_book by TP._book_sha and to the typed
    books/ sha.  Returns (trades in CLASSIC5 order, {sym: arms})."""
    trades, arms = [], {}
    for s in E.CLASSIC5:
        a, t = T9.replay9(s, CARD, ROLES, lo, hi)
        arms[s] = a
        trades += t
    ref = B.v6_book(lo, hi)
    if TP._book_sha(trades) != TP._book_sha(ref) or TP._book_sha(ref) != V6_BOOK_SHA \
            or len(trades) != V6_N:
        _halt(f"the v6 replay ({TP._book_sha(trades)[:16]}…, n {len(trades)}) is not the "
              f"book of record ({V6_BOOK_SHA[:16]}…, n {V6_N})")
    return trades, arms


def key_of(t) -> tuple:
    return (str(t.symbol), int(t.entry_ms))


# ══════════════════════════════════════════════════════ THE GATE FACTS (seams)
# Each definition is a module-level function looked up at CALL time, so a fixture
# can MUTATE one (F-DEF's plants) and watch the typed recomputation go RED.
def age_of(t) -> tuple[int, bool]:
    """L-G.1 of record: (run, left_censored) of LR.tide_streak at the ENTRY bar."""
    run, cens, _state = B.entry_streak(t)
    return int(run), bool(cens)


def edges_of(t, pool: dict):
    """L-G.1 of record: [q25, q50, q75] over the pooled prefix open_ms <= the entry
    bar's open (T9._trailing_edges, >= 30 bars) or None (unbanded)."""
    return B.trailing_edges(t, pool)


def old_refused(run: int, edges) -> bool:
    """P-AGE-1: OLD = band B4 = run >= trailing q75 (LR._streak_band == 3)."""
    return edges is not None and B.band_of(int(run), edges) == AGE_OLD_BAND


def abs_refused(run: int) -> bool:
    """The absolute shadow, exactly as written: streak > 206."""
    return int(run) > ABS_TIDE_CUT


def lag_of(t) -> int:
    return int(t.entry_i) - int(t.arm_i)


def win_refused(lag: int) -> bool:
    return int(lag) >= LAG_CUT


def lag7_15_refused(lag: int) -> bool:
    return SHADOW_LAG[0] <= int(lag) <= SHADOW_LAG[1]


def ratr_of(t) -> float:
    return float(t.r_dist) / float(t.atr_at_entry)


def ratr_refused(r: float) -> bool:
    return float(r) > RATR_CUT


def era_of_entry(entry_ms: int) -> str:
    """L-1.3: a campaign's era = E.era_of(its entry bar's CLOSE = entry_ms + 4h).  The
    ONE place this stage turns an entry bar into an era (facts, regbooks, slices)."""
    return str(E.era_of(int(entry_ms) + MS_4H))


def band_code(run: int, edges) -> str:
    if edges is None:
        return "unbanded"
    b = B.band_of(int(run), edges)
    return "unbanded" if b is None else B.BAND_CODES[b]


def facts_of(t, pool: dict) -> dict:
    """Every gate fact of one campaign, at full precision."""
    run, cens = age_of(t)
    ed = edges_of(t, pool)
    arm_age, arm_cens = T9.tide_streak_age(t, ROLES)
    lag = lag_of(t)
    r = ratr_of(t)
    ec = int(t.entry_ms) + MS_4H
    flags = {"age_old_refused": bool(old_refused(run, ed)),
             "age_abs206_refused": bool(abs_refused(run)),
             "win_refused": bool(win_refused(lag)),
             "lag7_15_refused": bool(lag7_15_refused(lag)),
             "ratr_refused": bool(ratr_refused(r))}
    return {
        "symbol": str(t.symbol), "entry_ms": int(t.entry_ms), "entry_close_ms": ec,
        "direction": int(t.direction), "arm_i": int(t.arm_i), "arm_ms": int(t.arm_ms),
        "entry_i": int(t.entry_i), "era": era_of_entry(t.entry_ms), "net_r": float(t.net_r),
        "tide_streak_entry": int(run), "tide_left_censored": bool(cens),
        "tide_edge_q25": (float(ed[0]) if ed is not None else float("nan")),
        "tide_edge_q50": (float(ed[1]) if ed is not None else float("nan")),
        "tide_edge_q75": (float(ed[2]) if ed is not None else float("nan")),
        "tide_band": band_code(run, ed),
        "tide_streak_age_arm": int(arm_age), "tide_streak_age_arm_censored": bool(arm_cens),
        "arm_band_on_entry_edges": band_code(arm_age, ed),
        "arm_old_on_entry_edges": bool(ed is not None and B.band_of(int(arm_age), ed)
                                       == AGE_OLD_BAND),
        "arm_age_gt206": bool(int(arm_age) > ABS_TIDE_CUT),
        "lag": int(lag), "lag_band": B.lag_band(int(lag)),
        "r_over_atr": float(r),
        **flags,
        "grid_cell": "|".join(f"{c}{int(flags[col])}" for c, col in GRID_FLAGS),
    }


def facts_frame(book: list, pool: dict) -> pd.DataFrame:
    return pd.DataFrame([facts_of(t, pool) for t in book])


def refused_keys(facts: pd.DataFrame, gate: str) -> set:
    col = GATES[gate][2]
    m = facts[col].astype(bool).to_numpy()
    return set(zip(facts["symbol"][m], facts["entry_ms"][m].astype(int)))


def apply_gate(book: list, refused: set) -> list:
    """THE POST-FILTER [L-1.5]: the base book minus exactly the refused campaigns —
    the same Trade objects, the base's order."""
    return [t for t in book if key_of(t) not in refused]


# ═══════════════════════════════════════ replay_g: replay9's loop, with the hooks
def window_end(a, hi_i: int) -> int:
    """The window's trigger range end, exclusive (tierc9.card_candidates9)."""
    return min(int(a.window_end_i), int(hi_i) + 1)


def is_flat(ti: int, open_until: int) -> bool:
    """One position per asset: flat iff the trigger bar is after the open
    campaign's exit bar (replay9's `ti <= open_until` refusal)."""
    return int(ti) > int(open_until)


def ratr_ok(r: float, cut: float) -> bool:
    """The first-trigger test: r_over_atr <= cut keeps v6's law; > cut passes."""
    return float(r) <= float(cut)


def sub_admissible(r: float, cut: float) -> bool:
    """The substitute test: a later cross is taken only if r_over_atr <= cut."""
    return float(r) <= float(cut)


def _stop_at(st: dict, ti: int, d: int):
    """(Stop | None, atr) — v6's stop law at the trigger bar (replay9 verbatim)."""
    f = st["f"]
    entry_px, atr_sig = float(f.c[ti]), float(f.atr[ti])
    if not (np.isfinite(atr_sig) and atr_sig > 0):
        return None, atr_sig
    stp = RC.struct_stop_4h(st["pv4"], int(ti), entry_px, int(d), atr_sig,
                            min_stop_atr=CARD.entry_rail_atr, forbidden=None)
    if stp is None or not (np.isfinite(stp.r_dist) and stp.r_dist > 0):
        return None, atr_sig
    return stp, atr_sig


def replay_g(sym: str, lo_ms: int, hi_ms: int, *, refuse=None, priority_cut=None,
             pool: dict | None = None) -> tuple[list, list]:
    """tierc9.replay9's candidate loop for card v6 (same armings, same gates, same
    order, one position per asset), riding every entry with RD.ride11 from its 4h
    close and booking it with RD.trade11.  Hooks (both None == v6 exactly):
      refuse(ctx) -> bool   a gate evaluated on a candidate at its own trigger bar
                            (ctx: sym, arm, ti, d, stp, atr, r_over_atr); a refused
                            trigger does not occupy the slot (the re-ride rival).
      priority_cut          the L-G.3 priority rule (module docstring).
    Returns (trades, window log)."""
    st = T9.frame(sym)
    f = st["f"]
    lo_i, hi_i = T7._idx_range(f.open_ms, lo_ms, hi_ms)
    lo_i = max(lo_i, ROLES.floor_bars)
    if hi_i < lo_i:
        return [], []
    arms, cc = T9.card_candidates9(sym, ROLES, lo_i, hi_i)
    ra = T9.role_arrays(sym, ROLES)
    cx = RD.ctx_of(sym, CARD, ROLES)
    cands = sorted([(ti, d, "card", a) for ti, d, a in cc], key=lambda c: (c[0], -c[1], c[2]))
    trades, log, open_until = [], [], -1

    def enter(a, ti, d, stp, atr_sig, sub):
        entry_px = float(f.c[ti])
        leg = RD.ride11(sym, CARD, ROLES, d, ti, entry_px, stp.stop_px, stp.r_dist, hi_i,
                        ctx=cx)
        t = RD.trade11(sym, CARD, ROLES, d, arm_i=a.arm_i, arm_ms=a.arm_ms, disp=a.disp,
                       entry_i=ti, entry_ms=int(f.open_ms[ti]), entry_px=entry_px, stp=stp,
                       atr_sig=atr_sig, leg=leg, lane="card")
        object.__setattr__(t, "priority_substitute", bool(sub))
        trades.append(t)
        return int(leg["exit_i"])

    for ti, d, _kind, a in cands:
        rec = {"symbol": sym, "direction": int(d), "arm_i": int(a.arm_i),
               "arm_ms": int(a.arm_ms), "first_trigger_i": int(ti),
               "first_trigger_ms": int(f.open_ms[ti]),
               "window_end_i": int(window_end(a, hi_i)),
               "first_r_over_atr": float("nan"), "outcome": "", "entry_i": -1,
               "entry_ms": -1, "entry_r_over_atr": float("nan"), "n_scanned": 0,
               "n_scan_not_flat": 0, "n_scan_no_stop": 0, "n_scan_over_cut": 0}
        stp0, atr0 = _stop_at(st, ti, d)
        r0 = (float(stp0.r_dist) / atr0) if stp0 is not None else float("nan")
        rec["first_r_over_atr"] = r0
        passed = (priority_cut is not None and stp0 is not None
                  and not ratr_ok(r0, priority_cut))
        if not passed:
            if not is_flat(ti, open_until):
                rec["outcome"] = "position_open"
            elif stp0 is None:
                rec["outcome"] = "no_stop_or_atr"
            elif refuse is not None and refuse({"sym": sym, "arm": a, "ti": ti, "d": d,
                                                 "stp": stp0, "atr": atr0, "r_over_atr": r0}):
                rec["outcome"] = "refused"
            else:
                open_until = enter(a, ti, d, stp0, atr0, False)
                rec.update(outcome="entered", entry_i=int(ti), entry_ms=int(f.open_ms[ti]),
                           entry_r_over_atr=r0)
            log.append(rec)
            continue
        # the PRIORITY pass: search the window's later same-direction 12/26 crosses
        trig = ra["t_up"] if d == 1 else ra["t_dn"]
        end = window_end(a, hi_i)
        rec["outcome"] = "passed_no_substitute"
        for c in (int(x) for x in np.flatnonzero(trig[ti + 1:end]) + ti + 1):
            rec["n_scanned"] += 1
            if not is_flat(c, open_until):
                rec["n_scan_not_flat"] += 1
                continue
            stp, atr = _stop_at(st, c, d)
            if stp is None:
                rec["n_scan_no_stop"] += 1
                continue
            r = float(stp.r_dist) / atr
            if not sub_admissible(r, priority_cut):
                rec["n_scan_over_cut"] += 1
                continue
            if refuse is not None and refuse({"sym": sym, "arm": a, "ti": c, "d": d,
                                              "stp": stp, "atr": atr, "r_over_atr": r}):
                continue
            open_until = enter(a, c, d, stp, atr, True)
            rec.update(outcome="passed_substituted", entry_i=int(c),
                       entry_ms=int(f.open_ms[c]), entry_r_over_atr=r)
            break
        log.append(rec)
    return trades, log


def replay_book(lo: int, hi: int, **kw) -> tuple[list, list]:
    trades, log = [], []
    for s in E.CLASSIC5:
        t, lg = replay_g(s, lo, hi, **kw)
        trades += t
        log += lg
    return trades, log


# ─────────────────────────────────── the gates as refusal hooks (the re-ride rival)
def refuse_hook(gate: str, pool: dict):
    """The gate's rule evaluated on a CANDIDATE at its own trigger bar."""
    def age_at(ctx):
        state, run, start = LR.tide_streak(ctx["sym"])
        f = T9.frame(ctx["sym"])["f"]
        ed = T9._trailing_edges(pool, int(f.open_ms[int(ctx["ti"])]))["streak_bar"]
        return int(run[int(ctx["ti"])]), ed

    if gate == "P-AGE-1":
        return lambda ctx: old_refused(*age_at(ctx))
    if gate == "P-AGE-1/shadow_abs206":
        return lambda ctx: abs_refused(age_at(ctx)[0])
    if gate == "P-WIN-1":
        return lambda ctx: win_refused(int(ctx["ti"]) - int(ctx["arm"].arm_i))
    if gate == "P-WIN-1/shadow_lag7_15":
        return lambda ctx: lag7_15_refused(int(ctx["ti"]) - int(ctx["arm"].arm_i))
    if gate == "L-G.3/ratr_admission":
        return lambda ctx: ratr_refused(ctx["r_over_atr"])
    _halt(f"no refusal hook for {gate}")


# ═════════════════════════════════════════════════════════ THE RIVAL COUNT (log)
def blocker_of(arm, trades_sym: list):
    """The one v6 campaign of the asset holding the slot at the trigger bar."""
    ti = int(arm.trigger_i)
    hit = [t for t in trades_sym if int(t.entry_i) <= ti <= int(t.exit_i)]
    if len(hit) != 1:
        _halt(f"{arm.symbol} trigger {iso(int(arm.trigger_ms))}: {len(hit)} blocking "
              f"campaigns (want exactly 1)")
    return hit[0]


def rival_rows(arms: dict, v6: list, pool: dict, facts: pd.DataFrame) -> pd.DataFrame:
    """Every position_open rejection of the v6 ride, with its blocker and, per gate,
    whether the blocker is refused (a RIVAL) and whether the rival trigger would
    itself pass the gate at its own trigger bar."""
    by_sym = {s: [t for t in v6 if t.symbol == s] for s in E.CLASSIC5}
    fx = facts.set_index(["symbol", "entry_ms"])
    rows = []
    for s in E.CLASSIC5:
        f = T9.frame(s)["f"]
        for a in arms[s]:
            if a.reject != "position_open":
                continue
            b = blocker_of(a, by_sym[s])
            stp, atr = _stop_at(T9.frame(s), int(a.trigger_i), int(a.direction))
            ctx = {"sym": s, "arm": a, "ti": int(a.trigger_i), "d": int(a.direction),
                   "stp": stp, "atr": atr,
                   "r_over_atr": (float(stp.r_dist) / atr if stp is not None else float("nan"))}
            row = {"symbol": s, "direction": int(a.direction), "arm_ms": int(a.arm_ms),
                   "trigger_ms": int(a.trigger_ms),
                   "trigger_close_ms": int(f.open_ms[int(a.trigger_i)]) + MS_4H,
                   "blocker_entry_ms": int(b.entry_ms), "blocker_exit_ms": int(b.exit_ms),
                   "blocker_net_r": float(b.net_r)}
            for g in GATE_ORDER:
                tag = g.replace("/", "__").replace("-", "_").replace(".", "_")
                row[f"rival__{tag}"] = bool(fx.loc[(s, int(b.entry_ms)), GATES[g][2]])
                row[f"rival_self_refused__{tag}"] = (bool(refuse_hook(g, pool)(ctx))
                                                    if stp is not None else False)
            rows.append(row)
    return pd.DataFrame(rows)


# ═════════════════════════════════════════════════════════ THE REGBOOK FRAMES
def haircut(stem: str, net_r: float, fee_r: float) -> float:
    fs = E.fees()[stem]
    if float(fs["taker_bps_side"]) != TAKER_BPS_SIDE:
        _halt(f"{stem}: taker_bps_side {fs['taker_bps_side']} != {TAKER_BPS_SIDE}")
    return float(net_r) - float(fee_r) * float(fs["slippage_bps_side"]) / TAKER_BPS_SIDE


def regbook_frame(book: list, pool: dict) -> pd.DataFrame:
    """The REGBOOK INTERFACE's required columns (full precision, from the Trade
    objects) plus the gate facts as extras."""
    fees = E.fees()
    rows = []
    for t in book:
        s = str(t.symbol)
        fx = facts_of(t, pool)
        ec = int(t.entry_ms) + MS_4H
        ev_ms, ev_stamp = B.exit_event(t)
        rows.append({
            "symbol": s, "entry_ms": int(t.entry_ms), "entry_close_ms": ec,
            "direction": int(t.direction), "entry_px": float(t.entry_px),
            "stop_px": float(t.stop_px), "r_dist": float(t.r_dist),
            "exit_close_ms": int(t.exit_ms) + MS_4H, "exit_reason": str(t.exit_reason),
            "net_r": float(t.net_r), "gross_r": float(t.gross_r), "fee_r": float(t.fee_r),
            "funding_r": float(t.funding_r),
            "haircut_net_r": haircut(s, float(t.net_r), float(t.fee_r)),
            "era": era_of_entry(t.entry_ms), "lane": str(t.lane),
            # ── extras ────────────────────────────────────────────────────────
            "arm_ms": int(t.arm_ms), "arm_i": int(t.arm_i), "entry_i": int(t.entry_i),
            "exit_ms": int(t.exit_ms), "exit_px": float(t.exit_px),
            "exit_event_ms": int(ev_ms), "exit_event_stamp": str(ev_stamp),
            "atr_at_entry": float(t.atr_at_entry), "mfe_r": float(t.mfe_r),
            "n_advances": int(len(t.advances)), "harvested": bool(t.harvested),
            "reached_1r": bool(t.reached_1r),
            "slip_bps_side": float(fees[s]["slippage_bps_side"]),
            "slippage_tier": str(fees[s]["slippage_tier"]),
            "lag": fx["lag"], "r_over_atr": fx["r_over_atr"],
            "tide_streak_entry": fx["tide_streak_entry"], "tide_edge_q75": fx["tide_edge_q75"],
            "tide_band": fx["tide_band"], "tide_streak_age_arm": fx["tide_streak_age_arm"],
            "priority_substitute": bool(getattr(t, "priority_substitute", False)),
        })
    df = pd.DataFrame(rows)
    if not len(df):
        df = pd.DataFrame({c: pd.Series(dtype=object) for c in REQUIRED})
    for c in REQ_INT + ("arm_ms", "arm_i", "entry_i", "exit_ms", "exit_event_ms",
                        "n_advances", "lag", "tide_streak_entry", "tide_streak_age_arm"):
        if c in df.columns:
            df[c] = df[c].astype("int64")
    df["direction"] = df["direction"].astype("int8")
    for c in REQ_FLOAT:
        df[c] = df[c].astype("float64")
    for c in REQ_STR:
        df[c] = df[c].astype(str)
    return df.sort_values(["symbol", "entry_close_ms"], kind="mergesort").reset_index(drop=True)


def canonical_csv(df: pd.DataFrame) -> bytes:
    """THE canonical CSV of the 16 required columns (module docstring)."""
    d = df.sort_values(["symbol", "entry_close_ms"], kind="mergesort")
    lines = [",".join(REQUIRED)]
    for row in d[list(REQUIRED)].itertuples(index=False):
        out = []
        for c, v in zip(REQUIRED, row):
            if c in REQ_FLOAT:
                out.append(repr(float(v)))
            elif c in REQ_INT or c == "direction":
                out.append(str(int(v)))
            else:
                sv = str(v)
                if "," in sv or "\n" in sv:
                    _halt(f"a string field {c}={sv!r} holds ',' or a newline")
                out.append(sv)
        lines.append(",".join(out))
    return ("\n".join(lines) + "\n").encode("utf-8")


def book_sha256(df: pd.DataFrame) -> str:
    return hashlib.sha256(canonical_csv(df)).hexdigest()


def regbook_dfs(R: dict) -> dict:
    """{(reg, arm): (kind, ruler, era_scope, frame, description)} — every arm."""
    pool = R["pool"]
    v6, sc_age, sc_win = R["v6"], R["books"]["P-AGE-1"], R["books"]["P-WIN-1"]
    f_v6 = regbook_frame(v6, pool)
    f_age, f_win = regbook_frame(sc_age, pool), regbook_frame(sc_win, pool)
    rs = R["refused"]
    base_desc = ("the v6 book [L-1.6]: TP.CONTROL_CARD + T9.V6_ROLES on CLASSIC5 over the "
                 "full TC11 corridor (TP._book_sha " + V6_BOOK_SHA[:16] + "…, n 200); the "
                 "two-sample comparison book")
    out = {
        (REG_AGE, "scored"): ("scored", "two_sample", "full", f_age,
                              "v6 minus the campaigns whose ENTRY-bar tide streak "
                              "(tierc7_lab_regime.tide_streak) >= the trailing q75 edge (B4 "
                              "OLD; tierc9._trailing_edges over CLASSIC5 4h bars with open <= "
                              "the entry bar, >= 30 bars) [L-G.1]; a post-filter [L-1.5]"),
        (REG_AGE, "base"): ("base", "two_sample", "full", f_v6, base_desc),
        (REG_AGE, "tierE__shadow_abs206"): (
            "tierE", "two_sample", "full",
            regbook_frame(apply_gate(v6, rs["P-AGE-1/shadow_abs206"]), pool),
            "SHADOW absolute: v6 minus ENTRY-bar tide streak > 206 bars, exactly as written; "
            + ABS_LABEL),
        (REG_AGE, "tierE__tuning"): ("tierE", "two_sample", "tuning",
                                     f_age[f_age["era"] == "tuning"].reset_index(drop=True),
                                     "the scored arm's TUNING slice (era by the entry bar's "
                                     "CLOSE, L-1.3); compare with `base` sliced to era == "
                                     "tuning"),
        (REG_AGE, "tierE__holdout"): ("tierE", "two_sample", "holdout",
                                      f_age[f_age["era"] == "holdout"].reset_index(drop=True),
                                      "the scored arm's HOLDOUT slice (era by the entry bar's "
                                      "CLOSE, L-1.3); compare with `base` sliced to era == "
                                      "holdout"),
        (REG_AGE, "tierE__refused_cohort"): (
            "tierE", "vs_zero", "full",
            regbook_frame([t for t in v6 if key_of(t) in rs["P-AGE-1"]], pool),
            "the REFUSED cohort of P-AGE-1 (B4 OLD at the entry bar): n / mean / ΣR printed "
            "on the gate row [L-1.5]"),
        (REG_WIN, "scored"): ("scored", "two_sample", "full", f_win,
                              "v6 minus campaigns with lag = entry_i - arm_i >= 16 (4h bars) "
                              "[L-G.2]; a post-filter [L-1.5]"),
        (REG_WIN, "base"): ("base", "two_sample", "full", f_v6, base_desc),
        (REG_WIN, "tierE__shadow_lag7_15"): (
            "tierE", "two_sample", "full",
            regbook_frame(apply_gate(v6, rs["P-WIN-1/shadow_lag7_15"]), pool),
            "SHADOW cut: v6 minus lag 7..15 [L-G.2]"),
        (REG_WIN, "tierE__tuning"): ("tierE", "two_sample", "tuning",
                                     f_win[f_win["era"] == "tuning"].reset_index(drop=True),
                                     "the scored arm's TUNING slice (era by the entry bar's "
                                     "CLOSE, L-1.3); compare with `base` sliced to era == "
                                     "tuning"),
        (REG_WIN, "tierE__holdout"): ("tierE", "two_sample", "holdout",
                                      f_win[f_win["era"] == "holdout"].reset_index(drop=True),
                                      "the scored arm's HOLDOUT slice (era by the entry bar's "
                                      "CLOSE, L-1.3); compare with `base` sliced to era == "
                                      "holdout"),
        (REG_WIN, "tierE__refused_cohort"): (
            "tierE", "vs_zero", "full",
            regbook_frame([t for t in v6 if key_of(t) in rs["P-WIN-1"]], pool),
            "the REFUSED cohort of P-WIN-1 (lag >= 16): n / mean / ΣR printed on the gate "
            "row [L-1.5]"),
        (REG_WIN, "tierE__ratr_admission"): (
            "tierE", "two_sample", "full",
            regbook_frame(apply_gate(v6, rs["L-G.3/ratr_admission"]), pool),
            "L-G.3 structure-distance ADMISSION: v6 minus r_over_atr = r_dist / "
            "ATR14_4h(entry) > 2.2 (a post-filter)"),
        (REG_WIN, "tierE__ratr_priority"): (
            "tierE", "two_sample", "full", regbook_frame(R["priority"], pool),
            "L-G.3 within-window PRIORITY book: replay9's loop; a window whose first 12/26 "
            "trigger has r_over_atr > 2.2 is passed and its entry is the first later "
            "same-direction 12/26 cross before the window closes with the asset flat and "
            "r_over_atr <= 2.2; ridden by tierc11_ride.ride11 from its 4h close; "
            f"{R['prio_summary']['n_substituted']} substitutions (priority_substitute)"),
    }
    return out


# ═══════════════════════════════════════════════════════════════ STATISTICS
def stats(net: pd.Series | np.ndarray | list) -> dict:
    v = np.asarray(list(net), dtype=float)
    n = int(len(v))
    if n == 0:
        return {"n": 0, "mean_net_r": float("nan"), "sum_net_r": 0.0,
                "win_pct": float("nan"), "nan_reason": "n = 0: no campaign in the cell"}
    tot = math.fsum(float(x) for x in v)          # exactly rounded: order-free
    return {"n": n, "mean_net_r": tot / n, "sum_net_r": tot,
            "win_pct": float(100.0 * (v > 0).sum() / n), "nan_reason": ""}


def collar(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    for k, v in COLLAR.items():
        d[k] = v
    return d


# ═════════════════════════════════════════════════════════════════ COMPUTE
def pin_record() -> dict:
    """AS_OF_PIN.json (tierc11_books.as_of_pin_record): the pin and the latest close at
    fetch time printed beside it [L-0.1].  HALTs unless it names PIN_MS."""
    rec = B.as_of_pin_record()
    if int(rec.get("as_of_last_closed_4h_close_ms", -1)) != int(PIN_MS):
        _halt(f"AS_OF_PIN.json names {rec.get('as_of_last_closed_4h_close_ms')}, not {PIN_MS}")
    return rec


def compute() -> dict:
    regs = registrations()
    pin_rec = pin_record()
    lo, hi, meta = B.corridor()
    v6, arms = v6_replay(lo, hi)
    pool = B.tide_pool(lo, hi)
    facts = facts_frame(v6, pool)
    # the written campaign table agrees on every band / flag the gates read
    camp = pd.read_parquet(str(B.OUT / "v6_campaigns.parquet"))
    m = camp.merge(facts, on=["symbol", "entry_ms"], suffixes=("_camp", ""))
    if len(m) != len(facts) or len(camp) != len(facts):
        _halt("books/v6_campaigns.parquet does not hold the v6 book's keys")
    dis = [c for c, w in (("tide_band", "tide_band_camp"), ("lag", "lag_camp"),
                          ("tide_streak_entry", "tide_streak_entry_camp"))
           if not (m[c].astype(str) == m[w].astype(str)).all()]
    if not (m["r_over_atr_gt_2p2"].astype(bool) == m["ratr_refused"].astype(bool)).all():
        dis.append("r_over_atr_gt_2p2")
    if not (m["tide_abs_gt206"].astype(bool) == m["age_abs206_refused"].astype(bool)).all():
        dis.append("tide_abs_gt206")
    if dis:
        _halt(f"the gate facts disagree with books/v6_campaigns.parquet on {dis}")
    refused = {g: refused_keys(facts, g) for g in GATE_ORDER}
    books = {g: apply_gate(v6, refused[g]) for g in GATE_ORDER}
    for g in GATE_ORDER:                    # the post-filter law, held before writing
        kb = [key_of(t) for t in books[g]]
        if set(kb) != {key_of(t) for t in v6} - refused[g] or len(kb) != len(v6) - len(refused[g]):
            _halt(f"gate {g}: the gated book is not v6 minus exactly its refused set")
    # the priority book + its identity control
    prio, plog = replay_book(lo, hi, priority_cut=RATR_CUT)
    ident, _ = replay_book(lo, hi)
    if TP._book_sha(ident) != V6_BOOK_SHA:
        _halt("replay_g with no hook is not the v6 book")
    # the re-ride rival books (a refusal hook per gate)
    reride = {g: replay_book(lo, hi, refuse=refuse_hook(g, pool)) for g in GATE_ORDER}
    rivals = rival_rows(arms, v6, pool, facts)
    R = {"regs": regs, "pin_rec": pin_rec, "lo": lo, "hi": hi, "meta": meta, "v6": v6,
         "arms": arms,
         "pool": pool, "facts": facts, "refused": refused, "books": books,
         "priority": prio, "prio_log": plog, "reride": reride, "rivals": rivals,
         "ident_sha": TP._book_sha(ident)}
    R["prio_summary"] = priority_summary(R)
    R["tables"] = tables(R)
    return R


# ═════════════════════════════════════════════════════════════════ THE TABLES
def priority_summary(R: dict) -> dict:
    v6k = {key_of(t) for t in R["v6"]}
    pk = {key_of(t) for t in R["priority"]}
    lg = pd.DataFrame(R["prio_log"])
    oc = lg["outcome"].value_counts().to_dict()
    # the structural reason the one-position rule barely binds: v6's BELL exits a
    # campaign at its window's counter 12/89 cross at the latest, and that bar is
    # the next window's arm bar
    wend = {(s, int(a.arm_i), int(a.direction)): int(a.window_end_i)
            for s in E.CLASSIC5 for a in R["arms"][s]}

    def after_end(book):
        return int(sum(1 for t in book
                       if int(t.exit_i) > wend[(t.symbol, int(t.arm_i), int(t.direction))]))
    return {"n": len(R["priority"]),
            "n_exit_after_window_end_bar_v6": after_end(R["v6"]),
            "n_exit_after_window_end_bar_priority": after_end(R["priority"]),
            "n_scan_not_flat": int(lg["n_scan_not_flat"].sum()),
            "n_position_open_priority": int(oc.get("position_open", 0)),
            "n_position_open_v6": int(sum(1 for s in E.CLASSIC5 for a in R["arms"][s]
                                          if a.reject == "position_open")),
            "sum_net_r": math.fsum(float(t.net_r) for t in R["priority"]),
            "n_substituted": int(sum(bool(t.priority_substitute) for t in R["priority"])),
            "n_windows": int(len(lg)),
            "outcomes": {k: int(oc[k]) for k in sorted(oc)},
            "n_v6_not_taken": len(v6k - pk), "n_new_not_in_v6": len(pk - v6k),
            "n_shared": len(v6k & pk)}


def _row(label: dict, net) -> dict:
    return {**label, **stats(net)}


def era_slice_rows(pairs) -> list[dict]:
    """[(registration, book name, trades)] -> the era-slice rows (tuning / holdout /
    full), the era by the entry bar's CLOSE (era_of_entry) [L-1.3]."""
    rows = []
    for reg, book_name, bk in pairs:
        for era in ("tuning", "holdout", "full"):
            sel = [float(t.net_r) for t in bk
                   if era == "full" or era_of_entry(t.entry_ms) == era]
            rows.append(_row({"registration": reg, "book": book_name, "era": era}, sel))
    return rows


FLAT_CLAIM = ("On this corridor 'asset flat' never binds and the re-ride rival is 0 for "
              "every gate (every count this sentence rests on is 0).")


def flat_claim(ps: dict, gate_rows: pd.DataFrame) -> str:
    """The one-position sentence of STAGE_G.md, from the COMPUTED counts: FLAT_CLAIM only
    when every count it rests on is 0; otherwise the non-zero counts, named."""
    counts = (("position_open rejections, v6 ride", int(ps["n_position_open_v6"])),
              ("position_open rejections, priority ride", int(ps["n_position_open_priority"])),
              ("substitute crosses skipped for 'asset not flat'", int(ps["n_scan_not_flat"])),
              ("rivals in the rejection log, all gates",
               int(gate_rows["rival_count_rejection_log"].sum())),
              ("re-ride campaigns not in v6, all gates",
               int(gate_rows["reride_admitted_not_in_v6"].sum())))
    if all(v == 0 for _k, v in counts):
        return FLAT_CLAIM
    return ("On this corridor the one-position rule acts: "
            + "; ".join(f"{k} {v}" for k, v in counts) + ".")


def tables(R: dict) -> dict:
    v6, facts, refused = R["v6"], R["facts"], R["refused"]
    net_v6 = [float(t.net_r) for t in v6]
    s_v6 = stats(net_v6)
    T = {}
    # ── registered books (no collar: book arithmetic, not a verdict) ─────────────
    rows = []
    for reg, gate in ((REG_AGE, "P-AGE-1"), (REG_WIN, "P-WIN-1")):
        for arm, bk in (("scored", R["books"][gate]), ("base", v6)):
            s = stats([float(t.net_r) for t in bk])
            rows.append({"registration": reg, "arm": arm, "gate": gate if arm == "scored" else "",
                         "n": s["n"], "sum_net_r": s["sum_net_r"], "mean_net_r": s["mean_net_r"],
                         "win_pct": s["win_pct"],
                         "sum_haircut_net_r": math.fsum(haircut(t.symbol, t.net_r, t.fee_r)
                                                        for t in bk),
                         "book_sha_tp": TP._book_sha(bk), "label": BOOK_NOTE})
    T["g_registered_books"] = (pd.DataFrame(rows), ["registration", "arm"], False)
    # ── gate rows (L-1.5): refused cohort + both books + the rival disclosure ─────
    rows = []
    for g in GATE_ORDER:
        bk = R["books"][g]
        ref = [t for t in v6 if key_of(t) in refused[g]]
        sb, sr = stats([float(t.net_r) for t in bk]), stats([float(t.net_r) for t in ref])
        tag = g.replace("/", "__").replace("-", "_").replace(".", "_")
        rv = R["rivals"]
        n_riv = int(rv[f"rival__{tag}"].sum()) if len(rv) else 0
        n_riv_self = (int((rv[f"rival__{tag}"] & rv[f"rival_self_refused__{tag}"]).sum())
                      if len(rv) else 0)
        rr, _ = R["reride"][g]
        rrk, v6k = {key_of(t) for t in rr}, {key_of(t) for t in v6}
        srr = stats([float(t.net_r) for t in rr])
        forfeit = (f"on per-campaign expectancy only; the gate forfeits "
                   f"{sr['sum_net_r']:+.4f} R total" if sr["n"] and sr["mean_net_r"] > 0 else "")
        rows.append({"gate": g, "registration": GATES[g][0], "rule": GATES[g][1],
                     "caveat": ABS_LABEL if g == "P-AGE-1/shadow_abs206" else "",
                     "n_base": s_v6["n"], "sum_net_r_base": s_v6["sum_net_r"],
                     "n_gated": sb["n"], "sum_net_r_gated": sb["sum_net_r"],
                     "mean_net_r_gated": sb["mean_net_r"],
                     "n_refused": sr["n"], "mean_net_r_refused": sr["mean_net_r"],
                     "sum_net_r_refused": sr["sum_net_r"], "forfeit_note": forfeit,
                     "rival_count_rejection_log": n_riv,
                     "rival_count_self_refused": n_riv_self,
                     "reride_n": srr["n"], "reride_sum_net_r": srr["sum_net_r"],
                     "reride_mean_net_r": srr["mean_net_r"],
                     "reride_admitted_not_in_v6": len(rrk - v6k),
                     "reride_v6_not_taken": len(v6k - rrk)})
    T["g_gate_rows"] = (collar(pd.DataFrame(rows)), ["gate"], True)
    # ── the rival log (every position_open rejection of the v6 ride) ────────────
    rv = R["rivals"].copy()
    if len(rv):
        rv["placeholder"] = False
    else:                                   # nothing to list: sentinels in the KEY only
        rv = pd.DataFrame({"symbol": ["(none)"], "direction": [0], "trigger_ms": [-1],
                           "arm_ms": pd.array([None], dtype="Int64"),
                           "trigger_close_ms": pd.array([None], dtype="Int64"),
                           "blocker_entry_ms": pd.array([None], dtype="Int64"),
                           "blocker_exit_ms": pd.array([None], dtype="Int64"),
                           "blocker_net_r": [float("nan")], "placeholder": [True]})
    T["g_rivals"] = (collar(rv), ["symbol", "trigger_ms", "direction"], True)
    # ── tierE book descriptors (the regbook arms that are Tier-E) ───────────────
    # (filled in build(), after the regbook frames exist)
    # ── era slices of every registered pair ─────────────────────────────────────
    rows = era_slice_rows([(reg, book_name, bk)
                           for reg, gate in ((REG_AGE, "P-AGE-1"), (REG_WIN, "P-WIN-1"))
                           for book_name, bk in (("scored", R["books"][gate]), ("base", v6))])
    T["g_era_slices"] = (collar(pd.DataFrame(rows)), ["registration", "book", "era"], True)
    # ── entry-bar tide bands (the P_AGE_1 table on the TC11 corridor) ───────────
    rows = []
    for b in ("B1", "B2", "B3", "B4", "unbanded"):
        sel = facts[facts["tide_band"] == b]
        rows.append(_row({"measure": "entry_bar_streak (L-G.1 of record)", "band": b,
                          "n_left_censored": int(sel["tide_left_censored"].sum()),
                          "caveat": ""}, sel["net_r"]))
    for b in ("B1", "B2", "B3", "B4", "unbanded"):
        sel = facts[facts["arm_band_on_entry_edges"] == b]
        rows.append(_row({"measure": "arm_bar_tide_streak_age (tierc9, disclosure; banded "
                          "on the same trailing edges)", "band": b,
                          "n_left_censored": int(sel["tide_streak_age_arm_censored"].sum()),
                          "caveat": ""}, sel["net_r"]))
    for lab, col, cens in (("entry_bar_streak > 206 (ABSOLUTE shadow)", "age_abs206_refused",
                            "tide_left_censored"),
                           ("arm_bar_tide_streak_age > 206 (disclosure)", "arm_age_gt206",
                            "tide_streak_age_arm_censored")):
        for v in (True, False):
            sel = facts[facts[col] == v]
            rows.append(_row({"measure": lab, "band": ">206" if v else "<=206",
                              "n_left_censored": int(sel[cens].sum()),
                              "caveat": ABS_LABEL}, sel["net_r"]))
    T["g_tide_bands"] = (collar(pd.DataFrame(rows)), ["measure", "band"], True)
    # ── the cross-tab: entry-bar band x arm-bar band ────────────────────────────
    rows = []
    bands = ("B1", "B2", "B3", "B4", "unbanded")
    for be in bands:
        for ba in bands:
            sel = facts[(facts["tide_band"] == be) & (facts["arm_band_on_entry_edges"] == ba)]
            rows.append(_row({"cell": f"entry:{be}|arm:{ba}", "entry_band": be,
                              "arm_band": ba}, sel["net_r"]))
    T["g_age_crosstab"] = (collar(pd.DataFrame(rows)), ["cell"], True)
    # ── lag bands ───────────────────────────────────────────────────────────────
    rows = []
    for name, _a, _b in B.LAG_BANDS:
        sel = facts[facts["lag_band"] == name]
        rows.append(_row({"lag_band": name}, sel["net_r"]))
    T["g_lag_bands"] = (collar(pd.DataFrame(rows)), ["lag_band"], True)
    # ── the 2x2x2 crossing (partition) and the eight gate books ─────────────────
    rows = []
    for a in (0, 1):
        for w in (0, 1):
            for s in (0, 1):
                cell = f"A{a}|W{w}|S{s}"
                sel = facts[facts["grid_cell"] == cell]
                rows.append(_row({"cell": cell, "age_old": bool(a), "lag_ge16": bool(w),
                                  "ratr_gt2p2": bool(s)}, sel["net_r"]))
    T["g_grid_partition"] = (collar(pd.DataFrame(rows)), ["cell"], True)
    rows = []
    for a in (0, 1):
        for w in (0, 1):
            for s in (0, 1):
                ref = set()
                if a:
                    ref |= refused["P-AGE-1"]
                if w:
                    ref |= refused["P-WIN-1"]
                if s:
                    ref |= refused["L-G.3/ratr_admission"]
                bk = apply_gate(v6, ref)
                cell = (f"age:{'on' if a else 'off'}|win:{'on' if w else 'off'}|"
                        f"ratr:{'on' if s else 'off'}")
                rr = [float(t.net_r) for t in v6 if key_of(t) in ref]
                rows.append({**_row({"cell": cell, "age_gate_on": bool(a),
                                     "win_gate_on": bool(w), "ratr_gate_on": bool(s)},
                                    [float(t.net_r) for t in bk]),
                             "n_refused": len(rr), "sum_net_r_refused": math.fsum(rr)})
    T["g_grid_books"] = (collar(pd.DataFrame(rows)), ["cell"], True)
    # ── the priority window log + substitutions ─────────────────────────────────
    lg = pd.DataFrame(R["prio_log"])
    v6_by = {key_of(t): t for t in v6}
    pr_by = {key_of(t): t for t in R["priority"]}
    lg["v6_net_r_at_first_trigger"] = [
        (float(v6_by[(s, int(m))].net_r) if (s, int(m)) in v6_by else float("nan"))
        for s, m in zip(lg["symbol"], lg["first_trigger_ms"])]
    lg["priority_net_r"] = [
        (float(pr_by[(s, int(m))].net_r) if (s, int(m)) in pr_by else float("nan"))
        for s, m in zip(lg["symbol"], lg["entry_ms"])]
    for c in ("entry_i", "entry_ms"):       # a window with no entry: null, not -1
        lg[c] = pd.array([int(x) if int(x) >= 0 else None for x in lg[c]], dtype="Int64")
    T["g_priority_windows"] = (collar(lg), ["symbol", "arm_ms", "direction"], True)
    # the priority book vs v6, key by key
    rows = []
    for k in sorted(set(v6_by) | set(pr_by)):
        a_, b_ = v6_by.get(k), pr_by.get(k)
        rows.append({"symbol": k[0], "entry_ms": int(k[1]),
                     "in_v6": a_ is not None, "in_priority": b_ is not None,
                     "priority_substitute": bool(getattr(b_, "priority_substitute", False)),
                     "v6_net_r": float(a_.net_r) if a_ is not None else float("nan"),
                     "priority_net_r": float(b_.net_r) if b_ is not None else float("nan"),
                     "r_over_atr": (ratr_of(a_) if a_ is not None else ratr_of(b_))})
    T["g_priority_vs_v6"] = (collar(pd.DataFrame(rows)), ["symbol", "entry_ms"], True)
    # ── cross-asset same-close collisions (disclosure) ──────────────────────────
    rows = []
    for name, bk in (("v6", v6), ("P-AGE-1 scored", R["books"]["P-AGE-1"]),
                     ("P-WIN-1 scored", R["books"]["P-WIN-1"]),
                     ("ratr admission", R["books"]["L-G.3/ratr_admission"]),
                     ("ratr priority", R["priority"])):
        by: dict = {}
        for t in bk:
            by.setdefault(int(t.entry_ms) + MS_4H, []).append(t)
        coll = {k: v for k, v in by.items() if len(v) >= 2}
        mixed = sum(1 for v in coll.values()
                    if len({ratr_refused(ratr_of(t)) for t in v}) > 1)
        rows.append({"book": name, "n_campaigns": len(bk), "n_entry_closes": len(by),
                     "n_collision_closes": len(coll),
                     "n_campaigns_in_collisions": int(sum(len(v) for v in coll.values())),
                     "max_assets_at_one_close": int(max((len(v) for v in by.values()), default=0)),
                     "n_collisions_mixed_ratr_class": int(mixed),
                     "binds": "no — one position per ASSET, no portfolio cap"})
    T["g_collisions"] = (collar(pd.DataFrame(rows)), ["book"], True)
    rows = []
    by = {}
    for t in v6:
        by.setdefault(int(t.entry_ms) + MS_4H, []).append(t)
    for k in sorted(by):
        if len(by[k]) >= 2:
            for t in sorted(by[k], key=lambda x: x.symbol):
                rows.append({"entry_close_ms": int(k), "entry_close": iso(k), "symbol": t.symbol,
                             "direction": int(t.direction), "r_over_atr": ratr_of(t),
                             "net_r": float(t.net_r), "placeholder": False})
    if rows:
        cl = pd.DataFrame(rows)
    else:                                   # nothing to list: sentinels in the KEY only
        cl = pd.DataFrame({"entry_close_ms": [-1], "entry_close": [""], "symbol": ["(none)"],
                           "direction": pd.array([None], dtype="Int64"),
                           "r_over_atr": [float("nan")], "net_r": [float("nan")],
                           "placeholder": [True]})
    T["g_collision_list_v6"] = (collar(cl), ["entry_close_ms", "symbol"], True)
    # ── arrivals after the TC10 pin + the continuation ──────────────────────────
    rows = []
    for t in v6:
        ec = int(t.entry_ms) + MS_4H
        kind = ("entered_after_tc10_pin" if ec > TC10_PIN_MS else
                "continuation" if ec <= TC10_PIN_MS <= int(t.exit_ms) else None)
        if kind is None:
            continue
        fx = facts[(facts["symbol"] == t.symbol) & (facts["entry_ms"] == int(t.entry_ms))].iloc[0]
        rows.append({"kind": kind, "symbol": t.symbol, "entry_ms": int(t.entry_ms),
                     "entry": iso(int(t.entry_ms)), "exit": iso(int(t.exit_ms)),
                     "exit_reason": str(t.exit_reason), "net_r": float(t.net_r),
                     "tide_band": fx["tide_band"], "age_old_refused": bool(fx["age_old_refused"]),
                     "lag": int(fx["lag"]), "win_refused": bool(fx["win_refused"]),
                     "placeholder": False})
    for kind in ("entered_after_tc10_pin", "continuation"):
        if not any(r["kind"] == kind for r in rows):   # nothing to list: sentinels in the KEY only
            rows.append({"kind": kind, "symbol": "(none)", "entry_ms": -1, "entry": "",
                         "exit": "", "exit_reason": "", "net_r": float("nan"), "tide_band": "",
                         "age_old_refused": None, "lag": None, "win_refused": None,
                         "placeholder": True})
    ar = pd.DataFrame(rows)
    ar["lag"] = pd.array(list(ar["lag"]), dtype="Int64")
    for c in ("age_old_refused", "win_refused"):
        ar[c] = pd.array(list(ar[c]), dtype="boolean")
    T["g_arrivals"] = (collar(ar), ["kind", "symbol", "entry_ms"], True)
    # ── every campaign's gate facts ─────────────────────────────────────────────
    T["g_campaign_gates"] = (collar(facts), ["symbol", "entry_ms"], True)
    return T


# ═══════════════════════════════════════════════════════════════════ WRITERS
def _inside(p: Path, root: Path) -> bool:
    return p == root or root in p.parents


def guard_out(out: Path) -> Path:
    """OUT_ROOT; a direct child of DET_ROOT; or a direct child of a `_det_stage_g/`
    directory OUTSIDE the repo tree."""
    o = Path(out).resolve()
    if o == OUT_ROOT.resolve() or o.parent == DET_ROOT.resolve():
        return o
    trees = {ROOT.resolve(), Path(E.MAIN_TREE).resolve()}
    if o.parent.name == DET_NAME and not any(_inside(o, t) for t in trees):
        return o
    _halt(f"output root {o} is neither {OUT_ROOT}, an F-DET run dir under {DET_ROOT}, nor "
          f"one under a {DET_NAME}/ scratch outside the repo")
    return o


def write_regbook(d: Path, reg: str, arm: str, kind: str, ruler: str, era_scope: str,
                  df: pd.DataFrame, desc: str, meta: dict) -> dict:
    d.mkdir(parents=True, exist_ok=True)
    stamped = TP.stamp_n(df, meta, "4h")
    if kind == "tierE":                     # a non-registered table carries the collar [L-1.4]
        stamped = collar(stamped)
    stamped.attrs = {}
    p = d / f"{arm}.parquet"
    tmp = d / f"{arm}.parquet.tmp"
    stamped.to_parquet(str(tmp), index=False)
    tmp.replace(p)
    side = {"registration": reg, "arm": arm, "kind": kind, "ruler": ruler,
            "panel": list(E.CLASSIC5), "era_scope": era_scope, "n": int(len(df)),
            "sum_net_r": math.fsum(float(x) for x in df["net_r"]) if len(df) else 0.0,
            "book_sha256": book_sha256(df), "description": desc,
            "source_script": SOURCE_SCRIPT, "book_sha256_law": BOOK_SHA_LAW,
            "haircut_law": HAIRCUT_LAW, "as_of": PIN_ISO, "seed": SEED}
    if sorted(side) != sorted(SIDECAR_KEYS):
        _halt(f"sidecar keys {sorted(side)} != {sorted(SIDECAR_KEYS)}")
    if kind == "tierE":
        side.update(COLLAR)
    (d / f"{arm}.json").write_text(json.dumps(side, indent=2, sort_keys=True,
                                              ensure_ascii=False) + "\n", encoding="utf-8")
    return side


def build(out_root: Path = OUT_ROOT) -> dict:
    out_root = guard_out(out_root)
    R = compute()
    meta = R["meta"]
    sdir = out_root / STAGE_DIR
    # ── the regbooks ─────────────────────────────────────────────────────────────
    rb = regbook_dfs(R)
    sides, arms_of = {}, {REG_AGE: [], REG_WIN: []}
    for (reg, arm), (kind, ruler, era_scope, df, desc) in rb.items():
        sides[(reg, arm)] = write_regbook(out_root / REGBOOK_DIR / reg, reg, arm, kind, ruler,
                                          era_scope, df, desc, meta)
        arms_of[reg].append(arm)
    for reg in (REG_AGE, REG_WIN):
        st = {"registration": reg, "status": "BUILT",
              "reason": ("every arm built by " + SOURCE_SCRIPT + " on the TC11 corridor "
                         f"(as of {PIN_ISO}); gates are post-filters of the v6 book [L-1.5]"),
              "arms": sorted(arms_of[reg])}
        (out_root / REGBOOK_DIR / reg / "STATUS.json").write_text(
            json.dumps(st, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    # ── the tierE descriptor table (needs the regbook frames) ─────────────────────
    rows = []
    for (reg, arm), (kind, ruler, era_scope, df, desc) in rb.items():
        if kind != "tierE":
            continue
        s = stats(df["net_r"])
        rows.append({"registration": reg, "arm": arm, "ruler": ruler, "era_scope": era_scope,
                     "n": s["n"], "sum_net_r": s["sum_net_r"], "mean_net_r": s["mean_net_r"],
                     "win_pct": s["win_pct"], "nan_reason": s["nan_reason"],
                     "sum_haircut_net_r": (math.fsum(float(x) for x in df["haircut_net_r"])
                                           if len(df) else 0.0),
                     "book_sha256": sides[(reg, arm)]["book_sha256"], "description": desc})
    R["tables"]["g_tiere_books"] = (collar(pd.DataFrame(rows)), ["registration", "arm"], True)
    # ── the stage tables ──────────────────────────────────────────────────────────
    put, W, K, SK = TP.make_put(sdir, meta, lens="4h")
    for name in sorted(R["tables"]):
        df, key, _collared = R["tables"][name]
        put(df, name, key)
    if SK:
        _halt(f"an empty stage table: {SK}")
    R["shas"] = {"content": dict(W), "keys": dict(K)}
    R["sides"] = sides
    # L-1.3: an entry bar straddling the era cut (open <= cut < close) is printed as a count
    straddles = {k: int(((v[3]["entry_ms"] <= ERA_CUT_MS) & (v[3]["entry_close_ms"] > ERA_CUT_MS))
                        .sum()) for k, v in rb.items()}
    def fsha(p: Path) -> str:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    pr = R["pin_rec"]
    man = {
        "tier": "TIER-C11", "stage": "TC11-G", "seed": SEED, "as_of": PIN_ISO,
        "as_of_close_ms": PIN_MS, "substrate": meta["substrate"],
        "as_of_pin_record": {
            "path": "research_outputs/tierc11/data/AS_OF_PIN.json",
            "as_of_last_closed_4h": pr["as_of_last_closed_4h"],
            "latest_closed_4h_at_pin_run": pr["latest_closed_4h_at_pin_run"],
            "pin_equals_latest_closed_at_pin_run": pr.get("pin_equals_latest_closed_at_pin_run")},
        "corridor": {"lo": iso(R["lo"]), "hi_close": iso(R["hi"] + 1),
                     "panel": list(E.CLASSIC5)},
        "sha": W, "keys": K, "skipped_empty": SK,
        "collared_tables": sorted(n for n, (_d, _k, c) in R["tables"].items() if c),
        "uncollared_tables": {n: "registered-book arithmetic (" + BOOK_NOTE + ")"
                              for n, (_d, _k, c) in sorted(R["tables"].items()) if not c},
        "input_sha": TP.input_sha(E.CLASSIC5),
        "v6_book_sha": V6_BOOK_SHA, "replay_g_identity_sha": R["ident_sha"],
        "regbooks": {f"{reg}/{arm}": {"n": s["n"], "sum_net_r": s["sum_net_r"],
                                      "book_sha256": s["book_sha256"], "kind": s["kind"],
                                      "ruler": s["ruler"], "era_scope": s["era_scope"],
                                      "n_entry_bar_straddles_era_cut": straddles[(reg, arm)],
                                      "parquet_file_sha256": fsha(out_root / REGBOOK_DIR / reg
                                                                  / f"{arm}.parquet"),
                                      "sidecar_file_sha256": fsha(out_root / REGBOOK_DIR / reg
                                                                  / f"{arm}.json")}
                     for (reg, arm), s in sorted(sides.items())},
        "regbook_status_file_sha256": {reg: fsha(out_root / REGBOOK_DIR / reg / "STATUS.json")
                                       for reg in (REG_AGE, REG_WIN)},
        "priority": R["prio_summary"],
        "canonical_csv_law": BOOK_SHA_LAW, "haircut_law": HAIRCUT_LAW,
        "registrations": {r: {"sha256": R["regs"][r]["sha256"],
                              "text_sha256": R["regs"][r]["text_sha256"]}
                          for r in (REG_AGE, REG_WIN)},
        "readings": list(READINGS),
    }
    (sdir / MANIFEST).write_text(json.dumps(man, indent=2, sort_keys=True, default=str,
                                            ensure_ascii=False) + "\n", encoding="utf-8")
    (sdir / REPORT).write_text(render_md(R, man), encoding="utf-8")
    R["manifest"] = man
    return R


# ═══════════════════════════════════════════════════════════════════ THE REPORT
def _fmt(v, c: str = "") -> str:
    if v is None or v is pd.NA:
        return "—"
    if isinstance(v, (bool, np.bool_)):
        return "yes" if bool(v) else "no"
    if isinstance(v, (int, np.integer)):
        if c.endswith("_ms") and int(v) > 10 ** 11:
            return iso(int(v))
        return str(int(v))
    if isinstance(v, (float, np.floating)):
        x = float(v)
        if math.isnan(x):
            return "—"
        if c.endswith("_ms") and x > 10 ** 11:
            return iso(int(x))
        return f"{x:+.4f}" if ("net_r" in c or "sum" in c or "mean" in c) else f"{x:.4f}"
    return str(v).replace("|", "¦")


def md_table(df: pd.DataFrame, cols: list | None = None) -> str:
    cols = list(cols or df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in df[cols].itertuples(index=False):
        out.append("| " + " | ".join(_fmt(v, c) for c, v in zip(cols, r)) + " |")
    return "\n".join(out)


def render_md(R: dict, man: dict) -> str:
    T = R["tables"]
    rg = R["regs"]
    L = []
    a = L.append
    a("# TIER-C11 · STAGE G — admission gates (P-AGE-1, P-WIN-1) and the L-G.3 Tier-E structure")
    a("")
    a(f"as_of_last_closed_4h: {PIN_ISO} · latest closed 4h at fetch time (AS_OF_PIN.json "
      f"latest_closed_4h_at_pin_run): {man['as_of_pin_record']['latest_closed_4h_at_pin_run']} "
      f"· substrate {man['substrate']} · corridor "
      f"{man['corridor']['lo']} → {man['corridor']['hi_close']} · CLASSIC5 · seed {SEED} · "
      f"source {SOURCE_SCRIPT}")
    a("")
    a("**No verdict is printed here.** The scorer (`scripts/tierc11_score.py`) reads "
      "`research_outputs/tierc11/regbooks/P-AGE-1/` and `.../P-WIN-1/` and computes every "
      "interval and verdict. Book numbers below are labelled *book, not a verdict*. Every "
      "non-registered table carries the collar (tier = 'TIER-E', selection_not_a_result = "
      "'a SELECTION, not a result', gates = 'nothing').")
    a("")
    a("## Readings built")
    a("")
    for ln in READINGS:
        a(f"- {ln}")
    a("")
    a("## The registrations (texts of record, verified by sha)")
    a("")
    for r in (REG_AGE, REG_WIN):
        spec = rg[r]["operative_spec"]
        a(f"**{r}** (payload sha256 `{rg[r]['sha256']}`)")
        a("")
        a("```")
        a(rg[r]["text_of_record"])
        a("```")
        a("")
        a(f"- scored arm (operative spec): {spec['scored_arm']}")
        a(f"- ruler: {spec['ruler']} vs {spec['base']} · panel {spec['panel']} · era "
          f"{spec['era']}")
        if spec.get("pre_seen"):
            a(f"- **pre_seen:** {spec['pre_seen']}")
        if spec.get("selection_hazard"):
            a(f"- **selection_hazard:** {spec['selection_hazard']}")
        a(f"- honesty label for the §0 cell [L-1.4]: \"<verdict> — IN-SAMPLE RE-SCORE, NOT "
          f"CONFIRMATORY (<hazard>)\"")
        a("")
    a("## Registered books (book, not a verdict)")
    a("")
    a(md_table(T["g_registered_books"][0]))
    a("")
    a("## Gate rows [L-1.5] — refused cohort, both books' ΣR, the re-ride rival")
    a("")
    a("The rival count of record is taken from the v6 ride's REJECTION LOG (T9.replay9 "
      "Arming.reject == 'position_open' whose blocking v6 campaign is refused), first order. "
      "`rival_count_self_refused` = rivals the same gate would refuse at their own trigger "
      "bar. The re-ride book (the gate evaluated on every candidate inside the replay, a "
      "refused trigger not occupying the slot) is printed beside it as a Tier-E book.")
    a("")
    a(md_table(T["g_gate_rows"][0]))
    a("")
    a("§0 gate disclosure per registration [L-1.5] (from the gate rows above; the scorer does "
      "not read them — the build doc takes them from here):")
    a("")
    gr = T["g_gate_rows"][0].set_index("gate")
    for reg in (REG_AGE, REG_WIN):
        x = gr.loc[reg]
        a(f"- **{reg}**: refused n {int(x['n_refused'])} · mean {x['mean_net_r_refused']:+.6f} · "
          f"ΣR {x['sum_net_r_refused']:+.6f}; ΣR base {x['sum_net_r_base']:+.6f} · gated "
          f"{x['sum_net_r_gated']:+.6f}; re-ride rival count (rejection log) "
          f"{int(x['rival_count_rejection_log'])} · re-ride book n {int(x['reride_n'])} ΣR "
          f"{x['reride_sum_net_r']:+.6f} · campaigns not in v6 "
          f"{int(x['reride_admitted_not_in_v6'])}; forfeit note: "
          f"{x['forfeit_note'] or '(none — mean(refused) <= 0)'} (book, not a verdict)")
    a("")
    a("## Tier-E regbook arms")
    a("")
    a(md_table(T["g_tiere_books"][0], ["registration", "arm", "ruler", "era_scope", "n",
                                       "sum_net_r", "mean_net_r", "win_pct",
                                       "sum_haircut_net_r", "book_sha256", "tier",
                                       "selection_not_a_result", "gates"]))
    a("")
    for (reg, arm), s in sorted(R["sides"].items()):
        if s["kind"] == "tierE":
            a(f"- `{reg}/{arm}`: {s['description']}")
    a("")
    a("## Era slices (by the entry bar's CLOSE, L-1.3)")
    a("")
    a(md_table(T["g_era_slices"][0]))
    a("")
    a("## F-DEF: both tide-age definitions, per band")
    a("")
    a(f"Absolute-shadow label: {ABS_LABEL}.")
    a("")
    a(md_table(T["g_tide_bands"][0]))
    a("")
    a("### Entry-bar band × arm-bar band (the cross-tab, 25 cells)")
    a("")
    a(md_table(T["g_age_crosstab"][0]))
    a("")
    a("## Lag bands (L-G.2)")
    a("")
    a(md_table(T["g_lag_bands"][0]))
    a("")
    a("## The three gates crossed 2 × 2 × 2 [L-G.3]")
    a("")
    a("(a) the crossing: the v6 book partitioned by the three refusal flags (A = P-AGE-1 "
      "OLD, W = lag >= 16, S = r_over_atr > 2.2):")
    a("")
    a(md_table(T["g_grid_partition"][0]))
    a("")
    a("(b) the eight gate books (v6 minus the union of the refused sets of the gates on):")
    a("")
    a(md_table(T["g_grid_books"][0]))
    a("")
    a("## The within-window PRIORITY book [L-G.3]")
    a("")
    ps = R["prio_summary"]
    a(f"- n {ps['n']} · ΣR {ps['sum_net_r']:+.6f} (book, not a verdict) · substitutions "
      f"**{ps['n_substituted']}** · windows {ps['n_windows']} · outcomes {ps['outcomes']}")
    a(f"- vs v6: shared keys {ps['n_shared']} · v6 campaigns not taken {ps['n_v6_not_taken']} "
      f"· campaigns not in v6 {ps['n_new_not_in_v6']}")
    a(f"- identity control: replay_g with no hook == the v6 book (TP._book_sha "
      f"{R['ident_sha'][:16]}… == {V6_BOOK_SHA[:16]}…)")
    a(f"- **the one-position rule, measured:** position_open rejections v6 "
      f"{ps['n_position_open_v6']}, priority {ps['n_position_open_priority']}; substitute "
      f"crosses skipped for 'asset not flat' {ps['n_scan_not_flat']}; campaigns exiting AFTER "
      f"their window's end bar v6 {ps['n_exit_after_window_end_bar_v6']}, priority "
      f"{ps['n_exit_after_window_end_bar_priority']}. v6's BELL (12/89 against) exits a "
      f"campaign at its window's counter cross at the latest — the next window's arm bar — "
      f"so a slot can be held into a later window only by a bell bar that is also that "
      f"window's lag-0 trigger. {flat_claim(ps, T['g_gate_rows'][0])}")
    a("")
    a("### Every window of the priority replay, by outcome (counts)")
    a("")
    lg = T["g_priority_windows"][0]
    oc = collar(lg.groupby("outcome").size().reset_index(name="n"))
    a(md_table(oc))
    a("")
    a("### The priority window log (every window, whole)")
    a("")
    a(md_table(lg, ["symbol", "direction", "arm_ms", "first_trigger_ms", "first_r_over_atr",
                    "window_end_i", "outcome", "entry_ms", "entry_r_over_atr", "n_scanned",
                    "n_scan_not_flat", "n_scan_no_stop", "n_scan_over_cut",
                    "v6_net_r_at_first_trigger", "priority_net_r", *TIERE_KEYS]))
    a("")
    a("### The priority book vs v6, key by key (whole)")
    a("")
    a(md_table(T["g_priority_vs_v6"][0]))
    a("")
    a("## Cross-asset same-close collisions (disclosure; cannot bind)")
    a("")
    a(md_table(T["g_collisions"][0]))
    a("")
    a("v6 collisions, listed whole:")
    a("")
    a(md_table(T["g_collision_list_v6"][0]))
    a("")
    a("## The re-ride rival log (every position_open rejection of the v6 ride)")
    a("")
    a("A row with placeholder = yes means there is nothing to list: its key fields are "
      "sentinels ('(none)', -1, 0) and every other field is null.")
    a("")
    a(md_table(T["g_rivals"][0]))
    a("")
    a("## Campaigns entered after the TC10 pin (2026-09-21T16:00Z), and the continuation")
    a("")
    a("continuation = entered at a close <= the TC10 pin, exit bar opening at or after it (open "
      "at the TC10 pin). A row with placeholder = yes means there is nothing of that kind: its "
      "key fields are sentinels ('(none)', -1) and every other field is empty or null.")
    a("")
    a(md_table(T["g_arrivals"][0]))
    a("")
    a("## Every v6 campaign's gate facts (200 rows, whole)")
    a("")
    a(md_table(T["g_campaign_gates"][0], ["symbol", "entry_ms", "direction", "era", "net_r",
                                          "tide_streak_entry", "tide_edge_q75", "tide_band",
                                          "age_old_refused", "age_abs206_refused",
                                          "tide_streak_age_arm", "arm_band_on_entry_edges",
                                          "lag", "win_refused", "lag7_15_refused",
                                          "r_over_atr", "ratr_refused", "grid_cell",
                                          *TIERE_KEYS]))
    a("")
    a("## Files")
    a("")
    for name, sha in sorted(man["sha"].items()):
        a(f"- `stage_g/{name}.parquet` content sha {sha} (key {man['keys'][name]}; floats "
          f"at 6 dp)")
    for k, v in sorted(man["regbooks"].items()):
        a(f"- `regbooks/{k}.parquet` n {v['n']} · ΣR {v['sum_net_r']:+.6f} · book_sha256 "
          f"{v['book_sha256']} · parquet file sha256 {v['parquet_file_sha256']} ({v['kind']}, "
          f"{v['ruler']}, {v['era_scope']}; entry bars straddling the era cut "
          f"{v['n_entry_bar_straddles_era_cut']})")
    a("")
    a(f"Canonical CSV law of book_sha256: {man['canonical_csv_law']}.")
    a("")
    a("Fixtures: `scripts/tierc11_stage_g_fixtures.py` (F-DEF · F-GATE · F-PRIORITY · F-GRID · "
      "F-KEY · F-DET); transcript of record `research_outputs/tierc11/stage_g/"
      "FIXTURES_STAGE_G.txt`.")
    a("")
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    od = next((a.split("=", 1)[1] for a in args if a.startswith("--out-dir=")), None)
    R = build(Path(od) if od else OUT_ROOT)
    for (reg, arm), s in sorted(R["sides"].items()):
        print(f"{reg}/{arm}: n {s['n']} · ΣR {s['sum_net_r']:+.6f} · {s['book_sha256'][:16]}…")
    print(f"priority: {R['prio_summary']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
