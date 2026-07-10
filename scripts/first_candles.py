"""D2: pin every symbol's first available futures candle per interval.

Writes data_starts.csv and refreshes the marked table in README.md.
The LIT floor (2025-12-01T00:00Z) is applied in first_valid — and enforced
again, independently, inside the loader (engine/data.py).
"""

import csv
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import data as dl
from engine.cells import INTERVALS, SYMBOLS

ROOT = Path(__file__).resolve().parent.parent
BEGIN, END = "<!-- data-starts:begin -->", "<!-- data-starts:end -->"


def iso_day(ms: int | None) -> str:
    if ms is None:
        return "-"
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M")


def main() -> int:
    rows = []
    for sym in SYMBOLS:
        for iv in INTERVALS:
            detected = dl.detect_first_candle(sym, iv)
            fv = dl.first_valid_ms(sym, iv, detected) if detected is not None else None
            rows.append({"symbol": sym, "interval": iv,
                         "detected_first_ms": detected if detected is not None else "",
                         "detected_first_utc": iso_day(detected),
                         "first_valid_ms": fv if fv is not None else "",
                         "first_valid_utc": iso_day(fv),
                         "floored": bool(fv is not None and detected is not None and fv > detected)})
            print(f"{sym:14s} {iv:>3s}  detected {iso_day(detected):>16s}  "
                  f"first_valid {iso_day(fv):>16s}"
                  + ("  <- LIT floor applied" if rows[-1]["floored"] else ""))

    csv_path = ROOT / "data_starts.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"-> {csv_path}")

    # Markdown table (one row per symbol; first_valid is interval-independent
    # in practice — report the 1m one and note any interval that differs).
    lines = ["| Symbol | First valid candle (UTC) | Notes |",
             "|---|---|---|"]
    for sym in SYMBOLS:
        sym_rows = [r for r in rows if r["symbol"] == sym and r["first_valid_ms"] != ""]
        if not sym_rows:
            lines.append(f"| {sym} | (no futures data) | |")
            continue
        earliest = min(sym_rows, key=lambda r: r["first_valid_ms"])
        note = "**hard-floored 2025-12-01 (Litentry history excluded)**" \
            if any(r["floored"] for r in sym_rows) else ""
        spread = {r["first_valid_utc"] for r in sym_rows}
        if len(spread) > 1 and not note:
            note = "per-interval starts differ — see data_starts.csv"
        lines.append(f"| {sym} | {earliest['first_valid_utc']} | {note} |")
    table = "\n".join(lines)

    readme = ROOT / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        block = f"{BEGIN}\n{table}\n{END}"
        if BEGIN in text:
            text = re.sub(re.escape(BEGIN) + ".*?" + re.escape(END), block,
                          text, flags=re.S)
        else:
            text += f"\n\n## Data starts (D2)\n\n{block}\n"
        readme.write_text(text, encoding="utf-8", newline="\n")
        print("-> README.md table refreshed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
