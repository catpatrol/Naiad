# BUILDERS REPORT — HEPHAESTUS — 2026-08-11 — QUEUE 003

## Report rotation, rerun provenance, and the anchor-context rule

**Lane:** HEPHAESTUS · **Date:** 2026-08-11 · **Branch:** `v12-v1-census` · **Head at start:** `759ad2a`
**Contract:** `exchange/queue/003_report-rotation-and-provenance.md` — RATIFIED operator 2026-08-11.
**Verdict: ACCEPT.** All eight fixtures pass with output printed; every verdict criterion holds.

D-1 + D-2 shipped together as required. D-3 and D-4 shipped alongside them.

---

## 1 · Verdict criteria

| criterion | evidence | verdict |
|---|---|---|
| every fixture passes with output printed | §3–§6 | **PASS** 8/8 |
| script provably contains no delete path — grep empty | §2 | **PASS** |
| every rotated file sha-identical at destination **and** reachable by `git log --follow` | F-303-2, F-303-3 | **PASS** |
| nothing outside `exchange/reports/` moved | §6 — nothing moved at all; `git status` shows zero renames | **PASS** |
| D-3 / D-4 landed at the positions their printed context shows | §5 | **PASS** |

---

## 2 · The no-delete proof

The central invariant of D-1 is that it **moves and never destroys**. The contract requires this be
grepped, not asserted:

```
$ grep -nE 'os\.remove|rmtree|unlink' scripts/rotate_reports.py
--- begin grep ---
--- end grep (empty above = PASS) ---

  wider net: grep -cE 'shutil|os\.rmdir|\.rm\(|remove\(' -> 0 hits
```

Empty. `shutil` is not imported at all. The only mutation the script performs is `git mv`.

**Why `git mv` rather than copy-then-remove:** a copy plus a removal loses the rename record and
`git log --follow` stops at the move. A rotated build document whose history stops is worth less
than one never rotated — the entire point is that the record stays retrievable. F-303-3 asserts the
history genuinely follows.

**The 30-day window is a constant, not a flag.** No `--days` option exists. A rotation window that
can be widened from the command line will be widened at the moment someone wants a file gone, which
is precisely the moment to refuse.

---

## 3 · Sandbox fixtures F-303-1 … F-303-5

Run against a fabricated git repo in a temp dir outside this repo, holding eight reports: two clearly
old, a 31-day boundary file, a 29-day boundary file, a fresh file, an exempt inbox note listed in a
fabricated DIGEST §4, a stale note absent from that DIGEST, and an undated `TABLES.md` committed with
a back-dated author date so the `git log` fallback has something old to find.

### F-303-1 · dry-run selects exactly the >30d set

```
rotate_reports -- DRY RUN (default)
  today        : 2026-08-11   window: 30 days   cutoff: files dated before 2026-07-12
  DIGEST inbox : 1 name(s) parsed from exchange/DIGEST.md
  before       : 1,001 B, 0.0% of the 6,390,000 B box

  CANDIDATES  : 5 file(s), 584 B, 0.01% of box
      2026-07-11         95 B  exchange/reports/BUILDERS_REPORT_EDGE_2026-07-11_thirtyone.md  (date from filename)
      2026-06-12        242 B  exchange/reports/BUILDERS_REPORT_OLD_2026-06-12_beta.md  (date from filename)
      2026-07-02        202 B  exchange/reports/BUILDERS_REPORT_OLD_2026-07-02_alpha.md  (date from filename)
      2026-06-27         12 B  exchange/reports/NOTE_GHOST_to_NOBODY_2026-06-27_closed.md  (date from filename)
      2026-06-22         33 B  exchange/reports/TABLES.md  (date from git log)
  EXEMPT      : 1 file(s)
             13 B  exchange/reports/NOTE_ARGUS_to_APOLLO_2026-06-27_open_question.md  -- unacted inbox note in DIGEST
  TOO YOUNG   : 2 file(s) inside the 30-day window

  DRY RUN: nothing moved. Re-run with --execute to move the candidates.

  PASS F-303-1   selected 5 = expected set True; exempt note excluded=True; 29d excluded=True;
                 nothing moved=True
```

Four selection paths exercised at once: filename date, `git log` fallback (`TABLES.md`), the DIGEST
exemption holding a live note back, and a same-shaped note **not** in the DIGEST correctly selected.

### F-303-2 · `--execute` moves, verifies at destination, logs one line each

