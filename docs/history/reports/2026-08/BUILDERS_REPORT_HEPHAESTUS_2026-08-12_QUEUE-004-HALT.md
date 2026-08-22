# BUILDERS REPORT — HEPHAESTUS — 2026-08-12 — QUEUE 004: HALT, CONTRACT ABSENT

**Lane:** HEPHAESTUS · **Date:** 2026-08-12 · **Branch:** `v12-v1-census` · **HEAD at start:** `0305179`
**Commissioning lane:** ATHENA · **Scope:** `exchange/queue/004_move-clone-out-of-onedrive.md` ONLY.

**Nothing was written to `exchange/queue/`. No file was created, modified, moved or deleted by the
edit paste. No code was written. Nothing was moved to `C:/Naiad`.** The only files this session
creates are this report and its ledger entry.

---

## 0 · Two departures from the paste, stated first so they can be overruled

**0.1 — The paste's own gate halted it. `exchange/queue/004_move-clone-out-of-onedrive.md` does not
exist.** It is not on disk, not tracked, and no commit on any branch has ever touched it. The queue
runs 001, 002, 003 and stops. Nothing was amended because there was nothing to amend.

**0.2 — This report is filed as `…_QUEUE-004-HALT.md`, not the mandated
`…_QUEUE-004-RATIFIED.md`.** The mandated filename asserts, in the index that every future session
reads, that queue 004 is ratified. It is not; it does not exist. Filing a false fact under a
filename is the failure CONVENTIONS §0 names, and §3.1 already instructs this lane to refuse
defective AFTER-lines rather than execute them. **If the operator wants the mandated name
regardless, this is one `git mv` from compliance** — say so and it changes.

Everything else in the paste was followed exactly.

---

## 1 · Gate values, as printed

The paste's four preflight gates. The first three passed; the fourth halted the run before the
Python heredoc was reached, so **no bytes were ever at risk**.

```
pwd=/c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad
branch=v12-v1-census  head=0305179
clone-check=OK
branch-check=OK
HALT: 004 missing
```

Exit code 1, at the line `[ -f exchange/queue/004_move-clone-out-of-onedrive.md ] || { echo "HALT: 004 missing"; exit 1; }`.

**What is actually in the queue:**

```
exchange/queue/001_condensed-project-history.md          RATIFIED operator 2026-08-06
exchange/queue/002_backup-and-publish-guards.md          RATIFIED operator 2026-08-04 · BUILT c32ffa5
exchange/queue/003_report-rotation-and-provenance.md     RATIFIED operator 2026-08-11
exchange/queue/2026-08-03_WF1_winner_forensics_APOLLO.md
exchange/queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md
exchange/queue/2026-08-06_MC1_may26_program_APOLLO.md
exchange/queue/README.md
```

---

## 2 · The absence was proved, not assumed

The `_1`-suffix lesson says an exact-filename gate can halt on a file that is really present under a
near-miss name. Six independent checks; all negative.

| # | check | result |
|---|---|---|
| 1 | `find . -iname "*004*"` (repo, excl. `.git`) | **0 hits** |
| 2 | `find . -iname "*move-clone*" -o -iname "*out-of-onedrive*"` | **0 hits** |
| 3 | `git log --all -- "exchange/queue/004*" "*move-clone*"` | **0 commits, any branch** — never committed, so not a deletion |
| 4 | `grep -r "move-clone-out-of-onedrive\|queue/004\|QUEUE-004"` | **0 hits** — no other file references it |
| 5 | `git status` / `git stash list` | clean but ` M .gitignore`; **no stash** |
| 6 | Downloads, Desktop, Documents — `*004*`, `*move-clone*`, `*onedrive*` | **0 hits** |

Also negative, and jointly decisive: **`C:/Naiad` appears nowhere in the repo**, and neither does
the string `Proposed destination`. The paste's anchors `A1`, `A2`, `A3` have **zero** possible
targets — not a wrong-anchor problem, an absent-file problem.

