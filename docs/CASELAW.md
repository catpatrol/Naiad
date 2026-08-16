# CASELAW — why the rules in CONVENTIONS say what they say

**Status:** tracked, and deliberately **OFF the bus.** This file is not in the tick set
(`exchange/` + `LEDGER.md`), so it costs no box budget and no lane pays context for it. Read it when
you want to know *why* a rule exists, or when you are about to argue that one is unnecessary.

**What this is.** Every rule in `exchange/status/CONVENTIONS.md` carries an `EARNED-BY` line. Where
that line cites a case number, the narrative is here: the failure, the near-miss, or the measurement
that put the rule in the file. Extracted 2026-08-15 in THE GREAT COLLAPSE, verbatim from the
pre-collapse CONVENTIONS.md, so that the rules file could shrink to rules.

**Why they were moved rather than deleted.** A rule with no story behind it gets cargo-culted by the
next reader and then quietly dropped by the one after that, because nobody can tell whether it was
reasoned or guessed. These narratives are the reasoning. They are also the honest record that this
project's operating rules were, without exception, **paid for.**

**Numbering is permanent.** CL-n is a stable citation. New cases append; existing numbers are never
reused or renumbered, because CONVENTIONS cites them by number.

**Dated corrections are NOT here.** Those stay in CONVENTIONS, beneath the rule they correct — a
correction is part of the rule's live text, not part of its history.

---

## Index

| case | what happened | earns |
|---|---|---|
| **CL-1** | The §0 three-triggers claim, corrected beneath itself | §0 · THE CORRECTION RULE |
| **CL-2** | Four routing failures, 2026-07-26 | §0 · THE IDENTITY GATE, §2.2 |
| **CL-3** | Four halts and one near-miss on irreversible deletion | §2.2 |
| **CL-4** | Four gates written from the pre-action state | §2.3 |
| **CL-5** | Three anchor misses in three days, each passing its own guard | §2.3 |
| **CL-6** | The read-only census that reached the operator only as a screenshot | §3.1 |
| **CL-7** | Five of six lane ledgers trailing their own filed reports | §3.1 |
| **CL-8** | The REFUSE at 40.2% that stopped a paste whose artifacts were already built | §3.2 |
| **CL-9** | 42 ARGUS documents versus two capture JSONs | §4.2 |
| **CL-10** | Two captures archived to docs/history/argus — reading surface fell 85%, box fell zero | §4.2 |
| **CL-11** | The de-dup paste that would have deleted the only version-controlled copies | §8.1 |
| **CL-12** | exchange/ at 51% of the box with nine of ten files under the 1 MB cap | §4.2 |
| **CL-13** | The backslash path and the __main__-less module | §2.4, §3.4 |
| **CL-14** | F4: deletion became available in an unattended scheduled run | §4.1 |
| **CL-15** | Three retained _run2 trees holding ~3.2 GB of pure redundancy | §4.4 |
| **CL-16** | seq8_run2 — 8 identical data files, 3 differing manifests, 1783.5 MB redundant | §4.4 |
| **CL-17** | The 2026-07-28 provenance error | §6.1 |
| **CL-18** | Three documents all asserting the --workflow trigger was armed | §6.2 |
| **CL-19** | The acceptance probe whose decisive signal was printed on its own signpost | §6.2 |
| **CL-20** | The builder's six refusals on a ratified invariant | §6.2 |
| **CL-21** | Two of five BOX_BYTES dependents contained no BOX_BYTES string | §6.4 |
| **CL-22** | mc1_report.py pinned versus census2b_report.py importing | §6.4 |
| **CL-23** | The sweep's own three defects, caught by adversarial verification | §6.4 |
| **CL-24** | The protocol run against the session that adopted it | §6.4 |
| **CL-25** | Reading engine/cells.py produced two material corrections | §6.3, §7.5 |
| **CL-26** | routine_jobs.json's bare `python` that would have failed every daily run silently | §8.4 |
| **CL-27** | Registered is not uploaded — the Google Drive hard-link failures | §8.2 |

---

### CL-1 · The §0 three-triggers claim, corrected beneath itself

