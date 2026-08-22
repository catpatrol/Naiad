# BUILDER'S REPORT — HEPHAESTUS — ROOT ADJUDICATION, ROTATION REPAIR, STAMPS

**Lane** HEPHAESTUS (local Claude Code at `~/Naiad`) · **Branch** `v12-v1-census` · **HEAD at start**
`04656c2` · **Commissioned by** the operator directly, 2026-08-22 · **Executed** 2026-08-22.

Follows `BUILDERS_REPORT_HEPHAESTUS_2026-08-18_BOX-CLEANUP-MAILBOX.md` and closes four of the six
findings it left open (F-1, F-2, F-3) or resolves them to a decision the operator must make (F-4, F-5).

---

## 0 · WHAT THIS IS, IN PLAIN LANGUAGE

Five things happened. **One file left the index, no file left the disk, and nothing was deleted.**

1. **The root was adjudicated in the open.** Every one of the 91 things at the top of `~/Naiad` was
   given a verdict with the exact `file:line` that pins it there. **86 KEEP · 4 MOVED · 1 note-only.**
   The answer the operator wanted is the table itself: after the 2026-08-18 sweep, the root is
   almost entirely load-bearing — nearly every remaining document is read by code.
2. **The rotation was repaired.** It had been dead for seven days. It now runs, exits 0, and its
   exemption is computed from the bus instead of read from a file that no longer exists.
3. **One index-only removal.** `exchange/.DS_Store` is no longer tracked. **The file on disk was not
   touched** — same 8,196 bytes, same sha256, before and after.
4. **One deletion was REFUSED by its own gate.** The `" copy.txt"` file turned out to have no twin.
   Deleting it would have destroyed the only copy of a live document. Details in §4 — including a
   bug in my first version of the gate that would have authorised exactly that.
5. **Two stamps** so the queue's backlog counter stops under-reporting.

---

## 1 · THE ROOT, ADJUDICATED

`git status --untracked-files=all`, root scope, at session start:

```
 M scripts/oracle_fixtures.py       <- another session's, untouched here
 M scripts/oracle_wrapper.py        <- another session's, untouched here
?? (root)                            no untracked file at the root itself
```

Every root entry, with the citation that pins it. **KEEP means a `grep -rInF` of the basename
across `scripts/ fixtures/ tests/ engine/` returned a hit**, and the first hit is printed; a
directory is out of this sweep's remit (the brief moves files); a rule-kept file names the rule.

