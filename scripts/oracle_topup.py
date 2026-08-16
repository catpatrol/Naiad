"""THE ORACLE TOP-UP — D-1 of queue BR-1b. Fetch-and-store, and nothing else.

BR-1b, verbatim:

    Fetch-and-store ONLY: scope = EXACTLY the (symbol, interval) set enumerated
    from oracle_daily.py's cache reads this session — to claim the set,
    enumerate the set. Slots 06:45 + 15:45 America/Argentina/Buenos_Aires via
    the slot-anchored wrapper. No journal import, no aggregation, no publish,
    no exchange/ writes. Network failure: log to
    research_outputs/oracle/calibration/topup_log.jsonl, exit nonzero; the
    Oracle is unaffected and stamps its as-of. Not this contract: no schema
    change, no new intervals, no touch of com.naiad.daily.

════════════════════════════════════════════════════════════════════════════
WHY THIS EXISTS. Finding V-8 of the ORACLE REBIRTH build: the kline estate was
a day stale and nothing scheduled refreshed it, because the network top-up job
was retired 2026-08-05 (ruling D-3). The Oracle is CACHE-ONLY BY DESIGN — a
firewalled run must never reach the network — so the fetching cannot live
inside it. It lives here, 15 minutes ahead of each Oracle slot.

════════════════════════════════════════════════════════════════════════════
"TO CLAIM THE SET, ENUMERATE THE SET."

A hardcoded symbol/interval list would be a claim about oracle_daily.py that
rots the moment that file changes. So the scope is obtained by INSTRUMENTING
oracle_daily's own `load_lens` on a real run and recording every (symbol,
interval) it actually touches — see `enumerate_scope()`. The result is pinned
to a manifest that also records the sha256 of the file it was enumerated from.

    IF oracle_daily.py's sha256 NO LONGER MATCHES THE PIN, THIS SCRIPT HALTS.

It does not guess, does not fall back to a default list, and does not fetch a
superset "to be safe". A superset would be a silent scope change, which is
precisely what the contract forbids. F-TU-1 re-enumerates and diffs every run.

WHAT THIS MODULE NEVER DOES: it never imports a journal, never aggregates
anything, never publishes, never writes under exchange/, never touches
com.naiad.daily, never adds an interval the Oracle does not read, and never
shrinks or rewrites a bar that already existed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from engine.data import cache_dir, backfill_klines, KLINE_COLS   # noqa: E402
from engine.cells import INTERVAL_MS                              # noqa: E402

SCOPE_MANIFEST = ROOT / "research_outputs" / "oracle" / "topup_scope.json"
TOPUP_LOG = ROOT / "research_outputs" / "oracle" / "calibration" / "topup_log.jsonl"
ORACLE_SRC = ROOT / "scripts" / "oracle_daily.py"

# How far back each fetch reaches from the newest cached bar. Enough to re-pull
# the last closed bars and any bar that was still forming when the previous run
# stored it; NOT a re-download of history.
OVERLAP_BARS = 12

REGISTER: dict[str, dict] = {
    "OVERLAP_BARS": {
        "value": OVERLAP_BARS,
        "ruled": False,
        "source": "PROPOSED by the BR-1b build 2026-08-16 — UNRULED [VETO]. The fetch "
                  "starts OVERLAP_BARS before the newest cached bar so that a bar stored "
                  "while still forming is re-pulled once closed. engine.data's cache "
                  "merge is keep='last' on open_time, so overlap is corrective, not "
                  "duplicative. 12 bars is ~1h at 5m and ~2d at 4h.",
    },
    "SLOTS": {
        "value": ("06:45", "15:45"),
        "ruled": True,
        "source": "BR-1b verbatim: 'Slots 06:45 + 15:45 America/Argentina/Buenos_Aires "
                  "via the slot-anchored wrapper' — 15 minutes ahead of the Oracle's "
                  "07:00 and 16:00 so the cache is fresh before the organ reads it.",
    },
    "SCOPE_SOURCE": {
        "value": "instrumented oracle_daily.load_lens",
        "ruled": True,
        "source": "BR-1b verbatim: 'to claim the set, enumerate the set'.",
    },
}


# ══════════════════════════════════════════════════════════ THE ENUMERATION

def enumerate_scope(log=print) -> dict:
    """Run the Oracle with a spy on its cache reader and record what it touches.

    This is the ONLY way the scope is ever established. It is deliberately
    expensive and deliberately real: a static read of the source would miss a
    conditional read, and a hardcoded list would miss a change.
    """
    import oracle_daily as OD

    seen: dict[tuple[str, str], int] = {}
    orig = OD.load_lens

    def spy(sym, tf, tail=None):
        seen[(sym, tf)] = seen.get((sym, tf), 0) + 1
        return orig(sym, tf, tail=tail)

    OD.load_lens = spy
    try:
        OD.run(slot="scope-enumeration", log=lambda *a, **k: None)
    finally:
        OD.load_lens = orig
        # The enumeration run emits a calibration JSON under a slot name that is
        # not a real slot. It is not evidence of anything and BR-2 must not read
        # it, so it is removed by the attended builder that created it seconds
        # earlier. Scheduled paths never delete (CADENCE §4); `--enumerate` is an
        # attended command.
        stray = (ROOT / "research_outputs" / "oracle" / "calibration"
                 / f"oracle_calibration_{datetime.now().astimezone():%Y-%m-%d}_"
                   f"scope-enumeration.json")
        if stray.exists():
            stray.unlink()

    pairs = sorted(seen)
    doc = {
        "class": "SCOPE MANIFEST — the (symbol, interval) set the Oracle actually reads",
        "method": "instrumented oracle_daily.load_lens over one full oracle_daily.run()",
        "enumerated_utc": datetime.now(timezone.utc).isoformat(),
        "oracle_daily_sha256": sha256_file(ORACLE_SRC),
        "pairs": [list(p) for p in pairs],
        "symbols": sorted({s for s, _ in pairs}),
        "intervals": sorted({t for _, t in pairs}),
        "read_counts": {f"{s}|{t}": n for (s, t), n in sorted(seen.items())},
        "note": "30m is ABSENT on purpose: the Oracle derives it from 15m by resample "
                "(census_build.RESAMPLE), so there is no 30m parquet to top up. 1m and "
                "12h are absent because the Oracle does not read them.",
    }
    log(f"  enumerated {len(pairs)} pair(s): {len(doc['symbols'])} symbol(s) x "
        f"{len(doc['intervals'])} interval(s) {doc['intervals']}")
    return doc


def sha256_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write_scope(doc: dict) -> tuple[Path, str, int]:
    SCOPE_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    b = json.dumps(doc, indent=1, sort_keys=True).encode("utf-8")
    SCOPE_MANIFEST.write_bytes(b)
    return SCOPE_MANIFEST, hashlib.sha256(b).hexdigest(), len(b)


def load_scope() -> list[tuple[str, str]]:
    """Read the pinned scope, HALTING if it is missing or stale.

    A missing manifest is not a reason to guess, and a changed oracle_daily.py
    is not a reason to carry on with yesterday's scope.
    """
    if not SCOPE_MANIFEST.exists():
        raise SystemExit(
            f"HALT: no scope manifest at {SCOPE_MANIFEST}. The scope is ENUMERATED, "
            f"never assumed — run `oracle_topup.py --enumerate` first.")
    doc = json.loads(SCOPE_MANIFEST.read_text())
    now = sha256_file(ORACLE_SRC)
    if doc.get("oracle_daily_sha256") != now:
        raise SystemExit(
            f"HALT: oracle_daily.py has changed since the scope was enumerated.\n"
            f"  pinned  {doc.get('oracle_daily_sha256')}\n  current {now}\n"
            f"The top-up will not fetch a scope it cannot vouch for. Re-run "
            f"`oracle_topup.py --enumerate`.")
    return [(s, t) for s, t in doc["pairs"]]


# ══════════════════════════════════════════════════════════ THE CACHE FACTS

def kline_path(sym: str, tf: str) -> Path:
    return cache_dir() / "klines" / f"{sym}_{tf}.parquet"


def read_cached(sym: str, tf: str) -> pd.DataFrame | None:
    p = kline_path(sym, tf)
    if not p.exists():
        return None
    return pd.read_parquet(p).sort_values("open_time").reset_index(drop=True)


def contiguity(df: pd.DataFrame, tf: str) -> list[dict]:
    """Every gap in the series at its own interval step. Empty list = gap-free."""
    step = INTERVAL_MS[tf]
    ot = df["open_time"].to_numpy("int64")
    if len(ot) < 2:
        return []
    d = ot[1:] - ot[:-1]
    gaps = []
    for i in (d != step).nonzero()[0]:
        i = int(i)
        gaps.append({
            "after_ms": int(ot[i]),
            "after_iso": datetime.fromtimestamp(ot[i] / 1000, timezone.utc).isoformat(),
            "missing_bars": int(round(d[i] / step)) - 1,
            "span_ms": int(d[i]),
        })
    return gaps


def fingerprint(df: pd.DataFrame) -> str:
    """A sha over the whole frame, for the no-clobber proof."""
    b = df[KLINE_COLS].to_csv(index=False).encode("utf-8")
    return hashlib.sha256(b).hexdigest()


def noclobber_verdict(before: pd.DataFrame, after: pd.DataFrame) -> dict:
    """G-TU-2, as a PURE function so a fixture can drive it with synthetic frames.

    Three distinct things, deliberately not conflated:
      shrank            — the series lost rows. Always a clobber.
      rewrote           — a bar STRICTLY OLDER than the previous newest changed
                          value. Always a clobber: closed bars are immutable.
      forming_corrected — the previously-newest bar changed. NOT a clobber: it
                          was stored while still forming and the top-up's whole
                          purpose is to replace it with the closed version.
    """
    if before is None or before.empty:
        return {"shrank": False, "rewrote": False, "forming_corrected": False}
    newest_before = int(before["open_time"].iloc[-1])
    shrank = len(after) < len(before)
    stable_before = before[before["open_time"] < newest_before].reset_index(drop=True)
    stable_after = after[after["open_time"] < newest_before].reset_index(drop=True)
    rewrote = (len(stable_after) != len(stable_before)
               or fingerprint(stable_before) != fingerprint(stable_after))
    overlap_after = after[after["open_time"] <= newest_before].reset_index(drop=True)
    forming = (len(overlap_after) == len(before)
               and fingerprint(overlap_after) != fingerprint(before)
               and not rewrote)
    return {"shrank": bool(shrank), "rewrote": bool(rewrote),
            "forming_corrected": bool(forming)}


# ═════════════════════════════════════════════════════════════ THE TOP-UP

def topup_pair(sym: str, tf: str, log=print) -> dict:
    """Fetch-and-store one pair, then prove nothing was clobbered."""
    before = read_cached(sym, tf)
    step = INTERVAL_MS[tf]
    row: dict = {"symbol": sym, "interval": tf}

    if before is None or before.empty:
        row.update({"status": "ABSENT", "detail": "no cached parquet; not created by "
                                                  "the top-up (no schema change, "
                                                  "no new intervals)"})
        return row

    n_before = len(before)
    newest_before = int(before["open_time"].iloc[-1])
    # The overlap is corrective, not a re-download: engine.data merges keep='last'.
    start_ms = newest_before - OVERLAP_BARS * step
    end_ms = int(datetime.now(timezone.utc).timestamp() * 1000)

    # The pre-existing rows, kept for the no-clobber comparison. Everything at or
    # before `newest_before` must survive byte-identical.
    backfill_klines(sym, tf, start_ms, end_ms, log=lambda *a, **k: None)

    after = read_cached(sym, tf)
    n_after = len(after)
    newest_after = int(after["open_time"].iloc[-1])

    v = noclobber_verdict(before, after)
    shrank, rewrote, forming_changed = v["shrank"], v["rewrote"], v["forming_corrected"]
    gaps = contiguity(after, tf)
    row.update({
        "status": "OK" if not (shrank or rewrote) else "CLOBBER",
        "rows_before": n_before, "rows_after": n_after,
        "rows_added": n_after - n_before,
        "newest_before_ms": newest_before,
        "newest_before_iso": datetime.fromtimestamp(newest_before / 1000,
                                                    timezone.utc).isoformat(),
        "newest_after_ms": newest_after,
        "newest_after_iso": datetime.fromtimestamp(newest_after / 1000,
                                                   timezone.utc).isoformat(),
        "advanced_bars": int((newest_after - newest_before) // step),
        "shrank": bool(shrank),
        "rewrote_closed_bars": bool(rewrote),
        "forming_bar_corrected": bool(forming_changed and not rewrote),
        "gaps": gaps,
        "gap_count": len(gaps),
    })
    return row


def run(slot: str = "topup", log=print) -> dict:
    pairs = load_scope()
    log(f"ORACLE TOP-UP · slot={slot} · {len(pairs)} pair(s) from the pinned scope")
    rows, failures = [], []
    for sym, tf in pairs:
        try:
            r = topup_pair(sym, tf, log=log)
        except Exception as e:
            r = {"symbol": sym, "interval": tf, "status": "ERROR",
                 "error": f"{e.__class__.__name__}: {e}"}
        rows.append(r)
        if r["status"] in ("ERROR", "CLOBBER"):
            failures.append(f"{sym} {tf}: {r['status']}")
        log(f"  {sym:14} {tf:4} {r['status']:7} "
            + (f"+{r['rows_added']:>5} rows  newest {r.get('newest_after_iso','—')}  "
               f"gaps={r.get('gap_count','—')}" if r["status"] == "OK"
               else r.get("error", r.get("detail", ""))))

    total_added = sum(r.get("rows_added", 0) for r in rows)
    gap_total = sum(r.get("gap_count", 0) for r in rows)
    log(f"  TOTAL +{total_added} rows across {len(pairs)} pair(s); "
        f"{gap_total} gap(s) across the estate")
    if gap_total:
        log("  GAP LIST (printed, never silently tolerated):")
        for r in rows:
            for g in r.get("gaps", []):
                log(f"    {r['symbol']:14} {r['interval']:4} after {g['after_iso']} "
                    f"missing {g['missing_bars']} bar(s)")

    verdict = "PASS" if not failures else "FAIL"
    doc = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "date": datetime.now().astimezone().strftime("%Y-%m-%d"),
        "slot": slot, "verdict": verdict,
        "pairs": len(pairs), "rows_added": total_added, "gaps": gap_total,
        "failures": failures,
        "detail": rows,
    }
    append_log(doc)
    return doc


def append_log(doc: dict) -> Path:
    TOPUP_LOG.parent.mkdir(parents=True, exist_ok=True)
    with TOPUP_LOG.open("a") as fh:
        fh.write(json.dumps(doc, sort_keys=True) + "\n")
    return TOPUP_LOG


# ═══════════════════════════════════════════════════════════════════ MAIN

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Oracle cache top-up (fetch-and-store only)")
    ap.add_argument("--enumerate", action="store_true",
                    help="re-enumerate the scope from oracle_daily's own cache reads")
    ap.add_argument("--slot", default="topup")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the pinned scope and the cache's current state; fetch nothing")
    a = ap.parse_args(argv)

    if a.enumerate:
        doc = enumerate_scope()
        p, sha, nb = write_scope(doc)
        print(f"scope manifest -> {p}\n  {nb} B  sha256 {sha}")
        print(f"  pinned oracle_daily.py sha256 {doc['oracle_daily_sha256']}")
        return 0

    if a.dry_run:
        for sym, tf in load_scope():
            df = read_cached(sym, tf)
            if df is None:
                print(f"  {sym:14} {tf:4} ABSENT")
                continue
            newest = datetime.fromtimestamp(int(df['open_time'].iloc[-1]) / 1000,
                                            timezone.utc).isoformat()
            print(f"  {sym:14} {tf:4} {len(df):>9,} rows  newest {newest}  "
                  f"gaps={len(contiguity(df, tf))}")
        return 0

    try:
        doc = run(slot=a.slot)
    except SystemExit:
        raise
    except Exception:
        # BR-1b: a network fault logs, exits nonzero, and the Oracle is unaffected.
        append_log({"ts": datetime.now(timezone.utc).isoformat(),
                    "date": datetime.now().astimezone().strftime("%Y-%m-%d"),
                    "slot": a.slot, "verdict": "FAIL", "pairs": 0, "rows_added": 0,
                    "gaps": 0, "failures": ["unhandled"],
                    "traceback": traceback.format_exc()[-1200:]})
        print("TOP-UP FAILED:\n" + traceback.format_exc())
        return 1
    return 0 if doc["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
