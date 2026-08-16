"""TIER-C4 · THE INDEPENDENT RE-DERIVATION — a second pair of hands.

NOT a fixture.  The ten-fixture contract is `scripts/tierc4_fixtures.py` and is
unchanged; this is a BUILDER'S CHECK filed so that the strongest check in the
build is reproducible rather than asserted.  It exits non-zero on any
disagreement.

WHY IT EXISTS
─────────────
Every fixture in `tierc4_fixtures.py` re-derives its evidence from raw bars, but
it re-derives it by calling the SAME functions the program called — that is what
makes a fixture cheap and it is also its limit.  Tier-C3's seal breach was found
by an adversarial audit that had no fixture, and the lesson recorded there is
that a build should be able to answer "what if the decision path itself is
wrong?" without appealing to the decision path.

So this module re-implements the WHOLE v4 card from the CARD TEXT, sharing with
the build ONLY:

    engine.indicators.ema / .atr   the estate's EMA/ATR primitives of record,
                                   which Stage B must ride identically anyway
    engine.data.cache_dir          the kline/funding cache location
    the raw parquet bars themselves

and sharing NOTHING else.  The (5,5) anchor scan, the (2,2) fractal scan, the
cross detector, the arming loop, the tide and displacement gates, the seal mask,
the ride, the ratchet, the harvest and the accounting are all written again here
from the card, in a different shape (a naive O(n) python scan rather than the
vectorised `engine.s1._pivots`, an inline cross rather than
`engine.indicators.crossover`, one flat loop rather than the program's layered
closures).  It imports NEITHER `tierc4_rules` NOR `tierc4_baseline` NOR their
parents.

It then compares, per trade, against the FILED `trade_journal.parquet`:
entry instant, R, advance count, harvest flag and net R.

WHAT A PASS MEANS AND WHAT IT DOES NOT
──────────────────────────────────────
A pass means two independent readings of the card agree on every number.  It
does NOT mean the card is right, that the corridor is representative, or that
either reading matches the operator's intent — those are §10's findings and the
operator's rulings.  It rules out one specific failure: that the shipped numbers
are an artefact of how the program is factored.

USAGE  ~/venvs/naiad/bin/python scripts/tierc4_independent.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine import indicators as ind                              # noqa: E402
from engine.data import cache_dir                                 # noqa: E402

KLINES = cache_dir() / "klines"
FUNDING = cache_dir() / "funding"
FILED = ROOT / "research_outputs" / "tierc4" / "trade_journal.parquet"

MS_1H, MS_4H, MS_1D = 3_600_000, 14_400_000, 86_400_000
UNIVERSE = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT")


def _ms(s: str) -> int:
    return int(pd.Timestamp(s, tz="UTC").value // 10 ** 6)


def _iso(m: int) -> str:
    return pd.Timestamp(int(m), unit="ms", tz="UTC").strftime("%Y-%m-%dT%H:%M:%SZ")


# ── the card's own numbers, typed out again on purpose ────────────────────
SCORED_LO, SCORED_HI = _ms("2025-10-06"), _ms("2026-01-31") + MS_1D - 1
LEAD_IN_DAYS = 30
LOCKBOX_LO, LOCKBOX_HI = _ms("2024-07-01"), _ms("2025-10-05") + MS_1D - 1
TIDE_FAST, TIDE_SLOW = 89, 316
WINDOW_FAST, WINDOW_SLOW = 12, 89
TRIGGER_FAST, TRIGGER_SLOW = 12, 26
D_MIN = 0.75
ATR_LEN = 14
ANCHOR_L = ANCHOR_R = 5
ANCHOR_LOOKBACK = 200
STOP_BUF = 0.5
MIN_STOP_ATR = 1.0
FRACTAL_L = FRACTAL_R = 2
HARVEST_FRACTION = 0.5
FEE_BPS_SIDE = 5.0


def strict_pivot_bars(x: np.ndarray, L: int, R: int, low: bool) -> np.ndarray:
    """Strict (L,R) extremes as a boolean mask over PIVOT BARS.

    Deliberately the naive loop, not `engine.s1._pivots`' rolling/shift form:
    if the two disagree anywhere this module is supposed to say so.
    """
    n = len(x)
    out = np.zeros(n, bool)
    for p in range(L, n - R):
        left, right = x[p - L:p], x[p + 1:p + 1 + R]
        out[p] = ((x[p] < left.min() and x[p] < right.min()) if low
                  else (x[p] > left.max() and x[p] > right.max()))
    return out


def cross_up(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """a crosses ABOVE b: a>b now AND a<=b prior. NaN compares False, as the
    engine's `crossover` specifies — written out rather than imported."""
    prev = np.r_[True, a[:-1] <= b[:-1]]
    return (a > b) & prev


