# SESSION SUMMARY — ATHENA · Memory workstream scoping · 2026-08-03

Zero-context explainer. Provenance tags: [verified] = computed/read this session ·
[operator] = operator-reported · [ratified] = operator decision on record ·
[handoff] = builder-reported · [open] = undetermined.

## 1 · What this session did

The operator ratified the memory snapshot (T-4) as the first task, with everything
else parked until done well. This session: (a) read the live project-memory panel
directly — 30 entries, matching the outgoing handoff's inventory exactly [verified];
(b) critically reviewed an uploaded third-party "memory tuning guide" and verified
its load-bearing claims against Anthropic's official documentation; (c) ran a
scoping interview; (d) produced this report, the verbatim snapshot
(docs/memory/claude_project_memory_2026-08-03.md), and the pre-registered
acceptance contract (exchange/reports/ACCEPTANCE_MEMORY-RESTRUCTURE_2026-08-03.md).

## 2 · Findings

**F-1 · The panel, read directly [verified]:** 30 entries (cap 30), up to 100,000
characters per entry. The binding constraint is entry COUNT and attention (injected
length degrades adherence), never character capacity.

**F-2 · Our memory entry #24 is contradicted by current official documentation —
Class A instance, ATHENA's to own.** Entry #24 asserts project memory "is NOT
included in that export." Anthropic's current support article states all memory
data IS included in data exports, and documents a dedicated export path (ask Claude
in chat to write out its memories verbatim; save as backup) plus an experimental
import flow that can restore from such text (extraction-based, lossy). Resolution
is empirical: inspect the first T-6 data export for memory content. Interim
posture: the repo snapshot ritual stands regardless — it is the only copy under
OUR verification standard, and a lossy import path makes verbatim capture MORE
valuable. Correction to entry #24 is edit E-1 in the plan below. [verified against
support.claude.com articles 11817273 and 12123587, read 2026-08-03]

**F-3 · Memory does not reach Cowork [verified, same source].** HERMES and
DIONYSUS have never seen any of the 30 entries. The memory surface covers the
three web lanes only (APOLLO, ARGUS, ATHENA). Any rule that must bind a Cowork
lane cannot live in memory — it must live in the repo. This independently
strengthens the two-tier design.

**F-4 · A global "Reset memory" permanently deletes project memories too, and
cannot be undone [verified, same source].** One settings action can erase all 30
entries. The snapshot is the recovery path.

**F-5 · Account is on the LEGACY memory experience** (Settings > Capabilities >
Memory, "Legacy" badge; Max plan) [operator, screenshot 2026-08-03]. Anthropic is
migrating free/Pro/Max users to a new experience (Settings > Memory, real-time
entries). All hands-on instructions in this workstream are written for the legacy
screens; when the migration lands, the click-paths change and this report's
successor must update them.

**F-6 · The prior handoff's research citations ("build commands", "shorter files
produce better adherence", "topic files on demand") trace to CLAUDE CODE memory
documentation, not claude.ai project-memory documentation.** The principles
transfer — both systems inject text at session start and the official Claude Code
docs state memory is treated "as context, not enforced configuration" — but the
provenance label was wrong. Corrected here. [verified]

**F-7 · The uploaded guide ("Proven AI Specialists", anonymous, browser-duplicate
filename):** mechanics mostly confirmed against official sources; one stale claim
(24-hour synthesis — legacy only); misses the import/export flow, the Cowork gap,
and the 30-entry mechanics entirely. Adopted principles (independently supported):
instruction-vs-state separation, negative memory, staleness-as-first-class,
fresh-session testing as acceptance gate. Status: principles digest, not a
mechanics reference.

## 3 · Rulings taken this session [ratified, operator 2026-08-03]

Q-0 = B (legacy experience). G-1 = c (tiered: memory carries what keeps every
lane oriented toward the project objective — identity, operator style,
behavior-critical rules, pointers; the repo carries state, reference, procedure).
G-2 = a (one workstream: snapshot → restructure → portable operator layer).
G-3 = a (fresh-session probe as acceptance test; contract pre-registered).
G-4 = a (pointer entry + custodian-skill session-start read + Hermes staleness
stamp), with operator emphasis: every behavior moved out of memory is REGISTERED
and its compliance ENFORCED. G-5 = a (reviewer-executed edits, per-edit approval,
snapshot-bracketed; sub-defaults: soft budget 6/lane + 6 shared; audit at every
phase boundary; snapshot regenerated at every audit).

Operator constraints on the conventions file [ratified]: moved entries keep their
EXCEPTIONS and REMINDERS intact (no stripping to bare rules); the file carries a
step-by-step plain-language maintenance guide; a MOVED-FROM-MEMORY register lists
every relocated behavior, its origin entry, and its probe coverage.

