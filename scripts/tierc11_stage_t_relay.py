#!/usr/bin/env python
"""TIER-C11 · STAGE T-relay — P-RELAY-1, the 1h relay inside the armed 4h window
[LEANS L-T.2, L-T.3, L-W.0; AM-5, AM-6, AM-7].

Contract of record: exchange/queue/2026-09-24_TC11_APOLLO.md (sha256 bb38e016…,
STEP Q b9ed953).  Executor HEPHAESTUS; seed 20260924.  Readings of record:
research_outputs/tierc11/LEANS.md (frozen) + LEANS_AMENDMENTS.md (AM-1..AM-7).
Registration of record: research_outputs/tierc11/registrations/REGISTRATIONS.json
seq 5 "P-RELAY-1" (text sha b089017b…).  This runner BUILDS the registered book
and its Tier-E arms and writes them through the REGBOOK INTERFACE; it computes no
CI, no p and no verdict (the scorer, scripts/tierc11_score.py, reads the regbooks).

THE READING BUILT (L-T.2, verbatim in substance)
  WINDOWS   every v6 arming on CLASSIC5 — the card's armings: a 4h 12/89 cross with
            TIDE true and d >= 0.75 at the arm bar (T9.replay9's own armings over
            replay9's own bounds), WHETHER OR NOT v6 entered it.
  ARMED     from the arm close until the EARLIEST of
            (i)   that window's v6 4h 12/26 trigger close (the card's first in-window
                  12/26 cross at or after the arm bar, known by the as-of);
            (ii)  the window-close instant (the counter 4h 12/89 cross's close);
            (iii) a 4h 89/316 cross against the window (its close).
  ENTRY     the FIRST 1h close strictly after the arm close and strictly before that
            earliest bound on which the 1h EMA9 crosses EMA12 in the trade direction
            (engine EMA of the 1h close, `RD.cross_1h`).  A 1h close AT the trigger
            instant is not a relay.  One relay per window; one position per asset
            within the relay book.
  RESOLVE   `RD.relay_entry(trigger_close_ms=…)` (L-W.0: an entry inside a MISMATCH
            4h bar is taken at the parent's close — `moved`; a moved entry landing on
            or after the trigger is `refused`); `RD.relay_stop` (struct_stop_4h,
            pivots and ATR(4h) as of the last CLOSED 4h bar, railed 1.0 ATR; R on
            4h); `RD.relay11(walk_after=True, moved=…)` (J's post-entry 1h children
            for STOP/+1R, then J's close slot BELL/HARVEST/TRAIL, then the v6 ride
            with the state carried, walked on 1h to resolve the exit instant);
            `RD.trade11` books it through tierc7._account_chain (net = gross − taker
            fee − funding).
  MISSES    every window the relay never activates is in the MISS COLUMN with its
            reason and what v6 did in it.  "every window is exactly one of relayed /
            missed" — the dispositions partition the windows.
  RULER     two-sample vs the v6 (12/26-triggered) base, full corridor [L-1.4].

EXECUTOR SUB-READINGS (the frozen text is silent; each printed in the lean block)
  SR-1  window set = replay9's armings with tide_ok and d_ok over replay9's own
        (lo_i = max(lo_i, 316), hi_i); the dispositions v6 gave them are replay9's.
  SR-2  bounds are those KNOWN by the as-of: a trigger / counter 12/89 / 89/316-against
        after the ride's last bar does not exist yet; a window with no bound by the
        pin is still ARMED at the pin, and 1h closes up to and including the pin are
        eligible (an entry at the pin rides to corridor_end at once, as v6 does with a
        trigger on the last bar).  Tie of two bounds on one bar: the reason is named
        in the order trigger → counter 12/89 → 89/316-against.
  SR-3  FIRST CROSS ONLY: the relay is the window's first qualifying 1h cross; if that
        entry cannot be taken (moved onto a bound, position open, no structural stop)
        the window is a MISS with that reason — v6's own law (replay9 takes each
        window's first trigger only and never a later one).  Refusal order is v6's:
        position open, then the stop.
  SR-4  a moved entry (L-W.0) is refused when its RESOLVED instant is not strictly
        before the bound: `relay_entry` refuses the trigger, and this runner applies
        the same law to the counter 12/89 and the 89/316-against bounds.
  SR-5  one position per asset at 1h resolution: a relay is admitted iff its entry
        instant is strictly after the previous relay's 1h-resolved exit instant on
        that asset.  v6's 4h-bar law (entry bar <= previous exit bar refused) is
        printed beside as a disclosure count.
  SR-6  the late-relay twin (the rival reading, Tier-E) = the record rule with bound
        (i) removed: the trigger instant and later are admissible; bounds (ii) and
        (iii) stay.
  SR-7  regbook columns: a relay's entry_ms = the OPEN of the 4h bar J containing the
        entry close (the lens bar), entry_close_ms = the exact entry instant (the 1h
        bar open is `entry_1h_open_ms`); a relay's exit_close_ms = the ride's
        1h-RESOLVED exit instant (walk_after=True); the base v6 book's exit_close_ms =
        the exit bar's close (tierc11_books' campaign-table convention: v6 is a 4h
        ride).  Both carry `exit_bar_close_ms`.
  SR-8  haircut_net_r = net_r − fee_r × slip_bps_side / taker_bps_side (AM-7), with
        the stem's charter tier from E.fees().

FIXTURE SEAMS (named, greppable; the defaults ARE the readings): relay_pair, relay_asof,
bound_of, first_index, moved_refused, position_open, windows_of, _miss_code.

Outputs:  research_outputs/tierc11/stage_t_relay/ (tables, manifest, STAGE_T_RELAY.md)
          research_outputs/tierc11/regbooks/P-RELAY-1/ (scored, base, tierE__* arms +
          sidecars, STATUS.json)

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_forward_ledger.py --refresh --snapshot $NAIAD_CACHE_DIR
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_t_relay.py              # the build
      (the report embeds the forward ledger of record, so the ledger refresh comes first)
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_t_relay.py --out-dir=DIR  # F-DET twin
      (DIR must be a direct child of research_outputs/tierc11/stage_t_relay/_det_stage_t_relay/,
       or of a `_det_stage_t_relay/` directory OUTSIDE the repo tree)
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_books as B                   # noqa: E402  (tierc11_env first: guard + shim + hook)
import tierc11_ride as RD                   # noqa: E402

import numpy as np                          # noqa: E402
import pandas as pd                         # noqa: E402

E = B.E
TP, T9, TB = E.TP, E.T9, E.TB
RC = RD.RC
iso = TB.iso
CARD, ROLES = TP.CONTROL_CARD, T9.V6_ROLES

# ══════════════════════════════════════════════════════════ CONSTANTS OF RECORD
REG_ID = "P-RELAY-1"
RELAY_FAST, RELAY_SLOW = 9, 12              # "ENTRY on the 1h 9/12 with-trend close"; veto "relay" (1h)
MS_1H, MS_4H = 3_600_000, 14_400_000
PIN_MS, PIN_ISO = E.PIN_MS, E.PIN_ISO
SEED = E.SEED
LANE = "relay"
OUT = E.OUT / "stage_t_relay"
REGBOOKS = E.OUT / "regbooks"
DET_ROOT = OUT / "_det_stage_t_relay"
REPORT = "STAGE_T_RELAY.md"
MANIFEST = "build_manifest.json"
COLLAR = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
          "gates": "nothing"}                # L-1.4: every non-registered table
BOOK_NOT_VERDICT = "book, not a verdict"
V6_BOOKS_MANIFEST = E.OUT / "books" / "build_manifest.json"
FWD_DIR = E.OUT / "forward"                 # the forward ledger of record (read for the report)
REGISTRATIONS = E.OUT / "registrations" / "REGISTRATIONS.json"

# the regbook interface (binding)
REQUIRED = ("symbol", "entry_ms", "entry_close_ms", "direction", "entry_px", "stop_px",
            "r_dist", "exit_close_ms", "exit_reason", "net_r", "gross_r", "fee_r",
            "funding_r", "haircut_net_r", "era", "lane")
INT64_COLS = ("entry_ms", "entry_close_ms", "exit_close_ms")
FLOAT_COLS = ("entry_px", "stop_px", "r_dist", "net_r", "gross_r", "fee_r", "funding_r",
              "haircut_net_r")
STR_COLS = ("symbol", "exit_reason", "era", "lane")
SIDECAR_KEYS = ("registration", "arm", "kind", "ruler", "panel", "era_scope", "n",
                "sum_net_r", "book_sha256", "description", "source_script")
BOOK_SHA_RECIPE = ("sha256 of the UTF-8 CSV: header = the 16 required columns in interface "
                   "order joined by ','; one line per row sorted by (symbol, entry_close_ms) "
                   "(stable mergesort); ints as str(int), floats as repr(float), strings as "
                   "is (csv.writer, QUOTE_MINIMAL, lineterminator '\\n')")

# the window dispositions — a PARTITION (every window exactly one)
RELAYED = "RELAYED"
DISPOSITIONS = (
    ("RELAYED", "relayed: the first with-trend 1h 9/12 close inside the armed interval, entered"),
    ("MISS_TRIGGER_FIRST_LAG0", "miss: the v6 4h 12/26 trigger closed first, at the arm bar "
                                "(lag 0 — no 1h close lies strictly between)"),
    ("MISS_TRIGGER_FIRST", "miss: the v6 4h 12/26 trigger closed first (lag >= 1)"),
    ("MISS_CLOSED_COUNTER_12_89", "miss: the window closed unrelayed (counter 4h 12/89)"),
    ("MISS_CLOSED_TIDE_AGAINST", "miss: the window closed unrelayed (4h 89/316 against)"),
    ("MISS_OPEN_AT_ASOF", "miss: still armed at the as-of, unrelayed (censored)"),
    ("MISS_REFUSED_MOVED_ONTO_BOUND", "miss: the first cross sits in an L-W.0 mismatch bar and "
                                      "its parent-close entry is not strictly before the bound"),
    ("MISS_REFUSED_POSITION_OPEN", "miss: the first cross came while a relay was open on the "
                                   "asset (one position per asset)"),
    ("MISS_REFUSED_NO_STOP", "miss: no structural stop (struct_stop_4h None / ATR not finite)"),
)
DISPOSITION_CODES = tuple(c for c, _ in DISPOSITIONS)
BOUND_ORDER = ("trigger", "counter_12_89", "tide_against")     # SR-2 tie order
V6_DISPOSITION = {"entered": "ENTERED", "position_open": "NOT ENTERED: position open",
                  "no_trigger": "NOT ENTERED: no trigger by the window close / as-of",
                  "": "NOT ENTERED: no structural stop / ATR"}
LEAD_4H_BINS = (("0", 0, 0), ("1", 1, 1), ("2", 2, 2), ("3", 3, 3), ("4", 4, 4),
                ("5-9", 5, 9), ("10-19", 10, 19), (">=20", 20, None))
LEAD_1H_BINS = (("1-3", 1, 3), ("4-7", 4, 7), ("8-15", 8, 15), ("16-31", 16, 31),
                ("32-63", 32, 63), (">=64", 64, None))

READINGS = (
    "[LEAN-HEPHAESTUS] L-T.2 windows = every v6 arming on CLASSIC5 (replay9's armings, TIDE "
    "and d >= 0.75 at the arm bar) whether or not v6 entered it; ARMED from the arm close to "
    "min(v6 4h 12/26 trigger close, counter 12/89 close, 89/316-against close); the relay "
    "enters at the FIRST 1h close strictly inside that interval on which EMA9 crosses EMA12 "
    "with the trend; one relay per window, one position per asset; stop struct_stop_4h as of "
    "the last CLOSED 4h bar railed 1.0 ATR (R on 4h); RD.relay_entry / relay_stop / "
    "relay11(walk_after=True).",
    "[LEAN-HEPHAESTUS] L-T.3 every relay's close < its window's v6 4h trigger close (when "
    "the window triggered); misses are windows whose trigger closed first (every lag-0 "
    "window) or that closed unrelayed — each with what v6 did in it.",
    "[LEAN-HEPHAESTUS] L-W.0 / AM-5 a relay entry inside a 4h bar whose four 1h children do "
    "not reproduce the parent is taken at the parent's close (moved) and the bar is counted; "
    "the book prints its mismatch-bar count and names the bars.",
    "[LEAN-HEPHAESTUS] AM-6 (s3) a relay stopped inside its entry bar J books mae/mfe at 1h "
    "resolution (the stop child is the stop unit); L-T.2 arms the harvest on close[J-1].",
    "[LEAN-HEPHAESTUS] AM-7 haircut_net_r = net_r - fee_r x slip_bps_side / taker_bps_side "
    "(charter tier per stem from E.fees()); printed beside net_r, never replacing it.",
    "[LEAN-HEPHAESTUS] SR-1 window set = replay9's armings (tide_ok and d_ok) over replay9's "
    "own bounds; v6's disposition of each is replay9's.",
    "[LEAN-HEPHAESTUS] SR-2 bounds known by the as-of only; a window with no bound by the pin "
    "is armed at the pin (1h closes <= the pin eligible); tie order trigger -> counter 12/89 "
    "-> 89/316-against.",
    "[LEAN-HEPHAESTUS] SR-3 first cross only: a window whose first qualifying cross cannot be "
    "entered is a MISS with the reason (v6's one-trigger-per-window law); refusal order "
    "position open, then the stop (replay9's order).",
    "[LEAN-HEPHAESTUS] SR-4 a moved entry is refused unless its RESOLVED instant is strictly "
    "before every bound (relay_entry refuses the trigger; the runner the other two).",
    "[LEAN-HEPHAESTUS] SR-5 one position per asset at 1h resolution: entry instant strictly "
    "after the previous relay's 1h-resolved exit; v6's 4h-bar law printed as a disclosure.",
    "[LEAN-HEPHAESTUS] SR-6 late-relay twin (Tier-E rival) = the record rule with the trigger "
    "bound removed (the trigger instant and later admissible).",
    "[LEAN-HEPHAESTUS] SR-7 relay entry_ms = open of the 4h bar J holding the entry close; "
    "relay exit_close_ms = the 1h-resolved exit instant; base v6 exit_close_ms = the exit "
    "bar's close (tierc11_books convention); both carry exit_bar_close_ms.",
)


def _halt(msg: str) -> None:
    raise SystemExit(f"HALT: {msg}")


# ════════════════════════════════════════════════════════ FIXTURE SEAMS (named)
def relay_pair() -> tuple[int, int]:
    """The 1h EMA pair of the relay entry (9, 12) [L-T.2; veto "relay"]."""
    return RELAY_FAST, RELAY_SLOW


def relay_asof(re_: dict) -> int:
    """The 4h index the stop and ATR are read at: the last CLOSED 4h bar at the
    entry instant, as `RD.relay_entry` resolves it (J-1 inside J; J at J's close)."""
    return int(re_["asof_i"])


def bound_of(w: dict, late: bool) -> tuple[int | None, tuple]:
    """(the earliest bound instant, the bound kinds binding at it) [L-T.2].
    `late` drops the trigger bound (the Tier-E rival, SR-6)."""
    cand = [("trigger", w["trigger_close_ms"]), ("counter_12_89", w["window_close_ms"]),
            ("tide_against", w["tide_against_close_ms"])]
    if late:
        cand = cand[1:]
    live = [(k, int(v)) for k, v in cand if v is not None]
    if not live:
        return None, ()
    b = min(v for _, v in live)
    return b, tuple(k for k in BOUND_ORDER for kk, v in live if kk == k and v == b)


def moved_refused(t_e: int, bound_ms: int | None) -> bool:
    """SR-4: a RESOLVED entry at or after the bound is not a relay (relay_entry refuses
    the trigger; this refuses the counter 12/89 and the 89/316-against bounds too)."""
    return bound_ms is not None and int(t_e) >= int(bound_ms)


def position_open(t_e: int, open_until: int | None) -> bool:
    """SR-5: one position per asset — an entry at or before the previous relay's
    1h-resolved exit instant is refused."""
    return open_until is not None and int(t_e) <= int(open_until)


def first_index(mask: np.ndarray, close_ms: np.ndarray, after_ms: int, before_ms: int | None,
                edge_ms: int) -> int | None:
    """The FIRST index k with mask[k] and after_ms < close_ms[k] < before_ms (None = no
    bound) and close_ms[k] <= edge_ms (the as-of)."""
    k0 = int(np.searchsorted(close_ms, int(after_ms), "right"))
    hi = int(edge_ms) + 1 if before_ms is None else min(int(before_ms), int(edge_ms) + 1)
    k1 = int(np.searchsorted(close_ms, hi, "left"))
    if k1 <= k0:
        return None
    hit = np.flatnonzero(mask[k0:k1])
    return int(k0 + hit[0]) if hit.size else None


# ═══════════════════════════════════════════════════════════════ THE WINDOWS
_ASSET: dict = {}


def asset_ctx(sym: str, lo: int, hi: int) -> dict:
    """Everything one asset's relay build reads, once: the 4h frame, replay9's own
    armings + v6 trades, the role arrays, the 1h walk and the 1h relay crosses."""
    k = (sym, lo, hi, relay_pair())
    if k in _ASSET:
        return _ASSET[k]
    f = T9.frame(sym)["f"]
    om = np.asarray(f.open_ms, dtype=np.int64)
    lo_i, hi_i, n = B.ride_bounds(sym, ROLES, lo, hi)
    arms, trades = T9.replay9(sym, CARD, ROLES, lo, hi)
    ra = T9.role_arrays(sym, ROLES)
    W = RD.walk_of(sym)
    fast, slow = relay_pair()
    up, dn = RD.cross_1h(W.h1, fast, slow)
    ctx = {"sym": sym, "f": f, "om": om, "lo_i": lo_i, "hi_i": hi_i, "n": n, "arms": arms,
           "trades": trades, "ra": ra, "W": W, "up": up, "dn": dn,
           "h1_close": np.asarray(W.h1.open_ms, dtype=np.int64) + MS_1H,
           "edge_ms": int(om[hi_i]) + MS_4H}
    _ASSET[k] = ctx
    return ctx


def windows_of(ctx: dict) -> list[dict]:
    """Every card arming (tide_ok and d_ok) of the asset, with its bounds as known at
    the as-of and v6's disposition of it [SR-1, SR-2]."""
    sym, f, om, hi_i, ra = ctx["sym"], ctx["f"], ctx["om"], ctx["hi_i"], ctx["ra"]
    v6_by_arm = {(int(t.arm_i), int(t.direction)): t for t in ctx["trades"]}
    out = []
    for a in ctx["arms"]:
        if not (a.tide_ok and a.d_ok):
            continue
        d, ai = int(a.direction), int(a.arm_i)
        ti = None if a.trigger_i is None else int(a.trigger_i)
        if ti is not None and not (ai <= ti <= hi_i):
            _halt(f"{sym} arm {iso(int(om[ai]))}: trigger_i {ti} outside [arm_i, hi_i]")
        we = B.known_window_end(int(a.window_end_i), hi_i)
        against = ra["b_dn"] if d == 1 else ra["b_up"]
        ta = np.flatnonzero(against[ai + 1:hi_i + 1])
        ta_i = int(ai + 1 + ta[0]) if ta.size else None
        t6 = v6_by_arm.get((ai, d))
        rej = str(a.reject)
        if (t6 is not None) != (rej == "entered"):
            _halt(f"{sym} arm {iso(int(om[ai]))}: replay9 says {rej!r} but the v6 trade "
                  f"{'exists' if t6 is not None else 'is absent'}")
        if rej not in V6_DISPOSITION:
            _halt(f"{sym} arm {iso(int(om[ai]))}: unknown replay9 disposition {rej!r}")
        w = {"symbol": sym, "direction": d, "arm_i": ai, "arm_ms": int(om[ai]),
             "arm_close_ms": int(om[ai]) + MS_4H, "disp": float(a.disp),
             "trigger_i": ti,
             "trigger_close_ms": None if ti is None else int(om[ti]) + MS_4H,
             "lag": None if ti is None else ti - ai,
             "window_end_i": we,
             "window_close_ms": int(om[we]) + MS_4H if we <= hi_i else None,
             "tide_against_i": ta_i,
             "tide_against_close_ms": None if ta_i is None else int(om[ta_i]) + MS_4H,
             "v6_disposition": V6_DISPOSITION[rej],
             "v6_entered": t6 is not None,
             "v6_entry_ms": None if t6 is None else int(t6.entry_ms),
             "v6_entry_close_ms": None if t6 is None else int(t6.entry_ms) + MS_4H,
             "v6_net_r": None if t6 is None else float(t6.net_r),
             "v6_exit_reason": None if t6 is None else str(t6.exit_reason)}
        out.append(w)
    return out


# ═══════════════════════════════════════════════════════════════ THE RELAY BOOK
def _miss_code(w: dict, kinds: tuple) -> str:
    if not kinds:
        return "MISS_OPEN_AT_ASOF"
    k = kinds[0]
    if k == "trigger":
        return "MISS_TRIGGER_FIRST_LAG0" if w["lag"] == 0 else "MISS_TRIGGER_FIRST"
    return "MISS_CLOSED_COUNTER_12_89" if k == "counter_12_89" else "MISS_CLOSED_TIDE_AGAINST"


def haircut_of(sym: str, net_r: float, fee_r: float) -> tuple[float, float, str]:
    """AM-7: net_r − fee_r × slip / taker, the stem's charter tier (E.fees())."""
    fz = E.fees()[sym]
    slip, taker = float(fz["slippage_bps_side"]), float(fz["taker_bps_side"])
    return float(net_r) - float(fee_r) * slip / taker, slip, str(fz["slippage_tier"])


def relay_asset(ctx: dict, late: bool = False) -> tuple[list, list[dict]]:
    """One asset's relay book (record, or the late twin) and every window's
    disposition.  Returns (trades, window rows)."""
    sym, om, hi_i, W = ctx["sym"], ctx["om"], ctx["hi_i"], ctx["W"]
    wins = windows_of(ctx)
    rows, cands = [], []
    for w in wins:
        d = w["direction"]
        b, kinds = bound_of(w, late)
        mask = ctx["up"] if d == 1 else ctx["dn"]
        k = first_index(mask, ctx["h1_close"], w["arm_close_ms"], b, ctx["edge_ms"])
        r = dict(w, variant="late" if late else "record", bound_ms=b,
                 bound_kind="+".join(kinds) if kinds else "none",
                 cross_close_ms=None if k is None else int(ctx["h1_close"][k]),
                 disposition=None, entry_close_ms=None, entry_kind=None, moved=None,
                 relay_entry_ms=None, relay_net_r=None, relay_exit_reason=None,
                 lead_1h=None, lead_4h=None, after_trigger=None)
        rows.append(r)
        if k is None:
            r["disposition"] = _miss_code(w, kinds)
            continue
        tcl = None if late else w["trigger_close_ms"]
        re_ = RD.relay_entry(sym, int(ctx["h1_close"][k]), walk=W, trigger_close_ms=tcl)
        r["entry_kind"], r["moved"] = str(re_["kind"]), bool(re_["moved"])
        t_e = int(re_["entry_close_ms"])
        if re_["refused"] is not None or moved_refused(t_e, b):
            r["disposition"] = "MISS_REFUSED_MOVED_ONTO_BOUND"
            r["entry_close_ms"] = t_e
            continue
        cands.append((t_e, int(w["arm_i"]), r, re_))
    cands.sort(key=lambda c: (c[0], c[1]))
    trades, open_until = [], None
    for t_e, _, r, re_ in cands:
        d = r["direction"]
        r["entry_close_ms"] = t_e
        if position_open(t_e, open_until):
            r["disposition"] = "MISS_REFUSED_POSITION_OPEN"
            continue
        stp, atr = RD.relay_stop(sym, relay_asof(re_), float(re_["entry_px"]), d, CARD)
        if stp is None:
            r["disposition"] = "MISS_REFUSED_NO_STOP"
            continue
        J = int(re_["J"])
        leg = RD.relay11(sym, CARD, ROLES, d, t_e, float(re_["entry_px"]), stp.stop_px,
                         stp.r_dist, hi_i, walk=W, walk_after=True, moved=bool(re_["moved"]))
        t = RD.trade11(sym, CARD, ROLES, d, arm_i=r["arm_i"], arm_ms=r["arm_ms"],
                       disp=r["disp"], entry_i=J, entry_ms=int(om[J]),
                       entry_px=float(re_["entry_px"]), stp=stp, atr_sig=atr, leg=leg,
                       lane=LANE, entry_close_ms=t_e)
        x = getattr(t, "exit_close_ms")
        if x is None:
            _halt(f"{sym} relay {iso(t_e)}: no 1h-resolved exit (walk_after must be on)")
        open_until = int(x)
        ext = {"window_arm_ms": r["arm_ms"], "window_arm_close_ms": r["arm_close_ms"],
               "trigger_close_ms": r["trigger_close_ms"], "window_close_ms":
                   r["window_close_ms"], "tide_against_close_ms": r["tide_against_close_ms"],
               "bound_ms": r["bound_ms"], "bound_kind": r["bound_kind"],
               "cross_close_ms": r["cross_close_ms"], "entry_kind": r["entry_kind"],
               "moved": r["moved"], "asof_i": relay_asof(re_), "relay_J": J,
               "v6_entered": r["v6_entered"], "v6_entry_ms": r["v6_entry_ms"],
               "v6_net_r": r["v6_net_r"], "variant": r["variant"]}
        for kk, vv in ext.items():
            object.__setattr__(t, kk, vv)
        trades.append(t)
        r["disposition"] = RELAYED
        r["relay_entry_ms"] = int(om[J])
        r["relay_net_r"] = float(t.net_r)
        r["relay_exit_reason"] = str(t.exit_reason)
        if r["trigger_close_ms"] is not None:
            r["lead_1h"] = (int(r["trigger_close_ms"]) - t_e) // MS_1H
            r["lead_4h"] = int(r["trigger_i"]) - J
            r["after_trigger"] = bool(t_e >= int(r["trigger_close_ms"]))
    for r in rows:
        if r["disposition"] not in DISPOSITION_CODES:
            _halt(f"{sym} arm {iso(r['arm_ms'])}: no disposition ({r['disposition']!r})")
    return trades, rows


def relay_book(lo: int, hi: int, late: bool = False) -> tuple[list, pd.DataFrame]:
    """The CLASSIC5 relay book (record or late twin) and the window table."""
    trades, rows = [], []
    for s in E.CLASSIC5:
        t, r = relay_asset(asset_ctx(s, lo, hi), late=late)
        trades += t
        rows += r
    return trades, pd.DataFrame(rows)


# ═════════════════════════════════════════════════════════════ THE REGBOOKS
def _ms_or_none(x):
    return None if x is None else int(x)


def regbook_frame(trades, kind: str) -> pd.DataFrame:
    """The regbook interface columns (+ extras) from Trade objects.  kind 'relay'
    (1h-resolved exit instant) or 'v6' (the exit bar's close) [SR-7]."""
    rows = []
    for t in trades:
        sym = str(t.symbol)
        hc, slip, tier = haircut_of(sym, float(t.net_r), float(t.fee_r))
        exit_bar_close = int(t.exit_ms) + MS_4H
        if kind == "relay":
            ecl = int(getattr(t, "entry_close_ms"))
            xcl = int(getattr(t, "exit_close_ms"))
        else:
            ecl = int(t.entry_ms) + MS_4H
            xcl = exit_bar_close
        row = {"symbol": sym, "entry_ms": int(t.entry_ms), "entry_close_ms": ecl,
               "direction": int(t.direction), "entry_px": float(t.entry_px),
               "stop_px": float(t.stop_px), "r_dist": float(t.r_dist),
               "exit_close_ms": xcl, "exit_reason": str(t.exit_reason),
               "net_r": float(t.net_r), "gross_r": float(t.gross_r), "fee_r": float(t.fee_r),
               "funding_r": float(t.funding_r), "haircut_net_r": hc,
               "era": str(E.era_of(ecl)), "lane": LANE if kind == "relay" else str(t.lane),
               # ── extras ──────────────────────────────────────────────────────
               "arm_ms": int(t.arm_ms), "entry_i": int(t.entry_i), "exit_i": int(t.exit_i),
               "exit_ms": int(t.exit_ms), "exit_bar_close_ms": exit_bar_close,
               "exit_px": float(t.exit_px), "reached_1r": bool(t.reached_1r),
               "harvested": bool(t.harvested), "mfe_r": float(t.mfe_r),
               "n_advances": int(len(t.advances)), "atr_at_entry": float(t.atr_at_entry),
               "slip_bps_side": slip, "slip_tier": tier,
               "funding_ceiling_bound": bool(t.funding_ceiling_bound)}
        if kind == "relay":
            row.update({
                "entry_1h_open_ms": ecl - MS_1H, "relay_J": int(getattr(t, "relay_J")),
                "entry_kind": str(getattr(t, "entry_kind")),
                "relay_path": str(getattr(t, "relay_path")),
                "moved": bool(getattr(t, "moved")), "asof_i": int(getattr(t, "asof_i")),
                "exit_resolved_by": str(getattr(t, "exit_resolved_by")),
                "exit_stamp_ms": int(getattr(t, "exit_stamp_ms")),
                "latch_1h_ms": _ms_or_none(getattr(t, "latch_1h_ms")),
                "n_walk_mismatch": int(getattr(t, "n_walk_mismatch")),
                "walk_mismatch_ms": ",".join(iso(int(x)) for x in getattr(t, "walk_mismatch_ms")),
                "window_arm_close_ms": int(getattr(t, "window_arm_close_ms")),
                "trigger_close_ms": _ms_or_none(getattr(t, "trigger_close_ms")),
                "window_close_ms": _ms_or_none(getattr(t, "window_close_ms")),
                "tide_against_close_ms": _ms_or_none(getattr(t, "tide_against_close_ms")),
                "bound_ms": _ms_or_none(getattr(t, "bound_ms")),
                "bound_kind": str(getattr(t, "bound_kind")),
                "cross_close_ms": int(getattr(t, "cross_close_ms")),
                "after_trigger": bool(getattr(t, "trigger_close_ms") is not None
                                      and ecl >= int(getattr(t, "trigger_close_ms"))),
                "v6_entered": bool(getattr(t, "v6_entered")),
                "v6_entry_ms": _ms_or_none(getattr(t, "v6_entry_ms")),
                "v6_net_r": (None if getattr(t, "v6_net_r") is None
                             else float(getattr(t, "v6_net_r"))),
                "variant": str(getattr(t, "variant"))})
        rows.append(row)
    df = pd.DataFrame(rows)
    if not len(df):
        df = pd.DataFrame(columns=list(REQUIRED))
    for c in INT64_COLS:
        df[c] = df[c].astype("int64")
    df["direction"] = df["direction"].astype("int8")
    for c in FLOAT_COLS:
        df[c] = df[c].astype("float64")
    for c in STR_COLS:
        df[c] = df[c].astype(str)
    for c in ("trigger_close_ms", "window_close_ms", "tide_against_close_ms", "bound_ms",
              "latch_1h_ms", "v6_entry_ms"):
        if c in df.columns:
            df[c] = df[c].astype("Int64")
    if "v6_net_r" in df.columns:
        df["v6_net_r"] = df["v6_net_r"].astype("float64")
    df = df.sort_values(["symbol", "entry_close_ms"], kind="mergesort").reset_index(drop=True)
    return df


def canonical_csv(df: pd.DataFrame) -> bytes:
    """The canonical CSV of the required columns [BOOK_SHA_RECIPE]."""
    d = df[list(REQUIRED)].sort_values(["symbol", "entry_close_ms"], kind="mergesort")
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(REQUIRED)
    for rec in d.itertuples(index=False, name=None):
        out = []
        for c, v in zip(REQUIRED, rec):
            if c in FLOAT_COLS:
                out.append(repr(float(v)))
            elif c in INT64_COLS or c == "direction":
                out.append(str(int(v)))
            else:
                out.append(str(v))
        w.writerow(out)
    return buf.getvalue().encode("utf-8")


def book_sha256(df: pd.DataFrame) -> str:
    return hashlib.sha256(canonical_csv(df)).hexdigest()


def sidecar(df: pd.DataFrame, arm: str, kind: str, ruler: str, era_scope: str,
            description: str) -> dict:
    s = {"registration": REG_ID, "arm": arm, "kind": kind, "ruler": ruler,
         "panel": list(E.CLASSIC5), "era_scope": era_scope, "n": int(len(df)),
         "sum_net_r": float(df["net_r"].sum()) if len(df) else 0.0,
         "book_sha256": book_sha256(df), "description": description,
         "source_script": "scripts/tierc11_stage_t_relay.py",
         # extras (the interface allows none to be missing; these are beside)
         "as_of_last_closed_4h": PIN_ISO, "seed": SEED,
         "book_sha256_recipe": BOOK_SHA_RECIPE,
         "mean_net_r": (float(df["net_r"].sum()) / len(df)) if len(df) else None,
         "label": BOOK_NOT_VERDICT}
    if kind == "tierE":
        s.update({"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
                  "gates": "nothing"})
    return s


def arms_of(R: dict) -> list[tuple]:
    """(arm, kind, ruler, era_scope, frame, description) — every arm written."""
    rec, base, late = R["reg_relay"], R["reg_v6"], R["reg_late"]
    miss_keys = set(R["miss_v6_keys"])
    miss_v6 = base[[(s, int(e)) in miss_keys for s, e in zip(base["symbol"], base["entry_ms"])]
                   ].reset_index(drop=True)
    return [
        ("scored", "scored", "two_sample", "full", rec,
         "P-RELAY-1 scored arm: the 1h EMA9/12 with-trend relay entered inside the armed v6 "
         "4h window strictly before min(trigger, counter 12/89, 89/316-against) [L-T.2]; "
         "stop struct_stop_4h as of the last closed 4h bar, railed 1.0 ATR, R on 4h; ridden "
         "by RD.relay11 (walk_after=True) and booked by tierc7._account_chain; CLASSIC5, "
         "full corridor; two-sample vs the base arm."),
        ("base", "base", "two_sample", "full", base,
         "card v6 (the 12/26-triggered base): TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, "
         "CLASSIC5) over the full TC11 corridor (tierc11_books.v6_book); entry_ms is v6's; "
         "exit_close_ms is the exit bar's close (SR-7)."),
        ("tierE__late_relay", "tierE", "two_sample", "full", late,
         "Tier-E rival reading (SR-6): relays allowed at/after the v6 4h trigger (the trigger "
         "bound removed; counter 12/89 and 89/316-against kept); one per window, one "
         "position per asset. a SELECTION, not a result."),
        ("tierE__tuning_slice", "tierE", "two_sample", "tuning",
         rec[rec["era"] == "tuning"].reset_index(drop=True),
         "Tier-E: the scored arm's campaigns whose entry close is in the tuning era "
         "(<= 2024-06-30T23:59:59Z, L-1.3); compare with base rows of era 'tuning'. a "
         "SELECTION, not a result."),
        ("tierE__holdout_slice", "tierE", "two_sample", "holdout",
         rec[rec["era"] == "holdout"].reset_index(drop=True),
         "Tier-E: the scored arm's campaigns whose entry close is in the holdout era; "
         "compare with base rows of era 'holdout'. a SELECTION, not a result."),
        ("tierE__miss_v6", "tierE", "vs_zero", "full", miss_v6,
         "Tier-E MISS COLUMN book: what v6 did in the windows the relay never activated "
         "(the v6 campaigns entered in missed windows). a SELECTION, not a result."),
    ]


# ═══════════════════════════════════════════════════════════════════ COMPUTE
def v6_anchor(v6) -> dict:
    """The base book is tierc11_books' v6 book: its TP._book_sha must equal the books
    manifest of record (F-CTRL is held there)."""
    man = json.loads(V6_BOOKS_MANIFEST.read_text(encoding="utf-8"))
    got, want = B.book_sha(v6), str(man["book_sha"]["v6"])
    if got != want or len(v6) != int(man["n"]["v6"]):
        _halt(f"the v6 base (sha {got[:16]}…, n {len(v6)}) is not the books manifest's "
              f"({want[:16]}…, n {man['n']['v6']})")
    return {"book_sha": got, "n": len(v6), "manifest": "research_outputs/tierc11/books/"
            "build_manifest.json"}


def registration_record() -> dict:
    reg = json.loads(REGISTRATIONS.read_text(encoding="utf-8"))
    hit = [r for r in reg["registrations"] if r["registration"] == REG_ID]
    if len(hit) != 1:
        _halt(f"{REG_ID} is not filed exactly once in REGISTRATIONS.json")
    r = hit[0]
    if r["operative_spec"]["ruler"] != "two-sample" or r["operative_spec"]["panel"] != "CLASSIC5":
        _halt(f"{REG_ID}'s operative spec is not two-sample on CLASSIC5")
    return {"text_sha256": r["text_sha256"], "sha256": r["sha256"], "seq": r["seq"],
            "tier_e_arms": list(r["operative_spec"]["tier_e_arms"])}


def h1_input_sha() -> dict:
    """sha256 of every 1h kline file the relay reads (TP.input_sha covers 4h + funding)."""
    out = {}
    for s in E.CLASSIC5:
        p = E.D.kline_path(s, "1h")
        out[s] = hashlib.sha256(Path(str(p)).read_bytes()).hexdigest()
    return out


def compute() -> dict:
    lo, hi, meta = B.corridor()
    reg = registration_record()
    v6 = B.v6_book(lo, hi)
    anc = v6_anchor(v6)
    # replay9 per asset must be the v6 book, campaign for campaign (SR-1)
    per = {}
    for s in E.CLASSIC5:
        per[s] = asset_ctx(s, lo, hi)["trades"]
    flat = [t for s in E.CLASSIC5 for t in per[s]]
    if B.book_sha(flat) != anc["book_sha"]:
        _halt("replay9's per-asset trades are not the v6 book")
    rec, win = relay_book(lo, hi, late=False)
    late, win_late = relay_book(lo, hi, late=True)
    reg_relay = regbook_frame(rec, "relay")
    reg_late = regbook_frame(late, "relay")
    reg_v6 = regbook_frame(v6, "v6")
    miss_keys = sorted((r["symbol"], int(r["v6_entry_ms"])) for _, r in win.iterrows()
                       if r["disposition"] != RELAYED and bool(r["v6_entered"]))
    return {"lo": lo, "hi": hi, "meta": meta, "reg": reg, "v6": v6, "anchor": anc,
            "relay": rec, "late": late, "win": win, "win_late": win_late,
            "reg_relay": reg_relay, "reg_late": reg_late, "reg_v6": reg_v6,
            "miss_v6_keys": miss_keys}


# ═══════════════════════════════════════════════════════════ THE STAGE TABLES
def _collared(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    for k, v in COLLAR.items():
        d[k] = v
    return d


WINDOW_COLS = ("symbol", "direction", "arm_ms", "arm_close_ms", "arm_i", "disp", "lag",
               "trigger_i", "trigger_close_ms", "window_end_i", "window_close_ms",
               "tide_against_i", "tide_against_close_ms", "bound_ms", "bound_kind",
               "cross_close_ms", "entry_kind", "moved", "entry_close_ms", "disposition",
               "relay_entry_ms", "relay_net_r", "relay_exit_reason", "lead_1h", "lead_4h",
               "v6_disposition", "v6_entered", "v6_entry_ms", "v6_entry_close_ms",
               "v6_net_r", "v6_exit_reason")
_INT_NULLABLE = ("lag", "trigger_i", "trigger_close_ms", "window_close_ms", "tide_against_i",
                 "tide_against_close_ms", "bound_ms", "cross_close_ms", "entry_close_ms",
                 "relay_entry_ms", "lead_1h", "lead_4h", "v6_entry_ms", "v6_entry_close_ms")


def window_table(win: pd.DataFrame, win_late: pd.DataFrame) -> pd.DataFrame:
    """THE MISS COLUMN, whole: one row per window, the record disposition and the
    late twin's beside it, and what v6 did."""
    a = win[list(WINDOW_COLS)].copy()
    lt = win_late[["symbol", "direction", "arm_ms", "bound_ms", "bound_kind",
                   "cross_close_ms", "entry_close_ms", "disposition", "relay_net_r",
                   "after_trigger"]].rename(columns={
                       "bound_ms": "late_bound_ms", "bound_kind": "late_bound_kind",
                       "cross_close_ms": "late_cross_close_ms",
                       "entry_close_ms": "late_entry_close_ms",
                       "disposition": "late_disposition", "relay_net_r": "late_relay_net_r",
                       "after_trigger": "late_after_trigger"})
    m = a.merge(lt, on=["symbol", "direction", "arm_ms"], how="left", validate="one_to_one")
    for c in _INT_NULLABLE + ("late_bound_ms", "late_cross_close_ms", "late_entry_close_ms"):
        m[c] = m[c].astype("Int64")
    for c in ("relay_net_r", "v6_net_r", "late_relay_net_r"):
        m[c] = m[c].astype("float64")
    m["moved"] = m["moved"].astype("boolean")
    m["late_after_trigger"] = m["late_after_trigger"].astype("boolean")
    m["direction"] = m["direction"].astype("int64")
    m["reason"] = m["disposition"].map(dict(DISPOSITIONS))
    m["late_reason"] = m["late_disposition"].map(dict(DISPOSITIONS))
    m = m.sort_values(["symbol", "arm_ms", "direction"], kind="mergesort").reset_index(drop=True)
    return _collared(m)


def disposition_grid(win: pd.DataFrame, win_late: pd.DataFrame) -> pd.DataFrame:
    """Per variant × disposition (EVERY typed code, zero rows included): n windows, the
    relay's n / ΣR, v6's entered n / ΣR in them."""
    rows = []
    for var, w in (("record", win), ("late", win_late)):
        for code, text in DISPOSITIONS:
            x = w[w["disposition"] == code]
            v = x[x["v6_entered"].astype(bool)]
            rr = x[x["disposition"] == RELAYED]
            rows.append({"variant": var, "disposition": code, "cell": f"{var}|{code}",
                         "reason": text, "n_windows": int(len(x)),
                         "n_lag0": int((x["lag"] == 0).sum()),
                         "relay_n": int(len(rr)),
                         "relay_sum_net_r": float(rr["relay_net_r"].sum()) if len(rr) else 0.0,
                         "v6_entered_n": int(len(v)),
                         "v6_sum_net_r": float(v["v6_net_r"].sum()) if len(v) else 0.0,
                         "v6_mean_net_r": (float(v["v6_net_r"].mean()) if len(v)
                                           else float("nan")),
                         "nan_reason": "" if len(v) else "no v6 campaign in these windows"})
        rows.append({"variant": var, "disposition": "ALL", "cell": f"{var}|ALL",
                     "reason": "every window", "n_windows": int(len(w)),
                     "n_lag0": int((w["lag"] == 0).sum()),
                     "relay_n": int((w["disposition"] == RELAYED).sum()),
                     "relay_sum_net_r": float(w.loc[w["disposition"] == RELAYED,
                                                    "relay_net_r"].sum()),
                     "v6_entered_n": int(w["v6_entered"].astype(bool).sum()),
                     "v6_sum_net_r": float(w.loc[w["v6_entered"].astype(bool),
                                                 "v6_net_r"].sum()),
                     "v6_mean_net_r": float(w.loc[w["v6_entered"].astype(bool),
                                                  "v6_net_r"].mean()),
                     "nan_reason": ""})
    return _collared(pd.DataFrame(rows))


def _bin(v: int, bins) -> str:
    for name, a, b in bins:
        if v >= a and (b is None or v <= b):
            return name
    _halt(f"lead {v} is in no bin")
    return ""


def lead_tables(win: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """The relay's lead over the v6 4h trigger (relayed windows that triggered):
    every distinct value (whole) and the typed bins (whole, zero cells included)."""
    x = win[(win["disposition"] == RELAYED)]
    trig = x[x["trigger_close_ms"].notna()]
    vals, bins = [], []
    for kind, col, B_ in (("lead_4h_bars", "lead_4h", LEAD_4H_BINS),
                          ("lead_1h_bars", "lead_1h", LEAD_1H_BINS)):
        v = trig[col].astype(int)
        for val, n in sorted(v.value_counts().items()):
            vals.append({"lead_kind": kind, "lead_value": int(val), "n": int(n)})
        for name, a, b in B_:
            n = int(sum(1 for q in v if _bin(int(q), B_) == name))
            bins.append({"lead_kind": kind, "bin": name, "cell": f"{kind}|{name}", "n": n})
        bins.append({"lead_kind": kind, "bin": "no trigger (NA)",
                     "cell": f"{kind}|no trigger (NA)",
                     "n": int(x["trigger_close_ms"].isna().sum())})
    return _collared(pd.DataFrame(vals)), _collared(pd.DataFrame(bins))


def era_slices(R: dict) -> pd.DataFrame:
    rows = []
    for arm, df in (("scored (relay)", R["reg_relay"]), ("base (v6)", R["reg_v6"]),
                    ("tierE__late_relay", R["reg_late"])):
        for era in ("tuning", "holdout", "full"):
            x = df if era == "full" else df[df["era"] == era]
            n = int(len(x))
            rows.append({"arm": arm, "era": era, "cell": f"{arm}|{era}", "n": n,
                         "sum_net_r": float(x["net_r"].sum()) if n else 0.0,
                         "mean_net_r": float(x["net_r"].mean()) if n else float("nan"),
                         "sum_haircut_net_r": float(x["haircut_net_r"].sum()) if n else 0.0,
                         "win_pct": (100.0 * float((x["net_r"] > 0).sum()) / n) if n
                         else float("nan"),
                         "nan_reason": "" if n else "no campaign"})
    return _collared(pd.DataFrame(rows))


def disclosure(R: dict) -> dict:
    rel = R["reg_relay"]
    kinds = {k: int(v) for k, v in sorted(rel["entry_kind"].value_counts().items())}
    mism = sorted({x for s in rel["walk_mismatch_ms"] for x in s.split(",") if x})
    # SR-5's disclosure: relays the v6 4h-bar law (entry bar <= previous exit bar) refuses
    v6law = 0
    for s, g in rel.groupby("symbol", sort=True):
        g = g.sort_values("entry_close_ms", kind="mergesort")
        prev_exit_i = None
        for _, r in g.iterrows():
            if prev_exit_i is not None and int(r["relay_J"]) <= prev_exit_i:
                v6law += 1
            prev_exit_i = int(r["exit_i"])
    return {"entry_kinds": kinds, "n_moved": int(rel["moved"].sum()),
            "n_mismatch_bar_rides": int(rel["n_walk_mismatch"].sum()),
            "mismatch_bars_named": mism,
            "exit_reasons": {k: int(v) for k, v in
                             sorted(rel["exit_reason"].value_counts().items())},
            "exit_resolved_by": {k: int(v) for k, v in
                                 sorted(rel["exit_resolved_by"].value_counts().items())},
            "stopped_inside_J": int(((rel["exit_i"] == rel["relay_J"])
                                     & (rel["exit_reason"] == "stop")).sum()),
            "belled_at_J": int(((rel["exit_i"] == rel["relay_J"])
                                & rel["exit_reason"].str.startswith("bell")).sum()),
            "relays_the_v6_4h_bar_law_would_refuse": v6law,
            "after_trigger_record": int(rel["after_trigger"].sum()),
            "after_trigger_late": int(R["reg_late"]["after_trigger"].sum())}


# ═══════════════════════════════════════════════════════════════════ RENDER
def _f(x, nd: int = 4) -> str:
    if x is None or (isinstance(x, float) and x != x) or (x is pd.NA):
        return "—"
    return f"{float(x):+.{nd}f}"


def _i(x) -> str:
    return "—" if x is None or x is pd.NA or (isinstance(x, float) and x != x) else iso(int(x))


def _collar_cols() -> str:
    return f" {COLLAR['tier']} | {COLLAR['selection_not_a_result']} | {COLLAR['gates']} |"


def render_md(R: dict, T: dict, arms: list, side: dict, disc: dict) -> str:
    L = []
    A = L.append
    A("as_of_last_closed_4h: 2026-09-25T00:00:00Z")
    A("")
    A("# TIER-C11 · STAGE T-relay — P-RELAY-1 (the 1h relay inside the armed 4h window)")
    A("")
    A(f"substrate {E.SNAPSHOT.name} · corridor {iso(R['lo'])} → {iso(R['hi'] + 1)} · CLASSIC5 · "
      f"seed {SEED} · registration {REG_ID} seq {R['reg']['seq']} text sha "
      f"{R['reg']['text_sha256'][:16]}… payload sha {R['reg']['sha256'][:16]}…")
    A("")
    A("**This stage builds books, not verdicts.** No CI, no p and no verdict word appear here; "
      "the scorer reads `research_outputs/tierc11/regbooks/P-RELAY-1/`. Every non-registered "
      "table carries the L-1.4 collar (tier = 'TIER-E', selection_not_a_result = 'a "
      "SELECTION, not a result', gates = 'nothing').")
    A("")
    A("## Readings built")
    A("")
    for ln in READINGS:
        A(f"- {ln}")
    A("")
    A("## Anchor")
    A("")
    A(f"- base v6 = tierc11_books.v6_book over the full TC11 corridor: TP._book_sha "
      f"{R['anchor']['book_sha']} n {R['anchor']['n']} == the books manifest of record "
      f"(F-CTRL held there); replay9's per-asset trades reproduce it campaign for campaign.")
    A("")
    A("## Regbooks written (book, not a verdict)")
    A("")
    A("| arm | kind | ruler | era_scope | n | ΣR (net) | mean R | Σ haircut R | book_sha256 | label |")
    A("|---|---|---|---|---:|---:|---:|---:|---|---|")
    for arm, kind, ruler, era_scope, df, _ in arms:
        s = side[arm]
        n = len(df)
        A(f"| {arm} | {kind} | {ruler} | {era_scope} | {n} | {_f(s['sum_net_r'])} | "
          f"{_f(s['mean_net_r']) if n else '—'} | "
          f"{_f(float(df['haircut_net_r'].sum()) if n else 0.0)} | {s['book_sha256'][:16]}… | "
          f"{BOOK_NOT_VERDICT}{' · Tier-E, a SELECTION, not a result' if kind == 'tierE' else ''} |")
    A("")
    A("## The window dispositions — a partition of every armed window (Tier-E, whole)")
    A("")
    g = T["relay_disposition_grid"]
    A("| variant | disposition | n windows | of which lag 0 | relay n | relay ΣR | v6 entered n | "
      "v6 ΣR in them | v6 mean R | tier | selection_not_a_result | gates |")
    A("|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|")
    for _, r in g.iterrows():
        A(f"| {r['variant']} | {r['disposition']} | {r['n_windows']} | {r['n_lag0']} | "
          f"{r['relay_n']} | {_f(r['relay_sum_net_r'])} | {r['v6_entered_n']} | "
          f"{_f(r['v6_sum_net_r'])} | {_f(r['v6_mean_net_r'])} |" + _collar_cols())
    A("")
    A("Disposition codes: " + " · ".join(f"`{c}` {t}" for c, t in DISPOSITIONS) + ".")
    A("")
    A("## The lead of the relay over the v6 4h trigger (relayed windows, Tier-E, whole)")
    A("")
    lb = T["relay_lead_bins"]
    A("| lead kind | bin | n | tier | selection_not_a_result | gates |")
    A("|---|---|---:|---|---|---|")
    for _, r in lb.iterrows():
        A(f"| {r['lead_kind']} | {r['bin']} | {r['n']} |" + _collar_cols())
    A("")
    lv = T["relay_lead_values"]
    A("Every distinct value (whole):")
    A("")
    A("| lead kind | lead value (bars) | n | tier | selection_not_a_result | gates |")
    A("|---|---:|---:|---|---|---|")
    for _, r in lv.iterrows():
        A(f"| {r['lead_kind']} | {r['lead_value']} | {r['n']} |" + _collar_cols())
    A("")
    A("## Era slices (by the entry CLOSE, L-1.3; Tier-E, whole)")
    A("")
    es = T["relay_era_slices"]
    A("| arm | era | n | ΣR | mean R | Σ haircut R | win % | tier | selection_not_a_result | gates |")
    A("|---|---|---:|---:|---:|---:|---:|---|---|---|")
    for _, r in es.iterrows():
        A(f"| {r['arm']} | {r['era']} | {r['n']} | {_f(r['sum_net_r'])} | {_f(r['mean_net_r'])} "
          f"| {_f(r['sum_haircut_net_r'])} | "
          f"{'—' if r['win_pct'] != r['win_pct'] else format(r['win_pct'], '.2f')} |"
          + _collar_cols())
    A("")
    A("## Mechanics disclosed (the relay book)")
    A("")
    A(f"- entry kinds: {disc['entry_kinds']} · moved to the parent's close (L-W.0): "
      f"{disc['n_moved']}")
    A(f"- mismatch-bar count (AM-5, bars ridden by the parent, summed over the book): "
      f"{disc['n_mismatch_bar_rides']}; bars named: "
      f"{', '.join(disc['mismatch_bars_named']) if disc['mismatch_bars_named'] else 'none'}")
    A(f"- exit reasons: {disc['exit_reasons']} · exit resolved by: {disc['exit_resolved_by']}")
    A(f"- stopped inside the entry bar J: {disc['stopped_inside_J']} · belled at J's close: "
      f"{disc['belled_at_J']}")
    A(f"- SR-5 disclosure: relays the v6 4h-bar position law (entry bar <= previous exit bar) "
      f"would refuse: {disc['relays_the_v6_4h_bar_law_would_refuse']}")
    A(f"- relays at/after the trigger: record {disc['after_trigger_record']} (must be 0, L-T.3) "
      f"· late twin {disc['after_trigger_late']}")
    A("")
    A("## The relay book (scored arm), whole — book, not a verdict")
    A("")
    rel = R["reg_relay"]
    A("| asset | dir | arm close | 1h cross close | entry (instant) | kind | trigger close | "
      "lead 1h | stop | R | exit (instant) | exit_reason | net R | haircut R | era | v6 in window |")
    A("|---|---:|---|---|---|---|---|---:|---:|---:|---|---|---:|---:|---|---|")
    wl = R["win"].set_index(["symbol", "direction", "arm_ms"])
    for _, r in rel.iterrows():
        w = wl.loc[(r["symbol"], int(r["direction"]), int(r["arm_ms"]))]
        v6 = (f"entered {_f(r['v6_net_r'])}" if bool(r["v6_entered"])
              else str(w["v6_disposition"]))
        A(f"| {r['symbol']} | {int(r['direction']):+d} | {_i(r['window_arm_close_ms'])} | "
          f"{_i(r['cross_close_ms'])} | {_i(r['entry_close_ms'])} | {r['entry_kind']} | "
          f"{_i(r['trigger_close_ms'])} | "
          f"{'—' if w['lead_1h'] is None or w['lead_1h'] != w['lead_1h'] else int(w['lead_1h'])} | "
          f"{r['stop_px']:.6g} | {r['r_dist']:.6g} | {_i(r['exit_close_ms'])} | "
          f"{r['exit_reason']} | {_f(r['net_r'], 6)} | {_f(r['haircut_net_r'], 6)} | {r['era']} | "
          f"{v6} |")
    A("")
    A("## The miss column — every window the relay never activated, whole (Tier-E)")
    A("")
    wt = T["relay_windows"]
    ms = wt[wt["disposition"] != RELAYED]
    A("| asset | dir | arm close | lag | trigger close | window close | 89/316 against | "
      "first 1h 9/12 close | disposition | what v6 did | v6 net R | late twin | tier | "
      "selection_not_a_result | gates |")
    A("|---|---:|---|---:|---|---|---|---|---|---|---:|---|---|---|---|")
    for _, r in ms.iterrows():
        late = (f"{r['late_disposition']} {_f(r['late_relay_net_r'])}"
                if r["late_disposition"] == RELAYED else str(r["late_disposition"]))
        A(f"| {r['symbol']} | {int(r['direction']):+d} | {_i(r['arm_close_ms'])} | "
          f"{'—' if pd.isna(r['lag']) else int(r['lag'])} | {_i(r['trigger_close_ms'])} | "
          f"{_i(r['window_close_ms'])} | {_i(r['tide_against_close_ms'])} | "
          f"{_i(r['cross_close_ms'])} | {r['disposition']} | {r['v6_disposition']} | "
          f"{_f(r['v6_net_r'])} | {late} |" + _collar_cols())
    A("")
    A("## The FORWARD LEDGER (L-T.6) — both books side by side")
    A("")
    fl, fm = FWD_DIR / "FORWARD_LEDGER.jsonl", FWD_DIR / "FORWARD_LEDGER.md"
    if fl.exists() and fm.exists():
        md = fm.read_text(encoding="utf-8")
        A(f"From `research_outputs/tierc11/forward/` (scripts/tierc11_forward_ledger.py --refresh): "
          f"FORWARD_LEDGER.jsonl sha256 {hashlib.sha256(fl.read_bytes()).hexdigest()} · "
          f"FORWARD_LEDGER.md sha256 {hashlib.sha256(md.encode('utf-8')).hexdigest()}. The "
          f"ledger's own report follows verbatim from its side-by-side table.")
        A("")
        body = md[md.index("## Both books, side by side"):] if "## Both books, side by side" \
            in md else md
        for ln in body.rstrip("\n").split("\n"):
            A(ln.replace("## ", "### ", 1) if ln.startswith("## ") else ln)
    else:
        A("(the forward ledger has not been refreshed yet — run scripts/tierc11_forward_ledger.py "
          "--refresh before this report)")
    A("")
    A("## Files")
    A("")
    for k in sorted(x for x in T if not x.endswith("__sha")):
        A(f"- `stage_t_relay/{k}.parquet` content sha {T[k + '__sha'][:16]}…")
    for arm, *_ in arms:
        A(f"- `regbooks/{REG_ID}/{arm}.parquet` + `{arm}.json` book_sha256 "
          f"{side[arm]['book_sha256'][:16]}…")
    A(f"- `regbooks/{REG_ID}/STATUS.json`")
    A("- the FORWARD LEDGER of this stage (L-T.6) is `research_outputs/tierc11/forward/"
      "FORWARD_LEDGER.jsonl` + `FORWARD_LEDGER.md` (scripts/tierc11_forward_ledger.py); the "
      "fixtures are `scripts/tierc11_stage_t_relay_fixtures.py` → "
      "`stage_t_relay/FIXTURES_STAGE_T_RELAY.txt`")
    return "\n".join(L) + "\n"


# ═══════════════════════════════════════════════════════════════════ BUILD
def _inside(p: Path, root: Path) -> bool:
    return p == root or root in p.parents


def _guard_out(out: Path) -> Path:
    """OUT's parent layout (the record), a direct child of DET_ROOT, or a direct child
    of a `_det_stage_t_relay/` directory OUTSIDE the repo tree."""
    o = Path(out).resolve()
    if o == E.OUT.resolve() or o.parent == DET_ROOT.resolve():
        return o
    trees = {ROOT.resolve(), Path(E.MAIN_TREE).resolve()}
    if o.parent.name == DET_ROOT.name and not any(_inside(o, t) for t in trees):
        return o
    _halt(f"output root {o} is neither {E.OUT}, an F-DET run dir under {DET_ROOT}, nor one "
          f"under a {DET_ROOT.name}/ scratch outside the repo")
    return o


def write_regbook(root: Path, arm: str, df: pd.DataFrame, side: dict) -> dict:
    d = root / "regbooks" / REG_ID
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{arm}.parquet"
    df.to_parquet(str(p), index=False)
    (d / f"{arm}.json").write_text(json.dumps(side, indent=2, sort_keys=True) + "\n",
                                   encoding="utf-8")
    return {"parquet": f"regbooks/{REG_ID}/{arm}.parquet",
            "content_sha": TB._content_sha(df), "book_sha256": side["book_sha256"]}


def build(root: Path = E.OUT) -> dict:
    """Compute, then write the stage tables, the regbooks and the report under `root`
    (the record: research_outputs/tierc11/)."""
    root = _guard_out(root)
    R = compute()
    stage = root / "stage_t_relay"
    T = {"relay_windows": window_table(R["win"], R["win_late"]),
         "relay_disposition_grid": disposition_grid(R["win"], R["win_late"]),
         "relay_era_slices": era_slices(R)}
    T["relay_lead_values"], T["relay_lead_bins"] = lead_tables(R["win"])
    keys = {"relay_windows": ["symbol", "arm_ms", "direction"],
            "relay_disposition_grid": ["variant", "disposition"],
            "relay_era_slices": ["arm", "era"],
            "relay_lead_values": ["lead_kind", "lead_value"],
            "relay_lead_bins": ["lead_kind", "bin"]}
    put, W, K, SK = TP.make_put(stage, R["meta"], lens="4h")
    for name in sorted(T):
        put(T[name], name, keys[name])
    if SK:
        _halt(f"an empty stage table: {SK}")
    for name in W:
        T[name + "__sha"] = W[name]
    arms = arms_of(R)
    side, regs = {}, {}
    for arm, kind, ruler, era_scope, df, desc in arms:
        side[arm] = sidecar(df, arm, kind, ruler, era_scope, desc)
        stamped = TP.stamp_n(df, R["meta"], "4h")
        stamped.attrs = {}
        regs[arm] = write_regbook(root, arm, stamped, side[arm])
    status = {"registration": REG_ID, "status": "BUILT",
              "reason": "the relay book and its base / Tier-E arms were built on the TC11 "
                        "corridor exactly as L-T.2 reads (no precondition or condition)",
              "arms": [a[0] for a in arms], "as_of_last_closed_4h": PIN_ISO,
              "source_script": "scripts/tierc11_stage_t_relay.py"}
    (root / "regbooks" / REG_ID / "STATUS.json").write_text(
        json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    disc = disclosure(R)
    man = {"tier": "TIER-C11", "stage": "TC11-T (relay)", "registration": REG_ID,
           "seed": SEED, "as_of": PIN_ISO, "as_of_close_ms": PIN_MS,
           "substrate": R["meta"]["substrate"],
           "corridor": {"lo": iso(R["lo"]), "hi_close": iso(R["hi"] + 1),
                        "panel": list(E.CLASSIC5)},
           "sha": W, "keys": K, "skipped_empty": SK,
           "input_sha": TP.input_sha(E.CLASSIC5), "input_sha_1h": h1_input_sha(),
           "v6_anchor": R["anchor"], "registration_record": R["reg"],
           "regbooks": regs, "disclosure": disc,
           "collar": {"applies_to": "every stage table here and every tierE__ arm", **COLLAR},
           "readings": list(READINGS), "dispositions": dict(DISPOSITIONS),
           "book_sha256_recipe": BOOK_SHA_RECIPE}
    (stage / MANIFEST).write_text(json.dumps(man, indent=2, sort_keys=True, default=str)
                                  + "\n", encoding="utf-8")
    (stage / REPORT).write_text(render_md(R, T, arms, side, disc), encoding="utf-8")
    R.update({"tables": T, "sidecars": side, "manifest": man, "disclosure": disc,
              "arms": arms})
    return R


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    od = next((a.split("=", 1)[1] for a in args if a.startswith("--out-dir=")), None)
    R = build(Path(od) if od else E.OUT)
    for arm, kind, ruler, era_scope, df, _ in R["arms"]:
        n = len(df)
        s = float(df["net_r"].sum()) if n else 0.0
        print(f"{arm:22} {kind:6} {ruler:10} {era_scope:8} n {n:4d} · ΣR {s:+.6f} · mean "
              f"{(s / n if n else float('nan')):+.6f} ({BOOK_NOT_VERDICT})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
