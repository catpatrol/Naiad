# HANDOFF — ATHENA · Full State, Every Open Ticket
### Also a Pantheon update: any lane reading this in the project box gets current
**Written by:** ATHENA (outgoing session) · **Date:** 2026-08-03 · **For:** the next ATHENA session, and every sibling lane

**Provenance tags are load-bearing.** `[verified]` = computed or read this session · `[ledger]` = in the committed ledger · `[ratified]` = operator decision on record · `[operator]` = operator-reported, not independently checked · `[handoff]` = builder-reported · `[open]` = undetermined. **An operator-reported fact is never `[verified]`** — that exact confusion produced a logged error on 2026-07-28.

---

## 0 · Read this first — how to see anything

**The project box is in SEARCH MODE.** GitHub-synced repo files are *indexed for retrieval*, **not mounted as browsable files**. Listing the mounted project directory shows only flat hand-uploaded files and will make a perfectly working sync look broken — this cost seven turns on 2026-08-03.

**Use the project-knowledge search tool, never a directory listing.** Synced files return real repo paths (`exchange/status/CADENCE.md`); hand-uploads return flattened names with fingerprints — a leading dot stripped (`.gitignore` → `_gitignore`) or a doubled underscore from a browser's `(1)` suffix.

**Verified working 2026-08-03:** searching returns `exchange/DIGEST.md`, `exchange/status/*`, `exchange/reports/*`, `docs/history/*`, `LEDGER.md`. The ferry loop is closed — builder reports no longer need attaching. `[verified]`

---

## 1 · Who you are

**ATHENA**, the resilience and sustainability lane. You inherit the old SYSTEM lane: repo operations, integrity, backups, the manifest ritual, scheduled routines, workflow design, context compaction. You are a **web chat** — you share the project box and project memory with APOLLO and ARGUS, you cannot read their conversations, you cannot touch the local disk, you cannot run on a schedule. Your hands are HEPHAESTUS (via paste-gos the operator runs) and HERMES (Cowork, who can touch files).

**The operator is Ludwig**, no programming background, owns every ratification and gate. Every decision you put to him is a **decision-funnel interview**: what it is in plain language · why it matters and why it needs *his* judgment · every option including your recommendation · the implications of each. Questions are self-contained; never reference scrollback. Big questions first, details cascading (HTF→LTF).

---

## 2 · The two standing workstreams

### 2.1 · DATA INTEGRITY

**The founding lesson.** A ledger risk note recorded the raw price journals as *"the single irreplaceable asset, on one machine under OneDrive."* **It was wrong, and had been since Phase 0.** The estate resolves through `engine/data.py:39-48 cache_dir()` to `%LOCALAPPDATA%\naiad\data_cache` — outside the sync root entirely, in a directory backup tools routinely exclude. It had **no protection of any kind** for the project's whole life. It survived months of careful work because nobody checked the actual path. That is the argument for everything below. `[verified]`

**The three tiers:**