```
  moving (sha256 -> git mv -> re-hash at destination):
      MOVED    exchange/reports/BUILDERS_REPORT_EDGE_2026-07-11_thirtyone.md -> docs/history/reports/2026-07/...  sha256=b15c5f16414d37a2...  (95 B, verified at destination)
      MOVED    exchange/reports/BUILDERS_REPORT_OLD_2026-06-12_beta.md       -> docs/history/reports/2026-06/...  sha256=c0bc7ded67d240a5...  (242 B, verified at destination)
      MOVED    exchange/reports/BUILDERS_REPORT_OLD_2026-07-02_alpha.md      -> docs/history/reports/2026-07/...  sha256=9680c77d3919af66...  (202 B, verified at destination)
      MOVED    exchange/reports/NOTE_GHOST_to_NOBODY_2026-06-27_closed.md    -> docs/history/reports/2026-06/...  sha256=8dd4de9d43133567...  (12 B, verified at destination)
      MOVED    exchange/reports/TABLES.md                                    -> docs/history/reports/2026-06/...  sha256=001a1011c9564403...  (33 B, verified at destination)

  wrote 5 line(s) to exchange/status/ROTATION_LOG.md
  after        : 417 B, 0.0% of the 6,390,000 B box
  5 moved, 0 refused/failed

  PASS F-303-2   rc=0; 5/5 landed under docs/history/reports/YYYY-MM (2026-06,2026-07);
                 sha256 identical=True; originals absent=True; ROTATION_LOG rows=5
```

Bus fell 1,001 B → 417 B. Each file is hashed before the move and re-hashed **at its destination**.

### F-303-3 · history follows

```
  PASS F-303-3   `git log --follow -- docs/history/reports/2026-06/TABLES.md` -> 2 commit(s):
                 ['rotation sweep', 'add tables']
```

`add tables` is the pre-move commit. The history survives the rotation, which is the whole claim.

### F-303-4 · idempotence

```
  CANDIDATES  : 0 file(s), 0 B, 0.00% of box
      (none -- nothing on the bus is older than the window)
  EXECUTE: no candidates; nothing to move.

  PASS F-303-4   rc=0; second run selected 0 candidate(s); ROTATION_LOG still 5 row(s) (no duplicates)
```

### F-303-5 · the 29-day file never moves

```
  PASS F-303-5   BUILDERS_REPORT_EDGE_2026-07-13_twentynine.md still on the bus=True;
                 absent from history=True (survived two --execute runs)
```

The 31-day file moved and the 29-day file did not, across two `--execute` runs. The boundary is real.

```
SANDBOX FIXTURES: 5/5 PASS
  F-303-1 PASS   F-303-2 PASS   F-303-3 PASS   F-303-4 PASS   F-303-5 PASS
```

---

## 4 · F-303-6 · the real tree

**(a) dry-run**

```
rotate_reports -- DRY RUN (default)
  scope        : exchange/reports/*.md
  today        : 2026-08-11   window: 30 days   cutoff: files dated before 2026-07-12
  destination  : docs/history/reports/YYYY-MM/
  DIGEST inbox : 4 name(s) parsed from exchange/DIGEST.md
  before       : 1,701,083 B, 26.6% of the 6,390,000 B box

  CANDIDATES  : 0 file(s), 0 B, 0.00% of box
      (none -- nothing on the bus is older than the window)
  EXEMPT      : 4 file(s)
         18,065 B  exchange/reports/NOTE_ARGUS_to_APOLLO_2026-08-03_census_candidates.md  -- unacted inbox note in DIGEST
          4,375 B  exchange/reports/NOTE_ARGUS_to_ATHENA_2026-08-03_publish_exchange_push_scope.md  -- unacted inbox note in DIGEST
          7,275 B  exchange/reports/NOTE_DIONYSUS_to_APOLLO_2026-08-04_range_detection_scoping.md  -- unacted inbox note in DIGEST
          5,645 B  exchange/reports/NOTE_DIONYSUS_to_APOLLO_2026-08-04_SEQ8_findings_and_agreements.md  -- unacted inbox note in DIGEST
  TOO YOUNG   : 50 file(s) inside the 30-day window
```

**(b) the real `--execute` sweep, same session**

```
rotate_reports -- EXECUTE
  before       : 1,701,083 B, 26.6% of the 6,390,000 B box
  CANDIDATES  : 0 file(s), 0 B, 0.00% of box
  EXECUTE: no candidates; nothing to move.
```

| | before | after |
|---|---|---|
| `exchange/` tracked | 1,701,083 B | 1,701,083 B |
| % of 6,390,000 B box | **26.6%** | **26.6%** |

**Empty, exactly as the contract predicted.** The oldest report on the bus is dated 2026-07-28; the
cutoff is 2026-07-12. The three undated files resolve by `git log` to 2026-08-02, 2026-08-04 and
2026-08-10 — all inside the window. Nothing was eligible and nothing moved. Per the contract, a
near-empty result today is expected and is not a failure.

