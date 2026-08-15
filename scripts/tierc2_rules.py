"""TIER-C2 · THE FORWARD BASELINE — THE DECISION PATH, AND NOTHING ELSE.

This module is the rule card in code.  It is a SEPARATE MODULE from
`tierc2_baseline.py` for one reason and it is a fixture, not a preference:

    F-C2-6 · CAPTURED-NOT-CONSULTED.  Amendment B1 states that NOTHING in the
    rule card reads the analytics registry.  A grep proves a grep; an import
    closure proves the property.  Every decision the baseline makes is made
    HERE, and this module's transitive import closure contains no `analytics`
    module at all -- asserted, printed, in `tierc2_fixtures.py`.

    The separation is structural rather than disciplined: `engine/` never
    imports `analytics/` either (invariant I-B, analytics/INTERFACE.md), so
    the closure below is {numpy, pandas, engine.*} and cannot reach a registry
    symbol by any path.

The tape (`analytics/`) is joined to these outputs downstream, by timestamp,
in `tierc2_baseline.py`.  It is RECORDED.  It is never READ back into a
decision.  Q6c -- the stillbirth counterfactual -- is the reason: the location
evidence has to be gathered on an UNCONDITIONED population of fills before any
location gate may become law.  Conditioning here would destroy the very
population that makes the later counterfactual answerable.

────────────────────────────────────────────────────────────────────────────
THE RULE CARD, verbatim from the ratified paste (operator 2026-08-15):

  UNIVERSE ["universe"]: {BTC,ETH,SOL,NEAR,ZEC}USDT · LENS ["lens"]: 4h only
  TIDE: long iff e89>e316 AND close>e316 on 4h (mirror short)
  WINDOW: 4h 12/89 cross in direction, no counter yet; displacement |close-e89|/ATR
    at the cross >= d=0.75 ["d"]; sensitivity strip {0.50,1.00} printed UNSCORED
  TRIGGER: first in-window 4h 12/26 cross -> enter at that bar close
  STOP ["stop"]: structural beyond nearest 1H swing pivot (architecture of record);
    R = entry-stop distance; one unit; one position per asset
  RIDE: no management of any kind
  BELL: counter 4h 12/89 OR 4h 89/316 against -> exit at close
  ACCOUNTING ["accounting"]: net of 10 bps round-trip + journaled funding; R units
────────────────────────────────────────────────────────────────────────────

EVERY CONSTANT BELOW IS CITED, NOT INVENTED (F-C2-3).  See `REGISTER`.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from engine import indicators as ind
from engine.s1 import _pivots

# ═══════════════════════════════════════════════════ THE CLOSED REGISTER
# F-C2-3: no value in this module is invented.  Each row names where the
# number already lived before this build opened.  `tierc2_fixtures.py` prints
# this table and re-reads the cited sources to prove the values still match.
REGISTER: dict[str, dict] = {
    # ── from the rule card as RATIFIED by the operator, 2026-08-15 ─────────
    "UNIVERSE": {
        "value": ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT"),
        "source": "rule card ['universe']; the estate's standing 5-asset panel "
                  "(configs/tc5_{btc,eth,sol,near,zec}.json)",
    },
    "LENS": {
        "value": "4h",
        "source": "rule card ['lens'] — 4h only; the 1h series is read ONLY for "
                  "the structural stop pivot, never for a decision",
    },
    "TIDE_FAST": {"value": 89, "source": "rule card TIDE — e89"},
    "TIDE_SLOW": {"value": 316, "source": "rule card TIDE — e316"},
    "WINDOW_FAST": {"value": 12, "source": "rule card WINDOW — 4h 12/89 cross"},
    "WINDOW_SLOW": {"value": 89, "source": "rule card WINDOW — 4h 12/89 cross"},
    "TRIGGER_FAST": {"value": 12, "source": "rule card TRIGGER — 4h 12/26 cross"},
    "TRIGGER_SLOW": {"value": 26, "source": "rule card TRIGGER — 4h 12/26 cross"},
    "D_DISPLACEMENT": {
        "value": 0.75,
        "source": "rule card ['d'] — displacement floor at the arming cross",
    },
    "D_STRIP": {
        "value": (0.50, 1.00),
        "source": "rule card ['d'] — sensitivity strip, printed UNSCORED",
    },
    # ── from the estate's own closed register, unchanged by this build ────
    "ATR_LEN": {
        "value": 14,
        "source": "configs/naiad_v0.yaml:`signal.atr_len` = 14 — the frozen live "
                  "paper line; ATR is Wilder/RMA of true range "
                  "(engine/indicators.py:53, analytics/volatility.py:32)",
    },
    "FEE_BPS_SIDE": {
        "value": 5.0,
        "source": "configs/naiad_v0.yaml:`trading.fee_bps_side` = 5.0 (taker, per "
                  "side, charter §5) — 10 bps ROUND TRIP, which is the rule "
                  "card's ['accounting'] figure exactly",
    },
    "PIVOT_L": {
        "value": 5,
        "source": "engine/trading.py:219 `struct_stop_at` — confirmed 1h (5,5) "
                  "pivots; analytics/structure.py:CONFIRMATION_LAG = 5 agrees",
    },
    "PIVOT_R": {"value": 5, "source": "engine/trading.py:219 — as PIVOT_L"},
    "PIVOT_LOOKBACK_1H": {
        "value": 200,
        "source": "engine/trading.py:222 `struct_stop_at` — 200-bar 1h lookback",
    },
    "STOP_BUF_ATR": {
        "value": 0.5,
        "source": "engine/trading.py:206 `TRAIL_B = 0.5`; configs/naiad_v0.yaml:"
                  "`signal.stop_buf_atr` = 0.5 — the stop sits this far BEYOND "
                  "the pivot, in ATR of the signal bar",
    },
}

UNIVERSE: tuple[str, ...] = REGISTER["UNIVERSE"]["value"]
LENS: str = REGISTER["LENS"]["value"]
TIDE_FAST: int = REGISTER["TIDE_FAST"]["value"]
TIDE_SLOW: int = REGISTER["TIDE_SLOW"]["value"]
WINDOW_FAST: int = REGISTER["WINDOW_FAST"]["value"]
WINDOW_SLOW: int = REGISTER["WINDOW_SLOW"]["value"]
TRIGGER_FAST: int = REGISTER["TRIGGER_FAST"]["value"]
TRIGGER_SLOW: int = REGISTER["TRIGGER_SLOW"]["value"]
D_DISPLACEMENT: float = REGISTER["D_DISPLACEMENT"]["value"]
D_STRIP: tuple[float, ...] = REGISTER["D_STRIP"]["value"]
ATR_LEN: int = REGISTER["ATR_LEN"]["value"]
FEE_BPS_SIDE: float = REGISTER["FEE_BPS_SIDE"]["value"]
FEE_BPS_ROUND_TRIP: float = 2.0 * FEE_BPS_SIDE          # 10.0, the ['accounting'] figure
PIVOT_L: int = REGISTER["PIVOT_L"]["value"]
PIVOT_R: int = REGISTER["PIVOT_R"]["value"]
PIVOT_LOOKBACK_1H: int = REGISTER["PIVOT_LOOKBACK_1H"]["value"]
STOP_BUF_ATR: float = REGISTER["STOP_BUF_ATR"]["value"]

MS_4H = 14_400_000
MS_1H = 3_600_000

# The funnel's stages, in order.  Every arming lands in exactly one TERMINAL
# stage; the cumulative columns are what "where the system leaks" means.
FUNNEL_STAGES = ("armings_seen", "passed_tide", "passed_d", "triggered",
                 "entered", "belled")


# ═══════════════════════════════════════════════════════════ indicators
@dataclass
class Frame4h:
    """Everything the rule card can see on the 4h lens.  Computed ONCE per
    asset over the FULL loaded history (warm-up included) so that a window
    boundary can never move an EMA -- see `warm_from` in the runner."""
    open_ms: np.ndarray
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    e12: np.ndarray
    e26: np.ndarray
    e89: np.ndarray
    e316: np.ndarray
    atr: np.ndarray


def build_4h(open_ms, o, h, l, c) -> Frame4h:
    """The 4h lens.  EMA/ATR are the ENGINE's primitives, not analytics' --
    the engine seeds at the series start for Pine parity (engine/indicators.py
    docstring), and Stage B must ride the identical arithmetic."""
    o = np.asarray(o, float); h = np.asarray(h, float)
    l = np.asarray(l, float); c = np.asarray(c, float)
    return Frame4h(
        open_ms=np.asarray(open_ms, np.int64), o=o, h=h, l=l, c=c,
        e12=ind.ema(c, TRIGGER_FAST), e26=ind.ema(c, TRIGGER_SLOW),
        e89=ind.ema(c, TIDE_FAST), e316=ind.ema(c, TIDE_SLOW),
        atr=ind.atr(h, l, c, ATR_LEN),
    )


@dataclass
class Pivots1h:
    """Confirmed 1h (5,5) swing pivots -- the structural stop's anchor.

    `conf` is the 1h bar index at which the pivot becomes KNOWABLE (pivot bar
    + R).  A caller working as-of 1h bar k filters `conf <= k`; that filter is
    the whole reason this is causal.  `engine.s1._pivots` returns exactly
    (confirm_bars, values) and is the estate's pivot of record.
    """
    low_conf: np.ndarray
    low_val: np.ndarray
    high_conf: np.ndarray
    high_val: np.ndarray


def build_pivots_1h(h1_high, h1_low) -> Pivots1h:
    lc, lv = _pivots(np.asarray(h1_low, float), PIVOT_L, PIVOT_R, low=True)
    hc, hv = _pivots(np.asarray(h1_high, float), PIVOT_L, PIVOT_R, low=False)
    return Pivots1h(low_conf=lc, low_val=lv, high_conf=hc, high_val=hv)


# ═══════════════════════════════════════════════════════════ the stop
def struct_stop(pv: Pivots1h, cur_1h_idx: int, entry_px: float, direction: int,
                atr_sig: float) -> float | None:
    """THE ARCHITECTURE OF RECORD, transcribed from `engine/trading.py:219`.

        Nearest confirmed 1h (5,5) pivot strictly beyond entry within a
        200-bar 1h lookback, offset -/+ 0.5 x ATR(signal bar).
        Returns None => no_struct_anchor, and the tranche is NOT taken.

    Transcribed rather than imported because the engine's copy is a closure
    over `arch_data` built inside `run_replay`, and `run_replay` cannot be
    called here at all: its G-1 guard refuses this study's corridor, and its
    signal path is the SSv11/v12 cascade, which is not this rule card.  The
    transcription is line-for-line and `tierc2_fixtures.py` (F-C2-2) reconciles
    three real stops against it by hand.

    `cur_1h_idx` is the index of the 1h bar that CLOSES with the 4h trigger
    bar, so no pivot later than the entry instant is ever eligible.
    """
    if not np.isfinite(atr_sig):
        return None
    if direction == 1:
        elig = ((pv.low_conf <= cur_1h_idx)
                & (cur_1h_idx - pv.low_conf <= PIVOT_LOOKBACK_1H)
                & (pv.low_val < entry_px))
        if not elig.any():
            return None
        anchor = float(pv.low_val[elig].max())          # nearest BELOW entry
        return anchor - STOP_BUF_ATR * atr_sig
    else:
        elig = ((pv.high_conf <= cur_1h_idx)
                & (cur_1h_idx - pv.high_conf <= PIVOT_LOOKBACK_1H)
                & (pv.high_val > entry_px))
        if not elig.any():
            return None
        anchor = float(pv.high_val[elig].min())         # nearest ABOVE entry
        return anchor + STOP_BUF_ATR * atr_sig


# ═══════════════════════════════════════════════════════════ the record
@dataclass
class Arming:
    """One 12/89 cross in one direction: the unit the funnel counts.

    Every arming carries the reason it stopped advancing, so the funnel is a
    partition and not a set of independent counts.
    """
    symbol: str
    direction: int                  # +1 long, -1 short
    arm_i: int                      # 4h index of the 12/89 cross
    arm_ms: int
    window_end_i: int               # 4h index of the counter 12/89 cross (exclusive)
    tide_ok: bool
    disp: float                     # |close - e89| / ATR at the cross
    d_ok: bool
    trigger_i: int | None = None
    trigger_ms: int | None = None
    entered: bool = False
    reject: str = ""                # terminal stage reason
    strip_d_ok: dict = field(default_factory=dict)   # {0.50: bool, 1.00: bool}


@dataclass
class Trade:
    symbol: str
    direction: int
    arm_i: int
    arm_ms: int
    entry_i: int
    entry_ms: int
    entry_px: float
    stop_px: float
    r_dist: float
    pivot_anchor: float
    atr_at_entry: float
    disp_at_arming: float
    exit_i: int
    exit_ms: int
    exit_px: float
    exit_reason: str                # "stop" | "bell_12_89" | "bell_89_316" | "corridor_end"
    bars_held: int
    gross_r: float
    fee_r: float
    funding_r: float
    net_r: float
    gross_r_bellonly: float         # UNSCORED sensitivity — see the runner
    net_r_bellonly: float
    exit_reason_bellonly: str
    exit_ms_bellonly: int


# ═══════════════════════════════════════════════════════════ the replay
def _crosses(f: Frame4h) -> dict:
    """Every cross the rule card names, precomputed.  `ind.crossover` is the
    engine's semantics of record: a>b now AND a<=b prior; NaN compares False."""
    return {
        "w_up": ind.crossover(f.e12, f.e89),      # window opens long
        "w_dn": ind.crossunder(f.e12, f.e89),     # window opens short / counter for long
        "t_up": ind.crossover(f.e12, f.e26),      # trigger long
        "t_dn": ind.crossunder(f.e12, f.e26),     # trigger short
        "b_up": ind.crossover(f.e89, f.e316),     # 89/316 turns up
        "b_dn": ind.crossunder(f.e89, f.e316),    # 89/316 turns down
    }


