"""THE STATION ENGINE — station canon v1, the four posture words, in code.

D-1 of queue BR-1 (RATIFIED operator 2026-08-16).  C-3, verbatim:

    C-3 STATIONS = station canon v1 verbatim (STALKING/ARMED/TRIGGERED/DEAD);
    one canonical module `scripts/station_engine.py` read by Board, Cards, and
    the Pine-parity fixture.  No re-derived semantics anywhere [D3].

════════════════════════════════════════════════════════════════════════════
READ THIS FIRST — THE NAME COLLISION.  "station canon v1" DENOTES TWO THINGS.

  (i)  OPERATOR RULING 2026-08-15, verbatim from
       docs/memory/NAIAD_MEMORY_VERBATIM_2026-08-15.md:
         'Rulings given: ["stations"] six-station lifecycle w/ ORACLE-class
          mapping = station canon v1'
       That is the S1..S6 TRADE-LIFETIME kit (WATCHLIST · ACTIVE HUNT ·
       TRIGGER · AGILE ENTRY · MANAGEMENT · GRACEFUL EXIT), written out in
       research_outputs/census2b/viz_payloads/v3_stations.json.

  (ii) BR-1 C-3, one day later, says "station canon v1 verbatim
       (STALKING/ARMED/TRIGGERED/DEAD)" — FOUR BOARD POSTURE WORDS.

  NO DOCUMENT RECONCILES THEM.  This module binds reading (ii), because C-3
  names the four words explicitly and BR-1 is the ratified commission.  The
  six-stage kit is a DIFFERENT REGISTER and is deliberately NOT implemented
  here; `LIFECYCLE_S1_S6_POINTER` names where it lives so no lane merges them.
  A third vocabulary — the SSv12 six binary gates TIDE/WINDOW/TRIGGER/ADD/
  RIDE/BELL (PINE_LANE_PRIMER_2026-08-15 §1) — is the GATE layer this engine
  reads; it is not a set of posture words either.

  Reported to the operator as a finding of the BR-1 build, not silently fixed.

════════════════════════════════════════════════════════════════════════════
THE SECOND DISCLOSURE — WHERE THE SEMANTICS COME FROM.

C-3 forbids re-derived semantics.  So this module DERIVES NOTHING.  Every
gate below is the ratified TC3 rule card executed through the already-fixtured
machinery of `scripts/tierc2_rules.py` (Frame4h, _crosses, armings), which
tierc3_rules.py inherits byte-for-byte.  The four posture words are a NAMING
MAP laid over those gates.

  THE MAP ITSELF IS NEW.  No estate document defines STALKING, ARMED,
  TRIGGERED or DEAD as separate sentences — the only canon text in the estate
  is the enumeration plus one transition sentence (quoted in CANON below).
  Every row of the map therefore carries `ruled`: True where a ratified
  sentence dictates it, False where this build PROPOSED it.  Every False row
  is a [VETO] awaiting the operator, is logged by the D-7 calibration logger,
  and is listed in the BR-1 build document.  Nothing here self-adopts.

FIREWALL (BR-1 §2).  This module's transitive import closure is
{numpy, dataclasses, json, hashlib, pathlib, engine.*, tierc2_rules,
tierc3_rules} — no `analytics`, no journal, no trading layer, no network.
F-BR-3 asserts it.  Live data is operations-only: this module RECORDS a
station, it never AGGREGATES an outcome.
"""
from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from engine import indicators as ind  # noqa: E402

import tierc2_rules as V2  # noqa: E402
import tierc3_rules as V3  # noqa: E402

# ═══════════════════════════════════════════════════════ THE CLOSED REGISTER
# The tierc2/tierc3 pattern (F-C2-3 / F-C3-3): no value is invented; each row
# names where the number already lived.  Rows this build PROPOSED carry
# 'ruled': False and the word PROPOSED in their source, and are [VETO].
# A stale row in a closed register is how a retired rule comes back.

