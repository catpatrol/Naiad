# Naiad Orchestration Protocol & Open Questions Register
### Coordinating the SYSTEM, BRIEF and ENGINE chats · v1 · 2026-07-27

---

## Part 1 — Why this exists

Three chats run in parallel against one repo, one ledger, one operator:

- **SYSTEM** — tooling, integrity, housekeeping, skills, contracts
- **BRIEF** — the daily market report and its evolution toward serving engine v2
- **ENGINE** — the v12 study: CENSUS-1c, Tier-C phases, the trading logic itself

They already share more than it appears: the same **project memory**, the same **context box**, the same **repo and ledger**. What they don't share is conversation context — so the failure mode is not collision, it's **stale state**. On 2026-07-27 the SYSTEM chat discovered two BRIEF commits (`76cc314`, `60e00c9`) by accident during an unrelated audit.

**Measured cost of the current pattern** (SYSTEM session, 2026-07-26/27): 25 paste events, 8 misrouted (32% waste), ~150 discrete operator actions, of which **9 were actual decisions — 6%**. The protocol below targets the other 94%.

---

## Part 2 — Orchestration decisions

**D-O1: One branch, not three.** Per-workstream branches would conflict on `LEDGER.md` at every merge, and the operator is a serial actor who can only run one builder task at a time. Concurrent writes are not the risk; stale state is. **Ruling: stay on `v12-v1-census`; solve freshness instead.**

**D-O2: State freshness via the manifest.** Extend `scripts/reviewer_manifest.py` to emit, alongside its existing keys: the ledger's head entry title and byte size, the last commit per workstream (classified by message prefix — `ops:` / `docs:` / study phase names), and the count of unresolved entries in this register. **Every chat opens by reading a fresh `MANIFEST.json`.** No chat asserts repo state from memory.

**D-O3: Commit-message prefixes are the workstream signal.** `ops:` = SYSTEM · `brief:` = BRIEF · phase names (`census`, `tc`, `s`) = ENGINE · `docs:` = any. Cheap, already half-observed, makes `git log` a coordination view.

**D-O4: One writer at a time.** Before any chat issues a paste that writes to the repo, it confirms from a fresh manifest that HEAD matches what it expects. If HEAD has moved, it re-reads before proceeding. This is a discipline, not a lock.

**D-O5: This register is the decision queue.** Any chat that needs an operator ruling appends here rather than blocking mid-conversation. The operator answers in batches, at a time of their choosing, with full context on each.

---

## Part 3 — The open-question format

Every entry carries four fields, because a question without them wastes the operator's attention:

1. **The question** — stated so it can be answered in one word where possible.
2. **Why it is a decision point** — what makes this the operator's call rather than the reviewer's. Usually: irreversibility, evidence spend, scope, taste, or risk appetite.
3. **Why a decision is needed now** — what is blocked, or what degrades while it waits. If nothing is blocked, say so; "no rush" is useful information.
4. **Options and implications** — each option's consequence, including the cost of *not* deciding.

---

## Part 4 — OPEN QUESTIONS REGISTER

### 🔴 Blocking — work cannot proceed without these

**Q-1 · CENSUS-1c: does the 1D lens stay in job 1?** *(ENGINE)*
- **Decision point:** it determines whether a finding can ever become a rule. The engine has no 1D timeframe anywhere (`INTERVAL_MS`/`MTF_SET` stop at 12h, verified from `cells.py`), so a 1D result is un-implementable without an engine change that breaks F-ENG.
- **Needed now:** CENSUS-1c cannot be drafted without it; every downstream Tier-C inherits the scope.
- **Options:** *(a)* include, labelled diagnostic-only — nearly free, completes the picture, but risks pressure to build an engine extension for a compelling number; *(b)* exclude — prevents an unactionable finding, discards information the substrate already contains. **Reviewer lean: (a).**

**Q-2 · CENSUS-1c: does 1c measure the D8 eligibility window?** *(ENGINE)*
- **Decision point:** it's a scope call — one extra job now versus an arbitrary constant in a rule contract later.
- **Needed now:** a 4H flag stays TRUE for 48 exec bars at 5m. Unpinned, a D8 add gate admits adds across a four-hour window rather than at the rung. The Tier-C needs a number.
- **Options:** *(a)* measure all three windows (first-bar / N-bar / full-period) in 1c — Tier-C inherits a measured constant, costs one job; *(b)* defer to the Tier-C — keeps 1c tight, but ships a rule contract carrying an unmeasured constant, which is the pattern behind several halts. **Reviewer lean: (a).**

