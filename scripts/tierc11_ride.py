#!/usr/bin/env python
"""TIER-C11 · THE RIDE — one engine, `ride11`, that IS card v6 when every hook
is off, and carries the hooks the frozen executor readings need.

Contract of record: exchange/queue/2026-09-24_TC11_APOLLO.md (sha256 bb38e016…).
Executor HEPHAESTUS; seed 20260924.  Readings of record: research_outputs/tierc11/
LEANS.md (frozen at 4ed4e67).  This module builds, and nothing else:
  L-W.0  the 1h WALK law ................................. `walk_of`, `ride11(walk=)`
  L-W.3  the 1h +1R latch and the 1h-RESOLVED exit ........ `ride11(walk=)`
  L-W.5  the WARN exit ..................................... `ride11(warn=)`
  L-A.1  the ADDS, booked by tierc7._account_chain ......... `admit_adds`
  L-H.1  the TAKE-PROFIT resting limit (+ its twins) ...... `ride11(tp=)`
  L-T.2  the RELAY ride (a 1h-close entry inside a 4h bar)  `relay11`, `relay_entry`,
                                                            `relay_stop`
  L-1.5  the v6 campaign set, rebuilt and TRANSFORMED ..... `v6_inputs`,
         and the IDENTITY law ............................ `transform_book`,
                                                            `identity_findings`

A DECISION MODULE [L-F.2].  It imports tierc11_env (the RANGE-FREE shim) and the
v6 lineage through it — never tierc11_nest, tierc10_census, tierc10_stamps,
tierc10_null, analytics.rangefinder_census or engine.rangefinder, and it reads no
Range object.  Range facts arrive as PLAIN ARRAYS from the caller: the TP levels
(`TPLevels.level_long/level_short`, NaN = no level), the add events ((1h close ms,
price) pairs), the 1h EMA crosses (`Warn.up/dn`, computed here from the 1h close
by the engine's own `ind.ema`, which is not range code).  It computes and prints
no registered book; the stage runners do.

THE ENGINE.  `ride11` is `tierc9._ride_leg9` transcribed, per 4h bar j:
  top of bar   +1R latch (v6: BEFORE the stop test), trail arming, harvest touch;
  intrabar     the exits in EXIT_ORDER = STOP -> WARN -> TP (adverse-first);
  the close    BELL -> HARVEST -> TRAIL (v6's close slot, unchanged).
With walk / warn / tp all None and no injected state it is `_ride_leg9` line for
line (F-RELAY-RIDE and F-WALK-IDENT prove it at 0.000e+00 on the whole CLASSIC5
book over the TC11 corridor).

(h0) THE 1h WALK [L-W.0, L-W.3].  `walk_of(sym)` marks each 4h bar WALKABLE iff
its four native 1h children exist on the 1h grid inside it and reproduce the
parent's high, low and close to REPR_TOL (= tierc10_lanes.REPR_TOL, 1e-9
relative, through tierc10_lanes._same_px — the be_sequence law).  On a walkable
bar the CHILDREN decide, in tape order, per child CHILD_ORDER = STOP -> LATCH ->
WARN; the parent's own stop answer must agree (L-W.3's HALT: a stop-exit bar on a
walkable bar with no child touching the stop HALTs, and so does the converse).
On any other bar the PARENT decides STOP and the +1R latch exactly as v6 does,
1h-only events on it are taken at the parent's close, and the bar is COUNTED
(`n_walk_mismatch`, `walk_mismatch_ms`).
  Outputs:  `latch_1h_ms`  close of the first child that LATCHED under the walk
                           law (STOP first: a child that both stops and prints
                           +1R stops and does not latch); a parent-decided latch
                           is stamped at the parent's close (`latch_1h_by`);
            `plus1r_1h_ms` the literal L-W.3 child: the first child after the
                           entry close whose high (low) reaches entry +/- R,
                           through the exit child; it differs from latch_1h_ms
                           only when that child is the stop child
                           (`latch_on_stop_child` = True) — both printed, so no
                           cohort reading is chosen here;
            `exit_close_ms` the 1h-RESOLVED exit instant: a stop exits at the
                           close of the first child of the exit bar touching the
                           stop in force (`exit_resolved_by` = '1h'); bell /
                           corridor_end at the 4h close ('close'); a stop on a
                           mismatch bar at the parent's close ('parent').
  THE WALK RESOLVES WHEN, NEVER WHAT, while no rule acts: v6's bar-level fields
  (reached_1r, mae_to_1r, mae, trail arming, and mfe's adverse-first law on a stop
  bar) keep v6's arithmetic, so F-WALK-IDENT is an identity, not a hope.

(h1) THE WARN EXIT [L-W.5].  On each walked child: STOP -> +1R latch -> at the
child's close, if pre-+1R (no 1h latch yet) and a counter cross closed on that
child, exit at that 1h close (`Warn.label`).  On a mismatch bar: the parent's
stop, the parent's latch (v6: top of bar), then at the parent's close the same
test over every child whose close lies in the bar.  A warn exit ends the bar at
that child, so the bar's mae / mae_to_1r / mfe are the HELD values through that
child [executor sub-reading, tierc10_lanes L-be-mfe's law at 1h resolution];
reached_1r stays what it was before the bar (a warn exit is pre-+1R by
definition).  BELL / HARVEST / TRAIL at 4h closes unchanged.

(h2) THE ADDS [L-A.1].  `admit_adds` takes the caller's (1h close ms, price)
events in time order and admits at most ADDS_MAX = 2 that are IN-TRADE (1h close
> the entry close and < the 1h-resolved exit) and AFTER the 1h latch (an event
on the latch child counts as after).  THE PRICE IS THE TAPE'S: an add enters "at
the 1h close of the triggering event", so the price is `walk.h1.c` of the 1h bar
closing at the event instant; a caller price (None = take the tape's) that is not
exactly that close HALTs [L-A.1].  An event on a mismatch bar is taken at the
parent's close at the parent's close price [L-W.0] (`moved_to_parent_close`).
Each admitted add is `RC.Add(i = the 4h bar containing the add's 1h close, size
0.5, px)`; the leg is booked by `tierc7._account_chain` unchanged: adds exit at
the campaign's exit price, are never harvested, funding runs from bar i+1's
open, the D12 ceiling is applied ONCE on the campaign's total.  add_r is printed
beside net_r; flags `below_entry` ((px - entry)*d < 0) and `post_harvest`
(harvest fired and i >= harvest_i: inside or after the harvest's 4h bar); the
Tier-E twins refusing each class are options (`refuse_below_entry`,
`refuse_post_harvest`).  Every event gets a disposition.
  SUB-READING (twin order) [executor]: the twin refusals are judged BEFORE the
  2-add cap, so an event a twin refuses does not spend a slot, and a later
  event of the other class may take it (the twin is "the book without that
  class of adds", not "the record book with those adds voided").
  NOTE (L-1.5 x L-A.1): when the D12 ceiling binds on the total, the paired
  delta net_r - v6 net_r is NOT add_r: it is add_r + (funding_uncapped -
  funding_capped) for a v6 leg the ceiling does not bind.  net_r is
  `_account_chain`'s (L-A.1); runners score the paired delta on net_r and never
  assert delta == add_r (AMENDMENT CANDIDATE on L-1.5's wording, raised by the
  TC11-RIDE verifier; F-ADD-ACCT prints the decomposition).

(h3) THE TAKE-PROFIT [L-H.1].  Per 4h bar j after entry: level = level_long[j]
(level_short[j]); a resting limit for the remainder is LIVE iff the level is
finite, the prior 4h close is on the NEAR side ((level - c[j-1])*d > 0 — a prior
close AT the level counts as not near [executor tie-break, measure zero]), and
(level - entry_px)*d > TP_GUARD_BPS (10 bps = the round-trip taker fee, L-1.1)
* entry_px.  Fill if h[j] >= level at max(level, o[j]) (long; l[j] <= level at
min(level, o[j]) short).  Order: STOP -> TP -> (close) BELL -> HARVEST -> TRAIL.
The remainder is whatever is open (1.0 before the band harvest, 0.5 after) —
`_account_chain` books it.  Modes: 'record'; 'post_harvest' (the twin: live only
once the v6 harvest has fired); 'unguarded' (the twin without the guard).
Counts per campaign: live bars, guard-withheld, far-side, pre-harvest-withheld,
a fill blocked by the stop.  The TP is 4h-granular (adverse-first) and is never
combined with the warn hook (no reading orders them) — HALT.  Under the walk
the TP's exit INSTANT is the close of the first child of j reaching the level
('1h'; a walkable bar where no child reaches it HALTs, as L-W.3's stop law), or
the parent's close on a mismatch bar ('parent').
  SUB-READING (TP-bar mfe) [executor]: on the TP exit bar mfe is capped at the
  FILL price, never the bar's high (low): the position is closed at the fill,
  and adverse-first 4h granularity cannot place the rest of the bar's range
  before the fill.  mfe_r is a CTRL_COL, so this is stated, not implied.

(h4) THE RELAY [L-T.2].  `relay_entry` resolves a 1h-close entry instant: at a
4h close it is a 4h-close entry (price = that 4h bar's close); strictly inside a
walkable bar J it is a 1h entry at that 1h close; inside a MISMATCH bar it is
taken at the parent's close [L-W.0] (flagged `moved`; pass `moved=True` to
relay11 so the bar is COUNTED in n_walk_mismatch).  Given `trigger_close_ms`,
an entry whose RESOLVED instant is at or after the window's 4h trigger close
is `refused` (L-T.2 / L-T.3: strictly before the trigger — a moved entry can
land exactly on it).  `relay_stop` =
struct_stop_4h with pivots confirmed and ATR(4h) as of the last CLOSED 4h bar at
the entry instant, railed card.entry_rail_atr (1.0) ATR.  `relay11` walks J's
post-entry children for STOP and the +1R latch, then J's close runs v6's close
slot (BELL on w_dn[J]/b_dn[J], mirrored; HARVEST armed per close[J-1], the touch
judged on the post-entry children only; TRAIL armed iff the latch fired), then
the 4h ride continues from J+1 with the state CARRIED (`carry_state`; the L-T.2
named set: stop, reached_1r, trail_armed, h_armed, mfe, mae, mae_to_1r — plus the
record: advances, harvest, blocked, opportunities, latch stamps).  An entry at a
4h close runs `ride11` from the next bar on a fresh state == `_ride_leg9`.
Trade convention: entry_i = J; entry_ms = the OPEN of the entry's own bar (the 4h
bar for a 4h-close entry — v6's convention — the 1h bar for a 1h entry);
`entry_close_ms` carries the exact instant.
  SUB-READING (the stop unit) [executor]: a relay stopped INSIDE J books mae /
  mfe at 1h resolution — the stop CHILD is the stop unit (its adverse counts,
  its favourable does not, nothing after it counts), the 1h image of v6's
  adverse-first stop-bar law.  ride11 on a WALKED stop bar keeps the 4h stop
  unit (the whole bar's adverse) so that the walk resolves WHEN, never WHAT
  (F-WALK-IDENT).  The relay's J has no 4h unit that excludes its pre-entry
  children, so it cannot take the 4h law; after J the relay is ride11's.
  HAZARD (walk_after): without `walk_after=True` the ride after J is v6's
  bar-level ride, so a relay can end with reached_1r True and latch_1h_ms None;
  a runner needing 1h latch stamps passes walk_after=True.

L-R.5 STAMPS.  `exit_stamp_ms` / `latch_stamp_ms` are the stamps of record: an
intrabar event (+1R, a stop, a TP fill) at the close of the 1h child that
resolves it, else at the OPEN of its 4h bar (a mismatch bar decided by the
parent, or a ride without the walk); a close event (bell, corridor_end, a warn
exit) at its close.  `exit_close_ms` / `latch_1h_ms` of a parent-decided event
are the parent's CLOSE — L-R.5's "post-event" twin.

READING-LEVEL DISCLOSURE (L-W.0) [not a module defect]: whether bar j is walked
is decided from all four children and the parent's high, low and close, so
"act at child k's close, or defer to the parent's close" depends on prices
later in the same 4h bar.  It moves no v6 number (F-WALK-IDENT) and touches only
the corridor's mismatch bars (listed by F-DET's probe).

FIXTURE SEAMS (named, greppable): `exit_order=`, `child_order=` (ride11 /
relay11), `carry=` (relay11), `max_adds=` (admit_adds), and a `Walk` built by
the caller.  The defaults are the readings.  (The fixtures also ride MUTATED
shadow copies of this file; nothing here reads its own path.)

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_ride.py          # prints the ride spec
"""
from __future__ import annotations

