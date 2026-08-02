# HANDOFF — DIONYSUS → ATHENA · Workflow Redesign Inputs
**Filed:** 2026-08-02 · **From:** DIONYSUS (Cowork, repo read) · **For:** ATHENA's exchange/ scoping and anti-ferrying design
**Route:** operator ferries this file (or its content) to ATHENA; supersedes nothing; append-only.
**Provenance:** operator's written replies to CHALLENGE_DIONYSUS_01 (2026-08-02) + capability verification against Anthropic help-center documentation, same date. Companion doc with full decision funnel: `FUNNEL_DIONYSUS_W1_Workflow_Architecture_2026-08-02.md`.

## 1 · Verified capabilities your design can build on

- **Project-box GitHub sync exists.** [verified-doc] A Claude Project can link the GitHub repo/branch, select folders, and pull file contents into project knowledge; refresh is one operator click ("Sync now"). Consequence: **pushed repo files are readable by every web lane.** This is the visibility bus the redesign has been missing.
- **Cowork scheduled tasks exist** (all paid plans) and run *remotely* — even with the operator's machine asleep. [verified-doc] Consequence: a scheduled Hermes routine likely sees GitHub, not the local folder. **Open experiment (cheap, do before finalizing):** one-off scheduled run that attempts to read a local repo file and reports. Until then, treat "scheduled = remote view" as the working assumption.
- **Cowork on-demand sessions have full local repo read/write + sandbox execution.** [observed first-hand this session]
- Web chats: shared box + project memory, no file hands, no schedule, no cross-chat reading. Hephaestus remains sole owner of the data estate. [known]

## 2 · Operator rulings and requirements already on the record (from his replies — treat as constraints, not suggestions)

1. **He will not do constant daily ferrying.** He remains the gate for every relevant design decision and wants to understand everything — plain-language context before any decision funnel.
2. **No chat or task may instruct another without his approval.** Any queue/action-list mechanism must carry his ratification stamp per item.
3. **Consolidation is not a goal in itself** — the goal is that every lane sees what the others are doing and how their work fits the whole. Digest = index with pointers to raw artifacts, never a re-authored substitute (anti-lossy).
4. **Challenges must never block work.** Open DIONYSUS queries must not stall ATHENA or APOLLO; the adopted form is a non-blocking written answer debt (funnel Q-7).
5. **Bundled back-and-forth packages with builders proved too time-consuming.** Target: infrastructure that pursues and completes tasks, stopping to ask only when necessary; minimize "placing files here or there."
6. **Per-lane ledgers are his own proposal** (every god, plus builder sessions, appends to its own ledger others can read) — endorsed in the funnel; central LEDGER.md stays the evidence ledger.
7. **CRONOS was conceived as the time/cadence function ("timestamper")** and he suspects it needs no separate agent — folding it into Hermes' schedule + staleness stamps is the funnel's recommendation (resolves W-3 pending his word).

## 3 · Design components for your exchange/ scoping (pending funnel rulings, marked)

- `exchange/status/LEDGER_<GOD>.md` — append-only per-lane ledgers, fixed template (naiad-eod format is the natural donor). [pending Q-3]
- `exchange/queue/` — numbered builder work orders; **RULED 2026-08-02:** drafting rights = APOLLO, ATHENA, ARGUS (operator: "Argus can also draft for Hephaestus") → operator ratifies each item (one word) → Hermes validates completeness (fixtures, invariants, deliverables, verdict criteria) and sequences → Hephaestus "works the queue" → results + manifest return. DIONYSUS/HERMES do not draft work orders.
- `exchange/drops/` — raw inbox: operator drags web-lane artifacts in unformatted; Hermes names (G-11), files, indexes. Reduces his ferry action to a drop.
- `exchange/reports/` + `DIGEST.md` — Hermes-consolidated one-page index at the head of the sync bus. [pending Q-1]
- **Standing push rule:** auto-push scope limited to `exchange/**` + lane ledgers; study artifacts keep per-authorization push. [pending Q-2 — this is the rule that makes the sync bus live]
- **Hermes charter:** hybrid — scheduled remote run 1–2×/day (digest, staleness) + on-demand local session (hash/manifest verification, drops filing, queue grooming). Never re-authors; never instructs without operator stamp. [pending Q-4]
- **Metrics baked in:** every session-end STATUS carries two integers — operator actions this session; files re-ingested to seed. Hermes tallies weekly. [pending Q-8]

## 3b · RULINGS COMPLETE — 2026-08-02, same day (fold-forward; supersedes the bracketed "pending" markers in §3)
Operator closed the funnel: **Q-1 C · Q-2 A · Q-3 A · Q-4 A · Q-5 modified (APOLLO/ATHENA/ARGUS draft for Hephaestus) · Q-6 A · Q-7 A · Q-8 A.** Every §3 component is now ruled and actionable. CRONOS is resolved (gate W-3): the time/cadence function = Hermes' schedule + staleness stamps; no seventh agent. HELIOS tripwire on record (spawn only if Hermes misses two consecutive cycles or ends up verifying his own executions). Your exchange/ scoping can proceed on all of it; the one open empirical item is the F4 experiment (whether a scheduled run sees the local folder), being run by DIONYSUS — its outcome tunes the Hermes scheduled/on-demand split but blocks nothing in the directory design.

## 4 · What this handoff is not
Not a ruling — every bracketed item awaits the operator's funnel answers. Not a claim that scheduled-task local access is impossible — that experiment is open. Not a transfer of your scoping mandate — these are inputs; the exchange/ design remains yours to ratify.

— DIONYSUS, 2026-08-02