| Tier | Contents | Protection |
|---|---|---|
| **1 · Data estate** | `%LOCALAPPDATA%\naiad\data_cache` — ~70 files, ~653 MB of klines + funding | `--estate` generations: 2026-07-28 (492,306,779 B) and 2026-08-02 (493,542,600 B) on `G:\My Drive\naiad-backups`, plus a 2026-07-27 generation on two browser-uploaded Drive accounts |
| **2 · Repo** | code, ledger, contracts, phase archives | GitHub is the durable copy of tracked files; phase archives in `research_outputs\_archive\` are the **PRIMARY** copy |
| **3 · The AI operating system** | conversations, project memory, preferences, primers, skills, exchange | `--workflow` generations (now 167 members incl. `scripts/` and root `*.md`); conversations export manually only; **project memory is NOT in any export** |

**The verification standard, and why it is trustworthy:** bidirectional per member — bytes re-read *out of* the archive must hash equal to a fresh read of the source **and** every embedded manifest pin must agree with both. Set membership cross-checked archive/manifest/disk so no stray or omission can hide. **F-K5** re-reads the archive *from the destination after writing*, which catches truncated or half-synced cloud writes. A no-clobber guard makes generation loss structurally impossible. `[verified]`

**🔴 RESTORE HAZARD.** Archives embed `MANIFEST.json` at their root while some phase folders carry `manifest.json`. On case-insensitive Windows, **extraction silently overwrites one with the other.** Confirmed on both tc5 and s3. Restore case-sensitively or rename one entry first. `[verified]`

**🔴 OPEN DEFECT — the retention rule, and it is mine.** `exchange/status/RETENTION.md` currently prints:

> `2026-07-27` · 6 archives · 1,025,189,589 B · **NO — outside the rule**

Those six archives (`s1 s2 s3 tc1 tc4 v3_anchor`) are the **only compressed copy of 20.56 GB of unique study evidence** — six *different phases*, not generations of one thing. My rule said "keep 1 phase set," which treats them as interchangeable snapshots. **Acting on that line would destroy irreplaceable evidence.** A correction paste exists (see §4, ticket T-1) and has not run. Until it does, **prune nothing flagged under "Phase sets."** `[verified]`

**Deletion policy by archive type — the answer to "should I delete previous zips":**

| Type | Generations? | Delete older? |
|---|---|---|
| Estate | Yes | Eventually — keep newest 4. Only 2 exist; delete nothing yet |
| Workflow | Yes | Eventually — keep newest 4. Only 1 exists |
| **Phase** | **No — each is a distinct phase** | **NEVER on a retention rule** |

**Correction to a common assumption:** the scripts write **directly into `G:\My Drive\naiad-backups`**, which Drive for Desktop syncs automatically. **No manual upload is required** for that account. What *is* manual: the **second Drive account is browser-only and not machine-verifiable**, and confirming a scheduled run actually fired.

### 2.2 · CONTINUOUS IMPROVEMENT OF OUR USE OF CLAUDE

**The measurement that drives it.** On 2026-07-26/27: **25 paste events, 8 misrouted (32% waste), ~150 discrete operator actions, of which 9 were decisions — 6%.** Everything built since attacks that denominator. `[verified]`

**The three costs and their cures:** routing (operator-facing routing line + hard environment assertion that halts before *any* write, read-only pastes included — because a misrouted write fails loudly on preconditions while a misrouted **read-only** paste silently returns plausible nonsense) · transport (one report file per paste, never screenshots; now superseded by the sync bus) · round trips (every paste carries its own decision tree for predictable outcomes).

**The reviewer error taxonomy — three classes, and the reviewer's mistakes are almost never analytical:**

- **Class A · Machinery-content** — asserting what the code or data contains without reading it. *Instances:* `census.json` holds relative paths and cannot pin a location · `tf_align=15m` when 15m is not in `MTF_SET` · "estate under OneDrive" · `claude/STATUS_ENGINE.md` specified when it has never existed · **reading `ls` output as proof the sync was broken while the box was in Search mode**. *Cure:* the context-gap audit moves **into contract drafting**; any §Basis claim must cite a file actually read this session.
- **Class B · Post-action-state** — writing a verification gate from the state *before* the paste's own actions run. *Instances:* a five-file deletion list against an empty-worktree gate when ten existed · a ledger entry asserting 18/18 while the same paste restored a file making it 19/19 · a phase-directory deletion contradicting its own expected-EMPTY git status · `.gitignore` covers `*.zip` but not the `.sha256` sidecar, so writing it legitimately failed F-K3. *Cure:* simulate the paste's own steps in order; write every gate from the **post**-action state before shipping.
- **Class C · Provenance** — promoting an operator or builder report to `[verified]`. *Instance:* a STATUS block tagged a Google Drive folder `[verified]` from an interview answer; the folder did not exist.

**The counter-pattern, and it is the system working:** the builder has refused a reviewer instruction on a ratified invariant at least **six** times — deleting git-tracked files, committing raw candles against charter §10, rewriting an allowlist into a Bash-breaking backslash form, appending false ledger history in a misrouted clone, treating a push authorization as transferable across environments, and throwing away real lane history to honour a wrong filename. **A stack whose executor never pushes back is a stack whose reviewer errors all land.**

---

## 3 · Verified infrastructure

**Scripts** (all under `scripts/`): `reviewer_manifest.py` v1.1 · `daily_brief.py` (F-B1..8) · `daily_routine.py` + `routine_jobs.json` (a config-driven **job registry** — new jobs are added by editing JSON, never code) · `backup_estate.py` (modes `--estate` `--phase` `--verify` `--workflow`, fixtures F-K1..7 incl. tracked-file preservation; deletion opt-in behind `--delete-source`) · `publish_exchange.py` (path-scoped publish guard, dry-run 12/12 including rejecting an `exchangeable/` lookalike, so evidence physically cannot ride an auto-push).

**Triggers ARMED** (Windows Task Scheduler): daily routine **07:00 every day** · estate backup **Sundays 08:00** · workflow backup **Sundays 08:30**. Next weekly runs: **2026-08-09**. `[handoff]`

**Environment:** venv at `C:\venvs\naiad` (Python 3.12.10), outside OneDrive and not in the repo. A venv cannot be moved, only rebuilt; scheduled tasks must call python by full path. Repo tree ~1.41 GB after the tc5 release (was 21.78 GB). `C:` ~35 GB free · `G:` ~11 GB free.

**The reviewer manifest — what it is and whether it still earns its place.** Built 2026-07-26 because establishing repo state cost hours of screenshot relay. One command emits `exchange/status/MANIFEST.json`: HEAD, branch, ahead/behind, worktree state, per-file size + sha256 + `match_head` for ~46 tracked sources, untracked inventory, `ledger_head`, `lane_last_commit`, `queue_open`. It runs unattended as **job #1** of the 07:00 routine. On its first three runs it caught a stale `.gitignore`, two reappeared root files and two unresolvable box names. **Its transport role is now superseded by the sync bus; its verification role remains and is why it stays.** `[verified]`

---

## 4 · EVERY OPEN TICKET

**T-1 · 🔴 Retention rule correction — HIGHEST PRIORITY.** A paste exists (drafted 2026-08-03, unrun) that: separates phase archives from generational archives so they can never be flagged prunable; verifies whether `daily_routine.py` has the `## 0. ACTION REQUIRED` alarm section and `HEARTBEAT.md`, adding both if absent; adds a `SECOND_ACCOUNT.md` reminder for the browser-only Drive account; and adds `--force-same-day` so the no-clobber guard stops forcing manual archive deletions (it has forced **four**). *Until this runs, prune nothing.* `[open]`

