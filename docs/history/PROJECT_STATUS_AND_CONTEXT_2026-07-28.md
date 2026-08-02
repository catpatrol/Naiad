# Project Naiad — Status & Context
### For the ORCHESTRATOR chat and the operator · 2026-07-28
**Covers: what has been done · where we are going · what is in the pipeline · distance to objectives · the standing subjects of optimization, workflow efficiency and resiliency · and the methodology by which chats communicate**

**Provenance tags, and they are load-bearing.** `[verified]` = computed or read from source by the reviewer in session · `[ledger]` = recorded in the committed ledger · `[ratified]` = operator decision on the record · `[operator]` = operator-reported, not independently checked · `[open]` = undetermined. **An operator-reported fact is never `[verified]`.** That exact confusion produced an error on 2026-07-28 (§12).

---

## 1. What the project is, for a reader with no context

Ludwig trades crypto perpetual futures discretionarily, guided by a TradingView indicator he wrote called **Secret Sauce Cascade**. **Project Naiad** is the effort to convert that discretionary skill into a mechanical system that can be tested honestly — not to prove it works, but to find out whether it does.

The mechanism in one sentence: after a confirmed 9/89 EMA cross on a slower *governor* timeframe sets trend direction, pullbacks into zones drawn from that governor's own EMAs get absorbed by trend participants, so a faster *execution* timeframe reclaim inside such a zone should carry positive expectancy net of costs.

Ten Binance USDT-M perpetuals × three mandates (swing 4H/5m, intraday 1H/1m, position 12H/15m) = a **30-cell pre-registered grid**, replayed by a Python engine that ports the Pine logic. History is partitioned: **exploration-classic** (through 2024-06-30) is free to mine; the **lockbox** (2024-07 → 2025-10) is sealed. Looking at the lockbox is irreversible — evidence spent cannot be unspent.

**The people.** Ludwig is the operator: no programming background, owns every merge and gate decision, answers in one-word rulings. Claude Code (local Windows) is the builder: executes contracts literally and has repeatedly caught reviewer errors. Four Claude chats are the reviewer, split by lane.

**The discipline.** Every headline recomputed from raw artifacts before acceptance · predictions pre-registered with explicit probabilities before investigation · falsification treated as a deliverable, not a failure · an append-only ledger · byte-identity enforced by numbered fixtures · nothing merges without operator sign-off.

**The three work tiers.** Tier A: arithmetic on data already on disk, free, no pre-registration. Tier B: new measurement with trading logic unchanged, byte-identity enforced. Tier C: an actual rule change, which **must** be pre-registered under rule G-7 — a ledger entry with config hash, hypothesis and numeric prediction — *before* it runs.

---

## 2. Where we stand — the honest one-paragraph version

The study has found **one architecture that is positive and robust** (the structural stop, +565.58 grid / +301.99 strip-best) and has **falsified more than it has confirmed** — which is the process working. Three mechanisms remain open: entry admission, the add gate, and take-profit. **Take-profit has no candidate mechanism at all**, and it is the operator's stated priority #3. Meanwhile the infrastructure that makes any of this trustworthy went from nothing to near-complete in three days: manifest, daily brief, daily routine and backup are all built and accepted; only the scheduler trigger is missing. The irreplaceable data, which was discovered to have **never** been backed up, now has three offsite copies. The operator's attention cost per session is measurably falling but is not yet where it should be.

---

## 3. What we have done

### 3.1 The study lane (chronological, each a completed phase)