Two things the real run proved that the sandbox could not: the DIGEST parser found **all four** live
inbox notes and held them back, and the `git log` fallback resolved all three undated files rather
than guessing. **An unknown age is treated as not-old** — the script reports undated files and never
selects them, because guessing in the direction of "move it" is the wrong guess.

---

## 5 · F-303-7 · D-3 and D-4, with anchor context printed BEFORE writing

D-4's own rule, applied to the paste that installs D-4.

**Line endings, measured on both sides:** before `CRLF=0 LF=833 bytes=48410` → after
`CRLF=0 LF=855 bytes=50218`. LF-only preserved.

### Anchor for D-4 — `### 2.3 Write every gate`, **2 hits**

```
     73| ### 2.1 Routing and the environment assertion
     74| ### 2.1b · Every paste-go carries a ROLLBACK line
     75| ### 2.2 Exact paste-ready text — MOVED FROM MEMORY #7, full text
 >   76| ### 2.3 Write every gate from the POST-action state
     77| ### 2.4 Design for autonomy — MOVED FROM MEMORY #14 + #16, merged, full text
     78| ## §3 · How to hand work back — ONE document
     79| ### 3.1 The build document
    280| Applies to: git commands, builder one-liner questions, and contract go-pastes.
    281| Purpose: the operator pastes and goes, with no reconstruction on his side.
    282|
 >  283| ### 2.3 Write every gate from the POST-action state
    284| *(From the reviewer error taxonomy, Class B. Stays in memory #23; the cure is restated here
    285| because it is a drafting procedure.)*
    286|
```

**This is the rule earning its keep on its own installation.** Two hits: line 76 is the heading
OUTLINE, line 283 is the section body. A count-based guard would have reported "found it" and
written into the index. The context shows which is which — line 76 is surrounded by other headings,
line 283 by prose. D-4 went in at the end of the §2.3 **body**, after its "Logged instances"
paragraph and before `### 2.4`.

### Anchor for D-3 — end of the R3 rule, **1 hit**

```
    545| A rerun exists to prove byte-identity, and the hash IS that proof. Print both digests in the build
    546| document, then delete the rerun copy in the same session. Never retain it: three retained _run2
    547| trees held ~3.2 GB of pure redundancy (seq8_run2 relocated 2026-08-11; journal_s3_run2 and
 >  548| s3_events_run2 live inside the s3 phase archive). Every study contract inherits this clause.
    549|
    550| ---
    551|
```

### Where they landed, verified after writing

```
  D-4 at line 295, inside: ### 2.3 Write every gate from the POST-action state
  D-3 at line 562, inside: ### 4.3 Confirming a file is actually visible — rule added 2026-08-03
```

D-4 is in §2.3 as the contract specifies. D-3 is in §4 as the contract specifies — directly beneath
the R3 rule it refines, which sits at the end of §4 (nearest preceding subheading 4.3). A refinement
belongs adjacent to the rule it refines, not in a separate subsection.

Diff: **22 insertions, 0 deletions**, one file.

---

## 6 · F-REG, and the finding the fixtures surfaced

**F-REG:** publish still works and 002's D3 guard meters the post-sweep bus — see §8, which shows the
budget line on this session's own publish.

### The finding: a real rotation will trip the publish scope guard

Not theorised — measured in the sandbox after a real `--execute`:

```
      staged after git mv : 5 path(s)
      guard(staged)       : ok=False, 5 offender(s) outside exchange/
        docs/history/reports/2026-06/BUILDERS_REPORT_OLD_2026-06-12_beta.md
        docs/history/reports/2026-06/NOTE_GHOST_to_NOBODY_2026-06-27_closed.md
        docs/history/reports/2026-06/TABLES.md
        docs/history/reports/2026-07/BUILDERS_REPORT_EDGE_2026-07-11_thirtyone.md
```

`git mv` stages **both** halves of a rename, and the destination is `docs/history/reports/…` —
outside `exchange/`. If a rotating session then calls `publish_exchange.publish()`, the scope guard
FLAGS the index and resets it. The worktree move survives; the staging does not.

That guard is behaving correctly — it exists so evidence never auto-publishes, and it cannot know a
`docs/` path is a legitimate rotation. **The procedure is therefore: the rotating session commits the
rotation itself, then publishes `exchange/` separately.** The script prints this instruction after any
non-empty sweep, so the next operator to run it is told at the moment it matters rather than
discovering it from a FLAG line. It did not arise today because the sweep was empty.