| root entry | kind | bytes | verdict | the citation that pins it (or why it moves) | ignored by |
|---|---|--:|:-:|---|---|
| `engine_1.0.2_noshrink_packet_20260711.zip` | packet zip | 17,371 | **MOVED** | 0 code references; operator-ferried transport bundle -> `research_outputs/packets/`, its named home (6 siblings already there) | `.gitignore:48 *.zip` |
| `engine_1_0_3_input_parity_packet_20260712.zip` | packet zip | 15,815 | **MOVED** | 0 code references; operator-ferried transport bundle -> `research_outputs/packets/`, its named home (6 siblings already there) | `.gitignore:48 *.zip` |
| `ssv11_3_grade_legibility_packet_20260711.zip` | packet zip | 48,242 | **MOVED** | 0 code references; operator-ferried transport bundle -> `research_outputs/packets/`, its named home (6 siblings already there) | `.gitignore:48 *.zip` |
| `v12_v1_census_packet_20260711.zip` | packet zip | 17,634 | **MOVED** | 0 code references; operator-ferried transport bundle -> `research_outputs/packets/`, its named home (6 siblings already there) | `.gitignore:48 *.zip` |
| `.claude` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `.DS_Store` | osjunk | 14,340 | **NOTE ONLY** | OS junk; untracked and ignored by `.gitignore:209 .DS_Store`. Removing it is a deletion of an operator-machine file, not a repo act | `.gitignore:209:.DS_Store` |
| `.git` | dir | — | **KEEP** | git itself | — |
| `.gitattributes` | rule | 1,797 | **KEEP** | git reads it only at the root of the worktree | — |
| `.github` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `.gitignore` | rule | 12,318 | **KEEP** | git reads it only at the root of the worktree | — |
| `.pytest_cache` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | `.gitignore:21:.pytest_cache/` |
| `_reviewer_box` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | `.gitignore:90:_reviewer_box/` |
| `analytics` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `briefs` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `census.json` | results JSON | 62,741 | **KEEP** | pinned by `scripts/backup_estate.py:13` (+20 more) | — |
| `CENSUS.md` | document | 8,653 | **KEEP** | pinned by `scripts/backup_estate.py:761` (+14 more) | — |
| `census1b_results.json` | results JSON | 68,351 | **KEEP** | pinned by `scripts/census1b_analyze.py:5` (+12 more) | — |
| `census1b_termini_enriched.jsonl` | substrate JSONL | 33,641,414 | **KEEP** | pinned by `scripts/census1b_analyze.py:6` (+16 more) | `.gitignore:84:/census1b_termini_enriched.jsonl` |
| `Census_1_Amendment_1.md` | document | 9,659 | **KEEP** | pinned by `scripts/census_build.py:4` | — |
| `Census_1_MTF_Signal_Stack_Builder_Contract.md` | document | 17,804 | **KEEP** | pinned by `scripts/census_build.py:3` (+1 more) | — |
| `CENSUS_1b.md` | document | 16,797 | **KEEP** | pinned by `scripts/census1b_analyze.py:7` (+2 more) | — |
| `census_results.json` | results JSON | 21,468 | **KEEP** | pinned by `scripts/census_analyze.py:4` (+3 more) | — |
| `CHANGELOG.md` | document | 34,431 | **KEEP** | pinned by `scripts/v12_packet.py:49` (+3 more) | — |
| `claude` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `configs` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `DATA_CENSUS.md` | document | 11,483 | **KEEP** | pinned by `scripts/backup_estate.py:761` (+9 more) | — |
| `data_starts.csv` | data CSV | 4,955 | **KEEP** | pinned by `scripts/census.py:147` (+6 more) | — |
| `docs` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `engine` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `exchange` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `fixtures` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `GAP_REPORT.md` | document | 1,214 | **KEEP** | pinned by `scripts/census.py:4` (+2 more) | — |
| `journal` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | `.gitignore:12:/journal/` |
| `LEDGER.md` | rule | 259,298 | **KEEP** | publish_exchange.py:120 `TICK_EXTRA = ("LEDGER.md",)` — it IS half the box's tick set | — |
| `logs` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | `.gitignore:206:logs/` |
| `MAILBOX` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | `.gitignore:261:MAILBOX/` |
| `naiad-backups` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | `.gitignore:172:naiad-backups/` |
| `Naiad_Phase0_Charter.md` | document | 20,584 | **KEEP** | pinned by `scripts/packet.py:53` | — |
| `Naiad_Phase1_Build_Prompt.md` | document | 14,497 | **KEEP** | pinned by `scripts/packet.py:54` | — |
| `ops` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `pine` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `prompts` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `pytest.ini` | rule | 596 | **KEEP** | pytest discovers its config by walking up to the rootdir; `testpaths = fixtures tests` lives here | — |
| `RC7_Amendment_1.md` | document | 8,857 | **KEEP** | pinned by `scripts/rc7_recompute.py:4` | — |
| `RC7_Amendment_2.md` | document | 7,158 | **KEEP** | pinned by `scripts/rc7_recompute.py:4` | — |
| `RC7_PostS1_Recompute_Builder_Contract.md` | document | 14,139 | **KEEP** | pinned by `scripts/rc7_recompute.py:3` | — |
| `rc7_results.json` | results JSON | 57,394 | **KEEP** | pinned by `scripts/rc7_recompute.py:809` (+1 more) | — |
| `RC7_RESULTS.md` | document | 24,824 | **KEEP** | pinned by `scripts/rc7_recompute.py:811` (+3 more) | — |
| `rc_recompute.json` | results JSON | 83,980 | **KEEP** | pinned by `scripts/rc_recompute.py:1434` (+2 more) | — |
| `RC_RECOMPUTE_RC0_RC6.md` | document | 29,101 | **KEEP** | pinned by `scripts/rc_recompute.py:1435` (+1 more) | — |
| `RC_Recompute_RC0_RC6_Builder_Contract.md` | document | 16,298 | **KEEP** | pinned by `scripts/rc_recompute.py:4` (+1 more) | — |
| `README.md` | rule | 9,683 | **KEEP** | the repository's front door; GitHub renders it at the root and nowhere else | — |
| `recompute.json` | results JSON | 57,735 | **KEEP** | pinned by `scripts/rc_recompute.py:1434` (+6 more) | — |
| `requirements.txt` | rule | 88 | **KEEP** | the dependency manifest; pip reads the path it is given, and every doc gives this one | — |
| `research` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `research_outputs` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `S1_Instrumented_Replay_Builder_Contract.md` | document | 21,307 | **KEEP** | pinned by `scripts/s1_runner.py:107` (+1 more) | — |
| `S1_MEASUREMENT.md` | document | 20,651 | **KEEP** | pinned by `scripts/s1_fixtures.py:777` | — |
| `s1_results.json` | results JSON | 50,186 | **KEEP** | pinned by `scripts/s1_fixtures.py:773` (+3 more) | — |
| `S2_Instrumented_Pass_Builder_Contract.md` | document | 19,134 | **KEEP** | pinned by `scripts/s2_runner.py:107` (+1 more) | — |
| `S2_MEASUREMENT.md` | document | 8,003 | **KEEP** | pinned by `scripts/s2_fixtures.py:618` (+1 more) | — |
| `s2_results.json` | results JSON | 12,481 | **KEEP** | pinned by `scripts/s2_fixtures.py:591` (+1 more) | — |
| `S2B_DECOMPOSITION.md` | document | 10,002 | **KEEP** | pinned by `scripts/s2b_decompose.py:443` (+2 more) | — |
| `S2b_Decomposition_Addendum_Builder_Contract.md` | document | 9,236 | **KEEP** | pinned by `scripts/s2b_decompose.py:3` | — |
| `s2b_results.json` | results JSON | 14,351 | **KEEP** | pinned by `scripts/s2b_decompose.py:441` | — |
| `S3_ENRICHMENT.md` | document | 9,697 | **KEEP** | pinned by `scripts/s3_enrich.py:14` (+2 more) | — |
| `S3_Enrichment_Builder_Contract.md` | document | 14,792 | **KEEP** | pinned by `scripts/s3_enrich.py:2` (+1 more) | — |
| `s3_excursion_substrate.jsonl` | substrate JSONL | 6,007,227 | **KEEP** | pinned by `scripts/wf1_forensics.py:11` (+6 more) | — |
| `s3_results.json` | results JSON | 60,679 | **KEEP** | pinned by `scripts/s3_enrich.py:14` (+3 more) | — |
| `scripts` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `skills` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `SPOT_CHECK.md` | document | 7,296 | **KEEP** | pinned by `scripts/spot_check.py:3` (+5 more) | — |
| `SS_Cascade_v11_0_2.pine` | pine source | 56,785 | **KEEP** | pinned by `engine/signals.py:1` | — |
| `study` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `TC1_DEFINITIONS.md` | document | 3,492 | **KEEP** | pinned by `scripts/tc1_fixtures.py:4` | — |
| `TC1_Factorial_Builder_Contract.md` | document | 10,479 | **KEEP** | pinned by `scripts/tc1_fixtures.py:4` | — |
| `tc1_results.json` | results JSON | 8,140 | **KEEP** | pinned by `scripts/tc1_fixtures.py:451` (+1 more) | — |
| `TC1_RESULTS.md` | document | 3,899 | **KEEP** | pinned by `scripts/tc1_fixtures.py:453` (+1 more) | — |
| `tc4_baseline.json` | results JSON | 12,785 | **KEEP** | pinned by `scripts/tc4_fixtures.py:7` (+1 more) | — |
| `TC4_BASELINE.md` | document | 7,045 | **KEEP** | pinned by `scripts/tc4_fixtures.py:7` (+2 more) | — |
| `TC4_Engine_1_0_8_Builder_Contract.md` | document | 15,314 | **KEEP** | pinned by `scripts/tc4_fixtures.py:3` (+2 more) | — |
| `TC5_Intraday_Respec_Builder_Contract.md` | document | 8,341 | **KEEP** | pinned by `scripts/tc5_fixtures.py:3` (+1 more) | — |
| `tc5_results.json` | results JSON | 7,597 | **KEEP** | pinned by `scripts/tc5_fixtures.py:448` | — |
| `TC5_RESULTS.md` | document | 4,205 | **KEEP** | pinned by `scripts/tc5_fixtures.py:450` (+1 more) | — |
| `tests` | dir | — | **KEEP** | directory — outside this sweep's remit (the brief moves FILES) | — |
| `V12_Study_Charter_Addendum_v1.0.md` | document | 11,892 | **KEEP** | pinned by `scripts/tierc3_rules.py:134` (+2 more) | — |
| `V12_V1_Census_Build_Prompt.md` | document | 14,040 | **KEEP** | pinned by `scripts/v12_packet.py:48` | — |
| `v12_v3_anchor_packet_20260713.zip` | packet zip | 45,537,070 | **KEEP** | pinned by `scripts/v3_scorer.py:393` | `.gitignore:48:*.zip` |
| `V3_RECOMPUTE_R1_R10.md` | document | 34,072 | **KEEP** | pinned by `scripts/rc_recompute.py:12` (+2 more) | — |
| `V3_Recompute_R1_R10_Builder_Contract.md` | document | 20,745 | **KEEP** | pinned by `scripts/v3_recompute.py:4` (+1 more) | — |
| `V3_STOP_AND_EXIT_FORENSICS.md` | document | 8,943 | **KEEP** | pinned by `scripts/v3_recompute.py:10` (+2 more) | — |

