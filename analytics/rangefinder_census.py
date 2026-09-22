"""SS12-RANGEFINDER · THE CENSUS PORT -- the range lifecycle as pure numpy.

TIER-C10 STAGE 0 (CENSUS-R, Tier-E, collared, no registrations).  The contract
asks for the RangeFinder "module-ized under analytics/ with pins frozen (STEP 0
sha)".  The machine of record lives in engine/rangefinder.py and stays there,
untouched: this file is a PORT of it, and a port is only worth the bytes it
reproduces.  The law that binds it is F-RF-EQ (scripts/tierc10_rf_fixtures.py):
on the frozen record tape the five event logs below must hash to the five shas
of record, and on two further tapes (ETHUSDT 4h full history, SOLUSDT 1d) every
event log, every Range field, every pivot and every summary number must equal
the machine's, byte for byte.  Identity is judged by sha, never by eye.

[LEAN-HEPHAESTUS] L3 analytics module = analytics/rangefinder_census.py: a PURE
numpy port (no engine import, no IO, ATR passed IN as an argument), NOT added
to analytics._MODULES (analytics_sha stays put) -- printed as a finding.

WHY A PORT AND NOT AN IMPORT -- four standing walls, one clean path:
  I-B / F-AN-3   nothing under analytics/ may import the engine package, and
                 the test globs EVERY file in this directory, listed or not.
  I-A / F-AN-4   no IO of any kind here: frames in, events out.
  F-BR-14        the machine's import closure may never reach `analytics`, and
                 no decision closure may reach a component named `rangefinder`.
                 This module's name is `rangefinder_census` -- one component,
                 not that one -- and nothing in a decision path imports it.
  I-D            warm-up honesty: an analytics function never seeds a number
                 into the warm-up region.  The machine's ATR is the engine's
                 Wilder RMA SEEDED AT TR[0] (finite from bar 0); this package's
                 own ATR is SMA-seeded with a NaN warm-up.  Computing the
                 former here would breach I-D; using the latter would move
                 every event sha.  So NO ATR IS COMPUTED HERE: the caller in
                 scripts/ computes it and hands it in, and ATR_LEN below
                 survives only as the ZigZag's warm floor.

NOT IN analytics._MODULES, ON PURPOSE, DISCLOSED: adding a file to that tuple
moves analytics_sha(), which every BRIEF capture prints, and I-F then demands a
version bump, an INTERFACE.md row and the INTERFACE_PUBLISHED sync.  A census
organ is not part of the brief's recipe.  The price is unhashed code inside
the package; the receipt is F-RF-EQ plus the sha the fixture prints.

THE PINS ARE FROZEN LITERALS, duplicated from the machine and asserted equal
to it AND to the Pine input defaults by F-RF-PINS.  STEP 0 of record
(2026-09-21, sha256 of the three files the pins were read from):
  pine/SS12_RangeFinder_v2.pine  4bed1e01189106c0339d0375a1049f2d9868d54c3644363a9436d43c7a14ddb6
  scripts/rangefinder_twin.py    7646b5762490e699f71193ad38f5e265103ca95fa3fc58b5cda6e5993f3772e9
  engine/rangefinder.py          bbae464fdc8e0e01fc90b286aa79e726fcff4422e6118dee1173f2460dab84d4
Pin of record 0.60 / 7 / 8, twin == Pine, no halt.  (Stage 0a then gave the
twin's two loaders an anchor keyword, so the twin's sha moved by that edit and
nothing else; the fixture proves "nothing else" against the STEP 0 blob.)

THE BASELINE OF RECORD -- sha256 of json.dumps(events, sort_keys=True) on the
FROZEN tape (BTCUSDT 4h, open_time <= 1787371200000 = 2026-08-22T04:00Z; the
last 1700 bars for v2, the last 420 complete UTC days for v1):
  v2 macro      92 events   2145418831a00be710fb401c3a7c16722c0857feda4a29d58d503f3dc2b09ed4
  v2 micro     573 events   73798d744a377d6f2398020b0ae891d2f34efab2e48fda1c0e745243e2b04c72
  v2 leash     153 events   824cdff43675053a54f5c2cbbec9ba8b87c2e3661fca20c00459880bd17ec54e
  v2 suppress   17 events   e7b0de6a072ea9ba0c5bb0b7dc2c0ebba72d68e2730b1e6056f26fa7189dba70
  v1 body      152 events   af2485e664bf822492e8bb86ef4c45afb05844bed5e342f4a9aa30588dba5404

THE QUIRKS ARE THE BYTES, carried over and not tidied: log() rounds every int
or float keyword to 2 dp THROUGH float() (so "p0_bar": 3.0, "closes": 8.0),
except rid/bars/count; event keys keep insertion order; pivots are logged
first and the list is then STABLE-sorted on "i"; leash px is 1 dp; _span_at
reads the ROUNDED "extreme" back; run_v2's "2026-02-01" is a BTC KEY-C literal.
One quirk needs its own line because it BITES downstream:
  knowable_at CAN READ -1.  The machine keys its seal lookup on
  round(np.float64, 2) -- numpy's rounding -- while log() rounded the same
  price with Python's.  The two disagree on some 3+ decimal prices, the lookup
  misses, and the pivot ships knowable_at = -1 (measured: 5 pivots on SOLUSDT
  1d; none on BTC, whose prices carry <= 2 dp).  A reader that trusts
  knowable_at would see such a pivot from bar 0 -- look-ahead.  The port
  reproduces the miss exactly (it must) and ALSO returns the truth beside it:
  out["seals"][k] is the bar pivot k became knowable at, never -1.
NEVER READ A PRICE FROM AN EVENT: read bar indices from events and prices from
the Range fields and the raw tape (full precision, scale-invariant).

WHAT IS DIFFERENT, AND WHY THE BYTES DO NOT MOVE -- the machine is O(n^2)
(four passes per bar over every range ever seeded; the leash walks every line
every bar); 5m full history is ~740k bars.  The port keeps the law and changes
only the bookkeeping:
  * POTENTIAL / CONFIRMED ranges are held in their own lists, in rid order --
    the order the machine's `for r in ranges` visits them -- so resolved
    ranges are never rescanned.
  * memory-line first touches come off two heaps (unfrozen dead tops by
    price, unfrozen dead bottoms by price); the bar's touches are re-sorted
    (rid, top-before-bottom) before they are logged, which is the machine's
    order.  A range that died on bar i enters the heaps after bar i's pass --
    the machine's `die_i == i` skip.
  * the seed's floor is a running max (every die_i / confirm_i is stamped with
    the current bar), and the terminal test scans only the visible pivots
    past it -- a suffix, because pivot bars rise in seal order (checked per
    run; if it ever failed the literal scan runs instead).
  * the leash finds the bar's touched lines by bisecting a price-sorted
    roster of born, unexpired lines, then visits them in line order; ttl
    expiry is a queue by birth bar; the cap phase keeps its own live lists.
  * _span_at reads a per-rid index of the two event kinds it looks at, and
    containment finds the parent by bisection when the confirmed macro lives
    are disjoint (ONE_ACTIVE guarantees it; otherwise the literal scan runs).
  * hot loops read Python lists, not numpy scalars.  Same IEEE doubles, same
    comparisons, same repr in the log.
ADDITIVE, never subtractive: run_machine also returns "seals" and "covered"
(the per-bar coverage mask the machine computes and drops).  `retests=False`
on the leash withholds the two per-bar spam classes (flip-retest, and the
"candidacy consumed" memory-retest) -- millions of dicts on a 5m tape -- and
the fixture proves the lean log equals the full log with those rows removed.
machine_known_at / leash_known_at return the bar each event is KNOWABLE at
(a pivot at its seal, a flip at its touch bar + FLIP_HOLD_BARS); F-RF-KNOWN
holds them to prefix-stability and shows the naive `i` filter failing it.

DISPLAY-ONLY · A MEASUREMENT ORGAN, like the machine it mirrors: it describes
structure on a tape and rules nothing.  TIER-C10's range-triggered cards are
research registrations under G-7; they read precomputed tables, never this.

RECONSTRUCTION, NOT CODE ACCESS: the semantics are rebuilt from the public
artifacts of a closed-source system (@sergio_tesla_, 2026-08-10 post + two
screenshots).  THE PINNED READINGS (SEED, CONFIRM, ONE ACTIVE RANGE, LATE
RETURN, CONSECUTIVE, COVERAGE, MERGE, BODY MODE, HARDEN, BACKDATE, SAME-BAR
TIE, CONTAINMENT, FLIP, LEASH) are the machine's and are stated once, in its
header; this file implements them and restates none.
"""

