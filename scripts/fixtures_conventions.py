#!/usr/bin/env python3
"""F-CONV-1..4 — the fixtures that hold the CONVENTIONS restructure honest.

Run: ~/venvs/naiad/bin/python scripts/fixtures_conventions.py

These are not unit tests of code; they are structural assertions about two
documents that the whole Pantheon reads. They exist because the 2026-08-15
collapse moved every rule in a 64 KB file and the only way to say "nothing was
lost" without being believed on trust is to count.

F-CONV-1  every «NAIAD-S*» token appears EXACTLY twice in CONVENTIONS.md
          (index row + section header) and NOWHERE else in the repo.
F-CONV-2  section 0 -- THE CORE, what every lane ingests every session --
          is at or under 6,000 bytes.
F-CONV-3  the memory-pointer tokens all resolve to a real section header.
F-CONV-4  rule census: zero rules lost, file shrinks, every extracted
          narrative is in CASELAW.md carrying a backlink.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CONV = REPO / "exchange" / "status" / "CONVENTIONS.md"
CASELAW = REPO / "docs" / "CASELAW.md"
CENSUS = REPO / "docs" / "CONVENTIONS_RULE_CENSUS_2026-08-15.md"

# The five tokens project memory points at. If one of these stops resolving, a
# memory entry has become a dangling pointer and the lane it steers reads
# nothing -- the failure mode the collapse was designed to make impossible.
MEMORY_POINTER_TOKENS = [
    "NAIAD-S0-CORE",
    "NAIAD-S2-PASTE",
    "NAIAD-S4-BOX",
    "NAIAD-S7-FRAMES",
    "NAIAD-S8-BACKUP",
]

CORE_BUDGET_BYTES = 6_000

# Size of exchange/status/CONVENTIONS.md immediately before the collapse,
# measured on disk at commit a2b69cf. Pinned, not imported: this is a
# historical figure and a historical figure reproduces history (CONVENTIONS
# S6, the named-constant protocol).
#
# READ THIS BEFORE "FIXING" A FAILURE OF THE SIZE CLAUSE.  This baseline is an
# ACCEPTANCE assertion about the 2026-08-15 collapse -- it proves the
# restructure made the rules file smaller on the day it landed.  It is NOT a
# permanent ceiling.  A rules file is supposed to grow as the project learns:
# new rules and dated corrections are the system working.  If this clause fails
# because a genuine rule or correction was added, the correct response is to
# RE-PIN this baseline with a dated note saying what grew and why -- never to
# delete a rule or trim a correction to get back under a number.  Deleting law
# to satisfy a fixture is the failure mode the fixture exists to prevent.
CONV_BYTES_BEFORE = 64_012

results: list[tuple[str, bool, str]] = []


def check(fixture: str, ok: bool, detail: str) -> None:
    results.append((fixture, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {fixture}: {detail}")


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def core_section_bytes(text: str) -> tuple[int, str]:
    """Bytes of section 0, from its header to the next top-level section."""
    start = text.index("## §0 ")
    nxt = text.index("\n## §1 ", start)
    body = text[start:nxt]
    return len(body.encode("utf-8")), body


def main() -> int:
    conv = read(CONV)

    # ---------------------------------------------------------------- F-CONV-1
    # Tokens live inside guillemets in the section headers and bare in the
    # index rows; count the bare identifier, which covers both.
    tokens = sorted(set(re.findall(r"NAIAD-S\d+-[A-Z]+", conv)))
    counts = {t: conv.count(t) for t in tokens}
    bad = {t: n for t, n in counts.items() if n != 2}

    # Uniqueness across the repo: grep -F, tracked files only. A token appearing
    # anywhere else is a SECOND HOME for a fact, which is the thing the collapse
    # exists to prevent.
    #
    # The allowlist below is not a loophole, it is the distinction the check
    # cannot make on its own: a second HOME versus a QUOTATION. CONVENTIONS is
    # the home. This script must name the memory-pointer tokens in order to
    # check them. And the collapse's own build document is required by the task
    # that commissioned it to reproduce the TOCs and section 0 VERBATIM, which
    # necessarily reproduces all nine tokens.
    #
    # Keep this list short and add to it deliberately. Every entry is a promise
    # that the file quotes CONVENTIONS rather than competing with it; a document
    # that starts *asserting* section content under a token belongs in neither
    # this list nor the repo.
    QUOTERS = {
        "exchange/status/CONVENTIONS.md",  # the home itself
        "scripts/fixtures_conventions.py",  # this checker
        "exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_COLLAPSE.md",
    }
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True
    ).stdout.split()
    strays: list[str] = []
    for rel in tracked:
        if rel in QUOTERS:
            continue
        p = REPO / rel
        if not p.is_file():
            continue
        try:
            body = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for t in tokens:
            if t in body:
                strays.append(f"{rel}:{t}")

    check(
        "F-CONV-1",
        not bad and not strays and len(tokens) == 9,
        f"{len(tokens)} tokens, all count==2 "
        f"({', '.join(f'{t}={n}' for t, n in sorted(counts.items()))}); "
        f"repo-unique outside CONVENTIONS: {'yes' if not strays else 'NO -> ' + ', '.join(strays)}"
        + (f"; OFFENDERS {bad}" if bad else ""),
    )

    # ---------------------------------------------------------------- F-CONV-2
    core_bytes, _ = core_section_bytes(conv)
    check(
        "F-CONV-2",
        core_bytes <= CORE_BUDGET_BYTES,
        f"section 0 = {core_bytes:,} B of {CORE_BUDGET_BYTES:,} B budget "
        f"({100.0 * core_bytes / CORE_BUDGET_BYTES:.1f}%), "
        f"headroom {CORE_BUDGET_BYTES - core_bytes:,} B",
    )

    # ---------------------------------------------------------------- F-CONV-3
    unresolved = []
    for t in MEMORY_POINTER_TOKENS:
        # Resolves == appears in a section header line beginning with '## '.
        if not re.search(rf"^## .*«{re.escape(t)}»", conv, re.M):
            unresolved.append(t)
    check(
        "F-CONV-3",
        not unresolved,
        f"{len(MEMORY_POINTER_TOKENS)} memory-pointer tokens, "
        f"{len(MEMORY_POINTER_TOKENS) - len(unresolved)} resolve to a section header"
        + (f"; UNRESOLVED {unresolved}" if unresolved else ""),
    )

    # ---------------------------------------------------------------- F-CONV-4
    conv_now = len(conv.encode("utf-8"))
    shrank = conv_now < CONV_BYTES_BEFORE

    caselaw = read(CASELAW)
    cl_ids = sorted(set(re.findall(r"^### (CL-\d+)", caselaw, re.M)))
    # Every case must carry a backlink naming the section whose rule it earned.
    cl_bodies = re.split(r"^### CL-\d+", caselaw, flags=re.M)[1:]
    no_backlink = [
        cid for cid, body in zip(cl_ids, cl_bodies) if "EARNS" not in body
    ]
    # Every case must be cited from CONVENTIONS, or it is an orphan record.
    uncited = [cid for cid in cl_ids if cid not in conv]

    census_ok = CENSUS.exists()
    census_txt = read(CENSUS) if census_ok else ""
    m_before = re.search(r"RULES BEFORE:\s*(\d+)", census_txt)
    m_after = re.search(r"RULES AFTER:\s*(\d+)", census_txt)
    m_lost = re.search(r"RULES LOST:\s*(\d+)", census_txt)
    before = int(m_before.group(1)) if m_before else -1
    after = int(m_after.group(1)) if m_after else -1
    lost = int(m_lost.group(1)) if m_lost else -1

    # Four clauses, reported one by one, because "F-CONV-4 FAILED" on its own
    # does not tell the next reader which half of the claim broke.
    clauses = [
        ("zero rules lost",
         census_ok and lost == 0 and after >= before,
         f"census {before} -> {after}, LOST {lost}"
         + ("" if census_ok else "  [census document missing]")),
        ("size shrinks",
         shrank,
         f"{CONV_BYTES_BEFORE:,} B -> {conv_now:,} B "
         f"({conv_now - CONV_BYTES_BEFORE:+,} B, "
         f"{100.0 * (conv_now - CONV_BYTES_BEFORE) / CONV_BYTES_BEFORE:+.2f}%)"),
        ("every narrative backlinked",
         bool(cl_ids) and not no_backlink,
         f"{len(cl_ids)} cases in CASELAW, all carry EARNS"
         + (f"; NO-BACKLINK {no_backlink}" if no_backlink else "")),
        ("every case cited from CONVENTIONS",
         not uncited,
         "all CL-n resolve both ways"
         + (f"; UNCITED {uncited}" if uncited else "")),
    ]
    failed_clauses = [n for n, ok, _ in clauses if not ok]
    check(
        "F-CONV-4",
        not failed_clauses,
        " · ".join(f"{n}: {d}" for n, _, d in clauses)
        + (f"  >>> FAILING CLAUSE(S): {', '.join(failed_clauses)}" if failed_clauses else ""),
    )
    for n, ok, d in clauses:
        print(f"         {'ok  ' if ok else 'FAIL'} {n} — {d}")

    failed = [f for f, ok, _ in results if not ok]
    print()
    print(f"F-CONV: {len(results) - len(failed)}/{len(results)} PASS")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