def armings(symbol: str, f: Frame4h, lo_i: int, hi_i: int) -> list[Arming]:
    """Every 12/89 cross with an arming index in [lo_i, hi_i], both directions.

    The window a cross opens runs to the COUNTER 12/89 cross ("no counter
    yet"), exclusive.  A cross whose counter falls outside the loaded history
    gets `window_end_i = n`, and the runner truncates its ride at the corridor
    edge with reason `corridor_end` -- disclosed, never silently dropped.
    """
    x = _crosses(f)
    n = len(f.c)
    out: list[Arming] = []
    for direction, opens, counter in ((1, x["w_up"], x["w_dn"]),
                                      (-1, x["w_dn"], x["w_up"])):
        idx = np.flatnonzero(opens)
        for i in idx:
            i = int(i)
            if not (lo_i <= i <= hi_i):
                continue
            later = np.flatnonzero(counter[i + 1:])
            end_i = int(i + 1 + later[0]) if later.size else n

            # TIDE, evaluated at the arming bar.
            if direction == 1:
                tide = bool(f.e89[i] > f.e316[i] and f.c[i] > f.e316[i])
            else:
                tide = bool(f.e89[i] < f.e316[i] and f.c[i] < f.e316[i])

            # DISPLACEMENT, |close - e89| / ATR, at the cross.
            a = f.atr[i]
            disp = float(abs(f.c[i] - f.e89[i]) / a) if (np.isfinite(a) and a > 0) else float("nan")
            d_ok = bool(np.isfinite(disp) and disp >= D_DISPLACEMENT)

            out.append(Arming(
                symbol=symbol, direction=direction, arm_i=i,
                arm_ms=int(f.open_ms[i]), window_end_i=end_i,
                tide_ok=tide, disp=disp, d_ok=d_ok,
                strip_d_ok={s: bool(np.isfinite(disp) and disp >= s) for s in D_STRIP},
            ))
    out.sort(key=lambda a: (a.arm_ms, -a.direction))
    return out
