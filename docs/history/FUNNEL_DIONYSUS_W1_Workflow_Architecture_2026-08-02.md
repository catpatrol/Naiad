# FUNNEL_DIONYSUS_W1 — Workflow Architecture Decision Funnel
**Filed:** 2026-08-02 · **Author:** DIONYSUS (Cowork, repo read) · **Basis:** Ludwig's written replies to CHALLENGE_DIONYSUS_01 (2026-08-02) + capability verification against Anthropic documentation this session
**Standing note (operator instruction):** this funnel and its rulings are part of the project's workflow design record. Web lanes should fold the outcome into project memory; this surface cannot write project memory directly (read-only mount), so the filed doc is the durable copy.

---

## Part 1 — What Claude can actually do (verified, plain language)

Every claim tagged. [verified-doc] = confirmed in Anthropic's help center today. [observed] = demonstrated first-hand this session. [reasoned] = inference, with the cheap experiment that would settle it.

**F1 — Web chats (APOLLO, ARGUS, ATHENA).** Share the project knowledge box and project memory. Cannot read each other's conversations, cannot touch files on your computer, cannot run on a schedule. Only you put files in the box — with one big exception, F2. [observed/known]

**F2 — THE KEY FINDING: the project box can sync a GitHub repository.** [verified-doc] A Claude Project can link a GitHub repo and branch, select files/folders, and pull their contents into project knowledge. Refreshing is one click ("Sync now") by you. Plain meaning: **anything committed AND pushed to GitHub becomes readable by every web chat in the project after one click** — no more per-file uploads. Limits: file contents only (no commit history); large sets handled by the paid-plan RAG mode; the sync click is manual and yours.

**F3 — Cowork tasks (me; a future Hermes session).** Read/write the local repo folder, run code in a sandbox, use skills. [observed — I filed two docs and hashed the manifest without a single ferry action]

**F4 — Cowork scheduled tasks exist.** [verified-doc] A prompt can be saved and run automatically on a cadence (all paid plans), with the same skills/connectors as normal tasks. **Critical caveat:** scheduled runs execute *remotely* — they run even when your computer is asleep. [verified-doc] That strongly implies a scheduled run does NOT see the local folder on your machine; its natural view is GitHub. [reasoned] **Cheap experiment before we commit:** schedule a one-off run that tries to read one repo file and reports back. Five minutes, settles it.

