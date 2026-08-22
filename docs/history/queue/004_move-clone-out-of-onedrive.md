# 004 · Move the working clone out of OneDrive to `C:/Naiad`

RATIFIED: **operator, 2026-08-12** — "ratify 004". Drafted ATHENA 2026-08-12; **redrafted the same
day** against the seven objections in `BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-HALT.md`.
Executor: HEPHAESTUS. **Three phases, separate operator gos.**

## ⚠ CHANGED AFTER THE OPERATOR'S STAMP — veto any line
He stamped a draft that had not been filed. Intent unchanged; these seven details are not:
(1) Phase 0's justification was **refuted** and is rewritten prospectively — the 2026-08-09 backup
failures targeted `G:`, not `D:`, and were root-caused to `backup_estate.py` returning 1 on a
publish-step stumble. (2) D-0b covers **9** wiring points, not 3. (3) The gate rule lands in the
residency notes, not CONVENTIONS §2. (4) O-5 gains ordering and ` (N)` handling. (5) **O-5 is
removed from Phase 0** — a retention-policy disagreement must not block a data-safety move.
(6) `C:/Naiad` is pinned for **path length and sync-tree exit**; the residency-parallelism argument
is dropped as decoration. (7) **D-0a ships first and measures**; no timing constants are pinned in
advance of measurement.

## Why this exists
The clone sits inside OneDrive. That has cost one outage (2026-07-27, quota exhaustion) and one
scare (2026-08-12, an accidental "Free up space" that dehydrated 164 files under a live git repo).
**OneDrive is not this project's protection** — GitHub holds tracked files, `D:` holds bulk data,
Drive holds archives. Its presence adds a hazard, consumes quota, and lengthens every path by ~60
characters against Windows' 260-character limit.

**Destination, PINNED: `C:/Naiad`** — the repo root itself. Internal storage that never sleeps,
outside every sync tree, short.

---

## PHASE 0 — the drive must be allowed to wake (prerequisite)

**Prospective justification, and only prospective.** After the move, and under the D: residency
rule, more work depends on an external disk than ever before: `--phase` archives, the `seq8` mirror,
Phase A's own A-6 mirror. Every gate today reads `[ -d "D:/Naiad" ]` — a single call that returns
false in milliseconds on a spun-down disk. **We would be treating "asleep" as "absent."** The
operator has since disabled USB selective suspend and disk-sleep on AC, which likely removes the
common case; this covers battery use, unplug events and USB dropouts, and makes the failure
distinguishable either way.

**D-0a · `scripts/drive_wait.py` — SHIPS FIRST, ALONE, AND MEASURES.**
`wait_for_drive(root, attempts=None, delay=None)`. Attempts access; on failure pokes the drive root
to trigger spin-up (wrapped, never raising); sleeps; retries. Returns three distinguishable states,
never raises: **PRESENT** · **WOKE** (prints elapsed seconds) · **UNREACHABLE**. Defaults are
**PROVISIONAL and marked as such in the source**. Every WOKE appends one line to
`exchange/status/DRIVE_WAKE_LOG.md` — date, root, attempts, elapsed. **The constants are pinned by a
later one-line amendment once that log holds real observations.** Reachable is not writable: the
caller still write-probes.

**D-0b · Wire it in — 9 points, enumerated at build time, not assumed.** Grep `backup_estate.py`,
`daily_routine.py`, `reviewer_manifest.py` and `archive_dependencies.py` for every `D:`/`G:`
existence check; print the full list with file and line **before editing**; wire each. Include the
two stale `REPO/research_outputs/_archive` paths (`daily_routine.py:537`,
`archive_dependencies.py:52`). **`G:` gates are excluded** — a Drive mount is not a sleeping disk.
The daily job is the priority: it is the most frequent unattended run.

