# BUILDERS' REPORT — ARGUS maintenance cycle, 2026-08-11

**Lane:** ARGUS (analytics). **Builder:** HEPHAESTUS.
**Contract:** small maintenance cycle under `NOTE_ATHENA_to_ARGUS_2026-08-11_DATA-RESIDENCY.md`.
**Branch:** `v12-v1-census`. **HEAD at start:** `04d05ab`.

**What this cycle changed:** one new test, one ledger entry, one document. **No analytics behaviour
changed. No published number moved.** `analytics/` was not touched — not a line — and the whole of
`scripts/`, `engine/`, `configs/`, `study/`, `briefs/`, `publish_exchange.py`, `reviewer_manifest.py`
and `backup_estate.py` were left alone as the contract required.

**Environment gate: PASSED.** Branch `v12-v1-census`; working directory
`C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad` (contains both `\Users\` and
`OneDrive`); `analytics/`, `tests/` and `exchange/` all present.

---

## 0. Data residency — why there is NO D: gate in this document

The 2026-08-11 residency note requires every contract that writes bulk data to write it **directly**
to `D:/Naiad/<repo-mirror-path>`, and to carry a reachability gate that HALTS if `D:` is absent
rather than silently falling back to the laptop.

**This cycle writes no bulk data, so no `D:` reachability gate applies, and none was run.** Saying
so explicitly rather than leaving it inferred: the three files this cycle touched are a Python test
module, a Markdown ledger and this Markdown report — exact sizes in §5. Nothing here is data-class,
nothing is a capture, render, results JSON, substrate, parquet or HTML, and nothing was written to
`D:` or needed to be. The rule is adopted and live for this lane — it simply had no work to do
today.

---

## 1. ITEM 1 — F-AN-15, the interface byte-identity fixture

### 1.1 What it is and why it exists

There are two copies of the same contract:

| copy | path | who reads it |
|---|---|---|
| **canonical** | `analytics/INTERFACE.md` | the code lane; this is the contract `analytics/` honours |
| **published** | `exchange/reports/INTERFACE_2026-08-06_C6.md` | **APOLLO** and every other web lane |

The web lanes reach repo content only through the context box, and the standing tick set is
`LEDGER.md` and `exchange/` **only** (CONVENTIONS §3.2). `analytics/INTERFACE.md` is therefore
unreachable to APOLLO — the `exchange/` copy is the only one it can open. The moment the two drift,
the census-facing lane is reading a contract this code no longer honours, **and nothing anywhere
says so.**

F-AN-15 is the thing that says so. It closes ATHENA's standing open want; the code is ARGUS's, so
closing it was ours to do.

**Location:** `tests/test_analytics.py`, `test_f_an_15_published_interface_is_byte_identical`.
It reads both files in **binary** (no newline translation) and compares sha256 over the raw bytes.

### 1.2 Current result — IDENTICAL

```
F-AN-15: IDENTICAL
  analytics/INTERFACE.md
      sha256 70c3f36894684442871f57c6435380fbcea9ca9e23680e356ce610f16f93c61e   48,885 B
  exchange/reports/INTERFACE_2026-08-06_C6.md
      sha256 70c3f36894684442871f57c6435380fbcea9ca9e23680e356ce610f16f93c61e   48,885 B
```

Both directions reported, as the contract asked: same hash, same byte count, canonical → published
and published → canonical. **The published contract APOLLO is reading is the contract this code
honours.** As of this cycle they have not drifted.

### 1.3 Three design decisions, and the reason for each

**It does NOT auto-copy on mismatch.** This was the contract's instruction and it is the right one.
An automated re-export would succeed every single time it ran, so the suite would go green for
exactly the staleness the fixture exists to catch — it would launder a stale publication into a
passing test. The fix is one deliberate copy, made by a human who has decided the canonical file is
ready to publish. The failure message names the command:

```
copy analytics\INTERFACE.md exchange\reports\INTERFACE_2026-08-06_C6.md
```

and offers the alternative of publishing under a fresh date, leaving the old snapshot as history.

**It SKIPS — it does not pass — when no published copy exists.** A missing mirror is an unanswered
question, not a satisfied assertion. The skip message says so in those words, and says that a
missing published copy means APOLLO has no contract to read at all.

**"Newest" is decided by the ISO date in the FILENAME, never by mtime.** git does not preserve
mtimes. A fresh clone would pick a different "newest" file than this working tree does, and a
fixture that compares different files on different machines is not a fixture. There is also an
explicit non-empty guard: two empty files hash alike, and that comparison would pass while saying
nothing.

### 1.4 THE MUTATION DEMONSTRATION — proof it can fail

This lane has now shipped one fixture that **could not fail** (`stoch_rsi` all-NaN, satisfying
`NaN == NaN` at every truncation point) and one fixture family that was **vacuous against sabotaged
code**. A fixture is not trusted here because it passes. It is trusted because it has been watched
to fail. Three runs, in order:

**Run A — one byte changed, file length unchanged → FAILED, correctly.**
The published copy was backed up bytewise, then the single byte at offset 20,000 was changed from
`' '` (0x20) to `'X'`. Length stayed at 48,885 B, so a size-only check would have missed it
entirely. F-AN-15 caught it:

```
E   AssertionError: PUBLISHED CONTRACT IS STALE -- the two copies are NOT identical.
E     canonical  analytics/INTERFACE.md
E                sha256 70c3f36894684442871f57c6435380fbcea9ca9e23680e356ce610f16f93c61e
E                bytes  48885
E     published  exchange/reports/INTERFACE_2026-08-06_C6.md
E                sha256 02937680f64339459711d02a24b8638cb5980686e0743e7634bfce120cc04ce0
E                bytes  48885
E     delta      published - canonical = +0 bytes; first differing byte at offset 20000
E
E     APOLLO is reading the published copy. It no longer matches the code.
E
E     THIS FIXTURE WILL NOT FIX IT FOR YOU. ...
E         copy analytics\INTERFACE.md exchange\reports\INTERFACE_2026-08-06_C6.md
=========================== short test summary info ===========================
FAILED tests/test_analytics.py::test_f_an_15_published_interface_is_byte_identical
```

Note what the failure reports without being asked: both hashes, both byte counts, the signed byte
delta, and the exact offset of the first difference.

**Run B — published copy removed entirely → SKIPPED, not passed.**

```
SKIPPED [1] tests\test_analytics.py:1092: SKIPPED, NOT PASSED: no
exchange/reports/INTERFACE_<date>*.md exists, so there is no published copy to compare
against. This is not a green result -- the census-facing lanes (APOLLO) have no contract to
read at all. Publish one with:
    copy analytics\INTERFACE.md exchange\reports\INTERFACE_<YYYY-MM-DD>_C6.md
```

pytest reported `s`, not `.`. The vacuous-pass path is closed.

**Run C — restored → PASSED, and the restore was sha-verified.**

```
restored INTERFACE_2026-08-06_C6.md  sha256 70c3f368...f6f93c61e  48885 B
RESTORE VERIFIED: True
```

The published copy is byte-for-byte what it was before the demonstration — confirmed both by sha256
against the pre-mutation backup and by `git status`, which reports
`exchange/reports/INTERFACE_2026-08-06_C6.md` as **unmodified**. The mutation script and the backup
live in the session scratchpad, outside the repo, and are not committed.

### 1.5 Suite state

**287 passed, 1 skipped** (`pytest` with the configured `testpaths = fixtures tests`), up from the
286 passed / 1 skipped baseline by exactly the one test added here. The single skip is pre-existing
and unrelated: `fixtures/test_f8_journal.py:110`, "dry-run journal not generated yet (D7)".

---

## 2. ITEM 2 — LEDGER_ARGUS acknowledgement, appended

The acknowledgement was appended **verbatim** to `exchange/status/LEDGER_ARGUS.md`, unedited.

| | bytes | sha256 |
|---|---|---|
| before | 3,894 | `362220e0…` (12-char prefix; the full prior hash is not this document's to pin) |
| appended | 3,771 | — |
| after | 7,665 | `2bc7a95290a16dc836d525a9cab0f0fda11e69c13b4124d765a7c79c599ef6c2` |

**Append-only verified mechanically, not assumed:** the post-append bytes were asserted to *start
with* the complete pre-append bytes. Not one prior byte changed. Line endings are LF throughout, as
the file already was — zero CR bytes before, zero after.

The entry carries nine bullets. One is a **⚠ RAISED TO ATHENA** item and is the live open question
out of this cycle; see §4.

---

## 3. Findings reported, NOT fixed

**`pytest.ini` now carries a stale comment.** Its explanatory comment reads "the whole F-AN-1..14
regression guard" and "adds exactly 41 items". With F-AN-15 the suite is F-AN-1..15 and
`tests/test_analytics.py` collects 42 items. **The comment is stale; the configuration is correct
and nothing is broken by it** — `testpaths = fixtures tests` still collects the new test, which is
how it was run above. `pytest.ini` sits outside this cycle's authorized set, so it was not edited.
One-line fix for whoever holds that file next.

**The ledger's own LANE STATE line says "suite 286 passed / 1 skipped".** That was true when the
contract text was written and is now 287 / 1 because of this cycle. The contract required the entry
**verbatim**, so it was appended verbatim rather than silently corrected. The ledger is append-only:
a correction is a new entry, never an edit. Flagging it here so the next ARGUS entry can carry the
current figure.

**The publish commit will carry other lanes' pending `exchange/` files.** `publish_exchange.py`
stages all of `exchange/**`, and at the time of this run the tree also held untracked HERMES and
ATHENA files plus a modified `exchange/DIGEST.md`. That is the script's designed behaviour, not a
defect, but it means the publish commit below is not exclusively this lane's work. Listed in §5 so
the record is not misleading.

---

## 4. Open, with owners

1. **⚠ ROTATION CONFLICT — owner: ATHENA, decision required.** Queue 003 rotates bus reports older
   than 30 days into `docs/history/reports/YYYY-MM/`, exempting only `NOTE_*_to_*` files.
   `INTERFACE_2026-08-06_C6.md` is neither a note nor a report — it is the **living census-facing
   contract APOLLO cites**, and the only copy a web lane can reach. Under the current rule it leaves
   APOLLO's reading surface on **2026-09-05**. ARGUS proposes relocating it to `exchange/status/`,
   which does not rotate and already holds `LEDGER_ARGUS.md`. Fallback: drop the date from the
   filename and exempt undated files from rotation. **ATHENA rules.**
   *Note the interaction with F-AN-15:* if the file is relocated out of `exchange/reports/`, F-AN-15
   will SKIP rather than fail — loudly, with a message saying no published copy exists. It will not
   pass vacuously. Whoever executes the relocation should widen the fixture's search path in the
   same change.
2. **`pytest.ini` comment refresh** — owner: whoever next holds that file. Cosmetic.
3. **Residency refinement for `briefs/panel/**/*.parquet`** — owner: ARGUS, not urgent. Recorded in
   the ledger entry: those partitions are 100% regenerable from the captures via `brief_panel.py`,
   making them the free candidate for `D:` when archive volume justifies a contract. Captures are
   the record and stay tracked.

---

## 5. File disposition

Box = **6,390,000 B** (the ~6.39 MB context box). The standing tick set is `LEDGER.md` and
`exchange/` **only**, so files outside `exchange/` cost the box nothing and are marked `n/a` with
their location named.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `tests/test_analytics.py` | yes | tracked (modified: 48,745 → 53,866 B, +5,121) | `d93bba1` | yes — `origin/v12-v1-census` | GitHub + estate zip | **n/a** — `tests/` is outside the tick set (`LEDGER.md` and `exchange/` only), so it never enters the box |
| `exchange/status/LEDGER_ARGUS.md` | yes | tracked (appended: 3,894 → 7,665 B, +3,771) | `45775d2` | yes — `origin/v12-v1-census` | GitHub + estate zip | 7,665 B — **0.12%** |
| `exchange/reports/BUILDERS_REPORT_ARGUS_2026-08-11_MAINT.md` | yes | tracked (new, then extended by the addendum) | pre-addendum text in `45775d2` / `39c5f2f`; **this final text in the addendum publish commit** — a document cannot name the commit that carries it, so its SHA is reported on screen | yes — `origin/v12-v1-census` | GitHub + estate zip | 30,800 B — **0.48%** |
| `exchange/status/CONVENTIONS.md` | yes | tracked (modified: 50,218 → 50,772 B, **+554**; `numstat` 8 insertions / 0 deletions) | addendum publish commit (SHA on screen) | yes — `origin/v12-v1-census` | GitHub + estate zip | 50,772 B — **0.79%** (marginal +554 B, +0.01%) |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked (appended: 13,583 → 16,327 B, **+2,744**) | addendum publish commit (SHA on screen) | yes — `origin/v12-v1-census` | GitHub + estate zip | 16,327 B — **0.26%** |

**Nothing here is over the ~1% flag threshold.** The four `exchange/` files occupy **105,564 B,
1.65% of the box** in total; the largest is `CONVENTIONS.md` at 0.79%, and it was already there —
this session added only 554 B to it. The whole addendum — ruling, ledger entry and all of §A–§E —
cost the box **17,697 B, 0.28%**. DOCUMENTS ARE CHEAP, DATA IS NOT: this cycle produced no data,
and no `D:` gate applied to any of it.

Files created outside the repo and deliberately **not** committed: the mutation script and the
pre-mutation backup of `INTERFACE_2026-08-06_C6.md`, both in the session scratchpad under
`%LOCALAPPDATA%\Temp\claude\...\scratchpad`. They are demonstration scaffolding, not artifacts.
**NOT PROTECTED**, and intentionally so.

---

## 6. Publish

`scripts/publish_exchange.py` has **no `__main__` block** — it is a library, and its documented
callers (`scripts/daily_routine.py:1048`, `scripts/backup_estate.py:943`) invoke
`publish_exchange.publish(ROOT, date)`. Running the file directly is a silent no-op, which is worth
knowing before anyone reports a publish that never happened. It was driven the documented way, from
a scratchpad driver; **`publish_exchange.py` itself was not modified.**

```
publish: committed 45775d2 (7 path(s)) and pushed to origin/v12-v1-census

- committed `45775d2` on `v12-v1-census` and pushed to origin
- 7 path(s) published, all inside `exchange/`
- `exchange/` size budget: 1,777,190 B, 27.8% of 6,390,000 B (WARN)
```

**Push: SUCCEEDED.** Verified against the actual remote, not just the local tracking ref —
`git ls-remote origin v12-v1-census` returns `45775d2a521f1bd9d06e69e1097c3106b3eb2e28`, matching
local `HEAD`. The earlier commit `d93bba1` (the F-AN-15 fixture) is an ancestor and went up with it.

### ⚠ THE SIZE BUDGET IS AT **WARN**

**1,777,190 B — 27.8% of the 6,390,000 B box.** Thresholds are WARN at ≥ 25%, REFUSE above 40%. The
publish proceeded and was not blocked, but `exchange/` has crossed the warning line and there is
about **12 percentage points of headroom left**. This is not caused by this cycle: the two files
added here are 0.4% of the box between them. It is the standing level of `exchange/`, now 101 files.
Recorded here so the next lane to add something large sees the number before it does, not after.

**The seven paths published were not all ARGUS's.** `publish_exchange.py` stages all of
`exchange/**`, so this commit also carried a modified `exchange/DIGEST.md` and four pending files
from the HERMES and ATHENA lanes that were sitting untracked in the tree. Designed behaviour, listed
in §3 and again here so the commit is not misread as one lane's work.

**Two publishes, and why.** The commit above was made while §5 and §6 of this document still held
placeholders, because the commit SHA and the budget line do not exist until the publish runs. This
final text was carried by a second publish immediately after. That second commit's SHA is
necessarily absent from the file it commits — the same reason a file never contains its own sha256.
It is reported to the operator on screen.

---

## 7. Honest summary for the operator

Two small things were asked for and both are done. The interface fixture now exists and has been
watched to fail before being trusted to pass — a one-byte change to the published contract, with the
file length left identical, was caught and reported with the exact offset. The two copies of the
contract are currently byte-identical, so APOLLO is reading the right thing today. The ledger has a
current entry for the first time in nine days, appended without touching a byte of what came before.

The one thing that needs a decision from someone other than this lane: the census-facing contract
`INTERFACE_2026-08-06_C6.md` is scheduled to rotate off APOLLO's reading surface on 2026-09-05 by a
rule that was never written with it in mind. ATHENA rules on where it should live. Until then it
stays where it is and F-AN-15 watches it.

*ARGUS lane, built by HEPHAESTUS, 2026-08-11.*

---
---

# ADDENDUM — 2026-08-12 (UTC), folded into this same document and the same publish

**Why this is in the 2026-08-11 document.** The addendum instruction is dated 2026-08-12 and this
report is dated 2026-08-11. Both are right. The machine clock reads **2026-08-11 22:35:38 −03:00**;
the same instant in UTC is **2026-08-12 01:35Z**. HERMES flagged the identical gap in its own cycle
report ("my sandbox clock reads 2026-08-12T01:04Z") and, correctly, refused to silently pick one.
The two are three hours apart, not one day. **The filename and the local-dated sections stay on
local time; the addendum keeps its UTC date, and every scheduler timestamp below is LOCAL** — which
matters, because the scheduler itself runs on local time.

---

## A. Did the routine fail four times, or fail once and never fire again?

**It failed ONCE.** The four-failure reading is wrong, and one of the three remaining days is not a
failure at all — it is a run that was *killed*, after the repair had already worked.

### A.1 The tasks — enumerated, not inferred from one lookup

There are **three** Naiad tasks, not four. **There is no HERMES scheduled task at all** — the
addendum's "plus any HERMES entry" has no referent, and that absence is itself worth recording.

| task | last run (local) | last result | next run | state |
|---|---|---|---|---|
| `\Naiad daily routine` | **11-Aug-26 16:36:33** | **-1073741510** = `0xC000013A` **STATUS_CONTROL_C_EXIT** | 12-Aug-26 07:00 | Ready / Enabled |
| `\Naiad weekly backup` (estate, Sun 08:00) | 09-Aug-26 15:51:58 | **1** (generic failure) | 16-Aug-26 08:00 | Ready / Enabled |
| `\Naiad weekly workflow backup` (Sun 08:30) | 09-Aug-26 15:51:58 | **1** (generic failure) | 16-Aug-26 08:30 | Ready / Enabled |

Note the last-run *times*: 15:51:58 for two tasks scheduled at 08:00 and 08:30, and 16:36:33 for one
scheduled at 07:00. **None of them ran at its scheduled time.** That is the signature of catch-up
firing, which brings us to the setting the addendum asked about.

### A.2 `StartWhenAvailable` — already ON, on all three

```
\Naiad daily routine             StartWhenAvailable=true  WakeToRun=(absent -> false)  DisallowStartIfOnBatteries=false
\Naiad weekly backup             StartWhenAvailable=true  WakeToRun=(absent -> false)  DisallowStartIfOnBatteries=false
\Naiad weekly workflow backup    StartWhenAvailable=true  WakeToRun=(absent -> false)  DisallowStartIfOnBatteries=false
```

**The recommendation the addendum asked for is moot: the setting is already enabled.** Nothing was
changed, as instructed. And the odd-hour implication the addendum wanted stated is not hypothetical
— **it has already happened twice**, and those two catch-up runs are exactly the 15:51 and 16:36
timestamps above.

### A.3 Why the per-day verdict rests on artifacts, not the event log

**`Microsoft-Windows-TaskScheduler/Operational` is DISABLED** (`IsEnabled=False`, 0 records). Task
Scheduler keeps only the *most recent* run time per task, so the log that would have answered this
directly does not exist. The verdict below is therefore built on **run artifacts**, and it turns on
one fact that makes absence into evidence:

> **A failed run still writes its DAILY document.** The 08-09 run failed at its first required job
> and *still* produced a complete `DAILY_2026-08-09.md`, including a "## 1. Failures" section. So
> "triggered" implies "a DAILY exists". The contrapositive is what licenses a NEVER-TRIGGERED
> verdict: no DAILY, no run — unless the process was killed before the write, which is precisely
> what distinguishes 08-11 below.

### A.4 VERDICT, per day

| date (local) | verdict | evidence |
|---|---|---|
| **08-09 Sun** | **TRIGGERED-AND-FAILED** | `DAILY_2026-08-09.md` (2,370 B), generated `2026-08-09T18:52:59Z` = 15:52 local. `manifest` (required) exit 1, `HALT: F-M3, F-M4 failed; no partial adoption (contract section 5)`. Run stopped; brief, brief2_capture, brief2_panel never attempted. **No `MANIFEST_2026-08-09.json` was written** — the halt was real and total. |
| **08-10 Mon** | **NEVER-TRIGGERED** | No `DAILY_2026-08-10.md`, no `MANIFEST_2026-08-10.json`, nothing anywhere. Scheduler's last-run for the daily is 08-11, so 08-10 was not the most recent start. Operator away, machine off or asleep; `WakeToRun` is false so nothing woke it. The missed 08-10 trigger was then satisfied by the 08-11 catch-up. |
| **08-11 Tue** | **TRIGGERED, THEN KILLED** — *not* a fixture failure | Started **16:36:33** (catch-up from 07:00). `MANIFEST_2026-08-11.json` written **16:37**, 24,164 B. Exit `0xC000013A` = STATUS_CONTROL_C_EXIT — the console was closed or the session ended. **No `DAILY_2026-08-11.md`**: the process died after the manifest job and before the document write. |
| **08-12 Wed** | **NOT YET DUE** | Next run 12-Aug-26 07:00; local clock is 2026-08-11 22:35. The day has not happened yet locally. HERMES counted it as a dead day by reading a UTC clock. |

### A.5 The finding that changes the picture: THE REPAIR WORKED

On 08-09 the manifest job halted and **no manifest was written**. On 08-11 the same job ran and
**`MANIFEST_2026-08-11.json` was written, 24,164 B**. The F-M3/F-M4 fixtures that halted the routine
on 08-09 **passed on 08-11**. The run then died for an unrelated reason.

This also resolves HERMES's headline. HERMES reported the routine "dead for three days" with its
`MANIFEST.json` freshness masked by publishes. The refinement: `exchange/status/MANIFEST.json`
(24,164 B, 16:37) and `exchange/status/daily/MANIFEST_2026-08-11.json` (24,164 B, 16:37) are the
same bytes at the same minute — **that manifest is the routine's own output, not a publish
artifact.** The routine was not dead on 08-11. It ran, did its first job correctly, and was killed.

### A.6 What actually killed it, and what to do (RECOMMENDATIONS — no settings were changed)

`ExecutionTimeLimit` is `PT2H`; a timeout kill returns `0x41306`, not `0xC000013A`, and the run
lasted under a minute — **not the time limit**. The task's principal is
`LogonType=InteractiveToken`: it runs inside the logged-on user's session, so **closing the console,
logging off, or sleeping the laptop sends the process a control-C and kills it mid-run.** That is
the 08-11 death, exactly.

1. **`StartWhenAvailable`: leave it alone — already `true`.** The addendum's proposed change is
   already in force. Its stated implication is confirmed rather than predicted: catch-up runs
   publish at odd hours (15:52 on 08-09, 16:36 on 08-11). That is the price and it is already being
   paid.
2. **Consider `WakeToRun=true`** *(operator's call)* — currently absent, so false. This is the
   setting that would actually change away-day behaviour: today a sleeping laptop is never woken and
   the run simply waits for the next wake. Implication: the machine wakes itself at 07:00.
3. **The real fragility is `InteractiveToken`.** Running whether-or-not-logged-on with stored
   credentials would have survived 08-11. Implication: it needs a stored password and the run
   becomes invisible (no console to watch).
4. **Turn on the Operational log** — `IsEnabled=False` is why this question needed forensics at all.
   One click makes the next occurrence answerable in seconds instead of by artifact archaeology.
5. **Both weekly backups last returned `1` (failure) on 08-09 and have not run since.** Out of this
   cycle's scope and NOT investigated. Next due 16-Aug. Flagged, not diagnosed. **Owner: ATHENA.**

**Bottom line: the 08-09 fixture failure is real and the repair for it is real and evidenced. What
is not real is a four-day failure streak.** One genuine failure, one away-day, one killed run, and
one day that has not arrived.

---

## B. Ruling 'append' installed in CONVENTIONS §3.1

Appended to the no-exceptions clause of **§3.1 The build document**.

**The placement hazard was live and was handled.** `### 3.1 The build document` occurs **twice** in
this file — line 79 (the outline at the top) and line 337 (the body). CONVENTIONS' own line 299
records a previous guard that matched the outline heading instead of the body one. The anchor used
here was a body-only sentence, asserted unique (1 occurrence), and asserted to sit *after* the body
heading — **a count alone is not a placement check.**

Pre-write context, post-write assertions, all passed:

```
'### 3.1' headings  : 2 at lines [79, 337]  <- TOC + body, as expected
anchor              : UNIQUE, 1 occurrence, line 348
placement check     : anchor line 348 > body heading line 337  OK
ruling present      : exactly 1 time  OK
CR bytes            : 0 -> 0  UNCHANGED  OK
LF bytes            : 855 -> 863  (+8, exactly the lines inserted)  OK
landing zone        : body '### 3.1' < ruling < 'It serves two readers at once'  OK
```

Independently confirmed with `git diff --numstat`: **8 insertions, 0 deletions** — a pure insertion,
no existing line rewritten. 50,218 → 50,772 B.

**One defect found and fixed in the same session.** The first write left the ruling with no blank
line before it, which in Markdown glues it to the end of the previous paragraph, and left a doubled
blank line after. Both were repaired; the repair moved a newline rather than adding one, so byte
count and LF count were identical before and after (50,772 B, 863 LF) and `numstat` still reads 8/0.

**Honouring it immediately:** this document ends by appending the session's STATUS entry to
**`exchange/status/LEDGER_ATHENA.md`** — ATHENA commissioned this work via
`NOTE_ATHENA_to_ARGUS_2026-08-11_DATA-RESIDENCY.md`. The rule's first application is its own
installer, as instructed. See §D.

---

## C. The manifest exception — NOT WRITTEN, text incomplete

**The instruction was truncated mid-sentence.** It ends:

> `exchange/status/MANIFEST.json` and `exchange/status/daily/MANIFEST_*.json` are data by type and
> bus-resident by

— and stops there. The rest of the sentence, and whatever conditions and bounds follow it, never
arrived.

**Nothing was written to CONVENTIONS §4.2.** This is a named exception to the text-only / 1 MB rule,
in the one file that governs every lane's behaviour, and the operator is explicitly reserving a veto
over it. Guessing the completion of a rule of that kind — inventing the justification for an
exception to the rule that has caught every box overflow so far — is not a defensible thing for a
builder to do quietly. The remaining text has been requested.

**§4.2 is unmodified.** When the full text arrives it goes in under the same edit discipline as §B,
and this section is replaced with the result.

*Context that may be useful when the text is finalised:* `exchange/status/MANIFEST.json` is
**24,164 B (0.38% of the box)** and `exchange/status/daily/` holds **7 dated `MANIFEST_*.json`
totalling 159,717 B (2.50%)**, kept by the §8 rolling window at newest-7. Together **183,881 B,
2.88% of the 6,390,000 B box** — under the 25% warn line on their own, but not negligible against
the 27.8% the bus is already carrying.

---

## D. Ledger append — Ruling 'append', first application

Per the ruling installed in §B, this document ends by appending the session's STATUS entry to the
**commissioning lane's** ledger. ATHENA commissioned this work through
`NOTE_ATHENA_to_ARGUS_2026-08-11_DATA-RESIDENCY.md`, so the entry goes to
**`exchange/status/LEDGER_ATHENA.md`**, in the `naiad-eod` STATUS format that file's own template
defines.

| | bytes |
|---|---|
| before | 13,583 |
| appended | 2,744 |
| after | 16,327 |

**Append-only verified mechanically:** the post-append bytes were asserted to *start with* the
complete pre-append bytes — no prior byte changed. CR count 0 before and after.

**Two ledgers carry this session, and that is correct, not duplication.** `LEDGER_ARGUS.md` holds
the lane's own acknowledgement of the residency note (§2) — that is the *recipient's* record, and it
is what satisfies the inbox-acknowledgement test the ruling restores: **acted = the recipient's
ledger references the note.** `LEDGER_ATHENA.md` holds the commissioning lane's record of what the
session produced. Different questions, different files.

---

## E. Addendum disposition and what remains open

**Files touched by the addendum, beyond those in §5:**

- `exchange/status/CONVENTIONS.md` — Ruling 'append' installed in §3.1
- `exchange/status/LEDGER_ATHENA.md` — STATUS entry appended
- `exchange/reports/BUILDERS_REPORT_ARGUS_2026-08-11_MAINT.md` — this document, extended

All three are in §5's table with their box cost.

**Read-only throughout item A.** Task Scheduler was queried, never modified: `schtasks /query` and
XML reads only. No task setting was changed, no task was run, disabled or re-registered. The
recommendations in §A.6 are recommendations.

**Open, with owners:**

1. **Item C — the manifest exception. Owner: operator.** Truncated mid-sentence; §4.2 unmodified,
   awaiting the remaining text. This is the one piece of the addendum that was not delivered, and
   the reason is stated in §C rather than papered over.
2. **Both weekly backups failing (result `1`) since 08-09. Owner: ATHENA.** Flagged in §A.6, not
   diagnosed — outside this cycle's scope. Next scheduled run 16-Aug 08:00 / 08:30.
3. **`WakeToRun` and `InteractiveToken`. Owner: operator.** §A.6 items 2 and 3, each with its
   implication stated. No setting was changed.
4. **Task Scheduler Operational log is disabled. Owner: operator.** §A.6 item 4.
5. **⚠ Rotation conflict on `INTERFACE_2026-08-06_C6.md`. Owner: ATHENA.** Unchanged from §4;
   still the item with a dated deadline (2026-09-05).