REGISTER: dict[str, dict] = {
    "LENS": {
        "value": V3.REGISTER["LENS"]["value"],
        "ruled": True,
        "source": "tierc2_rules.REGISTER['LENS'] — rule card ['lens'] 4h only. "
                  "BR-1 C-6 independently pins the card's anchor to the 4h lens.",
    },
    "TIDE_FAST": {"value": V3.REGISTER["TIDE_FAST"]["value"], "ruled": True,
                  "source": "tierc2_rules.REGISTER['TIDE_FAST'] — rule card TIDE e89"},
    "TIDE_SLOW": {"value": V3.REGISTER["TIDE_SLOW"]["value"], "ruled": True,
                  "source": "tierc2_rules.REGISTER['TIDE_SLOW'] — rule card TIDE e316"},
    "WINDOW_FAST": {"value": V3.REGISTER["WINDOW_FAST"]["value"], "ruled": True,
                    "source": "tierc2_rules.REGISTER['WINDOW_FAST'] — rule card WINDOW 12/89"},
    "WINDOW_SLOW": {"value": V3.REGISTER["WINDOW_SLOW"]["value"], "ruled": True,
                    "source": "tierc2_rules.REGISTER['WINDOW_SLOW'] — rule card WINDOW 12/89"},
    "TRIGGER_FAST": {"value": V3.REGISTER["TRIGGER_FAST"]["value"], "ruled": True,
                     "source": "tierc2_rules.REGISTER['TRIGGER_FAST'] — rule card TRIGGER 12/26"},
    "TRIGGER_SLOW": {
        "value": V3.REGISTER["TRIGGER_SLOW"]["value"],
        "ruled": True,
        "source": "tierc2_rules.REGISTER['TRIGGER_SLOW'] — rule card TRIGGER 12/26. "
                  "DISCLOSURE: the Board/Watch prose of LANE_UPDATE_DIONYSUS_2026-08-13 "
                  "says 'a 12/25 trigger', and the S3 gate text says '12x25/26 ... The 25 "
                  "is the ruled load-bearing shadow line [ratified]'. The EXECUTABLE canon "
                  "— rule card, census, Pine — is 26 everywhere. This engine uses 26 and "
                  "prints this line rather than reconciling the two by fiat.",
    },
    "D_DISPLACEMENT": {"value": V3.REGISTER["D_DISPLACEMENT"]["value"], "ruled": True,
                       "source": "tierc2_rules.REGISTER['D_DISPLACEMENT'] — rule card ['d'] "
                                 "floor at the arming cross. Inside the named-unruled 'fuzz' "
                                 "[VETO] set: a pin, not a truth."},
    "ATR_LEN": {"value": V3.REGISTER["ATR_LEN"]["value"], "ruled": True,
                "source": "tierc2_rules.REGISTER['ATR_LEN'] — configs/naiad_v0.yaml "
                          "signal.atr_len = 14, Wilder/RMA of true range"},
    "MIN_STOP_ATR": {"value": V3.REGISTER["MIN_STOP_ATR"]["value"], "ruled": True,
                     "source": "tierc3_rules.REGISTER['MIN_STOP_ATR'] — the F-3 rail "
                               "(operator 2026-08-15). BR-1 C-6 restates it as "
                               "'min 1.0 ATR rail, per the TC3 rulings'."},
    "STOP_BUF_ATR": {"value": V3.REGISTER["STOP_BUF_ATR"]["value"], "ruled": True,
                     "source": "tierc2_rules.REGISTER['STOP_BUF_ATR']"},
    "PIVOT_L": {"value": V3.REGISTER["PIVOT_L"]["value"], "ruled": True,
                "source": "tierc2_rules.REGISTER['PIVOT_L']"},
    "PIVOT_R": {"value": V3.REGISTER["PIVOT_R"]["value"], "ruled": True,
                "source": "tierc2_rules.REGISTER['PIVOT_R']"},

    # ── the window-boundary reading, RULED but two-valued: state which ──────
    "WINDOW_CLOSED_AT_T0": {
        "value": True,
        "ruled": True,
        "source": "census2b_parta.windows_for_cell docstring — 'window = [t0, next "
                  "counter-direction 12_89 cross) -- half-open'. Window is CLOSED at t0, "
                  "so a trigger on the arming bar IS in-window. The census-2A precedent "
                  "(t0, close] survives there as the separate column `fate_strict`; the "
                  "two readings differ on 6.3% of all windows. This engine takes the "
                  "census-2B reading and prints `trigger_on_arming_bar` so the other "
                  "reading is recoverable from the tape.",
    },

    # ── PROPOSED by this build. [VETO]. Nothing below self-adopts. ─────────
    "DEAD_MEMORY_BARS": {
        "value": 6,
        "ruled": False,
        "source": "PROPOSED by the BR-1 build 2026-08-16 — UNRULED [VETO]. The Board "
                  "shows ONE posture word per asset (C-5), but DEAD is a property of a "
                  "WINDOW, not of an asset: an asset with no open window is either being "
                  "watched (STALKING) or has just buried one (DEAD). This constant is how "
                  "long the burial stays on the Board — 6 bars on the 4h lens = 24h. "
                  "D-7 logs the resulting DEAD fraction every run so BR-2 can recalibrate "
                  "it against a week of measured distributions instead of a guess.",
    },
    "TRIGGER_FRESH_BARS": {
        "value": 6,
        "ruled": False,
        "source": "PROPOSED by the BR-1 build 2026-08-16 — UNRULED [VETO]. TRIGGERED has "
                  "no age term in the rule card: a window stays TRIGGERED until it closes, "
                  "so a 12/26 cross from 24 days ago still reads TRIGGERED today. That is "
                  "faithful to the card and MISLEADING on a Board whose word the operator "
                  "reads as 'the entry alert is live now'. This is the age past which a "
                  "trigger is printed STALE — the word does not change (the card rules the "
                  "word), the staleness prints beside it. 6 bars = 24h on the 4h lens. "
                  "D-7 logs the trigger-age distribution every run so BR-2 can rule it.",
    },
    "BOARD_PRECEDENCE": {
        "value": ("TRIGGERED", "ARMED", "DEAD", "STALKING"),
        "ruled": False,
        "source": "PROPOSED by the BR-1 build 2026-08-16 — UNRULED [VETO]. C-5 asks for "
                  "one posture word per row; C-7 lists 12/89 windows PLURAL per asset. "
                  "The collapse rule from N windows to one word is not written anywhere. "
                  "This is the order: live business outranks a burial, a burial outranks "
                  "an empty watch.",
    },
    "HEAT_KEY": {
        "value": "proximity_x_cluster_score",
        "ruled": False,
        "source": "PROPOSED by the BR-1 build 2026-08-16 — UNRULED [VETO]. The only text "
                  "is LANE_UPDATE_DIONYSUS_2026-08-13 'sorted by heat (proximity x cluster "
                  "score)'; no formula exists anywhere in the estate. The Board implements "
                  "it as score / (1 + atr_distance) and prints both inputs beside the "
                  "sort so the ranking is auditable rather than magic.",
    },
}

