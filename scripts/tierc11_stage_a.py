#!/usr/bin/env python
"""TIER-C11 · STAGE A · ADDS, DECIDED ["add"] — the P-ADD-BRK and P-ADD-SFP books
[LEANS L-A.1, L-A.2, L-A.3, L-W.0, L-W.3, L-1.5; AMENDMENTS AM-3, AM-5, AM-6, AM-7].

Contract of record: exchange/queue/2026-09-24_TC11_APOLLO.md (sha256 bb38e016…,
STEP Q b9ed953).  Executor HEPHAESTUS; seed 20260924.  Readings of record:
research_outputs/tierc11/LEANS.md (655e1605…) + LEANS_AMENDMENTS.md (AM-1..AM-7).
Registrations of record: research_outputs/tierc11/registrations/REGISTRATIONS.json
(P-ADD-BRK seq 7, P-ADD-SFP seq 8).  A RUNNER: it imports tierc11_nest (the only
module that reaches the range machine) and hands the ride PLAIN event instants —
the decision module (tierc11_ride) never sees a range object [L-F.2].

WHAT IT BUILDS
  For each CLASSIC5 v6 campaign (the v6 book of record, tierc11_books.v6_book over
  the full TC11 corridor), the 1h range facts at the CALIBRATED 1h pick
  (N.range_facts(stem, '1h', 'calibrated'); the frozen-3.0 twin beside) give the
  candidate ADD EVENTS:
    P-ADD-BRK  a 1h macro death (breakout-die of a CONFIRMED range) whose
               breakout side is the trade's direction (TOP death for a long,
               BOTTOM for a short), known at its 1h close  [L-A.2]
    P-ADD-SFP  a 1h harden (swing failure: a close back inside within 7 bars of
               the breach) in the trade's favour — a SPRING (bottom harden) for a
               long, an UPTHRUST (top harden) for a short — known at its 1h
               close; hardens occur only on confirmed ranges  [L-A.3]
  The candidates of a campaign are the same-direction events whose 1h close lies
  in (entry close, close of the exit 4h bar]; they are handed, as (1h close ms,
  None) pairs, to tierc11_ride's add hook (RD.transform_book(adds_of=…) ->
  RD.admit_adds), which admits at most 2 that are IN-TRADE (1h close > the entry
  close and < the 1h-resolved exit) and AFTER the +1R latch (the latch child
  counts as after), each a 0.5-unit tranche priced at the TAPE's 1h close (an
  event on an L-W.0 mismatch bar is taken at the parent's close), booked by
  tierc7._account_chain (Add.i = the 4h bar containing the 1h close; exit at the
  campaign's exit price; never harvested; the D12 ceiling ONCE on the total).
  Every passed event gets a disposition.

  REGBOOKS (the scorer reads ONLY these): research_outputs/tierc11/regbooks/<REG>/
    scored                      the registration's scored arm (full corridor)
    base                        the v6 book in this schema (the walked v6 ride,
                                hooks off — identical to v6 at 0.000e+00)
    tierE__frozen3              the same rule on the frozen-3.0 1h scale
    tierE__refuse_below_entry   the twin refusing adds priced below the entry
    tierE__refuse_post_harvest  the twin refusing adds after the harvest fired
                                (or inside its 4h bar)
    tierE__tuning / __holdout   the scored book's era slices (era by ENTRY CLOSE)
    tierE__head_to_head_vs_p_add_sfp (under P-ADD-BRK) / tierE__head_to_head_vs_p_add_brk
                                (under P-ADD-SFP): the scored book, ruled (paired)
                                against the OTHER registration's scored arm
                                (sidecar base_arm, the scorer's SC-3)
  + STATUS.json.  STAGE TABLES (research_outputs/tierc11/stage_a/): every add,
  every disposition, every acted campaign's Δ decomposition (AM-3), the
  head-to-head, the disposition grid, the 1h event tape, pick stability, the
  mismatch bars (AM-5), and STAGE_A.md (every table whole).

IDENTITY LAW [L-1.5]: every campaign on which the rule admits no add carries
v6's net_r, exit_ms and exit_reason exactly (RD.identity_findings, HALT on any
finding); every acted campaign keeps the v6 leg (exit bar, price, reason).
AM-3: the paired Δ is net_r(book) − net_r(v6); each acted row prints add_r and
the cap-absorbed funding beside it, and Δ − add_r == absorbed(book) −
absorbed(v6) is asserted to 1e-9 (never Δ == add_r).

NAMED-EVENT INSTANTS [SA-12; L-R.5, AM-6; the lanes pass, 2026-09-25]: every arm carries
the EXTRA columns add1_close_ms / add2_close_ms (Int64) = the instant of the first / second
ADMITTED add (Add.ms: the 1h close of its event, or the parent's close on an L-W.0
mismatch bar), NA where the campaign holds fewer adds — close events, stamped at their
close.  Extra columns only: the 16 required columns, every number, book_sha256 and every
sidecar are unchanged; Stage R's nest-book door reads them instead of refusing the add
arms UNSTAMPED.  FIXTURE SEAM: `add_instants_of`.

WHAT WOULD MAKE THIS WRONG: an event taken before its 1h close (look-ahead); a
death on the wrong side (a bottom death added to a long); an add before the +1R
latch; a third add; a price other than the tape's 1h close; re-admitting a
campaign into a freed slot; the frozen-3.0 events standing in for the scored
arm; an era read by the bar OPEN.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_a.py               # canonical build
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_a.py --out-dir=DIR # F-DET twin
      (DIR a direct child of research_outputs/tierc11/stage_a/_det_stage_a/, or of
       a `_det_stage_a/` directory OUTSIDE the repo tree)
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_nest as N                    # noqa: E402  (env shim first; the range door)
import tierc11_ride as RD                   # noqa: E402  (the decision module: plain instants in)
import tierc11_books as B                   # noqa: E402  (the v6 book of record)

import numpy as np                          # noqa: E402
import pandas as pd                         # noqa: E402

E = N.E
TP, T9, TB = E.TP, E.T9, E.TB
CARD, ROLES = TP.CONTROL_CARD, T9.V6_ROLES
iso = T9.iso

# ══════════════════════════════════════════════════════════ CONSTANTS OF RECORD
PIN_MS = E.PIN_MS
PIN_ISO = "2026-09-25T00:00:00Z"
SEED = E.SEED
ERA_CUT_MS = E.ERA_CUT_MS
MS_1H, MS_4H = 3_600_000, 14_400_000
LENS = "1h"                                  # "ONE LENS BELOW the trade (1h for a 4h campaign)"
SCALE_RECORD, SCALE_TWIN = "calibrated", "frozen3.0"
REGS = ("P-ADD-BRK", "P-ADD-SFP")
EVENT_OF = {"P-ADD-BRK": "death", "P-ADD-SFP": "harden"}
RIDDEN = ("scored", "tierE__frozen3", "tierE__refuse_below_entry", "tierE__refuse_post_harvest")
SCALE_OF_ARM = {"scored": SCALE_RECORD, "tierE__frozen3": SCALE_TWIN,
                "tierE__refuse_below_entry": SCALE_RECORD,
                "tierE__refuse_post_harvest": SCALE_RECORD}
OPTS_OF_ARM = {"scored": {}, "tierE__frozen3": {},
               "tierE__refuse_below_entry": {"refuse_below_entry": True},
               "tierE__refuse_post_harvest": {"refuse_post_harvest": True}}
SLICES = {"tierE__tuning": "tuning", "tierE__holdout": "holdout"}
# SA-11 the head-to-head Tier-E arm ("head-to-head vs P-ADD-SFP / P-ADD-BRK" in the
# registrations' tier_e_arms): the slug is the registration text's own, slugged
# ([a-z0-9_]); ruled (paired) against the OTHER registration's scored arm via the
# sidecar's base_arm (the scorer's SC-3).
OPPONENT = {"P-ADD-BRK": "P-ADD-SFP", "P-ADD-SFP": "P-ADD-BRK"}
H2H_ARM = {"P-ADD-BRK": "tierE__head_to_head_vs_p_add_sfp",
           "P-ADD-SFP": "tierE__head_to_head_vs_p_add_brk"}
H2H_BASE = {rule: f"{OPPONENT[rule]}/scored" for rule in REGS}
TIER_E_ARMS_OF = {rule: (H2H_ARM[rule],) + RIDDEN[1:] + tuple(SLICES) for rule in REGS}
ARMS_OF = {rule: ("scored", "base") + TIER_E_ARMS_OF[rule] for rule in REGS}
DISPOSITIONS = ("admitted", "refused: pre-entry", "refused: not before the 1h-resolved exit",
                "refused: before the +1R latch", "refused: below entry (twin)",
                "refused: post-harvest (twin)", f"refused: cap {RD.ADDS_MAX} reached")
COLLAR = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
          "gates": "nothing"}
BOOK_LABEL = "book, not a verdict"
NEITHER = "neither promoted by the other's failure"
RESIDUAL_TOL = 1e-9                          # a REPRESENTATION tolerance (AM-3 identity)
TAKER_BPS_SIDE = 5.0                         # AM-7: haircut = net - fee * (slip / 5.0)

REQUIRED = ("symbol", "entry_ms", "entry_close_ms", "direction", "entry_px", "stop_px",
            "r_dist", "exit_close_ms", "exit_reason", "net_r", "gross_r", "fee_r",
            "funding_r", "haircut_net_r", "era", "lane")
REQ_DTYPES = {"symbol": "object", "entry_ms": "int64", "entry_close_ms": "int64",
              "direction": "int8", "entry_px": "float64", "stop_px": "float64",
              "r_dist": "float64", "exit_close_ms": "int64", "exit_reason": "object",
              "net_r": "float64", "gross_r": "float64", "fee_r": "float64",
              "funding_r": "float64", "haircut_net_r": "float64", "era": "object",
              "lane": "object"}
BOOK_SHA_LAW = ("sha256 of a canonical CSV of the REQUIRED columns (in the order "
                f"{list(REQUIRED)}), rows sorted by (symbol, entry_close_ms); first line = "
                "the column names joined by ','; one line per row, fields joined by ','; "
                "floats as repr(float(x)), ints as str(int(x)), strings raw; every line "
                "ends '\\n'; UTF-8")

OUT = E.OUT / "stage_a"
REGBOOKS = E.OUT / "regbooks"
DET_ROOT = OUT / "_det_stage_a"
REPORT = "STAGE_A.md"
MANIFEST = "STAGE_A_MANIFEST.json"
SOURCE = "scripts/tierc11_stage_a.py"

TABLE_KEYS = {
    "ADDS": ["registration", "arm", "symbol", "entry_ms", "seq"],
    "DISPOSITIONS": ["registration", "arm", "symbol", "entry_ms", "event_ms", "event_rid"],
    "ACTED": ["registration", "arm", "symbol", "entry_ms"],
    "DISPOSITION_COUNTS": ["registration", "arm", "disposition"],
    "HEAD_TO_HEAD": ["arm", "registration"],
    "OVERLAP": ["arm"],
    "TIER_E_ARMS": ["registration", "arm"],
    "REGISTERED_BOOKS": ["registration", "arm"],
    "EVENTS_1H": ["asset", "scale_kind", "event_kind", "event_i"],
    "PICK_STABILITY_1H": ["asset"],
    "MISMATCH_BOOKS": ["registration", "arm"],
    "MISMATCH_BARS": ["asset", "bar_open_ms"],
}
TABLE_LENS = {"EVENTS_1H": "1h", "PICK_STABILITY_1H": "1h"}
UNCOLLARED = ("REGISTERED_BOOKS",)           # the registered books' own summary (no verdict)

LEAN = "[LEAN-HEPHAESTUS]"
READINGS = (
    f"{LEAN} SA-1 EVENTS [L-A.2, L-A.3]: from N.range_facts(stem, '1h', scale) (plain "
    "arrays): P-ADD-BRK = die_* rows (machine 'breakout-die' of a CONFIRMED range), trade "
    "direction = die_dir (+1 top death -> long, -1 bottom -> short); P-ADD-SFP = harden_* "
    "rows, trade direction = harden_dir (+1 bottom harden = spring -> long, -1 top harden "
    "= upthrust -> short). Known at the event bar's 1h close (known_at == event bar holds "
    "by the nest's construction, so its assert cannot fail; the as-of guard is F-ADD's "
    "prefix run of the machine); a confirmed range of the same rid alive at the prior 1h "
    "close (asserted); a death leaves it dead at its bar, a harden leaves it alive "
    "(asserted).",
    f"{LEAN} SA-2 CANDIDATES: per campaign, the same-direction events whose 1h close lies in "
    "(entry close, close of the exit 4h bar]; handed as (1h close ms, None) to "
    "RD.transform_book(walk=True, adds_of=...) -> RD.admit_adds, which decides in-trade "
    "(> entry close, < the 1h-resolved exit), after the +1R latch (latch child counts), the "
    "twins, then the 2-add cap (AM-6 s4), the tape's 1h close as the price (s5), a "
    "mismatch-bar event taken at the parent's close (L-W.0).",
    f"{LEAN} SA-3 SCALE [L-R.2]: the calibrated 1h pick of record (SCALE_PICKS.json, "
    "tuning-era calibration) for the scored arm and every twin but tierE__frozen3 (frozen "
    "3.0, fully causal). Every add row carries scale_in_sample (a calibrated read at an "
    "instant <= 2024-06-30T23:59:59Z), pick_window and stability_changed.",
    f"{LEAN} SA-4 BASE ARM: the v6 book in the regbook schema = RD.transform_book(v6, "
    "walk=True) with every hook off, asserted identical to v6 (TP.ctrl_diff worst "
    "0.000e+00, identity helper acted 0) AND to books/v6_campaigns.parquet on its 13 "
    "regbook columns at that file's 6 dp. exit_close_ms = the v6 book of record's "
    "exit_close_ms (the exit bar's 4h close; for a stop exit the L-R.5 post-event twin) on "
    "EVERY arm (the add books keep the v6 leg); the 1h-RESOLVED exit instant (L-W.3: a stop "
    "at the close of the first 1h child touching it, a bell at the 4h close, a mismatch-bar "
    "stop at the parent's close) rides beside as exit_close_1h_ms and is the instant the "
    "in-trade test uses; entry_ms = v6's entry_ms (the pairing key); entry_close_ms = "
    "entry_ms + 4h.",
    f"{LEAN} SA-5 ERA SLICES [L-1.3]: tierE__tuning / tierE__holdout = the scored book's "
    "rows with E.era_of(entry_close_ms) == the slice; paired against the base arm "
    "restricted to the same keys.",
    f"{LEAN} SA-6 HAIRCUT [AM-7]: haircut_net_r = net_r - fee_r x (slip_bps_side / 5.0), "
    "slip = the stem's charter tier (E.fees(): A 2 / B 5 / C 10 bps per side); fee_r is "
    "the ride's taker fee over every fill incl. the adds' entries and exits.",
    f"{LEAN} SA-7 Δ [AM-3]: delta_net_r = net_r(add book) - net_r(v6), the paired "
    "statistic; add_r (tierc7._account_chain) and the cap-absorbed funding "
    "(funding_r_uncapped - funding_r) printed beside; Δ - add_r == absorbed(book) - "
    "absorbed(v6) asserted to 1e-9; never Δ == add_r.",
    f"{LEAN} SA-8 FLAGS [L-A.1]: below_entry = (add_px - entry_px) x d < 0; post_harvest = "
    "the harvest fired and the add's 4h bar >= the harvest bar (after it, or inside its 4h "
    "bar). The twins refuse each class; the scored arm is unchanged. The 'inside its 4h "
    "bar' clause refuses an add whose 1h close precedes the harvest's decision at that "
    "bar's close — look-ahead at reading level inside a Tier-E twin; the count of such "
    "adds is printed (finding F7).",
    f"{LEAN} SA-9 COLLARS [L-1.4]: every stage table but REGISTERED_BOOKS carries tier "
    "'TIER-E', selection_not_a_result 'a SELECTION, not a result', gates 'nothing' and no "
    f"verdict word; registered books are labelled '{BOOK_LABEL}'. Head-to-head: "
    f"'{NEITHER}'.",
    f"{LEAN} SA-10 SCALE-IN-SAMPLE [L-R.2]: calibrated-scale range reads at instants <= the "
    "era cut are structurally in-sample (tuning-era calibration); the holdout slice "
    "(tierE__holdout) and the frozen-3.0 twin (tierE__frozen3) are the statistics printed "
    "beside the verdict.",
    f"{LEAN} SA-11 HEAD-TO-HEAD [registrations' tier_e_arms, scorer SC-3]: "
    "tierE__head_to_head_vs_p_add_sfp (under P-ADD-BRK) / tierE__head_to_head_vs_p_add_brk "
    "(under P-ADD-SFP) = the registration's scored book, row for row (the same book sha), "
    "with ruler 'paired' and sidecar base_arm '<the other registration>/scored'; both are "
    "the v6 key set, so the paired premise holds by construction. Extras opponent_net_r and "
    "delta_vs_opponent_net_r (= net_r - opponent_net_r). The head-to-head is a SELECTION, "
    f"not a result: '{NEITHER}'.",
    f"{LEAN} SA-12 NAMED-EVENT INSTANTS [L-R.5, AM-6; the lanes pass]: every arm carries the "
    "extra columns add1_close_ms / add2_close_ms = the instant of the first / second admitted "
    "add (Add.ms: the event's 1h close, or the parent's close on an L-W.0 mismatch bar), NA "
    "where fewer adds — close events, stamped at their close; required columns, numbers, "
    "book_sha256 and sidecars unchanged.",
)


def _halt(msg: str) -> None:
    raise SystemExit(f"HALT: {msg}")


def canon_csv(df: pd.DataFrame, cols=REQUIRED) -> bytes:
    """The canonical CSV of BOOK_SHA_LAW."""
    d = df.sort_values(["symbol", "entry_close_ms"], kind="mergesort")
    lines = [",".join(cols)]
    for row in d[list(cols)].itertuples(index=False, name=None):
        out = []
        for v in row:
            if isinstance(v, (float, np.floating)):
                out.append(repr(float(v)))
            elif isinstance(v, (int, np.integer)) and not isinstance(v, bool):
                out.append(str(int(v)))
            else:
                out.append(str(v))
        lines.append(",".join(out))
    return ("\n".join(lines) + "\n").encode("utf-8")


def book_sha(df: pd.DataFrame) -> str:
    return hashlib.sha256(canon_csv(df)).hexdigest()


def content_sha(df: pd.DataFrame) -> str:
    return TB._content_sha(df)


# ═════════════════════════════════════════════════════════════ THE EVENT TAPE
def check_tapes(stem: str) -> None:
    """The nest's 1h tape and the ride's 1h tape are ONE tape (bar opens and OHLC
    identical) — an event close handed to the ride names the bar the machine saw."""
    t = N.load11(stem, LENS)
    h = RD.h1_tape(stem)
    for nm, a, b in (("open", t.t0, h.open_ms), ("o", t.o, h.o), ("h", t.h, h.h),
                     ("l", t.l, h.l), ("c", t.c, h.c)):
        if len(a) != len(b) or not np.array_equal(np.asarray(a), np.asarray(b)):
            _halt(f"{stem}: the nest's 1h tape and the ride's differ on {nm}")


def event_frame(stem: str, rule: str, scale_kind: str) -> pd.DataFrame:
    """The rule's 1h events of one asset at one scale, from N.range_facts [SA-1]."""
    rf = N.range_facts(stem, LENS, scale_kind)
    close = rf["close_ms"]
    if rule == "P-ADD-BRK":
        i, ka, dr, rid = rf["die_i"], rf["die_known_at"], rf["die_dir"], rf["die_rid"]
        bnd, bpost, atr = rf["die_boundary"], np.full(len(i), np.nan), rf["die_atr"]
        sis = rf["die_scale_in_sample"]
    elif rule == "P-ADD-SFP":
        i, ka, dr, rid = rf["harden_i"], rf["harden_known_at"], rf["harden_dir"], rf["harden_rid"]
        bnd, bpost, atr = rf["harden_pre"], rf["harden_post"], rf["harden_atr"]
        sis = rf["harden_scale_in_sample"]
    else:
        _halt(f"unknown rule {rule!r}")
    i = np.asarray(i, np.int64)
    if not np.array_equal(i, np.asarray(ka, np.int64)):
        _halt(f"{stem} {rule} {scale_kind}: an event is not known at its own bar")
    if len(i) and int(i.min()) < 1:
        _halt(f"{stem} {rule} {scale_kind}: an event on bar 0 has no prior close")
    inr, rr = rf["in_range"], rf["rid"]
    alive_before = inr[i - 1] & (rr[i - 1] == rid)
    if not bool(np.all(alive_before)):
        _halt(f"{stem} {rule} {scale_kind}: {int((~alive_before).sum())} event(s) without a "
              f"CONFIRMED range of their rid alive at the prior 1h close")
    alive_at = inr[i] & (rr[i] == rid)
    if rule == "P-ADD-BRK" and bool(np.any(alive_at)):
        _halt(f"{stem} {rule} {scale_kind}: a death leaves its range alive")
    if rule == "P-ADD-SFP" and not bool(np.all(alive_at)):
        _halt(f"{stem} {rule} {scale_kind}: a harden kills its range")
    if not set(np.unique(dr).tolist()) <= {1, -1}:
        _halt(f"{stem} {rule} {scale_kind}: a direction outside {{+1, -1}}")
    kc = np.asarray(close, np.int64)[i]
    if len(kc) != len(np.unique(kc)):
        _halt(f"{stem} {rule} {scale_kind}: two events at one 1h close")
    sc = rf["stability_changed"]
    f = pd.DataFrame({
        "asset": stem, "rule": rule, "event_kind": EVENT_OF[rule], "scale_kind": scale_kind,
        "scale_mult": float(rf["scale_mult"]), "event_i": i, "event_rid": np.asarray(rid, np.int64),
        "dir": np.asarray(dr, np.int64).astype(np.int8), "known_close_ms": kc,
        "boundary": np.asarray(bnd, float), "boundary_post": np.asarray(bpost, float),
        "atr_known": np.asarray(atr, float), "scale_in_sample": np.asarray(sis, bool),
        "pick_window": str(rf["pick_window"]),
        "stability_changed": ("NA" if int(sc) < 0 else str(bool(int(sc)))),
        "era": E.era_of(kc) if len(kc) else np.array([], dtype=object)})
    return f


