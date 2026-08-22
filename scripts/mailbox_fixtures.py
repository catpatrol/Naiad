#!/usr/bin/env python
"""F-MB-1 -- the fixture that holds MAILBOX/ honest.

Seven legs, each printed with its FAILS IF.  The mailbox is wired into publish()'s
tail and into the daily routine, so its two dangerous properties are (a) that a
rebuild must be idempotent -- it runs twice on every routine day -- and (b) that its
prune step must be incapable of destroying a file with content.  Both are pinned here.

Run:  ~/venvs/naiad/bin/python scripts/mailbox_fixtures.py
"""

import hashlib
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mailbox_refresh as mb                                    # noqa: E402

BOX = REPO / mb.MAILBOX_DIRNAME
PLANTED_LINK = "__FMB1_dead_link__"
PLANTED_FILE = "__FMB1_real_file__.txt"
RESULTS = []


def check(leg, ok, fails_if, detail):
    RESULTS.append((leg, ok))
    print("  %-8s %s" % ("PASS" if ok else "**FAIL**", leg))
    print("           FAILS IF: %s" % fails_if)
    print("           observed: %s" % detail)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def snapshot():
    """(path -> (mtime_ns, sha256)) for every current link target."""
    out = {}
    for name, target, _tag in mb.desired(REPO)[0]:
        st = target.stat()
        out[target] = (st.st_mtime_ns, sha(target))
    return out


def links():
    return sorted(e for e in os.listdir(BOX)
                  if (BOX / e).is_symlink())


def main():
    print("F-MB-1 -- MAILBOX rebuild, seven legs")
    print("  repo   : %s" % REPO)
    print("  mailbox: %s/   ROLLING_N = %d" % (mb.MAILBOX_DIRNAME, mb.ROLLING_N))
    print()

    # ---- leg 0: the prune step cannot destroy content -----------------------
    src = (Path(mb.__file__)).read_text(encoding="utf-8")
    bad = [w for w in ("shutil.rmtree", "os.remove(", "os.rmdir(", "unlink(missing_ok")
           if w in src]
    # the ONE unlink call must be guarded by is_symlink()
    guarded = "if entry.is_symlink():" in src and src.count(".unlink()") == 1
    check("L0 no-destroy", not bad and guarded,
          "the module contains rmtree/os.remove, or its single unlink() is not inside "
          "the is_symlink() branch",
          "forbidden calls=%s  single-guarded-unlink=%s" % (bad or "none", guarded))

    # ---- leg 1: cold run creates links --------------------------------------
    before_targets = snapshot()
    r1 = mb.refresh(REPO)
    check("L1 rebuild", r1["error"] is None and r1["total"] > 0,
          "refresh() errors, or the mailbox ends up empty",
          "error=%s total=%d created=%d pruned=%d kept=%d"
          % (r1["error"], r1["total"], len(r1["created"]), len(r1["pruned"]), r1["kept"]))

    # ---- leg 2: every link resolves to a real file --------------------------
    broken = [n for n in links() if not (BOX / n).resolve().is_file()]
    check("L2 resolve", not broken,
          "any entry in MAILBOX/ is a symlink whose target is missing or is not a file",
          "%d link(s), %d broken %s" % (len(links()), len(broken), broken[:5]))

    # ---- leg 3: the printed count matches the disk --------------------------
    check("L3 count", r1["total"] == len(links()),
          "the count refresh() reports differs from the number of symlinks on disk",
          "reported=%d on-disk=%d" % (r1["total"], len(links())))

    # ---- leg 4: a planted DEAD link is pruned -------------------------------
    dead = BOX / PLANTED_LINK
    if dead.is_symlink():
        dead.unlink()
    dead.symlink_to(REPO / "__this_target_does_not_exist__")
    planted_present = dead.is_symlink()
    r2 = mb.refresh(REPO)
    check("L4 prune-dead", planted_present and PLANTED_LINK in r2["pruned"]
          and not dead.is_symlink(),
          "the planted dead link survives the rebuild, or is not named in `pruned`",
          "planted=%s pruned=%s still_present=%s"
          % (planted_present, PLANTED_LINK in r2["pruned"], dead.is_symlink()))

    # ---- leg 5: the next run is a no-op -------------------------------------
    r3 = mb.refresh(REPO)
    noop = (not r3["created"] and not r3["pruned"] and r3["kept"] == r3["total"])
    check("L5 idempotent", noop,
          "an immediately repeated rebuild creates or prunes anything, or `kept` does "
          "not account for every link",
          "created=%d pruned=%d kept=%d total=%d"
          % (len(r3["created"]), len(r3["pruned"]), r3["kept"], r3["total"]))

    # ---- leg 6: a REAL file in MAILBOX/ is left untouched -------------------
    real = BOX / PLANTED_FILE
    real.write_text("content that a prune must never destroy\n", encoding="utf-8")
    real_sha = sha(real)
    r4 = mb.refresh(REPO)
    survived = real.is_file() and sha(real) == real_sha
    check("L6 foreign-safe", survived and PLANTED_FILE in r4["foreign"],
          "a non-symlink file in MAILBOX/ is deleted or altered, or is not reported "
          "as `foreign`",
          "survived=%s reported_foreign=%s" % (survived, PLANTED_FILE in r4["foreign"]))
    if real.is_file() and sha(real) == real_sha:
        real.unlink()                       # remove only what THIS fixture planted
    mb.refresh(REPO)

    # ---- leg 7: no target was touched --------------------------------------
    after_targets = snapshot()
    moved = [p.name for p in before_targets
             if p in after_targets and before_targets[p] != after_targets[p]]
    check("L7 targets-untouched", not moved,
          "any link target's mtime or sha256 changed across four rebuilds",
          "%d target(s) compared, %d changed %s"
          % (len(before_targets), len(moved), moved[:5]))

    failed = [n for n, ok in RESULTS if not ok]
    print()
    print("F-MB-1: %d/%d PASS" % (len(RESULTS) - len(failed), len(RESULTS)))
    if failed:
        print("FAILED: %s" % ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
