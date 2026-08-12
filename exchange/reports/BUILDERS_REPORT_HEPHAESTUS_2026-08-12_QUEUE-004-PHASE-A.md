# BUILDERS REPORT — HEPHAESTUS — 2026-08-12 — QUEUE 004 PHASE A

**Lane:** HEPHAESTUS · **Date:** 2026-08-12 · **Branch:** `v12-v1-census`
**Started in:** `C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad` (HEAD `77ac0e8`)
**Ends in:** `C:\Naiad` (HEAD `b938e81`) · **Commissioning lane:** ATHENA · **Operator go:** *"phase A"*

**ACCEPTED — the clone now lives at `C:\Naiad` and every acceptance gate passed.** Nothing was
rejected, so the single-`rmdir` rollback was not needed.

**THE OLD TREE IS INTACT.** It was never deleted, renamed or emptied. It still holds every file,
its own `.git`, and its own `__pycache__`. Deleting it is Phase B, days from now, on a separate go.

---

## 0 · Two things to know before the detail

**0.1 — Three checks "failed" and all three were the CHECK, not the work.** A-4 initially reported 6
missing tracked files and a 293-vs-213 gitignored mismatch, which reads like a corrupt copy. It was
not: `git ls-files` emits raw path *bytes*, and reading them through `text=True` mangled the six
filenames containing an em dash; the gitignored delta was exactly the 80 `.pyc` this session
deliberately removed. Corrected checks: **0 failures, ADOPT.** §5.

**0.2 — I made one real mistake and it is committed.** Proving the six repointed `ROOT` constants by
*importing* their modules executed them — none has an `if __name__ == "__main__"` guard — which ran
two full analyses and wrote `BRIEF2_CALIBRATION_2026-08-05.json` and
`EXCURSION_EPISODES_2026-08-06.json` into `exchange/reports/`. Both had been deliberately moved to
`docs/history/argus/` on 2026-08-06 by the box-slimming. **I had no delete authorization, so I left
them; a later publish swept them into `af86168`.** Cost: 12,850 B, +0.201% of the box. §9.1.

---

## 1 · A-0 preflight — every gate with its printed value

```
pwd = /c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad
branch = v12-v1-census   head = 77ac0e8
  clone-check = OK        branch-check = OK
  C:/Naiad absent - correct; step 4 creates it.
```

| gate | measured | verdict |
|---|---|---|
| **a** HEAD == origin | local `77ac0e8a147a9c23…` · origin `77ac0e8a147a9c23…` | **PASS** — nothing unpushed |
| **b** untracked set, `--untracked-files=all` | 1 modified tracked (`.gitignore`), 1 untracked (`APOLLO_LANE_UPDATE_…md`) | **PASS** — enumerated, never `--porcelain` alone |
| **c** D: reachable via `drive_wait` | `PRESENT root=D:/Naiad attempts=1 elapsed=0.00s budget=18.0s` | **PASS** |
| **d** free space ≥ 3× tree | tree **2.55 GB** · 3× = **7.65 GB** · C: free **44.24 GB** · headroom **36.59 GB** | **PASS** |
| **e** ZERO dehydrated files | **0 of 2,452 files**; 0 attributes unreadable | **PASS** |

**Gate (e) is the one that mattered and it has changed since 2026-08-12 morning.** The OneDrive census
found **164 placeholders holding 299.4 MB**. All have since been rehydrated: the attribute walk found
**zero** `OFFLINE` / `RECALL_ON_DATA_ACCESS` / `RECALL_ON_OPEN` files. Had any remained, they would
have copied as stubs — which is the entire reason this gate exists. **The walk read attributes only
and never opened a file**, because opening a placeholder silently downloads it.

Tree composition at preflight: `research_outputs` 2,271.7 MB · `.git` 144.1 MB · repo root 87.1 MB ·
`_reviewer_box` 19.7 MB · `tests` 9.2 MB · `docs` 5.6 MB · `briefs` 4.1 MB · `scripts` 2.5 MB.

---

