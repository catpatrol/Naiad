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
