# BUILDER'S REPORT — HEPHAESTUS · CONVENTIONS.md amend + publish · 2026-08-03

Forensic record. Standalone: assumes zero prior context. Provenance tags:
[verified] = computed or read by the builder this session · [handoff] = asserted by the
commissioning contract · [operator] = operator-reported · [open] = undetermined.

---

## 1 · What this was

`exchange/status/CONVENTIONS.md` is the file that holds the operating rules every Naiad lane
follows. It exists because project memory is capped at 30 entries and **does not reach Claude
Cowork at all** — so rules that must bind HERMES, DIONYSUS and HEPHAESTUS cannot live in memory.
It is the only instruction surface reaching all six actors.

The previous paste (earlier this session) wrote the file correctly but **halted at its own final
gate**: the gate searched for `project memory does NOT reach Claude Cowork` in lowercase while the
file said `Project memory…` at the start of a sentence. Nothing was committed. The file was left
on disk, untracked.

This paste did three things: appended an amendment about the correct publish invocation, re-gated
the whole file with case-insensitive fragment checks, and published it. A read-only sha256
reconciliation of the project box against the repo (PART B) was also commissioned; it could not
run, for the reason in §6.

**Outcome: PART A complete and published. PART B blocked on the first attempt, then completed on
the second after `boxrescue/` reappeared — full table in §6.**

---

## 2 · Environment assertion — as printed

```
=== ENVIRONMENT ASSERTION (halts before any action) ===
pwd=/c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad
branch=v12-v1-census head=21f6f36
CONVENTIONS.md present: 29282 bytes
```

Working directory matched `*OneDrive*naiad*`, branch was `v12-v1-census`, and the previous
paste's file was present at its expected 29,282 bytes. HEAD before any action: `21f6f36`.
[verified]

---

## 3 · DEVIATION — the amendment step crashed as written, and how it was completed

**What the contract's step did.** It wrote the amendment text to `/tmp/conv_amend.md` and a helper
to `/tmp/conv_amend.py`, then ran the helper with the Windows interpreter. The helper crashed:

```
Traceback (most recent call last):
  File "C:\Users\luisf\AppData\Local\Temp\conv_amend.py", line 4, in <module>
    add = io.open('/tmp/conv_amend.md', encoding='utf-8').read()
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/conv_amend.md'
```

**Root cause, and it is worth understanding once because it will recur** [verified]:

MSYS (Git Bash) rewrites POSIX paths into Windows paths **only when they are passed as command
arguments** to a native executable. That is why the traceback shows the helper being found at
`C:\Users\luisf\AppData\Local\Temp\conv_amend.py` — the argument was converted. It performs **no
such rewriting on string literals inside the file being run.** Windows Python therefore read
`'/tmp/conv_amend.md'` as a drive-relative absolute path, `C:\tmp\conv_amend.md`. Confirmed
directly: bash `/tmp` resolves to `C:\Users\luisf\AppData\Local\Temp`, and `C:\tmp` **does not
exist on this machine**. The read could never have succeeded.

This is the same family as the backslash bug the amendment itself documents: bash and Windows
Python disagree about what a path is, and the disagreement is silent until something reads.

**State immediately after the crash** [verified]: `CONVENTIONS.md` still 29,282 bytes — unmodified.
No commit, no push. `HEAD` still `21f6f36`. Gate 4 then correctly reported the amendment absent:

```
    HALT missing: no `__main__` block
```

**What I did, and the line I drew.** The halt was a true report of a real absence, but its cause
was a temp-file location, not a content or verification problem. I re-ran the identical amendment
with **one change: the temp files live in the session scratchpad, at a path Windows Python can
resolve.** Specifically:

- The amendment markdown was transcribed **byte-for-byte** from the contract's heredoc, including
  its leading blank line. Inserted length **1,719 bytes** — see §4.