import copy
import dataclasses
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc11_env as E                                              # noqa: E402

T9, T8, T7, T5, D, LN = E.T9, E.T8, E.T7, E.T5, E.D, E.LN
RC = T9.RC                          # the exact rules object replay9 rides on
ind = T9.ind                        # engine.indicators, as tierc9 holds it

SEED = E.SEED                       # 20260924 — printed; this module draws nothing
MS_1H = 3_600_000
MS_4H = 14_400_000
N_1H = MS_4H // MS_1H               # 4 — an identity, not a pin
if MS_4H != int(T5.MS_4H):
    raise SystemExit("HALT: MS_4H disagrees with the lineage's")
REPR_TOL = float(LN.REPR_TOL)       # 1e-9 relative — the be_sequence law [L-W.0]
same_px = LN._same_px               # the law of record, not a copy of it

EXIT_ORDER = ("stop", "warn", "tp", "bell")     # intrabar, adverse-first; then the close
CHILD_ORDER = ("stop", "latch", "warn")         # per 1h child [L-W.5]
ADDS_MAX = 2                                     # "at most 2 adds" [L-A.1]
ADD_SIZE = 0.5                                   # "each a 0.5-unit tranche" [L-A.1]
TP_GUARD_BPS = 2.0 * float(RC.FEE_BPS_SIDE)      # 10 bps = the round-trip taker fee [L-1.1]
TP_MODES = ("record", "post_harvest", "unguarded")
TP_REASON = "tp"
WARN_LABEL = "warn_1h_12_89"

# L-T.2's carried set, by name; the rest of the state is the leg's own record.
CARRY_KEYS = ("stop", "reached_1r", "trail_armed", "h_armed", "mfe", "mae", "mae_to_1r")
STATE_KEYS = CARRY_KEYS + ("advances", "harv", "blocked", "n_opp", "latch_1h_ms",
                           "latch_1h_by", "plus1r_1h_ms", "mismatch_ms")


# ══════════════════════════════════════════════════════ THE CARD'S SCOPE
_CARD_FIELDS = frozenset(f.name for f in dataclasses.fields(T8.Card))


def scope(card) -> None:
    """ride11 rides card v6's MECHANICS only (replay9's guard, plus the knobs it
    never named).  A knob away from its v6 value HALTs rather than ride
    silently under a card's name; a card class with fields T8.Card does not have
    HALTs (totality, as tierc10_lanes.replay10's guard)."""
    names = frozenset(f.name for f in dataclasses.fields(card))
    if names != _CARD_FIELDS:
        raise SystemExit(f"HALT: tierc11_ride rides T8.Card's field set exactly; "
                         f"{type(card).__name__} adds {sorted(names - _CARD_FIELDS)} "
                         f"/ lacks {sorted(_CARD_FIELDS - names)}")
    bad = []
    for k, ok in (("lane", card.lane == "card"), ("adds_max", not card.adds_max),
                  ("seal_open", bool(card.seal_open)),
                  ("trail_extra_buf_atr", not card.trail_extra_buf_atr),
                  ("weave", not card.weave), ("reentry", not card.reentry),
                  ("ae_abort_r", card.ae_abort_r is None),
                  ("time_stop_bars", card.time_stop_bars is None),
                  ("anchor_kind", card.anchor_kind == "pivot"),
                  ("hybrid_anchor", not card.hybrid_anchor),
                  ("stop_grid_offset_atr", not card.stop_grid_offset_atr),
                  ("anchor_offset", card.anchor_offset == RC.STOP_BUF_ATR),
                  ("harvest", card.harvest == "band"),
                  ("wall_exit_atr", card.wall_exit_atr is None),
                  ("limit_ae_mult", card.limit_ae_mult is None),
                  ("grid", card.grid == "card")):
        if not ok:
            bad.append(f"{k}={getattr(card, k)!r}")
    if bad:
        raise SystemExit(f"HALT: tierc11_ride rides v6 mechanics only; the card sets "
                         f"{bad} (adds arrive through admit_adds, never through the card)")


def ctx_of(sym: str, card, roles) -> dict:
    """The 4h context replay9 reads, from the lineage's own memos."""
    st = T9.frame(sym)
    return {"f": st["f"], "pv4": st["pv4"], "ra": T9.role_arrays(sym, roles),
            "fr": T9.fractals(sym, card.trail_l, card.trail_r) if card.trail else None,
            "s": T8.anchor_series(sym)}


# ══════════════════════════════════════════════════ THE 1h TAPE AND THE WALK
@dataclass(frozen=True, eq=False)
class H1Tape:
    """The native 1h tape, CLOSED at the TC11 pin (tierc10_data.load_asof)."""
    sym: str
    open_ms: np.ndarray
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    source: str = "stage-d"

    def close_ms(self, k: int) -> int:
        return int(self.open_ms[k]) + MS_1H


_H1: dict[str, H1Tape] = {}
_WALKS: dict[str, "Walk"] = {}


def h1_tape(sym: str) -> H1Tape:
    """Memoised in THIS module (never the lineage's bare-symbol frame memo)."""
    if sym not in _H1:
        df = D.load_asof(sym, "1h")
        t = df["open_time"].to_numpy(np.int64)
        if len(t) > 1 and bool((np.diff(t) <= 0).any()):
            raise SystemExit(f"HALT: {sym} 1h tape is not strictly ascending")
        _H1[sym] = H1Tape(sym, t, df["open"].to_numpy(float), df["high"].to_numpy(float),
                          df["low"].to_numpy(float), df["close"].to_numpy(float))
    return _H1[sym]