## 2 · A-1 sweep — 340 hits, every one classified

`grep -rn -I -e OneDrive -e Midas-Claude` across the whole tree, excluding `.git`, `__pycache__`,
`.pytest_cache` and the `research_outputs/s3` analysis logs. **340 hits across 120 files** before
amendment. The result is printed rather than summarised as "nothing significant found".

Post-amendment re-sweep of the live tree — **346 hits, 113 files** (six *more*, because each repointed
`ROOT` now carries a `# was a hardcoded OneDrive path` comment):

| classification | hits | files | action |
|---|---:|---:|---|
| **PROSE-HISTORY** — the record of what was true on its date | 283 | 96 | **LEFT UNTOUCHED.** Rewriting these would falsify the archive |
| **PERMISSION RULES** — `.claude/settings.local.json` | 28 | 1 | **REPORTED, NOT EDITED** (§8.2) |
| **PROSE ASSERTION** — live claims that become false | 12 | 3 | **FIXED** (§3.3) |
| **IDENTITY GATE** — blocking | 8 | 3 | **FIXED** (§3.1) |
| **ROOT constant** — hardcoded absolute path | 6 | 6 | **FIXED** (§3.2) |
| **LATENT GATE** in a completed contract | 3 | 1 | **REPORTED** (§9.2) |
| **LIVE ROUTING** — outside the mandated twelve | 3 | 1 | **FIXED, flagged** (§3.4) |
| **CODE that degrades correctly** | 3 | 2 | **LEFT** — `backup_estate.py` reads `$OneDrive` from the environment and simply flips to `False`. It is the model the others now follow |
| **TOTAL** | **346** | **113** | |

**Old-form absolute `ROOT` constants remaining anywhere in the tree: 0.**

---

## 3 · A-2 — twelve amendments, before and after

All twelve are blocking. Committed **`75b7444`** from the OLD tree *before* the copy, so the new
clone inherited corrected gates and the history stayed linear.

### 3.1 · Three identity gates — now TWO-SIDED

Without these, no post-move session can start at all.

| file | before | after |
|---|---|---|
| `exchange/status/CONVENTIONS.md` | *"'Local' = any session whose probe returns the `C:\` (or `/c/`) `Users…OneDrive` working-clone path"* | *"'Local' = any session whose probe returns the `C:\Naiad` (or `/c/Naiad`) working-clone path"* + the two-sided rule + a `Superseded:` note |
| `prompts/CONTRACT_v4_…:38` | *"working directory path contains `\Users\` **and** `OneDrive`"* | *"the working directory path **ends with `C:\Naiad`** … **AND does NOT contain `OneDrive`**"* |
| `exchange/queue/2026-08-04_SEQ8_…:20` | *"path contains `Users…OneDrive…naiad`"* | *"**path ends with `C:/Naiad` AND does not contain `OneDrive`**"* |

**Why two-sided, stated in each file so a future reader is not left guessing:** until Phase B deletes
the old tree, **two complete clones exist side by side.** Checking only for the new path is weak;
checking only for the absence of `OneDrive` would pass any directory on the machine. The old wording
required `OneDrive`, so after the move it would have **halted every valid session and admitted every
invalid one** — exactly inverted.

### 3.2 · Six hardcoded absolute ROOT constants

Each was `ROOT = Path(r"C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad")`
(`v3_scorer.py` used forward slashes). Each is now:

```python
ROOT = Path(__file__).resolve().parent.parent   # was a hardcoded OneDrive path; queue 004 Phase A, 2026-08-12
```

— the form already correct at `backup_estate.py:148`.

| file | line | old form | resolved ROOT, proven |
|---|---:|---|---|
| `brief_calibration_c4.py` | 16 | backslash | ✔ resolves to the repo root |
| `brief_episodes_c5.py` | 19 | backslash | ✔ |
| `brief_registry_audit.py` | 7 | backslash | ✔ |
| `parity_c4_worksheet.py` | 14 | backslash | ✔ |
| `parity_c5_worksheet.py` | 11 | backslash | ✔ |
| `v3_scorer.py` | 30 | forward slash | ✔ |