# ═══════════════════════════════════════════════════════════════ THE CONTEXT
def context() -> dict:
    """The corridor, the v6 book of record, the walked base, the event tapes."""
    lo, hi, meta = B.corridor()
    v6 = B.v6_book(lo, hi)
    if len(v6) != len({(t.symbol, int(t.entry_ms)) for t in v6}):
        _halt("the v6 book repeats a key")
    for s in E.CLASSIC5:
        check_tapes(s)
    walked = RD.transform_book(v6, CARD, ROLES, lo, hi, walk=True)
    ok, worst, why = TP.ctrl_diff(TP.journal_frame(walked), TP.journal_frame(v6))
    idf, ist = RD.identity_findings(v6, walked)
    if not ok or worst != 0.0 or idf or ist["acted"] != 0:
        _halt(f"the walked base is not v6 [SA-4]: {why}; identity {idf[:3]} {ist}")
    events = {}
    for rule in REGS:
        for sk in (SCALE_RECORD, SCALE_TWIN):
            events[(rule, sk)] = {s: event_frame(s, rule, sk) for s in E.CLASSIC5}
    fees = E.fees()
    for s in E.CLASSIC5:
        if fees[s]["taker_bps_side"] != TAKER_BPS_SIDE:
            _halt(f"{s}: the taker toll is not {TAKER_BPS_SIDE} bps per side [L-1.1]")
    return {"lo": lo, "hi": hi, "meta": meta, "v6": v6, "walked": walked,
            "wmap": {(t.symbol, int(t.entry_ms)): t for t in walked},
            "vmap": {(t.symbol, int(t.entry_ms)): t for t in v6},
            "events": events, "fees": fees,
            "picks": {s: N.scale_label(s, LENS, SCALE_RECORD) for s in E.CLASSIC5}}