**What the paste's stamp line actually is.** `RATIFIED: **PENDING** — operator ratifies with one
word. Drafted: ATHENA, 2026-08-12.` is character-for-character the 003 stamp from 2026-08-11
(recorded at `BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-003-RATIFIED.md:23`) with the date
advanced. **004 was drafted in a session whose output never reached this repo.** The contract text
exists somewhere; it is not here. This is the same class as the 2026-08-12 operator ruling "file
it" — work that is real but unfiled.

---

## 3 · Post-write assertions: none ran, because no write occurred

Stated explicitly rather than omitted, because a missing assertions section reads like a skipped
check. The paste declared seven. **All seven are vacuous** — six describe a file that does not
exist, and the seventh (`file grew`) would compare against an empty read.

```
  POST-WRITE ASSERTIONS
   stamp replaced, PENDING gone        NOT RUN — no file
   destination pinned to C:/Naiad      NOT RUN — no file
   Phase 0 present exactly once        NOT RUN — no file
   Phase A survived                    NOT RUN — no file
   Phase B survived                    NOT RUN — no file
   file grew                           NOT RUN — no file
   line endings preserved              NOT RUN — no file
```

**A latent defect in the paste, worth fixing before it is re-run against a real 004.** Had the file
existed but the anchors not matched, `open(P,'wb').write(...)` at the end would still have fired and
rewritten the file unchanged — and the three assertions keyed to *new* strings would have failed
loudly, but `file grew` and `line endings preserved` would have passed. More importantly, the
Phase 0 insertion has a silent-no-op path of exactly the 2026-08-11 kind:

```python
if ('## PHASE 0' not in s) and ('## PHASE A' in s):
    s=s.replace('---'+eol+eol+'## PHASE A', P0, 1) if ('---'+eol+eol+'## PHASE A') in s else s.replace(...)
```

If `## PHASE A` is absent — say the contract calls it `## Phase A` — **both branches are skipped and
the whole conditional evaluates to nothing**, no exception, no message. The assertion
`Phase 0 present exactly once` would catch it, which is the improvement over 2026-08-11. But
`Phase A survived` and `Phase B survived` assert `count(...)==1` on strings the edit never touched:
they pass whether or not the edit worked, and would pass on a file where Phase 0 silently failed to
land. **Two of the seven assertions cannot fail.** Assertions that cannot fail are the counting
guard this project has now been bitten by three times.

### 3.1 · The one write this session did make, and the assertion that failed on it

The ledger append (§0, ruling "append") is the session's only edit to a tracked file. It ran under
the same discipline: whole-file read → append → whole-file write, context printed first, assertions
after. **Ten assertions, nine PASS, one FAIL:**

```
   STATUS block count +1                PASS        prior content intact (prefix match)  PASS
   END STATUS balanced                  *** FAIL ***    file grew                        PASS
   new NEXT line present                PASS        line endings preserved               PASS
   halt fact present                    PASS        utf-8 decodes clean                  PASS
   premise-refuted fact present         PASS        report filename referenced           PASS

   bytes 32374 -> 36710  (+4336)   CRLF=0  blocks=14
```

**The failure was in the assertion, not the file — and it is worth recording because the
distinction is the whole point of asserting.** `END STATUS balanced` required
`count('=== END STATUS ===') == count('=== STATUS_ATHENA')`. Measured: 15 closers, 14 openers. The
extra closer is **pre-existing and correct**: line 11 of the ledger holds a blank
`=== STATUS_<LANE> — <date> ===` template, closed at line 18, which is not an ATHENA block. The
imbalance predates this session by every commit in the file's history.

Re-run with the template accounted for, all seven structural checks pass — block opens at line 311,
closes at 332, exactly one `NEXT:`, file ends on a terminated block:

```
   real ATHENA blocks == 14         PASS      my block closes at 332        PASS
   closers == blocks + template     PASS      no unterminated block         PASS
   template present, uncounted      PASS      exactly one NEXT in my block  PASS
   my block opens at 311            PASS
```

**Nothing was corrected in the file, because nothing in the file was wrong.** A guard that fires on
a healthy artifact is a false halt, and this project has already paid for one of those — the
`prompts/CONTRACT_v4` §0.1 rationale at §5 item 5 exists because a pinned-HEAD gate produced exactly
this failure mode. The lesson is symmetrical with the one Phase 0's D-0d is reaching for: **a
failing check measures the check first.**