- The helper's logic is unchanged: same anchor string, same `assert n == 1` on the anchor count,
  same idempotence check on `` no `__main__` block ``, same `newline=''` UTF-8 write. Only the
  amendment file's path is computed relative to the helper instead of hardcoded to `/tmp`.
- **Gates 1–4 were re-run exactly as the contract wrote them, unmodified.** Gate 4 passed on its
  own merits after the amendment landed; it was not relaxed, reworded, or skipped.

The principle applied, stated so it can be argued with: **adapt the mechanism, never the
verification.** A temp-file path is mechanism. A gate is verification. When the previous paste's
*gate* was wrong, I halted and changed nothing, because weakening a gate to make a paste pass is
the one adaptation that destroys the value of gating. Here the gate was right and the plumbing was
broken, so the plumbing moved and the gate stayed.

**Anchor safety** [verified]: `operator knows whether to click Sync now.` occurs **exactly once**
in the file, checked before and enforced by the helper's assert. The amendment could not have
landed in more than one place.

---

## 4 · PART A — full transcript as printed

```
AMEND: inserted 1719 bytes
=== PART A GATES ===
gate 1 - top-level sections: 12 (expect 12)
gate 2 - register rows incl. separator: 12 (expect 12)
gate 3 - size: 31015 bytes (expect > 29000)
gate 4 - required fragments:
    OK   does not reach claude cowork
    OK   no `__main__` block
    OK   moved-from-memory register
    OK   decision-funnel interview
=== PUBLISH ===
  ?? exchange/status/CONVENTIONS.md
publish: committed dde8523 (1 path(s)) and pushed to origin/v12-v1-census
status= PUBLISHED commit= dde8523 pushed= True offenders= []
HEAD now: dde8523
## v12-v1-census...origin/v12-v1-census
```

| Gate | Requirement | Observed | Result |
|---|---|---|---|
| 1 · top-level sections | exactly 12 (§0…§11) | 12 | **PASS** |
| 2 · register rows incl. separator | exactly 12 (11 rules + separator) | 12 | **PASS** |
| 3 · size | > 29,000 bytes | 31,015 | **PASS** |
| 4a · fragment | `does not reach claude cowork` | found | **PASS** |
| 4b · fragment | `` no `__main__` block `` | found | **PASS** |
| 4c · fragment | `moved-from-memory register` | found | **PASS** |
| 4d · fragment | `decision-funnel interview` | found | **PASS** |

Amendment result line: **`AMEND: inserted 1719 bytes`** — the amendment was newly applied, not a
re-run of an already-amended file. File grew 29,282 → **31,015 bytes**, a delta of 1,733 bytes
(1,719 inserted plus the anchor line's own retained newline accounting; both numbers are as
printed and as measured). [verified]

### Publish return values

| Field | Value |
|---|---|
| `status` | **PUBLISHED** |
| `commit` | **`dde8523`** |
| `pushed` | **True** |
| `offenders` | **`[]`** — empty; every staged path was inside `exchange/` |
| paths published | 1 — `exchange/status/CONVENTIONS.md` |
| branch | `v12-v1-census` → `origin/v12-v1-census` |

**PUBLISH SUCCEEDED.** The invocation used was `publish_exchange.publish(ROOT, '2026-08-03')` —
the ratified guard, called as `scripts/daily_routine.py:1048` calls it. No separate
`git add`/`git commit` of exchange files was performed; the guard did the staging, exactly as the
amendment this paste installed instructs.

### Content verification

| File | Size | sha256 | CR bytes |
|---|---|---|---|
| `exchange/status/CONVENTIONS.md` | 31,015 | `d373186e02cd135f9ac63bbbdbbc92b4979786f33e1daba1fe0ed77844d99c57` | **0** |

Zero CR bytes confirms the amendment did not introduce Windows line endings into a file the rest
of the repo treats as LF. Working tree is clean against the committed blob. [verified]

---

## 5 · What the amendment says

Appended to §3.4 (Publishing and the on-screen close). It records, in full paste-ready form, the
publish invocation that actually works, and why two earlier forms did not:

- `scripts/publish_exchange.py` is a **library module with no `__main__` block** — run as a
  script it publishes nothing and exits quietly, which is the worst failure shape available
  because the surrounding paste reports success.
- A Windows path with **backslashes inside a bash block is destroyed by the shell**:
  `C:\venvs\naiad\Scripts\python.exe` collapses to `C:venvsnaiadScriptspython.exe`.
- Two generalised Class A cures: forward slashes for Windows paths in bash; verify a module has an
  entry point before writing "run the script".
- One Class B cure from the halt that produced the amendment: **a gate matches a distinctive
  fragment, case-insensitively — never a full sentence quoted from prose the same author is
  writing in the same act.** Content and its gate authored together get no second reading.

That last rule is the one this paste then demonstrated: gate 4 is fragment-based and
case-insensitive, and it worked.

---

## 6 · PART B — blocked on the first attempt, completed on the second

### 6.1 First attempt — blocked. Full output as printed

```
=== PART B - BOX RECONCILIATION BY SHA256 (read-only) ===
boxrescue/ not present at repo root — cannot reconcile. Report this and stop.
=== END PART B ===
```

The block behaved exactly as designed: it tested for `boxrescue/`, did not find it, printed its
own guard message, and stopped without creating, reading, or touching anything.

### FINDING 1 (material, now resolved as to state, open as to cause) · `boxrescue/` vanished mid-session and reappeared. The builder touched it in neither direction.

Timeline, all [verified] from this session's own transcripts:

| When | Observation |
|---|---|
| Earlier, at the previous paste's halt diagnosis | `git status --porcelain` listed `?? boxrescue/` at repo root. I reported it then, unprompted, noting I had not created or touched it. |
| Now | `test -d boxrescue` → false. `test -e boxrescue` → **does not exist at all**. It is absent from `git status`. |
| Now | `find` over the entire parent folder `Midas-Claude Code Resources`, depth 4, case-insensitive, for any directory matching `*boxrescue*` → **no results anywhere**. It was not moved or renamed within reach. |
| Now | `git reflog` shows only this session's four commits. No checkout, no reset, no clean. |

**I did not create, move, or delete it.** The contract's instruction — *"Do not delete boxrescue/"*
— was followed; the directory was already gone before PART B tested for it, and PART B is the only
step that referenced it. Because it was **untracked**, git never had a copy: there is nothing in
the repository that could have restored it, and nothing in this session's history that could have
removed it. [verified]

**It came back.** On the operator's prompt to try again, `boxrescue/` was present at repo root with
26 files, directory mtime **2026-08-04 01:04**, and `git status` again showed `?? boxrescue/`. Note
that mtime is *earlier* than the 01:46 check that found nothing — the directory did not have to be
rebuilt to reappear. [verified]

**Most likely cause, stated as a hypothesis and not as a finding:** OneDrive Files On-Demand. A
folder that is dehydrated, mid-sync, or being reconciled from another device can be genuinely
absent to `test -e` and to `find`, then present again minutes later with its original timestamps.
That fits every observation — including the unchanged mtime — better than a delete-and-restore
would. It remains **[open]**; the operator is the only one who can say whether anything was done
by hand.

**Why it is worth answering rather than shrugging at:** if repo-root directories can be
transiently invisible to file tests, then any gate of the form "the directory is missing, so stop"
can fire on a healthy tree — and any script that reacts to absence by *creating* or *cleaning*
something would act on a false premise. This one only reported, which is the correct shape.

### 6.2 Second attempt — completed. Full table as printed

**Deviation, same family as §3, recorded before the results.** The contract embeds
`reconcile.py` in a quoted bash heredoc containing `replace('\\','/')` — a Python escaped
backslash. One backslash was lost in transit to the shell, and Python refused the file:

```
  File "C:\Users\luisf\AppData\Local\Temp\reconcile.py", line 23
    rel = os.path.relpath(p, root).replace('\','/')
                                                 ^
SyntaxError: unterminated string literal (detected at line 23)
```

