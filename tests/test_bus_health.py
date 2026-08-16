"""F-BH-1 -- the bus-health block, and the three ways it has already been got wrong.

Added 2026-08-15 with ruling 007, which retired exchange/DIGEST.md and put the
HERMES lane dormant.  Everything that lane measured by hand each cycle is now
measured by the two steps that already run: publish() and the daily routine.
A hand-built index goes stale silently; a measurement cannot, but only if the
measuring is right, and each clause below pins a mistake this project has
actually made rather than one it might make.

What this pins:
  * THE BLOCK PRINTS.  Not "prints when interesting" -- the F-4 head pair is
    stated even when the two heads AGREE, because a line that appears only on
    disagreement is indistinguishable from a broken check on the days it is
    silent, and F-4 was re-found in five separate cycles for want of it.
  * THE RECENCY READER MATCHES ALL THREE LIVE HEADER FORMS.  Finding F-5, made
    for real on 2026-08-12: a reader matching only `=== STATUS_X — date ===`
    missed `## date — ...`, published a false staleness reading, and it read as
    another lane's neglect.  A third form -- `STATUS ATHENA` with a SPACE --
    is live in five of ATHENA's most recent entries.
  * IT IS NOT TOO LOOSE EITHER.  Grepping for any date returns forward-looking
    rotation due-dates out of prose (2026-08-28, 2026-09-05 were both returned
    this way).  Headers only, real ISO dates only.
  * THE FENCED TEMPLATE LINE, present in all six ledgers, is not an entry.
  * THE FOLDER ROWS RECONCILE to their own total -- a breakdown that does not
    add up is worse than none, because it looks checked.
  * THE RECENCY TABLE MATCHES A HAND ENUMERATION taken independently, by a
    different reader, on the live tree.
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import daily_routine as D                                       # noqa: E402
import publish_exchange as P                                    # noqa: E402


# --------------------------------------------------------------- the block prints
def test_fbh1_block_prints_every_component():
    """The rendered block carries the total, every folder row, and the heads."""
    sized = [(100, "exchange/reports/a.md"), (50, "exchange/queue/b.md")]
    lines = P.bus_health_lines(P.folder_rows(sized), 150, 2, "test basis",
                               "a" * 40, "b" * 40, delta=(3, 0))
    text = "\n".join(lines)
    assert "150 B in 2 file(s)" in text
    assert "test basis" in text
    assert "reports/" in text and "queue/" in text
    assert "aaaaaaa" in text and "bbbbbbb" in text
    assert "F-4 LAG" in text and "3 commit(s)" in text


def test_fbh1_heads_print_even_when_equal():
    """THE CLAUSE THIS FIXTURE EXISTS FOR.

    Equal heads must still produce a line, and it must say so in words rather
    than by saying nothing.
    """
    line = P.head_pair_line("c" * 40, "c" * 40)
    assert line, "an in-sync head pair produced no line at all"
    assert "IN SYNC" in line
    assert "ccccccc" in line
    # ...and the same call must not be mistaken for the lag case.
    assert "F-4 LAG" not in line


def test_fbh1_head_pair_degrades_without_raising():
    """Every unknown is a word in the line, never an exception."""
    assert "unknown" in P.head_pair_line(None, "d" * 40)
    assert "unknown" in P.head_pair_line("d" * 40, None)
    assert "unknown" in P.head_pair_line(None, None)


def test_fbh1_manifest_head_survives_a_malformed_manifest(tmp_path):
    """json.JSONDecodeError is a ValueError and is NOT in publish()'s except
    clause, so an unguarded read here would escape a function documented never
    to raise.  Both bad states must return None instead."""
    (tmp_path / "exchange" / "status").mkdir(parents=True)
    (tmp_path / P.MANIFEST_REL).write_text("{not json", encoding="utf-8")
    assert P.manifest_head(tmp_path) is None
    assert P.manifest_head(tmp_path / "nowhere") is None


def test_fbh1_manifest_head_survives_valid_json_that_is_not_an_object(tmp_path):
    """The case the first version of this fixture stopped one inch short of.

    `[]`, `null` and a bare string are all VALID json, so they sail past the
    ValueError guard and then blow up on .get with an AttributeError -- which
    publish()'s except clause does NOT catch.  Found by adversarial review
    after the first fixture passed.
    """
    (tmp_path / "exchange" / "status").mkdir(parents=True)
    for payload in ("[]", "null", '"bare string"', "5", "true"):
        (tmp_path / P.MANIFEST_REL).write_text(payload, encoding="utf-8")
        assert P.manifest_head(tmp_path) is None, f"{payload} was not handled"


# --------------------------------------------------------------- head verdict
def test_fbh1_verdict_is_one_function_for_both_renderers():
    """The publish line and the DAILY table must not drift apart, which they
    can only be stopped from doing by sharing the branch."""
    assert P.head_verdict("a" * 40, "a" * 40) == ("IN SYNC", "")
    assert P.head_verdict(None, "a" * 40)[0] == "NOT ENUMERABLE"
    assert P.head_verdict("a" * 40, "b" * 40, (5, 0))[0] == "F-4 LAG"


def test_fbh1_manifest_ahead_is_not_reported_as_behind_by_zero():
    """A two-dot range returns 0 when the manifest is AHEAD of live HEAD, and
    the line then said 'F-4 LAG, manifest is 0 commit(s) behind' -- the one
    manifest-vs-git relation this block exists to state, stated wrongly."""
    verdict, detail = P.head_verdict("a" * 40, "b" * 40, (0, 3))
    assert verdict == "MANIFEST AHEAD"
    assert "behind by 0" not in detail
    assert P.head_verdict("a" * 40, "b" * 40, (2, 3))[0] == "DIVERGED"


# --------------------------------------------------------------- folder rows
def test_fbh1_folder_rows_reconcile_to_their_total():
    sized = [(10, "exchange/reports/a.md"), (20, "exchange/reports/b.md"),
             (30, "exchange/status/c.md"), (40, "exchange/status/daily/d.json"),
             (5, "exchange/DIGEST.md")]
    rows = P.folder_rows(sized)
    assert sum(b for _, b, _ in rows) == sum(s for s, _ in sized) == 105
    assert sum(n for _, _, n in rows) == len(sized) == 5


def test_fbh1_nested_daily_is_broken_out_not_double_counted():
    """status/daily is inside status/.  Counting it in both is the easy bug and
    it makes the rows stop adding up."""
    sized = [(30, "exchange/status/c.md"), (40, "exchange/status/daily/d.json")]
    rows = dict((k, b) for k, b, _ in P.folder_rows(sized))
    assert rows["status/"] == 30
    assert rows["status/daily/"] == 40


def test_fbh1_root_files_are_gathered():
    rows = dict((k, b) for k, b, _ in P.folder_rows([(5, "exchange/DIGEST.md")]))
    assert rows == {"(root)": 5}


# --------------------------------------------------------------- recency reader
TODAY = date(2026, 8, 15)


def _recency(tmp_path, lane, body):
    (tmp_path / f"LEDGER_{lane}.md").write_text(body, encoding="utf-8")
    return dict((l, w) for l, w, _ in D.ledger_recency(tmp_path, today=TODAY))


def _recency_note(tmp_path, lane, body):
    (tmp_path / f"LEDGER_{lane}.md").write_text(body, encoding="utf-8")
    return dict((l, n) for l, _, n in D.ledger_recency(tmp_path, today=TODAY))


def test_fbh1_recency_matches_all_three_live_header_forms(tmp_path):
    """All three shapes are live in the ledgers TODAY.  Finding F-5 was caused
    by knowing only the first."""
    rows = _recency(tmp_path, "APOLLO", "=== STATUS_APOLLO — 2026-08-14 ===\n")
    assert rows["APOLLO"] == "2026-08-14"

    rows = _recency(tmp_path, "ATHENA", "=== STATUS ATHENA — 2026-08-15 — x ===\n")
    assert rows["ATHENA"] == "2026-08-15", "the SPACE form was missed"

    rows = _recency(tmp_path, "ARGUS", "## 2026-08-11 — ARGUS acknowledges\n")
    assert rows["ARGUS"] == "2026-08-11", "the '## date —' form was missed"


def test_fbh1_recency_ignores_forward_looking_prose_dates(tmp_path):
    """Too loose fails as badly as too strict, and more embarrassingly."""
    rows = _recency(tmp_path, "APOLLO",
                    "=== STATUS_APOLLO — 2026-08-15 ===\n"
                    "- rotation per queue 003, next ~2026-08-28\n"
                    "- INTERFACE rotates 2026-09-05\n")
    assert rows["APOLLO"] == "2026-08-15"


def test_fbh1_recency_ignores_the_fenced_template_line(tmp_path):
    """The literal `=== STATUS_<LANE> — <date> ===` sits in all six ledgers."""
    rows = _recency(tmp_path, "HERMES",
                    "```\n=== STATUS_<LANE> — <date> ===\n```\n"
                    "=== STATUS_HERMES — 2026-08-04 ===\n")
    assert rows["HERMES"] == "2026-08-04"


def test_fbh1_recency_takes_the_max_not_the_last(tmp_path):
    """Entries are appended, but ATHENA's ledger ends with a cross-lane entry,
    so 'the last header in the file' is the wrong rule in general."""
    rows = _recency(tmp_path, "ATHENA",
                    "=== STATUS_ATHENA — 2026-08-15 ===\n"
                    "=== STATUS_HEPHAESTUS — 2026-08-13 ===\n")
    assert rows["ATHENA"] == "2026-08-15"


def test_fbh1_recency_ignores_a_future_dated_header(tmp_path):
    """A typo'd year, or a planning heading, must NOT pin a lane at 'fresh'
    and hide a genuinely stale ledger underneath.  This is finding F-5 in the
    direction the obvious fixture does not test."""
    rows = _recency(tmp_path, "APOLLO",
                    "=== STATUS_APOLLO — 2027-08-15 ===\n"
                    "=== STATUS_APOLLO — 2026-06-01 ===\n")
    assert rows["APOLLO"] == "2026-06-01", "a future-dated header won max()"
    note = _recency_note(tmp_path, "APOLLO",
                         "=== STATUS_APOLLO — 2027-08-15 ===\n"
                         "=== STATUS_APOLLO — 2026-06-01 ===\n")["APOLLO"]
    assert "future-dated" in note, "the discard was silent"


def test_fbh1_recency_ignores_an_impossible_date(tmp_path):
    """`\\d{4}-\\d{2}-\\d{2}` happily matches 2026-13-45."""
    rows = _recency(tmp_path, "APOLLO",
                    "=== STATUS_APOLLO — 2026-13-45 ===\n"
                    "=== STATUS_APOLLO — 2026-06-01 ===\n")
    assert rows["APOLLO"] == "2026-06-01"


def test_fbh1_iso_anchor_is_load_bearing(tmp_path):
    """MUTATION-DRIVEN.  Adversarial review deleted the ISO anchor from the
    regex and the whole fixture still passed 16/16, which meant the docstring
    bullet 'real ISO dates only' was pinned by nothing.  A template line with
    a non-date placeholder must not become an entry.
    """
    rows = _recency(tmp_path, "HERMES",
                    "=== STATUS_HERMES — not-a-date ===\n"
                    "=== STATUS_HERMES — 2026-08-04 ===\n")
    assert rows["HERMES"] == "2026-08-04"


def test_fbh1_dormant_lane_is_labelled_not_just_aged(tmp_path):
    """The block that ABSORBED HERMES's staleness duty must not then report
    HERMES as the stalest lane forever -- §5 says nothing waits on HERMES."""
    note = _recency_note(tmp_path, "HERMES",
                         "=== STATUS_HERMES — 2026-08-04 ===\n")["HERMES"]
    assert "DORMANT" in note and "007" in note


def test_fbh1_recency_reports_a_missing_ledger_as_not_enumerable(tmp_path):
    rows = D.ledger_recency(tmp_path)
    assert len(rows) == 6
    assert all(w is None for _, w, _ in rows)
    assert "no ledger file" in rows[0][2]


def test_fbh1_recency_table_renders_every_lane():
    lines = D.ledger_recency_lines(
        [("APOLLO", "2026-08-15", "3 entry header(s)"),
         ("HERMES", None, "no entry header matched")], "2026-08-15")
    text = "\n".join(lines)
    assert "APOLLO" in text and "2026-08-15" in text
    assert "NOT ENUMERABLE" in text


# --------------------------------------------------------------- live tree
def test_fbh1_recency_matches_the_hand_enumeration():
    """THE ACCEPTANCE ANSWER, and it was produced independently.

    These six dates were hand-enumerated on the live tree by a separate reader
    that had not seen this parser, and they agree with a second enumeration
    made earlier the same day for the DIGEST-refresh draft (F-DIG-6).  Two
    hands, one answer.

    A lane whose date moves ABOVE its pin is the ledger being used and is not a
    failure -- re-pin it.  A lane whose date moves BELOW its pin is the parser
    losing an entry form, which is finding F-5 happening again, and that is
    what this clause is here to catch.
    """
    PINNED = {"APOLLO": ("2026-08-15", 26), "ARGUS": ("2026-08-11", 2),
              "ATHENA": ("2026-08-15", 24), "DIONYSUS": ("2026-08-13", 3),
              "HEPHAESTUS": ("2026-08-15", 2), "HERMES": ("2026-08-04", 2)}
    rows = D.ledger_recency()
    live = dict((lane, (when, note)) for lane, when, note in rows)
    assert set(live) == set(PINNED)
    for lane, (pinned_date, pinned_count) in PINNED.items():
        when, note = live[lane]
        assert when is not None, f"{lane}: no entry header matched at all"
        assert when >= pinned_date, (
            f"{lane}: recency went BACKWARDS, {when} < {pinned_date} -- "
            "the reader has stopped matching a header form (finding F-5)")
        # The COUNT is pinned too.  Dates alone let a parser that silently
        # dropped 22 of ATHENA's 24 entries pass, so long as it kept the
        # newest -- which is exactly the failure shape of F-5.
        count = int(note.split()[0])
        assert count >= pinned_count, (
            f"{lane}: entry count FELL, {count} < {pinned_count} -- "
            "the reader is losing entries (finding F-5)")


def test_fbh1_section_8_assembles_on_the_live_tree():
    """The whole block, end to end, against the real repo: it must render, and
    it must not raise even though rotate_reports currently HALTS."""
    lines = D.bus_health_lines(date.today().isoformat())
    text = "\n".join(lines)
    assert "| folder | bytes | files | % of box |" in text
    assert "manifest records" in text and "live HEAD" in text
    assert "Ledger recency" in text
    for lane in D.LEDGER_LANES:
        assert lane in text
    assert "rotation candidates" in text.lower()


def test_fbh1_daily_table_prints_the_verdict_when_heads_agree(monkeypatch):
    """THE RULING'S HEADLINE CLAUSE, asserted against the renderer that lands
    in the PUBLISHED report.

    The equal-heads case cannot occur naturally on this tree -- the live
    manifest is dozens of commits behind -- so it is injected.  Before this,
    the clause was pinned only on the console renderer while the DAILY table
    re-implemented the branch itself and went untested.
    """
    same = "e" * 40
    monkeypatch.setattr(D.publish_exchange, "measure_head_pair",
                        lambda _repo: (same, same, None))
    text = "\n".join(D.bus_health_lines("2026-08-15"))
    assert "**IN SYNC**" in text
    assert "eeeeeee" in text
    assert "F-4 LAG" not in text


def test_fbh1_daily_table_states_the_lag_when_heads_differ(monkeypatch):
    monkeypatch.setattr(D.publish_exchange, "measure_head_pair",
                        lambda _repo: ("a" * 40, "b" * 40, (7, 0)))
    text = "\n".join(D.bus_health_lines("2026-08-15"))
    assert "F-4 LAG" in text and "7 commit(s)" in text


def test_fbh1_rotation_line_reports_rather_than_raises():
    """Ruling 007 left the queue-003 exemption without a source, so this path
    is EXPECTED, not exceptional.  It must produce a stated reason and never
    propagate -- an unattended 07:00 run must not die for a report line."""
    lines = D.rotation_candidate_lines(date.today().isoformat())
    assert lines
    assert any("rotation candidates" in l.lower() for l in lines)
