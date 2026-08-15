"""SEQ-8 — The Cascade Event Extract · D1 raw event stream + D6 warmup table.

Contract: exchange/queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md
Executor: HEPHAESTUS. Engine 1.0.11 byte-UNTOUCHED — this script imports
engine.indicators (ema/atr/crossover/crossunder) and scripts/census_build.py
and edits neither.

WHY THIS FILE IMPORTS census_build RATHER THAN RESTATING ITS CONSTANTS
  I1 requires the exploration ceiling be asserted "from the census machinery's
  own constants"; I2 forbids a new resampler (ARGUS hazard F-1R-*). Both are
  satisfied structurally: CEIL_MS, ASSET_STARTS, TF_MS, TFS, RESAMPLE, ATR_LEN
  and the resampler `_resample` are READ from census_build, never re-typed. If
  the census machinery moves, this extract moves with it or fails loudly.

WHAT IT EMITS (research_outputs/seq8/)
  seq8_events.jsonl    D1 — one row per cross event, per asset x TF x lattice.
                       NO chaining of any kind: cascade definitions are views
                       computed on top of this stream (D2), never baked into
                       it. This is the atom-independence guarantee (SEQ-1).
  seq8_warmup.json     D6 — per asset x TF, the first timestamp at which
                       EMA300/EMA450 are fully warmed, or NEVER.
  seq8_extract_manifest.json  params, ceiling, per-file sha256, row counts.

THE TWO LATTICES (I3, ruling Q2a — measured in parallel, never merged)
  A {9,89,200}: pairs 9_89, 89_200, 9_200      (the census machinery's own)
  B {12,25}:    pair  12_25                    (Trader XO macro trend scanner,
                docs/knowledge/pine/12-25EMA Trend Scanner-Pinescript.txt)
  8 event classes total = 4 pairs x 2 directions.

EMA 300/450 WARMUP (I3 — "NaN until full warmup, never backfilled")
  engine.indicators.ema is seeded at the first finite value and is therefore
  never NaN after bar 0. A length alone does not define "warmed", so this file
  states the rule explicitly rather than picking a round multiple: bar k is
  warmed when the seed's residual weight (1-alpha)^k has decayed below
  SEED_RESIDUAL. That is a falsifiable arithmetic statement, printed with the
  bar counts it implies. Only the NEW 300/450 columns are masked — masking
  9/89/200 would fork them from the census and break F-SEQ1.

NO LOOKAHEAD (F-SEQ5). Every column on an event row derives from data at or
before that event bar's CLOSE. Cross-timeframe state (`mtf`) is gathered as-of
the last CLOSED bar of each other TF at that instant (engine.htf convention,
the same rule census_build.asof_idx applies).

Usage:
  python scripts/seq8_extract.py
  python scripts/seq8_extract.py --run2
  SEQ8_ASSETS=TAOUSDT python scripts/seq8_extract.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import census_build as cb                                       # noqa: E402
from engine.indicators import ema, atr, crossover, crossunder   # noqa: E402

# ---------------------------------------------------------------------------
# Configuration. Everything the census already fixed is READ from it (I1/I2);
# only genuinely new parameters are declared here.
# ---------------------------------------------------------------------------
LATTICES = {
    "A": {"emas": [9, 89, 200],
          "pairs": {"9_89": (9, 89), "89_200": (89, 200), "9_200": (9, 200)}},
    "B": {"emas": [12, 25],
          "pairs": {"12_25": (12, 25)}},
}
ALL_EMAS = [9, 89, 200, 12, 25]          # computed on every TF
HTF_ORIENT = [300, 450]                  # I3: HTF orientation columns
HTF_TFS = ["1h", "4h", "12h", "1d"]      # I3: only these carry 300/450
SEED_RESIDUAL = 1e-3                     # warmup rule; see module docstring

R6 = cb.R6                               # byte-stable float rounding
EXTRACT_VERSION = "seq8-extract-1.0.0"

# Q1c signal taxonomy (memory Entry 19, operator 2026-07-29). I4 requires the
# gap list be REPORTED, not improvised around. Emitted vs not, stated once here
# and echoed into the manifest so no downstream study can mistake the coverage.
Q1C_CLASSES = {
    "ema_ema_cross": {
        "emitted": True,
        "note": "both lattices, both directions, all 7 census TFs — this file"},
    "ema_ema_test_and_reject": {
        "emitted": False,
        "note": "no detector in the census machinery; I4 forbids building one here"},
    "price_test_and_bounce": {
        "emitted": False,
        "note": "no detector in the census machinery; D10 termini are the nearest "
                "existing relative (census_termini.jsonl) but are pivots, not "
                "test-and-bounce events"},
    "sr_flip": {
        "emitted": False,
        "note": "no detector in the census machinery; I4 forbids building one here"},
    "ribbon_state_episode": {
        "emitted": False,
        "note": "episodes are intervals, not events; continuation.jsonl carries a "
                "ribbon-separation flag but no episode object exists"},
}


def warmup_bars(length: int, residual: float = SEED_RESIDUAL) -> int:
    """Bars until an EMA(length) seeded at the series start has decayed its
    seed below `residual`. out[k] carries seed weight (1-alpha)^k, so the first
    warmed index is ceil(log(residual)/log(1-alpha))."""
    alpha = 2.0 / (length + 1.0)
    return int(math.ceil(math.log(residual) / math.log(1.0 - alpha)))


WARM = {L: warmup_bars(L) for L in HTF_ORIENT}

# mtf bit string — 7 orientation bits per TF, documented once, emitted per row.
MTF_BITS = ["e9>e89", "e89>e200", "e9>e200", "e12>e25",
            "close>e89", "close>e200", "e300>e450"]


def iso(ms_val: int) -> str:
    return (datetime.fromtimestamp(ms_val / 1000, timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ"))


def rnd(x) -> float | None:
    """Round for byte-stable emission; non-finite becomes null, never 0."""
    xf = float(x)
    return round(xf, R6) if math.isfinite(xf) else None


# ---------------------------------------------------------------------------
# Frame loading — census parity by construction
# ---------------------------------------------------------------------------
def load_tf_ext(klines: Path, sym: str, tf: str, start_ms: int) -> pd.DataFrame:
    """census_build.load_tf, extended with the {12,25} lattice and the 300/450
    HTF orientation columns.

    The load/ceiling/resample/warm-up-then-restrict sequence is copied from
    census_build.load_tf deliberately and is asserted equal to it downstream by
    `assert_census_parity` — this function may not drift from the machinery.
    Resampling calls census_build._resample (the s1 algorithm), satisfying I2.
    """
    if tf in cb.RESAMPLE:
        src_tf, step = cb.RESAMPLE[tf]
        raw = pd.read_parquet(klines / f"{sym}_{src_tf}.parquet")
        raw = raw[raw["open_time"] < cb.CEIL_MS].sort_values("open_time")
        df = cb._resample(raw.reset_index(drop=True), step)
    else:
        df = pd.read_parquet(klines / f"{sym}_{tf}.parquet")
        df = (df[df["open_time"] < cb.CEIL_MS]
              .sort_values("open_time").reset_index(drop=True))

    o = df["open_time"].to_numpy(np.int64)
    c = df["close"].to_numpy(float)
    h = df["high"].to_numpy(float)
    lo = df["low"].to_numpy(float)
    n = len(c)

    cols = {"open_time": o, "open": df["open"].to_numpy(float),
            "high": h, "low": lo, "close": c}
    for L in ALL_EMAS:
        cols[f"e{L}"] = ema(c, L)
    cols["atr"] = atr(h, lo, c, cb.ATR_LEN)

    # I3: the NEW columns only. Masked in-place before any restriction so the
    # mask indexes the recursion's own series, not the asset window.
    for L in HTF_ORIENT:
        if tf in HTF_TFS:
            v = ema(c, L)
            v[:min(WARM[L], n)] = np.nan          # never backfilled
        else:
            v = np.full(n, np.nan)
        cols[f"e{L}"] = v

    out = pd.DataFrame(cols)
    # restrict to the asset window AFTER warm-up (start_ms floor) — census rule
    return out[out["open_time"] >= start_ms].reset_index(drop=True)


def assert_census_parity(klines: Path, sym: str, tf: str, start_ms: int,
                         ext: pd.DataFrame, log) -> dict:
    """PROBE: the extended loader reproduces census_build.load_tf exactly on
    every column the census owns. A single mismatched float here would make
    F-SEQ1 meaningless, so it is checked per asset x TF, not sampled."""
    ref = cb.load_tf(klines, sym, tf, start_ms)
    shared = ["open_time", "open", "high", "low", "close",
              "e9", "e89", "e200", "atr"]
    res = {"rows_ref": int(len(ref)), "rows_ext": int(len(ext)), "cols": {}}
    ok = len(ref) == len(ext)
    for col in shared:
        a = ref[col].to_numpy()
        b = ext[col].to_numpy()
        if len(a) != len(b):
            res["cols"][col] = "LENGTH-MISMATCH"
            ok = False
            continue
        same = np.array_equal(a, b) or (
            np.array_equal(np.isnan(a), np.isnan(b))
            and np.array_equal(a[~np.isnan(a)], b[~np.isnan(b)]))
        res["cols"][col] = "identical" if same else "DIFFERS"
        ok = ok and same
    res["status"] = "PASS" if ok else "FAIL"
    if not ok:
        log(f"    PARITY FAIL {sym} {tf}: {res}")
    return res


# ---------------------------------------------------------------------------
# Cross detection — identical semantics to census_build.detect_crosses
# ---------------------------------------------------------------------------
def detect_all(df: pd.DataFrame) -> dict:
    """{(lattice, pair): {'up': idx[], 'down': idx[]}} on this TF's own bars.

    Runs on the RESTRICTED frame, exactly as census_build.detect_crosses does,
    so the first restricted bar has a NaN predecessor and cannot be a cross.
    Reproducing that edge is what makes F-SEQ1 a real reconciliation.
    """
    ev = {}
    for lat, spec in LATTICES.items():
        for name, (fa, sl) in spec["pairs"].items():
            a = df[f"e{fa}"].to_numpy()
            b = df[f"e{sl}"].to_numpy()
            ev[(lat, name)] = {"up": np.nonzero(crossover(a, b))[0],
                               "down": np.nonzero(crossunder(a, b))[0]}
    return ev


def mtf_state(frames: dict, tfs: list, ref_close_ms: np.ndarray) -> dict:
    """As-of orientation bits for every TF at each of `ref_close_ms`.

    As-of = the last bar of that TF whose CLOSE is <= the reference instant.
    For the event's own TF that resolves to the event bar itself. Bits are '1',
    '0', or 'x' when the input is NaN (unwarmed 300/450, or a TF with no closed
    bar yet). No lookahead is possible by construction (F-SEQ5).
    """
    out = {}
    for tf in tfs:
        f = frames[tf]
        fo = f["open_time"].to_numpy(np.int64)
        idx = np.searchsorted(fo + cb.TF_MS[tf], ref_close_ms, side="right") - 1
        take = np.clip(idx, 0, None)

        def col(name):
            v = f[name].to_numpy(float)[take].copy()
            v[idx < 0] = np.nan
            return v

        e9, e89, e200 = col("e9"), col("e89"), col("e200")
        e12, e25 = col("e12"), col("e25")
        e300, e450 = col("e300"), col("e450")
        cl = col("close")
        pairs = [(e9, e89), (e89, e200), (e9, e200), (e12, e25),
                 (cl, e89), (cl, e200), (e300, e450)]
        chars = []
        for x, y in pairs:
            with np.errstate(invalid="ignore"):
                gt = x > y
            bad = ~(np.isfinite(x) & np.isfinite(y))
            s = np.where(gt, "1", "0")
            s[bad] = "x"
            chars.append(s)
        out[tf] = np.char.add(np.char.add(np.char.add(chars[0], chars[1]),
                              np.char.add(chars[2], chars[3])),
                              np.char.add(np.char.add(chars[4], chars[5]),
                                          chars[6]))
    return out


# ---------------------------------------------------------------------------
# Per-asset extract
# ---------------------------------------------------------------------------
def extract_asset(klines: Path, sym: str, log) -> dict:
    t0 = time.time()
    start_ms = cb.ms(cb.ASSET_STARTS[sym])
    frames = {tf: load_tf_ext(klines, sym, tf, start_ms) for tf in cb.TFS}

    parity = {tf: assert_census_parity(klines, sym, tf, start_ms, frames[tf], log)
              for tf in cb.TFS}

    ex = frames[cb.EXEC_TF]
    xo = ex["open_time"].to_numpy(np.int64)
    xopen = ex["open"].to_numpy(float)
    N = len(ex)

    rows = []
    for tf in cb.TFS:
        f = frames[tf]
        fo = f["open_time"].to_numpy(np.int64)
        ev = detect_all(f)
        for (lat, pair), dirs in ev.items():
            for direction, sub in (("up", dirs["up"]), ("down", dirs["down"])):
                if len(sub) == 0:
                    continue
                ev_open = fo[sub]
                ev_close = ev_open + cb.TF_MS[tf]
                # exec anchor: FIRST exec bar whose open >= the cross bar's
                # close (census convention — the first tradeable instant).
                anch = np.searchsorted(xo, ev_close, side="left")
                bits = mtf_state(frames, cb.TFS, ev_close)
                ev_atr = f["atr"].to_numpy(float)[sub]
                cols = {c: f[c].to_numpy(float)[sub] for c in
                        ("open", "high", "low", "close",
                         "e9", "e89", "e200", "e12", "e25", "e300", "e450")}
                for j, i in enumerate(sub):
                    a = int(anch[j])
                    ok = a < N
                    r = {
                        "asset": sym, "tf": tf, "lattice": lat,
                        "event_class": pair, "dir": direction,
                        "ts": int(ev_open[j]), "ts_iso": iso(int(ev_open[j])),
                        "bar_close_ms": int(ev_close[j]),
                        "bar_idx": int(i),
                        "event_price": rnd(cols["close"][j]),
                        "bar_open": rnd(cols["open"][j]),
                        "bar_high": rnd(cols["high"][j]),
                        "bar_low": rnd(cols["low"][j]),
                        "atr": rnd(ev_atr[j]),
                        "exec_idx": a if ok else None,
                        "exec_ts": int(xo[a]) if ok else None,
                        "p0": rnd(xopen[a]) if ok else None,
                        # census_outcomes.jsonl keeps exactly these; the raw
                        # stream keeps everything and FLAGS them instead, so no
                        # event is silently dropped from the atom set (SEQ-1).
                        "exec_anchor_ok": bool(ok),
                        "atr_ok": bool(np.isfinite(ev_atr[j]) and ev_atr[j] > 0),
                        "mtf": {t: str(bits[t][j]) for t in cb.TFS},
                    }
                    for L in ALL_EMAS + HTF_ORIENT:
                        r[f"e{L}"] = rnd(cols[f"e{L}"][j])
                    rows.append(r)

    warm = warmup_rows(sym, frames)
    log(f"  {sym}: N={N} events={len(rows)} "
        f"parity={'PASS' if all(p['status'] == 'PASS' for p in parity.values()) else 'FAIL'} "
        f"({time.time() - t0:.1f}s)")
    return {"events": rows, "warmup": warm, "parity": parity,
            "exec_bars": N,
            "tf_bars": {tf: int(len(frames[tf])) for tf in cb.TFS}}


def warmup_rows(sym: str, frames: dict) -> list:
    """D6: per asset x TF, the first timestamp at which EMA300/EMA450 are fully
    warmed, or NEVER within the substrate. Emitted so no later study silently
    consumes an unconverged HTF value."""
    out = []
    for tf in cb.TFS:
        f = frames[tf]
        o = f["open_time"].to_numpy(np.int64)
        for L in HTF_ORIENT:
            applicable = tf in HTF_TFS
            v = f[f"e{L}"].to_numpy(float)
            good = np.nonzero(np.isfinite(v))[0]
            first = int(good[0]) if len(good) else None
            out.append({
                "asset": sym, "tf": tf, "ema": L,
                "applicable": applicable,
                "bars_in_window": int(len(o)),
                "warmup_bars_required": WARM[L] if applicable else None,
                "first_warm_ts": int(o[first]) if (applicable and first is not None) else None,
                "first_warm_iso": iso(int(o[first])) if (applicable and first is not None) else None,
                "warm_bars_in_window": int(len(good)) if applicable else 0,
                "status": ("NOT-APPLICABLE" if not applicable
                           else "WARMED" if first is not None else "NEVER"),
            })
    return out


# ---------------------------------------------------------------------------
# Emission
# ---------------------------------------------------------------------------
def write_jsonl(path: Path, rows: list, keyfn) -> str:
    """Byte-stable JSONL, census convention: total-order sort, sorted keys,
    compact separators, LF newlines (census_build.write_jsonl)."""
    rows = sorted(rows, key=keyfn)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, obj) -> str:
    path.write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n",
                    encoding="utf-8", newline="\n")
    return hashlib.sha256(path.read_bytes()).hexdigest()


EVENT_KEY = (lambda r: (r["asset"], r["tf"], r["lattice"], r["event_class"],
                        r["dir"], r["ts"]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run2", action="store_true",
                    help="write to the run2 root for the F-SEQ7 determinism pass")
    args = ap.parse_args()
    root = ROOT / "research_outputs" / ("seq8_run2" if args.run2 else "seq8")
    root.mkdir(parents=True, exist_ok=True)

    from engine.data import cache_dir
    klines = cache_dir() / "klines"
    assets_env = os.environ.get("SEQ8_ASSETS")
    assets = assets_env.split(",") if assets_env else list(cb.ASSET_STARTS)

    # ---- I1: the ceiling is READ from the census machinery and PRINTED ----
    print("SEQ-8 EXTRACT — D1 raw event stream + D6 warmup")
    print(f"  exploration ceiling : {cb.CEIL_MS}  ({iso(cb.CEIL_MS)})  "
          f"[census_build.CEIL_MS]")
    print(f"  lattices            : A {LATTICES['A']['emas']}  "
          f"B {LATTICES['B']['emas']}")
    print(f"  HTF orientation     : EMA {HTF_ORIENT} on {HTF_TFS}")
    print(f"  warmup rule         : seed residual < {SEED_RESIDUAL:g}  -> "
          + ", ".join(f"EMA{L}={WARM[L]} bars" for L in HTF_ORIENT))
    print(f"  assets              : {','.join(assets)}")

    t0 = time.time()
    events, warm, parity, tf_bars, exec_bars = [], [], {}, {}, {}
    for sym in assets:
        r = extract_asset(klines, sym, print)
        events.extend(r["events"])
        warm.extend(r["warmup"])
        parity[sym] = r["parity"]
        tf_bars[sym] = r["tf_bars"]
        exec_bars[sym] = r["exec_bars"]

    shas = {}
    shas["seq8_events.jsonl"] = write_jsonl(root / "seq8_events.jsonl",
                                            events, EVENT_KEY)
    shas["seq8_warmup.json"] = write_json(root / "seq8_warmup.json", warm)

    # per (asset, tf, lattice, class, dir) counts — the F-SEQ1 reconciliation
    # surface, emitted here so the fixture reads a table rather than the stream.
    counts = {}
    for r in events:
        k = f"{r['asset']}|{r['tf']}|{r['lattice']}|{r['event_class']}|{r['dir']}"
        c = counts.setdefault(k, {"raw": 0, "census_filtered": 0})
        c["raw"] += 1
        if r["exec_anchor_ok"] and r["atr_ok"]:
            c["census_filtered"] += 1
    shas["seq8_event_counts.json"] = write_json(root / "seq8_event_counts.json",
                                                counts)

    parity_fails = [f"{s}/{tf}" for s, d in parity.items()
                    for tf, p in d.items() if p["status"] != "PASS"]
    manifest = {
        "phase": "SEQ-8 extract (D1 raw event stream, D6 warmup)",
        "contract": "exchange/queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md",
        "extract_version": EXTRACT_VERSION,
        "engine_version_note": "engine 1.0.11 byte-untouched; imports indicators only",
        "census_machinery": "scripts/census_build.py (constants + _resample imported, not restated)",
        "window": {"assets": {a: cb.ASSET_STARTS[a] for a in assets},
                   "ceiling_ms": cb.CEIL_MS,
                   "ceiling": f"{iso(cb.CEIL_MS)} (exploration-classic)",
                   "ceiling_source": "census_build.CEIL_MS"},
        "params": {"tfs": cb.TFS, "lattices": {k: v["emas"] for k, v in LATTICES.items()},
                   "event_classes": sorted(
                       f"{lat}:{p}" for lat, spec in LATTICES.items()
                       for p in spec["pairs"]),
                   "htf_orient_emas": HTF_ORIENT, "htf_orient_tfs": HTF_TFS,
                   "seed_residual": SEED_RESIDUAL,
                   "warmup_bars": {str(L): WARM[L] for L in HTF_ORIENT},
                   "atr_len": cb.ATR_LEN, "mtf_bits": MTF_BITS,
                   "resampler": "census_build._resample (s1 algorithm; I2 — no new resampler)"},
        "q1c_coverage": Q1C_CLASSES,
        "assets_run": assets,
        "per_asset_exec_bars": exec_bars,
        "per_asset_tf_bars": tf_bars,
        "census_loader_parity": {"status": "PASS" if not parity_fails else "FAIL",
                                 "failures": parity_fails,
                                 "checked": sum(len(d) for d in parity.values())},
        "row_counts": {"events": len(events), "warmup": len(warm)},
        "sha256": shas,
        "versions": {"python": sys.version.split()[0], "numpy": np.__version__,
                     "pandas": pd.__version__},
        "elapsed_s": round(time.time() - t0, 1),
    }
    write_json(root / "seq8_extract_manifest.json", manifest)

    print(f"\nEXTRACT done -> {root.name} in {time.time() - t0:.1f}s")
    print(f"  events {len(events)}   warmup rows {len(warm)}")
    print(f"  census loader parity: {manifest['census_loader_parity']['status']} "
          f"({manifest['census_loader_parity']['checked']} asset x TF frames)")
    for k, v in shas.items():
        print(f"  {k:28} {v[:16]}")
    return 0 if not parity_fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
