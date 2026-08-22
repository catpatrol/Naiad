# HEPHAESTUS — file disposition inventory

**Filed:** 2026-08-02 — **the machine clock is correct**, per operator ruling. This report's filename
uses the true date.

**Lane:** HEPHAESTUS (local Windows Claude Code, working Naiad clone).
**Nature:** inventory only. No commits, no pushes, no deletions. The one write is this file.

---

## STEP 0 — ASSERT

| check | result |
|---|---|
| OS is Windows | PASS — `Windows_NT` |
| pwd is repo root | PASS — `…\Midas-Claude Code Resources\naiad`, `LEDGER.md` present |
| branch | PASS — `v12-v1-census` |
| **HEAD** | **`79280f7`** |
| porcelain before | **0** — clean and synced with `origin/v12-v1-census` |

### Correction on record: the two prior reports are misdated

Two committed reports carry `2026-08-03` in their filenames against a machine clock of `2026-08-02`:
`exchange/reports/2026-08-03_HEPHAESTUS_report_ai-operating-system.md` and
`…_tc5-archive-and-scaffolding.md`, plus `…_exchange-slimming.md`. Each flagged the offset in its own
text, but the filenames are now committed and pushed under the wrong date. Renaming needs a commit,
which this paste forbids — carried as a cleanup item.

---

## STANDING RULE ADOPTED

> **Every report from now on ends with a FILE DISPOSITION TABLE** covering every file created,
> modified or moved, with six columns: full repo-relative path · exists on disk ·
> tracked/untracked/ignored (naming the `.gitignore` line if ignored) · committed in which short SHA
> (or "not committed") · pushed yes/no plus remote ref · protected by which backup.

Effective immediately, including this report — see the closing section.

---

## 1 · RULING RECORDED — `.gitignore` for `research_outputs/_daily_archive/`

**APPROVED**, on the precedent of `research_outputs/brief/`. No action needed; the line stands as
written at `.gitignore:91`, with its reasoning in place four lines below the precedent it cites.

For the record, the rule as it stands:

```
# Daily routine reports aged out of the exchange rolling window (2026-08-03).
# Same class as the brief archive above and ignored for the same reason: these
# are ops artifacts moved OUT of exchange/ precisely because they no longer need
# to be published or box-synced. They stay on disk and in the weekly workflow
# backup; keeping them tracked would defeat the move.
research_outputs/_daily_archive/
```

One correction to that comment's own text: it is dated `2026-08-03` and should read `2026-08-02`.
Cosmetic, inside a comment, and it needs a commit to fix — carried as a cleanup item.

---

## 2 · COMMITTER IDENTITY — **I got this wrong last cycle, and here is the correction**

### The configuration

| scope | `user.name` | `user.email` |
|---|---|---|
| **local** (`.git/config:14-16`) | **`t`** | **`t@t`** |
| global | (unset) | (unset) |
| system | (unset) | (unset) |
| **effective** | **`t`** | **`t@t`** |

### Author counts — `git log --format='%an <%ae>' -20 | sort | uniq -c`

```
    12 t <t@t>
     8 catpatrol <catpatrolling@gmail.com>
```

### All 12 commits carrying `t <t@t>`

```
79280f7  2026-08-02 16:21  exchange: file the exchange-slimming report
bb7a076  2026-08-02 16:19  exchange: auto-publish 2026-08-02
23fbd9e  2026-08-02 16:15  ops: slim exchange — brief artifacts referenced not copied, 7-day rolling window
b06348c  2026-08-02 15:44  exchange: file the tc5 archive and scaffolding report
ec1317e  2026-08-02 15:43  ops: tc5 archived; AI operating-system scaffolding
6bac35d  2026-08-02 15:42  exchange: auto-publish 2026-08-02
71b6700  2026-08-02 15:29  exchange: file the AI operating-system scaffolding report
1563bff  2026-08-02 15:28  ops: AI operating-system scaffolding — preferences, memory convention
ae7948f  2026-08-02 15:27  exchange: auto-publish 2026-08-02
014434f  2026-08-02 14:31  exchange: file the HEPHAESTUS delta build report
5de3fac  2026-08-02 14:29  fix: guard every filesystem call in the sweep
9470d04  2026-08-02 13:57  base
```

### The correction

**Last cycle I reported `t <t@t>` as evidence of "another actor" writing to this branch with "an
unconfigured git identity". That inference was wrong and I am withdrawing it.**