**EARNS** — §0 · THE CORRECTION RULE: a correction REPLACES the assertion it corrects

Live instance, still visible in this file: §0 asserted three enforcement triggers when only one existed, and the first fix was a note appended *beneath* the false sentence — so a reader met the claim before its retraction. The sentence itself was rewritten on 2026-08-04, which is what a correction means. **A withdrawn instance, recorded because withdrawing it matters:** this rule originally cited a `--workflow` ARMED claim as its example. That example was itself false — the trigger had been armed all along — and has been removed. The rule stands on its own logic: a reader believes what they read first.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 12–12.*

---

### CL-2 · Four routing failures, 2026-07-26

**EARNS** — §0 · THE IDENTITY GATE, §2.2: every paste carries the two-sided gate and halts before any action

**Why this exists:** four routing failures on 2026-07-26. The three that carried the ENVIRONMENT
label were all halted by it. Zero damage.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 277–278.*

---

### CL-3 · Four halts and one near-miss on irreversible deletion

**EARNS** — §2.2: every paste-go states its own undo, or says it cannot be undone

**Why:** four halts and one near-miss on irreversible deletion in eight days. A paste that cannot
state its own undo has not been thought through to the end.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 290–291.*

---

### CL-4 · Four gates written from the pre-action state

**EARNS** — §2.3: write every gate from the POST-action state

Logged instances: a five-file deletion list checked against an empty-worktree gate when ten
existed · a ledger entry asserting 18/18 while the same paste restored a file making it 19/19 ·
a phase-directory deletion contradicting its own expected-EMPTY git status · `.gitignore`
covering `*.zip` but not the `.sha256` sidecar, so writing it legitimately failed F-K3.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 310–313.*

---

### CL-5 · Three anchor misses in three days, each passing its own guard

**EARNS** — §2.3: anchor context D-4 — print 3 lines either side before writing; an occurrence count is not a placement check

Three misses in three days, each
one passing its own guard: `find('### 3.1')` matched the heading OUTLINE at the top of this file
rather than the section body 250 lines later · a once-occurring anchor sat mid-sentence inside an
unrelated section, so inserting before it would have severed the sentence · a single-line
`.replace()` was handed a search string spanning a hard-wrapped line break, matched nothing, and
the script reported the edit applied. **Every one of those had a guard that returned "1 hit".**

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 318–323.*

---

### CL-6 · The read-only census that reached the operator only as a screenshot

**EARNS** — §3.1: no exceptions — every builder session emits the build document, read-only included

**No exceptions — rule hardened 2026-08-11 by operator instruction, after a reviewer
waived it for a "read-only" census and the results reached the operator only as a screenshot.**

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 364–365.*

---

### CL-7 · Five of six lane ledgers trailing their own filed reports

**EARNS** — §3.1: ruling 'append' — the build document ends by appending its STATUS entry to the lane ledger

**Ruling 'append' (operator, 2026-08-12), resolving the HERMES 2026-08-12 finding that five
of six lane ledgers trailed their own filed reports:**

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 370–371.*

---

### CL-8 · The REFUSE at 40.2% that stopped a paste whose artifacts were already built

**EARNS** — §3.2: the box ceiling and its warn 0.40 / refuse 0.70 thresholds

**The box was raised 6.39 MB → 16 MB on 2026-08-15 by operator ruling `["box", VETO]`**, after a
REFUSE at 40.2% stopped a paste whose artifacts were already built.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 427–428.*

---

### CL-9 · 42 ARGUS documents versus two capture JSONs

**EARNS** — §4.2: DOCUMENTS ARE CHEAP, DATA IS NOT — write more reports, never fewer

**The law, confirmed three separate times: DOCUMENTS ARE CHEAP, DATA IS NOT.** Every prose artifact
the ARGUS lane has ever written — 42 files, every report, summary, parity worksheet and interface
snapshot — totals ~770 KB, about 12% of the then-6.39 MB box. Two capture JSONs from a SINGLE
2026-08-06 cycle totalled 4,024,198 bytes, about 63% of it. **Two files outweighed a lane's entire
written history five to one** — a ratio, which is why the 2026-08-15 raise to 16 MB does not touch
this argument at all. **So: write more reports, never fewer. The documents are not the problem and
never were.**

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 448–454.*