def candidates(ctx: dict, rule: str, scale_kind: str, key) -> list:
    """SA-2: the same-direction events in (entry close, exit 4h bar close]."""
    t = ctx["wmap"][key]
    s, d = key[0], int(t.direction)
    lo_ms = int(t.entry_close_ms)
    hi_ms = int(T9.frame(s)["f"].open_ms[int(t.exit_i)]) + MS_4H
    e = ctx["events"][(rule, scale_kind)][s]
    kc = e["known_close_ms"].to_numpy(np.int64)
    sel = (e["dir"].to_numpy(np.int64) == d) & (kc > lo_ms) & (kc <= hi_ms)
    return [(int(ms), None) for ms in kc[sel]]


def ride_arm(ctx: dict, rule: str, arm: str, *, max_adds: int = RD.ADDS_MAX,
             event_shift_ms: int = 0) -> list:
    """One add book: the v6 set, transformed [L-1.5].  `event_shift_ms` and
    `max_adds` are FIXTURE SEAMS (the look-ahead and 3rd-add sabotages); the
    defaults are the readings."""
    sk = SCALE_OF_ARM[arm]

    def adds_of(key):
        return [(ms + int(event_shift_ms), px) for ms, px in candidates(ctx, rule, sk, key)]

    book = RD.transform_book(ctx["v6"], CARD, ROLES, ctx["lo"], ctx["hi"], walk=True,
                             adds_of=adds_of, add_opts=OPTS_OF_ARM[arm], max_adds=max_adds)
    idf, ist = RD.identity_findings(ctx["v6"], book)
    if idf:
        _halt(f"{rule} {arm}: the IDENTITY LAW fails [L-1.5]: {idf[:3]}")
    kb = [(t.symbol, int(t.entry_ms)) for t in ctx["v6"]]
    if [(t.symbol, int(t.entry_ms)) for t in book] != kb or ist["n"] != len(kb):
        _halt(f"{rule} {arm}: the paired premise fails (the key set moved)")
    return book


# ═══════════════════════════════════════════════════════════════ THE FRAMES
def add_instants_of(t) -> tuple:
    """SA-12 [L-R.5] (a FIXTURE SEAM): the named-event instants of a campaign's admitted
    adds, in admission (time) order — (add1, add2), None where absent.  Add.ms is the add's
    own instant (the 1h close; the parent's close on a mismatch bar), a close event."""
    ms = [int(a.ms) for a in t.adds]
    if len(ms) > RD.ADDS_MAX or ms != sorted(ms) or len(set(ms)) != len(ms):
        _halt(f"{t.symbol} {iso(int(t.entry_ms))}: the admitted adds are not <= "
              f"{RD.ADDS_MAX} strictly time-ordered instants: {ms}")
    ms += [None] * (RD.ADDS_MAX - len(ms))
    return tuple(ms[:2])


def _absorbed(t) -> float:
    return float(t.funding_r_uncapped) - float(t.funding_r)