@dataclass(frozen=True, eq=False)
class Walk:
    """Per 4h bar of the asset's frame: first child index `a`, child count `n`,
    WALKABLE `ok` [L-W.0], and the reason for every bar that is not (`why`)."""
    sym: str
    h1: H1Tape
    open4: np.ndarray
    a: np.ndarray
    n: np.ndarray
    ok: np.ndarray
    why: dict


def child_mismatch(h1: H1Tape, a: int, n: int, open4: int, H: float, L: float,
                   C: float) -> str:
    """'' iff the bar's native 1h children number 4, sit on the 1h grid inside the
    parent, and reproduce its high, low and close to REPR_TOL; else the reason."""
    if n != N_1H:
        return f"{n} native 1h children, expected {N_1H}"
    t = h1.open_ms[a:a + N_1H]
    if int(t[0]) != int(open4) or not np.array_equal(
            np.diff(t), np.full(N_1H - 1, MS_1H, dtype=np.int64)):
        return "the children are not the 1h grid inside the parent bar"
    hh, ll, cc = float(h1.h[a:a + N_1H].max()), float(h1.l[a:a + N_1H].min()), \
        float(h1.c[a + N_1H - 1])
    if not same_px(hh, H):
        return f"4h high {float(H):.10g} not reproduced (1h max {hh:.10g})"
    if not same_px(ll, L):
        return f"4h low {float(L):.10g} not reproduced (1h min {ll:.10g})"
    if not same_px(cc, C):
        return f"4h close {float(C):.10g} not reproduced (last 1h close {cc:.10g})"
    return ""


def walk_of(sym: str, h1: H1Tape | None = None) -> Walk:
    """The walk law over the asset's whole 4h frame.  With `h1` given (a planted
    tape) nothing is memoised."""
    real = h1 is None
    if real and sym in _WALKS:
        return _WALKS[sym]
    f = T9.frame(sym)["f"]
    tape = h1_tape(sym) if real else h1
    o4 = np.asarray(f.open_ms, dtype=np.int64)
    a = np.searchsorted(tape.open_ms, o4, "left")
    b = np.searchsorted(tape.open_ms, o4 + MS_4H, "left")
    n = b - a
    ok = np.zeros(len(o4), dtype=bool)
    why = {}
    for j in range(len(o4)):
        w = child_mismatch(tape, int(a[j]), int(n[j]), int(o4[j]), f.h[j], f.l[j], f.c[j])
        if w:
            why[j] = w
        else:
            ok[j] = True
    W = Walk(sym, tape, o4, a.astype(np.int64), n.astype(np.int64), ok, why)
    if real:
        _WALKS[sym] = W
    return W


def walk_children(h1: H1Tape, k0: int, k1: int, d: int, entry_px: float, R: float,
                  stop: float, latched: bool, wctr, order=CHILD_ORDER) -> dict:
    """Walk 1h children k0..k1-1 in TAPE ORDER; per child the ops in `order`
    (CHILD_ORDER = STOP, LATCH, WARN).  Stops at the first exit.

    Returns the exit ('stop' | 'warn' | None) and its child, the child that
    LATCHED (walk law), the literal first +1R child (`plus1r_k`, stop or not),
    the tape's min adverse unit move over the walked children (`min_uadv`) and
    over those walked while not yet latched (`min_uadv_pre`, the latch child's
    own adverse counting as before — v6's mae_to_1r law), and the best
    favourable extreme of the children that were HELD (survived the stop)."""
    out = {"exit": None, "exit_k": None, "latch_k": None, "plus1r_k": None,
           "min_uadv": float("inf"), "min_uadv_pre": float("inf"), "best_fav": None}
    for k in range(int(k0), int(k1)):
        fav = float(h1.h[k]) if d == 1 else float(h1.l[k])
        adv = float(h1.l[k]) if d == 1 else float(h1.h[k])
        ufav = (fav - entry_px) * d / R
        uadv = (adv - entry_px) * d / R
        if out["plus1r_k"] is None and ufav >= 1.0:
            out["plus1r_k"] = k
        out["min_uadv"] = min(out["min_uadv"], uadv)
        if not latched:
            out["min_uadv_pre"] = min(out["min_uadv_pre"], uadv)
        for op in order:
            if op == "stop":
                if (d == 1 and float(h1.l[k]) <= stop) or (d == -1 and float(h1.h[k]) >= stop):
                    out["exit"], out["exit_k"] = "stop", k
                    break
            elif op == "latch":
                if not latched and ufav >= 1.0:
                    latched = True
                    out["latch_k"] = k
            elif op == "warn":
                if wctr is not None and not latched and bool(wctr[k]):
                    out["exit"], out["exit_k"] = "warn", k
                    break
            else:
                raise SystemExit(f"HALT: unknown child op {op!r}")
        if out["exit"] != "stop":
            bf = out["best_fav"]
            if bf is None or (fav - entry_px) * d > (bf - entry_px) * d:
                out["best_fav"] = fav
        if out["exit"] is not None:
            break
    return out


# ═══════════════════════════════════════════════════════════ THE HOOK INPUTS
@dataclass(frozen=True, eq=False)
class Warn:
    """1h cross arrays aligned to a Walk's h1 tape.  `up` = fast crosses OVER
    slow, `dn` = UNDER.  The counter cross of a long is `dn`."""
    up: np.ndarray
    dn: np.ndarray
    label: str = WARN_LABEL

    def counter(self, d: int) -> np.ndarray:
        return self.dn if d == 1 else self.up


def cross_1h(h1: H1Tape, fast: int, slow: int) -> tuple[np.ndarray, np.ndarray]:
    """(crossover, crossunder) of the engine EMA of the 1h close [L-W.2]."""
    ef, es = ind.ema(h1.c, int(fast)), ind.ema(h1.c, int(slow))
    return ind.crossover(ef, es), ind.crossunder(ef, es)


def warn_of(walk: Walk, fast: int = 12, slow: int = 89) -> Warn:
    up, dn = cross_1h(walk.h1, fast, slow)
    return Warn(up, dn, f"warn_1h_{int(fast)}_{int(slow)}")


@dataclass(frozen=True, eq=False)
class TPLevels:
    """Per 4h bar of the asset's frame (NaN = no level), from the CALLER [L-H.1]."""
    level_long: np.ndarray
    level_short: np.ndarray
    mode: str = "record"
    guard_bps: float = TP_GUARD_BPS


# ══════════════════════════════════════════════════════════════ THE STATE
def fresh_state(card, entry_px: float, stop0: float) -> dict:
    """v6's initial ride state (tierc9._ride_leg9's first lines)."""
    return {"stop": float(stop0), "advances": [], "harv": None, "blocked": "",
            "mfe": float(entry_px), "mae": 0.0, "mae_to_1r": 0.0, "reached_1r": False,
            "trail_armed": card.trail_arm_after_r <= 0.0, "h_armed": False, "n_opp": 0,
            "latch_1h_ms": None, "latch_1h_by": None, "plus1r_1h_ms": None,
            "mismatch_ms": []}


def carry_state(st: dict) -> dict:
    """L-T.2's carry: the whole state, copied (lists are not shared)."""
    missing = [k for k in STATE_KEYS if k not in st]
    if missing:
        raise SystemExit(f"HALT: a ride state lacks {missing}")
    out = {k: st[k] for k in STATE_KEYS}
    out["advances"] = list(st["advances"])
    out["mismatch_ms"] = list(st["mismatch_ms"])
    return out


# ═══════════════════════════════════════════════════════════════ THE RIDE
def _leg(entry_i, entry_px, stop0, exit_i, exit_px, exit_reason, st, *, exit_close_ms,
         exit_by, exit_child_ms, latch_on_stop_child, tpc, warn_label,
         exit_stamp_ms=None) -> dict:
    acted = []
    if warn_label is not None and exit_reason == warn_label:
        acted.append("warn")
    if exit_reason == TP_REASON:
        acted.append("tp")
    lms, lby = st["latch_1h_ms"], st["latch_1h_by"]
    latch_stamp = (None if lms is None
                   else int(lms) - MS_4H if lby == "parent" else int(lms))   # L-R.5
    return {"own_r": abs(float(entry_px) - float(stop0)), "entry_i": int(entry_i),
            "entry_px": float(entry_px), "stop0": float(stop0),
            "exit_i": int(exit_i), "exit_px": float(exit_px), "exit_reason": exit_reason,
            "advances": st["advances"], "harvest": st["harv"], "blocked": st["blocked"],
            "mfe": st["mfe"], "mae": st["mae"], "adds": [], "final_stop": st["stop"],
            "n_opportunities": st["n_opp"],
            "mae_to_1r": st["mae_to_1r"] if st["reached_1r"] else None,
            "reached_1r": st["reached_1r"],
            # ── TC11 ─────────────────────────────────────────────────────────
            "mae_to_1r_raw": st["mae_to_1r"], "exit_close_ms": exit_close_ms,
            "exit_resolved_by": exit_by, "exit_child_ms": exit_child_ms,
            "latch_1h_ms": st["latch_1h_ms"], "latch_1h_by": st["latch_1h_by"],
            "plus1r_1h_ms": st["plus1r_1h_ms"], "latch_on_stop_child": latch_on_stop_child,
            "latch_stamp_ms": latch_stamp, "exit_stamp_ms": exit_stamp_ms,
            "n_walk_mismatch": len(st["mismatch_ms"]),
            "walk_mismatch_ms": list(st["mismatch_ms"]), "tp_counts": dict(tpc),
            "acted_by": "+".join(acted)}


