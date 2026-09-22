#!/usr/bin/env python
"""TIER-C10 · STAGE 0b — CENSUS-R, THE RANGE CENSUS ENGINE.

RATIFIED operator 2026-09-21 (contract TIER-C10, Q7 = CENSUS-R as Stage 0).
Drafted APOLLO, executed HEPHAESTUS; seed 20260921.  TIER-E: a MEASUREMENT,
collared, report-only.  It files no registration, takes no slot in m = 6,
runs no card, no trigger, no floor, no lane — it imports none of them.  What
it measures is the RangeFinder's lifecycle on a tape: how much of the tape a
confirmed macro range covers, how often one confirms, how long it lives, and
what price did AFTER each class of range event, net of the toll measured on
that class's own anchors.

WHAT IT DOES, IN ORDER, PER (asset, lens) CELL
  1. LOADS the tape from the FROZEN snapshot, full history, closed bars at or
     before the Stage D AS_OF pin.  1d is DERIVED here from native 4h [L1] and
     held equal to Stage D's own derived file.  ATR = engine.indicators.atr on
     the WHOLE tape, computed HERE and handed to the port (the port computes
     none — analytics I-D).  The tape is never chunked: a chunk re-warms.
  2. RUNS the macro machine + the leash through the port
     (analytics/rangefinder_census.py) at the FROZEN SCALE 3.0 and at the
     self-calibrated SCALE [L2], whole calibrator grid filed.
  3. BUILDS THE AS-OF LAYER: known_at for every event (a pivot at its SEAL, a
     flip at its touch bar + FLIP_HOLD_BARS, never at its own stamp) and the
     per-bar arrays a Stage-A stamp reads — macro state, as-of top / bottom
     (the pre-redraw value until the redraw is known), %-of-range, distance to
     the nearest boundary in ATR, boundary age, deviations per side, last
     flip.  Nothing in it reads Range.top / .bottom / .n_deviations (end-of-run
     values) or a range's back-dated left edge.
  4. EXTRACTS the six contract classes {breach, harden, DIE, memory-touch,
     flip-hold, retest-hold on EMA-band} — memory-touch under BOTH rival
     definitions; retest-hold from a PARAMETERISED detector whose pins are NOT
     RULED (the only hold pins on disk ride as the printed default and every
     such row says PROVISIONAL-PINS).
  5. MEASURES the outcome of every event at H20 / H100 BARS OF THE LENS from
     the close of the bar the event is KNOWN [L4]: censored, never shortened.
     toll_atr = median((bps / 10 000) * close / atr) over THAT row's anchors,
     bps read from the estate fee object; NET = median - toll_atr.
  6. FILES per-cell artifacts with their shas (a run resumes cell by cell) and
     merges them into the grid F-C10-TOLL reads: census/outcome_grid.parquet.

WHAT WOULD MAKE THIS WRONG: anchoring an outcome at an event's STAMP bar
instead of its known_at bar (a flip leaks six bars); reading a boundary from
the Range object or from a 2-dp event price; shortening a horizon at the tape
end instead of censoring it; quoting one lens's toll beside another's returns,
or typing a toll; chunking the tape; letting a whole-tape-fitted SCALE stand
in for the frozen pin anywhere a registration or a Stage-A stamp can read it.

Run: NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921 \\
     ~/venvs/naiad/bin/python scripts/tierc10_census.py \\
         [--assets PANEL17|CLASSIC5|UNSEEN12|SYM,SYM] [--lenses 5m,4h,1d] \\
         [--scale-kind both|frozen3.0|calibrated] [--out DIR] [--force] \\
         [--merge-only] [--time-only [--tail-bars N]]
Exit: 0 complete · 1 HALT.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = Path.home() / ".cache" / "naiad" / "snapshots" / "tc10_20260921"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"


def assert_substrate() -> Path:
    """THE FROZEN-SUBSTRATE GUARD [HARD LAW 3], Stage D's, restated here so
    the census stays importable without the fetcher.  Runs BEFORE engine.data
    is imported.

    HALTS IF: NAIAD_CACHE_DIR is unset, is the live cache, or is anything but
    the TC10 snapshot.
    """
    env = os.environ.get("NAIAD_CACHE_DIR", "")
    if not env:
        raise SystemExit("HALT: NAIAD_CACHE_DIR is unset — TC10 reads ONLY the "
                         f"snapshot {SNAPSHOT}")
    got = Path(env).expanduser().resolve()
    if got == LIVE_CACHE.resolve():
        raise SystemExit("HALT: NAIAD_CACHE_DIR is the LIVE cache — READ-NEVER, "
                         "WRITE-NEVER for TC10")
    if got != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={got} is not the TC10 snapshot "
                         f"{SNAPSHOT}")
    if not (got / "klines").is_dir():
        raise SystemExit(f"HALT: snapshot has no klines/ directory: {got}")
    return got


assert_substrate()

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from analytics import rangefinder_census as RC                       # noqa: E402
from engine import indicators as ind                                 # noqa: E402
from engine.data import cache_dir                                    # noqa: E402
import tierc2_rules as R2                                            # noqa: E402

SEED = 20260921                 # threaded to every seeded consumer; the census
                                # itself draws nothing at random
OUT = ROOT / "research_outputs" / "tierc10" / "census"
STAGE_D = ROOT / "research_outputs" / "tierc10" / "data"
PORT_PATH = ROOT / "analytics" / "rangefinder_census.py"

MS_1H = 3_600_000
DAY_MS = 24 * MS_1H
LENSES = ("5m", "4h", "1d")
LENS_MS = {"5m": 300_000, "4h": 4 * MS_1H, "1d": DAY_MS}
LENS_SOURCE = {"5m": "5m", "4h": "4h", "1d": "4h"}     # 1d DERIVED from native 4h [L1]
BARS_PER_DAY_4H = DAY_MS // LENS_MS["4h"]                # six — derived, not typed
TS_FMT = {"5m": "%Y-%m-%dT%H:%M", "4h": "%Y-%m-%dT%H:%M", "1d": "%Y-%m-%d"}

HORIZONS = (("H20", 20), ("H100", 100))     # BARS OF THE LENS [L4]; precedent
                                            # tierc5.MIDBAND_H, never census-2A's
                                            # duration-fixed law (critic W2)
FROZEN_SCALE = RC.PINS_V2["SCALE_MULT"]     # 3.0, by object [L2]
SCALE_GRID = tuple(1.5 + 0.25 * k for k in range(11))   # 1.5..4.0 step 0.25 —
                                            # the Pine input's minval / step [L2]
DENSITY_TARGET_PER_100 = 0.75               # the contract's figure; == the twin's
                                            # TARGETS_Q["Q3_conf_per_100"][0]
                                            # (the fixture holds the two equal)
SCALE_KINDS = ("frozen3.0", "calibrated")
SPRING_LOOK = 20                            # F-RF-4's house look, rangefinder_fixtures.py
PROVISIONAL_MIN_N = 30                      # == tierc5_rules.PROVISIONAL_MIN_N (fixtured)
BPS_PER_UNIT = 10_000
ROUND_ND = 8                                # every filed float; ATR-unit ratios only —
                                            # NO raw price is ever filed (a 6-dp round
                                            # would erase a sub-cent symbol)

# ── the six contract classes · ELEVEN labels since OPERATOR RULING R1 ──────
# R1 (verbatim): "Let's try the 89/127 ribbon, the 127/200 ribbon, and taps on
# each ema. Feel free to search data from past runs to tune the defaults".  The
# five bands REPLACE the provisional pair (ema89 line, ema200_300); the hold
# pins are TUNED under the protocol fixed before the look (see THE R1 TUNING).
RETEST_RIBBONS = ((89, 127), (127, 200))    # R1's two ribbons, in the ruling's order
RETEST_TAPS = (89, 127, 200)                # R1's three taps
RETEST_CLASSES = (tuple(f"retest-hold-ribbon{a}_{b}" for a, b in RETEST_RIBBONS)
                  + tuple(f"retest-hold-tap{p}" for p in RETEST_TAPS))
CLASSES = ("breach", "harden", "DIE", "memory-touch-v1", "memory-touch-2s",
           "flip-hold") + RETEST_CLASSES
# R1's tie-break order: "the simpler band (tap before ribbon, 89 before 127
# before 200)" — the ORDER A TIE IS BROKEN IN, never the filing order.
BAND_TIE_BREAK = (tuple(f"tap{p}" for p in RETEST_TAPS)
                  + tuple(f"ribbon{a}_{b}" for a, b in RETEST_RIBBONS))
FROZEN_PINS = "FROZEN-PINS (STEP 0 sha)"
PROVISIONAL_PINS = "PROVISIONAL-PINS"
TUNED_PINS = "TUNED-PINS (R1 protocol, tuning era only)"

# ── THE ERA SPLIT [R1] ────────────────────────────────────────────────────
# "TUNING ERA = bars with close time <= 2024-06-30T23:59:59Z (the estate's
# 'exploration-classic' era, LEDGER.md:97). HOLDOUT ERA = bars after it."
# An event's era is its ANCHOR bar's close — never its stamp bar: a hold that
# completes after the boundary is a holdout-era fact.
ERA_BOUNDARY_ISO = "2024-06-30T23:59:59Z"
ERA_BOUNDARY_MS = int(datetime.strptime(ERA_BOUNDARY_ISO, "%Y-%m-%dT%H:%M:%SZ")
                      .replace(tzinfo=timezone.utc).timestamp() * 1000)
ERA_TUNING, ERA_HOLDOUT, ERA_ALL = "tuning", "holdout", "ALL"
ERAS = (ERA_ALL, ERA_TUNING, ERA_HOLDOUT)   # ALL = the full-history row [contract]
ERA_LAW = (f"era = the ANCHOR bar's close: 'tuning' <= {ERA_BOUNDARY_ISO}, 'holdout' "
           "after it (an anchor beyond the tape's end has no close and is holdout by "
           "construction — the tape ends in 2026). 'ALL' = the full-history row the "
           "contract orders, filed beside the two era rows, never their sum.")


def era_of(known_close_ms) -> np.ndarray:
    """The era of every anchor, from its CLOSE stamp [ERA_LAW]."""
    k = np.asarray(known_close_ms, dtype=np.int64)
    return np.where((k >= 0) & (k <= ERA_BOUNDARY_MS), ERA_TUNING, ERA_HOLDOUT)


# ── THE COLLAR ON P-BRK-S1's SCORING GROUND [LAW 4 + R1] ──────────────────
COLLAR_5M_RETEST = (
    "P-BRK-S1 IS SCORED ON THE 5m RETEST-HOLD CLASSES IN THE HOLDOUT ERA. Those rows "
    "are FILED in the parquet and are NOT printed, summarised or quoted in any digest, "
    "log line or report field: a registration's text is filed before its result is "
    "seen. Only the TUNING-era 5m retest-hold rows are printed. Every other class and "
    "lens prints full history, as the contract orders.")


def printable(lens: str, cls: str, era: str) -> bool:
    """False for exactly the rows LAW 4 + R1 collar: 5m retest-hold outside the
    tuning era (the holdout rows AND the full-history rows that contain them)."""
    return not (str(lens) == "5m" and str(cls).startswith("retest-hold")
                and str(era) != ERA_TUNING)


PINS_STATUS = {c: (TUNED_PINS if c.startswith("retest-hold") else FROZEN_PINS)
               for c in CLASSES}
SIGN_LAW = {
    "breach": "breach direction (top +1 / bottom -1): a negative median = the fade",
    "harden": "back-inside direction (top -1 / bottom +1)",
    "DIE": "die direction (top +1 / bottom -1)",
    "memory-touch-v1": "parent death direction; v1 ONE-SIDED first touch per side "
                       "(h >= top / l <= bottom) — near-trivial on the breakout side",
    "memory-touch-2s": "parent death direction; DERIVED first TWO-SIDED touch of the "
                       "leash line (l <= px <= h), verdict NOT read",
    "flip-hold": "flip polarity (support +1 / resistance -1)",
}
SIGN_LAW.update({c: "DIE direction" for c in RETEST_CLASSES})
ANCHOR_LAW = {
    "breach": "close of the breach-open bar (known at i)",
    "harden": "close of the harden bar (known at i)",
    "DIE": "close of the breakout-die bar (known at i)",
    "memory-touch-v1": "close of the touch bar (known at i)",
    "memory-touch-2s": "close of the touch bar (the TOUCH is known at i; its "
                       "verdict is not, and is not read)",
    "flip-hold": "close of bar touch_i + FLIP_HOLD_BARS — never the stamp bar",
}
ANCHOR_LAW.update({c: "close of bar touch_i + hold_bars (the hold-confirm bar)"
                   for c in RETEST_CLASSES})

RETEST_LAW = ("the flip-hold law with the band in place of the memory line: after a "
              "macro DIE, the FIRST bar whose [low, high] meets the band having CLOSED "
              "beyond it on the die side the bar before gets the ONE evaluation; HOLD = "
              "no close through the band's far edge by margin_atr x ATR[k] on any of the "
              "hold_bars + 1 bars from the touch; a window the tape truncates never "
              "confirms; the candidacy lapses ttl_bars after the DIE or at the next "
              "macro DIE; a band is unreadable (NaN) until its slowest EMA has seen "
              "its own period of bars")
RETEST_DEFAULT = {
    "status": PROVISIONAL_PINS,
    "margin_atr": RC.PINS_V2["FLIP_HOLD_MARGIN"],      # by object: the ONLY hold
    "hold_bars": RC.PINS_V2["FLIP_HOLD_BARS"],         # pins that existed on disk
    "ttl_bars": RC.PINS_V2["MEM_TTL_BARS"],            # BEFORE the R1 tuning
    "law": RETEST_LAW,
    "source": "the frozen flip-hold pins — the only hold pins on disk before R1",
    "unruled": ("nothing outstanding on the BAND: R1 names the five. The candidacy "
                "TTL (MEM_TTL_BARS 400, superseded at the next macro DIE) and the "
                "band warm-up (NaN until `period` bars) remain executor pins."),
}

# ── THE R1 TUNING — the protocol, fixed BEFORE the look ───────────────────
TUNE_MARGINS = (0.25, 0.5, 1.0)             # R1, verbatim
TUNE_HOLDS = (3, 6, 12)                     # R1, verbatim
TUNE_FLOOR_N = {"5m": 200, "1d": 30}        # R1 · the task's 1d floor
TUNE_LENSES = tuple(TUNE_FLOOR_N)
TUNE_OBJECTIVE = ("pooled median NET term at H20 lens-bars (NET = the pooled median "
                  "term - the cell's BINDING measured toll), over the PANEL17 assets "
                  "that have tuning-era data on this lens; macro DIE at the FROZEN "
                  "SCALE 3.0; TUNING-ERA events only, on tapes CUT at the era boundary "
                  "before the detector runs")
TUNE_TIE_BREAK = ("the pins already on disk (margin 1.0, hold 6) first, then the "
                  "simpler band: tap before ribbon, 89 before 127 before 200")
TUNE_MIN_BARS = 400                         # a tuning tape shorter than the candidacy
                                            # TTL cannot carry one whole window
TUNING_RESULT_NAME = {"5m": "TUNING_RESULT.json", "1d": "TUNING_RESULT_1d.json"}
TUNING_GRID_NAME = {"5m": "TUNING_GRID", "1d": "TUNING_GRID_1d"}
TUNING_GRID_KEY = ["lens", "band", "margin_atr", "hold_bars"]


def tuning_result(lens: str = "5m", root: Path | None = None) -> dict | None:
    """The filed R1 tuning result for one lens, or None before it lands."""
    p = (OUT if root is None else Path(root)) / TUNING_RESULT_NAME[lens]
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        raise SystemExit(f"HALT: unreadable tuning result at {p}")


def resolve_retest_pins(root: Path | None = None) -> dict:
    """THE RETEST PINS OF RECORD for the census: the R1 5m tuning result once it
    has landed, the pre-R1 provisional pins before that.  ONE pin pair rules all
    five bands and all three lenses — R1 prints the other four bands "at the same
    hold pins ... beside as Tier-E", and the 1d tuning is filed SEPARATELY for the
    Tier-E P-BRK-I1 print, never mixed into this grid."""
    res = tuning_result("5m", root)
    if res is None:
        return dict(RETEST_DEFAULT)
    return {"status": TUNED_PINS, "margin_atr": float(res["margin_atr"]),
            "hold_bars": int(res["hold_bars"]), "ttl_bars": int(res["ttl_bars"]),
            "law": RETEST_LAW, "unruled": RETEST_DEFAULT["unruled"],
            "source": (f"R1 tuning, 5m, TUNING_RESULT.json (band {res['band']}, "
                       f"n {res['n']}, objective {res['objective']}, grid sha "
                       f"{res['grid_sha'][:16]})"),
            "scored_band": res["band"], "grid_sha": res["grid_sha"]}


RETEST_PINS = resolve_retest_pins()         # resolved ONCE per process: a run is
                                            # internally consistent or it is nothing

LEANS = (
    "[LEAN-HEPHAESTUS] L1 1d = exactly SIX complete native-4h bars per UTC day (the twin's "
    "law); 1w = seven such complete days, MONDAY-anchored UTC, complete weeks only. Source = "
    "native 4h, never 1h/5m aggregates.",
    "[LEAN-HEPHAESTUS] L2 SCALE_MULT: every registered lane and every Stage-A stamp uses the "
    "FROZEN 3.0 (Pine/twin pin of record). CENSUS-R prints the self-calibrated SCALE tables "
    "WITH the frozen-3.0 tables beside. Calibrator = grid 1.5..4.0 step 0.25 (Pine "
    "minval/step), nearest confirmed-macro-range density to 0.75 per 100 bars, tie-break "
    "toward 3.0 then lower; the whole grid printed (F-GRID: every grid whole).",
    "[LEAN-HEPHAESTUS] L3 analytics module = analytics/rangefinder_census.py: a PURE numpy "
    "port (no engine import, no IO, ATR passed IN as an argument), NOT added to "
    "analytics._MODULES (analytics_sha stays put) — printed as a finding.",
    "[LEAN-HEPHAESTUS] L4 Outcome horizons H20/H100 = BARS OF THE LENS; censor (require "
    "k+H <= n-1), never shorten; anchor = close of the bar the event is KNOWN (known_at); "
    "signs and toll law per map_critic.md §4.6.",
    "[LEAN-HEPHAESTUS] L6 Panels: CLASSIC5 = BTC ETH SOL NEAR ZEC; UNSEEN12 = the "
    "contract's twelve; PANEL17 = CLASSIC5 + admitted UNSEEN12.",
    "[LEAN-HEPHAESTUS] C-a BOUNDARY AGE = bars since the AS-OF boundary VALUE on that side "
    "last changed: set at the confirm bar, moved by each same-side harden's redraw FROM the "
    "harden bar; 0 on the bar it changes. bnd_age = the NEAREST boundary's (tie -> top, the "
    "snapshot's law). range_age = t - confirm_i rides beside. Never from backdated_from: "
    "the back-dated left edge is render-only and lies in the past of its own knowledge.",
    "[LEAN-HEPHAESTUS] C-b with NO live confirmed macro range (most bars at SCALE 3.0) "
    "%-of-range, dist-to-boundary, ages and deviations read NaN / -1 — never the last "
    "corpse's box; in_range says which.",
    "[LEAN-HEPHAESTUS] C-c memory-touch is filed under BOTH definitions: `memory-touch-v1` "
    "(the machine's one-sided first touch per side) and `memory-touch-2s` (the first "
    "two-sided touch of the leash line, verdict unread, anchored at the touch bar).",
    "[LEAN-HEPHAESTUS] C-d retest-hold rides the OPERATOR's five R1 bands — ribbon 89/127, "
    "ribbon 127/200, tap 89, tap 127, tap 200 — EMAs of CLOSE on the lens's own bars, the "
    "warm-up NaN and never imputed. The hold pins (margin_atr, hold_bars) are TUNED under "
    "the R1 protocol on the 5m lens, TUNING ERA ONLY, and ONE pin pair rules all five bands "
    "and all three lenses; the 1d tuning is filed SEPARATELY for the Tier-E P-BRK-I1 print "
    "and never mixed into this grid. The candidacy TTL (400 bars, superseded at the next "
    "macro DIE) and the band warm-up remain executor pins.",
    "[LEAN-HEPHAESTUS] C-h THE ERA SPLIT [R1]: every ledger and grid row carries the era of "
    "its ANCHOR bar's close — 'tuning' <= 2024-06-30T23:59:59Z, 'holdout' after. The grid is "
    "filed three ways per class: 'ALL' (the contract's full-history row) with 'tuning' and "
    "'holdout' BESIDE it. They are not addends: an anchor is in exactly one era, and ALL is "
    "the union, but a median of a union is not a function of the parts' medians.",
    "[LEAN-HEPHAESTUS] C-i THE COLLAR ON P-BRK-S1's SCORING GROUND [LAW 4 + R1]: the 5m "
    "retest-hold rows outside the TUNING era are FILED and never printed, summarised or "
    "quoted — not in a digest, not in a log line, not in a report field. printable(lens, "
    "cls, era) is the one gate and F-C10-COLLAR scans every artifact this build writes.",
    "[LEAN-HEPHAESTUS] C-e the leash runs LEAN (retests=False) on EVERY lens: the two "
    "per-bar spam classes feed none of the six classes and the port's fixture proves the "
    "lean log is the full log minus them. The micro scale is not run: it writes no state, "
    "line or flip.",
    "[LEAN-HEPHAESTUS] C-f the toll bps is READ per asset from Stage D's fee_schedule.json "
    "(round_trip_bps_used) and, absent that file, from tierc2_rules.FEE_BPS_ROUND_TRIP; the "
    "source rides every row. toll_atr on a row = median over THAT row's uncensored anchors; "
    "toll_atr_all = median over all of the class's anchors; pooled rows print the BINDING "
    "(max) per-asset toll.",
    "[LEAN-HEPHAESTUS] C-g n below PROVISIONAL_MIN_N (30) is PRINTED and flagged "
    "provisional, the lineage's law; a statistic is NaN only when n = 0, and then "
    "nan_reason says why (no events / all anchors censored).",
)

TIER = "TIER-E MEASUREMENT — UNSCORED, GATES NOTHING"
GATES = ("NOTHING — TIER-E MEASUREMENT ONLY. No registration rests on this row, none "
         "is implied, and no cell of this grid may be promoted.")
WARRANTY = ("these numbers are true AS OF the bars named in this row and of no other; "
            "the corridor advances with the cache [TC6V-a, carried by TIER-C10]. Pins "
            "were calibrated on BTC only (micro 1D/420, v2 4h/1700): every other asset "
            "and lens is an extrapolation of frozen pins, FULL history, not the Oracle's "
            "1700-bar window.")
AS_OF_COLUMNS = ("as_of_last_closed_4h", "as_of_panel_start", "as_of_span_days",
                 "warranty", "as_of_lens", "as_of_last_closed_bar", "as_of_panel",
                 "as_of_n_assets", "as_of_substrate")
COLLAR_COLUMNS = ("tier", "gates", "m_looks_this_table", "m_note", "in_sample")

LOG_LINES: list[str] = []
_NAN = float("nan")


def log(msg: str = "") -> None:
    print(msg, flush=True)
    LOG_LINES.append(msg)


def clock(msg: str) -> None:
    """Wall-clock facts: stdout ONLY, never an artifact [F-DET law]."""
    print(f"  [clock · stdout only] {msg}", flush=True)


def iso(ms) -> str | None:
    if ms is None:
        return None
    return (datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ"))


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def code_sha() -> str:
    """One sha over the two files a cell's numbers are a function of."""
    h = hashlib.sha256()
    for p in (Path(__file__).resolve(), PORT_PATH):
        h.update(p.read_bytes())
    return h.hexdigest()


