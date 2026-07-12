# BUILD PROMPT — Engine 1.0.3 "Input Parity" (conformance fix + journal regeneration)
### Feed this file to Claude Code. It is a self-contained contract. · 2026-07-12
### Builder: Claude Code · Reviewer: Claude (Project, Fable-mode) · Operator: Ludwig
### Root cause of record: engine hardcodes zone_memory=5 (cells.py:66); deployed
### Pine runs zoneMemory=3 (input default, operator-verified on both charts).
### The parity target is the deployed chart. The engine conforms to it — never
### the reverse.

---

## 0. Mission

Restore the engine's input constants to the deployed Pine's input defaults,
prove every other constant already conforms, regenerate the parity journal
into a clean state, and pin the whole class of drift with permanent fixtures —
so no config constant can ever again silently diverge from the instrument the
operator trades.

Definition of done: the input-parity audit table is delivered and clean (or
ruled); the fix lands; the regenerated journal diffs ZERO against the
validated shadow-at-3; all six case-window tables are regenerated; the suite
is green at its new, explained count; ledger entries committed; packet
ferried.

## 1. Read first / context the builder must honor

1. `research_outputs/ssv11_3/Engine_1.0.3_precontract_zoneMemory_fork.md` —
   the findings artifact this contract executes. The shadow-at-3 it validated
   bit-for-bit is the reference implementation for I3.
2. The regenerate-never-merge rule (LEDGER, 2026-07-10 anchors): config/key
   semantics changes regenerate journals into clean state; the idempotent
   writer strands rows under retired semantics if merged.
3. The mem=5 journal is NOT waste: it is pre-paid seed data for a future v12
   named-variant candidate ("zoneMemory-5"). It is archived, never deleted.
4. The knife-edge criterion amendment (LEDGER, bf92eaa) stands as ratified
   law; the Jun-23 instance reclassifies under it (config divergence, not
   float fork) via a dated correction — history is corrected in place with a
   note, never rewritten (house style per the CHANGELOG precedent).

## 2. Frozen invariants

- **I1 — Conformance.** After the fix, every `v11_faithful` input constant
  equals the deployed Pine input default. `naiad_v0` likewise, except
  divergences explicitly ratified in the Phase-0 charter (logic policies such
  as V-births-provisional are charter items, not input constants; no input
  constant divergence is currently ratified).
- **I2 — Regenerate, never merge.** The old parity journal moves intact to
  `research_outputs/parity/journal_mem5_archive/` with a README naming it as
  the zoneMemory-5 variant seed. The new journal is generated fresh, new
  run_id, full dev window.
- **I3 — Shadow equivalence.** The regenerated journal must diff ZERO
  (events, fields, stops) against the validated shadow-at-3 trace. Any
  nonzero diff is a failed phase — stop and report.
- **I4 — Drift can never recur silently.** A new fixture family pins this:
  (a) an input-parity fixture asserting every engine constant against a
  committed Pine-defaults manifest extracted from the .pine source;
  (b) behavioral pins at the divergence sites — May 23 16:20 fires NO PRIME,
  May 27 12:45 fires NO grade-C, Jun 23 17:00/17:45/20:45 fire NO CONFIRMs,
  at zone_memory=3.
- **I5 — Blast radius.** Config constants, fixtures, docs, journals,
  ledger. ZERO signal-logic changes — the logic was proven line-identical to
  the Pine; only the constant differs.
- **I6 — Version discipline.** ENGINE_VERSION 1.0.2 → 1.0.3, changelog
  entry, dedicated branch off v12-v1-census head, operator owns the merge.

## 3. Phase A — the input-parity audit (gate; do this FIRST)

Produce a table: every input constant in the engine's cell/config layer
(all mandates, both configs) | the Pine input default (cite the .pine line) |
match/diverge | if diverge: charter citation or "UNRATIFIED DRIFT".

**Stop rule:** if any unratified divergence exists BEYOND zone_memory,
STOP after the table — no fix, no regeneration — and report for reviewer
ruling. If zone_memory is the sole drift, proceed directly through Phase B.

## 4. Phase B — deliverables

- **D1 — The fix.** zone_memory → 3 (all mandates, both configs), plus any
  Phase-A drift the reviewer ruled on. Pine-defaults manifest committed as
  the fixture's source of truth.
