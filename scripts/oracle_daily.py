"""THE ORACLE — the daily organ. D-2 of queue BR-1 (RATIFIED operator 2026-08-16).

Amendment A1-1 names the product: "Oracle" unqualified is THIS daily organ.
The census-2B artifact is always "ORACLE GRID", fully qualified. Every
deliverable of this build is `oracle_*`.

Emits briefs/oracle/oracle_<date>.html containing, per BR-1 §3 as amended:

    BOARD        C-5  10 rows, heat-sorted: regime chip · ATR-distance to the
                      nearest high-score cluster · two lines in the sand ·
                      posture word.
    TRAP CARDS   C-6  entry · structural invalidation (4h-lens anchor + the
                      min 1.0 ATR rail) · target · net R:R after toll · what
                      proves me wrong. Derivation in the appendix.
    WATCH        C-7  live 12/89 windows (age, displacement, trigger status)
                      + a static last-96-bars mantle thumbnail per asset,
                      rendered FROM the v4 payload pattern.
    SPAGHETTI    C-4  event-anchored at each asset's last 89/316 tide flip,
                      ATR-normalised, one panel.
    GRID FOOTER  C-8  yesterday's fired events classified against the ORACLE
                      GRID's NET table, per lens.
    R1 ALERTS    C-9  alert-price blocks, TradingView paste-ready, prices only.
    PROVENANCE   F-BR-8  DISPLAY-ONLY header, payload shas, date, both the
                      certified and the not-certified lists.

════════════════════════════════════════════════════════════════════════════
CLASS AND FIREWALL — BR-1 §2, binding, reprinted in the rendered footer.

Operations/display-only. (1) Live data is operations-only, forbidden as study
evidence. (2) No journal reads; no signal-outcome statistics on any window.
(3) Engine modules imported read-only, trading disabled, never modified.
(4) The archive may be mined for hypotheses, never scored. RECORDING an event
is operations; AGGREGATING outcomes is census work under G-7.

This module reads `analytics/` (the measurement side) for levels, VWAP and
ATR. It does NOT let analytics touch a station: every posture word comes from
`posture_engine`, whose own import closure is analytics-free so the decision
path stays captured-not-consulted (F-C2-6). F-BR-3 asserts both properties.

WHAT THIS MODULE NEVER DOES: it never reads journal/, never imports
engine.trading, never counts a win or a loss, never scores a window.
"""
from __future__ import annotations

import hashlib
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from engine.cells import SYMBOLS                      # noqa: E402
from engine.data import cache_dir                     # noqa: E402
from analytics import levels as L                     # noqa: E402
from analytics import structure as ST                 # noqa: E402
from analytics import volatility as VOL               # noqa: E402
from analytics import vwap as VW                      # noqa: E402
from analytics import ANALYTICS_VERSION, analytics_sha  # noqa: E402

import posture_engine as PE                           # noqa: E402
import census2b_program as P                          # noqa: E402
import tierc3_rules as V3                             # noqa: E402

ZONE = "America/Argentina/Buenos_Aires"
OUT_DIR = ROOT / "briefs" / "oracle"
TAPE_DIR = ROOT / "research_outputs" / "oracle" / "tape"
CAL_DIR = ROOT / "research_outputs" / "oracle" / "calibration"
PAYLOAD_DIR = ROOT / "research_outputs" / "oracle" / "payloads"
GRID_PARQUET = ROOT / "research_outputs" / "census2b" / "oracle" / "oracle_grid.parquet"

# ═══════════════════════════════════════════════════════ THE CLOSED REGISTER
# Same law as tierc2/tierc3/posture_engine: nothing invented without saying so.
# 'ruled': False rows are [VETO] and are logged by D-7 every run.

REGISTER: dict[str, dict] = {
    "ROSTER": {
        "value": tuple(SYMBOLS),
        "ruled": True,
        "source": "engine/cells.py SYMBOLS — 'Basket frozen at ratification (charter §4)'. "
                  "BR-1 C-5 'Roster = current 10-asset capture set'; A1-2 'Roster as-is'.",
    },
    "LENS": {
        "value": PE.REGISTER["LENS"]["value"],
        "ruled": True,
        "source": "posture_engine.REGISTER['LENS'] — the rule card's 4h. The Board, the "
                  "Cards and the Watch all read ONE lens so a row means one thing.",
    },
    "MANTLE_BARS": {
        "value": 96,
        "ruled": True,
        "source": "BR-1 C-7 verbatim: 'static last-96-bars mantle thumbnail per asset'.",
    },
    "GRID_LENSES": {
        "value": ("5m", "15m", "30m", "1h", "4h"),
        "ruled": True,
        "source": "census2b_oracle.LENSES — the ORACLE GRID's own five lenses. C-8 "
                  "classifies fired events 'per lens', so the footer walks exactly these.",
    },
    "FIRED_WINDOW_HOURS": {
        "value": 24,
        "ruled": False,
        "deferred_to": "BR-2",
        "source": "DEFERRED-TO-BR2 by BR-1 Amendment A2-6 (operator, 2026-08-16): BR-2 proposes a measured value from a week of D-7 distributions; nothing self-adopts. ORIGINALLY: PROPOSED by the BR-1 build 2026-08-16 — UNRULED [VETO]. C-8 says "
                  "'yesterday's fired events' and does not define yesterday. 24h back "
                  "from the as-of bar. D-7 logs the resulting event count per run.",
    },
    "GRID_TOLL_KEY": {
        "value": ("4h", "12_26 IN-WINDOW"),
        "ruled": False,
        "deferred_to": "BR-2",
        "source": "DEFERRED-TO-BR2 by BR-1 Amendment A2-6 (operator, 2026-08-16): BR-2 proposes a measured value from a week of D-7 distributions; nothing self-adopts. ORIGINALLY: PROPOSED by the BR-1 build 2026-08-16 — UNRULED [VETO]. C-2 says the "
                  "toll comes from the ORACLE GRID 'by name and lens' but no mapping from "
                  "a Trap Card to a (lens, class) key is written anywhere. A card is a "
                  "12/26 in-window entry on the 4h lens, so this is that cell. "
                  "toll_atr = 0.035196 ATR at time of writing.",
    },
    "NET_RR_FORM": {
        "value": "(reward - toll_price) / (risk + toll_price)",
        "ruled": True,
        "source": "RATIFIED by BR-1 Amendment A2-4 (operator, 2026-08-16), closing "
                  "finding V-5: '(reward - toll) / (risk + toll), toll paid win or lose; "
                  "both inputs print beside every ratio.' Proposed by the BR-1 build "
                  "because no net-R:R formula existed anywhere in the estate while C-2 "
                  "required one and forbade a cost-free number. toll_price = toll_atr x "
                  "ATR(lens); both inputs print beside every ratio so the operator can "
                  "re-derive it by eye.",
    },
    "HEAT": {
        "value": "score / (1 + atr_distance)",
        "ruled": False,
        "deferred_to": "BR-2",
        "source": "DEFERRED-TO-BR2 by BR-1 Amendment A2-6 (operator, 2026-08-16): BR-2 proposes a measured value from a week of D-7 distributions; nothing self-adopts. ORIGINALLY: PROPOSED by the BR-1 build 2026-08-16 — UNRULED [VETO]. The only text "
                  "is 'sorted by heat (proximity x cluster score)'. Both inputs print in "
                  "the row so the sort is auditable. See posture_engine.REGISTER['HEAT_KEY'].",
    },
    "VWAP_WINDOWS_D": {
        "value": (7, 30),
        "ruled": True,
        "source": "analytics/INTERFACE — rolling VWAP windows; the 7d/30d pair is the "
                  "brief-2 short set. Rolling windows take NO maturity floor "
                  "(analytics.vwap docstring); the 90/365d windows are omitted here "
                  "because the Board reads today, not the year.",
    },
    "PIVOT_LOOKBACK_BARS": {
        "value": V3.REGISTER["PIVOT_LOOKBACK_4H"]["value"],
        "ruled": True,
        "source": "tierc3_rules.REGISTER['PIVOT_LOOKBACK_4H'] = 200 bars on the 4h lens.",
    },
}