| Phase | Result |
|---|---|
| **V3 anchor** | The faithful mechanical port lost heavily: grid −5,756.91 cell-R at 1× costs, all 20 cells negative, median harvest captured 6% of peak favourable move `[ledger]` |
| **PROTECTED paradox** | 90.35% of trades reaching +1R favourable excursion still exited at a gross loss, with zero stop advances before the peak. **The exit machinery, not entry quality, is the primary failure** `[ledger]` |
| **S-2 / S-2b** | The **structural stop** — anchor beyond a real 1-hour swing pivot rather than a fixed distance — is the dominant architecture: grid **+565.58**, strip-best **+301.99**; 52% of 4,167 shakeouts convert to ≥1R; swing turns positive-and-robust for the first time `[ledger]` |
| **TC-1 factorial** | The trailing exit is **dominated** and anti-synergises with the structural stop (interaction −703, negative in every mandate). Two-line exit architecture **falsified** `[ledger]` |
| **TC-5** | Intraday 1H/5m re-spec: the *mechanical* fractal claim confirmed (excursion-to-toll ratio 0.65 → 1.79), the *economic* claim falsified (still net negative). Ruling: **entries floored at 5 minutes, permanently** `[ratified]` |
| **S-3** | The add gate is frozen by circular topology: **97.59% of winning moments had no add signal available** — the gate closes precisely when adding is wanted. The winning book protects by *width, not advance*, and wins by **riding to regime break**, not by managing individual winners `[ledger]` |
| **CENSUS-1 / 1b** | Trade-independent photograph of price structure. **Two survived:** pullback termini land in SS zones at ~2× matched-null chance; the 4H cascade rung carries a real add-edge (quality ratio 1.0711, n 28,113). **Two died:** the pullback *outcome* edge (+0.0379 ATR, CI spans zero) and the nine-factor confluence framework (rho ~ 0.02-0.05) `[ledger]` |

**The macro-ruling that governs design from here:** entry-signal combinatorics do not tilt raw price. Measured edge lives in **exit asymmetry**, **toll-space scaling**, and **location structure** — not in cleverer entry signals.

### 3.2 The knowledge program

Two documents committed to `docs/knowledge/`, mapping the established literature against Naiad's own measurements, graded claim by claim `[ledger]`:

- **Trading Knowledge Foundation v0** — auction market theory, Wyckoff, time-series momentum, order flow, classical levels, derivatives posture, regime structure, plus a deliberate *anti-library* of what is excluded and why.
- **Level Selection Deep Dive (Wyckoff / AMT / CCL)** — how to choose *where* to enter and exit, rather than *when*.

**Three findings worth carrying forward.** The structural stop is a **mechanised Wyckoff spring** — the 52% shakeout-conversion figure is the canon's spring thesis, measured independently. The 4H rung's "median trade loses, population pays" shape is the signature of trend-following returns across forty years of managed-futures literature, rediscovered here without looking. And the operator's own MTF cross-cluster idea, reframed from *timing*-confluence (falsified in-house by D9) to **price-location** confluence (the family that survived), becomes the CENSUS-2 headline candidate — with its deflation gauge stated in advance, because cross density may be nothing but a noisy re-derivation of volume profile.

### 3.3 The infrastructure lane — three days of work

| Tool | State |
|---|---|
| `scripts/reviewer_manifest.py` | Built, accepted, F-M1..4 pass. One command emits repo HEAD, branch, ahead/behind, worktree state, and per-file size + sha256 + does-it-match-HEAD for 46 tracked sources `[ledger]` |
| `scripts/daily_brief.py` | Built, accepted, **F-B1..8 pass**, exit 0 in 337 s, headline biases for all ten assets `[verified]` |
| `scripts/daily_routine.py` + `routine_jobs.json` | Built, hand-run PASS. **Composable by design**: the JSON is a job *registry*, so new jobs are added by editing config, never code `[verified]` |
| `scripts/backup_estate.py` | Built, **7/7 fixtures pass**, first automated offsite backup completed `[verified]` |
| Skills | `naiad-custodian` (context-gap audit + integrity toolkit) and `naiad-daily-brief`, both installed |

### 3.4 The resiliency crisis, found and closed

**The single most consequential finding of the week.** A standing ledger risk note recorded the raw price journals as *"the single irreplaceable asset, on one machine under OneDrive."* **That was factually wrong and had been since Phase 0.** The estate resolves through `engine/data.py:39-48 cache_dir()` to `%LOCALAPPDATA%\naiad\data_cache` — outside the sync root entirely, in a directory routinely excluded by backup tools and purged by cleanup utilities. It had **no protection of any kind**, for the project's entire life `[verified]`.