Nothing ran, nothing was read, nothing was written. The script was then written **directly to the
scratchpad with no shell in the path**, so no escaping layer could touch it. One substantive line
changed: `replace('\\','/')` became `replace(os.sep, '/')`, which is the same operation on Windows
and cannot be mangled by any quoting layer. Every hash, every comparison, every verdict string and
the `SKIP` set are unchanged from the contract. This is a mechanism adaptation, not a verification
one — PART B is a read-only report and has no gates to weaken.

**Three separate backslash/path failures in two pastes now** — the bash-escaped Windows path, the
`/tmp` literal Windows Python cannot resolve, and this heredoc escape. The amendment installed in
`CONVENTIONS.md` §3.4 covers the first two. The third generalises the rule: **do not put
backslash escapes inside a heredoc that a shell will carry; write the file directly, or use a
form with no backslash at all.**

```
=== PART B - BOX RECONCILIATION BY SHA256 (read-only) ===
box files: 26   repo files hashed (size-matched only): 30

BOX FILE                                                   | VERDICT
-----------------------------------------------------------+---------------------------------------------
2026-08-03_HEPHAESTUS_report_retention-fix-and-alarm.md    | IDENTICAL AT exchange/reports/2026-08-03_HEPHAESTUS_report_retention-fix-and-alarm.md
AMENDMENT_2_BRIEF2_RESHAPE.md                              | IDENTICAL AT AMENDMENT_2_BRIEF2_RESHAPE_1.md
ARGUS_REPRIME_2026-08-02.md                                | IDENTICAL AT ARGUS_REPRIME_2026-08-02.md
BUILDERS_REPORT_ARGUS_2026-08-03_C4.md                     | IDENTICAL AT exchange/reports/BUILDERS_REPORT_ARGUS_2026-08-03_C4.md
CONTRACT_DESIGN_Atlas_Rewire_2026-07-30.md                 | IDENTICAL AT prompts/CONTRACT_DESIGN_Atlas_Rewire_2026-07-30.md
Deep_Trading_Philosophy_Analysis_Four_Traders.md           | *** NOT IN REPO ***
FUNNEL_DIONYSUS_W1_Workflow_Architecture_2026-08-02.md     | IDENTICAL AT docs/history/FUNNEL_DIONYSUS_W1_Workflow_Architecture_2026-08-02.md
HANDOFF_ATHENA_2026-08-03_FULL_STATE_1.md                  | IDENTICAL AT HANDOFF_ATHENA_2026-08-03_FULL_STATE_1.md
HANDOFF_DIONYSUS_to_ATHENA_2026-08-02_Workflow_Redesign_Inputs.md | IDENTICAL AT docs/history/HANDOFF_DIONYSUS_to_ATHENA_2026-08-02_Workflow_Redesign_Inputs.md
INTERFACE_2026-08-03.md                                    | IDENTICAL AT analytics/INTERFACE.md
Level_Selection_Deep_Dive_Wyckoff_AMT_CCL.md               | IDENTICAL AT docs/knowledge/Level_Selection_Deep_Dive_Wyckoff_AMT_CCL.md
Naiad_KB_Addendum_FourTraders_x_Canon_v1.md                | IDENTICAL AT Naiad_KB_Addendum_FourTraders_x_Canon_v1.md
Naiad_Knowledge_Canon_Synthesis_v1.md                      | IDENTICAL AT Naiad_Knowledge_Canon_Synthesis_v1.md
Naiad_Phase1_Build_Prompt.md                               | IDENTICAL AT Naiad_Phase1_Build_Prompt.md
Naiad_Trading_Knowledge_Foundation_v0.md                   | IDENTICAL AT docs/knowledge/Naiad_Trading_Knowledge_Foundation_v0.md
PRIMER_APOLLO_2026-08-01_v1_1.md                           | *** NOT IN REPO ***
PRIMER_DIONYSUS_2026-08-01_v1_1.md                         | *** NOT IN REPO ***
PRIMER_HERMES_2026-08-03_v2_FIRST_RUN.md                   | IDENTICAL AT PRIMER_HERMES_2026-08-03_v2_FIRST_RUN.md
Prometheus_Stop_Loss_Logic_Learnings.md                    | IDENTICAL AT Prometheus_Stop_Loss_Logic_Learnings.md
Rvwap_pine_code.txt                                        | IDENTICAL AT docs/knowledge/pine/Rvwap pine code.txt
SESSION_SUMMARY_ARGUS_2026-08-03_BRIEF2.md                 | IDENTICAL AT exchange/reports/SESSION_SUMMARY_ARGUS_2026-08-03_BRIEF2.md
SESSION_SUMMARY_ARGUS_2026-08-03_BRIEF2_C2.md              | IDENTICAL AT exchange/reports/SESSION_SUMMARY_ARGUS_2026-08-03_BRIEF2_C2.md
SSv11_3_Execution_Playbook_and_Field_Manual_1.md           | IDENTICAL AT SSv11_3_Execution_Playbook_and_Field_Manual.md
SSv12_SPEC_ERRATA.md                                       | IDENTICAL AT SSv12_SPEC_ERRATA.md
V12_Study_Charter_Addendum_v1_0.md                         | IDENTICAL AT V12_Study_Charter_Addendum_v1.0.md
V12_V1_Census_Build_Prompt.md                              | IDENTICAL AT V12_V1_Census_Build_Prompt.md

NOT IN REPO: 3
   - Deep_Trading_Philosophy_Analysis_Four_Traders.md
   - PRIMER_APOLLO_2026-08-01_v1_1.md
   - PRIMER_DIONYSUS_2026-08-01_v1_1.md

IDENTICAL rows are safe to remove from the project box. NOT IN REPO rows exist
nowhere else and must be filed before removal. NAME MATCH rows need a look.
=== END PART B ===
```