- **D2 — Fixtures.** The I4 family added. Separately: LIST every existing
  fixture whose pinned anchors change because the mem=5 journal anchors are
  retired (e.g., the journal-SHA/row-count pins from Phase 1). Each gets:
  old value → new value → one-line justification, in the packet manifest.
  No other existing fixture may be modified.
- **D3 — Regeneration.** Full dev-window parity journal regenerated;
  new journal SHA256, row count, and event-distribution census printed
  (the reviewer recomputes these). I3 diff executed and shown. The old
  naiad_v0 dryrun journal is archived alongside the mem=5 parity journal
  (non-load-bearing; the collector stamps fresh journals at its epoch).
- **D4 — Case windows.** All six tables in case_windows.md regenerated from
  the new journal; the "default inputs" sign-off note corrected to state the
  verified inputs explicitly (zoneMemory=3 et al.).
- **D5 — Ledger, byte-for-byte, one commit:**

```
## 2026-07-12 — Engine 1.0.3: input-parity conformance (root cause of the 3C break)
- Root cause: engine hardcoded zone_memory=5; deployed Pine runs zoneMemory=3 (operator-verified on deployed and v11.3 charts). Bands, EMAs, logic proven identical; one constant forked hadPrimeEp/activeZone state.
- Ruling: parity target is the deployed chart; engine conforms. zone_memory -> 3 all mandates/configs; input-parity fixture family added (drift can no longer recur silently).
- Journal: mem=5 parity journal ARCHIVED as v12 named-variant seed ("zoneMemory-5" candidate: 18 extra entries, 2 regrades, 4,360 stop-divergent bars over 9 months). Parity journal REGENERATED at mem=3; diff vs validated shadow = ZERO.
- Correction to 2026-07-11 criterion entry: the Jun-23 instance was config divergence, not a float fork; the criterion stands as law; measured float-fork count post-conformance: pending re-verify, expected 0.
- Reviewer record: theories 2-7 falsified by measurement; theory 1 ("engine is the deviant") confirmed by the operator's Inputs reading.
```

- **D6 — Packet.** Audit table, fix diff, fixture diffs + changed-anchor
  list, old/new journal SHAs + census, I3 diff output, regenerated
  case_windows.md, ledger diff, one-page manifest.

## 5. Verdict criteria (pre-registered)

Pass iff: Phase-A table delivered, clean or ruled; I3 diff exactly zero;
suite green at the new count with every count change explained (added I4
fixtures + listed anchor updates, nothing else); new census internally
consistent under reviewer recomputation; six windows regenerated; D5
committed byte-exact; packet ferried. Fail-pending-report on: any Phase-A
stop, any nonzero I3 diff, any unlisted fixture modification.

## 6. What this phase is not

No Pine changes (both charts are correct as deployed). No signal-logic
edits. No zoneMemory=5 anywhere in live configs — that value is now a
FUTURE v12 named-variant question with its seed data archived. No collector
work, no v12 analysis, no window re-verification (that is the reviewer's
next phase, on the regenerated tables).

---

## 7. Operator runbook (for Ludwig)

**Step 1 —** Move this file into the Naiad folder. If the hygiene commit
from the previous session is still staged and unreviewed, finish it first
(review the diff → commit → push), so this phase starts from a clean tree.

**Step 2 —** PowerShell in the folder → `claude` (or the full-path
launcher) → paste:
`Read Engine_1_0_3_Input_Parity_Build_Prompt.md in the project root and
execute it as this session's contract. Operator confirmation on record:
deployed chart and v11.3 layout both read Zone memory = 3.`

**Step 3 —** *What you should see, in order:* the Phase-A audit table
(pause here only if it flags drift beyond zone_memory — ferry the table and
stop); the one-line fix; the fixture work with its changed-anchor list; a
long regeneration run; the I3 diff line reading zero; the suite summary
(green, new count stated); the ledger commit; a packet path.

**Step 4 —** Ferry the packet here with the audit table, the I3 diff line,
the new journal SHA + census, and the suite summary pasted as text. The
reviewer recomputes, rules, and hands you the (short) re-verification list —
expected: two regraded-event glyph checks and a skim, because everything
else was already verified against the shadow through your own hovers.
