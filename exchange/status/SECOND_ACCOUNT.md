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

The newest generations from `D:\naiad-backups` — the LaCie external disk:

- `naiad_estate_<date>.zip` — the price estate
- `naiad_workflow_<date>.zip` — the project's thinking

> **CORRECTION 2026-08-12 — the source folder moved.** This section previously read
> `G:\My Drive\naiad-backups`. The operator moved the folder to `D:\naiad-backups` on
> 2026-08-12; `G:\My Drive\naiad-backups` still exists but is **empty (0 files, verified
> this session)**, so following the old instruction would have found nothing to upload.
> The sentence above is rewritten rather than annotated, per the correction rule at the
> top of `CONVENTIONS.md`: a reader believes what they read first.
>
> **This makes the manual upload MORE important, not less.** `D:` is a physical external
> disk. It is registered with Google Drive as a mirrored folder, but every upload attempt
> for these files is currently logging `CreateHardLinkW failed` — `D:` is exFAT, which has
> no hard links — and no upload-completion record exists in Drive's own logs. Until that is
> resolved, **the second-account upload is the only copy of the estate that is provably not
> on this desk.** See the 2026-08-12 build report, open item O-1.

Phase archives in `research_outputs/_archive` are **permanent evidence and are
never pruned**; if the second account does not hold them, upload those too. Each
one is the only copy of a phase that will never be produced again.

---

<!-- EDIT THE LINE BELOW after each manual upload. Format: YYYY-MM-DD -->

last_manual_upload: 2026-08-05

<!-- Nothing else in this file is parsed. The line above is the whole record. -->
