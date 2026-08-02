# HEPHAESTUS — exchange v1 build report

**Filed:** 2026-08-02 · **Lane:** HEPHAESTUS (local Claude Code, working Naiad clone)
**Authorization:** gate A-7, implementation push AUTHORIZED. Rulings taken as `FUNNEL_DIONYSUS_W1`
defaults (Q-1 C · Q-2 A · Q-3 A · Q-4 A · Q-5 as ruled · Q-6 A · Q-7 A · Q-8 A) and
`FUNNEL_ATHENA_W2` answered **defaults**.
**Deviation check:** the record was searched for any operator deviation from defaults before any
write. `FUNNEL_DIONYSUS_W1_Workflow_Architecture_2026-08-02.md` §"Rulings received" reads *"FUNNEL
CLOSED. Operator: all other questions your defaults"*, with Q-5 modified to add ARGUS drafting
rights — which the paste already carries. No deviation found, so the paste executed rather than
halting. **Note:** no `FUNNEL_ATHENA_W2` document exists in the repo; that ruling is taken from the
operator's paste itself, which is the authority here.

---

## STEP 0 — HARD ASSERT (before any write)

| Check | Result |
|---|---|
| OS is Windows | PASS — `Windows_NT`, Win 11 Home 10.0.26200 |
| PWD is repo root | PASS — `C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad` |
| `LEDGER.md` present | PASS |
| Branch | PASS — `v12-v1-census` |
| **HEAD at start** | **`5b0e36e`** |
| **Porcelain count at start** | **23** |

Assert satisfied. Proceeded.

---

## PART A — the exchange skeleton · **DONE**

Created `exchange/` with `status/`, `queue/`, `reports/`, `drops/`, plus `exchange/DIGEST.md`.

`DIGEST.md` is a placeholder whose header states plainly that **HERMES owns it**, that no other lane
writes it, and that nothing in it is authoritative until his first pass. Until then it points readers
at the raw files.

Each subfolder carries a `README.md` stating its convention in five lines:

