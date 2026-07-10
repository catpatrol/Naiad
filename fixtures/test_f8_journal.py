"""F8 — journal completeness.

(a) Schema <-> autopsy bidirectional check: every question in
    autopsy_questions.md maps to columns; every payload column is claimed by
    at least one question. Unmapped questions are a build failure.
(b) Dead-column scan on the committed dry-run journal (D7): every minimum
    field non-null somewhere, no always-zero numeric columns, no type traps
    (mixed JSON types within a column).
"""

import json
import re
from pathlib import Path

import pytest

from engine.journal import MIN_FIELDS, SHADOW_FIELDS

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / "fixtures" / "autopsy_questions.md"
DRYRUN = ROOT / "research_outputs" / "dryrun" / "journal"

# bookkeeping fields a question need not cite explicitly
EXEMPT = {"run_id", "engine_version", "config_id", "symbol", "tf_gov",
          "tf_exec", "ts_close", "evt", "dir"}
ENGAGEMENT_KEYS = {"xa_engaged_before_exit", "tpw_before_exit",
                   "ext_before_exit", "arrow_visible"}


def _questions():
    text = QUESTIONS.read_text(encoding="utf-8")
    blocks = re.findall(r"\*\*Q(\d+)\..*?(?=\n\*\*Q|\n---|\Z)", text, re.S)
    full = re.split(r"(?=\*\*Q\d+\.)", text)
    qs = [b for b in full if b.startswith("**Q")]
    return text, qs


def test_at_least_20_questions_each_mapped():
    text, qs = _questions()
    assert len(qs) >= 20, f"only {len(qs)} autopsy questions (need >= 20)"
    for q in qs:
        assert "Columns:" in q, f"unmapped question: {q[:60]}..."
        known = [f for f in MIN_FIELDS + SHADOW_FIELDS if f in q]
        assert known, f"question cites no known column: {q[:60]}..."


def test_every_payload_column_is_claimed():
    text, _ = _questions()
    for f in MIN_FIELDS:
        if f in EXEMPT:
            continue
        assert f in text, f"schema field '{f}' claimed by no autopsy question"
    for f in SHADOW_FIELDS:
        assert f in text, f"shadow field '{f}' claimed by no autopsy question"


# ── F8b (engine 1.0.1): same-bar multi-family rejects all persist ──

def test_f8b_same_bar_rejects_all_persist(synth_env, synth_cell, tmp_path,
                                          monkeypatch):
    """Synthetic scenario: campaign 1 fills its 3-tranche cap (all stopped
    out), then a PRIME add and a CONFIRM add fire on the SAME bar — the
    PRIME rejects max_tranches, the CONFIRM rejects not_positioned. Both
    REJECT rows must persist under distinct subkeys (trade_ADD_prime vs
    trade_ADD_confirm); pre-1.0.1 they collided and the merge dropped one."""
    import numpy as np

    from conftest import halt_scenario

    import engine.replay as replay_mod
    from engine.journal import read_journal
    from engine.signals import SignalEvent

    sig = halt_scenario()
    # keep campaign 1's three PRIMEs (bars 10/60/110, all stop out) and add a
    # same-bar PRIME-add + CONFIRM-add at bar 160 while flat at the cap
    sig.events = [e for e in sig.events
                  if e.evt == "REGIME" or (e.evt == "PRIME" and e.i < 200)]
    sig.events = [e for e in sig.events if not (e.evt == "REGIME" and e.i == 200)]
    sig.campaign_id[:] = np.where(sig.campaign_id > 0, 1, 0)
    sig.events.append(SignalEvent(160, "PRIME", 1, grade="A", rc=4, zone="Z2",
                                  stop=99.0, stage=2, tier="full",
                                  is_r1=False, is_add=True, grade_uncapped="A"))
    sig.events.append(SignalEvent(160, "CONFIRM", 1, grade="-", rc=4,
                                  zone="Z2", stop=99.0, stage=2, tier="full",
                                  is_add=True))
    monkeypatch.setattr(replay_mod, "compute_signals", lambda *a, **k: sig)

    summary = replay_mod.run_replay("naiad_v0", synth_cell.cell_id,
                                    "2024-01-15", "2024-01-16",
                                    tmp_path / "j", log=lambda *_: None)
    rows = read_journal(tmp_path / "j", synth_cell.cell_id)
    same_bar = [r for r in rows if r["evt"] == "REJECT"
                and r["ts_open"] == "2024-01-15T02:40:00Z"]
    keys = {(r["tranche_id"], r["reject_reason"]) for r in same_bar}
    assert ("trade_ADD_prime", "max_tranches") in keys, keys
    assert ("trade_ADD_confirm", "not_positioned") in keys, keys
    assert len(same_bar) == 2, f"expected both same-bar rejects persisted: {same_bar}"
    # and the summary row count equals what is on disk (F1b invariant holds)
    assert summary["rows"] == sum(
        1 for _ in open(summary["files"][0], encoding="utf-8"))


# ── (b) dead-column scan on the committed dry-run journal ──

pytestmark_b = pytest.mark.skipif(not DRYRUN.exists(),
                                  reason="dry-run journal not generated (D7)")


@pytest.mark.skipif(not DRYRUN.exists(),
                    reason="dry-run journal not generated yet (D7)")
def test_dryrun_journal_no_dead_columns():
    rows = []
    for path in sorted(DRYRUN.rglob("*.jsonl")):
        with open(path, encoding="utf-8") as f:
            rows.extend(json.loads(line) for line in f if line.strip())
    assert len(rows) > 100, "dry-run journal implausibly small"

    for field in MIN_FIELDS:
        values = [r[field] for r in rows if r.get(field) is not None]
        assert values, f"column '{field}' is null on every row (dead column)"
        types = {type(v).__name__ for v in values}
        types.discard("int") if "float" in types else None
        assert len(types) == 1 or types <= {"int", "float"}, \
            f"column '{field}' is type-trapped: {types}"
        numeric = [v for v in values if isinstance(v, (int, float))
                   and not isinstance(v, bool)]
        if numeric and field not in ("rc", "stage"):
            assert any(v != 0 for v in numeric), \
                f"column '{field}' is zero on every row"

    shadows = [r["shadow"] for r in rows if r.get("shadow")]
    assert shadows, "no shadow objects anywhere in the dry-run journal"
    for f in SHADOW_FIELDS:
        assert any(s.get(f) is not None for s in shadows), \
            f"shadow field '{f}' is null on every row (dead column)"

    flags = [r["engagement_flags"] for r in rows if r.get("engagement_flags")]
    keys = set().union(*(f.keys() for f in flags)) if flags else set()
    assert ENGAGEMENT_KEYS <= keys, \
        f"engagement flags missing: {ENGAGEMENT_KEYS - keys}"
