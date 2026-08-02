# LEDGER_HEPHAESTUS — append-only lane ledger

**Lane:** HEPHAESTUS — local builder. Sole actor that touches the data estate
(`AppData\Local\naiad\data_cache`). Executes ratified queue items; heavy compute stays local.
**Adopted:** 2026-08-02, ruling Q-3 A (`FUNNEL_DIONYSUS_W1`). Append-only. Never edit a past entry; a
correction is a NEW entry that names what it supersedes. The central `LEDGER.md` remains the
*evidence* ledger and is untouched by this file — this one carries coordination state only.

**Entry template (naiad-eod format):**

```
=== STATUS_<LANE> — <date> ===
NOW: <2-3 sentences>
LAST EVENT: <date> — <one line>
FACTS: <up to 6 lines, each ending with [verified/ledger/ratified/handoff/unconfirmed-live/open]>
PENDING: <numbered items waiting on the operator>
NEXT: <single next action + owner>
METRICS: operator actions this session = <n> · files re-ingested = <n>
=== END STATUS ===
```

---

=== STATUS_HEPHAESTUS — 2026-08-02 ===
NOW: Ledger founded, and founded with work in it. This lane had no prior status document, so nothing before 2026-08-02 is claimed here — but this session's build is recorded in full: exchange v1 skeleton, per-lane ledgers, reviewer-box migration, manifest v1.1, auto-publish, both Windows triggers, and queue item 001.
LAST EVENT: 2026-08-02 — exchange v1 built end to end under gate A-7 authorization; full account in `exchange/reports/2026-08-02_HEPHAESTUS_report_exchange-v1-build.md`.
FACTS:
- `exchange/{status,queue,reports,drops}/` created with a content guard: text only, 1 MB per-file cap, larger artifacts referenced by path + sha256 pointer [verified]
- `_reviewer_box/` retired as a location: reports, `daily/` and `MANIFEST.json` migrated to `exchange/`; a one-line pointer README is left behind [verified]
- `scripts/reviewer_manifest.py` amended to v1.1: BOX_DIR repointed, F-M1 became a round-trip test with the self-hash kept as a secondary assertion, four new fields added [verified]
- Auto-publish added to `daily_routine.py` and `backup_estate.py` via `scripts/publish_exchange.py`: stages `exchange/**` only, refuses to push if anything else is staged [verified]
- Windows triggers armed: "Naiad daily routine" daily 07:00, "Naiad weekly backup" Sundays 08:00, both start-in the repo root, both calling the venv interpreter by full path [verified]
- `backup_estate.py` gained a retention REPORT (keep newest 4 estate generations + 1 phase set); it lists violations and never deletes [verified]
PENDING:
1. Queue item 001 awaits the operator's ratification stamp — it is not executable until stamped
2. The daily routine's brief job is optional and its behaviour under the 07:00 trigger is unproven until the first unattended run
NEXT: Work the queue once item 001 is ratified. Owner: operator (ratification), then HEPHAESTUS.
METRICS: operator actions this session = 1 · files re-ingested = 0
=== END STATUS ===
