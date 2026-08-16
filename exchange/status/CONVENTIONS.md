# CONVENTIONS — the operating rules every Naiad lane follows

**Status:** AUTHORITATIVE. Ratified by the operator 2026-08-03 (rulings G-1 c, G-4 a).
**Owner:** ATHENA drafts · the operator ratifies. No other lane edits it. *(HERMES flagged staleness until ruling 007, 2026-08-15, put that lane dormant — §5.)*
**Shape:** restructured 2026-08-15 (THE GREAT COLLAPSE). One fact, one home, one pointer. §0 is read
by everyone; every other section is addressed, and read when its task comes up. Incident narratives
live in `docs/CASELAW.md`, cited as CL-n, off the bus.

**Format.** Every rule is three lines — **RULE** (what binds), *BECAUSE* (why), *EARNED-BY* (the
authority, and the case number where a narrative stands behind it). A rule that loses its BECAUSE is
on its way to being cargo-culted; one that loses its EARNED-BY cannot be told from a guess.

**Precedence.** (1) The operator's live instruction always wins. (2) This file and project memory —
by design they do not conflict: memory carries identity, operator style, behaviour-critical rules
and the pointers into this file; this file carries the rest, in full text. **If they do conflict, do not choose silently: say so,
quote both, and ask.** (3) Anything else — primers, handoffs, older status docs. `LEDGER.md` is the
evidence ledger and is not governed by this file.

**Reach.** This is the **only** instruction surface reaching all six actors — project memory does not
reach Claude Cowork, and HERMES, DIONYSUS and HEPHAESTUS have never seen a memory entry. If a rule
must bind everyone, it belongs here. **It holds the rules moved out of memory in full text, with
their exceptions and reminders intact, plus a summary of the rules that stayed — so a lane that
cannot see memory is still fully instructed.**

**One enforcement trigger exists, not three.** Only the memory pointer is real: `naiad-custodian`
predates this file and has never named it, and the staleness stamp needs HERMES, who has never run.
Treat the pointer as the single point of failure it is. *(CORRECTION 2026-08-04: this asserted three,
and the first fix was a note appended beneath the false sentence — so a reader met the claim before
its retraction. The sentence itself was rewritten, which is what a correction means. CL-1.)*

---

## FIND IT FAST — the question you have, and the section that answers it

*A retrieval search returns passages, not files, so a lane reading a chunk from the middle cannot
learn what else exists. This map is that way; a broad opening query surfaces it.*

| If you want to know | go to |
|---|---|
| What binds me before I know anything else, and what do I read at session start? | **§0** |
| Where is current state? | **§0** — THE MAP |
| How do I put a decision to the operator · ask him for a manual task · write him a report? | **§1** |
| Where do I paste this · how do I undo it · how do I write a gate that is not wrong? | **§2** |
| What is on this machine, and where does it live? | **§2.1** |
| What do I write at the end of a build · where did every file end up · how do I publish · how do I close? | **§3** |
| Who can see what · where do files go · what may never enter the bus · is this file visible to a web lane? | **§4** |
| What is my lane responsible for, and which sections do I read? | **§5** |
| How do I tag a claim · what does the reviewer keep getting wrong · how do I change a named constant? | **§6** |
| Which timeframes exist · what frame does a study start from · what is settled? | **§7** |
| Is this backed up · may I delete it, given a copy exists elsewhere? | **§8** |
| Why does a rule say what it says? | `docs/CASELAW.md`, cited as CL-n |
| How do I change a rule in this file? | **MAINTENANCE**, at the end |

## THE INDEX — section, token, and what is in it

*Quote the token to address a section from memory, a contract, or another lane.*

| § | token | what it holds |
|---|---|---|
| **0** | `NAIAD-S0-CORE` | THE FIRST RULE · the PRIME DIRECTIVE · the correction rule · THE MAP · the identity gate · the six invariants. **Every lane, every session.** |
| **1** | `NAIAD-S1-OPERATOR` | The decision-funnel interview · manual-task instructions · reporting methodology · invoking knowledge work. |
| **2** | `NAIAD-S2-PASTE` | Every paste explains itself · routing · rollback · the environment assertion · **2.1 this machine's geography** · exact paste-ready text · post-action gates · anchor context · shell hazards · autonomy. |
| **3** | `NAIAD-S3-REPORT` | The single build document · the disposition table with BOX COST · publishing and the on-screen close · the publish invocation · the STATUS block. |
| **4** | `NAIAD-S4-BOX` | The three surfaces · the exchange bus and its content guard · confirming a file is visible · the tick set · what may never enter the bus · determinism reruns. |
| **5** | `NAIAD-S5-LANES` | The six charters, each naming the sections that lane reads · queue drafting rights · lane attribution · the ARGUS charter in full · ledger discipline. |
| **6** | `NAIAD-S6-ERRORS` | Provenance tags · the three-class error taxonomy and its cures · the context-gap audit · the named-constant change protocol. |
| **7** | `NAIAD-S7-FRAMES` | The guiding attitude · the fractal lens · research inversion · the discriminant frame and TRG · MTF_SET · the EMA family · prior conclusions · sizing · analytical principles. |
| **8** | `NAIAD-S8-BACKUP` | Sync is not backup · existence is not protection · the three tiers · the binding verification standard · data residency v2 · the inventory and the armed triggers. |

---

## §0 · THE CORE «NAIAD-S0-CORE»

**WHO READS THIS: every lane, every session — before anything else, and before any other section.**

### THE FIRST RULE
**RULE — Be elitist, clever, concise, efficient, and elegant. Hold the highest standard of craft.**
BECAUSE signal-dense beats padded — no filler, no repetition, no restating what the reader already has; *clever* is the solution that makes the problem small, not the one that shows off; *elegant* is the shortest version that loses nothing — detail and context are never the fat, ceremony is.
EARNED-BY Operator, 2026-08-06. Binds every lane, document and paste. Where a rule below tensions with this one, keep the substance and cut the ceremony.

### THE PRIME DIRECTIVE
**RULE — Naiad develops profitable momentum trading systems. Secret Sauce is such system.**
BECAUSE it names the objective every other rule in this file serves, and it fixes Secret Sauce as an instance of the class, never as the project itself.
EARNED-BY Operator, 2026-08-15, verbatim.

> **CORRECTION 2026-08-15 — the sentence above REPLACES the 2026-08-01 wording.** That wording was,
> verbatim: *"Project Naiad's main purpose is to develop consistently profitable trading systems."*
> carried with the gloss *"Secret Sauce is ONE of Naiad's systems, not the project itself."* The
> operator restated the directive on 2026-08-15 and the restatement is what binds: **momentum** is
> now named as the class of system, where the old wording left the class open. The old text is
> quoted here, once, and asserted nowhere.

### THE CORRECTION RULE
**RULE — A correction REPLACES the assertion it corrects.**
BECAUSE appending a note beneath an uncorrected claim is not a correction; it is a second claim, and a reader believes the first one because the first one is what they read.
EARNED-BY Operator, 2026-08-04, after three failures of exactly this kind — CL-1.
**HOW** — rewrite every place that asserts the fact, summary tables and headings first because those are read first, and *then* add the dated note saying what changed and why. Never silently rewrite: the note is what keeps the history.

### THE MAP
**RULE — At session start read §0. Then read ONLY the section for the task in hand.**
BECAUSE this file instructs six actors across three surfaces; a lane that reads all of it spends its context on rules it will not use. §0 is what everyone shares; every other section is addressed to someone.
EARNED-BY Operator ruling 2026-08-15 (R2).

**Current state is NOT in this file.** It lives in three places, read in this order:

| what you need | where it is |
|---|---|
| your own lane's state | `exchange/status/LEDGER_<GOD>.md` |
| study state — verdicts, yields, the slate | `LEDGER.md` → **STANDING VERDICTS**, at its head |
| what exists, and the box budget | the **bus-health** and **budget** blocks — per-folder counts, bytes, ledger recency, manifest-vs-HEAD — printed on every publish and in `daily/DAILY_<date>.md` §8; repo state in `exchange/status/MANIFEST.json` |

