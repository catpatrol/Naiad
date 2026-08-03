#!/usr/bin/env python
"""brief_capture.py -- build and store a BRIEF-2 capture (Amendment 2 §8.1).

    C:\\venvs\\naiad\\Scripts\\python.exe scripts/brief_capture.py --slot ny_am

Writes `briefs/brief_<date>_<slot>.json` (TRACKED) and appends to
`briefs/index.jsonl`.  HTML is disposable and is regenerated from any stored
capture by `brief_render.py`; the JSON is the record.

WHY THE CAPTURE IS THE RECORD AND THE HTML IS NOT.  A stored capture embeds the
complete rule set, the rules hash, the analytics version and sha, and every
input's last_bar_utc -- so a capture from last week and one from today can be
told apart and compared.  A rendered page carries none of that reliably, and
regenerating it from the capture is cheap.

SLOT ISOLATION (F-B24).  Two captures on the same date with different slots
coexist; neither overwrites the other, and the index carries both.  A same-slot
re-run warns and requires --force, because silently replacing a stored capture
would break archive comparability for anything already published from it.
"""

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import analytics                                                    # noqa: E402
import brief2 as B2                                                 # noqa: E402
from analytics import structure as S                                # noqa: E402
from analytics import volatility as V                               # noqa: E402

BRIEFS_DIR = ROOT / "briefs"
INDEX_PATH = BRIEFS_DIR / "index.jsonl"
DAY_MS = 86_400_000

# v4 §II.11, carried forward.  LIT's usable history begins 2025-12-01 (the
# two-token trap: earlier LITUSDT history is Litentry, a different asset).  A
# quantity whose value depends on HOW MUCH history exists is therefore
# known-wrong for LIT and is marked; a quantity that is a PRICE is not.
LIT_KNOWN_WRONG_KINDS = ("percentile", "rank", "bar_count")
LIT_NOT_MARKED = ("level", "volume_weighted")


def _now_ms():
    return int(time.time() * 1000)


def iso(ms):
    if ms is None:
        return None
    return datetime.fromtimestamp(int(ms) / 1000, timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def lit_known_wrong(symbol, kind):
    """Should this quantity carry a known-wrong marker for this asset?

    v4 §II.11 is precise about scope and the precision is the point: mark
    PERCENTILE, RANK and BAR-COUNT quantities only.  Do NOT mark levels or
    volume-weighted quantities -- a VWAP or a POC computed over LIT's real
    history is a correct number about a real asset, and marking it would train
    the reader to ignore markers.
    """
    if symbol != "LITUSDT":
        return False
    return kind in LIT_KNOWN_WRONG_KINDS


def partition_footprint(as_of_ms, windows_days, warmup_days=0):
    """§8.4 -- which dates a capture would READ, warm-ups included.

    Reported so the lockbox overlap of a capture is a computed fact rather than
    an assurance.  Per the operator ruling of 2026-08-03 this is DISCLOSURE, not
    refusal: the seal governs scored outcome evidence, not raw price inside a
    display-only trailing window.
    """
    longest = max(list(windows_days) + [0]) + warmup_days
    start = int(as_of_ms) - longest * DAY_MS
    ov = analytics.lockbox_overlap(start, as_of_ms)
    return {"reads_from_ms": start, "reads_from_utc": iso(start),
            "as_of_ms": int(as_of_ms), "longest_window_days": longest,
            "warmup_days_included": warmup_days,
            "lockbox_overlap": ov}


def backfill_guard(target_date, first_capture_date, backfill=False):
    """§8.4 -- forward-only unless explicitly overridden.

    Refuses a target earlier than the first stored capture without --backfill.
    The override does not silently succeed: it stamps a provenance marker so a
    backfilled capture can never be mistaken for one taken live at the time.
    """
    if first_capture_date is None or target_date >= first_capture_date:
        return {"allowed": True, "backfilled": False, "marker": None}
    if not backfill:
        raise SystemExit(
            f"REFUSED: {target_date} is earlier than the first stored capture "
            f"({first_capture_date}). The brief is forward-only. Historical "
            f"confluence work is CENSUS work on exploration-classic, output to "
            f"research_outputs/census1d/, never into briefs/. Pass --backfill "
            f"to override; it stamps a provenance marker.")
    return {"allowed": True, "backfilled": True,
            "marker": {"backfilled": True,
                       "reason": "explicit --backfill override",
                       "first_capture_date": first_capture_date,
                       "stamped_utc": iso(_now_ms()),
                       "not_taken_live": True}}


def first_capture_date(briefs_dir=BRIEFS_DIR):
    dates = sorted(p.name.split("_")[1] for p in briefs_dir.glob("brief_*_*.json"))
    return dates[0] if dates else None


def _last_bars(klines):
    out = {}
    for tf, df in (klines or {}).items():
        if df is not None and len(df):
            out[tf] = iso(int(df["open_time"].iloc[-1]))
    return out


def build_capture(symbols, slot, as_of_ms=None, parity_certified=False,
                  backfill=False, log=print):
    """Assemble a full capture: envelope + Part I + Part II per asset."""
    import pandas as pd
    from engine.data import cache_dir
    from engine.version import ENGINE_VERSION

    t0 = time.time()
    as_of_ms = as_of_ms or _now_ms()
    date_str = iso(as_of_ms)[:10]

    guard = backfill_guard(date_str, first_capture_date(), backfill)

    doc = B2.capture_envelope(date_str, slot, parity_certified=parity_certified,
                              engine_version=ENGINE_VERSION, universe=symbols)
    doc["generated_utc"] = iso(_now_ms())
    doc["as_of_utc"] = iso(as_of_ms)
    doc["backfill"] = guard
    doc["assets"] = {}
    doc["runtime_by_layer"] = {}

    kd = cache_dir() / "klines"
    for sym in symbols:
        s0 = time.time()
        k = {}
        for tf in ("1m", "5m", "15m", "1h"):
            p = kd / f"{sym}_{tf}.parquet"
            if p.exists():
                k[tf] = pd.read_parquet(p)
        if "1h" not in k or not len(k["1h"]):
            log(f"  {sym}: no 1h klines, skipped")
            continue

        t = k["1h"]["open_time"].to_numpy().astype("int64")
        o, h, l, c, v = (k["1h"][x].to_numpy(float)
                         for x in ("open", "high", "low", "close", "volume"))
        price = float(c[-1])
        r1d = S.resample_ohlcv(t, o, h, l, c, v, DAY_MS)
        atr_d = float(V.atr(r1d["high"], r1d["low"], r1d["close"], 14)[-1])

        a = {"symbol": sym, "price": price,
             "price_at_utc": iso(int(t[-1])),
             "daily_atr": atr_d,
             "last_bar_utc": _last_bars(k),
             "vwap": {}, "structure": {}, "sessions": {}, "radar": [],
             "governor": {}, "funding": {}, "volatility": {}}

        part1, part2 = B2.brief2_asset(a, k, int(t[-1]), price, atr_d)
        a.update(part1)
        a["decision_instrument"] = part2
        a["substrate_used"] = part1["volume_windows"]["substrate_used"]
        a["partition_footprint"] = partition_footprint(
            int(t[-1]), [7, 30, 90, 365], warmup_days=0)
        if sym == "LITUSDT":
            a["known_wrong"] = {
                "applies_to": list(LIT_KNOWN_WRONG_KINDS),
                "not_marked": list(LIT_NOT_MARKED),
                "basis": "v4 §II.11 two-token trap; usable history begins "
                         "2025-12-01. Percentile/rank/bar-count depend on HOW "
                         "MUCH history exists and are known-wrong; levels and "
                         "volume-weighted quantities are correct numbers about "
                         "a real asset and are NOT marked."}
        doc["assets"][sym] = a
        doc["runtime_by_layer"][sym] = round(time.time() - s0, 2)
        log(f"  {sym}: {doc['runtime_by_layer'][sym]}s  "
            f"levels={part1['confluence'].get('level_count')}")

    doc["runtime_seconds"] = round(time.time() - t0, 2)
    return doc


def capture_path(date_str, slot, briefs_dir=BRIEFS_DIR):
    return briefs_dir / f"brief_{date_str}_{slot}.json"


def _rel(path):
    """Repo-relative when the path is inside the repo, absolute otherwise.

    Not cosmetic: a capture written outside ROOT (a fixture's tmp_path, or an
    operator pointing --briefs-dir elsewhere) must still produce a usable index
    line rather than raising ValueError out of relative_to.
    """
    p = Path(path)
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p).replace("\\", "/")