**T-2 · Arm HERMES.** `exchange/DIGEST.md` is still a **PLACEHOLDER**; his scheduled run is the only `CADENCE.md` trigger NOT ARMED. He is the answer to the operator's question *"can we use Hermes to keep track of file creation and movement — what has and hasn't been saved, why was this file created, who should read it."* A full re-primer enabling a complete first end-to-end run was written 2026-08-03: `PRIMER_HERMES_2026-08-03_v2_FIRST_RUN.md`. **This is the last unbuilt piece of the waterwheel.** `[open]`

**T-3 · Project memory restructure.** Memory is a **shared 30-slot budget across all lanes** and is at 30/30. Four slots freed on 2026-08-03 were consumed by other lanes within hours. The full inventory, the design proposal, and the decision funnel are in §6. `[open]`

**T-4 · The memory snapshot — still owed, and it is the last unprotected asset.** Project memory is **not included in Anthropic's data export**; a reviewer-written snapshot under `docs/memory/` is the only durable copy. The existing snapshot (`claude_project_memory_2026-07-26.md`) covers 21 entries and is stale; current is 30. `docs/memory/README.md` exists and states the convention. `[open]`

**T-5 · `OPERATOR_PREFERENCES.md` Part 1.** `docs/primers/OPERATOR_PREFERENCES.md` exists with two parts. **Part 1** is three empty blocks the operator must fill by hand — user preferences, project instructions, custom style — because these live only in Claude's cloud settings and appear in no export. **Part 2** is ATHENA's distillation of working conventions, still marked TO BE FILLED. `[open]`