### 1.1 · The headline: almost nothing at the root was movable, and that is the finding

**91 entries adjudicated: 86 KEEP · 4 MOVED · 1 note-only** — 26 directories, 61 files, and the 4
files that left. Of the 86 keeps:

| | count |
|---|--:|
| directories — outside a file sweep's remit | 26 |
| documents pinned by a live code reference | 36 |
| data and artifact files pinned by a live code reference | 18 |
| kept by rule (`LEDGER.md`, `README.md`, `.gitignore`, `.gitattributes`, `pytest.ini`, `requirements.txt`) | 6 |
| **total** | **86** |

`scripts/census_build.py` reads `Census_1_Amendment_1.md`; `scripts/tc4_fixtures.py` reads
`TC4_BASELINE.md`; `engine/version.py` reads `CHANGELOG.md`; `engine/data.py` reads
`data_starts.csv`. **Zero root files came back unreferenced and unruled** — the sweep found no
leftovers at all.

**So the operator is looking at the rule-kept set, and the table is the answer.** The 2026-08-18
sweep already removed everything that was merely sitting there. What is left is either load-bearing
or named by rule, with one exception class — the packet zips — dealt with below.

**Two things the brief expected that are not there, stated rather than passed over:**

- **There is no `requirements-lock*` file.** The brief's example pinned one to an "M1 bootstrap doc".
  Enumerated: `find . -maxdepth 2 -name 'requirements*'` returns exactly one path, `./requirements.txt`
  (88 B). The lock file does not exist at the root or one level below it, so nothing was adjudicated
  for it. `requirements.txt` is kept as the dependency manifest.
- **There is no untracked file at the root.** Root-scope `git status --untracked-files=all` is empty
  apart from two `scripts/oracle_*.py` modifications belonging to another session, which were left
  alone and are not committed here.

### 1.2 · The four MOVEs, and the fifth zip that stayed

Four operator-ferried packet zips had been at the root since July with **zero code references**.
They went to `research_outputs/packets/`, which is their named home — the `.gitignore` comment at
line 47 calls these *"operator-ferried session packets (transport bundles, never the source of
record)"*, and six siblings were already there.

```
ROOT SWEEP -- 4 packet zips -> research_outputs/packets/
method: sha256 -> move -> sha256 at destination -> require equal (rotate_reports.sha256_file)
NOTE: these are UNTRACKED and *.zip-ignored, so this is a FILESYSTEM move, not a git rename.

  OK   engine_1.0.2_noshrink_packet_20260711.zip        -> research_outputs/packets/
       sha256 f20bf1f2732ae3b6c8bfc57c7f82096969edb6f53aa8dc3d15d9d406b2b39fe0  EQUAL
  OK   engine_1_0_3_input_parity_packet_20260712.zip    -> research_outputs/packets/
       sha256 6846cac33a171bf1ead98ec46ab5eb00377a1acdafce3d162ef72be87d12c1d9  EQUAL
  OK   ssv11_3_grade_legibility_packet_20260711.zip     -> research_outputs/packets/
       sha256 a22f11d641aeda48efb7aa50cf7b1bcc27da8e6b647f4af57461d549b665f8f6  EQUAL
  OK   v12_v1_census_packet_20260711.zip                -> research_outputs/packets/
       sha256 88af8a5495dea29287a813ad84e5a542f2689a0b34b058618f28f55c18135c31  EQUAL

moved OK: 4   failures: 0
ROTATION_LOG: 4 row(s) appended
```

**Three things about these moves that a reader must not assume:**

1. **They are not git renames.** All four are untracked and `*.zip`-ignored (`.gitignore:48`), so
   git has never held these bytes. `git log --follow` will not find them. The verification is the
   sha256 pair, which is why the rotation primitive was used rather than `git mv`.
2. **Their protection did not change, and it is NONE.** Measured before moving, not assumed:
   `backup_estate.WORKFLOW_SOURCES` does not contain `research_outputs`, and
   `WORKFLOW_ROOT_GLOBS = ("*.md",)`, so these zips were outside the workflow archive at the root
   and are outside it at the destination. The estate archive covers the price-data cache, not the
   repo. **They were unprotected before and they are unprotected now** — the move is tidiness, not
   filing. Their source of record is the tracked study output each was built from.
3. **They are recorded in `ROTATION_LOG.md` under a provenance block that says they do not belong
   there.** That log's header scopes it to *"build documents moved off the exchange bus"*. These are
   neither. They are logged by explicit operator instruction, and the widening is named in the log
   itself so a future reader does not trip over zip rows in a document about build documents.

**The fifth zip stayed.** `v12_v3_anchor_packet_20260713.zip` (45,537,070 B) is pinned by
`scripts/v3_scorer.py:393` — `pk = ROOT / "v12_v3_anchor_packet_20260713.zip"`. Under the rule the
brief states, **the citation is what pins a file to KEEP**, so it kept it.

> **Named, because it is the one loose end this leaves:** that reference is a **write** target, not
> a read. `v3_scorer.py` *creates* that zip at the root, so a rerun of the V3 anchor scorer will put
> a new 45 MB packet back at the root. Moving it would therefore have needed the line changed in the
> same act — authorised by the standing rule, but a change to study code inside a tidy commit, which
> I did not make on my own authority. **One word and it moves with a one-line repoint.**

### 1.3 · OS junk — note only, as instructed

`~/Naiad/.DS_Store` (14,340 B) is untracked and ignored by `.gitignore:209`. It is a macOS Finder
file belonging to the operator's machine, not to the repository. **Note only; nothing done.**

