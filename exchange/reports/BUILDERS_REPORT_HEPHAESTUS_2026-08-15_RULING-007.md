# BUILDERS REPORT — HEPHAESTUS — 2026-08-15 — RULING 007

**Retire DIGEST · hibernate HERMES · automate the residue.**

**Lane:** HEPHAESTUS (builder) · **Commissioned by:** operator, ruling 007, 2026-08-15 ·
**Branch:** `v12-v1-census` · **Base:** `20f23a1` · **Supersedes:** queue/006 (never filed — see §1.3)

---

## 0 · What this is, in one paragraph

Ruling 007 says DIGEST and HERMES-as-author are not needed, because the collapse's self-reporting
sources replace them. So: the DIGEST is retired to `docs/history/` with a tombstone left at its old
path, the HERMES charter is marked DORMANT with each duty routed to whatever now discharges it, and
the handful of measurements that lane produced **by hand each cycle** are now taken **by the two
steps that already run every day** — `publish()` and the daily routine. A hand-built index goes
stale silently. That is what happened to the DIGEST, and it is the whole argument for this change.

**The one thing to read if you read nothing else:** ruling 007's own `git mv` staged a path outside
`publish_exchange.SCOPE`. Had the routine published before this was committed by hand, the guard
would have FLAGGED, `git reset` would have destroyed the staged rename, and the next publish would
have committed the tombstone **over** the DIGEST inside `exchange/` while the final edition was
never committed at all — leaving a tombstone pointing at a file that existed nowhere. Found by
adversarial review, not by me. §5, finding V-1.

---

## 1 · The retirement

### 1.1 The move
```
git mv exchange/DIGEST.md docs/history/DIGEST_RETIRED_2026-08-15.md
```
16,090 B left `exchange/`. The rename and the tombstone are in **one commit**, which is both what
makes `--follow` work across it and what keeps the publish guard away from the staged rename.

`--follow` was **proved, not assumed**: the exact commit shape was replayed in a `--no-hardlinks`
clone and `git log --follow -- docs/history/DIGEST_RETIRED_2026-08-15.md` returned the same 9
commits back to 2026-08-02 that `--follow` on the old path returned before the move. It works
despite the old path *surviving* as the tombstone because `try_to_follow_renames` sets
`find_copies_harder`, so the byte-identical destination is still paired with the modified source.

### 1.2 The tombstone — 561 B at `exchange/DIGEST.md`
It names the successors and nothing else. **One deviation from the ruling's dictated text, stated
plainly:** the ruling said MANIFEST.json is *"refreshed every publish"*. It is not. `publish()`
never imports `reviewer_manifest` and never writes MANIFEST.json; the only writer is the daily
routine's `manifest` job. Writing the dictated sentence would have put a false claim into the
tombstone whose entire purpose is to end a false-claims problem, so the tombstone says **written by
the daily routine** and names the resulting gap as finding F-4. A second wording change came out of
review: MANIFEST.json is **not** a file inventory (§5, V-6), so the tombstone credits it with *repo
state* and points "what the bus is carrying" at the bus-health block instead.

### 1.3 queue/006 and the staleness banner — both absent, by enumeration
- **queue/006 does not exist.** `ls exchange/queue` → `001, 002, 003, 004` + four dated items +
  README; `git ls-files` agrees; MANIFEST `queue_total = 8`. The earlier paste never ran, so there
  is nothing to mark WITHDRAWN. **Reported honestly:** the queue directory is a weak inventory —
  **005 is equally absent** yet is cited as worked and ratified in eight tracked files. "Not in
  `exchange/queue/`" therefore does not establish "never commissioned".
- **No staleness banner ever existed.** `git grep -i 'staleness banner'` → zero hits, tracked or
  untracked, anywhere in history. What the DIGEST carried is a hand-typed `## 8 · Staleness`
  **table**, and the new six-lane ledger-recency table is its measured successor.

---

## 2 · CONVENTIONS — the surgical edits

Anchor context (≥3 lines either side) was printed before every write, per rule D-4. Every edit was
asserted after writing, then F-CONV re-run. **A transcription caution worth recording:** a review
agent returned a "verbatim" anchor line reading `**RULE — A regola DIONYSUS's challenges...`, which
is not in the file. All edits were made against my own reads, never against agent-quoted text.

