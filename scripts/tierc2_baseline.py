"""TIER-C2 · THE FORWARD BASELINE — "the number every multiplier must beat".

RATIFIED operator 2026-08-15 ("let's go"; defaults per the interview leans, each
[VETO] by name).  Drafted APOLLO · Executor HEPHAESTUS · Seed 20260815.

CLASS: MEASUREMENT, NOT REGISTRATION.  Probe-ledger entry m = 0.  No lockbox
spend.  No estate write.  No live orders.  Box additions < 0.5%.

    STAGE A   clean-corridor replay of the rule card, five assets, both
              directions, paper accounting.  THE FUNNEL · THE HEADLINE ·
              the trade journal.
    A-TAPE    (Amendment B1) the analytics tape — CAPTURED, NEVER CONSULTED.
    STAGE B   the same rule card as an engine paper profile + one heartbeat.

THE DECISION PATH IS NOT IN THIS FILE.  It is `scripts/tierc2_rules.py`, whose
import closure contains no `analytics` module — that separation IS fixture
F-C2-6, and it is why Amendment B1's "captured-not-consulted" is a property of
the program rather than a promise in a document.  This file may import both;
`tierc2_rules` may import only `engine`.

────────────────────────────────────────────────────────────────────────────
THE CORRIDOR, AND WHY IT IS NOT THE ONE THE PASTE NAMED
────────────────────────────────────────────────────────────────────────────
The ratified STAGE A corridor was 2024-07-01 -> 2026-01-31.  Its first 462 days
(79.7%) ARE the sealed lockbox: `V12_Study_Charter_Addendum_v1.0.md` VR-1 pins
it at 2024-07-01T00:00:00Z -> 2025-10-05T23:59:59Z, `engine/replay.py:48-49`
encodes the same bounds, and `engine/replay.py:152` refuses any replay window
touching it without `NAIAD_LOCKBOX_ACK` because "unlocking is an operator act".
`LEDGER.md:865` rules the seal governs SCORED OUTCOME EVIDENCE — which is
precisely what THE HEADLINE is — and not raw price in a display-only window.

Raised to the operator 2026-08-15 with the arithmetic; ruling: SEAL INTACT,
score the post-lockbox remainder.  So:

    SCORED          2025-10-06 -> 2026-01-31      118 d    the yardstick
    NOT COMPUTED    2024-07-01 -> 2025-10-05      462 d    SEALED LOCKBOX
    DISPLAY-ONLY    exploration-classic (< 2024-07-01)     census-scored era
    DISPLAY-ONLY    2026-02-01 -> 2026-08-11               pinning window

The lockbox strip is NOT COMPUTED rather than display-only: a strip of net R
over sealed bars is scored outcome evidence wearing a label.  The other two
strips carry outcomes because neither is sealed.

WARM-UP TRAVERSAL IS DISCLOSED, NOT HIDDEN.  e316 on 4h needs ~316 bars of
history, so the EMA recursion traverses lockbox bars to reach 2025-10-06 warm.
That is the F4-a posture already on the record (`LEDGER.md:121`: "lockbox
warm-up traversal disclosed per cell in manifest; zero journal rows with
lockbox open times") — traversal is not emission, and NO row of any scored
table carries a lockbox timestamp.  F-C2-5 proves it by min/max ts per table.
────────────────────────────────────────────────────────────────────────────

USAGE
    ~/venvs/naiad/bin/python scripts/tierc2_baseline.py --stage all
    ~/venvs/naiad/bin/python scripts/tierc2_baseline.py --stage {replay,tape,tables}
    ~/venvs/naiad/bin/python scripts/tierc2_baseline.py --stage all --rerun   # F-C2-4
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc2_rules as RC                                          # noqa: E402
from engine.data import cache_dir                                  # noqa: E402

# The registry side.  Imported HERE and never in `tierc2_rules` — F-C2-6.
import analytics as AN                                             # noqa: E402
from analytics import structure as AS                              # noqa: E402
from analytics import vwap as AW                                   # noqa: E402
from analytics import volatility as AV                             # noqa: E402

SEED = 20260815                 # rule-card header; no stochastic step uses it,
                                # which is itself printed (F-C2-4)
OUT = ROOT / "research_outputs" / "tierc2"
OUT_RERUN = ROOT / "research_outputs" / "tierc2_run2"

# ── the four windows, as ruled ────────────────────────────────────────────
def _ms(s: str) -> int:
    return int(datetime.strptime(s, "%Y-%m-%d")
               .replace(tzinfo=timezone.utc).timestamp() * 1000)


SCORED = ("2025-10-06", "2026-01-31")
LOCKBOX = ("2024-07-01", "2025-10-05")        # NOT COMPUTED — sealed
CENSUS_ERA = ("2019-09-08", "2024-06-30")     # display-only, exploration-classic
PINNING = ("2026-02-01", "2026-08-11")        # display-only, crosses VR-1 forward edge

WINDOWS = {
    "SCORED":      {"span": SCORED,     "scored": True,
                    "note": "the yardstick"},
    "CENSUS_ERA":  {"span": CENSUS_ERA, "scored": False,
                    "note": "exploration-classic — the census-scored era"},
    "PINNING":     {"span": PINNING,    "scored": False,
                    "note": "the pinning window"},
}

DISPLAY_ONLY_HEADER = ("DISPLAY-ONLY — hypothesis generation only, never evidence")

# The RIDE-ONLY lineage row, quoted for print-beside.  PINNED + LABELLED
# HISTORICAL per CONVENTIONS §6.4 leg 3: this reproduces a filed record
# (BUILD_2026-08-12_CENSUS2A_RUN_6.md §2.3) and must never track a live value.
CENSUS_RIDE_ONLY = {
    "source": "CENSUS-2A CEN-5, BUILD_2026-08-12_CENSUS2A_RUN_6.md §2.3 "
              "(restated CENSUS2A_CLOSEOUT_2026-08-12.md:59-61 F1)",
    "era": "2019-10-01T01:13Z -> 2024-06-30T17:53Z (exploration-classic)",
    "ruler": "gross R = (exit-entry)/|entry-stop|, SIZE-FREE, NOT net of toll",
    "rows": [("loss", 5829, -1.0415, -0.9690),
             ("win", 814, +2.1422, +9.4458),
             ("ALL", 6643, -1.0324, +0.3072)],
    "win_rate_pct": 12.2535,
    "sum_r": 2040.9022,
}

MS_4H, MS_1H, MS_1D = 14_400_000, 3_600_000, 86_400_000
LOG_LINES: list[str] = []


def log(msg: str = "") -> None:
    print(msg)
    LOG_LINES.append(msg)


def iso(ms: int | float) -> str:
    return (datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ"))


def r4(x):
    return None if x is None or (isinstance(x, float) and not np.isfinite(x)) \
        else round(float(x) + 0.0, 4)


def r6(x):
    return None if x is None or (isinstance(x, float) and not np.isfinite(x)) \
        else round(float(x) + 0.0, 6)


def pct(x, d):
    return None if not d else r4(100.0 * x / d)


# ═══════════════════════════════════════════════ determinism plumbing
def _content_sha(df: pd.DataFrame) -> str:
    """Canonicalised CONTENT hash, not parquet bytes — `mc1_program.py:1910`.
    Parquet embeds a writer version and (on some builds) a creation stamp, so
    byte-hashing a parquet is a determinism test of pyarrow, not of us."""
    return hashlib.sha256(df.to_csv(index=False).encode("utf-8")).hexdigest()


def _round_floats(df: pd.DataFrame, nd: int = 6) -> pd.DataFrame:
    d = df.copy()
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].round(nd)
    return d


def write_table(df: pd.DataFrame, name: str, keys: list[str],
                root: Path) -> str:
    """Sort by a TOTAL key, round, write atomically, return the content sha.

    Atomic because a killed run leaves a footerless parquet stump that
    `Path.exists()` happily accepts (`census2b_program.py:240-252`).
    """
    root.mkdir(parents=True, exist_ok=True)
    d = _round_floats(df)
    if keys:
        assert_key(d, keys, name)
        d = d.sort_values(keys, kind="mergesort").reset_index(drop=True)
    sha = _content_sha(d)
    p = root / f"{name}.parquet"
    tmp = p.with_suffix(".parquet.tmp")
    d.to_parquet(tmp, index=False)
    os.replace(tmp, p)
    log(f"    wrote {name:28} rows={len(d):>7,}  sha={sha[:16]}")
    return sha


def assert_key(df: pd.DataFrame, keys: list, label: str) -> None:
    """F-KEY — transcribed from `census2a_program.py:2217`.  A join key must be
    DECLARED and UNIQUE, before the join.  HALTs; always logs, so a green run
    shows the key it checked."""
    dup = int(df.duplicated(subset=keys).sum())
    log(f"    F-KEY  {label:30} key={keys} rows={len(df):,} dup={dup}")
    if dup:
        ex = df[df.duplicated(subset=keys, keep=False)].head(3)[keys].to_dict("records")
        raise SystemExit(f"HALT (F-KEY): '{label}' key {keys} is NOT unique — "
                         f"{dup} duplicate row(s), e.g. {ex}. A join on a "
                         f"non-unique key silently drops or multiplies rows.")


# ═══════════════════════════════════════════════════════ the estate (read-only)
KLINES = cache_dir() / "klines"
FUNDING = cache_dir() / "funding"


def load_klines(sym: str, tf: str) -> pd.DataFrame:
    p = KLINES / f"{sym}_{tf}.parquet"
    if not p.exists():
        raise SystemExit(f"HALT: missing {p}")
    return pd.read_parquet(p).sort_values("open_time").reset_index(drop=True)


def load_funding(sym: str) -> dict[int, float]:
    """Funding rates keyed to the hour they land on.

    Convention transcribed from `engine/trading.py:238-246`: Binance funding
    stamps jitter a few ms past the hour (16:00:00.012), so floor to the hour;
    rates on the same hour SUM defensively.
    """
    p = FUNDING / f"{sym}.parquet"
    if not p.exists():
        return {}
    d = pd.read_parquet(p)
    out: dict[int, float] = {}
    for ft, fr in zip(d["funding_time"].astype(np.int64),
                      d["funding_rate"].astype(float)):
        k = int(ft) // MS_1H * MS_1H
        out[k] = out.get(k, 0.0) + fr
    return out


# ═══════════════════════════════════════════════════════════ STAGE A · replay
def _idx_range(open_ms: np.ndarray, lo_ms: int, hi_ms: int) -> tuple[int, int]:
    """Inclusive index range of bars whose OPEN time lies in [lo, hi]."""
    lo = int(np.searchsorted(open_ms, lo_ms, "left"))
    hi = int(np.searchsorted(open_ms, hi_ms, "right")) - 1
    return lo, hi


def replay_asset(sym: str, win_name: str, k4: pd.DataFrame, k1: pd.DataFrame,
                 funding: dict[int, float]) -> tuple[list, list]:
    """The rule card, ridden bar by bar.  Returns (armings, trades).

    EMAs and ATR are computed over the FULL loaded history and only THEN
    restricted to the window, so a window edge can never move an indicator.
    That is the warm-up traversal disclosed in the module docstring.
    """
    span = WINDOWS[win_name]["span"]
    lo_ms, hi_ms = _ms(span[0]), _ms(span[1]) + MS_1D - 1

    f = RC.build_4h(k4["open_time"].to_numpy(np.int64),
                    k4["open"].to_numpy(float), k4["high"].to_numpy(float),
                    k4["low"].to_numpy(float), k4["close"].to_numpy(float))
    pv = RC.build_pivots_1h(k1["high"].to_numpy(float), k1["low"].to_numpy(float))
    h1_open = k1["open_time"].to_numpy(np.int64)

    lo_i, hi_i = _idx_range(f.open_ms, lo_ms, hi_ms)
    if hi_i < lo_i:
        return [], []

    arms = RC.armings(sym, f, lo_i, hi_i)
    trades: list[RC.Trade] = []
    open_until = -1              # 4h index the open position releases at
    x = RC._crosses(f)           # hoisted: the cross grid is per-asset, not per-arming

    for a in arms:
        if not a.tide_ok:
            a.reject = "tide"
            continue
        if not a.d_ok:
            a.reject = "d"
            continue

        # TRIGGER — first in-window 12/26 cross in the arming's direction.
        trig_flags = x["t_up"] if a.direction == 1 else x["t_dn"]
        end = min(a.window_end_i, hi_i + 1)
        cand = np.flatnonzero(trig_flags[a.arm_i:end])
        if cand.size == 0:
            a.reject = "no_trigger"
            continue
        ti = int(a.arm_i + cand[0])
        a.trigger_i, a.trigger_ms = ti, int(f.open_ms[ti])

        # ONE POSITION PER ASSET — a trigger arriving while a position is open
        # is a real leak and is counted as one, never silently dropped.
        if ti <= open_until:
            a.reject = "position_open"
            continue

        entry_px = float(f.c[ti])
        atr_sig = float(f.atr[ti])
        # the 1h bar that CLOSES with this 4h bar: open = 4h open + 3h
        cur_1h = int(np.searchsorted(h1_open, int(f.open_ms[ti]) + 3 * MS_1H, "right")) - 1
        stop_px = RC.struct_stop(pv, cur_1h, entry_px, a.direction, atr_sig)
        if stop_px is None:
            a.reject = "no_struct_anchor"
            continue
        r_dist = abs(entry_px - stop_px)
        if not (np.isfinite(r_dist) and r_dist > 0):
            a.reject = "degenerate_R"
            continue

        a.entered = True
        a.reject = "entered"

        # ── RIDE.  No management of any kind. ──────────────────────────────
        def ride(honour_stop: bool):
            for j in range(ti + 1, hi_i + 1):
                if honour_stop:
                    if a.direction == 1 and f.l[j] <= stop_px:
                        return j, stop_px, "stop"
                    if a.direction == -1 and f.h[j] >= stop_px:
                        return j, stop_px, "stop"
                if a.direction == 1:
                    if bool(x["w_dn"][j]):
                        return j, float(f.c[j]), "bell_12_89"
                    if bool(x["b_dn"][j]):
                        return j, float(f.c[j]), "bell_89_316"
                else:
                    if bool(x["w_up"][j]):
                        return j, float(f.c[j]), "bell_12_89"
                    if bool(x["b_up"][j]):
                        return j, float(f.c[j]), "bell_89_316"
            return hi_i, float(f.c[hi_i]), "corridor_end"

        xi, xpx, xreason = ride(True)
        bi, bpx, breason = ride(False)
        open_until = xi

        def account(exit_i, exit_px):
            gross = (exit_px - entry_px) * a.direction
            fee = (RC.FEE_BPS_SIDE / 10_000.0) * (entry_px + exit_px)
            fund = 0.0
            for j in range(ti + 1, exit_i + 1):
                rate = funding.get(int(f.open_ms[j]))
                if rate:                      # qty = 1 unit, on last closed px
                    fund += rate * float(f.c[j - 1]) * a.direction
            return gross / r_dist, fee / r_dist, fund / r_dist

        g_r, fee_r, fund_r = account(xi, xpx)
        gb_r, feeb_r, fundb_r = account(bi, bpx)

        trades.append(RC.Trade(
            symbol=sym, direction=a.direction, arm_i=a.arm_i, arm_ms=a.arm_ms,
            entry_i=ti, entry_ms=int(f.open_ms[ti]), entry_px=entry_px,
            stop_px=stop_px, r_dist=r_dist,
            pivot_anchor=stop_px + (RC.STOP_BUF_ATR * atr_sig * a.direction),
            atr_at_entry=atr_sig, disp_at_arming=a.disp,
            exit_i=xi, exit_ms=int(f.open_ms[xi]), exit_px=xpx,
            exit_reason=xreason, bars_held=xi - ti,
            gross_r=g_r, fee_r=fee_r, funding_r=fund_r,
            net_r=g_r - fee_r - fund_r,
            gross_r_bellonly=gb_r, net_r_bellonly=gb_r - feeb_r - fundb_r,
            exit_reason_bellonly=breason, exit_ms_bellonly=int(f.open_ms[bi]),
        ))

    return arms, trades


# ═══════════════════════════════════════════════════════ THE FUNNEL
def funnel_table(arms: list) -> pd.DataFrame:
    """Per stone: armings seen -> passed tide -> passed d -> triggered ->
    entered -> belled, per asset/direction.  WHERE THE SYSTEM LEAKS, COUNTED.

    Cumulative by construction: each column is a subset of the one before it,
    so `leak_*` columns are exact differences and the rows reconcile.
    """
    rows = []
    for sym in RC.UNIVERSE:
        for d, dname in ((1, "long"), (-1, "short")):
            a = [x for x in arms if x.symbol == sym and x.direction == d]
            seen = len(a)
            tide = [x for x in a if x.tide_ok]
            dd = [x for x in tide if x.d_ok]
            trig = [x for x in dd if x.trigger_i is not None]
            ent = [x for x in trig if x.entered]
            rows.append({
                "asset": sym, "direction": dname,
                "armings_seen": seen, "passed_tide": len(tide),
                "passed_d": len(dd), "triggered": len(trig),
                "entered": len(ent),
                "leak_tide": seen - len(tide),
                "leak_d": len(tide) - len(dd),
                "leak_no_trigger": len(dd) - len(trig),
                "leak_position_open": sum(1 for x in trig if x.reject == "position_open"),
                "leak_no_struct_anchor": sum(1 for x in trig if x.reject == "no_struct_anchor"),
                "leak_degenerate_R": sum(1 for x in trig if x.reject == "degenerate_R"),
            })
    return pd.DataFrame(rows)


def strip_d_table(arms: list) -> pd.DataFrame:
    """The {0.50, 1.00} sensitivity strip.  UNSCORED — counts only, no outcome,
    because a swept threshold with an R attached is a selection surface."""
    rows = []
    for s in (RC.D_STRIP[0], RC.D_DISPLACEMENT, RC.D_STRIP[1]):
        tide = [x for x in arms if x.tide_ok]
        if s == RC.D_DISPLACEMENT:
            ok = [x for x in tide if x.d_ok]
        else:
            ok = [x for x in tide if x.strip_d_ok.get(s)]
        rows.append({"d": s, "is_ratified": bool(s == RC.D_DISPLACEMENT),
                     "passed_tide": len(tide), "passed_d": len(ok),
                     "pass_pct": pct(len(ok), len(tide))})
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════ THE HEADLINE
def _maxdd_r(vals: list[tuple[int, str, float]]) -> float:
    """Peak-to-trough of EXIT-ORDERED cumulative net R, seeded at 0 — the only
    implementation in the estate (`scripts/v3_scorer.py:98-103`), reused
    exactly, tie-broken on a stable secondary key.  Positive magnitude."""
    seq = sorted(vals, key=lambda t: (t[0], t[1]))
    cum = peak = dd = 0.0
    for _, _, r in seq:
        cum += r
        peak = max(peak, cum)
        dd = max(dd, peak - cum)
    return dd


def _top_decile_share(rs: list[float]) -> float | None:
    """Tail concentration: the top decile's share of the WINNING mass.

    Named, because the estate has four incompatible tail metrics and quoting
    one without naming it is how they get crossed (`census` comparability (d)).
    This is the `s2b_decompose.py:158-169` shape generalised from top-10 to a
    true decile, with the `wf1_forensics.py:64-70` k = floor(0.10 n) rule.
    """
    if not rs:
        return None
    wins = sum(v for v in rs if v > 0)
    if wins <= 0:
        return None
    k = int(np.floor(0.10 * len(rs)))
    if k < 1:
        return None
    top = sum(sorted(rs, reverse=True)[:k])
    return r4(100.0 * top / wins)


def headline_rows(trades: list, group: str) -> pd.DataFrame:
    """net R · expectancy/trade · win rate · maxDD(R) · tail concentration."""
    def agg(label, ts):
        if not ts:
            return {"group": group, "key": label, "n": 0, "net_r": None,
                    "expectancy_r": None, "win_rate_pct": None,
                    "max_dd_r": None, "top_decile_share_pct": None,
                    "gross_r": None, "fee_r": None, "funding_r": None,
                    "best_r": None, "strip_best_net_r": None,
                    "net_r_bellonly": None}
        rs = [t.net_r for t in ts]
        best = max(rs)
        return {
            "group": group, "key": label, "n": len(ts),
            "net_r": r4(sum(rs)),
            "expectancy_r": r4(float(np.mean(rs))),
            "win_rate_pct": pct(sum(1 for v in rs if v > 0), len(rs)),
            "max_dd_r": r4(_maxdd_r([(t.exit_ms, t.symbol, t.net_r) for t in ts])),
            "top_decile_share_pct": _top_decile_share(rs),
            "gross_r": r4(sum(t.gross_r for t in ts)),
            "fee_r": r4(sum(t.fee_r for t in ts)),
            "funding_r": r4(sum(t.funding_r for t in ts)),
            "best_r": r4(best),
            "strip_best_net_r": r4(sum(rs) - best),
            "net_r_bellonly": r4(sum(t.net_r_bellonly for t in ts)),
        }

    rows = []
    if group == "ALL":
        rows.append(agg("ALL", trades))
    elif group == "asset":
        for s in RC.UNIVERSE:
            rows.append(agg(s, [t for t in trades if t.symbol == s]))
    elif group == "direction":
        for d, n in ((1, "long"), (-1, "short")):
            rows.append(agg(n, [t for t in trades if t.direction == d]))
    elif group == "exit_reason":
        for r in ("stop", "bell_12_89", "bell_89_316", "corridor_end"):
            rows.append(agg(r, [t for t in trades if t.exit_reason == r]))
    return pd.DataFrame(rows)


def monthly_equity(trades: list) -> pd.DataFrame:
    """Monthly equity series in R, exit-stamped (a trade lands in the month it
    RESOLVES; an open trade contributes nothing until it does)."""
    if not trades:
        return pd.DataFrame(columns=["month", "n", "net_r", "cum_net_r"])
    d = pd.DataFrame([{"month": iso(t.exit_ms)[:7], "net_r": t.net_r}
                      for t in trades])
    g = d.groupby("month", as_index=False).agg(n=("net_r", "size"),
                                               net_r=("net_r", "sum"))
    g = g.sort_values("month").reset_index(drop=True)
    g["cum_net_r"] = g["net_r"].cumsum()
    return g


def stop_geometry(trades: list) -> pd.DataFrame:
    """R measured in ATR, and the toll measured in R — the two numbers that
    explain the headline.

    The rule card sets R from a 1H swing pivot but enters on a 4h bar, so R
    and the 4h bar's own noise are unrelated quantities.  When R/ATR is small
    the trade is stopped by ordinary bar noise AND the fixed 10 bps toll
    becomes a large fraction of R.  Both effects are printed per trade rather
    than asserted, because the architecture of record carries a rail against
    exactly this (`min_stop_atr = 0.5`, configs/tc1_B.yaml:53, engine G-8c)
    and THE RULE CARD AS RATIFIED NAMES NO SUCH RAIL.
    """
    rows = []
    for t in trades:
        rows.append({
            "asset": t.symbol, "entry_ms": t.entry_ms,
            "entry_ts": iso(t.entry_ms),
            "direction": "long" if t.direction == 1 else "short",
            "r_dist": r6(t.r_dist), "atr_at_entry": r6(t.atr_at_entry),
            "r_over_atr": r6(t.r_dist / t.atr_at_entry
                             if t.atr_at_entry else None),
            "under_g8c_rail": bool(t.atr_at_entry
                                   and t.r_dist < 0.5 * t.atr_at_entry),
            "toll_share_of_r_pct": r4(100.0 * t.fee_r),
            "bars_held": t.bars_held, "exit_reason": t.exit_reason,
            "net_r": r6(t.net_r), "net_r_bellonly": r6(t.net_r_bellonly),
            "stop_cost_r": r6(t.net_r_bellonly - t.net_r),
        })
    return pd.DataFrame(rows)


def journal_frame(trades: list) -> pd.DataFrame:
    rows = []
    for t in trades:
        rows.append({
            "asset": t.symbol, "entry_ms": t.entry_ms,
            "entry_ts": iso(t.entry_ms),
            "direction": "long" if t.direction == 1 else "short",
            "arm_ms": t.arm_ms, "arm_ts": iso(t.arm_ms),
            "disp_at_arming": r6(t.disp_at_arming),
            "entry_px": r6(t.entry_px), "stop_px": r6(t.stop_px),
            "pivot_anchor": r6(t.pivot_anchor), "r_dist": r6(t.r_dist),
            "atr_at_entry": r6(t.atr_at_entry),
            "exit_ms": t.exit_ms, "exit_ts": iso(t.exit_ms),
            "exit_px": r6(t.exit_px), "exit_reason": t.exit_reason,
            "bars_held": t.bars_held,
            "gross_r": r6(t.gross_r), "fee_r": r6(t.fee_r),
            "funding_r": r6(t.funding_r), "net_r": r6(t.net_r),
            "net_r_bellonly": r6(t.net_r_bellonly),
            "exit_reason_bellonly": t.exit_reason_bellonly,
            # ── Amendment B1 · RECORDED ONLY.  Nothing reads these back. ──
            "wall_family_at_arming": None, "dist_atr_at_arming": None,
            "dist_atr_at_trigger": None, "coloc_n": None,
        })
    return pd.DataFrame(rows)


# ═════════════════════════════════════════ A-TAPE (Amendment B1) · analytics
# CAPTURED, NOT CONSULTED.  Everything below runs AFTER the replay has already
# decided everything.  No value computed here is ever handed back to
# `tierc2_rules`; F-C2-6 proves that by import closure, not by inspection.
#
# The six ribbons, verbatim from `scripts/census2b_program.py:76-84`.
RIBBONS = {"FAST": (9, 12, 26), "M": (62, 89, 127), "MH": (262, 316, 423),
           "H": (616, 889, 1272), "VH": (1618, 2618, 3618),
           "UH": (4236, 4618, 5000)}
WALL_ATR = 0.5          # census2b_wtb1.py:106 — the 0.5-ATR contact test
COLOCATION_ATR = 0.15   # census2a_program.py:2531 — pinned, register row 13
RVWAP_WINDOWS = (7, 30, 90, 365)        # brief2.py:50 / mc1_program.py:712
TAPE_SIGMAS = (1, 2)                    # Amendment B1 asks +-1s AND +-2s

TAPE_FAMILIES = ("avwap", "rvwap", "prior_extreme")


def _daily_atr_map(k1: pd.DataFrame, target_ms: np.ndarray) -> np.ndarray:
    """Daily ATR at each target instant, from the LAST CLOSED daily bar.

    1h -> 1d through `analytics.structure.resample_ohlcv`, which drops the
    forming bucket unconditionally (AMENDMENT FAN8) — so the value at a 4h
    instant is a completed day's ATR and never a fraction of today.
    """
    d = AS.resample_ohlcv(k1["open_time"].to_numpy(np.int64),
                          k1["open"].to_numpy(float), k1["high"].to_numpy(float),
                          k1["low"].to_numpy(float), k1["close"].to_numpy(float),
                          k1["volume"].to_numpy(float), MS_1D)
    dt = d["open_time"]
    da = AV.atr(d["high"], d["low"], d["close"], RC.ATR_LEN)
    # last daily bar whose CLOSE (open + 1d) is at or before the instant
    k = np.searchsorted(dt + MS_1D, target_ms, "right") - 1
    out = np.full(len(target_ms), np.nan)
    ok = k >= 0
    out[ok] = da[k[ok]]
    return out


def _ribbon_bands(c: np.ndarray) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """Each ribbon's SR band = [min, max] of its three EMAs, on the 4h close.
    `analytics.momentum.ema` (SMA-seeded, NaN before warm-up) — the registry
    side deliberately uses the analytics recipe, not the engine's Pine-parity
    one, because this is measurement, not a trading decision."""
    from analytics.momentum import ema
    out = {}
    for fam, lens in RIBBONS.items():
        e = np.vstack([ema(c, L) for L in lens])
        out[fam] = (np.nanmin(e, axis=0), np.nanmax(e, axis=0))
    return out


def _single_wall(bands: dict, close: np.ndarray, atr_d: np.ndarray, i: int):
    """(family, signed distance in daily ATR) of THE SINGLE wall at bar i.

    Transcribed from `census2b_wtb1.py:220-245`.  "Single" is the point: the
    stamp is the IDENTITY of the one SR price is leaning on, and it is only an
    identity when exactly one qualifies.  Returns "n/a" on a bad ATR, "none"
    on zero hits, "multi" on more than one.
    """
    a = atr_d[i]
    if not (np.isfinite(a) and a > 0):
        return "n/a", None
    hits = []
    for fam, (lo, hi) in bands.items():
        l, u = lo[i], hi[i]
        if not (np.isfinite(l) and np.isfinite(u)):
            continue
        c = close[i]
        d = 0.0 if l <= c <= u else min(abs(c - u), abs(c - l))
        if d <= WALL_ATR * a:
            # sign: + means price is ABOVE the band (support), - below
            sgn = 0.0 if l <= c <= u else (1.0 if c > u else -1.0)
            hits.append((fam, sgn * d / a))
    if not hits:
        return "none", None
    if len(hits) > 1:
        return "multi", min(hits, key=lambda h: abs(h[1]))[1]
    return hits[0][0], hits[0][1]


def build_level_series(k4: pd.DataFrame) -> dict[str, dict[str, np.ndarray]]:
    """Every level family, as CAUSAL full-length series on the 4h lens.

    ENDPOINT-ONLY, HONOURED.  `analytics/INTERFACE.md:42` defines endpoint_only
    as "valid only at the end of the supplied array".  Every function used here
    is CAUSAL (F-AN-13 asserts it), so series[k] is identically the value a
    caller would get by slicing to k and reading [-1].  That identity is not
    assumed: F-C2-7 re-derives sampled instants by ACTUAL endpoint slicing and
    asserts exact equality, and the sabotage lever proves a future bar is
    rejected on this corridor.
    """
    ot = k4["open_time"].to_numpy(np.int64)
    hi, lo = k4["high"].to_numpy(float), k4["low"].to_numpy(float)
    cl, vol = k4["close"].to_numpy(float), k4["volume"].to_numpy(float)
    src = (hi + lo + cl) / 3.0                       # hlc3, the estate's source
    out: dict[str, dict[str, np.ndarray]] = {"avwap": {}, "rvwap": {},
                                             "prior_extreme": {}}

    # AVWAP set — week / month / year anchors (mc1_program.py:806-816 shape)
    ts = pd.to_datetime(ot, unit="ms", utc=True)
    for tag, mask in (("week", ts.dayofweek == 0),
                      ("month", ts.day == 1),
                      ("year", (ts.day == 1) & (ts.month == 1))):
        w = np.flatnonzero(np.asarray(mask))
        if w.size == 0:
            continue
        # the anchor in force AT EACH BAR is the most recent anchor at or
        # before it — a step function, so the series stays causal.
        series = np.full(len(cl), np.nan)
        for a0, a1 in zip(w, list(w[1:]) + [len(cl)]):
            v = AW.anchored_vwap(src[:a1], vol[:a1], int(a0))["vwap"]
            series[a0:a1] = v[a0:a1]
        out["avwap"][f"avwap_{tag}"] = series

    # RVWAP +-1s / +-2s
    for wd in RVWAP_WINDOWS:
        r = AW.rolling_vwap(ot, src, vol, window_days=wd, sigmas=TAPE_SIGMAS)
        out["rvwap"][f"rvwap_{wd}d"] = r["vwap"]
        for s in TAPE_SIGMAS:
            out["rvwap"][f"rvwap_{wd}d_up{s}"] = r[f"band_up_{s}"]
            out["rvwap"][f"rvwap_{wd}d_dn{s}"] = r[f"band_dn_{s}"]

    # prior-day / week / month extremes
    for per, tag in (("D", "day"), ("W", "week"), ("M", "month")):
        ph, pl = AS.prior_period_extremes(ot, hi, lo, period=per)
        out["prior_extreme"][f"prior_{tag}_high"] = ph
        out["prior_extreme"][f"prior_{tag}_low"] = pl
    return out


def tape_rows(sym: str, k4: pd.DataFrame, k1: pd.DataFrame,
              instants: list[tuple[int, str]], win_name: str) -> pd.DataFrame:
    """One row per instant: nearest level per family, SIGNED distance in ATR,
    single-wall identity, co-location count, and the six-ribbon state.

    A signed distance is BUILT here, not reused: the estate's two existing
    as-of distances (`mc1_program.py:983`, `census2a_program.py:2615`) are both
    `abs()`.  Sign convention: POSITIVE = price is ABOVE the level.
    """
    ot = k4["open_time"].to_numpy(np.int64)
    cl = k4["close"].to_numpy(float)
    atr4 = RC.build_4h(ot, k4["open"].to_numpy(float), k4["high"].to_numpy(float),
                       k4["low"].to_numpy(float), cl).atr
    fams = build_level_series(k4)
    bands = _ribbon_bands(cl)

    idx = {int(t): i for i, t in enumerate(ot)}
    want = [(t, kind) for t, kind in instants if int(t) in idx]
    tms = np.array([t for t, _ in want], dtype=np.int64)
    if tms.size == 0:
        return pd.DataFrame()
    atr_d = _daily_atr_map(k1, tms)

    all_levels = [v for f in fams.values() for v in f.values()]
    rows = []
    for n, (t, kind) in enumerate(want):
        i = idx[int(t)]
        c, a4, ad = cl[i], atr4[i], atr_d[n]
        row = {"asset": sym, "ts": int(t), "ts_iso": iso(t), "instant": kind,
               "window": win_name, "close": r6(c),
               "atr_4h": r6(a4), "atr_1d": r6(ad)}
        for fam in TAPE_FAMILIES:
            best_name, best_sd = None, None
            for name, series in fams[fam].items():
                v = series[i]
                if not np.isfinite(v) or not (np.isfinite(a4) and a4 > 0):
                    continue
                sd = (c - v) / a4
                if best_sd is None or abs(sd) < abs(best_sd):
                    best_name, best_sd = name, sd
            row[f"{fam}_nearest"] = best_name
            row[f"{fam}_dist_atr"] = r6(best_sd)
        # the nearest level ACROSS the three families — this is what the
        # journal's `dist_atr_*` columns record.  Chosen over the wall
        # distance because `dist_atr_at_trigger` has no wall companion in the
        # amendment's column list, so the general reading is the only one that
        # makes both columns mean the same thing.
        cands = [(row[f"{f_}_nearest"], row[f"{f_}_dist_atr"])
                 for f_ in TAPE_FAMILIES if row.get(f"{f_}_dist_atr") is not None]
        if cands:
            nm, sd = min(cands, key=lambda p: abs(p[1]))
            row["nearest_level"], row["nearest_dist_atr"] = nm, sd
        else:
            row["nearest_level"], row["nearest_dist_atr"] = None, None
        # the wall test is evaluated at THIS instant only, so the daily-ATR
        # vector it is handed is this instant's value broadcast — the function
        # reads index `i` and nothing else.
        wf, wd = _single_wall(bands, cl, np.full(len(cl), ad), i)
        row["wall_family"] = wf
        row["wall_dist_atr"] = r6(wd)
        row["coloc_n"] = (int(sum(
            1 for s in all_levels
            if np.isfinite(s[i]) and np.isfinite(ad) and ad > 0
            and abs(c - s[i]) <= COLOCATION_ATR * ad))
            if np.isfinite(ad) else None)
        row["n_levels"] = int(sum(1 for s in all_levels if np.isfinite(s[i])))
        rows.append(row)
    return pd.DataFrame(rows)


def ribbon_state(sym: str) -> pd.DataFrame:
    """The six-ribbon state columns ALREADY LOCAL — joined by ts, never
    recomputed.  `research_outputs/census2b/oracle/state_v2/<asset>/4h.parquet`
    (ORACLE stage R-3, filed 2026-08-15)."""
    p = (ROOT / "research_outputs" / "census2b" / "oracle" / "state_v2"
         / sym / "4h.parquet")
    if not p.exists():
        return pd.DataFrame()
    d = pd.read_parquet(p).rename(columns={"open_time": "ts"})
    return d


def tape_inventory(tape: pd.DataFrame) -> pd.DataFrame:
    """instants x families x nulls.  AN INVENTORY, NOT AN ANALYSIS.

    The build document prints this table and nothing derived from it.  Q6c is
    why: the stillbirth counterfactual requires that location evidence be
    gathered on an UNCONDITIONED population, so the moment this tape is cut,
    ranked or conditioned on, the population it describes stops being the one
    the baseline traded.  Counting nulls is inventory; comparing a null rate
    between winners and losers is a probe, and would need its own m declared
    BEFORE the look.
    """
    cols = ([f"{f}_nearest" for f in TAPE_FAMILIES]
            + [f"{f}_dist_atr" for f in TAPE_FAMILIES]
            + ["nearest_level", "nearest_dist_atr", "wall_family",
               "wall_dist_atr", "coloc_n", "atr_1d"]
            + [c for c in tape.columns if c.endswith("_state_v2")])
    rows = []
    for inst, g in tape.groupby("instant"):
        for c in cols:
            if c not in tape.columns:
                continue
            nn = int(g[c].isna().sum())
            extra = ""
            if c == "wall_family":
                vc = g[c].value_counts().to_dict()
                extra = ", ".join(f"{k}={v}" for k, v in sorted(vc.items()))
            rows.append({"instant": inst, "column": c, "n": len(g),
                         "nulls": nn, "null_pct": pct(nn, len(g)),
                         "note": extra})
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════ the driver
def daily_spine(k4: pd.DataFrame, lo_ms: int, hi_ms: int) -> list[int]:
    """A 00:00Z bar per day across the window — the tape's regular heartbeat,
    so the record is not only the instants the rule card happened to like."""
    ot = k4["open_time"].to_numpy(np.int64)
    m = (ot >= lo_ms) & (ot <= hi_ms) & (ot % MS_1D == 0)
    return [int(t) for t in ot[m]]


def run(root: Path, do_tape: bool = True) -> dict:
    t0 = time.time()
    man: dict = {"seed": SEED, "windows": {}, "sha": {}, "counts": {}}

    log("=" * 78)
    log("TIER-C2 · THE FORWARD BASELINE — the number every multiplier must beat")
    log("=" * 78)
    log(f"  analytics {AN.ANALYTICS_VERSION}  sha {AN.analytics_sha()[:16]}…")
    log(f"  seed {SEED} · universe {', '.join(RC.UNIVERSE)} · lens {RC.LENS}")
    log(f"  klines {KLINES}")
    log("")
    log("  WINDOWS")
    for n, w in WINDOWS.items():
        log(f"    {n:12} {w['span'][0]} -> {w['span'][1]}   "
            f"{'SCORED' if w['scored'] else 'DISPLAY-ONLY'}  ({w['note']})")
    lo = AN.lockbox_overlap(_ms(LOCKBOX[0]), _ms(LOCKBOX[1]) + MS_1D - 1)
    log(f"    {'LOCKBOX':12} {LOCKBOX[0]} -> {LOCKBOX[1]}   NOT COMPUTED  "
        f"(sealed; overlap disclosure {lo['overlap_days']:.3f} d)")
    log("")

    all_arms: dict[str, list] = {}
    all_trades: dict[str, list] = {}
    tape_frames: list[pd.DataFrame] = []

    for win_name in WINDOWS:
        span = WINDOWS[win_name]["span"]
        lo_ms, hi_ms = _ms(span[0]), _ms(span[1]) + MS_1D - 1
        log(f"  ── {win_name} {span[0]} -> {span[1]} "
            f"{'(SCORED)' if WINDOWS[win_name]['scored'] else '(DISPLAY-ONLY)'}")
        arms_w, trades_w = [], []
        for sym in RC.UNIVERSE:
            k4, k1 = load_klines(sym, "4h"), load_klines(sym, "1h")
            fund = load_funding(sym)
            a, t = replay_asset(sym, win_name, k4, k1, fund)
            arms_w += a
            trades_w += t
            log(f"    {sym:9} armings={len(a):5d}  trades={len(t):4d}")

            if do_tape and WINDOWS[win_name]["scored"]:
                inst: list[tuple[int, str]] = []
                for x in a:
                    inst.append((x.arm_ms, "arming"))
                    if x.trigger_ms is not None:
                        inst.append((x.trigger_ms, "trigger"))
                for tr in t:
                    inst.append((tr.exit_ms, "exit"))
                for d in daily_spine(k4, lo_ms, hi_ms):
                    inst.append((d, "spine"))
                # one row per (asset, ts): an instant that is both an arming
                # and a spine bar collapses, arming winning — F-KEY depends on it
                order = {"arming": 0, "trigger": 1, "exit": 2, "spine": 3}
                seen: dict[int, str] = {}
                for ts, kind in sorted(inst, key=lambda p: (p[0], order[p[1]])):
                    seen.setdefault(int(ts), kind)
                tp = tape_rows(sym, k4, k1, sorted(seen.items()), win_name)
                if len(tp):
                    rs = ribbon_state(sym)
                    if len(rs):
                        assert_key(rs, ["ts"], f"ribbon_state[{sym}]")
                        tp = tp.merge(rs, on="ts", how="left", validate="1:1")
                    tape_frames.append(tp)
        all_arms[win_name] = arms_w
        all_trades[win_name] = trades_w
        man["windows"][win_name] = {
            "span": list(span), "scored": WINDOWS[win_name]["scored"],
            "armings": len(arms_w), "trades": len(trades_w)}
        log("")

    # ── tables ────────────────────────────────────────────────────────────
    log("  ── TABLES")
    scored_arms, scored_trades = all_arms["SCORED"], all_trades["SCORED"]

    fn = funnel_table(scored_arms)
    man["sha"]["funnel"] = write_table(fn, "funnel", ["asset", "direction"], root)
    man["sha"]["strip_d"] = write_table(strip_d_table(scored_arms), "strip_d_unscored",
                                        ["d"], root)

    head = pd.concat([headline_rows(scored_trades, g)
                      for g in ("ALL", "asset", "direction", "exit_reason")],
                     ignore_index=True)
    man["sha"]["headline"] = write_table(head, "headline", ["group", "key"], root)
    man["sha"]["monthly"] = write_table(monthly_equity(scored_trades),
                                        "monthly_equity", ["month"], root)
    sg = stop_geometry(scored_trades)
    man["sha"]["stop_geometry"] = write_table(
        sg, "stop_geometry", ["asset", "entry_ms"] if len(sg) else [], root)

    jr = journal_frame(scored_trades)
    if len(jr):
        # Amendment B1: the four RECORDED-ONLY columns, filled from the tape
        # by ts join.  Written after the decision, read by nothing.
        tp = pd.concat(tape_frames, ignore_index=True) if tape_frames else pd.DataFrame()
        if len(tp):
            am = tp.set_index(["asset", "ts"])
            for i, row in jr.iterrows():
                ka, kt = (row["asset"], row["arm_ms"]), (row["asset"], row["entry_ms"])
                if ka in am.index:
                    jr.at[i, "wall_family_at_arming"] = am.loc[ka, "wall_family"]
                    jr.at[i, "dist_atr_at_arming"] = am.loc[ka, "nearest_dist_atr"]
                    jr.at[i, "coloc_n"] = am.loc[ka, "coloc_n"]
                if kt in am.index:
                    jr.at[i, "dist_atr_at_trigger"] = am.loc[kt, "nearest_dist_atr"]
    man["sha"]["journal"] = write_table(jr, "trade_journal",
                                        ["asset", "entry_ms"] if len(jr) else [], root)

    # display-only strips — outcomes, clearly headed, never scored
    ds = []
    for win_name in ("CENSUS_ERA", "PINNING"):
        h = headline_rows(all_trades[win_name], "ALL")
        h["window"] = win_name
        h["class"] = DISPLAY_ONLY_HEADER
        ds.append(h)
    man["sha"]["display_only"] = write_table(pd.concat(ds, ignore_index=True),
                                             "display_only_strips",
                                             ["window", "group", "key"], root)

    if tape_frames:
        tape = pd.concat(tape_frames, ignore_index=True)
        man["sha"]["tape"] = write_table(tape, "analytics_tape",
                                         ["asset", "ts"], root)
        man["counts"]["tape_rows"] = len(tape)
        man["counts"]["tape_instants"] = tape["instant"].value_counts().to_dict()
        man["sha"]["tape_inventory"] = write_table(
            tape_inventory(tape), "tape_inventory", ["instant", "column"], root)

    man["counts"]["scored_trades"] = len(scored_trades)
    man["counts"]["scored_armings"] = len(scored_arms)
    man["elapsed_s"] = round(time.time() - t0, 1)

    root.mkdir(parents=True, exist_ok=True)
    (root / "build_manifest.json").write_text(
        json.dumps(man, indent=2, sort_keys=True, default=str))
    log(f"\n  manifest → {root / 'build_manifest.json'}   ({man['elapsed_s']}s)")
    return man


# ═════════════════════════════════════════════════ STAGE B · the heartbeat
PAPER_PROFILE = ROOT / "configs" / "tierc2_paper.yaml"
LIVE_FROM = "2026-02-01"        # the live tail; a warm start well past warm-up


def load_profile() -> dict:
    """Read the paper profile AND assert every value against the register.

    A config that can drift from the code it configures is a second source of
    truth.  This one cannot: it is checked on every load, and a mismatch HALTs.
    """
    import yaml
    p = yaml.safe_load(PAPER_PROFILE.read_text())
    s, t = p["signal"], p["trading"]
    checks = [
        ("universe", tuple(p["universe"]), RC.UNIVERSE),
        ("lens", p["lens"], RC.LENS),
        ("tide_fast", s["tide_fast"], RC.TIDE_FAST),
        ("tide_slow", s["tide_slow"], RC.TIDE_SLOW),
        ("window_fast", s["window_fast"], RC.WINDOW_FAST),
        ("window_slow", s["window_slow"], RC.WINDOW_SLOW),
        ("trigger_fast", s["trigger_fast"], RC.TRIGGER_FAST),
        ("trigger_slow", s["trigger_slow"], RC.TRIGGER_SLOW),
        ("d_displacement", s["d_displacement"], RC.D_DISPLACEMENT),
        ("d_strip", tuple(s["d_strip"]), RC.D_STRIP),
        ("atr_len", s["atr_len"], RC.ATR_LEN),
        ("pivot_l", s["pivot_l"], RC.PIVOT_L),
        ("pivot_r", s["pivot_r"], RC.PIVOT_R),
        ("pivot_lookback_1h", s["pivot_lookback_1h"], RC.PIVOT_LOOKBACK_1H),
        ("stop_buf_atr", s["stop_buf_atr"], RC.STOP_BUF_ATR),
        ("fee_bps_side", t["fee_bps_side"], RC.FEE_BPS_SIDE),
    ]
    bad = [(n, a, b) for n, a, b in checks if a != b]
    if bad:
        raise SystemExit(f"HALT: configs/tierc2_paper.yaml disagrees with "
                         f"tierc2_rules.REGISTER on {bad}")
    if t["enabled"]:
        raise SystemExit("HALT: trading.enabled must be false — this profile "
                         "is PAPER and may never place a live order.")
    log(f"    profile {PAPER_PROFILE.name}: {len(checks)} values, all agree with "
        f"the register; trading.enabled={t['enabled']}")
    return p


def heartbeat() -> dict:
    """One heartbeat: the rule card's live state, positions none/open printed.

    DISPLAY-ONLY, live era.  This is an OPS artifact and never study evidence:
    it reads bars past the v12 Study's right edge (VR-1 puts everything after
    2026-07-07 in "Naiad's domain; the v12 Study never reads it"), which is
    exactly where a forward paper line is supposed to live.

    The com.naiad.daily 07:00 agent is NOT modified — the profile records that
    plainly (`agent_modified: false`), and wiring this into
    `scripts/routine_jobs.json` is a separate operator-authorised act.
    """
    log("=" * 78)
    log("TIER-C2 · STAGE B — LIVE PAPER ARMED · one heartbeat")
    log("=" * 78)
    p = load_profile()
    log(f"    {p['heartbeat']['class_header']}")
    log("")

    now_ms = int(time.time() * 1000)
    rows, open_pos, armed = [], [], []
    for sym in RC.UNIVERSE:
        k4, k1 = load_klines(sym, "4h"), load_klines(sym, "1h")
        # PROVABLY CLOSED only: the newest cached bar may still be forming, so
        # it is dropped unconditionally — the same law as
        # analytics.structure._provably_closed_count.
        ot_all = k4["open_time"].to_numpy(np.int64)
        closed = ot_all[ot_all + MS_4H <= now_ms]
        if not len(closed):
            continue
        last_ms = int(closed[-1])
        k4 = k4[k4["open_time"] <= last_ms].reset_index(drop=True)

        hb_win = {"span": (LIVE_FROM, iso(last_ms)[:10]), "scored": False,
                  "note": "live paper"}
        WINDOWS["_HB"] = hb_win
        try:
            arms, trades = replay_asset(sym, "_HB", k4, k1, load_funding(sym))
        finally:
            WINDOWS.pop("_HB", None)

        f = RC.build_4h(k4["open_time"].to_numpy(np.int64),
                        k4["open"].to_numpy(float), k4["high"].to_numpy(float),
                        k4["low"].to_numpy(float), k4["close"].to_numpy(float))
        last_i = len(f.c) - 1
        px = float(f.c[last_i])

        # an OPEN position = a trade whose ride was truncated at the live edge
        live = [t for t in trades if t.exit_reason == "corridor_end"
                and t.exit_i == last_i]
        for t in live:
            unreal = (px - t.entry_px) * t.direction / t.r_dist
            open_pos.append({
                "asset": sym, "direction": "long" if t.direction == 1 else "short",
                "entry_ts": iso(t.entry_ms), "entry_px": r6(t.entry_px),
                "stop_px": r6(t.stop_px), "r_dist": r6(t.r_dist),
                "bars_held": t.bars_held, "mark_px": r6(px),
                "unrealised_r": r4(unreal)})

        # an ARMED window = tide+d passed, window still open, no trigger yet
        for a in arms:
            if a.reject == "no_trigger" and a.window_end_i > last_i:
                armed.append({
                    "asset": sym,
                    "direction": "long" if a.direction == 1 else "short",
                    "armed_ts": iso(a.arm_ms), "disp_at_arming": r6(a.disp),
                    "awaiting": f"first 4h 12/{RC.TRIGGER_SLOW} cross"})

        rows.append({"asset": sym, "last_closed_4h": iso(last_ms),
                     "close": r6(px), "trades_since_" + LIVE_FROM: len(trades)})

    log("  BAR STATE — last provably-closed 4h bar per asset")
    for r in rows:
        log(f"    {r['asset']:9} {r['last_closed_4h']}  close={r['close']}")
    log("")
    log(f"  POSITIONS: {'NONE' if not open_pos else str(len(open_pos)) + ' OPEN'}")
    for o in open_pos:
        log(f"    OPEN  {o['asset']:9} {o['direction']:5} entry {o['entry_ts']} "
            f"@ {o['entry_px']}  stop {o['stop_px']}  held {o['bars_held']} bars  "
            f"mark {o['mark_px']}  unrealised {o['unrealised_r']:+.4f} R")
    log("")
    log(f"  ARMED WINDOWS AWAITING TRIGGER: "
        f"{'NONE' if not armed else str(len(armed))}")
    for a in armed:
        log(f"    ARMED {a['asset']:9} {a['direction']:5} since {a['armed_ts']}  "
            f"d={a['disp_at_arming']}  awaiting {a['awaiting']}")

    state = {"run_ts": iso(now_ms), "class": p["heartbeat"]["class_header"],
             "profile": p["config_id"], "executor": p["executor"],
             "agent": p["heartbeat"]["agent"],
             "agent_modified": p["heartbeat"]["agent_modified"],
             "registered_in_routine_jobs": p["heartbeat"]["registered_in_routine_jobs"],
             "live_from": LIVE_FROM, "bars": rows,
             "positions": open_pos, "armed": armed}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "heartbeat.json").write_text(json.dumps(state, indent=2, sort_keys=True))
    log("")
    log(f"  state → {OUT / 'heartbeat.json'}")
    log(f"  agent {p['heartbeat']['agent']} UNTOUCHED "
        f"(agent_modified={p['heartbeat']['agent_modified']}, "
        f"registered_in_routine_jobs="
        f"{p['heartbeat']['registered_in_routine_jobs']})")
    return state


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all",
                    choices=["all", "replay", "tape", "heartbeat"])
    ap.add_argument("--rerun", action="store_true",
                    help="write to research_outputs/tierc2_run2 (F-C2-4)")
    a = ap.parse_args()
    if a.stage == "heartbeat":
        heartbeat()
        return 0
    root = OUT_RERUN if a.rerun else OUT
    run(root, do_tape=(a.stage in ("all", "tape")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
