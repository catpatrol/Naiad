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
  * the naming trip-wire is ABSOLUTE -- it does NOT move with the box
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


# ------------------------------------------------------ the naming trip-wire
def test_fbox1_flag_bytes_is_pinned():
    """The operator-ratified absolute, stated once so a drift is visible here."""
    assert P.FLAG_BYTES == 64_000


def test_fbox1_flag_bytes_does_not_scale_with_the_box():
    """ABSOLUTE by ruling 2026-08-15, and that is the whole content of the rule.

    NOTE THE DELIBERATE INVERSION of the idiom above: the warn/refuse tests
    prove the edges DO derive from the constants, so that a re-pin re-tests
    itself.  This one proves the opposite for this constant, on purpose.  The
    failure it catches is the one that actually happened one block up a day
    earlier -- an editor seeing several numbers in one block and carrying them
    all up proportionally with a raised ceiling.

    THE OBVIOUS VERSION OF THIS TEST IS WRONG, and it was written first:
    asserting `FLAG_BYTES < int(BOX_BYTES * 0.01)` derives the check from the
    very constant it claims independence from, and it goes RED if the ceiling
    is ever LOWERED to 6.4 MB -- which is what the box was the day before the
    pin.  A future operator tightening the box would get a red suite whose
    message told them to move FLAG_BYTES with the box: the precise opposite of
    the ruling.  So independence is tested by INDEPENDENCE -- the wire must
    give the same answer under any ceiling.
    """
    fixed = [(70_000, "exchange/a.md"), (10_000, "exchange/b.md")]
    baseline = P.over_flag(fixed)
    for pretend_box in (6_390_000, 16_000_000, 48_000_000):
        original, P.BOX_BYTES = P.BOX_BYTES, pretend_box
        try:
            assert P.over_flag(fixed) == baseline, \
                f"the wire moved when BOX_BYTES became {pretend_box:,}"
            assert P.FLAG_BYTES == 64_000
        finally:
            P.BOX_BYTES = original
    assert P.BOX_BYTES == 16_000_000, "the box constant must be restored"


def test_fbox1_flag_edge_is_exclusive():
    """"OVER 64,000 B" is read literally -- exactly 64,000 does not flag.

    Same reading as REFUSE, and for the same reason: a boundary that fires at
    its own stated limit surprises the one reader who checked the number first.
    """
    assert P.over_flag([(P.FLAG_BYTES, "exchange/x.md")]) == []
    assert P.over_flag([(P.FLAG_BYTES + 1, "exchange/x.md")]) == \
        [(P.FLAG_BYTES + 1, "exchange/x.md")]


def test_fbox1_flag_line_names_the_file_and_its_bytes():
    """The duty is to name it BY NAME.  A count is not a flag."""
    blob = "\n".join(P.flag_lines([(70_000, "exchange/status/LEDGER_X.md")]))
    assert "LEDGER_X.md" in blob
    assert "70,000" in blob
    assert "64,000" in blob, "the reader must see the wire that was crossed"


def test_fbox1_flag_line_speaks_when_nothing_is_over():
    """Silence is how a reader cannot tell a passing check from an absent one."""
    blob = "\n".join(P.flag_lines([]))
    assert "no box-bound file over" in blob and "64,000" in blob


def test_fbox1_flag_is_advisory_never_a_refusal():
    """Six files are already over the wire.  If it ever refused, the bus would
    be non-compliant on the day it landed and the pressure would be to raise
    the number rather than fix the files.  Naming is the whole duty."""
    over = P.over_flag([(P.FLAG_BYTES + 1, "exchange/big.md")])
    blob = "\n".join(P.flag_lines(over))
    assert "never refuses" in blob.lower(), \
        "the block must say in words that it cannot refuse a publish"
    assert "REFUSE" not in blob, \
        "and it must not look like the REFUSE branch beside it"


def test_fbox1_flag_reads_the_tick_set_not_exchange_alone():
    """§3.2 binds "any BOX-BOUND file", and §4.3 defines the box as exchange/
    AND LEDGER.md.  Metering exchange/ alone here is the D3 gap re-opened at
    file level -- and it hides the single largest box-bound file in the
    project.  Caught in adversarial review, where the first version reported
    "zero files over the raised wire" while a 259 KB LEDGER.md sat over it.
    """
    scope_rows = [(10, "exchange/a.md")]
    extra_rows = [(259_298, "LEDGER.md")]
    assert P.over_flag(scope_rows) == [], "nothing in exchange/ is over"
    named = [p for _sz, p in P.over_flag(scope_rows + extra_rows)]
    assert "LEDGER.md" in named, "the tick extra must be eligible for naming"


def test_fbox1_flag_list_is_capped_like_its_siblings():
    """Every other list in this module slices at ten or twenty.  The pin
    guarantees this one only grows as the bus fills, and an unbounded list in
    a launchd log is how the interesting lines stop being read."""
    many = [(70_000 + i, f"exchange/f{i}.md") for i in range(25)]
    blob = "\n".join(P.flag_lines(P.over_flag(many)))
    assert "and 15 more over the wire" in blob
    assert blob.count("exchange/f") == 10


def test_fbox1_flag_points_at_the_intended_home_duty():
    """§3.2 asks for the name AND the intended home.  Publish can only supply
    the first, so it must point at where the second is recorded rather than
    quietly redefining the duty down to what it implemented."""
    blob = "\n".join(P.flag_lines([(70_000, "exchange/x.md")]))
    assert "intended home" in blob and "disposition table" in blob


def test_fbox1_flag_reaches_the_durable_report_not_only_stdout():
    """A line in a launchd log does not discharge "flagged TO THE OPERATOR"."""
    blob = "\n".join(P.report_lines(
        {"status": "PUBLISHED", "commit": "abc1234", "branch": "b",
         "staged": ["exchange/x.md"], "bytes": None,
         "over_flag": [(70_000, "exchange/status/LEDGER_X.md")]}))
    assert "naming trip-wire" in blob and "LEDGER_X.md" in blob
    blob_clean = "\n".join(P.report_lines(
        {"status": "PUBLISHED", "commit": "a", "branch": "b",
         "staged": [], "bytes": None, "over_flag": []}))
    assert "no box-bound file over" in blob_clean