# The six-stage kit is a DIFFERENT register.  Pointer only — never merged.
LIFECYCLE_S1_S6_POINTER = (
    "research_outputs/census2b/viz_payloads/v3_stations.json :: data.six_rules "
    "(sha256 37b00bed88104b180ec05ccf7311dceca714d9bf11e1d7ec5aadf1271a7b43d0, "
    "sourced from LANE_UPDATE_DIONYSUS_2026-08-13). S1 WATCHLIST · S2 ACTIVE HUNT · "
    "S3 TRIGGER · S4 AGILE ENTRY · S5 MANAGEMENT · S6 GRACEFUL EXIT. "
    "This is operator ruling 2026-08-15's 'station canon v1'. It is NOT this module's."
)

# ══════════════════════════════════════════════════════════ THE FOUR WORDS

STATION_WORDS = ("STALKING", "ARMED", "TRIGGERED", "DEAD")

# The ONLY canon text the estate holds about these words, quoted rather than
# paraphrased.  Both quotes are from
# exchange/reports/LANE_UPDATE_DIONYSUS_2026-08-13_BR-momentum_winner-zoom_brief-feedback.md
CANON_QUOTE_ENUMERATION = (
    "THE BOARD — ten rows, one glance, sorted by heat (proximity x cluster score): "
    "regime chip (HTF trend/range + governor state, the operator's regime question "
    "answered first), location now (ATR distance to nearest high-score cluster "
    "above/below), the two lines in the sand, and a posture word: STALKING · ARMED · "
    "TRIGGERED · DEAD. Answers the only morning question: where is business possible today."
)
CANON_QUOTE_TRANSITION = (
    "THE WATCH — the armed-window registry, live: an arming opens a window; the board "
    "lists open windows per asset/lens with age; a 12/25 trigger inside one is the entry "
    "alert; seal or counter-cross closes it. The census studies dead armed windows; the "
    "brief displays living ones — same organ, two tempos."
)

