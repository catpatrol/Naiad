# SECOND ACCOUNT — manual upload record

**This file exists because the second Google Drive account cannot be checked by
machine.** There is no API, no mounted drive, nothing `daily_routine.py` can
read. It is a genuine blind spot, and the only honest way to cover it is a date
the operator writes down.

## How it works

After you upload the newest archives to the second Google Drive account **in the
browser**, edit the date line below to the day you did it.

`daily_routine.py` compares that date against the newest estate and workflow
archive it can see in the primary destination. If an archive is newer than the
date, section 0 raises:

> **manual upload to the second Google Drive account is outstanding**

If the file is missing, or the date line is unreadable, that is *also* an alert —
an unknown state must never read as a healthy one, which is the same rule the
unreachable-destination check follows.

## Why a second account at all

The primary destination is one Google account. An account-level loss — suspension,
billing failure, a mistaken deletion that syncs — takes every generation with it
at once. The second account is the only copy that does not share that failure
mode, which is precisely why its state deserves an alarm rather than a good
intention.

## What to upload

The newest generations from `G:\My Drive\naiad-backups`:

- `naiad_estate_<date>.zip` — the price estate
- `naiad_workflow_<date>.zip` — the project's thinking

Phase archives in `research_outputs/_archive` are **permanent evidence and are
never pruned**; if the second account does not hold them, upload those too. Each
one is the only copy of a phase that will never be produced again.

---

<!-- EDIT THE LINE BELOW after each manual upload. Format: YYYY-MM-DD -->

last_manual_upload: 2026-07-28

<!-- Nothing else in this file is parsed. The line above is the whole record. -->
