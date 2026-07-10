"""v12 Study V1 census CLI (deliverables D1–D4).

  python scripts/census.py                 # scan estate, write census.json,
                                           # DATA_CENSUS.md, GAP_REPORT.md
  python scripts/census.py --repair        # re-fetch download_hole gaps via
                                           # REST, log attempts, re-census
  python scripts/census.py --verify        # re-hash estate vs census.json
  python scripts/census.py --extend        # top up any series short of the
                                           # coverage target (resumable)

Census artifacts land at the repo root; sidecars (retrieval_meta.json,
refetch_log.json) in research_outputs/census/. All scans are timestamp-and-
bytes only (I3-safe).
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd

from engine import data as phase1
from engine.cells import INTERVAL_MS
from study import census as cz
from study import loader

ROOT = Path(__file__).resolve().parent.parent
SIDECARS = ROOT / "research_outputs" / "census"


def extend_estate() -> None:
    """D1: bring every series to the coverage target (resumable; the census
    re-verifies afterwards). Downloads may run past the right edge — forward
    rows are Naiad's and stay outside the manifest."""
    end_ms = loader.EDGE_EXCL_MS  # backfill clamps to last closed bar itself
    for sym in cz.STUDY_SYMBOLS:
        first = phase1.detect_first_candle(sym, "1h") or 0
        phase1.backfill_funding(sym, phase1.first_valid_ms(sym, "1h", first),
                                end_ms - 1)
        for iv in cz.STUDY_INTERVALS:
            detected = phase1.detect_first_candle(sym, iv)
            if detected is None:
                print(f"  {sym} {iv}: no futures data — skipped")
                continue
            start_ms = phase1.first_valid_ms(sym, iv, detected)
            phase1.backfill_klines(sym, iv, start_ms, end_ms - 1)
            print(f"  {sym} {iv}: covered")


def repair_holes() -> None:
    """D4: two independent REST re-fetch attempts per download_hole, with an
    attempt ledger; holes still missing after two attempts become
    exchange_side at the next census render."""
    census_path = ROOT / "census.json"
    if not census_path.exists():
        print("run the census first"); return
    census = cz.load_json(census_path, {})
    refetch = cz.load_json(SIDECARS / "refetch_log.json", {})
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for k in census.get("klines", []):
        sym, iv = k["symbol"], k["interval"]
        step = INTERVAL_MS[iv]
        for g in k["gaps"]:
            if g["classification"] != "download_hole":
                continue
            key = f"{sym}|{iv}|{g['gap_start_ms']}"
            ent = refetch.setdefault(key, {"attempts": 0, "dates": [],
                                           "result": "still_missing"})
            while ent["attempts"] < 2 and ent["result"] == "still_missing":
                df = phase1._fetch_rest_klines(
                    sym, iv, g["gap_start_ms"], g["gap_end_ms"])
                ent["attempts"] += 1
                ent["dates"].append(today)
                got = df["open_time"].to_numpy() if len(df) else np.array([])
                want = np.arange(g["gap_start_ms"], g["gap_end_ms"] + step, step)
                hit = np.isin(want, got)
                if hit.any():
                    cache = pd.read_parquet(phase1._kline_path(sym, iv))
                    merged = pd.concat([cache, df[df["open_time"].isin(want)]],
                                       ignore_index=True)
                    phase1._save_cache(sym, iv, merged)
                    ent["result"] = ("filled" if hit.all()
                                     else "partially_filled")
                    print(f"  {key}: fetched {int(hit.sum())}/{len(want)} bars")
                else:
                    print(f"  {key}: attempt {ent['attempts']} — exchange "
                          "returned nothing for the range")

    for f in census.get("funding", []):
        sym = f["symbol"]
        for g in f["gaps"]:
            if g["classification"] != "download_hole":
                continue
            key = f"{sym}|funding|{g['gap_start_ms']}"
            ent = refetch.setdefault(key, {"attempts": 0, "dates": [],
                                           "result": "still_missing"})
            while ent["attempts"] < 2 and ent["result"] == "still_missing":
                before = phase1._funding_path(sym).stat().st_size
                phase1.backfill_funding(sym, g["gap_start_ms"] - 1,
                                        g["gap_end_ms"] + 1, log=None)
                ent["attempts"] += 1
                ent["dates"].append(today)
                ft = pd.read_parquet(phase1._funding_path(sym),
                                     columns=["funding_time"])["funding_time"]
                inside = ft[(ft >= g["gap_start_ms"]) &
                            (ft <= g["gap_end_ms"])]
                if len(inside):
                    ent["result"] = "filled"
                    print(f"  {key}: filled ({len(inside)} records)")
                else:
                    print(f"  {key}: attempt {ent['attempts']} — exchange "
                          "returned nothing for the range")

    cz.save_json(SIDECARS / "refetch_log.json", refetch)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--extend", action="store_true")
    ap.add_argument("--repair", action="store_true")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    if args.verify:
        census = cz.load_json(ROOT / "census.json", None)
        if census is None:
            print("no census.json"); return 1
        bad = cz.verify_hashes(census)
        for b in bad:
            print(f"HASH MISMATCH {b['path']}: manifest {b['expected'][:12]} "
                  f"actual {b['actual'][:12]}")
        print(f"{len(bad)} mismatch(es) across "
              f"{len(census['klines']) + len(census['funding'])} files")
        return 1 if bad else 0

    if args.extend:
        extend_estate()
    if args.repair:
        repair_holes()

    census = cz.run_census(out_dir=ROOT, sidecar_dir=SIDECARS,
                           data_starts_csv=ROOT / "data_starts.csv")
    holes = sum(1 for k in census["klines"] for g in k["gaps"]
                if g["classification"] == "download_hole")
    holes += sum(1 for f in census["funding"] for g in f["gaps"]
                 if g["classification"] == "download_hole")
    n_anom = sum(k["anomaly_count"] for k in census["klines"])
    cov = census["coverage_ok"] or {}
    short = [k for k, ok in cov.items() if not ok]
    print(f"census: {len(census['klines'])} kline series, "
          f"{len(census['funding'])} funding series")
    print(f"unresolved download_hole gaps: {holes}")
    print(f"timestamp anomalies: {n_anom}")
    print(f"coverage vs data_starts + right edge: "
          f"{len(cov) - len(short)}/{len(cov)} ok"
          + (f" — SHORT: {', '.join(short)}" if short else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