CERTIFIED = (
    "oscillators + ATR (72/72)", "resample_ohlcv (40/40)",
    "rolling VWAP both substrates (14/14, 28/28)",
    "anchored VWAP incl. sigma (42/42)", "band geometry (54 triples)",
)
NOT_CERTIFIED = (
    "volume_profile / LVN / va_nesting — FIXTURE-VERIFIED, never chart-certified BY DESIGN",
    "RVOL — uncertified",
    "posture canon v1 — the four-word MAP is PROPOSED, not ruled (see the [VETO] table)",
    "net R:R form — PROPOSED, no estate precedent exists",
)


# ═══════════════════════════════════════════════════════════════ LOADING

def load_lens(sym: str, tf: str, tail: int | None = None) -> pd.DataFrame:
    """Whole-file parquet read, the tierc2_baseline idiom. Cache only, no network."""
    p = cache_dir() / "klines" / f"{sym}_{tf}.parquet"
    if not p.exists():
        raise FileNotFoundError(f"HALT: no klines for {sym} {tf} at {p}")
    df = pd.read_parquet(p).sort_values("open_time").reset_index(drop=True)
    if tail is not None and len(df) > tail:
        df = df.iloc[-tail:].reset_index(drop=True)
    return df


def daily_atr(h1: pd.DataFrame) -> float:
    """The house daily-ATR convention: resample 1h -> 1d, then analytics ATR(14).

    Every ATR-normalised LEVEL distance in the brief uses this daily ATR, not
    the lens ATR (the two are different quantities and the estate keeps them
    apart deliberately).
    """
    r = ST.resample_ohlcv(h1["open_time"].to_numpy("int64"),
                          h1["open"].to_numpy("float64"), h1["high"].to_numpy("float64"),
                          h1["low"].to_numpy("float64"), h1["close"].to_numpy("float64"),
                          h1["volume"].to_numpy("float64"), 86_400_000)
    return float(VOL.atr(r["high"], r["low"], r["close"], 14)[-1])


# ═══════════════════════════════════════════════════════════════ LEVELS

def level_registry(sym: str, h4: pd.DataFrame, h1: pd.DataFrame, atr_d: float):
    """A level pool for the Board's clusters. analytics/ is the only arithmetic.

    Two families only, and both are causal at the decision bar:
      structure     — confirmed (5,5) 4h swing pivots, plus prior-day extremes
      vwap_rolling  — 7d / 30d rolling VWAP on the 1h substrate, hlc3 source

    analytics/levels has no time axis and cannot police causality, so the
    slicing is done HERE: confirmed_pivots carries CONFIRMATION_LAG = 5 and
    prior_period_extremes reads only completed days.
    """
    reg = L.LevelRegistry()
    look = REGISTER["PIVOT_LOOKBACK_BARS"]["value"]
    hi = h4["high"].to_numpy("float64")
    lo = h4["low"].to_numpy("float64")
    n = len(hi)
    as_of = n - 1
    for kind, vals in (("high", hi), ("low", lo)):
        idx, lvl, _conf = ST.confirmed_pivots(vals, as_of, left=PE.REGISTER["PIVOT_L"]["value"],
                                              right=PE.REGISTER["PIVOT_R"]["value"], kind=kind)
        for i, v in zip(np.asarray(idx), np.asarray(lvl)):
            if int(i) >= n - look:
                reg.add("structure", f"4h pivot {kind} @{int(i)}", float(v),
                        "confirmed_pivots(4h)", timeframe="4h")

    ext = ST.prior_period_extremes(h1["open_time"].to_numpy("int64"),
                                   h1["high"].to_numpy("float64"),
                                   h1["low"].to_numpy("float64"), period="D")
    # Returns a (prior_high, prior_low) pair of as-of-each-bar arrays; the
    # decision bar is the last element of each. Causal by construction.
    pairs = ext.items() if isinstance(ext, dict) else zip(("high", "low"), ext)
    for label, arr in pairs:
        a = np.asarray(arr).ravel()
        if a.size == 0:
            continue
        v = float(a[-1])
        if np.isfinite(v):
            reg.add("structure", f"prior-day {str(label).replace('prior_', '')}", v,
                    "prior_period_extremes(1h->D)", timeframe="1d")

    src = VW.hlc3(h1["high"].to_numpy("float64"), h1["low"].to_numpy("float64"),
                  h1["close"].to_numpy("float64"))
    for wd in REGISTER["VWAP_WINDOWS_D"]["value"]:
        rv = VW.rolling_vwap(h1["open_time"].to_numpy("int64"), src,
                             h1["volume"].to_numpy("float64"), wd)
        v = float(np.asarray(rv["vwap"])[-1])
        if np.isfinite(v):
            reg.add("vwap_rolling", f"rVWAP {wd}d", v, "rolling_vwap(1h, hlc3)",
                    timeframe="1h")
        for k in (1, 2):
            for side in ("up", "dn"):
                band = rv.get(f"band_{side}_{k}")
                if band is None:
                    continue
                b = float(np.asarray(band)[-1])
                if np.isfinite(b):
                    reg.add("vwap_rolling", f"rVWAP {wd}d {side}{k}σ", b,
                            "vw_sigma_bands(1h)", timeframe="1h")

    members = L.collapse_same_family(reg.as_list(), atr_d)
    clusters = L.cluster(members, atr_d)
    return reg, members, clusters


# ═══════════════════════════════════════════════════════════════ THE TOLL

def grid_toll() -> pd.DataFrame:
    """The ORACLE GRID per-lens NET toll table, cut='ALL'. C-2's table."""
    if not GRID_PARQUET.exists():
        raise FileNotFoundError(f"HALT: ORACLE GRID absent at {GRID_PARQUET}; "
                                "C-2 forbids a cost-free number, so there is no "
                                "degraded mode. Rebuild with census2b_oracle.py.")
    g = pd.read_parquet(GRID_PARQUET)
    return g[g["cut"] == "ALL"].reset_index(drop=True)


def toll_for(g: pd.DataFrame, tf: str, cls: str) -> float | None:
    row = g[(g["tf"] == tf) & (g["cls"] == cls)]
    if row.empty:
        return None
    v = float(row["toll_atr"].iloc[0])
    return v if np.isfinite(v) else None


def net_rr(reward: float, risk: float, toll_price: float) -> float | None:
    """REGISTER['NET_RR_FORM'], [VETO]. No cost-free ratio is ever returned."""
    den = risk + toll_price
    if not np.isfinite(den) or den <= 0:
        return None
    v = (reward - toll_price) / den
    return float(v) if np.isfinite(v) else None


# ═══════════════════════════════════════════════════════ THE MANTLE PAYLOAD
# C-7: rendered FROM the v4 payload pattern, never recomputed ad hoc.
# The v4 shape is reproduced exactly: {'meta', 'data'}; meta.sha256 is the sha
# of the DATA BLOCK (json.dumps(data, sort_keys=True, separators=(',',':'))),
# which is the sha the shipped VIZ-4 footers stamp. Threads, thread_sr,
# thread_k, disp orientation (EMA - price)/ATR, and the null-means-absent rule
# are all the v4 contract's, not this build's.