**T-6 · Monthly conversation export.** Settings → Privacy → **Export data** → emailed link → save into `G:\My Drive\naiad-backups\operator-exports\` (created and empty). The alarm in T-1 nags after 35 days. `[open]`

**T-7 · Queue item 001** — `exchange/queue/001_condensed-project-history.md` carries `RATIFIED: PENDING`. It commissions `docs/PROJECT_HISTORY.md`, ledger-derived and provenance-tagged, superseding the pile of dated handoffs. **One word from the operator releases it.** `[open]`

**T-8 · Box cleanup.** Full list in §7. Now genuinely safe because sync supplies the repo. `[open]`

**T-9 · Phase archives are single-provider locally.** `research_outputs\_archive\` is the PRIMARY copy; whether every phase archive also sits on both Drive accounts is `[operator]`-reported, not machine-verified. Worth one confirmation pass. `[open]`

**T-10 · APOLLO and ARGUS ledger seeds are stale.** Both were synthesized from older status docs and carry PENDING items long since resolved. Marked as stale in-file with provenance notes; each lane should refresh its own. `[handoff]`

**T-11 · Parked, recorded so they are not lost:** manifest v1.1 further amendments · whether to archive `census`/`census_run2` · the `2026-07-29` analytics archives (26 KB) flagged prunable by the same broken rule · `_daily_archive` gitignore line (approved on the `research_outputs/brief/` precedent).

**RESOLVED — do not re-investigate:** the `t <t@t>` committer was this clone's own `git config --local`, not a foreign actor; commit `9470d04 "base"` created `scripts/orchestrator_state.py` (410 lines) and set that config in one act — it is also the explanation for the 07-28 "foreign files" and the stale `index.lock`. Identity is corrected going forward; history was deliberately **not** rewritten because the ledger cites SHAs. `[verified]`

---

## 5 · Discrepancy register

| # | Discrepancy | Explained by the manifest? |
|---|---|---|
| 1 | Phase archives flagged "outside the rule" | **No** — rule-design error (ATHENA's). T-1 fixes it |
| 2 | 2026-07-29 analytics archives (26 KB) flagged prunable | No — same rule flaw |
| 3 | Workflow archive `a480625a…` manually deleted for a same-day re-run — the **fourth** such deletion | No — no-clobber has no same-day path. T-1 adds `--force-same-day` |
| 4 | Phase archives live local-only in `research_outputs\_archive\` | No — single-provider primary copy (T-9) |
| 5 | `DIGEST.md` still a placeholder | No — Hermes unarmed (T-2) |
| 6 | Second Drive account browser-only | No — structurally unverifiable |
| 7 | `t <t@t>` and the "foreign files" | **Yes — resolved** (see §4) |
| 8 | 07-28 stale `index.lock` | **Yes — annulled**, same cause |

Two of eight resolved by the manifest; the rest are design or process gaps. That is the honest split.

---

## 6 · The memory question — inventory, research, proposal, funnel

### 6.1 · The 30 slots, exactly as they stand

| # | Entry | Class | Verdict |
|---|---|---|---|
| 1 | SS Pine display backlog (B-1, B-3) | Apollo backlog | move → CONVENTIONS |
| 2 | Reporting methodology (zero-context explainers) | operator style | **KEEP** |
| 3 | Guiding attitude ("alpha buried under debris") | operator direction | **KEEP** |
| 4 | TC-4 design rulings | study history | merge |
| 5 | Fractal lens | analytic frame | **KEEP (condense)** |
| 6 | Study findings through 2026-07-20 | study history | **KEEP (already merged ×6)** |
| 7 | Exact paste-ready text rule | convention | move → CONVENTIONS |
| 8 | Standing reviewer practice (context-gap audit) | convention | move → CONVENTIONS |
| 9 | Claude-optimization track | history | move → CONVENTIONS |
| 10 | Two builder environments | machinery | merge into 11 |
| 11 | Paste-routing + env assertion + file disposition | convention | **KEEP (pointer form)** |
| 12 | Estate location + rulings | machinery fact | **KEEP** |
| 13 | Multi-chat orchestration + STATUS block | convention | **KEEP (condense)** |
| 14 | Workflow-design rule | convention | move → CONVENTIONS |
| 15 | BRIEF/Argus lane purpose | lane charter | move → CONVENTIONS |
| 16 | Standing workflow preference | convention | merge into 14 |
| 17 | Renames + rescope + SS working definition | lane defs + study | **KEEP (split)** |
| 18 | Decision-gate & workflow rules | convention | merge into 27 |
| 19 | SS interview rulings Q1c–Q11 | study design | move → CONVENTIONS (Apollo's) |
| 20 | **Prime directive** | identity | **KEEP — never move** |
| 21 | Olympian architecture + pause | identity | **KEEP (condense)** |
| 22 | Workflow architecture RULED (W1/W2, F2, F4) | machinery + ruling | **KEEP** |
| 23 | Reviewer error taxonomy | behaviour-critical | **KEEP** |
| 24 | Backup architecture, three tiers | behaviour-critical | **KEEP (condense)** |
| 25 | Infrastructure inventory | reference | move → CONVENTIONS |
| 26 | Surface-access map (Search mode!) | behaviour-critical | **KEEP** |
| 27 | Decision-funnel interview format | operator style | **KEEP** |
| 28 | Builder handback standing rules | convention | move → CONVENTIONS |
| 29 | Manual-task instruction rule | convention | move → CONVENTIONS |
| 30 | Rulings 2026-08-03 (forensics, discriminant, W-F1) | study history | Apollo's — merge later |

**Rough shape: ~13 stay, ~12 move to a synced conventions file, ~5 merge.** That would land memory near 15/30 with genuine headroom for four lanes.

### 6.2 · What the research says

Anthropic's own guidance is unusually direct: <cite index="18-1">keep memory to facts Claude should hold in every session — build commands, conventions, project layout, "always do X" rules — and if an entry is a multi-step procedure or only matters for one part of the codebase, move it to a skill or a path-scoped rule instead</cite>. On length: <cite index="18-1">these files are loaded in full regardless of length, though shorter files produce better adherence</cite> — so bloat does not just cost slots, it **degrades compliance with what remains**. And the retrieval model I am proposing is theirs: <cite index="18-1">topic files are not loaded at startup; Claude reads them on demand using its standard file tools when it needs the information</cite>.

Two more, both apposite: <cite index="15-1">leverage imports and avoid duplication across memory files — instead of copying content that exists elsewhere, reference it</cite>, and the warning that matters most given entry #13's wrong paths — <cite index="17-1">if Claude saved an incorrect assumption early on, it will keep applying it until you remove it</cite>.

### 6.3 · The honest answer to "do rules moved to conventions still determine project behaviour?"

**Partially — and pretending otherwise would be the error.**

- **Authority is unchanged.** A ratified rule stays ratified wherever it is written. `CONVENTIONS.md` in the repo is *more* durable than memory: versioned, hash-pinned, backed up by `--workflow`, and **included in exports** where memory is not.
- **Enforcement is weaker unless engineered.** Memory is injected into every conversation automatically. A repo file is read **only if the lane goes looking**. Move a rule without a hook and you have quietly made it optional.
- **Therefore the pointer must stay in memory.** One slot reading *"at session start, read `exchange/status/CONVENTIONS.md`; it is authoritative for paste construction, reporting, file handling and lane etiquette"* preserves behaviour while freeing the slots the detail occupied. That single entry is the load-bearing part of the whole proposal.
- **Reinforce with rituals that already fire:** the `naiad-custodian` skill's session-start audit can name the file; the daily routine can flag a `CONVENTIONS.md` newer than the last STATUS block.

**Net:** you free roughly twelve slots **and** keep the behaviours — *provided* the pointer entry exists and the session-start ritual holds. Without those two, you free slots and lose behaviours. State that plainly to the operator; it is the whole risk.

### 6.4 · Decision funnel — scoping the memory restructure

**M-Q1 · Do we adopt the two-tier model at all?**
*What it is:* memory keeps identity, operator style, behaviour-critical facts and one pointer; `exchange/status/CONVENTIONS.md` holds the detailed procedures, inventories and histories, read on demand through the sync bus.
*Why it is yours:* it changes how reliably every lane follows the rules you ratified.
*(a)* **Adopt** *(recommended)* — frees ~12 slots, gives four lanes headroom, improves adherence to what remains, and puts conventions somewhere exportable and backed up. Risk: a rule not read is a rule not followed, mitigated by the pointer and the ritual. *(b)* **Keep everything in memory** — maximum automatic injection, but the cap is already binding and lanes will keep evicting each other. *(c)* **Adopt for reference material only** (inventories, histories) and keep all behavioural rules in memory — safest, frees ~5 slots instead of 12.

**M-Q2 · Who owns `CONVENTIONS.md`?**
*(a)* **ATHENA drafts, operator ratifies, Hermes flags staleness** *(recommended)* — matches existing lane roles. *(b)* Each lane owns its section. *(c)* Hermes owns it — but he must never re-author content, so this conflicts with his charter.

**M-Q3 · What is the per-lane memory budget?**
*Why it is yours:* four lanes share 30 slots with no arbitration, which is why the cap keeps recurring.
*(a)* **Soft budget: 6 slots per lane + 6 shared** *(recommended)*, published in `CONVENTIONS.md`, with a lane needing a seventh required to merge one of its own first. *(b)* No budget, first-come. *(c)* Only ATHENA edits memory; other lanes request via the queue.

**M-Q4 · Cadence of memory audit?**
*(a)* **At every phase boundary** *(recommended)* — natural, already a ritual. *(b)* Monthly. *(c)* Only when the cap is hit — which is what has been happening, and it means edits get made under pressure.

**M-Q5 · Does the memory snapshot become a scheduled artifact?**
*(a)* **Yes — regenerate at every audit and at every phase boundary** *(recommended)*; it is the only durable copy since exports exclude memory. *(b)* Ad hoc when someone remembers.

---

## 7 · Box cleanup list — reissued, safe now that sync works

**Remove now — superseded or duplicated, all present in the repo:**

*Superseded handoffs and state docs (9):* `REVIEWER_HANDOFF_2026-07-12` · `REVIEWER_HANDOFF_2026-07-13_V3_FORENSICS` · `REVIEWER_HANDOFF_2026-07-25_ENGINE_INGESTION` · `HANDOFF_2026-07-26_Daily_Brief_Design` · `HANDOFF_2026-07-27_BRIEF_to_ENGINE` · `HANDOFF_2026-07-27_BRIEF_to_CENSUS_1` · `HANDOFF_2026-07-29_REVIEWER_CHAT_to_SECRET_SAUCE` · `STATUS_HANDOFF_BRIEF_2026-07-28` · `PROJECT_STATUS_AND_CONTEXT_2026-07-28`

*Duplicates (2):* `AMENDMENT_2_BRIEF2_RESHAPE_1.md` — the `_1` is the browser duplicate signature, keep `AMENDMENT_2_BRIEF2_RESHAPE.md` · `Cascade_Atlas_CENSUS_1b_v2__1_.html` if still present — keep `Cascade_Atlas_CENSUS_1b_v2_1.html`

*Superseded status docs (6+):* `claude_STATUS_SYSTEM` · `claude_STATUS_ENGINE` · `claude_STATUS_BRIEF` · both `STATUS___*.txt` · `ORCHESTRATOR_CONTROL_CENTER___protocol___state_of_record.txt` · `__ORCHESTRATOR_PRIMER___*.txt` · `claude_ORCHESTRATOR_PRIMER.md` — **all superseded by `exchange/status/LEDGER_*.md`**, which sync now supplies

*Prometheus (3):* `Prometheus_Paper_Analysis_Week1` · `Prometheus_Data_Collection_Design` · `Prometheus_Stop_Loss_Logic_Learnings` — the deprecated first-agent repo, removed from scope by ruling R-A

*V3 phase artifacts (3):* `V3_RECOMPUTE_R1_R10` · `__V3_Anchor___Engine_Logic_Extract.txt` · `recompute.json` — archived and verified in `v3_anchor_2026-07-27.zip`

*Upload artifacts:* `_gitignore` — a mangled hand-upload of `.gitignore`; the real file arrives via sync

**Then, once you have confirmed a search returns `exchange/status/CADENCE.md`:** remove the ~50 manual copies of repo files — `LEDGER.md`, the engine `.py` files, the census/tc scripts, the configs, `census.json`, `DATA_CENSUS.md`. Sync supplies all of them, and each manual copy consumes capacity the sync needs.

**Keep:** the three WhatsApp architecture sheets only if the operator wants them (their content is transcribed into the primers and memory) · anything a lane is actively working from that is not yet in the repo.

**Sequencing matters:** remove superseded status docs *only after* confirming the synced ledgers are readable, or lanes lose their status view.

---

## 8 · Pantheon update — what every lane should know as of 2026-08-03

1. **The sync bus works.** Anything pushed to `exchange/` on `v12-v1-census` is readable by every web lane after one operator **Sync now** click — **via project-knowledge search, not a directory listing.**
2. **The exchange is the universal bus.** Operator ruling: all six actors exchange files through `exchange/` and no other route. Because it is tracked, auto-pushed and covered by `--workflow`, backing it up also preserves recent project context.
3. **Reports no longer need ferrying.** Builder reports land in `exchange/reports/` and every lane reads them there.
4. **Two mandatory artifacts per builder package** (operator, no exceptions): a **Builder's Report** (forensic, with the six-column file-disposition table) and a **Session Summary** (the decision artifact). Both to `exchange/reports/`, both published by `publish_exchange.py`.
5. **The file-disposition table is standing:** path · exists on disk · tracked/untracked/ignored · committed in which SHA · pushed yes/no · **protected by which backup**. Committed ≠ pushed; pushed ≠ backed up.
6. **Memory is a shared, contended resource.** Before adding an entry, merge one of your own. A restructure is proposed in §6.
7. **Do not prune phase archives** until T-1 lands.
8. **HERMES has never run.** Until he does, no lane should expect the DIGEST to be authoritative.

---

## 9 · First actions for the next ATHENA

1. Confirm exchange access with a project-knowledge search for `exchange/status/CADENCE.md`. If it returns a real repo path, the bus is live.
2. Read `exchange/status/RETENTION.md` and `exchange/status/LEDGER_ATHENA.md` for anything that moved since this handoff.
3. Put **T-1** (retention correction) to the operator first — it is the only ticket where inaction risks evidence loss.
4. Deliver **T-2** by handing `PRIMER_HERMES_2026-08-03_v2_FIRST_RUN.md` to a Cowork task with the naiad folder attached.
5. Run the **§6.4 funnel** for the memory restructure, then execute it with per-merge approval.
6. Write the memory snapshot (**T-4**) — it is the last asset with no copy outside Anthropic's cloud.

— ATHENA, 2026-08-03