---

## 2 · F-2 REPAIR — the rotation runs again

### 2.1 What was broken

Queue 003's D-1 exempted *"any `NOTE_*_to_*` file listed as unacted inbox in the newest DIGEST"*.
Ruling 007 retired `exchange/DIGEST.md` on 2026-08-15 and left a tombstone at its path. The
exemption's only input died with it, and from that day `rotate_reports.py --dry-run` **halted with
exit 2** before classifying anything. The script was right to refuse — guessing which notes are live
is exactly the guess that rotates a live message off the bus — but **no rotation could run at all**,
and nothing noticed for seven days because nothing calls it on a schedule.

### 2.2 The contract amendment — correction REPLACES

`exchange/queue/003_report-rotation-and-provenance.md`, D-1. Anchor context printed before writing,
occurrence count asserted as 1, document re-read after (§6.4 corollary).

**BEFORE** (quoted once, asserted nowhere):

> `kind.** Exemptions, checked per file: any `NOTE_*_to_*` file listed as unacted inbox in the`
> `newest DIGEST; anything under `exchange/status/`, `queue/`, or `DIGEST.md` (out of scope by`
> `construction).`

**AFTER, as it now reads in the contract:**

> `kind.** Exemptions, checked per file: **any `NOTE_*` file that is the NEWEST note of its`
> `lane pair** — sender→recipient parsed from the filename, broadcasts grouped as`
> `` `<LANE>→ALL-LANES` ``, `newest by filename date with mtime as tie-break; anything under`
> `` `exchange/status/`, `queue/`, or `DIGEST.md` `` `(out of scope by construction).`

A dated `CORRECTION 2026-08-22` block at the foot of the contract records what changed and why. **A
second stale assertion was corrected in the same act:** D-2's cadence clause named *"HERMES's
box-budget section in the DIGEST"*, and HERMES has been dormant since ruling 007 — it now names the
bus-health block, which has been doing that job since.

### 2.3 The implementation, and the two widenings named rather than slipped in

`scripts/rotate_reports.py`: `digest_inbox_names()` and `DIGEST_PATH` are **gone** — grep returns
nothing — replaced by `note_pair()` and `newest_note_per_lane_pair()`.

**Widening 1 — the note pattern.** `NOTE_RE` went from `^NOTE_.+_to_.+` to `^NOTE_`. The old pattern
only ever matched `NOTE_<FROM>_to_<TO>_…`. **Broadcasts never matched it**, so
`NOTE_HERMES_2026-08-12_ALL-LANES_…` and `NOTE_DIONYSUS_2026-08-12_PANTHEON_…` were **never
exemptible at all**, even on the days the DIGEST read worked. That was a live hole in the ratified
rule, not something this correction introduced, and it is now closed. F-ROT-4 pins it.

**Widening 2 — the input.** The exemption is computed from `exchange/reports/` itself. **A rule with
no external input has no unavailable state**, which is the property the DIGEST version lacked and
the reason it could break. F-ROT-5 pins it.

**What did NOT change:** `AGE_DAYS = 30`, `SCOPE_DIR`, `DEST_ROOT`, the sha256→`git mv`→sha256
discipline, the no-delete invariant, `--dry-run` as the default, and the out-of-scope list. F-ROT-6
and F-ROT-7 pin those.

`InboxSourceUnavailable` is **retained but never raised** — `daily_routine.rotation_candidate_lines()`
names it in an `except` clause, and deleting a class one caller references to gain nothing is a
break for its own sake. Its docstring now says plainly that it is no longer raised.

### 2.4 THE PROOF — `--dry-run` exits 0 and prints its candidate set

```
rotate_reports -- DRY RUN (default)
  scope        : exchange/reports/*.md
  today        : 2026-08-22   window: 30 days   cutoff: files dated before 2026-07-23
  destination  : docs/history/reports/YYYY-MM/
  exemption    : 10 note(s) -- newest of their lane pair, computed from exchange/reports/ (queue 003 correction 2026-08-22)
      EXEMPT  APOLLO         -> ATHENA     NOTE_APOLLO_2026-08-15_TO_ATHENA_box-governance-handoff.md
      EXEMPT  ARGUS          -> APOLLO     NOTE_ARGUS_to_APOLLO_2026-08-16_rulings_relay.md
      EXEMPT  ARGUS          -> ATHENA     NOTE_ARGUS_to_ATHENA_2026-08-03_publish_exchange_push_scope.md
      EXEMPT  ATHENA         -> APOLLO     NOTE_ATHENA_to_APOLLO_2026-08-11_data-residency.md
      EXEMPT  ATHENA         -> ARGUS      NOTE_ATHENA_to_ARGUS_2026-08-11_DATA-RESIDENCY.md
      EXEMPT  DIONYSUS       -> ALL-LANES  NOTE_DIONYSUS_2026-08-12_PANTHEON_lane_status_and_census_challenge.md
      EXEMPT  DIONYSUS       -> APOLLO     NOTE_DIONYSUS_to_APOLLO_2026-08-04_SEQ8_findings_and_agreements.md
      EXEMPT  HEPHAESTUS     -> ATHENA     NOTE_HEPHAESTUS_2026-08-15_TO_ATHENA_digest-refresh-contract-draft.md
      EXEMPT  HERMES         -> ALL-LANES  NOTE_HERMES_2026-08-12_ALL-LANES_DIGEST-REFRESH.md
      EXEMPT  HERMES         -> ATHENA     NOTE_HERMES_to_ATHENA_2026-08-12_STALE-CLONE-DETECTION.md
  before       : 2,298,068 B, 14.4% of the 16,000,000 B box

  CANDIDATES  : 0 file(s), 0 B, 0.00% of box
      (none -- nothing on the bus is older than the window)
  EXEMPT      : 10 file(s)
  TOO YOUNG   : 52 file(s) inside the 30-day window

  DRY RUN: nothing moved. Re-run with --execute to move the candidates.
EXIT=0
```

**Exit 0, 0 candidates — expected, and it is the right answer**: the 2026-08-18 named-set sweep just
ran, so nothing on the bus is older than the 30-day window. The instrument works; there is simply
nothing for it to select.

### 2.5 The fixture — and a correction to the brief's own number

The brief asked: *"the six currently-unacted notes appear in the exemption list by name."*

**There are TEN, and the six does not reproduce from the tree.** The "six" came from a count
hardcoded into the ruling-007 error string — *"six unacted notes are unprotected, the first becoming
a candidate 2026-09-03"*. I tried to derive it and could not. Measured against the bus as it stood
at the tip before the 2026-08-18 sweep (`git ls-tree 98951cd^`):