THREADS = list(P.ALL_EMAS)                       # 18 lengths, 9 .. 5000
THREAD_SR = [fam for L_ in THREADS for fam, m in P.RIBBONS.items() if L_ in m]
STATE_K = {"FAST": 20, "M": 20, "MH": 40, "H": 111, "VH": 327, "UH": 577}
THREAD_K = [STATE_K[s] for s in THREAD_SR]


def _r3(x):
    return None if x is None or not np.isfinite(x) else round(float(x), 3)


def mantle_payload(sym: str, h4: pd.DataFrame, bars: int) -> dict:
    """A NARROW mantle payload: the last `bars` bars at stride 1.

    The shipped v4 payloads are decimated (stride 8 at 1h, 92 at 5m), so a
    'last-96-bars' strip is NOT a slice of them — 96 bars is 12 columns at 1h
    and about one column at 5m. Rather than silently reinterpret 'bars' as
    'steps', this emits a fresh payload whose source slice is short enough
    that decimate() would give stride 1 and every bar survives. The shape is
    identical; only the window is narrow.
    """
    close = h4["close"].to_numpy("float64")
    high = h4["high"].to_numpy("float64")
    low = h4["low"].to_numpy("float64")
    ot = h4["open_time"].to_numpy("int64")
    atr_v = P.atr(high, low, close, P.ATR_LEN)

    df = pd.DataFrame({"open_time": ot, "close": close, "high": high,
                       "low": low, "atr": atr_v})
    for L_ in THREADS:
        v = P.ema(close, L_)
        v[: min(P.warm_bars(L_), len(v))] = np.nan
        df[f"e{L_}"] = v

    sl = slice(max(0, len(df) - bars), len(df))
    ts = [int(t) for t in ot[sl]]

    disp = []
    for L_ in THREADS:
        e = df[f"e{L_}"].to_numpy("float64")[sl]
        a = atr_v[sl]
        c = close[sl]
        with np.errstate(invalid="ignore", divide="ignore"):
            d = np.where(np.isfinite(e) & np.isfinite(a) & (a > 0), (e - c) / a, np.nan)
        disp.append([_r3(x) for x in d])

    knot, orient = {}, {}
    for fam in P.FAMILIES:
        fs = P.family_state(fam, df)
        k = fs["knot"][sl]
        o = fs["orient"][sl]
        knot[fam] = [None if int(x) == P.KN_NA else int(x) for x in k]
        orient[fam] = [None if int(x) == P.OR_NA else int(x) for x in o]

    data = {
        "asset": sym, "lens": REGISTER["LENS"]["value"],
        "threads": THREADS, "thread_sr": THREAD_SR, "thread_k": THREAD_K,
        "hem_lens": [12, 26], "rod_lens": [2618, 3618, 4236, 4618, 5000],
        "ts": ts, "disp": disp,
        "knot": knot, "orient": orient,
        "knot_codes": {"no": 0, "knot": 1, "absent": None},
        "orient_codes": {"bear-fanned": -1, "mixed": 0, "bull-fanned": 1, "absent": None},
    }
    blob = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    meta = {
        "payload": f"oracle_mantle_{sym}_{REGISTER['LENS']['value']}.json",
        "sha256": hashlib.sha256(blob).hexdigest(),
        "rows": sum(len(v) for v in disp) + len(ts),
        "bars": len(ts),
        "class": "DISPLAY-ONLY / operations",
        "downsample_rule": f"stride 1, anchored at the LAST bar: the last {len(ts)} "
                           f"source bars of the {REGISTER['LENS']['value']} lens; every "
                           f"bar survives (no decimation)",
        "note": "displacements are (EMA-price)/ATR; null = not woven, render ABSENT "
                "never zero; knot/orient null = NOT COMPUTED, which is not 'no knot'",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }
    return {"meta": meta, "data": data}


# ═══════════════════════════════════════════════════════════════ THE VIEW

def build_view(as_of_ms: int | None = None, log=print) -> dict:
    """Everything the render and the tape read. One pass, one substrate."""
    roster = list(REGISTER["ROSTER"]["value"])
    lens = REGISTER["LENS"]["value"]
    g = grid_toll()
    toll_tf, toll_cls = REGISTER["GRID_TOLL_KEY"]["value"]
    card_toll_atr = toll_for(g, toll_tf, toll_cls)
    if card_toll_atr is None:
        raise ValueError(f"HALT: no toll for {REGISTER['GRID_TOLL_KEY']['value']}")

    assets, payloads = [], {}
    for sym in roster:
        h4 = load_lens(sym, "4h")
        h1 = load_lens(sym, "1h", tail=24 * 400)
        if as_of_ms is not None:
            h4 = h4[h4["open_time"] <= as_of_ms].reset_index(drop=True)
            h1 = h1[h1["open_time"] <= as_of_ms].reset_index(drop=True)
        atr_d = daily_atr(h1)
        st = PE.stations_for(sym, h4)
        reg, members, clusters = level_registry(sym, h4, h1, atr_d)
        price = st.close
        lis = L.lines_in_sand(clusters, price, atr_d)

        scored = [c for c in clusters if c["score"] > 0]
        nearest = min(scored, key=lambda c: abs(c["mean"] - price)) if scored else None
        nearest_d = abs(nearest["mean"] - price) / atr_d if nearest else float("nan")
        heat = (nearest["score"] / (1.0 + nearest_d)) if nearest else 0.0

        pay = mantle_payload(sym, h4, REGISTER["MANTLE_BARS"]["value"])
        payloads[pay["meta"]["payload"]] = pay

        assets.append({
            "symbol": sym, "station": st, "atr_d": atr_d, "price": price,
            "clusters": clusters, "n_levels": len(reg), "lis": lis,
            "nearest": nearest, "nearest_d": nearest_d, "heat": heat,
            "payload_name": pay["meta"]["payload"], "payload_sha": pay["meta"]["sha256"],
            "card": trap_card(sym, h4, st, clusters, atr_d, card_toll_atr),
        })
        log(f"  {sym:14} {st.board_word:10} heat={heat:6.3f} levels={len(reg):3d} "
            f"clusters={len(clusters):3d} atr_d={atr_d:.6g}")

    assets.sort(key=lambda a: -a["heat"])
    return {
        "as_of_ms": assets[0]["station"].as_of_ms if assets else 0,
        "lens": lens, "assets": assets, "payloads": payloads,
        "grid": g, "card_toll_atr": card_toll_atr,
        "fired": fired_events(roster, as_of_ms, g, log=log),
    }


def f_close_at(h4, i: int) -> float:
    """The close of bar i on the lens frame — the rule card's entry price."""
    return float(h4["close"].to_numpy("float64")[i])