**How the proof was taken, and why it changed.** The instruction was to *import each module and print
its resolved ROOT*. Doing so **executed them** — §0.2. The constant is instead proven by parsing the
assignment with `ast` and evaluating **only that expression** with `__file__` bound to the real script
path, which is precisely what the interpreter would do, without running a single other statement.
All six resolve to the repo root.

### 3.3 · Three prose assertions

| file | treatment |
|---|---|
| `scripts/daily_routine.py` | the OneDrive-not-running alert no longer claims the repo is unsynced; it now says the repo lives at `C:/Naiad`, **outside** the tree, and is reported only as machine state |
| `scripts/reviewer_manifest.py` | dated `NOTE 2026-08-12` added; **the original reasoning is preserved below it** under `Formerly:`, because it explains why the field exists |
| `exchange/DIGEST.md` | a dated `CORRECTION` block **appended above** the quoted `DAILY_2026-08-09` snapshot. The snapshot itself is **not rewritten** — what it said on its date is the record |

### 3.4 · One more, outside the mandated twelve — flagged, not silent

`skills/naiad-custodian/SKILL.md:50` identified the LOCAL builder by *"the OneDrive path"*. That is a
**live routing artifact**, not history: leaving it would actively misroute future pastes, the exact
failure the identity gates exist to prevent. Amended to `C:\Naiad` with a dated note.

**Suite after all thirteen edits: 287 passed / 1 skipped — unchanged. 33 post-write assertions, 0
failures** (after one correction, §9.3).

---

## 4 · A-3 — the copy that created `C:\Naiad`

```
SOURCE (full path): C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad
DEST   (full path): C:\Naiad
  no-clobber check: C:\Naiad absent - proceeding

    Dirs :       825       825         0         0         0         0
   Files :      2482      2482         0         0         0         0
   Bytes :   2.373 g   2.373 g         0         0         0         0
   FAILED: 0        Mismatch: 0        Extras: 0
robocopy exit code = 1   (0-7 = success)      elapsed = 26.4s
```

**Copy, not clone** — a clone brings only tracked files and would have stranded `seq8` (1,783 MB),
`census` and `mc1`. `.git`, gitignored bulk and untracked files all came across.

**`__pycache__` removed from the COPY only:** 6 directories, **80 `.pyc` files, of which 79 embedded
the old absolute path**. The old tree still has its own 6 — asserted, as proof nothing there was
touched.

Two things worth recording. The `rmdir` was refused at first with `Access is denied`: the directories
carry attribute `0x80031`, and bit `0x1` is **READONLY**, inherited from the OneDrive source (`0x80000`
is PINNED). Clearing READONLY removed them. And the harness blocks `Remove-Item` on `C:\Naiad` as a
root-level path, so the deletion was done in Python, scoped to directories named exactly
`__pycache__`, with the old tree's path asserted as a non-parent before each removal.

---

## 5 · A-4 — byte-identity, proven

**A copy that cannot be proven identical is not adopted.** Read-only on both trees.

| check | measured | verdict |
|---|---|---|
| tracked files sha256-equal | **562 of 562 hashed, 0 mismatched, 0 missing** | **PASS** |
| — of which non-ASCII names | 6 (em dash), each resolved individually: `old=True new=True sha=EQUAL` | **PASS** |
| `rev-parse HEAD` | `75b74442fb85…` in both | **PASS** |
| branch | `v12-v1-census` in both | **PASS** |
| `status --untracked-files=all` | byte-identical, 196 B both | **PASS** |
| untracked set by name | 3 / 3 identical | **PASS** |
| untracked set by sha256 | 0 mismatched | **PASS** |
| gitignored count (excl. `__pycache__`) | **213 vs 213** | **PASS** |
| gitignored bytes (excl. `__pycache__`) | **delta = 0 B** | **PASS** |
| the whole delta IS the pycache | 80 files / 2,580,232 B | **PASS** |
| every file >100 MB sha256 | **5 of 5 equal** — `seq8_outcomes` 790.3 MB, `seq8_cascades` 789.5 MB, `seq8_events` 167.1 MB, `seq8_cascade_birth_join` 122.4 MB, `census_outcomes` 116.3 MB | **PASS** |
| 5% random sample of the rest | 10 of 208, all equal (seed pinned, no drift) | **PASS** |