def book_frame(ctx: dict, book: list, rule: str, arm: str, scale_kind: str | None) -> pd.DataFrame:
    rows = []
    for t in book:
        k = (t.symbol, int(t.entry_ms))
        v = ctx["vmap"][k]
        slip = float(ctx["fees"][t.symbol]["slippage_bps_side"])
        tier = str(ctx["fees"][t.symbol]["slippage_tier"])
        adds = list(t.adds)
        disp = [r for r in getattr(t, "add_dispositions", []) if r["disposition"] == "admitted"]
        ev = (ctx["events"][(rule, scale_kind)][t.symbol].set_index("known_close_ms")
              if scale_kind is not None else None)
        n_sis = sum(1 for r in disp if bool(ev.loc[int(r["event_ms"]), "scale_in_sample"])) \
            if ev is not None else 0
        latch = t.latch_1h_ms
        lab = ctx["picks"][t.symbol]
        net = float(t.net_r)
        a1, a2 = add_instants_of(t)
        rows.append({
            "symbol": t.symbol, "entry_ms": int(t.entry_ms),
            "entry_close_ms": int(t.entry_close_ms), "direction": int(t.direction),
            "entry_px": float(t.entry_px), "stop_px": float(t.stop_px),
            "r_dist": float(t.r_dist), "exit_close_ms": int(t.exit_ms) + MS_4H,
            "exit_reason": str(t.exit_reason), "net_r": net, "gross_r": float(t.gross_r),
            "fee_r": float(t.fee_r), "funding_r": float(t.funding_r),
            "haircut_net_r": net - float(t.fee_r) * (slip / TAKER_BPS_SIDE),
            "era": str(E.era_of(int(t.entry_close_ms))), "lane": str(t.lane),
            # ── extras ──────────────────────────────────────────────────────
            "exit_ms": int(t.exit_ms), "exit_px": float(t.exit_px),
            "exit_close_1h_ms": int(t.exit_close_ms),
            "exit_resolved_by": str(t.exit_resolved_by),
            "latch_1h_ms": int(latch) if latch is not None else -1,
            "latched_1h": latch is not None, "harvested": bool(t.harvested),
            "n_adds": len(adds), "add_r": float(t.add_r) if t.add_r is not None else 0.0,
            "add1_close_ms": a1, "add2_close_ms": a2,                   # SA-12 [L-R.5]
            "v6_net_r": float(v.net_r), "delta_net_r": net - float(v.net_r),
            "funding_r_uncapped": float(t.funding_r_uncapped),
            "funding_absorbed_r": _absorbed(t), "v6_funding_absorbed_r": _absorbed(v),
            "funding_ceiling_bound": bool(t.funding_ceiling_bound),
            "n_adds_below_entry": int(t.n_adds_below_entry),
            "n_adds_post_harvest": int(t.n_adds_post_harvest),
            "n_adds_moved": sum(1 for r in disp if r["moved_to_parent_close"]),
            "n_adds_scale_in_sample": int(n_sis),
            "n_walk_mismatch": int(t.n_walk_mismatch), "acted_by": str(t.acted_by),
            "slip_bps_side": slip, "slip_tier": tier,
            "scale_kind": scale_kind if scale_kind is not None else "none (v6)",
            "pick_window_1h": str(lab["pick_window"]),
            "stability_changed_1h": ("NA" if lab["stability_changed"] is None
                                     else str(bool(lab["stability_changed"])))})
    f = pd.DataFrame(rows)
    f["direction"] = f["direction"].astype(np.int8)
    for c in ("entry_ms", "entry_close_ms", "exit_close_ms", "exit_ms", "exit_close_1h_ms",
              "latch_1h_ms"):
        f[c] = f[c].astype(np.int64)
    for c in ("add1_close_ms", "add2_close_ms"):
        f[c] = pd.array([None if pd.isna(v) else int(v) for v in f[c]], dtype="Int64")
    return f.sort_values(["symbol", "entry_ms"], kind="mergesort").reset_index(drop=True)


def adds_rows(ctx: dict, book: list, rule: str, arm: str) -> list[dict]:
    sk = SCALE_OF_ARM[arm]
    ev = ctx["events"][(rule, sk)]
    out = []
    for t in book:
        disp = [r for r in t.add_dispositions if r["disposition"] == "admitted"]
        if len(disp) != len(t.adds):
            _halt(f"{t.symbol} {iso(int(t.entry_ms))}: admitted dispositions != adds")
        e = ev[t.symbol].set_index("known_close_ms")
        om = T9.frame(t.symbol)["f"].open_ms
        for q, (r, a) in enumerate(zip(disp, t.adds), start=1):
            if int(r["ms"]) != int(a.ms) or float(r["px"]) != float(a.px):
                _halt(f"{t.symbol} {iso(int(t.entry_ms))}: add {q} disposition != Add")
            er = e.loc[int(r["event_ms"])]
            out.append({
                "registration": rule, "arm": arm, "symbol": t.symbol,
                "entry_ms": int(t.entry_ms), "seq": q, "direction": int(t.direction),
                "event_kind": EVENT_OF[rule], "scale_kind": sk,
                "event_ms": int(r["event_ms"]), "event_i": int(er["event_i"]),
                "event_rid": int(er["event_rid"]), "event_boundary": float(er["boundary"]),
                "event_atr": float(er["atr_known"]),
                "scale_in_sample": bool(er["scale_in_sample"]),
                "pick_window": str(er["pick_window"]),
                "stability_changed": str(er["stability_changed"]),
                "add_ms": int(a.ms), "add_px": float(a.px), "add_size": float(a.size),
                "add_4h_i": int(a.i), "add_4h_open_ms": int(om[int(a.i)]),
                "moved_to_parent_close": bool(r["moved_to_parent_close"]),
                "below_entry": bool(r["below_entry"]), "post_harvest": bool(r["post_harvest"]),
                "entry_close_ms": int(t.entry_close_ms), "entry_px": float(t.entry_px),
                "latch_1h_ms": int(t.latch_1h_ms), "exit_close_1h_ms": int(t.exit_close_ms),
                "exit_px": float(t.exit_px), "era": str(E.era_of(int(t.entry_close_ms)))})
    return out


def disposition_rows(ctx: dict, book: list, rule: str, arm: str) -> list[dict]:
    ev = ctx["events"][(rule, SCALE_OF_ARM[arm])]
    out = []
    for t in book:
        e = ev[t.symbol].set_index("known_close_ms")
        for r in t.add_dispositions:
            er = e.loc[int(r["event_ms"])]
            out.append({"registration": rule, "arm": arm, "symbol": t.symbol,
                        "entry_ms": int(t.entry_ms), "direction": int(t.direction),
                        "event_ms": int(r["event_ms"]), "event_i": int(er["event_i"]),
                        "event_rid": int(er["event_rid"]), "add_ms": int(r["ms"]),
                        "add_px": float(r["px"]), "add_4h_i": int(r["i"]),
                        "moved_to_parent_close": bool(r["moved_to_parent_close"]),
                        "below_entry": bool(r["below_entry"]),
                        "post_harvest": bool(r["post_harvest"]),
                        "scale_in_sample": bool(er["scale_in_sample"]),
                        "disposition": str(r["disposition"])})
    return out


def acted_rows(bf: pd.DataFrame, rule: str, arm: str) -> list[dict]:
    out = []
    for r in bf[bf["n_adds"] > 0].itertuples(index=False):
        delta = float(r.net_r) - float(r.v6_net_r)
        resid = delta - float(r.add_r) - (float(r.funding_absorbed_r)
                                          - float(r.v6_funding_absorbed_r))
        if abs(resid) > RESIDUAL_TOL:
            _halt(f"{rule} {arm} {r.symbol} {iso(int(r.entry_ms))}: Δ - add_r - (absorbed - "
                  f"v6 absorbed) = {resid!r} [AM-3]")
        out.append({"registration": rule, "arm": arm, "symbol": r.symbol,
                    "entry_ms": int(r.entry_ms), "direction": int(r.direction),
                    "era": r.era, "n_adds": int(r.n_adds), "net_r": float(r.net_r),
                    "v6_net_r": float(r.v6_net_r), "delta_net_r": delta,
                    "add_r": float(r.add_r), "funding_r_uncapped": float(r.funding_r_uncapped),
                    "funding_r": float(r.funding_r),
                    "funding_absorbed_r": float(r.funding_absorbed_r),
                    "v6_funding_absorbed_r": float(r.v6_funding_absorbed_r),
                    "delta_minus_add_r": delta - float(r.add_r),
                    "am3_residual": resid, "harvested": bool(r.harvested),
                    "n_adds_below_entry": int(r.n_adds_below_entry),
                    "n_adds_post_harvest": int(r.n_adds_post_harvest),
                    "n_adds_moved": int(r.n_adds_moved),
                    "haircut_net_r": float(r.haircut_net_r)})
    return out


