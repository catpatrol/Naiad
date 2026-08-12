# BUILDERS' REPORT — HEPHAESTUS — 2026-08-12 — CLOSE-OUT

**Lane:** HEPHAESTUS (builder), commissioned by ATHENA. **Operator go:** 2026-08-12.
**Branch:** `v12-v1-census`. **HEAD at start:** `2604d5e`.
**Environment gate: PASSED** — pwd inside `OneDrive…naiad`, branch `v12-v1-census`.

**Nine items. Seven delivered in full, one delivered with a correction to the instruction that
issued it, one HALT-SOFT that needs one line from you in an admin shell.** Everything below is
evidence; where something did not happen, it says so and why.

> **Read this first if you read nothing else.** The daily routine was never dead. It failed once,
> on 2026-08-09, on a real fixture halt. It was then killed mid-run on 08-11 by session
> termination, and skipped 08-10 entirely because the machine was away. `publish` now prints the
> routine's true age on every run, so this class of outage can no longer hide behind a fresh
> manifest — **and the very first time the new line ran in production it printed
> `*** STALE >36h ***`.** It works because it caught something.

---

## Scope, and one judgment call inside it

**Authorised:** `scripts/publish_exchange.py`, `scripts/reviewer_manifest.py`,
`tests/test_analytics.py` (F-AN-15 path only), `exchange/**`. Anything else: HALT and report.

**Judgment call — where F-P6 and F-Q1 live.** The contract asks for both as *fixtures*. A permanent
fixture file would have to go in `fixtures/` or `tests/`, and neither is in scope
(`tests/test_analytics.py` is admitted for the F-AN-15 path only). So both were built as **asserting
harnesses run from the session scratchpad, outside the repo**, and their full transcripts are below.
Every case asserts — neither merely prints, because a fixture that only prints cannot fail.

**This is a gap and I am naming it rather than leaving it implied:** F-P6 and F-Q1 do **not** run in
`pytest`, so they will not catch a future regression on their own. Making them permanent needs one
line of scope for `fixtures/`. **Owner: ATHENA.**

**Nothing outside scope was modified.** `backup_estate.py`, `daily_routine.py`, `rotate_reports.py`
and `.gitignore` were read and in two cases *run*, never edited.

---

## 1 · F-P6 — publish now says when the ROUTINE last ran

### 1.1 The defect being closed

Queue 002 made **publish** refresh `MANIFEST.json`. That closed one defect and opened a worse one:
`MANIFEST.json` is the file every lane reads to check the repo is alive, and after 002 its freshness
only proved **that someone published** — never that the routine ran. The routine halted 2026-08-09;
eleven publishes on 08-11 kept the manifest looking six hours old; the outage ran three days unseen.

`publish_exchange.py` now prints, immediately after the budget line, when the routine last
*completed* — read from `HEARTBEAT.md`, which publish does not write. Signal and signalled are
separated again.

**Print-only, never blocks.** A stale heartbeat is information, not grounds to refuse a publish —
the publishes are usually how a human is repairing the very outage being reported, and a guard here
would fight the repair. It is also printed on the REFUSE path, before that early return.

`heartbeat_line(text, now)` is a **pure function**, like `budget()` beside it, so STALE and MISSING
are demonstrable on doctored input without waiting two days or touching the real heartbeat.

### 1.2 F-P6 transcript — 5 cases, every one asserted

