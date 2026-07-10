"""v12 Study loader guards (V1 build prompt §3, invariants I1–I4).

Wraps the Phase 1 cache (engine/data.py — same parquet files, same layout,
invariant I8) with the three study guards:

- I1  LIT floor: LITUSDT candles before 2025-12-23T00:00:00Z are Litentry, a
      different asset. Requests for earlier ranges return empty + guard event.
      (Stricter than the Phase 1 engine floor of 2025-12-01, which stands
      untouched for the Naiad line.)
- I2  Study right edge: no candle with open time > 2026-07-07T23:59:59Z is
      served. Forward data on disk belongs to Naiad and is invisible here.
- I3  Lockbox seal: OHLCV *values* of candles opening inside
      [2024-07-01T00:00Z, 2025-10-05T23:59:59Z] are sealed until V8. Value-mode
      reads that touch the range raise LockboxViolation; `integrity_only=True`
      returns counts / timestamps / hashes and nothing price-shaped.

Partition classes are a pure function of (symbol, open time) — VR-1 of
V12_Study_Charter_Addendum_v1.0.md. Guard events append to a JSONL log inside
the cache directory (never the repo; NAIAD_CACHE_DIR-aware so fixtures stay
hermetic).
"""

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from engine import data as phase1
from engine.cells import INTERVAL_MS

# ── VR-1 boundaries, candle open time, UTC milliseconds ─────────────────────
LIT_FLOOR_STUDY_MS = 1_766_448_000_000        # 2025-12-23T00:00:00Z (I1)
LOCKBOX_START_MS = 1_719_792_000_000          # 2024-07-01T00:00:00Z
LOCKBOX_END_EXCL_MS = 1_759_708_800_000       # 2025-10-06T00:00:00Z
EDGE_EXCL_MS = 1_783_468_800_000              # 2026-07-08T00:00:00Z (I2)

CLASS_EXPLORATION = "exploration-classic"
CLASS_LOCKBOX = "lockbox"
CLASS_SPENT = "spent"
CLASS_CONTAMINATED = "regime-contaminated"
CLASS_FORWARD = "forward"


class LockboxViolation(Exception):
    """A code path asked for OHLCV values of sealed lockbox rows (I3)."""