`t <t@t>` is **this repository's own local git config**. Every commit made from this clone adopts it.
The author timeline shows the switch precisely:

- every commit up to and including `dd926bc` (13:53) → `catpatrol <catpatrolling@gmail.com>`
- `9470d04` "base" (13:57) → the **first** `t <t@t>` commit
- every commit after it → `t <t@t>`, **including all eleven of mine**

So whatever produced `9470d04` at 13:57 **also wrote `[user] name = t / email = t@t` into
`.git/config`**, and every commit I have made since silently inherited it. The identity is not a
fingerprint of a third party; it is a local setting that changed mid-session.

**What remains genuinely unexplained is narrower, and still worth your attention:** `9470d04 base` is
a commit I did not author. It committed the six paths I had deliberately left untracked for your
decision (`ARGUS_REPRIME_2026-08-02.md`, `ORCHESTRATOR CONTROL CENTER — protocol & state of
record.txt`, `SCHED_TEST_RESULT_2026-08-02.md`, `analytics/`, `scripts/orchestrator_state.py`,
`tests/test_analytics.py`), and it changed the repo's commit identity for everything that followed.

**Practical consequence:** eleven commits of legitimate work are attributed to `t <t@t>` rather than
to you. History was **not** rewritten, per instruction. Fixing it going forward is one command —
`git config --local user.name "catpatrol"` and the matching email — which this paste does not run.

---

## 3 · FULL DISPOSITION INVENTORY

**Scope:** every file under `exchange/`, `scripts/`, `docs/`, `claude/`, `prompts/`, plus repo-root
`*.md`. `__pycache__` excluded. **169 files.**

### How "protected by" was resolved — by content, not by path

The newest workflow archive is **`naiad_workflow_2026-08-02.zip`**, sha256
**`f981cc3e17fe15afad08756426b38e09759aee7ba05ebd6df101cce2011cf112`**, 67 members.

Membership was resolved by comparing each file's **sha256 against the archive's embedded manifest**,
not by matching path prefixes. That distinction changed four rows: a file whose path is in the archive
but whose bytes have since changed is **not** protected in its current form — the archive holds a
different file. Reporting those as protected would be precisely the false comfort this inventory
exists to prevent. They appear as **`GitHub only (workflow copy is STALE)`** and are sorted directly
after the NOT PROTECTED block.

No file in scope is git-ignored, so the ".gitignore line" clause of the column has no rows to fill.

### Rows — NOT PROTECTED first, then stale-archive, then GitHub only, then fully protected