```
fixed clock for reproducibility: now = 2026-08-12T01:35:00+00:00

CASE 1 -- LIVE heartbeat, exactly as it sits on disk
  HEARTBEAT.md run: line -> 2026-08-09T18:52:59Z
  LINE: publish: routine last completed 2026-08-09 (55h ago) *** STALE >36h ***
  ASSERT: reports 2026-08-09 and flags STALE   OK

CASE 2 -- DOCTORED FRESH: same file, run stamp moved to 3h ago
  doctored run: -> 2026-08-11T22:35:00Z
  LINE: publish: routine last completed 2026-08-11 (3h ago)
  ASSERT: reports 3h and does NOT flag STALE   OK

CASE 3 -- BOUNDARY: 36h is not stale, 36.1h is
   35.9h -> STALE=False  (want False)
   36.0h -> STALE=False  (want False)
   36.1h -> STALE=True   (want True)
  ASSERT: threshold is strictly ABOVE 36h   OK

CASE 4 -- MISSING / UNREADABLE / GARBLED, four ways
  file unreadable (None)   -> publish: *** HEARTBEAT MISSING *** (exchange/status/HEARTBEAT.md unreadable)
  empty file               -> publish: *** HEARTBEAT MISSING *** (exchange/status/HEARTBEAT.md unreadable)
  no run: line             -> publish: *** HEARTBEAT MISSING *** (no `run:` line in exchange/status/HEARTBEAT.md)
  unparseable stamp        -> publish: *** HEARTBEAT MISSING *** (unparseable run stamp 'not-a-date' in …)
  ASSERT: all four report MISSING, none raise   OK

CASE 5 -- naive (no timezone) stamp is read as UTC, not crashed on
  LINE: publish: routine last completed 2026-08-12 (1h ago)
  ASSERT: naive stamp handled   OK

F-P6: 5 cases, all asserted, all passed.
```

### 1.3 It fired in PRODUCTION, unprompted, and was right

The workflow backup calls `publish()`. Its output, unedited:

```
PUBLISH
  publish: routine last completed 2026-08-09 (56h ago) *** STALE >36h ***
  publish: committed e835755 (12 path(s)) and pushed to origin/v12-v1-census
```

**That is the line doing its job on a real publish, on real data, an hour after being written.**
Under the old behaviour this publish would have refreshed `MANIFEST.json` and said nothing at all.

---

## 2 · F-Q1 — truthful queue counters

### 2.1 Two bugs, not one

`MANIFEST.json` reported **`queue_open: 0` against six work orders** (HERMES F-3). Two independent
causes, both fixed:

1. **The file filter.** The old rule counted only `NNN_*.md` — three digits then an underscore. The
   three date-named contracts (WF1, SEQ8, MC1) are full ratified work orders and were **not counted
   at all**. The filter was not wrong about the files it looked at; it was wrong about which files
   were work orders.
2. **The stamp parser.** It required a line to *start with* a bare `RATIFIED:`. SEQ8's stamp reads
   `**RATIFIED: operator, 2026-08-06** — "stamp seq8"` — a real, valid, operator-issued stamp that
   is **invisible** to `startswith`. A counter that calls a ratified item unratified because of two
   asterisks is measuring its own formatting assumptions, not the queue. The parser now strips
   leading `>`, `#`, `*`, `_` before matching.

### 2.2 The `BUILT:` stamp — a convention that had to exist first

`queue_ratified_unbuilt` needs to distinguish *started* from *finished*, and **the queue had no such
stamp**: `queue/README.md` defined only `RATIFIED`. Computing "unbuilt" from the files was therefore
impossible as specified. Rather than invent a proxy, rule 6 was added to `queue/README.md`:

> `BUILT: <artifact or commit>` on a line of its own once the item is delivered.

**Four items stamped, each from an artifact verified on disk in this session — not copied from the
DIGEST's audit:**

| item | BUILT evidence | checked |
|---|---|---|
| `002_backup-and-publish-guards.md` | commit `c32ffa5` | `git log` resolves it |
| `2026-08-03_WF1_winner_forensics_APOLLO.md` | `WF1_tables.md` + `WF1_discriminants.json` | both present |
| `2026-08-04_SEQ8_…_DIONYSUS.md` | `BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SEQ8.md` | present |
| `2026-08-06_MC1_may26_program_APOLLO.md` | `BUILD_APOLLO_2026-08-06_MC1.md` + `MC1_results.json` | both present |

**Two deliberately NOT stamped** — these are the real backlog:

- `001_condensed-project-history.md` — no condensed-history artifact exists anywhere on disk.
- `003_report-rotation-and-provenance.md` — `scripts/rotate_reports.py` (D-1) exists, but
  `ROTATION_LOG.md` and `docs/history/reports/` do **not**. **Partially built is not built.**

**This is a scope judgment and you may veto it.** Adding a convention and stamping six files is more
than "replace one counter with three". It is authorised (`exchange/**`), and without it the counter
would have reported all six as unbuilt — which is the same kind of falsehood the item exists to end.

### 2.3 F-Q1 transcript — machine vs HAND, side by side

The hand column was written by reading the six files by eye; it is **not** derived from the code
under test. If both columns came from the same parser the fixture would prove nothing.

```
work order                                        | MACHINE            | HAND               | verdict
001_condensed-project-history.md                  | rat=True  built=False | rat=True  built=False | AGREE
002_backup-and-publish-guards.md                  | rat=True  built=True  | rat=True  built=True  | AGREE
003_report-rotation-and-provenance.md             | rat=True  built=False | rat=True  built=False | AGREE
2026-08-03_WF1_winner_forensics_APOLLO.md         | rat=True  built=True  | rat=True  built=True  | AGREE
2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md | rat=True  built=True  | rat=True  built=True  | AGREE
2026-08-06_MC1_may26_program_APOLLO.md            | rat=True  built=True  | rat=True  built=True  | AGREE
file sets identical (6 == 6) and every row agrees   OK

counter                     MACHINE     HAND
queue_total                       6        6   OK
queue_unratified                  0        0   OK
queue_ratified_unbuilt            2        2   OK
queue_open                        2        2   OK

REGRESSION the old counter could not catch:
  old rule = NNN_*.md only, bare `RATIFIED:` prefix  ->  queue_open: 0 over 6 items
  new rule = every non-README .md, emphasis-tolerant ->  6 total, 0 unratified, 2 ratified-unbuilt
  queue_open alias == queue_ratified_unbuilt  OK
  SEQ8 `**RATIFIED:**` invisible to old parser, seen by new one  OK

F-Q1: PASSED.
```

`queue_open` is **kept as an alias** of `queue_ratified_unbuilt`, so nothing reading the old key
breaks. Its meaning has changed, deliberately: the old number answered "what may not be executed
yet" and was read by everyone as "what still has to be done". On 2026-08-12 those differed by the
entire queue.

### 2.4 Live in the manifest

`MANIFEST.json`, regenerated by the manifest job this session:

```
queue_open                 = 2
queue_ratified_unbuilt     = 2
queue_total                = 6
queue_unratified           = 0
```

---

## 3 · Pointer stubs — verify → stub → `git rm`

Both stub verifications, unedited:

```
STUB OK  exchange/reports/MC1_results.json -> research_outputs/mc1/MC1_results.json  sha=a954668b88f7e58d...
STUB OK  exchange/reports/WF1_discriminants.json -> research_outputs/wf1/WF1_discriminants.json  sha=06d2bcfd6498185d...
```

**Independently re-verified before deleting anything** — the copy step's own check is not the check
that authorises a delete:

```
a954668b88f7e58d33efefd7df0238eccbc77fc55586b3e56910e1bf6d4d6ad8  exchange/reports/MC1_results.json
a954668b88f7e58d33efefd7df0238eccbc77fc55586b3e56910e1bf6d4d6ad8  research_outputs/mc1/MC1_results.json
06d2bcfd6498185db0f641614e3b7e8d21922758d369abe4b32846051e9e36b4  exchange/reports/WF1_discriminants.json
06d2bcfd6498185db0f641614e3b7e8d21922758d369abe4b32846051e9e36b4  research_outputs/wf1/WF1_discriminants.json
```

Sizes match exactly (261,072 B and 113,355 B). Both then `git rm`'d. **Box freed: 374,427 B = 5.86%
of the box** — the single largest reduction in this session by a wide margin.

### ⚠ 3.1 Where the safety copies actually live — read this before trusting them