| # | where | change |
|---|---|---|
| a | §0 THE MAP | the `exchange/DIGEST.md` row is gone. Current state is now lane ledgers → `LEDGER.md` STANDING VERDICTS → the bus-health/budget blocks, with a dated RETIRED note below the table. Still three rows, so §0's "three places" claim survives. |
| b | §5 HERMES | charter row is **DORMANT (2026-08-15, ruling 007)**; a block below routes each duty. |
| c | §4.2 / §4.3 | tree diagram entry becomes a tombstone marker; the tick-set BECAUSE no longer rests on a hand index. |
| + | header line 4, §MAINTENANCE line 839 | **added after review** — both still assigned HERMES a *live* staleness duty, contradicting the dormancy block 521 lines away. The correction rule says rewrite every place that asserts the fact, headings first. |
| + | `exchange/README.md:16` | the bus table's DIGEST row, the last live/normative pointer outside CONVENTIONS. |

**The HELIOS tripwire is intact, byte-identical** — verified by diffing the surrounding 12 lines:
*"BECAUSE a verifier who re-authors is not verifying — the HELIOS tripwire."* with its RULE above
and *"EARNED-BY Standing. HERMES never self-verifies."* below. It binds any future coordinator.

**Duties: five absorbed, two PARKED and named.** The first draft claimed *every* duty was absorbed.
Review showed **"files drops"** had vanished from the charter with no successor, so §5 now says so
outright: nothing names and files `exchange/drops/`, and the queue-003 unacted-inbox list has no
home. Both are operator calls. Claiming full absorption would have been the same defect as a stale
index — a confident sentence nobody had checked.

### 2.1 F-CONV — the constant this forced, and the protocol it ran
The three edits grew CONVENTIONS past `CONV_BYTES_BEFORE = 64_012`, failing F-CONV-4's "size
shrinks" clause. **The fixture's own docstring rules on exactly this case:** re-pin with a dated
note saying what grew and why — *"never to delete a rule or trim a correction to get back under a
number."* Growth here is a DORMANT charter, a duties block, a revival condition and three dated
corrections. All law. So the law stayed and the baseline moved.

**§6.4 named-constant protocol, all three legs:**
1. **Grep NAME, VALUE, THRESHOLD TEXT** — `CONV_BYTES_BEFORE` (5 sites, all in the fixture);
   `64_012 / 64,012` (1 live + 4 historical); `"size shrinks"` (1 live + 2 filed).
2. **Every dependent, pin-vs-import recorded** — one live consumer (`fixtures_conventions.py`,
   edited); four historical pins left **untouched**: `LEDGER_ATHENA.md:623`,
   `BUILDERS_REPORT_..._COLLAPSE.md:318,320,473`, `docs/CONVENTIONS_RULE_CENSUS_2026-08-15.md:17`.
3. **Historical regenerators stay pinned** — which is why `CONV_BYTES_BEFORE` was **not
   overwritten**. It means *"the size immediately before the collapse"*; changing its value would
   make its own name false and silently restate three filed documents against a number that did not
   exist when they were written. A **new** `CONV_BYTES_CEILING` carries the live clause instead.

Two further fixture corrections came out of review:
- **The ceiling carries headroom.** My first attempt pinned it at *exactly* the current size — zero
  headroom, so the next one-word correction fails the fixture, which is a standing invitation to
  trim law to make it pass. Now 66,500 B against 65,703 B.
- **A live rule-count clause was added.** F-CONV-4's "zero rules lost" clause reads the rule census,
  a document frozen at the collapse (its own terminal figure is 64,008 B), so as a *live* guarantee
  it certifies a revision that no longer exists. Its label is now narrowed to **"zero rules lost IN
  THE 2026-08-15 COLLAPSE (frozen evidence)"** and a new clause counts top-level `**RULE —` lines
  against a **floor** of 89 — measured 89 at the collapse commit and 89 now, both sides.

---

## 3 · Bus health — the residue, automated

Four components, and the split between `publish()` and the daily routine is **measured cost, not
taste**:

| component | publish() | daily §8 | why |
|---|---|---|---|
| per-folder breakdown (bytes, files) | ✅ | ✅ | free in publish — `sized` is already computed for the budget; aggregating is ~0.06 ms and **zero** new git calls |
| manifest head vs live HEAD | ✅ | ✅ | one `rev-parse` + one small json read |
| ledger recency, six lanes | — | ✅ | a new parser over ~235 KB, on a function documented *"Never raises"* that runs up to eleven times a day |
| rotation candidates (queue 003) | — | ✅ | **147 ms**, of which 145 ms is six `git log --follow` subprocesses; also a circular import (`rotate_reports` already imports `publish_exchange`) |

