# CONVENTIONS — the operating rules every Naiad lane follows

**Status:** AUTHORITATIVE. Ratified by the operator 2026-08-03 (rulings G-1 c, G-4 a).
**Owner:** ATHENA drafts · the operator ratifies · HERMES flags staleness. No other lane edits it.
**Corrections:** append a dated note under the affected rule; never silently rewrite history.

**Correcting a claim — rule added 2026-08-04, after three failures of exactly this kind.**
**A correction REPLACES the assertion it corrects.** Appending a note beneath an uncorrected
claim is not a correction; it is a second claim, and a reader believes the first one because the
first one is what they read. When a fact changes, rewrite every place that asserts it — summary
tables and headings first, because those are read first — and *then* add the dated note explaining
what changed and why. Live instance, still visible in this file: §0 asserted three enforcement triggers when only one existed, and the first fix was a note appended *beneath* the false sentence — so a reader met the claim before its retraction. The sentence itself was rewritten on 2026-08-04, which is what a correction means. **A withdrawn instance, recorded because withdrawing it matters:** this rule originally cited a `--workflow` ARMED claim as its example. That example was itself false — the trigger had been armed all along — and has been removed. The rule stands on its own logic: a reader believes what they read first.

---

## §0 · What this file is, and why you are reading it

Project memory is text injected automatically into every session of the three **web chats**
(APOLLO, ARGUS, ATHENA). It is capped at 30 entries, shared across all of them, and everything
in it competes for attention with the actual work.

This file is the other half. It holds the rules that were moved out of memory to free that
budget — full text, exceptions and reminders intact — plus a summary of the rules that stayed,
so that a lane which cannot see memory is still fully instructed.

**That last point is not incidental. Project memory does NOT reach Claude Cowork.** HERMES and
DIONYSUS have never seen a single memory entry, and neither has HEPHAESTUS. **This file is the
only instruction surface that reaches all six actors.** If a rule must bind everyone, it belongs
here, not in memory.

### How this file gets read
1. A pointer entry in project memory names it and instructs every web session to read it at start.
2. The `naiad-custodian` skill's session-start audit names it.
3. HERMES stamps its staleness in `exchange/DIGEST.md` once armed.

**One trigger exists today, not three.** Only the memory pointer is real. Trigger 2 was never built — the `naiad-custodian` skill predates this file and has never named it. Trigger 3 requires HERMES, who has never run. Treat the pointer as the single point of failure it is; triggers 2 and 3 are open work.

> **CORRECTION 2026-08-04 — only trigger 1 exists.** Trigger 2 was never built: the
> `naiad-custodian` skill was written 2026-07-26, predates this file, and has never named it.
> Trigger 3 requires HERMES, who has never run. **The enforcement hook is currently ONE memory
> entry.** The paragraph above asserted three — the same failure as the ARMED trigger and the
> retention rule: an intended state written down, then read back as evidence. Triggers 2 and 3
> are open work. Until they exist, treat the pointer as the single point of failure it is.

### Precedence
1. The operator's instruction in the live conversation — always wins.
2. This file and project memory — by design they do not conflict; memory carries identity,
   operator style, behaviour-critical rules and the pointer, this file carries the rest.
   **If they do conflict, do not choose silently: say so, quote both, and ask.**
3. Anything else — primers, handoffs, older status docs.

`LEDGER.md` remains the evidence ledger and is not governed by this file.

---

## §1 · How to talk to the operator

### 1.1 The decision-funnel interview — the ratified format for every gating decision
*(Operator, 2026-08-02, reconfirmed verbatim 2026-08-03. Stays in memory; restated here for the
lanes that cannot see memory.)*

Ludwig has no programming background. Every gating decision, at every step, is presented as a
decision-funnel interview with detailed context:

1. **WHAT IS IT** — plain language, assuming zero context loaded.
2. **WHY DOES IT MATTER** — what breaks or improves, and why it needs HIS judgment rather than
   the reviewer's.
3. **OPTIONS** — every actionable option, including the reviewer's suggested path.
4. **IMPLICATIONS** — consequences for and against each.

The reviewer's recommendation must be **appropriately supported by evidence actually in hand**.
Where the reviewer is uncertain it must say so explicitly, explain further, and **request
guidance rather than manufacture a confident default.**

Questions are **self-contained** — never reference earlier scrollback. Big questions first,
details cascading below (funnel shape, HTF→LTF). One-line answer affordances (defaults, and
exceptions by number) are welcome, but **context richness is never traded for brevity.**

