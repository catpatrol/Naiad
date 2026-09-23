"""ORACLE ROSTER MAPPING + BACKFILL — OR-2 STEP 6 (ruling R-7, operator 2026-09-22).

Operations lane only. Two verbs, each run ONCE by hand, each leaving a record:

  probe     ONE GET of Binance USDT-M exchangeInfo. For every `--map DROPPED=LIVE` the
            operator ruled, the LIVE contract's record is copied out and MAPPED only when
            it reads contractType PERPETUAL, status TRADING, quoteAsset USDT. The other
            names the probe of record DROPPED are re-checked against the same response and
            printed with their near-name live contracts — NOT MAPPED: that is the
            operator's call, never this script's. Writes the mapping record (--out).

  backfill  Every mapped LIVE symbol x the Oracle's intervals (read off
            backfill_state.json, never typed) fetched to BTC-parity depth or listing,
            whichever is later — AMENDMENT A-OR1-1 i: holding the wrapper's single-flight
            lock so no two writers touch one parquet, honouring Binance's used-weight
            header (back off at 80%), no-clobber (every pre-existing kline parquet
            byte-identical after), contiguity verified, one line per pair. Appends the new
            pairs to research_outputs/oracle/backfill_state.json.

WHY A SCRIPT OF ITS OWN. OR-1 finding 4: "No Oracle fetch path honours X-MBX-USED-WEIGHT
or backs off at 80%: engine/data._get ignores headers and retries 429/418 blindly, and
step C's backfill ran outside the wrapper lock ... A future roster addition needs a
lane-local, header-aware backfiller under scripts/." engine/ is outside this lane's write
authority (BR-1 §2 clause 3), so the header-aware GET is installed IN THIS PROCESS ONLY
over engine.data._get; engine/data.py is not edited. scripts/backfill.py is NOT used: it
rewrites the tracked research_outputs/coverage/coverage.json and defaults to the study
basket.

It REFUSES a scoped NAIAD_CACHE_DIR (TIER-C10's frozen snapshot lives behind that
variable), never reads or writes oracle_daily.py, the top-up's manifest or its log, and
names no ticker but BTCUSDT (the parity anchor): every other symbol comes from its argv or
its records.

  ~/venvs/naiad/bin/python scripts/oracle_roster_backfill.py probe --ruling R-7 \\
      --map PUMPFUNUSDT=PUMPUSDT --out research_outputs/oracle/roster_mapping_2026-09-22.json
  ~/venvs/naiad/bin/python scripts/oracle_roster_backfill.py backfill \\
      --mapping research_outputs/oracle/roster_mapping_2026-09-22.json
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

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import requests                                   # noqa: E402

from engine import data as ED                     # noqa: E402

PROBE_OF_RECORD = ROOT / "research_outputs" / "oracle" / "roster_probe_2026-09-21.json"
BACKFILL_STATE = ROOT / "research_outputs" / "oracle" / "backfill_state.json"
EP_EXCHANGE_INFO = "/fapi/v1/exchangeInfo"
# A-OR1-1 i, verbatim: "honour Binance weight headers, back off at 80%". The 1-minute
# request-weight limit of USDT-M futures is 2400 (the exchangeInfo rateLimits row
# REQUEST_WEIGHT / MINUTE / 1 is read and PREFERRED when the probe has it).
WEIGHT_LIMIT_1M = 2400
WEIGHT_BACKOFF = 0.80
WEIGHT_HEADER = "X-MBX-USED-WEIGHT-1M"
UTC = timezone.utc


def iso(ms: int | None) -> str | None:
    return None if ms is None else datetime.fromtimestamp(ms / 1000, UTC).strftime("%Y-%m-%dT%H:%MZ")


def refuse_scoped_cache() -> Path:
    if os.environ.get("NAIAD_CACHE_DIR"):
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={os.environ['NAIAD_CACHE_DIR']!r} is set — this "
                         f"lane writes the LIVE cache only (TIER-C10's snapshot is frozen). Unset it.")
    live = Path.home() / ".cache" / "naiad" / "data_cache"
    if ED.cache_dir() != live:
        raise SystemExit(f"HALT: cache_dir() is {ED.cache_dir()}, not the live {live}")
    return live


# ═══════════════════════════════════════════ THE HEADER-AWARE GET (this process only)

class Weight:
    limit = WEIGHT_LIMIT_1M
    peak = 0
    calls = 0
    backoffs = 0


def weighted_get(url: str, params: dict | None = None, retries: int = 4) -> requests.Response:
    """engine.data._get's contract (200/404 returned, anything else retried then raised),
    plus A-OR1-1 i: on a fapi host the used-weight header is read after every answer and
    at or above WEIGHT_BACKOFF of the limit the process sleeps into the next minute; a
    429 honours Retry-After; a 418 (an IP ban) aborts at once."""
    last = None
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=60)
        except requests.RequestException as e:
            last = e
            time.sleep(1.5 * (attempt + 1))
            continue
        Weight.calls += 1
        used = r.headers.get(WEIGHT_HEADER)
        if used is not None:
            Weight.peak = max(Weight.peak, int(used))
            if int(used) >= WEIGHT_BACKOFF * Weight.limit:
                wait = 61 - datetime.now(UTC).second
                Weight.backoffs += 1
                print(f"    weight {used}/{Weight.limit} >= {WEIGHT_BACKOFF:.0%} — backing off {wait}s")
                time.sleep(wait)
        if r.status_code == 418:
            raise SystemExit(f"HALT: HTTP 418 from {url} — an IP ban; nothing more is fetched")
        if r.status_code == 429:
            wait = int(r.headers.get("Retry-After", "60"))
            print(f"    HTTP 429 — honouring Retry-After {wait}s")
            time.sleep(wait)
            last = RuntimeError(f"HTTP 429 for {url}")
            continue
        if r.status_code in (200, 404):
            return r
        last = RuntimeError(f"HTTP {r.status_code} for {url}")
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"failed after {retries} attempts: {url}") from last


# ═══════════════════════════════════════════════════════════════════ PROBE

def _record(s: dict) -> dict:
    keep = ("symbol", "baseAsset", "quoteAsset", "marginAsset", "contractType", "status",
            "onboardDate")
    out = {k: s.get(k) for k in keep}
    out["onboardDate_iso"] = iso(s.get("onboardDate"))
    return out


def probe(maps: list[str], ruling: str, out: Path) -> int:
    refuse_scoped_cache()
    pairs = []
    for m in maps:
        dropped, _, live = m.partition("=")
        if not dropped or not live:
            raise SystemExit(f"HALT: --map takes DROPPED=LIVE, got {m!r}")
        pairs.append((dropped.strip(), live.strip()))
    if not PROBE_OF_RECORD.exists():
        raise SystemExit(f"HALT: the probe of record {PROBE_OF_RECORD} is absent")
    rec = json.loads(PROBE_OF_RECORD.read_text(encoding="utf-8"))
    dropped_by_ruling = list(rec.get("dropped", ()))
    for d, _l in pairs:
        if d not in dropped_by_ruling:
            raise SystemExit(f"HALT: {d} is not a name the probe of record DROPPED "
                             f"({dropped_by_ruling}) — nothing to map")
    url = ED.REST_BASE + EP_EXCHANGE_INFO
    r = weighted_get(url)                           # THE one GET
    body = r.content
    doc = r.json()
    syms = {s["symbol"]: s for s in doc.get("symbols", [])}
    for rl in doc.get("rateLimits", []):
        if rl.get("rateLimitType") == "REQUEST_WEIGHT" and rl.get("interval") == "MINUTE" \
                and rl.get("intervalNum") == 1:
            Weight.limit = int(rl.get("limit", WEIGHT_LIMIT_1M))
    mappings, bad = [], []
    for d, live in pairs:
        s = syms.get(live)
        ok = bool(s) and s.get("contractType") == "PERPETUAL" and s.get("status") == "TRADING" \
            and s.get("quoteAsset") == "USDT"
        mappings.append({"dropped": d, "live": live, "verdict": "MAP" if ok else "REFUSED",
                         "operator_index": rec.get("operator_22", []).index(d)
                         if d in rec.get("operator_22", []) else None,
                         "record": _record(s) if s else None})
        if not ok:
            bad.append(f"{d} -> {live}: {'absent from exchangeInfo' if not s else _record(s)}")
    live_usdt = [k for k, s in syms.items() if s.get("contractType") == "PERPETUAL"
                 and s.get("status") == "TRADING" and s.get("quoteAsset") == "USDT"]
    not_mapped = []
    mapped_names = {d for d, _l in pairs}
    for f in rec.get("findings_reported_not_fixed", []):
        d = f.get("dropped")
        if d in mapped_names:
            continue
        near = []
        for n in f.get("near_name_live_contracts", []):
            now = syms.get(n.get("symbol"))
            near.append({"symbol": n.get("symbol"), "match_rules": n.get("match_rules"),
                         "string_match": n.get("string_match"),
                         "now": _record(now) if now else "ABSENT from this response"})
        not_mapped.append({"dropped": d, "near_name_live_contracts": near,
                           "note": "NOT MAPPED — a near-name is a string likeness, not an "
                                   "identity; mapping it is the operator's ruling, never this "
                                   "script's."})
    rec_out = {
        "class": "DISPLAY-ONLY / operations — ROSTER MAPPING (OR-2 STEP 6)",
        "ruling": ruling,
        "ruling_source": "exchange/queue/2026-09-22_OR2_oracle_rulings_ARGUS.md STEP 6 "
                         "(RATIFIED operator 2026-09-22, verbatim \"leans\")",
        "probe_of_record": str(PROBE_OF_RECORD.relative_to(ROOT)),
        "endpoint": url, "http_status": r.status_code,
        "probed_utc": datetime.now(UTC).isoformat(),
        "server_time_ms": doc.get("serverTime"),
        "response_bytes": len(body), "response_sha256": hashlib.sha256(body).hexdigest(),
        "symbols_in_response": len(syms), "live_usdt_perpetual_trading": len(live_usdt),
        "used_weight_1m": r.headers.get(WEIGHT_HEADER), "weight_limit_1m": Weight.limit,
        "rule": "MAP = the live contract present AND contractType == PERPETUAL AND status == "
                "TRADING AND quoteAsset == USDT; the operator named the pair (R-7)",
        "mappings": mappings, "not_mapped": not_mapped,
    }
    if bad:
        print("REFUSED: " + " · ".join(bad))
        return 2
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec_out, indent=1) + "\n", encoding="utf-8")
    b = out.read_bytes()
    print(f"probe: HTTP {r.status_code} · {len(body):,} B · sha256 {rec_out['response_sha256'][:16]}… · "
          f"{len(syms)} symbols ({len(live_usdt)} USDT PERPETUAL TRADING) · weight "
          f"{rec_out['used_weight_1m']}/{Weight.limit}")
    for m in mappings:
        rr = m["record"]
        print(f"MAPPED ({ruling}): {m['dropped']} -> {m['live']} · {rr['contractType']} · "
              f"{rr['status']} · base {rr['baseAsset']} · quote {rr['quoteAsset']} · onboard "
              f"{rr['onboardDate_iso']}")
    for nm in not_mapped:
        names = [f"{n['symbol']} ({n['now']['contractType']}·{n['now']['status']})"
                 if isinstance(n["now"], dict) else f"{n['symbol']} (ABSENT)"
                 for n in nm["near_name_live_contracts"]]
        print(f"NOT MAPPED (operator's call): {nm['dropped']} -> " + (", ".join(names) or "no near-name"))
    print(f"record -> {out.relative_to(ROOT)} · {len(b):,} B · sha256 {hashlib.sha256(b).hexdigest()}")
    return 0


# ═════════════════════════════════════════════════════════════════ BACKFILL

def _snapshot(kdir: Path) -> dict:
    return {p.name: (p.stat().st_size, p.stat().st_mtime_ns,
                     hashlib.sha256(p.read_bytes()).hexdigest())
            for p in sorted(kdir.glob("*.parquet"))}


def backfill(mapping: Path) -> int:
    import pandas as pd
    import oracle_topup as TU
    import oracle_wrapper as OW
    from engine.cells import INTERVAL_MS
    live_cache = refuse_scoped_cache()
    kdir = live_cache / "klines"
    doc = json.loads(mapping.read_text(encoding="utf-8"))
    symbols = [m["live"] for m in doc["mappings"] if m["verdict"] == "MAP"]
    onboard = {m["live"]: m["record"]["onboardDate"] for m in doc["mappings"] if m["verdict"] == "MAP"}
    state = json.loads(BACKFILL_STATE.read_text(encoding="utf-8"))
    intervals = list(state["intervals"])
    order = sorted(intervals, key=lambda tf: -INTERVAL_MS[tf])     # 4h, 1h, 15m, 5m
    btc_first = {p["interval"]: p["oldest"] for p in state["pairs"] if p["symbol"] == "BTCUSDT"}
    Weight.limit = int(doc.get("weight_limit_1m") or WEIGHT_LIMIT_1M)

    OW.reclaim_dead_lock(log=print)
    holder = OW.live_lock_holder()
    if holder is not None:
        print(f"HALT: the single-flight lock is held by a LIVE run ({holder}) — standing down")
        return 2
    if not OW.acquire_lock("backfill/or2-step6-R-7", log=print):
        print("HALT: could not take the single-flight lock")
        return 2
    real_get = ED._get
    lines, new_pairs, fail = [], [], False
    try:
        ED._get = weighted_get                      # this process only; engine/ untouched
        before = _snapshot(kdir)
        print(f"no-clobber snapshot: {len(before)} kline parquet(s), sha256 each")
        for sym in symbols:
            for tf in order:
                step = INTERVAL_MS[tf]
                ob_bar = (int(onboard[sym]) // step) * step
                btc = int(pd.Timestamp(btc_first[tf]).value // 1_000_000)
                first = ED.detect_first_candle(sym, tf)
                target = max(btc, ob_bar)
                basis = "max(BTC first bar, onboardDate floored to the bar)"
                if first is not None and first > target:
                    target, basis = first, "venue first candle, later than onboardDate"
                t0 = time.time()
                ED.backfill_klines(sym, tf, target, int(time.time() * 1000), log=lambda *a: None)
                df = TU.read_cached(sym, tf)
                gaps = TU.contiguity(df, tf)
                dups = int(df["open_time"].duplicated().sum())
                off = int((df["open_time"] % step != 0).sum())
                oldest, newest = int(df["open_time"].min()), int(df["open_time"].max())
                status = "AT_PARITY" if oldest <= target else "SHORT"
                ok = status == "AT_PARITY" and not gaps and not dups and not off
                fail |= not ok
                p = kdir / f"{sym}_{tf}.parquet"
                ln = (f"{sym} {tf:>3}  rows {len(df):>7,}  {iso(oldest)} -> {iso(newest)}  gaps "
                      f"{len(gaps)} dups {dups} off_grid {off}  parity {iso(target)} {status}  "
                      f"{time.time() - t0:5.1f}s  {'OK' if ok else 'FAIL'}")
                print(ln)
                lines.append(ln)
                new_pairs.append({"symbol": sym, "interval": tf, "new_in_or2_step6": True,
                                  "oldest": iso(oldest), "newest": iso(newest), "rows": int(len(df)),
                                  "gaps": len(gaps), "duplicates": dups, "off_grid": off,
                                  "onboardDate": iso(int(onboard[sym])), "parity_target": iso(target),
                                  "parity_basis": basis, "status": status,
                                  "days_short": round(max(0, oldest - target) / 86_400_000, 2),
                                  "file_sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
        after = _snapshot(kdir)
        clobbered = [k for k, v in before.items() if after.get(k) != v]
        added = sorted(set(after) - set(before))
        want_new = sorted(f"{s}_{tf}.parquet" for s in symbols for tf in intervals)
        print(f"no-clobber: {len(before)} pre-existing file(s), {len(clobbered)} changed "
              f"{clobbered[:3]}; {len(added)} added {added}")
        if clobbered or sorted(set(added)) != sorted(set(want_new) - set(before)):
            fail = True
            print("FAIL: the cache moved beyond the new pairs")
        print(f"weight: {Weight.calls} fapi/bulk call(s), peak used-weight {Weight.peak}/"
              f"{Weight.limit}, {Weight.backoffs} back-off(s)")
        if not fail:
            # the OPERATOR's order (the probe of record's 22), each mapped name in its dropped
            # name's place — never appended at the end
            rec = json.loads(PROBE_OF_RECORD.read_text(encoding="utf-8"))
            maps = {m["dropped"]: m["live"] for m in doc["mappings"] if m["verdict"] == "MAP"}
            kept = set(rec.get("kept", ()))
            roster = [maps.get(x, x) for x in rec.get("operator_22", ()) if x in kept or x in maps]
            state.update(
                written_utc=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                roster=roster,
                pairs=[p for p in state["pairs"] if p["symbol"] not in symbols] + new_pairs,
                remaining=[], complete=True,
                or2_step6={"ruling": doc["ruling"], "mapping_record": str(mapping.relative_to(ROOT)),
                           "symbols": symbols, "lock": "backfill/or2-step6-R-7",
                           "weight_peak_1m": Weight.peak, "weight_limit_1m": Weight.limit,
                           "backoffs": Weight.backoffs, "no_clobber": "every pre-existing "
                           "kline parquet byte-identical (sha256) after the run",
                           "lines": lines})
            BACKFILL_STATE.write_text(json.dumps(state, indent=1) + "\n", encoding="utf-8")
            print(f"state -> {BACKFILL_STATE.relative_to(ROOT)} · {len(state['pairs'])} pair(s)")
    finally:
        ED._get = real_get
        OW.release_lock(log=print)
    return 1 if fail else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="verb", required=True)
    pp = sub.add_parser("probe")
    pp.add_argument("--map", action="append", required=True, help="DROPPED=LIVE, as ruled")
    pp.add_argument("--ruling", required=True)
    pp.add_argument("--out", required=True, type=Path)
    pb = sub.add_parser("backfill")
    pb.add_argument("--mapping", required=True, type=Path)
    a = ap.parse_args(argv)
    if a.verb == "probe":
        return probe(a.map, a.ruling, (ROOT / a.out) if not a.out.is_absolute() else a.out)
    return backfill((ROOT / a.mapping) if not a.mapping.is_absolute() else a.mapping)


if __name__ == "__main__":
    raise SystemExit(main())