**The head pair prints even when the two agree** — the ruling's headline clause — and it also prints
on the `NOTHING` path, where `publish()` skips the budget block entirely. That is precisely the run
where a manifest 33 commits behind is likeliest and least visible.

**Live block, this session** (rendered, not described):

```
| lane | newest entry | age (days) | entries |
|---|---|---:|---:|
| **APOLLO** | 2026-08-15 | 0 | 26 entry header(s) |
| **ARGUS** | 2026-08-11 | 4 | 2 entry header(s) |
| **ATHENA** | 2026-08-15 | 0 | 24 entry header(s) |
| **DIONYSUS** | 2026-08-13 | 2 | 3 entry header(s) |
| **HEPHAESTUS** | 2026-08-15 | 0 | 2 entry header(s) |
| **HERMES** | 2026-08-04 | 11 | 2 entry header(s) · DORMANT (ruling 007) — not expected to move |

| manifest records | `d830ecb` |
| live HEAD | `20f23a1` |
| verdict | **F-4 LAG** — manifest behind by 33 commit(s) |
```

The DORMANT label is a review fix: without it, the block that **absorbed** HERMES's staleness duty
reported HERMES as the stalest lane in the project, by a margin growing one day per day forever,
while §5 tells the reader nothing waits on HERMES. The successor surface would have contradicted
the ruling that created it.

**The recency reader knows all three live header forms**, because a reader that knows one is finding
F-5 — a false staleness reading that reads as another lane's neglect, committed for real on
2026-08-12:

| form | where it is live |
|---|---|
| `=== STATUS_ARGUS — 2026-08-11 ===` | the naiad-eod template, all six ledgers |
| `=== STATUS ATHENA — 2026-08-15 ===` | a **space**, not an underscore — five of ATHENA's most recent entries |
| `## 2026-08-11 — ARGUS acknowledges…` | ARGUS's newest entry, and **only** this form |

Both patterns anchor on a real ISO date, which excludes the fenced `<date>` template line present in
all six files and stops APOLLO's `2026-08-15b` sequence suffix corrupting the date. Anchoring on the
**header** rather than any date excludes forward-looking rotation due-dates in prose — a naive grep
returns 2026-08-28 and 2026-09-05 for two lanes exactly that way.

**Amendment recorded, not done quietly.** `daily_routine.py`'s docstring asserted *"the ONLY git
operations are the final PUBLISH step's"*. §8 reads live git (`rev-parse HEAD`, and `rev-list` only
when the heads differ — both read-only). A dated AMENDMENT stanza now says so, because a section
whose whole subject is manifest-versus-git cannot answer the question from the manifest alone.

---

## 4 · The coupling nobody commissioned: rotation

`scripts/rotate_reports.py` was **the only executable file in the repo that reads DIGEST.md**
(enumerated: `git grep`, plus `scripts/ tests/ fixtures/ .github/ *.json *.plist` and
`~/Library/LaunchAgents/`; every other hit is `hashlib.hexdigest()` or prose).

Retiring the DIGEST would have made `digest_inbox_names()` return **a plausible non-zero wrong
answer**, not an empty one. The `start is None` fallback scrapes `.md` basenames from the whole
file, so against the tombstone it returns 2 names and the dry-run banner prints
`DIGEST inbox : 2 name(s) parsed` — an operator reading that sees a **successful parse of an inbox
that no longer exists**. Six live unacted notes silently lose their exemption, and the **first
becomes a rotation candidate on 2026-09-03** (measured by stepping `classify()` day by day; the
naive "date + 30" gives 2026-09-02 and is one day early, because the comparison is strict).

**Fixed by refusing to answer, not by guessing.** The two unanswerable states now raise
`InboxSourceUnavailable`; `main()` turns it into a loud `exit 2` that moves nothing.

**No ratified policy was touched** — `AGE_DAYS`, `SCOPE_DIR`, `NOTE_RE` and the `name in inbox` test
are exactly as queue 003 ratified them. What changed is only what happens when the rule's **input
cannot be obtained**: the script used to invent an answer and now refuses. *Refusing to compute is
not a policy decision; guessing was.* The builder holds no queue drafting rights, so restoring the
exemption is the operator's call — a one-line repoint of `DIGEST_PATH` once its new home is ruled.

It is a `RuntimeError`, deliberately **not** a `SystemExit`: the CLI halts loudly while the daily
routine catches it and reports. A `SystemExit` here would have killed an unattended 07:00 run.

**The count still prints.** `classify()` gained an `inbox=` override used by exactly one caller —
the report — so ruling 007's fourth component is a number and not a shrug. It is labelled an **UPPER
BOUND with the exemption NOT APPLIED**. `rotate()` never passes it, so the actual sweep still halts.

