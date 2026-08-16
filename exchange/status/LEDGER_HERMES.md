# LEDGER_HERMES — append-only lane ledger

**Lane:** HERMES — digest, staleness stamps, drops filing and naming (G-11), queue validation and
sequencing. Never re-authors content; never instructs a lane without the operator's stamp.
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

=== STATUS_HERMES — 2026-08-02 ===
NOW: Ledger founded. HERMES has not yet run: the infrastructure he operates on — `exchange/drops/`, `exchange/queue/`, `DIGEST.md` and this ledger — was created for him this session by HEPHAESTUS, and stands empty and waiting. This is a founding line; no history is claimed before this date.
LAST EVENT: 2026-08-02 — ledger founded by HEPHAESTUS during the exchange v1 build (ruling Q-3 A).
FACTS:
- No prior LEDGER_HERMES existed; nothing before 2026-08-02 is recorded here [verified]
- Charter ruled Q-4 A: hybrid — scheduled remote run 1-2x/day (digest, staleness) plus on-demand local session (hash/manifest verification, drops filing, queue grooming) [ratified]
- CRONOS is resolved into this lane (gate W-3): the time/cadence function is the schedule itself plus staleness stamps; there is no seventh agent [ratified]
- Two standing constraints: never re-author content; never instruct a lane without the operator's stamp [ratified]
- `DIGEST.md` exists as a placeholder only and is not authoritative until HERMES' first pass [verified]
- The HELIOS tripwire is on record: spawn only if HERMES misses two consecutive cycles, or ends up both executing study runs and verifying them [ratified]
PENDING:
1. Hermes' scheduled trigger (2x/day) is NOT armed — it is Hermes-side and waits on the F4 experiment
2. First pass: build DIGEST.md from the lane ledgers, the queue and the manifest
3. Weekly tally of the Q-8 metrics once two or more sessions have reported them
NEXT: Await the F4 result, then arm the Hermes schedule. Owner: operator / DIONYSUS (F4).
METRICS: operator actions this session = 0 · files re-ingested = 0
=== END STATUS ===

---

=== STATUS_HERMES — 2026-08-04 ===
NOW: First end-to-end run executed against PRIMER_HERMES v2 §6, all seven steps. `DIGEST.md` placeholder
replaced with the first real pass. Nine findings raised, none adjudicated. Wrote two files, both inside
`exchange/`; deleted nothing; instructed no lane.
LAST EVENT: 2026-08-04 — HERMES first run; DIGEST.md authored, this entry appended.
FACTS:
- Manifest is clock-fresh (40 min) but content-stale: repo moved 2 commits past its HEAD `484d62c8` to
  `afa5013` (efaf44b auto-publish, then afa5013 retention fix) before this run began [verified]
- Integrity spot-check: 10 files hashed via Python hashlib binary reads; 4 had manifest rows; 4/4 MATCH,
  0 mismatches. Manifest-wide 46 sources, 0 with `match_head: false` [verified]
- Manifest pins 16 of 66 `exchange/` files (24%), all under `status/` — `queue/`, `reports/` and
  `drops/` are entirely unhashed [verified]
- Content guard breached once: `reports/CAPTURE_2026-08-03_post_ny.json` = 1,879,133 B vs a 1 MB cap;
  67% of the whole exchange tree by bytes [verified]
- `reports/` naming convention holds for 8 files and is broken by 33 (80% deviation); every conforming
  file is HEPHAESTUS's [verified]
- RETENTION.md phase-archive defect is FIXED, not pending — regenerated 2026-08-04T00:42:06Z, 9 archives
  / 1,043,591,544 B all marked permanent. Primer's carry-forward warning is closed on evidence [verified]
- `allow_cowork_file_delete`, granted in an earlier session, was still in force at this session's start —
  the permission does not expire. Nothing was deleted; this is evidence FOR the CADENCE §4 policy [verified]