**Result: 26 box files · 23 IDENTICAL · 0 NAME MATCH · 3 NOT IN REPO.**

Matching is by **sha256 of file contents**, so it is name-independent — that is why the flattened
box names still resolve. Four rows are worth reading twice, because the name differs and only the
hash proves the match:

| box name | repo name | what the difference is |
|---|---|---|
| `AMENDMENT_2_BRIEF2_RESHAPE.md` | `AMENDMENT_2_BRIEF2_RESHAPE_1.md` | browser duplicate suffix `_1` |
| `INTERFACE_2026-08-03.md` | `analytics/INTERFACE.md` | dated on upload, undated in repo |
| `Rvwap_pine_code.txt` | `docs/knowledge/pine/Rvwap pine code.txt` | spaces flattened to underscores |
| `V12_Study_Charter_Addendum_v1_0.md` | `V12_Study_Charter_Addendum_v1.0.md` | `.` flattened to `_` |

These are exactly the hand-upload flattening artifacts §4.3 of `CONVENTIONS.md` describes. Byte
identity is confirmed in every case.

### 6.3 The three files that exist nowhere else

`Deep_Trading_Philosophy_Analysis_Four_Traders.md` · `PRIMER_APOLLO_2026-08-01_v1_1.md` ·
`PRIMER_DIONYSUS_2026-08-01_v1_1.md`

Two independent checks, both [verified] this session:

1. **By content** — no file anywhere in the scanned tree has a matching sha256.
2. **By name** — a case-insensitive `find` across the *entire* repo, with no directory exclusions
   beyond `.git`, for `PRIMER_APOLLO*`, `PRIMER_DIONYSUS*`, `Deep_Trading*`, `Four_Traders*` and
   `FourTraders*` returns **only the `boxrescue/` copies themselves**. There is no near-name
   variant, no older version, and no differently-named twin.

The name search matters because the reconciliation's own NAME-MATCH test compares exact filenames,
and the box flattens `v1.1` → `v1_1` — so a repo file called `PRIMER_APOLLO_2026-08-01_v1.1.md`
would have been reported as NOT IN REPO even if it existed. It does not exist. The verdict stands
on both axes.