> **RETIRED 2026-08-15 (ruling 007).** The first row was `exchange/DIGEST.md`, an index built by hand. Sources that report themselves replace it; final edition `docs/history/DIGEST_RETIRED_2026-08-15.md`.

Anything beyond those three is pursued as needed: ask the operator to drag the file into the conversation, where it costs nothing permanent (§4).

### THE IDENTITY GATE
**RULE — Every paste opens with the two-sided gate and halts before ANY action — read-only pastes included.**
BECAUSE a misrouted *write* fails loudly on its preconditions; a misrouted *read* silently returns plausible nonsense. That asymmetry is why the rule has no exemptions.
EARNED-BY Four routing failures, 2026-07-26 — CL-2. Sides restated 2026-08-15 for macOS; the two-sided SHAPE is unchanged.

```bash
case "$(pwd)" in *OneDrive*|*com~apple~CloudDocs*|*Mobile\ Documents*) echo "HALT: cloud tree"; exit 1;; "$HOME/Naiad") : ;; *) echo "HALT: not \$HOME/Naiad"; exit 1;; esac
```

Both sides are required: checking **only the path** passes a copy left behind in a cloud-synced tree, and checking **only for the absence of markers** passes any directory on the machine. Geography and the rationale for each side: §2.1.

### THE SIX INVARIANTS
Cited by number everywhere else in this file. Where one of these and a local instruction conflict, this wins.

1. **SYNC IS NOT BACKUP** — sync propagates deletions faithfully. → §8
2. **EXISTENCE IS NOT PROTECTION** — a file sitting at a path proves nothing about surviving this machine. Committed ≠ pushed ≠ backed up. → §8
3. **DOCUMENTS ARE CHEAP, DATA IS NOT** — so write more reports, never fewer; captures, renders, results JSONs, substrates, parquet and HTML never enter `exchange/`. → §4
4. **ONE BUILD DOCUMENT, AND IT APPENDS ITS LEDGER LINE** — every builder session emits exactly one document and ends by appending its STATUS entry to the commissioning lane's ledger. A report without its ledger entry is an incomplete deliverable. → §3
5. **EVERY GATING DECISION IS A DECISION-FUNNEL INTERVIEW** — what it is · why it matters · every actionable option · implications for and against. → §1
6. **TO CLAIM ABSENCE, ENUMERATE** — a negative from a single lookup measures that lookup, not absence. → §6

---

## §1 · OPERATOR INTERFACE «NAIAD-S1-OPERATOR»

**WHO READS THIS: every lane that addresses the operator — for gating decisions, hands-on task
instructions, and major deliverables.**

Ludwig is a discretionary crypto trader in Buenos Aires with no programming background. Every rule
here follows from that fact.

### 1.1 The decision-funnel interview
**RULE — Every gating decision is presented as a four-step funnel: (1) WHAT IS IT, plain language, zero context assumed · (2) WHY DOES IT MATTER, what breaks or improves, and why it needs HIS judgment rather than the reviewer's · (3) OPTIONS, every actionable one including the reviewer's own path · (4) IMPLICATIONS, for and against each.**
BECAUSE a technical summary put to a non-programmer is not a decision put to him at all; he can only ratify or trust, and trust is not review.
EARNED-BY Operator, 2026-08-02, reconfirmed verbatim 2026-08-03. Invariant 5.

**RULE — The recommendation is supported only as far as evidence in hand supports it; where the reviewer is uncertain it says so explicitly, explains further, and requests guidance rather than manufacturing a confident default.**
BECAUSE a confident default read by someone who cannot check it is indistinguishable from a finding.
EARNED-BY Operator, 2026-08-02.

**RULE — Questions are self-contained and never reference earlier scrollback; big questions first, details cascading below (funnel shape, HTF→LTF); one-line answer affordances are welcome, but context richness is never traded for brevity.**
BECAUSE he answers between other work, without the conversation loaded.
EARNED-BY Operator, 2026-08-02.