| # | path | on disk | git status | committed | pushed | protected by |
|---:|---|---|---|---|---|---|
| 1 | `exchange/status/MANIFEST.json` | yes | tracked | bb7a076 | yes (origin/v12-v1-census) | ⚠ GitHub only (workflow copy is STALE) |
| 2 | `exchange/status/RETENTION.md` | yes | tracked | 6bac35d | yes (origin/v12-v1-census) | ⚠ GitHub only (workflow copy is STALE) |
| 3 | `exchange/status/daily/DAILY_2026-08-02.md` | yes | tracked | 79280f7 | yes (origin/v12-v1-census) | ⚠ GitHub only (workflow copy is STALE) |
| 4 | `exchange/status/daily/MANIFEST_2026-08-02.json` | yes | tracked | bb7a076 | yes (origin/v12-v1-census) | ⚠ GitHub only (workflow copy is STALE) |
| 5 | `ARGUS_REPRIME_2026-08-02.md` | yes | tracked | 9470d04 | yes (origin/v12-v1-census) | GitHub only |
| 6 | `CENSUS.md` | yes | tracked | eb671df | yes (origin/v12-v1-census) | GitHub only |
| 7 | `CENSUS_1b.md` | yes | tracked | d77c2d6 | yes (origin/v12-v1-census) | GitHub only |
| 8 | `CENSUS_1b_Rescore_and_Anatomy_Builder_Contract.md` | yes | tracked | a70a49c | yes (origin/v12-v1-census) | GitHub only |
| 9 | `CENSUS_DEFINITIONS.md` | yes | tracked | 495abc8 | yes (origin/v12-v1-census) | GitHub only |
| 10 | `CHANGELOG.md` | yes | tracked | 9f82db8 | yes (origin/v12-v1-census) | GitHub only |
| 11 | `Census_1_Amendment_1.md` | yes | tracked | 495abc8 | yes (origin/v12-v1-census) | GitHub only |
| 12 | `Census_1_MTF_Signal_Stack_Builder_Contract.md` | yes | tracked | 495abc8 | yes (origin/v12-v1-census) | GitHub only |
| 13 | `DATA_CENSUS.md` | yes | tracked | 53b8199 | yes (origin/v12-v1-census) | GitHub only |
| 14 | `GAP_REPORT.md` | yes | tracked | 53b8199 | yes (origin/v12-v1-census) | GitHub only |
| 15 | `HANDOFF_2026-07-22_Census_to_Census1b.md` | yes | tracked | fc8ad9c | yes (origin/v12-v1-census) | GitHub only |
| 16 | `LEDGER.md` | yes | tracked | f1dc026 | yes (origin/v12-v1-census) | GitHub only |
| 17 | `Naiad_Phase0_Charter.md` | yes | tracked | a6da1b9 | yes (origin/v12-v1-census) | GitHub only |
| 18 | `Naiad_Phase1_Build_Prompt.md` | yes | tracked | a6da1b9 | yes (origin/v12-v1-census) | GitHub only |
| 19 | `Prometheus_Data_Collection_Design.md` | yes | tracked | fc08d93 | yes (origin/v12-v1-census) | GitHub only |
| 20 | `Prometheus_Paper_Analysis_Week1.md` | yes | tracked | fc08d93 | yes (origin/v12-v1-census) | GitHub only |
| 21 | `Prometheus_Stop_Loss_Logic_Learnings.md` | yes | tracked | a6da1b9 | yes (origin/v12-v1-census) | GitHub only |
| 22 | `RC7_Amendment_1.md` | yes | tracked | 393a79a | yes (origin/v12-v1-census) | GitHub only |
| 23 | `RC7_Amendment_2.md` | yes | tracked | 393a79a | yes (origin/v12-v1-census) | GitHub only |
| 24 | `RC7_PostS1_Recompute_Builder_Contract.md` | yes | tracked | 393a79a | yes (origin/v12-v1-census) | GitHub only |
| 25 | `RC7_RESULTS.md` | yes | tracked | 548e265 | yes (origin/v12-v1-census) | GitHub only |
| 26 | `RC_RECOMPUTE_RC0_RC6.md` | yes | tracked | 0cc3e0f | yes (origin/v12-v1-census) | GitHub only |
| 27 | `RC_Recompute_RC0_RC6_Builder_Contract.md` | yes | tracked | e6c3042 | yes (origin/v12-v1-census) | GitHub only |
| 28 | `README.md` | yes | tracked | f1df573 | yes (origin/v12-v1-census) | GitHub only |
| 29 | `REVIEWER_HANDOFF_2026-07-12.md` | yes | tracked | 7f1b4a9 | yes (origin/v12-v1-census) | GitHub only |
| 30 | `REVIEWER_HANDOFF_2026-07-13_V3_FORENSICS.md` | yes | tracked | fc08d93 | yes (origin/v12-v1-census) | GitHub only |
| 31 | `REVIEWER_HANDOFF_2026-07-15_V3_RECOMPUTE.md` | yes | tracked | e768c7d | yes (origin/v12-v1-census) | GitHub only |
| 32 | `REVIEWER_HANDOFF_2026-07-25_ENGINE_INGESTION.md` | yes | tracked | 95c4b82 | yes (origin/v12-v1-census) | GitHub only |
| 33 | `S1_Findings_Report_3_Winners_Losers_MTF_Map.md` | yes | tracked | fc08d93 | yes (origin/v12-v1-census) | GitHub only |
| 34 | `S1_Instrumented_Replay_Builder_Contract.md` | yes | tracked | e459bca | yes (origin/v12-v1-census) | GitHub only |
| 35 | `S1_MEASUREMENT.md` | yes | tracked | 7c546c5 | yes (origin/v12-v1-census) | GitHub only |
| 36 | `S2B_DECOMPOSITION.md` | yes | tracked | 5de40af | yes (origin/v12-v1-census) | GitHub only |
| 37 | `S2_Instrumented_Pass_Builder_Contract.md` | yes | tracked | 6af174b | yes (origin/v12-v1-census) | GitHub only |
| 38 | `S2_MEASUREMENT.md` | yes | tracked | 6fdab03 | yes (origin/v12-v1-census) | GitHub only |
| 39 | `S2b_Decomposition_Addendum_Builder_Contract.md` | yes | tracked | 5dd5c13 | yes (origin/v12-v1-census) | GitHub only |
| 40 | `S3_ENRICHMENT.md` | yes | tracked | f656dbd | yes (origin/v12-v1-census) | GitHub only |
| 41 | `S3_Enrichment_Builder_Contract.md` | yes | tracked | 91c389b | yes (origin/v12-v1-census) | GitHub only |
| 42 | `SCHED_TEST_RESULT_2026-08-02.md` | yes | tracked | 9470d04 | yes (origin/v12-v1-census) | GitHub only |
| 43 | `SPOT_CHECK.md` | yes | tracked | 36f4c5c | yes (origin/v12-v1-census) | GitHub only |
| 44 | `SSv11_3_Execution_Playbook_and_Field_Manual.md` | yes | tracked | 7f1b4a9 | yes (origin/v12-v1-census) | GitHub only |
| 45 | `SSv11_Field_Manual.md` | yes | tracked | a6da1b9 | yes (origin/v12-v1-census) | GitHub only |
| 46 | `SSv12_SPEC_ERRATA.md` | yes | tracked | 1d3e498 | yes (origin/v12-v1-census) | GitHub only |
| 47 | `State_of_Project_2026-07-22_Census_Findings_and_Implications.md` | yes | tracked | fc8ad9c | yes (origin/v12-v1-census) | GitHub only |
| 48 | `TC1_DEFINITIONS.md` | yes | tracked | c9d9821 | yes (origin/v12-v1-census) | GitHub only |
| 49 | `TC1_Design_Brief_Lifecycle_AsIs_vs_Proposed.md` | yes | tracked | fc08d93 | yes (origin/v12-v1-census) | GitHub only |
| 50 | `TC1_Factorial_Builder_Contract.md` | yes | tracked | c9d9821 | yes (origin/v12-v1-census) | GitHub only |
| 51 | `TC1_RESULTS.md` | yes | tracked | 57cf217 | yes (origin/v12-v1-census) | GitHub only |
| 52 | `TC4_BASELINE.md` | yes | tracked | c2835b3 | yes (origin/v12-v1-census) | GitHub only |
| 53 | `TC4_Engine_1_0_8_Builder_Contract.md` | yes | tracked | 61240bb | yes (origin/v12-v1-census) | GitHub only |
| 54 | `TC5_Amendment_1.md` | yes | tracked | 7d21ad0 | yes (origin/v12-v1-census) | GitHub only |
| 55 | `TC5_Intraday_Respec_Builder_Contract.md` | yes | tracked | 1731793 | yes (origin/v12-v1-census) | GitHub only |
| 56 | `TC5_RESULTS.md` | yes | tracked | b14c3ef | yes (origin/v12-v1-census) | GitHub only |
| 57 | `V12_Study_Charter_Addendum_v1.0.md` | yes | tracked | 070cff4 | yes (origin/v12-v1-census) | GitHub only |
| 58 | `V12_V1_Census_Build_Prompt.md` | yes | tracked | 070cff4 | yes (origin/v12-v1-census) | GitHub only |
| 59 | `V3_Forensics_Report_2_Deep_Dive.md` | yes | tracked | fc08d93 | yes (origin/v12-v1-census) | GitHub only |
| 60 | `V3_RECOMPUTE_R1_R10.md` | yes | tracked | 2bdda8d | yes (origin/v12-v1-census) | GitHub only |
| 61 | `V3_Recompute_R1_R10_Builder_Contract.md` | yes | tracked | e6c3042 | yes (origin/v12-v1-census) | GitHub only |
| 62 | `V3_STOP_AND_EXIT_FORENSICS.md` | yes | tracked | fc08d93 | yes (origin/v12-v1-census) | GitHub only |
| 63 | `docs/ARCHIVE_DEPENDENCIES.md` | yes | tracked | 629930e | yes (origin/v12-v1-census) | GitHub only |
| 64 | `docs/handoffs/HANDOFF_2026-07-27_BRIEF_to_CENSUS_1.md` | yes | tracked | 49e2f87 | yes (origin/v12-v1-census) | GitHub only |
| 65 | `docs/handoffs/HANDOFF_2026-07-27_BRIEF_to_ENGINE.md` | yes | tracked | 49e2f87 | yes (origin/v12-v1-census) | GitHub only |
| 66 | `docs/reports/Cascade Rewire.html` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | GitHub only |
| 67 | `docs/reports/Naiad — Orchestrator Control Center.html` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | GitHub only |
| 68 | `exchange/reports/2026-08-03_HEPHAESTUS_report_exchange-slimming.md` | yes | tracked | 79280f7 | yes (origin/v12-v1-census) | GitHub only |
| 69 | `exchange/reports/2026-08-03_HEPHAESTUS_report_tc5-archive-and-scaffolding.md` | yes | tracked | b06348c | yes (origin/v12-v1-census) | GitHub only |
| 70 | `scripts/archive_dependencies.py` | yes | tracked | 629930e | yes (origin/v12-v1-census) | GitHub only |
| 71 | `scripts/backfill.py` | yes | tracked | 49adda9 | yes (origin/v12-v1-census) | GitHub only |
| 72 | `scripts/backup_estate.py` | yes | tracked | ec1317e | yes (origin/v12-v1-census) | GitHub only |
| 73 | `scripts/brief_lookup.py` | yes | tracked | 76cc314 | yes (origin/v12-v1-census) | GitHub only |
| 74 | `scripts/census.py` | yes | tracked | 53b8199 | yes (origin/v12-v1-census) | GitHub only |
| 75 | `scripts/census1b_analyze.py` | yes | tracked | d77c2d6 | yes (origin/v12-v1-census) | GitHub only |
| 76 | `scripts/census1b_det.py` | yes | tracked | d77c2d6 | yes (origin/v12-v1-census) | GitHub only |
| 77 | `scripts/census1b_report.py` | yes | tracked | d77c2d6 | yes (origin/v12-v1-census) | GitHub only |
| 78 | `scripts/census_analyze.py` | yes | tracked | eb671df | yes (origin/v12-v1-census) | GitHub only |
| 79 | `scripts/census_build.py` | yes | tracked | eb671df | yes (origin/v12-v1-census) | GitHub only |
| 80 | `scripts/daily_brief.py` | yes | tracked | 76cc314 | yes (origin/v12-v1-census) | GitHub only |
| 81 | `scripts/daily_routine.py` | yes | tracked | 23fbd9e | yes (origin/v12-v1-census) | GitHub only |
| 82 | `scripts/dryrun_autopsy.py` | yes | tracked | c2ae143 | yes (origin/v12-v1-census) | GitHub only |
| 83 | `scripts/first_candles.py` | yes | tracked | 49adda9 | yes (origin/v12-v1-census) | GitHub only |
| 84 | `scripts/orchestrator_state.py` | yes | tracked | 9470d04 | yes (origin/v12-v1-census) | GitHub only |
| 85 | `scripts/packet.py` | yes | tracked | c2ae143 | yes (origin/v12-v1-census) | GitHub only |
| 86 | `scripts/parity_pack.py` | yes | tracked | 0c51660 | yes (origin/v12-v1-census) | GitHub only |
| 87 | `scripts/publish_exchange.py` | yes | tracked | 8be8e79 | yes (origin/v12-v1-census) | GitHub only |
| 88 | `scripts/rc7_recompute.py` | yes | tracked | 548e265 | yes (origin/v12-v1-census) | GitHub only |
| 89 | `scripts/rc_recompute.py` | yes | tracked | 0cc3e0f | yes (origin/v12-v1-census) | GitHub only |
| 90 | `scripts/replay.py` | yes | tracked | 49adda9 | yes (origin/v12-v1-census) | GitHub only |
| 91 | `scripts/reviewer_manifest.py` | yes | tracked | 8be8e79 | yes (origin/v12-v1-census) | GitHub only |
| 92 | `scripts/routine_jobs.json` | yes | tracked | 23fbd9e | yes (origin/v12-v1-census) | GitHub only |
| 93 | `scripts/s1_fixtures.py` | yes | tracked | 7c546c5 | yes (origin/v12-v1-census) | GitHub only |
| 94 | `scripts/s1_resample.py` | yes | tracked | e459bca | yes (origin/v12-v1-census) | GitHub only |
| 95 | `scripts/s1_runner.py` | yes | tracked | 7c546c5 | yes (origin/v12-v1-census) | GitHub only |
| 96 | `scripts/s2_fixtures.py` | yes | tracked | 6fdab03 | yes (origin/v12-v1-census) | GitHub only |
| 97 | `scripts/s2_runner.py` | yes | tracked | 6fdab03 | yes (origin/v12-v1-census) | GitHub only |
| 98 | `scripts/s2b_decompose.py` | yes | tracked | 5dd5c13 | yes (origin/v12-v1-census) | GitHub only |
| 99 | `scripts/s3_analyze.py` | yes | tracked | f656dbd | yes (origin/v12-v1-census) | GitHub only |
| 100 | `scripts/s3_enrich.py` | yes | tracked | f656dbd | yes (origin/v12-v1-census) | GitHub only |
| 101 | `scripts/setup_brief_schedule.ps1` | yes | tracked | 97f0eee | yes (origin/v12-v1-census) | GitHub only |
| 102 | `scripts/spot_check.py` | yes | tracked | 36f4c5c | yes (origin/v12-v1-census) | GitHub only |
| 103 | `scripts/tc1_fixtures.py` | yes | tracked | 57cf217 | yes (origin/v12-v1-census) | GitHub only |
| 104 | `scripts/tc1_runner.py` | yes | tracked | 57cf217 | yes (origin/v12-v1-census) | GitHub only |
| 105 | `scripts/tc4_fixtures.py` | yes | tracked | c2835b3 | yes (origin/v12-v1-census) | GitHub only |
| 106 | `scripts/tc4_runner.py` | yes | tracked | c2835b3 | yes (origin/v12-v1-census) | GitHub only |
| 107 | `scripts/tc5_fixtures.py` | yes | tracked | b14c3ef | yes (origin/v12-v1-census) | GitHub only |
| 108 | `scripts/tc5_runner.py` | yes | tracked | b14c3ef | yes (origin/v12-v1-census) | GitHub only |
| 109 | `scripts/tick.py` | yes | tracked | 49adda9 | yes (origin/v12-v1-census) | GitHub only |
| 110 | `scripts/v12_packet.py` | yes | tracked | 53b8199 | yes (origin/v12-v1-census) | GitHub only |
| 111 | `scripts/v3_recompute.py` | yes | tracked | 2bdda8d | yes (origin/v12-v1-census) | GitHub only |
| 112 | `scripts/v3_scorer.py` | yes | tracked | 972bb69 | yes (origin/v12-v1-census) | GitHub only |
| 113 | `claude/STATUS_SYSTEM.md` | yes | tracked | 97f0eee | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 114 | `docs/history/CHALLENGE_DIONYSUS_01_Architecture_2026-08-02.md` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 115 | `docs/history/FUNNEL_DIONYSUS_W1_Workflow_Architecture_2026-08-02.md` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 116 | `docs/history/HANDOFF_DIONYSUS_to_ATHENA_2026-08-02_Workflow_Redesign_Inputs.md` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 117 | `docs/history/Naiad_Orchestration_and_Open_Questions.md` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 118 | `docs/history/PROJECT_STATUS_AND_CONTEXT_2026-07-28.md` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 119 | `docs/history/STATUS — BRIEF (daily market brief · Atlas HTML report · live laboratory).txt` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 120 | `docs/history/STATUS — ENGINE (engine builds · repo operations · integrity & manifest).txt` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 121 | `docs/history/STATUS_HANDOFF_BRIEF_2026-07-28.md` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 122 | `docs/knowledge/Level_Selection_Deep_Dive_Wyckoff_AMT_CCL.md` | yes | tracked | 95c4b82 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 123 | `docs/knowledge/Naiad_Trading_Knowledge_Foundation_v0.md` | yes | tracked | 95c4b82 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 124 | `docs/knowledge/pine/12-25EMA Trend Scanner-Pinescript.txt` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 125 | `docs/knowledge/pine/Rvwap pine code.txt` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 126 | `docs/memory/README.md` | yes | tracked | ec1317e | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 127 | `docs/memory/claude_project_memory_2026-07-26.md` | yes | tracked | 95c4b82 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 128 | `docs/primers/# ORCHESTRATOR PRIMER — what a fresh orchestrator session needs to know.txt` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 129 | `docs/primers/About Apollo, Athena, Argus, Hermes and Dionysus.txt` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 130 | `docs/primers/About Apollo, Athena, Argus, Hermes, Hephaestus and Dionysus.txt` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 131 | `docs/primers/OPERATOR_PREFERENCES.md` | yes | tracked | ec1317e | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 132 | `exchange/DIGEST.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 133 | `exchange/README.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 134 | `exchange/drops/README.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 135 | `exchange/queue/001_condensed-project-history.md` | yes | tracked | 60cf2d1 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 136 | `exchange/queue/README.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 137 | `exchange/reports/2026-08-02_HEPHAESTUS_report_exchange-v1-build.md` | yes | tracked | 014434f | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 138 | `exchange/reports/2026-08-03_HEPHAESTUS_report_ai-operating-system.md` | yes | tracked | 71b6700 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 139 | `exchange/reports/ATHENA_STATUS_2026-08-01.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 140 | `exchange/reports/BACKUP_BUILD_2026-07-28.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 141 | `exchange/reports/CONTRACT_V4_2026-07-28.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 142 | `exchange/reports/FIXUP_2026-07-28.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 143 | `exchange/reports/PUSH_2026-07-28.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 144 | `exchange/reports/README.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 145 | `exchange/reports/SETUP_2026-07-28.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 146 | `exchange/status/2026-08-02_DELTA_W1-rulings-and-exchange.md` | yes | tracked | 60cf2d1 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 147 | `exchange/status/CADENCE.md` | yes | tracked | 60cf2d1 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 148 | `exchange/status/LEDGER_APOLLO.md` | yes | tracked | 60cf2d1 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 149 | `exchange/status/LEDGER_ARGUS.md` | yes | tracked | 60cf2d1 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 150 | `exchange/status/LEDGER_ATHENA.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 151 | `exchange/status/LEDGER_DIONYSUS.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 152 | `exchange/status/LEDGER_HEPHAESTUS.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 153 | `exchange/status/LEDGER_HERMES.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 154 | `exchange/status/README.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 155 | `exchange/status/daily/DAILY_2026-07-28.md` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 156 | `exchange/status/daily/MANIFEST_2026-07-28.json` | yes | tracked | 74caae3 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 157 | `prompts/CONTRACT_ANALYTICS1_BRIEF2_FORWARD0_draft.md` | yes | tracked | 49e2f87 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 158 | `prompts/CONTRACT_ARGUS_Analytics_Scoping_2026-07-29.md` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 159 | `prompts/CONTRACT_DESIGN_Atlas_Rewire_2026-07-30.md` | yes | tracked | 4899975 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 160 | `prompts/CONTRACT_v4_ANALYTICS1_BRIEF2_FORWARD0.md` | yes | tracked | 49e2f87 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 161 | `prompts/Daily_Brief_Builder_Contract.md` | yes | tracked | 95c4b82 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 162 | `prompts/Daily_Brief_Contract_Amendment_1.md` | yes | tracked | 76cc314 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 163 | `prompts/Engine_1.0.2_NoShrink_Patch_Build_Prompt.md` | yes | tracked | 1d3e498 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 164 | `prompts/Engine_1_0_3_Input_Parity_Build_Prompt.md` | yes | tracked | 7f1b4a9 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 165 | `prompts/PC1_Pre_Census_Consolidation_Builder_Contract.md` | yes | tracked | 5b0e36e | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 166 | `prompts/Reviewer_Manifest_Builder_Contract.md` | yes | tracked | 95c4b82 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 167 | `prompts/SSv11_3_Grade_Legibility_Build_Prompt.md` | yes | tracked | 1d3e498 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 168 | `prompts/SSv11_Execution_Playbook_v1_1.md` | yes | tracked | 7f1b4a9 | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |
| 169 | `prompts/V3_Anchor_Run_Contract.md` | yes | tracked | 350b82b | yes (origin/v12-v1-census) | --workflow (naiad_workflow_2026-08-02.zip) + GitHub |