---

### CL-10 · Two captures archived to docs/history/argus — reading surface fell 85%, box fell zero

**EARNS** — §4.2: archiving is not a fix

**And archiving is not a fix.** On 2026-08-06 two captures were moved from `exchange/reports/` to
`docs/history/argus/`; both were then retrieved from the box at their NEW paths, because both
folders sit inside the sync selection. The reading surface fell 85%. Box consumption fell by zero.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 461–463.*

---

### CL-11 · The de-dup paste that would have deleted the only version-controlled copies

**EARNS** — §8.1: EXISTENCE IS NOT PROTECTION — three checks before removing any file

**Why this is a rule and not a note.** On 2026-08-04 a reviewer paste de-duplicated `exchange/` by
the test "does a byte-identical file exist anywhere outside `exchange/`". Two of three matches were
git-ignored. Running it would have deleted the **only version-controlled copy** of both files and
left a pointer stub asserting *"a byte-identical copy exists in the repo"* — true as English,
false as protection. The builder checked the twins' tracked state, refused both removals, and
performed only the one whose twin was verified in `HEAD` and on `origin`. **The reviewer wrote the
rule this paragraph extends and then broke it in the same week; the executor reading the invariant
rather than the instruction is what stopped it.**

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 489–496.*

---

### CL-12 · exchange/ at 51% of the box with nine of ten files under the 1 MB cap

**EARNS** — §4.2: a per-file size limit does not bound a folder — budget the TOTAL, not the item

**Corollary for guards.** A per-file size limit does not bound a folder. `exchange/` reached 51% of
the context box while nine of its ten data files were individually under the 1 MB cap — one
breach, nine compliant, half the box gone. **Budget the total, not the item.**

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 498–500.*

---

### CL-13 · The backslash path and the __main__-less module

**EARNS** — §2.4, §3.4: forward slashes in bash blocks; publish_exchange.py is a library, call publish()

*(Worked example, kept because it is the fastest way to recognise both failures: a Windows path
written with backslashes inside a bash block is read by the shell as escapes — `C:\venvs\naiad\Scripts\python.exe` collapses to
`C:venvsnaiadScriptspython.exe` → command not found. And a `__main__`-less module run as a
script is a silent no-op — the worst failure shape available, because the surrounding paste
reports success.)*

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 538–542.*

---

### CL-14 · F4: deletion became available in an unattended scheduled run

**EARNS** — §4.1: no scheduled lane deletes anything

F4 found that deletion, initially blocked,
became available in an **unattended** run by calling `allow_cowork_file_delete`, with no human
present to approve it.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 578–580.*

---

### CL-15 · Three retained _run2 trees holding ~3.2 GB of pure redundancy

**EARNS** — §4.4: R3 — hash-and-compare, then discard the rerun

Never retain it: three retained _run2
trees held ~3.2 GB of pure redundancy (seq8_run2 relocated 2026-08-11; journal_s3_run2 and
s3_events_run2 live inside the s3 phase archive).

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 635–637.*

---

### CL-16 · seq8_run2 — 8 identical data files, 3 differing manifests, 1783.5 MB redundant

**EARNS** — §4.4: refinement D-3 — discard the DATA, keep the PROVENANCE

Measured, and this is
what the refinement is built on: `seq8_run2` was byte-identical to `seq8` on **all 8 data files**
and **differed on all 3 of its metadata files** (`seq8_extract_manifest.json`,
`seq8_outcomes_manifest.json`, `seq8_views_summary.json`) — the signature of a determinism rerun,
identical outputs with fresh run manifests. The 1783.5 MB of data was genuinely redundant; the few
KB recording what run 2 did was not.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 642–647.*

---

### CL-17 · The 2026-07-28 provenance error

**EARNS** — §6.1: an operator-reported fact is never [verified]

That exact confusion produced a logged error
on 2026-07-28.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 738–739.*

---

### CL-18 · Three documents all asserting the --workflow trigger was armed

**EARNS** — §6.2: a claim repeated across documents is not a claim verified

Three documents said the
   `--workflow` trigger was armed; each had copied the one before it.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 754–755.*

