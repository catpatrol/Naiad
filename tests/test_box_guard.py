"""F-BOX-1 -- the publish guard's size budget, at its edges.

Added 2026-08-15 with the box-governance transfer (APOLLO -> ATHENA).  The
recalibration to warn 0.40 / refuse 0.70 and the D3 tick-set closure both touch
arithmetic that nothing previously asserted: the guard had no test at all, which
is how a threshold can be moved and a boundary quietly inverted.

What this pins:
  * warn fires at EXACTLY WARN_FRACTION, not a hair above
  * refuse fires STRICTLY above REFUSE_FRACTION -- exactly 70.0% warns
  * the comparators, not the constants, are the definition: the edges are
    derived from the module's own values, so a future re-pin re-tests itself
  * the tick set is exchange/ + TICK_EXTRA, and it is what governs
  * both figures reach the reader, with absolute MB beside every percentage
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import publish_exchange as P                                    # noqa: E402


# ----------------------------------------------------------------- thresholds
def test_fbox1_pinned_values():
    """The operator-ratified numbers, stated once so a drift is visible here."""
    assert P.BOX_BYTES == 16_000_000
    assert P.WARN_FRACTION == 0.40
    assert P.REFUSE_FRACTION == 0.70


def test_fbox1_warn_edge_is_inclusive():
    """WARN at or above 0.40 -- exactly 40.0% warns, a hair under is OK."""
    at = int(P.BOX_BYTES * P.WARN_FRACTION)
    assert P.budget(at)[0] == "WARN", "exactly 40.0% must WARN"
    assert P.budget(at - 1)[0] == "OK", "just under 40.0% must be OK"


def test_fbox1_refuse_edge_is_exclusive():
    """REFUSE strictly above 0.70 -- exactly 70.0% WARNS and does not refuse.

    This is the boundary semantic carried unchanged from the 0.80 era; it is
    the whole reason the comparator is `>` and not `>=`.
    """
    at = int(P.BOX_BYTES * P.REFUSE_FRACTION)
    assert P.budget(at)[0] == "WARN", "exactly 70.0% must WARN, not REFUSE"
    assert P.budget(at + 1)[0] == "REFUSE", "just over 70.0% must REFUSE"


def test_fbox1_three_levels_are_reachable():
    assert P.budget(0)[0] == "OK"
    assert P.budget(int(P.BOX_BYTES * 0.55))[0] == "WARN"
    assert P.budget(P.BOX_BYTES)[0] == "REFUSE"


def test_fbox1_fraction_is_exact_not_rounded():
    """4 MB of a 16 MB box is 25% -- comfortably OK under a 40% warn line."""
    lvl, frac = P.budget(4_000_000)
    assert lvl == "OK"
    assert abs(frac - 0.25) < 1e-12


def test_fbox1_edges_derive_from_the_constants():
    """A future re-pin must re-test itself rather than pass on stale edges."""
    for frac in (P.WARN_FRACTION, P.REFUSE_FRACTION):
        at = int(P.BOX_BYTES * frac)
        assert P.budget(at)[0] == "WARN"
    assert P.budget(int(P.BOX_BYTES * P.REFUSE_FRACTION) + 1)[0] == "REFUSE"


# ------------------------------------------------------------------ tick set
def test_fbox1_tick_extra_is_declared():
    """The D3 closure: the box is exchange/ PLUS the ledger, not exchange alone."""
    assert "LEDGER.md" in P.TICK_EXTRA


def test_fbox1_tick_extra_measures_a_real_tracked_file():
    total, rows = P.tick_extra_bytes(str(ROOT))
    assert total > 0, "LEDGER.md is tracked; the tick extra must not read 0"
    assert any(p.endswith("LEDGER.md") for _sz, p in rows)


def test_fbox1_tick_set_exceeds_exchange_alone():
    """The gap the closure exists to remove is real and non-zero."""
    extra, _ = P.tick_extra_bytes(str(ROOT))
    assert extra > 0
    scope_only = 2_500_000
    assert P.budget(scope_only + extra)[1] > P.budget(scope_only)[1]


# ------------------------------------------------------------- dual reporting
def test_fbox1_budget_lines_print_both_figures_and_mb():
    lines = P.budget_lines(2_500_000, 2_755_000, "OK")
    blob = "\n".join(lines)
    assert "TICK SET" in blob and "[governs]" in blob
    assert "exchange-only" in blob and "continuity" in blob
    assert "2,755,000" in blob and "2,500,000" in blob
    assert blob.count("MB") >= 4, "every percentage needs an absolute beside it"
    assert "warn 40%" in blob and "refuse 70%" in blob


def test_fbox1_report_lines_carry_the_tick_set():
    result = {"status": "PUBLISHED", "commit": "abc1234", "branch": "b",
              "staged": ["exchange/x.md"], "bytes": 2_500_000,
              "fraction": 2_500_000 / P.BOX_BYTES, "tick_bytes": 2_755_000,
              "tick_fraction": 2_755_000 / P.BOX_BYTES, "budget": "OK"}
    blob = "\n".join(P.report_lines(result))
    assert "tick set" in blob and "governs" in blob
    assert "2,755,000" in blob and "2,500,000" in blob
    assert "continuity" in blob


def test_fbox1_refuse_report_quotes_the_tick_figure_not_the_scope_figure():
    """A refusal must not under-report itself by the size of the ledger."""
    result = {"status": "REFUSED", "bytes": 11_000_000,
              "fraction": 11_000_000 / P.BOX_BYTES, "tick_bytes": 11_255_000,
              "tick_fraction": 11_255_000 / P.BOX_BYTES, "budget": "REFUSE",
              "largest": [(9_000, "exchange/big.md")]}
    blob = "\n".join(P.report_lines(result))
    assert "11,255,000" in blob