- **status/** — one append-only `LEDGER_<LANE>.md` per lane · `MANIFEST.json` · `daily/` staged
  outputs · `CADENCE.md` · append, never rewrite.
- **queue/** — `NNN_<slug>.md`, full-contract format, `RATIFIED: <word> <date>` stamp line, drafting
  rights APOLLO/ATHENA/ARGUS, HERMES validates and sequences, HEPHAESTUS executes ratified items only.
- **reports/** — builder outputs, `YYYY-MM-DD_<LANE>_<type>_<name>.md`, one file per run, never
  overwritten.
- **drops/** — raw operator inbox, HERMES names (G-11) and files, a drop still present is a drop
  still unprocessed.

**CONTENT GUARD** in `exchange/README.md`, binding on every file under `exchange/**`:

1. text only — no binaries, no archives, no images;
2. 1 MB per-file cap (1,048,576 bytes);
3. larger artifacts referenced by `path:` + `sha256:` pointer, never carried.

**Guard compliance at close of build:** 29 files under `exchange/`, all text, largest
`status/daily/brief_2026-08-02.json` at **258,713 B — 24.7% of the cap**. No violations.

---

## PART B — per-lane ledgers (Q-3 A) · **DONE**

Six append-only ledgers created under `exchange/status/`, each carrying the naiad-eod template header
(`=== STATUS_<LANE> — <date> ===` / NOW / LAST EVENT / FACTS / PENDING / NEXT), extended with the
Q-8 `METRICS:` line. Each states that `LEDGER.md` remains the *evidence* ledger and is untouched.

| ledger | seeded from | note |
|---|---|---|
| `LEDGER_APOLLO.md` | STATUS_ENGINE | dated 2026-07-27, tagged stale |
| `LEDGER_ARGUS.md` | STATUS_BRIEF | dated 2026-07-27, tagged stale |
| `LEDGER_ATHENA.md` | `claude/STATUS_SYSTEM.md` (ops content) | **plus the required 2026-08-02 entry** |
| `LEDGER_DIONYSUS.md` | founding line | no prior status doc |
| `LEDGER_HERMES.md` | founding line | no prior status doc |
| `LEDGER_HEPHAESTUS.md` | founding line + this session's build | no prior status doc |

`LEDGER_ATHENA.md` carries, verbatim as instructed:

> 2026-08-02 — W1 (Dionysus funnel) rulings ingested; FUNNEL_ATHENA_W2 answered defaults; exchange v1
> built this session.

### ⚠ Deviation, disclosed: where the APOLLO and ARGUS seeds came from

The paste directed the seeds to `claude\STATUS_*.md`. **`claude/` contains exactly one file —
`STATUS_SYSTEM.md`.** There is no `claude/STATUS_ENGINE.md` and no `claude/STATUS_BRIEF.md`.

The documents the paste names do exist, as untracked `.txt` files at repo root:

- `STATUS — ENGINE (engine builds · repo operations · integrity & manifest).txt` (2,917 B, 2026-07-27)
- `STATUS — BRIEF (daily market brief · Atlas HTML report · live laboratory).txt` (3,008 B, 2026-07-27)

Their content is unmistakably the intended source — same lanes, same format, referenced as
`claude/STATUS_ENGINE.md` and `claude/STATUS_BRIEF.md` by
`ORCHESTRATOR CONTROL CENTER — protocol & state of record.txt`. I used them and recorded a
provenance note at the foot of each seeded ledger naming the exact source file, its byte size, its
date, and the fact that it is stale. **The alternative reading — that APOLLO and ARGUS get founding
lines because the literal `.md` paths are absent — would have thrown away real lane history to honour
a filename.** Flagged for the operator: if the intent was founding lines, say so and I will replace
the two seeds.

Both seeds are explicitly marked stale, and demonstrably are: APOLLO's PENDING list includes a push
ruling long since resolved, and ARGUS's predates `CONTRACT_ARGUS_Analytics_Scoping_2026-07-29.md`.

### `exchange/status/CADENCE.md`

The trigger registry, with the state of each of the four triggers:

| # | trigger | when | owner | state |
|---|---|---|---|---|
| 1 | Naiad daily routine | daily 07:00 | machine | **ARMED this session** |
| 2 | Naiad weekly backup | Sundays 08:00 | machine | **ARMED this session** |
| 3 | Hermes scheduled run | 2×/day | HERMES (Cowork) | **NOT ARMED — Hermes-side, pending F4** |
| 4 | Sync now | on demand | **operator** | **MANUAL, and stays manual** |

It also carries each task's next-run time, the G:-absent runtime guard, the retention posture, and
the two removal commands.

---

## PART C — migrate `_reviewer_box` (gate A-3a) · **DONE**

11 files moved, nothing copied, nothing deleted:

| from | to | count |
|---|---|---|
| `_reviewer_box/reports/*` | `exchange/reports/` | 6 |
| `_reviewer_box/daily/*` | `exchange/status/daily/` | 4 |
| `_reviewer_box/MANIFEST.json` | `exchange/status/MANIFEST.json` | 1 |

`_reviewer_box/README.md` now reads, in one line:

> Retired 2026-08-02 (gate A-3a) — reports, daily outputs and MANIFEST.json now live in `exchange/`.

**Note:** `_reviewer_box/` is git-ignored (`.gitignore:80`), so that pointer file **cannot be
committed and stays local by design.** That is the correct outcome — it exists to orient anyone who
opens the local folder, and there is nothing to publish about a retired directory.

### .gitignore — which rule, if any, would catch `exchange/**`

**None. No negation was added, because none is needed.** `git check-ignore -v` was run against nine
real exchange paths (`README.md`, `DIGEST.md`, `status/MANIFEST.json`, `status/CADENCE.md`, both
`daily/brief_*` artifacts, a report, and both subfolder READMEs) and **exited 1 — no rule matched any
of them.**

One rule *could* bite content placed inside the tree: **`.gitignore:38 — `*.zip``**, which is global.
A probe confirms it: `exchange/drops/example.zip` would be ignored. I did **not** negate it. A `.zip`
under `exchange/` is already forbidden by the content guard, so that rule reinforces the guard rather
than fighting it — and adding `!exchange/` would silently permit exactly what PART A's guard exists
to prevent. Recorded here so the interaction is on the record rather than discovered later.

---

## PART D — manifest v1.1 (rides A-3) · **DONE — 4/4 FIXTURES PASS**

`scripts/reviewer_manifest.py` amended. Fixture lines from the run, verbatim:

```
PASS F-M1 - round-trip byte-identical over 23796 bytes; self sha256 409f2fe6a0749e4f
PASS F-M2 - true copy accepted, one-byte mutant rejected (81f8722f270c)
PASS F-M3 - two builds byte-identical over 23752 chars
PASS F-M4 - porcelain unchanged (25 entries before and after)
wrote exchange/status/MANIFEST.json (46 sources, 12 box files, 19 untracked root)
v1.1 fields: onedrive_running=NO, queue_open=0, ledger 244110 B
```

Exit 0. **No fixture failed, so the paste continued to PART G as specified.**

### Changes made

1. **`BOX_DIR` → `exchange/status`.** Output path and box inventory both follow.
2. **F-M1 is now a ROUND-TRIP test.** Three ordered assertions: the bytes on disk equal the bytes
   intended; they re-parse as JSON; re-serialising the re-parsed object reproduces them byte for
   byte. **The self-hash is retained as a fourth, secondary assertion inside the same fixture**, as
   instructed — it was not replaced.
3. **§1.3 rewritten** to "Git is queried with READ-ONLY commands, **including but not limited to**:
   rev-parse, status, cat-file, ls-files, log, and **`git config --get`**." v1.0 carried a closed
   four-command list that `git config --get` already had to be excused from by footnote; the footnote
   is now the rule, and `git log` (needed by `lane_last_commit`) is covered by the same wording.
4. **Four new fields**, verified live:

| field | value at build | meaning |
|---|---|---|
| `onedrive_running` | `false` | process check via `tasklist`; null on non-Windows |
| `ledger_head` | `{present: true, title: "# Data-Spend Ledger", size: 244110}` | title line + byte size |
| `lane_last_commit` | `ops` → `837c635`, `docs` → `f1dc026`, `brief`/`exchange`/`study-phase` → `null` | most recent commit per prefix |
| `queue_open` | **1** (after PART G; 0 before it) | queue items lacking a ratification |

A `manifest_version: "1.1"` field was added so a consumer can tell the two schemas apart.

### ⚠ Two amendments the migration forced, neither of which was in the paste

**1. F-M4 now normalises out the manifest's own output path.** This is not optional and not
cosmetic. F-M4 asserts "porcelain unchanged across the run". That worked only because the output
lived in a git-ignored directory, so writing it could not move `git status`. Once
`exchange/status/MANIFEST.json` is **tracked**, every run legitimately shows it as modified — and
F-M4 would have **failed on every run after the first commit**, for a reason that is not a defect.
The fixture now drops exactly that one path, matched literally, from both sides before comparing.
Anything else the run touches still lands in the comparison and still fails the fixture. Invariant 1
was rewritten to match: the output is now tracked, and that is stated rather than implied.

**2. `guess_source()`'s bare-name fallback was narrowed.** The fallback resolved a box filename to
any tracked path whose `/` → `_` flattening matched. `_reviewer_box/` held flat *copies* of root
files, so that was right. `exchange/status/` holds **native artifacts, not copies** — and under the
old rule `exchange/status/README.md` resolved to the repo's own root `README.md` and reported
`match_head: false`: a copy-is-stale alarm about a file that is a copy of nothing. The fallback now
requires the resolved target to contain a `/`, i.e. to be genuinely flattened. **Verified:** all 12
box entries now record `source_guess: null`, including `README.md`. Every real flattened resolution
is preserved.

Both amendments are documented in the script itself, at the point of change, with the reasoning.

---

## PART E — routine + backup gain the publish step (gate A-6a) · **DONE**

### `scripts/routine_jobs.json` — repointed (version 1 → 2)

- `output_dir`: `_reviewer_box/daily` → **`exchange/status/daily`**
- manifest stage `from`: `_reviewer_box/MANIFEST.json` → **`exchange/status/MANIFEST.json`**
- new `"publish": true` switch, so the step is config-controlled like everything else in the registry

### `scripts/publish_exchange.py` — new, and the single implementation

**Implementation choice, disclosed:** the paste says to append a PUBLISH step to both scripts. Rather
than duplicating ~60 lines of identical git logic into two files — two copies to audit, two to
drift — the guard and the publish routine live in one module that both import. `daily_routine.py` and
`backup_estate.py` each gained a final publish step, as instructed; the step's body is shared.

The sequence: stage `exchange/` only → read the **whole index** back via
`git diff --cached --name-only` → every path must start with `exchange/` → if **anything** else is
staged, `git reset` (unstage all), write a FLAG line, **skip the push** → otherwise commit
`exchange: auto-publish <yyyy-mm-dd>` and push.

It reads the whole index rather than trusting its own `git add` on purpose: `git add -- exchange`
stages what we asked for, but cannot tell us what was **already** in the index on arrival. A
half-finished `git add` from an earlier session would otherwise be published under an auto-publish
subject line — which is precisely the evidence-leak the Q-2 A scope rule exists to prevent. The reset
discards hand-staged index state; that is deliberate, touches no working-tree file, and loses no work.

### Guard DRY-RUN — executed for real, 12/12 checks pass

Not proved by code review: the guard was exercised against a **throwaway index file**
(`GIT_INDEX_FILE`), so `git diff --cached --name-only` genuinely reported a non-exchange path and the
guard genuinely judged it.

```
PART 1 -- guard() as a pure function
  PASS empty index is clean - nothing staged is not a violation
  PASS all-exchange index passes - 0 offenders
  PASS one stray trips the guard - offenders=['engine/signals.py']
  PASS multiple strays all reported - offenders=['LEDGER.md', 'research_outputs/census/build_manifest.json']
  PASS prefix lookalike is NOT in scope - 'exchangeable/' must not pass as 'exchange/'

PART 2 -- real staging against a throwaway index
  PASS throwaway index seeded from HEAD
  PASS staged a NON-exchange path - Naiad_Orchestration_and_Open_Questions.md
  PASS diff --cached reports it - staged=['Naiad_Orchestration_and_Open_Questions.md']
  PASS GUARD TRIPS on the real staged list - offenders=['Naiad_Orchestration_and_Open_Questions.md']
  PASS still trips with exchange paths added alongside - 25 staged, 1 offenders
  PASS exchange-only index PASSES the guard - 24 exchange paths staged, 0 offenders
  PASS REAL index byte-identical before and after - sha256 f55606b54eb35729
```

Worth recording: the first attempt used `git add -N` to avoid writing blobs, and produced a **false
PASS-shaped failure** — since git 2.14 intent-to-add entries are deliberately excluded from
`diff --cached`, so `-N` cannot exercise this guard at all. Switched to a plain `git add` against the
throwaway index. The repo's real index was hashed before and after and is **byte-identical**.

### `daily_routine.py`

Its docstring previously read **"NO git operations of any kind, ever"**. That line is now false and
was rewritten rather than left to rot: an `AMENDMENT 2026-08-02 (gate A-6a, ruling Q-2 A)` block
records why. Sections 3 and 4 still read repo state from the MANIFEST and never from git — that part
of the original contract is untouched and deliberately so. The publish step is the single bounded
exception and it fails closed.

Ordering note: publish runs **after** the report is written, so the report is inside the commit; the
publish outcome is then appended to the report as section 6, and those appended bytes are published
by the *next* run. The report says so in its own text.

### `backup_estate.py`

Publish step added to `--estate` and `--phase`. **`--verify` deliberately does neither** — it is an
inspection mode and stays read-only.

---

## PART F — arm the triggers (gates A-4a, A-5a) · **DONE — BOTH ARMED AND VERIFIED**

`schtasks /create /XML` was used rather than a bare `/create`, because **`schtasks` has no flag for
"Start in"** — the working directory is only settable through task XML. The XML was written to the
session scratchpad, outside the repo.

### Commands used

```
schtasks /create /TN "Naiad daily routine" /XML "<scratch>\naiad_daily.xml" /F
schtasks /create /TN "Naiad weekly backup" /XML "<scratch>\naiad_weekly.xml" /F
```

### Removal counterparts

```
schtasks /delete /tn "Naiad daily routine" /f
schtasks /delete /tn "Naiad weekly backup" /f
```

### Verified state, read back from Task Scheduler

| field | Naiad daily routine | Naiad weekly backup |
|---|---|---|
| Status | Ready | Ready |
| State | **Enabled** | **Enabled** |
| Schedule | Daily, every 1 day, 07:00 | Weekly, **SUN**, 08:00 |
| **Next run** | **2026-08-03 07:00** | **2026-08-09 08:00** |
| Task to run | `C:\venvs\naiad\Scripts\python.exe scripts\daily_routine.py` | `C:\venvs\naiad\Scripts\python.exe scripts\backup_estate.py --estate --dest "G:\My Drive\naiad-backups"` |
| **Start in** | repo root | repo root |
| Run as | `luisf`, InteractiveToken, least privilege | same |
| Last result | `267011` = "has not yet run" | same |

`G:` was present at arm time (11.02 GB free), so the contingency did not apply. The runtime guard
exists regardless: `backup_estate.py`'s environment assertion fails closed on an unwritable
destination, so a missing Drive surfaces as a failed task rather than a silent no-op.

**Caveat on record:** InteractiveToken means both tasks run only while this user is logged on.
Neither wakes the machine. Both have `StartWhenAvailable`, so a missed run catches up.

### RETENTION REPORT — added, and it never deletes

Rule: **keep the newest 4 estate generations + 1 phase set.** The report names everything outside the
rule and **removes nothing, ever** — pruning backups unprompted is exactly the class of act this
project halts to ask about. Written to `exchange/status/RETENTION.md` (overwritten each run, so it is
a current-state surface rather than an accumulating log) and echoed to stdout.

Rendered against live data during the build:

- **Estate generations:** 1 present (`naiad_estate_2026-07-28.zip`, 492,306,779 B), 0 outside the
  rule — fewer than 5 exist, so nothing to consider.
- **Phase sets:** 2 present. `2026-07-29` (2 archives, 26,457 B) within the rule;
  **`2026-07-27` (6 archives, 1,025,189,589 B) outside it** — `s1`, `s2`, `s3`, `tc1`, `tc4`,
  `v3_anchor`, each listed individually with its size.

That ~977 MB is the operator's call. Nothing was touched.

---

## PART G — queue item 001 (gate C-1a) · **DONE — FILED, NOT EXECUTED**

`exchange/queue/001_condensed-project-history.md`, drafted by ATHENA, 4,870 B.

- **Deliverable:** `docs/PROJECT_HISTORY.md`
- **Basis:** ledger-derived — `LEDGER.md` is authority; where a handoff and the ledger disagree, the
  ledger wins and the disagreement is noted
- **Provenance tags, mandatory, one per claim:** `[ledger]` `[commit]` `[ratified]` `[handoff]`
  `[unconfirmed]`
- **Supersedes nine dated documents** — seven tracked (`HANDOFF_2026-07-22_Census_to_Census1b.md`,
  four `REVIEWER_HANDOFF_*`, two `docs/handoffs/HANDOFF_2026-07-27_*`) and two untracked
  (`PROJECT_STATUS_AND_CONTEXT_2026-07-28.md`, `STATUS_HANDOFF_BRIEF_2026-07-28.md`), each with its
  byte size. They are **moved to `docs/history/`, never deleted**, each gaining a pointer line. The
  order explicitly does **not** supersede current coordination state (the Dionysus 2026-08-02
  documents, `claude/STATUS_SYSTEM.md`, the new lane ledgers).
- **Fixtures F-H1..F-H6:** F-H1 is the required "every claim carries a tag" check; the rest verify
  that `[commit]` shas resolve, `[ledger]` anchors are locatable, `[unconfirmed]` stays ≤5% and
  collected, all nine sources survive, and the guard's size limit holds.
- **Verdict:** the reviewer spot-checks **10 claims** against the ledger, reviewer's choice, across
  ≥4 phases. **10/10 ACCEPT · 9/10 ACCEPT WITH CORRECTION · ≤8/10 REJECT.** A tag that is present but
  *wrong* counts as a failure, not a nit — mis-tagging is the failure mode the set exists to catch.

**Stamp line reads `RATIFIED: PENDING`. It was not executed.** The manifest's `queue_open` field
independently confirms this: **1**.

---

## PART H — run once, commit, push · **DONE**

### The first run failed to publish. Reported in full.

`daily_routine.py` was run by hand. Jobs passed (manifest 4.7 s, brief 426.4 s, exit 0) — **but the
publish step failed**, and section 6 of that run's report recorded:

```
- publish did not complete: git add failed: fatal: Unable to create
  '.../.git/index.lock': File exists.
```

**Cause: a stale lock, not a defect in the new code.** `.git/index.lock` was zero bytes, created
**2026-08-01 19:41** — roughly twenty hours before this session began — with **no git process
running**. It was left by an interrupted git operation the previous day and had been silently
blocking every staging attempt since. Nothing was committed and nothing was pushed; the index was
verified clean (0 staged).

**Action taken:** after asserting no `git` process was running and the file was zero bytes, the stale
lock was **removed by hand** and the routine re-run. This is disclosed because it is a manual
intervention in `.git/`, however routine.

### Two real defects this exposed, both fixed before the re-run

1. **A failed publish exited 0.** Only `FLAGGED` produced a non-zero exit; `ERROR` did not. An
   unattended 07:00 run would have reported success while the bus silently failed to update. Both
   scripts now exit non-zero on `FLAGGED` **or** `ERROR`. A bus that did not update is a failure
   whichever caused it.
2. **The lock message was unactionable.** git's generic text sends the reader hunting for a running
   process that is not there. `publish_exchange.py` now detects `index.lock` and says specifically
   that a stale lock must be removed **by hand** — and states that the script will not remove it
   itself, because a lock that is *not* stale is protecting a real operation.

### The re-run

```
  manifest: exit=0 elapsed=4.6s
  brief: exit=0 elapsed=205.6s
wrote exchange/status/daily/DAILY_2026-08-02.md
publish: committed 74caae3 (29 path(s)) and pushed to origin/v12-v1-census
ROUTINE_EXIT=0
```

**The first auto-publish commit is `74caae3`** — 29 paths, every one inside `exchange/`, guard clean,
pushed. The waterwheel turned once on its own.

### The build commit

Staged explicitly — six paths, verified before committing, nothing else:
`scripts/reviewer_manifest.py`, `scripts/daily_routine.py`, `scripts/backup_estate.py`,
`scripts/routine_jobs.json`, `scripts/publish_exchange.py` (new), and
`exchange/status/daily/DAILY_2026-08-02.md` (the appended section 6 tail).

```
[v12-v1-census 8be8e79] ops: exchange v1 — waterwheel infrastructure per FUNNEL_DIONYSUS_W1 + FUNNEL_ATHENA_W2 (defaults)
 6 files changed, 683 insertions(+), 43 deletions(-)
 create mode 100644 scripts/publish_exchange.py
To https://github.com/catpatrol/Naiad.git
   74caae3..8be8e79  v12-v1-census -> v12-v1-census
```

`.gitignore` was **not** modified — no rule excludes `exchange/`, so there was nothing to change.
`docs/history/` was **not** created — queue item 001 was not executed, by instruction.

### Final state

```
$ git log --oneline -5
8be8e79 ops: exchange v1 — waterwheel infrastructure per FUNNEL_DIONYSUS_W1 + FUNNEL_ATHENA_W2 (defaults)
74caae3 exchange: auto-publish 2026-08-02
5b0e36e chore: file PC-1 contract into prompts/, drop root duplicate of contract v4 (G-11), refresh coverage after LIT re-extend
f1dc026 docs: PC-1 Stage 3 ledger record - LIT estate remediation, save-path floor enforcement, engine 1.0.12
4257067 fix: enforce the symbol floor at the cache persistence boundary; LIT estate remediation; engine 1.0.12

$ git status -sb
## v12-v1-census...origin/v12-v1-census
```

**Synced with origin, no tracked file dirty.** The 23 untracked root entries present at STEP 0 are
unchanged and untouched — none of them belongs to this build.

This report is filed to `exchange/reports/` and published by a following commit, which is what that
directory is for.

---

## SUMMARY OF VERDICTS

| Part | Verdict |
|---|---|
| STEP 0 | **PASS** — Windows, repo root, `v12-v1-census`, HEAD `5b0e36e`, porcelain 23 |
| A | **DONE** — skeleton + DIGEST placeholder (Hermes-owned) + 4 conventions + content guard; 29 files, all text, largest 24.7% of the 1 MB cap |
| B | **DONE** — 6 ledgers seeded (2 from root `.txt` STATUS docs — deviation disclosed) + `CADENCE.md` with all 4 triggers |
| C | **DONE** — 11 files migrated, pointer left; **no `.gitignore` rule excludes `exchange/**`**, no negation added |
| D | **DONE — 4/4 FIXTURES PASS** — round-trip F-M1, §1.3 reworded, 4 new fields live; two disclosed amendments (F-M4, `guess_source`) |
| E | **DONE** — paths repointed, shared publish module, **guard dry-run 12/12 against a real throwaway index** |
| F | **DONE** — both tasks ARMED and verified (next runs 08-03 07:00, 08-09 08:00); retention REPORT added, deletes nothing |
| G | **DONE** — 001 filed, `RATIFIED: PENDING`, `queue_open=1`, **not executed** |
| H | **DONE** — auto-publish `74caae3` + build `8be8e79`, both pushed; tree clean and synced |

## ITEMS FOR THE OPERATOR

1. **Configure GitHub sync in the Claude project, then click Sync now.** Nothing else makes the bus
   live for the web lanes. This is the one recurring action the design cannot absorb.
2. **Ratify or reject queue item 001.** It carries `RATIFIED: PENDING` and is not executable until
   stamped.
3. **APOLLO/ARGUS ledger seeds** came from the root `.txt` STATUS documents, not `claude/*.md` — say
   the word if founding lines were intended instead.
4. **A stale `.git/index.lock` from 2026-08-01 was removed by hand.** If an interrupted git session
   is a recurring pattern here, it is worth knowing why.
5. **~977 MB of 2026-07-27 phase archives sit outside the retention rule.** Reported only.
6. **`OneDrive.exe` is not running**, and the repo lives inside the OneDrive tree — now recorded in
   every manifest as `onedrive_running`.
7. **Hermes' 2×/day schedule is not armed**, pending the F4 experiment (owner DIONYSUS).
8. **The daily routine's brief job takes 3.5–7 minutes** and has never run unattended. Tomorrow
   07:00 is its first real test.

---

## METRICS (Q-8)

**Operator actions this session = 1** (one paste).
**Files re-ingested = 0.**
