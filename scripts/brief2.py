#!/usr/bin/env python
"""brief2.py -- the BRIEF-2 layers and the decision instrument.

CONTRACT v4 Amendment 2, §3-§7.  Pure computation over already-loaded klines,
kept OUT of daily_brief.py so the v1.1 monitor and its F-B1..F-B8 fixtures keep
working unchanged while the new layers are built and fixtured beside them.

WHAT THIS IS NOT (§11, reprinted because it is load-bearing).  Not a signal
service.  Not sizing advice.  Not study evidence.  Confluence scores measure
AGREEMENT BETWEEN TOOLS, not edge.  R:R measures GEOMETRY, not probability.
Whether any of it predicts anything is census work under G-7.

THE SEQUENCING RULE (§2.2) is the reason this module is shaped the way it is.
Part II must be reconstructable BY HAND from Part I's printed numbers plus the
rules header -- no hidden inputs.  So every function here takes numbers that
Part I already prints, and `decision_instrument` in particular reads only the
level registry and the printed rules.  If a future edit needs a quantity Part I
does not print, the fix is to print it, never to reach past the report.

ADOPTION IS NOT PARITY.  Nothing here may be trusted until the operator's parity
readings are returned and matched; PARITY_BANNER prints on every render until
the certification flag is set, and F-B33 asserts it.
"""

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import analytics                                                   # noqa: E402
from analytics import levels as L                                  # noqa: E402
from analytics import momentum as M                                # noqa: E402
from analytics import nesting as N                                 # noqa: E402
from analytics import profile as P                                 # noqa: E402
from analytics import structure as S                               # noqa: E402
from analytics import volatility as V                              # noqa: E402
from analytics import vwap as W                                    # noqa: E402

DAY_MS = 86_400_000
HOUR_MS = 3_600_000

# §3.1 -- ONE VOCABULARY EVERYWHERE, for both rolling VWAPs and windowed
# profiles.  The v1.1 5d and 20d windows are RETIRED: they near-duplicated 7d and
# 30d, and in a system that scores by counting agreement, near-duplicates inflate
# scores while adding nothing.
WINDOWS = ("prior-day", "7d", "30d", "90d", "365d")
RVWAP_WINDOWS = (7, 30, 90, 365)
SIGMAS = (1, 2, 3)

# §6.1 -- the 1M plane carries price and volume structure ONLY.  A closed-bar
# monthly oscillator in late July is June's number and has almost no sample.
OSC_TFS = ("1h", "4h", "12h", "1d", "1w")
STEP_MS = {"1h": HOUR_MS, "4h": 4 * HOUR_MS, "12h": 12 * HOUR_MS,
           "1d": DAY_MS, "1w": 7 * DAY_MS}

# §3.5 chart planes.  All four windows toggleable on every plane; these are the
# defaults the render opens with.
CHART_PLANES = {"4H": ("7d", "30d"), "1D": ("30d", "90d"),
                "1W": ("90d", "365d"), "1M": ("365d",)}

# §3.7 -- display-only lattice.  The practitioner study landed this pair as XO's
# higher-timeframe filter and the census will measure it against {9,89,200}
# regardless; rendering it now lets the operator's eye rehearse the comparison
# months before it is scored.  NO SIGNAL, NO VOTE, NO SCORE.
LATTICE_EMAS = (12, 25)
LATTICE_PLANES = ("1d", "1w")

# §6.2 cross-state layers.  Observation only -- H-RVX and H-M1X are routed to
# APOLLO.  TC-5's permanent 5m entry floor is untouched: measuring 1m crosses as
# CONTEXT is measurement, not entry logic.
SS_EMAS = (9, 89, 200)
SS_LENSES = ("1h", "4h", "12h")
FAST_EMAS = (300, 450)

PARITY_BANNER = ("PARITY NOT CERTIFIED — numbers not yet adopted. "
                 "The operator's parity readings have not been returned and "
                 "matched; nothing here may be trusted or acted on.")

# R-1 (reviewer finding, 2026-08-03).  R:R = reward / risk is INVERSELY
# PROPORTIONAL to the invalidation distance, so the tightest and least survivable
# stops float to the top of a board sorted by R:R.  The arithmetic is exact and
# F-B29 passes on it; the RANKING is still misleading.  Measured on the
# 2026-08-03 capture: the top row scored 11.23 on a stop 163.15 wide against a
# daily ATR of 1,699.80 -- 0.096 ATR, inside the noise it would have to survive.
#
# Drafts below the floor still PRINT -- suppressing them would hide geometry the
# operator asked to see -- but they are excluded from the RANKED board and
# flagged, because ranking them is what makes them look like the best ideas.
#
# DEMOTED to a CAUTION CHIP, cycle 3 (reviewer ruling D2-2).  The §7.2
# conformance fix already solved R-1: with invalidation BEYOND the far edge a
# 0.096-ATR stop is geometrically impossible, and the floor of the geometry is
# ~0.15 ATR.  Measured inval_atr then spanned 0.244-0.276 -- a 0.03 spread -- so
# excluding 2 of 12 on it was an arbitrary cut wearing the appearance of a
# principle.  Rows below the threshold now PRINT ON THE RANKED BOARD carrying a
# caution chip; nothing is excluded.
MIN_INVAL_ATR = 0.25

# C.2 STRUCTURE-DERIVED INVALIDATION.  Invalidation is the far edge of the NEXT
# CLUSTER BEYOND the entry cluster, not a mechanical function of cluster width.
# Dense structure gives a tight stop, a void gives a wide one, and BOTH ARE TRUE
# INFORMATION -- which a width-derived stop could never express, because it knew
# only how wide one cluster happened to be.
#
# When no next cluster exists within reach, the draft prints WITHOUT an R:R and
# says why.  A fabricated stop to complete a ratio would be the worst of both:
# a number that looks measured and is invented.
INVAL_SEARCH_ATR = 3.0


def _f(x):
    """None for anything not finite, so a NaN can never reach a printed number."""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if np.isfinite(v) else None


def _cols(df):
    return (df["open_time"].to_numpy().astype("int64"),
            df["open"].to_numpy(float), df["high"].to_numpy(float),
            df["low"].to_numpy(float), df["close"].to_numpy(float),
            df["volume"].to_numpy(float))


# ══════════════════════════════════════════════════════ §3 the volume filter