CANON: dict[str, dict] = {
    "STALKING": {
        "station": 1,
        "gate": "No open 12/89 window in force on the lens. The asset is watched, "
                "not armed. A 12/89 cross that fails the TIDE gate or the "
                "displacement floor d>=0.75 leaves the asset STALKING and prints "
                "its reject reason ('tide' or 'd').",
        "ruled": False,
        "source": "PROPOSED. The word appears only in the enumeration. The gate is the "
                  "COMPLEMENT of the ruled ARMED gate, plus the rule card's own reject "
                  "reasons (tierc2_rules.armings sets tide_ok / d_ok; "
                  "tierc3_baseline assigns Arming.reject 'tide' | 'd').",
    },
    "ARMED": {
        "station": 2,
        "gate": "An open 12/89 window: a close-confirmed 4h 12/89 cross in the tide "
                "direction, TIDE true at the arming bar, displacement "
                "|close-e89|/ATR at the cross >= 0.75, and no counter 12/89 and no "
                "89/316-against since. No in-window 12/26 trigger yet.",
        "ruled": True,
        "source": "RULED. tierc3_rules.RULE_CARD_V3 verbatim: 'TIDE: long iff e89>e316 "
                  "AND close>e316 on 4h (mirror short) / WINDOW: 4h 12/89 cross in "
                  "direction, no counter yet; displacement |close-e89|/ATR at the cross "
                  ">= d=0.75'. Canon transition text: 'an arming opens a window'.",
    },
    "TRIGGERED": {
        "station": 3,
        "gate": "An open window that contains a same-direction 4h 12/26 cross at or "
                "after the arming bar. The trigger does not close the window; it is "
                "the entry alert inside it.",
        "ruled": True,
        "source": "RULED. RULE_CARD_V3: 'TRIGGER: first in-window 4h 12/26 cross -> "
                  "enter at that bar close'. Canon transition text: 'a 12/25 trigger "
                  "inside one is the entry alert'. See REGISTER['TRIGGER_SLOW'] for the "
                  "25-vs-26 disclosure.",
    },
    "DEAD": {
        "station": 4,
        "gate": "The window is closed — by the counter 4h 12/89 cross, or by the 4h "
                "89/316 turning against the window's direction (the bell), whichever "
                "comes first. The closing reason is printed, never inferred. A closed "
                "window keeps the asset on the Board as DEAD for DEAD_MEMORY_BARS "
                "bars, then the asset returns to STALKING.",
        "ruled": True,
        "source": "RULED for the CLOSE: RULE_CARD_V3 'BELL: counter 4h 12/89 OR 4h "
                  "89/316 against -> exit at close'; canon transition text 'seal or "
                  "counter-cross closes it'. PROPOSED for the MEMORY: how long DEAD "
                  "stays on an asset row is REGISTER['DEAD_MEMORY_BARS'], [VETO]. "
                  "DISCLOSURE: the 89/316 seal is 'a eulogy, arriving ~28h after the "
                  "decision mattered' (S3 gate text) — it closes a window, it never "
                  "opens one.",
    },
}


# ═══════════════════════════════════════════════════════════ THE RECORDS

@dataclass
class Window:
    """One 12/89 armed window, alive or buried. RECORDING, never AGGREGATING."""
    symbol: str
    lens: str
    direction: int                 # +1 long, -1 short
    arm_i: int
    arm_ms: int
    tide_ok: bool
    disp: float                    # |close - e89| / ATR at the cross
    d_ok: bool
    strip_d_ok: dict               # the unscored {0.50, 1.00} sensitivity strip
    admitted: bool                 # tide_ok AND d_ok — did it ever become ARMED
    reject: str                    # '' | 'tide' | 'd'
    trigger_i: int | None
    trigger_ms: int | None
    trigger_on_arming_bar: bool
    trigger_age_bars: int | None   # bars from the trigger to as_of; None if untriggered
    trigger_stale: bool            # trigger_age_bars > TRIGGER_FRESH_BARS [VETO]
    close_i: int | None            # None while alive
    close_ms: int | None
    closed_by: str                 # '' (alive) | 'counter-12_89' | 'bell-89_316'
    age_bars: int                  # bars from arming to as-of (alive) or to close
    station: str                   # the word THIS window is in