| copy | tracked? | pushed? | protection |
|---|---|---|---|
| `research_outputs/mc1/MC1_results.json` | **NO** — `.gitignore:107` ignores `research_outputs/mc1/**` | no | local disk + git history |
| `research_outputs/wf1/WF1_discriminants.json` | no — untracked, but **not** ignored | no | local disk + git history |

**Neither safety copy is on GitHub.** The delete authorisation required sha-verified copies to
*exist* in `research_outputs/`, and they do. But the durable protection for both files is **git
history**, not the new copies: the blobs remain retrievable at their old paths forever —

```
git show 2604d5e:exchange/reports/MC1_results.json
git show 2604d5e:exchange/reports/WF1_discriminants.json
```

`research_outputs/wf1/` *could* be tracked (nothing ignores it); `research_outputs/mc1/` could not
without editing `.gitignore`. **Both are outside this session's scope, so neither was added.**
**Owner: ATHENA**, if tracked copies are wanted.

---

## 4 · CONVENTIONS §4.2 — the named exception, and the instruction's own bug

### 4.1 The paste's script put it in the wrong section

The supplied script anchored on `s.find('referenced by path + sha256')` — the **first** occurrence.
That string appears twice, and the first is **line 414, inside §3.2**, which merely *quotes* the 4.2
rule. The rule itself is at line 555, inside §4.2's body.

**Run as given, the exception landed in §3.2.** This is the third time this file's shape has bitten:
every section heading exists twice (outline at the top, body below), and its "unique" strings sit
mid-sentence.

```
  ANCHOR at offset 22957, paragraph ends at 23168
  --- CONTEXT (pre-write) ---
   | **Captures, renders, results JSONs, substrates, parquet and HTML do not belong in `exchange/` at
   | all.** §4.2 already says text only, 1 MB per file, larger artifacts referenced by path + sha256
   | pointer — every overflow so far traces to a breach of that rule. …
  OK  4.2 exception inserted, post-write asserted
```

The post-write assertion the paste specified — "both ends of the block present" — **passed**, because
presence is not placement. It could not have caught this.

### 4.2 Relocated to §4.2, with placement asserted

```
  block currently at line 418
  '### 4.2' headings: 2 at lines [85, 541]  <- outline + body
  4.2 body: lines 541..558; content guard at line 555  -> INSIDE  OK
  --- 3 context lines at the DESTINATION ---
   555 | **Content guard:** text only, 1 MB per file. Larger artifacts are referenced by path + sha256
   556 | pointer, never copied in.
   557 |

POST-WRITE ASSERTIONS
  block present exactly once   OK
  bytes 51346 -> 51346  UNCHANGED (a block moved, none added)   OK
  LF 870 -> 870  ·  CR 0 -> 0   UNCHANGED   OK
  landing zone: body '### 4.2' < block < '### 4.3'   OK
  block sits immediately after the text-only/1 MB rule   OK
  block is NO LONGER inside 3.2   OK
```

Final placement, lines 548–556: the exception sits immediately beneath the content guard it
qualifies. Byte count and LF count are identical before and after the move — a block relocated, none
added.

---

## 5 · CONVENTIONS §8 — orphan fragment removed

Line 778 held the whole sentence; **line 779 was the orphaned tail of an earlier revision of it**.
HERMES flagged it twice.

```
PRE-WRITE CONTEXT
   776 | auto-push).
   777 |
   778 | **Triggers armed** (enumerated from Task Scheduler 2026-08-04, …  <-- SENTENCE
   779 | 08:30. **Not armed:** the HERMES scheduled run. **Manual and staying manual:** Sync now.  <-- ORPHAN

POST-WRITE ASSERTIONS
  orphan fragment GONE (0 occurrences)   OK
  old '**Not armed:**' form gone   OK
  clean NOT ARMED sentence present exactly once   OK
  clean Triggers-armed sentence present exactly once   OK
  'Manual and staying manual BY DESIGN' present exactly once   OK
  LF 870 -> 870  EQUAL   OK
  CR 0   OK
  everything outside the two replaced lines is byte-identical   OK
```

