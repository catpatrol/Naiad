# LEDGER_DIONYSUS — append-only lane ledger

**Lane:** DIONYSUS — critique, architecture challenge, decision funnels. Files CHALLENGE memos; does
not draft work orders (ruling Q-5).
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

=== STATUS_DIONYSUS — 2026-08-02 ===
NOW: Ledger founded. This lane had no prior status document, so this is a founding line rather than a carried-over state: no history is claimed before this date. DIONYSUS' work to date lives in the two filed documents named below, which this ledger now indexes rather than restates.
LAST EVENT: 2026-08-02 — ledger founded by HEPHAESTUS during the exchange v1 build (ruling Q-3 A).
FACTS:
- No prior LEDGER_DIONYSUS existed; nothing before 2026-08-02 is recorded here [verified]
- `CHALLENGE_DIONYSUS_01_Architecture_2026-08-02.md` (8,822 B) is on file at repo root [verified]
- `FUNNEL_DIONYSUS_W1_Workflow_Architecture_2026-08-02.md` (11,271 B) is on file at repo root; it is the decision record the exchange was built from [verified]
- `HANDOFF_DIONYSUS_to_ATHENA_2026-08-02_Workflow_Redesign_Inputs.md` (5,814 B) is on file at repo root [verified]
- Charter constraint on record: DIONYSUS critiques via CHALLENGE memos and does not draft queue work orders [ratified]
- The F4 experiment (whether a scheduled Cowork run can read the local folder) is DIONYSUS' open item; its outcome tunes the Hermes split [open]
PENDING:
1. Run the F4 experiment — one-off scheduled run that attempts to read a repo file and reports back
2. E2 (critic-lethality clock) — deferred by operator instruction, parked not forgotten
NEXT: Run the F4 experiment. Owner: DIONYSUS.
METRICS: operator actions this session = 0 · files re-ingested = 0
=== END STATUS ===
