#!/usr/bin/env python
"""mailbox_refresh.py -- MAILBOX/, the operator's one-click view of what is current.

WHY THIS EXISTS.  Six actors write into this repo and the operator is the transport
layer between them (CONVENTIONS §3.3).  Finding the current document meant knowing
which of four folders it landed in and what it was called.  MAILBOX/ is a flat folder
of SYMLINKS -- drag it into the Finder sidebar once and everything current is one
click away, and it refreshes itself on every publish and every daily routine.

WHAT IT IS NOT.  It is not a copy, not a backup, and not a second home for anything.
Every entry is a link; the file of record never moves and is never written to.  The
folder is gitignored, so nothing here reaches git, GitHub or the project box -- it
costs zero bytes of the box by construction.

THE TWO SETS.
  PINNED   -- always present, regardless of age: LEDGER.md, CONVENTIONS.md, every
              lane ledger, every queue item not yet stamped BUILT, and the working
              set the operator named on 2026-08-18.
  ROLLING  -- the newest ROLLING_N files by mtime across the report surfaces.

MEASURED, NOT MAINTAINED.  The lane ledgers are globbed, not listed; the active queue
is read through reviewer_manifest.queue_items(), the same parser MANIFEST.json uses,
so the mailbox cannot disagree with the manifest about what is open.  The only
hand-kept list is WORKING_SET, which is a named operator ruling and nothing else.

SAFETY.  The prune step unlinks SYMLINKS ONLY.  A real file found in MAILBOX/ is left
exactly where it is and reported as `foreign` -- this module contains no call that can
destroy a file with content, and no scheduled lane may delete anything (§4.1).
"""

import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- named constants
# One definition each.  publish_exchange and daily_routine both CALL refresh();
# neither copies a value from this block.  Changing one of these runs the
# named-constant protocol (CONVENTIONS §6.4) -- grep the NAME, the VALUE and the
# threshold text, and record a pin-vs-import decision per dependent.
MAILBOX_DIRNAME = "MAILBOX"
ROLLING_N = 25
ABOUT_NAME = "000_README.txt"          # managed by this module; never pruned, never foreign

# The rolling surfaces.  (directory, glob) -- the glob is what "top-level report
# renders only" means for research_outputs: `*.html` and not `**/*.html`, so the 30
# nested payload renders under research_outputs/<study>/ stay out of the mailbox.
ROLLING_SCOPES = (
    ("exchange/reports", "**/*"),
    ("exchange/queue", "**/*"),
    ("docs/history/reports", "**/*"),
    ("research_outputs", "*.html"),
)

# The living working set, named by the operator 2026-08-18 (box-cleanup brief).
# Entries are globs, so QUEUE-008-BUILD joins the mailbox the moment it is filed
# without this list being edited.  A pattern that matches nothing is REPORTED as
# missing, never skipped silently (CONVENTIONS §3.3).
WORKING_SET = (
    "exchange/reports/BRIEF_ATHENA_SAIL_REPO_2026-08-17.md",
    "exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-17_SAIL-STEP1-INVENTORY.md",
    "exchange/reports/*QUEUE-008-FILED*.md",
    "exchange/reports/*QUEUE-008-BUILD*.md",
    "exchange/reports/SS_SYSTEM_SYNTHESIS_2026-08-06.md",
    "exchange/reports/CENSUS2A_CLOSEOUT_2026-08-12.md",
    "exchange/reports/HANDOFF_APOLLO_NAIAD_SUCCESSION_2026-08-17.md",
    "exchange/reports/BUILD_2026-08-16_TIERC6_REVB.md",
)

ALWAYS_PINNED = ("LEDGER.md", "exchange/status/CONVENTIONS.md")
LANE_LEDGER_GLOB = "exchange/status/LEDGER_*.md"
QUEUE_DIR = "exchange/queue"

ABOUT_TEXT = """MAILBOX -- links, not copies.

Every item here is a shortcut to a file that lives somewhere else in ~/Naiad.
Opening one opens the real file.  Deleting one deletes only the shortcut.
The folder rebuilds itself on every publish and every daily routine: new work
appears, finished work drops off, broken shortcuts are cleared.

PINNED   the ledgers, CONVENTIONS, every open queue item, the current working set
ROLLING  the %d most recently changed reports, work orders and report renders

Nothing here is committed or published -- MAILBOX/ is gitignored.
"""


# ------------------------------------------------------------------- the two sets
def _active_queue_names():
    """Queue work orders not yet stamped BUILT, via the manifest's own parser.

    Falls back to EVERY work order if reviewer_manifest cannot be imported, and
    says so in the returned reason -- a mailbox holding one item too many is a
    nuisance, a mailbox silently holding one too few is a lost work order.
    """
    try:
        import reviewer_manifest
    except Exception as exc:                                    # noqa: BLE001
        return None, "reviewer_manifest unavailable (%s); pinning ALL queue items"% exc
    items = reviewer_manifest.queue_items()
    if items is None:
        return [], "exchange/queue/ does not exist"
    return [n for n, _rat, built in items if not built], ""