def _dump(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n",
                   encoding="utf-8")
    os.replace(tmp, path)


# ═══════════════════════════════════════════════ determinism plumbing
def content_sha(df: pd.DataFrame) -> str:
    """CONTENT hash (the csv), not parquet bytes [tierc2_baseline._content_sha]."""
    return hashlib.sha256(df.to_csv(index=False).encode("utf-8")).hexdigest()


def canon(df: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    """The filed form of a table: floats rounded to ROUND_ND, rows in TOTAL key
    order, str column names.  HALTS IF the declared key is not unique [F-KEY]."""
    d = df.copy()
    d.attrs = {}
    d.columns = [str(c) for c in d.columns]
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].round(ROUND_ND)
    dup = int(d.duplicated(subset=keys).sum())
    if dup:
        ex = d[d.duplicated(subset=keys, keep=False)].head(3)[keys].to_dict("records")
        raise SystemExit(f"HALT (F-KEY): key {keys} is NOT unique — {dup} duplicate "
                         f"row(s), e.g. {ex}")
    return d.sort_values(keys, kind="mergesort").reset_index(drop=True)


def write_table(df: pd.DataFrame, name: str, keys: list[str], root: Path) -> str:
    """canon() -> atomic parquet -> content sha.  Atomic because a killed run
    leaves a footerless stump that Path.exists() happily accepts."""
    root.mkdir(parents=True, exist_ok=True)
    d = canon(df, keys)
    p = root / f"{name}.parquet"
    tmp = p.with_name(p.name + ".tmp")
    d.to_parquet(tmp, index=False)
    os.replace(tmp, p)
    return content_sha(d)


# ═══════════════════════════════════════════════ Stage D, read as DATA
def stage_d_pin() -> dict | None:
    p = STAGE_D / "AS_OF_PIN.json"
    return json.loads(p.read_text()) if p.exists() else None


def stage_d_manifest() -> dict | None:
    p = STAGE_D / "STAGE_D_MANIFEST.json"
    return json.loads(p.read_text()) if p.exists() else None


def panels() -> dict:
    """Panel name -> stems, from Stage D's manifest [L6].  HALTS IF a named
    panel is asked for and Stage D has not landed (a panel is never guessed)."""
    man = stage_d_manifest()
    if man is None:
        raise SystemExit(f"HALT: no Stage D manifest under {STAGE_D} — name the "
                         "assets explicitly (--assets SYM,SYM) or land Stage D")
    p = man["panels"]
    return {"CLASSIC5": list(p["CLASSIC5"]),
            "UNSEEN12": list(p["UNSEEN_admitted_stems"]),
            "PANEL17": list(p["PANEL17_stems"])}


POOL_ALL = "POOLED:ALL"
SUB_POOLS = ("CLASSIC5", "UNSEEN12")            # [L6] filed BESIDE POOLED:ALL


def pools_for(assets: list) -> dict:
    """THE POOLS of one commission, label -> member stems in commission order:
    POOLED:ALL (every commissioned asset) and, beside it, POOLED:CLASSIC5 and
    POOLED:UNSEEN12 [L6] — the known five apart from the unseen twelve, so a
    pooled row never lets the tapes the pins were met on speak for the ones
    they were not.  A sub-pool is filed ONLY when it is non-empty AND a PROPER
    subset of the commission: a sub-pool that IS the commission would be
    POOLED:ALL's row under a second label (the smoke, a CLASSIC5 run).
    Membership is READ from Stage D's manifest, never typed; with no Stage D
    there is no sub-pool."""
    out = {POOL_ALL: list(assets)}
    if stage_d_manifest() is None:
        return out
    P = panels()
    for name in SUB_POOLS:
        mem = [a for a in assets if a in set(P[name])]
        if mem and len(mem) < len(assets):
            out[f"POOLED:{name}"] = mem
    return out


def as_of_close_ms(fallback_stem: str | None = None) -> tuple[int, str]:
    """(AS_OF close ms, source).  The Stage D pin when present; otherwise the
    asked asset's OWN last native-4h bar — printed as a fallback, never silent."""
    pin = stage_d_pin()
    if pin is not None:
        return int(pin["as_of_last_closed_4h_close_ms"]), "Stage D AS_OF_PIN.json"
    if fallback_stem is None:
        raise SystemExit("HALT: no Stage D AS_OF pin and no asset to fall back on")
    f = pd.read_parquet(cache_dir() / "klines" / f"{fallback_stem}_4h.parquet",
                        columns=["open_time"])
    return (int(f["open_time"].max()) + LENS_MS["4h"],
            f"FALLBACK: {fallback_stem}_4h.parquet's own last bar (no Stage D pin)")


def toll_bps_for(stem: str) -> tuple[float, str]:
    """The round-trip toll in bps for one asset, READ from the estate fee
    object — Stage D's per-asset fee_schedule.json when it has landed, the
    tier card's FEE_BPS_ROUND_TRIP object otherwise.  Never a typed literal
    [F-C10-TOLL]; the source rides every row that quotes it."""
    p = STAGE_D / "fee_schedule.json"
    if p.exists():
        for a in json.loads(p.read_text())["assets"]:
            if a.get("stem") == stem:
                return (float(a["round_trip_bps_used"]),
                        f"research_outputs/tierc10/data/fee_schedule.json[{stem}]"
                        ".round_trip_bps_used")
    return float(R2.FEE_BPS_ROUND_TRIP), "scripts/tierc2_rules.py FEE_BPS_ROUND_TRIP"


# ═══════════════════════════════════════════════ 1 · THE TAPE
@dataclass
class Tape:
    sym: str
    lens: str
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    t0: np.ndarray                  # bar OPEN ms, int64
    ts: list                        # ISO-sortable strings, bar OPEN
    atr: np.ndarray                 # engine Wilder RMA seeded at TR[0], finite
    meta: dict = field(default_factory=dict)

    @property
    def n(self) -> int:
        return len(self.c)

    @property
    def step(self) -> int:
        return LENS_MS[self.lens]

    @property
    def d(self) -> tuple:
        """The port's positional tape."""
        return (self.o, self.h, self.l, self.c, self.ts)

    def head(self, t: int) -> "Tape":
        """tape[:t] — a PREFIX.  The ATR is seeded at TR[0], so atr[:t] IS the
        prefix's own ATR; a tail would not be (it re-warms) and is refused."""
        return Tape(self.sym, self.lens, self.o[:t], self.h[:t], self.l[:t],
                    self.c[:t], self.t0[:t], self.ts[:t], self.atr[:t],
                    dict(self.meta, prefix_of=self.n))