**D-0e · The missed-run detector (the operator's chronic fix).** On every routine run, compare
`HEARTBEAT.md`'s last completion against the expected daily cadence, **enumerate the missing
`DAILY_*` dates by name**, and print them at the top of the day's report. Report-only; no backfill,
no catch-up execution. Pairs with F-P6, which already reports staleness at publish. A skill cannot
do this — it is machine state, so it lives in the machine.

**D-0d · One line into the residency notes:** *a single failed lookup measures that lookup, not
absence — of a file, a task, or a disk.*

**Fixtures.** F-0-1 all three states asserted; UNREACHABLE via a nonexistent letter; elapsed printed.
F-0-2 `--workflow` succeeds through the helper, 0 mismatches. F-0-3 D-0e prints a synthetic 3-day gap
by date, and prints nothing when there is none. F-0-4 full suite still green (expect 287/1).

---

## PHASE A — copy, verify, repoint (reversible; separate go)

**A-0 pre-flight, all must pass:** HEAD == origin (nothing unpushed) · untracked set enumerated with
`--untracked-files=all`, **never `--porcelain` alone — it collapses an untracked directory to one
line** · `D:` reachable via `wait_for_drive` · destination volume free space ≥ 3× tree · **zero
dehydrated files** (a placeholder copies as a stub).

**A-1 · Hardcoded-path sweep, print the empty result if empty.** Grep everything for `OneDrive`,
`Midas-Claude`, and the absolute old path.

**A-2 · BLOCKING — the three identity gates.** `CONVENTIONS.md:253`, `prompts/CONTRACT_v4…:38`, and
the SEQ8 queue contract all **assert the path contains `OneDrive`**. `C:/Naiad` fails both conjuncts,
so **without this amendment no post-move session can start**. New form, two-sided: HALT if the path
contains `OneDrive`; HALT unless it ends with `C:/Naiad`. Also fix the three prose assertions
(`daily_routine.py:551`, `reviewer_manifest.py:411`, `DIGEST.md:145`); `backup_estate.py:371` already
degrades correctly and is the model.

**A-3 · Copy, never clone.** A clone brings only tracked files and would strand `seq8` (1,783 MB),
`census`, `mc1`. Copy the whole tree including `.git`. No-clobber. Delete `__pycache__` afterwards —
74 `.pyc` files embed the old path.

**A-4 · Verify:** every tracked file sha256-equal; `rev-parse HEAD` identical; `status --porcelain`
byte-identical; untracked set identical by name and hash; gitignored bulk equal by count and bytes,
hashed above 100 MB and on a 5% sample.

**A-5 · Run from the new location before trusting it:** full suite (287/1), routine end-to-end, one
publish. Any pass-there-fail-here → **reject and delete the destination**.

**A-6 · Scheduler:** repoint all three tasks, **read each back from XML**, preserve
`StartWhenAvailable` and the logon principal the operator set on 2026-08-12.

**A-7 · Mirror `research_outputs/census/**` and `mc1/**` to `D:`** copy-only, sha-verified, via
`wait_for_drive`.

**A-8 · Operator actions, BRIGHT COLOURS:** re-attach the Cowork folder at the new path — **HERMES
and DIONYSUS lose their mount and cannot tell you**; a stale mount reads a frozen bus.

## PHASE B — decommission the old tree (separate go, ≥3 days later, one clean scheduled run)
Re-verify tracked-file identity · delete the old tree — **the only irreversible step** · print the
reminder: **deleting inside OneDrive fills the online recycle bin, and quota is not reclaimed until
the operator empties it at onedrive.com.**

## Verdict criteria
Per phase. ACCEPT Phase A only if every fixture passes, not one tracked file differs, suite+routine+
publish pass **in the destination**, a shell in the old path halts under the new gate, and all three
tasks read back correct. **REJECT = delete the destination**; the old tree is untouched throughout.

## What this phase is NOT
Not a fresh clone · not a change to `D:` residency, the estate cache, the venv, GitHub, the box, or
any backup destination · not an OneDrive uninstall · not a quota fix by itself · **not O-5**, which
is a separate ATHENA item.

---

BUILT: 2026-08-22 (retroactive) — Phase A executed 2026-08-12; Phase B superseded by
Queue 005 and the pending PC-decommission phase.

*Context, so "retroactive" is not read as a claim that anything ran today: Phase A landed
on 2026-08-12 and is filed at
`docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-PHASE-A.md`.
Phase B — deleting the old OneDrive tree — was never run and is now moot: Queue 005 moved
the project to a MacBook on 2026-08-14/15, so the Windows tree this contract was written to
decommission is not on the machine any more. What remains of Phase B belongs to the pending
PC-decommission phase, not to this contract. The stamp is dated 2026-08-22 because that is
when it was written, not when the work happened; the work's own date is above.*
