# docs/memory — project memory snapshots

## The convention

1. **Snapshots are append-only, dated, and never edited.** A new export is a new file
   `claude_project_memory_<yyyy-mm-dd>.md`. An existing snapshot is never corrected in place — if it
   was wrong, it was wrong on that date, and that is part of the record.
2. **The newest snapshot supersedes older ones for READING ONLY.** Superseding is never done by
   deletion. Older snapshots stay exactly where they are, forever. They are how anyone reconstructs
   what was believed and when.
3. **Discrepancies resolve in favour of `LEDGER.md` first, then the newest snapshot.**

## Why these files exist at all

**Project memory is NOT included in Anthropic data exports.** It lives in the claude.ai project and
comes out by no automated route — not by export, not by backup, not by GitHub sync. If the project
were lost, so would every memory entry be.

**These snapshots are therefore the only durable copy.** That is the entire reason the directory
exists. They are covered by `backup_estate.py --workflow`, which archives `docs/memory/` dated and
sha-pinned to Google Drive weekly, so the durable copy is itself backed up.

The same is true of the operator's settings — user preferences, project instructions, custom style.
Those have their own hand-maintained file at [`docs/primers/OPERATOR_PREFERENCES.md`](../primers/OPERATOR_PREFERENCES.md),
for the same reason and with the same limitation: a human has to paste them.

## Current state — the snapshot on file is STALE

`claude_project_memory_2026-07-26.md` is **stale**. Dated 2026-07-26; a week old as of this note.

| | count |
|---|---|
| numbered operator-ratified entries **in this snapshot** | **19** (verified: Section 2 runs 1–19) |
| entries in live project memory | **29**, per the operator |

So on the operator's figure the snapshot is missing **ten** ratified entries, and everything added to
the auto-generated section since 2026-07-26 besides.

> **Discrepancy on record, for the operator to settle.** The instruction that prompted this file gave
> the snapshot's count as **21**. Counted directly, Section 2 of the file contains **19** numbered
> entries, highest number 19, last entry "Paste-routing convention (2026-07-26…)". The count above
> reports what the file actually holds. Whether the live figure is 29 against 19 or against 21
> changes the size of the gap, not its existence — a fresh export is due either way.

**Anything read from this snapshot should be treated as "true on 2026-07-26", not "true now".**

## Taking a new snapshot

Export both layers verbatim — the auto-generated project memory and the numbered operator-ratified
edits — into `claude_project_memory_<today>.md`, keeping the two-section structure the 2026-07-26 file
uses. Then update the table above. Do not delete anything.