def _check_walk(walk: Walk, sym: str, f) -> None:
    if walk.sym != sym or len(walk.open4) != len(f.open_ms) \
            or not np.array_equal(walk.open4, np.asarray(f.open_ms, dtype=np.int64)):
        raise SystemExit(f"HALT: the Walk ({walk.sym}) is not built on {sym}'s 4h frame")


def ride11(sym, card, roles, d, ti, entry_px, stop0, r_dist, hi_i, *, walk=None,
           warn=None, tp=None, state=None, j0=None, exit_order=EXIT_ORDER,
           child_order=CHILD_ORDER, ctx=None) -> dict:
    """ONE CAMPAIGN'S RIDE.  walk/warn/tp None and state None == tierc9._ride_leg9.

    `state` (a `carry_state` dict) and `j0` (the first bar ridden, default ti+1)
    inject an initial state [L-T.2].  Returns _ride_leg9's dict plus the TC11
    keys (`_leg`).

    WHAT WOULD MAKE THIS WRONG: moving v6's top-of-bar latch below the stop
    test; deciding a mismatch bar on its children; resolving a stop at the 4h
    close; letting a child that stops also latch; reading a TP level or a warn
    cross the caller did not stamp causally (that is the caller's warranty —
    L-W.1, L-H.1 — never this function's)."""
    scope(card)
    if warn is not None and walk is None:
        raise SystemExit("HALT: the warn exit is a 1h rule; it needs the walk [L-W.5]")
    if warn is not None and tp is not None:
        raise SystemExit("HALT: no reading orders a 1h warn against a 4h TP; "
                         "one hook per book")
    if tp is not None and tp.mode not in TP_MODES:
        raise SystemExit(f"HALT: TP mode {tp.mode!r} not in {TP_MODES}")
    cx = ctx or ctx_of(sym, card, roles)
    f, ra, fr, s = cx["f"], cx["ra"], cx["fr"], cx["s"]
    om = f.open_ms
    if walk is not None:
        _check_walk(walk, sym, f)
    wctr = None
    if warn is not None:
        wctr = warn.counter(d)
        if len(wctr) != len(walk.h1.open_ms):
            raise SystemExit("HALT: the warn arrays are not aligned to the walk's 1h tape")
    if tp is not None and (len(tp.level_long) != len(om) or len(tp.level_short) != len(om)):
        raise SystemExit("HALT: the TP level arrays are not aligned to the 4h frame")
    warn_label = warn.label if warn is not None else None
    R = float(r_dist)
    entry_px = float(entry_px)
    st = fresh_state(card, entry_px, stop0) if state is None else carry_state(state)
    stop = float(st["stop"])
    advances, harv, blocked = st["advances"], st["harv"], st["blocked"]
    mfe, mae, mae_to_1r = st["mfe"], st["mae"], st["mae_to_1r"]
    reached_1r, trail_armed, h_armed = st["reached_1r"], st["trail_armed"], st["h_armed"]
    n_opp = st["n_opp"]
    latch_ms, latch_by, plus1r_ms = st["latch_1h_ms"], st["latch_1h_by"], st["plus1r_1h_ms"]
    mism = st["mismatch_ms"]
    bell_w = f"bell_{roles.win_f}_{roles.win_s}"
    bell_t = f"bell_{roles.tide_f}_{roles.tide_s}"
    exit_i, exit_px, exit_reason = hi_i, float(f.c[hi_i]), "corridor_end"
    exit_close_ms = (int(om[hi_i]) + MS_4H) if walk is not None else None
    exit_by = "close" if walk is not None else None
    exit_stamp = int(om[hi_i]) + MS_4H               # L-R.5: corridor_end is a close event
    exit_child_ms, latch_on_stop_child = None, False
    tpc = {"live": 0, "guard_withheld": 0, "far_side": 0, "preharvest_withheld": 0,
           "filled": 0, "fill_blocked_by_stop": 0}

    for j in range(ti + 1 if j0 is None else int(j0), hi_i + 1):
        close_j = int(om[j]) + MS_4H
        fav = float(f.h[j]) if d == 1 else float(f.l[j])
        adverse = float(f.l[j]) if d == 1 else float(f.h[j])
        ufav = (fav - entry_px) * d / R
        uadv = (adverse - entry_px) * d / R
        mae0, m1r0, reached0 = mae, mae_to_1r, reached_1r
        mae = min(mae, uadv)
        if not reached_1r:
            mae_to_1r = min(mae_to_1r, uadv)
            if ufav >= 1.0:
                reached_1r = True
        if not trail_armed and ufav >= card.trail_arm_after_r:
            trail_armed = True

        if card.harvest == "band":
            pe = RC.harvest_edge(float(ra["tide_f"][j - 1]),
                                 float(ra["tide_s"][j - 1]), d)
            if not h_armed and RC.harvest_outside(float(f.c[j - 1]), pe, d):
                h_armed = True
            edge = RC.harvest_edge(float(ra["tide_f"][j]),
                                   float(ra["tide_s"][j]), d)
            ufill = (float(f.c[j]) - entry_px) * d / R
            touch = (harv is None and h_armed
                     and RC.harvest_touched(float(f.h[j]), float(f.l[j]),
                                            edge, d)
                     and ufill >= card.harvest_min_unit_r)
        else:
            edge, touch = float("nan"), False

        parent_stop = bool((d == 1 and f.l[j] <= stop) or (d == -1 and f.h[j] >= stop))
        hits = {"stop": False, "warn": False, "tp": False, "bell": False}
        wk = None
        plus1r_before = plus1r_ms
        if walk is None:
            hits["stop"] = parent_stop
        elif walk.ok[j]:
            a = int(walk.a[j])
            wk = walk_children(walk.h1, a, a + N_1H, d, entry_px, R, stop,
                               latch_ms is not None, wctr, child_order)
            if plus1r_ms is None and wk["plus1r_k"] is not None:
                plus1r_ms = walk.h1.close_ms(wk["plus1r_k"])
            if latch_ms is None and wk["latch_k"] is not None:
                latch_ms, latch_by = walk.h1.close_ms(wk["latch_k"]), "1h"
            if wk["exit"] is None and parent_stop:
                raise SystemExit(
                    f"HALT: L-W.3 — {sym} 4h bar {T9.iso(int(om[j]))} is a stop-exit bar "
                    f"on a WALKABLE bar and no 1h child touches the stop {stop!r}")
            if wk["exit"] == "stop" and not parent_stop:
                raise SystemExit(
                    f"HALT: L-W.3 — {sym} 4h bar {T9.iso(int(om[j]))}: a 1h child touches "
                    f"the stop {stop!r} and the walkable parent does not")
            hits["stop"] = wk["exit"] == "stop"
            hits["warn"] = wk["exit"] == "warn"
        else:
            mism.append(int(om[j]))
            if plus1r_ms is None and ufav >= 1.0:
                plus1r_ms = close_j
            if latch_ms is None and ufav >= 1.0:          # v6: the top of the bar
                latch_ms, latch_by = close_j, "parent"
            hits["stop"] = parent_stop
            if wctr is not None and latch_ms is None:
                a, n = int(walk.a[j]), int(walk.n[j])
                hits["warn"] = bool(n > 0 and np.any(wctr[a:a + n]))

        tp_fill = None
        if tp is not None:
            lvl = float(tp.level_long[j] if d == 1 else tp.level_short[j])
            if np.isfinite(lvl):
                near = (lvl - float(f.c[j - 1])) * d > 0.0
                guard_ok = (lvl - entry_px) * d > tp.guard_bps / 10_000.0 * entry_px
                post_ok = harv is not None
                if not near:
                    tpc["far_side"] += 1
                elif not guard_ok:
                    tpc["guard_withheld"] += 1
                elif tp.mode == "post_harvest" and not post_ok:
                    tpc["preharvest_withheld"] += 1
                live = (near and (guard_ok or tp.mode == "unguarded")
                        and (post_ok or tp.mode != "post_harvest"))
                if live:
                    tpc["live"] += 1
                    if (d == 1 and float(f.h[j]) >= lvl) or (d == -1 and float(f.l[j]) <= lvl):
                        tp_fill = (max(lvl, float(f.o[j])) if d == 1
                                   else min(lvl, float(f.o[j])))
                        hits["tp"] = True

        bell = (((bell_w if bool(ra["w_dn"][j])
                  else bell_t if bool(ra["b_dn"][j]) else None)) if d == 1
                else ((bell_w if bool(ra["w_up"][j])
                       else bell_t if bool(ra["b_up"][j]) else None)))
        hits["bell"] = bell is not None
        winner = next((x for x in exit_order if hits[x]), None)

        if winner == "stop":
            exit_i, exit_px, exit_reason = j, stop, "stop"
            exit_stamp = int(om[j])                  # L-R.5: intrabar -> the bar's OPEN ...
            if touch:
                blocked = "stop"
            if tp_fill is not None:
                tpc["fill_blocked_by_stop"] += 1
            if wk is not None:
                exit_child_ms = walk.h1.close_ms(wk["exit_k"])
                exit_close_ms, exit_by = exit_child_ms, "1h"
                exit_stamp = exit_child_ms           # ... or the resolving child's close
                latch_on_stop_child = bool(plus1r_before is None
                                           and wk["plus1r_k"] == wk["exit_k"])
            elif walk is not None:
                exit_close_ms, exit_by = close_j, "parent"
            break
        if winner == "warn":
            exit_i, exit_reason = j, warn_label
            if wk is not None:                       # left at child k: the HELD law
                k = wk["exit_k"]
                exit_px = float(walk.h1.c[k])
                exit_child_ms = walk.h1.close_ms(k)
                exit_close_ms, exit_by = exit_child_ms, "1h"
                mae = min(mae0, wk["min_uadv"])
                mae_to_1r = m1r0 if reached0 else min(m1r0, wk["min_uadv"])
                reached_1r = reached0
                bf = wk["best_fav"]
                if bf is not None and (bf - entry_px) * d > (mfe - entry_px) * d:
                    mfe = bf
            else:                                    # mismatch: the parent's close
                exit_px = float(f.c[j])
                exit_close_ms, exit_by = close_j, "parent"
                if (fav - entry_px) * d > (mfe - entry_px) * d:
                    mfe = fav
            exit_stamp = exit_close_ms               # L-R.5: a close event
            if touch:
                blocked = "warn"
            break
        if winner == "tp":
            exit_i, exit_px, exit_reason = j, float(tp_fill), TP_REASON
            exit_stamp = int(om[j])                  # L-R.5: intrabar -> the bar's OPEN ...
            tpc["filled"] += 1
            if (tp_fill - entry_px) * d > (mfe - entry_px) * d:
                mfe = float(tp_fill)
            if touch:
                blocked = "tp"
            if walk is not None:
                lvl = float(tp.level_long[j] if d == 1 else tp.level_short[j])
                if walk.ok[j]:
                    a = int(walk.a[j])
                    fk = [k for k in range(a, a + N_1H)
                          if (d == 1 and float(walk.h1.h[k]) >= lvl)
                          or (d == -1 and float(walk.h1.l[k]) <= lvl)]
                    if not fk:
                        raise SystemExit(
                            f"HALT: L-W.3 (TP) — {sym} 4h bar {T9.iso(int(om[j]))} fills the "
                            f"TP {lvl!r} on a WALKABLE bar and no 1h child reaches it")
                    exit_child_ms = walk.h1.close_ms(fk[0])
                    exit_close_ms, exit_by = exit_child_ms, "1h"
                    exit_stamp = exit_child_ms       # ... or the resolving child's close
                else:
                    exit_close_ms, exit_by = close_j, "parent"
            break
        if (fav - entry_px) * d > (mfe - entry_px) * d:
            mfe = fav
        if winner == "bell":
            exit_i, exit_px, exit_reason = j, float(f.c[j]), bell
            exit_stamp = close_j                     # L-R.5: a close event
            if touch:
                blocked = "bell"
            if walk is not None:
                exit_close_ms, exit_by = close_j, "close"
            break
        if touch:
            harv = (j, RC.harvest_fill_px(f.c[j]),
                    (RC.harvest_fill_px(f.c[j]) - entry_px) * d / R)
        if card.trail and trail_armed:
            adv, opp = T8.matched_step(fr, j, d, stop, float(f.c[j]),
                                       float(f.atr[j]), s, card.anchor_kind,
                                       card.anchor_offset, f.open_ms,
                                       min_advance_atr=card.trail_min_advance_atr)
            n_opp += int(opp)
            if adv is not None:
                advances.append(adv)
                stop = float(adv.new_stop)

    out_st = {"stop": stop, "advances": advances, "harv": harv, "blocked": blocked,
              "mfe": mfe, "mae": mae, "mae_to_1r": mae_to_1r, "reached_1r": reached_1r,
              "trail_armed": trail_armed, "h_armed": h_armed, "n_opp": n_opp,
              "latch_1h_ms": latch_ms, "latch_1h_by": latch_by, "plus1r_1h_ms": plus1r_ms,
              "mismatch_ms": mism}
    return _leg(ti, entry_px, stop0, exit_i, exit_px, exit_reason, out_st,
                exit_close_ms=exit_close_ms, exit_by=exit_by, exit_child_ms=exit_child_ms,
                latch_on_stop_child=latch_on_stop_child, tpc=tpc, warn_label=warn_label,
                exit_stamp_ms=exit_stamp)