| measured | count |
|---|--:|
| `NOTE_*.md` on the bus just before the 08-18 sweep | 14 |
| — of those, dated on or before 2026-08-15 (when the "six" was written) | **13** |
| — of those 13, matched by the old `^NOTE_.+_to_.+` pattern | **9** |
| — of those 13, broadcasts the old pattern could never match | **4** |
| `NOTE_*.md` on the bus today, every one the newest of its lane pair | **10** |

**No reading of the tree yields six** — not 13, not 9, not 10. So the figure was not a measurement
that has since drifted; it was a number with no derivation, sitting inside an error message where
nothing could ever check it. **It is now gone along with the function that carried it**, which is
the right outcome.

The count that IS true today is **10**, and every one of them is printed above by name.

**The fixture is therefore stated as a RULE, not a count** — *every* note that is the newest of its
lane pair must appear by name, whatever that number happens to be — so it cannot go stale the way
"six" did, and it will still be right the day the eleventh note lands. `scripts/rotation_exemption_fixtures.py`, **F-ROT 7/7 PASS**:

| leg | FAILS IF | observed |
|---|---|---|
| F-ROT-1 classifies | `classify()` raises — the ruling-007 halt is still there | raised nothing |
| **F-ROT-2 live notes exempt by name** | any newest-of-pair note is absent from the exemption list | **10 live, 10 exempt, 0 missing** |
| F-ROT-3 superseded note rotates | the older note of a pair is exempted too | kept only the 08-16 note |
| F-ROT-4 broadcasts exemptible | a broadcast is not exemptible — the old pattern's gap | 2 exempt; matched by the OLD pattern: **0** |
| F-ROT-5 no external input | the module still reads a DIGEST path, or fails with no DIGEST present | read removed ✓, computes ✓ |
| F-ROT-6 no delete path | any delete call in the module — queue 003's verdict criterion | none |
| F-ROT-7 AGE_DAYS pinned | the correction touched a ratified constant | `AGE_DAYS = 30` |

> **A BUG THE FIXTURE CAUGHT ON ITS FIRST RUN, reported because finding it is the fixture's whole
> point.** F-ROT-3 fabricates a temp tree outside the repo. `newest_note_per_lane_pair()` called
> `path.relative_to(REPO)` unconditionally and raised `ValueError` on it. The function had only ever
> been pointed at the live bus, so nothing had exercised that path. Fixed: a note outside the repo
> has no git history, so only its filename can date it, and that is now what happens.


---

## 3 · DELETION (a) — `exchange/.DS_Store` untracked, F-1 CLOSED

An index-only removal. **The file on disk was not touched**, which is the whole point of
`--cached` and is asserted rather than claimed:

```
=== BEFORE ===
tracked : exchange/.DS_Store
on disk : 8196 B
sha256  : 42630efe4c77beb43e9740abb5623d887728bbd8a28f020e49f5e52001275a6f

=== ACT ===
$ git rm --cached exchange/.DS_Store
rm 'exchange/.DS_Store'

=== AFTER ===
tracked : error: pathspec 'exchange/.DS_Store' did not match any file(s) known to git
on disk : 8196 B
sha256  : 42630efe4c77beb43e9740abb5623d887728bbd8a28f020e49f5e52001275a6f
FILE UNTOUCHED — sha256 identical before and after
```

**The ignore already covered it repo-wide — no new line was added, and adding one would have been
redundant.** `.gitignore:209` is a bare `.DS_Store`, and a gitignore pattern containing no slash
matches at every depth. Asserted at five depths rather than assumed:

```
  .DS_Store                      IGNORED
  exchange/.DS_Store             IGNORED
  exchange/queue/.DS_Store       IGNORED
  docs/.DS_Store                 IGNORED
  a/b/c/.DS_Store                IGNORED
```

**Why it was tracked at all, since the ignore was always there:** ignore rules never reach a file
that is already in the index. It was committed before the rule existed, and every `.gitignore` pass
since then looked correct while doing nothing about it.

```
=== any tracked .DS_Store left anywhere? ===
NONE — clean repo-wide
```

**Box effect: −8,196 B off the tick set**, and one binary blob off a bus that §4.2 says is text only.
**14** `.DS_Store` files remain on disk across the tree (excluding the ephemeral agent worktrees
under `.claude/`); every one is untracked and ignored, and **none of them is a repository object any
more**.

---

## 4 · DELETION (b) — REFUSED BY ITS OWN GATE

### 4.1 The verdict: KEEP

`exchange/reports/NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS copy.txt` — **4 of 4 checks
failed. Nothing was deleted.**

```
GATE — the four checks of the 2026-08-12 TIDY precedent
  target : exchange/reports/NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS copy.txt
  bytes  : 6371
  sha256 : 7c2e69c0aa615a2f637c1f5caceccd26cac5c407594d5eb6227a65334fcf52a8
  blob   : a496e233c2b1a1e5271ebcaab2b9705da13cde4d

STEP 0 — ENUMERATE THE TWIN SET. 'There is no twin' is a NEGATIVE, and a
         negative from one lookup measures the lookup (invariant 6).

  (a) same stem anywhere on disk           : 1
        ./exchange/reports/NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS copy.txt
  (b) TRACKED paths carrying that blob     : 1   [NUL-safe parse]
        'exchange/reports/NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS copy.txt'
  (c) same stem in git history (all refs)  : 1
        exchange/reports/NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS copy.txt
  (d) tracked 'MAC*ERA' paths              : 1
        exchange/reports/NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS copy.txt

  TWIN SET = 0   -- EMPTY --

STEP 1 — THE FOUR CHECKS
  1. sha256 equal to a twin           **FAIL**
       NO TWIN EXISTS — this check has nothing to evaluate. It is not that the
       hashes differ; it is that there is exactly one file.
  2. twin tracked                     **FAIL**   no twin to be tracked
  3. twin's blob on origin            **FAIL**   no twin to be on origin
  4. worktree == that blob            **FAIL**   no twin, so no blob to compare

VERDICT: **KEEP AND REPORT** — 4 of 4 checks failed. Nothing was deleted.
```

**The brief calls this file a "stray beside its NOTE twin". That premise is false.** Enumerated four
ways — by stem on disk, by identical git blob across the whole index, by stem across git history on
all refs, and by a raw grep of every tracked path — **there is no twin**. This is the only edition of
the 2026-08-15 ATHENA all-lanes status note that exists anywhere. The `" copy"` in the name is a
Finder artifact from how it was ferried in, not evidence that a second copy exists.

