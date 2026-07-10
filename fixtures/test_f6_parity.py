"""F6 — parity pack (D5) structural validation.

ACCEPTANCE for F6 is the OPERATOR's sign-off: the 4H/12H cross lists and the
six case windows checked against TradingView bar-by-bar (numeric tolerance:
cross timestamps exact to the bar; EMA/ATR within 0.05% after F7 warm-up).
This fixture can only verify that the pack exists, is well-formed, and is
internally consistent — it cannot replace the human check.

Skipped when the pack has not been generated yet (CI before D5).
"""

import csv
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PARITY = ROOT / "research_outputs" / "parity"

pytestmark = pytest.mark.skipif(
    not (PARITY / "crosses_4h.csv").exists(),
    reason="parity pack not generated yet (scripts/parity_pack.py — D5)")


def _load(name):
    with open(PARITY / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


@pytest.mark.parametrize("name", ["crosses_4h.csv", "crosses_12h.csv"])
def test_cross_lists_wellformed(name):
    rows = _load(name)
    assert rows, f"{name} is empty"
    assert set(rows[0]) >= {"ts_close_utc", "direction", "tier"}
    for r in rows:
        assert r["direction"] in ("long", "short")
        assert r["tier"] in ("full", "provisional")
        assert r["ts_close_utc"].endswith("Z")
    ts = [r["ts_close_utc"] for r in rows]
    assert ts == sorted(ts), f"{name} not chronological"
    assert ts[0] >= "2025-10-06" and ts[-1] <= "2026-07-08"


def test_case_windows_present():
    text = (PARITY / "case_windows.md").read_text(encoding="utf-8")
    for marker in ["May 16", "Jul 2", "Jun 14", "Jun 22", "Feb 6", "Dec 4"]:
        assert marker in text, f"case window '{marker}' missing"
    assert "operator sign-off" in text.lower()