@dataclass
class AssetStations:
    """Everything the Board and the Watch read for one asset. One lens."""
    symbol: str
    lens: str
    as_of_ms: int
    as_of_i: int
    close: float
    atr: float
    tide: str                      # 'long' | 'short' | 'none'
    tide_flip_i: int | None        # last 89/316 flip — the C-4 spaghetti anchor
    tide_flip_ms: int | None
    tide_flip_dir: str
    board_word: str
    board_reason: str
    open_windows: list = field(default_factory=list)
    recent_dead: list = field(default_factory=list)


# ══════════════════════════════════════════════════════════════ THE ENGINE

def build_frame(df) -> V2.Frame4h:
    """The lens object, built by the rule card's own constructor.

    `df` is a kline frame with open_time/open/high/low/close. We call
    tierc2_rules.build_4h so the EMA and ATR semantics are the DECISION
    path's (engine.indicators, seeded at series start, Pine parity) and not
    a second implementation. C-3: no re-derived semantics anywhere.
    """
    return V2.build_4h(
        df["open_time"].to_numpy(dtype="int64"),
        df["open"].to_numpy(dtype="float64"),
        df["high"].to_numpy(dtype="float64"),
        df["low"].to_numpy(dtype="float64"),
        df["close"].to_numpy(dtype="float64"),
    )


def crosses(f: V2.Frame4h) -> dict:
    """Every cross the rule card names. A re-export, NOT a reimplementation:
    the body is tierc2_rules._crosses, so Board, Cards, Watch, the ORACLE GRID
    footer and the parity fixture all read one set of semantics (C-3)."""
    return V2._crosses(f)


def last_tide_flip(f: V2.Frame4h, as_of_i: int) -> tuple[int | None, int | None, str]:
    """The C-4 spaghetti anchor: each asset's LAST 89/316 tide flip at or before as_of.

    'TIDE FLIP' = crossover/crossunder of e89 vs e316 on the lens —
    tierc2_rules._crosses()['b_up'] / ['b_dn'] exactly. F-BR-5 asserts this
    is deterministic across two computations from the same substrate.
    """
    x = crosses(f)
    up = np.flatnonzero(x["b_up"][: as_of_i + 1])
    dn = np.flatnonzero(x["b_dn"][: as_of_i + 1])
    last_up = int(up[-1]) if up.size else -1
    last_dn = int(dn[-1]) if dn.size else -1
    if last_up < 0 and last_dn < 0:
        return None, None, "none"
    if last_up >= last_dn:
        return last_up, int(f.open_ms[last_up]), "up"
    return last_dn, int(f.open_ms[last_dn]), "down"


def tide_at(f: V2.Frame4h, i: int) -> str:
    """The rule card's TIDE, evaluated at bar i. Long iff e89>e316 AND close>e316."""
    if f.e89[i] > f.e316[i] and f.c[i] > f.e316[i]:
        return "long"
    if f.e89[i] < f.e316[i] and f.c[i] < f.e316[i]:
        return "short"
    return "none"


def _bell_index(x: dict, direction: int, arm_i: int) -> int | None:
    """First 89/316-against bar strictly after the arming. Rule card BELL, limb 2."""
    against = x["b_dn"] if direction == 1 else x["b_up"]
    later = np.flatnonzero(against[arm_i + 1:])
    return int(arm_i + 1 + later[0]) if later.size else None


