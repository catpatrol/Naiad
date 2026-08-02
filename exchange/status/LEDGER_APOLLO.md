# LEDGER_APOLLO — append-only lane ledger

**Lane:** APOLLO — engine builds · repo operations · integrity & manifest.
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

=== STATUS_APOLLO — 2026-07-27 ===
NOW: Engine 1.0.11 frozen. Repo at manifest snapshot HEAD 60e00c9, ahead 4 / behind 0 vs origin 70a5be0, worktree clean. THE BIG CORRECTION: the raw price estate was never under OneDrive — it sat unprotected in AppData\Local\naiad\data_cache (633.5 MB, 71 files) for the project's whole life, and now has its first offsite backups on two independent Google Drive accounts.
LAST EVENT: 2026-07-27 — Estate protection established; OneDrive root-caused (quota exhaustion, 21.78 GB tree); 19.61 GB reclaimed across six archived phases (13,502 members, 0 mismatches, reviewer re-hashed 6/6 + 90 sampled members; 25 git-tracked files preserved in place); tree down to ~1.9 GB.
FACTS:
- Integrity at snapshot: 46/46 tracked sources match HEAD; box 19 repo copies match + 2 brief artifacts + 1 stale .gitignore [verified]
- Rulings R-A (cloud sessions scoped to Naiad only), R-B (second-cloud dated non-overwriting archives), R-C (corrections folded, 713dfa7→72b921f amended-SHA on record) [ratified]
- Standing rule: every paste-go opens with a hard environment assertion that halts — read-only included — and no write precedes it; gates written from POST-action state [ledger]
- Routing failures final count on 07-26/27: seven, not three; every labelled paste was halted by its header [ledger]
- %G? reports N when SSH verification is impossible, not only when unsigned — not a signature-presence test [verified]
PENDING:
1. PUSH RULING — unpushed commits were then the only asset without an off-machine copy
2. R-A' proposed, not ruled: cloud-session commits must push same-session or they don't count
3. s3_excursion_substrate.jsonl git-tracked while sibling substrates are fenced — exception or drift?
4. Remaining backup steps: six phase archives to the second cloud · .venv relocation · .gitignore sync exclusions
NEXT: Item 1 (push ruling), then a fresh MANIFEST.json to confirm ahead/behind returns to 0. Owner: operator.
METRICS: operator actions this session = not recorded (predates Q-8) · files re-ingested = not recorded
=== END STATUS ===

**Provenance note (HEPHAESTUS, 2026-08-02):** this seed entry is a synthesis of the lane's standing
status document, carried over unmodified in substance at ledger adoption. Source document:
`STATUS — ENGINE (engine builds · repo operations · integrity & manifest).txt` (repo root, 2,917 B,
updated 2026-07-27 late). It is dated 2026-07-27 and its PENDING items may since have been resolved —
several of them demonstrably were. **Treat as stale until APOLLO appends a current entry.** [handoff]
