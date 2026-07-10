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