def replay(sym: str) -> list[dict]:
    k = (pd.read_parquet(KLINES / f"{sym}_4h.parquet")
         .sort_values("open_time").reset_index(drop=True))
    ot = k["open_time"].to_numpy(np.int64)
    h = k["high"].to_numpy(float)
    lo = k["low"].to_numpy(float)
    c = k["close"].to_numpy(float)
    e12 = ind.ema(c, TRIGGER_FAST)
    e26 = ind.ema(c, TRIGGER_SLOW)
    e89 = ind.ema(c, TIDE_FAST)
    e316 = ind.ema(c, TIDE_SLOW)
    atr = ind.atr(h, lo, c, ATR_LEN)

    funding: dict[int, float] = {}
    fp = FUNDING / f"{sym}.parquet"
    if fp.exists():
        d = pd.read_parquet(fp)
        for ft, fr in zip(d["funding_time"].astype(np.int64),
                          d["funding_rate"].astype(float)):
            key = int(ft) // MS_1H * MS_1H
            funding[key] = funding.get(key, 0.0) + fr

    anc_lo = strict_pivot_bars(lo, ANCHOR_L, ANCHOR_R, low=True)
    anc_hi = strict_pivot_bars(h, ANCHOR_L, ANCHOR_R, low=False)
    fr_lo = strict_pivot_bars(lo, FRACTAL_L, FRACTAL_R, low=True)
    fr_hi = strict_pivot_bars(h, FRACTAL_L, FRACTAL_R, low=False)
    sealed = (ot >= LOCKBOX_LO) & (ot <= LOCKBOX_HI)

    w_up, w_dn = cross_up(e12, e89), cross_up(e89, e12)
    t_up, t_dn = cross_up(e12, e26), cross_up(e26, e12)
    b_up, b_dn = cross_up(e89, e316), cross_up(e316, e89)

    lead_lo = SCORED_LO - LEAD_IN_DAYS * MS_1D
    lead_i = int(np.searchsorted(ot, lead_lo, "left"))
    hi_i = int(np.searchsorted(ot, SCORED_HI, "right")) - 1

    arms = []
    for d_, opens, counter in ((1, w_up, w_dn), (-1, w_dn, w_up)):
        for i in np.flatnonzero(opens):
            i = int(i)
            if not (lead_i <= i <= hi_i):
                continue
            later = np.flatnonzero(counter[i + 1:])
            arms.append((int(ot[i]), -d_, i, d_,
                         int(i + 1 + later[0]) if later.size else len(c)))
    arms.sort()

    out, open_until = [], -1
    for _arm_ms, _neg, i, d_, end in arms:
        tide = ((e89[i] > e316[i] and c[i] > e316[i]) if d_ == 1
                else (e89[i] < e316[i] and c[i] < e316[i]))
        if not tide:
            continue
        a_i = float(atr[i])
        if not (np.isfinite(a_i) and a_i > 0 and abs(c[i] - e89[i]) / a_i >= D_MIN):
            continue
        tf = t_up if d_ == 1 else t_dn
        cand = np.flatnonzero(tf[i:min(end, hi_i + 1)])
        if cand.size == 0:
            continue
        ti = int(i + cand[0])
        if ti <= open_until:
            continue
        entry_px, atr_sig = float(c[ti]), float(atr[ti])
        if not np.isfinite(atr_sig):
            continue

        # THE ENTRY ANCHOR — nearest confirmed strict (5,5) pivot beyond entry,
        # within 200 bars, whose own bar is not sealed.
        best = None
        mask, series = (anc_lo, lo) if d_ == 1 else (anc_hi, h)
        for p in np.flatnonzero(mask):
            p = int(p)
            if p + ANCHOR_R > ti or ti - (p + ANCHOR_R) > ANCHOR_LOOKBACK:
                continue
            if sealed[p]:
                continue
            if (series[p] >= entry_px) if d_ == 1 else (series[p] <= entry_px):
                continue
            if best is None or ((series[p] > series[best]) if d_ == 1
                                else (series[p] < series[best])):
                best = p
        if best is None:
            continue
        anchor = float(series[best])
        pivot_stop = anchor - d_ * STOP_BUF * atr_sig
        rail_stop = entry_px - d_ * MIN_STOP_ATR * atr_sig
        stop0 = (min(pivot_stop, rail_stop) if d_ == 1
                 else max(pivot_stop, rail_stop))
        r_dist = abs(entry_px - stop0)
        if not (np.isfinite(r_dist) and r_dist > 0):
            continue
        scored = bool(ot[ti] >= SCORED_LO)

        # THE RIDE — stop, bell, harvest, ratchet; the advance governs bar j+1.
        stop, harv, n_adv = float(stop0), None, 0
        xi, xpx, xreason = hi_i, float(c[hi_i]), "corridor_end"
        for j in range(ti + 1, hi_i + 1):
            edge = (max(e89[j], e316[j]) if d_ == 1 else min(e89[j], e316[j]))
            touch = (harv is None
                     and ((lo[j] <= edge) if d_ == 1 else (h[j] >= edge)))
            if (d_ == 1 and lo[j] <= stop) or (d_ == -1 and h[j] >= stop):
                xi, xpx, xreason = j, stop, "stop"
                break
            bell = ((w_dn[j] or b_dn[j]) if d_ == 1 else (w_up[j] or b_up[j]))
            if bell:
                xi, xpx, xreason = j, float(c[j]), "bell"
                break
            if touch:
                harv = (j, float(c[j]))
            p = j - FRACTAL_R
            fm = fr_lo if d_ == 1 else fr_hi
            if p >= 0 and fm[p] and not sealed[p]:
                pv = float(lo[p] if d_ == 1 else h[p])
                A = float(atr[j])
                if np.isfinite(A) and A > 0:
                    cd = pv - d_ * STOP_BUF * A
                    rl = float(c[j]) - d_ * MIN_STOP_ATR * A
                    adm = min(cd, rl) if d_ == 1 else max(cd, rl)
                    if (adm > stop) if d_ == 1 else (adm < stop):
                        stop, n_adv = adm, n_adv + 1
        open_until = xi
        if not scored:
            continue

        def accrue(lo_j: int, hi_j: int, qty: float) -> float:
            s = 0.0
            for j in range(lo_j + 1, hi_j + 1):
                rate = funding.get(int(ot[j]))
                if rate:
                    s += rate * float(c[j - 1]) * d_ * qty
            return s

        bps = FEE_BPS_SIDE / 10_000.0
        if harv is None:
            gross = (xpx - entry_px) * d_
            fee = bps * (entry_px + xpx)
            fund = accrue(ti, xi, 1.0)
        else:
            hj, hpx = harv
            q = HARVEST_FRACTION
            gross = q * (hpx - entry_px) * d_ + (1 - q) * (xpx - entry_px) * d_
            fee = bps * q * (entry_px + hpx) + bps * (1 - q) * (entry_px + xpx)
            fund = accrue(ti, hj, q) + accrue(ti, xi, 1 - q)
        out.append({"asset": sym, "entry_ts": _iso(int(ot[ti])),
                    "r_dist": r_dist, "n_advances": n_adv,
                    "harvested": harv is not None, "exit_reason": xreason,
                    "net_r": (gross - fee - fund) / r_dist})
    return out