def utc_str(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S")


def partition_class(symbol: str, open_ms: int) -> str:
    """VR-1: pure function of (symbol, open time)."""
    if open_ms < LOCKBOX_START_MS:
        return CLASS_EXPLORATION
    if open_ms < LOCKBOX_END_EXCL_MS:
        return CLASS_LOCKBOX
    if open_ms < EDGE_EXCL_MS:
        return CLASS_SPENT if symbol == "BTCUSDT" else CLASS_CONTAMINATED
    return CLASS_FORWARD


def guard_log_path() -> Path:
    return phase1.cache_dir() / "guard_log.jsonl"


def _guard_event(event: str, symbol: str, interval: str | None,
                 start_ms: int, end_ms: int, detail: str) -> None:
    rec = {
        "ts_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "event": event, "symbol": symbol, "interval": interval,
        "requested_start_ms": int(start_ms), "requested_end_ms": int(end_ms),
        "detail": detail,
    }
    with open(guard_log_path(), "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class IntegrityView:
    """Everything integrity mode may reveal about a range: timestamps and
    bytes, never values (I3)."""
    symbol: str
    interval: str
    row_count: int
    first_open_ms: int | None
    last_open_ms: int | None
    duplicate_count: int
    gap_count: int
    gaps: list = field(default_factory=list)   # {gap_start_ms, gap_end_ms, bars_missing}
    file_sha256: str = ""


def _empty_klines() -> pd.DataFrame:
    return pd.DataFrame(columns=phase1.KLINE_COLS)


def _clamp(symbol: str, interval: str | None, start_ms: int, end_ms: int
           ) -> tuple[int, int] | None:
    """Apply I1 + I2. Returns clamped (start, end) or None for empty+logged."""
    if end_ms >= EDGE_EXCL_MS:
        _guard_event("right_edge_clamp", symbol, interval, start_ms, end_ms,
                     "request crossed the study right edge "
                     "2026-07-07T23:59:59Z; clamped (I2)")
        end_ms = EDGE_EXCL_MS - 1
    if start_ms >= EDGE_EXCL_MS:
        _guard_event("right_edge_empty", symbol, interval, start_ms, end_ms,
                     "request entirely past the study right edge (I2)")
        return None
    if symbol == "LITUSDT":
        if end_ms < LIT_FLOOR_STUDY_MS:
            _guard_event("lit_floor_empty", symbol, interval, start_ms, end_ms,
                         "request entirely before the LIT floor "
                         "2025-12-23T00:00:00Z — that history is Litentry (I1)")
            return None
        if start_ms < LIT_FLOOR_STUDY_MS:
            _guard_event("lit_floor_clamp", symbol, interval, start_ms, end_ms,
                         "request start floored to 2025-12-23T00:00:00Z (I1)")
            start_ms = LIT_FLOOR_STUDY_MS
    return start_ms, end_ms


def _touches_lockbox(start_ms: int, end_ms: int) -> bool:
    return start_ms < LOCKBOX_END_EXCL_MS and end_ms >= LOCKBOX_START_MS


def load_study_klines(symbol: str, interval: str, start_ms: int, end_ms: int,
                      integrity_only: bool = False):
    """The v12 Study's only sanctioned path to candles.

    Value mode returns an OHLCV frame and refuses (LockboxViolation) any range
    touching the sealed lockbox. Integrity mode returns an IntegrityView —
    counts, timestamps, gaps, file hash — and is lawful on every range.
    """
    clamped = _clamp(symbol, interval, start_ms, end_ms)

    if not integrity_only:
        if clamped is None:
            return _empty_klines()
        s, e = clamped
        if _touches_lockbox(s, e):
            raise LockboxViolation(
                f"{symbol} {interval}: value-mode read of "
                f"[{utc_str(s)}, {utc_str(e)}] touches the sealed lockbox "
                f"[2024-07-01, 2025-10-05 23:59:59]. Integrity ops only "
                f"until V8 (I3); pass integrity_only=True.")
        df = phase1.load_klines(symbol, interval, s, e)
        if symbol == "LITUSDT" and len(df):
            assert int(df["open_time"].min()) >= LIT_FLOOR_STUDY_MS
        return df

    path = phase1._kline_path(symbol, interval)
    sha = file_sha256(path) if path.exists() else ""
    if clamped is None or not path.exists():
        return IntegrityView(symbol, interval, 0, None, None, 0, 0, [], sha)
    s, e = clamped
    ot = pd.read_parquet(path, columns=["open_time"])["open_time"].to_numpy()
    ot = ot[(ot >= s) & (ot <= e)]
    dup = int(len(ot) - len(np.unique(ot)))
    ot_sorted = np.unique(ot)
    step = INTERVAL_MS[interval]
    gaps = []
    if len(ot_sorted) > 1:
        d = np.diff(ot_sorted)
        for i in np.nonzero(d > step)[0]:
            gaps.append({"gap_start_ms": int(ot_sorted[i] + step),
                         "gap_end_ms": int(ot_sorted[i + 1] - step),
                         "bars_missing": int(d[i] // step - 1)})
    return IntegrityView(
        symbol, interval, int(len(ot)),
        int(ot_sorted[0]) if len(ot_sorted) else None,
        int(ot_sorted[-1]) if len(ot_sorted) else None,
        dup, len(gaps), gaps, sha)


def load_study_funding(symbol: str, start_ms: int, end_ms: int) -> pd.DataFrame:
    """Funding history, right-edge clamped. Collected for the later cost
    model; the census itself only ever reads funding_time (never rates)."""
    clamped = _clamp(symbol, None, start_ms, end_ms)
    if clamped is None:
        return pd.DataFrame(columns=["funding_time", "funding_rate"])
    s, e = clamped
    return phase1.load_funding(symbol, s, e)