### 1.2 The manual-task instruction rule
**RULE — Any hands-on task asked of the operator — parity readings, chart captures, screenshots, data collection — is fully self-contained and states EXACTLY what to capture: which instrument, which timeframe, which period or candle, which indicator and its exact settings, and what must be in frame if he screenshots (symbol, timeframe, the hovered candle's timestamp, the values panel).**
BECAUSE "take the readings" assumes he knows which ones, has prior context loaded, has the referenced file open, and has no other task. None of those hold.
EARNED-BY Operator, 2026-08-02.

**RULE — Instructions are chunked and resumable, and each block states what it certifies.**
BECAUSE he must be able to stop after any block without losing the work already done.
EARNED-BY Operator, 2026-08-02.

**PREFERENCE — designs that remove dependencies on artifacts he may not have.** Recompute reviewer-side against whatever candle he read, not a specific pre-named one he must find.

### 1.3 Reporting methodology
**RULE — Major deliverables are zero-context plain-language explainers: they explain the project and every mechanism from scratch, define all jargon, state provenance per claim (verified / measured / expect / open), and end with an options menu plus reasoning.**
BECAUSE it lets him verify the work conceptually, without a programming background and while running other work in parallel, without holding full project context.
EARNED-BY Operator, ratified 2026-07-15.

### 1.4 Operator attention is the scarce resource
**RULE — Keep everything moving that can be moving: all independent workstreams run in parallel, always.**
BECAUSE builder idle time during reviewer↔operator sessions is a cost to design against, not absorb.
EARNED-BY Operator, 2026-07-29.

**RULE — Invocation convention for knowledge work: "Depth: `<topic>`" = one-theme deep pass or operator interview; "Breadth: `<domains>`" = wide search-enriched sweep with citations.**
BECAUSE the two produce different artifacts; the choice belongs to the asker.
EARNED-BY Claude-optimization track, 2026-08-03.

---

## §2 · PASTE LAW «NAIAD-S2-PASTE»

**WHO READS THIS: any lane drafting a paste, a go-paste or a queue contract, and the builder
executing one — for contract drafting, verification gates, and anything that touches this machine.**

### 2.0 Every paste explains itself, before it is run
**RULE — Before any code block, in plain language: (1) what this paste is for — why it exists, what problem or ruling it answers · (2) what each step does, numbered, one line each, in run order, saying *why* it is there and not only what it calls · (3) what you should see on screen, and what a failure looks like · (4) what changes on disk — which files are created, modified or moved, or the explicit words "read-only" if nothing changes.**
BECAUSE pastes here run to hundreds of lines of guarded edits, fixtures and publish steps, unreviewable unless something outside the block says what it means. **A paste the operator cannot evaluate is one he can only trust — and trust is not review.**
EARNED-BY Operator ruling 2026-08-04.

This sits alongside, not instead of, the routing line and the ROLLBACK line — three separate
things: **where** it goes, **what** it does, **how** to undo it.

**Narrow exception:** a one-line diagnostic the operator just asked for by name needs no preamble —
everything else does, read-only pastes included: "this only reads" is itself information he needs to
run it without worrying.

### 2.1 GEOGRAPHY — what is on this machine, and where
*(Data residency v2, operator ruling 2026-08-15. The identity gate in §0 enforces the first row of
this table; the rest is why.)*

| place | what it is |
|---|---|
| `~/Naiad` (= `/Users/luis/Naiad`) | **the working repo**, ~4.6 GB, outside every sync tree. Live working data — substrates, census outputs, new acquisitions — is born and read here. |
| `/Volumes/LaCie` | **backup only.** Bulk mirror plus the `naiad-backups` vault, Drive-mirrored to cloud. Reads never touch it in normal work. |
| GitHub `catpatrol/Naiad` via SSH | **the anchor.** Branch `v12-v1-census` carries all project work; the browser's default `main` view is why files look missing. |
| `~/venvs/naiad` | the venv — interpreter `~/venvs/naiad/bin/python`, Python 3.12.14 — **outside the repo and any synced tree.** A venv cannot be moved, only rebuilt; scheduled jobs call python by full path. |
| `~/.cache/naiad/data_cache` | the data estate. NOT in the repo, never synced. `$NAIAD_CACHE_DIR` overrides. |

Machine: MacBook Pro 16" M5, 48 GB, macOS, Terminal/zsh, native bash.

**RULE — The canonical READ path is repo-relative, anchored on `Path(__file__).resolve().parent.parent` — never an env-var root, never a drive letter.**
BECAUSE a drive letter is a fact about one machine, and this project has outlived one.
EARNED-BY Data residency v2, 2026-08-15.

**RULE — ZIP AGING: new archives are BORN LOCAL (`--phase`) and mirrored to the LaCie in the same act; older/completed zips live on the LaCie ONLY. The repo keeps the git-tracked `.sha256` sidecars and `POINTER.md` as the fingerprint set.**
BECAUSE `.gitignore` covers `*.zip` and not `*.sha256` — archive out of git, fingerprint in — so the repo can prove what an absent archive was without carrying it.
EARNED-BY Operator, 2026-08-15, refined same day. **Named cost:** the newest archives are LaCie-sole-copy until the Drive mirror syncs.

**RULE — `drive_wait` gates backup WRITES, not substrate reads.**
BECAUSE under v1 an absent drive meant unreadable data and a halted run; under v2 only an unwritable backup copy. Same helper, same three states, different blast radius. PRESENT answers in 0.00s; the 18s budget is the asleep case.
EARNED-BY Data residency v2, 2026-08-15.

**Why each side exists.** The marker side: **a cloud-synced tree corrupts bulk writes** — the sync
client rewrites, relocates and locks files underneath a run, so a bulk paste cannot trust that what
it reads back is what it wrote. The path side: a marker check alone passes any directory on the
machine. CL-2.

**Identity probe when unsure:** `git rev-parse --short HEAD; pwd`. **"Local" = any session whose
probe returns the `$HOME/Naiad` working-clone path** — desktop-app Code tab and terminal CLI both
qualify. **Cloud sessions** target `catpatrol/Naiad` only and must push in the SAME session, or the
work does not count (R-A').

### 2.2 Routing, rollback, and exact text
**RULE — Every paste-go carries an operator-facing routing line ABOVE the code block** — e.g. "→ WHERE TO PASTE: your LOCAL Claude Code — the terminal window on your Mac" — **or an explicit cloud target; an in-paste ENVIRONMENT header; and the hard environment assertion of §0.**
BECAUSE the operator routes by reading, not inferring.
EARNED-BY Standing; sides restated 2026-08-15. CL-2.

**RULE — Every paste-go states in one sentence exactly how to undo what it does — the command, or the plain statement that it cannot be undone.**
BECAUSE a paste that cannot state its own undo has not been thought through to the end.
EARNED-BY Adopted 2026-08-04 after four halts and one near-miss on irreversible deletion in eight days — CL-3.

Most repo edits roll back with `git checkout -- <paths>`; a pushed commit with `git revert <sha>`.
**Anything touching the data estate, an archive, or a deletion is not reversible and must say so in
those words**, so he reads the risk before running, not after.

**RULE — Any next steps a lane produces (commands, questions or instructions for the builder or the terminal) carry the EXACT paste-ready text in a code block — never a paraphrase, never a description of what to ask.**
BECAUSE the operator pastes and goes, with no reconstruction on his side.
EARNED-BY Ratified 2026-07-19. Applies to git commands, builder one-liner questions and contract go-pastes.

### 2.3 Write every gate from the POST-action state
**RULE — Simulate the paste's own steps in order, then write every verification gate against the state that will exist AFTER those steps run, not the state before.**
BECAUSE a gate written from the pre-paste state passes on the wrong evidence, and the paste reports success.
EARNED-BY Reviewer error taxonomy Class B (§6) — CL-4.

**RULE — A verification gate matches a distinctive FRAGMENT, case-insensitively — never a full sentence quoted from prose the same author is writing in the same act.**
BECAUSE content and its gate authored together get no second reading.
EARNED-BY 2026-08-04, from the halt behind the publish amendment — CL-13.

**RULE — Anchor context, rule D-4: any paste that edits this file prints at least 3 lines either side of every anchor BEFORE writing, and the build document shows what was printed.**
BECAUSE **an occurrence count is not a placement check.** Counting proves a string exists; only the surrounding lines prove it is the right place. Prefer a structural boundary (the `---` closing a section) over a prose fragment.
EARNED-BY Queue 003, ratified 2026-08-11, after three misses in three days, each passing its own guard — CL-5.

### 2.4 Shell hazards — each of these has cost a failed run
**RULE — Any path inside a bash block uses forward slashes.**
BECAUSE backslashes die in transit: the shell reads them as escapes.
EARNED-BY CL-13.

**RULE — `scripts/publish_exchange.py` is a LIBRARY with no `__main__` block. Call `publish()` exactly as written in §3; never run the module as a script.**
BECAUSE running it as a script publishes nothing and exits quietly — the worst failure shape available: the surrounding paste reports success.
EARNED-BY Two wrong forms shipped — CL-13.

**RULE — Any "run the script" instruction is checked against the module actually having an entry point before it ships.**
BECAUSE it is the general form of the rule above, and a Class A cure (§6).
EARNED-BY 2026-08-04.

**RULE — A status read through a pipe ending in a formatter always exits 0; capture grep's status directly.**
BECAUSE the pipeline reports the formatter's success, not the search result.
EARNED-BY Standing.

**RULE — Use Python-hashlib binary reads for byte questions.**
BECAUSE a text-mode read is the wrong instrument for a byte question on any platform. *(Original reason — msys `grep`/`sed` silently stripping CR — Windows-era, retired here.)*
EARNED-BY Claude-optimization track; reason retired 2026-08-15, rule unchanged.

**RULE — Three skill-embedded rules, binding on every paste: (1) ONE PASTE, COMPLETE MANIFEST — a paste that writes a set writes the whole set and lists it, never a partial set for a follow-up · (2) EXPLICIT DESTINATION FILENAMES — never leave a write to an inferred or defaulted path · (3) AUTHORIZATION BOUNDARIES — a paste does only what its contract authorizes; a lane needing more says so rather than taking it.**
BECAUSE a half-applied change is the state nobody verifies, an inferred destination is what the operator cannot check by reading, and the boundary holds only while written down (§6's counter-pattern depends on it).
EARNED-BY Claude-optimization track; carried by `naiad-custodian` and `naiad-daily-brief`.

> **NOTE 2026-08-15 — three Windows-era hazards are RETIRED here:** msys translation, the `chr(92)`
> backslash escape, and `PYTHONIOENCODING` (the venv's stdio is already `utf-8`). **NOT retired:**
> the `__main__`-less module rule and the Class B gate-fragment cure — neither depended on platform.

### 2.5 Design for autonomy
**RULE — Design any workflow needing lane↔builder coordination to optimise operator attention and Claude time: decision-tree contracts that execute autonomously until an operator decision is genuinely required, halting only on failures or true forks. At fork points, run the §1.1 interview.**
BECAUSE the alternative is a round trip per step, and the operator is the bottleneck in every one.
EARNED-BY Operator, 2026-07-27, extended 2026-07-29.

**RULE — Minimise screenshot-bridging: contracts instruct the builder to hand back machine-readable reports and artifacts into `exchange/`, plus STATUS blocks.**
BECAUSE the operator should move files, not photograph terminals.
EARNED-BY Operator, 2026-07-27.

---

## §3 · REPORTING «NAIAD-S3-REPORT»

**WHO READS THIS: HEPHAESTUS on every session, and every lane that commissions or receives a build
— for build documents, file disposition, publishing, and session close.**

### 3.1 The single build document
**RULE — Every builder session emits EXACTLY ONE document, written as a FILE and never a screen-only block, to `exchange/reports/BUILDERS_REPORT_<LANE>_<date>_<phase>.md`. It is standalone, readable with zero prior context, required at the end of any block of work and at interim stage boundaries when the block is very large.**
BECAUSE it serves two readers — the forensic record letting a run be re-derived or refuted, and the review artifact letting the operator and the Pantheon choose the next move. Proliferation was the problem, not content.
EARNED-BY Operator ruling 2026-08-04, replacing the former two-artifact rule, nothing dropped in the merge. Invariant 4.

**RULE — No exceptions, read-only sessions included. A reviewer paste may not waive this; an AFTER line saying "no document needed" is a drafting defect — refuse it.**
BECAUSE a measurement nobody can re-read will be re-run.
EARNED-BY Hardened 2026-08-11 by operator instruction — CL-6.

**RULE — Every build document ENDS by appending the session's STATUS entry to the commissioning lane's ledger (`exchange/status/LEDGER_<LANE>.md`) in the same session. The ledger line is a byproduct of the build document, never a separate chore.**
BECAUSE **a report without its ledger entry is an incomplete deliverable**, and it restores the inbox-acknowledgement test: acted = the recipient's ledger references the note.
EARNED-BY Ruling 'append', operator 2026-08-12; HERMES finding: five of six lane ledgers trailed their filed reports — CL-7.

**As the forensic record:** gate and probe values **as printed** · the full fixture transcript ·
**full result tables, not summaries** · versions, hashes, commits · findings **reported-not-fixed** ·
exact repo paths of every artifact · the file-disposition table.

**As the review artifact:** what was built and what it is for · what was decided and **on whose
authority** · what was found that changes the plan, especially findings reported-not-fixed and **any
operator ruling reinterpreted mid-build** · what remains open, **with its owner** · the honest next
options **with their implications**. Plain language, zero prior context, no jargon left undefined.

**RULE — A file never contains its own sha256.**
BECAUSE that row is stale the moment it is written.
EARNED-BY Standing.

### 3.2 The file-disposition table
**RULE — The document ENDS with a table covering every file the paste created, modified or moved.**
BECAUSE the operator must see at a glance where every artifact lives and whether losing the machine loses it. **Committed is not pushed. Pushed is not backed up.**
EARNED-BY Operator, 2026-08-02; BOX COST added 2026-08-06.

| column | content |
|---|---|
| PATH | full repo-relative path |
| EXISTS | on disk |
| TRACKED | tracked / untracked / ignored — and which `.gitignore` line if ignored |
| COMMITTED | which short SHA, or "not committed" |
| PUSHED | yes/no, plus the remote ref |
| PROTECTED BY | estate zip / phase archive / `--workflow` archive / GitHub only / **NOT PROTECTED** |
| **BOX COST** | bytes and % of the box for anything under `exchange/` or another synced path, **and FLAGGED if the file is over the trip-wire** — that flag, not the percentage, is what the rule below asks for. `n/a` if it lands somewhere unsynced — say which. Take both constants from `publish_exchange` (`BOX_BYTES`, `FLAG_BYTES`), never a copy. |

*(Seven columns. Ratified as "six columns, standing" 2026-08-02; BOX COST added 2026-08-06 without
updating the heading count — noted here, and the heading dropped, not carried as a second wrong
number.)*

**RULE — Creating a file that will enter the project-knowledge box is a WORKFLOW DECISION, not a side effect. Any box-bound file over 64,000 B is flagged to the operator by name, with its intended home, at the moment it is created. The wire is ABSOLUTE: it does NOT move with `BOX_BYTES`.**
BECAUSE the three web lanes reach repo content ONLY through that box, and creation is the only moment the choice is cheap. Absolute because the intent was a SENSITIVITY, not a proportion — what is worth a sentence at creation does not scale with the ceiling.
EARNED-BY Operator ruling 2026-08-06, after the box overflowed twice — CL-8; PINNED ABSOLUTE at 64,000 B by operator ruling "pin", 2026-08-15.

**The box is 16,000,000 B. Its thresholds are warn 0.40 / refuse 0.70** — 6.4 MB and 11.2 MB — **and
the guard governs on the TICK SET** (`exchange/` + `LEDGER.md`), not `exchange/` alone. Exactly the
refuse fraction WARNS; it does not refuse. Fixture **F-BOX-1** pins all of it. The capacity of
record is `publish_exchange.BOX_BYTES`, and the trip-wire of record is
`publish_exchange.FLAG_BYTES` — described here, not defined here. **Three limits look alike and are
not:** the 64,000 B trip-wire NAMES a file, the §4.2 1 MB cap REFUSES one, and warn/refuse govern
the whole tick set. Only the middle one is a limit.

> **CORRECTION 2026-08-15 (box governance, APOLLO → ATHENA).** This paragraph first read *"warn
> 25→50%, refuse 40→80%"*. Those were the raise's own first thresholds and they held for part of one
> day. Carried up proportionally from a 6.39 MB box, they put the first warning at 8 MB — the bus
> would have tripled with nothing said. ATHENA recalibrated to **0.40 / 0.70** on the governance
> transfer, and closed the D3 metering gap in the same change so the figure the thresholds read is
> the whole box rather than `exchange/` alone. Boundary semantics were preserved verbatim through
> both moves. The assertion above is rewritten rather than annotated, per the correction rule in §0.

> **CORRECTION 2026-08-15 (ruling "pin"). The trip-wire above read *"over ~1% of the budget"*.**
> A fraction moves with the ceiling, so the 6.39 MB → 16 MB raise loosened it from ~63,900 B to
> ~160,000 B — **a 2.5× loosening nobody separately asked for.** APOLLO flagged the consequence
> rather than burying it (*"each of this lane's last three build documents would have tripped the
> old wire and none trips the new one"*) and carried it to ATHENA as the one box question still
> open. The operator has now ruled: **pin it absolute at 64,000 B.** Measured 2026-08-15 on the
> tracked tick set — 7 files over the new wire, **the same 7** over the old ~63,900 B one, and just
> **1** over the raised ~160,000 B one, with no file at all in the 100 B gap between old and new. So
> this restores a sensitivity that had been all but switched off; it does not invent a limit. *(A
> snapshot of a moving quantity — the live count is printed on every publish.)* The rule is
> rewritten rather than annotated, per §0. The OPEN item it replaces is closed in `LEDGER_ATHENA.md`,
> which holds threshold custody and carried it — open items live in ledgers.
>
> **Named cost, stated because it is real:** the duty binds *at creation*, so it never binds a file
> that GREW across the wire — and three of the six are append-only files with no moment of creation
> at their current size. `publish()` therefore reads the wire again on every publish and names what
> is over it. Advisory: nothing is refused, and nothing on the bus today is in breach.

### 3.3 Publishing and the on-screen close
**RULE — The document is written into `exchange/reports/` with sha256 verified before and after; the paste then publishes `exchange/**` with the invocation below and states on screen whether the push SUCCEEDED.**
BECAUSE the operator needs to know whether to click Sync now. This is the ratified W1 Q-2 exception to commit-no-push.
EARNED-BY Standing.

**RULE — Never write "skip silently if absent". If a directory is missing, create it and say so.**
BECAUSE a silent skip is indistinguishable from success.
EARNED-BY Standing.

**RULE — On-screen output stays short and displays, in BRIGHT COLOURS, the exact filenames and full repo paths the operator must carry.**
BECAUSE he is the transport layer between six actors that cannot read each other.
EARNED-BY Operator, 2026-07-29.

### 3.4 The publish invocation — written out, because two wrong forms have shipped

    ~/venvs/naiad/bin/python -c "import sys; from pathlib import Path; R=Path('.').resolve(); sys.path.insert(0,str(R/'scripts')); import publish_exchange as p; r=p.publish(R,'<YYYY-MM-DD>'); print(r['status'], r['commit'], r['pushed'], r['offenders'])"

**RULE — `publish()` stages `exchange/**` only, guard-checks the whole index, commits and pushes. Do NOT `git add` or `git commit` exchange files separately — let the guard do it, so evidence cannot ride along.**
BECAUSE the guard's path scope is the mechanism keeping data off the auto-push.
EARNED-BY Standing.

**RULE — A `git add` of any file OUTSIDE `exchange/**` in the same paste goes nowhere and leaves it stranded as an uncommitted change. Commit non-exchange paths explicitly, in their own authorized commit.**
BECAUSE the guard's path scope cuts both ways.
EARNED-BY 2026-08-04 — CL-13.

### 3.5 Session close — the STATUS block
**RULE — End any MATERIAL session (phase registered or completed, ruling ratified, ledger entry, contract drafted, commit or push, acceptance, halt, incident, go-paste, fixtures reported) with a STATUS block: under 25 lines, no prose padding, machine-relayable.**
BECAUSE the operator relays these between lanes by hand; anything longer does not survive the trip.
EARNED-BY Standing; the two integers are ruling Q-8 A, tallied weekly by HERMES.

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

---

## §4 · BOX & DATA «NAIAD-S4-BOX»

**WHO READS THIS: every lane — for deciding where a file goes, whether another lane can see it, and
what may never enter the bus.**

### 4.1 The three surfaces
- **WEB CHATS** (APOLLO, ARGUS, ATHENA): share the box and project memory. Cannot read each other,
  touch the local disk, or run on a schedule. Box additions DO appear mid-conversation.
- **COWORK** (HERMES, DIONYSUS): read/list/write the mounted repo, run code in a Linux sandbox,
  write into the box. **No project memory.** Scheduled runs see the live folder but have **no network
  egress** and no OAuth connectors; **git availability is UNTESTED** — assume no commit, no push.
- **HEPHAESTUS** (local Claude Code at `~/Naiad`): the only actor touching the data estate.
  Commit-no-push by default; auto-push scoped to `exchange/**` only.

**RULE — No scheduled lane deletes anything — not files, not archives, not repo content. Deletion is an attended builder action with an operator decision behind it.**
BECAUSE it replaces a technical guardrail that did not hold, and **it holds regardless of any re-test** — the cost of being wrong is asymmetric.
EARNED-BY F4, 2026-08-02 — CL-14. Standing.

**Three accesses that are NOT the same:** (1) trusted Cowork folders reach Cowork lanes only ·
(2) a file dragged into a chat lives in that ONE conversation, never enters the box, costs
nothing permanent · (3) project knowledge / GitHub sync is the only path reaching every web lane.

### 4.2 The exchange bus
**RULE — All six actors exchange files through `exchange/` and no other route.**
BECAUSE chats cannot read each other; the bus, the box and operator-relayed STATUS blocks are the only channels.
EARNED-BY Operator ruling, 2026-08-03.

```
exchange/
├── DIGEST.md        RETIRED 2026-08-15 — a tombstone; its source list is inside
├── status/          LEDGER_<LANE>.md · MANIFEST.json · CADENCE.md · RETENTION.md ·
│                    HEARTBEAT.md · SECOND_ACCOUNT.md · CONVENTIONS.md · daily/
├── queue/           numbered builder work orders; each a FULL contract with a RATIFIED stamp
├── reports/         every builder and lane report
└── drops/           raw operator inbox
```

**RULE — Content guard: text only, 1 MB per file. Larger artifacts are referenced by path + sha256 pointer, never copied in. Captures and renders go to `briefs/`; study artifacts to `research_outputs/`; local working files to `_reviewer_box/`.**
BECAUSE **DOCUMENTS ARE CHEAP, DATA IS NOT** — two capture JSONs outweighed a lane's written history five to one. **So write more reports, never fewer.**
EARNED-BY Confirmed three separate times — CL-9. Invariant 3.

**RULE — A per-file size limit does not bound a folder. Budget the TOTAL, not the item.**
BECAUSE `exchange/` hit 51% of the box while nine of its ten data files sat individually under the 1 MB cap — one breach, nine compliant, half the box gone.
EARNED-BY CL-12.

**RULE — Archiving is not a fix.**
BECAUSE two captures moved 2026-08-06 from `exchange/reports/` to `docs/history/argus/` were still retrieved from the box at their NEW paths — both folders sit in the sync selection. Reading surface fell 85%. Box consumption fell by zero.
EARNED-BY CL-10.

**RULE — Threshold custody is ATHENA's. The box ceiling, the warn/refuse fractions, the metered set and the naming trip-wire change ATHENA-first; the operator's word comes through her; no lane edits `publish_exchange.BOX_BYTES` / `WARN_FRACTION` / `REFUSE_FRACTION` / `TICK_EXTRA` / `FLAG_BYTES` on its own authority, and any such change runs the named-constant protocol (§6).**
BECAUSE one constant with five dependents is the shape that goes stale silently.
EARNED-BY APOLLO → ATHENA box-governance handoff, 2026-08-15.

**Named exception (2026-08-12, drafted ATHENA on the HERMES recommendation; operator may veto):**
`exchange/status/MANIFEST.json` and `daily/MANIFEST_*.json` are data by type but bus-resident by
PURPOSE — read off the bus, each under 0.5% of the box, series capped by the rolling window. The
text-only rule does not apply. **A rule in permanent technical breach stops being
enforced**; the exception keeps the rule sharp everywhere else. Nothing else inherits it.

### 4.3 The tick set, and confirming a file is visible
**RULE — The standing tick set is `LEDGER.md` and `exchange/` ONLY. Every other file is requested per lane, per need — dragged into that one conversation at zero permanent cost.**
BECAUSE it works only while something says what is there: **a lane cannot request a file it does not know about.** Since ruling 007 that is the bus-health block — per-folder counts and bytes on every publish and in `daily/DAILY_<date>.md` §8 — measured rather than maintained by hand. **Named cost:** it reports the SHAPE of the bus, not a filename list, so a lane hunting a specific file still asks the operator.
EARNED-BY Operator, 2026-08-06.

**RULE — The box is in SEARCH MODE: synced repo files are indexed for retrieval, NOT mounted as browsable files. Test visibility with the project-knowledge search tool, never a directory listing. A file is confirmed synced only when a search returns it WITH a folder path.**
BECAUSE listing the mounted project directory shows only hand-uploads and makes a working sync look broken. **A bare filename proves nothing** — hand-uploads are flattened (`.gitignore` → `_gitignore`; `v1.1` → `v1_1`), so a bare name may be the upload itself.
EARNED-BY Rule added 2026-08-03.

> **CORRECTION 2026-08-06 (finding H-1, raised by HERMES).** This passage previously carried a
> 2026-08-03 measurement — "the sync reaches `exchange/`, `docs/`, `prompts/`" — superseded by the
> 2026-08-06 tick ruling and never rewritten. For two days the file asserted both, and the two imply
> box occupancy of 21.2% and 109.7%. Not a competing rule: a stale fact stated as a current one —
> the exact failure this file names, committed inside the file that names it.

**What a web lane must DISCOVER belongs under `exchange/`; what it only needs to READ, the
operator drags into that one conversation.**

### 4.4 Determinism reruns
**RULE — R3: a rerun exists to prove byte-identity, and the hash IS that proof. Print both digests in the build document, then delete the rerun copy in the same session. Every study contract inherits this clause.**
BECAUSE three retained `_run2` trees held ~3.2 GB of redundancy.
EARNED-BY Operator, 2026-08-11 — CL-15.

**RULE — Refinement D-3: discard the DATA, keep the PROVENANCE. "Delete the rerun copy" means its data files only; RETAIN its run manifests and logs — KB-scale — beside the build document or inside the phase archive.**
BECAUSE they are the second run's provenance and all a discard costs: on `seq8_run2`, the 1783.5 MB of data was redundant; the few KB recording what run 2 did was not.
EARNED-BY Queue 003, ratified 2026-08-11 — CL-16.

---

## §5 · LANE CHARTERS «NAIAD-S5-LANES»

**WHO READS THIS: every lane, once — for knowing what is yours, what is someone else's, and which
sections of this file you are expected to have read.**

| lane | surface | charter | reads |
|---|---|---|---|
| **APOLLO** | web chat | SSv12, census programme, Tier-C runs, Engine V2, SSv12 Pine indicator | §0 · §1 · §2 · §6 · **§7** |
| **ARGUS** | web chat | analytics toolkit, daily brief, volume filter (charter, 5.1) | §0 · §1 · §2 · §6 · **§7** |
| **ATHENA** | web chat | system resilience and sustainability: repo operations, integrity, backups, manifest ritual, scheduled routines, workflow design, context compaction. Inherits the old SYSTEM lane; holds threshold custody. | §0 · §1 · §2 · §4 · §6 · **§8** |
| **DIONYSUS** | Cowork | independent creative critique | §0 · §6 · **§7** |
| **HERMES** | Cowork | **DORMANT** (2026-08-15, ruling 007) — coordination and verification; duties absorbed or parked, see below | §0 · §3 · §4 · §5 |
| **HEPHAESTUS** | local Claude Code | the builder | §0 · §2 · **§3** · §6 · §8, plus §7 for study work |

**HERMES IS DORMANT — 2026-08-15, ruling 007.** Five duties are now discharged by something that reports itself: **budget** → printed on every publish · **queue validation** → manifest counters and RATIFIED stamps · **staleness** → F-P6 and the bus-health block · **inbox** → ledger appends, since acted means the recipient's ledger cites the note · **`DIGEST.md`** → retired to `docs/history/DIGEST_RETIRED_2026-08-15.md`.
**Two are PARKED, not absorbed, and are named rather than quietly dropped:** *filing `drops/`* — nothing now names and files what the operator leaves in `exchange/drops/`; and *the queue-003 unacted-inbox list*, whose only home was the DIGEST, so `rotate_reports.py` HALTS rather than guess (§4.3). Both are operator calls.
**Revival condition:** cross-lane coordination pain that a script cannot measure. Until then nothing waits on HERMES, and the rule below still binds any lane that takes the role.

**RULE — DIONYSUS's challenges are NON-BLOCKING; a written answer is owed by the next phase boundary.**
BECAUSE critique that blocks becomes critique avoided.
EARNED-BY Ruling Q-7 A.

**RULE — HERMES never re-authors another lane's content and never instructs a lane without the operator's ratification stamp.**
BECAUSE a verifier who re-authors is not verifying — the HELIOS tripwire.
EARNED-BY Standing. HERMES never self-verifies.

**RULE — Queue drafting rights: APOLLO, ATHENA and ARGUS may draft builder work orders. DIONYSUS and HERMES may not — they critique and verify. Every item is a full contract carrying the operator's RATIFIED stamp before HEPHAESTUS works it.**
BECAUSE separating commissioning from verifying is the only independent check in the stack.
EARNED-BY Ruling Q-5, 2026-08-02.

**RULE — Lane attribution is by CONTENT, not chat title. Flag it when emitting so events get filed correctly.**
BECAUSE the operator runs lanes from whichever window is open.
EARNED-BY Standing.

**RULE — The status layer of record is `exchange/status/LEDGER_<GOD>.md`, append-only: a correction is a NEW entry. Lane state never returns to shared memory — it lives in the per-lane ledgers, read at session start.**
BECAUSE shared memory is capped; lane state crowds out identity and standing rules for lanes that do not need it.
EARNED-BY Rulings 2026-08-01/02; memory synthesis guidance, operator 2026-08-11.

### 5.1 The ARGUS lane
*(Operator-ratified 2026-07-27.)*

**Purpose.** The operator's discretionary method has a **mechanical half** (where levels are, which
tools agree at each price, regime per timeframe, funding/OI posture) and a **judgment half** (what it
means, whether to take it, what would prove him wrong). **The brief automates the mechanical half
only.** Four objectives, in order:

1. **SERVE THE TRADE.** Reproduce his manual review's grammar: every layer produces levels → levels
   earn authority by multi-tool confluence → output collapses to two lines-in-the-sand per asset
   plus if-then hypotheses. **Analysis is never an end in itself.**
2. **BUILD A COMPOUNDING RECORD.** Identical printed rules every day make captures comparable across
   months. Each capture is self-describing — rule set, `rules_version`, the sha that produced it.
   **JSON is the record; HTML is a disposable regenerable view.**
3. **FEED NAIAD THROUGH THE CORRECT DOOR ONLY.** The archive is a hypothesis mine and the proving
   ground where shared measurement tools are stress-tested by daily use — a bug hiding in a study
   batch job surfaces in a week when read every morning. **It is NEVER evidence.**
4. **FORCE TACIT SKILL INTO EXPLICIT RULES.** Automating forces stating what counts as a level, how
   close is the same level, what makes one area stronger — the mechanism that made Secret Sauce a
   Pine script and then a replay engine.

**Governing tension:** the brief's live/lockbox-era data is legitimate for ops, forbidden as
evidence. The confluence engine is the sharpest edge: a high-scoring area **feels** like a discovery
when it only states that tools agree. Whether agreement predicts anything is a study question
(CCL / CENSUS-2), answerable only on exploration-classic data under G-7.

**RULE — Every ARGUS feature fact carries its firewall side: display-only vs evidence. The LIVE-DATA FIREWALL on the brief is standing — an ops artifact, never study evidence, no journal reads, no lockbox outcome stats.**
BECAUSE the brief reads data that would contaminate any study it touched.
EARNED-BY Operator-ratified 2026-07-27; firewall from the Claude-optimization track.

**Labour division.** Operator = judgment, all merges, all gate decisions, position file and journal
notes, TradingView parity readings. Reviewer = specification, contracts, independent acceptance,
falsification on record, plain-language interviews at true forks. Builder = execution, fixtures,
commit-no-push.

---

## §6 · ERROR TAXONOMY & PROTOCOLS «NAIAD-S6-ERRORS»

**WHO READS THIS: reviewer lanes drafting contracts, and the builder verifying them — for
provenance, contract basis, and any change to a named constant.**

### 6.1 Provenance tags — load-bearing
`[verified]` = computed or read **this session** · `[ledger]` = in the committed ledger ·
`[ratified]` = an operator decision on record · `[operator]` = operator-reported, not independently
checked · `[handoff]` = builder-reported · `[open]` = undetermined.

**RULE — An operator-reported fact is never `[verified]`.**
BECAUSE that exact confusion produced a logged error on 2026-07-28.
EARNED-BY Standing — CL-17.

### 6.2 The reviewer error taxonomy
*(Three classes. The reviewer's mistakes are almost never analytical.)*

**Class A · machinery-content** — asserting what code, data or memory contains without reading it.
**Class B · post-action-state** — writing a gate from the state before the paste's own steps run.
**Class C · provenance** — promoting an operator or builder report to `[verified]`.

**RULE — Class A cure: any §Basis claim cites a file actually read this session. The memory panel counts as a file — call the view.**
BECAUSE injected text does not feel like a file. It is one.
EARNED-BY Strengthened 2026-08-04 after a fifth instance.

**RULE — Before claiming something lives ONLY in place P, enumerate every place it could live and check each. To claim a thing does not exist, ENUMERATE the set.**
BECAUSE a negative from one lookup measures that lookup, not absence.
EARNED-BY 2026-08-04 — CL-19. Invariant 6.

**RULE — A claim repeated across documents is not a claim verified. Corroboration requires independent measurement, not restatement.**
BECAUSE three documents said the `--workflow` trigger was armed; each copied the one before.
EARNED-BY 2026-08-04 — CL-18.

**RULE — Class B cure: §2.3. Class C cure: the tags in 6.1.**

**The counter-pattern:** the builder has refused reviewer instructions on ratified invariants
nine-plus times. **A stack whose executor never pushes back is a stack whose reviewer errors all
land.** CL-20.

> **CORRECTION 2026-08-15 — the count, and that it changed.** This read *"at least six times"* until
> today, while project memory's copy said *"nine-plus"*. **One fact, two homes, two values** — what
> the collapse exists to prevent, caught by an adversarial checker, not by the rewrite that carried
> it. The later figure is adopted; CL-20 keeps "six" verbatim as the pre-collapse record.

### 6.3 The context-gap audit
**RULE — Periodically — roughly once or twice a day, and ALWAYS at the start of a session or a new phase — audit whether the project has produced files the reviewer cannot access, and judge which would improve reasoning or context. This runs DURING contract drafting, not after.**
BECAUSE it is the Class A cure, and Class A errors are committed while drafting.
EARNED-BY Ratified 2026-07-25; moved into drafting 2026-08-04.

**Method:** grep the ledger, contracts and in-box scripts for referenced repo paths and import
statements; diff against what is reachable; rank gaps by which upcoming artifact each unblocks.
If gaps matter, ask the operator to make them reachable or issue an exact paste-ready builder
instruction (§2.2).

**Binding consequence: any contract §Basis claim must cite a file actually read this session.**
Precedent CL-25 — the audit that added the engine package and produced two material corrections.

### 6.4 The named-constant change protocol
*(Adopted 2026-08-15, credited APOLLO handoff §1.4. It sits here as a Class A cure: asserting a
change is complete without reading everywhere it lands.)*

**RULE — Changing any named constant requires all three of: (1) grep the NAME, the VALUE, and the THRESHOLD TEXT · (2) list every dependent with a pin-vs-import decision recorded per site · (3) a historical report reproduces history — regenerators of already-filed documents stay PINNED and labelled historical, live consumers IMPORT from the one definition.**
BECAUSE a name-only grep reports a false clean sweep: of five sites depending on `BOX_BYTES`, two contained no `BOX_BYTES` string at all. And importing a live constant into a historical regenerator restates a filed record against a value that did not exist when written.
EARNED-BY The BOX_CAPACITY incident, 2026-08-15 — CL-21. **Exemplar, both halves — CL-22:** `scripts/mc1_report.py:25` (pinned + labelled) versus `scripts/census2b_report.py` (now imports).

**RULE — Corollary: after editing a document, RE-READ THE DOCUMENT.**
BECAUSE grepping for a value finds values — not a claim that *contradicts* it 26 lines below, an ownership row a ruling has just closed, or a second stale figure further down the same file. All three happened; adversarial verification caught them, not the sweep.
EARNED-BY Same day, from the sweep's own three defects — CL-23.

**This protocol governed the session that adopted it** — the 2026-08-15 threshold recalibration ran
its own three legs; dependents table in
`BUILDERS_REPORT_HEPHAESTUS_2026-08-15_BOX-GOVERNANCE.md`. CL-24.

---

## §7 · STANDING STUDY FRAMES «NAIAD-S7-FRAMES»

**WHO READS THIS: APOLLO, ARGUS, DIONYSUS and HEPHAESTUS on study work — for any census, contract,
engine change or analysis. These frames are inputs to a study, never conclusions of one.**

*New to this file 2026-08-15: these frames sat in project memory, which does not reach Cowork or
the builder — HEPHAESTUS and the Cowork lanes inherit them here.*

### 7.1 The guiding attitude
**RULE — "The alpha is buried under a pile of debris." Stay with underperforming mandates — turn the problem until the mechanism is apparent, then fix it. Never retire one early.**
BECAUSE an underperforming mandate has told you something; retiring it discards the finding.
EARNED-BY Operator, ratified 2026-07-15.

**RULE — Priority order: better trade-birth filters → effective stop ratchet → take-profit that keeps profit. No restructuring around fees or execution before the strategy shows demonstrable edge.**
BECAUSE cost engineering on a system without edge optimises the wrong term.
EARNED-BY Operator, ratified 2026-07-15.

### 7.2 The fractal lens
**RULE — Price structure may replicate across timeframes with scale-adapted variables; never treat cross-TF signals or outcomes as different animals by default. Study the correlations explicitly and falsifiably.**
BECAUSE either default assumption is untested; this one is at least productive.
EARNED-BY Operator, 2026-07-18, standing analytic frame.

**Working hypothesis:** GROSS behaviour is fractal-compatible, NET is not — costs are scale-invariant
in bps while excursions scale with TF.

**RULE — All MTF tables print absolute AND governor-relative coordinates.**
BECAUSE FH-3 is CONFIRMED RELATIVE: all cross-TF rules are in governor-relative steps.
EARNED-BY Fractal programme; TC-5 confirmed the mechanical fractal and falsified the economic claim — **entries are floored at 5m PERMANENTLY.**

### 7.3 Research inversion — ratified "forensics"
**RULE — Condition on outcome, discriminate at birth.**
BECAUSE the loser book is TWO species with opposite cures: born-dead births → entry gates; died-of-neglect +1R round-trips → harvest fixes; one cure for both makes each worse.
EARNED-BY Ratified as "forensics"; census-2A structural finding.

### 7.4 The discriminant frame and the tail-retention gauge
**RULE — Mandatory census deliverables: decision-curtain-clean · five-asset sign-replicated · held-in-time stable · BH-FDR q=0.10. The TRG is printed beside strip-best.**
BECAUSE without all four a result is a number, not a finding — and the panel votes together (return correlation 0.6458, sign-agreement 0.60): **five witnesses ≈ one.**
EARNED-BY Standing census requirement.

### 7.5 The machinery frame
**RULE — `MTF_SET = {5m, 1h, 4h, 12h}`. The engine has NO 1D and NO 30m anywhere.**
BECAUSE `INTERVAL_MS` / `MTF_SET` stop at 12h, so a graduation basis of "robust on 12h/1d" was half un-representable, narrowed to 12H/position primary + 4H/swing secondary; the census's "governor lens" is a **measurement frame**, NOT the engine's per-cell `tf_gov`.
EARNED-BY Read from `engine/cells.py`, 2026-07-25 — CL-25.

**RULE — Completion commits reproduce the run from a clean checkout.**
BECAUSE a run not reproducible from its commit is not evidence.
EARNED-BY Standing.

### 7.6 The EMA family — the 500 amendment
**RULE — The observed EMA family gains the 500, with ±n×ATR cushion grammar, across all future Naiad instruments and contracts.**
BECAUSE if the 450 clips as a ratchet reference, the 500 may be the efficient one.
EARNED-BY Operator, 2026-08-12, verbatim "PLEASE REMEMBER THROUGH THIS LANE".

**Warmup (SEQ8 rule, ~1,731 bars):** trivial ≤4h · 12h warms ~2022 · 1d evidence-side warms only
weeks before the 2024-07-01 ceiling (marginal) · 1d ops-side fine · **1W/1M never.**

**RULE — Pairs discipline: primary = price↔500 interactions plus the 450/500 ribbon spread. The full cross-pair set is ANNEX-ONLY.**
BECAUSE the combinatorics are otherwise unbounded.
EARNED-BY Operator, 2026-08-12.

### 7.7 What a prior conclusion is, and what sizing is not
**RULE — Prior conclusions are points of control, never mandatory design constraints.**
BECAUSE a finding hardened into a constraint stops being falsifiable, and this spine is built to be falsified.
EARNED-BY Rulings 2026-08-03.

**RULE — Sizing is deferred post-TC-1. When it arrives it is count-based tiers, never fitted weights.**
BECAUSE the incumbent loser decile turned out to be a position-size selector (97.5% size-0.5).
EARNED-BY Census-2A structural finding.

**FALSIFIED, never re-assert:** the two-line exit architecture (S-2 — the native ratchet fires first
and the trail clips engaged winners).

*Full verdicts, yields and the next-cycle slate: `LEDGER.md` → **STANDING VERDICTS**. Definitions,
THE PATH and the MC programme: `exchange/reports/SS_SYSTEM_SYNTHESIS_2026-08-06.md`.*

### 7.8 Standing analytical principles
**RULE — Analysis always runs HTF→LTF: trend tier 1D/1W/1M, build tier 12H–5m. Every LTF structure is stamped with its HTF enclosure state.**
BECAUSE a 5m "range" may be one 4H wick, and read without its enclosure it is a different object than it appears.
EARNED-BY SS interview rulings, 2026-08-03.

**RULE — Signals are developing RELATIONSHIPS (price↔EMA, EMA↔EMA) — episodes plus events, never instants.**
BECAUSE an instantaneous reading discards the approach, where the information is.
EARNED-BY Same.

**Carried backlogs are lane state and live where §5 says:** APOLLO's SS Pine backlog (**B-1** SWING
MODE, **B-3** SSv11.3 glyphs) and the locked **SS interview rulings Q1c–Q11** are in
`exchange/status/LEDGER_APOLLO.md`, on the bus, read at that lane's session start; verbatim rulings
in `docs/memory/claude_project_memory_2026-08-03.md`, Entry 19. *(Relocated 2026-08-15 — one lane's
TODO list should not sit in the file all six actors read.)*

---

## §8 · PROTECTION «NAIAD-S8-BACKUP»

**WHO READS THIS: ATHENA and HEPHAESTUS — for backups, integrity, archives, deletions and the data
estate.**

### 8.1 The two invariants that govern everything here
**RULE — SYNC IS NOT BACKUP.**
BECAUSE sync propagates deletions faithfully.
EARNED-BY Standing. Invariant 1.

**RULE — EXISTENCE IS NOT PROTECTION. Before removing any file because a copy exists elsewhere, verify the copy is TRACKED and present on the REMOTE. Three checks, all of them, none assumed:**

1. `git ls-files --error-unmatch <twin>` — is it tracked at all?
2. `git cat-file -e origin/v12-v1-census:<twin>` — is it on the remote?
3. `git hash-object <twin>` against the committed blob — is the worktree copy the committed one?

BECAUSE **a path proves nothing about surviving this machine.** Some directories are git-ignored *on purpose*, per `.gitignore` — `_reviewer_box/`, `research_outputs/brief/`. A duplicate living only there is not a backup, just a second copy on the same disk.
EARNED-BY Rule added 2026-08-04 — CL-11. Invariant 2.

### 8.2 The three tiers
- **Tier 1 · data** — `~/.cache/naiad/data_cache` (macOS), via `engine/data.py` `cache_dir()`. NOT in
  the repo, never synced. Vault: `/Volumes/LaCie/naiad-backups`, Drive-mirrored to cloud.
- **Tier 2 · repo** — GitHub `catpatrol/Naiad` for everything tracked. **Phase archives are PERMANENT
  EVIDENCE, never prunable**; the repo keeps the tracked `.sha256` sidecars + `POINTER.md`.
- **Tier 3 · AI state** — `docs/memory/` snapshots are the restore path. **Import is lossy, and a
  global "Reset memory" deletes project memories irreversibly.**

**RULE — REGISTERED IS NOT UPLOADED. A folder registered with a cloud mirror is not evidence that anything reached the cloud; treat an off-site copy as UNCONFIRMED until the destination itself is checked.**
BECAUSE a mirror verified as *registered* by decoding the sync client's own configuration was erroring 50 times over on these very archives, with no upload-completion record in its logs.
EARNED-BY Measured 2026-08-12 — CL-27. Invariant 1 at its sharpest: configured correctly, holding nothing.

### 8.3 The backup verification standard — binding on every backup job
**RULE — Bidirectional per member: bytes re-read OUT of the archive hash equal to a fresh read of the source · set membership cross-checked archive/manifest/disk · archive re-read FROM the destination after write · no-clobber guard.**
BECAUSE an archive not read back is an assertion, not a backup.
EARNED-BY Standing, state verified 2026-08-04/05, guards live 2026-08-11.

**RULE — Restore case-sensitively: `MANIFEST.json` and `manifest.json` silently clobber on a case-insensitive filesystem, and the collision carries to APFS.**
BECAUSE `zipfile.read()` returns the LAST member of a name collision, so a verifier compares the wrong file and reports a name collapse as a mismatch.
EARNED-BY Restore hazard, measured.

### 8.4 The infrastructure inventory
**RULE — Refresh this inventory from `exchange/status/MANIFEST.json` rather than re-deriving it.**
BECAUSE re-deriving produces a second answer that will disagree somewhere.
EARNED-BY Standing. Verbatim history: `docs/memory/claude_project_memory_2026-08-03.md`, Entry 25.

**Scripts, all under `scripts/`:** `reviewer_manifest.py` v1.1 · `daily_brief.py` (F-B1..8, LIVE-DATA
FIREWALL) · `daily_routine.py` + `routine_jobs.json` (a config-driven **job registry** — new jobs by
editing JSON, never code) · `backup_estate.py` (`--estate --phase --verify --workflow`; deletion
opt-in behind `--delete-source`, never touches the estate) · `publish_exchange.py` (the path-scoped
guard, so evidence cannot ride an auto-push). Skills: `naiad-custodian`,
`naiad-daily-brief`.

**Triggers ARMED — three launchd agents, enumerated from `launchctl print`, not inferred:**
`com.naiad.daily` (07:00 daily, `daily_routine.py`) · `com.naiad.estate` (Sun 08:00,
`backup_estate.py --estate`) · `com.naiad.workflow` (Sun 08:30, `--workflow`), bootstrapped into
`gui/501`; a missed calendar job runs at next wake, launchd's default. **NOT ARMED:** no HERMES task,
pending the operator. **Manual BY DESIGN:** Sync now. Registry and `bootout` lines: `CADENCE.md`.
*(The Windows Task Scheduler enumeration is retired; its prerequisite defect is CL-26 — it would have
broken every daily run silently.)*

**RULE — `--estate` and `--workflow` write to `/Volumes/LaCie/naiad-backups`. `--phase` is SEPARATE: phase zips are WORKING COPIES living in the repo at `~/Naiad/research_outputs/_archive` (see that folder's `POINTER.md`), backed up to the LaCie beside the rest.**
BECAUSE the two were conflated once already; recording the destination here lets a lane read it without querying a scheduler.
EARNED-BY Data residency v2, 2026-08-15.

**Destination precedence, highest first: an explicit `--dest` · `$NAIAD_BACKUP_DEST` ·
`BACKUP_DEST_DEFAULT`.** The default is `/Volumes/LaCie/naiad-backups` and is CORRECT — read from
`scripts/backup_estate.py:328` this session. **Pass no `--dest` unless you mean to override it.**

> **CORRECTION 2026-08-15 — this asserted the opposite, and the old text was dangerous.** It read:
> *"`BACKUP_DEST_DEFAULT` … was still the Windows-era `D:/naiad-backups` … every v2 backup must pass
> `--dest` or `$NAIAD_BACKUP_DEST` explicitly."* True when written, **now false**: the constant was
> retargeted the same day (`AMENDED 2026-08-15 (v2)`, same disk, new address). Worse than wrong — an
> explicit `--dest` **outranks** the default, so obeying it re-enables the very override that kept
> the Sunday runs writing to a dead Google Drive path (**CL-27**). Rewritten, not annotated, per §0.
> *Windows-era destination history is kept as migration evidence in CL-27, not deleted.*


---

## MAINTENANCE — step by step, plain language

**RULE — A rule with no probe coverage is a rule on trust. Name the uncovered ones rather than implying all are checked.**
BECAUSE rules covered only by operator inspection are ones you notice if a lane drops them — its own detection, but an argument, not an assumption.
EARNED-BY Memory-restructure acceptance, 2026-08-03. **Pass requires ≥5 of 6 behaviours, and B6 — did the session consult this file — must be among them; if B6 fails the pointer failed and the restructure is reconsidered.** Probes: `ACCEPTANCE_MEMORY-RESTRUCTURE_2026-08-03.md`. Relocation register: the ANNEX in `docs/CASELAW.md`. Fixtures: `scripts/fixtures_conventions.py`. Census: `docs/CONVENTIONS_RULE_CENSUS_2026-08-15.md`.


**Who does what.** ATHENA drafts every change. You ratify it. HEPHAESTUS writes and publishes it.
Staleness is flagged by the bus-health block, not by a lane (ruling 007). Nobody else edits this file.

**To change a rule:**

1. **Say what you want changed**, in any chat. ATHENA finds the section and drafts the new wording.
2. **ATHENA shows you a before/after** — old text, new text, and what behaviour changes.
3. **You approve or amend.** One word is enough.
4. **ATHENA issues a paste** that edits this file, rewrites every place asserting the old fact, and
   appends a dated note saying what changed and when. Nothing is silently rewritten.
5. **You run the paste.** The screen tells you `PUSH SUCCEEDED` or `PUSH FAILED`.
6. **You click Sync now** in the project settings. This is what makes the change visible to APOLLO,
   ARGUS and ATHENA. Until you click it, they read the old version.
7. **ATHENA confirms** by searching for this file and checking the new text is there.

**Nothing here requires you to edit a file by hand.** If a paste asks you to, that is a drafting
mistake — say so.

**Adding or moving a section** re-runs all four F-CONV fixtures: every token appears exactly twice
(INDEX row + section header), §0 stays under 6,000 bytes, memory-pointer tokens resolve, no rule is
lost. They keep the collapse from silently un-collapsing.

**Audited** at every phase boundary, with the project-memory audit: ATHENA re-reads it against the
live memory panel, reports drift, and regenerates the snapshot under `docs/memory/`.

**If a lane ignores a rule in here:** that is a finding, not a nuisance. Tell ATHENA which rule and
which lane. The likely cause is that the pointer or session-start ritual failed, and the remedy is
the **FAIL protocol: the rule comes back to project memory rather than being repeated at the lane.**
A rule re-taught every session is a rule in the wrong surface.

---

*Ends. Corrections append below this line with a date and the section they amend.*
