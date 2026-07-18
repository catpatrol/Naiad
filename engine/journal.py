"""Journal layer (build prompt §8, invariants 4/8/11).

- Append-only JSONL, one row per event, organized as
  journal/{cell_id}/{YYYY-MM}.jsonl by event open time (UTC).
- Idempotent: rows merge by the unique key (cell_id, evt, ts_open, tranche_id).
  For non-tranche events tranche_id doubles as a deterministic subkey (e.g.
  the zone of a TAG row) so same-bar same-type rows cannot collide.
- Canonical serialization (sorted keys, minimal separators, \n endings) and a
  deterministic run_id make reruns byte-identical (F1). No wall-clock values
  are ever written.
- Every §8 minimum field is present on every row (null where not applicable),
  so no reader ever key-errors and F8 can scan for dead columns.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

# Chronological tie-break for same-timestamp rows: signal events in Pine
# emission order, then trading events in wake order.
EVT_ORDER = ["REGIME", "STAGE", "TAG", "PRIME", "CONFIRM", "V", "TPW",
             "CLUSTER", "X", "REJECT", "ENTRY_FILL", "ADD_FILL", "STOP_FILL",
             "EXIT", "HALT"]

SHADOW_FIELDS = ["entry_alt_px", "entry_alt_t", "entry_alt_stop",
                 "ladder_strict",
                 "ladder_unthrottled_grade", "ladder_unthrottled_size_r",
                 "stop_alt_anchor", "stop_alt_volbuf",
                 "stop_alt_anchor_exit_r", "stop_alt_volbuf_exit_r",
                 "size_full_r1", "size_big_adds",
                 "exit_XA", "exit_XB", "exit_XC", "exit_XD"]

# Engine 1.0.8 (TC-4, additive): present ONLY on ENTRY_FILL/ADD_FILL rows —
# every other row keeps its exact pre-1.0.8 key set, so the F-SIG population
# (signal-event rows) stays byte-comparable across engine versions and old
# tooling keeps working (readers .get() them; no reader key-errors).
FILL_ONLY_FIELDS = ["concurrent_open_at_fill", "fill_class"]

MIN_FIELDS = ["run_id", "engine_version", "config_id", "cell_id", "symbol",
              "tf_gov", "tf_exec", "ts_open", "ts_close", "evt", "dir",
              "tier", "grade", "rc", "zone", "stage", "retr", "px_signal",
              "px_fill", "stop", "atr_exec", "atr_gov", "tranche_id",
              "size_r", "qty", "fees", "funding_cum", "slippage",
              "pnl_usd", "realized_r", "equity_after",
              "mfe_r", "mae_r", "give_back_r",
              "postexit_cont_1", "postexit_cont_5", "postexit_cont_20",
              "exit_reason", "cohort", "engagement_flags", "shadow",
              "reject_reason"]


def iso(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def make_row(**kw) -> dict:
    """A journal row with every minimum field present (nulls where n/a)."""
    row = {k: None for k in MIN_FIELDS}
    row["shadow"] = None
    row.update(kw)
    unknown = set(row) - set(MIN_FIELDS) - set(FILL_ONLY_FIELDS)
    if unknown:
        raise KeyError(f"unknown journal fields: {sorted(unknown)}")
    return row


def row_key(row: dict) -> tuple:
    return (row["cell_id"], row["evt"], row["ts_open"], row["tranche_id"] or "-")


def sort_key(row: dict) -> tuple:
    return (row["ts_open"], EVT_ORDER.index(row["evt"]), row["tranche_id"] or "-")


def _dumps(row: dict) -> str:
    return json.dumps(row, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


def write_journal(rows: list[dict], journal_root: Path) -> list[Path]:
    """Merge rows into monthly JSONL files, idempotently.

    Existing rows with the same unique key are REPLACED by the incoming row
    (re-scans recompute rows from the same inputs, so replacement is a no-op
    unless the engine version changed — which is a new run_id anyway).
    """
    by_file: dict[Path, list[dict]] = {}
    for row in rows:
        month = row["ts_open"][:7]
        path = journal_root / row["cell_id"] / f"{month}.jsonl"
        by_file.setdefault(path, []).append(row)

    written = []
    for path, new_rows in sorted(by_file.items()):
        merged: dict[tuple, dict] = {}
        if path.exists():
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        r = json.loads(line)
                        merged[row_key(r)] = r
        for r in new_rows:
            merged[row_key(r)] = r
        path.parent.mkdir(parents=True, exist_ok=True)
        ordered = sorted(merged.values(), key=sort_key)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            for r in ordered:
                f.write(_dumps(r) + "\n")
        written.append(path)
    return written


def files_sha256(paths: list[Path]) -> str:
    """THE documented journal hash formula (reviewer ticket D-1): sha256 over
    the byte concatenation of the journal files in chronological (filename)
    order. Reproducible from the packeted files alone:
        sha256(cat 2026-05.jsonl 2026-06.jsonl 2026-07.jsonl ...)
    No salts, no separators."""
    h = hashlib.sha256()
    for path in sorted(paths, key=lambda p: p.name):
        h.update(path.read_bytes())
    return h.hexdigest()


def count_lines(paths: list[Path]) -> int:
    """Rows as persisted: newline-terminated lines across the files."""
    return sum(p.read_bytes().count(b"\n") for p in paths)


def journal_sha256(journal_root: Path, cell_id: str) -> str:
    """Hash a cell's whole persisted journal (F1: bit-identical reruns)."""
    return files_sha256(list((journal_root / cell_id).glob("*.jsonl")))


def read_journal(journal_root: Path, cell_id: str) -> list[dict]:
    rows = []
    cell_dir = journal_root / cell_id
    for path in sorted(cell_dir.glob("*.jsonl")):
        with open(path, encoding="utf-8") as f:
            rows.extend(json.loads(line) for line in f if line.strip())
    return rows