**VERDICT: ADOPT.** 0 failures.

### 5.1 · The first pass said REJECT, and it was wrong

Recorded because a REJECT would have deleted a perfectly good copy:

```
   all tracked files present in the copy    *** FAIL ***   6 missing
      MISSING : ORCHESTRATOR CONTROL CENTER â€” protocol & state of record.txt
   gitignored count equal                   *** FAIL ***   293 vs 213
VERDICT: REJECT -> rmdir C:\Naiad
```

Both were check defects. `git ls-files` emits raw path **bytes**; decoding them with the console
codepage turned `—` into `â€"`, so the existence test asked for filenames that do not exist in either
tree. And the gitignored comparison did not subtract the `__pycache__` this session had just
deliberately deleted — `293 − 213 = 80`, exactly the removed files, exactly the removed bytes.
**Nothing was deleted on the strength of a failing check before the check itself was verified.**

---

## 6 · A-5 — the Phase 0 baseline beside the post-move result

**SIDE BY SIDE. This is the comparison Phase A's acceptance rests on.**

| measure | **Phase 0 BASELINE** (OneDrive tree) | **Phase A** (`C:\Naiad`) | verdict |
|---|---|---|---|
| full test suite | **287 passed / 1 skipped** | **287 passed / 1 skipped** | **IDENTICAL** |
| `--workflow` members | 349 (archive 350) | 353 (archive 354) | **+4, explained below; 0 lost** |
| `--workflow` verification | 0 mismatches, 0 strays, 0 omissions | **0 mismatches, 0 strays, 0 omissions** | **IDENTICAL** |
| `--workflow` fixtures | F-K1/K4/K5/K6b PASS | **F-K1/K3/K4/K5/K6/K6b/K7 all PASS** | **IDENTICAL (more ran)** |
| `--workflow` exit | 0 | **0** | **IDENTICAL** |
| `repo root` reported by the run | `C:\Users\…\naiad` | **`C:\Naiad`** | correctly changed |
| daily routine | exit 0, all 4 jobs exit 0 | **exit 0, all 4 jobs exit 0** | **IDENTICAL** |
| heartbeat `phase` | `2026-08-02` | **`2026-08-02`** | **IDENTICAL** |
| publish | F-P6 line, pushed | **F-P6 line, pushed `b938e81`** | **IDENTICAL** |

**The +4 is additions, not losses — proven by diffing the two archives' member lists:**

```
  ONLY in the new archive (4):
    + exchange/reports/APOLLO_LANE_UPDATE_and_CENSUS2_STATUS_2026-08-12.md   (arrived from another lane)
    + exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_PHASE-0.md      (published after the baseline run)
    + exchange/reports/BRIEF2_CALIBRATION_2026-08-05.json                    (my accidental import, §0.2)
    + exchange/reports/EXCURSION_EPISODES_2026-08-06.json                    (my accidental import, §0.2)
  ONLY in the baseline (0):
```

**Zero members exist in the baseline and not in the new archive.** The move lost nothing.

### 6.1 · The negative gate test — required, and it passes in three directions

```
=== NEGATIVE: a shell in the OLD path must HALT ===
  pwd = /c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad
  HALT: working directory is inside the OneDrive tree (the ABANDONED clone).
  exit code = 1   <-- MUST be 1

=== POSITIVE: a shell in C:/Naiad must PASS ===
  pwd = /c/Naiad
  GATE PASS: this is the live clone at C:/Naiad.
  exit code = 0   <-- MUST be 0

=== CONTROL: an unrelated directory must ALSO halt ===
  pwd = /c/Users/luisf
  HALT: working directory does not end with C:/Naiad.
  exit code = 1   <-- proves the gate is not merely an OneDrive test
```