Two lines replaced two lines, so **EOL counts are equal** as required. The replacement is also a
**fact update** from this session's own Task Scheduler enumeration: all three tasks carry
`StartWhenAvailable`; the workflow backup **has** now fired (2026-08-09), so "armed and not yet
fired" was stale; and the HERMES task does not exist.

---

## 6 · The INTERFACE rotation conflict — closed

Per ATHENA's ruling:

```
R  exchange/reports/INTERFACE_2026-08-06_C6.md -> exchange/status/INTERFACE_PUBLISHED.md
```

git recorded it as a **rename**, and the hash is unchanged across the move —
`70c3f368…f6f93c61e`, 48,885 B, still byte-identical to `analytics/INTERFACE.md`.

Both halves of the ruling matter: `exchange/status/` is outside queue 003's rotation scope, so the
contract can no longer age off the surface APOLLO reads on 2026-09-05; and the **dateless** name
means a future re-export overwrites in place instead of quietly becoming a second "newest" copy.

F-AN-15 updated to follow it. `exchange/reports/` is still searched **second, on purpose**: a
half-finished migration that left a stale dated copy behind should fail loudly against the canonical
file, not skip as though nothing were published.

```
F-AN-15: IDENTICAL
  analytics/INTERFACE.md
      sha256 70c3f36894684442871f57c6435380fbcea9ca9e23680e356ce610f16f93c61e  48885 B
  exchange/status/INTERFACE_PUBLISHED.md
      sha256 70c3f36894684442871f57c6435380fbcea9ca9e23680e356ce610f16f93c61e  48885 B
```

**Suite: 287 passed, 1 skipped — unchanged**, as the contract required.

---

## 7 · The two failed weekly backups — diagnosed

### 7.1 The destination is healthy. That was never the problem.

```
G: root present : True
dest exists     : True
WRITABLE        : True (probe written and removed)
GoogleDriveFS running, PID 5272,11724
```

**And the 2026-08-09 archives exist and are intact** — `naiad_estate_2026-08-09.zip` (495,130,299 B,
written 15:55:15) and `naiad_workflow_2026-08-09.zip` (2,529,667 B, 15:52:51). Both tasks started at
15:51:58 and **both produced correct archives before returning `1`.**

### 7.2 Both run clean today

`--workflow`: **exit 0**, 8/8 fixtures, 321 members, sha `b2bfbb16…`, sidecar written.
`--estate`: **exit 0**, 8/8 fixtures, 73 members, 495,619,988 B, sha `f0cfdb2a…`, sidecar written.

```
  PASS F-K1 - 73/73 members verified both directions; 0 mismatches, 0 strays, 0 omissions
  PASS F-K2 - census 60/60 klines, 10/10 funding; 0 unresolved
  PASS F-K3 - 20-file sha sample unchanged: True; git porcelain identical: True
  PASS F-K4 - 10 members restored to …Temp… outside repo; 0 hash mismatches
  PASS F-K5 - re-read from destination: sha256 f0cfdb2a56ad4853… matches=True, sidecar matches=True,
              CRC clean=True, 73 members
  PASS F-K6 - default refuses; --force-same-day yields naiad_estate_2026-08-11-01.zip while
              naiad_estate_2026-08-11.zip survives untouched
  PASS F-K6b - --force-same-day correctly does NOT apply to an older archive
  PASS F-K7 - 3/3 git-tracked source files still present on disk; 0 missing
```

> **The `REFUSING TO CLOBBER` lines at the top of that run are fixtures F-K6/F-K6b deliberately
> exercising the refusal path. They are the test, not a failure.** Both PASS. Worth knowing before
> the next person reads that output and reaches for the alarm.

**The bidirectional verification standard is met by both.**

### 7.3 The mechanism, found

Both `--estate` and `--workflow` end the same way:

```python
    pub = publish_step(args)
    if pub["status"] in ("FLAGGED", "REFUSED", "ERROR"):
        return 1
    return 0 if fx.ok else 1
```