def windows_for(symbol: str, f: V2.Frame4h, as_of_i: int | None = None,
                lens: str | None = None) -> list[Window]:
    """Every 12/89 window in the loaded history, stationed as of `as_of_i`.

    The gates are the rule card's, executed through tierc2_rules.armings()
    (which is byte-inherited by tierc3_rules). Nothing is re-derived here:
    this function only (a) finds the trigger inside the window, (b) applies
    the BELL's second limb, and (c) names the resulting posture word.
    """
    lens = lens or REGISTER["LENS"]["value"]
    n = len(f.c)
    as_of_i = n - 1 if as_of_i is None else int(as_of_i)
    if not (0 <= as_of_i < n):
        raise ValueError(f"as_of_i {as_of_i} out of range for {n} bars; negative "
                         f"indices are NOT honoured here — the scalar stamps would "
                         f"follow Python's wrap-around while the arming range and "
                         f"every age would not, giving a silently wrong board")
    x = crosses(f)

    out: list[Window] = []
    for a in V2.armings(symbol, f, 0, as_of_i):
        # ── the close: counter 12/89 OR 89/316-against, whichever is first ──
        counter_i = a.window_end_i if a.window_end_i < n else None
        bell_i = _bell_index(x, a.direction, a.arm_i)
        cands = [(i, why) for i, why in ((counter_i, "counter-12_89"),
                                         (bell_i, "bell-89_316")) if i is not None]
        if cands:
            close_i, closed_by = min(cands, key=lambda t: t[0])
        else:
            close_i, closed_by = None, ""

        # A window that closes after as_of is still ALIVE as of as_of.
        if close_i is not None and close_i > as_of_i:
            close_i, closed_by = None, ""

        # ── the trigger: first same-direction 12/26 at-or-after the arming,
        #    strictly inside the window. Window is CLOSED at t0 (census-2B
        #    reading, REGISTER['WINDOW_CLOSED_AT_T0']).
        t_series = x["t_up"] if a.direction == 1 else x["t_dn"]
        hi = (close_i if close_i is not None else as_of_i + 1)
        seg = np.flatnonzero(t_series[a.arm_i:hi])
        trig_i = int(a.arm_i + seg[0]) if seg.size else None

        admitted = bool(a.tide_ok and a.d_ok)
        reject = "" if admitted else ("tide" if not a.tide_ok else "d")

        # ── the word ────────────────────────────────────────────────────────
        if not admitted:
            station = "STALKING"
        elif close_i is not None:
            station = "DEAD"
        elif trig_i is not None:
            station = "TRIGGERED"
        else:
            station = "ARMED"

        end_for_age = close_i if close_i is not None else as_of_i
        out.append(Window(
            symbol=symbol, lens=lens, direction=a.direction,
            arm_i=a.arm_i, arm_ms=a.arm_ms,
            tide_ok=a.tide_ok, disp=a.disp, d_ok=a.d_ok,
            strip_d_ok=dict(a.strip_d_ok),
            admitted=admitted, reject=reject,
            trigger_i=trig_i,
            trigger_ms=(int(f.open_ms[trig_i]) if trig_i is not None else None),
            trigger_on_arming_bar=bool(trig_i is not None and trig_i == a.arm_i),
            trigger_age_bars=(None if trig_i is None else int(as_of_i - trig_i)),
            trigger_stale=bool(trig_i is not None
                               and (as_of_i - trig_i) > REGISTER["TRIGGER_FRESH_BARS"]["value"]),
            close_i=close_i,
            close_ms=(int(f.open_ms[close_i]) if close_i is not None else None),
            closed_by=closed_by,
            age_bars=int(end_for_age - a.arm_i),
            station=station,
        ))
    out.sort(key=lambda w: (w.arm_ms, -w.direction))
    return out


def stations_for(symbol: str, df, as_of_i: int | None = None) -> AssetStations:
    """One asset, one lens, everything the Board and the Watch need."""
    lens = REGISTER["LENS"]["value"]
    f = build_frame(df)
    n = len(f.c)
    as_of_i = n - 1 if as_of_i is None else int(as_of_i)
    if not (0 <= as_of_i < n):
        raise ValueError(f"as_of_i {as_of_i} out of range for {n} bars")
    wins = windows_for(symbol, f, as_of_i=as_of_i, lens=lens)
    dead_memory = REGISTER["DEAD_MEMORY_BARS"]["value"]

    live = [w for w in wins if w.admitted and w.close_i is None]
    buried = [w for w in wins if w.admitted and w.close_i is not None
              and (as_of_i - w.close_i) <= dead_memory]

    # BOARD_PRECEDENCE, [VETO]: live business outranks a burial, a burial an
    # empty watch. Both inputs printed so the collapse is auditable.
    trg = [w for w in live if w.station == "TRIGGERED"]
    if trg:
        w = min(trg, key=lambda w: w.trigger_age_bars)
        why = (f"an open window holds an in-window 12/26 cross, "
               f"{w.trigger_age_bars} bar(s) ago")
        if w.trigger_stale:
            why += (f" — STALE, older than TRIGGER_FRESH_BARS="
                    f"{REGISTER['TRIGGER_FRESH_BARS']['value']} [VETO]")
        word = "TRIGGERED"
    elif live:
        word, why = "ARMED", f"{len(live)} open 12/89 window(s), no trigger yet"
    elif buried:
        w = max(buried, key=lambda w: w.close_i)
        word, why = "DEAD", (f"window closed {as_of_i - w.close_i} bar(s) ago "
                             f"by {w.closed_by}")
    else:
        word, why = "STALKING", "no open window on the lens"

    flip_i, flip_ms, flip_dir = last_tide_flip(f, as_of_i)
    return AssetStations(
        symbol=symbol, lens=lens,
        as_of_ms=int(f.open_ms[as_of_i]), as_of_i=as_of_i,
        close=float(f.c[as_of_i]), atr=float(f.atr[as_of_i]),
        tide=tide_at(f, as_of_i),
        tide_flip_i=flip_i, tide_flip_ms=flip_ms, tide_flip_dir=flip_dir,
        board_word=word, board_reason=why,
        open_windows=live, recent_dead=buried,
    )


