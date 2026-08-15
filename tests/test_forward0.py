"""F-F1..F-F5 -- FORWARD-0, the hash-chained trade diary (v4 Phase III).

Run: python -m pytest tests/test_forward0.py

F-F1 chain integrity   -- a deliberately mutated line is detected
F-F2 append-only       -- rewriting history is refused
F-F3 no aggregation    -- source scan proves no statistic is applied to log data
F-F4 kind isolation    -- no code path mixes kinds
F-F5 capture linkage   -- every brief_json_sha256 matches an existing capture
"""

import hashlib
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import forward_log as FL                                            # noqa: E402


def _log(tmp_path):
    return tmp_path / "forward_log.jsonl"


def _seed(path, n=3, kind="mechanical", sha="cap-sha"):
    out = []
    for i in range(n):
        e = FL.log_intent(kind, "BTCUSDT", "4h", "long",
                          f"reclaim level {i}", 63000.0 + i, 62000.0 + i,
                          [64000.0, 65000.0], "2026-08-03", "post_ny", sha,
                          "2.0.0", "1.2.0", note=f"entry {i}", path=path)
        out.append(e)
    return out


# --------------------------------------------------------------- F-F1

def test_f_f1_chain_detects_a_mutated_line(tmp_path):
    p = _log(tmp_path)
    _seed(p, 4)
    assert FL.verify_chain(p)["ok"] is True

    lines = p.read_text(encoding="utf-8").splitlines()
    doc = json.loads(lines[1])
    doc["entry_level"] = 99999.0                       # retroactive edit
    lines[1] = json.dumps(doc, sort_keys=True, ensure_ascii=False)
    p.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    res = FL.verify_chain(p)
    assert res["ok"] is False
    assert res["first_bad_line"] == 2
    assert "edited after it was written" in res["reason"]


def test_f_f1_chain_detects_a_removed_or_reordered_line(tmp_path):
    p = _log(tmp_path)
    _seed(p, 4)
    lines = p.read_text(encoding="utf-8").splitlines()

    kept = lines[:1] + lines[2:]                       # delete line 2
    p.write_text("\n".join(kept) + "\n", encoding="utf-8", newline="\n")
    res = FL.verify_chain(p)
    assert res["ok"] is False and res["first_bad_line"] == 2
    assert "inserted, removed or reordered" in res["reason"]

    swapped = lines[:1] + [lines[2], lines[1]] + lines[3:]
    p.write_text("\n".join(swapped) + "\n", encoding="utf-8", newline="\n")
    assert FL.verify_chain(p)["ok"] is False


def test_f_f1_a_clean_chain_verifies_and_is_not_vacuous(tmp_path):
    p = _log(tmp_path)
    entries = _seed(p, 5)
    res = FL.verify_chain(p)
    assert res["ok"] is True
    assert res["checked"] == 5, "the guard must actually have walked 5 lines"
    assert res["head"] == entries[-1]["entry_sha256"]
    # the chain genuinely links: each prev is the predecessor's digest
    assert entries[0]["prev_sha256"] == FL.GENESIS
    for a, b in zip(entries, entries[1:]):
        assert b["prev_sha256"] == a["entry_sha256"]


def test_f_f1_digest_excludes_itself_and_covers_content(tmp_path):
    p = _log(tmp_path)
    e = _seed(p, 1)[0]
    assert "entry_sha256" not in FL.canonical(e)
    assert FL.chain_hash(e, e["prev_sha256"]) == e["entry_sha256"]
    mutated = dict(e, note="changed")
    assert FL.chain_hash(mutated, e["prev_sha256"]) != e["entry_sha256"]


# --------------------------------------------------------------- F-F2

def test_f_f2_append_with_a_stale_prev_is_refused(tmp_path):
    p = _log(tmp_path)
    _seed(p, 3)
    stale = FL.make_entry("mechanical", "ETHUSDT", "1h", "short", "lose level",
                          3000.0, 3100.0, [2900.0], "2026-08-03", "post_ny",
                          "cap-sha", "2.0.0", "1.2.0",
                          prev_sha256=FL.GENESIS)         # not the head
    with pytest.raises(ValueError) as e:
        FL.append_entry(stale, p)
    assert "Rewriting history is refused" in str(e.value)
    assert FL.verify_chain(p)["checked"] == 3, "the refused entry must not land"


def test_f_f2_a_forged_digest_is_refused(tmp_path):
    p = _log(tmp_path)
    _seed(p, 2)
    forged = FL.make_entry("actual", "SOLUSDT", "1h", "long", "t", 150.0, 140.0,
                           [160.0], "2026-08-03", "post_ny", "cap-sha",
                           "2.0.0", "1.2.0", prev_sha256=FL.last_sha(p))
    forged["entry_level"] = 1.0                          # content changed after hashing
    with pytest.raises(ValueError) as e:
        FL.append_entry(forged, p)
    assert "does not match the entry's own content" in str(e.value)