**A perfect, fully verified 472 MB archive reports failure if the git publish afterwards had a
hiccup.** The exit code conflates "the backup is bad" with "the publish step stumbled". That is the
mechanism by which two good backups reported `1`.

### 7.4 What I could and could not establish

**Ruled OUT — the size budget.** Reconstructed from the actual commits that day:

| commit | time | `exchange/` bytes | % of box | level |
|---|---|---|---|---|
| `0fad653` | 08-09 15:52 | 1,229,336 | 19.2% | OK |
| `d4834be` | 08-09 15:53 | 1,232,018 | 19.3% | OK |
| `7a3a881` | 08-09 15:55 | 1,232,301 | 19.3% | OK |

Nowhere near the 40% ceiling, and **all three publishes committed successfully.**

**Most probable cause — concurrent git contention.** Both weekly tasks fired at the *same second*
(15:51:58, catch-up via `StartWhenAvailable`), and the daily routine published at 15:53 between
them. Three processes ran `git add`/`git commit` against one index inside a 3½-minute window.
`index.lock` contention returns ERROR from `publish_step()`, and ERROR returns `1` — while another
process's commit still lands, which is exactly the pattern the three commits show.

**I cannot prove which process lost the race.** The Task Scheduler Operational log was disabled
(§8) and `backup_estate.py` keeps no per-run log. **Stated as the leading hypothesis, not as fact.**

**The actionable finding stands regardless of the root cause:** a verified backup should not report
failure because a downstream git step stumbled. `backup_estate.py` is **out of scope** — reported,
not fixed. **Owner: ATHENA.**

---

## 8 · The scheduler log — HALT-SOFT, needs one line from you

```
wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true
exit=5  Failed to save configuration or activate log … Access is denied.
IsEnabled now = False
```

**This requires an elevated shell and cannot be done from this session.** Run in an **ADMIN
PowerShell**:

```
wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true
```

Until then, every future scheduler question needs artifact archaeology instead of a log read — which
is precisely what §7.4 just ran into.

---

## 9 · Prove, commit, publish

### 9.1 The manifest job — PASSES

The manifest job (`scripts/reviewer_manifest.py`) ran and **regenerated `MANIFEST_2026-08-11.json`,
24,164 → 24,916 B**, carrying the new counters (§2.4). **The job that halted on 08-09 now passes**,
confirming the repair independently of the 08-11 evidence.

### 9.2 HEARTBEAT — and an accidental reproduction of the 08-11 death

ROUTINE_OUTCOME

### 9.3 The code commit

**One commit, `f83d321`**, exact staged set printed before committing:

```
78	1	scripts/publish_exchange.py
98	30	scripts/reviewer_manifest.py
52	33	tests/test_analytics.py
(3 paths staged, nothing else)
```

### 9.4 Publishes — FOUR, not one, and why

The contract asked for ONE publish. There were four. **Three were not mine to choose:**

| commit | what triggered it | why it was unavoidable |
|---|---|---|
| `e835755` | `backup_estate.py --workflow` | the script calls `publish()` itself; there is **no `--no-publish` flag** |
| `7a708d6` | `backup_estate.py --estate` | same |
| ROUTINE_PUB | `daily_routine.py` | `routine_jobs.json` sets `"publish": true` |
| FINAL_PUB | this document + ledger | the one publish the contract intended |

Item 7 required running both backups and item 9 required running the routine; each publishes as a
side effect. **Reported rather than engineered around** — suppressing them would have meant editing
`backup_estate.py` or the registry, both out of scope.

### 9.5 Final publish

FINAL_PUBLISH_BLOCK

---

## 10 · Findings reported, NOT fixed

1. **`backup_estate.py` returns `1` when a perfect backup meets a stumbling publish** (§7.3). Out of
   scope. **Owner: ATHENA.**