### 🟡 Live — not blocking, but degrading or accumulating

**Q-3 · `s3_excursion_substrate.jsonl` is git-tracked while every sibling is fenced.** *(SYSTEM)*
- **Decision point:** it's a governance question about the fencing discipline, not a technical one. Only the operator knows whether it was deliberate.
- **Needed:** no urgency — 5.7 MB, and the whole pack is 2.59 MiB. But it's the one hole in an otherwise perfect record, and unexplained exceptions erode a rule.
- **Options:** *(a)* deliberate exception — document why in the ledger and close it; *(b)* drift — fence it, accepting that history retains the blob; *(c)* leave undetermined — costs nothing today, but the next auditor asks the same question.

**Q-4 · Cowork adoption.** *(ALL)*
- **Decision point:** it changes where work happens and how much the operator supervises. Verified capabilities: direct local file access (kills the screenshot round trip), scheduled recurring tasks (not available in chats), sub-agent coordination, Dispatch routing. Verified limitation: Projects are local-only, no cross-device sync.
- **Needed:** the screenshot return path is the single largest attention cost measured (~40% of operator actions).
- **Options:** *(a)* run a ten-minute test — open Cowork on the repo folder, ask it to read `_reviewer_box/MANIFEST.json` and summarise, and check whether it sees this Project's context box; *(b)* adopt for scheduled tasks only (daily brief, nightly manifest); *(c)* defer. **Reviewer lean: (a) before anything else — the answer is cheap and it determines whether the rest of this protocol is worth building.**

**Q-5 · Archive `tc5` (398 MB) and leave `census` alone?** *(SYSTEM)*
- **Decision point:** `census` is the active evidence base CENSUS-1c will read; `tc5` is closed.
- **Needed:** no urgency. The tree is ~1.9 GB, comfortably inside quota.
- **Options:** *(a)* archive tc5 too — ~380 MB recovered, one command once `backup_estate.py` exists; *(b)* leave both — the tree is already healthy. **Reviewer lean: (a) once the script is built, since it costs one command.**

**Q-6 · `v12_v3_anchor_packet_20260713.zip` (43 MB, untracked).** *(SYSTEM)*
- **Decision point:** unknown whether its contents are inside `v3_anchor_2026-07-27.zip` or are a distinct curated packet.
- **Needed:** no urgency; it's one file.
- **Options:** *(a)* verify contents against the phase archive, then delete if subsumed; *(b)* leave it. **Reviewer lean: (a), bundled into the next SYSTEM paste.**

### ⚪ Parked — recorded so they aren't lost

**Q-7 · D-2: does TC-1 arm B become the reference architecture?** *(ENGINE)* — parked since S-2b; the structural stop is the architecture of record in practice but has never been formally adopted.

**Q-8 · SSv11.4 display decisions D-SS-1..7.** *(ENGINE)* — Report 5 open; display-only, no study impact.

**Q-9 · S-1 / arm-A excursion back-fill.** *(ENGINE)* — named follow-up from S-3's D5; byte-safe re-emission, enables joins that currently can't be made.

**Q-10 · reviewer_manifest v1.1 amendments.** *(SYSTEM)* — F-M1 strengthened to a manifest round-trip test (as ratified it cannot fail); §1.3's git-command enumeration to read "including but not limited to", naming `config --get`; add `onedrive_running` surveillance. Non-blocking; the tool is usable as-is.

---

## Part 5 — Standing conventions this register assumes

- **Paste design:** every paste carries its own decision tree for predictable outcomes. A round trip is spent only when a branch genuinely needs operator or reviewer judgement. *(Adopted 2026-07-27 after measuring 17 round trips where roughly half were predictable branches.)*
- **Environment assertion first:** every paste, read-only included, opens with a hard assertion that halts before any write.
- **Post-action gates:** verification steps are written from the state that will exist *after* the paste's own actions, simulated step by step before shipping.
- **Output convention:** builder writes structured output to `_reviewer_box/` rather than to the terminal alone, so the return path is one file drop rather than N screenshots.
- **R-A′:** cloud sessions push in-session or the work does not count.