def trap_card(sym, h4, st, clusters, atr_d, toll_atr) -> dict | None:
    """C-6. A pre-framed if-then, never a recommendation.

    entry        — the rule card enters at the in-window 12/26 bar close.
    invalidation — tierc3_rules.struct_stop_4h: the structural 4h anchor with
                   the 0.5 ATR buffer, RAILED to at least 1.0 ATR (the F-3
                   ruling). Not re-derived here; the module is called.
    target       — the nearest cluster beyond entry on the trade's side.
    net R:R      — REGISTER['NET_RR_FORM'], toll from the ORACLE GRID.
    """
    live = [w for w in st.open_windows if w.admitted]
    if not live:
        return None
    w = max(live, key=lambda w: w.arm_i)
    direction = w.direction
    atr_l = st.atr

    # THE ENTRY ANCHOR. The rule card is explicit — "TRIGGER: first in-window 4h
    # 12/26 cross -> enter at that bar close" — so a TRIGGERED window's entry is
    # the CLOSE OF THE TRIGGER BAR, not today's close. Anchoring it to today's
    # close silently re-prices a card that already fired: on NEARUSDT that was a
    # 10.1 ATR drift, and every derived field (risk, target, net R:R) inherited
    # it. An ARMED window has not fired yet, so its entry is genuinely unknown
    # and the card is PROVISIONAL: the last close stands in as the reference and
    # says so, rather than pretending to a price the market has not printed.
    if w.trigger_i is not None:
        entry = float(f_close_at(h4, w.trigger_i))
        entry_basis = (f"close of the 12/26 trigger bar, {w.trigger_age_bars} bar(s) ago"
                       + (" — STALE" if w.trigger_stale else ""))
        provisional = False
    else:
        entry = st.close
        entry_basis = "PROVISIONAL — the 12/26 has not fired; last close stands in"
        provisional = True

    # THE STOP IS NOT COMPUTED HERE. tierc3_rules.struct_stop_4h is the ratified
    # anchor: nearest confirmed 4h (5,5) pivot strictly beyond entry within the
    # lookback, offset 0.5 ATR, THEN railed to at least MIN_STOP_ATR. It returns
    # None for `no_struct_anchor`, and the rule card is explicit that the rail
    # does NOT invent a stop where structure names none — "A trade left with no
    # admissible anchor is NOT TAKEN. Printed both ways." So is this card.
    pv = V3.build_pivots_4h(h4["high"].to_numpy("float64"), h4["low"].to_numpy("float64"))
    stop = V3.struct_stop_4h(pv, st.as_of_i, entry, direction, atr_l,
                             lookback=REGISTER["PIVOT_LOOKBACK_BARS"]["value"],
                             min_stop_atr=PE.REGISTER["MIN_STOP_ATR"]["value"])
    if stop is None:
        return {
            "direction": "long" if direction == 1 else "short",
            "station": w.station, "arm_ms": w.arm_ms, "disp": w.disp,
            "not_taken": True, "provisional": provisional, "entry_basis": entry_basis,
            "trigger_age_bars": w.trigger_age_bars, "trigger_stale": w.trigger_stale,
            "entry": entry,
            "entry_rule": "at the close of the first in-window 4h 12/26 cross",
            "invalidation": None, "anchor": "NO ADMISSIBLE 4h PIVOT ANCHOR — NOT TAKEN",
            "risk": None, "target": None, "target_score": None, "reward": None,
            "toll_atr": toll_atr, "toll_price": toll_atr * atr_l, "net_rr": None,
            "wrong_if": ("no card exists: the rule card refuses a trade with no "
                         "admissible structural anchor, and the rail does not "
                         "invent one"),
        }
    stop_px = float(stop.stop_px)
    anchor = (f"4h swing pivot @bar {stop.anchor_bar} + "
              f"{PE.REGISTER['STOP_BUF_ATR']['value']} ATR buffer"
              + ("; RAIL BINDING at 1.0 ATR" if stop.rail_binding else "")
              + f"; {stop.n_eligible} eligible pivot(s)")
    risk = float(stop.r_dist)

    side = [c for c in clusters
            if (c["mean"] - entry) * direction > 0 and c["score"] > 0]
    tgt = min(side, key=lambda c: abs(c["mean"] - entry)) if side else None
    target_px = tgt["mean"] if tgt else None
    reward = abs(target_px - entry) if target_px is not None else None

    toll_price = toll_atr * atr_l
    rr = net_rr(reward, risk, toll_price) if reward is not None else None
    return {
        "direction": "long" if direction == 1 else "short",
        "station": w.station, "arm_ms": w.arm_ms, "disp": w.disp,
        "not_taken": False, "provisional": provisional, "entry_basis": entry_basis,
        "trigger_age_bars": w.trigger_age_bars, "trigger_stale": w.trigger_stale,
        "entry": entry, "entry_rule": "at the close of the first in-window 4h 12/26 cross",
        "invalidation": stop_px, "anchor": anchor, "risk": risk,
        "target": target_px, "target_score": (tgt["score"] if tgt else None),
        "reward": reward, "toll_atr": toll_atr, "toll_price": toll_price,
        "net_rr": rr,
        "wrong_if": ("a counter 4h 12/89 cross, or the 4h 89/316 turning against "
                     "the window — either closes it (rule card BELL)"),
    }


def fired_events(roster, as_of_ms, g, log=print) -> dict:
    """C-8. Yesterday's fired events, classified against the GRID's NET table.

    RECORDING, not aggregating: this counts events and prints the GRID's
    already-filed NET for that (lens, class). It computes no outcome of its
    own — that would be census work under G-7.
    """
    hours = REGISTER["FIRED_WINDOW_HOURS"]["value"]
    out, warm_note = [], {}
    tf_ms = {"5m": 300_000, "15m": 900_000, "30m": 1_800_000,
             "1h": 3_600_000, "4h": 14_400_000}
    warm = P.warm_bars(316)
    for tf in REGISTER["GRID_LENSES"]["value"]:
        src_tf, step = ("15m", 2) if tf == "30m" else (tf, 1)
        need = warm * 3 + int(hours * 3_600_000 / tf_ms[tf]) + 10
        for sym in roster:
            try:
                df = load_lens(sym, src_tf, tail=need * step + 50)
            except FileNotFoundError:
                continue
            if step > 1:
                r = ST.resample_ohlcv(df["open_time"].to_numpy("int64"),
                                      df["open"].to_numpy("float64"),
                                      df["high"].to_numpy("float64"),
                                      df["low"].to_numpy("float64"),
                                      df["close"].to_numpy("float64"),
                                      df["volume"].to_numpy("float64"), tf_ms[tf])
                df = pd.DataFrame({k: r[k] for k in
                                   ("open_time", "open", "high", "low", "close", "volume")})
            if as_of_ms is not None:
                df = df[df["open_time"] <= as_of_ms].reset_index(drop=True)
            if len(df) < warm + 5:
                continue
            f = PE.build_frame(df)
            x = PE.crosses(f)
            cut = int(f.open_ms[-1]) - hours * 3_600_000
            recent = f.open_ms >= cut
            for cls, series in (("12_89", x["w_up"] | x["w_dn"]),
                                ("12_26 IN-WINDOW", x["t_up"] | x["t_dn"]),
                                ("89_316", x["b_up"] | x["b_dn"])):
                n = int(np.count_nonzero(series & recent))
                if n:
                    out.append({"lens": tf, "asset": sym, "cls": cls, "n": n})
            warm_note[tf] = (f"EMA warm-up: {warm} bars needed for e316; "
                             f"{len(df)} loaded on {tf}"
                             + (" (derived from 15m by resample)" if step > 1 else ""))
    rows = {}
    for e in out:
        k = (e["lens"], e["cls"])
        rows.setdefault(k, {"lens": e["lens"], "cls": e["cls"], "n": 0, "assets": []})
        rows[k]["n"] += e["n"]
        rows[k]["assets"].append(f"{e['asset'].replace('USDT','')}x{e['n']}")
    for k, r in rows.items():
        row = g[(g["tf"] == r["lens"]) & (g["cls"] == r["cls"])]
        for h in ("H20", "H100"):
            v = float(row[f"{h}_net"].iloc[0]) if not row.empty else float("nan")
            r[f"{h}_net"] = None if not np.isfinite(v) else round(v, 6)
        t = float(row["toll_atr"].iloc[0]) if not row.empty else float("nan")
        r["toll_atr"] = None if not np.isfinite(t) else round(t, 6)
    log(f"  fired events in the last {hours}h: "
        f"{sum(r['n'] for r in rows.values())} across {len(rows)} (lens, class) cells")
    return {"rows": sorted(rows.values(), key=lambda r: (r["lens"], r["cls"])),
            "hours": hours, "warm_note": warm_note}