---

## 4 · COUNTS PER PROTECTION CLASS

| protection class | files | share |
|---|---:|---:|
| **NOT PROTECTED** | **0** | **0.0%** |
| ⚠ GitHub only (workflow copy is STALE) | 4 | 2.4% |
| GitHub only | 108 | 63.9% |
| `--workflow (naiad_workflow_2026-08-02.zip)` + GitHub | 57 | 33.7% |
| **total** | **169** | 100% |

### **TOTAL BYTES IN THE NOT PROTECTED CLASS: 0**

Every file in scope exists on disk, is tracked, is committed, and is pushed to
`origin/v12-v1-census`. There is no file in this scope that lives only on this disk.

### By area

| area | files | bytes | `--workflow` + GitHub | GitHub only | stale wf copy | NOT PROTECTED |
|---|---:|---:|---:|---:|---:|---:|
| `(repo root *.md)` | 58 | 1,144,044 | 0 | 58 | 0 | 0 |
| `claude` | 1 | 1,849 | 1 | 0 | 0 | 0 |
| `docs` | 23 | 558,782 | 18 | 5 | 0 | 0 |
| `exchange` | 31 | 287,758 | 25 | 2 | 4 | 0 |
| `prompts` | 13 | 195,072 | 13 | 0 | 0 | 0 |
| `scripts` | 43 | 954,156 | 0 | 43 | 0 | 0 |
| **total** | **169** | **3,141,661** | **57** | **108** | **4** | **0** |