**F5 — Hephaestus (local Claude Code) remains the only actor that touches the data estate** (`AppData\Local\naiad\data_cache`). Heavy compute stays local. Cloud Claude Code sessions evaporate unless pushed (existing rule R-A').

**F6 — No lane can message another directly on any surface.** The bus is: files + the box + you. Your approval gate is not a workaround for a product limit — it is the design, and it stays.

## Part 2 — The shape that falls out (my suggestion: the waterwheel)

One loop, turning on its own weight, you standing beside it rather than carrying the water:

1. `exchange/` in the repo: `status/` (one ledger per lane) · `queue/` (builder work orders) · `reports/` · `drops/` (raw inbox).
2. Web lanes produce artifacts → you **drop** them into `exchange/drops/` (a drag, not a formatting job). Hermes files, names (G-11), and indexes them. Your ferry action shrinks to: drop.
3. Hephaestus pushes `exchange/` + ledgers under a standing rule → you click **Sync now** → every web lane sees current state of everything. Your ferry action shrinks to: one click.
4. Hermes routine (scheduled and/or on-demand — Q-4) verifies, staleness-stamps, consolidates a DIGEST, maintains the queue. Never re-authors, never instructs a lane without your stamp.
5. You keep: every verdict, every merge, every queue ratification, and the understanding — the DIGEST's job is that you can read one page and know how each lane's work fits the whole (your A3).

Recurring operator cost, honestly stated: drops + one sync click per cycle + verdicts. That is the floor today's product allows. [reasoned]

---

## Part 3 — The funnel (multiple choice; one word per question answers it)

**Q-1 · Visibility bus — how does everyone see everyone's work?**
*Context:* today visibility = you uploading files one by one. F2 makes a repo-to-box pipe possible.
- **A** — GitHub-sync bus: push exchange/ + ledgers; you click Sync now ~1×/day.
- **B** — Digest ferry: Hermes builds one DIGEST.md; you upload that single file each cycle.
- **C** — Both: sync as the pipe (raw files, anti-lossy), DIGEST at its head (the one-page "how it all fits").
**Recommendation: C.** *Implications:* A/C require Q-2. B keeps you as the pipe, minimized but not removed.

**Q-2 · Standing push rule — the gate that makes Q-1 real.**
*Context:* current default is commit-no-push, per-authorization. A sync bus needs GitHub current.
- **A** — Authorize auto-push for `exchange/**` + lane ledgers ONLY; study code/results keep today's per-authorization rule.
- **B** — Keep all pushes manual; you say "push exchange" when you want the box refreshable.
**Recommendation: A.** *Implications:* narrow scope — coordination state auto-publishes, evidence never does without you.

**Q-3 · Ledgers — your "everyone gets their own ledger" idea.**
- **A** — Adopt it: `exchange/status/LEDGER_<GOD>.md`, append-only, fixed template (naiad-eod format), written at each material session end; Hermes consolidates + stamps staleness. Central LEDGER.md stays the *evidence* ledger, untouched.
- **B** — One shared coordination ledger, lane-tagged entries.
- **C** — Status quo (central ledger + ad-hoc status docs).
**Recommendation: A.** *Implications:* parallel writing with no collisions; clean provenance per lane; your idea, and it is the right one.

**Q-4 · Hermes' charter — what he IS. (Also resolves CRONOS/W-3.)**
*Context:* F4 — scheduled runs are remote; local file work needs an opened session. Your sheets drew Hermes as two ports and CRONOS as the timestamper above.
- **A** — Hybrid Hermes: (i) scheduled remote run 1–2×/day reads GitHub → DIGEST + staleness report; (ii) on-demand local session (you open it, say "routine") → hash/manifest verification, files the drops, grooms the queue. **CRONOS = the schedule itself + the timestamps** — the cron *is* Cronos; no seventh agent, no primer.
- **B** — On-demand only (no schedule; you trigger every cycle).
- **C** — Scheduled only (accept the remote-view limit; local integrity work falls to Hephaestus).
**Recommendation: A**, starting at 2×/day, not your floated 3–6 — each run costs usage and produces noise; cadence can rise on evidence. *Precondition:* the F4 experiment (one-off scheduled run) before finalizing the split. *Codified either way:* Hermes never re-authors content; never instructs a lane without your stamp.

**Q-5 · Builder queue — your question "can Hermes keep a queue for the builder?" Answer: yes. Adopt?**
- **A** — `exchange/queue/`: numbered work orders; any lane may draft; **you ratify each with one word**; Hermes validates completeness (fixtures, invariants, deliverables) and sequences; Hephaestus sessions open with "work the queue"; results + manifest land back in the repo.
- **B** — Same, but only APOLLO and ATHENA may draft entries.
- **C** — Keep the current per-contract paste flow.
**Recommendation: A.** *Implications:* your no-cross-instruction rule is preserved by the ratification stamp — the queue is a request lane, not a command lane.

**Q-6 · Apollo's hands — chat, executive brother, or migration?**
- **A** — APOLLO stays a web chat (keeps his accumulated context and project memory); his ratified action lists execute through the Q-5 queue via Hermes. No new agent.
- **B** — Spawn HELIOS (Cowork executive brother) — but only when a written tripwire fires: Hermes misses two consecutive cycles, OR Hermes ends up both executing study runs and verifying them (conflict of duties).
- **C** — Migrate APOLLO to Cowork now (gains hands; pays the resurrection tax every session; loses chat continuity).
**Recommendation: A now, with B's tripwire written into the record.** Fewest moving pieces first; the ferry census (Q-8) tells us if escalation is needed.

**Q-7 · Challenge handling — revised after your veto of blocking gates.**
- **A** — Non-blocking answer debt: every CHALLENGE gets an ID and must receive a *written* answer (one line suffices) by the next phase boundary; **no work ever waits on it**.
- **B** — Challenges answered only when you schedule a review.
**Recommendation: A.** *Implications:* critique stays lethal without ever becoming a brake — your requirement, met.

**Q-8 · Tracking the resurrection tax (your "how do we track this?").**
- **A** — Two self-reported numbers in every session-end STATUS: *operator actions this session* (drops, pastes, clicks) and *files re-ingested to seed*. Hermes tallies them in the DIGEST weekly. This is also the E1 ferry census — one mechanism, both metrics.
- **B** — Don't track; revisit if the pain returns.
**Recommendation: A** — two integers per session, near-zero cost, and every future architecture argument becomes evidence instead of taste.

**Answer format:** eight words — e.g. `1C 2A 3A 4A 5A 6A 7A 8A` — or `defaults` (= all recommendations).

---

## Rulings received (append-only, fold-forward)
- **2026-08-02 · Q-5 RULED.** Operator, verbatim: *"Argus can also draft for Hephaestus."* Interpretation on record (operator may veto): builder queue adopted with drafting rights = **APOLLO, ATHENA, ARGUS**; DIONYSUS and HERMES do not draft work orders (HERMES validates and sequences; DIONYSUS critiques via CHALLENGE memos, which are not work orders). Operator ratification stamp per queue item unchanged and mandatory.
- **2026-08-02 · FUNNEL CLOSED.** Operator: *"all other questions your defaults."* Final rulings: **Q-1 C** (sync bus + digest) · **Q-2 A** (auto-push `exchange/**` + lane ledgers only) · **Q-3 A** (per-lane append-only ledgers; central LEDGER.md stays evidence) · **Q-4 A** (hybrid Hermes, 2×/day scheduled start; **CRONOS = the schedule + timestamps — gate W-3 resolved, no seventh agent**; F4 experiment to run before the split is finalized) · **Q-5** as ruled above (APOLLO/ATHENA/ARGUS draft) · **Q-6 A** (Apollo stays a chat; HELIOS tripwire on record: Hermes misses two consecutive cycles OR verifies his own executions) · **Q-7 A** (non-blocking written answer debt, due by next phase boundary) · **Q-8 A** (two integers per session-end STATUS; Hermes tallies weekly).
- Standing rules ratified by these rulings, to be folded into the register: (i) push scope G-rule — coordination state auto-publishes, evidence never without operator; (ii) HERMES never re-authors content, never instructs a lane without operator stamp; (iii) CHALLENGE answer debt non-blocking; (iv) STATUS metrics (operator actions · files re-ingested).

## Deferred by operator instruction
E2 (critic-lethality clock) — "ask later." Parked, not forgotten.

— DIONYSUS, 2026-08-02. Sources: Anthropic Help Center — "Using the GitHub integration" (project knowledge sync); "Schedule recurring tasks in Claude Cowork" (remote scheduled execution).