It is also **live**: the newest ATHENA→ALL-LANES broadcast, which makes it KEEP-HOT under the
retention law and — as of §2 today — one of the ten notes the repaired rotation exemption protects
by name. Deleting it would have destroyed the sole copy of a live document.

### 4.2 A bug in my first version of this gate, which would have authorised exactly that

Reported because a deletion gate that mis-parses a filename is worse than no gate at all.

My first draft enumerated blob-identical tracked paths with:

```
git ls-files -s | awk '$2=="<blob>"{print $4}'
```

`git ls-files -s` prints `<mode> <blob> <stage>\t<path>`, and **the target's own filename contains a
space**. `awk` splits on whitespace, so it truncated
`…MAC-ERA-STATUS copy.txt` to `…MAC-ERA-STATUS` and reported that truncation as a **TWIN**. All four
checks then passed:

```
  TWIN SET = 1
  1. sha256 equal to a twin?            PASS
  2. twin tracked?                      PASS
  3. twin's blob on origin?             PASS
  4. worktree == that blob?             PASS
VERDICT: all four checks PASS -> DELETE authorised.
```

**The phantom does not exist:**

```
$ git ls-files --error-unmatch "exchange/reports/NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS"
error: pathspec '...MAC-ERA-STATUS' did not match any file(s) known to git
```

Re-run with a NUL-safe parse (`git ls-files -s -z`, split on `\0`, split path on the tab), the twin
set is empty and all four checks fail.

**What caught it was not the gate.** It was reading the gate's own output against the enumeration
printed three lines above it: check (a) found one file, check (b) claimed a different path with the
same content, and two files cannot occupy one enumeration. **The lesson is specific and worth keeping: a
filename containing a space defeats every whitespace-splitting shell idiom.** Measured:
`git ls-files | grep ' '` returns **12 tracked paths with spaces in them** — two `docs/history`
status files, the `ORCHESTRATOR CONTROL CENTER` file this lane moved on 2026-08-18, four primers and
knowledge notes, two rendered HTML reports, one `research_outputs` handoff — **and exactly one on
the bus: this file.** Every enumeration in the final gate is NUL-safe or raw-grep; none splits on
whitespace.

### 4.3 The VIZ-4 pair — REPORT ONLY, APOLLO's call

```
DESIGN_CONTRACT_VIZ4_EMA_MANTLE_2026-08-15.md      3857 B
    sha256 8e8b3264805c9dee92d4bd9ad79ba62e56f1f404175d9a60d82ae9d1b1cdec7c
    blob   e65eff1eba776726537b5456628556f5df395c94   tracked=yes   on origin=yes
DESIGN_CONTRACT_VIZ4_EMA_MANTLE_2026-08-15_1.md    3857 B
    sha256 8e8b3264805c9dee92d4bd9ad79ba62e56f1f404175d9a60d82ae9d1b1cdec7c
    blob   e65eff1eba776726537b5456628556f5df395c94   tracked=yes   on origin=yes
```

**Identical to the byte and to the git blob.** Unlike §4.2, this pair *would* pass all four checks —
sha equal, twin tracked, blob on origin, worktree == blob — so a deletion here would be safe. **It
was not made: the brief reserves this call for APOLLO, and it is a retention decision about a design
contract, not a hygiene sweep.** One word and the `_1` twin rotates or is deleted; 3,857 B, 0.024%
of the box, no urgency.

### 4.4 F-4 rides with it — the ruling whose premise failed seven minutes later

```
2026-08-15 22:40:26  exchange/reports/RULES_OF_RECORD_VIZ_IRON_2026-08-15.md
2026-08-15 22:47:32  exchange/reports/DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md
```

**7 minutes 6 seconds.** `RULES_OF_RECORD_VIZ_IRON` records operator ruling F-1 declaring the VIZ-3
design contract *"sought and **ABSENT** for a third cycle — not attached, not in
`exchange/reports/`, nowhere in the tree"*, and on that basis promotes VIZ-4's inline restatement,
closes V-10, and strikes the re-attach item. The contract it declared absent is on the bus, written
seven minutes later.

Both files are KEEP-HOT and both are published, so a reader still meets the ruling and its own
refutation side by side. The iron rules are identical in substance either way, so **nothing
operational turns on it** — but §0's correction rule says a superseded assertion is rewritten, not
left standing. **APOLLO's and the operator's to reconcile; unchanged here for the second session
running.**

---

## 5 · STAMPS — F-3 CLOSED

Both written into the work orders where they now live, in the README's documented stamp grammar so
the parser that feeds `MANIFEST.json` can read them.

**`docs/history/queue/001_condensed-project-history.md`:**

> `WITHDRAWN: 2026-08-22 (operator via ATHENA) — revivable by re-filing; the drafting is`
> `preserved and was judged the best in the queue.`

**`docs/history/queue/004_move-clone-out-of-onedrive.md`:**

> `BUILT: 2026-08-22 (retroactive) — Phase A executed 2026-08-12; Phase B superseded by`
> `Queue 005 and the pending PC-decommission phase.`

Each carries a short context paragraph beneath it so the stamp is not misread — that WITHDRAWN is
not REJECTED and the text revives by re-filing, and that "retroactive" dates the *stamp*, not the
work, whose own date is in the contract above it.

> **One deviation, one character.** The brief's text reads `BUILT 2026-08-22` and
> `WITHDRAWN 2026-08-22`, without a colon. Written that way, `reviewer_manifest._is_stamped()`
> **does not see them** — the queue README defines the form as `BUILT: <artifact or commit>`, and the
> parser requires it. Verified by writing them verbatim first and watching the machine read
> `BUILT=False`. A colon was added to each so the stamps parse; the operator's words are otherwise
> untouched.

**Machine re-read, by the same parser `MANIFEST.json` uses:**

```
001_condensed-project-history.md    RATIFIED=True  BUILT=False WITHDRAWN=True
004_move-clone-out-of-onedrive.md   RATIFIED=True  BUILT=True  WITHDRAWN=False
```

### 5.1 The backlog counters, re-printed truthful

```
{'queue_total': 3, 'queue_unratified': 0, 'queue_ratified_unbuilt': 3, 'queue_open': 3}
   003_report-rotation-and-provenance.md                  ratified=True built=False
   008_sail-skeleton.md                                   ratified=True built=False
   2026-08-16_BR2_oracle_calibration_parity_R2_ARGUS.md   ratified=True built=False
```