def account11(sym: str, card, d: int, r_dist: float, leg: dict) -> dict:
    """tierc7._account_chain on a one-leg chain (fees, funding, the D12 ceiling
    ONCE on the total, adds booked at the leg's exit price)."""
    return T7._account_chain(sym, card, d, r_dist,
                             {"legs": [leg], "n_reentries": 0, "reentry_refused": ""})


# ═════════════════════════════════════════════════════════════ THE RELAY
def relay_entry(sym: str, entry_close_ms: int, walk: Walk | None = None,
                trigger_close_ms: int | None = None) -> dict:
    """Resolve a relay's 1h-close entry instant under L-W.0 (see the docstring).
    With `trigger_close_ms` (the window's v6 4h trigger close), `refused` names
    an entry whose RESOLVED instant is not strictly before it [L-T.2 / L-T.3];
    else `refused` is None.  Refusing is the runner's act (a miss)."""
    W = walk or walk_of(sym)
    f = T9.frame(sym)["f"]
    _check_walk(W, sym, f)
    t = int(entry_close_ms)
    if t % MS_1H:
        raise SystemExit(f"HALT: relay entry {t} is not a 1h close")
    om = np.asarray(f.open_ms, dtype=np.int64)
    J = int(np.searchsorted(om, t, "left")) - 1
    if J < 0 or not (int(om[J]) < t <= int(om[J]) + MS_4H):
        raise SystemExit(f"HALT: relay entry {T9.iso(t)} lies in no 4h bar of {sym}")
    close_J = int(om[J]) + MS_4H
    if t == close_J:
        out = {"J": J, "kind": "4h-close", "entry_close_ms": t, "entry_px": float(f.c[J]),
               "asof_i": J, "moved": False, "child_k": None}
    elif not W.ok[J]:
        out = {"J": J, "kind": "parent-close (L-W.0 mismatch)", "entry_close_ms": close_J,
               "entry_px": float(f.c[J]), "asof_i": J, "moved": True, "child_k": None,
               "why": W.why.get(J, "")}
    else:
        k = int(W.a[J]) + (t - int(om[J])) // MS_1H - 1
        if W.h1.close_ms(k) != t:
            raise SystemExit(f"HALT: relay entry {T9.iso(t)}: child {k} does not close there")
        out = {"J": J, "kind": "1h", "entry_close_ms": t, "entry_px": float(W.h1.c[k]),
               "asof_i": J - 1, "moved": False, "child_k": k}
    out["refused"] = None
    if trigger_close_ms is not None and out["entry_close_ms"] >= int(trigger_close_ms):
        out["refused"] = (f"resolved entry {T9.iso(out['entry_close_ms'])} is not strictly "
                          f"before the 4h trigger close {T9.iso(int(trigger_close_ms))} "
                          f"[L-T.2/L-T.3]" + (" — moved there by L-W.0" if out["moved"] else ""))
    return out


def relay_stop(sym: str, asof_i: int, entry_px: float, d: int, card):
    """struct_stop_4h, pivots confirmed and ATR(4h) as of the last CLOSED 4h bar
    at the entry instant (`asof_i`), railed card.entry_rail_atr ATR [L-T.2].
    Returns (Stop | None, atr_sig)."""
    st = T9.frame(sym)
    atr_sig = float(st["f"].atr[asof_i])
    if not (np.isfinite(atr_sig) and atr_sig > 0):
        return None, atr_sig
    stp = RC.struct_stop_4h(st["pv4"], int(asof_i), float(entry_px), int(d), atr_sig,
                            min_stop_atr=card.entry_rail_atr, forbidden=None)
    if stp is None or not (np.isfinite(stp.r_dist) and stp.r_dist > 0):
        return None, atr_sig
    return stp, atr_sig