# ═════════════════════════════════════════════ THE ONE TRUTH SOURCE (BR-2)
# BR-2 F-R2-1 CANON IDENTITY: 'JS reads the same station_canon.json sha as
# Python'. The JSON below IS the canon; Python reads these same dicts. The
# R2 page must read this file and must not re-implement any gate.

CANON_JSON_PATH = Path(__file__).resolve().parent.parent / "research_outputs" / "oracle" / "station_canon.json"


def canon_doc() -> dict:
    """The canonical document. Ordering and separators are pinned so the sha
    is reproducible from either side of the language boundary."""
    return {
        "canon": "station canon v1 (BR-1 C-3 reading: the four Board posture words)",
        "version": "1.0.0",
        "words": list(STATION_WORDS),
        "stations": CANON,
        "register": {k: {"value": _jsonable(v["value"]), "ruled": v["ruled"],
                         "source": v["source"]} for k, v in REGISTER.items()},
        "canon_quotes": {
            "enumeration": CANON_QUOTE_ENUMERATION,
            "transition": CANON_QUOTE_TRANSITION,
        },
        "name_collision_disclosure": (
            "'station canon v1' denotes TWO things. Operator ruling 2026-08-15 gave the "
            "name to the SIX-STAGE lifecycle kit; BR-1 C-3 of 2026-08-16 gives it to these "
            "FOUR posture words. This document binds the BR-1 reading. The six-stage kit "
            "is a different register and lives at: " + LIFECYCLE_S1_S6_POINTER
        ),
        "unruled_rows_are_veto": [k for k, v in REGISTER.items() if not v["ruled"]]
                                 + [k for k, v in CANON.items() if not v["ruled"]],
    }


def _jsonable(v):
    if isinstance(v, tuple):
        return list(v)
    return v


def canon_bytes() -> bytes:
    """The exact bytes whose sha both languages must agree on."""
    return json.dumps(canon_doc(), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def canon_sha() -> str:
    return hashlib.sha256(canon_bytes()).hexdigest()


def write_canon_json(path: Path | None = None) -> tuple[Path, str, int]:
    """Emit station_canon.json. Returns (path, sha256, bytes)."""
    path = Path(path) if path is not None else CANON_JSON_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    b = canon_bytes()
    path.write_bytes(b)
    return path, hashlib.sha256(b).hexdigest(), len(b)


def register_table() -> list[str]:
    """The closed register, printed. tierc2/tierc3 print theirs the same way."""
    rows = ["REGISTER — station canon v1 (RULED rows are law; UNRULED rows are [VETO])"]
    for k, v in REGISTER.items():
        mark = "RULED  " if v["ruled"] else "[VETO] "
        rows.append(f"  {mark}{k:22} = {v['value']!r}")
    for k, v in CANON.items():
        mark = "RULED  " if v["ruled"] else "[VETO] "
        rows.append(f"  {mark}CANON.{k:16} station {v['station']}")
    return rows


if __name__ == "__main__":  # a printer, not a builder
    for line in register_table():
        print(line)
    p, sha, nb = write_canon_json()
    print(f"\nstation_canon.json -> {p}")
    print(f"  {nb} B  sha256 {sha}")