**Honest limit of the content check:** the hashing walk skips `research_outputs/`, `briefs/`,
`node_modules/`, `.venv/` and cache directories, so a byte-identical copy hiding *inside* one of
those under a different name would not have been seen. The name search did cover those
directories and found nothing, which makes that scenario unlikely — but it is not excluded by
hash. [verified as stated]

**Consequence, and this is the operator-facing point:** those three files exist **only** in the
project box and in `boxrescue/`. Deleting them from the box without filing them into the repo
first would destroy them. The other 23 are safe to remove from the box — every one has a
byte-identical, tracked twin in the repo, reachable by the lanes through GitHub sync.

**Not filed by this paste.** Filing them means choosing a destination directory, which is a
content decision for ATHENA and the operator, not a build step. `docs/history/` is the obvious
candidate for the two primers, given `FUNNEL_DIONYSUS_W1` and `HANDOFF_DIONYSUS_to_ATHENA` already
live there; `docs/knowledge/` is the obvious candidate for the trading-philosophy analysis, beside
`Naiad_Trading_Knowledge_Foundation_v0.md`. Recommended, not done.

---

## 7 · Findings carried forward from earlier this session, still open

- **The armed weekly backup task runs `backup_estate.py --estate` only.** No trigger runs
  `--workflow`, and the newest workflow archive is `naiad_workflow_2026-08-02.zip`, which predates
  every file created today — including `CONVENTIONS.md` and the memory snapshot. Their only
  off-machine copy is GitHub. Remedy, one command, operator's or ATHENA's call:
  `C:/venvs/naiad/Scripts/python.exe scripts/backup_estate.py --workflow --dest "G:/My Drive/naiad-backups"`
  Note that `CONVENTIONS.md` claims in §8 that a *workflow backup Sundays 08:30* trigger is armed.
  **That is not what the Task Scheduler contains** — the only weekly job is the estate one. Flagged
  for ATHENA as a §8 correction; not edited here, because this file is ATHENA's to amend and the
  correction is a content change, not a build step.
- **Large contract pastes exceed the OS argument limit.** Blocks around 30 KB and above fail with
  `ENAMETOOLONG` before any shell starts. They run correctly when written to a scratchpad file
  (outside the repo, so the assert-before-any-write property holds) and executed with `bash`, after
  verifying **0 CR bytes** with a Python binary read.

---

## 8 · What this session did NOT do

- Did not delete, move, or recreate `boxrescue/`.
- Did not edit any gate, or relax gate 4 to make the paste pass.
- Did not `git add` or `git commit` exchange files by hand — the guard staged them.
- Did not touch the data estate, the six untracked root files, or any other lane's report.
- Did not push anything outside `exchange/**`.

---