def relay11(sym, card, roles, d, entry_close_ms, entry_px, stop0, r_dist, hi_i, *,
            walk=None, carry=carry_state, child_order=CHILD_ORDER, ctx=None,
            walk_after=False, moved=False) -> dict:
    """THE RELAY RIDE [L-T.2].  An entry at a 4h close is ride11 from the next
    bar on a fresh state (== _ride_leg9).  An entry strictly inside a WALKABLE
    bar J: J's post-entry children (STOP -> LATCH), then J's close slot (BELL,
    HARVEST armed per close[J-1] with the touch on the post-entry children,
    TRAIL armed iff the latch fired), then ride11 from J+1 on `carry(state)`.
    A 1h entry inside a mismatch bar HALTs: L-W.0 takes it at the parent's
    close, and `relay_entry` says so before any ride; pass that resolution's
    `moved=True` so the mismatch bar J is COUNTED (n_walk_mismatch) [L-W.0].
    `walk_after` walks J+1.. on 1h (to resolve the exit instant); the ride after
    J is v6's either way."""
    scope(card)
    if card.trail_arm_after_r != 1.0:
        raise SystemExit("HALT: L-T.2 arms the trail iff the +1R latch fired; a card "
                         f"arming at {card.trail_arm_after_r} R is not that reading")
    cx = ctx or ctx_of(sym, card, roles)
    f, ra, fr, s = cx["f"], cx["ra"], cx["fr"], cx["s"]
    om = np.asarray(f.open_ms, dtype=np.int64)
    W = walk or walk_of(sym)
    _check_walk(W, sym, f)
    t = int(entry_close_ms)
    if t % MS_1H:
        raise SystemExit(f"HALT: relay entry {t} is not a 1h close")
    J = int(np.searchsorted(om, t, "left")) - 1
    if J < 1 or not (int(om[J]) < t <= int(om[J]) + MS_4H) or J > hi_i:
        raise SystemExit(f"HALT: relay entry {T9.iso(t)} lies in no ridable 4h bar")
    after = W if walk_after else None
    if moved and (t != int(om[J]) + MS_4H or bool(W.ok[J])):
        raise SystemExit(f"HALT: relay entry {T9.iso(t)} flagged moved, but it is not the "
                         f"close of a MISMATCH 4h bar [L-W.0]")
    if t == int(om[J]) + MS_4H:
        leg = ride11(sym, card, roles, d, J, entry_px, stop0, r_dist, hi_i, walk=after,
                     child_order=child_order, ctx=cx)
        leg.update(relay_path="4h-close", relay_J=J, entry_close_ms=t, state_after_J=None)
        if moved:                                  # L-W.0: the bar is counted per book
            leg["walk_mismatch_ms"] = [int(om[J])] + list(leg["walk_mismatch_ms"])
            leg["n_walk_mismatch"] = len(leg["walk_mismatch_ms"])
            leg["relay_path"] = "4h-close (moved: L-W.0 mismatch)"
        return leg
    if not W.ok[J]:
        raise SystemExit(f"HALT: relay entry {T9.iso(t)} lies inside a MISMATCH 4h bar "
                         f"({W.why.get(J, '')}); L-W.0 takes it at the parent's close — "
                         f"resolve it with relay_entry() first")
    R, entry_px = float(r_dist), float(entry_px)
    st = fresh_state(card, entry_px, stop0)
    a = int(W.a[J])
    k_e = a + (t - int(om[J])) // MS_1H - 1
    if W.h1.close_ms(k_e) != t:
        raise SystemExit(f"HALT: relay entry {T9.iso(t)}: child {k_e} does not close there")
    wk = walk_children(W.h1, k_e + 1, a + N_1H, d, entry_px, R, st["stop"], False, None,
                       child_order)
    st["mae"] = min(st["mae"], wk["min_uadv"])
    st["mae_to_1r"] = min(st["mae_to_1r"], wk["min_uadv_pre"])
    if wk["plus1r_k"] is not None:
        st["plus1r_1h_ms"] = W.h1.close_ms(wk["plus1r_k"])
    if wk["latch_k"] is not None:
        st["reached_1r"] = True
        st["latch_1h_ms"], st["latch_1h_by"] = W.h1.close_ms(wk["latch_k"]), "1h"
        st["trail_armed"] = True                      # armed iff the latch fired
    bf = wk["best_fav"]
    if bf is not None and (bf - entry_px) * d > (st["mfe"] - entry_px) * d:
        st["mfe"] = bf
    post = slice(k_e + 1, a + N_1H)
    hi_post, lo_post = float(W.h1.h[post].max()), float(W.h1.l[post].min())
    pe = RC.harvest_edge(float(ra["tide_f"][J - 1]), float(ra["tide_s"][J - 1]), d)
    if not st["h_armed"] and RC.harvest_outside(float(f.c[J - 1]), pe, d):
        st["h_armed"] = True
    edge = RC.harvest_edge(float(ra["tide_f"][J]), float(ra["tide_s"][J]), d)
    ufill = (float(f.c[J]) - entry_px) * d / R
    touch = (st["harv"] is None and st["h_armed"]
             and RC.harvest_touched(hi_post, lo_post, edge, d)
             and ufill >= card.harvest_min_unit_r)
    tpc = {"live": 0, "guard_withheld": 0, "far_side": 0, "preharvest_withheld": 0,
           "filled": 0, "fill_blocked_by_stop": 0}
    close_J = int(om[J]) + MS_4H

    def done(exit_px, reason, exit_close, by, child_ms) -> dict:
        leg = _leg(J, entry_px, stop0, J, exit_px, reason, st, exit_close_ms=exit_close,
                   exit_by=by, exit_child_ms=child_ms, latch_on_stop_child=bool(
                       reason == "stop" and wk["plus1r_k"] is not None
                       and wk["plus1r_k"] == wk["exit_k"]), tpc=tpc, warn_label=None,
                   exit_stamp_ms=exit_close)       # L-R.5: the stop child / J's close
        leg.update(relay_path="1h", relay_J=J, entry_close_ms=t, state_after_J=None)
        return leg

    if wk["exit"] == "stop":
        if touch:
            st["blocked"] = "stop"
        cm = W.h1.close_ms(wk["exit_k"])
        return done(st["stop"], "stop", cm, "1h", cm)
    bell = (((f"bell_{roles.win_f}_{roles.win_s}" if bool(ra["w_dn"][J])
              else f"bell_{roles.tide_f}_{roles.tide_s}" if bool(ra["b_dn"][J]) else None))
            if d == 1 else
            ((f"bell_{roles.win_f}_{roles.win_s}" if bool(ra["w_up"][J])
              else f"bell_{roles.tide_f}_{roles.tide_s}" if bool(ra["b_up"][J]) else None)))
    if bell:
        if touch:
            st["blocked"] = "bell"
        return done(float(f.c[J]), bell, close_J, "close", None)
    if touch:
        st["harv"] = (J, RC.harvest_fill_px(f.c[J]),
                      (RC.harvest_fill_px(f.c[J]) - entry_px) * d / R)
    if card.trail and st["trail_armed"]:
        adv, opp = T8.matched_step(fr, J, d, st["stop"], float(f.c[J]), float(f.atr[J]), s,
                                   card.anchor_kind, card.anchor_offset, f.open_ms,
                                   min_advance_atr=card.trail_min_advance_atr)
        st["n_opp"] += int(opp)
        if adv is not None:
            st["advances"].append(adv)
            st["stop"] = float(adv.new_stop)
    if J >= hi_i:
        return done(float(f.c[J]), "corridor_end", close_J, "close", None)
    stJ = carry(st)
    snap = carry_state(stJ)
    leg = ride11(sym, card, roles, d, J, entry_px, stop0, r_dist, hi_i, walk=after,
                 state=stJ, j0=J + 1, child_order=child_order, ctx=cx)
    leg.update(relay_path="1h", relay_J=J, entry_close_ms=t, state_after_J=snap)
    return leg


# ═══════════════════════════════════════════════════════════════ THE ADDS
def admit_adds(leg: dict, events, *, sym: str, d: int, entry_px: float,
               entry_close_ms: int, walk: Walk, max_adds: int = ADDS_MAX,
               size: float = ADD_SIZE, refuse_below_entry: bool = False,
               refuse_post_harvest: bool = False) -> tuple[list, list[dict]]:
    """L-A.1: at most `max_adds` of the caller's (1h close ms, price) events, in
    time order, IN-TRADE and AFTER the 1h latch.  Returns (adds, dispositions).
    The price is the TAPE's 1h close at the event instant (`price` None = take
    it; any other caller price must equal it exactly, else HALT).  The leg must
    come from a walked ride (it carries the 1h-resolved exit and the 1h latch)."""
    if leg.get("exit_close_ms") is None:
        raise SystemExit("HALT: adds need the 1h-resolved exit — ride with walk= [L-A.1]")
    f = T9.frame(sym)["f"]
    _check_walk(walk, sym, f)
    om = np.asarray(f.open_ms, dtype=np.int64)
    h1 = walk.h1
    x_ms, latch = int(leg["exit_close_ms"]), leg.get("latch_1h_ms")
    h_i = leg["harvest"][0] if leg["harvest"] is not None else None
    evs = sorted(((int(ms), None if px is None else float(px), n)
                  for n, (ms, px) in enumerate(events)), key=lambda e: (e[0], e[2]))
    adds, disp = [], []
    for ms, px, n in evs:
        if ms % MS_1H:
            raise SystemExit(f"HALT: add event {ms} is not a 1h close")
        i = int(np.searchsorted(om, ms, "left")) - 1
        if i < 0 or not (int(om[i]) < ms <= int(om[i]) + MS_4H):
            raise SystemExit(f"HALT: add event {T9.iso(ms)} lies in no 4h bar")
        k = int(np.searchsorted(h1.open_ms, ms - MS_1H, "left"))
        has_k = k < len(h1.open_ms) and int(h1.open_ms[k]) == ms - MS_1H
        px_1h = float(h1.c[k]) if has_k else None
        if px is not None and (px_1h is None or px != px_1h):
            raise SystemExit(f"HALT: add event {T9.iso(ms)} price {px!r} is not the 1h close of "
                             f"its triggering event ({px_1h!r}) [L-A.1]")
        moved = not bool(walk.ok[i])
        if not moved and px_1h is None:
            raise SystemExit(f"HALT: add event {T9.iso(ms)}: no 1h bar closes there on a "
                             f"walkable 4h bar")
        t_eff, p_eff = (int(om[i]) + MS_4H, float(f.c[i])) if moved else (ms, px_1h)
        row = {"event": n, "event_ms": ms, "event_px": px_1h, "ms": t_eff, "px": p_eff, "i": i,
               "moved_to_parent_close": moved, "below_entry": bool((p_eff - entry_px) * d < 0),
               "post_harvest": bool(h_i is not None and i >= h_i)}
        if t_eff <= int(entry_close_ms):
            row["disposition"] = "refused: pre-entry"
        elif t_eff >= x_ms:
            row["disposition"] = "refused: not before the 1h-resolved exit"
        elif latch is None or t_eff < int(latch):
            row["disposition"] = "refused: before the +1R latch"
        elif refuse_below_entry and row["below_entry"]:
            row["disposition"] = "refused: below entry (twin)"
        elif refuse_post_harvest and row["post_harvest"]:
            row["disposition"] = "refused: post-harvest (twin)"
        elif len(adds) >= int(max_adds):
            row["disposition"] = f"refused: cap {int(max_adds)} reached"
        else:
            row["disposition"] = "admitted"
            adds.append(RC.Add(i=i, ms=t_eff, px=p_eff, size=float(size),
                               retrace_i=-1, retrace_ms=-1))
        disp.append(row)
    return adds, disp