def daily_from_4h(f4: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """[L1] native 4h -> 1d: a UTC day exists ONLY if all of its 4h bars do.
    Returns (frame open_time/open/high/low/close, dropped incomplete days)."""
    day = (f4["open_time"] // DAY_MS).to_numpy()
    g = (f4.assign(_day=day).groupby("_day")
         .agg(n=("open_time", "size"), open=("open", "first"), high=("high", "max"),
              low=("low", "min"), close=("close", "last")))
    keep = g[g["n"] == BARS_PER_DAY_4H]
    d = pd.DataFrame({"open_time": keep.index.to_numpy(np.int64) * DAY_MS,
                      "open": keep["open"].to_numpy(), "high": keep["high"].to_numpy(),
                      "low": keep["low"].to_numpy(), "close": keep["close"].to_numpy()})
    return d, int((g["n"] != BARS_PER_DAY_4H).sum())


def load_tape(sym: str, lens: str, tail_bars: int | None = None) -> Tape:
    """Full history of (sym, lens) from the snapshot, CLOSED bars <= AS_OF.

    HALTS IF: the file is missing; a stamp repeats or runs backward; an OHLC
    value is not finite (the machine has no NaN guard — a NaN would silently
    turn every comparison it touches False); the 1d tape derived here differs
    from Stage D's derived file.  Gaps are COUNTED into the meta and never
    filled: a missing bar compresses the machine's bar-counted pins, and the
    reader is told how many.  `tail_bars` is for the timing probe ONLY — a
    tail re-warms the ATR and is therefore never a census cell.
    """
    if lens not in LENSES:
        raise SystemExit(f"HALT: unknown lens {lens!r}; one of {list(LENSES)}")
    src = LENS_SOURCE[lens]
    p = cache_dir() / "klines" / f"{sym}_{src}.parquet"
    if not p.exists():
        raise SystemExit(f"HALT: missing {p}")
    close_ms, as_of_src = as_of_close_ms(sym)
    f = pd.read_parquet(p).sort_values("open_time", kind="mergesort").reset_index(drop=True)
    rows_file = len(f)
    f = f[f["open_time"] + LENS_MS[src] <= close_ms].reset_index(drop=True)
    dropped_days = None
    if lens == "1d":
        f, dropped_days = daily_from_4h(f)
        f = f[f["open_time"] + DAY_MS <= close_ms].reset_index(drop=True)
        q = cache_dir() / "klines" / f"{sym}_1d.parquet"
        if q.exists():
            sd = pd.read_parquet(q).sort_values("open_time").reset_index(drop=True)
            sd = sd[sd["open_time"] + DAY_MS <= close_ms].reset_index(drop=True)
            cols = ["open_time", "open", "high", "low", "close"]
            if len(sd) != len(f) or not all(
                    np.array_equal(sd[k].to_numpy(), f[k].to_numpy()) for k in cols):
                raise SystemExit(f"HALT: the 1d tape derived here for {sym} "
                                 f"({len(f)} days) is not Stage D's {q.name} "
                                 f"({len(sd)} days) — one law [L1], two answers")
    t0 = f["open_time"].to_numpy(np.int64)
    o, h, l, c = (f[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    step = LENS_MS[lens]
    dt = np.diff(t0)
    if len(t0) == 0:
        raise SystemExit(f"HALT: {sym} {lens}: no closed bar at or before AS_OF")
    if (dt <= 0).any():
        raise SystemExit(f"HALT: {sym} {lens}: {int((dt <= 0).sum())} repeated or "
                         "backward stamps")
    if not (np.isfinite(o) & np.isfinite(h) & np.isfinite(l) & np.isfinite(c)).all():
        raise SystemExit(f"HALT: {sym} {lens}: non-finite OHLC")
    gaps = int((dt > step).sum())
    missing = int((dt[dt > step] // step - 1).sum())
    if tail_bars is not None:
        k = max(0, len(t0) - int(tail_bars))
        t0, o, h, l, c = t0[k:], o[k:], h[k:], l[k:], c[k:]
    ts = pd.to_datetime(t0, unit="ms", utc=True).strftime(TS_FMT[lens]).tolist()
    atr = ind.atr(h, l, c, RC.ATR_LEN)
    meta = {
        "asset": sym, "lens": lens, "source_file": f"klines/{p.name}",
        "source_sha256": file_sha256(p), "source_rows_file": int(rows_file),
        "derived": (f"1d = {BARS_PER_DAY_4H} complete native-4h bars per UTC day [L1]"
                    if lens == "1d" else "native"),
        "dropped_incomplete_days": dropped_days,
        "n_bars": int(len(t0)), "first_bar_open_ms": int(t0[0]),
        "last_bar_open_ms": int(t0[-1]), "first_bar_open": iso(t0[0]),
        "last_bar_close": iso(int(t0[-1]) + step),
        "span_days": round((int(t0[-1]) + step - int(t0[0])) / DAY_MS, 1),
        "gap_count": gaps, "missing_bars_total": missing,
        "gap_note": ("gaps are COUNTED, never filled: a missing bar compresses every "
                     "bar-counted pin (TTL, hold, lifetimes)"),
        "as_of_close_ms": int(close_ms), "as_of_last_closed_4h": iso(close_ms),
        "as_of_source": as_of_src,
        "tail_bars": None if tail_bars is None else int(tail_bars),
    }
    return Tape(sym, lens, o, h, l, c, t0, ts, atr, meta)


# ═══════════════════════════════════════════════ 2 · THE MACHINE, VIA THE PORT
def run_scale(tape: Tape, scale_mult: float) -> dict:
    """Macro machine + LEAN leash at one SCALE [C-e]: the census call."""
    return RC.run_v2(tape.d, tape.atr, dict(RC.PINS_V2, SCALE_MULT=float(scale_mult)),
                     with_micro=False, retests=False)


def density_per_100(m: dict) -> float:
    return 100.0 * m["n_confirmed"] / m["n_bars"]


def pick_scale(dens: dict) -> float:
    """[L2] the grid cell whose confirmed-macro-range density is NEAREST the
    target; ties go toward the frozen 3.0, then to the lower SCALE.  Grid +
    nearest, never bisection: the density curve is not monotone."""
    return min(sorted(dens), key=lambda s: (round(abs(dens[s] - DENSITY_TARGET_PER_100), 9),
                                            abs(s - FROZEN_SCALE), s))


def calibrate(tape: Tape) -> tuple[float, pd.DataFrame]:
    """SCALE self-calibration, the WHOLE grid returned.  IN-SAMPLE BY
    CONSTRUCTION: the pick is fitted on the whole tape, so every macro event
    downstream of it is in-sample with respect to that pin — which is why no
    registered lane and no Stage-A stamp may read it [L2]."""
    rows, dens = [], {}
    for s in SCALE_GRID:
        m = RC.run_machine(tape.d, tape.atr, RC.macro_pins(s))
        dens[s] = density_per_100(m)
        rows.append({"asset": tape.sym, "lens": tape.lens, "scale_mult": float(s),
                     "n_bars": int(m["n_bars"]), "n_confirmed": int(m["n_confirmed"]),
                     "density_per_100": dens[s],
                     "abs_err_to_target": abs(dens[s] - DENSITY_TARGET_PER_100),
                     "coverage_pct": float(m["coverage_pct"]),
                     "mean_confirmed_lifetime": (_NAN if m["mean_confirmed_lifetime"] is None
                                                 else float(m["mean_confirmed_lifetime"])),
                     "density_quantum_per_100": 100.0 / m["n_bars"],
                     "is_frozen_pin": bool(s == FROZEN_SCALE)})
    pick = pick_scale(dens)
    g = pd.DataFrame(rows)
    g["chosen"] = g["scale_mult"] == pick
    # a pick on the grid's EDGE, or a grid that never brackets the target, is a
    # CLAMP, not a fit — said in columns so no reader takes 1.50 for a calibration
    g["pick_at_grid_edge"] = bool(pick in (SCALE_GRID[0], SCALE_GRID[-1]))
    g["target_bracketed"] = bool(min(dens.values()) <= DENSITY_TARGET_PER_100
                                 <= max(dens.values()))
    g["target_per_100"] = DENSITY_TARGET_PER_100
    g["tie_break"] = "nearest density; then toward 3.0; then the lower SCALE"
    g["calibrated_in_sample"] = True
    return pick, g


# ═══════════════════════════════════════════════ 3 · THE AS-OF LAYER
def _step_fill(n: int, cps: list, fill, dtype) -> np.ndarray:
    """A step function from change points [(bar, value)] in LOG order: the
    value at bar t is that of the LAST change point with bar <= t."""
    out = np.full(n, fill, dtype=dtype)
    if not cps:
        return out
    ii = np.array([i for i, _ in cps], dtype=np.int64)
    vv = np.array([v for _, v in cps], dtype=dtype)
    if (np.diff(ii) < 0).any():
        raise ValueError("census as-of: change points out of bar order")
    k = np.searchsorted(ii, np.arange(n, dtype=np.int64), side="right") - 1
    ok = k >= 0
    out[ok] = vv[k[ok]]
    return out


def known_frame(m: dict) -> pd.DataFrame:
    """Every event of ONE machine run (macro or micro) with the bar it is
    KNOWN at: a pivot at its SEAL (the port's seals — the machine's
    knowable_at can read -1), everything else at its own bar."""
    ka = RC.machine_known_at(m)
    ev = m["events"]
    # the -1 quirk, held OUT in code: a known bar is never before the tape and
    # never before the event's own stamp (the engine's knowable_at = -1 read as
    # a known bar would be both) [F-RNG-ASOF-SEAL proves the seal on raw bars]
    early = [e["i"] for k, e in zip(ka, ev) if k < e["i"] or k < 0]
    if early:
        raise ValueError(f"census as-of: {len(early)} event(s) known BEFORE their own "
                         f"stamp bar, e.g. bar {early[0]} — a seal was not read")
    return pd.DataFrame({"pos": np.arange(len(ev)), "i": [e["i"] for e in ev],
                         "known_at": ka, "event": [e["event"] for e in ev],
                         "rid": [int(e["rid"]) if "rid" in e else -1 for e in ev],
                         "side": [e.get("side", "") for e in ev]})


def leash_frame(leash: list, hold_bars: int) -> pd.DataFrame:
    """Every leash event with its known_at: a flip / failed / truncated verdict
    at touch + HOLD, a same-side touch or an expiry at its own bar."""
    ka = RC.leash_known_at(leash, hold_bars)
    return pd.DataFrame({"pos": np.arange(len(leash)), "i": [e["i"] for e in leash],
                         "known_at": ka, "event": [e["event"] for e in leash],
                         "rid": [int(e["rid"]) for e in leash],
                         "side": [e["side"] for e in leash],
                         "verdict": [e.get("verdict", "") for e in leash]})


def asof_view(tape: Tape, macro: dict, leash: list) -> dict:
    """THE PER-BAR AS-OF ARRAYS.  Element t of every array is what a reader
    standing at the CLOSE of bar t can know — no more.

      in_range / rid     a CONFIRMED macro range is alive: confirm_i <= t < die_i
                         (dead BY the close of die_i); never from seed_i, p0_bar
                         or backdated_from.
      state              0 NEUTRAL · +1 BULL_EXP · -1 BEAR_EXP, the machine's
                         own latch replayed from confirm / breakout-die and the
                         first SEALED pivot.
      top / bot          top0 / bottom0 from the confirm bar, moved by each
                         harden FROM the harden bar to the wick extreme of its
                         episode (raw tape, full precision) — the pre-redraw
                         value until the redraw is known.
      pct / dist_atr / near_side   100*(c-bot)/(top-bot) unclamped;
                         min(|top-c|, |c-bot|)/atr; tie -> top.
      top_age / bot_age / bnd_age / range_age   [LEAN C-a]; -1 out of range.
      dev_top / dev_bot  hardens on that side SO FAR; inc_top / inc_bot the
                         inception zone (the defining wick beyond the body).
      covered            the machine's coverage mask, rebuilt as-of (asserted
                         equal to the mask the machine computes bar by bar).
      flip_pol / flip_age   last flip KNOWN (touch + HOLD <= t): +1 support /
                         -1 resistance / 0 none; bars since it became known.

    RAISES IF: the as-of replay does not land on the machine's own end-of-life
    boundaries or coverage mask — the recipe and the machine have parted.
    """
    n = tape.n
    h, l, c, atr = tape.h, tape.l, tape.c, tape.atr
    if RC.PINS.get("REDRAW_BASIS", "wick") != "wick" or RC.PINS.get("MULTI_ACTIVE", 0):
        raise ValueError("census as-of: the recipe is proven for REDRAW_BASIS == 'wick' "
                         "and ONE active range only")
    hold = int(RC.PINS_V2["FLIP_HOLD_BARS"])
    ev = macro["events"]
    by_rid = {r.rid: r for r in macro["ranges"]}

    # episodes: a harden closes the last same-side breach-open of its range
    opens: dict = {}
    hardens: dict = {}
    for e in ev:
        if e["event"] == "breach-open":
            opens[(e["rid"], e["side"])] = e["i"]
        elif e["event"] == "harden":
            hardens.setdefault(e["rid"], []).append(
                (e["i"], e["side"], opens[(e["rid"], e["side"])]))

    cp_rid, cp_top, cp_bot, cp_conf = [], [], [], []
    cp_tsince, cp_bsince, cp_dt, cp_db, cp_it, cp_ib = [], [], [], [], [], []
    cp_shi, cp_slo = [], []
    last_die = -1
    for r in macro["ranges"]:
        if r.confirm_i < 0:
            continue
        a = int(r.confirm_i)
        if a < last_die:
            raise ValueError("census as-of: confirmed lives overlap (ONE_ACTIVE broken)")
        top, bot = float(r.top0), float(r.bottom0)
        hb, lb = ((r.p0_bar, r.p1_bar) if r.confirm_side == "top"
                  else (r.p1_bar, r.p0_bar))
        z_hi, z_lo = float(h[hb]), float(l[lb])        # the defining wicks
        n_t = n_b = 0
        for cps, v in ((cp_rid, r.rid), (cp_top, top), (cp_bot, bot), (cp_conf, a),
                       (cp_tsince, a), (cp_bsince, a), (cp_dt, 0), (cp_db, 0),
                       (cp_it, int(z_hi > top)), (cp_ib, int(z_lo < bot)),
                       (cp_shi, max(top, z_hi)), (cp_slo, min(bot, z_lo))):
            cps.append((a, v))
        for i, side, a_open in hardens.get(r.rid, ()):
            if side == "top":
                top = max(top, float(h[a_open:i + 1].max()))
                n_t += 1
                cp_top.append((i, top)); cp_tsince.append((i, i)); cp_dt.append((i, n_t))
                cp_shi.append((i, max(top, z_hi)))
            else:
                bot = min(bot, float(l[a_open:i + 1].min()))
                n_b += 1
                cp_bot.append((i, bot)); cp_bsince.append((i, i)); cp_db.append((i, n_b))
                cp_slo.append((i, min(bot, z_lo)))
        if top != r.top or bot != r.bottom:
            raise ValueError(f"census as-of: rid {r.rid} replays to ({bot}, {top}) but the "
                             f"machine ended it at ({r.bottom}, {r.top})")
        if r.die_i >= 0 and r.state == "DEAD":
            d_i = int(r.die_i)
            last_die = d_i
            for cps, v in ((cp_rid, -1), (cp_top, _NAN), (cp_bot, _NAN), (cp_conf, -1),
                           (cp_tsince, -1), (cp_bsince, -1), (cp_dt, 0), (cp_db, 0),
                           (cp_it, 0), (cp_ib, 0), (cp_shi, _NAN), (cp_slo, _NAN)):
                cps.append((d_i, v))

    def fill(cps, fill_v, dtype):
        return _step_fill(n, sorted(cps, key=lambda x: x[0]), fill_v, dtype)

    rid = fill(cp_rid, -1, np.int64)
    top_a, bot_a = fill(cp_top, _NAN, float), fill(cp_bot, _NAN, float)
    in_range = rid >= 0
    t_idx = np.arange(n, dtype=np.int64)
    conf = fill(cp_conf, -1, np.int64)
    tsince, bsince = fill(cp_tsince, -1, np.int64), fill(cp_bsince, -1, np.int64)
    with np.errstate(invalid="ignore", divide="ignore"):
        pct = 100.0 * (c - bot_a) / (top_a - bot_a)
        d_top, d_bot = np.abs(top_a - c), np.abs(c - bot_a)
        dist = np.minimum(d_top, d_bot) / atr
        shi, slo = fill(cp_shi, _NAN, float), fill(cp_slo, _NAN, float)
        covered = in_range & (slo <= c) & (c <= shi)
    near_top = in_range & (d_top <= d_bot)                 # tie -> top
    near_side = np.where(in_range, np.where(near_top, 1, -1), 0).astype(np.int8)
    top_age = np.where(in_range, t_idx - tsince, -1)
    bot_age = np.where(in_range, t_idx - bsince, -1)
    if not np.array_equal(covered, np.asarray(macro["covered"], dtype=bool)):
        raise ValueError("census as-of: the rebuilt coverage mask is not the machine's")

    # macro state: the machine's latch, replayed from what is KNOWN
    cp_state: list = []
    if any(int(s) <= int(p[0]) for p, s in zip(macro["pivots"], macro["seals"])):
        raise ValueError("census as-of: a pivot's seal is not AFTER its wick bar — the "
                         "engine's knowable_at = -1 quirk must never reach this layer")
    if macro["pivots"]:
        k0 = min(range(len(macro["pivots"])),
                 key=lambda k: (macro["seals"][k], macro["pivots"][k][0]))
        cp_state.append((int(macro["seals"][k0]),
                         1 if macro["pivots"][k0][2] == -1 else -1))
    life = [(e["i"], 0 if e["event"] == "confirm" else (1 if e["side"] == "top" else -1))
            for e in ev if e["event"] in ("confirm", "breakout-die")]
    state = _step_fill(n, sorted(cp_state + life, key=lambda x: x[0]), 0, np.int8)

    # last flip KNOWN: touch + HOLD
    lf = leash_frame(leash, hold)
    fl = lf[lf["event"] == "flip"].sort_values(["known_at", "pos"], kind="mergesort")
    pol = [1 if s == "top" else -1 for s in fl["side"]]
    flip_pol = _step_fill(n, list(zip(fl["known_at"].tolist(), pol)), 0, np.int8)
    flip_known = _step_fill(n, list(zip(fl["known_at"].tolist(),
                                        fl["known_at"].tolist())), -1, np.int64)
    flip_age = np.where(flip_known >= 0, t_idx - flip_known, -1)
    flip_rid = _step_fill(n, list(zip(fl["known_at"].tolist(), fl["rid"].tolist())),
                          -1, np.int64)

    return {
        "n": n, "rid": rid, "in_range": in_range, "state": state,
        "top": top_a, "bot": bot_a, "pct": pct, "dist_atr": dist, "near_side": near_side,
        "top_age": top_age, "bot_age": bot_age,
        "bnd_age": np.where(near_top, top_age, bot_age),
        "range_age": np.where(in_range, t_idx - conf, -1),
        "dev_top": fill(cp_dt, 0, np.int64), "dev_bot": fill(cp_db, 0, np.int64),
        "inc_top": fill(cp_it, 0, np.int64), "inc_bot": fill(cp_ib, 0, np.int64),
        "covered": covered, "flip_pol": flip_pol, "flip_age": flip_age,
        "flip_rid": flip_rid,
        "_by_rid": by_rid, "_leash_frame": lf,
    }


def asof_index(tape: Tape, instant_ms) -> np.ndarray:
    """The bar a reader standing at `instant_ms` may read: the LAST bar of the
    lens whose CLOSE is at or before the instant; -1 before the first close.
    A bar still forming at the instant — a 4h or 1d bar around a 5m entry — is
    never read, which is the engine's own law (engine/htf.map_htf_to_exec)."""
    closes = tape.t0 + tape.step
    return np.searchsorted(closes, np.asarray(instant_ms, dtype=np.int64), side="right") - 1


STATE_NAME = {0: "NEUTRAL", 1: "BULL_EXP", -1: "BEAR_EXP"}


def stamps_at(tape: Tape, view: dict, idx: int) -> dict:
    """THE STAGE-A STAMP RECORD at one as-of bar (idx from asof_index): macro
    state · %-of-range · dist-to-boundary ATR · boundary age · deviations per
    side · last flip — CAPTURED, NEVER CONSULTED.  idx = -1 (no closed bar
    yet) and every out-of-range field read None, never a neighbour's value."""
    if idx < 0:
        return {"rf_lens": tape.lens, "rf_bar_close_ms": None, "rf_state": None,
                "rf_in_range": None, "rf_pct_of_range": None, "rf_dist_boundary_atr": None,
                "rf_nearest_side": None, "rf_boundary_age": None, "rf_range_age": None,
                "rf_dev_top": None, "rf_dev_bot": None, "rf_inception_top": None,
                "rf_inception_bot": None, "rf_last_flip": None, "rf_last_flip_age": None}
    inside = bool(view["in_range"][idx])
    pol = int(view["flip_pol"][idx])

    def f(a):
        return float(a[idx]) if inside and np.isfinite(a[idx]) else None

    def k(a):
        return int(a[idx]) if inside else None
    return {"rf_lens": tape.lens, "rf_bar_close_ms": int(tape.t0[idx]) + tape.step,
            "rf_state": STATE_NAME[int(view["state"][idx])], "rf_in_range": inside,
            "rf_pct_of_range": f(view["pct"]), "rf_dist_boundary_atr": f(view["dist_atr"]),
            "rf_nearest_side": ({1: "top", -1: "bottom"}[int(view["near_side"][idx])]
                                if inside else None),
            "rf_boundary_age": k(view["bnd_age"]), "rf_range_age": k(view["range_age"]),
            "rf_dev_top": k(view["dev_top"]), "rf_dev_bot": k(view["dev_bot"]),
            "rf_inception_top": k(view["inc_top"]), "rf_inception_bot": k(view["inc_bot"]),
            "rf_last_flip": {1: "support", -1: "resistance", 0: None}[pol],
            "rf_last_flip_age": int(view["flip_age"][idx]) if pol else None}


ASOF_ARRAYS = ("rid", "in_range", "state", "top", "bot", "pct", "dist_atr", "near_side",
               "top_age", "bot_age", "bnd_age", "range_age", "dev_top", "dev_bot",
               "inc_top", "inc_bot", "covered", "flip_pol", "flip_age", "flip_rid")


# ═══════════════════════════════════════════════ 4 · THE SIX CLASSES
def band_ema_line(period: int):
    """band = callable(close) -> (lo, hi).  One EMA line: lo == hi.  NaN — no
    touch can read it — until the EMA has seen `period` bars (the lineage's
    warm-up law: no arming before bar 316 on e316).  The EMA is the engine's,
    seeded at the series start, so ema(c)[:t] IS ema(c[:t])."""
    def band(c: np.ndarray):
        e = ind.ema(c, period)
        e[:period] = np.nan
        return e, e.copy()
    band.label = f"EMA{period} line"
    return band


def band_ema_pair(p1: int, p2: int):
    """band = [min, max](EMA p1, EMA p2), evaluated AT each bar; NaN until the
    SLOWER of the two has seen its own period."""
    def band(c: np.ndarray):
        a, b = ind.ema(c, p1), ind.ema(c, p2)
        lo, hi = np.minimum(a, b), np.maximum(a, b)
        lo[:max(p1, p2)] = np.nan
        hi[:max(p1, p2)] = np.nan
        return lo, hi
    band.label = f"[min,max](EMA{p1}, EMA{p2})"
    return band


def band_of(name: str):
    """THE FIVE R1 BANDS by name — EMAs of CLOSE on the lens's own bars, the
    warm-up NaN and never imputed.  `ribbonA_B` = [min, max](EMA A, EMA B);
    `tapP` = the single line (lo == hi == EMA P)."""
    if name.startswith("ribbon"):
        a, b = (int(x) for x in name[len("ribbon"):].split("_"))
        return band_ema_pair(a, b)
    return band_ema_line(int(name[len("tap"):]))


RETEST_BAND_NAMES = tuple(c[len("retest-hold-"):] for c in RETEST_CLASSES)
RETEST_BANDS = tuple((n, band_of(n)) for n in RETEST_BAND_NAMES)


def retest_holds(tape: Tape, dies: list, lo: np.ndarray, hi: np.ndarray,
                 margin_atr: float, hold_bars: int, ttl_bars: int) -> list[dict]:
    """THE PARAMETERISED RETEST-HOLD DETECTOR [LEAN C-d, PROVISIONAL-PINS].
    `dies` = [(die_i, rid, side)] in bar order; (lo, hi) = the band per bar.

    One evaluation per DIE: the first bar j in (die_i, min(die_i + ttl_bars,
    next die - 1)] whose [low, high] meets the band AND whose PRIOR close sat
    beyond the band on the die side (top-DIE: c[j-1] > hi[j-1] — price comes
    DOWN to it).  Touches from the other side spend nothing.  Then, for k in
    j..j+hold_bars: FAILED iff c[k] < lo[k] - margin*atr[k] (top-DIE; mirrored
    for a bottom-DIE).  j + hold_bars >= n => TRUNCATED, never a hold.
    known_at = j + hold_bars for all three verdicts.  DIEs that are never
    retested return NO row (their window's end is not a bar-t fact).
    """
    h, l, c, atr = tape.h, tape.l, tape.c, tape.atr
    n, H = tape.n, int(hold_bars)
    rows = []
    for q, (d_i, rid, side) in enumerate(dies):
        nxt = dies[q + 1][0] if q + 1 < len(dies) else n
        end = min(d_i + int(ttl_bars), nxt - 1, n - 1)
        if end <= d_i:
            continue
        w = np.arange(d_i + 1, end + 1)
        with np.errstate(invalid="ignore"):
            touch = (l[w] <= hi[w]) & (h[w] >= lo[w])
            opp = (c[w - 1] > hi[w - 1]) if side == "top" else (c[w - 1] < lo[w - 1])
        hit = np.nonzero(touch & opp)[0]
        if not len(hit):
            continue
        j = int(w[hit[0]])
        if j + H >= n:
            verdict = "truncated"
        else:
            k = np.arange(j, j + H + 1)
            with np.errstate(invalid="ignore"):
                through = ((c[k] < lo[k] - margin_atr * atr[k]) if side == "top"
                           else (c[k] > hi[k] + margin_atr * atr[k]))
                unread = ~np.isfinite(lo[k]) | ~np.isfinite(hi[k])
            verdict = "failed" if (through | unread).any() else "hold"
        rows.append({"rid": int(rid), "side": side, "die_i": int(d_i), "touch_i": j,
                     "known_at": j + H, "verdict": verdict})
    return rows


# ═══════════════════════════════════════════════ 4b · THE R1 TUNING
# THE CODE PATH IS INCAPABLE OF READING A HOLDOUT-ERA ROW: era_cut() cuts the
# tape BEFORE any detector sees it, tune() REFUSES a tape whose last bar closes
# after the boundary, and nothing in this section ever reloads a tape.  A hold
# whose window completes after the boundary is not on the cut tape at all, so
# it cannot count — "as-of clean" in the strongest sense available.
def era_cut(tape: Tape) -> int:
    """The number of leading bars of `tape` whose CLOSE is inside the tuning
    era.  0 when the tape starts after the boundary."""
    return int(np.searchsorted(tape.t0 + tape.step, ERA_BOUNDARY_MS, side="right"))


def tuning_tapes(assets: list, lens: str) -> tuple[dict, list]:
    """(cut tapes by stem, skipped rows).  THE ONLY DOOR into the tuning: every
    tape that comes out is already CUT at the era boundary."""
    keep, skipped = {}, []
    for sym in assets:
        tape = load_tape(sym, lens)
        t = era_cut(tape)
        if t < TUNE_MIN_BARS:
            skipped.append({"asset": sym, "lens": lens, "tuning_era_bars": t,
                            "reason": (f"fewer than TUNE_MIN_BARS ({TUNE_MIN_BARS}) "
                                       "tuning-era bars — no whole candidacy window")})
            continue
        keep[sym] = tape.head(t)
    return keep, skipped


def _tune_ledgers(cut: Tape, band, margin: float, hold: int, ttl: int,
                  cls: str, dies: list, view: dict, bps: float) -> pd.DataFrame:
    """One (band, margin, hold) cell's ledger on ONE cut tape, through the
    census's OWN detector, ledger and era law — nothing re-implemented."""
    lo, hi = band(cut.c)
    up = {"top": 1, "bottom": -1}
    rows = [{"cls": cls, "i": g["touch_i"], "known_at": g["known_at"], "rid": g["rid"],
             "side": g["side"], "sgn": up[g["side"]]}
            for g in retest_holds(cut, dies, lo, hi, margin, hold, ttl)
            if g["verdict"] == "hold"]
    cols = ["cls", "i", "known_at", "rid", "side", "sgn"]
    evf = (pd.DataFrame(rows, columns=cols) if rows else
           pd.DataFrame({k: pd.Series(dtype=(object if k in ("cls", "side") else np.int64))
                         for k in cols}))
    for k in ("i", "known_at", "rid", "sgn"):
        evf[k] = evf[k].astype(np.int64)
    return outcome_ledger(cut, evf, view, bps)


def tune(cut: dict, lens: str, floor_n: int, ttl: int | None = None) -> tuple:
    """THE R1 GRID, WHOLE: five bands x margin_atr {0.25, 0.5, 1.0} x hold_bars
    {3, 6, 12} on ALREADY-CUT tuning-era tapes, macro DIE at the FROZEN SCALE
    3.0, objective = the pooled median NET term at H20 under the census's own
    pooling law (BINDING toll).  Returns (grid frame, result dict).

    HALTS IF a tape handed in carries a bar that closes after the era boundary
    — the one guard that makes this path incapable of a holdout-era look."""
    for sym, t in cut.items():
        last = int(t.t0[-1] + t.step)
        if last > ERA_BOUNDARY_MS:
            raise SystemExit(f"HALT: tuning tape {sym} {lens} ends at {iso(last)}, after "
                             f"the era boundary {ERA_BOUNDARY_ISO} — the tuning path "
                             "may not see a holdout-era bar")
    ttl = int(RETEST_DEFAULT["ttl_bars"] if ttl is None else ttl)
    per = {}
    for sym, t in cut.items():
        v2 = run_scale(t, float(FROZEN_SCALE))
        view = asof_view(t, v2["macro"], v2["leash"])
        dies = [(e["i"], e["rid"], e["side"]) for e in v2["macro"]["events"]
                if e["event"] == "breakout-die"]
        per[sym] = (t, view, dies, *toll_bps_for(sym))
    rows = []
    for bname, band in RETEST_BANDS:
        cls = f"retest-hold-{bname}"
        for margin in TUNE_MARGINS:
            for hold in TUNE_HOLDS:
                leds, asset_rows = [], []
                for sym, (t, view, dies, bps, src) in per.items():
                    led = _tune_ledgers(t, band, float(margin), int(hold), ttl,
                                        cls, dies, view, bps)
                    led = canon(led.assign(asset=sym, lens=lens, scale_kind="frozen3.0",
                                           scale_mult=float(FROZEN_SCALE),
                                           pins_status=TUNED_PINS), LEDGER_KEY)
                    leds.append(led)
                    asset_rows += grid_rows(led, sym, lens, "frozen3.0",
                                            float(FROZEN_SCALE), bps, src)
                af = pd.DataFrame(asset_rows)
                pooled = grid_rows(pd.concat(leds, ignore_index=True), "POOLED:TUNE",
                                   lens, "frozen3.0", float(FROZEN_SCALE), None,
                                   "per asset — see the asset rows", tolls=af)
                pf = pd.DataFrame(pooled)
                q = pf[(pf["cls"] == cls) & (pf["era"] == ERA_TUNING)
                       & (pf["horizon"] == "H20")]
                if len(q) != 1:
                    raise SystemExit(f"HALT: tuning cell {bname}|{margin}|{hold}: "
                                     f"{len(q)} pooled H20 rows")
                r = q.iloc[0]
                a20 = af[(af["era"] == ERA_TUNING) & (af["horizon"] == "H20")]
                rows.append({
                    "lens": lens, "band": bname, "band_label": band.label,
                    "margin_atr": float(margin), "hold_bars": int(hold),
                    "ttl_bars": ttl, "cls": cls, "era": ERA_TUNING,
                    "n": int(r["n"]), "n_events": int(r["n_events"]),
                    "n_censored": int(r["n_censored"]),
                    "median_term": float(r["median_term"]),
                    "toll_atr": float(r["toll_atr"]),
                    "objective_net_h20": float(r["net"]),
                    "hit_rate": float(r["hit_rate"]),
                    "median_mfe": float(r["median_mfe"]),
                    "median_mae": float(r["median_mae"]),
                    "n_assets_with_events": int((a20["n"] > 0).sum()),
                    "floor_n": int(floor_n),
                    "eligible": bool(int(r["n"]) >= int(floor_n)),
                    "ineligible_reason": ("" if int(r["n"]) >= int(floor_n)
                                          else f"n {int(r['n'])} < floor {int(floor_n)}"),
                    "on_disk_pins": bool(float(margin) == float(RETEST_DEFAULT["margin_atr"])
                                         and int(hold) == int(RETEST_DEFAULT["hold_bars"])),
                    "band_tie_break_rank": BAND_TIE_BREAK.index(bname),
                    "objective_law": TUNE_OBJECTIVE, "tie_break_law": TUNE_TIE_BREAK,
                    "era_boundary": ERA_BOUNDARY_ISO,
                    "tuning_assets": ",".join(sorted(cut)),
                    "n_tuning_assets": len(cut),
                })
    grid = canon(pd.DataFrame(rows), TUNING_GRID_KEY)
    gsha = content_sha(grid)
    elig = grid[grid["eligible"]]
    if not len(elig):
        res = {"lens": lens, "band": None, "margin_atr": None, "hold_bars": None,
               "ttl_bars": ttl, "n": 0, "objective": None,
               "selected": False, "floor_n": int(floor_n),
               "reason": (f"NO cell of the whole {len(grid)}-cell grid reaches the "
                          f"floor n >= {floor_n} on the {lens} lens"),
               "objective_law": TUNE_OBJECTIVE, "tie_break_law": TUNE_TIE_BREAK,
               "era_boundary": ERA_BOUNDARY_ISO, "grid_sha": gsha,
               "tuning_assets": sorted(cut), "n_cells": int(len(grid)),
               "n_eligible": 0}
        return grid, res
    order = elig.assign(_neg=-elig["objective_net_h20"].round(ROUND_ND),
                        _disk=(~elig["on_disk_pins"]).astype(int),
                        _band=elig["band_tie_break_rank"],
                        _m=elig["margin_atr"], _h=elig["hold_bars"])
    order = order.sort_values(["_neg", "_disk", "_band", "_m", "_h"], kind="mergesort")
    w = order.iloc[0]
    res = {"lens": lens, "band": str(w["band"]), "band_label": str(w["band_label"]),
           "cls": str(w["cls"]), "margin_atr": float(w["margin_atr"]),
           "hold_bars": int(w["hold_bars"]), "ttl_bars": ttl, "n": int(w["n"]),
           "objective": float(w["objective_net_h20"]),
           "median_term": float(w["median_term"]), "toll_atr": float(w["toll_atr"]),
           "selected": True, "floor_n": int(floor_n),
           "reason": "the eligible cell with the highest objective under the tie-break",
           "objective_law": TUNE_OBJECTIVE, "tie_break_law": TUNE_TIE_BREAK,
           "era_boundary": ERA_BOUNDARY_ISO, "grid_sha": gsha,
           "tuning_assets": sorted(cut), "n_cells": int(len(grid)),
           "n_eligible": int(len(elig)),
           "n_ties_on_objective": int((order["_neg"] == order["_neg"].iloc[0]).sum())}
    return grid, res


def tuning_md(grid: pd.DataFrame, res: dict, skipped: list, lens: str) -> str:
    """The whole grid as text — INELIGIBLE CELLS INCLUDED [F-GRID]."""
    out = [f"# TIER-C10 · CENSUS-R · R1 HOLD-PIN TUNING GRID — {lens} lens",
           "", f"TIER: {TIER}", f"GATES: {GATES}", "",
           "PROTOCOL (fixed BEFORE the look, OPERATOR_RULINGS.md R1):",
           f"- grid: {len(RETEST_BANDS)} bands x margin_atr {list(TUNE_MARGINS)} x "
           f"hold_bars {list(TUNE_HOLDS)} = {len(grid)} cells, WHOLE",
           f"- objective: {TUNE_OBJECTIVE}", f"- floor: n >= {res['floor_n']}",
           f"- tie-break: {TUNE_TIE_BREAK}", f"- era: {ERA_LAW}",
           f"- tuning assets ({res['n_tuning_assets'] if 'n_tuning_assets' in res else len(res['tuning_assets'])}): "
           + ", ".join(res["tuning_assets"]), ""]
    if skipped:
        out += ["SKIPPED (no tuning-era tape on this lens):"]
        out += [f"- {s['asset']}: {s['tuning_era_bars']} bars — {s['reason']}" for s in skipped]
        out += [""]
    out += ["| band | margin_atr | hold_bars | n | median term | toll | NET H20 | hit | "
            "assets | eligible |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r in grid.itertuples():
        out.append(f"| {r.band} | {r.margin_atr:g} | {r.hold_bars} | {r.n} | "
                   f"{r.median_term:.4f} | {r.toll_atr:.4f} | {r.objective_net_h20:.4f} | "
                   f"{r.hit_rate:.3f} | {r.n_assets_with_events} | "
                   f"{'yes' if r.eligible else 'NO — ' + r.ineligible_reason} |")
    out += ["", "## RESULT", "```json", json.dumps(res, indent=2, sort_keys=True), "```",
            "", f"WARRANTY: {WARRANTY}", "", COLLAR_5M_RETEST]
    return "\n".join(out) + "\n"


def run_tuning(root: Path, assets: list, lens: str) -> dict:
    """Tune, file TUNING_GRID{.parquet,.md} + TUNING_RESULT{...}.json, print."""
    floor = TUNE_FLOOR_N[lens]
    cut, skipped = tuning_tapes(assets, lens)
    if not cut:
        raise SystemExit(f"HALT: no asset has {TUNE_MIN_BARS}+ tuning-era {lens} bars")
    log(f"\n  R1 TUNING · {lens} lens · TUNING ERA ONLY (<= {ERA_BOUNDARY_ISO}) · "
        f"FROZEN SCALE {float(FROZEN_SCALE):g} · floor n >= {floor}")
    log(f"    objective: {TUNE_OBJECTIVE}")
    log(f"    tie-break: {TUNE_TIE_BREAK}")
    for sym in sorted(cut):
        log(f"      {sym:>16} {lens:>3}  tuning-era bars {cut[sym].n:>8,}  "
            f"(cut at {iso(int(cut[sym].t0[-1] + cut[sym].step))})")
    for s in skipped:
        log(f"      {s['asset']:>16} {lens:>3}  SKIPPED — {s['reason']} "
            f"({s['tuning_era_bars']} bars)")
    grid, res = tune(cut, lens, floor)
    res["n_tuning_assets"] = len(cut)
    res["skipped"] = skipped
    # the tuning grid is a FILED table of the census root, so it wears the same
    # collar and the same as-of stamps as every other one [F-KEY totality] —
    # with its OWN edge: the last TUNING-ERA bar, not the tape's last bar
    metas = [cut[s_].meta for s_ in sorted(cut)]
    grid = stamp(collar(grid, f"CENSUS-R R1 hold-pin tuning grid, {lens}"), metas, lens,
                 f"TUNING:{len(cut)} of PANEL17")
    grid["as_of_last_closed_bar"] = iso(max(int(t.t0[-1]) + t.step for t in cut.values()))
    grid["in_sample"] = ("IN-SAMPLE BY CONSTRUCTION: the hold pins are FITTED on these "
                         "rows (tuning era only); the holdout era is where they are judged")
    # the sha of record is the FILED frame's — collar and stamps included, so a
    # reader who opens the parquet can hash what is in front of them
    res["grid_sha_unstamped"] = res["grid_sha"]
    res["grid_sha"] = content_sha(grid)
    root.mkdir(parents=True, exist_ok=True)
    gp = root / f"{TUNING_GRID_NAME[lens]}.parquet"
    grid.to_parquet(gp, index=False)
    (root / f"{TUNING_GRID_NAME[lens]}.md").write_text(tuning_md(grid, res, skipped, lens))
    _dump(res, root / TUNING_RESULT_NAME[lens])
    log(f"\n    THE WHOLE GRID ({len(grid)} cells; ineligible cells PRINTED)")
    log(f"      {'band':>14} {'marg':>5} {'hold':>4} {'n':>7} {'medTerm':>9} {'toll':>7} "
        f"{'NET20':>9} {'hit':>6} {'assets':>6}  eligible")
    for r in grid.itertuples():
        log(f"      {r.band:>14} {r.margin_atr:>5.2f} {r.hold_bars:>4} {r.n:>7,} "
            f"{r.median_term:>9.4f} {r.toll_atr:>7.4f} {r.objective_net_h20:>9.4f} "
            f"{r.hit_rate:>6.3f} {r.n_assets_with_events:>6}  "
            f"{'yes' if r.eligible else 'NO  ' + r.ineligible_reason}")
    if res["selected"]:
        log(f"\n    RESULT [{lens}]: band {res['band']} · margin_atr {res['margin_atr']:g} · "
            f"hold_bars {res['hold_bars']} · n {res['n']:,} · objective "
            f"{res['objective']:.6f} ATR · {res['n_eligible']} of {res['n_cells']} cells "
            f"eligible · grid sha {res['grid_sha'][:16]}")
    else:
        log(f"\n    RESULT [{lens}]: NO CELL REACHES THE FLOOR — {res['reason']}. "
            "The Tier-E print falls back to the 5m-selected pins.")
    log(f"    filed -> {gp.name} · {TUNING_GRID_NAME[lens]}.md · {TUNING_RESULT_NAME[lens]}")
    return res


def census_events(tape: Tape, macro: dict, leash: list, view: dict,
                  bands=RETEST_BANDS, retest: dict | None = None
                  ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(events, hold_tally).  events: one row per class event — cls, i (the
    STAMP bar), known_at (the ANCHOR bar), rid, side, sgn — and nothing that is
    not knowable at known_at.  hold_tally: per hold anchor, how the one-shot
    evaluations ended (whole-tape counts, report-only)."""
    rp = dict(RETEST_PINS if retest is None else retest)
    hold = int(RC.PINS_V2["FLIP_HOLD_BARS"])
    rows: list[dict] = []
    die_side: dict = {}
    dies: list = []
    up = {"top": 1, "bottom": -1}
    for e in macro["events"]:
        k = e["event"]
        if k == "breach-open":
            rows.append({"cls": "breach", "i": e["i"], "known_at": e["i"],
                         "rid": e["rid"], "side": e["side"], "sgn": up[e["side"]]})
        elif k == "harden":
            rows.append({"cls": "harden", "i": e["i"], "known_at": e["i"],
                         "rid": e["rid"], "side": e["side"], "sgn": -up[e["side"]]})
        elif k == "breakout-die":
            die_side[e["rid"]] = e["side"]
            dies.append((e["i"], e["rid"], e["side"]))
            rows.append({"cls": "DIE", "i": e["i"], "known_at": e["i"],
                         "rid": e["rid"], "side": e["side"], "sgn": up[e["side"]]})
    for e in macro["events"]:
        if e["event"] == "memory-touch":
            rows.append({"cls": "memory-touch-v1", "i": e["i"], "known_at": e["i"],
                         "rid": e["rid"], "side": e["side"],
                         "sgn": up[die_side[e["rid"]]]})
    lf = view["_leash_frame"]
    seen: set = set()
    tally = []
    ft = {"hold": 0, "failed": 0, "truncated": 0}
    for e in lf.itertuples():
        key = (e.rid, e.side)
        if e.event != "line-expired" and key not in seen:
            seen.add(key)               # the first TWO-SIDED touch of this line
            rows.append({"cls": "memory-touch-2s", "i": e.i, "known_at": e.i,
                         "rid": e.rid, "side": e.side, "sgn": up[die_side[e.rid]]})
        if e.event == "flip":
            ft["hold"] += 1
            rows.append({"cls": "flip-hold", "i": e.i, "known_at": e.i + hold,
                         "rid": e.rid, "side": e.side, "sgn": up[e.side]})
        elif e.verdict.startswith("failed through"):
            ft["failed"] += 1
        elif e.verdict.startswith("hold window truncated"):
            ft["truncated"] += 1
    n_lines = 2 * len(dies)
    tally.append({"anchor": "memory-line", "band": "dead macro boundary (the leash)",
                  "pins_status": FROZEN_PINS, "n_candidates": n_lines,
                  "n_evaluated": sum(ft.values()), "n_hold": ft["hold"],
                  "n_failed": ft["failed"], "n_truncated": ft["truncated"],
                  "n_not_evaluated": n_lines - sum(ft.values()),
                  "margin_atr": float(RC.PINS_V2["FLIP_HOLD_MARGIN"]),
                  "hold_bars": hold, "ttl_bars": int(RC.PINS_V2["MEM_TTL_BARS"])})
    for name, band in bands:
        lo, hi = band(tape.c)
        got = retest_holds(tape, dies, lo, hi, float(rp["margin_atr"]),
                           int(rp["hold_bars"]), int(rp["ttl_bars"]))
        for g in got:
            if g["verdict"] == "hold":
                rows.append({"cls": f"retest-hold-{name}", "i": g["touch_i"],
                             "known_at": g["known_at"], "rid": g["rid"],
                             "side": g["side"], "sgn": up[g["side"]]})
        v = [g["verdict"] for g in got]
        tally.append({"anchor": name, "band": band.label, "pins_status": rp["status"],
                      "n_candidates": len(dies), "n_evaluated": len(got),
                      "n_hold": v.count("hold"), "n_failed": v.count("failed"),
                      "n_truncated": v.count("truncated"),
                      "n_not_evaluated": len(dies) - len(got),
                      "margin_atr": float(rp["margin_atr"]),
                      "hold_bars": int(rp["hold_bars"]), "ttl_bars": int(rp["ttl_bars"])})
    cols = ["cls", "i", "known_at", "rid", "side", "sgn"]
    evf = (pd.DataFrame(rows, columns=cols) if rows
           else pd.DataFrame({k: pd.Series(dtype=(object if k in ("cls", "side") else np.int64))
                              for k in cols}))
    for k in ("i", "known_at", "rid", "sgn"):
        evf[k] = evf[k].astype(np.int64)
    evf = evf.sort_values(["cls", "known_at", "rid", "side"], kind="mergesort")
    return evf.reset_index(drop=True), pd.DataFrame(tally)


# ═══════════════════════════════════════════════ 5 · OUTCOMES, NET OF THE TOLL
def outcome_ledger(tape: Tape, evf: pd.DataFrame, view: dict, bps: float) -> pd.DataFrame:
    """One row per event: term / MFE / MAE in ATR at every horizon, measured
    from the CLOSE of the known_at bar k [L4]:
        term = sgn * (c[k+H] - c[k]) / atr[k]
        MFE / MAE = the favourable / adverse extreme of bars k+1..k+H, both as
                    positive excursions (census-2A's arithmetic; its horizon
                    law is NOT used)
    CENSORED when k + H > n - 1 — the horizon is never shortened to fit the
    tape.  toll_atr_evt = (bps / 10 000) * c[k] / atr[k], the round trip in
    this anchor's own ATR units.  The as-of stamps AT the anchor ride beside
    (captured, not consulted)."""
    n, c, atr = tape.n, tape.c, tape.atr
    k = evf["known_at"].to_numpy(np.int64)
    sg = evf["sgn"].to_numpy(float)
    out = evf.copy()
    inside = k <= n - 1
    ks = np.where(inside, k, 0)
    ok_atr = inside & (atr[ks] > 0)
    out["known_close_ms"] = np.where(inside, tape.t0[ks] + tape.step, -1)
    out["bad_atr"] = ~ok_atr
    with np.errstate(invalid="ignore", divide="ignore"):
        out["toll_atr_evt"] = np.where(ok_atr, (bps / BPS_PER_UNIT) * c[ks] / atr[ks], np.nan)
    hi_s, lo_s = pd.Series(tape.h), pd.Series(tape.l)
    for name, H in HORIZONS:
        live = ok_atr & (k + H <= n - 1)
        e = np.where(live, k + H, 0)
        f_hi = hi_s.rolling(H).max().to_numpy()[e]      # max h[k+1..k+H]
        f_lo = lo_s.rolling(H).min().to_numpy()[e]
        with np.errstate(invalid="ignore", divide="ignore"):
            term = sg * (c[e] - c[ks]) / atr[ks]
            mfe = np.where(sg > 0, f_hi - c[ks], c[ks] - f_lo) / atr[ks]
            mae = np.where(sg > 0, c[ks] - f_lo, f_hi - c[ks]) / atr[ks]
        out[f"cens_{name}"] = ~live
        out[f"term_{name}"] = np.where(live, term, np.nan)
        out[f"mfe_{name}"] = np.where(live, mfe, np.nan)
        out[f"mae_{name}"] = np.where(live, mae, np.nan)
    out["era"] = era_of(out["known_close_ms"])          # [ERA_LAW] the ANCHOR's era
    out["state_at"] = view["state"][ks]
    out["in_range_at"] = view["in_range"][ks]
    out["pct_at"] = view["pct"][ks]
    out["dist_atr_at"] = view["dist_atr"][ks]
    out["flip_pol_at"] = view["flip_pol"][ks]
    return out


LEDGER_KEY = ["asset", "lens", "scale_kind", "cls", "rid", "side", "i"]
POOL_COLUMNS = (["asset", "lens", "scale_kind", "cls", "era", "bad_atr", "toll_atr_evt"]
                + [f"{x}_{hn}" for hn, _ in HORIZONS for x in ("cens", "term", "mfe", "mae")])
GRID_KEY = ["asset", "lens", "cls", "scale_kind", "era", "horizon"]


def grid_rows(led: pd.DataFrame, asset: str, lens: str, scale_kind: str,
              scale_mult: float, bps: float, bps_source: str,
              tolls: pd.DataFrame | None = None, pins: dict | None = None) -> list[dict]:
    """The outcome rows of ONE (asset | pool, lens, scale_kind): every class x
    every ERA x every horizon, WHOLE — a class with no event still gets its
    rows, NaN, with the reason.  `led` is the FILED (rounded) ledger, so a row
    is an exact function of bytes a reader can open.  `tolls` = the per-asset
    rows when this is a POOLED row: the toll quoted is then the BINDING (max)
    one.  ERA 'ALL' is the contract's full-history row; 'tuning' / 'holdout'
    ride beside it [R1, ERA_LAW] and are never its addends."""
    rows = []
    pooled = tolls is not None
    rp = dict(RETEST_PINS if pins is None else pins)
    pin_text = (f"margin {float(rp['margin_atr']):g} ATR / hold {int(rp['hold_bars'])} "
                f"bars / ttl {int(rp['ttl_bars'])} [{rp['status']}]")
    era_col = (led["era"] if "era" in led.columns
               else pd.Series([ERA_HOLDOUT] * len(led), index=led.index))
    for cls in CLASSES:
        is_retest = cls in RETEST_CLASSES
        C_ = led[led["cls"] == cls]
        e_c = era_col[led["cls"] == cls]
        for era in ERAS:
            L = C_ if era == ERA_ALL else C_[e_c == era]
            ok = L[~L["bad_atr"]] if len(L) else L
            for name, H in HORIZONS:
                S = ok[~ok[f"cens_{name}"]] if len(ok) else ok
                t = S[f"term_{name}"] if len(S) else pd.Series(dtype=float)
                nn = int(len(t))
                r = {"asset": asset, "lens": lens, "cls": cls, "scale_kind": scale_kind,
                     "era": era, "horizon": name, "horizon_bars": H,
                     "horizon_unit": "bars of the lens", "era_law": ERA_LAW,
                     "scale_mult": float(scale_mult), "pins_status": PINS_STATUS[cls],
                     "retest_pins": pin_text if is_retest else "n/a — not a retest class",
                     "printable": bool(printable(lens, cls, era)),
                     "pooled": pooled, "n_events": int(len(L)), "n": nn,
                     "n_censored": int(len(ok) - nn), "n_bad_atr": int(len(L) - len(ok))}
                # the class's toll over ALL its anchors does not wait for a horizon:
                # it is measurable the moment one anchor exists, censored or not
                if pooled:
                    Ta = tolls[(tolls["cls"] == cls) & (tolls["era"] == era)
                               & (tolls["horizon"] == name)]["toll_atr_all"]
                    r["toll_atr_all"] = float(Ta.max()) if Ta.notna().any() else _NAN
                else:
                    r["toll_atr_all"] = float(ok["toll_atr_evt"].median()) if len(ok) else _NAN
                if nn:
                    own = float(S["toll_atr_evt"].median())
                    r.update({
                        "median_term": float(t.median()), "mean_term": float(t.mean()),
                        "q25_term": float(t.quantile(0.25)), "q75_term": float(t.quantile(0.75)),
                        "hit_rate": float((t > 0).mean()),
                        "hit_rate_net": float((t - S["toll_atr_evt"] > 0).mean()),
                        "median_mfe": float(S[f"mfe_{name}"].median()),
                        "median_mae": float(S[f"mae_{name}"].median())})
                    if pooled:
                        T = tolls[(tolls["cls"] == cls) & (tolls["era"] == era)
                                  & (tolls["horizon"] == name) & (tolls["n"] > 0)]
                        r["toll_atr"] = float(T["toll_atr"].max())
                        r["binding_over_n_assets"] = int(len(T))
                        r["toll_pooling"] = ("BINDING: the max of the pooled assets' own "
                                             "toll_atr (a pooled median would be one "
                                             "asset's number under a pooled label)")
                    else:
                        r["toll_atr"] = own
                        r["binding_over_n_assets"] = 1
                        r["toll_pooling"] = "median over this row's own uncensored anchors"
                    # NET is struck on the FILED figures — numpy's rounding, the one
                    # canon() files with (a median of an even count is a half-unit
                    # tie, and Python's round breaks it the other way) — so the
                    # identity NET = median - toll_atr holds on the row a reader opens
                    r["net"] = float(np.round(r["median_term"], ROUND_ND)
                                     - np.round(r["toll_atr"], ROUND_ND))
                    r["nan_reason"] = ""
                else:
                    for col in STAT_COLS:
                        r[col] = _NAN
                    r["binding_over_n_assets"] = 0
                    r["toll_pooling"] = ""
                    r["nan_reason"] = (
                        ("no event of this class in this era on any pooled tape" if pooled
                         else "no event of this class in this era on this tape")
                        if not len(L) else
                        f"all {len(L)} anchors censored (k + {H} > n - 1) or on a zero ATR")
                r["provisional"] = bool(nn < PROVISIONAL_MIN_N)
                r["toll_bps"] = float(bps) if bps is not None else _NAN
                r["toll_bps_source"] = bps_source
                r["sign_law"] = SIGN_LAW[cls]
                r["anchor_law"] = ANCHOR_LAW[cls]
                rows.append(r)
    return rows


STAT_COLS = ("median_term", "mean_term", "q25_term", "q75_term", "hit_rate",
             "hit_rate_net", "median_mfe", "median_mae", "toll_atr", "net")
# NaN exactly when n = 0.  toll_atr_all rides OUTSIDE this law: it is NaN
# exactly when the class has no anchor at all (n_events - n_bad_atr = 0).


# ═══════════════════════════════════════════════ F-RF-4 · spring overlap
def spring_overlap(tape: Tape, macro: dict, view: dict, look: int = SPRING_LOOK) -> list[dict]:
    """F-RF-4's kinship, parametrised off the BTC-1D globals and MIRRORED: per
    side (bottom = springs, top = upthrusts),
      law        hardens that sweep the boundary they breached and close back
                 inside it (definitional — the content is the reclaim close);
                 the boundary is the AS-OF one at the breach bar, never the
                 2-dp event field;
      (a)        of those hardens, how many ALSO sweep the prior `look`-bar
                 wick extreme and close back beyond it (the house spring scan);
      (b)        of the house springs / upthrusts found on the raw tape, how
                 many fall INSIDE a deviation episode [breach-open, harden]."""
    h, l, c, n = tape.h, tape.l, tape.c, tape.n
    lo_prior = pd.Series(l).rolling(look).min().shift(1).to_numpy()
    hi_prior = pd.Series(h).rolling(look).max().shift(1).to_numpy()
    with np.errstate(invalid="ignore"):
        springs = np.nonzero((l < lo_prior) & (c > lo_prior))[0]
        upthrusts = np.nonzero((h > hi_prior) & (c < hi_prior))[0]
    opens: dict = {}
    eps = {"bottom": [], "top": []}
    for e in macro["events"]:
        if e["event"] == "breach-open":
            opens[(e["rid"], e["side"])] = e["i"]
        elif e["event"] == "harden":
            eps[e["side"]].append((opens[(e["rid"], e["side"])], e["i"]))
    rows = []
    for side, scan in (("bottom", springs), ("top", upthrusts)):
        law = also = 0
        for b, i in eps[side]:
            if side == "bottom":
                bnd, ext = view["bot"][b], float(l[b:i + 1].min())
                law += int(ext < bnd and c[i] >= bnd)
                prior = float(l[max(0, b - look):b].min()) if b > 0 else _NAN
                also += int(ext < prior and c[i] > prior)
            else:
                bnd, ext = view["top"][b], float(h[b:i + 1].max())
                law += int(ext > bnd and c[i] <= bnd)
                prior = float(h[max(0, b - look):b].max()) if b > 0 else _NAN
                also += int(ext > prior and c[i] < prior)
        inside = np.zeros(n + 1, dtype=np.int64)
        for b, i in eps[side]:
            inside[b] += 1
            inside[i + 1] -= 1
        in_ep = np.cumsum(inside)[:n] > 0
        rows.append({"side": side, "shape": "spring" if side == "bottom" else "upthrust",
                     "look_bars": look, "n_hardens": len(eps[side]), "n_law_reclaim": law,
                     "n_hardens_also_sweep_look": also, "n_house_shapes": int(len(scan)),
                     "n_house_shapes_inside_episode": int(in_ep[scan].sum())})
    return rows


# ═══════════════════════════════════════════════ stamps + collar
def stamp(df: pd.DataFrame, metas: list[dict], lens: str, panel: str) -> pd.DataFrame:
    """THE WARRANTY, lens-aware, in COLUMNS [TC6V-a] — the four tierc8.stamp
    names F-KEY demands AND the lens-aware five, under the panel module's own
    names.  `metas` = the tape meta of every asset the row was built from.

    WHAT WOULD MAKE THIS WRONG: stamping a 5m or 1d row with the 4h edge only,
    or stamping the wall clock."""
    d = df.copy()
    d["as_of_last_closed_4h"] = metas[0]["as_of_last_closed_4h"]
    d["as_of_panel_start"] = iso(min(m["first_bar_open_ms"] for m in metas))
    d["as_of_span_days"] = max(m["span_days"] for m in metas)
    d["warranty"] = WARRANTY
    d["as_of_lens"] = lens
    d["as_of_last_closed_bar"] = iso(max(m["last_bar_open_ms"] for m in metas)
                                     + LENS_MS[lens])
    d["as_of_panel"] = panel
    d["as_of_n_assets"] = len(metas)
    d["as_of_substrate"] = SNAPSHOT.name
    return d


def collar(df: pd.DataFrame, surface: str) -> pd.DataFrame:
    """THE TIER-E COLLAR, in columns: a caption does not survive a copy of the
    row.  m = the number of LOOKS this table holds — logged, not corrected:
    nothing here is a test, there is no verdict column and no bar.  in_sample
    is said PER ROW: a calibrated-SCALE row is in-sample by construction."""
    d = df.copy()
    m_here = int(len(d))
    d["tier"] = TIER
    d["gates"] = GATES
    d["m_looks_this_table"] = m_here
    d["m_note"] = (f"m = {m_here} looks in this table ({surface}). NO multiplicity "
                   "correction is applied and none is needed: NOTHING HERE IS A TEST. "
                   "m is logged so a reader who later turns a cell into a claim can "
                   "see how many ways the tape was cut first.")
    d["in_sample"] = (d["scale_kind"].map(IN_SAMPLE) if "scale_kind" in d.columns
                      else IN_SAMPLE["calibrated"] if "chosen" in d.columns
                      else "n/a — text")
    return d


IN_SAMPLE = {
    "frozen3.0": "full history, frozen pins: descriptive of THIS tape; pins were "
                 "calibrated on BTC only",
    "calibrated": "IN-SAMPLE BY CONSTRUCTION: SCALE fitted on this whole tape; no "
                  "registered lane and no Stage-A stamp may read it [L2]",
}


# ═══════════════════════════════════════════════ 6 · ONE CELL
CELL_TABLES = {
    "events": LEDGER_KEY,
    "grid": GRID_KEY,
    "coverage": ["asset", "lens", "scale_kind"],
    "scale_grid": ["asset", "lens", "scale_mult"],
    "spring_overlap": ["asset", "lens", "scale_kind", "side"],
    "hold_tally": ["asset", "lens", "scale_kind", "anchor"],
}


def compute_cell(tape: Tape, kinds: tuple = SCALE_KINDS, timing: dict | None = None) -> dict:
    """Everything one (asset, lens) cell files, as frames — no IO."""
    tm = {} if timing is None else timing
    sym, lens = tape.sym, tape.lens
    bps, bps_src = toll_bps_for(sym)
    t0 = time.perf_counter()
    pick, sgrid = calibrate(tape)
    tm["calibrate_11_scales_s"] = time.perf_counter() - t0
    scale_of = {"frozen3.0": float(FROZEN_SCALE), "calibrated": float(pick)}
    ev_all, grid_all, cov, spr, tal = [], [], [], [], []
    done: dict = {}
    for kind in kinds:
        s = scale_of[kind]
        if s not in done:
            t1 = time.perf_counter()
            v2 = run_scale(tape, s)
            tm[f"machine+leash@{s}_s"] = time.perf_counter() - t1
            t1 = time.perf_counter()
            view = asof_view(tape, v2["macro"], v2["leash"])
            tm[f"asof@{s}_s"] = time.perf_counter() - t1
            t1 = time.perf_counter()
            evf, tally = census_events(tape, v2["macro"], v2["leash"], view)
            led = outcome_ledger(tape, evf, view, bps)
            tm[f"events+outcomes@{s}_s"] = time.perf_counter() - t1
            done[s] = (v2, view, led, tally)
        v2, view, led, tally = done[s]
        m = v2["macro"]
        led = led.assign(asset=sym, lens=lens, scale_kind=kind, scale_mult=s,
                         pins_status=led["cls"].map(PINS_STATUS))
        led = canon(led, LEDGER_KEY)
        ev_all.append(led)
        grid_all += grid_rows(led, sym, lens, kind, s, bps, bps_src)
        n_die = int((led["cls"] == "DIE").sum())
        cov.append({
            "asset": sym, "lens": lens, "scale_kind": kind, "scale_mult": s,
            "n_bars": int(m["n_bars"]), "coverage_pct": float(m["coverage_pct"]),
            "n_confirmed": int(m["n_confirmed"]),
            "density_per_100": density_per_100(m),
            "mean_confirmed_lifetime": (_NAN if m["mean_confirmed_lifetime"] is None
                                        else float(m["mean_confirmed_lifetime"])),
            "n_lifetime_censored": int(m["n_lifetime_censored"]),
            "n_died": n_die, "n_pivots": int(m["n_pivots"]),
            "n_flips": int(len(v2["flips"])),
            "bars_in_live_range_pct": 100.0 * float(view["in_range"].mean()),
            "final_state": m["final_state"],
            "gap_count": tape.meta["gap_count"],
            "missing_bars_total": tape.meta["missing_bars_total"],
            "coverage_law": "close inside the alive CONFIRMED macro range's span "
                            "(boundaries + deviation zones), % of ALL bars",
            "lifetime_law": "mean(die_i - confirm_i) over confirmed ranges that DIED; "
                            "still-alive ones excluded and counted beside"})
        spr += [dict(r, asset=sym, lens=lens, scale_kind=kind, scale_mult=s)
                for r in spring_overlap(tape, m, view)]
        tal += [dict(r, asset=sym, lens=lens, scale_kind=kind, scale_mult=s)
                for r in tally.to_dict("records")]
    metas = [tape.meta]
    frames = {
        "events": pd.concat(ev_all, ignore_index=True),
        "grid": pd.DataFrame(grid_all),
        "coverage": pd.DataFrame(cov),
        "scale_grid": sgrid,
        "spring_overlap": pd.DataFrame(spr),
        "hold_tally": pd.DataFrame(tal),
    }
    out = {}
    for name, df in frames.items():
        out[name] = stamp(collar(df, f"CENSUS-R {name}, {sym} {lens}"),
                          metas, lens, f"ASSET:{sym}")
    return {"frames": out, "calibrated_scale": float(pick), "toll_bps": bps,
            "toll_bps_source": bps_src}


def cell_dir(root: Path, sym: str, lens: str) -> Path:
    return root / "cells" / f"{sym}__{lens}"


def cell_is_current(root: Path, sym: str, lens: str, kinds: tuple, code: str) -> tuple[bool, str]:
    """RESUME LAW.  A cell is reused only if its receipt says COMPLETE, under
    THIS code sha, THESE pins, THIS as-of, the SAME input file bytes, at least
    the asked scale kinds — and every table it lists is on disk with the
    content sha it recorded.  Anything else is recomputed."""
    cd = cell_dir(root, sym, lens)
    p = cd / "cell.json"
    if not p.exists():
        return False, "no receipt"
    try:
        rc = json.loads(p.read_text())
    except json.JSONDecodeError:
        return False, "unreadable receipt"
    if not rc.get("complete"):
        return False, "receipt not complete"
    if rc.get("code_sha") != code:
        return False, "code sha moved"
    if rc.get("pins") != _pins_block():
        return False, "pins moved"
    if not set(kinds) <= set(rc.get("scale_kinds", [])):
        return False, "scale kinds not covered"
    if rc.get("as_of_close_ms") != as_of_close_ms(sym)[0]:
        return False, "as-of moved"
    src = cache_dir() / rc["tape"]["source_file"]
    if not src.exists() or file_sha256(src) != rc["tape"]["source_sha256"]:
        return False, "input bytes moved"
    for name, t in rc["tables"].items():
        q = cd / f"{name}.parquet"
        if not q.exists() or content_sha(pd.read_parquet(q)) != t["sha"]:
            return False, f"table {name} missing or moved"
    return True, "current"


def _pins_block() -> dict:
    return {"PINS": dict(RC.PINS), "PINS_V2": dict(RC.PINS_V2),
            "ATR_LEN": RC.ATR_LEN, "MEM_CAP_PER_SIDE": RC.MEM_CAP_PER_SIDE,
            "SCALE_GRID": list(SCALE_GRID), "DENSITY_TARGET_PER_100": DENSITY_TARGET_PER_100,
            "HORIZONS": [list(x) for x in HORIZONS], "SPRING_LOOK": SPRING_LOOK,
            "RETEST_PINS": {k: v for k, v in RETEST_PINS.items()},
            "RETEST_BANDS": [[n_, b.label] for n_, b in RETEST_BANDS],
            "ERA_BOUNDARY_MS": ERA_BOUNDARY_MS, "ERAS": list(ERAS)}


def run_cell(root: Path, sym: str, lens: str, kinds: tuple = SCALE_KINDS,
             force: bool = False) -> dict:
    """Compute-or-reuse one cell; returns its receipt."""
    code = code_sha()
    cd = cell_dir(root, sym, lens)
    if not force:
        ok, why = cell_is_current(root, sym, lens, kinds, code)
        if ok:
            log(f"  {sym:>16} {lens:>3}  REUSED (receipt current)")
            return json.loads((cd / "cell.json").read_text())
        if (cd / "cell.json").exists():
            log(f"  {sym:>16} {lens:>3}  recomputing: {why}")
    t0 = time.perf_counter()
    tape = load_tape(sym, lens)
    res = compute_cell(tape, kinds)
    (cd / "cell.json").unlink(missing_ok=True)     # no receipt while tables move
    tables = {}
    for name, df in res["frames"].items():
        tables[name] = {"sha": write_table(df, name, CELL_TABLES[name], cd),
                        "rows": int(len(df)), "key": CELL_TABLES[name]}
    rc = {"asset": sym, "lens": lens, "complete": True, "seed": SEED,
          "code_sha": code, "pins": _pins_block(), "scale_kinds": list(kinds),
          "calibrated_scale": res["calibrated_scale"],
          "toll_bps": res["toll_bps"], "toll_bps_source": res["toll_bps_source"],
          "as_of_close_ms": tape.meta["as_of_close_ms"],
          "as_of_last_closed_4h": tape.meta["as_of_last_closed_4h"],
          "tape": tape.meta, "tables": tables}
    _dump(rc, cd / "cell.json")
    g = res["frames"]["coverage"]
    log(f"  {sym:>16} {lens:>3}  n={tape.n:>7,}  " + "  ".join(
        f"{r.scale_kind}@{r.scale_mult:g}: cov {r.coverage_pct:5.2f}% dens "
        f"{r.density_per_100:.3f}/100 life {r.mean_confirmed_lifetime:6.1f}"
        for r in g.itertuples()) + f"  events {tables['events']['rows']:,}")
    clock(f"{sym} {lens}: {time.perf_counter() - t0:.2f}s")
    return rc


# ═══════════════════════════════════════════════ 7 · THE MERGE
ROOT_TABLES = {
    "outcome_grid": GRID_KEY,
    "coverage": CELL_TABLES["coverage"],
    "scale_grid": CELL_TABLES["scale_grid"],
    "spring_overlap": CELL_TABLES["spring_overlap"],
    "hold_tally": CELL_TABLES["hold_tally"],
    "leans": ["lean"],
}


def declared_cells(assets: list, lenses: list, kinds: tuple, pooled: bool = True) -> list:
    """THE COMMISSION, as a list of grid keys — F-GRID holds the filed grid to
    it (the fixture builds its own from its own literals)."""
    names = list(assets) + (list(pools_for(assets)) if pooled else [])
    return [(a, l, c, k, e, hn) for a in names for l in lenses for c in CLASSES
            for k in kinds for e in ERAS for hn, _ in HORIZONS]


def merge(root: Path, assets: list, lenses: list, kinds: tuple, label: str) -> dict:
    """Per-cell artifacts -> the root tables.  HALTS IF a commissioned cell
    has no current receipt (a grid is filed WHOLE or not at all).  POOLED
    rows — POOLED:ALL and the [L6] sub-pools beside it (pools_for) — are
    computed from the filed per-cell ledgers of THAT pool's members — true
    pooled medians — and quote the BINDING toll over those members."""
    code = code_sha()
    receipts, parts = {}, {k: [] for k in CELL_TABLES}
    for sym in assets:
        for lens in lenses:
            ok, why = cell_is_current(root, sym, lens, kinds, code)
            if not ok:
                raise SystemExit(f"HALT: cell {sym} {lens} is not current ({why}) — "
                                 "the grid is filed whole or not at all")
            cd = cell_dir(root, sym, lens)
            receipts[f"{sym}__{lens}"] = json.loads((cd / "cell.json").read_text())
            for name in CELL_TABLES:
                # the ledger is read NARROW: a 5m cell carries ~10^5 rows and the
                # collar's text columns are not what a pooled median needs
                d = pd.read_parquet(cd / f"{name}.parquet",
                                    columns=POOL_COLUMNS if name == "events" else None)
                if "scale_kind" in d.columns:
                    d = d[d["scale_kind"].isin(kinds)]
                parts[name].append(d)
    grid = pd.concat(parts["grid"], ignore_index=True)
    pools = pools_for(assets)
    pooled = []
    for lens in lenses:
        for kind in kinds:
            led_k = pd.concat([d[(d["lens"] == lens) & (d["scale_kind"] == kind)]
                               for d in parts["events"]], ignore_index=True)
            tolls_k = grid[(grid["lens"] == lens) & (grid["scale_kind"] == kind)]
            for pool, members in pools.items():
                metas = [receipts[f"{s}__{lens}"]["tape"] for s in members]
                led = led_k[led_k["asset"].isin(members)]
                tolls = tolls_k[tolls_k["asset"].isin(members)]
                scales = sorted(set(tolls["scale_mult"]))
                rows = grid_rows(led, pool, lens, kind,
                                 scales[0] if len(scales) == 1 else _NAN, None,
                                 "per asset — see the asset rows", tolls=tolls)
                pooled.append(stamp(pd.DataFrame(rows), metas, lens,
                                    label if pool == POOL_ALL else
                                    f"{pool.split(':', 1)[1]} within {label}"))
    sha, keys = {}, {}
    frames = {"outcome_grid": pd.concat([grid] + pooled, ignore_index=True)}
    for name in ("coverage", "scale_grid", "spring_overlap", "hold_tally"):
        frames[name] = pd.concat(parts[name], ignore_index=True)
    surface = f"{label}: {len(assets)} asset(s) x {lenses} x {list(kinds)}"
    for name in list(frames):           # the collar speaks for the MERGED table
        frames[name] = collar(frames[name].drop(columns=list(COLLAR_COLUMNS),
                                                errors="ignore"),
                              f"CENSUS-R {name}, {surface}")
    any_meta = [next(iter(receipts.values()))["tape"]]
    frames["leans"] = stamp(collar(pd.DataFrame(
        [{"lean": f"{i:02d}", "text": x} for i, x in enumerate(LEANS)]),
        "the executor leans, verbatim"), any_meta, "4h", label)
    for name, df in frames.items():
        sha[name] = write_table(df, name, ROOT_TABLES[name], root)
        keys[name] = ROOT_TABLES[name]
        log(f"    wrote {name:16} rows={len(df):>7,}  sha={sha[name][:16]}")
    # the R1 tuning grids are filed BEFORE the census (they choose its pins) and
    # are DECLARED here, so F-KEY's totality over the root is whole
    for lens_ in TUNE_LENSES:
        q = root / f"{TUNING_GRID_NAME[lens_]}.parquet"
        if q.exists():
            n_ = TUNING_GRID_NAME[lens_]
            sha[n_] = content_sha(pd.read_parquet(q))
            keys[n_] = TUNING_GRID_KEY
            log(f"    declared {n_:14} rows={len(pd.read_parquet(q)):>7,}  "
                f"sha={sha[n_][:16]}")
    full = None
    if stage_d_manifest() is not None:
        full = (list(assets) == panels()["PANEL17"] and tuple(lenses) == LENSES
                and tuple(kinds) == SCALE_KINDS)
    man = {
        "seed": SEED, "stage": "TIER-C10 · STAGE 0b · CENSUS-R", "tier": TIER,
        "as_of": any_meta[0]["as_of_last_closed_4h"],
        "as_of_source": any_meta[0]["as_of_source"], "substrate": SNAPSHOT.name,
        "commission": {"label": label, "assets": list(assets), "lenses": list(lenses),
                       "scale_kinds": list(kinds), "classes": list(CLASSES),
                       "eras": list(ERAS), "era_law": ERA_LAW,
                       "era_boundary": ERA_BOUNDARY_ISO,
                       "retest_bands": [[n_, b.label] for n_, b in RETEST_BANDS],
                       "retest_pins": {k: v for k, v in RETEST_PINS.items()},
                       "tuning_result": tuning_result("5m", root),
                       "tuning_result_1d": tuning_result("1d", root),
                       "collar_5m_retest": COLLAR_5M_RETEST,
                       "horizons": [list(x) for x in HORIZONS], "pooled": list(pools),
                       "pools": pools,
                       "is_the_contract_grid": bool(full),
                       "n_declared_grid_rows": len(declared_cells(assets, lenses, kinds))},
        "pins": _pins_block(), "leans": list(LEANS),
        "sign_law": SIGN_LAW, "anchor_law": ANCHOR_LAW, "pins_status": PINS_STATUS,
        "code_sha": code, "port_sha256": file_sha256(PORT_PATH),
        "input_sha": {r["tape"]["source_file"]: r["tape"]["source_sha256"]
                      for r in receipts.values()},
        "cells": {k: {"tables": r["tables"], "calibrated_scale": r["calibrated_scale"],
                      "n_bars": r["tape"]["n_bars"], "toll_bps": r["toll_bps"],
                      "toll_bps_source": r["toll_bps_source"]}
                  for k, r in receipts.items()},
        "sha": sha, "keys": keys, "skipped_empty": [],
        "warranty": WARRANTY,
    }
    _dump(man, root / "build_manifest.json")
    return man


# ═══════════════════════════════════════════════ THE READER F-C10-TOLL BINDS TO
def get_toll(asset: str, lens: str, cls: str, scale_kind: str = "frozen3.0",
             horizon: str | None = None, grid_path: Path | None = None,
             era: str = ERA_ALL) -> float:
    """The measured toll in ATR for (asset, lens, class, era), READ FROM THE
    FILED GRID AND FROM NOTHING ELSE.  horizon=None -> toll_atr_all (the median
    over ALL of the class's anchors in that era; one number per class);
    horizon="H20"/"H100" -> that row's own toll_atr (the one its NET was struck
    with).  era defaults to the contract's full-history row.

    HALTS IF: the grid is absent, the row is absent or repeated, or the toll
    it holds is NaN (a class with no event has no measured toll — and a caller
    must not be handed a default in its place)."""
    p = Path(grid_path) if grid_path is not None else OUT / "outcome_grid.parquet"
    if not p.exists():
        raise SystemExit(f"HALT: no CENSUS-R grid at {p}")
    g = pd.read_parquet(p)
    q = g[(g["asset"] == asset) & (g["lens"] == lens) & (g["cls"] == cls)
          & (g["scale_kind"] == scale_kind) & (g["era"] == era)]
    col = "toll_atr_all"
    if horizon is not None:
        q, col = q[q["horizon"] == horizon], "toll_atr"
    vals = sorted(set(q[col].round(ROUND_ND).tolist())) if len(q) and q[col].notna().all() else []
    if len(vals) != 1:
        raise SystemExit(f"HALT: get_toll({asset}, {lens}, {cls}, {scale_kind}, {horizon}, "
                         f"era={era}): {len(q)} row(s), {col} values "
                         f"{vals or 'NaN / none'} in {p}")
    return float(vals[0])


# ═══════════════════════════════════════════════ printing
def print_report(root: Path) -> None:
    cov = pd.read_parquet(root / "coverage.parquet")
    log("\n  COVERAGE · DENSITY · MEAN LIFE  (report-only; frozen 3.0 beside calibrated)")
    log(f"  {'asset':>16} {'lens':>4} {'kind':>10} {'SCALE':>5} {'bars':>8} {'cov%':>6} "
        f"{'conf':>5} {'/100':>6} {'life':>7} {'cens':>4} {'flips':>5}")
    for r in cov.itertuples():
        log(f"  {r.asset:>16} {r.lens:>4} {r.scale_kind:>10} {r.scale_mult:>5.2f} "
            f"{r.n_bars:>8,} {r.coverage_pct:>6.2f} {r.n_confirmed:>5} "
            f"{r.density_per_100:>6.3f} {r.mean_confirmed_lifetime:>7.1f} "
            f"{r.n_lifetime_censored:>4} {r.n_flips:>5}")
    sg = pd.read_parquet(root / "scale_grid.parquet")
    log("\n  SCALE CALIBRATOR — THE WHOLE GRID [L2]  (* chosen · F frozen pin; target "
        f"{DENSITY_TARGET_PER_100}/100, quantum = one range)")
    for (a, l_), S in sg.groupby(["asset", "lens"], sort=True):
        cells = "  ".join(f"{r.scale_mult:.2f}:{r.density_per_100:.3f}"
                          f"{'*' if r.chosen else ''}{'F' if r.is_frozen_pin else ''}"
                          for r in S.itertuples())
        log(f"  {a:>16} {l_:>4}  q={S['density_quantum_per_100'].iloc[0]:.4f}  {cells}")
    g = pd.read_parquet(root / "outcome_grid.parquet")
    piv = g.set_index(GRID_KEY)
    log(f"\n  {COLLAR_5M_RETEST}")

    def era_table(era: str, assets_too: bool) -> None:
        log(f"\n  OUTCOME AFTER EVENT — era {era} — median term [ATR], toll, NET; "
            "H in BARS OF THE LENS")
        log(f"  {'asset':>16} {'lens':>4} {'kind':>10} {'class':>26} "
            f"{'n20':>7} {'med20':>8} {'toll':>7} {'NET20':>8} "
            f"{'n100':>7} {'med100':>8} {'toll':>7} {'NET100':>8}  pins")
        held = 0
        for (a, l_, k), _ in g.groupby(["asset", "lens", "scale_kind"], sort=True):
            if not assets_too and not a.startswith("POOLED:"):
                continue
            for cls in CLASSES:
                if not printable(l_, cls, era):
                    held += 1
                    continue
                x = piv.loc[(a, l_, cls, k, era, "H20")]
                y = piv.loc[(a, l_, cls, k, era, "H100")]

                def f(v, w=8):
                    return f"{v:>{w}.3f}" if np.isfinite(v) else f"{'NaN':>{w}}"
                log(f"  {a:>16} {l_:>4} {k:>10} {cls:>26} {x['n']:>7,} "
                    f"{f(x['median_term'])} {f(x['toll_atr'], 7)} {f(x['net'])} "
                    f"{y['n']:>7,} {f(y['median_term'])} {f(y['toll_atr'], 7)} "
                    f"{f(y['net'])}  "
                    f"{'TUNED' if cls in RETEST_CLASSES else 'frozen'}"
                    f"{' · n<30' if (x['provisional'] or y['provisional']) else ''}"
                    f"{' · ' + x['nan_reason'] if x['nan_reason'] else ''}")
        if held:
            log(f"    [COLLARED] {held} row-pair(s) filed and NOT printed in this table "
                "(5m retest-hold outside the tuning era) [LAW 4 + R1]")

    era_table(ERA_ALL, True)
    for era in (ERA_TUNING, ERA_HOLDOUT):
        era_table(era, False)


# ═══════════════════════════════ THE DIGEST — Tier-E, collared, no verdicts
NULL_ROOT = ROOT / "research_outputs" / "tierc10" / "null"
NULL_VARIANT_DIR = {"gaps-only": "gaps_only", "gaps+order": "gaps_order"}
PRIOR_ESTATE = {
    "census2b": ROOT / "research_outputs" / "census2b",
    "census2a": ROOT / "research_outputs" / "census2a",
    "synthesis": ROOT / "exchange" / "reports" / "SS_SYSTEM_SYNTHESIS_2026-08-06.md",
}


def prior_evidence() -> list[str]:
    """PRIOR ESTATE EVIDENCE on EMA taps / holds / retests at 5m-1h, READ from
    the filed artifacts at digest time — CONTEXT for R1's "feel free to search
    data from past runs", never a decider: the mechanical rule decides.  A
    missing artifact is said so, never guessed."""
    out: list[str] = []
    c2b = PRIOR_ESTATE["census2b"]
    man = c2b / "census2b_manifest.json"
    if man.exists():
        m = json.loads(man.read_text())
        p = m.get("pins", {})
        rib = p.get("ribbons", {})
        out.append(f"- `research_outputs/census2b/census2b_manifest.json` — CENSUS-2B's own "
                   f"ribbon pins: M = {rib.get('M')}, MH = {rib.get('MH')}; the pared "
                   f"within-S/R pairs {p.get('parta_wtb1', {}).get('pared_within_sr')}. "
                   f"**The operator's 89/127 ribbon is already the estate's M band's top "
                   f"pair**, and 89_127 is already a pared within-S/R pair. Warm-up rule "
                   f"{p.get('warm_bars_rule')!r} (e89 {p.get('warm_bars', {}).get('89')} "
                   f"bars, e127 {p.get('warm_bars', {}).get('127')}); CENSUS-R's warm-up is "
                   f"stricter still (NaN until `period` bars, never imputed).")
        out.append(f"- the same manifest's `ceil_ms` = {m.get('ceil_ms')} "
                   f"({iso(m.get('ceil_ms'))}) — **CENSUS-2B was itself cut at the era "
                   f"boundary R1 names**, one millisecond past it. The tuning era is the "
                   f"estate's own exploration corridor, not a new line.")
        kiss = p.get("kiss")
        if kiss:
            out.append(f"- the same manifest's `kiss` pins {kiss} — a prior approach/reject "
                       f"test with its own eps/delta in ATR and a k-bar window; CENSUS-R's "
                       f"retest-hold is a different object (a post-DIE candidacy with one "
                       f"evaluation), and none of those numbers is carried over.")
    sp = sorted((c2b / "springs").glob("*/5m.parquet"))
    if sp:
        rows = []
        for q in sp:
            d = pd.read_parquet(q)
            for side, S in d.groupby("side"):
                rows.append((str(S["asset"].iloc[0]), str(side), int(len(S)),
                             float(S["term_H20"].median()), float(S["toll_atr"].iloc[0])))
        out.append("- `research_outputs/census2b/springs/<asset>/5m.parquet` — the estate's "
                   "own 5m reclaim study (sweep of a prior extreme, then reclaim), same "
                   "H20/H100 arithmetic, same toll unit: "
                   + " · ".join(f"{a} {s} n={n:,} med term H20 {t:+.3f} toll {tl:.3f} "
                                f"NET {t - tl:+.3f}" for a, s, n, t, tl in rows[:4])
                   + f" … {len(rows)} (asset, side) cells. **The 5m toll of that study "
                     f"({min(r[4] for r in rows):.3f}–{max(r[4] for r in rows):.3f} ATR) is "
                     f"the same order as CENSUS-R's measured 5m toll**, and its NET at H20 "
                     f"sits within a tenth of an ATR of zero on every cell — the prior "
                     f"estate already saw that the 5m lens is toll-bound.")
    rc = c2b / "wtb1" / "agg" / "w_d_reclaim.parquet"
    if rc.exists():
        d = pd.read_parquet(rc)
        g = d.groupby("ema").agg(n=("ckey", "size"), lag=("reclaim_lag_h", "median"),
                                 after=("after_reclaim_to_exit_atr", "median"))
        out.append("- `research_outputs/census2b/wtb1/agg/w_d_reclaim.parquet` — EMA "
                   "loss-then-reclaim inside a live campaign, "
                   + " · ".join(f"e{int(i)}: n={int(r.n)}, median reclaim lag {r.lag:g} h, "
                                f"median move after reclaim {r.after:+.3f} ATR"
                                for i, r in g.iterrows())
                   + ". Long-EMA reclaims were measured as a RATCHET question there, on the "
                     "H/VH/UH ribbons, never on 89/127/200 and never after a range DIE.")
    ch = c2b / "wtb1" / "wtb1_cohort.parquet"
    if ch.exists():
        cols = [c for c in pd.read_parquet(ch).columns if c.startswith("rat_")]
        lens = sorted({c.split("_")[1] for c in cols})
        emas = sorted({int(c.split("_")[2]) for c in cols})
        marg = sorted({float(c.split("_")[3]) for c in cols})
        out.append(f"- `research_outputs/census2b/wtb1/wtb1_cohort.parquet` — {len(cols)} "
                   f"EMA-proximity columns `rat_<lens>_<ema>_<margin ATR>` over lenses "
                   f"{lens}, EMAs {emas}, margins {marg}. **R1's margin grid "
                   f"{list(TUNE_MARGINS)} is the estate's own proximity grid**, carried "
                   f"over unchanged; the EMAs are not (those were 200/300/450/500).")
    syn = PRIOR_ESTATE["synthesis"]
    if syn.exists():
        want = [("C5", "test-and-reclaims of the long EMAs"),
                ("C6", "test-and-reclaim in trend is simultaneously the add trigger"),
                ("CQ-9", "Long-EMA reclaims on 15m/1H/4H as ratchet/add points")]
        body = syn.read_text(errors="ignore").splitlines()
        for tag, needle in want:
            hit = [(k + 1, ln) for k, ln in enumerate(body) if needle in ln]
            if hit:
                k, ln = hit[0]
                frag = ln[max(0, ln.find(needle) - 60):ln.find(needle) + len(needle) + 120]
                out.append(f"- `exchange/reports/SS_SYSTEM_SYNTHESIS_2026-08-06.md:{k}` "
                           f"[{tag}] …{frag.strip()}…")
        out.append("- the synthesis carries the long-EMA test-and-reclaim as a LIVE "
                   "HYPOTHESIS with a 'tunable n x ATR cushion' and no measurement behind "
                   "it (CQ-9 is an OPEN question there). CENSUS-R measures the object for "
                   "the first time, after a range DIE, on the operator's five bands.")
    if not out:
        out.append("- NO prior estate artifact on EMA taps / holds / retests was found on "
                   "disk under the paths searched.")
    out.append("- SEARCHED AND EXCLUDED per the task: any `_reviewer_box` copy and the "
               "`docs/history` JSON mirrors.")
    return out


def _null_summary(variant: str) -> pd.DataFrame | None:
    p = NULL_ROOT / NULL_VARIANT_DIR[variant] / "null_summary.parquet"
    return pd.read_parquet(p) if p.exists() else None


def digest(root: Path) -> Path:
    """CENSUS_R_DIGEST.md — Tier-E wording only, no verdict language, and the
    LAW 4 + R1 collar enforced by printable() on every row it writes."""
    man = json.loads((root / "build_manifest.json").read_text())
    com = man["commission"]
    cov = pd.read_parquet(root / "coverage.parquet")
    sg = pd.read_parquet(root / "scale_grid.parquet")
    spr = pd.read_parquet(root / "spring_overlap.parquet")
    tal = pd.read_parquet(root / "hold_tally.parquet")
    g = pd.read_parquet(root / "outcome_grid.parquet")
    nulls = {v: _null_summary(v) for v in NULL_VARIANT_DIR}
    L: list[str] = []
    A = L.append
    A("# TIER-C10 · STAGE 0 · CENSUS-R — THE RANGE CENSUS, THE R1 BAND TUNING, THE NULL MODEL")
    A("")
    A(f"**{TIER}.** {GATES}")
    A("")
    A(f"- AS OF **{man['as_of']}** ({man['as_of_source']}) · substrate `{man['substrate']}` "
      f"· seed {man['seed']}")
    A(f"- commission: {com['label']} = {len(com['assets'])} assets x {com['lenses']} x "
      f"{com['scale_kinds']} x {com['eras']} eras x {[h[0] for h in com['horizons']]} "
      f"· is_the_contract_grid = **{com['is_the_contract_grid']}**")
    A(f"- classes ({len(com['classes'])}): {', '.join(com['classes'])}")
    A(f"- census code sha `{man['code_sha'][:16]}` · port `{man['port_sha256'][:16]}` "
      f"· grid sha `{man['sha']['outcome_grid'][:16]}`")
    A(f"- WARRANTY: {man['warranty']}")
    A("")
    A(f"> {COLLAR_5M_RETEST}")
    A("")
    A(f"> {ERA_LAW}")
    A("")
    A("## 0 · THE EXECUTOR LEANS, VERBATIM")
    A("")
    for x in LEANS:
        A(f"- {x}")
    A("")

    # ── 1 · coverage / density / life ─────────────────────────────────────
    A("## 1 · COVERAGE · CONFIRMED-RANGE DENSITY · MEAN LIFE — per asset, per lens")
    A("")
    A("Coverage = close inside the alive CONFIRMED macro range's span (boundaries + "
      "deviation zones), % of ALL bars. Density = confirmed macro ranges per 100 bars. "
      "Life = mean(die_i - confirm_i) over ranges that DIED; still-alive ones excluded and "
      "counted. `frozen3.0` is the pin of record [L2]; `calibrated` is IN-SAMPLE BY "
      "CONSTRUCTION and is printed beside it, never instead of it.")
    for lens in com["lenses"]:
        A("")
        A(f"### {lens}")
        A("")
        A("| asset | bars | gaps | cov% f3.0 | dens f3.0 | life f3.0 | SCALE cal | cov% cal "
          "| dens cal | life cal | flips f3.0 |")
        A("|---|---|---|---|---|---|---|---|---|---|---|")
        for a in com["assets"]:
            f = cov[(cov["asset"] == a) & (cov["lens"] == lens)
                    & (cov["scale_kind"] == "frozen3.0")]
            c = cov[(cov["asset"] == a) & (cov["lens"] == lens)
                    & (cov["scale_kind"] == "calibrated")]
            if not len(f) or not len(c):
                continue
            f, c = f.iloc[0], c.iloc[0]
            A(f"| {a} | {int(f.n_bars):,} | {int(f.gap_count)} | {f.coverage_pct:.2f} | "
              f"{f.density_per_100:.3f} | {f.mean_confirmed_lifetime:.1f} | "
              f"{c.scale_mult:g} | {c.coverage_pct:.2f} | {c.density_per_100:.3f} | "
              f"{c.mean_confirmed_lifetime:.1f} | {int(f.n_flips)} |")
    A("")
    A("### The SCALE calibrator — the whole grid [L2, F-GRID]")
    A("")
    A(f"Target {DENSITY_TARGET_PER_100}/100 bars; grid {list(SCALE_GRID)} (the Pine input's "
      "minval/step); tie-break: nearest density, then toward 3.0, then the lower SCALE. "
      "`*` = chosen · `F` = the frozen pin.")
    A("")
    A("| asset | lens | quantum/100 | " + " | ".join(f"{s:g}" for s in SCALE_GRID) + " |")
    A("|---" * (3 + len(SCALE_GRID)) + "|")
    for (a, l_), S in sg.groupby(["asset", "lens"], sort=True):
        S = S.sort_values("scale_mult")
        cells = " | ".join(f"{r.density_per_100:.3f}{'*' if r.chosen else ''}"
                           f"{'F' if r.is_frozen_pin else ''}" for r in S.itertuples())
        A(f"| {a} | {l_} | {S['density_quantum_per_100'].iloc[0]:.4f} | {cells} |")
    A("")

    # ── 2 · F-RF-4 spring overlap, both directions ────────────────────────
    A("## 2 · F-RF-4 — SPRING / UPTHRUST OVERLAP, BOTH DIRECTIONS, PRINTED")
    A("")
    A("Both overlap directions on every (asset, lens, scale kind): how many hardens "
      "reclaim by law, how many ALSO sweep the 20-bar extreme (harden -> house shape), and "
      "how many house shapes fall INSIDE a harden episode (house shape -> harden). "
      "`bottom` = springs, `top` = upthrusts.")
    A("")
    A("| lens | kind | side | hardens | law reclaim | also sweep look | house shapes | "
      "inside an episode |")
    A("|---|---|---|---|---|---|---|---|")
    for (l_, k, side), S in spr.groupby(["lens", "scale_kind", "side"], sort=True):
        A(f"| {l_} | {k} | {side} | {int(S['n_hardens'].sum()):,} | "
          f"{int(S['n_law_reclaim'].sum()):,} | {int(S['n_hardens_also_sweep_look'].sum()):,} "
          f"| {int(S['n_house_shapes'].sum()):,} | "
          f"{int(S['n_house_shapes_inside_episode'].sum()):,} |")
    A("")

    # ── 3 · hold tallies ──────────────────────────────────────────────────
    A("## 3 · HOLD TALLIES — every one-shot evaluation, per anchor")
    A("")
    A("`memory-line` rides the FROZEN flip-hold pins; the five R1 bands ride the TUNED "
      "pins. `not evaluated` = a candidate that was never retested inside its window (its "
      "window's end is not a bar-t fact).")
    A("")
    A("| lens | kind | anchor | band | pins | candidates | evaluated | hold | failed | "
      "truncated | not evaluated |")
    A("|---|---|---|---|---|---|---|---|---|---|---|")
    for (l_, k, anc), S in tal.groupby(["lens", "scale_kind", "anchor"], sort=True):
        r0 = S.iloc[0]
        A(f"| {l_} | {k} | {anc} | {r0['band']} | {r0['margin_atr']:g} ATR / "
          f"{int(r0['hold_bars'])} bars / ttl {int(r0['ttl_bars'])} | "
          f"{int(S['n_candidates'].sum()):,} | {int(S['n_evaluated'].sum()):,} | "
          f"{int(S['n_hold'].sum()):,} | {int(S['n_failed'].sum()):,} | "
          f"{int(S['n_truncated'].sum()):,} | {int(S['n_not_evaluated'].sum()):,} |")
    A("")

    # ── 4 · the R1 tuning ─────────────────────────────────────────────────
    A("## 4 · THE R1 HOLD-PIN TUNING — protocol fixed BEFORE the look")
    A("")
    A(f"- OPERATOR R1, verbatim: *\"Let's try the 89/127 ribbon, the 127/200 ribbon, and "
      f"taps on each ema. Feel free to search data from past runs to tune the defaults\"*")
    A(f"- GRID: {len(RETEST_BANDS)} bands x margin_atr {list(TUNE_MARGINS)} x hold_bars "
      f"{list(TUNE_HOLDS)} = 45 cells, WHOLE (ineligible cells printed)")
    A(f"- OBJECTIVE: {TUNE_OBJECTIVE}")
    A(f"- TIE-BREAK: {TUNE_TIE_BREAK}")
    A(f"- ERA: tuning = close <= {ERA_BOUNDARY_ISO}. The tapes are CUT at the boundary "
      f"BEFORE the detector runs, and `tune()` HALTS on any tape that reaches past it "
      f"(F-C10-TUNE plants a 5x edge in every holdout bar of a COPY: the grid sha and the "
      f"whole result are bit-identical).")
    for lens in ("5m", "1d"):
        res = tuning_result(lens, root)
        gp = root / f"{TUNING_GRID_NAME[lens]}.parquet"
        A("")
        A(f"### {lens} lens — floor n >= {TUNE_FLOOR_N[lens]}")
        if res is None or not gp.exists():
            A("")
            A(f"NOT FILED — no tuning result on disk for the {lens} lens.")
            continue
        tg = pd.read_parquet(gp)
        A("")
        A(f"Tuning assets ({len(res['tuning_assets'])}): {', '.join(res['tuning_assets'])}")
        if res.get("skipped"):
            A("")
            A("Skipped (no tuning-era tape on this lens): "
              + " · ".join(f"{s['asset']} ({s['tuning_era_bars']} bars)"
                           for s in res["skipped"]))
        A("")
        A("| band | margin_atr | hold_bars | n | median term | toll | **NET H20** | hit | "
          "assets | eligible |")
        A("|---|---|---|---|---|---|---|---|---|---|")
        for r in tg.itertuples():
            star = " **<-- SELECTED**" if (res["selected"] and r.band == res["band"]
                                           and float(r.margin_atr) == res["margin_atr"]
                                           and int(r.hold_bars) == res["hold_bars"]) else ""
            A(f"| {r.band} | {r.margin_atr:g} | {r.hold_bars} | {r.n:,} | "
              f"{r.median_term:+.4f} | {r.toll_atr:.4f} | {r.objective_net_h20:+.4f}{star} | "
              f"{r.hit_rate:.3f} | {r.n_assets_with_events} | "
              f"{'yes' if r.eligible else 'NO — ' + r.ineligible_reason} |")
        A("")
        if res["selected"]:
            A(f"**RESULT ({lens})**: band `{res['band']}` ({res['band_label']}) · "
              f"margin_atr **{res['margin_atr']:g}** · hold_bars **{res['hold_bars']}** · "
              f"ttl {res['ttl_bars']} · n {res['n']:,} · objective "
              f"{res['objective']:+.6f} ATR · {res['n_eligible']}/{res['n_cells']} cells "
              f"eligible · grid sha `{res['grid_sha'][:16]}` · ties on the objective: "
              f"{res.get('n_ties_on_objective')}")
        else:
            A(f"**RESULT ({lens})**: {res['reason']}. The Tier-E print falls back to the "
              f"5m-selected pins.")
    A("")
    A(f"**The census's retest pins of record**: margin_atr {RETEST_PINS['margin_atr']:g} · "
      f"hold_bars {RETEST_PINS['hold_bars']} · ttl_bars {RETEST_PINS['ttl_bars']} "
      f"[{RETEST_PINS['status']}] — source: {RETEST_PINS['source']}. ONE pin pair rules all "
      "five bands and all three lenses; the four unselected bands ride beside the selected "
      "one as Tier-E, per R1.")
    A("")

    # ── 5 · outcome after event, real vs null ─────────────────────────────
    A("## 5 · OUTCOME AFTER EVENT — REAL BESIDE THE NULL (both null variants)")
    A("")
    A("Term / MFE / MAE are measured in ATR from the CLOSE of the bar the event is KNOWN "
      "at (`known_at`), over H bars OF THE LENS, CENSORED and never shortened [L4]. "
      "NET = median term - the row's measured toll; a pooled row quotes the BINDING (max) "
      "per-asset toll [C-f]. The null's `median [q25, q75]` is across K draws and `pct` is "
      "the mid-rank percentile of the real value among them — a DESCRIPTION of where the "
      "real number sits, NEVER a p-value. `n<30` flags the lineage's provisional floor.")
    A("")
    for v, s in nulls.items():
        A(f"- null variant `{v}`: "
          + (f"{len(s):,} summary rows filed at "
             f"`research_outputs/tierc10/null/{NULL_VARIANT_DIR[v]}/`"
             if s is not None else "NOT FILED"))
    A("")

    def null_cell(v, asset, lens, kind, cls, era, hn, stat="median_term"):
        s = nulls.get(v)
        if s is None:
            return "n/a"
        q = s[(s["asset"] == asset) & (s["lens"] == lens) & (s["scale_kind"] == kind)
              & (s["cls"] == cls) & (s["era"] == era) & (s["horizon"] == hn)
              & (s["stat"] == stat)]
        if len(q) != 1:
            return "—"
        r = q.iloc[0]
        if not np.isfinite(r["null_median"]):
            return "NaN"
        return (f"{r['null_median']:+.3f} [{r['null_q25']:+.3f}, {r['null_q75']:+.3f}] "
                f"pct {r['real_pctile_in_null']:.0f}"
                if np.isfinite(r["real_pctile_in_null"]) else
                f"{r['null_median']:+.3f} [{r['null_q25']:+.3f}, {r['null_q75']:+.3f}]")

    piv = g.set_index(GRID_KEY)
    for pool in [POOL_ALL] + [f"POOLED:{p}" for p in SUB_POOLS]:
        if pool not in set(g["asset"]):
            continue
        for kind in com["scale_kinds"]:
            for lens in com["lenses"]:
                for era in ERAS:
                    rows = []
                    for cls in CLASSES:
                        if not printable(lens, cls, era):
                            continue
                        try:
                            x = piv.loc[(pool, lens, cls, kind, era, "H20")]
                            y = piv.loc[(pool, lens, cls, kind, era, "H100")]
                        except KeyError:
                            continue
                        rows.append((cls, x, y))
                    if not rows:
                        continue
                    A("")
                    A(f"### {pool} · {lens} · {kind} · era `{era}`")
                    A("")
                    head = ("| class | n H20 | med H20 | toll | **NET H20** | n H100 | "
                            "med H100 | **NET H100** | flags |")
                    both = pool == POOL_ALL and kind == "frozen3.0"
                    if both:
                        head = ("| class | n H20 | med H20 | toll | **NET H20** | "
                                "null gaps-only (H20) | null gaps+order (H20) | n H100 | "
                                "med H100 | **NET H100** | null gaps-only (H100) | "
                                "null gaps+order (H100) | flags |")
                    A(head)
                    A("|---" * (head.count("|") - 1) + "|")

                    def fn(v, w=3):
                        return f"{v:+.{w}f}" if np.isfinite(v) else "NaN"
                    for cls, x, y in rows:
                        flags = []
                        if x["provisional"] or y["provisional"]:
                            flags.append("n<30")
                        if cls in RETEST_CLASSES:
                            flags.append("TUNED")
                        if x["nan_reason"]:
                            flags.append(x["nan_reason"])
                        cells = [cls, f"{int(x['n']):,}", fn(x["median_term"]),
                                 f"{x['toll_atr']:.3f}" if np.isfinite(x["toll_atr"]) else "NaN",
                                 f"**{fn(x['net'])}**"]
                        if both:
                            cells += [null_cell("gaps-only", pool, lens, kind, cls, era, "H20"),
                                      null_cell("gaps+order", pool, lens, kind, cls, era, "H20")]
                        cells += [f"{int(y['n']):,}", fn(y["median_term"]),
                                  f"**{fn(y['net'])}**"]
                        if both:
                            cells += [null_cell("gaps-only", pool, lens, kind, cls, era, "H100"),
                                      null_cell("gaps+order", pool, lens, kind, cls, era, "H100")]
                        cells.append(" · ".join(flags))
                        A("| " + " | ".join(cells) + " |")
    n_held = int((~g["printable"].astype(bool)).sum())
    A("")
    A(f"**{n_held:,} of {len(g):,} grid rows are FILED AND NOT PRINTED here** — the 5m "
      "retest-hold rows outside the tuning era, P-BRK-S1's scoring ground [LAW 4 + R1]. "
      "F-C10-COLLAR proves not one of their figures appears in this file.")
    A("")

    # ── 6 · prior estate evidence ─────────────────────────────────────────
    A("## 6 · PRIOR ESTATE EVIDENCE ON EMA TAPS / HOLDS / RETESTS — CONTEXT ONLY")
    A("")
    A("R1 invited a search of past runs. What follows is CONTEXT, read from the filed "
      "artifacts at digest time; **the mechanical rule in §4 decided the pins, and nothing "
      "below moved them.**")
    A("")
    for x in prior_evidence():
        A(x)
    A("")

    # ── 7 · artifacts ─────────────────────────────────────────────────────
    A("## 7 · ARTIFACTS, KEYS, COST")
    A("")
    A("| table | key | rows | sha |")
    A("|---|---|---|---|")
    for name, sha in man["sha"].items():
        q = root / f"{name}.parquet"
        A(f"| `{name}.parquet` | {man['keys'][name]} | "
          f"{len(pd.read_parquet(q)):,} | `{sha[:16]}` |")
    A("")
    A(f"- per-cell ledgers: `{root.name}/cells/<SYM>__<lens>/{{events,grid,coverage,"
      f"scale_grid,spring_overlap,hold_tally}}.parquet` + `cell.json` (the resume receipt) "
      f"— cited by path and sha from `build_manifest.json['cells']`, gitignored.")
    A(f"- the R1 tuning: `TUNING_GRID.parquet` / `.md` / `TUNING_RESULT.json` (5m) and "
      f"`TUNING_GRID_1d.*` / `TUNING_RESULT_1d.json` (1d).")
    A(f"- the null model: `research_outputs/tierc10/null/gaps_only/` (contract-literal) and "
      f"`research_outputs/tierc10/null/gaps_order/` (the builder's leak-reduced variant) — "
      f"FILED SIDE BY SIDE, LABELLED, NEITHER CHOSEN. APOLLO rules which is the null of "
      f"record; this digest prints both and picks nothing.")
    A("")
    A(f"WARRANTY: {WARRANTY}")
    p = root / "CENSUS_R_DIGEST.md"
    p.write_text("\n".join(L) + "\n")
    return p


def time_only(sym: str, lens: str, tail_bars: int | None) -> None:
    """THE TIMING PROBE: the whole cell pipeline in memory, nothing written.
    A tail re-warms the ATR, so what it times is never a census cell."""
    t0 = time.perf_counter()
    tape = load_tape(sym, lens, tail_bars)
    t_load = time.perf_counter() - t0
    tm: dict = {}
    t1 = time.perf_counter()
    res = compute_cell(tape, SCALE_KINDS, tm)
    total = time.perf_counter() - t1
    ev = res["frames"]["events"]
    log(f"  TIMING PROBE {sym} {lens} n={tape.n:,} (tail_bars={tail_bars}) — NOTHING "
        f"WRITTEN · calibrated SCALE {res['calibrated_scale']:g} · {len(ev):,} class "
        "events over both scale kinds")
    clock(f"load+ATR {t_load:.2f}s · cell {total:.2f}s · " + " · ".join(
        f"{k} {v:.2f}" for k, v in tm.items()))


def main() -> int:
    ap = argparse.ArgumentParser(description="TIER-C10 CENSUS-R (Tier-E, report-only)")
    ap.add_argument("--assets", default="PANEL17")
    ap.add_argument("--lenses", default=",".join(LENSES))
    ap.add_argument("--scale-kind", default="both")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--merge-only", action="store_true")
    ap.add_argument("--time-only", action="store_true")
    ap.add_argument("--tail-bars", type=int, default=None)
    ap.add_argument("--tune", default=None, choices=list(TUNE_LENSES),
                    help="run the R1 hold-pin tuning on this lens and file it "
                         "(TUNING-ERA ONLY; files no census cell)")
    ap.add_argument("--digest", action="store_true",
                    help="write CENSUS_R_DIGEST.md from the FILED tables (run after the "
                         "census and both null variants have landed); computes nothing")
    a = ap.parse_args()
    label = a.assets if a.assets in ("PANEL17", "CLASSIC5", "UNSEEN12") else "NAMED"
    assets = (panels()[a.assets] if label != "NAMED"
              else [s.strip() for s in a.assets.split(",") if s.strip()])
    lenses = [x for x in LENSES if x in {s.strip() for s in a.lenses.split(",")}]
    kinds = SCALE_KINDS if a.scale_kind == "both" else tuple(
        k for k in SCALE_KINDS if k in {s.strip() for s in a.scale_kind.split(",")})
    if not assets or not lenses or not kinds:
        raise SystemExit("HALT: empty commission (assets / lenses / scale kinds)")
    if label == "NAMED":
        label = f"NAMED({len(assets)})"
    root = Path(a.out).expanduser().resolve()
    close_ms, src = as_of_close_ms(assets[0])
    log(f"TIER-C10 · STAGE 0b · CENSUS-R · {TIER}")
    log(f"  seed {SEED} · substrate {SNAPSHOT} · AS_OF {iso(close_ms)} ({src})")
    log(f"  commission {label}: {len(assets)} asset(s) x {lenses} x {list(kinds)} -> {root}")
    for x in LEANS:
        log(f"  {x}")
    log(f"  RETEST-HOLD [{RETEST_PINS['status']}]: margin_atr {RETEST_PINS['margin_atr']} · "
        f"hold_bars {RETEST_PINS['hold_bars']} · ttl_bars {RETEST_PINS['ttl_bars']} · "
        f"bands {[b.label for _, b in RETEST_BANDS]}")
    log(f"    pins source: {RETEST_PINS['source']}")
    log(f"    law: {RETEST_PINS['law']}")
    log(f"    executor pins still unruled: {RETEST_PINS['unruled']}")
    log(f"  ERA: {ERA_LAW}")
    log(f"  {COLLAR_5M_RETEST}")
    if a.tune:
        run_tuning(root, assets, a.tune)
        return 0
    if a.digest:
        p = digest(root)
        log(f"\n  digest -> {p}  ({len(p.read_text().splitlines()):,} lines)")
        return 0
    if a.time_only:
        for sym in assets:
            for lens in lenses:
                time_only(sym, lens, a.tail_bars)
        return 0
    if a.tail_bars is not None:
        raise SystemExit("HALT: --tail-bars is for --time-only; a tail re-warms the ATR "
                         "and is never a census cell")
    t0 = time.perf_counter()
    if not a.merge_only:
        for sym in assets:
            for lens in lenses:
                run_cell(root, sym, lens, kinds, force=a.force)
    man = merge(root, assets, lenses, kinds, label)
    print_report(root)
    log(f"\n  grid -> {root / 'outcome_grid.parquet'}  ({man['commission']['n_declared_grid_rows']} "
        f"declared rows; is_the_contract_grid = {man['commission']['is_the_contract_grid']})")
    log(f"  manifest -> {root / 'build_manifest.json'}")
    clock(f"total {time.perf_counter() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
