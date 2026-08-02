# status/ — convention

1. One append-only ledger per lane: `LEDGER_<LANE>.md` (ATHENA, APOLLO, ARGUS, DIONYSUS, HERMES, HEPHAESTUS).
2. `MANIFEST.json` — the integrity manifest, rewritten in place by `scripts/reviewer_manifest.py`.
3. `daily/` — the daily routine's staged outputs (`DAILY_<date>.md`, `MANIFEST_<date>.json`, brief artifacts).
4. `CADENCE.md` — the trigger registry: every scheduled or on-demand trigger, its owner, and its state.
5. Append, never rewrite: a correction is a new entry that supersedes, not an edit to an old one.