from bisect import bisect_left, bisect_right, insort
from dataclasses import dataclass
from heapq import heappop, heappush

import numpy as np

__all__ = ["ATR_LEN", "PINS", "PINS_V2", "V2_WINDOW_BARS", "MEM_CAP_PER_SIDE",
           "STEP0_SHA256", "EVENT_SHAS_OF_RECORD", "RECORD_ANCHOR_MS",
           "Range", "macro_pins", "run_machine", "span_at", "containment",
           "flips_and_leash", "run_v2", "machine_known_at", "leash_known_at"]

ATR_LEN = 14               # the ZigZag's warm floor ONLY -- the ATR itself is
                           # handed in (header, I-D); never swept

# THE CALIBRATED PINS [VETO], frozen literals.  Key order is export order.
PINS = {
    "LEG_MIN": 0.5,
    "REV_MIN": 1.75,
    "TOUCH_EPS": 0.60,
    "DEV_RETURN_BARS": 7,
    "BREAK_CONFIRM_N": 8,
    # at these pins breach-lapse is UNREACHABLE (BREAK_CONFIRM_N <=
    # DEV_RETURN_BARS + 1); the law stays implemented, as in the machine
    "BREAK_MARGIN": 1.5,
    "BOUNDARY_MODE": "body",
    "REDRAW_BASIS": "wick",
    "MULTI_ACTIVE": 0,
}

V2_WINDOW_BARS = 1700          # the Oracle's 4h window; CENSUS-R runs FULL
                               # history and says so beside every number
MEM_CAP_PER_SIDE = 6           # H3, commissioned

PINS_V2 = {
    "SCALE_MULT": 3.0,         # [LEAN-HEPHAESTUS] L2: every registered lane and
                               # every Stage-A stamp uses this FROZEN 3.0
    "FLIP_HOLD_MARGIN": 1.0,
    "FLIP_HOLD_BARS": 6,
    "MEM_TTL_BARS": 400,       # PROPOSED, adopted, not fitted [disclosed]
}

STEP0_SHA256 = {
    "pine/SS12_RangeFinder_v2.pine":
        "4bed1e01189106c0339d0375a1049f2d9868d54c3644363a9436d43c7a14ddb6",
    "scripts/rangefinder_twin.py":
        "7646b5762490e699f71193ad38f5e265103ca95fa3fc58b5cda6e5993f3772e9",
    "engine/rangefinder.py":
        "bbae464fdc8e0e01fc90b286aa79e726fcff4422e6118dee1173f2460dab84d4",
}

RECORD_ANCHOR_MS = 1_787_371_200_000       # 2026-08-22T04:00Z, last bar OPEN

EVENT_SHAS_OF_RECORD = {
    "v2_macro": (92, "2145418831a00be710fb401c3a7c16722c0857feda4a29d58d503f3dc2b09ed4"),
    "v2_micro": (573, "73798d744a377d6f2398020b0ae891d2f34efab2e48fda1c0e745243e2b04c72"),
    "v2_leash": (153, "824cdff43675053a54f5c2cbbec9ba8b87c2e3661fca20c00459880bd17ec54e"),
    "v2_suppress": (17, "e7b0de6a072ea9ba0c5bb0b7dc2c0ebba72d68e2730b1e6056f26fa7189dba70"),
    "v1_body": (152, "af2485e664bf822492e8bb86ef4c45afb05844bed5e342f4a9aa30588dba5404"),
}

_NAN = float("nan")