def main() -> int:
    if not FILED.exists():
        print(f"HALT: filed journal absent at {FILED} — run "
              f"scripts/tierc4_baseline.py --stage all first.")
        return 1
    mine = pd.DataFrame([r for s in UNIVERSE for r in replay(s)])
    filed = pd.read_parquet(FILED)[
        ["asset", "entry_ts", "r_dist", "n_advances", "harvested", "net_r"]]
    print("=" * 78)
    print("TIER-C4 · INDEPENDENT RE-DERIVATION — builder's check, not a fixture")
    print("=" * 78)
    print(f"  shares with the build: engine.indicators.ema/.atr, "
          f"engine.data.cache_dir, the raw bars. NOTHING else.")
    print(f"  imports tierc4_rules / tierc4_baseline: NO")
    print()
    m = mine.merge(filed, on=["asset", "entry_ts"], how="outer",
                   indicator=True, suffixes=("_indep", "_filed"))
    ok = True
    # PRECISION, STATED RATHER THAN CHOSEN: the filed journal is written at 6 dp
    # (`write_table` rounds every float column), so agreement is testable at 6 dp
    # and no finer. This module's own values are full precision; they are rounded
    # the same way before comparison and then required to agree to 1e-9. The raw
    # unrounded gap is printed in the summary so the reader can see it is not
    # hiding anything.
    worst_raw = 0.0
    print(f"{'asset':9} {'entry':21} {'R indep':>13} {'R filed':>13} "
          f"{'net indep':>11} {'net filed':>11} {'adv':>7} {'harv':>9}")
    for _, r in m.sort_values(["asset", "entry_ts"]).iterrows():
        both = r["_merge"] == "both"
        if both:
            worst_raw = max(worst_raw,
                            abs(float(r["net_r_indep"]) - float(r["net_r_filed"])))
        dr = (abs(round(float(r["r_dist_indep"]), 6) - float(r["r_dist_filed"]))
              if both else float("inf"))
        dn = (abs(round(float(r["net_r_indep"]), 6) - float(r["net_r_filed"]))
              if both else float("inf"))
        da = (int(r["n_advances_indep"]) == int(r["n_advances_filed"])) if both else False
        dh = (bool(r["harvested_indep"]) == bool(r["harvested_filed"])) if both else False
        good = both and dr < 1e-9 and dn < 1e-9 and da and dh
        ok &= good
        print(f"[{'OK ' if good else 'BAD'}] {r['asset']:9} {r['entry_ts']:21} "
              f"{r['r_dist_indep']:13.6f} {r['r_dist_filed']:13.6f} "
              f"{r['net_r_indep']:11.6f} {r['net_r_filed']:11.6f} "
              f"{str(r['n_advances_indep']) + '/' + str(r['n_advances_filed']):>7} "
              f"{str(r['harvested_indep']) + '/' + str(r['harvested_filed']):>9}"
              f"{'' if both else '   ' + str(r['_merge'])}")
    same_n = len(mine) == len(filed)
    ok &= same_n
    print()
    print(f"[{'OK ' if same_n else 'BAD'}] population: independent {len(mine)} "
          f"trades == filed {len(filed)}")
    print(f"      independent net R {mine['net_r'].sum():+.4f} · expectancy "
          f"{mine['net_r'].mean():+.4f} · advances "
          f"{int(mine['n_advances'].sum())} · harvests "
          f"{int(mine['harvested'].sum())}")
    print(f"      filed       net R {filed['net_r'].sum():+.4f} · expectancy "
          f"{filed['net_r'].mean():+.4f} · advances "
          f"{int(filed['n_advances'].sum())} · harvests "
          f"{int(filed['harvested'].sum())}")
    print(f"      worst gap between this module's UNROUNDED value and the filed "
          f"6-dp value: {worst_raw:.3e}")
    print(f"      — that is BOUNDED BY 5e-7 by the rounding alone, so it is a "
          f"floor on what this comparison can see, not a measurement of "
          f"disagreement. The comparison above is at 6 dp for that reason.")
    print("=" * 78)
    if not ok:
        print("*** HALT: two readings of the card disagree. ***")
        return 1
    print("AGREED on every trade. This rules out ONE failure — that the shipped")
    print("numbers are an artefact of how the program is factored. It does not")
    print("say the card is right; that is the operator's ruling, not a test's.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