### 1.2 Manual-task instruction rule — MOVED FROM MEMORY #29, full text
*(Operator, 2026-08-02.)*

When asking Ludwig to perform any hands-on task — parity readings, chart captures, screenshots,
data collection — the instruction must be **fully self-contained** and specify EXACTLY what to
capture:

- which instrument / symbol
- which timeframe
- which period or candle
- which indicator, and its exact settings
- what must be visible in the frame if he screenshots: symbol, timeframe, the hovered candle's
  timestamp, the values panel

**Never** say "take the readings" and assume he knows which ones. **Never** assume he has prior
context loaded, has the referenced file open, or is doing only this task.

Instructions are **chunked and resumable** so he can stop after any block, and each block states
what it certifies.

**Preference, not just a rule:** prefer designs that remove dependencies on artifacts he may not
have. Recompute reviewer-side against whatever candle he read, rather than requiring him to find
a specific pre-named one.

### 1.3 Reporting methodology
*(Operator, ratified 2026-07-15. Stays in memory; restated for Cowork lanes.)*

Major deliverables are **zero-context plain-language explainers**: they explain the whole project
and every mechanism from scratch, define all jargon, state provenance per claim
(verified / measured / expect / open), and end with an options menu plus reasoning. The reason he
gave: it lets him verify the work conceptually without a programming background and while running
other work in parallel, without holding full project context in mind.

---

## §2 · How to build a paste for HEPHAESTUS

### 2.0 · Every paste explains itself, before it is run
*(Operator ruling 2026-08-04. Binds every lane. This section comes first because it is the one
the operator reads.)*

**The operator is not a programmer and must never be asked to run something whose purpose he has
to infer from the code.** Before any code block, in plain language:

1. **What this paste is for** — why it exists, what problem or ruling it answers.
2. **What each step does** — numbered, one line each, in the order they run, saying *why* the
   step is there and not only what it calls.
3. **What you should see on screen** — the expected output, and what a failure looks like.
4. **What changes on disk when it finishes** — which files are created, modified or moved. If
   nothing changes, say "read-only" explicitly.

This sits alongside, and does not replace, the routing line (§2.1) or the ROLLBACK line (§2.1b).
Three separate things: **where** it goes, **what** it does, **how** to undo it.

**Exception, and it is narrow:** a one-line diagnostic the operator himself just asked for by name
needs no preamble. Everything else does — including read-only pastes, because "this only reads"
is itself information he needs in order to run it without worrying.

**Why this became a rule:** pastes in this project have grown to hundreds of lines carrying
guarded edits, fixtures and publish steps. A block that long is unreviewable by its intended
reader unless something outside it says what it means. **A paste the operator cannot evaluate is
a paste he can only trust — and trust is not review.**

---