# ═══════════════════════════════════════════════════════ the machine
@dataclass
class Range:
    # field order IS the asdict() export order -- the machine's, verbatim
    rid: int
    top: float
    bottom: float
    top0: float            # original (pre-redraw) boundaries
    bottom0: float
    seed_i: int
    confirm_i: int = -1
    die_i: int = -1
    state: str = "POTENTIAL"        # POTENTIAL|CONFIRMED|DEAD|INVALIDATED|SUPERSEDED
    confirm_side: str = ""          # boundary touched at confirmation
    dev_top_ext: float = float("nan")     # furthest deviation extremes
    dev_bot_ext: float = float("nan")
    n_deviations: int = 0
    mem_top_frozen_i: int = -1      # memory-line first-touch bars
    mem_bot_frozen_i: int = -1
    pending: dict | None = None     # the open breach, if any
    born_at: int = -1               # C3: the confirm bar
    backdated_from: int = -1        # C3: the terminal pivot's bar
    n_inception_zones: int = 0      # C1: spring-birth zones at the seed
    p0_bar: int = -1
    p1_bar: int = -1

    @property
    def mid(self) -> float:
        return (self.top + self.bottom) / 2.0


def macro_pins(scale_mult, pins=None) -> dict:
    """The MACRO pin set at one SCALE: only LEG_MIN and REV_MIN scale; the
    touch, return and breakout pins are shared by both scales [v2 law]."""
    base = PINS if pins is None else pins
    return dict(base, LEG_MIN=base["LEG_MIN"] * scale_mult,
                REV_MIN=base["REV_MIN"] * scale_mult)


def _tape(d, atr):
    """(o, h, l, c, atr) as float arrays + ts as a list, from a frame-like
    (anything indexable by "o" "h" "l" "c" and optionally "ts": a DataFrame,
    a dict of arrays) or an (o, h, l, c[, ts]) tuple.  POSITIONAL: bar index
    is row position.  ts, when given, must be a sortable STRING per bar (the
    machine prints and compares it, never parses it); absent, events carry
    None.  Refuses an ATR that is not one finite number per bar -- the
    machine's ATR is finite from bar 0, and a NaN would silently switch
    every comparison it touches to False."""
    if isinstance(d, (tuple, list)):
        o, h, l, c = d[0], d[1], d[2], d[3]
        ts = d[4] if len(d) > 4 else None
    else:
        o, h, l, c = d["o"], d["h"], d["l"], d["c"]
        ts = d["ts"] if "ts" in d else None
    o, h, l, c = (np.asarray(x, dtype=float) for x in (o, h, l, c))
    a = np.asarray(atr, dtype=float)
    n = len(c)
    if not (len(o) == len(h) == len(l) == n == len(a)):
        raise ValueError(f"rangefinder_census: o/h/l/c/atr lengths differ "
                         f"({len(o)},{len(h)},{len(l)},{n},{len(a)})")
    if n and not np.isfinite(a).all():
        raise ValueError("rangefinder_census: the ATR handed in is not finite "
                         "on every bar -- the machine's ATR is the Wilder RMA "
                         "SEEDED AT TR[0]; an SMA-seeded ATR (NaN warm-up) is "
                         "a different machine")
    if ts is None:
        ts = [None] * n
    else:
        ts = ts.tolist() if hasattr(ts, "tolist") else list(ts)
        if len(ts) != n:
            raise ValueError("rangefinder_census: ts length differs from the tape")
    return o, h, l, c, a, ts