---

## 4 · The amendment's factual claims, checked against the code

Six independent verifications were run — not to second-guess the drafter, but because the report
must say whether the amendment is *buildable*, and a ratification stamp is cheap to apply and
expensive to retract. **Two claims confirm, one is under-specified by a factor of three, two are
false, and the premise that motivates the entire phase is refuted.**

### 4.1 · D-0c / O-5 retention grouping — **CONFIRMED, and worse than described**

`scripts/backup_estate.py:976-998`. There is no generation key at all: the sort key is the whole
filename (`key=lambda p: p.name`) and the keep set is a raw slice `gens[:keep_n]`. No date
extraction, no day grouping. The `DATED_ZIP` regex at `:179` — which would *not* match a `-NN` name
— is used only at `:1090` for a display column and never touches `_generations()`.

`-NN` siblings are produced deliberately by `assert_no_clobber()` (`:535-542`, wired at `:1150` and
`:1233` under `--force-same-day`). The double-slot is **live in the committed report**, not
hypothetical — `exchange/status/RETENTION.md:31-34`:

```
| `naiad_workflow_2026-08-12.zip`    | 2,749,895 | yes |
| `naiad_workflow_2026-08-12-01.zip` | 3,579,058 | yes |
| `naiad_workflow_2026-08-11.zip`    | 2,721,722 | yes |
| `naiad_workflow_2026-08-09.zip`    | 2,529,667 | yes |
```

Four keep-slots covering **three** calendar days; `naiad_workflow_2026-08-04.zip` is pushed to
"outside the rule" one generation early as a direct result.

**New defect found while verifying, not in the amendment:** the lexicographic sort is *inverted*
within a day. `.` (0x2E) sorts above `-` (0x2D), so `…2026-08-12.zip` ranks above
`…2026-08-12-01.zip` — but mtimes show `-01` was written at 03:45 and the bare name at 02:47. **The
newer same-day archive is ranked as the older generation**, so it is the first of that day to be
labelled prunable. Any grouping fix must fix the ordering too, or it will keep the wrong file.
Also present: `naiad_workflow_2026-08-02 (1).zip`, a OneDrive-style duplicate hitting the same bug
from a different direction — so the fix must handle ` (N)` as well as `-NN`.

The amendment's "report-only, must not start deleting" is **exactly right**: `retention_report()`
never mutates (`:951`, `:963`, `:972-973`), and every `unlink`/`rmtree` in the 1,531-line file is
outside the retention path.

### 4.2 · Fixture F-0-4 "expect 287/1" — **CONFIRMED**

Plain pytest, `pytest.ini`, `testpaths = fixtures tests`. 287 passed / 1 skipped is current, is
recorded in multiple places including today, and a live collect-only returns 288 items. The
drafter's number is right.

### 4.3 · D-0b "three D: resolution sites" — **UNDER-COMPLETE, materially**

A census of every D: resolution and reachability gate found **20 executable sites across 4 files**
(9 resolution, 11 gates), plus 2 out-of-repo scheduled-task destination strings. The amendment names
three. All three are real, but:

- **Claim (c) is not one site — it is three.** `retention_report()` holds `:1032` (anchor check),
  `:1072` (`is_dir`) and **`:980`, which is ungated**. `_generations()` — the estate/workflow half —
  has no anchor check and catches only `OSError`. **An unmounted D: yields an empty glob, not an
  error, so it prints "- none found"** at `:985`. That is precisely the drive-absent / archives-absent
  conflation ruling O-4 fixed for the phase half on 2026-08-12 **and left standing here.** The
  current `RETENTION.md` shows both sections reading `Location: D:\naiad-backups`.
- **Two more inside `backup_estate.py` are omitted:** `assert_environment()` (`:356`), the write
  probe *all three modes* funnel through (`:1141`, `:1226`, `:1329`), and `--mirror` (`:474`,
  `:1400`), which resolves a destination drive with **zero** mount checking.