---

### CL-19 · The acceptance probe whose decisive signal was printed on its own signpost

**EARNS** — §6.2: Class A cure — enumerate before claiming something lives only in place P

The instance that produced this: an acceptance probe was designed around the six-column
disposition table as a signal unique to this file, while that table was still described in full by
memory entry #8 **and named in the pointer entry itself** — a test whose decisive signal was
printed on its own signpost. The probe was recorded INCONCLUSIVE rather than passed.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 758–761.*

---

### CL-20 · The builder's six refusals on a ratified invariant

**EARNS** — §6.2: the counter-pattern: a stack whose executor never pushes back is a stack whose reviewer errors all land

**The counter-pattern, and it is the system working:** the builder has refused a reviewer
instruction on a ratified invariant at least six times. **A stack whose executor never pushes back
is a stack whose reviewer errors all land.**

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 763–765.*

> **Two counts existed, and the collapse had to pick one.** CONVENTIONS said *"at least six times"*
> — written 2026-08-04. Project memory's 2026-08-15 capture said *"nine-plus times"*. Neither is
> wrong; the later count is simply later, and the two surfaces drifted because the same fact had two
> homes. **The restructured §6.2 carries "nine-plus"** as the more recent figure, and this note is
> the record that the number was reconciled rather than silently chosen. Exactly the class of
> divergence the collapse exists to make structurally impossible: one fact, one home, one pointer.

---

### CL-21 · Two of five BOX_BYTES dependents contained no BOX_BYTES string

**EARNS** — §6.4: grep the NAME, the VALUE, and the THRESHOLD TEXT — a name-only grep reports a clean sweep and is wrong

On 2026-08-15, of five
   sites depending on `BOX_BYTES`, **two contained no `BOX_BYTES` string at all** — one held a copy
   under a different name (`BOX_CAPACITY`), one stated the thresholds as prose (`25 % / 40 %`) with
   no identifier to find. A name-only grep reports a clean sweep and is wrong.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 774–777.*

---

### CL-22 · mc1_report.py pinned versus census2b_report.py importing

**EARNS** — §6.4: a historical report reproduces history — pin regenerators, import into live consumers

**The exemplar, both halves, from the day it was written:** `scripts/mc1_report.py:25`
(`BOX_CAPACITY`, pinned + labelled — it regenerates the MC-1 document filed 2026-08-06) versus
`scripts/census2b_report.py` (now imports — one definition in one place; the hand-kept copy it had
would have made every occupancy figure wrong by 2.5×).

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 785–788.*

---

### CL-23 · The sweep's own three defects, caught by adversarial verification

**EARNS** — §6.4: corollary — after editing a document, RE-READ THE DOCUMENT

**Corollary, added the same day from the sweep's own three defects: after editing a document,
RE-READ THE DOCUMENT.** Grepping for a value finds values. It does not find a claim that
*contradicts* a value 26 lines below it, an ownership row a ruling has just closed, or a second
instance of the same stale figure further down the same file. All three happened; all three were
caught by adversarial verification rather than by the sweep that made them.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 790–794.*

---

### CL-24 · The protocol run against the session that adopted it

**EARNS** — §6.4: the named-constant protocol governed the session that adopted it

**This protocol governed the session that adopted it** — the 2026-08-15 threshold recalibration ran
its own three legs and its dependents table is in
`BUILDERS_REPORT_HEPHAESTUS_2026-08-15_BOX-GOVERNANCE.md`.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 796–798.*

---

### CL-25 · Reading engine/cells.py produced two material corrections

**EARNS** — §6.3, §7.5: the context-gap audit's binding consequence; MTF_SET has no 1D and no 30m

**Rationale and precedent, kept because it is the argument:** the 2026-07-25 audit added the
engine package, configs and data-estate manifest — and reading `engine/cells.py` immediately
produced two material corrections. The engine has **no 1D and no 30m timeframe anywhere**
(`INTERVAL_MS` / `MTF_SET` stop at 12h), so D5's graduation basis of "robust on 12h/1d" was half
un-representable and narrowed to 12H/position primary + 4H/swing secondary; and the census's
"governor lens" is a **measurement frame**, NOT the engine's per-cell `tf_gov`.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 812–817.*

