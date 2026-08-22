#!/usr/bin/env python
"""F-ROT-1..7 -- the fixtures that hold queue 003's repaired exemption honest.

The exemption input was `exchange/DIGEST.md` until ruling 007 retired it, after
which rotate_reports.py halted (exit 2) for seven days and no rotation could run
at all.  The 2026-08-22 correction replaces the DIGEST read with a rule computed
from the bus itself: THE NEWEST NOTE OF EACH LANE PAIR IS LIVE AND EXEMPT.

These fixtures pin the two properties that repair has to have -- it must protect
every live note, and it must be incapable of the unavailable state that broke it.

Run:  ~/venvs/naiad/bin/python scripts/rotation_exemption_fixtures.py
"""

import datetime as dt
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rotate_reports as rr                                     # noqa: E402

RESULTS = []


def check(leg, ok, fails_if, detail):
    RESULTS.append((leg, ok))
    print("  %-8s %s" % ("PASS" if ok else "**FAIL**", leg))
    print("           FAILS IF: %s" % fails_if)
    print("           observed: %s" % detail)


def main():
    print("F-ROT -- queue 003's exemption input after the 2026-08-22 correction")
    print("  scope     : %s/*.md      window: AGE_DAYS = %d" % (rr.SCOPE_DIR, rr.AGE_DAYS))
    print()

    today = dt.date(2026, 8, 22)

    # ---- F-ROT-1 : it classifies at all -----------------------------------
    raised = None
    try:
        parts = rr.classify(today)
    except Exception as exc:                                    # noqa: BLE001
        raised = "%s: %s" % (type(exc).__name__, exc)
        parts = None
    check("F-ROT-1 classifies", raised is None,
          "classify() raises -- the halt that ruling 007 caused is still there",
          "raised=%s" % (raised or "nothing"))
    if parts is None:
        print("\nF-ROT: 1/1 legs run, HALTED")
        return 1
    candidates, exempt, young, undated, cutoff, inbox = parts

    # ---- F-ROT-2 : every live note is exempt, BY NAME ----------------------
    # The operator's fixture.  Stated as a rule rather than a number: EVERY note
    # on the bus that is the newest of its lane pair must appear by name.
    live = rr.newest_note_per_lane_pair()
    exempt_names = {Path(rel).name for rel, _s, _w, _why in exempt}
    missing = sorted(live - exempt_names)
    print("           the exemption list, by name (%d):" % len(live))
    for n in sorted(live):
        s, r = rr.note_pair(n)
        print("             %-12s -> %-10s %s" % (s, r, n))
    check("F-ROT-2 live notes exempt by name", not missing,
          "any note that is the newest of its lane pair is absent from the "
          "exemption list",
          "%d live note(s), %d exempt, %d missing %s"
          % (len(live), len(exempt_names), len(missing), missing))

    # ---- F-ROT-3 : a SUPERSEDED note of the same pair is NOT exempt --------
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        (d / "NOTE_ARGUS_to_APOLLO_2026-08-03_old.md").write_text("old", encoding="utf-8")
        (d / "NOTE_ARGUS_to_APOLLO_2026-08-16_new.md").write_text("new", encoding="utf-8")
        got = rr.newest_note_per_lane_pair(d)
        ok3 = got == {"NOTE_ARGUS_to_APOLLO_2026-08-16_new.md"}
    check("F-ROT-3 superseded note rotates", ok3,
          "the older note of a pair is exempted too -- the exemption would then "
          "pin every note that ever existed and rotation would never reclaim one",
          "kept %s" % sorted(got))

    # ---- F-ROT-4 : broadcasts ARE exemptible (the old pattern's gap) -------
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        for n in ("NOTE_HERMES_2026-08-12_ALL-LANES_digest.md",
                  "NOTE_DIONYSUS_2026-08-12_PANTHEON_status.md"):
            (d / n).write_text("x", encoding="utf-8")
        got = rr.newest_note_per_lane_pair(d)
        old_pattern_would_match = [n for n in got
                                   if __import__("re").match(r"^NOTE_.+_to_.+", n,
                                                             __import__("re").I)]
    check("F-ROT-4 broadcasts exemptible", len(got) == 2 and not old_pattern_would_match,
          "a broadcast note is not exemptible -- the gap the old `^NOTE_.+_to_.+` "
          "pattern left open, which never protected a broadcast at all",
          "%d broadcast(s) exempt; matched by the OLD pattern: %d"
          % (len(got), len(old_pattern_would_match)))

    # ---- F-ROT-5 : the rule has NO external input --------------------------
    digest = REPO / "exchange" / "DIGEST.md"
    module_src = Path(rr.__file__).read_text(encoding="utf-8")
    no_digest_read = ("DIGEST_PATH" not in module_src
                      and "digest_inbox_names" not in module_src)
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        (d / "NOTE_ARGUS_to_APOLLO_2026-08-16_new.md").write_text("n", encoding="utf-8")
        survives = rr.newest_note_per_lane_pair(d) == {"NOTE_ARGUS_to_APOLLO_2026-08-16_new.md"}
    check("F-ROT-5 no external input", no_digest_read and survives,
          "the module still reads a DIGEST path, or the rule cannot be computed "
          "against a tree that has no DIGEST at all",
          "DIGEST read removed=%s · computes with no DIGEST present=%s · "
          "(the live tombstone at exchange/DIGEST.md exists=%s and is now irrelevant)"
          % (no_digest_read, survives, digest.is_file()))

    # ---- F-ROT-6 : still no delete path (queue 003 verdict criterion) -----
    banned = [w for w in ("os.remove", "shutil.rmtree", ".unlink(", "os.rmdir")
              if w in module_src]
    check("F-ROT-6 no delete path", not banned,
          "rotate_reports.py contains any delete call -- queue 003's verdict "
          "criterion is that the grep prints empty",
          "forbidden calls: %s" % (banned or "none"))

    # ---- F-ROT-7 : the ratified window is untouched ------------------------
    check("F-ROT-7 AGE_DAYS pinned", rr.AGE_DAYS == 30,
          "AGE_DAYS is not 30 -- the correction touched a ratified constant it "
          "had no authority over",
          "AGE_DAYS = %d · cutoff %s · candidates %d · exempt %d · too young %d"
          % (rr.AGE_DAYS, cutoff.isoformat(), len(candidates), len(exempt), len(young)))

    failed = [n for n, ok in RESULTS if not ok]
    print()
    print("F-ROT: %d/%d PASS" % (len(RESULTS) - len(failed), len(RESULTS)))
    if failed:
        print("FAILED: %s" % ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