It survived months of careful work because nobody checked the actual path. That is the argument for the whole verification programme in one sentence.

**Also root-caused:** the OneDrive outage of 2026-07-27 was **quota exhaustion** — registry `ItemCantFitInQuotaLastShown = 2026-07-27T01:05:08Z` against a 21.78 GB tree `[verified]`. Implication on the record: the cloud copy of that tree was **probably incomplete**, so OneDrive must not be assumed to have been backing up `research_outputs` either.

**Resolved by:** archiving six completed phases (21,055.60 MB -> 977.70 MB, 13,502 members, **0 mismatches**, 25 git-tracked files preserved) for **19.61 GB reclaimed**; rebuilding `.venv` outside OneDrive (**214.9 MB, 7,813 files**); and 252 MB of proven redundancy removed. Tree: 21.78 GB -> **~1.7 GB** `[verified]`.

---

## 4. Verified state of record — 2026-07-28

**Repo:** HEAD **`837c635`**, branch `v12-v1-census`, **ahead 2, unpushed**. Engine 1.0.11. Test suite **73 passed, 1 skipped** `[verified]`.

**The estate:** `C:\Users\luisf\AppData\Local\naiad\data_cache` — 70 files, 652,451,079 B. Reconciled exactly against the 2026-07-27 baseline of 71 files / 664,269,426 B: the orphaned `ZECUSDT_1m.parquet.4100.tmp` (12,563,190 B) was deleted, leaving 744,843 B of daily top-ups `[verified in session]`.

**Offsite protection — three generations, two providers:**