# ═══════════════════════════════════════════════════════════════ THE RENDER

def _f(x, nd=6):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{x:,.{nd}g}"


def svg_spaghetti(view: dict) -> str:
    """C-4. One panel. Each asset's ATR-normalised path from its LAST 89/316
    tide flip. Event-anchored, exactly as the operator's two pins name it."""
    W, H, PAD = 920, 300, 34
    paths, legend = [], []
    series = []
    for a in view["assets"]:
        st = a["station"]
        if st.tide_flip_i is None:
            continue
        h4 = load_lens(a["symbol"], "4h")
        c = h4["close"].to_numpy("float64")
        i0 = st.tide_flip_i
        if i0 >= len(c) - 1:
            continue
        seg = (c[i0:] - c[i0]) / a["atr_d"]
        series.append((a["symbol"], seg, st.tide_flip_dir))
    if not series:
        return "<p class='muted'>no tide flip in loaded history</p>"
    n_max = max(len(s) for _, s, _ in series)
    v_max = max(float(np.nanmax(np.abs(s))) for _, s, _ in series) or 1.0
    for k, (sym, seg, dirn) in enumerate(series):
        hue = int(360 * k / max(1, len(series)))
        pts = []
        for i, v in enumerate(seg):
            x = PAD + (W - 2 * PAD) * (i / max(1, n_max - 1))
            y = H / 2 - (H / 2 - PAD) * (v / v_max)
            pts.append(f"{x:.1f},{y:.1f}")
        paths.append(f'<polyline points="{" ".join(pts)}" fill="none" '
                     f'stroke="hsl({hue},55%,58%)" stroke-width="1.6" opacity="0.85"/>')
        legend.append(f'<span style="color:hsl({hue},55%,58%)">■</span> '
                      f'{html.escape(sym.replace("USDT",""))} '
                      f'<span class="muted">({dirn}, {len(seg)}b)</span>')
    axis = (f'<line x1="{PAD}" y1="{H/2}" x2="{W-PAD}" y2="{H/2}" '
            f'stroke="#5b5148" stroke-dasharray="3 3"/>')
    return (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
            f'aria-label="ATR-normalised paths since each asset\'s last 89/316 tide flip">'
            f'{axis}{"".join(paths)}'
            f'<text x="{PAD}" y="16" fill="#8a7f72" font-size="11">'
            f'+{v_max:.2f} ATR</text>'
            f'<text x="{PAD}" y="{H-6}" fill="#8a7f72" font-size="11">'
            f'-{v_max:.2f} ATR</text></svg>'
            f'<div class="legend">{" · ".join(legend)}</div>')


MANTLE_JS = """
// heatCanvas — ported from the shipped VIZ-4 render, same law, same colours.
// disp is thread-major; null is ABSENT (alpha 0), never zero. Row order is
// flipped: rod on TOP, hem at the BOTTOM, exactly as the v4 strip draws it.
function divRGB(v){var t=Math.min(1,Math.log10(1+Math.abs(v)/0.5)/2.6);
  var a=[233,220,195],b=v>=0?[85,148,155]:[198,113,57],k=0.15+0.85*t;
  return [a[0]+(b[0]-a[0])*k,a[1]+(b[1]-a[1])*k,a[2]+(b[2]-a[2])*k];}
function heatCanvas(pl){var d=pl.data,nT=d.threads.length,nX=d.ts.length;
  var cv=document.createElement('canvas');cv.width=nX;cv.height=nT;
  var cx=cv.getContext('2d'),im=cx.createImageData(nX,nT);
  for(var i=0;i<nT;i++){var row=nT-1-i,sr=d.thread_sr[i];
    for(var j=0;j<nX;j++){var v=d.disp[i][j],o=4*(row*nX+j);
      if(v===null||v===undefined){im.data[o+3]=0;continue;}
      var c=divRGB(v),kn=d.knot[sr]&&d.knot[sr][j]===1?0.45:1;
      im.data[o]=c[0]*kn;im.data[o+1]=c[1]*kn;im.data[o+2]=c[2]*kn;im.data[o+3]=255;}}
  cx.putImageData(im,0,0);return cv;}
function paintStrips(){var P=window.__PAYLOADS||{};
  document.querySelectorAll('canvas[data-payload]').forEach(function(el){
    var pl=P[el.getAttribute('data-payload')];if(!pl)return;
    var src=heatCanvas(pl),cx=el.getContext('2d');
    cx.imageSmoothingEnabled=true;cx.drawImage(src,0,0,el.width,el.height);});}
document.addEventListener('DOMContentLoaded',paintStrips);
"""