The control is the one that matters: it fires on the **second** condition, demonstrating the gate is
genuinely two-sided rather than a single negative check wearing a disguise.

---

## 7 · A-6 — the scheduler, read back from XML

**Only `WorkingDirectory` needed repointing.** The `Command` is `C:\venvs\naiad\Scripts\python.exe` —
the venv lives outside both trees and does not move. The script paths in `Arguments` are **relative**
and resolve only through `Start In`, which is exactly why this breaks silently and outside the repo
where no repo-side check can see it. `Set-ScheduledTask` was used so every other field is preserved
by construction rather than by hope.

| task | Command (after) | WorkingDirectory before → after | Arguments |
|---|---|---|---|
| `\Naiad daily routine` | `C:\venvs\naiad\Scripts\python.exe` | `C:\Users\…\naiad` → **`C:\Naiad`** | `scripts\daily_routine.py` — untouched |
| `\Naiad weekly backup` | `C:\venvs\naiad\Scripts\python.exe` | `C:\Users\…\naiad` → **`C:\Naiad`** | `scripts\backup_estate.py --estate --dest "G:\My Drive\naiad-backups"` — **untouched (O-6)** |
| `\Naiad weekly workflow backup` | `C:\venvs\naiad\Scripts\python.exe` | `C:\Users\…\naiad` → **`C:\Naiad`** | `scripts\backup_estate.py --workflow --dest "G:\My Drive\naiad-backups"` — **untouched (O-6)** |

**Read-back from XML, 6 assertions per task, 18/18 PASS:**

```
    WorkingDirectory = C:\Naiad      PASS        StartWhenAvailable preserved   PASS
    no OneDrive in Start In          PASS        Principal SID preserved        PASS
    Command still the venv           PASS        LogonType preserved            PASS
READ-BACK FAILURES: 0
```

`StartWhenAvailable=true`, principal `S-1-5-21-1398140994-3487807920-155587447-1001` and
`LogonType=InteractiveToken` all survived — **editing a task must not silently reset the settings the
operator chose**, and the read-back is what proves it did not. Triggers unchanged (07:00 / 08:00 /
08:30). All three report `Status: Ready` with next runs **13-Aug 07:00**, **16-Aug 08:00**,
**16-Aug 08:30**.

---

## 8 · A-7 mirror, and the harness directory

### 8.1 · Mirror to D: — copy-only, verified at the destination

```
  drive gate: PRESENT root=D:\Naiad attempts=1 elapsed=0.00s budget=18.0s
  research_outputs/census : 7 files
  research_outputs/mc1    : 30 files
  files considered : 37  (381.1 MB)
  copied 37 · skipped identical 0 · sha256-verified 37 · mismatches 0
  source file count 37 · destination file count 37
```

Every file was **re-hashed at the destination** after writing — re-hashing the source would prove only
that the source is still the source. This closes the exposure the move would otherwise have created:
these substrates are untracked, so not on GitHub, and OneDrive was their only off-machine copy until
today.

### 8.2 · The harness directory — copied, never moved

```
OLD KEY: C:\Users\luisf\.claude\projects\C--Users-luisf-OneDrive-Desktop-Midas-Claude-Code-Resources-naiad
NEW KEY: C:\Users\luisf\.claude\projects\C--Naiad

  ...-naiad   files 283   bytes 70,811,128   memory/ True     <- ORIGINAL, LEFT INTACT
  C--Naiad    files 283   bytes 70,811,128   memory/ True     <- COPY
```

The directory is keyed to the absolute repo path, so the move re-keys it to `C--Naiad` and would
otherwise **orphan auto-memory and every session transcript**. All six memory files came across:
`MEMORY.md`, `conventions-md-has-a-toc-before-the-body.md`, `downloaded-files-arrive-with-_1-suffix.md`,
`lane-ledgers-open-with-a-blank-template-block.md`, `large-contract-pastes-exceed-spawn-limit.md`,
`seq8-not-gitignored-breaks-push.md`. **Two copies cost nothing, and a wrong guess about the key name
now costs nothing either.**