def run_machine(d, atr, pins: dict) -> dict:
    """The whole lifecycle over one tape.  `atr` is the caller's
    engine-law ATR (Wilder RMA of true range, length ATR_LEN, seeded at the
    tape's first bar), one finite value per bar.  Returns the machine's dict
    -- events (ordered), pivots, ranges, coverage and the summary keys -- plus
    two additive keys: "seals" (the bar each pivot became KNOWABLE at, aligned
    with "pivots"; never -1) and "covered" (the per-bar coverage mask)."""
    o_a, h_a, l_a, c_a, atr_a, ts = _tape(d, atr)
    n = len(c_a)
    h, l, c = h_a.tolist(), l_a.tolist(), c_a.tolist()
    body_hi = np.maximum(o_a, c_a).tolist()     # C1: the pivot-bar BODY extremes
    body_lo = np.minimum(o_a, c_a).tolist()
    atr_l = atr_a.tolist()
    body_mode = pins.get("BOUNDARY_MODE", "body") == "body"
    rev_min, leg_min = pins["REV_MIN"], pins["LEG_MIN"]
    touch_eps = pins["TOUCH_EPS"]
    dev_ret, brk_n, brk_m = (pins["DEV_RETURN_BARS"], pins["BREAK_CONFIRM_N"],
                             pins["BREAK_MARGIN"])
    redraw_body = pins.get("REDRAW_BASIS", "wick") == "body"
    ev: list[dict] = []

    def log(i, kind, **kw):
        ev.append({"i": int(i), "ts": ts[i], "event": kind,
                   **{k: (round(float(v), 2) if isinstance(v, (int, float))
                          and k not in ("rid", "bars", "count") else v)
                      for k, v in kw.items()}})

    # ── ZigZag pivots (alternating by construction; merge law in the machine)
    pivots: list[tuple[int, float, int]] = []   # (bar, px, dir +1 high/-1 low)
    seals: list[int] = []                       # the bar each pivot SEALED at
    zdir = 0
    ext_i, ext_px = 0, (c[0] if n else _NAN)
    warm = ATR_LEN                               # ATR seed floor
    for i in range(n):
        if i < warm:
            if h[i] >= ext_px:
                ext_i, ext_px = i, h[i]
            continue
        if zdir == 0:
            if h[i] - l[ext_i] >= rev_min * atr_l[i] and l[ext_i] <= l[i]:
                zdir, ext_i, ext_px = 1, i, h[i]
            elif ext_px - l[i] >= rev_min * atr_l[i]:
                zdir = -1
                pivots.append((ext_i, ext_px, 1))
                seals.append(i)
                log(ext_i, "pivot", px=ext_px, side="high")
                ext_i, ext_px = i, l[i]
            elif h[i] > ext_px:
                ext_i, ext_px = i, h[i]
            continue
        if zdir == 1:
            if h[i] > ext_px:
                ext_i, ext_px = i, h[i]
            elif (ext_px - l[i] >= rev_min * atr_l[i]
                  and (not pivots
                       or abs(ext_px - pivots[-1][1]) >= leg_min * atr_l[i])):
                pivots.append((ext_i, ext_px, 1))
                seals.append(i)
                log(ext_i, "pivot", px=ext_px, side="high")
                zdir, ext_i, ext_px = -1, i, l[i]
        else:
            if l[i] < ext_px:
                ext_i, ext_px = i, l[i]
            elif (h[i] - ext_px >= rev_min * atr_l[i]
                  and (not pivots
                       or abs(ext_px - pivots[-1][1]) >= leg_min * atr_l[i])):
                pivots.append((ext_i, ext_px, -1))
                seals.append(i)
                log(ext_i, "pivot", px=ext_px, side="low")
                zdir, ext_i, ext_px = 1, i, h[i]
    order = sorted(range(len(pivots)), key=lambda k: pivots[k][0])
    pivots = [pivots[k] for k in order]
    seals = [seals[k] for k in order]

    # ── the lifecycle sweep.  Knowability IS the recorded seal bar [F-RF-12].
    conf_order: list[tuple[int, tuple]] = list(zip(seals, pivots))
    conf_order.sort(key=lambda x: (x[0], x[1][0]))
    # the suffix law's premise, CHECKED not assumed: pivot bars rise strictly
    # in knowability order, so "visible pivots past floor_i" is a suffix
    suffix_ok = all(conf_order[k][1][0] < conf_order[k + 1][1][0]
                    for k in range(len(conf_order) - 1))

    ranges: list[Range] = []
    potentials: list[Range] = []       # state == POTENTIAL, rid order
    confirmed: list[Range] = []        # state == CONFIRMED, rid order
    top_heap: list[tuple] = []         # (top, rid) of DEAD, top unfrozen
    bot_heap: list[tuple] = []         # (-bottom, rid) of DEAD, bottom unfrozen
    by_rid: dict[int, Range] = {}
    multi = bool(pins.get("MULTI_ACTIVE", 0))
    state = "NEUTRAL"
    covered = bytearray(n)
    rid_seq = 0
    known: list[tuple] = []          # pivots visible so far
    seg_lo = 0                       # known[seg_lo:] are past floor_i
    floor_i = -1                     # last lifecycle boundary (confirm / any die)
    ci = 0
    n_conf_order = len(conf_order)

    for i in range(n):
        # pivots that became knowable this bar
        while ci < n_conf_order and conf_order[ci][0] == i:
            known.append(conf_order[ci][1])
            ci += 1
            # SEED check on the newest pivot pair (P0 expansion-terminal, P1
            # first counter-pivot); under ONE_ACTIVE only while no confirmed
            # range is alive, under MULTI always
            if (multi or not confirmed) and len(known) >= 2:
                p1 = known[-1]
                p0 = known[-2]
                # p0 must be the expansion extreme among the pivots visible
                # since the last lifecycle boundary [pinned in calibration]
                if suffix_ok:
                    while seg_lo < len(known) and known[seg_lo][0] <= floor_i:
                        seg_lo += 1
                    seg = known[seg_lo:]
                else:
                    seg = [p for p in known if p[0] > floor_i]
                if p0[2] == 1:
                    is_term = p0[1] >= max((p[1] for p in seg if p[2] == 1),
                                           default=p0[1])
                else:
                    is_term = p0[1] <= min((p[1] for p in seg if p[2] == -1),
                                           default=p0[1])
                if is_term and p1[2] == -p0[2]:
                    hi_p = p0 if p0[2] == 1 else p1
                    lo_p = p1 if p0[2] == 1 else p0
                    if body_mode:
                        top = float(body_hi[hi_p[0]])
                        bot = float(body_lo[lo_p[0]])
                    else:
                        top, bot = hi_p[1], lo_p[1]
                    if top <= bot:      # degenerate body cluster -- refuse
                        continue
                    rid_seq += 1
                    r = Range(rid=rid_seq, top=top, bottom=bot, top0=top,
                              bottom0=bot, seed_i=i)
                    r.p0_bar, r.p1_bar = int(p0[0]), int(p1[0])
                    if body_mode:
                        if hi_p[1] > top:
                            r.dev_top_ext = hi_p[1]
                            r.n_inception_zones += 1
                        if lo_p[1] < bot:
                            r.dev_bot_ext = lo_p[1]
                            r.n_inception_zones += 1
                    # the seed's FINAL pivot P1 is the last-touched side;
                    # confirmation must touch the OPPOSITE boundary
                    r.confirm_side = "top" if p1[2] == -1 else "bottom"
                    ranges.append(r)
                    potentials.append(r)
                    by_rid[r.rid] = r
                    log(i, "seed", rid=r.rid, top=top, bottom=bot,
                        p0_bar=p0[0], p1_bar=p1[0],
                        inception_zones=r.n_inception_zones)
        atr_i = atr_l[i]
        c_i, h_i, l_i = c[i], h[i], l[i]

        # potentials: invalidate / confirm (the close outranks the wick)
        if potentials:
            keep: list[Range] = []
            k = 0
            n_pot = len(potentials)
            while k < n_pot:
                r = potentials[k]
                k += 1
                if c_i > r.top or c_i < r.bottom:
                    r.state = "INVALIDATED"
                    r.die_i = i
                    floor_i = i
                    log(i, "potential-invalidate", rid=r.rid,
                        px=c_i, boundary=("top" if c_i > r.top else "bottom"))
                    continue
                eps = touch_eps * atr_i
                if r.confirm_side == "top" and h_i >= r.top - eps:
                    r.state = "CONFIRMED"
                elif r.confirm_side == "bottom" and l_i <= r.bottom + eps:
                    r.state = "CONFIRMED"
                if r.state != "CONFIRMED":
                    keep.append(r)
                    continue
                r.confirm_i = i
                r.born_at = i
                r.backdated_from = r.p0_bar
                floor_i = i
                insort(confirmed, r, key=lambda x: x.rid)
                log(i, "confirm", rid=r.rid, boundary=r.confirm_side,
                    top=r.top, bottom=r.bottom, mid=r.mid)
                log(i, "backdate", rid=r.rid, born_at=i,
                    backdated_from=r.p0_bar)
                if r.dev_top_ext == r.dev_top_ext:
                    log(i, "inception-deviation", rid=r.rid, side="top",
                        extreme=r.dev_top_ext, boundary=r.top)
                if r.dev_bot_ext == r.dev_bot_ext:
                    log(i, "inception-deviation", rid=r.rid, side="bottom",
                        extreme=r.dev_bot_ext, boundary=r.bottom)
                if not multi:
                    # the stock falls: survivors so far, then the unvisited
                    # tail -- rid order, the machine's
                    for q in keep + potentials[k:]:
                        q.state, q.die_i = "SUPERSEDED", i
                        log(i, "potential-superseded", rid=q.rid)
                    keep = []
                    break
            potentials = keep

        # breach lifecycle, per alive range
        if confirmed:
            died = False
            for r in list(confirmed):
                pending = r.pending
                if pending is None:
                    if c_i > r.top:
                        r.pending = {"side": "top", "open_i": i,
                                     "extreme": h_i, "body_ext": body_hi[i],
                                     "closes": 1}
                        log(i, "breach-open", rid=r.rid, side="top", px=c_i,
                            boundary=r.top)
                    elif c_i < r.bottom:
                        r.pending = {"side": "bottom", "open_i": i,
                                     "extreme": l_i, "body_ext": body_lo[i],
                                     "closes": 1}
                        log(i, "breach-open", rid=r.rid, side="bottom",
                            px=c_i, boundary=r.bottom)
                    pending = r.pending
                else:
                    beyond = (c_i > r.top if pending["side"] == "top"
                              else c_i < r.bottom)
                    if pending["side"] == "top":
                        pending["extreme"] = max(pending["extreme"], h_i)
                        pending["body_ext"] = max(pending["body_ext"], body_hi[i])
                    else:
                        pending["extreme"] = min(pending["extreme"], l_i)
                        pending["body_ext"] = min(pending["body_ext"], body_lo[i])
                    if beyond:
                        pending["closes"] += 1
                    else:
                        # body close back INSIDE
                        bars_out = i - pending["open_i"]
                        if bars_out <= dev_ret:
                            r.n_deviations += 1
                            rd = (pending["body_ext"] if redraw_body
                                  else pending["extreme"])
                            if pending["side"] == "top":
                                r.dev_top_ext = (pending["extreme"]
                                                 if r.dev_top_ext != r.dev_top_ext
                                                 else max(r.dev_top_ext,
                                                          pending["extreme"]))
                                old_b = r.top
                                r.top = max(r.top, rd)
                            else:
                                r.dev_bot_ext = (pending["extreme"]
                                                 if r.dev_bot_ext != r.dev_bot_ext
                                                 else min(r.dev_bot_ext,
                                                          pending["extreme"]))
                                old_b = r.bottom
                                r.bottom = min(r.bottom, rd)
                            log(i, "harden", rid=r.rid,
                                side=pending["side"], bars_outside=bars_out,
                                extreme=pending["extreme"])
                            log(i, "redraw", rid=r.rid, side=pending["side"],
                                frm=old_b, to=(r.top if pending["side"] == "top"
                                               else r.bottom), mid=r.mid)
                        else:
                            log(i, "breach-lapse", rid=r.rid,
                                side=pending["side"], bars_outside=bars_out)
                        r.pending = pending = None
                if pending is not None:
                    die_by_n = pending["closes"] >= brk_n
                    bnd = r.top if pending["side"] == "top" else r.bottom
                    die_by_m = (abs(c_i - bnd) >= brk_m * atr_i
                                and ((c_i > bnd) if pending["side"] == "top"
                                     else (c_i < bnd)))
                    if die_by_n or die_by_m:
                        r.state, r.die_i = "DEAD", i
                        floor_i = i
                        died = True
                        log(i, "breakout-die", rid=r.rid, side=pending["side"],
                            by=("n_closes" if die_by_n else "margin"),
                            closes=pending["closes"], px=c_i)
                        state = ("BULL_EXP" if pending["side"] == "top"
                                 else "BEAR_EXP")
                        r.pending = None
        else:
            died = False

        # memory-line first touches on dead ranges (never on the death bar:
        # this bar's dead enter the heaps only after this pass)
        if (top_heap and top_heap[0][0] <= h_i) or (
                bot_heap and bot_heap[0][0] <= -l_i):
            hits = []
            while top_heap and top_heap[0][0] <= h_i:
                hits.append((heappop(top_heap)[1], 0))
            while bot_heap and bot_heap[0][0] <= -l_i:
                hits.append((heappop(bot_heap)[1], 1))
            hits.sort()
            for rid, side in hits:
                r = by_rid[rid]
                if side == 0:
                    r.mem_top_frozen_i = i
                    log(i, "memory-touch", rid=r.rid, side="top", px=r.top)
                else:
                    r.mem_bot_frozen_i = i
                    log(i, "memory-touch", rid=r.rid, side="bottom",
                        px=r.bottom)
        if died:
            for r in confirmed:
                if r.state == "DEAD":
                    heappush(top_heap, (r.top, r.rid))
                    heappush(bot_heap, (-r.bottom, r.rid))
            confirmed = [r for r in confirmed if r.state == "CONFIRMED"]

        # coverage + state -- union over alive ranges
        if confirmed:
            state = "NEUTRAL"
            for r_cov in confirmed:
                lo_b = (r_cov.bottom if r_cov.dev_bot_ext != r_cov.dev_bot_ext
                        else min(r_cov.bottom, r_cov.dev_bot_ext))
                hi_b = (r_cov.top if r_cov.dev_top_ext != r_cov.dev_top_ext
                        else max(r_cov.top, r_cov.dev_top_ext))
                if lo_b <= c_i <= hi_b:
                    covered[i] = 1
                    break
        elif state == "NEUTRAL" and known:
            state = "BULL_EXP" if known[-1][2] == -1 else "BEAR_EXP"

    # pivot events are stamped at their WICK bar with the bar they became
    # KNOWABLE at riding beside.  The key is rounded by NUMPY (the machine's
    # pivot prices are np.float64) and looked up by a PYTHON-rounded price:
    # where the two rounders disagree the machine ships -1, and so must this
    # [header: knowable_at CAN READ -1; "seals" carries the truth]
    know = {(p[0], round(np.float64(p[1]), 2)): cb for cb, p in conf_order}
    for e in ev:
        if e["event"] == "pivot":
            e["knowable_at"] = int(know.get((e["i"], e["px"]),
                                            know.get((e["i"],
                                                      round(e["px"], 2)), -1)))
    ev.sort(key=lambda e: e["i"])

    n_pending_open = sum(1 for r in ranges
                         if r.state == "CONFIRMED" and r.pending is not None)
    cov_mask = np.frombuffer(bytes(covered), dtype=np.uint8).astype(bool)

    conf = [r for r in ranges if r.confirm_i >= 0]
    # censored (still-alive-at-window-end) lifetimes are EXCLUDED from the
    # mean and counted beside it
    lifetimes = [r.die_i - r.confirm_i for r in conf if r.die_i >= 0]
    n_censored = sum(1 for r in conf if r.die_i < 0)
    out = {
        "events": ev, "pivots": pivots, "ranges": ranges,
        "coverage_pct": round(100.0 * cov_mask.sum() / n, 2),
        "n_bars": n, "n_pivots": len(pivots),
        "n_confirmed": len(conf),
        "n_potential_unresolved": sum(1 for r in ranges
                                      if r.state == "POTENTIAL"),
        "mean_confirmed_lifetime": (round(float(np.mean(lifetimes)), 1)
                                    if lifetimes else None),
        "n_lifetime_censored": n_censored,
        "n_pending_open": n_pending_open,
        "final_state": state,
        "status_line": "",
    }
    out["status_line"] = (f"{n} CANDLES · {out['coverage_pct']}% RANGE "
                          f"COVERAGE · {out['n_potential_unresolved']} "
                          f"POTENTIAL · {out['n_confirmed']} CONFIRMED · "
                          f"{out['n_pivots']} SUPPORTING PIVOTS · "
                          f"{n_pending_open} D PENDING")
    # ADDITIVE [header]: not in the machine's dict, not in any event sha
    out["seals"] = seals
    out["covered"] = cov_mask
    return out