**The numbers are unchanged from yesterday — and now they are TRUE, which they were not before.**
`queue_ratified_unbuilt = 3` reads the same as it did last night, but last night two of the five it
had dropped were unfinished work orders whose relocation nobody had recorded. The stamps do not move
the counter; **they make the counter's silence honest**, because 001 and 004 are now stamped in the
files themselves rather than being merely absent from a directory the parser scans.

**Note for whoever reads the counter next:** `reviewer_manifest.queue_items()` scans
`exchange/queue/` only, so a stamp in `docs/history/queue/` never affects it. That is correct — a
rotated work order is not backlog — but it means **the stamps' audience is a human reading the
contract, not the counter.** Their value is that the contract now states its own disposition instead
of leaving it to be reconstructed from a report.

---

## 6 · PROOF

| check | result |
|---|---|
| **suite** | **334 passed, 1 skipped, 0 failed**, 14.62 s — `testpaths = fixtures tests` |
| **F-CONV** | **4/4 PASS** |
| **F-ROT** *(new this session)* | **7/7 PASS** — `scripts/rotation_exemption_fixtures.py` |
| **F-MB-1** | **8/8 PASS** |
| `rotate_reports.py --dry-run` | **exit 0**, 0 candidates / 10 exempt / 52 too young — it was exit 2 this morning |
| **MAILBOX** | `43 link(s) -- 0 created, 0 pruned, 43 unchanged` |

**The mailbox no-op is honest, not a stall.** Nothing this session touched is in either mailbox set:
the four zips are not a rolling surface, `.DS_Store` was never linked, and
`exchange/queue/003_…md` — which *was* edited — is **pinned**, so it was already linked and stays
linked. A delta would have meant something unexpected moved. The one pinned entry not on disk is
still `*QUEUE-008-BUILD*.md`, which is correct: 008 is ratified and unbuilt.

**One stale test docstring was corrected in the same act.** `tests/test_bus_health.py` asserted its
block renders *"even though rotate_reports currently HALTS"*. It does not halt any more. The
assertion is unchanged and still right; the sentence describing why is now true.

---

## 7 · FILE DISPOSITION

Constants read from `publish_exchange`, never copied: `BOX_BYTES = 16,000,000`,
`FLAG_BYTES = 64,000`. **BOX COST is `n/a` outside `exchange/`** — `docs/`, `scripts/` and
`research_outputs/` are in the repo but not in the tick set.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/queue/003_report-rotation-and-provenance.md` | yes | tracked | this publish | yes | GitHub + `--workflow` | 5,374 → **8,280 B**, 0.052% |
| `exchange/status/ROTATION_LOG.md` | yes | tracked | this publish | yes | GitHub + `--workflow` | 23,015 → **24,486 B**, 0.153% |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | this publish | yes | GitHub + `--workflow` | +this session's entry — **over the 64,000 B wire (append-only)** |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-22_ROOT-ADJUDICATION.md` *(this document)* | yes | tracked (new) | this publish | yes | GitHub + `--workflow` | see the FLAG below |
| `exchange/.DS_Store` | **yes, on disk, untouched** | **UNTRACKED as of this commit** — `.gitignore:209` | removed from the index in `<this session's commit>` | yes | **NOT PROTECTED — and correctly so; it is Finder metadata** | **−8,196 B, removed from the box** |
| `scripts/rotate_reports.py` | yes | tracked | this session's commit | yes | GitHub + `--workflow` | n/a — outside `exchange/` |
| `scripts/rotation_exemption_fixtures.py` | yes | tracked (new) | this session's commit | yes | GitHub + `--workflow` | n/a — outside `exchange/` |
| `tests/test_bus_health.py` | yes | tracked | this session's commit | yes | GitHub only — `tests/` is **not** in `WORKFLOW_SOURCES` | n/a — outside `exchange/` |
| `docs/history/queue/001_condensed-project-history.md` | yes | tracked | this session's commit | yes | GitHub + `--workflow` (`docs/history`) | n/a — off the bus since 2026-08-18 |
| `docs/history/queue/004_move-clone-out-of-onedrive.md` | yes | tracked | this session's commit | yes | GitHub + `--workflow` (`docs/history`) | n/a — off the bus since 2026-08-18 |
| **4 packet zips** → `research_outputs/packets/` | yes, at the new paths | **untracked, `.gitignore:48 *.zip`** | never — git has never held them | never | **NOT PROTECTED, before or after** — measured, §1.2 | n/a — never were in the box |
| `~/Naiad/.DS_Store` | yes | untracked, ignored | — | — | operator's machine | n/a — note only |

> ### ⚑ §3.2 TRIP-WIRE — read against the tick set after this session
>
> This document is under the 64,000 B naming wire; its intended home is `exchange/reports/`, on the
> bus. The live figure is printed by the publish, below — a file never contains its own measurement
> of itself. **`exchange/.DS_Store` leaving the index takes 8,196 B off the box; nothing this
> session added crosses the wire on its own.**

---

## 8 · WHAT REMAINS OPEN

| # | item | owner | state |
|--:|---|---|---|
| 1 | ~~rotation halts~~ | — | **CLOSED** this session (§2). Exit 0, F-ROT 7/7. |
| 2 | ~~001 / 004 unstamped~~ | — | **CLOSED** this session (§5). |
| 3 | ~~`exchange/.DS_Store` tracked~~ | — | **CLOSED** this session (§3). |
| 4 | `" copy.txt"` — no twin, sole copy of a live note | **operator** | **KEEP**, gate refused (§4.1). If the intent was to normalise the *name*, that is a rename, not a deletion, and it would break the citation in `LEDGER_ATHENA` — so it wants a decision, not a tidy. |
| 5 | VIZ-4 byte-identical twin | **APOLLO** | Report only (§4.3). Would pass all four checks; one word removes it. |
| 6 | Ruling F-1's premise vs the VIZ-3 contract on the bus | **APOLLO / operator** | Unchanged, second session running (§4.4). |
| 7 | `v12_v3_anchor_packet_20260713.zip` still written to the root by `v3_scorer.py:393` | **operator** | Kept by its citation (§1.2). One word + a one-line repoint moves it to the packets home. |
| 8 | The four packet zips are **unprotected**, at the root or in `research_outputs/packets/` | **operator / ATHENA** | Not a regression — they never were protected. If they should be, `research_outputs/packets/` needs adding to `backup_estate.WORKFLOW_SOURCES`, which is a measured widening, not a one-liner. |
| 9 | QUEUE-008 (SAIL): all eight PENDING items, D-0 first | **operator** | Carried, untouched. The only ratified unbuilt work with nothing blocking it but an answer. |