def test_f_f2_exit_is_a_new_line_not_an_edit(tmp_path):
    """§III.2: exits are status transitions on the same entry, and the log is
    append-only. The only reconciliation is a NEW line carrying the same id."""
    p = _log(tmp_path)
    e = _seed(p, 1)[0]
    before = p.read_text(encoding="utf-8")

    t = FL.log_transition(e["id"], "closed", exit_level=64500.0,
                          exit_reason="target 1", path=p)
    after = p.read_text(encoding="utf-8")

    assert after.startswith(before), "the original line was modified"
    assert len(after.splitlines()) == 2
    assert t["id"] == e["id"] and t["status"] == "closed"
    assert t["exit_level"] == 64500.0
    assert FL.verify_chain(p)["ok"] is True

    # the original line still says what it said when it was written
    first = json.loads(after.splitlines()[0])
    assert first["status"] == "open" and first["exit_level"] is None


# --------------------------------------------------------------- F-F3

BANNED_STATS = (
    "mean(", "median(", "average(", "np.mean", "np.sum", "np.std", "stdev(",
    "variance(", "expectancy", "win_rate", "winrate", "hit_rate", "hitrate",
    "profit", "pnl", "p_and_l", "r_multiple", "sharpe", "drawdown",
    "value_counts", "groupby", "describe(", "aggregate(", "cumsum", "corr(",
    "performance", "returns(",
)