- `drops/` empty; no filing or G-11 naming owed this cycle [verified]
PENDING:
1. Configure project GitHub sync and click Sync now — nothing in `exchange/` reaches the three web lanes until then
2. Ratify or reject queue item 001 (validated COMPLETE as a contract; unstamped, so not executable)
3. Manual upload to the second Google Drive account — outstanding since 2026-07-28 against a 2026-08-02 archive
4. OneDrive.exe not running — the repo is not syncing to the cloud
5. Arm or defer the HERMES 2×/day trigger; recommendation filed with this run rather than self-armed
6. APOLLO and ARGUS owe current ledger entries — their 8-day-stale seeds carry resolved PENDING items
NEXT: Operator ratifies or rejects queue item 001, and rules on the Hermes cadence. Owner: operator.
METRICS: operator actions this session = 1 · files re-ingested = 2
=== END STATUS ===

---

=== STATUS_HERMES — 2026-08-15 — DORMANT (ruling 007) ===
NOW: This lane is DORMANT by operator ruling 007, 2026-08-15. It ran once, on 2026-08-04. Every duty it held is now discharged by something that reports itself, or is named as parked with no successor. This entry is written by HEPHAESTUS on the ruling's authority, not by HERMES: the lane does not self-verify (HELIOS tripwire, §5), and it cannot append to its own ledger while dormant.
LAST EVENT: 2026-08-15 — ruling 007 retired DIGEST.md and put this lane to sleep; filed as exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_RULING-007-LANE-CLOSE.md.
FACTS:
- FIVE DUTIES ABSORBED, each by a source that reports itself: budget -> printed on every publish · queue validation -> manifest counters and RATIFIED stamps · staleness -> F-P6 and the bus-health block · inbox -> ledger appends, since acted means the recipient's ledger cites the note · DIGEST.md -> retired to docs/history/DIGEST_RETIRED_2026-08-15.md with a tombstone at the old path [ratified]
- TWO DUTIES PARKED, NOT ABSORBED, and named rather than quietly dropped: filing exchange/drops/, which nothing now owns; and the queue-003 unacted-inbox list, whose only home was the DIGEST — rotate_reports.py HALTS rather than guess, and the first unacted note becomes a rotation candidate 2026-09-03. Both are operator calls. The first draft of the dormancy block claimed EVERY duty was absorbed; that was an overclaim and adversarial review caught it [verified]
- THIS LEDGER'S 11-DAY STALENESS CLOSES AS A BYPRODUCT, which is what ruling 'append' is for. The bus-health recency table had been reporting HERMES as the stalest ledger in the project — correctly, and it was this lane's own. It now carries a DORMANT label in that table (daily_routine.DORMANT_LANES), because the block that ABSORBED the staleness duty must not then report a parked lane's age as a finding while §5 says nothing waits on HERMES [verified]
- THE PRIMER IS KEPT, NOT DELETED, and now carries a dated DORMANT banner. exchange/reports/PRIMER_HERMES_2026-08-11_v4.md is the run-book any future coordinator inherits; its step 3 ordered a rebuild of DIGEST.md and now has no target. Only the byte figures were corrected (the naming trip-wire, pinned absolute at 64,000 B this session); the lane's own content is untouched, because a builder re-authoring the coordination lane's output is the HELIOS tripwire [verified]
- THE HELIOS TRIPWIRE SURVIVES THE DORMANCY, byte-identical and deliberately so: "HERMES never re-authors another lane's content and never instructs a lane without the operator's ratification stamp... a verifier who re-authors is not verifying." It binds whoever takes the role next, which is the whole reason the charter row was marked DORMANT rather than deleted [verified]
PENDING (operator):
1. The unacted-inbox list has no home. DEADLINE 2026-09-03. A one-line repoint of rotate_reports.DIGEST_PATH restores the exemption once you rule where it lives
2. exchange/drops/ has no owner
3. Revival is yours alone: the condition recorded in §5 is cross-lane coordination pain that a script cannot measure
NEXT: Nothing. Nothing waits on HERMES — that is the point of the ruling. Owner: none until revival.
METRICS: operator actions this session = 0 · files re-ingested = 0 · duties absorbed = 5 · duties parked = 2 · days stale at dormancy = 11
=== END STATUS ===