def _collar(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    for k, v in COLLAR.items():
        d[k] = v
    return d


def _stats(bf: pd.DataFrame) -> dict:
    n = len(bf)
    s = float(bf["net_r"].sum()) if n else 0.0
    return {"n": n, "sum_net_r": s, "mean_net_r": (s / n) if n else float("nan"),
            "sum_haircut_net_r": float(bf["haircut_net_r"].sum()) if n else 0.0}


def _keys(bf: pd.DataFrame) -> list:
    return [(str(s), int(m)) for s, m in zip(bf["symbol"], bf["entry_ms"])]


def h2h_frame(sc: pd.DataFrame, opp: pd.DataFrame, rule: str) -> pd.DataFrame:
    """SA-11: the head-to-head arm = the rule's scored book, row for row, with the
    OTHER registration's scored net_r beside it (the paired premise asserted)."""
    if _keys(sc) != _keys(opp) or len(set(_keys(sc))) != len(sc):
        _halt(f"{rule} head-to-head: the key sets of {rule}/scored and {H2H_BASE[rule]} "
              f"differ — the paired premise fails [SA-11]")
    f = sc.copy()
    f["h2h_opponent"] = H2H_BASE[rule]
    f["opponent_net_r"] = opp["net_r"].to_numpy(np.float64)
    f["delta_vs_opponent_net_r"] = (f["net_r"].to_numpy(np.float64)
                                    - f["opponent_net_r"].to_numpy(np.float64))
    return f


def paired_delta(bf: pd.DataFrame, other: pd.DataFrame) -> np.ndarray:
    """net_r(bf) - net_r(other) on bf's keys (other restricted to them), key-sorted."""
    m = bf[["symbol", "entry_ms", "net_r"]].merge(
        other[["symbol", "entry_ms", "net_r"]], on=["symbol", "entry_ms"], how="left",
        suffixes=("", "__o"), validate="one_to_one")
    if m["net_r__o"].isna().any():
        _halt("a paired delta against a book that lacks some of the arm's keys")
    m = m.sort_values(["symbol", "entry_ms"], kind="mergesort")
    return m["net_r"].to_numpy(np.float64) - m["net_r__o"].to_numpy(np.float64)


# ══════════════════════════════════════════════════════════════════ COMPUTE
V6_CAMPAIGNS = E.OUT / "books" / "v6_campaigns.parquet"
V6_CMP = (("entry_close_ms", "entry_close_ms"), ("direction", "direction"),
          ("entry_px", "entry_px"), ("stop_px", "stop_px"), ("r_dist", "r_dist"),
          ("exit_close_ms", "exit_close_ms"), ("exit_reason", "exit_reason"),
          ("net_r", "net_r"), ("gross_r", "gross_r"), ("fee_r", "fee_r"),
          ("funding_r", "funding_r"), ("era", "era_of_entry"), ("lane", "lane"))


def base_ident_findings(base_bf: pd.DataFrame) -> list[str]:
    """SA-4: the base arm == the v6 book of record (books/v6_campaigns.parquet) on
    its 13 regbook columns, floats at that file's 6 dp, keyed (symbol, entry_ms)."""
    v = pd.read_parquet(str(V6_CAMPAIGNS))
    m = base_bf.merge(v, on=["symbol", "entry_ms"], how="outer", suffixes=("", "__v6"),
                      indicator=True)
    out = []
    if not (m["_merge"] == "both").all() or len(m) != len(base_bf):
        out.append(f"BASE-IDENT: key sets differ ({int((m['_merge'] != 'both').sum())} rows)")
        return out
    for a, b in V6_CMP:
        x, y = m[a], m[b if b != a else f"{b}__v6"]
        if pd.api.types.is_float_dtype(x):
            bad = ~np.isclose(x.round(6).to_numpy(float), y.to_numpy(float), rtol=0, atol=0)
        else:
            bad = x.astype(str).to_numpy() != y.astype(str).to_numpy()
        if bad.any():
            out.append(f"BASE-IDENT: {int(bad.sum())} row(s) differ on {a}")
    return out


def compute() -> dict:
    ctx = context()
    base_bf = book_frame(ctx, ctx["walked"], "v6", "base", None)
    bi = base_ident_findings(base_bf)
    if bi:
        _halt(f"the base arm is not the v6 book of record [SA-4]: {bi}")
    books, frames, adds, disp, acted = {}, {}, [], [], []
    for rule in REGS:
        for arm in RIDDEN:
            bk = ride_arm(ctx, rule, arm)
            books[(rule, arm)] = bk
            bf = book_frame(ctx, bk, rule, arm, SCALE_OF_ARM[arm])
            frames[(rule, arm)] = bf
            adds += adds_rows(ctx, bk, rule, arm)
            disp += disposition_rows(ctx, bk, rule, arm)
            acted += acted_rows(bf, rule, arm)
        sc = frames[(rule, "scored")]
        for arm, era in SLICES.items():
            frames[(rule, arm)] = sc[sc["era"] == era].reset_index(drop=True)
            acted += [dict(r, arm=arm) for r in acted_rows(frames[(rule, arm)], rule, arm)]
        frames[(rule, "base")] = base_bf
    for rule in REGS:                                     # SA-11 the head-to-head arms
        frames[(rule, H2H_ARM[rule])] = h2h_frame(frames[(rule, "scored")],
                                                  frames[(OPPONENT[rule], "scored")], rule)
    adds_df = pd.DataFrame(adds)
    for arm, era in SLICES.items():                      # the slices' adds, by era of entry
        sl = adds_df[(adds_df["arm"] == "scored") & (adds_df["era"] == era)].copy()
        sl["arm"] = arm
        adds_df = pd.concat([adds_df, sl], ignore_index=True)
    disp_df = pd.DataFrame(disp)
    acted_df = pd.DataFrame(acted)
    T = {"ADDS": adds_df, "DISPOSITIONS": disp_df, "ACTED": acted_df}
    T["DISPOSITION_COUNTS"] = pd.DataFrame(
        [{"registration": rule, "arm": arm, "disposition": dz,
          "n_events": int(((disp_df["registration"] == rule) & (disp_df["arm"] == arm)
                           & (disp_df["disposition"] == dz)).sum())}
         for rule in REGS for arm in RIDDEN for dz in DISPOSITIONS])
    undeclared = sorted(set(disp_df["disposition"]) - set(DISPOSITIONS))
    if undeclared:
        _halt(f"a disposition outside the declared set: {undeclared}")
    h2h = []
    for arm in RIDDEN + tuple(SLICES):
        for rule in REGS:
            bf = frames[(rule, arm)]
            ad = adds_df[(adds_df["registration"] == rule) & (adds_df["arm"] == arm)]
            nb, act = len(bf), bf[bf["n_adds"] > 0]
            h2h.append({"arm": arm, "registration": rule, "event_kind": EVENT_OF[rule],
                        "n_campaigns": nb, "n_campaigns_acted": len(act),
                        "n_adds": int(len(ad)), "sum_add_r": float(bf["add_r"].sum()),
                        "sum_delta_net_r": float(bf["delta_net_r"].sum()),
                        "mean_delta_net_r": float(bf["delta_net_r"].mean()) if nb else float("nan"),
                        "mean_delta_net_r_acted": (float(act["delta_net_r"].mean()) if len(act)
                                                   else float("nan")),
                        "n_adds_below_entry": int(ad["below_entry"].sum()),
                        "n_adds_post_harvest": int(ad["post_harvest"].sum()),
                        "n_adds_moved": int(ad["moved_to_parent_close"].sum()),
                        "n_adds_scale_in_sample": int(ad["scale_in_sample"].sum()),
                        "note": NEITHER})
    T["HEAD_TO_HEAD"] = pd.DataFrame(h2h)
    ov = []
    for arm in RIDDEN + tuple(SLICES):
        a = set(map(tuple, frames[("P-ADD-BRK", arm)].loc[
            frames[("P-ADD-BRK", arm)]["n_adds"] > 0, ["symbol", "entry_ms"]].values.tolist()))
        b = set(map(tuple, frames[("P-ADD-SFP", arm)].loc[
            frames[("P-ADD-SFP", arm)]["n_adds"] > 0, ["symbol", "entry_ms"]].values.tolist()))
        ov.append({"arm": arm, "n_campaigns": len(frames[("P-ADD-BRK", arm)]),
                   "acted_brk": len(a), "acted_sfp": len(b), "acted_both": len(a & b),
                   "acted_either": len(a | b), "acted_brk_only": len(a - b),
                   "acted_sfp_only": len(b - a), "note": NEITHER})
    T["OVERLAP"] = pd.DataFrame(ov)
    te, rb = [], []
    for rule in REGS:
        for arm in ("scored", "base"):
            bf = frames[(rule, arm)]
            st = _stats(bf)
            rb.append({"registration": rule, "arm": arm, **st,
                       "n_acted": int((bf["n_adds"] > 0).sum()), "n_adds": int(bf["n_adds"].sum()),
                       "sum_delta_vs_base": float(bf["delta_net_r"].sum()),
                       "mean_delta_vs_base": float(bf["delta_net_r"].mean()),
                       "era_scope": "full", "ruler": "paired", "book_sha256": book_sha(bf),
                       "label": BOOK_LABEL})
        for arm in TIER_E_ARMS_OF[rule]:
            bf = frames[(rule, arm)]
            st = _stats(bf)
            keys = set(zip(bf["symbol"], bf["entry_ms"]))
            bb = base_bf[[k in keys for k in zip(base_bf["symbol"], base_bf["entry_ms"])]]
            if arm == H2H_ARM[rule]:
                ruled, rbk = H2H_BASE[rule], frames[(OPPONENT[rule], "scored")]
            else:
                ruled, rbk = "base", base_bf
            rr = rbk[[k in keys for k in zip(rbk["symbol"], rbk["entry_ms"])]]
            dv = paired_delta(bf, rbk)
            te.append({"registration": rule, "arm": arm,
                       "era_scope": SLICES.get(arm, "full"), **st,
                       "ruled_against": ruled,
                       "ruled_base_sum_net_r": float(rr["net_r"].sum()),
                       "sum_delta_vs_ruled_base": float(dv.sum()),
                       "mean_delta_vs_ruled_base": (float(dv.mean()) if len(dv)
                                                    else float("nan")),
                       "base_sum_net_r": float(bb["net_r"].sum()),
                       "n_acted": int((bf["n_adds"] > 0).sum()), "n_adds": int(bf["n_adds"].sum()),
                       "sum_add_r": float(bf["add_r"].sum()),
                       "sum_delta_net_r": float(bf["delta_net_r"].sum()),
                       "mean_delta_net_r": float(bf["delta_net_r"].mean()) if len(bf) else float("nan"),
                       "n_adds_below_entry": int(bf["n_adds_below_entry"].sum()),
                       "n_adds_post_harvest": int(bf["n_adds_post_harvest"].sum()),
                       "n_adds_moved": int(bf["n_adds_moved"].sum()),
                       "book_sha256": book_sha(bf)})
    T["REGISTERED_BOOKS"] = pd.DataFrame(rb)
    T["TIER_E_ARMS"] = pd.DataFrame(te)
    ev = pd.concat([ctx["events"][(rule, sk)][s] for rule in REGS for sk in (SCALE_RECORD, SCALE_TWIN)
                    for s in E.CLASSIC5], ignore_index=True)
    T["EVENTS_1H"] = ev.drop(columns=["rule"])
    picks = json.loads((N.PICKS_PATH).read_text(encoding="utf-8"))
    ps = []
    for c in picks["cells"]:
        if c["lens"] == LENS and c["asset"] in E.CLASSIC5:
            ps.append({"asset": c["asset"], "pick_of_record": float(c["pick_of_record"]),
                       "pick_window": c["pick_window"], "tuning_pick": c["tuning_pick"],
                       "whole_tape_pick": float(c["whole_tape_pick"]),
                       "first_half_pick": float(c["first_half_pick"]),
                       "frozen_scale": float(c["frozen_scale"]),
                       "stable_first_half_vs_tuning": bool(c["stable_first_half_vs_tuning"]),
                       "stability_changed": not bool(c["stable_first_half_vs_tuning"]),
                       "in_sample_tuning": bool(c["in_sample_tuning"]),
                       "in_sample_holdout": bool(c["in_sample_holdout"]),
                       "label": c["label"],
                       "scale_of_record_used": float(N.scale_of(c["asset"], LENS, SCALE_RECORD))})
    if sorted(p["asset"] for p in ps) != sorted(E.CLASSIC5):
        _halt("pick stability: not one 1h pick per CLASSIC5 asset")
    for p in ps:
        if p["scale_of_record_used"] != p["pick_of_record"]:
            _halt(f"{p['asset']}: the scale used is not the filed 1h pick")
    T["PICK_STABILITY_1H"] = pd.DataFrame(ps)
    mb = []
    for rule in REGS:
        for arm in ("base",) + RIDDEN:
            bk = ctx["walked"] if arm == "base" else books[(rule, arm)]
            bars = sorted({int(m) for t in bk for m in t.walk_mismatch_ms})
            ad = adds_df[(adds_df["registration"] == rule) & (adds_df["arm"] == arm)]
            dd = disp_df[(disp_df["registration"] == rule) & (disp_df["arm"] == arm)]
            mb.append({"registration": rule, "arm": arm,
                       "n_mismatch_bars_ridden": int(sum(int(t.n_walk_mismatch) for t in bk)),
                       "n_campaigns_on_mismatch": int(sum(1 for t in bk if t.n_walk_mismatch)),
                       "mismatch_bars": " ".join(iso(b) for b in bars) or "none",
                       "n_events_moved": int(dd["moved_to_parent_close"].sum()) if len(dd) else 0,
                       "n_adds_moved": int(ad["moved_to_parent_close"].sum()) if len(ad) else 0})
    T["MISMATCH_BOOKS"] = pd.DataFrame(mb)
    mbar = []
    for s in E.CLASSIC5:
        W = RD.walk_of(s)
        for j, why in sorted(W.why.items()):
            mbar.append({"asset": s, "bar_open_ms": int(W.open4[j]), "bar_open": iso(int(W.open4[j])),
                         "reason": str(why)})
    T["MISMATCH_BARS"] = pd.DataFrame(mbar)
    return {"ctx": ctx, "frames": frames, "books": books, "T": T, "base_bf": base_bf}


# ═══════════════════════════════════════════════════════════════════ WRITE
def _inside(p: Path, root: Path) -> bool:
    return p == root or root in p.parents


def _guard_out(out: Path | None) -> tuple[Path, Path]:
    """(stage dir, regbooks dir): the record, or an F-DET twin under DET_ROOT / a
    `_det_stage_a/` scratch outside the repo tree."""
    if out is None:
        return OUT, REGBOOKS
    o = Path(out).resolve()
    trees = {ROOT.resolve(), Path(E.MAIN_TREE).resolve()}
    if o.parent == DET_ROOT.resolve() or (o.parent.name == DET_ROOT.name
                                          and not any(_inside(o, t) for t in trees)):
        return o / "stage_a", o / "regbooks"
    _halt(f"output dir {o} is neither the record nor an F-DET run dir under {DET_ROOT} or a "
          f"{DET_ROOT.name}/ scratch outside the repo")
    return o, o  # unreachable


def _write_parquet(df: pd.DataFrame, p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    df.to_parquet(str(tmp), index=False)                 # AM-2: pandas on a path string
    os.replace(str(tmp), str(p))


def _write_text(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


def _json(obj) -> str:
    return json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False, default=str) + "\n"


def stamp(df: pd.DataFrame, meta: dict, lens: str = "4h") -> pd.DataFrame:
    return TP.stamp_n(df, meta, lens)


ARM_TEXT = {
    "scored": "the registration's scored arm: v6 campaigns plus <= 2 adds of 0.5 unit at the "
              "1h close of the rule's event (calibrated 1h scale), IN-TRADE and after the +1R "
              "latch, booked by tierc7._account_chain [L-A.1]",
    "base": "the v6 book (walked v6 ride, hooks off; identical to v6 at 0.000e+00), the "
            "paired comparison book [L-1.5, SA-4]",
    "tierE__frozen3": "Tier-E twin: the same rule on the FROZEN 3.0 1h scale (fully causal) "
                      "[L-R.2]",
    "tierE__refuse_below_entry": "Tier-E twin: adds priced below the entry ((px - entry) x d "
                                 "< 0) refused (judged before the 2-add cap, AM-6 s4) [L-A.1]",
    "tierE__refuse_post_harvest": "Tier-E twin: adds after the harvest fired or inside its 4h "
                                  "bar refused (judged before the 2-add cap, AM-6 s4) [L-A.1]",
    "tierE__tuning": "Tier-E slice: the scored book's campaigns with era(entry close) == "
                     "tuning; paired vs the base restricted to the same keys [L-1.3]",
    "tierE__holdout": "Tier-E slice: the scored book's campaigns with era(entry close) == "
                      "holdout (the only slice with a causal calibrated scale); paired vs the "
                      "base restricted to the same keys [L-1.3, L-R.2]",
    **{H2H_ARM[r]: (f"Tier-E head-to-head vs {OPPONENT[r]}: this registration's scored book, "
                    f"row for row, ruled (paired, on (symbol, entry_ms)) against base_arm "
                    f"{H2H_BASE[r]} — the other rule's add book on the same v6 campaigns; "
                    f"extras opponent_net_r, delta_vs_opponent_net_r; {NEITHER} [SA-11]")
       for r in REGS},
}


def regbook_files(R: dict, rule: str) -> dict:
    """{arm: (frame, sidecar)} for one registration."""
    out = {}
    for arm in ARMS_OF[rule]:
        bf = R["frames"][(rule, arm)]
        kind = "scored" if arm == "scored" else "base" if arm == "base" else "tierE"
        side = {"registration": rule, "arm": arm, "kind": kind, "ruler": "paired",
                "panel": list(E.CLASSIC5), "era_scope": SLICES.get(arm, "full"),
                "n": int(len(bf)), "sum_net_r": float(bf["net_r"].sum()),
                "book_sha256": book_sha(bf),
                "description": f"{rule} · {arm}: {ARM_TEXT[arm]}",
                "source_script": SOURCE, "as_of_last_closed_4h": PIN_ISO,
                "pairing_key": ["symbol", "entry_ms"],
                "paired_with": H2H_BASE[rule] if arm == H2H_ARM[rule] else "base",
                "required_columns": list(REQUIRED), "book_sha_law": BOOK_SHA_LAW,
                "scale_kind": ("none (v6)" if arm == "base"
                               else SCALE_OF_ARM.get(arm, SCALE_RECORD)),
                "seed": SEED}
        if arm == H2H_ARM[rule]:
            side["base_arm"] = H2H_BASE[rule]              # the scorer's SC-3
            side["note"] = NEITHER
        if kind == "tierE":
            side.update(COLLAR)
            side["tier"] = "TIER-E"
        if kind == "scored":
            side["label"] = BOOK_LABEL
            side["scale_in_sample"] = (
                "SCALE-IN-SAMPLE: calibrated-scale range reads at instants <= the era cut are "
                "structurally in-sample (tuning-era calibration); the holdout-slice statistic "
                "(tierE__holdout) and the frozen-3.0 twin (tierE__frozen3) are printed beside "
                "the verdict; pick stability printed [L-R.2]")
        out[arm] = (bf, side)
    return out


def build(out: Path | None = None) -> dict:
    stage_dir, reg_dir = _guard_out(out)
    R = compute()
    meta = R["ctx"]["meta"]
    files = {}
    for name, df in R["T"].items():
        key = TABLE_KEYS[name]
        d = df.copy()
        if name not in UNCOLLARED:
            d = _collar(d)
        d = stamp(d, meta, TABLE_LENS.get(name, "4h"))
        dup = int(d.duplicated(subset=key).sum())
        if dup:
            _halt(f"{name}: key {key} not unique ({dup} duplicates)")
        d = d.sort_values(key, kind="mergesort").reset_index(drop=True)
        _write_parquet(d, stage_dir / f"{name}.parquet")
        files[f"stage_a/{name}.parquet"] = {"rows": len(d), "key": key,
                                            "content_sha256": content_sha(d)}
        R["T"][name] = d
    for rule in REGS:
        arms = regbook_files(R, rule)
        for arm, (bf, side) in arms.items():
            d = stamp(bf, meta, "4h")
            if d.duplicated(subset=["symbol", "entry_ms"]).any():
                _halt(f"{rule} {arm}: the pairing key is not unique")
            _write_parquet(d, reg_dir / rule / f"{arm}.parquet")
            _write_text(reg_dir / rule / f"{arm}.json", _json(side))
            files[f"regbooks/{rule}/{arm}.parquet"] = {
                "rows": len(d), "key": ["symbol", "entry_ms"], "content_sha256": content_sha(d),
                "book_sha256": side["book_sha256"]}
        n_un = int((R["frames"][(rule, "scored")]["n_adds"] == 0).sum())
        status = {"registration": rule, "status": "BUILT",
                  "reason": (f"paired add book built on the v6 campaign set (n "
                             f"{len(R['frames'][(rule, 'scored')])}); the identity law held on "
                             f"every campaign without an add ({n_un} unacted, 0.000e+00) and "
                             f"the key sets are identical"),
                  "arms": list(ARMS_OF[rule]), "as_of_last_closed_4h": PIN_ISO,
                  "source_script": SOURCE}
        _write_text(reg_dir / rule / "STATUS.json", _json(status))
    man = manifest(R, files)
    _write_text(stage_dir / MANIFEST, _json(man))
    _write_text(stage_dir / REPORT, render_md(R, man))
    R["manifest"] = man
    return R


def _sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def manifest(R: dict, files: dict) -> dict:
    inputs = {rel: _sha_file(ROOT / rel) for rel in (
        "research_outputs/tierc11/LEANS.md", "research_outputs/tierc11/LEANS_AMENDMENTS.md",
        "research_outputs/tierc11/registrations/REGISTRATIONS.json",
        "research_outputs/tierc11/ranges/SCALE_PICKS.json",
        "research_outputs/tierc11/data/fee_schedule.json",
        "scripts/tierc11_env.py", "scripts/tierc11_nest.py", "scripts/tierc11_ride.py",
        "scripts/tierc11_books.py", SOURCE)}
    return {"tier": "TIER-C11", "stage": "TC11-A", "seed": SEED, "as_of": PIN_ISO,
            "as_of_close_ms": PIN_MS, "substrate": R["ctx"]["meta"]["substrate"],
            "corridor": {"lo": iso(R["ctx"]["lo"]), "hi_close": iso(R["ctx"]["hi"] + 1),
                         "panel": list(E.CLASSIC5)},
            "registrations": list(REGS),
            "arms": {rule: list(ARMS_OF[rule]) for rule in REGS}, "inputs_sha256": inputs,
            "files": files, "book_sha_law": BOOK_SHA_LAW, "collar": COLLAR,
            "readings": list(READINGS), "v6_book_sha": B.book_sha(R["ctx"]["v6"]),
            "n_v6": len(R["ctx"]["v6"])}


# ═════════════════════════════════════════════════════════════════ THE REPORT
def _fmt(v) -> str:
    if isinstance(v, (bool, np.bool_)):
        return "yes" if v else "no"
    if isinstance(v, (float, np.floating)):
        return "nan" if not np.isfinite(v) else f"{float(v):+.6f}"
    if isinstance(v, (int, np.integer)):
        return str(int(v))
    return str(v).replace("|", "/")


def md_table(df: pd.DataFrame, cols: list[str], ms_cols=()) -> str:
    L = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in df[cols].itertuples(index=False, name=None):
        cells = []
        for c, v in zip(cols, r):
            if c in ms_cols and isinstance(v, (int, np.integer)):
                cells.append(iso(int(v)) if int(v) >= 0 else "—")
            else:
                cells.append(_fmt(v))
        L.append("| " + " | ".join(cells) + " |")
    return "\n".join(L) + "\n"


def findings_lines(R: dict) -> list[str]:
    """The stage's findings, each DERIVED from the books (never typed)."""
    T, fr = R["T"], R["frames"]
    out = []
    mb = T["MISMATCH_BOOKS"]
    on_mm = sorted((t for t in R["ctx"]["walked"] if int(t.n_walk_mismatch) > 0),
                   key=lambda t: (t.symbol, int(t.entry_ms)))
    out.append(f"- F1 [AM-5, L-W.0] mismatch bars ridden by the v6 set: "
               f"{sum(int(t.n_walk_mismatch) for t in on_mm)} bar(s) in {len(on_mm)} "
               f"campaign(s) — "
               + ("; ".join(f"{t.symbol} entered {iso(int(t.entry_ms))} rides "
                            + " ".join(iso(int(m)) for m in sorted(t.walk_mismatch_ms))
                            for t in on_mm) or "none")
               + f"; add events moved to a parent close: "
               f"{int(mb['n_events_moved'].sum())}, adds moved: {int(mb['n_adds_moved'].sum())} "
               f"(every arm). Decided by the parent per L-W.0; the walk-or-defer choice reads "
               f"later prices of the same 4h bar (AM-5 disclosure).")
    for rule in REGS:
        a = T["ACTED"][(T["ACTED"]["registration"] == rule) & (T["ACTED"]["arm"] == "scored")]
        cap = a[a["funding_absorbed_r"] - a["v6_funding_absorbed_r"] > 0]
        out.append(f"- F2 [AM-3] {rule} scored: {len(cap)} acted campaign(s) where the D12 "
                   f"ceiling absorbs tranche funding (Δ != add_r): "
                   + ("; ".join(f"{r.symbol} {iso(int(r.entry_ms))} Δ {r.delta_net_r:+.6f} = "
                                f"add_r {r.add_r:+.6f} + absorbed {r.funding_absorbed_r:.6f} "
                                f"− v6 absorbed {r.v6_funding_absorbed_r:.6f}"
                                for r in cap.itertuples()) or "none")
                   + "; the paired Δ is scored on net_r (AM-3), never on add_r.")
    for rule in REGS:
        sc = book_sha(fr[(rule, "scored")])
        same_arms = [arm for arm in RIDDEN[1:] if book_sha(fr[(rule, arm)]) == sc]
        if same_arms:
            out.append(f"- F3 {rule}: the Tier-E arm(s) {same_arms} are byte-identical to the "
                       f"scored book (the twin's class holds no admitted add on the data).")
    dc = T["DISPOSITION_COUNTS"]
    for rule in REGS:
        n_cap = int(dc[(dc["registration"] == rule) & (dc["arm"] == "scored")
                       & (dc["disposition"] == f"refused: cap {RD.ADDS_MAX} reached")]["n_events"].sum())
        if n_cap == 0:
            out.append(f"- F4 {rule}: the 2-add cap never binds on the scored arm (0 events "
                       f"refused at the cap), so a 3rd-add sabotage on it must be a planted row.")
    ps = T["PICK_STABILITY_1H"]
    ch = sorted(ps.loc[ps["stability_changed"], "asset"])
    out.append(f"- F5 [L-R.2] 1h pick stability: the first-half-of-tuning pick differs from the "
               f"tuning pick for {ch or 'none'}; every add row of those assets carries "
               f"stability_changed = True. Scale-in-sample adds on the scored arms: "
               + ", ".join(f"{r.registration} {int(r.n_adds_scale_in_sample)}/{int(r.n_adds)}"
                           for r in T["HEAD_TO_HEAD"][T["HEAD_TO_HEAD"]["arm"] == "scored"]
                           .itertuples()) + " (all in the tuning era).")
    out.append("- F6 [SA-4] exit_close_ms of every arm is the v6 book of record's (the exit "
               "bar's 4h close), so the base arm is the ONE base book the scorer's "
               "F-BASE-IDENT demands; the 1h-resolved exit instant is exit_close_1h_ms.")
    for rule in REGS:                                   # SA-8's in-bar clause (disclosure)
        bk_s, bk_t = R["books"][(rule, "scored")], R["books"][(rule, "tierE__refuse_post_harvest")]
        om = {s: T9.frame(s)["f"].open_ms for s in E.CLASSIC5}

        def _early(t, i, ms):
            return (bool(t.harvested) and int(i) == int(t.harvest_i)
                    and int(ms) < int(om[t.symbol][int(t.harvest_i)]) + MS_4H)
        n_s = sum(1 for t in bk_s for a in t.adds if _early(t, a.i, a.ms))
        n_t = sum(1 for t in bk_t for r in t.add_dispositions
                  if r["disposition"] == "refused: post-harvest (twin)"
                  and _early(t, r["i"], r["ms"]))
        out.append(f"- F7 [L-A.1, SA-8] {rule}: the post-harvest twin's 'inside its 4h bar' "
                   f"clause reads the harvest before its bar's close for an add at an earlier "
                   f"1h close of that bar — {n_s} such add(s) on the scored arm, {n_t} event(s) "
                   f"refused by that clause on tierE__refuse_post_harvest (look-ahead at reading "
                   f"level, inside a Tier-E twin).")
    te = T["TIER_E_ARMS"]
    for rule in REGS:
        h = te[(te["registration"] == rule) & (te["arm"] == H2H_ARM[rule])].iloc[0]
        out.append(f"- F8 [SA-11] {rule} head-to-head arm {H2H_ARM[rule]}: paired vs "
                   f"{h['ruled_against']} on {int(h['n'])} identical keys, ΣΔ "
                   f"{float(h['sum_delta_vs_ruled_base']):+.6f} (mean "
                   f"{float(h['mean_delta_vs_ruled_base']):+.6f}) — a SELECTION, not a result; "
                   f"{NEITHER}.")
    return out


def render_md(R: dict, man: dict) -> str:
    T = R["T"]
    L = [f"# TIER-C11 · STAGE A · ADDS, DECIDED — P-ADD-BRK and P-ADD-SFP\n",
         f"as_of_last_closed_4h: {PIN_ISO} · substrate {man['substrate']} · seed {SEED} · "
         f"corridor {man['corridor']['lo']} → {man['corridor']['hi_close']} · panel CLASSIC5 "
         f"· v6 n {man['n_v6']} (book sha {man['v6_book_sha'][:16]}…)\n",
         "Registered books are printed as **book, not a verdict** (no CI, no p, no verdict "
         "word: the scorer, scripts/tierc11_score.py, decides). Every other table carries the "
         "collar tier = TIER-E · selection_not_a_result = 'a SELECTION, not a result' · gates "
         "= nothing.\n",
         "## Readings (executor sub-readings of this stage)\n"]
    L += [f"- {x}" for x in READINGS]
    L.append("")
    L.append("## 1 · Registered books (book, not a verdict)\n")
    L.append(md_table(T["REGISTERED_BOOKS"], ["registration", "arm", "n", "n_acted", "n_adds",
                                              "sum_net_r", "mean_net_r", "sum_haircut_net_r",
                                              "sum_delta_vs_base", "mean_delta_vs_base",
                                              "era_scope", "ruler", "label"]))
    L.append("SCALE-IN-SAMPLE [L-R.2]: the calibrated 1h scale is fit on the tuning era, so "
             "every range read at an instant ≤ 2024-06-30T23:59:59Z is structurally in-sample "
             "(outcome-free look-ahead). The holdout slice (tierE__holdout) and the frozen-3.0 "
             "twin (tierE__frozen3) below are the statistics to print beside each verdict.\n")
    L.append("## 2 · Tier-E arms (a SELECTION, not a result)\n")
    L.append(md_table(T["TIER_E_ARMS"], ["registration", "arm", "era_scope", "n", "n_acted",
                                         "n_adds", "sum_net_r", "mean_net_r", "ruled_against",
                                         "ruled_base_sum_net_r", "sum_delta_vs_ruled_base",
                                         "mean_delta_vs_ruled_base", "base_sum_net_r",
                                         "sum_delta_net_r", "mean_delta_net_r", "sum_add_r",
                                         "n_adds_below_entry", "n_adds_post_harvest",
                                         "n_adds_moved", "tier"]))
    L.append("ruled_against = the book each Tier-E arm is paired against (the base restricted "
             "to the arm's keys, or the head-to-head arm's base_arm, the other registration's "
             "scored book); base_sum_net_r / sum_delta_net_r are always vs v6 (the base).\n")
    L.append("## 3 · HEAD-TO-HEAD — P-ADD-BRK vs P-ADD-SFP (neither promoted by the other's "
             "failure)\n")
    L.append(md_table(T["HEAD_TO_HEAD"], ["arm", "registration", "n_campaigns",
                                          "n_campaigns_acted", "n_adds", "sum_add_r",
                                          "sum_delta_net_r", "mean_delta_net_r",
                                          "mean_delta_net_r_acted", "n_adds_below_entry",
                                          "n_adds_post_harvest", "n_adds_moved",
                                          "n_adds_scale_in_sample", "tier"]))
    L.append(f"**{NEITHER}.** mean_delta_net_r is over the arm's campaigns (the paired "
             "statistic's point value); _acted over the campaigns that took an add. The "
             "direct paired head-to-head is the Tier-E arm "
             + " / ".join(f"{H2H_ARM[r]} (under {r}, base_arm {H2H_BASE[r]})" for r in REGS)
             + " in §2 (sum_delta_vs_ruled_base).\n")
    L.append("### Overlap of the acted campaigns\n")
    L.append(md_table(T["OVERLAP"], ["arm", "n_campaigns", "acted_brk", "acted_sfp",
                                     "acted_both", "acted_either", "acted_brk_only",
                                     "acted_sfp_only", "tier"]))
    L.append("## 4 · Event dispositions (every candidate event handed to the add hook; the "
             "grid whole)\n")
    L.append(md_table(T["DISPOSITION_COUNTS"], ["registration", "arm", "disposition", "n_events",
                                                "tier"]))
    L.append("## 5 · Acted campaigns — Δ decomposition [AM-3] (every row)\n")
    L.append("Δ = net_r(add book) − net_r(v6); add_r and the cap-absorbed funding beside; "
             "am3_residual = Δ − add_r − (absorbed − v6 absorbed), asserted |·| ≤ 1e-9.\n")
    for rule in REGS:
        for arm in RIDDEN:
            a = T["ACTED"][(T["ACTED"]["registration"] == rule) & (T["ACTED"]["arm"] == arm)]
            L.append(f"### {rule} · {arm} ({len(a)} campaigns)\n")
            L.append(md_table(a, ["symbol", "entry_ms", "direction", "era", "n_adds", "v6_net_r",
                                  "net_r", "delta_net_r", "add_r", "funding_absorbed_r",
                                  "v6_funding_absorbed_r", "am3_residual", "harvested",
                                  "n_adds_below_entry", "n_adds_post_harvest", "n_adds_moved"],
                              ms_cols=("entry_ms",)))
    L.append("(The era slices' acted rows are the scored rows of that era; ACTED.parquet "
             "carries them under arm tierE__tuning / tierE__holdout.)\n")
    L.append("## 6 · Every admitted add (every row)\n")
    for rule in REGS:
        for arm in RIDDEN:
            a = T["ADDS"][(T["ADDS"]["registration"] == rule) & (T["ADDS"]["arm"] == arm)]
            L.append(f"### {rule} · {arm} ({len(a)} adds)\n")
            L.append(md_table(a, ["symbol", "entry_ms", "seq", "direction", "event_ms",
                                  "event_i", "event_rid", "add_ms", "add_px", "add_4h_open_ms",
                                  "latch_1h_ms", "exit_close_1h_ms", "moved_to_parent_close",
                                  "below_entry", "post_harvest", "scale_in_sample"],
                              ms_cols=("entry_ms", "event_ms", "add_ms", "add_4h_open_ms",
                                       "latch_1h_ms", "exit_close_1h_ms")))
    L.append("(The era slices' adds are the scored adds of campaigns of that era; ADDS.parquet "
             "carries them under arm tierE__tuning / tierE__holdout.)\n")
    L.append("## 7 · 1h pick stability (CLASSIC5) [L-R.2]\n")
    L.append(md_table(T["PICK_STABILITY_1H"], ["asset", "pick_of_record", "pick_window",
                                               "first_half_pick", "whole_tape_pick",
                                               "frozen_scale", "stability_changed",
                                               "in_sample_tuning", "in_sample_holdout", "tier"]))
    L.append("Every add row carries stability_changed of its asset (ADDS.parquet).\n")
    L.append("## 8 · The 1h event tape (counts; EVENTS_1H.parquet holds every event)\n")
    ev = T["EVENTS_1H"]
    cnt = []
    for s in E.CLASSIC5:
        for sk in (SCALE_RECORD, SCALE_TWIN):
            for kind in ("death", "harden"):
                g = ev[(ev["asset"] == s) & (ev["scale_kind"] == sk) & (ev["event_kind"] == kind)]
                cnt.append({"asset": s, "scale_kind": sk, "event_kind": kind, "n": len(g),
                            "n_long": int((g["dir"] == 1).sum()),
                            "n_short": int((g["dir"] == -1).sum()),
                            "n_scale_in_sample": int(g["scale_in_sample"].sum()),
                            **COLLAR})
    L.append(md_table(pd.DataFrame(cnt), ["asset", "scale_kind", "event_kind", "n", "n_long",
                                          "n_short", "n_scale_in_sample", "tier"]))
    L.append("## 9 · Mismatch bars [L-W.0, AM-5]\n")
    L.append(md_table(T["MISMATCH_BOOKS"], ["registration", "arm", "n_mismatch_bars_ridden",
                                            "n_campaigns_on_mismatch", "mismatch_bars",
                                            "n_events_moved", "n_adds_moved", "tier"]))
    L.append("The corridor's mismatch bars (a 4h bar whose four 1h children do not reproduce "
             "its H/L/C; 1h-only events on them are taken at the parent's close):\n")
    L.append(md_table(T["MISMATCH_BARS"], ["asset", "bar_open", "reason", "tier"]))
    L.append("## 10 · Findings (derived in-build; findings-not-fixed for the build doc)\n")
    L += findings_lines(R)
    L.append("")
    L.append("## 11 · Files\n")
    L.append("| file | rows | key | content sha256 | book sha256 |\n|---|---|---|---|---|")
    for k, v in sorted(man["files"].items()):
        L.append(f"| {k} | {v['rows']} | {', '.join(v['key'])} | {v['content_sha256'][:16]}… | "
                 f"{v.get('book_sha256', '—')[:16]}{'…' if 'book_sha256' in v else ''} |")
    L.append("")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    od = next((a.split("=", 1)[1] for a in args if a.startswith("--out-dir=")), None)
    R = build(Path(od) if od else None)
    rb = R["T"]["REGISTERED_BOOKS"]
    for r in rb.itertuples(index=False):
        print(f"{r.registration} {r.arm}: n {r.n} · ΣR {r.sum_net_r:+.6f} · mean "
              f"{r.mean_net_r:+.6f} · adds {r.n_adds} ({BOOK_LABEL})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