# ═══════════════════════════ v2 · HIERARCHY + FLIPS + THE LEASH [RF-3]
def _zone_index(events) -> dict:
    """rid -> [(i, side, extreme)] over the two event kinds _span_at reads, in
    log order.  One pass, instead of one pass PER RANGE."""
    idx: dict = {}
    for e in events:
        if e["event"] in ("inception-deviation", "harden"):
            idx.setdefault(e.get("rid"), []).append(
                (e["i"], e["side"], float(e["extreme"])))
    return idx


def span_at(r, events, i: int, _index=None) -> tuple:
    """A range's span AS OF bar i, rebuilt from its own events -- boundaries
    at their pre-redraw values plus any zone extremes logged at or before i.
    The machine's _span_at, quirk included: it reads the ROUNDED "extreme"
    (2 dp), so it is a CONTAINMENT organ, not a price source -- on a sub-dollar
    tape scale the prices by a printed power of ten first, or skip micro."""
    top, bot = float(r.top0), float(r.bottom0)
    rows = (_zone_index(events) if _index is None else _index).get(r.rid, ())
    for e_i, side, ext in rows:
        if e_i > i:
            continue
        if side == "top":
            top = max(top, ext)
        else:
            bot = min(bot, ext)
    return bot, top


def containment(micro: dict, macro: dict) -> tuple[list, list]:
    """[H1] kept micro rids + suppression events.  Spans AS OF the micro's
    confirm bar -- at-birth for the micro, current-as-of-that-bar for the
    macro [pinned law; never end-of-run]."""
    kept, sup = [], []
    mic_idx = _zone_index(micro["events"])
    mac_idx = _zone_index(macro["events"])
    lives = [q for q in macro["ranges"] if q.confirm_i >= 0]
    # the parent is the FIRST macro range, in rid order, alive at the bar.
    # When the confirmed lives are disjoint and rise with rid (ONE_ACTIVE),
    # at most one can be alive and bisection finds it; otherwise scan.
    disjoint = all(a.die_i >= 0 and a.die_i <= b.confirm_i
                   for a, b in zip(lives, lives[1:]))
    starts = [q.confirm_i for q in lives]
    for r in micro["ranges"]:
        if r.confirm_i < 0:
            continue
        i = r.confirm_i
        parent = None
        if disjoint:
            k = bisect_right(starts, i) - 1
            if k >= 0 and (lives[k].die_i < 0 or lives[k].die_i > i):
                parent = lives[k]
        else:
            for q in lives:
                if q.confirm_i <= i and (q.die_i < 0 or q.die_i > i):
                    parent = q
                    break
        if parent is None:
            sup.append({"i": i, "event": "micro-suppressed", "rid": r.rid,
                        "reason": "no_live_macro"})
            continue
        mlo, mhi = span_at(r, None, i, mic_idx)
        plo, phi = span_at(parent, None, i, mac_idx)
        if mlo >= plo and mhi <= phi:
            kept.append((r.rid, parent.rid))
        else:
            sup.append({"i": i, "event": "micro-suppressed", "rid": r.rid,
                        "reason": "outside_macro_span",
                        "parent_rid": parent.rid})
    return kept, sup