### Reading the result honestly

**Zero NOT PROTECTED is the good outcome, but it is thinner than it looks.**

**108 of 169 files — 64%, including every one of `scripts/` and every repo-root `*.md` — are
"GitHub only".** One copy, on one third-party service. That is a real single point of failure for the
entire toolchain: `daily_brief.py`, `backup_estate.py`, every census and recompute script, the whole
charter and contract set at repo root. The `--workflow` archive deliberately does not cover `scripts/`
or repo-root `*.md`; the estate archive covers price data, not code.

**The 4 stale rows are the mechanism to watch, not the 4 files.** Every one is a file the daily
routine rewrites (`MANIFEST.json`, `RETENTION.md`, today's `DAILY_*` and `MANIFEST_*`). They go stale
in the archive within hours of every run, by design — the weekly archive simply cannot be current for
daily-churn files. Their current bytes live on GitHub alone until the next Sunday 08:30 run.

Neither observation is a defect in what was built. Both are the honest shape of the coverage, which
is what an inventory is for.

---

## 5 · NO-WRITE VERIFICATION

```
git status --porcelain   (before)   → 0 entries
git status --porcelain   (after)    → 1 entry: ?? exchange/reports/2026-08-02_HEPHAESTUS_report_disposition-inventory.md
```

**Unchanged apart from this report file**, which the paste's own REPORT directive requires. No
commits, no pushes, no deletions, no file moved or removed. Working scripts were written to the
session scratchpad **outside the repository** and touched nothing inside it.

---

## ITEMS FOR THE OPERATOR

1. **`git config --local user.name` is `t` / `t@t`.** Eleven commits of legitimate work are
   misattributed. One command fixes it going forward; history was not rewritten.
2. **`9470d04 base` remains unexplained** — a commit I did not author that also changed the repo's
   commit identity.
3. **64% of files in scope are GitHub-only**, including all of `scripts/`. If a code copy off GitHub
   matters, `scripts/` and repo-root `*.md` would need adding to the `--workflow` root list.
4. **Three committed report filenames carry `2026-08-03`** and should read `2026-08-02`; likewise one
   comment line in `.gitignore`. Both need a commit.
5. Still outstanding: **configure GitHub sync and click Sync now** · **paste the three settings
   blocks** · **take a fresh memory snapshot** · **ratify queue item 001**.

---

## FILE DISPOSITION TABLE — this paste

Per the standing rule adopted above. Every file this paste created, modified or moved:

| path | on disk | git status | committed | pushed | protected by |
|---|---|---|---|---|---|
| `exchange/reports/2026-08-02_HEPHAESTUS_report_disposition-inventory.md` | yes | untracked | not committed | no | **NOT PROTECTED** |

**One file created. Nothing modified, nothing moved, nothing deleted.**

This report is, at the moment of writing, the only NOT PROTECTED file this session produced — it
exists on this disk alone. It leaves that class the moment it is committed and pushed, and enters
`--workflow` coverage at the next Sunday 08:30 run. Committing it was not authorised by this paste.

Working files were written to the session scratchpad outside the repository
(`…\scratchpad\disposition.py`, `render_table.py`, `report_head.md`, `report_tail.md`,
`porcelain_before.txt`) and are not repository files; they are listed only so the record is complete.

---

## METRICS (Q-8)

**Operator actions this session = 1** (one paste).
**Files re-ingested = 0.**