# ═════════════════════════════════════════════════ THE TRADE, AS replay9 BUILDS IT
def trade11(sym, card, roles, d, *, arm_i, arm_ms, disp, entry_i, entry_ms, entry_px,
            stp, atr_sig, leg, lane: str = "card", entry_close_ms=None):
    """tierc9.replay9's Trade construction, verbatim, plus the TC11 extras."""
    f = T9.frame(sym)["f"]
    acc = account11(sym, card, d, stp.r_dist, leg)
    harv = leg["harvest"]
    t = RC.Trade(
        symbol=sym, lane=lane, direction=d,
        arm_i=arm_i, arm_ms=arm_ms, entry_i=entry_i,
        entry_ms=int(entry_ms), entry_px=entry_px,
        stop_px=stp.stop_px, r_dist=stp.r_dist, anchor=stp.anchor,
        anchor_bar_ms=(int(f.open_ms[stp.anchor_bar])
                       if stp.anchor_bar >= 0 else -1),
        anchor_was_sealed=bool(
            stp.anchor_bar >= 0
            and T9._ms(RC.LOCKBOX_WAS[0])
            <= int(f.open_ms[stp.anchor_bar])
            <= T9._ms(RC.LOCKBOX_WAS[1]) + 86_400_000 - 1),
        atr_at_entry=atr_sig,
        disp_at_arming=disp,
        exit_i=leg["exit_i"], exit_ms=int(f.open_ms[leg["exit_i"]]),
        exit_px=leg["exit_px"], exit_reason=leg["exit_reason"],
        bars_held=leg["exit_i"] - entry_i, scored=True,
        advances=list(leg["advances"]),
        final_stop_px=leg["final_stop"],
        stop_advanced_atr=(leg["final_stop"] - leg["stop0"]) * d / atr_sig,
        ratchet_exit=bool(leg["exit_reason"] == "stop" and leg["advances"]
                          and abs(leg["final_stop"] - leg["stop0"]) > 1e-12),
        harvested=harv is not None,
        harvest_i=(harv[0] if harv else None),
        harvest_ms=(int(f.open_ms[harv[0]]) if harv else None),
        harvest_px=(harv[1] if harv else None),
        harvest_unit_move_r=(harv[2] if harv else None),
        harvest_blocked_by=leg["blocked"],
        harvest_ride_would_have_r=acc["harvest_ride_would_have_r"],
        adds=list(leg["adds"]), add_r=acc["add_r"], spring=None,
        mfe_r=(leg["mfe"] - entry_px) * d / stp.r_dist,
        mae_to_1r_r=leg["mae_to_1r"], reached_1r=leg["reached_1r"],
        gross_r=acc["gross_r"], fee_r=acc["fee_r"],
        funding_r=acc["funding_r"],
        funding_r_uncapped=acc["funding_r_uncapped"],
        funding_ceiling_bound=acc["funding_ceiling_bound"],
        net_r=acc["net_r"], net_r_harvest_half=acc["n1"],
        net_r_runner_half=acc["n2"], net_r_bellonly=None)
    acted = [x for x in leg["acted_by"].split("+") if x]
    if leg["adds"]:
        acted.append("adds")
    extras = {"mae_r": leg["mae"], "n_opportunities": leg["n_opportunities"],
              "roles_name": roles.name,
              "entry_close_ms": (int(entry_close_ms) if entry_close_ms is not None
                                 else int(f.open_ms[entry_i]) + MS_4H),
              "exit_close_ms": leg["exit_close_ms"], "exit_resolved_by": leg["exit_resolved_by"],
              "exit_child_ms": leg["exit_child_ms"], "latch_1h_ms": leg["latch_1h_ms"],
              "latch_1h_by": leg["latch_1h_by"], "plus1r_1h_ms": leg["plus1r_1h_ms"],
              "latch_on_stop_child": leg["latch_on_stop_child"],
              "latch_stamp_ms": leg["latch_stamp_ms"], "exit_stamp_ms": leg["exit_stamp_ms"],
              "n_walk_mismatch": leg["n_walk_mismatch"],
              "walk_mismatch_ms": leg["walk_mismatch_ms"], "tp_counts": leg["tp_counts"],
              "acted_by": "+".join(acted),
              "n_adds_below_entry": sum(1 for a in leg["adds"] if (a.px - entry_px) * d < 0),
              "n_adds_post_harvest": sum(1 for a in leg["adds"]
                                         if harv is not None and a.i >= harv[0]),
              "relay_path": leg.get("relay_path")}
    for k, v in extras.items():
        object.__setattr__(t, k, v)
    return t


# ═══════════════════════════════════════ L-1.5 · THE v6 SET, REBUILT AND TRANSFORMED
@dataclass(frozen=True)
class CampaignInput:
    """One v6 campaign's inputs, rebuilt from the book (arm, entry, stop, R, the
    corridor edge) — same entries, never re-admitted [L-1.5]."""
    symbol: str
    direction: int
    lane: str
    arm_i: int
    arm_ms: int
    disp: float
    ti: int
    entry_ms: int
    entry_px: float
    stop: object
    atr_sig: float
    hi_i: int
    roles_name: str

    @property
    def key(self) -> tuple:
        return (self.symbol, int(self.entry_ms))

    @property
    def entry_close_ms(self) -> int:
        return int(self.entry_ms) + MS_4H

    def role_arrays(self, roles) -> dict:
        """The campaign's role arrays (six EMAs + crosses), from the lineage memo."""
        if roles.name != self.roles_name:
            raise SystemExit(f"HALT: roles {roles.name!r} are not the book's "
                             f"{self.roles_name!r}")
        return T9.role_arrays(self.symbol, roles)


def v6_inputs(book, card, roles, lo_ms: int, hi_ms: int) -> list[CampaignInput]:
    """Rebuild every campaign's inputs from a v6 book.  The entry must be the
    trigger bar's close and the stop must re-derive EXACTLY through
    struct_stop_4h at the entry bar — a book that is not card v6's HALTs here.
    `roles` is the card's role stack: its arrays are `T9.role_arrays(sym, roles)`."""
    scope(card)
    out = []
    for t in book:
        st = T9.frame(t.symbol)
        f = st["f"]
        _, hi_i = T7._idx_range(f.open_ms, lo_ms, hi_ms)
        ti, d = int(t.entry_i), int(t.direction)
        e = float(f.c[ti])
        atr_sig = float(f.atr[ti])
        stp = RC.struct_stop_4h(st["pv4"], ti, e, d, atr_sig,
                                min_stop_atr=card.entry_rail_atr, forbidden=None)
        why = []
        if t.lane != "card":
            why.append(f"lane {t.lane!r}")
        if int(f.open_ms[ti]) != int(t.entry_ms):
            why.append("entry_ms is not the entry bar's open")
        if e != float(t.entry_px):
            why.append(f"entry_px {t.entry_px!r} != close[ti] {e!r}")
        if stp is None or stp.stop_px != float(t.stop_px) or stp.r_dist != float(t.r_dist):
            why.append(f"stop {t.stop_px!r}/{t.r_dist!r} does not re-derive "
                       f"({None if stp is None else (stp.stop_px, stp.r_dist)})")
        if atr_sig != float(t.atr_at_entry):
            why.append("atr_at_entry differs")
        if getattr(t, "roles_name", roles.name) != roles.name:
            why.append(f"roles {getattr(t, 'roles_name', None)!r} != {roles.name!r}")
        if int(t.exit_i) > hi_i:
            why.append("exit beyond the corridor edge")
        if why:
            raise SystemExit(f"HALT: v6_inputs — {t.symbol} {T9.iso(int(t.entry_ms))} is not "
                             f"a v6 campaign of this card/corridor: {why}")
        out.append(CampaignInput(t.symbol, d, t.lane, int(t.arm_i), int(t.arm_ms),
                                 float(t.disp_at_arming), ti, int(t.entry_ms), e, stp,
                                 atr_sig, int(hi_i), roles.name))
    return out