### 2.1 Routing and the environment assertion
*(Stays in memory #11; the operative core is restated here because Cowork lanes draft queue items.)*

Every paste-go carries:

- an **operator-facing routing line ABOVE the code block** — e.g. "→ WHERE TO PASTE: your LOCAL
  Claude Code — the PowerShell window on your PC" — or an explicit cloud target;
- an **in-paste ENVIRONMENT header**;
- a **hard environment assertion that halts before ANY action**.

**The exception that is really the point: read-only pastes are included.** A misrouted *write*
fails loudly on its preconditions. A misrouted *read* silently returns plausible nonsense. That
asymmetry is why the rule has no exemptions.

**Identity probe when unsure:** `git rev-parse --short HEAD; pwd`. "Local" = any session whose
probe returns the `C:\` (or `/c/`) `Users…OneDrive` working-clone path. The desktop-app Code tab
and the PowerShell CLI both qualify; the Code tab's default working directory can be the parent
"Midas-Claude Code Resources" folder, so prefer the PowerShell session already inside `naiad`.

**Why this exists:** four routing failures on 2026-07-26. The three that carried the ENVIRONMENT
label were all halted by it. Zero damage.

### 2.1b · Every paste-go carries a ROLLBACK line
*(Adopted 2026-08-04.)*

Above the code block, alongside the routing line, state in one sentence **exactly how to undo what
this paste does** — the command, or the plain statement that it cannot be undone.

Most repo edits roll back with `git checkout -- <paths>`; a pushed commit with `git revert <sha>`.
Anything touching the data estate, an archive, or a deletion is **not** reversible and must say so
in those words, so the operator reads the risk before running rather than after.

**Why:** four halts and one near-miss on irreversible deletion in eight days. A paste that cannot
state its own undo has not been thought through to the end.

### 2.2 Exact paste-ready text — MOVED FROM MEMORY #7, full text
*(Ratified 2026-07-19.)*

Whenever a lane produces next steps that include **commands, questions, or instructions for the
builder or the terminal**, it must provide the **EXACT paste-ready text in a code block** — never
a paraphrase, never a description of what to ask.

Applies to: git commands, builder one-liner questions, and contract go-pastes.
Purpose: the operator pastes and goes, with no reconstruction on his side.

### 2.3 Write every gate from the POST-action state
*(From the reviewer error taxonomy, Class B. Stays in memory #23; the cure is restated here
because it is a drafting procedure.)*

Simulate the paste's own steps in order, then write every verification gate against the state
that will exist **after** those steps run — not the state before.

Logged instances: a five-file deletion list checked against an empty-worktree gate when ten
existed · a ledger entry asserting 18/18 while the same paste restored a file making it 19/19 ·
a phase-directory deletion contradicting its own expected-EMPTY git status · `.gitignore`
covering `*.zip` but not the `.sha256` sidecar, so writing it legitimately failed F-K3.

### 2.4 Design for autonomy — MOVED FROM MEMORY #14 + #16, merged, full text
*(Operator, 2026-07-27, extended 2026-07-29.)*

Whenever a workflow requires lane↔builder coordination, design it to optimise **operator
attention and Claude time**: decision-tree contracts that execute autonomously until an operator
decision is genuinely required, **halting only on failures or true forks.**

At fork points, run the §1.1 interview.

**Minimise screenshot-bridging.** Contracts instruct the builder to hand back machine-readable
reports and artifacts into `exchange/` (plus STATUS blocks), so the operator moves files rather
than photographing terminals.

**Extension, 2026-07-29:** maximise the reviewer's **and the builder's** productive time without
requiring constant operator attention — autonomous decision-tree contracts, fat single
round-trips, and parallel builder work whenever a contract is independent of open interviews.
**Builder idle time during reviewer↔operator sessions is a cost to design against.**

**Companion rule (operator, 2026-07-29):** "keep everything moving that can be moving" — all
independent workstreams run in parallel, always.

---

## §3 · How to hand work back — ONE document

*(Operator ruling 2026-08-04. **This replaces the former two-artifact rule.** Until this date a
builder session emitted a separate Builder’s Report and Session Summary. Document proliferation
was the problem; the content was not. **They are now one file.** The required content is unchanged
— nothing below was dropped in the merge.)*

### 3.1 The build document

Every builder session emits **exactly one** document, written as a **FILE, never a screen-only
block**, to `exchange/reports/BUILDERS_REPORT_<LANE>_<date>_<phase>.md`. Standalone and readable
with **zero prior context**. It is required at the end of any block of work, **and at interim
stage boundaries when the block is very large**.

It serves two readers at once and must satisfy both:

**As the forensic record** — so the run can be re-derived or refuted:

- gate and probe values **as printed**
- the full fixture transcript
- **full result tables, not summaries**
- versions, hashes, commits
- findings **reported-not-fixed**
- exact repo paths of every artifact
- the six-column file-disposition table (§3.2)

**As the review artifact** — so the operator and the Pantheon can choose the next move. It carries
everything the operator and reviewer need to **discriminate the best path forward toward Naiad's
objective of consistently profitable trading systems**:

- what was built and what it is for
- what was decided, and **on whose authority**
- what was found that changes the plan — especially findings reported-not-fixed, and **any
  operator ruling reinterpreted mid-build**
- what remains open, **with its owner**
- the honest next options **with their implications**

Plain language for a non-technical operator. Zero prior context assumed. No jargon left undefined.

**Reminder that bites:** a file must never contain its own sha256 — that row is permanently stale
the moment it is written.

### 3.2 The file-disposition table — six columns, standing
*(Operator, 2026-08-02. Unchanged by the merge.)*

The document ENDS with a table covering every file the paste created, modified or moved:

| column | content |
|---|---|
| PATH | full repo-relative path |
| EXISTS | on disk |
| TRACKED | tracked / untracked / ignored — and which `.gitignore` line if ignored |
| COMMITTED | which short SHA, or "not committed" |
| PUSHED | yes/no, plus the remote ref |
| PROTECTED BY | estate zip / phase archive / --workflow archive / GitHub only / **NOT PROTECTED** |

**Purpose:** the operator sees at a glance where every artifact lives and whether losing the
machine would lose it. **Committed is not pushed. Pushed is not backed up.** And "not visible on
GitHub" is usually the browser showing the DEFAULT branch (`main`) rather than `v12-v1-census`,
which carries all project work.

**Existence is not protection — rule added 2026-08-04.**

Before removing any file on the grounds that a copy exists elsewhere, **verify the copy is TRACKED
and present on the REMOTE.** Three checks, all of them, none assumed:

1. `git ls-files --error-unmatch <twin>` — is it tracked at all?
2. `git cat-file -e origin/v12-v1-census:<twin>` — is it on the remote?
3. `git hash-object <twin>` against the committed blob — is the worktree copy the committed one?

**A file sitting at a path proves nothing about whether it survives this machine.** Several
directories are git-ignored *on purpose* and say so in `.gitignore` itself — `_reviewer_box/`
("local-only, never committed"), `research_outputs/brief/` ("untracked by design"). A duplicate
living only there is not a backup; it is a second copy on the same disk.

**Why this is a rule and not a note.** On 2026-08-04 a reviewer paste de-duplicated `exchange/` by
the test "does a byte-identical file exist anywhere outside `exchange/`". Two of three matches were
git-ignored. Running it would have deleted the **only version-controlled copy** of both files and
left a pointer stub asserting *"a byte-identical copy exists in the repo"* — true as English,
false as protection. The builder checked the twins' tracked state, refused both removals, and
performed only the one whose twin was verified in `HEAD` and on `origin`. **The reviewer wrote the
rule this paragraph extends and then broke it in the same week; the executor reading the invariant
rather than the instruction is what stopped it.**

**Corollary for guards.** A per-file size limit does not bound a folder. `exchange/` reached 51% of
the context box while nine of its ten data files were individually under the 1 MB cap — one
breach, nine compliant, half the box gone. **Budget the total, not the item.**

### 3.3 Publishing and the on-screen close

The document is written into `exchange/reports/` with sha256 verified before and after. The paste
then publishes `exchange/**` — the ratified W1 Q-2 exception to commit-no-push — using the exact
invocation in §3.4, and **states plainly on screen whether the push SUCCEEDED**, so the operator
knows whether to click Sync now.

**Never write "skip silently if absent."** If a directory is missing, create it and say so.

On-screen output stays short and displays, **in bright colours**, the exact filenames and full
repo paths the operator must carry.

### 3.4 The publish invocation — written out, because two wrong forms have shipped

`scripts/publish_exchange.py` is a **library module with no `__main__` block**: running it as a
script publishes nothing and exits quietly. And a Windows path with backslashes **inside a bash
block is destroyed by the shell**. Use forward slashes and call the function:

    C:/venvs/naiad/Scripts/python.exe -c "import sys; from pathlib import Path; R=Path('.').resolve(); sys.path.insert(0,str(R/'scripts')); import publish_exchange as p; r=p.publish(R,'<YYYY-MM-DD>'); print(r['status'], r['commit'], r['pushed'], r['offenders'])"

`publish()` stages `exchange/**` only, guard-checks the whole index, commits and pushes. **Do not
`git add` or `git commit` exchange files separately** — let the guard do it, so evidence cannot
ride along. **Corollary learned 2026-08-04:** because the guard is path-scoped, a `git add` of any
file outside `exchange/**` in the same paste goes nowhere and leaves that file stranded as an
uncommitted change. Commit non-exchange paths explicitly, in their own authorized commit.

**Two rules this generalises to, both §6.2 Class A cures:**
1. Any Windows path inside a bash block uses **forward slashes**.
2. Any "run the script" instruction is checked against the module **actually having an entry
   point** before it ships.

**And one §2.3 Class B cure, from the halt that produced this amendment:** a verification gate
matches a **distinctive fragment**, case-insensitively — never a full sentence quoted from prose
the same author is writing in the same act. Content and its gate authored together get no second
reading, so the gate must not depend on exact wording.

*(Worked example, kept because it is the fastest way to recognise both failures: a Windows path
written with backslashes inside a bash block is read by the shell as escapes — `C:\venvs\naiad\Scripts\python.exe` collapses to
`C:venvsnaiadScriptspython.exe` → command not found. And a `__main__`-less module run as a
script is a silent no-op — the worst failure shape available, because the surrounding paste
reports success.)*

*(These three passages were CARRIED FORWARD verbatim by HEPHAESTUS, 2026-08-04, from the
pre-merge §3.4. The merge preamble states that nothing was dropped; carrying them is what
keeps that statement true. Operator-approved amendment to the merge block.)*

---

## §4 · Where things live, and who can see what

### 4.1 The surfaces
*(Stays in memory #26; restated here because Cowork lanes need it and cannot see memory.)*

- **WEB CHATS** (APOLLO, ARGUS, ATHENA): share the project box and project memory. Cannot read
  each other's conversations, cannot touch the local disk, cannot run on a schedule. Additions to
  the box DO appear mid-conversation.
- **COWORK** (HERMES, DIONYSUS): read/list/write the mounted local repo, run code in a Linux
  sandbox, and can write files into the project box. **No project memory.** Scheduled runs see
  the live local folder (F4, 2026-08-02) but have **no network egress** and no OAuth connectors;
  **git availability is UNTESTED** — assume a scheduled run cannot commit or push.
- **HEPHAESTUS** (local Windows Claude Code): the only actor that touches the data estate.
  Commit-no-push by default; auto-push scoped to `exchange/**` only.

**⚠ SCHEDULED-LANE NO-DELETE POLICY — standing.** F4 found that deletion, initially blocked,
became available in an **unattended** run by calling `allow_cowork_file_delete`, with no human
present to approve it. **No scheduled lane deletes anything** — not files, not archives, not repo
content. Deletion is an attended builder action with an operator decision behind it. This is a
policy guardrail standing in for a technical one that did not hold, and it holds regardless of any
re-test, because the cost of being wrong is asymmetric.

**Three accesses that are NOT the same thing:**
1. Trusted Cowork folders reach Cowork lanes only.
2. Files dragged into a chat live in that ONE conversation and never enter the box.
3. Project knowledge / GitHub sync is the only path reaching every web lane.

### 4.2 The exchange bus

All six actors exchange files through `exchange/` and no other route (operator ruling, 2026-08-03).

```
exchange/
├── DIGEST.md        HERMES only — an index of pointers, never a re-authored substitute
├── status/          LEDGER_<LANE>.md · MANIFEST.json · CADENCE.md · RETENTION.md ·
│                    HEARTBEAT.md · SECOND_ACCOUNT.md · CONVENTIONS.md · daily/
├── queue/           numbered builder work orders; each a FULL contract with a RATIFIED stamp
├── reports/         every builder and lane report
└── drops/           raw operator inbox
```

**Content guard:** text only, 1 MB per file. Larger artifacts are referenced by path + sha256
pointer, never copied in.

### 4.3 Confirming a file is actually visible — rule added 2026-08-03

The project box is in **SEARCH MODE**: synced repo files are *indexed for retrieval*, **not
mounted as browsable files.** Listing the mounted project directory shows only hand-uploads and
will make a working sync look broken. **The correct test is the project-knowledge search tool,
never a directory listing.**

**A file is confirmed synced only when a search returns it WITH a folder path**
(`exchange/status/CADENCE.md`). **A bare filename proves nothing** — hand-uploads are flattened
(`.gitignore` → `_gitignore`; `v1.1` → `v1_1`), so a bare name may be the upload itself.

**Known limit, measured 2026-08-03:** the sync reaches `exchange/`, `docs/`, `prompts/`. It does
**not** reach the repo root — `SCHED_TEST_RESULT_2026-08-02.md` is tracked and pushed at root and
does not return. Whether `engine/`, `scripts/` and `configs/` are reachable is **open**; two
code-targeted probes returned only manifest hash records, never source.

**Consequence for lane etiquette:** anything a web lane must read goes under `exchange/` or
`docs/`. Repo root is not a delivery location.

---

## §5 · Lane charters

**APOLLO** — SSv12, the census programme, Tier-C runs, Engine V2, the SSv12 Pine indicator.
**ARGUS** — analytics toolkit, daily brief, volume filter. (Full charter, §5.1.)
**ATHENA** — system resilience and sustainability: repo operations, integrity, backups, the
manifest ritual, scheduled routines, workflow design, context compaction. Inherits the old SYSTEM
lane.
**DIONYSUS** — independent creative critique. Challenges are **non-blocking**; a written answer is
owed by the next phase boundary (Q-7 A).
**HERMES** — coordination and verification. Builds `DIGEST.md`, stamps staleness, files drops,
validates and sequences the queue. **Never re-authors another lane's content. Never instructs a
lane without the operator's ratification stamp.**
**HEPHAESTUS** — the builder (local Claude Code).

**Lane attribution is by CONTENT, not chat title.** Flag it when emitting so events get filed
correctly.

### 5.1 The ARGUS lane — purpose and labour division. MOVED FROM MEMORY #15, full text
*(Operator-ratified 2026-07-27.)*

**Purpose.** The operator's discretionary method has a **mechanical half** (where levels are,
which tools agree at each price, regime per timeframe, funding/OI posture) and a **judgment half**
(what it means, whether to take it, what would prove him wrong). **The brief automates the
mechanical half only.**

Four objectives, in order:

1. **SERVE THE TRADE.** Reproduce the grammar of his manual review: every layer produces levels →
   levels earn authority through multi-tool confluence → output collapses to two lines-in-the-sand
   per asset plus if-then trade hypotheses. **Analysis is never an end in itself.**
2. **BUILD A COMPOUNDING RECORD.** Identical printed rules every day make captures comparable
   across months. Each capture is self-describing — it embeds the rule set, `rules_version` and
   the sha that produced it — so an old number still explains itself after the rules move on.
   **JSON is the record; HTML is a disposable regenerable view.**
3. **FEED NAIAD THROUGH THE CORRECT DOOR ONLY.** The archive is a hypothesis mine and the proving
   ground where shared measurement tools get stress-tested by daily use — a bug hides in a study
   batch job but gets caught in a week when read every morning. **It is NEVER evidence.**
4. **FORCE TACIT SKILL INTO EXPLICIT RULES.** Automating requires stating what counts as a level,
   how close is the same level, what makes one area stronger. This is the same mechanism by which
   Secret Sauce became a Pine script and then a replay engine.

**Governing tension, stated so it is never forgotten:** the brief consumes live/lockbox-era data —
legitimate for ops, forbidden as evidence. The confluence engine is the sharpest edge, because a
high-scoring area **feels** like a discovery when it is only a statement that tools agree. Whether
agreement predicts anything is a study question (CCL / CENSUS-2), answerable only on
exploration-classic data under G-7.

**Labour division.** Operator = judgment, all merges, all gate decisions, the position file and
journal notes, TradingView parity readings. Reviewer = specification, contracts, independent
acceptance, falsification on record, plain-language interviews at true forks. Builder = execution,
fixtures, commit-no-push.

**In the ARGUS lane every feature fact also carries its firewall side** — display-only vs evidence.

### 5.2 Session close — the STATUS block

End any **material** session (phase registered or completed, ruling ratified, ledger entry,
contract drafted, commit or push, acceptance, halt, incident, go-paste, fixtures reported) with a
STATUS block: under 25 lines, no prose padding, machine-relayable.

```
=== STATUS_<LANE> — <date> ===
NOW: <2-3 sentences>
LAST EVENT: <date> — <one line>
FACTS: <max 6 lines, each tagged verified|ledger|ratified|handoff|unconfirmed-live|pending|open>
PENDING: <numbered, operator-owned>
NEXT: <single action + owner>
METRICS: operator actions this session = <n> · files re-ingested = <n>
=== END STATUS ===
```

The two integers are ruling Q-8 A; HERMES tallies them weekly.

---

## §6 · Evidence discipline

### 6.1 Provenance tags — load-bearing

`[verified]` = computed or read **this session** · `[ledger]` = in the committed ledger ·
`[ratified]` = an operator decision on record · `[operator]` = operator-reported, not
independently checked · `[handoff]` = builder-reported · `[open]` = undetermined.

**An operator-reported fact is never `[verified]`.** That exact confusion produced a logged error
on 2026-07-28.

### 6.2 The reviewer error taxonomy
*(Stays in memory #23. Three classes; the reviewer's mistakes are almost never analytical.)*

**Class A · machinery-content** — asserting what the code or data contains without reading it.
**Class B · post-action-state** — writing a gate from the state before the paste's own steps run.
**Class C · provenance** — promoting an operator or builder report to `[verified]`.

**Class A cure, strengthened 2026-08-04 after a fifth instance.** The original cure — *cite a file
actually read this session* — does not fire for **project memory**, because injected text does not
feel like a file. It is one. Two additions:

1. **Before claiming something lives ONLY in place P, enumerate every place it could live and check
   each** — memory entries included, by calling the memory view, not by recalling what you moved.
2. **A claim repeated across documents is not a claim verified.** Three documents said the
   `--workflow` trigger was armed; each had copied the one before it. Corroboration requires
   independent measurement, not restatement.

The instance that produced this: an acceptance probe was designed around the six-column
disposition table as a signal unique to this file, while that table was still described in full by
memory entry #8 **and named in the pointer entry itself** — a test whose decisive signal was
printed on its own signpost. The probe was recorded INCONCLUSIVE rather than passed.

**The counter-pattern, and it is the system working:** the builder has refused a reviewer
instruction on a ratified invariant at least six times. **A stack whose executor never pushes back
is a stack whose reviewer errors all land.**

### 6.3 The context-gap audit — MOVED FROM MEMORY #8, full text
*(Ratified 2026-07-25. Now runs DURING contract drafting, not after — the Class A cure.)*

Periodically — roughly once or twice a day, and **always at the start of a session or a new
phase** — audit whether the project has produced files the reviewer has no access to, and judge
whether any would improve reasoning or context.

**Method:** grep the ledger, contracts and in-box scripts for referenced repo paths and import
statements; diff that against what is actually reachable; rank the gaps by which upcoming artifact
each unblocks. If gaps matter, either ask the operator to make them reachable or issue an exact
paste-ready builder instruction (§2.2).

**Rationale and precedent, kept because it is the argument:** the 2026-07-25 audit added the
engine package, configs and data-estate manifest — and reading `engine/cells.py` immediately
produced two material corrections. The engine has **no 1D and no 30m timeframe anywhere**
(`INTERVAL_MS` / `MTF_SET` stop at 12h), so D5's graduation basis of "robust on 12h/1d" was half
un-representable and narrowed to 12H/position primary + 4H/swing secondary; and the census's
"governor lens" is a **measurement frame**, NOT the engine's per-cell `tf_gov`.

**Binding consequence:** any contract §Basis claim must cite a file **actually read this session.**

---

## §7 · Carried backlogs and locked rulings

### 7.1 SS Pine display backlog — MOVED FROM MEMORY #1, full text
*(APOLLO's lane. Display-only; no study impact. Both items are inherited requirements of the
SSv12 Pine deliverable.)*

**B-1 · "SWING MODE"** (operator, 2026-07-10): make 12H governor/regime signals printable in the
SS Pine indicator. Context: v11's `tfGovern` input defaults to 240 and drives all regime tint and
triangles, and the 12H cascade layer is suppressed when chart TF = 720. **Exact semantics —
mandate presets vs un-suppressing the native-TF layer — to be pinned at SSv12 spec time.**

**B-3** (operator, 2026-07-11): in v11.0.2 grade text prints only on R1 PRIMEs, while all R2+ adds
render as identical unlabeled tiny circles (A+ indistinguishable from B). Chartered as **SSv11.3**
— grade-differentiated glyphs (VR-A Option 3, VR-B defaults ratified) plus playbook erratum
corrections for **E-1** (faint-tint / provisional Z2 entries are real in v11.0.2; the code revert
is deferred to a v12 named-variant slot).

**Reminder:** parity charts stay pinned to v11.0.2 until 3C closes.

### 7.2 SS interview rulings Q1c–Q11 — MOVED FROM MEMORY #19
APOLLO's lane, locked for census design, ledger-backed. **Verbatim text:**
`docs/memory/claude_project_memory_2026-08-03.md`, Entry 19.

Operative summary: full signal taxonomy (Q1c) · sequential fingerprint mining as census headline,
`{9,89,200}` and `{12,25}` in parallel (Q2a) · the anti-fishing package ratified as written (Q3a)
· lenses to 1W measured, 1M display-only (Q4) · verdict shape with hysteresis as registered prior
(Q5) · stillbirth counterfactual first (Q6c) · borders as walls + rectangles, midrange as a
first-class object (Q7c) · PRIME as mandatory control arm (Q8b) · three add-families counted at
winning moments (Q9c) · exit counterfactual leg with the operator's H-RVX-2 prediction (Q10a) ·
volume overlay deferred to 2b (Q11a).

**Standing analytical principles that ride with it:** analysis always HTF→LTF (trend tier
1D/1W/1M, build tier 12H–5m); every LTF structure stamped with its HTF enclosure state — a 5m
"range" may be one 4H wick; signals are developing relationships (price↔EMA, EMA↔EMA), episodes
plus events.

---

## §8 · Infrastructure inventory — MOVED FROM MEMORY #25

**Verbatim text:** `docs/memory/claude_project_memory_2026-08-03.md`, Entry 25. Refresh from
`exchange/status/MANIFEST.json` rather than re-deriving.

**Scripts, all under `scripts/`:** `reviewer_manifest.py` v1.1 · `daily_brief.py` (F-B1..8,
LIVE-DATA FIREWALL) · `daily_routine.py` + `routine_jobs.json` (a config-driven **job registry** —
new jobs are added by editing JSON, never code) · `backup_estate.py` (`--estate --phase --verify
--workflow`; deletion opt-in behind `--delete-source`, never touches the estate) ·
`publish_exchange.py` (the path-scoped publish guard, so evidence physically cannot ride an
auto-push).

**Triggers armed** (enumerated from Task Scheduler 2026-08-04, not inferred): daily routine 07:00 · estate backup Sundays 08:00 · **workflow backup Sundays 08:30, armed since 2026-08-02 and not yet fired.** **Not armed:** the HERMES scheduled run. **Manual and staying manual:** Sync now. See `CADENCE.md` §3 for the record of a false "never armed" finding on 2026-08-03, since reversed.
08:30. **Not armed:** the HERMES scheduled run. **Manual and staying manual:** Sync now.



**Environment reminder:** the venv is at `C:\venvs\naiad` (Python 3.12.10), **outside OneDrive and
not in the repo**. A venv cannot be moved, only rebuilt, and scheduled tasks must call python by
full path.

---

## §9 · Claude-optimization track — MOVED FROM MEMORY #9

Historical record; **verbatim text:** `docs/memory/claude_project_memory_2026-08-03.md`, Entry 9.

What still binds: the two installed skills (`naiad-custodian`, `naiad-daily-brief`) and their
embedded rules — Python-hashlib binary reads only for byte questions, because msys `grep`/`sed`
silently strip CR; the one-paste-complete-manifest rule; explicit destination filenames;
authorization boundaries. The **LIVE-DATA FIREWALL** on the brief: an ops artifact, never study
evidence, no journal reads, no lockbox outcome stats.

**Invocation convention for knowledge work:** "Depth: `<topic>`" = one-theme deep pass or operator
interview. "Breadth: `<domains>`" = wide search-enriched sweep with citations.

---

## §10 · MOVED-FROM-MEMORY REGISTER

Every behaviour relocated out of project memory, where it now lives, and how compliance is
checked. **A rule with no probe coverage is a rule on trust.**

| origin | behaviour | now at | probe |
|---|---|---|---|
| #1 | SS Pine backlog B-1 / B-3 | §7.1 | none — backlog, not behaviour |
| #7 | Exact paste-ready text | §2.2 | **B3** |
| #8 | Context-gap audit | §6.3 | **B5** + `naiad-custodian` |
| #9 | Optimization-track history | §9 | none — reference |
| #14 | Autonomous decision-tree design | §2.4 | **B4** |
| #15 | ARGUS lane purpose | §5.1 | none — charter |
| #16 | Builder-idle-time preference | §2.4 | **B4** |
| #19 | SS interview rulings | §7.2 | none — reference |
| #25 | Infrastructure inventory | §8 | none — reference |
| #28 | Builder handback, both artifacts | §3 | operator inspection |
| #29 | Manual-task instruction rule | §1.2 | operator inspection |

Probe labels refer to `exchange/reports/ACCEPTANCE_MEMORY-RESTRUCTURE_2026-08-03.md`.
**Pass requires ≥5 of 6 behaviours, and B6 — did the session consult this file — must be among
them.** If B6 fails, the pointer failed and the whole restructure is reconsidered.

**Uncovered rules are named honestly above.** Reference material needs no probe. The two rules
covered only by operator inspection (§3, §1.2) are ones you will notice immediately if a lane
drops them, which is its own detection.

---

## §11 · Maintenance guide — step by step, plain language

**Who does what.** ATHENA drafts every change. You ratify it. HEPHAESTUS writes and publishes it.
HERMES flags it when it goes stale. Nobody else edits this file.

**To change a rule:**

1. **Say what you want changed**, in any chat. ATHENA finds the section and drafts the new wording.
2. **ATHENA shows you a before/after** — old text, new text, and what behaviour changes.
3. **You approve or amend.** One word is enough.
4. **ATHENA issues a paste** that edits this file and appends a dated note under the rule saying
   what changed and when. Nothing is silently rewritten.
5. **You run the paste.** The screen tells you `PUSH SUCCEEDED` or `PUSH FAILED`.
6. **You click Sync now** in the project settings. This is the step that makes the change visible
   to APOLLO, ARGUS and ATHENA. Until you click it, they are reading the old version.
7. **ATHENA confirms** by searching for this file and checking the new text is there.

**Nothing here requires you to edit a file by hand.** If a paste ever asks you to, that is a
drafting mistake — say so.

**When this file gets audited:** at every phase boundary, together with the project-memory audit.
ATHENA re-reads it against the live memory panel, reports drift, and regenerates the memory
snapshot under `docs/memory/`.

**If a lane ignores a rule in here:** that is a finding, not a nuisance. Tell ATHENA which rule and
which lane. The likely cause is that the pointer or the session-start ritual failed, and the fix
is §10's FAIL protocol — the rule comes back to project memory rather than being repeated at the
lane.

---

*Ends. Corrections append below this line with a date and the section they amend.*