## 4 · PROPOSED edit plan — awaiting per-edit approval, nothing executed

Sequence: this snapshot committed → CONVENTIONS.md drafted, committed, pushed,
synced, and verified readable via project-knowledge search → only then edits, one
approval each → closing snapshot → acceptance probe.

| # | Entry | Proposed action |
|---|---|---|
| E-1 first | #24 backup architecture | KEEP + CORRECT the export claim per F-2 (condense) |
| 1 | SS Pine backlog | MOVE → CONVENTIONS (Apollo backlog section) |
| 2 | Reporting methodology | KEEP |
| 3 | Guiding attitude | KEEP |
| 4 | TC-4 rulings | MERGE → into #6 |
| 5 | Fractal lens | KEEP (condense) |
| 6 | Study findings | KEEP |
| 7 | Exact paste-ready rule | MOVE (probe behavior B3 covers it) |
| 8 | Context-gap audit | MOVE (double-covered by naiad-custodian skill) |
| 9 | Claude-optimization track | MOVE (history) |
| 10 | Two builder environments | MERGE → into #11 |
| 11 | Paste-routing/env-assertion/disposition | KEEP (condensed safety core) |
| 12 | Estate location | KEEP |
| 13 | Orchestration + STATUS | KEEP (condense) |
| 14 | Workflow-design rule | MOVE |
| 15 | ARGUS lane purpose | MOVE (lane charter) |
| 16 | Workflow preference | MERGE → into #14, moves with it |
| 17 | Renames + rescope + SS definition | SPLIT: lane names → #21; SS working definition → #6 |
| 18 | Decision-gate rules | MERGE → into #27 |
| 19 | SS interview rulings | MOVE (Apollo; ledger-backed) |
| 20 | Prime directive | KEEP — never move |
| 21 | Olympian architecture | KEEP (condense; absorbs 17a) |
| 22 | W1/W2 architecture | KEEP (condense) |
| 23 | Reviewer error taxonomy | KEEP |
| 25 | Infrastructure inventory | MOVE |
| 26 | Surface-access map | KEEP |
| 27 | Decision-funnel format | KEEP (absorbs #18) |
| 28 | Builder handback rules | MOVE (probe-covered; pointer names it) |
| 29 | Manual-task rule | MOVE |
| 30 | Rulings 2026-08-03 | HOLD — APOLLO's active state; merge into #6 at next phase boundary, not mid-flight |
| NEW | Pointer entry | ADD ("at session start, read exchange/status/CONVENTIONS.md — authoritative for paste construction, reporting, file handling, lane etiquette") |

Projected end state: 16 entries (14 keeps + #30 held + pointer), 14 slots free.
Target ≤ 16 met.

## 5 · Open items and honest risks

R-1 · Transcription fidelity: the snapshot was transcribed verbatim from the panel
read; a 30-entry manual capture carries nonzero copy risk. Mitigation: the next
memory audit re-reads the panel and diffs against this file; the closing snapshot
provides a second independent capture. [open]
R-2 · The export dispute (F-2) resolves only when the first T-6 export is
inspected. [open]
R-3 · Experience migration (F-5) will invalidate the legacy click-paths in these
documents at an unknown date. [open]

## 6 · Next steps

1. Operator confirms this paste's push succeeded, clicks Sync now (also brings the
   stale RETENTION.md picture current in the box — flagged 2026-08-03).
2. ATHENA delivers the CONVENTIONS.md draft paste.
3. Sync + search-verify CONVENTIONS.md readable → per-edit memory approvals begin.
4. Closing snapshot → acceptance probe per the contract → portable operator layer
   (T-5 Part 1 draft) closes the workstream.

=== STATUS_ATHENA — 2026-08-03 ===
NOW: Memory workstream scoped and ratified (Q-0, G-1..G-5). Verbatim 30-entry
snapshot, this report, and the pre-registered acceptance contract committed.
Edits not yet begun — gated on snapshot confirmation and CONVENTIONS.md landing.
LAST EVENT: 2026-08-03 — snapshot paste executed by HEPHAESTUS.
FACTS:
- Panel read directly: 30 entries, matching handoff inventory [verified]
- Entry #24's "memory not in export" claim contradicted by current official docs; empirical resolution via first T-6 export [verified]
- Memory does not reach Cowork; HERMES/DIONYSUS bound only by repo files [verified]
- Global Reset memory deletes project memories irreversibly [verified]
- Account on LEGACY memory experience, Max plan [operator]
- Edit plan (16-entry end state) PROPOSED, awaiting per-edit approval [open]
PENDING:
1. Confirm push + Sync now
2. Per-edit approvals once CONVENTIONS.md is live
NEXT: ATHENA drafts CONVENTIONS.md paste. Owner: ATHENA.
METRICS: operator actions this session = 3 · files re-ingested = 2
=== END STATUS ===