| Copy | Where | Verification |
|---|---|---|
| `naiad_estate_2026-07-27.zip` (477.6 MB) | Two Google Drive accounts, uploaded by browser | 71/71 bidirectional `[verified]` / placement `[operator]` |
| `naiad_estate_2026-07-28.zip` (469.5 MB, sha `ad94dc6e...be12`) | `G:\My Drive\naiad-backups`, **written automatically** | 73/73 bidirectional, **re-verified from the Drive path after upload settled — sha byte-identical to write time** `[verified]` |
| Six phase archives (977.70 MB) | Local `research_outputs\_archive\` + Drive accounts | 13,502 members, 0 mismatches, independently re-hashed by the reviewer plus 90 random member extractions `[verified]` |

**Drive headroom is the binding constraint.** 13.14 GB free of 15 GB. At 469.5 MB per estate generation that is **~28 generations, or ~26 once phase archives are copied across** `[verified in session]`. Nothing prunes anything, by design — **a retention rule must be decided before scheduling, not after.**

---

## 5. Standing subject — continuous optimization

The premise: **every phase should leave the machinery better than it found it**, and the reviewer should be measurably harder to fool over time.

**What this has produced.** The manifest exists because establishing repo state cost hours. The backup script exists because a manual archiving run proved a pattern worth encoding. The daily routine's job *registry* exists because the first version would have needed rewriting to add a job — a system, not a fix. Each was built from an operation that had already succeeded manually, so the specification was derived from evidence rather than design speculation.

**The mechanism that makes it stick** is the error log (§12). Every reviewer mistake produces a standing rule, and the rules are encoded where they will be re-read — in the custodian skill, in the paste template, in the contract amendments — not in a document nobody opens.

**Measured improvement.** On the first real run, the manifest caught three things nobody asked it to look for: a stale `.gitignore`, two reappeared root files, and two unresolvable box entries. The backup script's smoke test reproduced a ledger-recorded hash, giving a fifth independent verification path on an archive already verified four ways. Both tools found problems on their first day. That is the test of whether an optimization was worth building.

---

## 6. Standing subject — workflow efficiency

**The measurement that drives everything.** In the 2026-07-26/27 session: **25 paste events, 8 misrouted (32% waste), ~150 discrete operator actions, of which 9 were decisions — 6%** `[verified in session]`. The other 94% was copying pastes, hunting for the right window, screenshotting terminals, uploading images.

**The three costs, and what each is being replaced with:**

| Cost | Was | Now / becoming |
|---|---|---|
| **Routing** — which window | 7 misroutes in two days | Operator-facing routing line above every paste; hard environment assertion inside it, **read-only pastes included** |
| **Transport** — screenshots | Up to 9 images per round trip | Every paste writes a **single report file** to `_reviewer_box\reports\`; one drag replaces N screenshots |
| **Round trips** — sequential dependency | 17 in one session | Every paste now carries **its own decision tree** for predictable outcomes; a round trip is spent only on genuine judgement |

**The reviewer's own biggest failure, named:** treating Claude Code as a shell rather than an agent — writing linear command sequences and taking a round trip at every branch, when the builder repeatedly demonstrated it could reason far past that. A paste that says *"do A; if X then B else C; report all"* collapses three exchanges into one.

**Why read-only pastes need the same assertion as writes** — the least obvious rule and the most important. A misrouted *write* paste fails loudly on preconditions. A misrouted *read-only* paste **silently succeeds and returns plausible nonsense**: a size audit run in a fresh clone would have produced a phase-coldness table whose dates were all clone timestamps, and it would have looked entirely credible.

**Where this ends.** Once the daily routine has a trigger, the recurring work — manifest, brief, change-detection — happens before the operator wakes. Target steady state: **~7 minutes a day, nearly all of it reading.**

---

## 7. Standing subject — resiliency

**Principle: sync is not backup.** OneDrive, Google Drive and Dropbox all propagate deletions and corruption as faithfully as they propagate good data. Version history is a retention window, not durability. The architecture therefore uses **dated, non-overwriting, hash-pinned archives across independent providers**.

**The four layers now in place:**

1. **Local primary** — the working tree and the estate at `%LOCALAPPDATA%`. Fast, complete, single point of failure.
2. **Local archive** — `research_outputs\_archive\`, six verified zips holding 20.56 GB of evidence in 977 MB. Kept deliberately: deleting them would leave the evidence at a single provider.
3. **Sync layer** — OneDrive for the repo (now ~1.7 GB, comfortably inside quota).
4. **Offsite generations** — `G:\My Drive\naiad-backups`, dated and non-overwriting, with `--verify` able to re-check any copy without extracting it.

**What makes it trustworthy rather than merely present:** verification is **bidirectional** — every member re-read *out of the archive* must hash equal to a fresh read of the source, **and** every embedded manifest pin must agree with both. Set membership is cross-checked in all three directions (archive / manifest / disk), so a stray or an omission cannot hide. F-K5 re-reads the archive **from the destination after writing**, which is what catches a truncated or half-synced cloud write. And the no-clobber guard makes accidental generation loss *structurally impossible* rather than merely discouraged.

**Open resiliency items.** A **retention rule** is needed before scheduling (§4). The **`--phase` archive-and-release path is fixtured but never run live** — first real use should target an already-archived phase so the output can be diffed against a known-good zip. And **something is writing to the working tree**: a stale `index.lock` 117 minutes old with no owning process, and `scripts/orchestrator_state.py` appearing unbidden — the third and fourth foreign artifacts in one day. Cause unresolved; the routine will report them as "untracked added" with no local explanation.

---

## 8. Standing subject — how the chats communicate

**The constraint that shapes everything:** chats cannot read each other. They share the same **project memory**, the same **context box**, the same **repo and ledger** — but not conversation context. So the failure mode is not collision, it is **stale state**. On 2026-07-27 the SYSTEM chat discovered two BRIEF commits by accident during an unrelated audit.

**The four lanes.** SYSTEM (v12 study, census phases, Tier-C contracts, knowledge program) · ENGINE (engine versions, repo operations, integrity, manifest ritual) · BRIEF (the daily market report) · ORCHESTRATOR (compiles the three status docs and the cross-lane action queue, and is the **only** component that can *write* to the project box).

**Live discrepancy worth knowing:** the SYSTEM-titled chat has done overwhelmingly ENGINE-lane work — integrity, manifest, backup, housekeeping. **File its events by content, not by the block's title.**

**The five orchestration decisions:**

- **D-O1 — one branch, not three.** Per-lane branches would conflict on `LEDGER.md` at every merge, and the operator is a serial actor who can only run one builder task at a time. Concurrent writes are not the risk; stale state is.
- **D-O2 — freshness via the manifest.** Every chat opens by reading a current `MANIFEST.json`. **No chat asserts repo state from memory.**
- **D-O3 — commit prefixes are the workstream signal.** `ops:` = SYSTEM · `brief:` = BRIEF · phase names = ENGINE · `docs:` = any. Makes `git log` a coordination view.
- **D-O4 — one writer at a time.** Before issuing a paste that writes, a chat confirms from a fresh manifest that HEAD matches expectation. Discipline, not a lock.
- **D-O5 — the open-questions register is the decision queue.** A chat needing a ruling *appends* rather than blocking mid-conversation; the operator answers in batches, with full context on each.

**Three layers, three jobs, no substitutes:** `MANIFEST.json` is machine-generated ground truth about files and git — it cannot be misremembered. `STATUS_*.md` carries intent and narrative, which no file scan can infer. The **open-questions register** holds what is pending on the operator.

**The question format**, because a question without it wastes attention: the question · **why it is the operator's call** rather than the reviewer's · **what is blocked** while it waits · **each option's consequence**, including the cost of not deciding. Reviewer leans are stated and labelled as leans.

**Status blocks are now written into `claude/STATUS_SYSTEM.md` by paste** rather than emitted in chat `[ratified]`. The relay disappears from the operator's view; the content still reaches the dashboard.

**The paste contract** — five rules, each earned: an operator-facing routing line above the code block · a hard environment assertion inside it that halts before *any* write, read-only included · verification gates written from the **post-action** state, simulated step by step before shipping · a single report file instead of screenshots · and a decision tree for outcomes the reviewer can predict.

**Document delivery, revised 2026-07-28:** downloads from the Claude app have failed repeatedly for `.md` and `.py` files. Documents are therefore delivered as **builder-write pastes** — the builder writes the file directly into the repo — rather than as downloads.

---

## 9. The pipeline

**Immediate, unblocked:**
1. **Cowork re-test** — 10 minutes, new task with the naiad folder attached. Decides whether the daily routine is triggered by a Cowork schedule (which would also publish results to the project box, removing the operator's daily drag) or by Windows Task Scheduler. Settings show tasks run locally, so the earlier negative result — from a *chat*, not a folder-attached task — is probably not representative.
2. **Register the trigger** — every day 07:00 `[ratified]`.
3. **Push** — 2 commits ahead, unpushed.
4. **A retention rule** for Drive, before scheduling the backup.

**Study lane, blocked on two rulings:**
5. **CENSUS-1c** — cannot be drafted until Q-1 (does the 1D lens stay in, labelled diagnostic-only?) and Q-2 (does 1c measure the D8 eligibility window?) are answered. Both have reviewer leans of *yes*.
6. **Then:** Tier-C for D5 (slow-stack entry, scoped to 12H/position primary) and D8 (4H cascade add, gate only — no sizing change) -> **TC-2**, the re-entry quality bar, whose candidate mechanism is the Wyckoff spring test.

**Named but not scheduled:** CENSUS-2 / the CCL location hypothesis · the take-profit mechanism (AMT opposing-level harvest) · manifest v1.1 · the parked D-2 adoption ruling · SSv11.4 display decisions · the S-1/arm-A excursion back-fill.

---

## 10. Distance to objectives

### Short term — infrastructure that runs itself · **~90% there**
All four tools exist and are accepted. **What is missing is one trigger and one retention rule.** Days, not weeks.

### Mid term — a v12 engine with demonstrable edge · **~40% there**
Honestly assessed by mechanism:

| Mechanism | State |
|---|---|
| **Stop** | **Solved.** Structural stop is positive-and-robust; swing flips positive for the first time |
| **Entry admission** | **Partly.** Location conditioning survived (zones at 2x null, the no_zone gate vindicated); timing confluence is dead. D5 graduated but narrowed to 12H primary |
| **Add gate** | **Diagnosed, not solved.** Circular topology proven; D8's 4H rung is the only measured edge; the eligibility window is unmeasured |
| **Take-profit** | **Not started.** Priority #3, no candidate mechanism in the engine. The leading idea — harvest into opposing value-area edges and naked POCs — exists only in the knowledge program, untested |

**The critical path is take-profit.** It is the largest measured failure (90.35% of +1R-touching trades exit at a gross loss) and the least developed. The daily brief's volume-profile engine is the infrastructure that candidate needs, which is a genuine convergence between the two lanes.

### Long term — a validated system · **~15% there**
The end state is a v12 engine whose rules were all pre-registered on exploration-classic data, then tested **once** against the sealed lockbox. **The lockbox has never been opened** — that discipline is intact, and it is the single most valuable asset the project holds, because it can only be spent once.

The realistic sequence: close the three open mechanisms -> assemble v12 -> pre-register the full specification -> **one** lockbox run. Everything before that final step is preparation for a single irreversible measurement.

---

## 11. Open decisions

| # | Question | Blocks | Reviewer lean |
|---|---|---|---|
| Q-1 | CENSUS-1c: 1D lens in, as diagnostic-only? | The whole ENGINE lane | Include, labelled |
| Q-2 | CENSUS-1c: measure the D8 eligibility window? | Same | Measure all three |
| NEW | Drive retention — how many generations before pruning? | Scheduling the backup | Keep 4 estate + 1 phase set; report, never auto-prune |
| NEW | Investigate the foreign files writing to the working tree? | Nothing yet — but trust in `git status` | Investigate; unexplained writes to an integrity-critical tree are not acceptable indefinitely |
| Q-3 | `s3_excursion_substrate.jsonl` tracked while siblings are fenced | Nothing | **Default taken:** document as a known exception; removing it would rewrite every commit hash the ledger cites |
| Q-5 | Archive `tc5` (398 MB)? | Nothing | Yes, once `--phase` has one live run |
| Q-7..Q-10 | D-2 adoption · SSv11.4 display · excursion back-fill · manifest v1.1 | Nothing | Parked deliberately |

---

## 12. Errors logged — the pattern matters more than the list

An orchestrator that sees only successes will trust this chat's output more than it should.

- **Three paste-construction errors** where a verification gate was written from the *pre*-action state: a five-file deletion list against an empty-worktree gate when ten existed; a ledger entry asserting 18/18 while the same paste restored a file making it 19/19; a phase-directory deletion contradicting its own expected-EMPTY git status.
- **A provenance violation** — a STATUS block tagged a Google Drive folder `[verified]` when the source was an interview answer. The folder did not exist.
- **A dependency blind spot** — archiving checked for git-tracked files but not test-fixture dependencies, silently breaking the `c141t213` regression gate at `268cdf9`. Undetected until a rebuild happened to run the suite.
- **A projection error** — compression estimated at 741 MB from one file's ratio; actual 977.70 MB, off 32%. One file from one phase is not a sample.
- **Two specification errors caught by the builder in a single day** — instructing a commit that violates charter §10 ("raw candles are never committed"), and specifying a backslash path form that would have broken 32 Bash allowlist entries.
- **Seven routing failures** — pastes addressed to the local machine delivered to a cloud session. Every labelled paste was halted by its ENVIRONMENT header; the convention worked, the routing did not.

**The pattern:** the reviewer's errors are almost never analytical. They are errors about **what the machinery actually contains** and **what state will exist after the reviewer's own instructions run**. Both are now guarded — the custodian audit moves machinery checks earlier into contract drafting, and post-action gate simulation is mandatory before a paste ships.

**The builder catching these is the system working, not failing.** Three separate refusals this week — deleting tracked files, committing against the charter, and rewriting an allowlist into a broken form — each preserved an invariant the reviewer had overlooked.