def flips_and_leash(macro: dict, d, atr, pins: dict,
                    mem_cap: int | None = None,
                    retests: bool = True) -> list[dict]:
    """[H2+H3] the memory-line lifecycle, re-walked post-machine: expiry
    (ttl/cap) precedes touches; the first opposite-side touch that holds
    flips.  Returns ordered leash/flip events, byte-identical to the
    machine's at retests=True.

    retests=False withholds the two per-bar spam classes -- `flip-retest`
    and the "candidacy consumed" `memory-retest`, one dict per touched bar
    per spent line, FOREVER (frozen lines never expire) -- and nothing else:
    the result equals the full log with those rows removed [fixtured].

    AS-OF WARNING, the machine's and unchanged: a `flip` (and a "failed
    through" / "truncated" memory-retest) is stamped at its TOUCH bar i but
    is decided by bars i..i+FLIP_HOLD_BARS -- it is KNOWN at i + HOLD, never
    at i; the spam classes leak that verdict by their names."""
    cap = MEM_CAP_PER_SIDE if mem_cap is None else int(mem_cap)
    _, h_a, l_a, c_a, atr_a, ts = _tape(d, atr)
    h, l, c, atr_l = h_a.tolist(), l_a.tolist(), c_a.tolist(), atr_a.tolist()
    n = len(c)
    ttl = int(pins["MEM_TTL_BARS"])
    hold_n = int(pins["FLIP_HOLD_BARS"])
    hold_m = float(pins["FLIP_HOLD_MARGIN"])
    # line registry, the machine's order: corpses in range order, top first
    lines = []
    for r in macro["ranges"]:
        # corpses = DEAD CONFIRMED ranges only [H2/H3 law]
        if r.state == "DEAD" and r.confirm_i >= 0 and r.die_i >= 0:
            for side, px in (("top", float(r.top)), ("bottom", float(r.bottom))):
                lines.append({"rid": r.rid, "side": side, "px": px,
                              "born": r.die_i, "state": "live",
                              "die_ts": ts[r.die_i], "k": len(lines)})
    by_birth = sorted(range(len(lines)), key=lambda k: (lines[k]["born"], k))
    n_lines = len(lines)
    p_cap = p_walk = p_ttl = 0
    live_side = {"top": [], "bottom": []}    # line indices, ascending: LIVE
                                             # and born <= i (the cap's view)
    roster_px: list[float] = []              # born < i, not expired -- sorted
    roster_k: list[int] = []                 # by (px, k), parallel lists

    def roster_drop(x):
        if not x.get("in_roster"):
            return
        x["in_roster"] = False
        j = bisect_left(roster_px, x["px"])
        while roster_k[j] != x["k"]:      # equal prices sit side by side
            j += 1
        del roster_px[j], roster_k[j]

    ev = []
    for i in range(n):
        # cap: count live per side, expire oldest [H3]
        while p_cap < n_lines and lines[by_birth[p_cap]]["born"] <= i:
            x = lines[by_birth[p_cap]]
            insort(live_side[x["side"]], x["k"])
            p_cap += 1
        for side in ("top", "bottom"):
            live = live_side[side]
            if len(live) > cap:
                for k in sorted(live, key=lambda y: lines[y]["born"])[
                        :len(live) - cap]:
                    x = lines[k]
                    x["state"] = "expired"
                    live.remove(k)
                    roster_drop(x)
                    ev.append({"i": i, "ts": ts[i], "event": "line-expired",
                               "rid": x["rid"], "side": side,
                               "px": round(x["px"], 1), "reason": "cap"})
        # the walk sees lines born BEFORE this bar
        while p_walk < n_lines and lines[by_birth[p_walk]]["born"] < i:
            x = lines[by_birth[p_walk]]
            p_walk += 1
            if x["state"] == "live":
                j = bisect_right(roster_px, x["px"])
                roster_px.insert(j, x["px"])
                roster_k.insert(j, x["k"])
                x["in_roster"] = True
        due = []
        while p_ttl < n_lines and i - lines[by_birth[p_ttl]]["born"] > ttl:
            if lines[by_birth[p_ttl]]["state"] == "live":
                due.append(by_birth[p_ttl])
            p_ttl += 1
        lo = bisect_left(roster_px, l[i])
        hi = bisect_right(roster_px, h[i])
        if lo >= hi and not due:
            continue
        visit = sorted(set(roster_k[lo:hi]) | set(due))
        for k in visit:
            x = lines[k]
            if x["state"] not in ("live", "frozen") or x["born"] >= i:
                continue
            if x.get("flip_done"):
                if l[i] <= x["px"] <= h[i]:
                    ev.append({"i": i, "ts": ts[i],
                               "event": ("flip-retest" if x.get("flipped")
                                         else "memory-retest"),
                               "rid": x["rid"], "side": x["side"],
                               "px": round(x["px"], 1),
                               **({} if x.get("flipped") else
                                  {"verdict": "candidacy consumed — the "
                                              "one evaluation is spent "
                                              "[pinned]"})})
                continue
            # ttl runs from death; an expired line neither freezes nor flips
            if x["state"] == "live" and i - x["born"] > ttl:
                x["state"] = "expired"
                live_side[x["side"]].remove(k)
                roster_drop(x)
                ev.append({"i": i, "ts": ts[i], "event": "line-expired",
                           "rid": x["rid"], "side": x["side"],
                           "px": round(x["px"], 1), "reason": "ttl"})
                continue
            # TWO-SIDED touch [H2 law]
            touched = l[i] <= x["px"] <= h[i]
            if not touched:
                continue
            if x["state"] == "live":
                x["state"] = "frozen"          # freeze at FIRST touch (any
                x["touch_i"] = i               # side) -- the v1 render law
                live_side[x["side"]].remove(k)
            # flip candidacy [H2]: the FIRST OPPOSITE-side approach gets ONE
            # evaluation, frozen or not; same-side touches spend nothing
            appr_above = c[i - 1] > x["px"]
            opposite = (appr_above if x["side"] == "top"
                        else not appr_above)
            if not opposite:
                ev.append({"i": i, "ts": ts[i], "event": "memory-retest",
                           "rid": x["rid"], "side": x["side"],
                           "px": round(x["px"], 1),
                           "verdict": "same-side touch, no flip candidacy"})
                continue
            x["flip_done"] = True          # one evaluation, consumed
            if not retests:
                # a spent line can only ever emit spam: leave the roster
                roster_drop(x)
            if i + hold_n >= n:
                ev.append({"i": i, "ts": ts[i], "event": "memory-retest",
                           "rid": x["rid"], "side": x["side"],
                           "px": round(x["px"], 1),
                           "verdict": "hold window truncated by tape end — "
                                      "NOT confirmed"})
                continue
            held = True
            for j in range(i, i + hold_n + 1):
                thr = hold_m * atr_l[j]
                through = (c[j] < x["px"] - thr if x["side"] == "top"
                           else c[j] > x["px"] + thr)
                if through:
                    held = False
                    break
            if held:
                ev.append({"i": i, "ts": ts[i], "event": "flip",
                           "rid": x["rid"], "side": x["side"],
                           "px": round(x["px"], 1),
                           "polarity": ("support" if x["side"] == "top"
                                        else "resistance"),
                           "glyph": "▲" if x["side"] == "top" else "▼",
                           "parent_death": x["die_ts"],
                           "retest": ts[i]})
                x["flipped"] = True
            else:
                ev.append({"i": i, "ts": ts[i], "event": "memory-retest",
                           "rid": x["rid"], "side": x["side"],
                           "px": round(x["px"], 1),
                           "verdict": "failed through within the hold "
                                      "window — touch only"})
    return ev


