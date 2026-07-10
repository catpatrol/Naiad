"""v12 Study V1 census engine (deliverables D2/D3/D4).

Touches metadata and bytes, never meaning: every scan in this module reads
ONLY the open_time / funding_time column plus raw file bytes for hashing.
No OHLCV value is ever materialized here (I3-safe on the lockbox by
construction).

Determinism (I7): given an unchanged estate, `run_census` writes byte-identical
outputs. No wall-clock timestamps enter the census body; retrieval dates live
in a write-once sidecar (`retrieval_meta.json`) keyed by file content hash —
they are only (re)stamped when a file's bytes change, i.e. on a real re-fetch.

Gap policy (D4): every gap is classified
  listing_edge   — begins within 24h of the series' first candle (contract
                   birth), expected and accepted;
  download_hole  — presumed fetchable; must be re-fetched (scripts/census.py
                   --repair);
  exchange_side  — survived >= 2 independent re-fetch attempts (attempt count
                   lives in refetch_log.json), documented and accepted.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from engine import data as phase1
from engine.cells import INTERVAL_MS
from study import loader

STUDY_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT",
                 "JTOUSDT", "TAOUSDT", "HYPEUSDT", "FARTCOINUSDT", "LITUSDT"]
STUDY_INTERVALS = ["1m", "5m", "15m", "1h", "4h", "12h"]

LISTING_EDGE_WINDOW_MS = 86_400_000          # gaps born within 24h of listing
FUNDING_HOUR_MS = 3_600_000
FUNDING_JITTER_MAX_MS = 60_000               # observed Binance jitter is ~ms

CENSUS_SCHEMA = "v12-census-1"


# ── sidecars ─────────────────────────────────────────────────────────────────

def load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def save_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
        f.write("\n")


def stamp_retrieval(meta: dict, rel_path: str, sha: str, source: str) -> dict:
    """Write-once per content version: a file keeps its recorded retrieval
    date until its bytes change."""
    ent = meta.get(rel_path)
    if ent is None or ent["sha256"] != sha:
        meta[rel_path] = {
            "sha256": sha,
            "source": source,
            "retrieved_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        }
    return meta[rel_path]


# ── timestamp-discipline scan (I4, fixture F4) ───────────────────────────────

def scan_timestamps(ts_file_order: np.ndarray, step: int) -> dict:
    """Anomalies on the raw stored order: duplicates, backward steps,
    off-grid stamps — each individually identified."""
    ts = ts_file_order.astype(np.int64)
    anomalies = {"duplicates": [], "backward": [], "off_grid": []}
    vals, counts = np.unique(ts, return_counts=True)
    for v, c in zip(vals[counts > 1], counts[counts > 1]):
        anomalies["duplicates"].append({"open_ms": int(v), "occurrences": int(c)})
    if len(ts) > 1:
        back = np.nonzero(np.diff(ts) < 0)[0]
        for i in back:
            anomalies["backward"].append({"open_ms": int(ts[i + 1]),
                                          "after_ms": int(ts[i])})
    off = np.nonzero(ts % step != 0)[0]
    for i in off:
        anomalies["off_grid"].append({"open_ms": int(ts[i])})
    return anomalies


def find_gaps(ts_sorted_unique: np.ndarray, step: int) -> list[dict]:
    gaps = []
    if len(ts_sorted_unique) > 1:
        d = np.diff(ts_sorted_unique)
        for i in np.nonzero(d > step)[0]:
            gaps.append({
                "gap_start_ms": int(ts_sorted_unique[i] + step),
                "gap_end_ms": int(ts_sorted_unique[i + 1] - step),
                "bars_missing": int(d[i] // step - 1),
            })
    return gaps


def classify_gap(gap: dict, series_first_ms: int, refetch: dict,
                 refetch_key: str) -> str:
    if gap["gap_start_ms"] <= series_first_ms + LISTING_EDGE_WINDOW_MS:
        return "listing_edge"
    attempts = refetch.get(refetch_key, {}).get("attempts", 0)
    return "exchange_side" if attempts >= 2 else "download_hole"


# ── kline census ─────────────────────────────────────────────────────────────

def census_kline_file(symbol: str, interval: str, refetch: dict,
                      meta: dict, default_source: str) -> dict:
    path = phase1._kline_path(symbol, interval)
    rel = f"klines/{path.name}"
    step = INTERVAL_MS[interval]
    sha = loader.file_sha256(path)
    m = stamp_retrieval(meta, rel, sha, default_source)

    ts = pd.read_parquet(path, columns=["open_time"])["open_time"].to_numpy()
    floor = loader.LIT_FLOOR_STUDY_MS if symbol == "LITUSDT" else 0
    in_scope = ts[(ts >= floor) & (ts < loader.EDGE_EXCL_MS)]
    anomalies = scan_timestamps(in_scope, step)
    su = np.unique(in_scope)

    gaps = find_gaps(su, step)
    first = int(su[0]) if len(su) else None
    for g in gaps:
        g["classification"] = classify_gap(
            g, first, refetch, f"{symbol}|{interval}|{g['gap_start_ms']}")
        g["gap_start_utc"] = loader.utc_str(g["gap_start_ms"])
        g["gap_end_utc"] = loader.utc_str(g["gap_end_ms"])

    parts = {loader.CLASS_EXPLORATION: 0, loader.CLASS_LOCKBOX: 0,
             loader.CLASS_SPENT: 0, loader.CLASS_CONTAMINATED: 0}
    if len(su):
        edges = [0, loader.LOCKBOX_START_MS, loader.LOCKBOX_END_EXCL_MS,
                 loader.EDGE_EXCL_MS]
        counts = np.histogram(su, bins=edges)[0]
        parts[loader.CLASS_EXPLORATION] = int(counts[0])
        parts[loader.CLASS_LOCKBOX] = int(counts[1])
        key = (loader.CLASS_SPENT if symbol == "BTCUSDT"
               else loader.CLASS_CONTAMINATED)
        parts[key] = int(counts[2])

    return {
        "path": rel, "symbol": symbol, "interval": interval,
        "sha256": sha, "source": m["source"], "retrieved_utc": m["retrieved_utc"],
        "first_open_ms": first,
        "first_open_utc": loader.utc_str(first) if first is not None else None,
        "last_open_ms": int(su[-1]) if len(su) else None,
        "last_open_utc": loader.utc_str(int(su[-1])) if len(su) else None,
        "rows": int(len(in_scope)),
        "partition_rows": parts,
        "gap_count": len(gaps),
        "largest_gap_bars": max((g["bars_missing"] for g in gaps), default=0),
        "gaps": gaps,
        "anomalies": anomalies,
        "anomaly_count": sum(len(v) for v in anomalies.values()),
    }


# ── funding census ───────────────────────────────────────────────────────────

def _funding_segments(snapped: np.ndarray) -> list[dict]:
    """Split the (snapped, hour-grid) series into stable-spacing segments.
    A run of >= 3 identical spacings anchors a segment; isolated deviations
    between segments are returned as anomalies/gaps by the caller."""
    if len(snapped) < 2:
        return []
    d = np.diff(snapped)
    segs = []
    i = 0
    while i < len(d):
        j = i
        while j + 1 < len(d) and d[j + 1] == d[i]:
            j += 1
        segs.append({"start_ms": int(snapped[i]), "end_ms": int(snapped[j + 1]),
                     "spacing_ms": int(d[i]), "records": int(j - i + 2)})
        i = j + 1
    return segs


def census_funding_file(symbol: str, refetch: dict, meta: dict,
                        default_source: str) -> dict:
    path = phase1._funding_path(symbol)
    rel = f"funding/{path.name}"
    sha = loader.file_sha256(path)
    m = stamp_retrieval(meta, rel, sha, default_source)

    ft = pd.read_parquet(path, columns=["funding_time"])["funding_time"] \
        .to_numpy().astype(np.int64)
    floor = loader.LIT_FLOOR_STUDY_MS if symbol == "LITUSDT" else 0
    ft = np.sort(ft[(ft >= floor) & (ft < loader.EDGE_EXCL_MS)])

    snapped = np.round(ft / FUNDING_HOUR_MS).astype(np.int64) * FUNDING_HOUR_MS
    jitter = np.abs(ft - snapped)
    max_jitter = int(jitter.max()) if len(ft) else 0

    raw_segs = _funding_segments(np.unique(snapped))
    # keep stable segments; fold isolated spacings into gaps when they are a
    # clean multiple of an adjacent stable spacing
    segments, gaps, anomalies = [], [], []
    for k, s in enumerate(raw_segs):
        if s["records"] >= 4:
            segments.append(s)
            continue
        neigh = [n["spacing_ms"] for n in
                 ([raw_segs[k - 1]] if k else []) +
                 ([raw_segs[k + 1]] if k + 1 < len(raw_segs) else [])
                 if n["records"] >= 4]
        base = min(neigh) if neigh else None
        if base and s["spacing_ms"] % base == 0 and s["spacing_ms"] > base:
            missing = s["spacing_ms"] // base - 1
            gaps.append({
                "gap_start_ms": s["start_ms"] + base,
                "gap_start_utc": loader.utc_str(s["start_ms"] + base),
                "gap_end_ms": s["end_ms"] - base,
                "gap_end_utc": loader.utc_str(s["end_ms"] - base),
                "records_missing": missing * (s["records"] - 1),
                "local_grid_hours": base // FUNDING_HOUR_MS,
            })
        else:
            anomalies.append({
                "start_ms": s["start_ms"], "start_utc": loader.utc_str(s["start_ms"]),
                "end_ms": s["end_ms"], "end_utc": loader.utc_str(s["end_ms"]),
                "spacing_hours": s["spacing_ms"] / FUNDING_HOUR_MS,
                "records": s["records"],
            })
    for g in gaps:
        first = int(ft[0]) if len(ft) else 0
        g["classification"] = classify_gap(
            {"gap_start_ms": g["gap_start_ms"]}, first, refetch,
            f"{symbol}|funding|{g['gap_start_ms']}")

    return {
        "path": rel, "symbol": symbol,
        "sha256": sha, "source": m["source"], "retrieved_utc": m["retrieved_utc"],
        "first_ms": int(ft[0]) if len(ft) else None,
        "first_utc": loader.utc_str(int(ft[0])) if len(ft) else None,
        "last_ms": int(ft[-1]) if len(ft) else None,
        "last_utc": loader.utc_str(int(ft[-1])) if len(ft) else None,
        "records": int(len(ft)),
        "max_jitter_ms": max_jitter,
        "jitter_over_tolerance": bool(max_jitter > FUNDING_JITTER_MAX_MS),
        "grid_segments": [
            {"start_utc": loader.utc_str(s["start_ms"]),
             "end_utc": loader.utc_str(s["end_ms"]),
             "spacing_hours": s["spacing_ms"] / FUNDING_HOUR_MS,
             "records": s["records"]} for s in segments],
        "gap_count": len(gaps),
        "gaps": gaps,
        "anomalies": anomalies,
    }


# ── the census proper ────────────────────────────────────────────────────────

def run_census(out_dir: Path, sidecar_dir: Path,
               symbols: list[str] | None = None,
               intervals: list[str] | None = None,
               data_starts_csv: Path | None = None,
               default_source: str = "binance_vision_bulk+rest_topup") -> dict:
    """Scan the estate; write census.json / DATA_CENSUS.md / GAP_REPORT.md
    into out_dir. Sidecars (retrieval_meta.json, refetch_log.json) live in
    sidecar_dir and survive across runs."""
    symbols = symbols or STUDY_SYMBOLS
    intervals = intervals or STUDY_INTERVALS
    out_dir.mkdir(parents=True, exist_ok=True)

    meta_path = sidecar_dir / "retrieval_meta.json"
    refetch_path = sidecar_dir / "refetch_log.json"
    meta = load_json(meta_path, {})
    refetch = load_json(refetch_path, {})

    klines = [census_kline_file(s, iv, refetch, meta, default_source)
              for s in symbols for iv in intervals]
    funding = [census_funding_file(s, refetch, meta, default_source)
               for s in symbols]

    coverage_ok = None
    if data_starts_csv and data_starts_csv.exists():
        starts = pd.read_csv(data_starts_csv)
        exp = {(r.symbol, r.interval): int(r.first_valid_ms)
               for r in starts.itertuples()}
        coverage_ok = {}
        for k in klines:
            key = (k["symbol"], k["interval"])
            if key not in exp:
                continue
            want_first = max(exp[key],
                             loader.LIT_FLOOR_STUDY_MS
                             if k["symbol"] == "LITUSDT" else 0)
            step = INTERVAL_MS[k["interval"]]
            want_last = (loader.EDGE_EXCL_MS - 1) // step * step
            coverage_ok[f"{k['symbol']}_{k['interval']}"] = bool(
                k["first_open_ms"] == want_first
                and k["last_open_ms"] == want_last)

    census = {
        "schema": CENSUS_SCHEMA,
        "header": {
            "study": "v12", "phase": "V1",
            "engine_anchor": "engine 1.0.1 @ da31062 (signal logic untouched)",
            "boundaries": {
                "exploration_end_excl_ms": loader.LOCKBOX_START_MS,
                "lockbox_start_ms": loader.LOCKBOX_START_MS,
                "lockbox_end_excl_ms": loader.LOCKBOX_END_EXCL_MS,
                "study_right_edge_excl_ms": loader.EDGE_EXCL_MS,
                "lit_floor_ms": loader.LIT_FLOOR_STUDY_MS,
            },
            "storage_convention": (
                "Phase 1 parquet cache: klines/{SYMBOL}_{interval}.parquet "
                "(open_time ms UTC + OHLCV float64), funding/{SYMBOL}.parquet "
                "(funding_time ms UTC + funding_rate). Cache lives outside "
                "the repo (NAIAD_CACHE_DIR)."),
            "conventions_added": [
                "retrieval_meta.json sidecar (write-once per content hash)",
                "refetch_log.json sidecar (gap re-fetch attempt ledger)",
                "guard_log.jsonl in the cache dir (loader guard events)",
                "census artifacts at repo root: census.json, DATA_CENSUS.md, "
                "GAP_REPORT.md, SPOT_CHECK.md",
            ],
            "value_read_policy": (
                "census scans read only open_time / funding_time columns and "
                "raw bytes for SHA256; no OHLCV value is materialized (I3)"),
            "note_hash_scope": (
                "sha256 covers whole cache files as of this census; rows/"
                "first/last describe the in-scope slice (>= LIT floor, "
                "< right edge)"),
        },
        "klines": klines,
        "funding": funding,
        "coverage_ok": coverage_ok,
    }

    save_json(out_dir / "census.json", census)
    save_json(meta_path, meta)
    if not refetch_path.exists():
        save_json(refetch_path, refetch)
    (out_dir / "DATA_CENSUS.md").write_text(render_census_md(census),
                                            encoding="utf-8", newline="\n")
    (out_dir / "GAP_REPORT.md").write_text(render_gap_report(census),
                                           encoding="utf-8", newline="\n")
    return census


# ── verification (fixture F8) ────────────────────────────────────────────────

def verify_hashes(census: dict) -> list[dict]:
    """Re-hash every estate file against the manifest; return mismatches."""
    bad = []
    for section, key in (("klines", "path"), ("funding", "path")):
        for ent in census[section]:
            p = phase1.cache_dir() / ent[key]
            actual = loader.file_sha256(p) if p.exists() else "(missing)"
            if actual != ent["sha256"]:
                bad.append({"path": ent[key], "expected": ent["sha256"],
                            "actual": actual})
    return bad


# ── human-readable renderings (D2, D4) ───────────────────────────────────────

def render_census_md(census: dict) -> str:
    b = census["header"]["boundaries"]
    lines = [
        "# DATA_CENSUS — v12 Study, Phase V1",
        "",
        f"Partition boundaries (candle open time, UTC): exploration-classic "
        f"< {loader.utc_str(b['lockbox_start_ms'])} · lockbox "
        f"{loader.utc_str(b['lockbox_start_ms'])} → "
        f"{loader.utc_str(b['lockbox_end_excl_ms'] - 1000)} · spent(BTC)/"
        f"regime-contaminated(non-BTC) → "
        f"{loader.utc_str(b['study_right_edge_excl_ms'] - 1000)} · "
        f"LIT floor {loader.utc_str(b['lit_floor_ms'])}.",
        "",
        "Machine manifest of record: `census.json` (same directory). "
        "Gap detail: `GAP_REPORT.md`.",
        "",
        "## Candle series (60)",
        "",
        "| Symbol | TF | First (UTC) | Last (UTC) | Rows | Gaps | Largest gap"
        " | Expl-classic | Lockbox | Spent/Contam | Source | SHA256[:12] |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for k in census["klines"]:
        p = k["partition_rows"]
        sc = p[loader.CLASS_SPENT] + p[loader.CLASS_CONTAMINATED]
        lines.append(
            f"| {k['symbol']} | {k['interval']} | {k['first_open_utc']} | "
            f"{k['last_open_utc']} | {k['rows']} | {k['gap_count']} | "
            f"{k['largest_gap_bars']} | {p[loader.CLASS_EXPLORATION]} | "
            f"{p[loader.CLASS_LOCKBOX]} | {sc} | {k['source']} | "
            f"{k['sha256'][:12]} |")
    lines += [
        "",
        "## Funding series (10)",
        "",
        "| Symbol | First (UTC) | Last (UTC) | Records | Grid | Gaps |"
        " Max jitter (ms) | SHA256[:12] |",
        "|---|---|---|---:|---|---:|---:|---|",
    ]
    for f in census["funding"]:
        grid = " → ".join(f"{s['spacing_hours']:g}h×{s['records']}"
                          for s in f["grid_segments"]) or "(single record)"
        lines.append(
            f"| {f['symbol']} | {f['first_utc']} | {f['last_utc']} | "
            f"{f['records']} | {grid} | {f['gap_count']} | "
            f"{f['max_jitter_ms']} | {f['sha256'][:12]} |")

    expl = sorted({k["symbol"] for k in census["klines"]
                   if k["partition_rows"][loader.CLASS_EXPLORATION] > 0})
    no_expl = [s for s in STUDY_SYMBOLS
               if s in {k["symbol"] for k in census["klines"]}
               and s not in expl]
    lines += [
        "",
        "## Summary",
        "",
        f"Exploration-classic history (free to mine) comes from "
        f"{', '.join(expl) if expl else 'no asset'}. "
        f"{', '.join(no_expl) if no_expl else 'No asset'} contribute(s) no "
        "exploration-classic rows: their pre-2025-10-06 history either sits "
        "inside the sealed lockbox (HYPE, FARTCOIN list dates fall in the "
        "lockbox window) or does not exist under the study floor (LIT is "
        "Lighter-only from 2025-12-23). Those assets are exploration-eligible "
        "only in the regime-contaminated slice (2025-10-06 → 2026-07-07) and "
        "are therefore validation-only / contaminated-only: panel findings on "
        "them are held to the structural (mechanism-level) standard of the "
        "charter addendum, not absolute-expectancy claims. BTCUSDT rows in "
        "2025-10-06 → 2026-07-07 are spent (characterization only, forever).",
        "",
    ]
    return "\n".join(lines)


def render_gap_report(census: dict) -> str:
    lines = [
        "# GAP_REPORT — v12 Study, Phase V1 (deliverable D4)",
        "",
        "Policy: `listing_edge` (gap begins within 24h of the contract's "
        "first candle) — expected, accepted. `download_hole` — must be "
        "re-fetched (`scripts/census.py --repair`); a hole surviving two "
        "independent re-fetch attempts escalates to `exchange_side` — "
        "documented, accepted. Phase verdict requires zero unresolved "
        "`download_hole` entries.",
        "",
        "## Candle gaps",
        "",
    ]
    any_gap = False
    for k in census["klines"]:
        for g in k["gaps"]:
            any_gap = True
            lines.append(
                f"- **{k['symbol']} {k['interval']}** — missing "
                f"{g['bars_missing']} bar(s), {g['gap_start_utc']} → "
                f"{g['gap_end_utc']} — `{g['classification']}`")
    if not any_gap:
        lines.append("(none)")
    lines += ["", "## Funding gaps", ""]
    any_f = False
    for f in census["funding"]:
        for g in f["gaps"]:
            any_f = True
            lines.append(
                f"- **{f['symbol']} funding** — missing "
                f"{g['records_missing']} record(s) on the "
                f"{g['local_grid_hours']}h grid, {g['gap_start_utc']} → "
                f"{g['gap_end_utc']} — `{g['classification']}`")
        for a in f["anomalies"]:
            any_f = True
            lines.append(
                f"- **{f['symbol']} funding** — irregular spacing "
                f"{a['spacing_hours']:g}h over {a['records']} record(s), "
                f"{a['start_utc']} → {a['end_utc']} — `grid_shift` "
                "(exchange-side funding-interval change, documented)")
    if not any_f:
        lines.append("(none)")
    lines += ["", "## Timestamp-discipline anomalies", ""]
    any_a = False
    for k in census["klines"]:
        a = k["anomalies"]
        for d in a["duplicates"]:
            any_a = True
            lines.append(f"- {k['symbol']} {k['interval']}: duplicate open "
                         f"{loader.utc_str(d['open_ms'])} ×{d['occurrences']}")
        for d in a["backward"]:
            any_a = True
            lines.append(f"- {k['symbol']} {k['interval']}: backward stamp "
                         f"{loader.utc_str(d['open_ms'])}")
        for d in a["off_grid"]:
            any_a = True
            lines.append(f"- {k['symbol']} {k['interval']}: off-grid stamp "
                         f"open_ms={d['open_ms']}")
    if not any_a:
        lines.append("(none)")
    lines.append("")
    return "\n".join(lines)