---

## 5 · Findings from adversarial review — what it caught in my own work

Five independent agents were run against the finished build with instructions to refute it. They
found defects I had not, including one that would have destroyed the retirement. All are **fixed**
unless marked otherwise.

| # | finding | severity | status |
|---|---|---|---|
| **V-1** | `git mv` staged `docs/history/…` — **outside** `SCOPE`. A publish would have FLAGGED, `git reset` would have destroyed the staged rename, and the next publish would commit the tombstone **over** the DIGEST while the final edition was never committed. Proven end-to-end in a clone. | **blocking** | fixed by commit design: rename + tombstone + fixture in one hand commit **before** any publish |
| **V-2** | `manifest_head()` raised `AttributeError` on any manifest that is valid JSON but not an object (`[]`, `null`, `"str"`). Not in `publish()`'s except clause → escapes a function documented *never to raise*, and kills the daily report, heartbeat **and** publish. | **blocking** | fixed (`isinstance` check + fixture clause) |
| **V-3** | Two-dot `recorded..HEAD` returns 0 when the manifest is **ahead**, rendering *"F-4 LAG · manifest is 0 commit(s) behind"* — the one relation this block exists to state, stated wrongly. | important | fixed (`--left-right --count`, with AHEAD/DIVERGED verdicts) |
| **V-4** | `ledger_recency` took `max()` over unvalidated dates: one typo'd or future-dated header pins a lane "fresh" **forever**, hiding a stale ledger. F-5 in the direction the obvious fixture does not test. | important | fixed (parse, drop future/impossible, **report the discard**) |
| **V-5** | The DAILY table re-implemented the head verdict inline — a second renderer, untested, and the one that lands in the published report. The ruling's headline clause was pinned only on the console copy. | important | fixed (one `head_verdict()`, shared; two new fixture clauses) |
| **V-6** | §0 called MANIFEST.json a **file inventory**. It is not: `sources` is 46 hardcoded engine/script paths and `reviewer_box` is 29 paths **all under `exchange/status/`** — it lists no report on the bus. | important | fixed (§0, §4.3 and the tombstone reworded) |
| **V-7** | Header line 4 and §MAINTENANCE still gave HERMES a live staleness duty. | important | fixed |
| **V-8** | §5 claimed *every* duty absorbed; **"files drops"** had no successor. | important | fixed (named as PARKED) |
| **V-9** | The recency table reported dormant HERMES as the stalest lane, forever. | important | fixed (DORMANT label) |
| **V-10** | `basis` string said *"staged for this commit"* while reporting the whole index — false on any publish changing 3 files of 148. | important | fixed |
| **V-11** | §8 was unguarded in `main()`, before the report write, the heartbeat **and** the publish. | important | fixed (degrades to NOT ENUMERABLE) |
| **V-12** | F-BH-1 soft spots: deleting the ISO anchor still passed 16/16; entry counts unpinned. | minor | fixed (25 clauses now) |
| **V-13** | F-CONV-4's census clause certifies a frozen revision. | important | fixed (label narrowed + live rule-count floor) |

### Reported, NOT fixed — operator calls
1. **`exchange/reports/PRIMER_HERMES_2026-08-11_v4.md:102`** still instructs HERMES to *"Rebuild
   `exchange/DIGEST.md` in full"* every cycle, and `:46` restates the D-2 rotation duty. It is a
   live **instruction surface for another lane**, and superseding it is a HERMES-lane instruction
   requiring the operator's ratification (§5). Untouched deliberately.
2. **Queue 003 D-2** names HERMES's DIGEST budget section as where the rotation-candidate list is
   published each cycle. Retirement orphans that clause. The bus-health block now publishes the
   figure, but re-homing a **ratified** cadence is not the builder's to do.
3. **The unacted-inbox list has no home.** Deadline **2026-09-03**, when the first note becomes a
   candidate. Until then rotation halts rather than guess.
4. **Two `docs/memory/` snapshots** (`NAIAD_MEMORY_VERBATIM_2026-08-15.md:189,326`) record HERMES's
   duty as *"DIGEST 2x/day, box budget, staleness stamps, inbox"*. They mirror the **live Claude
   project-memory panel**, which only the operator can edit. Repo snapshots left alone.
5. **F-BH-1 does not run in CI.** `.github/workflows/ci.yml` runs `pytest fixtures/ -v` only, so
   `tests/` — including the pre-existing F-BOX-1 — never executes on push. One-line fix
   (`pytest fixtures/ tests/`) **not applied**: widening CI scope is an ops decision and could turn
   the build red on unrelated environment-dependent tests.