## 9 · FILE DISPOSITION TABLE

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY |
|---|---|---|---|---|---|
| `exchange/status/CONVENTIONS.md` | yes (31,015 B) | tracked | yes — `dde8523` | yes — `origin/v12-v1-census` | **GitHub only.** Inside `WORKFLOW_SOURCES` but the newest workflow archive (`naiad_workflow_2026-08-02.zip`) predates it — see §7 |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-03_CONVENTIONS.md` (this file) | yes | untracked at time of writing | **not committed** at time of writing | **no** at time of writing — publish runs next, §10 | **NOT PROTECTED** at time of writing |
| `boxrescue/` (26 files) | **yes — reappeared, see §6** | untracked | never committed | never pushed | **NOT PROTECTED.** Read-only in this paste; not created, moved or deleted by the builder |
| `boxrescue/Deep_Trading_Philosophy_Analysis_Four_Traders.md` | yes | untracked | never committed | never pushed | **NOT PROTECTED — exists nowhere else, §6.3** |
| `boxrescue/PRIMER_APOLLO_2026-08-01_v1_1.md` | yes | untracked | never committed | never pushed | **NOT PROTECTED — exists nowhere else, §6.3** |
| `boxrescue/PRIMER_DIONYSUS_2026-08-01_v1_1.md` | yes | untracked | never committed | never pushed | **NOT PROTECTED — exists nowhere else, §6.3** |
| `…\scratchpad\reconcile.py` (PART B script, executed copy) | yes | **outside the repository** — session scratchpad | n/a — intentionally never committed | n/a | **NOT PROTECTED**, by design |
| `…\scratchpad\conv_amend.md` (amendment text, executed copy) | yes | **outside the repository** — session scratchpad | n/a — intentionally never committed | n/a | **NOT PROTECTED**, by design; its content is now inside the published `CONVENTIONS.md` |
| `…\scratchpad\conv_amend.py` (amendment helper) | yes | **outside the repository** — session scratchpad | n/a | n/a | **NOT PROTECTED**, by design |
| `C:\Users\luisf\AppData\Local\Temp\conv_amend.md` / `.py` (the contract's own `/tmp` copies) | yes | **outside the repository** | n/a | n/a | **NOT PROTECTED**, by design; inert leftovers of the crashed step |

Committed ≠ pushed. Pushed ≠ backed up. "Not visible on GitHub" is usually the browser opening the
default branch `main` rather than `v12-v1-census`, which carries all project work.

---

## 10 · Publish of this report

Published with the same `publish_exchange.publish()` invocation immediately after this file was
written. The result is stated on screen in the session output; a report cannot honestly declare
the outcome of a command that runs after it is written. `git log -- exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-03_CONVENTIONS.md`
shows the commit that carried it.

---

## 11 · Exact artifacts for the operator

Repository root: `C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad`

| File | Full repo-relative path |
|---|---|
| The conventions file (the deliverable) | `exchange/status/CONVENTIONS.md` |
| This builder's report | `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-03_CONVENTIONS.md` |

Both reach the web lanes through GitHub sync — no hand-uploads. One operator action remains:
**click Sync now** in the Naiad project settings.

=== STATUS_HEPHAESTUS — 2026-08-03 ===
NOW: CONVENTIONS.md amended with the exact publish invocation, re-gated with case-insensitive
fragment checks, and published — commit dde8523, guard 0 offenders. All four PART A gates passed.
PART B blocked on attempt 1, completed on attempt 2: 26 box files, 23 IDENTICAL, 3 NOT IN REPO.
LAST EVENT: 2026-08-03 — dde8523 pushed to origin/v12-v1-census via publish_exchange.publish().
FACTS:
- Gates 1-4 all PASS; file 29,282 -> 31,015 bytes, 0 CR bytes, worktree clean vs blob [verified]
- publish() returned status=PUBLISHED commit=dde8523 pushed=True offenders=[] [verified]
- Three backslash/path failures across two pastes (bash path, /tmp literal, heredoc escape); all worked around from scratchpad, no gate altered [verified]
- boxrescue/ vanished then reappeared with mtime unchanged at 01:04; OneDrive dehydration is the leading hypothesis, cause [open]
- 3 box files exist nowhere else by hash AND by name: Deep_Trading_Philosophy_Analysis_Four_Traders.md, PRIMER_APOLLO_2026-08-01_v1_1.md, PRIMER_DIONYSUS_2026-08-01_v1_1.md [verified]
- CONVENTIONS.md §8 claims a workflow-backup trigger Sundays 08:30 that Task Scheduler does not contain [verified]
PENDING:
1. Operator: click Sync now in the Naiad project settings
2. Operator/ATHENA: file the 3 NOT-IN-REPO files before deleting anything from the project box
3. ATHENA: correct §8's trigger claim; arm or hand-run backup_estate.py --workflow
NEXT: file the three orphans, then the 23 IDENTICAL box copies can be removed. Owner: ATHENA.
METRICS: operator actions this session = 2 · files re-ingested = 0
=== END STATUS ===