# ═══════════════════════════════════════ the AS-OF law, one bar per event
# ADDITIVE.  An event's "i" is the bar it is STAMPED at, which is not always
# the bar it could be KNOWN at.  These two return known_at, aligned with the
# log they are handed: the event is knowable at the CLOSE of bar known_at and
# not one bar sooner.  The law is prefix-stability, and it is fixtured: the
# log of tape[:t] equals the full log filtered by known_at <= t - 1 (the naive
# filter i <= t - 1 does NOT survive that test).
def machine_known_at(m: dict) -> list[int]:
    """known_at per event of m["events"], m from run_machine HERE.  A pivot
    is stamped at its WICK bar and known at its SEAL -- read from m["seals"],
    never from the event's knowable_at, which can read -1 [header].  Every
    other machine event is known at its own bar."""
    seal_of = {(p[0], "high" if p[2] == 1 else "low"): s
               for p, s in zip(m["pivots"], m["seals"])}
    return [seal_of[(e["i"], e["side"])] if e["event"] == "pivot" else e["i"]
            for e in m["events"]]


def leash_known_at(leash: list, hold_bars: int) -> list[int]:
    """known_at per leash event (full or lean log).  The ONE flip evaluation
    of a line is stamped at its touch bar i and decided by bars i..i+HOLD:
    `flip`, "failed through" and "truncated" are known at i + HOLD.  The spam
    classes that follow NAME that verdict, so they are known no sooner than
    it: max(i, evaluation bar + HOLD).  Same-side touches and expiries are
    known at i.  ("failed through" is in truth knowable at its first failing
    close, which the log does not carry; i + HOLD is the conservative bound.)"""
    hold = int(hold_bars)
    eval_i: dict = {}
    out = []
    for e in leash:
        key, i = (e.get("rid"), e.get("side")), e["i"]
        verdict = e.get("verdict", "")
        if e["event"] == "flip" or verdict.startswith(("failed through",
                                                       "hold window truncated")):
            eval_i[key] = i
            out.append(i + hold)
        elif e["event"] == "flip-retest" or verdict.startswith("candidacy consumed"):
            out.append(max(i, eval_i.get(key, i) + hold))
        else:
            out.append(i)
    return out