def _code_only(path):
    """Source with docstrings and comments removed.

    The scan must read CODE, not prose. forward_log.py's own docstring QUOTES
    the prohibition it enforces -- "any aggregate, win rate, expectancy, P&L
    summary" -- and a naive scan flags the sentence that forbids the thing as if
    it were the thing. Stripping prose is what makes the fixture test behaviour
    instead of vocabulary.
    """
    import ast
    import io
    import tokenize

    src = Path(path).read_text(encoding="utf-8")
    out = []
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.COMMENT:
            continue
        out.append(tok)
    stripped = tokenize.untokenize(out)

    tree = ast.parse(stripped)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                             ast.AsyncFunctionDef)):
            if (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                node.body[0].value.value = ""
    return ast.unparse(tree).lower()


def test_f_f3_no_statistic_is_applied_to_log_data():
    """Any statistic over this log waits on G-10 being separately ratified."""
    code = _code_only(ROOT / "scripts" / "forward_log.py")
    for token in BANNED_STATS:
        assert token not in code, (
            f"forward_log.py CODE contains {token!r} -- aggregation over the "
            f"diary is prohibited until G-10 is separately ratified")

    # ANTI-VACUITY: the stripper must not have eaten the code as well as the
    # prose, or this fixture passes against anything.
    assert "def verify_chain" in code and "chain_hash" in code
    assert "expectancy" not in code
    assert "expectancy" in (ROOT / "scripts" / "forward_log.py").read_text(
        encoding="utf-8").lower(), \
        "the prohibition must still be STATED in the prose it was stripped from"


def test_f_f3_module_exposes_no_aggregate_surface():
    """No CALLABLE may compute over the diary. Constants are exempt -- a tuple
    of status names cannot aggregate anything, and banning the substring 'stat'
    outright would forbid the word `STATUSES`."""
    callables = [n for n in dir(FL)
                 if not n.startswith("_") and callable(getattr(FL, n))]
    assert callables, "no public callables found -- the scan would be vacuous"
    for name in callables:
        low = name.lower()
        for bad in ("summar", "aggregate", "score", "total", "rate",
                    "count_by", "performance", "pnl", "statistic"):
            assert bad not in low, f"forward_log exposes callable {name!r}"

    # verify_chain reports integrity metadata only -- never an outcome field
    res = FL.verify_chain(ROOT / "ops" / "forward_log.jsonl")
    assert set(res) <= {"ok", "checked", "head", "first_bad_line", "reason", "id"}
    for k in ("exit_level", "exit_reason", "status", "pnl"):
        assert k not in res


def test_f_f3_the_prohibition_is_stated_in_the_source():
    src = (ROOT / "scripts" / "forward_log.py").read_text(encoding="utf-8")
    assert "G-10" in src and "DIARY, NOT A SCOREBOARD" in src.upper()
    assert "Recording an exit is diary-keeping" in src


# --------------------------------------------------------------- F-F4

def test_f_f4_selection_requires_an_explicit_kind(tmp_path):
    p = _log(tmp_path)
    _seed(p, 2, kind="mechanical")
    _seed(p, 3, kind="hypothetical")
    _seed(p, 1, kind="actual")

    assert len(FL.entries_of_kind("mechanical", p)) == 2
    assert len(FL.entries_of_kind("hypothetical", p)) == 3
    assert len(FL.entries_of_kind("actual", p)) == 1

    for got in (FL.entries_of_kind(k, p) for k in FL.KINDS):
        assert len({e["kind"] for e in got}) == 1, "a selection mixed kinds"

    with pytest.raises(ValueError):
        FL.entries_of_kind("all", p)
    with pytest.raises(ValueError):
        FL.entries_of_kind(None, p)


def test_f_f4_no_function_returns_mixed_kinds_for_analysis():
    """`read_lines` exists for append and verify. It must not be a sampling
    surface, and nothing else may return entries without naming a kind."""
    src = (ROOT / "scripts" / "forward_log.py").read_text(encoding="utf-8")
    assert "for append and verify only" in src.lower()
    assert "entries_of_kind" in src

    import inspect
    sig = inspect.signature(FL.entries_of_kind)
    assert "kind" in sig.parameters
    assert sig.parameters["kind"].default is inspect.Parameter.empty, \
        "kind must be REQUIRED; a default would make mixing the easy path"


def test_f_f4_invalid_kind_is_refused_at_write_time(tmp_path):
    with pytest.raises(ValueError):
        FL.make_entry("guess", "BTCUSDT", "4h", "long", "t", 1.0, 2.0, [],
                      "2026-08-03", "post_ny", "s", "2.0.0", "1.2.0")
    for k in FL.KINDS:
        FL.make_entry(k, "BTCUSDT", "4h", "long", "t", 1.0, 2.0, [],
                      "2026-08-03", "post_ny", "s", "2.0.0", "1.2.0")


# --------------------------------------------------------------- F-F5

def test_f_f5_capture_linkage_matches_a_stored_capture(tmp_path):
    briefs = tmp_path / "briefs"
    briefs.mkdir()
    cap = briefs / "brief_2026-08-03_post_ny.json"
    cap.write_text('{"schema":"naiad_daily_brief"}', encoding="utf-8", newline="\n")
    real_sha = hashlib.sha256(cap.read_bytes()).hexdigest()

    p = _log(tmp_path)
    _seed(p, 2, sha=real_sha)
    res = FL.verify_capture_linkage(p, briefs)
    assert res["ok"] is True and res["orphans"] == []
    assert res["captures_known"] >= 1

    _seed(p, 1, sha="deadbeef" * 8)
    bad = FL.verify_capture_linkage(p, briefs)
    assert bad["ok"] is False and len(bad["orphans"]) == 1
    assert bad["orphans"][0]["brief_json_sha256"].startswith("deadbeef")


def test_f_f5_real_log_if_present_links_to_real_captures():
    p = ROOT / "ops" / "forward_log.jsonl"
    if not p.exists() or not FL.read_lines(p):
        pytest.skip("no forward_log entries yet")
    assert FL.verify_chain(p)["ok"] is True
    assert FL.verify_capture_linkage(p)["ok"] is True


# --------------------------------------------------------------- schema

def test_record_schema_matches_the_contract():
    """§III.2's field list, asserted so the CLI and the record cannot drift."""
    p = Path(ROOT) / "ops"
    e = FL.make_entry("mechanical", "BTCUSDT", "4h", "long", "reclaim", 1.0,
                      2.0, [3.0], "2026-08-03", "post_ny", "s", "2.0.0", "1.2.0")
    assert set(e) == set(FL.FIELDS), (
        f"schema drift: missing {set(FL.FIELDS) - set(e)}, "
        f"extra {set(e) - set(FL.FIELDS)}")
    assert FL.KINDS == ("mechanical", "hypothetical", "actual")


def test_direction_and_status_are_validated():
    with pytest.raises(ValueError):
        FL.make_entry("mechanical", "B", "4h", "sideways", "t", 1.0, 2.0, [],
                      "2026-08-03", "post_ny", "s", "2.0.0", "1.2.0")
    with pytest.raises(ValueError):
        FL.make_entry("mechanical", "B", "4h", "long", "t", 1.0, 2.0, [],
                      "2026-08-03", "post_ny", "s", "2.0.0", "1.2.0",
                      status="winning")


def test_no_sizing_in_the_record_schema():
    """A diary of intent carries no size, and the schema is where that is
    enforced -- a field that does not exist cannot be filled in later."""
    for f in FL.FIELDS:
        assert not re.search(r"size|qty|quantity|notional|leverage|contracts",
                             f, re.I), f"sizing field {f!r} in the record schema"