def render_html(view: dict, date_str: str, canon_sha: str) -> str:
    lens = view["lens"]
    a0 = view["assets"]
    as_of = datetime.fromtimestamp(view["as_of_ms"] / 1000, timezone.utc)

    board = []
    for a in a0:
        st = a["station"]
        w = st.board_word
        lis_txt = []
        for key in ("above", "below"):
            ln = a["lis"].get(key) if isinstance(a["lis"], dict) else None
            if ln and ln.get("mean") is not None:
                lis_txt.append(f"{key} {_f(ln['mean'])} "
                               f"<span class='muted'>(score {ln.get('score','—')})</span>")
        board.append(
            f"<tr class='w-{w.lower()}'><td class='sym'>{html.escape(a['symbol'].replace('USDT',''))}</td>"
            f"<td><span class='chip t-{st.tide}'>{st.tide}</span></td>"
            f"<td class='num'>{a['nearest_d']:.2f}<span class='muted'> ATR</span></td>"
            f"<td class='num muted'>{a['nearest']['score'] if a['nearest'] else '—'}</td>"
            f"<td class='lis'>{' · '.join(lis_txt) or '<span class=muted>—</span>'}</td>"
            f"<td class='post w-{w.lower()}'>{w}</td>"
            f"<td class='muted small'>{html.escape(st.board_reason)}</td>"
            f"<td class='num muted'>{a['heat']:.3f}</td></tr>")

    cards = []
    for a in a0:
        c = a["card"]
        if not c:
            continue
        cards.append(f"""
<div class="card">
  <div class="card-h"><b>{html.escape(a['symbol'].replace('USDT',''))}</b>
    <span class="chip d-{c['direction']}">{c['direction']}</span>
    <span class="chip w-{c['station'].lower()}">{c['station']}</span>
    {'<span class="chip stale">STALE TRIGGER</span>' if c.get('trigger_stale') else ''}
    {'<span class="chip prov">PROVISIONAL</span>' if c.get('provisional') else ''}
    <span class="muted small">displacement {c['disp']:.2f} ATR at the arming</span></div>
  <table class="kv">
    <tr><td>IF</td><td>{html.escape(c['entry_rule'])}</td></tr>
    <tr><td>ENTRY</td><td class="num">{_f(c['entry'])}
        <span class="muted">— {html.escape(c['entry_basis'])}</span></td></tr>
    <tr><td>INVALIDATION</td><td class="num">{_f(c['invalidation'])}
        <span class="muted">— {html.escape(c['anchor'])}; risk {_f(c['risk'])}</span></td></tr>
    <tr><td>TARGET</td><td class="num">{_f(c['target'])}
        <span class="muted">cluster score {c['target_score'] if c['target_score'] is not None else '—'}</span></td></tr>
    <tr><td>NET R:R</td><td class="num big">{'—' if c['net_rr'] is None else f"{c['net_rr']:.2f}"}
        <span class="muted">after toll {c['toll_atr']:.6f} ATR = {_f(c['toll_price'])}
        · {html.escape(REGISTER['NET_RR_FORM']['value'])} [VETO]</span></td></tr>
    <tr><td>WHAT PROVES ME WRONG</td><td>{html.escape(c['wrong_if'])}</td></tr>
  </table>
</div>""")

    watch = []
    for a in a0:
        st = a["station"]
        rows = []
        for w in st.open_windows:
            rows.append(f"<tr><td>{'long' if w.direction==1 else 'short'}</td>"
                        f"<td class='num'>{w.age_bars}</td>"
                        f"<td class='num'>{w.disp:.2f}</td>"
                        f"<td>{'TRIGGERED' if w.trigger_i is not None else 'waiting'}</td></tr>")
        tbl = ("<table class='watch'><tr><th>dir</th><th>age (4h bars)</th>"
               "<th>disp ATR</th><th>trigger</th></tr>" + "".join(rows) + "</table>"
               ) if rows else "<p class='muted small'>no open window</p>"
        watch.append(f"""
<div class="wcell">
  <div class="wh"><b>{html.escape(a['symbol'].replace('USDT',''))}</b>
      <span class="chip w-{st.board_word.lower()}">{st.board_word}</span></div>
  {tbl}
  <canvas width="960" height="180" class="strip"
          data-payload="{html.escape(a['payload_name'])}"></canvas>
  <div class="stripfoot">payload {html.escape(a['payload_name'])} sha256
      {a['payload_sha']} · rod 5000 top, hem 9 bottom · dark pinch = knot ·
      holes = unwoven</div>
</div>""")

    fired = []
    for r in view["fired"]["rows"]:
        toll_s = "—" if r["toll_atr"] is None else format(r["toll_atr"], ".6f")
        h20_s = "—" if r["H20_net"] is None else format(r["H20_net"], "+.4f")
        h100_s = "—" if r["H100_net"] is None else format(r["H100_net"], "+.4f")
        fired.append(f"<tr><td>{r['lens']}</td><td>{html.escape(r['cls'])}</td>"
                     f"<td class='num'>{r['n']}</td>"
                     f"<td class='num'>{toll_s}</td>"
                     f"<td class='num'>{h20_s}</td>"
                     f"<td class='num'>{h100_s}</td>"
                     f"<td class='muted small'>{html.escape(', '.join(r['assets']))}</td></tr>")

    r1 = r1_block(view)

    def _chip(src):
        return ('<span class="chip defer">DEFERRED-TO-BR2</span>'
                if src.get("deferred_to") == "BR-2"
                else '<span class="chip">[VETO]</span>')

    veto = []
    rows = ([(k, v) for k, v in PE.REGISTER.items() if not v["ruled"]]
            + [(k, v) for k, v in REGISTER.items() if not v["ruled"]]
            + [(f"CANON.{k}", v) for k, v in PE.CANON.items() if not v["ruled"]])
    try:
        import oracle_topup as _TU
        rows += [(k, v) for k, v in _TU.REGISTER.items() if not v.get("ruled", True)]
    except Exception:
        pass
    for name, src in rows:
        veto.append(f"<tr><td><code>{html.escape(name)}</code></td>"
                    f"<td>{_chip(src)}</td>"
                    f"<td class='num'>{html.escape(str(src.get('value', 'gate')))}</td>"
                    f"<td class='small'>{html.escape(src['source'])}</td></tr>")

    pay_js = []
    for name, pl in view["payloads"].items():
        blob = json.dumps(pl, separators=(",", ":"), ensure_ascii=False)
        pay_js.append(f'window.__PAYLOADS=window.__PAYLOADS||{{}};'
                      f'window.__PAYLOADS[{json.dumps(name)}]={blob};')

    shas = " · ".join(f"payload {n} sha256 {p['meta']['sha256']}"
                      for n, p in view["payloads"].items())
    stale_banner = staleness_banner(view)

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>THE ORACLE — {date_str}</title>
<style>
:root{{--bg:#14120f;--ink:#e9dcc3;--mut:#8a7f72;--line:#2b2620;--teal:#55949b;--terra:#c67139;--sage:#a3b581}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}}
.wrap{{max-width:1180px;margin:0 auto;padding:28px 20px 80px}}
h1{{font-size:20px;letter-spacing:.14em;margin:0 0 4px}}
h2{{font-size:13px;letter-spacing:.18em;color:var(--mut);margin:34px 0 10px;
   border-bottom:1px solid var(--line);padding-bottom:6px;text-transform:uppercase}}
.banner{{border:1px solid var(--terra);color:var(--terra);padding:8px 12px;
   font-size:11px;letter-spacing:.1em;margin:14px 0 6px}}
.stale{{border:2px solid var(--terra);background:rgba(198,113,57,.14);color:var(--terra);
   padding:10px 12px;font-size:12px;font-weight:700;letter-spacing:.1em;margin:14px 0 6px}}
.chip.defer{{color:var(--sage);border-color:var(--sage)}}
table{{width:100%;border-collapse:collapse;font-size:12.5px}}
th{{text-align:left;color:var(--mut);font-weight:400;font-size:11px;
   letter-spacing:.1em;border-bottom:1px solid var(--line);padding:6px 8px}}
td{{padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.muted,.small{{color:var(--mut)}} .small{{font-size:11px}}
.sym{{font-weight:700;letter-spacing:.06em}}
.chip{{display:inline-block;padding:1px 7px;border:1px solid var(--line);
   border-radius:9px;font-size:10.5px;letter-spacing:.08em}}
.t-long{{color:var(--teal);border-color:var(--teal)}}
.t-short{{color:var(--terra);border-color:var(--terra)}}
.d-long{{color:var(--teal);border-color:var(--teal)}}
.d-short{{color:var(--terra);border-color:var(--terra)}}
.stale{{color:var(--terra);border-color:var(--terra);font-weight:700}}
.prov{{color:var(--mut);border-color:var(--mut)}}
.post{{font-weight:700;letter-spacing:.1em}}
.w-triggered{{color:var(--sage)}} .w-armed{{color:var(--teal)}}
.w-dead{{color:var(--terra)}} .w-stalking{{color:var(--mut)}}
.card{{border:1px solid var(--line);padding:12px 14px;margin:10px 0}}
.card-h{{display:flex;gap:10px;align-items:center;margin-bottom:8px}}
.kv td:first-child{{color:var(--mut);width:190px;font-size:11px;letter-spacing:.08em}}
.big{{font-size:17px}}
.wcell{{border:1px solid var(--line);padding:12px 14px;margin:10px 0}}
.wh{{display:flex;gap:10px;align-items:center;margin-bottom:6px}}
.strip{{width:100%;height:auto;display:block;margin-top:8px;background:#181512;border-radius:6px}}
.stripfoot{{font-size:10px;color:var(--mut);word-break:break-all;margin-top:4px}}
.legend{{font-size:11px;color:var(--mut);margin-top:6px}}
pre.r1{{background:#0e0c0a;border:1px solid var(--line);padding:12px;
   font-size:12px;overflow-x:auto;white-space:pre}}
footer{{margin-top:40px;border-top:1px solid var(--line);padding-top:14px;
   font-size:10.5px;color:var(--mut);word-break:break-word}}
</style></head><body><div class="wrap">
<h1>THE ORACLE — {date_str}</h1>
{stale_banner}<div class="banner">DISPLAY-ONLY · OPERATIONS · not study evidence · no journal is read ·
no outcome is scored · rules are born only under G-7 on exploration-classic</div>
<p class="small muted">lens {lens} · as-of bar {as_of.strftime('%Y-%m-%dT%H:%MZ')} ·
roster {len(a0)} · posture canon v1 sha256 {canon_sha}</p>

<h2>The Board — where is business possible today</h2>
<table><tr><th>asset</th><th>regime</th><th>dist</th><th>score</th>
<th>two lines in the sand</th><th>posture</th><th>why</th><th>heat</th></tr>
{''.join(board)}</table>
<p class="small muted">heat = {html.escape(REGISTER['HEAT']['value'])} [VETO — proposed,
not ruled]. Both inputs print in the row so the sort is auditable.</p>

<h2>Trap Cards — pre-framed if-thens</h2>
{''.join(cards) or '<p class="muted">no admitted open window on the roster.</p>'}

<h2>The Watch — living 12/89 windows</h2>
{''.join(watch)}

<h2>Spaghetti — anchored at each asset's last 89/316 tide flip</h2>
{svg_spaghetti(view)}

<h2>ORACLE GRID footer — the last {view['fired']['hours']}h of fired events</h2>
<table><tr><th>lens</th><th>class</th><th>fired</th><th>toll ATR</th>
<th>GRID NET H20</th><th>GRID NET H100</th><th>assets</th></tr>{''.join(fired)}</table>
<p class="small muted">NET is the ORACLE GRID's own filed median-minus-toll for that
(lens, class) cell — panel-pooled over 5 assets, m=0, unranked. It is NOT an outcome
computed from these events; this organ records events and reads the grid. Toll is not
comparable across assets. H20 at 4h is infeasible by construction (0 bars) and prints —.</p>

<h2>R1 — alert prices, paste-ready</h2>
<pre class="r1">{html.escape(r1)}</pre>

<h2>Appendix — posture canon v1 · the rows still open</h2>
<p class="small muted">BR-1 Amendment A2 (operator, 2026-08-16) ruled the naming, the trigger
pair, the net R:R form and the schedule. The rows below are what remains: each is
DEFERRED-TO-BR2, which proposes a measured value from a week of D-7 distributions.
Nothing self-adopts.</p>
<table><tr><th>constant</th><th>disposition</th><th>value</th><th>why it is not law</th></tr>
{''.join(veto)}</table>

<footer>
DISPLAY-ONLY · operations · {date_str} · lens {lens} ·
posture canon v1 sha256 {canon_sha} · {shas} ·
displacements are (EMA−price)/ATR · analytics {ANALYTICS_VERSION} sha {analytics_sha()} ·
net R:R = {html.escape(REGISTER['NET_RR_FORM']['value'])}, toll from the ORACLE GRID
(census-2B, oracle_grid.parquet) — no cost-free number prints on this page.<br>
CERTIFIED: {html.escape(' · '.join(CERTIFIED))}.<br>
NOT CERTIFIED: {html.escape(' · '.join(NOT_CERTIFIED))}.<br>
No claim is made or implied. Nothing here is scored. Promotion requires registration
under G-7 on exploration-classic.
</footer></div>
<script>{''.join(pay_js)}</script>
<script>{MANTLE_JS}</script>
</body></html>"""


# ═══════════════════════════════════════════ A2-7 · THE STALENESS BANNER
# BR-1 Amendment A2-7 (operator, 2026-08-16), a PARTIAL remedy for finding T-3:
# launchd runs a missed calendar job on wake, so a laptop asleep at 06:45 can
# fetch AFTER the 07:00 Oracle has already rendered, and the brief would be a
# day stale with nothing to say so. This banner says so. It is display-only and
# [VETO-by-firing]: the threshold earns its keep the first time it fires.
#
# It does NOT close T-3. The wake-order race — should the Oracle refuse to
# render at all on a stale cache? — is still an open ruling.
STALE_LENS_PERIODS = 2

LENS_MS = {"5m": 300_000, "15m": 900_000, "30m": 1_800_000,
           "1h": 3_600_000, "4h": 14_400_000, "12h": 43_200_000}


def staleness_banner(view: dict) -> str:
    """A2-7. Fires when the newest cache bar is older than STALE_LENS_PERIODS
    lens periods AT RENDER TIME. The as-of stamp prints regardless — the banner
    adds an alarm, it never replaces the provenance."""
    step = LENS_MS[view["lens"]]
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    age_ms = now_ms - int(view["as_of_ms"])
    limit = STALE_LENS_PERIODS * step
    if age_ms <= limit:
        return ""
    return (f'<div class="stale">STALE DATA — the newest {view["lens"]} bar is '
            f'{age_ms / 3_600_000:.1f}h old, over the {STALE_LENS_PERIODS}-lens-period '
            f'limit of {limit / 3_600_000:.1f}h. The top-up may not have run. Every '
            f'number below is computed from that bar, and the as-of stamp names it.</div>')


def r1_block(view: dict) -> str:
    """C-9 / F-BR-7. Prices only. Grammar: <SYMBOL> <TAG> <PRICE>, one per line.
    No prose, no advice, no ratio — a parser must be able to read every line."""
    out = []
    for a in view["assets"]:
        sym = a["symbol"]
        lis = a["lis"] if isinstance(a["lis"], dict) else {}
        for key, tag in (("above", "LIS_ABOVE"), ("below", "LIS_BELOW")):
            ln = lis.get(key)
            if ln and ln.get("mean") is not None:
                out.append(f"{sym} {tag} {float(ln['mean']):.10g}")
        c = a["card"]
        if c:
            if c["invalidation"] is not None:
                out.append(f"{sym} INVAL {float(c['invalidation']):.10g}")
            if c["target"] is not None:
                out.append(f"{sym} TARGET {float(c['target']):.10g}")
    return "\n".join(out)


# ═══════════════════════════════════════════════════════════ D-4 THE TAPE

TAPE_COLS = ["as_of_ms", "as_of_iso", "asset", "lens", "station", "tide",
             "tide_flip_ms", "direction", "arm_ms", "age_bars", "disp_atr",
             "d_ok", "trigger_ms", "trigger_on_arming_bar", "closed_by",
             "close_px", "atr_lens", "atr_daily", "n_levels", "n_clusters",
             "nearest_cluster_atr", "nearest_cluster_score", "heat",
             "payload_sha"]


def write_tape(view: dict, date_str: str) -> tuple[Path, str, int]:
    """C-10 / D-4. One event stream, two renders — HTML for the operator,
    parquet for TC4. RECORDING only: not one outcome column exists here."""
    TAPE_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for a in view["assets"]:
        st = a["station"]
        base = {
            "as_of_ms": st.as_of_ms,
            "as_of_iso": datetime.fromtimestamp(st.as_of_ms / 1000, timezone.utc).isoformat(),
            "asset": a["symbol"], "lens": st.lens, "station": st.board_word,
            "tide": st.tide, "tide_flip_ms": st.tide_flip_ms,
            "close_px": st.close, "atr_lens": st.atr, "atr_daily": a["atr_d"],
            "n_levels": a["n_levels"], "n_clusters": len(a["clusters"]),
            "nearest_cluster_atr": a["nearest_d"],
            "nearest_cluster_score": (a["nearest"]["score"] if a["nearest"] else None),
            "heat": a["heat"], "payload_sha": a["payload_sha"],
        }
        wins = list(st.open_windows) + list(st.recent_dead)
        if not wins:
            rows.append({**base, "direction": None, "arm_ms": None, "age_bars": None,
                         "disp_atr": None, "d_ok": None, "trigger_ms": None,
                         "trigger_on_arming_bar": None, "closed_by": None})
        for w in wins:
            rows.append({**base, "station": w.station, "direction": w.direction,
                         "arm_ms": w.arm_ms, "age_bars": w.age_bars, "disp_atr": w.disp,
                         "d_ok": w.d_ok, "trigger_ms": w.trigger_ms,
                         "trigger_on_arming_bar": w.trigger_on_arming_bar,
                         "closed_by": w.closed_by or None})
    df = pd.DataFrame(rows, columns=TAPE_COLS)
    p = TAPE_DIR / f"oracle_tape_{date_str}.parquet"
    df.to_parquet(p, index=False)
    b = p.read_bytes()
    return p, hashlib.sha256(b).hexdigest(), len(b)


# ═══════════════════════════════════════════════ D-7 THE CALIBRATION LOGGER
# A1-4, verbatim: "display-machinery distribution stats ONLY (per-asset level
# counts, cluster widths, collapse events, LIS distances, maturity-withheld
# fractions, window ages). NO outcome fields, NO signal-performance fields —
# enforced by fixture F-BR-10."
#
# THE BANNED VOCABULARY IS DECLARED HERE, IN CODE, so F-BR-10 scans a list and
# not a mood. If a future edit adds an outcome column, the fixture fails.

BANNED_CALIBRATION_KEYS = (
    "win", "loss", "pnl", "r_multiple", "net_r", "gross_r", "return", "outcome",
    "hit_rate", "expectancy", "profit", "equity", "mfe", "mae", "term_h20",
    "term_h100", "sharpe", "edge", "score_of_signal", "accuracy", "precision",
)


def write_calibration(view: dict, date_str: str, slot: str) -> tuple[Path, str, int]:
    CAL_DIR.mkdir(parents=True, exist_ok=True)
    per_asset = []
    for a in view["assets"]:
        st = a["station"]
        widths = [ (max(m["level"] for m in c["members"]) -
                    min(m["level"] for m in c["members"])) / a["atr_d"]
                   for c in a["clusters"] if c["member_count"] > 1 ]
        lis = a["lis"] if isinstance(a["lis"], dict) else {}
        per_asset.append({
            "asset": a["symbol"],
            "level_count": a["n_levels"],
            "cluster_count": len(a["clusters"]),
            "collapse_events": a["n_levels"] - sum(c["member_count"] for c in a["clusters"]),
            "cluster_width_atr_p50": (round(float(np.median(widths)), 6) if widths else None),
            "cluster_width_atr_max": (round(float(np.max(widths)), 6) if widths else None),
            "lis_distance_atr": {k: (round(abs(lis[k]["mean"] - a["price"]) / a["atr_d"], 6)
                                     if lis.get(k) and lis[k].get("mean") is not None else None)
                                 for k in ("above", "below")},
            # REPAIRED 2026-08-21, two defects on one line, both found by the
            # T-3 diagnostic. (1) `lines_in_sand` writes None on a side with no
            # qualifying cluster (levels.py `out[side] = None`), so the key is
            # PRESENT holding None and `.get(k, {})` never reaches its default —
            # `.get("fallback")` on None raised AttributeError and killed every
            # scheduled run from 2026-08-20T10:00Z. The line directly above already
            # guarded this way; this one did not. (2) the flag was read from a
            # "fallback" key that `lines_in_sand` never writes — it marks the
            # fallback with source="fallback" — so this field recorded False for
            # every asset on every side since 2026-08-16 and could not have said
            # otherwise. None here means NO LINE on that side, matching the None
            # convention `lis_distance_atr` above already uses.
            "lis_fallback_used": {k: (None if not lis.get(k)
                                      else lis[k].get("source") == "fallback")
                                  for k in ("above", "below")},
            "maturity_withheld_fraction": 0.0,
            "open_window_ages_bars": [w.age_bars for w in st.open_windows],
            "open_window_disp_atr": [round(w.disp, 6) for w in st.open_windows],
            "station": st.board_word,
            "nearest_cluster_atr": (round(a["nearest_d"], 6)
                                    if np.isfinite(a["nearest_d"]) else None),
            "heat": round(a["heat"], 6),
        })
    doc = {
        "class": "DISPLAY-MACHINERY DISTRIBUTIONS ONLY — no outcome fields, no "
                 "signal-performance fields (BR-1 Amendment A1-4, enforced by F-BR-10)",
        "date": date_str, "slot": slot, "lens": view["lens"],
        "as_of_ms": view["as_of_ms"],
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "posture_canon_sha256": PE.canon_sha(),
        "thresholds_in_force": {
            "collapse_atr": L.COLLAPSE_ATR, "cluster_atr": L.CLUSTER_ATR,
            "lis_atr": L.LIS_ATR, "family_cap": L.FAMILY_CAP,
            "maturity_line_min": VW.LINE_MIN_BARS, "maturity_band_min": VW.BAND_MIN_BARS,
            "d_displacement": PE.REGISTER["D_DISPLACEMENT"]["value"],
            "dead_memory_bars": PE.REGISTER["DEAD_MEMORY_BARS"]["value"],
        },
        "veto_rows_awaiting_ruling": (
            [k for k, v in PE.REGISTER.items() if not v["ruled"]]
            + [k for k, v in REGISTER.items() if not v["ruled"]]
            + [f"CANON.{k}" for k, v in PE.CANON.items() if not v["ruled"]]),
        "station_distribution": {w: sum(1 for a in view["assets"]
                                        if a["station"].board_word == w)
                                 for w in PE.STATION_WORDS},
        "fired_event_cells": len(view["fired"]["rows"]),
        "per_asset": per_asset,
    }
    p = CAL_DIR / f"oracle_calibration_{date_str}_{slot}.json"
    b = json.dumps(doc, indent=1, sort_keys=True).encode("utf-8")
    p.write_bytes(b)
    return p, hashlib.sha256(b).hexdigest(), len(b)


# ═══════════════════════════════════════════════════════════════════ MAIN

def run(slot: str = "full", as_of_ms: int | None = None, log=print) -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PAYLOAD_DIR.mkdir(parents=True, exist_ok=True)
    now_ba = datetime.now(tz=None).astimezone()
    date_str = now_ba.strftime("%Y-%m-%d")

    log(f"ORACLE {slot} · {date_str} · lens {REGISTER['LENS']['value']}")
    canon_p, canon_sha, canon_b = PE.write_canon_json()
    log(f"  posture_canon.json {canon_b} B sha256 {canon_sha}")

    view = build_view(as_of_ms=as_of_ms, log=log)

    for name, pl in view["payloads"].items():
        (PAYLOAD_DIR / name).write_bytes(
            json.dumps(pl, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))

    doc = render_html(view, date_str, canon_sha)
    out = OUT_DIR / f"oracle_{date_str}.html"
    out.write_text(doc, encoding="utf-8")
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    log(f"  {out} {out.stat().st_size:,} B sha256 {sha}")

    tape_p, tape_sha, tape_b = write_tape(view, date_str)
    log(f"  {tape_p} {tape_b:,} B sha256 {tape_sha}")
    cal_p, cal_sha, cal_b = write_calibration(view, date_str, slot)
    log(f"  {cal_p} {cal_b:,} B sha256 {cal_sha}")

    return {"html": out, "html_sha": sha, "html_bytes": out.stat().st_size,
            "tape": tape_p, "tape_sha": tape_sha,
            "calibration": cal_p, "calibration_sha": cal_sha,
            "canon": canon_p, "canon_sha": canon_sha, "view": view}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    slot = "full"
    if "--slot" in argv:
        slot = argv[argv.index("--slot") + 1]
    run(slot=slot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
