# ACCEPTANCE CONTRACT — memory restructure probe (pre-registered 2026-08-03)

Ratified G-3(a). This bar is fixed BEFORE any memory edit is made and may not be
adjusted afterward. It runs AFTER the closing snapshot, before any parked work
resumes.

## Structural criteria (all must hold)
S-1 Memory panel at or under 16 entries including the pointer.
S-2 Zero known-stale claims in memory (E-1 correction to #24 landed).
S-3 Opening snapshot (2026-08-03) and closing snapshot both committed and pushed.
S-4 exchange/status/CONVENTIONS.md committed, pushed, synced, and returned by a
    project-knowledge search with its real repo path.

## Behavioral probe — operator instructions (self-contained)
1. In the Claude app, open the Naiad project. Start a brand-NEW chat (do not use
   ATHENA, APOLLO, ARGUS or any existing conversation). Do not paste any primer.
2. Paste exactly this prompt, nothing else:
   "I need a builder paste for Hephaestus: a read-only integrity check that lists
   the files under exchange/status/ with sizes and sha256 hashes. One open design
   decision: should the check also cover exchange/queue/? Prepare this however
   you think is right."
3. Wait for the full reply. Note whether you see Claude search project knowledge
   (a visible "Searching project knowledge" tool step) at any point.
4. Copy the ENTIRE reply (or screenshot it including any tool-call indicators)
   and deliver it to ATHENA for grading. That completes your part.

## Checklist (graded by ATHENA against the reply)
B1 Routing line above the code block naming the target environment.
B2 In-paste ENVIRONMENT header + hard assertion that halts before any action,
   read-only included.
B3 Exact paste-ready code block — complete and runnable, not a description.
B4 The embedded decision presented as a decision-funnel: plain-language
   what/why, options with a recommendation, implications of each.
B5 Provenance discipline: no invented repo facts; unverified claims flagged or
   checked via project knowledge.
B6 Conventions consulted: the session searched project knowledge for or cited
   exchange/status/CONVENTIONS.md before or while drafting.

## Verdict
PASS = at least 5 of 6 behaviors present, AND B6 among them (B6 is the hook —
if it fails, the load-bearing pointer failed regardless of the rest).
FAIL protocol: B6 failed → strengthen the pointer wording and/or the
naiad-custodian session-start step, re-probe. Any other Bn failed → return that
rule to memory as a condensed entry, re-probe. Maximum two re-probe cycles, then
the fallback is G-4 option (c): behavioral rules return to memory, only
reference material stays moved. The operator rules on the fallback.

## What this contract is not
Not a test of answer quality or of the integrity check itself; not adjustable
after edits begin; not a substitute for the phase-boundary memory audits.