## 9 · THE HONEST NEXT OPTIONS

1. **Build queue 008 (SAIL)** once D-0 closes. It is the only ratified, unbuilt, unblocked work order
   left. *For:* it is the actual work; the last two sessions have both been housekeeping. *Against:*
   D-0 needs the operator's answer first, and eight PENDING items sit behind it.
2. **Clear the four small VIZ/packet decisions** (items 5, 6, 7) in one pass — they are four words
   from the operator and they close the last of the 2026-08-18 findings. *For:* cheap, and item 6 is
   a live contradiction on a published bus. *Against:* none of them is costing anything today.
3. **Decide whether the packet zips deserve backup coverage** (item 8). *For:* "existence is not
   protection" is invariant 2, and five transport bundles sitting unprotected is exactly the shape
   it warns about. *Against:* they are transport bundles whose source of record is tracked — the
   honest answer may be that they are disposable, in which case say so and stop carrying them.

---

## 10 · SESSION CLOSE

```
=== STATUS_HEPHAESTUS — 2026-08-22 (second session) ===
NOW: The root is adjudicated in the open — 86 KEEP with a file:line citation each, 4 packet zips
moved, 1 note-only. Queue 003's rotation is REPAIRED and runs again (exit 0, was exit 2 for seven
days). exchange/.DS_Store is out of the index with the file untouched on disk. Two stamps written.
One authorised deletion was REFUSED by its own gate: the " copy.txt" has no twin.
LAST EVENT: 2026-08-22 — one commit (rotation repair, fixtures, stamps, the .DS_Store untrack) and
one publish carrying the amended contract, ROTATION_LOG's 4 new rows and this report.
FACTS:
- ROOT: 86 KEEP / 4 MOVED / 1 note-only. 36 of the keeps are documents a live code reference pins;
  22 are data files read by name; 6 are kept by rule; 22 are directories. NOTHING ELSE WAS
  MOVABLE — the 08-18 sweep already took what was merely sitting there [verified]
- ROTATION REPAIRED: --dry-run exit 0, 0 candidates / 10 exempt / 52 too young. The exemption is
  now computed from the bus (newest note per lane pair) and has NO EXTERNAL INPUT, so it cannot
  reach the unavailable state that broke it. AGE_DAYS = 30 untouched. F-ROT 7/7 [verified]
- TWO WIDENINGS NAMED: NOTE_RE went ^NOTE_.+_to_.+ -> ^NOTE_, because broadcasts NEVER matched the
  old pattern and were never exemptible at all — a live hole in the ratified rule, not one this
  correction made. And D-2's stale "HERMES's DIGEST box-budget section" now names the bus-health
  block [verified]
- THE BRIEF'S "SIX UNACTED NOTES" DOES NOT REPRODUCE. Measured at 98951cd^: 14 notes on the bus,
  13 dated on/before 2026-08-15, 9 matched by the old pattern, 4 broadcasts it could never match,
  10 live today. No reading yields six. It was a number hardcoded in an error message with no
  derivation and nothing that could check it; it is gone with the function that carried it, and the
  fixture is now stated as a RULE rather than a count so it cannot go stale the same way [verified]
- A DELETION GATE OF MY OWN NEARLY AUTHORISED THE WRONG DELETE. My first draft enumerated twins
  with `git ls-files -s | awk '{print $4}'`; the target's filename CONTAINS A SPACE, awk truncated
  it, and the truncation was reported as a twin — all four checks PASSED. Re-run NUL-safe: twin set
  EMPTY, 4/4 checks FAIL, KEEP. The file is the only edition of the newest ATHENA->ALL-LANES
  broadcast and is one of the ten notes the repaired exemption now protects. 12 tracked paths in
  this repo contain spaces; one is on the bus [verified]
- exchange/.DS_Store untracked, file byte-identical on disk before and after (sha 42630efe…);
  .gitignore:209's bare pattern already covered it at every depth, asserted at five; no tracked
  .DS_Store remains anywhere; -8,196 B off the box [verified]
- STAMPS written in the README's grammar after the operator's colon-less form was verified NOT to
  parse (BUILT=False). Counters unchanged at 3/0/3 — and now TRUE rather than silently right
  [verified]
- suite 334 passed / 1 skipped · F-CONV 4/4 · F-ROT 7/7 · F-MB-1 8/8 · MAILBOX no-op 43/43
  [verified]
PENDING (operator):
1. QUEUE-008 D-0 — the only unblocked ratified work; everything else here is closed or is a word
2. The " copy.txt": KEEP stands. A rename is possible but breaks a LEDGER_ATHENA citation
3. VIZ-4 twin (APOLLO) — would pass all four checks; one word removes it
4. Ruling F-1 vs the VIZ-3 contract on the bus (APOLLO) — unchanged, second session running
5. v12_v3_anchor_packet: v3_scorer.py:393 still writes it to the root; one-line repoint on your word
6. Should the packet zips be backed up at all? They are unprotected and always were
NEXT: build queue 008 (SAIL) on the D-0 answer. Owner: HEPHAESTUS.
METRICS: operator actions this session = 0 · files re-ingested = 0 · files moved = 4 · files
deleted = 0 · index removals = 1 · deletions refused by gate = 1 · defects found in own work = 2
(the awk twin, the relative_to crash), both fixed
=== END STATUS ===
```

**BRIGHT COLOURS — what is still at the root, as a closed list.**

Nothing at `~/Naiad` needs the operator's attention. The **61 files** there are, exhaustively —
**6 + 36 + 18 + 1**, and the four numbers add up:

- **6 kept by rule** — `LEDGER.md` · `README.md` · `.gitignore` · `.gitattributes` · `pytest.ini` ·
  `requirements.txt`
- **36 study documents** — every one read by name from `scripts/`, `fixtures/`, `tests/` or
  `engine/`; moving any of them breaks a script
- **18 data and artifact files** — 16 results JSONs / substrates / one CSV, one `.pine` source, and
  `v12_v3_anchor_packet_20260713.zip`; every one pinned by a code reference
- **1 OS file** — `.DS_Store`, untracked, ignored, the operator's machine's own

Plus **26 directories**, which a file sweep does not touch. **There is no residue: not one root
file came back unreferenced.**

**And one folder to keep using: `~/Naiad/MAILBOX`** — 43 links, still current, still refreshing
itself on every publish and every daily routine.