---

### CL-26 · routine_jobs.json's bare `python` that would have failed every daily run silently

**EARNS** — §8.4: the launchd trigger registry, and why a bare interpreter name is a silent killer

> **One prerequisite had to be fixed first, and it would have broken every daily run silently.**
> `scripts/routine_jobs.json` carried `"python": "python"` — a bare interpreter name inherited
> from Windows. `daily_routine.py` builds `argv = [python, script]` and has no `--python`
> override. Bare `python` does not resolve on this machine **at all**: not under launchd's
> minimal `PATH`, and not in the operator's interactive shell either. Every child job would have
> returned `exit=126, "could not launch: [Errno 2] No such file or directory"`. It is now the
> absolute venv path. See `CADENCE.md` for the trigger registry and the `bootout` undo lines.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 890–896.*

---

### CL-27 · Registered is not uploaded — the Google Drive hard-link failures

**EARNS** — §8.2: REGISTERED IS NOT UPLOADED — treat an off-site copy as unconfirmed until checked

**Two things that are true and uncomfortable, both measured 2026-08-12, neither yet fixed:** the
two weekly scheduled tasks still pass `--dest "G:\My Drive\naiad-backups"` **explicitly**, and an
explicit `--dest` outranks the new default — so until those task arguments are edited the Sunday
runs still target the old, now-empty path. And `D:/naiad-backups` **is** registered with Google
Drive as a mirrored folder (verified by decoding the DriveFS `SyncTargets` registry value, not
inferred), but its uploads are erroring — `CreateHardLinkW failed`, 50 occurrences naming these
archives, because exFAT has no hard links — with no upload-completion record in Drive's logs.
**Registered is not uploaded.** Treat the off-site copy as UNCONFIRMED until the operator checks
Drive's web UI under *Computers*.

*Verbatim from CONVENTIONS.md as it stood at commit a2b69cf, lines 930–938.*

---

## ANNEX · The relocation register

*Moved here 2026-08-15 in the collapse. It records the 2026-08-03 memory restructure — every
behaviour relocated out of project memory, where it now lives after the collapse renumbered the
sections, and how compliance is checked. It is history plus an audit map, not a rule, so it sits
off the bus. **The rule it carries — "a rule with no probe coverage is a rule on trust" — stayed in
CONVENTIONS**, under MAINTENANCE.*

| origin | behaviour | now at | probe |
|---|---|---|---|
| memory #1 | SS Pine backlog B-1 / B-3 | `LEDGER_APOLLO.md` | none — backlog, not behaviour |
| memory #7 | Exact paste-ready text | CONVENTIONS §2.2 | **B3** |
| memory #8 | Context-gap audit | §6.3 | **B5** + `naiad-custodian` |
| memory #9 | Optimization-track history | §1.4, §2.4, §5.1 | none — reference |
| memory #14 | Autonomous decision-tree design | §2.5 | **B4** |
| memory #15 | ARGUS lane purpose | §5.1 | none — charter |
| memory #16 | Builder-idle-time preference | §1.4 | **B4** |
| memory #19 | SS interview rulings | `LEDGER_APOLLO.md` | none — reference |
| memory #25 | Infrastructure inventory | §8.4 | none — reference |
| memory #28 | Builder handback, both artifacts | §3.1 | operator inspection |
| memory #29 | Manual-task instruction rule | §1.2 | operator inspection |
| memory #3, #4, #14 | Study frames — fractal lens, spine, EMA family | **§7** (new 2026-08-15) | **F-CONV-3** |
| memory #13, #15 | Geography and data residency v2 | **§2.1** (new 2026-08-15) | **F-CONV-3** |
| memory #4, #16 | Study verdicts and census-2A yield | `LEDGER.md` → STANDING VERDICTS | **F-CONV-3** |

**Uncovered rules are named honestly above.** Reference material needs no probe. The two rules
covered only by operator inspection (§3.1, §1.2) are ones you will notice immediately if a lane
drops them, which is its own detection.

---

*Ends. New cases append with the next free number and an EARNS line naming the section whose rule they earned.*