- **A whole second gate cluster lives outside the file.** `scripts/daily_routine.py` carries its own
  D: literal (`scripts/routine_jobs.json:9`, independent of `BACKUP_DEST_DEFAULT`) and its own gate
  at `:489`, raising "backup destination unreachable" at `:492`. **This is the job that runs
  unattended most often — daily.** A helper wired only into `backup_estate.py` leaves it alarming on
  every cold boot, which is the exact symptom the amendment exists to remove.
- **Two stale in-repo `_archive` paths still live:** `daily_routine.py:537` and
  `archive_dependencies.py:52` both resolve `REPO/research_outputs/_archive` — the pre-O-4 bug,
  surviving in a second and third file. A wait helper would be watching a drive these call sites
  never touch.

**Minimum correct wiring set is 9 points, not 3.**

**And the sharpest one — D-0b as written would wait on the wrong drive.** Both weekly tasks pass
`--dest "G:\My Drive\naiad-backups"` explicitly, and `backup_dest_root()` (`:439`) honours `--dest`
first. So claim (b) gates on `G:\`, not `D:\`. Wiring `wait_for_drive` there makes the Sunday runs
wait for the Google Drive mount. `exchange/status/CONVENTIONS.md:792-795` already records this as
measured-and-unfixed, and it is carried as open item O-6.

### 4.4 · D-0d "CONVENTIONS §2 becomes a `wait_for_drive` call" — **FALSE**

§2 (body line 208) is titled **"How to build a paste for HEPHAESTUS"**. Its six subsections govern
paste construction: self-explanation, routing, rollback lines, exact paste text, post-action gates,
autonomy. **None concerns drives.** Literal `D:` occurs on three lines in the whole file — 784, 788,
795 — all inside §8 Infrastructure inventory, all backup *destinations*, none a gate.

**The D: gate rule is not in CONVENTIONS.md at all.** It is the 2026-08-11 data-residency ruling,
filed as lane notes: `exchange/reports/NOTE_ATHENA_to_ARGUS_2026-08-11_DATA-RESIDENCY.md:19` —
*"Every D:-path contract carries a reachability gate that HALTS if D: is absent"* — mirrored in the
APOLLO note and adopted at `exchange/status/LEDGER_ARGUS.md:52`. **D-0d as drafted would edit a
section that does not contain the rule, and leave the real rule untouched.**

Anchor guidance for whoever redrafts it, since this file has bitten us before: the §2 heading occurs
at TOC line **71** and body line **208**, and there is a *third* decoy the standing note doesn't
cover — the FIND IT FAST table at lines 35–58 holds bare `§2.x` tokens, so `§2.1` is a **3-hit**
string. Verified-unique structural anchor: `"## §2 · How to build a paste for HEPHAESTUS\n\n"` (the
TOC fence has no blank lines between headings; the body has one at line 209).

### 4.5 · The motivating premise — **REFUTED on all three clauses**

The amendment says the 2026-08-09 weekly backups "very likely" failed because an 08:00 trigger hit
an idle drive. The repo's own records contradict every part of that.

| clause | record |
|---|---|
| the backups failed | **Both archives exist and verify.** `naiad_estate_2026-08-09.zip` (495,130,299 B, 15:55:15) and `naiad_workflow_2026-08-09.zip` (2,529,667 B, 15:52:51); both re-verified 2026-08-12; `RETENTION.md` shows **no gap** in either date series. The tasks did return exit 1 — with correct archives written. |
| an 08:00 trigger fired | **It did not.** Actual start 15:51:58 for tasks scheduled 08:00 and 08:30. All carry `StartWhenAvailable=true` (`CONVENTIONS.md:778`) — the machine was asleep and they caught up ~8 hours later. There was no 08:00 disk access to fail. |
| the LaCie was the destination | **It was not.** On 08-09 both tasks targeted `G:\My Drive\naiad-backups`, the Google Drive mount. `D:` did not become the backup target until **2026-08-12**, three days later (commit `0509912`). |

The cause is already diagnosed in `BUILDERS_REPORT_HEPHAESTUS_2026-08-12_CLOSEOUT.md` §7.3:
`backup_estate.py` returns 1 when `publish_step()` is FLAGGED/REFUSED/ERROR, so **a perfect,
fully-verified 472 MB archive reports failure if the git publish afterwards stumbles.** The
destination was probed healthy — writable, sync client running. The leading hypothesis for the
publish stumble is git index contention, explicitly recorded as unproven.

**This does not make Phase 0 wrong.** The operator reports the LaCie failing to wake, and that is a
live constraint worth engineering for; `D:` genuinely is the backup target *now*. But the
justification must be rewritten, because as drafted it attributes a real incident to a mechanism
that demonstrably was not involved — and it says so in a contract that will be read as settled fact.
**That is this project's signature failure: a stale or mistaken fact stated as a current one.** The
honest framing is prospective: *D: became the backup destination on 2026-08-12; a spun-down external
disk is a foreseeable failure mode for every scheduled job that now targets it, and no gate
currently distinguishes asleep from absent.* That argument stands on its own and needs no incident.

---

## 5 · The destination `C:/Naiad` — no collision, but the stated reason does not hold

**The path is unclaimed.** Zero occurrences of `C:/Naiad` or `C:\Naiad` anywhere in the repo;
`C:/Naiad` does not exist on disk (verified). The C: data roots in play are elsewhere —
`C:/Users/luisf/AppData/Local/naiad/data_cache` and the venv `C:\venvs\naiad`. **Namespace-wise the
move is clean, and pinning the repo root rather than `C:/Naiad/repo` is the better of the two.**

**But the amendment's reason is unsupported.** It argues the pinning "matters because the D:
residency rule mirrors repo paths." The rule is written **repo-relative** —
`D:/Naiad/<repo-mirror-path>` — never as a drive-letter substitution of an absolute C: path, and no
code derives the D: destination from the repo's location: `backup_estate.py:249` is a literal
constant and `phase_archive_root()` gates on the drive anchor. **The two trees are already exactly
parallel in repo-relative terms, today, from the OneDrive path.** The gain is a shorter, legible
path outside a sync tree — real and sufficient. It is not correctness.

**Counter-risk worth naming:** `C:/Naiad` and `D:/Naiad` become two identically-named trees, one the
repo and one the bulk mirror. A mistyped drive letter then silently targets the wrong one. The
current asymmetric naming is itself a guard, and pinning removes it.

**The move is not free — 23 enumerated breakages, three of them silent and outside the repo.** Any
Phase A must carry these as a cutover checklist:

1. **Six hardcoded absolute `ROOT` constants** — `brief_episodes_c5.py:19`, `brief_calibration_c4.py:16`,
   `brief_registry_audit.py:7`, `parity_c4_worksheet.py:14`, `parity_c5_worksheet.py:11`,
   `v3_scorer.py:30`. All fail immediately. Fix by adopting `Path(__file__).resolve().parent.parent`,
   already used correctly at `backup_estate.py:148`.
2. **Three armed Task Scheduler jobs** whose `Start In` is the OneDrive path, with *relative* script
   paths that resolve only through it. **Breaks silently, outside the repo — no repo-side check
   catches it.**
3. **The harness project directory** `C:\Users\luisf\.claude\projects\C--Users-luisf-OneDrive-…-naiad\`
   is keyed to the absolute path. A move re-keys it to `C--Naiad`, **orphaning auto-memory and every
   session transcript** unless renamed by hand. Silent.
4. **~25 `.claude/settings.local.json` permission rules** keyed to the path or its temp slug — the
   broad repo read grant among them. Degrades to new prompts, not failure.
5. **Three HARD identity gates that assert the path contains `OneDrive`** —
   `prompts/CONTRACT_v4_ANALYTICS1_BRIEF2_FORWARD0.md:38` (*"working directory path contains
   `\Users\` **and** `OneDrive`"*), `CONVENTIONS.md:253` (the project's definition of "Local"), and
   the SEQ8 queue contract. **`C:/Naiad` fails both conjuncts, so every builder session halts at
   pre-flight.** These must be amended in the *same* change that moves the clone, or the first
   post-move session cannot start. Note the irony worth recording: the file carrying that gate is
   itself titled "PHASE 0 — PRE-FLIGHT", and its §0.1 rationale is about a gate that produced a
   false halt.
6. **Three prose assertions that become untrue rather than broken** — `daily_routine.py:551`,
   `reviewer_manifest.py:411`, `DIGEST.md:145` all state the repo lives inside OneDrive.
   `backup_estate.py:371` degrades correctly (`inside_onedrive` flips to False) and is the model.

**Confirmed safe:** `.gitignore` (all repo-relative), `pytest.ini`, `.git/hooks` (none installed),
GitHub workflows, `engine/data.py` (uses `$LOCALAPPDATA`), and **the venv** — `C:\venvs\naiad` is
outside both the repo and OneDrive, so all ~20 interpreter references survive untouched. Delete
`__pycache__` post-move (74 `.pyc` files embed the old path).

---

## 6 · Objections, consolidated — what I would change before ratifying

Requested by the paste. Ordered by how much they would cost if ratified as drafted.

1. **Rewrite Phase 0's justification.** The 2026-08-09 attribution is refuted by the project's own
   records (§4.5). Argue it prospectively from the 2026-08-12 destination change instead. The
   deliverables survive this rewrite unchanged — only the *why* is wrong.
2. **D-0b's scope is 9 wiring points, not 3**, and one of the 3 named gates on `G:` (§4.3). As
   drafted it would ship, pass its fixtures, and leave the daily job — the most frequent unattended
   run — still failing on a cold drive.
3. **D-0d targets the wrong document** (§4.4). The D: gate rule lives in the residency notes and
   `LEDGER_ARGUS.md:52`, not CONVENTIONS §2.
4. **Fix `_generations()`'s same-day *ordering* along with its grouping** (§4.1), and handle
   ` (N)` duplicates as well as `-NN`. Grouping alone would still keep the wrong file.
5. **Split D-0c out of Phase 0.** O-5 is report-only, already carried as a ledger item owned by
   ATHENA, and shares no code with drive-waking. It is bundled here only because both touch
   `retention_report()`. Bundling a cosmetic report fix into the prerequisite that gates Phase A
   means a disagreement about retention policy can block a data-safety move.
6. **`C:/Naiad` is a good destination for a reason the amendment does not give** (§5). Pin it for
   path length and sync-tree exit; drop the residency-parallelism argument; add the identity-gate
   amendments (item 5 of §5) to Phase A as blocking work, since without them no post-move session
   can run.
7. **Add the pre-flight the paste itself lacked.** Both this session's `wait_for_drive` fixtures and
   Phase A's A-6 mirror touch D:. Neither can be written against a drive whose real wake latency is
   unknown — which is exactly what D-0a's elapsed-seconds print is for. **Ship D-0a first and
   measure before the rest of Phase 0 is drafted**, rather than pinning `attempts=6, delay=3.0`
   (~18s) in a contract in advance of the measurement that would justify it.

**One thing the amendment gets exactly right, and it should survive any redraft:** the framing rule
in D-0d — *a single failed lookup measures that lookup, not absence — of a file, a task, or a disk.*
That is the 2026-08-04 retraction generalised correctly, it is the real defect at
`backup_estate.py:980`, and **this session is itself an instance of it**: the paste's gate saw one
missing file and could not distinguish "never drafted" from "drafted elsewhere and never filed."
§2 answers that question with six checks rather than one. The rule belongs in the standing
conventions whatever happens to the rest of Phase 0.

---

## 7 · What remains open, with owners

| # | item | owner |
|---|---|---|
| 1 | **File the 004 contract text into `exchange/queue/`.** It exists in an unfiled session; nothing can be stamped until it lands. Same class as the 2026-08-12 "file it" ruling. | ATHENA (drafter) |
| 2 | Rule on §6 objections 1–7, then re-issue the amendment against the filed file | ATHENA, then operator |
| 3 | **`_generations()` at `:980` still conflates unmounted-D: with no-archives** — O-4's fix covered the phase half only | ATHENA (O-5, widened) |
| 4 | Same-day sort inversion + ` (N)` duplicates — new, found this session | ATHENA (O-5) |
| 5 | Two stale `REPO/research_outputs/_archive` paths (`daily_routine.py:537`, `archive_dependencies.py:52`) | HEPHAESTUS, next build |
| 6 | Both Sunday tasks still pass `--dest "G:\…"` — carried as O-6, and it defeats D-0b claim (b) | operator |
| 7 | The paste's two unfailable assertions (§3) — fix before re-running against a real 004 | drafter |

**Nothing here was fixed. This session wrote no code by design.**

---

## 8 · Publish and rollback

`exchange/` measured **1,566,668 B — 24.5%** of the 6.39 MB box before this report (107 tracked
files); the tick set with `LEDGER.md` is 28.5%.

**Publish output, as printed:**

```
publish: WARNING -- exchange/ holds 1,598,604 B, 25.0% of the 6,390,000 B box (warn at 25%, refuse above 40%).
publish: routine last completed 2026-08-12 (5h ago)
publish: committed 56e6be0 (2 path(s)) and pushed to origin/v12-v1-census
status= PUBLISHED commit= 56e6be0 pushed= True offenders= []
```

**Correction to this section's own first draft, recorded rather than silently edited.** It predicted
the two files would leave `exchange/` "just under the 25% warn line." They did not: +31,936 B took it
to **1,598,604 B, exactly 25.0%, and the guard fired.** The estimate was low because it costed the
report at its pre-correction length and omitted this section. **The number that matters is the
measured one, and 002's D3 guard is now warning on every publish** — which is the guard doing its
job, and is the case for building queue 003's rotation rather than a reason to write less. Per
CONVENTIONS §3.2: documents are cheap, data is not; the answer to WARN is rotation, not silence.

`.gitignore` remains modified in the working tree. It was already modified at session start
(`0305179`) and is untouched by this session — it is deliberately not part of this publish.

**Rollback:** `git checkout -- exchange/queue/` is a no-op — the queue was never touched. To undo
this session entirely, delete this report and revert the `LEDGER_ATHENA.md` append; there is nothing
else.

---

## 9 · File-disposition table (§3.2)

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/queue/004_move-clone-out-of-onedrive.md` | **no** | — | — | — | — | **0 — the halt; never existed** |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-HALT.md` | yes | tracked (new) | `56e6be0`, +§8 correction in a follow-up commit | yes — `origin/v12-v1-census` | GitHub + estate zip | ~27 KB — ~0.42% of the 6.39 MB box (stated rounded: a file cannot carry its own exact final size or sha256) |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | `56e6be0` | yes — `origin/v12-v1-census` | GitHub + estate zip | **+4,336 B — +0.07%**; 32,374 B → 36,710 B, 14 STATUS_ATHENA blocks |
| `exchange/queue/**` (all other) | yes | tracked | unchanged | unchanged | GitHub + estate zip | **0 — nothing amended, nothing stamped** |
| `scripts/drive_wait.py` | **no** | — | — | — | — | 0 — D-0a not built; no `wait_for_drive` symbol exists anywhere in the repo |
| `scripts/backup_estate.py` | yes | tracked, **unchanged** | unchanged | unchanged | GitHub + estate zip | 0 — D-0b/D-0c are Phase 0's work, not this paste's |
| `exchange/status/CONVENTIONS.md` | yes | tracked, **unchanged** | unchanged | unchanged | GitHub + estate zip | 0 — D-0d not applied, and §4.4 finds it targets the wrong section |
| `C:/Naiad` | **no** | n/a — outside the repo | — | — | — | n/a — nothing was moved |

No other file was created, modified, moved or deleted.

---

## 10 · Status

**Queue 004 is NOT ratified, because queue 004 does not exist in this repository.** The operator's
"ratify 004" is recorded here as received and unexecuted — it is not refused, it is **blocked on the
contract text being filed**. The instruction survives; the moment 004 lands in `exchange/queue/`,
one short paste stamps it.

Phase 0 and Phase A were not begun, per the paste's own instruction and the standing rule that a
ratified contract gets its own build session.