def ride_campaign(inp: CampaignInput, card, roles, *, walk=None, warn=None, tp=None,
                  add_events=None, add_opts=None, exit_order=EXIT_ORDER,
                  child_order=CHILD_ORDER, max_adds: int = ADDS_MAX):
    """One v6 campaign, transformed: ride11 with the hooks, adds admitted and
    booked, the Trade built as replay9 builds it."""
    leg = ride11(inp.symbol, card, roles, inp.direction, inp.ti, inp.entry_px,
                 inp.stop.stop_px, inp.stop.r_dist, inp.hi_i, walk=walk, warn=warn, tp=tp,
                 exit_order=exit_order, child_order=child_order)
    disp = []
    if add_events is not None:
        if walk is None:
            raise SystemExit("HALT: adds need the walk [L-A.1]")
        adds, disp = admit_adds(leg, add_events, sym=inp.symbol, d=inp.direction,
                                entry_px=inp.entry_px, entry_close_ms=inp.entry_close_ms,
                                walk=walk, max_adds=max_adds, **(add_opts or {}))
        leg["adds"] = adds
    t = trade11(inp.symbol, card, roles, inp.direction, arm_i=inp.arm_i, arm_ms=inp.arm_ms,
                disp=inp.disp, entry_i=inp.ti, entry_ms=inp.entry_ms, entry_px=inp.entry_px,
                stp=inp.stop, atr_sig=inp.atr_sig, leg=leg, lane=inp.lane)
    object.__setattr__(t, "add_dispositions", disp)
    return t


def transform_book(base, card, roles, lo_ms: int, hi_ms: int, *, walk=False,
                   warn_of=None, tp_of=None, adds_of=None, add_opts=None,
                   exit_order=EXIT_ORDER, child_order=CHILD_ORDER,
                   max_adds: int = ADDS_MAX) -> list:
    """THE v6 CAMPAIGN SET, TRANSFORMED [L-1.5]: every base campaign re-ridden on
    its own arm/entry/stop/R with the hooks; same keys, same order, nothing
    re-admitted into a freed slot.
      walk     False | True (the real walk per asset) | callable sym -> Walk
      warn_of  None | callable sym -> Warn          (needs the walk)
      tp_of    None | callable sym -> TPLevels
      adds_of  None | callable key -> [(1h close ms, px | None), ...] or None
    A `walk` that is neither a bool nor a callable (e.g. a Walk object, which is
    truthy) HALTs — it would otherwise silently ride the REAL walk."""
    if not (isinstance(walk, bool) or callable(walk)):
        raise SystemExit(f"HALT: transform_book(walk=) takes False | True | a callable "
                         f"sym -> Walk, not a {type(walk).__name__}")
    out = []
    for inp in v6_inputs(base, card, roles, lo_ms, hi_ms):
        s = inp.symbol
        W = (walk(s) if callable(walk) else walk_of(s) if walk else None)
        ev = adds_of(inp.key) if adds_of is not None else None
        out.append(ride_campaign(inp, card, roles, walk=W,
                                 warn=warn_of(s) if warn_of is not None else None,
                                 tp=tp_of(s) if tp_of is not None else None,
                                 add_events=ev, add_opts=add_opts, exit_order=exit_order,
                                 child_order=child_order, max_adds=max_adds))
    return out


def identity_findings(base, book) -> tuple[list[str], dict]:
    """THE IDENTITY LAW [L-1.5]: the book holds EXACTLY the base's keys; every
    campaign the rule never acted on (acted_by == '') carries the base's net_r,
    exit_ms and exit_reason at 0.000e+00; an adds-acted campaign keeps the v6
    leg (exit_ms, exit_px, exit_reason); an acted flag leaves a footprint."""
    kb = [(t.symbol, int(t.entry_ms)) for t in base]
    kn = [(t.symbol, int(t.entry_ms)) for t in book]
    out = []
    if len(set(kn)) != len(kn):
        out.append("IDENTITY: the book repeats a key")
    extra, missing = sorted(set(kn) - set(kb)), sorted(set(kb) - set(kn))
    if extra or missing:
        out.append(f"IDENTITY: key set differs — {len(extra)} admitted that v6 never took "
                   f"{extra[:3]}, {len(missing)} v6 campaigns missing {missing[:3]}")
    bm = {(t.symbol, int(t.entry_ms)): t for t in base}
    n_acted = n_un = 0
    worst = 0.0
    for t in book:
        k = (t.symbol, int(t.entry_ms))
        b = bm.get(k)
        if b is None:
            continue
        acted = getattr(t, "acted_by", None)
        if acted is None:
            out.append(f"IDENTITY {k}: no acted_by stamp — not a tierc11_ride campaign")
            continue
        if not acted:
            n_un += 1
            for col in ("net_r", "exit_ms"):
                dv = abs(float(getattr(t, col)) - float(getattr(b, col)))
                worst = max(worst, dv)
                if dv != 0.0:
                    out.append(f"IDENTITY {k[0]} {T9.iso(k[1])}: {col} differs by {dv:.3e} "
                               f"on a campaign the rule never acted on")
            if t.exit_reason != b.exit_reason:
                out.append(f"IDENTITY {k[0]} {T9.iso(k[1])}: exit_reason {t.exit_reason!r} "
                           f"!= v6 {b.exit_reason!r} on a campaign the rule never acted on")
        else:
            n_acted += 1
            if "adds" in acted.split("+"):
                for col in ("exit_ms", "exit_px"):
                    if float(getattr(t, col)) != float(getattr(b, col)):
                        out.append(f"IDENTITY {k[0]} {T9.iso(k[1])}: adds moved the v6 leg "
                                   f"({col})")
                if t.exit_reason != b.exit_reason:
                    out.append(f"IDENTITY {k[0]} {T9.iso(k[1])}: adds moved the v6 exit")
            if t.exit_reason == b.exit_reason and not t.adds:
                out.append(f"IDENTITY {k[0]} {T9.iso(k[1])}: acted_by {acted!r} but no "
                           f"footprint (same exit reason, no adds)")
    return out, {"n": len(book), "acted": n_acted, "unacted": n_un, "worst": worst}


# ════════════════════════════════════════════════════════════════════ SPEC
def spec_lines() -> list[str]:
    return [
        "TIER-C11 · tierc11_ride — the ride engine (a DECISION module; no range import)",
        f"  seed {SEED} · REPR_TOL {REPR_TOL:.0e} (tierc10_lanes) · 1h children per 4h bar {N_1H}",
        f"  EXIT_ORDER {EXIT_ORDER} (intrabar, adverse-first; BELL -> HARVEST -> TRAIL at the close)",
        f"  CHILD_ORDER {CHILD_ORDER} [L-W.5]",
        f"  ADDS_MAX {ADDS_MAX} · ADD_SIZE {ADD_SIZE} [L-A.1] · TP_GUARD_BPS {TP_GUARD_BPS} "
        f"(2 x FEE_BPS_SIDE {RC.FEE_BPS_SIDE}) [L-H.1] · TP modes {TP_MODES}",
        f"  CARRY_KEYS {CARRY_KEYS} [L-T.2]",
        "  SUB-READINGS [executor, disclosed]: (s1) warn exit: mae/mfe/mae_to_1r HELD through "
        "the warn child; (s2) TP exit bar: mfe capped at the fill; (s3) a relay stopped inside "
        "J: the stop CHILD is the stop unit (1h image of v6's stop-bar law) while ride11 keeps "
        "the 4h unit on walked bars; (s4) add twins refuse BEFORE the 2-add cap (a refused "
        "event spends no slot); (s5) add price = the tape's 1h close (a differing caller price "
        "HALTs)",
        "  L-R.5 stamps: exit_stamp_ms / latch_stamp_ms = the resolving 1h child's close, else "
        "the 4h bar's OPEN for an intrabar event decided by the parent; close events at their "
        "close; exit_close_ms / latch_1h_ms of a parent-decided event = the post-event twin",
        "  L-1.5 x L-A.1: when the D12 ceiling binds, net_r - v6 net_r != add_r (paired delta is "
        "scored on net_r) — AMENDMENT CANDIDATE on L-1.5's wording",
        "  L-W.0 disclosure: walkability of bar j reads all four children and the parent's "
        "H/L/C (later prices of the same 4h bar decide act-at-child vs defer-to-close)",
    ]


if __name__ == "__main__":
    sys.stdout.write("\n".join(spec_lines()) + "\n")