---

## 7 · D-2 · cadence

D-2 requires no code and no new instruction surface, as the contract states. The `--dry-run` output
in §4(a) **is** the artifact: it prints candidate count, bytes, and % of box — exactly the three
figures HERMES's box-budget section needs each cycle — plus the exempt and too-young tallies.

`DIGEST.md` was **not edited**. It is HERMES's surface and no verdict criterion asks for it; a builder
writing into another lane's section would be the defect this project already has a rule against.
**For HERMES:** run `python scripts/rotate_reports.py` (dry-run is the default, it moves nothing) and
paste the CANDIDATES block. Today it reads zero.

Nothing rotates unattended. `--execute` is never implied.

---

## 8 · Disposition table

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `scripts/rotate_reports.py` | yes (new) | tracked | see §9 | see §9 | GitHub + `--workflow` archive | n/a — `scripts/` not in the tick set |
| `exchange/status/CONVENTIONS.md` | yes | tracked | see §9 | see §9 | GitHub + estate zip | **+1,808 B** (D-3 and D-4), 0.028% of box |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-003.md` | yes (new) | tracked | see §9 | see §9 | GitHub + estate zip | see §9 |
| `exchange/queue/003_report-rotation-and-provenance.md` | yes | tracked, **unchanged** | unchanged | unchanged | GitHub + estate zip | 0 |
| `exchange/status/ROTATION_LOG.md` | **no** | — | — | — | — | 0 — created on first non-empty sweep; today's was empty |
| `docs/history/reports/` | **no** | — | — | — | — | 0 — nothing landed |
| `exchange/reports/**` (54 files) | yes | tracked | unchanged | unchanged | GitHub + estate zip | **0 — nothing moved, zero renames in `git status`** |
| fixture harness `q003_fixtures.py` | scratchpad only | not in repo | no | no | **NOT PROTECTED — §3 is its record** | 0 — outside the repo |

---

## 9 · Publish

```
publish: WARNING -- exchange/ holds 1,717,591 B, 26.9% of the 6,390,000 B box
         (warn at 25%, refuse above 40%).
publish: committed ce16233 (2 path(s)) and pushed to origin/v12-v1-census
status= PUBLISHED commit= ce16233 pushed= True bytes= 1717591 budget= WARN
```

**F-REG satisfied:** publish works and 002's D3 guard metered the post-sweep bus at 26.9%.

| commit | contents | pushed |
|---|---|---|
| `f3efb0f` | `scripts/rotate_reports.py` (D-1) | not by this commit — carried by the next branch push, per the §11 finding of the 002 report |
| `ce16233` | `exchange/status/CONVENTIONS.md` (D-3, D-4) + this report | yes, by the guard |

Box cost of the whole contract: **+1,808 B** of `CONVENTIONS` and this report. The bus rose from
26.6% to 26.9% delivering the machinery that will lower it — the first sweep with anything to move
is around 2026-08-27.

---

## 10 · Open items

1. **The rotation/publish-guard interaction (§6) should reach `CONVENTIONS.md` §3.3 or §3.4**, where
   the publish procedure lives. It is currently documented only here and in the script's own output.
   Not done — 003's scope is D-1..D-4 and `CONVENTIONS` edits beyond those were not authorised.
2. **Rotation will not relieve the bus for roughly two more weeks.** The oldest report is 2026-07-28,
   so the first non-empty sweep is around 2026-08-27. Between now and then `exchange/` keeps growing
   at the measured rate. If the bus nears 40% before that date, the lever available is §8.2 of the
   002 report — `MC1_results.json` (261 KB) and `WF1_discriminants.json` (113 KB) are data files in
   `exchange/` that §4.2 says do not belong there, worth ~5.9 points between them.
3. **The fixture harness is not permanent**, same as 002's. Both now exist only as transcripts.
   `tests/test_rotate_reports.py` plus `tests/test_backup_publish_guards.py` would put D-1 and 002's
   D1–D3 under F-REG; that is one ruling and one session.
4. **Four inbox notes have been exempt and unanswered since 2026-08-03/04.** The exemption is correct
   and will hold them on the bus indefinitely — an unanswered note is never rotated. That is the rule
   working, but it means 35,360 B stays hot until APOLLO and ATHENA reply.

---

## 11 · Rollback

- `git checkout -- exchange/status/CONVENTIONS.md` reverts D-3 and D-4.
- `scripts/rotate_reports.py` is a new file; removing it reverts D-1.
- No file was moved, no file was deleted, `ROTATION_LOG.md` was never created, and
  `docs/history/reports/` does not exist. There is no rotation to undo.