def volume_layer(klines, now_ms):
    """Windowed volume profiles at {prior-day, 7, 30, 90, 365} (§3.3, §3.4).

    The substrate ACTUALLY USED is recorded per window, per §3.3, and the tier
    map is the probed one: 1m/5m/15m are all stored for all ten assets, so
    nothing here is silently resampled from a coarser interval.  When a tier's
    interval is missing for an asset the fallback is recorded explicitly rather
    than applied quietly -- an undisclosed substitution is the exact failure the
    'DO NOT silently resample' instruction names.
    """
    out = {"windows": {}, "substrate_used": {}, "rows": P.PROFILE_ROWS,
           "value_area": P.VALUE_AREA, "provenance": "approximation",
           "approximation": P.APPROXIMATION,
           "lvn_threshold": P.LVN_THRESHOLD, "lvn_min_rows": P.LVN_MIN_ROWS,
           "retired_windows": ["5d", "20d"]}

    for name in WINDOWS:
        want = P.WINDOW_SUBSTRATE[name]
        sub = want if (want in klines and len(klines[want])) else None
        if sub is None:
            for alt in ("15m", "5m", "1m", "1h"):
                if alt in klines and len(klines[alt]):
                    sub = alt
                    break
        if sub is None:
            out["windows"][name] = {"warming": True, "reason": "no substrate"}
            continue
        if sub != want:
            out.setdefault("substrate_substitutions", {})[name] = {
                "wanted": want, "used": sub,
                "note": "disclosed substitution, not a silent resample"}
        out["substrate_used"][name] = sub

        t, o, h, l, c, v = _cols(klines[sub])
        if name == "prior-day":
            today = (now_ms // DAY_MS) * DAY_MS
            sel = (t >= today - DAY_MS) & (t < today)
            vp = (P.volume_profile(h[sel], l[sel], v[sel], bins=P.PROFILE_ROWS,
                                   value_area=P.VALUE_AREA)
                  if sel.any() else None)
            if vp is None:
                out["windows"][name] = {"warming": True, "reason": "no prior day"}
                continue
            vp["lvns"] = P.low_volume_nodes(vp["edges"], vp["hist"])
            vp["warming"] = False
            vp["substrate"] = sub
            vp["window_start_ms"] = int(today - DAY_MS)
            vp["as_of_ms"] = int(today)
            vp["lockbox_overlap"] = analytics.lockbox_overlap(today - DAY_MS, today)
        else:
            vp = P.windowed_profile(t, h, l, v, float(name[:-1]), now_ms,
                                    substrate=sub)
        out["windows"][name] = _profile_public(vp)
    return out


def _profile_public(vp):
    """Strip the histogram arrays; keep every number the report prints.

    The edges/hist arrays are large and are not part of the record schema; the
    LVNs derived from them are.
    """
    if vp.get("warming"):
        return {"warming": True, "poc": None, "vah": None, "val": None,
                "lvns": [], "bars": vp.get("bars"),
                "substrate": vp.get("substrate"),
                "window_start_ms": vp.get("window_start_ms"),
                "lockbox_overlap": vp.get("lockbox_overlap"),
                "chip": "warming"}
    return {"warming": False,
            "poc": _f(vp["poc"]), "vah": _f(vp["vah"]), "val": _f(vp["val"]),
            "lvns": [{"low": _f(n["low"]), "high": _f(n["high"]),
                      "mid": _f(n["mid"]), "rows": n["rows"]}
                     for n in vp.get("lvns", [])],
            "bars": vp.get("bars"), "substrate": vp.get("substrate"),
            "window_start_ms": vp.get("window_start_ms"),
            "lockbox_overlap": vp.get("lockbox_overlap"),
            "approximation": P.APPROXIMATION}


def rvwap_layer(klines, now_ms, tf="1h"):
    """Rolling VWAP with 1/2/3 sigma bands on 7/30/90/365d (§3.2).

    The operator: "the key is executing the rvwap with std's on the 7, 30, 90 and
    365 day".  Warm-up honesty is not optional -- an asset without a year of data
    prints a `warming` chip rather than a number, because a 365d VWAP computed on
    200 days is a 200-day VWAP wearing the wrong label.
    """
    out = {"tf": tf, "windows": {}, "sigmas": list(SIGMAS)}
    if tf not in klines or not len(klines[tf]):
        return out
    t, o, h, l, c, v = _cols(klines[tf])
    src = W.hlc3(h, l, c)
    span_ms = int(t[-1] - t[0])

    for wd in RVWAP_WINDOWS:
        need = wd * DAY_MS
        if span_ms < need:
            out["windows"][f"{wd}d"] = {
                "warming": True, "chip": "warming", "vwap": None, "stdev": None,
                "history_days": round(span_ms / DAY_MS, 1), "needs_days": wd,
                "bands": {}}
            continue
        rv = W.rolling_vwap(t, src, v, wd, sigmas=SIGMAS)
        bands = {}
        for k in SIGMAS:
            bands[f"up_{k}"] = _f(rv[f"band_up_{k}"][-1])
            bands[f"dn_{k}"] = _f(rv[f"band_dn_{k}"][-1])
        # R3 needs the SAMPLE DEPTH, not the span.  Count the bars actually in
        # the trailing window at the evaluated bar, by the same membership rule
        # rolling_vwap uses (open_time > t_now - W, current bar included).
        bars = int(np.count_nonzero(t > t[-1] - need))
        out["windows"][f"{wd}d"] = {
            "warming": False, "vwap": _f(rv["vwap"][-1]),
            "stdev": _f(rv["stdev"][-1]), "bands": bands,
            "bars": bars, "maturity": W.maturity(bars),
            "substrate": W.VWAP_SUBSTRATE, "source": W.VWAP_SOURCE,
            "lockbox_overlap": analytics.lockbox_overlap(now_ms - need, now_ms)}
    return out


def rvol_layer(klines, tf="1h"):
    """§3.6 RVOL (ratified B-7) -- the one volume-side addition still owed.

    Reported on the 1h plane, where the time-of-day bucket is an hour and the
    trailing 20 days give 20 clean samples.  A 5m bucket would give the same 20
    samples of a twelfth the volume and a far noisier ratio, for no extra
    information about the day's character.

    OBSERVATION ONLY.  RVOL casts NO VOTE and enters NO registry: it describes
    participation, not price, so it has no level to contribute and nothing to be
    confluent with.  The bias print counts agreement between things that locate
    price; a volume ratio is a different kind of claim and mixing it in would
    make the count mean less, not more.
    """
    out = {"tf": tf, "lookback_days": P.RVOL_LOOKBACK_DAYS,
           "observation_only": True,
           "no_vote": "RVOL describes participation, not price -- it contributes "
                      "no level and casts no vote (§7.3 counts locators only)"}
    if tf not in klines or not len(klines[tf]):
        out["warming"] = True
        out["reason"] = "no substrate"
        return out
    t, o, h, l, c, v = _cols(klines[tf])
    r = P.relative_volume(t, v)
    out.update(r)
    out["bar_utc_ms"] = int(t[-1])
    return out


def nesting_layer(vol, price):
    """VA nesting across adjacent window scales (§4), with the §4.2 prose.

    §4.2 is explicit that a table alone does not satisfy §4, so `prose` is a
    first-class output: when a pair is disjoint the report must SAY SO IN WORDS,
    naming the gap and both facing edges.
    """
    out = {"pairs": {}, "prose": [], "levels": []}
    for pair in N.ADJACENT_PAIRS:
        a = vol["windows"].get(pair[0]) or {}
        b = vol["windows"].get(pair[1]) or {}
        nest = N.va_nesting(a.get("val"), a.get("vah"),
                            b.get("val"), b.get("vah"))
        nest["price_location"] = N.price_location(price, nest)
        key = f"{pair[0]}<->{pair[1]}"
        out["pairs"][key] = {k: nest[k] for k in
                             ("state", "overlap_frac", "consensus_band",
                              "gap_band", "facing_edges", "price_location")}
        out["prose"].append(N.describe_nesting(pair, nest))
        out["levels"].extend(N.nesting_levels(pair, nest))
    return out


# ══════════════════════════════════════════════════════ §6 indicator layers

def _resampled(klines, tf):
    """Closed-bucket OHLCV at `tf`, from the finest sane native source.

    Routed through analytics.structure.resample_ohlcv rather than a private copy,
    so the Amendment-2 §1.2 closure discipline -- only buckets PROVED closed by a
    bar in a strictly later bucket -- applies to every plane the report prints.
    This is the fix for the duplicate resample implementation at
    daily_brief.py:216, which does not inherit that guarantee.
    """
    if tf in klines and len(klines[tf]):
        return _cols(klines[tf])
    base = None
    for cand in ("1h", "15m", "5m", "1m"):
        if cand in klines and len(klines[cand]):
            base = cand
            break
    if base is None:
        return None
    t, o, h, l, c, v = _cols(klines[base])
    if len(t) < 2:
        return None
    r = S.resample_ohlcv(t, o, h, l, c, v, STEP_MS[tf])
    if not len(r["open_time"]):
        return None
    return (r["open_time"], r["open"], r["high"], r["low"], r["close"], r["volume"])


def oscillator_layer(klines):
    """RSI / StochRSI / MACD / AO on {1h,4h,12h,1d,1w}, plus generalised
    divergences on RSI, MACD-histogram and AO -- regular and hidden (§6.1).

    Every divergence records the PRICE LEVEL of its pivot, which is what turns
    "is the same divergence printing on the AO, and is it landing where Secret
    Sauce has a level?" into a computed line rather than an impression.

    Divergences consume CONFIRMED pivots only, via structure.confirmed_pivots at
    the decision bar -- the caller-side half of the F-AN-13 lag:5 discipline that
    Phase I-R fixtured.
    """
    out = {"timeframes": {}, "divergences": [],
           "note": "1M plane carries price and volume structure only (§6.1)"}
    for tf in OSC_TFS:
        got = _resampled(klines, tf)
        if got is None:
            continue
        t, o, h, l, c, v = got
        if len(c) < 40:
            out["timeframes"][tf] = {"warming": True, "bars": int(len(c))}
            continue
        rsi = M.rsi(c, 14)
        k_line, d_line = M.stoch_rsi(c)
        macd_line, macd_sig, macd_hist = M.macd(c)
        ao = M.awesome_oscillator(h, l)
        out["timeframes"][tf] = {
            "warming": False, "bars": int(len(c)),
            "last_bar_utc_ms": int(t[-1]),
            "rsi": _f(rsi[-1]),
            "stoch_rsi_k": _f(k_line[-1]), "stoch_rsi_d": _f(d_line[-1]),
            "macd": _f(macd_line[-1]), "macd_signal": _f(macd_sig[-1]),
            "macd_hist": _f(macd_hist[-1]), "ao": _f(ao[-1]),
        }
        as_of = len(c) - 1
        for osc_name, osc in (("rsi", rsi), ("macd_hist", macd_hist), ("ao", ao)):
            for pk, px in (("high", h), ("low", l)):
                p_i, p_v, _ = S.confirmed_pivots(px, as_of, 5, 5, pk)
                o_i, o_v, _ = S.confirmed_pivots(osc, as_of, 5, 5, pk)
                for kind in ("regular", "hidden"):
                    for d in M.divergences(p_i, p_v, o_i, o_v, pk, kind=kind):
                        out["divergences"].append({
                            "timeframe": tf, "oscillator": osc_name,
                            "kind": kind, "pivot_kind": pk,
                            "direction": d["direction"],
                            "price_level": _f(d["price_level"]),
                            "from_index": d["from_index"],
                            "to_index": d["to_index"]})
    return out


def cross_state_layer(klines, atr_d):
    """§6.2 -- RVWAP crosses, RVWAP<->SS-EMA distances, the 1m fast lattice.

    All three are OBSERVATION layers, recorded as state and never voting.
    Whether any of them predicts anything is census work: H-RVX and H-M1X, both
    routed to APOLLO.
    """
    out = {"rvwap_pairs": {}, "rvwap_to_ss_ema": {}, "fast_lattice": {},
           "display_only": True,
           "census_candidates": ["H-RVX", "H-M1X"]}
    if "1h" not in klines or len(klines["1h"]) < 50:
        return out
    t, o, h, l, c, v = _cols(klines["1h"])
    src = W.hlc3(h, l, c)

    rv = {}
    span_ms = int(t[-1] - t[0])
    for wd in RVWAP_WINDOWS:
        if span_ms >= wd * DAY_MS:
            rv[wd] = W.rolling_vwap(t, src, v, wd)["vwap"]

    for a, b in ((7, 30), (7, 90), (30, 90), (90, 365)):
        if a not in rv or b not in rv:
            out["rvwap_pairs"][f"{a}x{b}"] = {"warming": True}
            continue
        va, vb = rv[a], rv[b]
        above = va[-1] > vb[-1]
        sign = np.sign(va - vb)
        bars = 0
        for i in range(len(sign) - 1, 0, -1):
            if sign[i] != sign[i - 1] and np.isfinite(sign[i - 1]):
                break
            bars += 1
        spread = _f(va[-1] - vb[-1])
        out["rvwap_pairs"][f"{a}x{b}"] = {
            "warming": False, "above": bool(above), "bars_since_cross": int(bars),
            "spread": spread,
            "spread_atr": _f(spread / atr_d) if (spread is not None and atr_d) else None}

    for lens in SS_LENSES:
        got = _resampled(klines, lens)
        if got is None:
            continue
        lt, lo, lh, ll, lc, lv = got
        for n in SS_EMAS:
            e = M.ema(lc, n)
            if not np.isfinite(e[-1]):
                continue
            for wd in rv:
                d = _f(rv[wd][-1] - e[-1])
                if d is None:
                    continue
                out["rvwap_to_ss_ema"][f"{wd}d_vs_ema{n}_{lens}"] = {
                    "distance": d,
                    "bps": _f(1e4 * d / e[-1]) if e[-1] else None,
                    "atr_d": _f(d / atr_d) if atr_d else None}

    if "1m" in klines and len(klines["1m"]) > 500:
        _, _, _, _, c1, _ = _cols(klines["1m"])
        fast = {}
        for n in tuple(FAST_EMAS) + SS_EMAS:
            e = M.ema(c1, n)
            fast[f"ema{n}"] = _f(e[-1])
        out["fast_lattice"]["1m"] = fast
        out["fast_lattice"]["1m_above"] = {
            f"ema{a}_over_ema{b}": bool(fast[f"ema{a}"] > fast[f"ema{b}"])
            for a, b in ((300, 450), (9, 89), (89, 200))
            if fast.get(f"ema{a}") is not None and fast.get(f"ema{b}") is not None}
    got5 = _resampled(klines, "5m") if "5m" in klines else None
    if got5 is not None:
        _, _, _, _, c5, _ = got5
        f5 = {f"ema{n}": _f(M.ema(c5, n)[-1]) for n in SS_EMAS}
        out["fast_lattice"]["5m"] = f5
        out["fast_lattice"]["note"] = ("TC-5's permanent 5m entry floor is "
                                       "untouched; 1m is context, not entry logic")
    return out


def lattice_layer(klines):
    """§3.7 -- the {12,25} EMA lattice on 1D and 1W.  DISPLAY ONLY.

    No signal, no vote, no score contribution.  It is rendered so the operator's
    eye can rehearse the comparison against {9,89,200} that the census will make
    regardless.
    """
    out = {"display_only": True, "no_vote": True, "no_score": True,
           "emas": list(LATTICE_EMAS), "planes": {}}
    for tf in LATTICE_PLANES:
        got = _resampled(klines, tf)
        if got is None:
            continue
        t, o, h, l, c, v = got
        if len(c) < max(LATTICE_EMAS) + 2:
            out["planes"][tf] = {"warming": True, "bars": int(len(c))}
            continue
        e12 = M.ema(c, LATTICE_EMAS[0])
        e25 = M.ema(c, LATTICE_EMAS[1])
        out["planes"][tf] = {"warming": False,
                             "ema12": _f(e12[-1]), "ema25": _f(e25[-1]),
                             "ema12_above_ema25": bool(e12[-1] > e25[-1])}
    return out


def chart_planes(klines, vol):
    """§3.5 -- the four planes, their default windows, and the forming candle.

    THE FORMING-CANDLE RULE.  On weekly and monthly planes the current candle is
    unfinished most of the time.  It is DRAWN, GREYED and LABELLED so the chart
    looks like the operator's chart -- while EVERY COMPUTED NUMBER USES CLOSED
    CANDLES ONLY.  Mid-week, the weekly RSI is last week's; that staleness is
    deliberate and is the founding law of this toolkit.

    `forming` below is therefore explicitly marked draw_only and is emitted in a
    separate branch of the document from every computed value, so F-B31 can
    assert no computed number equals it.
    """
    out = {"planes": {}, "value_areas_extend": True,
           "forming_candle_rule": "drawn and greyed; excluded from every "
                                  "computed value (§3.5)"}
    for plane, wins in CHART_PLANES.items():
        tf = {"4H": "4h", "1D": "1d", "1W": "1w", "1M": "1M"}[plane]
        entry = {"default_windows": list(wins),
                 "all_windows_toggleable": list(WINDOWS),
                 "value_areas": {w: {"vah": (vol["windows"].get(w) or {}).get("vah"),
                                     "val": (vol["windows"].get(w) or {}).get("val"),
                                     "poc": (vol["windows"].get(w) or {}).get("poc")}
                                 for w in wins}}
        if plane == "1M":
            entry["oscillators"] = None
            entry["note"] = "price and volume structure only (§6.1)"
        if plane in ("1W", "1M"):
            step = STEP_MS["1w"] if plane == "1W" else None
            entry["forming"] = _forming_candle(klines, step)
        out["planes"][plane] = entry
    return out


def _forming_candle(klines, step_ms):
    """The unfinished bucket, for DRAWING ONLY.

    Built from the legacy keep-the-bucket path on purpose: the public
    resample_ohlcv now refuses to emit an unproven bucket, which is exactly
    right for computation and exactly wrong for a candle we intend to draw and
    label as unfinished.  Marked draw_only so it can never be mistaken for a
    computed value.
    """
    if step_ms is None or "1h" not in klines or len(klines["1h"]) < 2:
        return {"draw_only": True, "available": False}
    t, o, h, l, c, v = _cols(klines["1h"])
    closed = S.resample_ohlcv(t, o, h, l, c, v, step_ms)
    legacy = S._resample_ohlcv_legacy(t, o, h, l, c, v, step_ms)
    n_closed = len(closed["open_time"])
    if len(legacy["open_time"]) <= n_closed:
        return {"draw_only": True, "available": False}
    i = n_closed
    return {"draw_only": True, "available": True, "label": "forming",
            "greyed": True,
            "open_time_ms": int(legacy["open_time"][i]),
            "open": _f(legacy["open"][i]), "high": _f(legacy["high"][i]),
            "low": _f(legacy["low"][i]), "close": _f(legacy["close"][i]),
            "volume": _f(legacy["volume"][i]),
            "excluded_from_computation": True}


# ══════════════════════════════════ §5.1 prior anchors + confirmed pivots

PRIOR_ANCHOR_PERIODS = ("M", "Q", "Y")
PIVOT_LOOKBACK_DAYS = 180


def prior_anchored_vwaps(klines, now_ms):
    """Prior M/Q/Y anchored VWAP with 1/2/3 sigma (ratified D-B11).

    These are FIXED historical levels: the anchored VWAP accumulated across the
    PREVIOUS COMPLETED period, read at that period's last bar.  They do not
    develop -- prior-quarter VWAP is where the last quarter's business settled,
    which is why the operator's manual reviews cite them by name ("price wicked
    under pQ-VWAP", "reclaim std1-confluent with pM-VWAP").

    `daily_brief` supplies only the DEVELOPING W/M/Q/Y anchors, so these are
    computed here rather than read.  Cycle-2's registry was missing them.
    """
    out = {}
    if "1h" not in klines or len(klines["1h"]) < 2:
        return out
    t, o, h, l, c, v = _cols(klines["1h"])
    src = W.hlc3(h, l, c)
    d = t.astype("datetime64[ms]").astype("datetime64[D]")

    for period in PRIOR_ANCHOR_PERIODS:
        if period == "M":
            key = d.astype("datetime64[M]")
        elif period == "Y":
            key = d.astype("datetime64[Y]")
        else:
            m = d.astype("datetime64[M]").astype(int)
            key = (m - m % 3).astype("datetime64[M]")
        key = np.asarray(key)
        ks = key.astype("datetime64[ms]").astype("int64")
        uniq = np.unique(ks)
        if len(uniq) < 2:
            out[f"prior_{period}"] = {"warming": True,
                                      "reason": "no completed prior period"}
            continue
        prev = uniq[-2]
        sel = np.flatnonzero(ks == prev)
        a0, a1 = int(sel[0]), int(sel[-1])
        r = W.anchored_vwap(src[:a1 + 1], v[:a1 + 1], a0, sigmas=SIGMAS)
        vw, sd = _f(r["vwap"][-1]), _f(r["stdev"][-1])
        if vw is None:
            out[f"prior_{period}"] = {"warming": True, "reason": "no volume"}
            continue
        nbars = int(a1 - a0 + 1)
        out[f"prior_{period}"] = {
            "warming": False, "vwap": vw, "sigma": sd,
            "anchor_utc_ms": int(t[a0]), "closed_utc_ms": int(t[a1]),
            "bars": nbars, "maturity": W.maturity(nbars),
            "substrate": W.VWAP_SUBSTRATE, "source": W.VWAP_SOURCE,
            "bands": {f"{sgn}{k}s": _f(vw + mult * k * (sd or 0.0))
                      for k in SIGMAS for sgn, mult in (("+", 1), ("-", -1))},
            "note": "FIXED level from the completed prior period; does not develop"}
    return out


def confirmed_pivot_levels(klines, now_ms, lookback_days=PIVOT_LOOKBACK_DAYS):
    """Confirmed 1d pivots inside a trailing lookback (§5.1, F-AN-13 lag:5).

    FINDING F-3R-A, fixed here.  The registry was fed by `daily_brief`'s
    `last_pivots(..., n=3)` -- a DISPLAY cap of the three most recent highs and
    lows, which is why `structure` reported EXACTLY 13 levels for all ten assets.
    Ten instruments cannot share a pivot count; the number was an artifact of the
    cap, not a property of the market.

    `analytics.structure.confirmed_pivots` was never emitted into the registry at
    all -- it was used only inside `oscillator_layer` for divergences. It is the
    causality-disciplined entry point (it filters to `confirmation_lag <=
    as_of_index`, so an unconfirmed pivot cannot leak), and §5.1 names confirmed
    pivots as a structure member.

    A trailing LOOKBACK is used rather than a count cap: it is self-limiting,
    it varies per asset as it should, and "recent structure" is a statement about
    time, not about how many pivots happen to have printed.
    """
    out = {"lookback_days": lookback_days, "highs": [], "lows": [],
           "substrate": "1d resampled from 1h, closed buckets only"}
    got = _resampled(klines, "1d")
    if got is None:
        return out
    t, o, h, l, c, v = got
    if len(c) < 20:
        return out
    as_of = len(c) - 1
    floor_ms = int(t[-1]) - lookback_days * DAY_MS
    for kind, arr, bucket in (("high", h, "highs"), ("low", l, "lows")):
        idx, lvl, conf = S.confirmed_pivots(arr, as_of, 5, 5, kind)
        for i, lv, cf in zip(idx, lvl, conf):
            if int(t[i]) < floor_ms:
                continue
            out[bucket].append({"level": _f(lv), "index": int(i),
                                "bar_utc_ms": int(t[i]),
                                "confirmed_at_index": int(cf)})
    return out


# ══════════════════════════════════════ D.5 / D.6  stretch and excursion

# A sigma computed over very few bars is arithmetically exact and
# informationally empty -- it is the spread between two numbers, not a
# dispersion estimate.  Stretch and excursion records carry the bar count and a
# `thin_sample` flag so a reader never mistakes one for the other.  This is the
# same honesty the `warming` chip provides for windows that cannot be computed
# at all; here the quantity CAN be computed and still should not be trusted.
THIN_SAMPLE_BARS = 30

# §D.6: the bands whose touches are recorded.  Recording only -- whether a touch
# pays is H-VBR, census work under G-7, and nothing here claims it does.
EXCURSION_SIGMAS = (1, 2, 3)


def _stretch_row(name, kind, mean, sigma, price, atr_d, bars=None,
                 warming=False):
    """One anchor's or window's stretch record.

    `sigma_position` is the quantity D.5 asks for: how far price sits from the
    mean IN SIGMA UNITS.  It is recorded beside bps and daily-ATR because the
    three answer different questions -- bps is scale-free, ATR is
    volatility-relative, and sigma is relative to THIS tool's own dispersion,
    which is what makes two anchors comparable to each other.
    """
    row = {"name": name, "kind": kind, "warming": bool(warming),
           "mean": _f(mean), "sigma": _f(sigma), "bars": bars,
           "sigma_position": None, "bps": None, "atr": None,
           "thin_sample": None, "band_reached": None}
    if warming or mean is None or price is None:
        return row
    d = float(price) - float(mean)
    row["bps"] = _f(1e4 * d / mean) if mean else None
    row["atr"] = _f(d / atr_d) if atr_d else None
    if sigma and sigma > 0:
        row["sigma_position"] = _f(d / sigma)
        row["thin_sample"] = bool(bars is not None and bars < THIN_SAMPLE_BARS)
        # the outermost band price has actually reached, signed
        k = 0
        for s in EXCURSION_SIGMAS:
            if abs(row["sigma_position"]) >= s:
                k = s
        row["band_reached"] = (0 if k == 0
                               else (k if row["sigma_position"] > 0 else -k))
    return row


def stretch_layer(a, rv, prior, price, atr_d):
    """D.5 -- price's distance from every VWAP mean, in SIGMA UNITS.

    Covers the developing W/M/Q/Y anchors, the prior M/Q/Y anchors, and the
    rolling 7/30/90/365 windows, so every volume-weighted mean in the instrument
    is on one comparable scale.

    D.5.1 records the MULTI-SCALE STRETCH DISAGREEMENT explicitly.  Price can sit
    above one anchor's upper band and below another's lower band at the same
    instant -- overextended up against the month and down against the year, both
    true -- and that disagreement is the object of interest, not a contradiction
    to be resolved.  It is the same class of thing as the VA-nesting layer and it
    belongs beside it in the report.
    """
    rows = []

    for name, blob in ((a.get("vwap") or {}).get("anchored") or {}).items():
        if not isinstance(blob, dict):
            continue
        rows.append(_stretch_row(
            f"anchored {name}", "anchored", blob.get("vwap"), blob.get("sigma"),
            price, atr_d, bars=blob.get("bars"),
            warming=blob.get("vwap") is None))

    for name, blob in (prior or {}).items():
        if not isinstance(blob, dict):
            continue
        rows.append(_stretch_row(
            name.replace("_", " "), "prior_anchor", blob.get("vwap"),
            blob.get("sigma"), price, atr_d, bars=blob.get("bars"),
            warming=bool(blob.get("warming"))))

    for name, blob in (rv.get("windows") or {}).items():
        if not isinstance(blob, dict):
            continue
        rows.append(_stretch_row(
            f"RVWAP {name}", "rolling", blob.get("vwap"), blob.get("stdev"),
            price, atr_d, bars=None, warming=bool(blob.get("warming"))))

    live = [r for r in rows if r["sigma_position"] is not None]
    out = {"rows": rows, "thin_sample_bars": THIN_SAMPLE_BARS,
           "price": _f(price), "n_live": len(live),
           "units": "sigma_position = (price - mean) / sigma, signed"}

    if live:
        hi = max(live, key=lambda r: r["sigma_position"])
        lo = min(live, key=lambda r: r["sigma_position"])
        out["disagreement"] = {
            "max": {"name": hi["name"], "sigma_position": hi["sigma_position"],
                    "thin_sample": hi["thin_sample"]},
            "min": {"name": lo["name"], "sigma_position": lo["sigma_position"],
                    "thin_sample": lo["thin_sample"]},
            "spread_sigma": _f(hi["sigma_position"] - lo["sigma_position"]),
            "most_disagreeing_pair": [hi["name"], lo["name"]],
            "straddles_one_sigma": bool(hi["sigma_position"] >= 1.0
                                        and lo["sigma_position"] <= -1.0),
            "note": "price can be overextended UP against one scale and DOWN "
                    "against another at the same instant; both are true and the "
                    "disagreement is the object of interest"}
    else:
        out["disagreement"] = None
    return out


def excursion_layer(stretch, atr_d):
    """D.6 -- band-excursion events.  RECORDING ONLY.

    Records, per VWAP, whether price has reached sigma1/2/3 on either side and
    what it would take to get back to the mean.  This is the substrate for the
    operator's thesis -- enter at an extreme band, target the mean -- and for
    census candidate H-VBR.

    WHAT IS DELIBERATELY NOT HERE.  No count of "captures since the last touch"
    is stored.  A capture is a point in time and must stay self-describing; a
    stored counter would be state the capture cannot verify about itself, and
    `brief_panel.py` rebuilds every partition FROM CAPTURES ALONE.  The
    since-last-touch series is therefore DERIVED at panel-build time from the
    stored per-capture `band_reached` column, where it is reproducible from the
    archive rather than trusted from a counter.

    RECORDING IS OPS.  Whether a band touch pays anything is H-VBR under G-7,
    routed to APOLLO, and nothing in this function claims it does.
    """
    events, live = [], 0
    for r in (stretch.get("rows") or []):
        if r["sigma_position"] is None:
            continue
        live += 1
        sp = r["sigma_position"]
        reached = r["band_reached"] or 0
        if reached == 0:
            continue
        events.append({
            "name": r["name"], "kind": r["kind"],
            "side": "above" if sp > 0 else "below",
            "band_reached": abs(reached),
            "sigma_position": sp,
            "bars": r["bars"], "thin_sample": r["thin_sample"],
            "distance_to_mean_sigma": _f(abs(sp)),
            "distance_to_mean_atr": _f(abs(r["atr"])) if r["atr"] is not None else None,
            "returned_to_mean": False,
            "recording_only": True})
    return {"events": events, "n_live_vwaps": live,
            "sigmas_watched": list(EXCURSION_SIGMAS),
            "since_last_touch": "DERIVED at panel-build time from the stored "
                                "band_reached series; not stored per capture, so "
                                "the capture stays self-describing and the panel "
                                "stays rebuildable from captures alone",
            "census_candidate": "H-VBR",
            "claims_nothing": "recording is OPS; whether a band touch pays is "
                              "census work under G-7"}


# ══════════════════════════════════════════════ §5 registry and dual scoring

def build_registry(a, vol, rv, nest_levels, prior_anchors=None, pivots=None):
    """Assemble the level registry from all five families (§5.1).

    Every level carries the window it came from, because §4.3's scale
    confirmation is keyed on `timeframe` -- a level with no window can never be
    badged, and a mislabelled one would badge a coincidence as agreement.

    DENSITY WARNING (§5.3), recorded rather than defended: v1.1 ran 46-62 levels
    per asset; with rolling bands, windowed profiles with LVNs, prior anchors and
    sigma-2/3, expect ~180-200. Every threshold was calibrated against a registry
    a third that size, and no threshold is defended on intuition once the
    calibration report exists.
    """
    reg = L.LevelRegistry()

    # R3 MATURITY FLOORS (operator ruling, 2026-08-05).  Every level withheld
    # here is RECORDED, never silently dropped: `withheld` is returned on the
    # registry so the report can say which anchors were too young, at what bar
    # count, and whether it was the line or only the bands that failed.  A floor
    # that cannot be audited is indistinguishable from a bug.
    withheld = []

    def _admit(blob, family, line_label, line_level, source_layer, tf,
               band_items, what):
        """Emit a VWAP line and its bands subject to the R3 floors.

        `band_items` is an iterable of (label, level) already computed.  The
        bands are gated SEPARATELY from the line and at a higher floor,
        because the line is a weighted mean (fast to stabilise) and the sigma
        is a dispersion estimate over the same few points (slow).
        """
        mat = blob.get("maturity") or W.maturity(blob.get("bars"))
        if line_level is not None:
            if mat["line_ok"]:
                reg.add(family, line_label, line_level, source_layer, tf)
            else:
                withheld.append({"what": what, "level": "line",
                                 "label": line_label, "bars": mat["bars"],
                                 "floor": mat["line_min_bars"],
                                 "reason": "below R3 line floor"})
        for blabel, blevel in band_items:
            if blevel is None:
                continue
            if mat["band_ok"]:
                reg.add(family, blabel, blevel, source_layer, tf)
            else:
                withheld.append({"what": what, "level": "band",
                                 "label": blabel, "bars": mat["bars"],
                                 "floor": mat["band_min_bars"],
                                 "reason": "below R3 band floor"})

    # vwap_anchored -- developing W/M/Q/Y, each with 1/2/3 sigma.
    #
    # `daily_brief` publishes sigma as a scalar and only the 1-sigma band, so the
    # 2s/3s levels are DERIVED here from the same sigma rather than read.  That is
    # arithmetic on a published number, not a second recipe.
    #
    # Its `vwap.rolling` block is deliberately NOT read: brief2's own rvwap_layer
    # is the pinned §3.2 recipe and already supplies the vwap_rolling family.
    # Adding both would double-count the same tool as two agreeing voices, which
    # is precisely the degeneracy collapse_same_family exists to prevent.
    anchored = ((a.get("vwap") or {}).get("anchored") or {})
    for key, blob in anchored.items():
        if not isinstance(blob, dict):
            continue
        lv = _f(blob.get("vwap"))
        if lv is None:
            continue
        sig = _f(blob.get("sigma"))
        bitems = []
        if sig is not None and sig > 0:
            for k in SIGMAS:
                bitems.append((f"{key} +{k}s", lv + k * sig))
                bitems.append((f"{key} -{k}s", lv - k * sig))
        _admit(blob, "vwap_anchored", f"{key} anchored VWAP", lv,
               "vwap_complex", key, bitems, f"anchored {key}")

    # vwap_rolling -- 7/30/90/365d RVWAP, each with 1/2/3 sigma
    for wname, blob in (rv.get("windows") or {}).items():
        if blob.get("warming"):
            continue
        _admit(blob, "vwap_rolling", f"RVWAP {wname}", blob.get("vwap"),
               "rvwap", wname,
               [(f"RVWAP {wname} {bk}", bv)
                for bk, bv in (blob.get("bands") or {}).items()],
               f"RVWAP {wname}")

    # profile_windowed -- POC/VAH/VAL per window, LVN midpoints and edges
    for wname, blob in (vol.get("windows") or {}).items():
        if blob.get("warming"):
            continue
        for tag in ("poc", "vah", "val"):
            if blob.get(tag) is not None:
                reg.add("profile_windowed", f"{wname} {tag.upper()}",
                        blob[tag], "windowed_profile", wname)
        for j, n in enumerate(blob.get("lvns") or []):
            for tag in ("mid", "low", "high"):
                if n.get(tag) is not None:
                    reg.add("profile_windowed", f"{wname} LVN{j} {tag}",
                            n[tag], "lvn", wname)

    # profile_windowed -- consensus and gap band edges from the nesting layer
    for lv in nest_levels:
        reg.add(lv["family"], lv["label"], lv["level"],
                lv["source_layer"], lv["timeframe"])

    # vwap_anchored -- PRIOR M/Q/Y, fixed levels from completed periods (D-B11)
    for pname, blob in (prior_anchors or {}).items():
        if not isinstance(blob, dict) or blob.get("warming"):
            continue
        _admit(blob, "vwap_anchored", f"{pname} VWAP", blob.get("vwap"),
               "prior_anchor", pname,
               [(f"{pname} {bk}", bv)
                for bk, bv in (blob.get("bands") or {}).items()],
               pname)

    # structure -- CONFIRMED pivots (F-3R-A: was daily_brief's display-capped
    # top-3, which is why every asset reported exactly 13 structure levels)
    st = a.get("structure") or {}
    if pivots:
        for bucket, tag in (("highs", "confirmed pivot high"),
                            ("lows", "confirmed pivot low")):
            for p in pivots.get(bucket) or []:
                lv = _f(p.get("level"))
                if lv is not None:
                    reg.add("structure", f"{tag} @{p['index']}", lv,
                            "confirmed_pivots", "1d")
    else:
        for tag, plist in (("pivot high", st.get("pivot_highs")),
                           ("pivot low", st.get("pivot_lows"))):
            for i, p in enumerate(plist or []):
                lv = _f((p or {}).get("level"))
                if lv is not None:
                    reg.add("structure", f"{tag} {(p or {}).get('day', i)}", lv,
                            "structure_layer", "1d")
    for period, tf in (("prior_day", "1d"), ("prior_week", "1w"),
                       ("prior_month", "1M")):
        blob = st.get(period) or {}
        for edge in ("high", "low"):
            lv = _f(blob.get(edge))
            if lv is not None:
                reg.add("structure", f"{period.replace('_', ' ')} {edge}", lv,
                        "structure_layer", tf)
    for period, blob in (st.get("period_opens") or {}).items():
        lv = _f((blob or {}).get("level"))
        if lv is not None:
            reg.add("structure", f"{period} open", lv, "structure_layer", period)

    for name, blob in ((a.get("sessions") or {}).get("sessions") or {}).items():
        for edge in ("high", "low"):
            lv = _f((blob or {}).get(edge))
            if lv is not None:
                reg.add("structure", f"session {name} {edge}", lv,
                        "sessions_layer", "1h")

    # ss -- armed zone edges and governor band edges per lens
    for row in (a.get("radar") or []):
        if not isinstance(row, dict):
            continue
        lens = row.get("lens", "?")
        for zone, band in (row.get("armed_bands") or {}).items():
            if not isinstance(band, dict) or not band.get("armed"):
                continue
            for edge in ("top", "bot"):
                lv = _f(band.get(edge))
                if lv is not None:
                    reg.add("ss", f"{lens} {zone} {edge}", lv, "radar", lens)
        for edge in ("governor_band_top", "governor_band_bot"):
            lv = _f(row.get(edge))
            if lv is not None:
                reg.add("ss", f"{lens} {edge}", lv, "radar", lens)

    # Ride the audit trail out on the registry rather than in a second return
    # value: every existing caller keeps working, and no caller can obtain the
    # registry without also being able to see what was kept out of it.
    reg.withheld = withheld
    return reg


def confluence(reg, price, atr_d):
    """§5.2 + §5.4 -- both scored views, plus the sensitivity annex."""
    if not atr_d or atr_d <= 0:
        return {"unavailable": True, "reason": "no positive daily ATR"}
    out = L.dual_score(reg.as_list(), atr_d, price)
    out["rules"] = {"collapse_atr": L.COLLAPSE_ATR, "cluster_atr": L.CLUSTER_ATR,
                    "lis_atr": L.LIS_ATR, "family_cap": L.FAMILY_CAP,
                    "families": list(L.FAMILIES),
                    "volume_families": list(L.VOLUME_FAMILIES),
                    "scoring": "sum over families of min(count, cap) + distinct "
                               "families -- counted, never fitted"}
    out["level_count"] = len(reg)
    out["level_count_by_family"] = reg.by_family()

    # R3 audit trail.  Counts AND the rows, because "3 levels withheld" is not
    # checkable and "prior_Y line at 2 bars, floor 10" is.
    wh = list(getattr(reg, "withheld", []) or [])
    out["maturity_floors"] = {
        "ruling": "R3 (operator, 2026-08-05) -- INTERIM, 1h substrate",
        "line_min_bars": W.LINE_MIN_BARS, "band_min_bars": W.BAND_MIN_BARS,
        "withheld_count": len(wh),
        "withheld_lines": sum(1 for r in wh if r["level"] == "line"),
        "withheld_bands": sum(1 for r in wh if r["level"] == "band"),
        "withheld": wh,
        "note": "withheld levels still PRINT with a thin_sample chip; they are "
                "excluded from SCORING only"}
    return out


# ══════════════════════════════════════════════════ §7 decision instrument

def _cluster_edges(cl):
    lv = [m["level"] for m in cl["members"]]
    return min(lv), max(lv)


def _structure_invalidation(clusters, line, side, entry, lo, hi, atr_d):
    """C.2 -- the far edge of the NEXT CLUSTER BEYOND the entry cluster.

    The level fails when price is through the next piece of structure past it,
    not when price has travelled some fixed multiple of the entry cluster's own
    width.  Dense structure therefore gives a tight stop and a void gives a wide
    one, and both are true statements about the chart.

    Returns (invalidation, source) or (None, reason) when no cluster lies within
    INVAL_SEARCH_ATR -- the caller then prints the draft with NO R:R rather than
    inventing a stop to complete the ratio.
    """
    if not atr_d or atr_d <= 0:
        return None, "no daily ATR"
    reach = INVAL_SEARCH_ATR * atr_d
    beyond = []
    for c in clusters:
        m = c.get("mean")
        if m is None:
            continue
        if side == "above" and m > hi and (m - entry) <= reach:
            beyond.append(c)
        elif side == "below" and m < lo and (entry - m) <= reach:
            beyond.append(c)
    if not beyond:
        return None, "no cluster beyond within reach"
    nxt = sorted(beyond, key=lambda c: abs(c["mean"] - entry))[0]
    n_lo, n_hi = _cluster_edges(nxt)
    inval = n_hi if side == "above" else n_lo
    return _f(inval), (f"far edge of the next cluster beyond "
                       f"(mean {nxt['mean']:,.2f}, score {nxt['score']})")


def rr_board(conf, price, atr_d, view="with_volume"):
    """§7.2 -- R:R ranking, GEOMETRY not prophecy.

    Every component is printed so the operator can recompute by hand, and F-B29
    asserts exactly that: no ratio prints without entry, invalidation and target
    all present, and every printed ratio recomputes from its own components.

    entry        = the line's cluster mean
    invalidation = the cluster's FAR edge -- the price that says the level failed
    target 1     = the next opposing cluster scoring >= 4; target 2 = beyond it
    R:R          = |target - entry| / |entry - invalidation|

    The board sorts by R:R and says plainly what the ranking is: STRUCTURAL
    QUALITY, not probability.  A high R:R means the geometry is favourable,
    nothing more -- any claim that a setup is LIKELY to work would need outcome
    statistics the firewall reserves for the census.
    """
    v = (conf or {}).get(view) or {}
    lines, clusters = v.get("lines") or {}, v.get("clusters") or []
    board, excluded, no_rr = [], [], []
    for side in ("above", "below"):
        line = lines.get(side)
        if not line:
            continue
        entry = _f(line["mean"])
        lo, hi = _cluster_edges(line)
        invalidation, inval_src = _structure_invalidation(
            clusters, line, side, entry, lo, hi, atr_d)
        if invalidation is None:
            no_rr.append({
                "side": "short" if side == "above" else "long",
                "line_side": side, "entry": entry,
                "cluster_score": int(line["score"]),
                "cluster_families": list(line["families"]),
                "rr": None, "invalidation": None,
                "reason": f"no cluster beyond the level within "
                          f"{INVAL_SEARCH_ATR} daily-ATR -- no structure to fail "
                          f"against, so no R:R is printed rather than a "
                          f"fabricated stop"})
            continue
        if entry is None or invalidation is None or entry == invalidation:
            continue
        opposing = sorted(
            [c for c in clusters
             if c["score"] >= 4 and ((c["mean"] < entry) if side == "above"
                                     else (c["mean"] > entry))],
            key=lambda c: abs(c["mean"] - entry))
        targets = [_f(c["mean"]) for c in opposing[:2]]
        risk = abs(entry - invalidation)
        inval_atr = (risk / atr_d) if atr_d else None
        for n, tgt in enumerate(targets, start=1):
            if tgt is None or risk <= 0:
                continue
            row = {
                "side": "short" if side == "above" else "long",
                "line_side": side, "target_rank": n,
                "entry": entry, "invalidation": invalidation, "target": tgt,
                "reward": abs(tgt - entry), "risk": risk,
                "inval_atr": inval_atr,
                "rr": abs(tgt - entry) / risk,
                "cluster_score": int(line["score"]),
                "cluster_families": list(line["families"]),
                "source": line.get("source", "primary")}
            # R-1 DEMOTED: a tight invalidation now carries a CAUTION CHIP and
            # stays on the ranked board.  Excluding it was an arbitrary cut.
            row["rankable"] = True
            tight = inval_atr is not None and inval_atr < MIN_INVAL_ATR
            row["caution"] = tight
            row["flag"] = ("invalidation tighter than "
                           f"{MIN_INVAL_ATR} daily-ATR -- caution") if tight else None
            row["invalidation_source"] = inval_src
            board.append(row)

    board.sort(key=lambda r: -r["rr"])
    return {"view": view, "board": board,
            "excluded_too_tight": excluded,
            "no_rr": no_rr,
            "caution_count": sum(1 for r in board if r.get("caution")),
            "min_inval_atr": MIN_INVAL_ATR,
            "min_inval_atr_is": "v1 placeholder; re-ratified against the "
                                "inval_atr distribution in the calibration report",
            "excluded_count": len(excluded),
            "ranking_is": "structural quality, not probability (§7.2)",
            "why_a_floor": "R:R is inversely proportional to the invalidation "
                           "distance (R-1). The §7.2 fix made a knife-edge stop "
                           "geometrically impossible, so the threshold is now a "
                           "CAUTION CHIP, not an exclusion gate -- excluding on a "
                           "0.03-ATR spread was an arbitrary cut.",
            "invalidation_rule": "far edge of the NEXT CLUSTER beyond the entry "
                                 "cluster (C.2); dense structure -> tight stop, "
                                 "void -> wide stop, both true information",
            "contains_no_probability_claim": True}


def hypothesis_drafts(conf, price, atr_d=None, view="with_volume"):
    """§7.1 -- if-then drafts, mechanically derived.  NO SIZING, EVER.

    R-1: a draft whose invalidation is tighter than MIN_INVAL_ATR still PRINTS
    here, carrying `rankable: False` and the reason.  Suppressing it would hide
    geometry the operator asked to see; ranking it is what made it look like the
    best idea on the board.
    """
    v = (conf or {}).get(view) or {}
    lines = v.get("lines") or {}
    out = []
    for side, word in (("above", "reclaims"), ("below", "loses")):
        line = lines.get(side)
        if not line:
            continue
        lo, hi = _cluster_edges(line)
        entry = _f(line["mean"])
        # C.2 -- the SAME structure-derived rule rr_board uses, so a draft and
        # its ranked row can never disagree about where the level failed.
        far, _src = _structure_invalidation(
            (v.get("clusters") or []), line, side, entry, lo, hi, atr_d)
        inval_atr = (abs(entry - far) / atr_d) if (atr_d and far is not None
                                                   and entry is not None) else None
        tight = inval_atr is not None and inval_atr < MIN_INVAL_ATR
        out.append({
            "draft": True, "no_sizing": True,
            "inval_atr": inval_atr,
            "rankable": not tight,
            "flag": "invalidation too tight to rank" if tight else None,
            "if": f"price {word} {line['mean']:,.2f} "
                  f"(cluster {lo:,.2f}-{hi:,.2f}, score {line['score']})",
            "then": ("watch for continuation toward the next opposing area"
                     if side == "above" else
                     "watch for follow-through toward the next area below"),
            "invalidated_if": (f"price closes back "
                               f"{'below' if side == 'above' else 'above'} "
                               f"{far:,.2f}") if far is not None else
                              ("no cluster beyond this level within reach -- no "
                               "structural invalidation, so no R:R is printed"),
            "level": _f(line["mean"]), "score": int(line["score"]),
            "families": list(line["families"])})
    return out


def composite_bias(a, vol, nest, conf, price):
    """§7.3 -- five families each declare a side. Counted, dissent named.

    Equal weights, count-based, NEVER fitted.  The compression flag demotes the
    final band one step toward neutral; it does NOT half-weight votes, because
    that would contradict count-based purity.

    Both this and the radar may disagree; when they do a disagreement chip prints
    and nothing is reconciled.  They measure different things, and the
    disagreement is information.
    """
    votes, why = {}, {}

    gov = a.get("governor") or {}
    dirs = [(gov.get(l) or {}).get("direction") for l in SS_LENSES]
    up = sum(1 for d in dirs if d == "long")
    dn = sum(1 for d in dirs if d == "short")
    votes["trend"] = 1 if up > dn else (-1 if dn > up else 0)
    why["trend"] = f"governor {up} long / {dn} short across {list(SS_LENSES)}"

    osc = (a.get("brief2_oscillators") or {}).get("timeframes") or {}
    sig = []
    for tf in ("4h", "12h"):
        b = osc.get(tf) or {}
        if b.get("warming") or b.get("rsi") is None:
            continue
        sig.append(1 if b["rsi"] > 50 else -1)
        if b.get("macd_hist") is not None:
            sig.append(1 if b["macd_hist"] > 0 else -1)
        if b.get("ao") is not None:
            sig.append(1 if b["ao"] > 0 else -1)
    s_sum = sum(sig)
    votes["momentum"] = 0 if not sig else (1 if s_sum > 0 else (-1 if s_sum < 0 else 0))
    why["momentum"] = f"RSI+MACD+AO on 4h/12h: net {s_sum} of {len(sig)} signed"

    loc = []
    for key, blob in (a.get("vwap") or {}).items():
        lv = _f(blob.get("vwap")) if isinstance(blob, dict) else None
        if lv is not None:
            loc.append(1 if price > lv else -1)
    pd_ = (vol.get("windows") or {}).get("prior-day") or {}
    if pd_.get("vah") is not None and pd_.get("val") is not None:
        loc.append(1 if price > pd_["vah"] else (-1 if price < pd_["val"] else 0))
    l_sum = sum(loc)
    votes["location"] = 0 if not loc else (1 if l_sum > 0 else (-1 if l_sum < 0 else 0))
    why["location"] = f"price vs anchored VWAP complex and prior-day value: net {l_sum}"

    vl = []
    for w in ("7d", "30d", "90d", "365d"):
        blob = (vol.get("windows") or {}).get(w) or {}
        if blob.get("warming") or blob.get("vah") is None or blob.get("val") is None:
            continue
        vl.append(1 if price > blob["vah"] else (-1 if price < blob["val"] else 0))
    for _key, pair in (nest.get("pairs") or {}).items():
        if pair.get("price_location") == "inside_consensus":
            vl.append(0)
    v_sum = sum(vl)
    votes["volume_location"] = 0 if not vl else (1 if v_sum > 0 else
                                                 (-1 if v_sum < 0 else 0))
    why["volume_location"] = f"price vs windowed value areas and consensus: net {v_sum}"

    fp = _f((a.get("funding") or {}).get("percentile"))
    votes["crowding"] = 0 if fp is None else (-1 if fp >= 90 else (1 if fp <= 10 else 0))
    why["crowding"] = f"funding percentile {fp}"

    total = sum(votes.values())
    majority = 1 if total > 0 else (-1 if total < 0 else 0)
    agree = sum(1 for v in votes.values() if v == majority and v != 0)
    dissent = sorted(k for k, v in votes.items() if v != majority and v != 0)

    bands = ["Short", "Lean-short", "Neutral-mixed", "Lean-long", "Long"]
    idx = 2 + (1 if total >= 2 else 0) + (1 if total >= 4 else 0) \
            - (1 if total <= -2 else 0) - (1 if total <= -4 else 0)
    idx = max(0, min(4, idx))
    compression = bool((a.get("volatility") or {}).get("compression_flag"))
    if compression:
        idx = idx - 1 if idx > 2 else (idx + 1 if idx < 2 else idx)

    radar_states = [r.get("state") for r in (a.get("radar") or [])
                    if isinstance(r, dict)]
    return {
        "votes": votes, "rationale": why,
        "total": total, "agree": agree, "of": 5,
        "dissenting": dissent,
        "print": f"{agree} of 5 agree" + (f", dissenting: {', '.join(dissent)}"
                                          if dissent else ", no dissent"),
        "band": bands[idx],
        "compression_demoted": compression,
        "weights": "equal, count-based, never fitted (§7.3)",
        "radar_states": radar_states,
        "disagreement_chip": bool(dissent),
        "not_reconciled": "the bias print and the radar measure different things; "
                          "when they disagree nothing is reconciled (§7.3)",
    }


def decision_instrument(a, vol, nest, conf, price, atr_d):
    """PART II, in the §2.2 order.  Derived from Part I under printed rules.

    SEQUENCING RULE: every input below is a number Part I prints.  A reader with
    Part I and the rules header can reconstruct all of this by hand.
    """
    area_map = {}
    for view in ("with_volume", "without_volume"):
        v = conf.get(view)
        if not v:
            continue
        area_map[view] = [
            {"mean": c["mean"], "score": c["score"], "families": c["families"],
             "member_count": c["member_count"],
             "scale_confirmed": sorted(
                 {w for m in c["members"] for w in (m.get("scale_confirmed") or [])})}
            for c in sorted(v.get("clusters") or [], key=lambda c: -c["score"])[:12]]

    return {
        "part": "II -- decision instrument",
        "answers": "where would I act, and what would prove me wrong?",
        "confluence_area_map": area_map,
        "lines_in_sand": {v: (conf.get(v) or {}).get("lines")
                          for v in ("with_volume", "without_volume")
                          if conf.get(v)},
        "lines_differ": conf.get("differ"),
        "hypothesis_drafts": hypothesis_drafts(conf, price, atr_d),
        "rr_ranking": rr_board(conf, price, atr_d),
        "rr_ranking_without_volume": rr_board(conf, price, atr_d,
                                              view="without_volume"),
        "composite_bias": composite_bias(a, vol, nest, conf, price),
        "sequencing_rule": "Part II is derivable from Part I's printed numbers "
                           "alone; no hidden inputs (§2.2)",
    }


def brief2_asset(a, klines, now_ms, price, atr_d):
    """Compute every BRIEF-2 layer for one asset: Part I additions, then Part II."""
    vol = volume_layer(klines, now_ms)
    rv = rvwap_layer(klines, now_ms)
    nest = nesting_layer(vol, price)
    osc = oscillator_layer(klines)
    prior = prior_anchored_vwaps(klines, now_ms)
    pivs = confirmed_pivot_levels(klines, now_ms)
    a = dict(a)
    a["brief2_oscillators"] = osc
    cross = cross_state_layer(klines, atr_d)
    lat = lattice_layer(klines)
    planes = chart_planes(klines, vol)
    stretch = stretch_layer(a, rv, prior, price, atr_d)
    excursion = excursion_layer(stretch, atr_d)
    reg = build_registry(a, vol, rv, nest["levels"], prior, pivs)
    conf = confluence(reg, price, atr_d)

    part1 = {"volume_windows": vol, "rvwap": rv, "va_nesting": nest,
             "oscillators": osc, "cross_state": cross, "lattice_12_25": lat,
             "chart_planes": planes, "prior_anchors": prior,
             "confirmed_pivots": pivs, "stretch": stretch,
             "band_excursions": excursion, "rvol": rvol_layer(klines),
             "confluence": conf}
    part2 = decision_instrument(a, vol, nest, conf, price, atr_d)
    return part1, part2


# ══════════════════════════════════════════════════ §8.1 the capture envelope

# 2.1.0 -- D-1 (reviewer ruling 2026-08-03): dual_score no longer emits the flat
# `members` list beside `clusters[].members`.  The collapsed registry was stored
# twice, at 18.12% of the capture.  Captures written under 2.0.0 remain readable
# and are simply larger; the bump is what tells the two apart.
SCHEMA_VERSION = "2.1.0"

# §8.1 ratified A-6.  The closed-bar correction plus the volume filter MOVE
# published numbers, and archive-comparability law requires a major bump.  The
# f_an_8_diff table is the bridge between eras.
RULES_VERSION = "2.0.0"

# §2.3 ratified A-3.  Session-anchored slots, times HELD IN America/New_York and
# resolved through the zone at generation time -- the UTC times below are the
# standard-time renderings and shift with US DST, which is why the zone and not
# the UTC offset is the stored quantity.
SLOTS = {
    "london": {"utc_hint": "12:00", "local": "07:00", "zone": "America/New_York"},
    "ny_am": {"utc_hint": "15:00", "local": "10:00", "zone": "America/New_York"},
    "post_ny": {"utc_hint": "21:30", "local": "16:30", "zone": "America/New_York"},
}


def capture_envelope(date, slot, parity_certified=False, engine_version=None,
                     universe=None, extra_rules=None):
    """The provenance envelope every capture embeds (§8.1).

    ADOPTION AND PARITY ARE SEPARATE GATES.  This amendment may be BUILT before
    the operator's parity readings return; its output may not be TRUSTED until
    they do.  So `banner` is a function of `parity_certified` and F-B33 asserts
    both directions -- present while unset, cleared only when set.  A banner that
    were merely a constant string would assert nothing.
    """
    if slot not in SLOTS:
        raise ValueError(f"unknown slot {slot!r}; expected one of {sorted(SLOTS)}")

    rules = {
        "rules_version": RULES_VERSION,
        "windows": list(WINDOWS),
        "retired_windows": ["5d", "20d"],
        "profile_rows": P.PROFILE_ROWS,
        "value_area": P.VALUE_AREA,
        "lvn_threshold": P.LVN_THRESHOLD,
        "lvn_min_rows": P.LVN_MIN_ROWS,
        "window_substrate": dict(P.WINDOW_SUBSTRATE),
        "collapse_atr": L.COLLAPSE_ATR,
        "cluster_atr": L.CLUSTER_ATR,
        "lis_atr": L.LIS_ATR,
        "family_cap": L.FAMILY_CAP,
        "families": list(L.FAMILIES),
        "volume_families": list(L.VOLUME_FAMILIES),
        "sensitivity_tolerances": [0.10, L.CLUSTER_ATR, 0.20],
        "sigmas": list(SIGMAS),
        "oscillator_timeframes": list(OSC_TFS),
        "lattice_emas": list(LATTICE_EMAS),
        "scoring": "sum over families of min(count, cap) + distinct families -- "
                   "counted, never fitted",
        "forming_candle": "drawn and greyed; excluded from every computed value",
        "slots": {k: dict(v) for k, v in SLOTS.items()},
    }
    if extra_rules:
        rules.update(extra_rules)

    doc = {
        "schema": "naiad_daily_brief",
        "schema_version": SCHEMA_VERSION,
        "date": date,
        "slot": slot,
        "slot_zone": SLOTS[slot]["zone"],
        "rules_version": RULES_VERSION,
        "rules": rules,
        "rules_sha256": canonical_rules_sha256(rules),
        "analytics_version": analytics.ANALYTICS_VERSION,
        "analytics_sha": analytics.analytics_sha(),
        "engine_version": engine_version,
        "universe": list(universe or []),
        "parity_certified": bool(parity_certified),
        "banner": None if parity_certified else PARITY_BANNER,
        "firewall": ("ops artifact, never study evidence; no journal reads, no "
                     "lockbox outcome statistics; confluence measures agreement "
                     "between tools, not edge"),
        "lockbox": {"window": [analytics.LOCKBOX_START_MS,
                               analytics.LOCKBOX_END_MS],
                    "policy": "seal governs scored outcome evidence, not raw "
                              "price in a display-only trailing window "
                              "(operator ruling 2026-08-03); every windowed "
                              "layer discloses its overlap"},
    }
    return doc


def canonical_rules_sha256(rules):
    """sha256 over the rule set, canonically serialised.

    Sorted keys and compact separators, so the same rules always hash the same
    regardless of insertion order -- a capture's rules_sha256 is what lets two
    archived captures be compared without trusting their prose.
    """
    import hashlib
    import json
    blob = json.dumps(rules, sort_keys=True, separators=(",", ":"),
                      default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()