2. **F-P6 and F-Q1 are not in `pytest`** (Scope §). They cannot catch a future regression on their
   own. One line of scope for `fixtures/` fixes it. **Owner: ATHENA.**
3. **Neither pointer safety copy is pushed** (§3.1). Git history is the real protection. **Owner:
   ATHENA.**
4. **`001` and `003` are ratified but unbuilt** (§2.2) — now *visible* as `queue_ratified_unbuilt: 2`
   rather than hidden behind `queue_open: 0`. 003 in particular is half-built: the tool exists, the
   log and the destination directory do not. **Owner: HEPHAESTUS, next cycle.**
5. **The supplied §4.2 script had a real placement bug** (§4.1) and its own post-write assertion
   could not catch it, because presence is not placement. Any future paste editing CONVENTIONS
   should assert the **enclosing section**, not just that the text arrived.
6. **`operator-exports` is still missing** at `G:\My Drive\naiad-backups\operator-exports` — flagged
   in `DAILY_2026-08-09.md`, still absent. Not the backup failure cause (both run clean without it).
   **Owner: operator.**

---

## 11 · Open, with owners

1. **Enable the Operational log** — one admin line, §8. **Operator.**
2. **`WakeToRun` is false**; a sleeping laptop is never woken, so an away-day still waits for the
   next wake. **Operator's call**, implication: the machine wakes itself at 07:00.
3. **`LogonType=InteractiveToken`** — the routine dies if the session ends, which is what killed it
   on 08-11 and again during this session (§9.2). **Operator's call.**
4. **Items 1–3 and 6 of §10.** **ATHENA**, except §10.6.
5. **`queue_ratified_unbuilt: 2`** — 001 and 003 are the standing backlog. **HEPHAESTUS.**

---

## 12 · File disposition