def serialize(doc):
    """Deterministic JSON.  sort_keys so two builds of the same capture are
    byte-identical, which is what F-B9's round-trip depends on."""
    return json.dumps(doc, indent=1, sort_keys=True, default=str,
                      ensure_ascii=False)


def write_capture(doc, briefs_dir=BRIEFS_DIR, force=False):
    briefs_dir.mkdir(parents=True, exist_ok=True)
    path = capture_path(doc["date"], doc["slot"], briefs_dir)
    if path.exists() and not force:
        raise SystemExit(
            f"REFUSED: {path.name} already exists. A same-slot re-run would "
            f"replace a stored capture and break archive comparability for "
            f"anything already published from it. Pass --force to confirm.")
    blob = serialize(doc)
    path.write_text(blob, encoding="utf-8", newline="\n")
    sha = hashlib.sha256(path.read_bytes()).hexdigest()

    line = {"date": doc["date"], "slot": doc["slot"],
            "generated_utc": doc["generated_utc"],
            "as_of_utc": doc.get("as_of_utc"),
            "rules_version": doc["rules_version"],
            "rules_sha256": doc["rules_sha256"],
            "analytics_version": doc["analytics_version"],
            "analytics_sha": doc["analytics_sha"],
            "schema_version": doc["schema_version"],
            "parity_certified": doc["parity_certified"],
            "universe": doc["universe"],
            "json_path": _rel(path),
            "json_sha256": sha}
    idx = briefs_dir / "index.jsonl"
    with idx.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(line, sort_keys=True) + "\n")
    return path, sha, line


def main():
    ap = argparse.ArgumentParser(description="Build a BRIEF-2 capture")
    ap.add_argument("--slot", required=True, choices=sorted(B2.SLOTS))
    ap.add_argument("--symbols", default=None,
                    help="comma-separated; default = the ten basket assets")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--backfill", action="store_true")
    ap.add_argument("--parity-certified", action="store_true",
                    help="ONLY after the operator's parity readings match")
    args = ap.parse_args()

    from engine.cells import SYMBOLS
    symbols = ([s.strip() for s in args.symbols.split(",")] if args.symbols
               else list(SYMBOLS))

    print(f"BRIEF-2 capture: slot={args.slot} symbols={len(symbols)}")
    doc = build_capture(symbols, args.slot, backfill=args.backfill,
                        parity_certified=args.parity_certified)
    path, sha, _ = write_capture(doc, force=args.force)
    print(f"\nwrote {path}")
    print(f"  sha256 {sha}")
    print(f"  runtime {doc['runtime_seconds']}s")
    if doc.get("banner"):
        print(f"\n  {doc['banner']}")


if __name__ == "__main__":
    main()