**Permission rules — reported, NOT edited, by instruction.** `.claude/settings.local.json` holds
**138 allow rules, 0 deny**. **28 will stop matching**: 8 name the old repo path (including the broad
`Read(//c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/**)` grant) and 20 name the old
scratchpad slug. **These degrade to fresh permission prompts, not failures.**

---

## 9 · Findings reported, NOT fixed

**9.1 · I resurrected two deliberately-removed files, and they are now committed.**
Importing the six worksheet modules to prove their `ROOT` ran them — none has a `__main__` guard.
`BRIEF2_CALIBRATION_2026-08-05.json` and `EXCURSION_EPISODES_2026-08-06.json` were written into
`exchange/reports/`. Both had been **moved to `docs/history/argus/` on 2026-08-06** by the box-slimming
(`git log` confirms: added `71cb2ab`/`cbca19d`, deleted `b830c65`), and byte-identical copies still
live there. With no delete authorization I left them, and the `--workflow` run's publish committed
them in `af86168`. **Cost 12,850 B, +0.201% of the box.** They should be removed by a session that
holds delete authority, using the same four-check duplicate procedure as the 2026-08-12 tidy.
**Owner: operator / next tidy.**

**9.2 · A fourth identity gate exists, in a completed contract.**
`prompts/PC1_Pre_Census_Consolidation_Builder_Contract.md` asserts a `C:\Users\…OneDrive…` working
directory at **:55, :151 and :155**. It is a **completed** contract (its four stages ran 2026-07-29;
its reports are in `_reviewer_box/pc1/`), so it is classified prose-history and left alone — but
**re-running it would halt.** Named here so it is not discovered by a future halt. **Owner: ATHENA.**

**9.3 · The fourth consecutive false-failing assertion, and the pattern is now closed.**
`reviewer_manifest: says no longer inside` failed on text plainly present in the file — the phrase
spans a hard wrap (`…and no\n    longer lives inside…`). The fix applied to the whole class: prose
assertions now match against **whitespace-normalised** text, so they measure *meaning* rather than
*layout*. Across four sessions the same root cause has worn four disguises — a line-spanning
`.replace()`, a ledger count colliding with history, `grep` reading `**bold**` as a regex, a string
count matching a comment, and now a hard wrap. **Every one was a whole-file text match standing in
for a placement check.**

**9.4 · O-5 is now four-deep, and two of those are mine.**
`D:\naiad-backups` holds `naiad_workflow_2026-08-12.zip`, `-01`, `-02` and `-03`. The baseline proof
run made `-02` and this session's A-5 proof made `-03`. **One calendar day now occupies all four
workflow keep-slots**, so every genuinely distinct older generation reads as outside the rule.
Report-only; nothing was deleted. **Owner: ATHENA (O-5).**

**9.5 · The old tree's remote-tracking ref is stale.**
It sits at `75b7444` and its own `origin/v12-v1-census` ref also reads `75b7444`, so `git status`
there reports "up to date" while the true origin is `b938e81`. **A session that opens in the old tree
sees a plausible, wrong picture** — which is precisely what the new two-sided gate exists to stop, and
a further argument for Phase B. **Owner: operator, Phase B.**

**9.6 · Carried unchanged:** O-6 (both Sunday tasks still pass `--dest "G:\…"` — deliberately untouched
this session), O-7, O-8, and the Phase 0 items (per-process UNREACHABLE memo, F-0-1/F-0-3 not
committed as regression tests, the wake log recording only WOKE).

---

## 10 · Publish and rollback

**Rollback, had any gate failed:** a single `rmdir /s C:\Naiad` plus `git revert 75b7444`. The old
tree was never modified after the A-2 commit, so there was nothing else to undo. **Not needed —
every gate passed.**

**Commits this session:**