def desired(repo=REPO):
    """[(linkname, target Path, why)] for everything the mailbox should hold."""
    repo = Path(repo)
    notes = []
    pinned = [(repo / r, "pinned: core") for r in ALWAYS_PINNED if (repo / r).is_file()]
    missing = [r for r in ALWAYS_PINNED if not (repo / r).is_file()]

    for p in sorted(repo.glob(LANE_LEDGER_GLOB)):
        pinned.append((p, "pinned: lane ledger"))

    names, why = _active_queue_names()
    if why:
        notes.append(why)
    qdir = repo / QUEUE_DIR
    if names is None:                                            # degraded fallback
        for p in sorted(qdir.glob("*.md")):
            if p.name.lower() != "readme.md":
                pinned.append((p, "pinned: queue item (degraded: BUILT unknown)"))
    else:
        for n in names:
            p = qdir / n
            if p.is_file():
                pinned.append((p, "pinned: open queue item"))

    for pattern in WORKING_SET:
        hits = sorted(repo.glob(pattern))
        if hits:
            for p in hits:
                pinned.append((p, "pinned: named working set"))
        else:
            missing.append(pattern)

    pinned_paths = {p for p, _ in pinned}

    rolling = []
    for scope, pat in ROLLING_SCOPES:
        base = repo / scope
        if not base.is_dir():
            notes.append("rolling scope absent: %s" % scope)
            continue
        for p in base.glob(pat):
            if p.is_file() and not p.name.startswith("."):
                rolling.append(p)
    rolling = [p for p in set(rolling) if p not in pinned_paths]
    rolling.sort(key=lambda p: (-p.stat().st_mtime, p.name))
    rolling = [(p, "rolling: newest %d" % ROLLING_N) for p in rolling[:ROLLING_N]]

    out, taken = [], {}
    for p, tag in pinned + rolling:
        name = p.name
        if name in taken:                       # deterministic collision handling
            name = "%s__%s" % (p.parent.name, p.name)
        taken[name] = p
        out.append((name, p, tag))
    return out, sorted(set(missing)), notes


# ----------------------------------------------------------------------- the act
def refresh(repo=REPO, log=None):
    """Rebuild MAILBOX/ idempotently.  Creates missing links, prunes dead ones,
    never touches a target.  Returns a result dict; never raises."""
    repo = Path(repo)
    res = {"dir": None, "created": [], "pruned": [], "kept": 0, "total": 0,
           "missing": [], "foreign": [], "notes": [], "error": None}
    try:
        box = repo / MAILBOX_DIRNAME
        res["dir"] = MAILBOX_DIRNAME
        if not box.exists():
            box.mkdir(parents=True)
            res["notes"].append("created %s/ (it did not exist)" % MAILBOX_DIRNAME)
        want, missing, notes = desired(repo)
        res["missing"], res["notes"] = missing, res["notes"] + notes
        want_map = {n: p for n, p, _ in want}

        for entry in sorted(box.iterdir()):
            if entry.name == ABOUT_NAME:
                continue
            if entry.is_symlink():
                target = os.readlink(entry)
                keep = (entry.name in want_map
                        and Path(target) == want_map[entry.name].resolve()
                        and entry.resolve().exists())
                if keep:
                    res["kept"] += 1
                else:
                    entry.unlink()                     # SYMLINK ONLY -- see module docstring
                    res["pruned"].append(entry.name)
            else:
                res["foreign"].append(entry.name)      # a real file: left untouched

        for name, path, _tag in want:
            link = box / name
            if not link.is_symlink():
                link.symlink_to(path.resolve())
                res["created"].append(name)

        about = box / ABOUT_NAME
        text = ABOUT_TEXT % ROLLING_N
        if not about.exists() or about.read_text(encoding="utf-8") != text:
            about.write_text(text, encoding="utf-8")

        res["total"] = sum(1 for e in box.iterdir()
                           if e.is_symlink() or e.name == ABOUT_NAME) - 1
    except Exception as exc:                                  # noqa: BLE001
        # Broad on purpose: refresh() is called from publish()'s `finally`, and
        # publish() must never raise.  A mailbox that failed to rebuild is a line
        # on screen, never a failed publish or a failed daily routine.
        res["error"] = "%s: %s" % (type(exc).__name__, exc)
    if log:
        for line in report_lines(res):
            log(line)
    return res


def report_lines(res):
    if res["error"]:
        return ["mailbox: ERROR -- %s (links unchanged)" % res["error"]]
    out = ["mailbox: %d link(s) in %s/ -- %d created, %d pruned, %d unchanged"
           % (res["total"], res["dir"], len(res["created"]), len(res["pruned"]),
              res["kept"])]
    if res["missing"]:
        out.append("mailbox: %d pinned entr(ies) not on disk -- %s"
                   % (len(res["missing"]), ", ".join(res["missing"])))
    if res["foreign"]:
        out.append("mailbox: %d real file(s) present and LEFT UNTOUCHED -- %s"
                   % (len(res["foreign"]), ", ".join(res["foreign"])))
    for n in res["notes"]:
        out.append("mailbox: %s" % n)
    return out


def main(argv=None):
    res = refresh(REPO, log=print)
    if res["error"]:
        return 1
    for name, path, tag in sorted(desired(REPO)[0]):
        print("  %-72s  %s  [%s]" % (name, path.relative_to(REPO).as_posix(), tag))
    return 0


if __name__ == "__main__":
    sys.exit(main())