6. **Latent F-CONV-1 defect:** its "definition" regex `^#{1,6} .*«TOKEN»` treats any **Python
   comment** starting `# ` as a markdown heading, so a code comment citing a token in guillemets
   fails the fixture. Worked around by citing without guillemets and saying so at the site.

---

## 6 · Gate values, as printed

```
F-CONV: 4/4 PASS
[PASS] F-CONV-1: 9 tokens, all count==2 (...); repo-unique outside CONVENTIONS: yes
[PASS] F-CONV-2: section 0 = 5,334 B of 6,000 B budget (88.9%), headroom 666 B
[PASS] F-CONV-3: 5 memory-pointer tokens, 5 resolve to a section header
[PASS] F-CONV-4: zero rules lost IN THE 2026-08-15 COLLAPSE (frozen evidence): census 422 -> 422,
       LOST 0 · size within ceiling: 65,703 B of 66,500 B ceiling (headroom 797 B); pre-collapse
       64,012 B, +1,691 B since · every narrative backlinked: 27 cases in CASELAW, all carry EARNS ·
       every case cited from CONVENTIONS: all CL-n resolve both ways · rule count holds: 89 top-level
       rules, floor 89 (+0)
```

```
pytest            324 passed, 1 skipped in 15.00s   (325 collected)
pytest fixtures    73 passed, 1 skipped in  6.48s   ( 74)
pytest tests      251 passed              in  8.92s  (251)
                                                     74 + 251 = 325  ✓
```

**SUITE SCOPE, RECONCILED AND RE-MEASURED — the quoted baseline was stale.** The figure carried in
the ledgers is *"287 passed / 1 skipped = 288 = fixtures 74 + tests 214"*. Measured live at
`20f23a1` **before** this build: **299 passed / 1 skipped = 300 = fixtures 74 + tests 226**. The +12
is exactly `tests/test_box_guard.py`, added 2026-08-15. A third version, *"286 passed / 1 skipped"*,
sits in `LEDGER_ARGUS.md`. **This number demonstrably propagates by copying** — the reason ruling
007 exists. This build adds F-BH-1's 25 clauses: 300 → **325**. Do not re-quote 288.

```
rotate_reports -- HALT: the unacted-inbox exemption has no source.  ...  Exit 2.
```

---

## 7 · File disposition

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `docs/history/DIGEST_RETIRED_2026-08-15.md` | yes | tracked (renamed) | hand commit | yes | GitHub | **−16,090 B** (left `exchange/`) |
| `exchange/DIGEST.md` | yes | tracked | hand commit | yes | GitHub | 561 B · 0.004% |
| `exchange/status/CONVENTIONS.md` | yes | tracked | publish | yes | GitHub | 65,703 B · 0.411% |
| `exchange/README.md` | yes | tracked | publish | yes | GitHub | 2,163 B · 0.014% |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_RULING-007.md` | yes | tracked | publish | yes | GitHub | this file |
| `exchange/status/LEDGER_HEPHAESTUS.md` | yes | tracked | publish | yes | GitHub | appended |
| `scripts/publish_exchange.py` | yes | tracked | hand commit | yes | GitHub | n/a |
| `scripts/daily_routine.py` | yes | tracked | hand commit | yes | GitHub | n/a |
| `scripts/rotate_reports.py` | yes | tracked | hand commit | yes | GitHub | n/a |
| `scripts/fixtures_conventions.py` | yes | tracked | hand commit | yes | GitHub | n/a |
| `scripts/mc1_report.py` | yes | tracked | hand commit | yes | GitHub | n/a |
| `tests/test_bus_health.py` | yes | tracked | hand commit | yes | GitHub | n/a |

**Net box effect: `exchange/` SHRINKS by ~15,500 B** — the DIGEST's 16,090 B leaves, a 561 B
tombstone and ~1,700 B of new CONVENTIONS law arrive.

**Rollback:** `git revert <hand-commit-sha>` then `git revert <publish-sha>`; the DIGEST returns to
`exchange/DIGEST.md` with history intact. Nothing was deleted, so nothing is unrecoverable.

**Noted:** other sessions were writing to this repo concurrently (`a5e7a5c` VIZ-4 landed mid-session;
tierc3 files are untracked now). `publish()` stages all of `exchange/` by design, so this publish
carries any other session's `exchange/reports/` files too. My hand commit lists explicit paths only.