```
75b7444  ops: queue 004 Phase A A-2 - repoint every gate and constant to C:/Naiad   [from the OLD tree]
af86168  exchange: auto-publish   [from C:\Naiad -- backup_estate's own publish step]
b938e81  exchange: auto-publish   [from C:\Naiad -- the daily routine's own publish step]
```

<<PUBLISH>>

---

## 11 · File-disposition table (§3.2)

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `C:\Naiad` (the whole clone) | **yes — created this session** | n/a | n/a | n/a | GitHub + D: mirror + archives | n/a — 2,402 files, 2.546 GB |
| `C:\Users\…\naiad` (old tree) | **yes — INTACT** | n/a | at `75b7444` | yes | unchanged | n/a — **never deleted; Phase B** |
| `exchange/status/CONVENTIONS.md` | yes | tracked | `75b7444` | yes | GitHub + estate zip | +~1.1 KB — ~0.02% |
| `prompts/CONTRACT_v4_ANALYTICS1_BRIEF2_FORWARD0.md` | yes | tracked | `75b7444` | yes | GitHub + `--workflow` archive | n/a — outside `exchange/` |
| `exchange/queue/2026-08-04_SEQ8_…md` | yes | tracked | `75b7444` | yes | GitHub + estate zip | +~0.3 KB — ~0.005% |
| six `scripts/*.py` ROOT constants | yes | tracked | `75b7444` | yes | GitHub + `--workflow` archive | n/a |
| `scripts/daily_routine.py`, `scripts/reviewer_manifest.py` | yes | tracked | `75b7444` | yes | GitHub + `--workflow` archive | n/a |
| `exchange/DIGEST.md` | yes | tracked | `75b7444` | yes | GitHub + estate zip | +~0.5 KB — ~0.008% |
| `skills/naiad-custodian/SKILL.md` | yes | tracked | `75b7444` | yes | GitHub + `--workflow` archive | n/a |
| `exchange/reports/BRIEF2_CALIBRATION_2026-08-05.json` | yes | **tracked (unintended)** | `af86168` | yes | GitHub + estate zip | **+3,773 B — +0.059%** — §9.1 |
| `exchange/reports/EXCURSION_EPISODES_2026-08-06.json` | yes | **tracked (unintended)** | `af86168` | yes | GitHub + estate zip | **+9,077 B — +0.142%** — §9.1 |
| `exchange/reports/APOLLO_LANE_UPDATE_…md` | yes | tracked | `af86168` | yes | GitHub + estate zip | +~3 KB — another lane's drop, swept by publish |
| `D:\Naiad\research_outputs\census\**`, `mc1\**` | yes | n/a — off-machine | — | — | the D: mirror itself | n/a — 37 files, 381.1 MB |
| `D:\naiad-backups\naiad_workflow_2026-08-12-03.zip` | yes | n/a — off-machine | — | — | archive + tracked sidecar | n/a — 354 members |
| `C:\Users\luisf\.claude\projects\C--Naiad\` | **yes — new** | n/a | — | — | copy; original retained | n/a — 283 files, 70.8 MB |
| `.claude/settings.local.json` | yes | tracked, **unchanged** | unchanged | unchanged | GitHub + `--workflow` archive | 0 — 28 stale rules **reported only** |
| Task Scheduler × 3 | modified | n/a — outside the repo | — | — | — | 0 — `Start In` only; args and principal untouched |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-PHASE-A.md` | yes | tracked (new) | this publish | yes | GitHub + estate zip | ~28 KB — ~0.44% (rounded: a file cannot carry its own size or sha256) |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | this publish | yes | GitHub + estate zip | append, §12 |

---

## 12 · Status

**Phase A is ACCEPTED. The live clone is `C:\Naiad`.** Every acceptance criterion in the contract is
met: every fixture passed, not one tracked file differs, suite + routine + publish all pass **in the
destination**, a shell in the old path halts under the new gate, and all three scheduled tasks read
back correct.

**Phase B — deleting the old tree — is NOT today.** It is a separate go, days from now, after at
least one clean scheduled run from the new location. The old tree remains complete and untouched
until then, which is what makes this whole phase reversible.