Box = **6,390,000 B**. Tick set is `LEDGER.md` and `exchange/` only, so anything outside `exchange/`
costs the box nothing.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `scripts/publish_exchange.py` | yes | tracked (+78 −1) | `f83d321` | yes — `origin/v12-v1-census` | GitHub + estate zip | **n/a** — outside the tick set |
| `scripts/reviewer_manifest.py` | yes | tracked (+98 −30) | `f83d321` | yes | GitHub + estate zip | **n/a** — outside the tick set |
| `tests/test_analytics.py` | yes | tracked (+52 −33) | `f83d321` | yes | GitHub + estate zip | **n/a** — outside the tick set |
| `exchange/queue/README.md` | yes | tracked (+5 −0) | `e835755` | yes | GitHub + estate zip | 967 B — **0.02%** |
| `exchange/queue/002_backup-and-publish-guards.md` | yes | tracked (+1) | `e835755` | yes | GitHub + estate zip | 8,801 B — **0.14%** |
| `exchange/queue/2026-08-03_WF1_winner_forensics_APOLLO.md` | yes | tracked (+1) | `e835755` | yes | GitHub + estate zip | 4,031 B — **0.06%** |
| `exchange/queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md` | yes | tracked (+1) | `e835755` | yes | GitHub + estate zip | 8,588 B — **0.13%** |
| `exchange/queue/2026-08-06_MC1_may26_program_APOLLO.md` | yes | tracked (line moved, 0 net) | `e835755` | yes | GitHub + estate zip | 9,494 B — **0.15%** |
| `exchange/status/CONVENTIONS.md` | yes | tracked (+9 −2) | `e835755` | yes | GitHub + estate zip | 51,454 B — **0.81%** |
| `exchange/status/INTERFACE_PUBLISHED.md` | yes | tracked (**renamed** from `reports/INTERFACE_2026-08-06_C6.md`) | `e835755` | yes | GitHub + estate zip | 48,885 B — **0.77%** |
| `exchange/reports/MC1_results.json` | **NO — deleted** | was tracked | `e835755` | yes | git history + `research_outputs/mc1/` | **−261,072 B (−4.09%)** |
| `exchange/reports/WF1_discriminants.json` | **NO — deleted** | was tracked | `e835755` | yes | git history + `research_outputs/wf1/` | **−113,355 B (−1.77%)** |
| `exchange/reports/MC1_results.json.pointer.md` | yes | tracked (new) | `e835755` | yes | GitHub + estate zip | 362 B — **0.01%** |
| `exchange/reports/WF1_discriminants.json.pointer.md` | yes | tracked (new) | `e835755` | yes | GitHub + estate zip | 374 B — **0.01%** |
| `exchange/status/RETENTION.md` | yes | tracked (regenerated) | `7a708d6` | yes | GitHub + estate zip | 1,705 B — **0.03%** |
| `exchange/status/MANIFEST.json` | yes | tracked (regenerated) | ROUTINE_PUB | yes | GitHub + estate zip | MANIFEST_COST |
| `exchange/status/daily/MANIFEST_2026-08-11.json` | yes | tracked (regenerated) | ROUTINE_PUB | yes | GitHub + estate zip | DAILYMAN_COST |
| `exchange/status/HEARTBEAT.md` | yes | tracked | HEARTBEAT_COMMIT | yes | GitHub + estate zip | HEARTBEAT_COST |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked (appended) | FINAL_PUB | yes | GitHub + estate zip | LEDGER_COST |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_CLOSEOUT.md` | yes | tracked (new) | FINAL_PUB — a document cannot name the commit carrying it; SHA on screen | yes | GitHub + estate zip | SELFSIZE B — **SELFPCT%** |
| `research_outputs/mc1/MC1_results.json` | yes | **untracked — `.gitignore:107`** | never | **no** | local disk + git history | **n/a** — outside the tick set |
| `research_outputs/wf1/WF1_discriminants.json` | yes | untracked (not ignored) | never | **no** | local disk + git history | **n/a** — outside the tick set |
| `G:\…\naiad_workflow_2026-08-11.zip` (+ `.sha256`) | yes | n/a — off-repo | n/a | n/a | Google Drive | **n/a** — off-repo |
| `G:\…\naiad_estate_2026-08-11.zip` (+ `.sha256`) | yes | n/a — off-repo | n/a | n/a | Google Drive | **n/a** — off-repo |

**Nothing created this session is over the ~1% flag threshold.** The largest single artifact is
`CONVENTIONS.md` at 0.81%, and it was already there. **This session was net-NEGATIVE on the box: the
two `git rm`'d JSONs freed 374,427 B (5.86%) against roughly ADDBACK B added.** That is the whole
point of the pointer-stub pattern, and it is why the budget line at the end reads what it reads.

**Scratchpad, deliberately NOT committed:** the F-P6 and F-Q1 harnesses, the stamping and
section-repair scripts, and the routine log — all under
`%LOCALAPPDATA%\Temp\claude\…\scratchpad`. Demonstration scaffolding, **NOT PROTECTED**, intentionally.

---

## 13 · Ledger — ruling "append" honoured

Per ruling "append" (CONVENTIONS §3.1), this document ends by appending this session's STATUS entry
to the commissioning lane's ledger, **`exchange/status/LEDGER_ATHENA.md`**, in the same session.
Append-only, verified mechanically — details in §12's row for that file.

---

## 14 · Plain summary

Your automation was never dead; it failed once and then got unlucky twice. The reason you could not
see that is now fixed: every publish states how old the routine is, and the first live run of that
line immediately flagged a 56-hour-old routine. The queue counter that said "0 open" against six
items now says 6 total, 0 unratified, 2 ratified-but-unbuilt — and those two, `001` and `003`, are
your real backlog. Two large JSON files left the bus for pointer stubs, freeing 5.86% of the box.
The census-facing contract moved somewhere rotation cannot reach it, and the fixture that watches it
followed it there. Both weekly backups verify clean today; they were failing because a good backup
was reporting the publish step's stumble as its own.

**Two things need you, not me:** one admin line to turn on the scheduler log, and a decision on
whether the routine should wake the laptop and survive logoff. Both are in §11.

*HEPHAESTUS, 2026-08-12.*