def run_v2(d, atr, pins_v2: dict, mem_cap: int | None = None,
           with_micro: bool = True, retests: bool = True) -> dict:
    """MACRO (LEG_MIN / REV_MIN scaled by SCALE_MULT) + MICRO (v1 pins, FROZEN)
    + containment + the leash: the machine's run_v2, same keys, same bytes at
    the defaults.  with_micro=False skips the micro run and containment (the
    macro scale is the only writer of state, lines and flips; on a 5m tape
    micro is most of the cost): micro / kept / suppressed / micro_kept_events
    then read None -- absent, never an empty list that would pass for
    "nothing was kept"."""
    macro = run_machine(d, atr, macro_pins(pins_v2["SCALE_MULT"]))
    leash = flips_and_leash(macro, d, atr, pins_v2, mem_cap=mem_cap,
                            retests=retests)
    if with_micro:
        micro = run_machine(d, atr, dict(PINS))    # v1 ruled values, FROZEN
        kept, sup = containment(micro, macro)
        kept_rids = {k for k, _ in kept}
        micro_kept_events = [e for e in micro["events"]
                             if e.get("rid") is None or e["rid"] in kept_rids
                             or e["event"] == "pivot"]
    else:
        micro = kept = sup = micro_kept_events = None
    ts = _tape(d, atr)[5]
    # a BTC KEY-C literal, kept for the bytes; meaningless off-BTC, None
    # when the tape carries no ts
    conf_feb_aug = (None if (ts and ts[0] is None) else
                    len([r for r in macro["ranges"] if r.confirm_i >= 0
                         and ts[r.confirm_i] >= "2026-02-01"]))
    n_kept = len(kept) if kept is not None else 0
    return {
        "macro": macro, "micro": micro, "kept": kept, "suppressed": sup,
        "micro_kept_events": micro_kept_events, "leash": leash,
        "flips": [e for e in leash if e["event"] == "flip"],
        "state": macro["final_state"],
        "macro_count_feb_aug": conf_feb_aug,
        "status_line": (f"{len(ts)} CANDLES · {macro['final_state']} · "
                        f"{macro['coverage_pct']}% COV (MACRO) · "
                        f"{macro['n_pending_open']} PENDING · "
                        f"{macro['n_confirmed']} MACRO · "
                        f"{n_kept} MICRO · "
                        f"{macro['n_pivots']} PIVOTS"),
    }
