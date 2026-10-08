# SCOUT U9 · PROCESS — RESUME LAW, FIXTURES, REVIEW WORKTREES, CLOSE (mapped for TIER-C12)

Read-only scout. Scouted 2026-10-08 ~23:00Z (20:00 −03:00). Contract read verbatim:
`scratchpad/tc12/2026-10-08_TC12_APOLLO.md` sha256 `861d6050e80e66995e4f9db2855aaf274d63285249c2549e5a0813582095a7bd`
(12,209 B, 137 lines) — byte-identical to the main tree's `exchange/queue/2026-10-08_TC12_APOLLO.md`.

Abbreviations: **M** = `/Users/luis/Naiad` (main tree, branch `v12-v1-census`); **X** =
`/Users/luis/Naiad/.claude/worktrees/tierc11x` (branch `tierc11x`). `T11` = `M/research_outputs/tierc11`,
`XO` = `X/research_outputs/tierc11x`. Every number below was read from the cited file in this session. Where a figure
was computed by this scout from files it says "[measured here]".

---------------------------------------------------------------------------------------------------------------
## 1 · FACTS

### 1.1 The trees as they stand

| fact | value | source |
|---|---|---|
| main HEAD | `28e006bc5def421bd65e3835a95a2905c4e21b93` = `tierc12(STEP Q): contract filed verbatim — exchange/queue/2026-10-08_TC12_APOLLO.md sha256 861d6050…` (one file, 137 insertions, 2026-10-08 19:52:13 −0300) | `git -C M show --stat 28e006b` |
| main HEAD moved during this scout | `a399b47` (auto-publish 2026-10-08) → `28e006b` | git status snapshot vs `git rev-parse HEAD` |
| main dirty state (pre-existing, not TC12's) | ` M exchange/status/daily/DAILY_2026-10-08.md` · ` M research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt` (mtime Sep 23 11:36) · untracked `pine/SS12_*.pine`, `pine/SS_Anchor_v12_T_0.pine`, five `research_outputs/*.html` / `VIZ3-4/` | `git -C M status --porcelain` |
| remote-tracking ref | `origin/v12-v1-census` = `ac8d8da` (pushed 2026-09-26 07:00:07 −0300 by the daily routine); main is **15 commits ahead** (14 auto-publish + STEP Q); `6f34939` (tierc11 CLOSE) IS an ancestor of `ac8d8da` | `git reflog show origin/v12-v1-census`; `git merge-base --is-ancestor` |
| the push is failing now | "publish did not complete: committed a399b47 but push failed: ssh: connect to host github.com port 22: Undefined error: 0" | `M/exchange/status/daily/DAILY_2026-10-08.md:123` |
| X tip | `7b24f835bcbf7430eb0f97b6c39b6b1b233eef11` (`tc11x(X-CLOSE): …`), porcelain = one line `?? research_outputs/tierc11x/close/CERTIFIED_TIP` | `git -C X rev-parse HEAD`; `status --porcelain` |
| `XO/close/CERTIFIED_TIP` | 41 B, holds `7b24f835bcbf7430eb0f97b6c39b6b1b233eef11`; untracked BY DESIGN | file; `XO/close/close_acts.sh:56,133-141` |
| merge base main↔tierc11x | `e97ad73` (tierc11 TC11-D) | `git merge-base` |
| paths changed since the base | main 225, tierc11x 161, **overlap 0**; X has no path outside its allow-list | `git diff --name-only` [measured here] |
| `scripts/tc11x_*.py` in main | none (X's code exists only on `tierc11x`) | `ls M/scripts/tc11x_*` |
| `M/exchange/rows/` | does not exist (it exists only on `tierc11x`: 3,072 KB) | `ls` |
| `M/research_outputs/tierc12/`, `scripts/tierc12_*`, `analytics/value_area.py` | none exist | `ls` |
| registered worktrees | 31: main, `tierc11x`, 28 × `wf_8995cf0d-ab5-*`, `MAILBOX/.claude/worktrees/adoring-franklin-efc306`; no `tc11-review-*` / `tc11x-rv-*` left; 0 prunable | `git worktree list --porcelain` |
| `.claude/worktrees/` | excluded by `M/.git/info/exclude` (`**/.claude/worktrees/`) | file |
| machine | 18 cores, 51,539,607,552 B RAM; 1.6 TiB free; `/Volumes/LaCie` mounted | `sysctl`, `df`, `ls /Volumes` |

### 1.2 The resume law and PROGRESS.json

**The law's text of record** — `M/exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:11-24` (LAW OF RESUMPTION 1-6) and
`:26-33` (R0 census). TC12's contract names it at `:5-6` ("R0 census · verify-or-quarantine · frozen texts · one
corridor · draft off-bus · commit + PROGRESS.json per stage").
1. COMPLETE only if artifacts exist, manifest shas verify, fixtures RE-PASS now; else PARTIAL.
2. Partials QUARANTINED to `research_outputs/<tier>/_partial_<ts>/` (format `_partial_<YYYYMMDD>T<HHMM>Z`), never deleted.
3. Registration texts FROZEN; a re-computed verdict prints BESIDE the fresh value, never re-chosen.
4. ONE corridor: the as-of of the COMPLETE Stage D manifest governs every stage.
5. The build doc drafts under `research_outputs/<tier>/` and moves to `exchange/reports/` ONLY at close.
6. After EVERY stage: commit + update PROGRESS.json {stage, status, artifact shas, as_of, fixtures} + one line to the draft.
R0 (read-only; writes only PROGRESS.json): identity v2 · branch · HEAD · `git log --since` · `git status` · inventory per
stage · PRINT THE STAGE LEDGER (COMPLETE-VERIFIED / PARTIAL / ABSENT) · resume at the first non-complete stage.

**TC11's `T11/PROGRESS.json`** (sha256 `dbcc08cf60a9dbb5827c65f3728857fcab12df50aeefee7667ba3dbfc205c4fe`, 101,683 B;
hand-maintained by the orchestrator — no `scripts/tierc11_*` writes it):
- top-level keys, in order: `tier` "TIER-C11" · `identity` "v2" · `branch` · `head_at_r0` · `seed` 20260924 ·
  `substrate` "tc11_20260925" · `as_of_of_record` · `as_of_last_closed_4h_close_ms` 1790294400000 ·
  `contract_of_record {path, sha256}` · `leans_of_record {path, sha256}` · `registrations_of_record {path, sha256, head}`
  · `live_cache_touched` false · `r0_census_utc` · `r0_census` (prose) · `law_1_note` · `resume_point` (prose) ·
  `stages` (list of 20) · `amendments_of_record {path, sha256}` · `last_sweep_utc`.
- `r0_census` (fresh-tier form): "fresh tier: no tierc11 artifact existed before STEP Q (b9ed953); nothing to verify or
  quarantine. TC10 CLOSE is PARTIAL (operator's close_acts.sh not run) … TC11 builds on TC10's filed artifacts read-only
  and its CLOSE is ordered after TC10's (LEANS L-F.4)."
- stage record keys: `stage, status, as_of, blockers, artifact_shas, fixtures, one_line` (+ `artifact_count`, `notes`).
  `artifact_shas` = `{repo-rel path: {"bytes": int, "sha256": hex}}`. fixture record keys: `suite, exit_code, legs_red,
  legs_total, transcript_drift, transcript_sha_before, transcript_sha_after, wall_seconds` (+ `note`).
- stage names: `STEP Q, TC11-REG, TC11-D, TC11-ENV, TC11-BOOKS, TC11-NEST, TC11-RIDE, TC11-R, TC11-R4, TC11-S, TC11-W,
  TC11-G, TC11-T-BRK, TC11-T-RELAY, TC11-A, TC11-H, TC11-SCORE-BUILD, TC11-SCORE, TC11-LANES, TC11-FIX`; all 20 are
  `COMPLETE-VERIFIED`. **There is no TC11-CLOSE stage record**; `resume_point` = "TC11-CLOSE (build draft, …,
  close_acts.sh ordered after TC10's close)". `last_sweep_utc` = "2026-09-25 (TC11-FIX): 17 suites, 134 fixtures GREEN,
  transcripts byte-identical".
- legal statuses (TC10's law): `LEGAL_STATUS = ("COMPLETE-VERIFIED","PARTIAL","ABSENT")`, `STAGE_KEYS`, `FIXTURE_KEYS`
  at `M/scripts/tierc10_resume_fixtures.py:296-300` (as mapped in `T11/scout/H_fixture_conventions.md:405-419`). TC10's
  own PROGRESS has three PARTIAL stages: `D-CORE`, `D-5M`, `CLOSE` (`M/research_outputs/tierc10/PROGRESS.json`, sha
  `e0abf4cacc869c8b7282bcd52e0e7bba36d7f75e068774d8674696bbcf72b549`).
- "COMPLETE-VERIFIED ⇒ zero blockers, ≥ 1 fixture record, every exit 0, every legs_red 0"; fixture records are matched
  BY INDEX against HEAD, so **append, never insert** (`H_fixture_conventions.md:419-424`).

**X's pattern (the one parallel builders used)** — `X/scripts/tc11x_progress.py` (86 lines, sha256
`5dbd5c916eb6ed509eedc5a1e51ff3b0cf8c9e7dc07505731bf98a1603d37562`):
- builders write `XO/progress/<STAGE>.json` and **never PROGRESS.json** (`:4-7`); `main()` (`:33-82`) merges: a `fixed`
  list of pre-stages typed in the script (`:34-51`: STEP Q, X-UNDERSTAND, X-VENDOR, X-LEANS, each with `commit`), then
  every `progress/*.json` except `fix_*` (`:53-58`), each carried verbatim plus `_record {path, sha256}`, ordered by
  `ORDER` (`:19-20`) through `stage_key` (`:27-30`); header keys `tier, branch, seed, substrate,
  as_of_last_closed_4h_close_ms, as_of_of_record, contract_of_record, leans_of_record, amendments_of_record, law_1_note,
  merge_law, stages, registrations_of_record` (`:60-79`). Run: `~/venvs/naiad/bin/python -B scripts/tc11x_progress.py`.
- X's header has **no** `r0_census`, `resume_point`, `head_at_r0`, `live_cache_touched`, `last_sweep_utc`.
- X used a fourth status word: `X6` "COMPLETE", `X-REVIEW` "COMPLETE", `X-CLOSE` "COMPLETE (repaired: …) — awaits the
  orchestrator's X-CLOSE commit …, close/CERTIFIED_TIP, and the operator's close_acts.sh run" (`XO/PROGRESS.json`, sha
  `4c91b2efef002e7347f125bc9bcb1450f7eb35a7888814a4b7d8c67fe9b39475`).
- progress record files on disk: `X-D, X-REG, X-FOUND.books, X-FOUND.ranges, X1..X6, X-SCORE, X-FIX, X-REVIEW, X-CLOSE`
  + `fix_FOUNDATION, fix_X1_X4, fix_X2_X3, fix_X5_X-SCORE, fix_X6` (`ls XO/progress`).
- stage plan table (# · stage · what · artifacts · fixtures) + order constraints: `XO/REGISTRATION_PLAN.md:334-387`.

### 1.3 LEANS — format, review, freeze, amendments

**Reading format** (`T11/LEANS.md`, sha256 `655e1605165e7a66c67f544e5cda421b46aa0b6fcd4cb97a6ad19654479f294f`, 590
lines): header block `:1-17` (contract path + sha, executor, seed, "Frozen BEFORE any TC11 range or trade book was
computed", the two bullet laws: "A reading may be challenged at CLOSE. It is never re-chosen after a number is seen." /
"If a reading must change mid-build, the change is filed … as a dated AMENDMENT"). Each reading is
`**L-<stage>.<n> TITLE** — "<contract phrase quoted>"` + what it chose + why + the rival; cheap rivals print as Tier-E
twins. Sections: `## 0 Substrate, corridor, code reuse` (L-0.1..0.5) · `## 1 Tolls, eras, rulers, verdicts`
(L-1.1..1.7) · one `##` per stage · `## 9 Fixtures and close` (L-F.1 F-DET `:520`, L-F.2 IMPORT-CLOSURE `:523`,
L-F.3 WORKTREE ATTESTATION `:531`, L-F.4 CLOSE ORDER `:537`) · `## 10 Review disposition` (`:545`: ACCEPTED table
finding→where, REJECTED with reasons).

**The printed tag.** Code prints readings as `[LEAN-HEPHAESTUS] L-…` lines in lean blocks / transcript headers:
`LEAN_TAG = "[LEAN-HEPHAESTUS]"` at `M/scripts/tierc11_env.py:132`; e.g. `M/scripts/tierc11_books.py:226-244`,
`M/scripts/tierc11_data.py:330-371`; X: `XO/close/FIXTURES_CLOSE_draft.txt:4-7`.

**Names/git readings to mirror:** L-0.4 (`:66-69`): scripts `scripts/tierc11_*.py`, outputs `research_outputs/tierc11/`,
commit subjects start `tierc11(`, PROGRESS stages prefixed `TC11-`, own PROGRESS ledger. L-0.5 (`:71-75`): `.gitignore`
gains lines only at its END; documents of record committed; parquet shas live in PROGRESS and manifests; only tier
paths staged.

**How it was reviewed and frozen.**
- TC11: five lenses `fidelity, causality, statistics, buildability, trading` (51 findings) →
  `T11/review/LEANS_REVIEW_2026-09-25.json` (a workflow journal: `summary, agentCount 5, result[5] {lens, findings,
  summary}, workflowProgress, totalTokens 1089019`); disposition merged into LEANS §10; frozen by commit `4ed4e67`
  `tierc11(TC11-REG): executor readings frozen and the nine registrations filed — before any TC11 book`;
  `T11/registrations/REGISTRATIONS.json` (sha `648834bf30e20e92713bddef2374ddef1aae843f4d8ba152fc50166c8cc6f1ee`) pins
  `contract.sha256` and `leans.sha256`; `REGISTRY_PIN.json` (`ea77921a410db962376412a5f179fd3d9225f81fb5405a788c8077cd46de748f`)
  repeats head `6772568b…`, `contract_sha256`, `leans_sha256`.
- X: `XO/review/LEANS_X_REVIEW_2026-09-25.json` (sha `e753601e84a8da01fe19ac2a32372d53693f28e794cd8c5dcc8d0d452645dd48`,
  185,410 B) — keys `tier, artifact, date, contract{path,sha256}, drafted_sha, revised_sha, plan_drafted_sha,
  plan_revised_sha, lenses[5]{lens, verdict_on_draft, findings[{id, severity, where, quote, …}]}, orchestrator_notes,
  conflicts_ruled, corrections_by_reviser, reviser_reads_note, preserved_bytes, counts, critic_pass`.
  **The five lenses:** FIDELITY · CAUSALITY — as-of and look-ahead · STATISTICS — rulers, verdict rule, cluster
  granularity, independence, honesty labels, forking paths … · BUILDABILITY · TRADING. `counts`: 64 findings, 60
  accepted, 4 rejected; by severity BLOCKER 1+1, MAJOR 28+0, MINOR 31+3. Then a **second pass, the completeness
  critic** (`critic_pass`: 110 clauses checked, 17 gaps, all closed; `leans_sha_after bf6c36eb…`, `plan_sha_after
  a887ea64…`). Frozen at commit `c2da417` `tc11x(X-LEANS)`; `LEANS_X.md` of record =
  `74a989ee6357e2169f2ad88722b67f1174cf0d080783dc8c77f5f064e3468623` (250,656 B, 2,720 lines) = the critic's bytes
  (prefix 249,653 B) + the orchestrator's re-ruling block (1,003 B) — `XO/review/WORKTREE_ATTEST_REG.jsonl` record 2.
- X's known gap: the drafts were reviewed UNTRACKED in the build worktree, so "HEAD == reviewed sha, detached" could not
  bind; X substituted a **hash-bound attestation** (`WORKTREE_ATTEST_REG.jsonl`: header, three `bind` records,
  per-review `cwd/head: "not recorded"`) — `XO/LEANS_X.md:474-480`. The rival it names: commit the drafts first as
  `tc11x(X-REG-DRAFT)` and review that sha in detached worktrees.

**Amendments without editing the frozen file.**
- TC11: `T11/LEANS_AMENDMENTS.md` (sha `85f57ce7832b2754cff70fe052dc87dcf4bcf4182f61112c7a1d227df84f0c07`, 133 lines).
  `:3-8`: LEANS.md "stays byte-frozen, because REGISTRATIONS.json pins its sha"; **Law:** "an amendment may follow from a
  build fact … or from a verifier's finding. It may never follow from a registered rule's outcome." Dated WAVE headings
  (`## FOUNDATION WAVE — 2026-09-25, filed before any stage runner …`, `## STAGE WAVE`, `## FINAL-REVIEW WAVE`), items
  `**AM-n · L-x.y (source).**` each naming what was redone; errata are new items ("AM-5 ERRATUM"). PROGRESS carries
  `amendments_of_record {path, sha256}`.
- X: `XO/LEANS_X_AMENDMENTS.md` (sha `af845b95d1c7699f788aa242af6f5bef0d0f86b92a74a938cb7ca14c9d87d059`): AM-X1..AM-X28,
  heading `## AM-Xn · <date> (~HH:MMZ) · <readings> · ruling on AP-n (option)`, body **Text amended. / Amended to. /
  Reason.**; builders PROPOSE in `XO/AMENDMENTS_PROPOSED.md` (AP-n), the orchestrator RULES (`:1-7`).

### 1.4 Fixture-suite conventions

- One suite per stage: `scripts/<tier>_<stage>_fixtures.py` → transcript `research_outputs/<tier>/<stage>/FIXTURES_<X>.txt`
  (TC11: 18 tracked transcripts; X: 17). Tally line `  N GREEN, M RED` (e.g. `T11/closure/FIXTURES_CLOSURE.txt` last
  block). Sum of TC11's 17 swept suites = 134 [measured here from the tally lines: 14+4+8+7+9+8+11+4+9+9+9+7+7+7+15+3+3].
- **The harness of record** (`M/scripts/tierc11_closure_fixtures.py`): `say(line)` `:169` (deterministic → transcript;
  temp paths scrubbed by `_TMP_RX`), `clock(line)` `:175` (stdout only), `prove(fid, title, break_if, real_if,
  break_leg, real_leg)` `:183` — BREAK leg FIRST, must go RED or the fixture is VOID; a break leg that raises proves
  nothing; `plants(rows)` `:207` — rows `(name, expected detector substring, thunk -> findings)`, judged ONE AT A TIME,
  CAUGHT only if a finding NAMES THE INTENDED DETECTOR; a crash is a FIXTURE DEFECT; a `SystemExit` is a finding.
  Transcript lines: `<FID> — <title>` / `  [BREAK] FAILS IF: …` / `  [BREAK] deliberate violation -> RED (correct): …` /
  `  [REAL]  FAILS IF: …` / `  [PASS] <FID>: …`.
- **First transcript line** = `as_of_last_closed_4h: <ISO>` (`AS_OF_LINE` `:115`), then `=`×78 banner, title, `seed … ·
  substrate … · pin …`, the typed-literals lines.
- **No-clobber transcript law** — `file_transcript(out, body, refile)` `:1161-1171`: absent and no `--refile-transcript`
  → finding, nothing written; identical bytes → silent; different bytes and no refile → writes `<stem>_rerun.txt`,
  record untouched, RED; a leg-substring run writes `…_partial.txt`, never the record (`:1215-1216`). Exit 1 if any RED
  **or** any transcript finding (`:1222`). CLI: `[leg-substring ...] [--refile-transcript] [--root=DIR]`.
- **Banned** (every header): self-comparison; one example where cardinality was possible; a check whose claim is not the
  design's claim (`:80-81`). Fixture-typed literals are a second object, never the module's own (`:111`).
- **X's common law** `XO/LEANS_X.md:2282-2299` (LX-F.1): `FAILS IF:` on every leg + a sabotage that must turn RED;
  hook legs in subprocesses; truncated-tape legs build fresh arrays; **production against production** (the sabotage is
  planted inside the production function, never in the comparator); per-directory manifests; as-of legs hold a fitted
  pin at its filed value and say they do not test the pick; every stage that runs a fixture files a transcript and
  PROGRESS records its sha before and after the re-run.
- **F-DET** (TC11 L-F.1 `T11/LEANS.md:520-521`): two subprocess builds with PYTHONHASHSEED "1" and the tier seed into
  `_det_*/`, byte-equal on file set, bytes and parquet content shas; no clock field (X adds: a worker count or load
  average counts as a clock field, regex `CLOCK_NAME_RX` at `X/scripts/tc11x_books_fixtures.py:203-204`).
- **Per-directory manifest** `build_manifest.json` {`sha` (content sha per table), `keys`, `skipped_empty`, `input_sha`,
  `seed`, `as_of` …; X adds `code_sha`, `contract_sha256`, `leans_x_sha256`, `amendments_of_record`, `pins`} written via
  `TP.make_put`; F-KEY and F-DET run per directory (`XO/LEANS_X.md:431-436`).
- **The sweep: there is NO sweep driver script in either tree** (`ls scripts | grep -i 'sweep|roll|run_all|suite'` is
  empty in both). TC11's "17 suites / 134 fixtures" sweep and X's "full roll" were run by a gate agent, **one suite at
  a time, each in a fresh process, in plan order, WITHOUT `--refile-transcript`** ("the harness writes nothing when the
  bytes are identical and a *_rerun.txt otherwise; none was written" — `XO/progress/X-FIX.json` `gate_method.no_refile`).
  X's roll: 12 suites, 102 GREEN, 0 RED, 583 plants, 16:04:59Z–16:36:15Z, Σ wall 1,871.4 s (`X-FIX.json` `suites[*].wall_s`,
  `suites_totals`). Its order list is `ROLL` at `X/scripts/tc11x_close_draft.py:121-137`.
- TC10's nearest thing: `scripts/tierc10_resume_fixtures.py` (F-C10-RESUME, re-hashes filed artifact shas; all literals
  TC10-specific; sweeps `scripts/tierc10_*.py` by `TC_SUITE_GLOB` and the tierc10 root — `T11/scout/F_close_ledger_publish.md:14-18`).

Per-suite walls on record (seconds):

| suite | wall | source |
|---|---:|---|
| X-D 19.7 · X-REG 4.0 · X-FOUND(a) 25.7 · X-FOUND(b) 13.9 · env re-pass 24.2 · X1 93.8 · **X2 350.4** · **X3 (VA) 988.9** · **X4 300.4** · X5 26.4 · X6 7.5 · X-SCORE 16.5 | | `XO/progress/X-FIX.json` `suites[*].wall_s` |
| TC11-ENV 15 · R 124 · **R4 805** · S 6 · W 126 · G 20 · T-BRK 83 · T-RELAY 30 · A 43 · H 71 · SCORE-BUILD 127 · scorer run of record 22 | | `T11/PROGRESS.json` `stages[*].fixtures[*].wall_seconds` |
| TC11 nest suite 240.7 (F-CAL 96.7, F-EQ-SCAN 76.4, F-NEST-ASOF 46.7 on 5 forked workers ≈185 serial, F-DET 15.8) | | `T11/review/FOUNDATION_REVIEW_2026-09-25.json` `.modules[1].built` "Wall times" |

### 1.5 Import closure

**TC11** — `M/scripts/tierc11_closure_fixtures.py` (sha `68253ed1a09a70c5828f08ede47c1ad0358c61fb7659948e7d77469a9c2f2d4e`;
3 legs: F-CLOSURE-ALL · F-HOOK-ESCAPE-ALL · F-DET → `T11/closure/FIXTURES_CLOSURE.txt`):
- **How the decision set is enumerated:** `tierc11_names()` `:246-248` = every `scripts/tierc11_*.py` whose stem does
  not end `_fixtures` (a GLOB). THE DECISION SET = that set **minus** `NEST = "tierc11_nest"` and the TYPED runners
  `RUNNERS_T = ("tierc11_stage_a","tierc11_stage_h","tierc11_stage_r","tierc11_stage_r4","tierc11_stage_t_brk")`
  (`:119-121`). **Each exemption must be EARNED** (the runner's source must import `tierc11_nest`, else "EXEMPTION
  UNEARNED"). **A module the file does not name defaults to the DECISION set and is scanned** (`:9-13`).
- **The lineage** = the static repo closure of the DECISION set (imports anywhere incl. function bodies, plus
  name-held dynamic imports), which must hold `LINEAGE_ENV_T` (15 modules: `tierc2_baseline … tierc9`, `:122-124`) and
  every repo module a fresh interpreter actually loads.
- **Forbidden:** `FORBIDDEN = ("rangefinder","tierc10_census","tierc10_stamps","tierc10_null","tierc11_nest")` (`:118`),
  SUBSTRING match on module names; plus a `Range.top/.bottom` read by attribute / `getattr` / `__dict__` / `vars()`;
  a non-constant import site other than the declared door `DYN_DECLARED_T = (("tierc11_env","tc10_import"),)` (`:144`); any
  `exec/eval/compile`; a `sys.modules` reach.
- Two detectors: a fresh interpreter per DECISION module (`sys.modules` after import; module must load from
  `scripts/<name>.py`) AND this file's own AST walk (`walk_imports` `:293`, `dyn_sites` `:312`).
- **F-HOOK-ESCAPE-ALL** (AM-2/AM-8): `E.hook_escapes(src)` (`M/scripts/tierc11_env.py:1212`) over every non-fixture
  tierc11 module — no pyarrow-native I/O, no os-level out-of-process call; `subprocess` only in the three AM-8 modules,
  each with ONE pinned call site (`AM8_SITE_T` `:135-139`) and git subcommands ⊂ `{worktree, rev-parse, status, show}`.

**X** — F-CLOSURE-X in `X/scripts/tc11x_books_fixtures.py` (`:1162-1250`; typed sets `:194-201`): decision closure
`("tc11x_books","tc11x_pct") + ("tc11x_era","tc11x_exit","tc11x_forward")`; `FORBIDDEN_SUBSTR_TYPED = ("rangefinder",
"tierc10_census","tierc10_stamps","tierc10_null")`, **`FORBIDDEN_EXACT_TYPED = ("analytics.profile",
"analytics.rangefinder_census")`**; leg (ii) AST: the source **imports nothing under `analytics`**; leg (iii) the
`tierc*_rules` closure holds no analytics; leg (iv) `hook_escapes` over a GLOB `tc11x_*.py` minus `_fixtures`; leg (v)
the range-door law: only `tc11x_ranges` imports a range module, only `{tc11x_ranges, tc11x_sfp, tc11x_va}` reach one,
**only `tc11x_va` imports `analytics.profile`** (`XO/progress/X-FIX.json` `f_closure_x.range_law`).

**What "extends to analytics/value_area.py — decision modules import NOTHING from it" requires on this disk:**
- `analytics/` precedent is `M/analytics/rangefinder_census.py:1-40`: "[LEAN-HEPHAESTUS] L3 … a PURE numpy port (no
  engine import, no IO, ATR passed IN as an argument), NOT added to analytics._MODULES (analytics_sha stays put) —
  printed as a finding." Walls it names: **I-B/F-AN-3** (nothing under analytics may import engine; "the test globs
  EVERY file in this directory, listed or not"), **I-A/F-AN-4** (no IO), **F-BR-14**, **I-D** (analytics ATR is
  SMA-seeded with a NaN warm-up; the engine's is Wilder RMA seeded at TR[0] → **no ATR computed inside; the caller
  hands it in**).
- `M/tests/test_analytics.py:120-121` `_sources()` globs `analytics/*.py`; `:124-127` F-AN-3 (regex
  `^\s*(from|import)\s+engine\b`); `:147-160` F-AN-4 bans the tokens `read_parquet, requests, urllib, os.environ,
  socket` and any `open(` call in code (comments/strings stripped).
- `M/analytics/__init__.py:116-118` `_MODULES` = 10 files (`__init__, momentum, vwap, volatility, profile, structure,
  levels, stats, parity, nesting`); `analytics_sha()` `:123-136` hashes exactly those. Now: `ANALYTICS_VERSION` 1.5.0,
  `analytics_sha()` = `ea5f02f21ca43b6b71e450b540ff09c807b305971e3eb8cff50bea84c985dc91` [measured here]; the same value
  is printed in `M/analytics/INTERFACE.md:8-9`. Consumers of `analytics_sha`/`ANALYTICS_VERSION`: brief2, brief_capture,
  forward_log, oracle_daily, tierc2..tierc10 manifests, tests (grep). `tests/test_analytics.py:1040-1167` also holds
  `analytics/INTERFACE.md` byte-equal to `exchange/status/INTERFACE_PUBLISHED.md`.
- The lineage imports the PACKAGE: `import analytics as AN`, `from analytics import vwap/volatility/structure/momentum`
  (grep over `scripts/tierc[2-9]*`). So `analytics` is in `sys.modules` of every decision interpreter; a closure leg
  must match the exact module `analytics.value_area` (and attribute reach `analytics.value_area`), not `analytics`.

### 1.6 Review-worktree attestation — the two procedures on disk

**TC11's tool** — `M/scripts/tierc11_worktree_attest.py` (sha `96bfbab887e8eeacf0f7a02d2c5931a4d326fc6ca743c87ecf927bcac4592a45`):
```
~/venvs/naiad/bin/python scripts/tierc11_worktree_attest.py --commit <sha> --lens <name> --open
        (prints the worktree path; the reviewer works there)
~/venvs/naiad/bin/python scripts/tierc11_worktree_attest.py --lens <name> --close [--out-dir=DIR]
```
- `open_wt(commit, lens, out=OUT, stage_root=ROOT) -> dict` `:247`: `git worktree add --detach
  .claude/worktrees/tc11-review-<lens> <commit>` (`wt_path` `:239`); **stages the gitignored parquet** (copies every
  `research_outputs/tierc11/**/*.parquet` not under `_det_*` from the main tree: `STAGE_GLOBS` `:65`,
  `stage_artifacts` `:113`, `shutil.copy2`); stages EXACTLY two TC10 records read-only 0444 (`TC10_STAGED` `:70-71`);
  reads the **reviewed commit's own record** with `git show <commit>:research_outputs/tierc11/PROGRESS.json`
  (`commit_record` `:175`: every stage's `artifact_shas`, the LAST stage recording a path governs) and files findings
  `STAGED != RECORD / STAGED NOT IN RECORD / RECORDED NOT STAGED / NO RECORD`; records `before = {head, porcelain}`
  (`state` `:90`: `git rev-parse HEAD`, `git status --porcelain`); writes `<out>/<lens>.open.json`.
- `close_wt(lens, out=OUT) -> dict` `:277`: `after` state; RED if HEAD ≠ commit or porcelain non-empty before or after;
  re-hashes every staged file (`STAGED CHANGED / VANISHED / STAGED-CLASS APPEARED`); re-checks TC10 records against
  the main tree; `git worktree remove --force`; writes `<out>/<lens>.json` with `verdict` GREEN/RED, `fails_if`.
  Exit 0 iff GREEN. Records of record: `T11/review/attest/{causality,fidelity,reproducibility,statistics,trading}.json`
  (reviewed commit `04067a04…`, 142 staged artifacts, GREEN) and `fix-head.json` (`d307829`, GREEN).
- TC11's FINAL-review lenses: **causality · fidelity · reproducibility · statistics · trading**.
- Its fixtures: `M/scripts/tierc11_attest_fixtures.py` (sha `36c8fbbfbfc7e5a17629d1916a5c11d796b1b91d74255b5af3d926e56ec42734`)
  — F-ATTEST (14 plants on real scratch worktrees `tc11-review-fixture-<tag>`), F-DET, F-GUARD →
  `T11/closure/FIXTURES_ATTEST.txt` "3 GREEN, 0 RED" (157 parquet staged at that run).

**X's procedure** — `XO/review/attest.sh` (44 lines, sha `f7779b54bab2edf3ffdb84176f702bf72576c6b1c732d4910bbac3a90c8b3bf5`;
"A bash script, not a scripts/tc11x_*.py source, because it runs git out of process", `:12-13`):
```
attest.sh <before|after> <reviewed_sha> <lens>=<path> [<lens>=<path> ...]
```
per worktree appends one JSON line to `review/WORKTREE_ATTEST.jsonl` IN THE BUILD worktree: `phase, lens, realpath,
head, reviewed_sha, detached, porcelain_lines, porcelain_sha256, ignored_lines, ignored_sha256, ok, why`. Commands:
`git --no-optional-locks rev-parse HEAD`, `rev-parse --abbrev-ref HEAD` (detached iff "HEAD"), `status --porcelain=v1
--untracked-files=all`, `status --porcelain=v1 --ignored=matching`. FAILS (exit 1) if HEAD ≠ reviewed sha; not
detached; porcelain non-empty; or at `after` the ignored listing's sha differs from its `before` record (`:32-38`).
- Record: `XO/review/WORKTREE_ATTEST.jsonl` (10 lines, sha `c13d4f5ed224023d73061d52477997e7eb8ede3fddc64dbaa5d67e1edb433fd3`):
  five `before` + five `after`, all `ok: true`, HEAD `7cd24970f223a180048b7350c4c29b2618333bd4`, `detached: true`,
  `porcelain_lines 0`, `ignored_lines 0`, both shas = `e3b0c442…b855` (the empty string's sha256).
- X-REVIEW's five lenses: **verdicts · causality · fidelity · isolation · landing**; worktrees
  `/Users/luis/Naiad/.claude/worktrees/tc11x-rv-<lens>` (all since removed).
- A judge record followed: `XO/review/BUILD_REVIEW_2026-09-25.json` (keys `reviewed_sha, lenses, deduped, fix_now,
  carry_to_close, rejected, verdicts_stand, verdicts, severity_tally_after_judging, judge_checks, close_brief`) and
  the corrected `review/CLOSE_BRIEF.json` that the report renderer obeys.
- A side effect worth knowing: the untracked attest log turned X6's F-ROWS (SCOPE) RED until AM-X26 typed it into the
  ferry's class list (`XO/progress/X-REVIEW.json` `suites_totals.red_before_this_stage`).

### 1.7 As-of warranty stamps and the Tier-E collar

- **Nine as-of columns on every table** — `AS_OF_COLUMNS` at `M/scripts/tierc10_panel.py:2557-2560`:
  `as_of_last_closed_4h, as_of_panel_start, as_of_span_days, warranty` (the four of `tierc8.stamp(df, meta)`,
  `M/scripts/tierc8.py:96-111`; `warranty` text = "these numbers are true AS OF the corridor named in this row and of
  no other; the corridor advances with the cache [TC6V-a]") + `as_of_lens, as_of_last_closed_bar, as_of_panel,
  as_of_n_assets, as_of_substrate` (added by `stamp_n(df, meta, lens="4h", lens_last_closed_ms=None)` `:2528-2554`,
  which HALTs if a lens edge falls after the corridor end).
- `lens_edge(hi_ms, lens)` `:2515`; `LENS_MS` `:2511-2512` = `{5m, 1h, 4h, 12h, 1d, 1w}` (no 15m; 1w Monday-anchored).
- Writer: `make_put(root, meta, lens="4h") -> (put, W, K, SK)` `:2563-2588`; `put(df, name, key, lens_=None,
  lens_last_closed_ms=None, meta_=None)` stamps (unless already stamped), writes through
  `tierc2_baseline.write_table(df, name, keys, root) -> content_sha` (`M/scripts/tierc2_baseline.py:170-188`: round
  floats to 6 dp, mergesort by key, atomic `.tmp` → `os.replace`); `_content_sha(df)` =
  `sha256(df.to_csv(index=False))` (`:155-159`); `assert_key` `:191`.
- Checks: `grid_whole(declared, written, cell_col="cell", require_cols=(), require_false=(), label="grid")` `:2592-2625`;
  `check_keys(root, manifest=None, need_cols=AS_OF_COLUMNS)` `:2628-2658` (globs `root/*.parquet`, no recursion);
  `check_det(root_a, root_b)` `:2661-2689`.
- **The collar has no single shared helper.** Three generations:
  - TC10: `COLLAR_COLUMNS = ("tier","gates","m_looks_this_table","m_note","in_sample")` (`M/scripts/tierc10_census.py:362`).
  - TC11: dict `COLLAR = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result", "gates": "nothing"}`
    re-typed per module (`M/scripts/tierc11_score.py:258-259`, `tierc11_stage_r.py:148-149`), plus `would_read_ci_only`
    (`T11/LEANS.md:128-131`).
  - X (the fullest): `COLLAR_COLS = ("tier","selection_not_a_result","gates","would_read_ci_only",
    "m_looks_this_table","m_note")` (`X/scripts/tc11x_books.py:137-138`), `M_NOTE` `:131-132`, and the helper
    **`collar(df, would, m) -> DataFrame`** at `X/scripts/tc11x_exit.py:1175-1185`; grids also carry
    `promotable = False` as a `require_false` of F-GRID (`XO/LEANS_X.md:814-830`).

### 1.8 The CLOSE machinery

**TC11** — one deterministic generator `M/scripts/tierc11_close.py` (2,814 lines, sha
`246b32cb72479922f7f107c08e76dad830743acbfd0f9558077e7db2337bf81a`) + `tierc11_close_fixtures.py` (2,216 lines, sha
`435b57191adee2b7810ddb9a3be39324506fec7a3207634a31dfb09ee33f43d8`). Writes exactly (`:24-30`): `BUILD_DRAFT.md`,
`LEDGER_APOLLO_APPEND.md`, `close/S5_FINDINGS_NOT_FIXED.{json,md}`, `close/BOX_COST.{md,json}`, `close/TRACES.json`,
`close/close_acts.sh`. "never writes under exchange/, never commits, never pushes and never calls publish()" (`:7`).
Two typed input records: `close/COMPUTE_LEDGER.json` ("the ONE exception to 'no typed number'") and
`close/TC11_FIX_VERIFY.json`. Imports TC10's import-safe quote helpers `tierc10_close_close_ledger_append as LA`
(`:83`). Close fixtures (9): F-S0-NINE · F-NUM · F-FEAS-0 · F-LAR11 · F-BOXCOST · F-FNF · F-CLAIMS · F-CLOSE-ORDER ·
F-DET (`tierc11_close_fixtures.py:9-43`) → `close/FIXTURES_CLOSE.txt` "9 GREEN, 0 RED".

**X** — four modules (+ fixtures): `tc11x_close_draft.py` (renderer; sha `bdc8b4c91f802fec32a347dc396d36efd08a75a915a3f0abd2416326fc4be8e5`),
`tc11x_close_findings.py` (`17a3e5c24a4ce742cabd0b799b4adb1f0392eca64a3e4287c5dd27190cbaa34c`), `tc11x_close_box_cost.py`
(`aec455fc12d586bf92e48e5df6e5186a3de949fc8e89f61762be730c6a723d9b`), `tc11x_close_fixtures.py`
(`ef00901584fec058b81e6b613282a801adb5d17dcfe397dc961ea7c5b6f6656e`: F-LEDGER-FMT · F-ISO (b) · F-ISO (c) ·
F-CLOSE-SCRIPT · F-LAND, and `--stamp` used by close_acts step 5), plus `tc11x_land.py` (the TC11-landing printer).

**BUILD_DRAFT layouts (§ headings, read from the files):**

| TC11 `T11/BUILD_DRAFT.md` (887,648 B; sha `e2cc3648…4233`) | X `XO/BUILD_DRAFT.md` (169,771 B; sha `0555cafc…3e6e`) |
|---|---|
| `# BUILD — TIER-C11 · THE ENGINE BOUND TO EVENTS — …` + `> **DRAFT.**` banner + header bullets (contract+sha, drafted/executor/seed/branch/HEAD, AS-OF OF RECORD, Reading rule, SIZE — FLAGGED) | `# BUILD — TIER-C11-X · …` + `> **DRAFT — NOT YET THE REPORT OF RECORD.**` + header bullets (Lane, RATIFIED, Contract, Readings, Plan, Review, Substrate, Reading rule, SIZE) |
| `## 0 · VERDICTS` — 0.1 R5's chop table (printed first) · 0.2 The nine rows, exactly as `scores/S0_VERDICTS.md` §0 files them · 0.3 The feasibility verdict per lens · 0.4 The family · 0.5 The forward ledger, opened · 0.6 The verdicts in words | `## 0 · VERDICTS FIRST` — 0.1 The three rows, exactly as SCORED_X files them · 0.2 THE POOL · 0.3 DETECTOR AGREEMENT · 0.4 THE ERA QUESTION · 0.5 THE R2 LENS ROWS · 0.6 THE TC11-LANDING TABLE AT X-CLOSE |
| `## 1 · R0 and the build log` | `## 1 · X1 — THE EXIT FAMILY: THE GRID WHOLE` |
| `## 2 · STAGE R — ranges, done once` (lines 421-5294: the nesting grid whole) | `## 2 · X2 — THE SWING FAILURE AS A RANGE TRADE …` |
| `## 3 · STAGE W` · `## 4 · STAGE G` · `## 5 · STAGE T` · `## 6 · STAGE S` · `## 7 · STAGE A` · `## 8 · STAGE H` | `## 3 · X3 — THE VALUE-AREA DETECTOR` · `## 4 · X4 — THE ERA` · `## 5 · X5 — THE FORWARD LEDGER` · `## 6 · X6 — THE FERRY LAW` |
| `## 9 · FIXTURES — the transcripts of record` | `## 7 · THE FIXTURE ROLL — every transcript filed before this render` |
| `## 10 · FINDINGS — REPORTED, NOT FIXED (condensed, ranked)` | `## 8 · FINDINGS — REPORTED, NOT FIXED` |
| `## 11 · OPERATOR QUESTIONS STILL OPEN` (Q1..Q9 — the list TC12's rulings answer) | `## 9 · BOX-COST AND COMPUTE COST` |
| `## 12 · WHAT THIS BUILD IS NOT` | `## 10 · THE AMENDMENTS OF RECORD — AM-X1 … AM-X28, one line each` |
| `## 13 · THE LEDGER APPEND — verbatim, as staged` | `## 11 · THE LEDGER APPEND, AS STAGED (LX-C.4)` (inside a `~~~text` fence) |
| `## 14 · DISPOSITION · BOX-COST` — 14.1 Git · 14.2 The tick set now, and after both CLOSEs · 14.3 The compute ledger · 14.4 The CLOSE acts · 14.5 The file-disposition table (the document ENDS with it) | `## 12 · STATE PUSH AND THE CLOSE ACTS` (… 12.4 The draft's inputs) — last line `Operator: click Sync now.` (AM-X28) |

TC10's for reference: `## 0 VERDICTS · ## R0 WHAT THE INTERRUPTION LEFT · 1 STAGE B · 2 CENSUS-R · 3 STAGE D MANIFEST ·
4 FIXTURES · 5 FINDINGS · 6 OPERATOR QUESTIONS STILL OPEN · 7 WHAT THIS BUILD IS NOT · 8 DISPOSITION · BOX-COST`.

**The number-tracing pass — two mechanisms, one loose figure.**
- TC11: `T11/close/TRACES.json` (`schema tierc11.close.TRACES.v1`; keys `law, regions, traces, exemptions,
  r4_star_rows`; **231 traces**, 1 exemption ("9/12", a NAME)). A trace = `{key, lit, fmt, spec {kind: json|parquet|text|
  git|ast|filesha, path, sel}, value, uses {s0|append|s5|doc: n}}`. A number enters an output ONLY as (1) `T(key, spec,
  fmt)` resolved from its record, (2) a VERBATIM block behind `<!-- verbatim: <path>:<line spans> -->`, or (3) a
  «cite» with `|`/`+` quote lines (`tierc11_close.py:32-41`). **F-NUM** "FAILS IF a trace … does not re-derive from its
  record, a verbatim block differs from its source lines, a digit in §0 or in the append prose is neither a traced
  literal (used exactly its declared number of times), a verified block or cite, a masked token nor a counted
  exemption" (`tierc11_close_fixtures.py:11-14`).
- X: no TRACES file; the renderer copies cells and `F-DRAFT-NUMBERS` ("every cell of every marked table equals its
  source at the printed precision"; tables are marked `<!-- draft-table: <ID> -->`), `F-DRAFT-VERBATIM`,
  `F-DRAFT-ANCHORS` (39 typed prose facts each found in draft and source), `F-DRAFT-WORDS` (no verdict word outside §0
  and the fenced append: `VERDICT_RX` at `tc11x_close_draft_fixtures.py:55`), `F-DRAFT-FORM`, `F-DRAFT-ISO`, `F-DET`
  (`XO/close/FIXTURES_CLOSE_draft.txt`, "7 GREEN, 0 RED").
- **"5,353 tokens, 0 mismatches"** appears ONLY in the subject of commit `7b24f83`; no file under `XO/` carries it
  (`git grep '5,353' 7b24f83 -- research_outputs/tierc11x` is empty; `progress/X-CLOSE.json` does not hold it).

**S5 findings-not-fixed.** `T11/close/S5_FINDINGS_NOT_FIXED.json` (`schema tierc11.close.S5_FINDINGS_NOT_FIXED.v1`): keys
`schema, label, status_law, ranking_law, dedup_law, tier, as_of_of_record, contract{path,sha256,clause{line,text}},
built_by, counts, findings, superseded, inputs`. A finding: `id, class ∈ {HARVESTED, MEASURED, LEAN}, owner ∈ {operator,
executor}, owner_basis{path, field, quote, reading}, source{path, field, how, …}, status "REPORTED, NOT FIXED", text,
text_form, rank, also_reported_by, reviewer_class`. Counts: HARVESTED 54 · MEASURED 7 · LEAN 11 = **72** (36 operator /
36 executor); 3 superseded. Laws: status ("records what THIS build did"), ranking (operator-owned first), dedup (one
fact = one finding; other sources under `also_reported_by`). `inputs` = 35 paths with bytes+sha. X's
`XO/close/FINDINGS_NOT_FIXED.{json,md}` = the same schema forked, owner set extended with **ATHENA**, harvest keys
FIX/STAGE/REVIEW/XREVIEW/AMEND/BUS/OPS/LXC2/LAND, 65 findings (`tc11x_close_findings.py:2-46`; commit `7b24f83`).

**BOX-COST — what is measured.** CONVENTIONS §3.2 (`M/exchange/status/CONVENTIONS.md:341-343`): "The document ENDS with a
table covering every file the paste created, modified or moved", seven columns **PATH · EXISTS · TRACKED · COMMITTED ·
PUSHED · PROTECTED BY · BOX COST**; "Committed is not pushed. Pushed is not backed up." Rows (X's sets,
`tc11x_close_box_cost.py:19-33`): (a) every path in a commit whose SUBJECT starts with the tier prefix (`git log
--grep=^<prefix>( --name-only`, subject re-checked); (b) every PROGRESS `artifact_shas` path not in (a); (c) the PLANNED
report sized from the draft; (d) the PLANNED LEDGER_APOLLO append; (e) every `exchange/rows/**` file; (f) the frozen
snapshot ("n/a — outside repo"); (g) the close's own uncommitted files. Columns: EXISTS `os.lstat`; TRACKED `git
ls-files` (+ `check-ignore -v` names the ignore line; "force-added past" it); COMMITTED `git log -1 --format=%h`; PUSHED
`git branch -r --contains` (refs as last fetched, **no fetch**); PROTECTED BY "GitHub only" iff pushed and unmodified
else **NOT PROTECTED**; BOX COST = bytes · % of `BOX_BYTES` · FLAGGED when strictly over `FLAG_BYTES`, for box-bound
paths (under `exchange/` or `LEDGER.md`). Constants are read by `ast.literal_eval` — the modules are never imported
(F-BC-CONST): `BOX_BYTES = 16_000_000` (`M/scripts/publish_exchange.py:95`), `WARN_FRACTION = 0.40` (`:109`),
`REFUSE_FRACTION = 0.70` (`:110`, strict `>`), `FLAG_BYTES = 64_000` (`:160`), `SCOPE = "exchange/"` (`:48`),
`TICK_EXTRA = ("LEDGER.md",)` (`:128`), `SUBJECT = "exchange: auto-publish {date}"` (`:49`),
`OVERRIDE_ENV = "NAIAD_ALLOW_OVERSIZE_PUBLISH"` (`:111`). **COMPUTE COST** rides with it: per workflow `agents
(agentCount) · tokens (totalTokens) · tool calls · wall (durationMs)` from the harness journals
`~/.claude/projects/-Users-luis-Naiad/<session>/workflows/wf_*.json`, filtered on the exact workflow-name prefix
(`tc11x-`; TC11's were `tc11-scout, tc11-leans-review, tc11-data, tc11-foundation, tc11-stages, tc11-lanes-and-review,
tc11-final-repairs` — `T11/close/COMPUTE_LEDGER.json`), plus every COMPUTE note quoted verbatim from PROGRESS
(`XO/close/BOX_COST.md:395-458`). X's six journaled workflows: 63 agents, 24,607,467 tokens, 14.60 h wall (`:9-20`).

**LEDGER_APOLLO_APPEND.md format** (staged at `research_outputs/<tier>/LEDGER_APOLLO_APPEND.md`; destination
`exchange/status/LEDGER_APOLLO.md`, append-only, last block now `=== STATUS_APOLLO — 2026-08-22 — TIER-C9 …` at
`:2355`; file 2,426 lines / 174,090 B / sha `cd6ad43a0fe4890635e6d7098d29ae52d4af1268be4466740823701014222d2c`):
- `check_format(block)` at `M/scripts/tierc10_close_ledger_append_root.py:554-567`: opens with `SEP = "\n---\n\n"`
  (`:84`); body matches `=== STATUS_APOLLO — \d{4}-\d{2}-\d{2} — TIER-C\d+ · [^\n]+ ===\nLANE      [^\n]+\nCLASS     `;
  ends `\n=== END ===\n` with exactly one `=== END ===`; **`"Operator: click Sync now."` must NOT be inside the block**.
- cites: a line `«path:L1[-L2]»` or `«path#selector»`, then quote lines at indent+2 beginning `| ` (one per source
  line) or `+ ` (wrap continuation); `LA.render_quote(indent, q)` (`M/scripts/tierc10_close_close_ledger_append.py:626`),
  `parse_quotes(text)` `:978`, `verify_quote(q, src)` `:1012` (module import-safe on any env).
- every digit in the prose is traced, masked or a counted exemption; a number known only after the push is a
  `⟦STAMP AT CLOSE — …⟧` placeholder (TC11 `:189`: "replace this bracket with 'N tierc11 commits, M on a remote'").
- TC11's section labels (two-space indent): `THE FAMILY — ONE, AS FILED:` · `SAIL · STILL HELD.` · `VERDICTS, each
  under its own text …` · `RANGE TRADING — THE R2 LAW …` · `THE FORWARD LEDGER — OPENED, STANDING, UNSCORED:` · `THE
  PUSH FACT (git, read at draft time):` · `ALSO FILED` · `INTEGRITY` · `OPEN FOR THE OPERATOR (BUILD §11)` · `THE TIER
  LINE.` then the closing tier sentence ("ELEVEN TIERS. …  SAIL stays HELD; no card change is proposed.") and
  `=== END ===` (`T11/LEDGER_APOLLO_APPEND.md`, 253 lines, 16,732 B, sha `227317d1097c0f4e551ed90b717c09aa559a13006cb29e20c078a3e6d16414e1`).
  The tier line cites the previous tier's append by line (`«research_outputs/tierc10/LEDGER_APOLLO_APPEND.md:250-254»`).
- X's header: `=== STATUS_APOLLO — 2026-09-25 — TIER-C11 · TC11-X — THE EXIT, … ===` (`XO/LEDGER_APOLLO_APPEND.md:4`;
  260 lines, 16,154 B, sha `c63f7a18e2c4540f8ef8eddb178918252a7a6a50f43317b0a051ae41364db9e3`; two pending stamps `:132`, `:220`).

**close_acts.sh — three scripts, all PENDING, strictly ordered TC10 → TC11 → X.**
Evidence that none has run: no `BUILD_2026-09-21_TIERC10…` / `BUILD_2026-09-24_TIERC11…` in `M/exchange/reports/`; the
ledger's last block is TIER-C9; both stamps still pending (`M/research_outputs/tierc10/LEDGER_APOLLO_APPEND.md:213`,
`T11/LEDGER_APOLLO_APPEND.md:189`).

| script | sha256 | steps | step-0 refusals |
|---|---|---|---|
| `M/research_outputs/tierc10/close/close_acts.sh` (120 lines) | `3f5c868ba089965ae3dad120c9293b9375dde992df5043dcfecea2b02e4440f8` | 0 pre · 1 push · 2 LAW 5 move+push · 3 builder's report moves · 4 stamp + F-LAR · 5 `cat >>` ledger · 6 commit residue (**`:103` `git add "$APP" "$LAR"` — no `-f`; fails on `.gitignore:263`: FN-M-TC10-ACTS-IGNORED**) · 7 publish() · 8 bright paths | branch; **index clean** (`:43`); files present; destinations absent; stamp pending |
| `T11/close/close_acts.sh` (140 lines) | `7f601f8106f61fa857f79a0c95cea3edf74fe28cf34653ca5d4c7e931b78e2ba` | 0 pre · 1 push · 2 LAW 5 (`cp`, sha equal, `git rm` draft, commit, push) · 3 stamp + `F-LAR11 --stamped` · 4 `cat "$APP" >> "$LEDGER"` · 5 commit residue · 6 publish() (push result STATED) · 7 bright paths + `Operator: click Sync now.` | `:48` branch; `:49-53` TC10's report tracked AND a `TIER-C10 · ` block committed on the ledger; `:54` **index clean**; `:55-59` every SOURCES file present, tracked and **== HEAD** (14 files, `:41`); `:60` DOC absent; `:61` no `TIER-C11 · ` block yet; `:62` stamp pending; `:64` **F-LAR11 re-run on the pre-stamp append "as the sources stand now"**; `--check` runs step 0 only |
| `XO/close/close_acts.sh` (331 lines; run FROM THE MAIN TREE) | `02191457023d062a757f42d980f6b0ecc31ce127be8b3606e50b7e642d4d1940` | 0 pre · 1 the ferry of record in the X worktree (`tc11x_ferry.py --stage=X-CLOSE --pin-merge-target`, `--fresh`, F-ROWS; commit on `tierc11x`; `ferry_restore` undo `:77`) · 2 `git merge --no-ff tierc11x` (`:256`) · 3 `git push origin v12-v1-census` · 4 LAW 5 · 5 stamps + `F-LEDGER-FMT --stamped` · 6 `cat >>` + tail-bytes check · 7 `git add -f` residue (`:307`) · 8 publish() · 9 bright paths + final line (`:331`) | main on `v12-v1-census`, **clean index**; `CERTIFIED_TIP` present, one 40-hex sha; **`refs/heads/tierc11x` == CERT** (`:136`); X worktree HEAD == CERT, on branch, **clean except `?? …/close/CERTIFIED_TIP`** (`:140-141`); **TC10's then TC11's blocks landed BY BYTES** (each tier's committed append occurs once in the committed ledger, TC10's offset < TC11's; ledger == HEAD; X's header absent) `:142-180`; **merge path allow-list** (`allow_list` `:108-121`: `research_outputs/tierc11x/*`, the X contract, `exchange/rows/tierc11/*`, `exchange/rows/tierc11x/*`, `scripts/tc11x_*.py`; anything under `research_outputs/tierc11/` refused); `:184` report destination absent; **`:185` `research_outputs/tierc11x` must NOT exist in the main tree**; draft has no `<<…>>` placeholder; stamps pending; `:192` `F-LEDGER-FMT --check` |

What TC11's pending append cites (so these bytes are load-bearing until the operator runs it): the TC11 contract by
line **12 times** (e.g. `:9`, `:40-42`, `:99`), `T11/forward/FORWARD_LEDGER.md` lines `:5`, `:7`, `:38`,
`T11/stage_r/STAGE_R.md`, `T11/books/FIXTURES_BOOKS.txt`, `scores/SCORES.json#rows[…].verdict_cell` ×9,
`scores/FAMILY.json#law`, `research_outputs/tierc10/LEDGER_APOLLO_APPEND.md:250-254`, the TC10 contract `:2-3`
(grep of `«…»` in `T11/LEDGER_APOLLO_APPEND.md`).
What X's step 1 asserts about the MAIN tree: it lists `research_outputs/tierc11` and "asserts every TC11-FILE row's sha
equals the sha TC11's PROGRESS certifies now" over **every tabular file (`.parquet`, `.csv`, `.jsonl`) outside
`_det_*`** (`X/scripts/tc11x_ferry.py:62-74`, `TABULAR` `:212`, `tc11_plan` `:1497-1514`); exit 3 = HALTED ELEMENTS,
exit 1 = HALT → `die` (`close_acts.sh:201-202`).

### 1.9 Commit conventions and .gitignore

- Subjects: `tierc11(<STAGE>): <sentence>` — on disk: `STEP Q, TC11-REG, TC11-D, FOUNDATION, AM-7, STAGES, SCORE,
  LANES, FIX, CLOSE` (`git log --grep='^tierc11'`: 10 commits). X: `tc11x(<STAGE>): …` — `STEP Q, X-UNDERSTAND,
  X-VENDOR, X-LEANS, X-D, X-REG, X-FOUND, X1, X4, X5, X2, X-SCORE, X3, X6, X-FIX input, X-FIX, X-REVIEW, X-CLOSE`
  (18 commits). TC12's first: `tierc12(STEP Q): contract filed verbatim — <path> sha256 <64hex>` (28e006b).
- The prefix is machine-read: TC10's stamp counts subjects starting `tierc10`; TC11's stamp counts
  `startswith("tierc11(")` (`T11/close/close_acts.sh:97-98`); X's BOX-COST greps `^tc11x(`. `tierc12(` matches none.
- Body: plain prose with results/counts/shas, what was NOT done. Trailer `Co-Authored-By: Claude Opus 5.5 (1M context)
  <noreply@anthropic.com>` (e.g. `git show -s d307829`).
- Root `M/.gitignore`: 288 lines, sha `fd786bf96f7f78dce6440620a6ef37bb4843fd518417e3ab0bdfd4e3a0e25bd9` (identical
  in X). `:19-20` `__pycache__/`, `*.pyc`; `:44-45` `!research_outputs/**/build_manifest.json`, `!…/manifest.json`;
  **`:263-264` `research_outputs/tierc10/**`, `tierc10_run2/**`** (whole tree ignored → TC10 documents were
  force-added: 59 tracked files); **`:287-288` `research_outputs/tierc11/**/*.parquet`, `research_outputs/tierc11/**/_det_*/`**
  (TC11: 182 tracked, 178 ignored paths), appended at the END "so that line numbers other lanes cite (TC10 cites :263)
  stay put" (`:284-286`). **X never edited the root file**: nested `XO/.gitignore` = `*.parquet`, `_det_*/` (4 lines).
- `git check-ignore` probes [measured here]: `research_outputs/tierc12/x.parquet` → NOT ignored;
  `research_outputs/tierc12/_det_x/a.txt` → NOT ignored; `research_outputs/tierc12/va/build_manifest.json` → matched by
  the negation `:44`; `exchange/rows/tierc12/a.csv`, `analytics/value_area.py`, `scripts/tierc12_va.py` → NOT ignored.
- **How untracked artifacts are pinned** (X's va parquets: `git -C X ls-files research_outputs/tierc11x/va` lists only
  `FIXTURES_X3.txt, X3.md, build_manifest.json`): (1) the stage's progress record `artifact_shas {bytes, sha256}` =
  FILE bytes (e.g. `va_series_4h.parquet` 10,771,152 B `d5881508a02475eb46c180b757e1948466313cb1673d2a909ea9ab5bda25891c`
  — re-hashed equal on disk now); (2) the tracked per-directory `build_manifest.json` `sha` map = CONTENT sha
  (`va/build_manifest.json` sha `769ac0915ee35b8783d99e0d39870f9e164871b81b94b6bb3533204fa28f078b`, equal to X3's
  record) + `parquet_content_sha` in the progress record. The bytes themselves exist ONLY in that worktree's working
  directory ("protected_by: NOT PROTECTED — gitignored parquet", `XO/LEANS_X.md:2214`).

### 1.10 Compute etiquette and runtimes

- The cap of record (X's LX-0.9, `XO/LEANS_X.md:526-539`): "X jobs use at most 6 worker processes while
  `os.getloadavg()[0] < 10`, else 2. TC11 has priority." Every worker is a `spawn` process that imports the env shim
  before any I/O; **results merged in a fixed key order before any write**; worker count and load average recorded
  ONLY in PROGRESS and BOX_COST, never in an artifact (F-DET treats them as clock fields).
- **Nest picks** (`M/scripts/tierc11_nest.py --build-picks [--procs=N]`, `mp.get_context("fork").Pool` `:623`, default
  1): serial dry run **71.6 s**; as filed on a 10-process fork pool **123.2 s — slower than serial**
  (`FOUNDATION_REVIEW_2026-09-25.json` `.modules[1].built`). BTC 5m calibration, one tape, 11 scales: 4.0 s.
- **VA series (X3, 4 lenses × 5 assets, 1h included)**: build of record 4 spawn workers, load 6.02 at launch, **6m07s
  wall, cpu_user 1,050.9 s**; a first build at load 15.06 ran 1 worker, **14m33s**; fixture roll 746 s (refile) / 716 s
  (re-run) / 988.9 s at the X-FIX roll (`XO/progress/X3.json` `compute`; `X-FIX.json suites[7]`). Output sizes:
  `va_series_1h.parquet` 36,748,745 B, `4h` 10,771,152, `12h` 3,747,949, `1d` 2,025,996, `events_va` 20,751,566.
- **Scorer bootstrap**: `T5.cluster_boot(values, clusters, seed=SEED, n_boot=4000)` (`M/scripts/tierc5.py:1178`) "at
  4,000 draws takes 0.024-0.031 s, so bootstraps are negligible" (`XO/LEANS_X.md:538-539`); X scorer build 1.9 s,
  fixture roll ~16 s; TC11 scorer run 22 s, SCORE-BUILD suite 127 s.
- Other builds: X2 rebuild 92 s (suite 350–418 s); X4 build ~60 s (suite 300–360 s); X1 build ~10 s (suite ~94 s);
  X ferry ~23–27 s (`XO/close/BOX_COST.md:440-452`).
- Env for every command: `export NAIAD_CACHE_DIR=<snapshot> PYTHONDONTWRITEBYTECODE=1` BEFORE python starts, and
  `~/venvs/naiad/bin/python -B` (TC11's close guard HALTs unless `PYTHONDONTWRITEBYTECODE == "1"`,
  `tierc11_close.py:78`).

### 1.11 The shared main tree — schedules and lanes

| job | when (local −03:00) | what it does to the tree | source |
|---|---|---|---|
| `com.naiad.daily` → `scripts/daily_routine.py` | **07:00 daily** (last run 2026-10-08T10:08:15Z) | rewrites `exchange/status/daily/DAILY_<date>.md`, `MANIFEST*.json`, `HEARTBEAT.md`; moves old dailies to `research_outputs/_daily_archive`; refreshes `MAILBOX/`; then **`publish_exchange.publish(ROOT, today)`** (`daily_routine.py:1489`) | `~/Library/LaunchAgents/com.naiad.daily.plist`; `M/exchange/status/HEARTBEAT.md` |
| `com.naiad.estate` / `com.naiad.workflow` → `backup_estate.py --estate` / `--workflow` | **Sunday 08:00 / 08:30** (next 2026-10-11) | read-only archives (`--workflow` zips `scripts`, `exchange`, repo-root `*.md` …); publish() as final step (auto-publish commits seen 2026-10-04 08:33 and 11:52) | plists; `backup_estate.py:1-32` |
| five `com.naiad.oracle-*` agents | 06:45 / 07:00 / 15:45 / 16:00 / catch-up | **SUSPENDED since 2026-09-21** (booted out and `launchctl disable`d; plists retained); replaced by the on-demand `/oracle` skill | `M/research_outputs/oracle/SCHEDULE_SUSPENDED` |

- **`publish()`** (`M/scripts/publish_exchange.py:565`): `git add -- exchange` (stages EVERY change under exchange/,
  untracked included) → reads the index back; **if any staged path is outside `exchange/`: `git reset` (mixed), FLAGGED,
  no push** → budget (WARN prints; REFUSE strictly > 70% resets) → `git commit -m "exchange: auto-publish <date>"` →
  **`git push origin <branch>` — the whole branch**. Proof it pushes tier commits: TC11's own append,
  `T11/LEDGER_APOLLO_APPEND.md:180-184`: "The operator's daily publish 4ae8c81 … pushed the branch … 8 of the 9 tierc11
  commits are on origin". CONVENTIONS §3.4 (`CONVENTIONS.md:411-417`): "Do NOT `git add` or `git commit` exchange files
  separately — let the guard do it".
- **The oracle / ARGUS lane** (commits `or1:` / `or2:`, last `11bec23`): `scripts/oracle_{daily,fixtures,
  ondemand_fixtures,roster_backfill,topup,wrapper}.py`, `scripts/rangefinder_core{,_fixtures}.py`,
  `research_outputs/oracle/**`, `exchange/queue/*ARGUS.md`, `exchange/reports/NOTE_ARGUS…`, `.gitignore` (appended
  lines), `.claude/skills/oracle/SKILL.md` (`git log --grep='^or[12]:' --name-only`); at run time also the LIVE cache
  `~/.cache/naiad/data_cache/klines` (mtime Sep 23 14:50), `logs/launchd/oracle-ondemand.log`, `ORACLE_DOWN.flag`
  (`oracle_wrapper.py:122-130,480`), `briefs/`. Idle since 2026-09-23 but can be invoked any time.
- Other writers into the tree: the MACROREPORT skill → `M/MAILBOX/` (gitignored `:262`); a pine lane (untracked
  `pine/*.pine`).

### 1.12 The box, now and after the pending closes

- Now [measured here]: tracked `exchange/` files on disk 116 → 2,642,845 B; + `LEDGER.md` 259,298 B = **tick set
  2,902,143 B = 18.14%** of 16,000,000; headroom to WARN (6,400,000) 3,497,857 B. (The daily's own figure, a different
  basis: "Bus carrying 2,670,074 B in 118 file(s) (worktree, including anything not yet committed)" = 16.69%,
  `DAILY_2026-10-08.md:72,82`.) Rotation candidates: 58 files, 1,490,026 B (`:104`).
- Pending adds: TC10's close 161,600 B; TC11's 904,220 B (= 887,648 + 16,572); X's report reserved 178,216 B + append
  16,154 B; swept exchange edits 3,293 B (`XO/BUILD_DRAFT.md:940`).
- **X's forecast at its pin** (main `6f349395545a`, tick 2,883,248 B): 19 WRITTEN, 80 HELD FOR ATHENA, box after ferry
  5,134,272 B; with the reservation 6,397,755 B — **2,244 B below WARN** (`XO/BUILD_DRAFT.md:939-944`). The first-fit
  fills the box up to WARN by design; "the ferry of record re-decides the holds on the box as it stands at close_acts
  step 1" (`:947`). Today's tick is already 18,895 B above that pin's [2,902,143 − 2,883,248], more than the slack.
- X's bus as committed at X-FIX: `exchange/rows/tierc11x/` 6 CSV + manifest (largest `sfp__X2_trades_1h.csv`
  1,999,149 B), `exchange/rows/tierc11/` 7 CSV + manifest (`ls X/exchange/rows/*`).
- Ferry law details TC12 inherits by reference (`XO/LEANS_X.md:2184-2262`): path `exchange/rows/<tier>/<source path
  relative to research_outputs/<tier>/, extension dropped, '/' as '__'>.csv`; serializer `pandas.to_csv(index=False,
  lineterminator="\n", encoding="utf-8")`; cap 2,000,000 B on the CSV, whole rows only; pointer in
  `ferry/FERRY_MANIFEST.json` rendered as `exchange/rows/<tier>/ROWS_MANIFEST.md`; a file that would cross WARN is NOT
  written and is listed "HELD FOR ATHENA"; `REFUSE` never overridden; files projected in a fixed order; "Written only
  in the worktree. Never in the main tree's `exchange/`, which the 07:00 routine would sweep" (`:2195-2196`).

### 1.13 The stale worktrees (report only — nothing removed)

`git worktree list --porcelain` registers **28** (not 30) under `M/.claude/worktrees/wf_8995cf0d-ab5-N`: N = 1..30
**without 14 and 21**. Each is on its own branch `worktree-wf_8995cf0d-ab5-N`; every branch tip and HEAD =
`a6da1b97e95ce9475290083ec1639cfb93c84d11` ("Add files via upload", 2026-07-09 21:04:36 −0300). **None is clean**: all
status entries are `??` (3,698 untracked entries in total, 0 tracked modifications). `--no-optional-locks status
--porcelain=v1 --untracked-files=all` line counts [measured here]:

| N | lines | N | lines | N | lines | N | lines |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 244 | 8 | 12 | 16 | 8 | 24 | 4 |
| 2 | 238 | 9 | 219 | 17 | 223 | 25 | 4 |
| 3 | 278 | 10 | 146 | 18 | 4 | 26 | 214 |
| 4 | 214 | 11 | 171 | 19 | 2 | 27 | 162 |
| 5 | 204 | 12 | 195 | 20 | 5 | 28 | 1 |
| 6 | 5 | 13 | 322 (has a `mirror/` symlink loop) | 22 | 274 | 29 | 4 |
| 7 | 207 | 15 | 160 | 23 | 1 | 30 | 177 |

Plus one more at the same commit: `M/MAILBOX/.claude/worktrees/adoring-franklin-efc306` (branch
`claude/adoring-franklin-efc306`). TC10 already recorded that these reach none of the tier's commits
(`H_fixture_conventions.md:304`).

### 1.14 Records TC12 will pin for this unit (sha256, re-hashed here)

| path | sha256 |
|---|---|
| `M/exchange/queue/2026-10-08_TC12_APOLLO.md` | `861d6050e80e66995e4f9db2855aaf274d63285249c2549e5a0813582095a7bd` |
| `M/exchange/queue/2026-09-24_TC11_APOLLO.md` | `bb38e016a8f3e55ca3bcc09fec53ba6b8dc40accb60d054f8163d033a898f835` |
| `X/exchange/queue/2026-09-25_TC11X_APOLLO.md` | `40e0c4b716b978ab913e3900db01502b0113b93ece16afa60a8079d7d0203c3d` |
| `T11/PROGRESS.json` | `dbcc08cf60a9dbb5827c65f3728857fcab12df50aeefee7667ba3dbfc205c4fe` |
| `XO/PROGRESS.json` | `4c91b2efef002e7347f125bc9bcb1450f7eb35a7888814a4b7d8c67fe9b39475` |
| `M/research_outputs/tierc10/PROGRESS.json` | `e0abf4cacc869c8b7282bcd52e0e7bba36d7f75e068774d8674696bbcf72b549` |
| `T11/LEANS.md` / `LEANS_AMENDMENTS.md` | `655e1605…294f` / `85f57ce7…0c07` (full values in 1.3) |
| `XO/LEANS_X.md` / `LEANS_X_AMENDMENTS.md` / `REGISTRATION_PLAN.md` | `74a989ee…8623` / `af845b95…d059` / `a887ea64a5099b8b27b5433d263969911ea7795c0fade2af9b40a5b92b8c3d15` |
| `T11/scores/REGISTRY_CHECK.json` / `scores/FAMILY.json` | `aea83bf10b5bbe62ff6c0af542870cd60f5ad8773b6bb61fab45ea465d8f8ed0` / `3fa36bd482eac4de729b0e1ff2a66e7becbc30f2646ce16fc0df8fc369b2fd73` |
| `XO/registrations/REGISTRY_PIN_X.json` / `REGISTRATIONS_X.json` | `6a445afe147f8e36eceeb03cc1b41c906b0c8102b0f36d2a4a32af6b42b72e73` / `6b0eb52d63ce6823c35f27010705e04263b21e7bfc1603f241c9a7b4b7deb0a4` |
| `T11/BUILD_DRAFT.md` / `XO/BUILD_DRAFT.md` / TC10 `BUILD_DRAFT.md` | `e2cc364860d5a11393d0a064bc1637cf5c07e14aaddc857fe30e78b915354233` / `0555cafc1129cdda6c12f39885e1e84fd8e567d7dbcf179452e0b08d84a43e6e` / `244ad5a46a4f73c522361990638499206c9ef3c341d436e2aa67bdd898791149` |
| the three staged appends (TC10 / TC11 / X) | `1288b59bae687f6a56f31cd75d958dc53400af78f4c7ff77ede3965972d5021e` / `227317d1…14e1` / `c63f7a18…b9e3` |
| `T11/forward/FORWARD_LEDGER.jsonl` (2 lines, chain head `0db88942…`) | `e53328add9e71f1c6198f724a131565a2a10ad2ad1600c36a74c6676f7ada288` |
| `XO/forward/FORWARD_LEDGER.jsonl` (4 lines) | `4a6da7e89a3cf5f0127f76aca0d2ae12d218ffc06417c6528c70210092cfa4c5` |
| `M/scripts/tierc10_panel.py` / `tierc11_env.py` / `publish_exchange.py` | `40b660cdc943a947f199f2e59f38bfbda04866b44191506de2298d8474d79b0e` / `1526093b25161927337ced6112a310075b1a57c825f08705814e48619398f798` / `15eec3d0bf0420200d94fc3087e4868a59eecb5cdb1fc21e01b8c80daae8a65b` |
| `M/exchange/status/CONVENTIONS.md` | `42b2cdd6ae4fa5cd85548c133862ac25ddad9c7dd3910b63555a5b628f8a226e` |
| `XO/va/*.parquet` file shas | `va_series_1h 860b895448dec9e3d53c10a3bf5233f3e94610a4cb983efe02d676ee64a1af7e` · `4h d5881508…891c` · `12h c2ce9a8f131fac79de5a3890d67aa626fbf1f9d6bf0a27cb4e4fce0014c40359` · `1d 1fc7bc75033c4d57a39e3bdae0de4d8bb590e7752894bb0ad329398e106ae1a7` · `events_va 2c35b15162a1dfa96fa09074688650dd313fd9245836ccb301cfa2eb3aa35848` · `feasibility ea8573b3240bb1112521c55f0a52ee2ed7156c598b7665685d0b86eefbecb6f0` · `two_trades a03ef1343cc93c9bc093c4f34960978daac51ca24d5160480546d40bf76f91b0` · `agreement 7984fb78f9393df19eaeaaee0291edf54a4cf6e3e6859c1e0725b753d8b2e41a` (`XO/progress/X3.json artifact_shas`) |

---------------------------------------------------------------------------------------------------------------
## 2 · CONTRACT-vs-DISK

C1. **"resume law (R0 census · verify-or-quarantine · … · commit + PROGRESS.json per stage)"** (:5-6). The disk carries
the law as TC10's text and two different ledger practices: TC11's hand-edited PROGRESS with `r0_census` /
`resume_point`, and X's merged PROGRESS without them. No reusable R0 driver and no resume fixture exist outside
`tierc10_resume_fixtures.py` (TC10-literal). TC12's R0 is a fresh-tier census (STEP Q `28e006b`, nothing to
quarantine) that must still record three unfinished predecessors.

C2. **"read-only review worktrees"** (:6) / **"worktree attestation"** (:124). Two procedures on disk that check
different things (1.6): TC11's stages the ignored parquet and holds it to the reviewed commit's PROGRESS record; X's
checks detached + porcelain + an ignored-listing sha. The contract names neither. Neither covers reads of X's records
or of a new snapshot.

C3. **"analytics/value_area.py; decision modules import NOTHING from it — import-closure extends to it"** (:25-26).
(a) the file does not exist; (b) `tests/test_analytics.py` scans every `analytics/*.py` (no engine import, no I/O
tokens); (c) `analytics._MODULES` membership moves `analytics_sha()` `ea5f02f2…`; (d) "decision modules" is defined
only per tier (TC11: glob minus typed runners; X: five typed modules) — there is no `tierc12` set yet; (e) three of
the five registrations (P-DIR-1, P-SFP-VA-1, P-SCALP-3) DECIDE on VA state, so the state must reach decision code as
data, not by import (the TC10 "CAPTURED, NOT CONSULTED" / TC11 `range_facts` adapter precedent, `tierc11_nest.py:54`, `:1533`).

C4. **"V1 Source of record = TC11-X's filed implementation (research_outputs/tierc11x/va/, scripts, shas printed)"**
(:27). From the main tree that relative path does not exist: X is UNMERGED; the path resolves only at
`X/research_outputs/tierc11x/va/`; its parquet are untracked (exist on that worktree's disk only); `scripts/tc11x_*.py`
are not in main. And X's close refuses if `research_outputs/tierc11x` exists in main (`close_acts.sh:185`).

C5. **"Q1/Q2 keep SCORES.json leaves; stamp TC11 BUILT and re-pin its registry files ["tc11-stamp"]"** (:13). Q2's own
text names three files ("re-pin REGISTRATIONS.json, REGISTRY_CHECK.json and PROGRESS.json", `T11/BUILD_DRAFT.md:5989`).
The disk: the contract sha `bb38e016…` is carried by **23 tracked main-tree files** (`git grep -l bb38e016a8f3 --
research_outputs/tierc11 scripts exchange analytics`: incl. write-once pins `data/AS_OF_PIN.json`,
`ranges/SCALE_PICKS.json`, `data/STAGE_D_MANIFEST.json`; the frozen `LEANS.md`; five `scripts/tierc11_*.py`; the close
SOURCES `BUILD_DRAFT.md`, `TRACES.json`, `S5_*`, `FIXTURES_CLOSE.txt`) and **7 files on the frozen X branch** (incl.
`data/tc11_rec/**` copies and `REGISTRATIONS_X.json`). TC11's generator HALTs on a stamped contract: "the TC11
contract already carries a BUILT line" (`tierc11_close.py:961-962`) and on any contract-sha ≠ PROGRESS / REGISTRATIONS
pin (`:608-612`). The queue convention is "`BUILT: <artifact or commit>` on a line of its own" (`exchange/queue/README.md`
item 6) — and the artifact (TC11's report) is not in `exchange/reports/` yet. TC11's own finding FN-M-QUEUE-STAMP
says the same (`tierc11_close.py:950-955`).

C6. **"Q6 the close acts remain the operator's keystrokes"** (:14-15). Three scripts are pending and chained
(1.8). TC10's has a known defect at `:103`. TC12's close cannot land before all three, and its step 0 has to prove it.

C7. **"FERRY: every per-trade and per-asset row file → exchange/rows/tierc12/ as CSV, 2 MB cap; files that would push
the box past WARN are held and LISTED for ATHENA"** (:111-112). `exchange/rows/` does not exist in main; the ferry code
(`tc11x_ferry.py`, 165,341 B) exists only in X; anything written under `M/exchange/` before close is swept and pushed
by the 07:00 routine; after X's close the box is forecast 2,244 B below WARN, so by this sentence nearly every TC12
row file will be HELD.

C8. **"F-LEDGER (append-only on the three existing books; the fourth re-hashes)"** (:122) and Stage L "all four books …
re-ridden … (first appended rows)" (:108-110). The three books live in TWO chains with DIFFERENT schemas: TC11's
(GENESIS/REFRESH lines, `line_sha256`/`prev`; v6 and 9/12, both `n_appended_total 0`) and X's (`book_open` lines,
`entry_sha256`/`prev_sha256`; `v6` and `trg912` as "X twin", `gated-v6-oldtide` "of record"). Both files are frozen
inputs of pending close acts (TC11's append cites `FORWARD_LEDGER.md:5,7,38`; X's ferry asserts every TC11 tabular
sha incl. `forward/FORWARD_LEDGER.jsonl`).

C9. **"CLOSE: exchange/reports/BUILD_2026-10-08_TIERC12_VALUE_AREA.md — §0 VERDICTS FIRST: … the VA stack whole …"**
(:126-129). "Whole" on disk has cost 887,648 B once (TC11's nesting grid inside the document) and the document is
box-bound; X held its report to 169,771 B by pointing to parquet. The contract also lists no fixtures-roll, amendments
or operator-questions section, which both predecessors carry.

C10. **"publish_exchange; STATE push; bright paths; final line"** (:130-131). On disk the executor has never pushed,
published or merged: every tier hands a `close_acts.sh` to the operator; "STATE push" = the push result stated on
screen; the final line is printed by the script and is the document's last line, and is forbidden inside the append
(`check_format`).

C11. **"LEDGER_APOLLO append (the "maker" ruling verbatim; SAIL HELD; families declared; in-sample labels carried)"**
(:129-130). The header regex requires `TIER-C\d+ · ` — `TIER-C12 · ` passes. The tier line must cite the previous
tier's block; two blocks precede (TC11's, then X's "TIER-C11 · TC11-X"), neither landed.

C12. **"FIXTURES … import-closure · worktree attestation"** and **"F-DET hash-identical"** (:123-124): no sweep driver
exists to re-run the suites; TC11 and X both did it by hand-run gates. **"every grid printed WHOLE"**: helper exists
(`TP.grid_whole`). **"every fixture leg states its failure condition"**: harness exists (1.4).

C13. **"`data/fee_schedule.json` must carry maker_bps_side per venue"** (:21-23) [cross-unit, frozen-record angle only]:
there is no repo-root `data/`. The files are `M/research_outputs/tierc10/data/fee_schedule.json` (`3a18b84e…`) and
`T11/data/fee_schedule.json` (`6febe170…`, certified by TC11-D; "adds maker 2.0 bps (ASSUMPTION)" per its PROGRESS
one_line). TC11's file is a certified TC11 artifact — a TC12 edit in place would break TC11's record and X's ferry
assertion.

C14. **V3 "HALT if the mirror disagrees on any word"** [cross-unit, noted because the comparator is a fixture]: X's
filed words (`XO/va/build_manifest.json` `va_lens_verdicts`) are `4h: "PASS"`, `1d: "PASS"`, `12h: "FAIL"` and
`1h: "FAIL — maker twin PASSES (the reopening path; needs a toll-model change the operator rules)"` with
`maker_twin: "PASS"`. The 1h "word" is a sentence; X pins L only for {1h 71, 4h 66, 12h 53, 1d 35} — no 1w.

---------------------------------------------------------------------------------------------------------------
## 3 · READINGS NEEDED (candidate leans, each to freeze BEFORE building)

**U9-1 · WHERE TC12 IS BUILT.** Options: (a) the main tree on `v12-v1-census` (TC11's way; STEP Q is already there);
(b) a dedicated worktree + branch (X's way: immune to the 07:00 sweep, bus CSVs committable, but a second operator
merge and allow-list, and it still cannot import X). **Recommend (a)** with U9-6 and U9-9 as its conditions: nothing
under `exchange/` before close, index never left staged. State the cost plainly in LEANS: the daily routine will push
`tierc12(` commits whenever SSH works again (as it did TC11's) — "no push without the operator's word" cannot be
enforced in the main tree and is filed as a finding, not hidden.

**U9-2 · NAMES.** Scripts `scripts/tierc12_*.py`; outputs `research_outputs/tierc12/`; commit subjects
`tierc12(<STAGE>): …`; PROGRESS stages `STEP Q, TC12-UNDERSTAND, TC12-LEANS, TC12-REG, TC12-D, TC12-V, TC12-C, TC12-G,
TC12-R, TC12-S, TC12-L, TC12-SCORE, TC12-FIX, TC12-REVIEW, TC12-CLOSE`; workflow names `tc12-…` (the compute ledger
filters on the exact prefix); review worktrees `tc12-review-<lens>`. Never a `tierc10_`, `tierc11_` or `tc11x_` name
(each is swept by a foreign fixture or collides with X's merge). Recommend as stated — it reuses L-0.4 / LX-0.5.

**U9-3 · PROGRESS MAINTENANCE.** Options: hand-edited (TC11) or builder records merged by a pure script (X).
**Recommend X's**: `research_outputs/tierc12/progress/<STAGE>.json` written by builders, `scripts/tierc12_progress.py`
(fork of the 86-line `tc11x_progress.py`) merges — but keep TC11's header keys the contract's law needs (`identity`,
`head_at_r0`, `r0_census`, `r0_census_utc`, `resume_point`, `live_cache_touched`, `last_sweep_utc`). Statuses
restricted to COMPLETE-VERIFIED / PARTIAL / ABSENT (X's fourth word "COMPLETE" is not in the law; "built, awaiting
verification" = PARTIAL with a blocker). Fixture records appended, never inserted.

**U9-4 · R0 CENSUS CONTENT (fresh tier).** Recommend recording, read from files: `head_at_r0 = 28e006b…`; "no tierc12
artifact existed before STEP Q"; predecessors — TC10 CLOSE PARTIAL, TC11 has no CLOSE stage (resume_point TC11-CLOSE),
X-CLOSE awaiting the operator, tierc11x unmerged at `7b24f835`; the main tree's pre-existing dirty paths by name; the
pins of 1.14. Rival: a one-line census (loses the tier-order evidence the close needs).

**U9-5 · LEANS: FORMAT, REVIEW, FREEZE.** Recommend `research_outputs/tierc12/LEANS.md` in TC11's reading format, code
printing `[LEAN-HEPHAESTUS] L-…`; a five-lens review (FIDELITY · CAUSALITY · STATISTICS · BUILDABILITY · TRADING) plus
X's completeness-critic second pass; review record `review/LEANS_REVIEW_2026-10-08.json` carrying drafted/revised
shas and counts; **commit the drafts first (`tierc12(TC12-LEANS-DRAFT)`) and review that sha in detached worktrees**,
which closes the gap X had to paper over with a hash-bound attestation; freeze = the commit that files
`REGISTRATIONS.json` pinning the contract, LEANS and review shas, before any book; thereafter never edited —
`LEANS_AMENDMENTS.md` (AM-n, dated, reason, what was redone; never on an outcome), builders proposing in
`AMENDMENTS_PROPOSED.md`. Rival: review untracked drafts (X's path).

**U9-6 · NOTHING UNDER `exchange/` BEFORE CLOSE (the ferry included).** Options: (a) write CSVs to
`exchange/rows/tierc12/` during the build; (b) stage them off-bus (`research_outputs/tierc12/ferry/bus/…`) with
manifests and a box FORECAST, and make the ferry of record a CLOSE ACT that re-measures the box and copies sha-equal
(X's AM-X21, plus LAW 5's "a draft under exchange/ is not a draft"). **Recommend (b).** (a) publishes evidence at the
next 07:00 run and eats the headroom X's ferry of record is about to measure.

**U9-7 · THE FERRY'S BOX RULE AT ≈ZERO HEADROOM.** The contract's WARN sentence + X's forecast imply most TC12 rows are
HELD. Options: literal (hold and list everything that would cross WARN, in a fixed priority order — the five
registered books first); or ask ATHENA before the build. **Recommend literal**, with the priority order typed in LEANS
before any book exists and the forecast printed, so the held set is not chosen after a result is seen.

**U9-8 · "tc11-stamp": WHEN AND HOW.** Options: (a) stamp and re-pin during the build; (b) enact it as a NAMED STEP OF
TC12's close_acts.sh, after TC10's, TC11's and X's blocks have landed: append the `BUILT:` line as the LAST line of the
TC11 contract (every `:line` cite stays valid), re-pin exactly the files Q2 names in one dated commit, file an
old→new sha map and the list of files that keep the old sha as history under `research_outputs/tierc12/`; (c) sibling
file only. **Recommend (b)** — it enacts the ruling, keeps Q6 intact, and until then TC12 reads TC11 at its filed pins
(`bb38e016…`, `dbcc08cf…`). (a) risks stopping the operator's TC11 and X close acts at step 0/1. Flag for the
operator: X's frozen records will name the old sha permanently.

**U9-9 · STAGING AND COMMIT DISCIPLINE IN A SHARED TREE.** Recommend: stage by explicit pathspec only (never `-A`/`-a`),
stage-and-commit in one step, never leave the index staged, no commit between 06:55 and 07:20 local (and Sunday
08:00–08:40); never touch the two pre-existing modified files or the untracked pine/html files. Rival: none worth
keeping.

**U9-10 · .gitignore.** Options: append two lines at the END of the root file (TC11) or a nested
`research_outputs/tierc12/.gitignore` with `*.parquet` and `_det_*/` (X). **Recommend nested** — the root file's sha
and every cited line number stay put. It must exist before the first parquet is written (else `git status` shows bulk).

**U9-11 · WHERE X IS READ FROM AND HOW IT IS PINNED.** Recommend: read X by absolute worktree path, read-only, each
read asserted against `XO/PROGRESS.json` (`4c91b2ef…`) `artifact_shas` / the directory manifest and recorded per stage
(`data/X_READS_<stage>.json`, X's own TC11_READS pattern); vendor the X source bytes TC12 mirrors under
`research_outputs/tierc12/vendor/<name>@<sha8>.py` (X's F-VENDOR pattern) rather than importing from X; never create
`research_outputs/tierc11x/` or any `scripts/tc11x_*` in main; copy the X parquet TC12 depends on into a tierc12
directory (ignored, sha-pinned) so the build survives the worktree's removal after the operator's merge.

**U9-12 · IMPORT-CLOSURE SCOPE FOR TC12.** Recommend: DECISION set = every non-fixture `scripts/tierc12_*.py` except a
TYPED list of VA doors/runners, each exemption EARNED (it must import the door), a new module defaulting to DECISION;
forbidden = TC11's five substrings + exact `analytics.value_area` + `analytics.profile` +
`analytics.rangefinder_census`; AST leg also flags attribute reach `analytics.value_area`, `sys.modules`, dynamic
imports, exec/eval; fresh-interpreter leg per module; VA state reaches decision code only as stamped columns or
arguments. Rival: X's blanket "nothing under analytics" (cannot hold if TC12 re-uses the lineage, which imports the
package).

**U9-13 · `analytics/value_area.py` STAYS OUT OF THE HASHED RECIPE.** Recommend the `rangefinder_census` precedent:
pure (no I/O token, no engine/scripts import, ATR passed in), NOT added to `analytics._MODULES`, `INTERFACE.md` or
`__init__` — `analytics_sha()` stays `ea5f02f2…`; printed as a finding; its own sha printed by the fixtures instead.
Rival: register it (bumps the version, moves every brief capture's sha, forces an `exchange/status` sync).

**U9-14 · FIXTURE DIALECT, TRANSCRIPTS, F-DET.** Recommend the closure-suite harness verbatim (BREAK first, named
detector, crash = defect, `FAILS IF:` on both legs), first line `as_of_last_closed_4h: <pin>`, no-clobber
`file_transcript`, `_partial` for filtered runs, F-DET = two subprocess builds at PYTHONHASHSEED "1" and "20261008" per
parquet directory with its own `build_manifest.json`, no clock/worker/load field in any artifact.

**U9-15 · THE SWEEP.** No driver exists. Options: a gate agent by hand (precedent) or a filed driver. **Recommend a
filed driver that is not a non-fixture python module** (a bash script under `research_outputs/tierc12/review/`, as X's
`attest.sh` is, or a `*_fixtures.py`), running each suite in a fresh process in plan order WITHOUT `--refile-transcript`
and recording per-suite tally, plants, wall and load into `progress/TC12-FIX.json` only.

**U9-16 · REVIEW-WORKTREE ATTESTATION.** Recommend forking TC11's tool (`scripts/tierc12_worktree_attest.py`: staged
parquet held to the reviewed commit's PROGRESS record, re-hashed at close) and adding X's four clauses
(`--no-optional-locks`, `--untracked-files=all`, detached, ignored-listing sha before == after); records under
`research_outputs/tierc12/review/attest/`, typed OUT of every enumerating fixture from the start (the AM-X26 lesson).
Lenses for the final review to be named in LEANS (suggest: fidelity · causality · statistics/verdicts · trading/fills ·
reproducibility+isolation). Rival: X's bash-only attestation (cannot see the ignored parquet's content).

**U9-17 · AS-OF STAMPS AND THE COLLAR.** Recommend `TP.make_put` / `stamp_n` for the nine columns on every table and
ONE shared collar helper with X's six columns + `promotable = False` on grids; absent only on the five §0 rows.
Rival: TC11's three-column dict (drops `m_looks_this_table`, which the contract's "families … before the look" spirit
wants logged).

**U9-18 · THE CLOSE GENERATOR AND THE NUMBER TRACE.** Options: TC11's single generator with `TRACES.json` + F-NUM
(digit-level on §0 and the append), or X's renderer with marked tables. **Recommend TC11's trace file as the record**
(the count of traces and of mismatches printed in the transcript, not only in a commit subject), with X's
marked-table cell check for the large tables and X's `F-DRAFT-WORDS` (no verdict word outside §0).

**U9-19 · REPORT LAYOUT AND "WHOLE".** Recommend the contract's order as §0–§7 (§0 verdicts first with its four named
parts; families; Stage V pins + traverse table; the VA stack; scalper fill-sensitivity and twins; findings-not-fixed;
BOX-COST; the append verbatim) followed by the precedent sections (fixture roll, amendments one line each, operator
questions still open, what this build is not, state push + close acts, the seven-column table LAST). "The VA stack
whole" = the cell-level grid whole in the document, per-instant rows by path + sha (never inlined). Reserve the
report's size in the box forecast (X's floor was 200,000 B).

**U9-20 · THE FORWARD LEDGER'S HOME.** Recommend a TC12-owned chain (`research_outputs/tierc12/forward/`) that carries
all four books; "append-only on the three existing books" proven by (i) TC11's and X's ledger files re-hashing to
`e53328ad…` / `4a6da7e8…` untouched and (ii) TC12's re-ride reproducing their filed book shas and zero appended rows
at their pins before adding rows. Never refresh TC11's or X's ledger in place. (Cross-unit; listed because both files
are inputs of pending close acts.)

**U9-21 · TC12's close_acts.sh STEP 0.** Recommend X's shape: clean index; branch; every close SOURCE tracked and ==
HEAD (TC11's rule — main HEAD moves daily, so a CERTIFIED_TIP is only meaningful if TC12 is on its own branch);
TC10's, TC11's and X's blocks landed **by bytes**, in that order, ledger == HEAD; `research_outputs/tierc11x` present
in main (X merged); destination absent; stamps pending; the format fixture `--check` on the pre-stamp append. Then:
ferry of record → LAW 5 → the tc11-stamp step (U9-8) → stamps → `cat >>` + tail-bytes check → `git add -f` residue →
publish() → bright paths → `Operator: click Sync now.` The executor never runs it (bash -n + scratch-repo fixture
only, X's F-CLOSE-SCRIPT).

**U9-22 · COMPUTE CAP.** Recommend LX-0.9 as written (≤ 6 workers while 1-min load < 10, else 2; spawn; fixed-order
merge; counts only in PROGRESS/BOX_COST). Note for planning: a fork pool was slower than serial on the nest picks.

---------------------------------------------------------------------------------------------------------------
## 4 · HAZARDS

**H1 · The 07:00 routine (and Sunday 08:00/08:30) commits and pushes from the main tree.** It stages every change under
`exchange/`; resets the index if anything else is staged (a builder's half-made `git add` is silently unstaged); commits
on the checked-out branch (main HEAD moves under a running build — anything that pinned "HEAD" goes stale); pushes the
whole branch. The remote-tracking ref has not moved since 2026-09-26 07:00:07 −0300 and today's run logged the SSH
failure (15 commits queued locally); the first successful push flushes everything, `tierc12(` commits included.

**H2 · Three operator close acts are pending and each has step-0/1 tripwires TC12 can trip from the main tree:**
- a non-clean index (all three);
- any change to a TC11 close SOURCE (14 files, `T11/close/close_acts.sh:41`) or to a line TC11's append cites: the
  TC11 contract (12 cites), `T11/forward/FORWARD_LEDGER.md:5,7,38`, `T11/stage_r/STAGE_R.md`, `SCORES.json` verdict
  cells, `FAMILY.json#law`, TC10's append `:250-254`;
- for TC10's F-LAR: `LEDGER.md:829-836`, `LEDGER_APOLLO.md` above `:2426`, `scripts/tierc10_panel.py:746`, the TC10
  contract (`F_close_ledger_publish.md:345-352`);
- for X: `research_outputs/tierc11x` existing in main; any main-tree file at a path X's merge brings
  (`scripts/tc11x_*.py`, `exchange/rows/tierc11/`, `exchange/rows/tierc11x/`, the X contract) → merge failure; **any
  new or changed tabular file (`.parquet/.csv/.jsonl`) under `research_outputs/tierc11/` outside `_det_*`**, or a TC11
  PROGRESS that no longer certifies those bytes → X's ferry of record HALTs at step 1; a gained file or commit in the
  X worktree, or a moved `tierc11x` ref → step 0 refuses.
  Corollary: `research_outputs/tierc11/**`, `research_outputs/tierc10/**`, the X worktree and the three contracts are
  byte-frozen until those scripts have run. Running TC11's or X's own suites in place writes `_det_*` scratch and
  `*_rerun.txt` there — use `--root=<scratch>` or TC12's own readers.

**H3 · Name sweeps.** `scripts/tierc10_*.py` (F-C10-RESUME's `TC_SUITE_GLOB`; an unlisted file turns it RED);
`scripts/tierc11_*.py` (TC11's closure treats a new module as DECISION); any loose file in `research_outputs/tierc10/`;
a repo-root `*.md`/`*.json` or a new `exchange/status/LEDGER_*.md` (TC10's data-spend corpus; a PUMP/MNT/SUI token
there turns F-D-5 RED) — `F_close_ledger_publish.md:14-18`, `:357`.

**H4 · analytics/.** A new file there is scanned by `tests/test_analytics.py` (engine import or an I/O token fails
it); adding it to `_MODULES` moves `analytics_sha()` for every consumer; importing it from `analytics/__init__.py`
would load it into EVERY lineage interpreter and turn any closure leg RED; computing ATR inside breaches I-D or moves
numbers (the engine's ATR is seeded differently).

**H5 · X's parquet are untracked and single-copy.** The operator's merge will not carry them; `git worktree remove`
deletes them. Any TC12 leg that needs them (the mirror, the 4h-holdout semantics check) needs its own pinned copy.

**H6 · Pre-existing dirty state is not TC12's to commit or revert:** `M research_outputs/tierc10/close/
FIXTURES_CLOSE_ledger_append_root.txt` (TC10's step 6 commits it) and `M exchange/status/daily/DAILY_2026-10-08.md`
(the routine's own tail), plus untracked pine/html files of other lanes.

**H7 · Determinism.** `__pycache__` (always `PYTHONDONTWRITEBYTECODE=1` and `-B`; `analytics/__pycache__` already
exists in main); a clock, worker-count or load field in any artifact; set/dict order under PYTHONHASHSEED; pool
scheduling (merge in fixed key order); parquet BYTES vs content sha (F-DET compares both); a transcript line carrying a
temp path or a line number; an enumerating fixture (ferry SCOPE, box-cost rows, a root allow-list) that goes RED when a
later record (attestation log, progress record, close file) appears — X hit this twice (X6-XF2, AM-X26).

**H8 · Causality in the process itself.** A LEANS edit after any number exists; a fixture that re-fits a pin while
claiming an as-of test; a sabotage planted in the comparator instead of the production function; a held-file set or a
"whole vs pointed" choice made after the verdicts are known (freeze both in LEANS — U9-7, U9-19).

**H9 · The box.** After the three closes the forecast leaves 2,244 B below WARN; TC12's contract file (12,209 B) is
already on the bus and already larger than that slack. TC12's report and append are box-bound and FLAGGED-size; REFUSE
is strict > 70% (11,200,000 B) and is never overridden.

**H10 · The "tc11-stamp" blast radius** (C5): 23 + 7 files carry the old sha; TC11's generator HALTs on a stamped
contract; inserting the line anywhere but the end shifts 12 line cites.

**H11 · Worktree hygiene.** 28 stale `wf_8995cf0d-ab5-*` worktrees + one under MAILBOX, all dirty (untracked only), all
at `a6da1b9`; their branches exist. Do not reuse those names; do not `git worktree prune`/remove as a side effect;
review worktrees get their own `tc12-review-*` names and are removed by the tool that made them.

**H12 · Parallel lanes.** `/oracle` on demand writes the LIVE cache, `research_outputs/oracle/**`, oracle scripts and
possibly `.gitignore` (appended) and `exchange/`; the MACROREPORT skill writes `MAILBOX/`. TC12 must run on a frozen
snapshot, never the live cache, and never assume `.gitignore`'s last line is its own.

**H13 · A figure with no file.** X's "5,353 tokens, 0 mismatches" lives only in a commit subject. If TC12's report or
append wants such a count it must come from a filed transcript.

---------------------------------------------------------------------------------------------------------------
## 5 · REUSE PLAN

**Import as-is (already importable from the main tree, no fork):**
- `tierc10_panel` as `TP`: `stamp_n`, `AS_OF_COLUMNS`, `make_put`, `grid_whole`, `check_keys`, `check_det`, `lens_edge`
  (through whatever env shim the substrate unit provides — `TP` binds TC10's pin and registry at import).
- `tierc2_baseline`: `write_table`, `_content_sha`, `assert_key`.
- `tierc10_close_close_ledger_append` as `LA`: `render_quote`, `parse_quotes`, `verify_quote` (import-safe anywhere;
  TC11's close already does this).
- `publish_exchange` constants by `ast.literal_eval` only — never import-and-call `publish()` in a build.

**Fork into `scripts/tierc12_*` (copy, rename, re-type the literals):**
- `tierc11_closure_fixtures.py` → `tierc12_closure_fixtures.py`: harness (`say/clock/prove/plants/file_transcript`),
  AST walk, lineage walk, hook-escape leg; re-type `FORBIDDEN`, the runner list, the AM-8 call sites; add the
  `analytics.value_area` exact/attribute legs (U9-12).
- `tierc11_worktree_attest.py` + `tierc11_attest_fixtures.py` → tierc12 twins; change `STAGE_GLOBS`, `PROGRESS_REL`,
  `wt_path` prefix (`tc12-review-`), staged foreign records; add X's four clauses (U9-16).
- `tierc11_close.py` + `tierc11_close_fixtures.py` → the generator, `TRACES.json`, F-NUM, F-BOXCOST, F-FNF, F-LAR,
  F-CLOSE-ORDER, F-DET; re-point every path constant (`:86-110`), the family reader, the tier line.
- From X (vendor the bytes first, pinned by sha, since X is unmerged): `tc11x_progress.py` → `tierc12_progress.py`;
  `tc11x_exit.collar` → one shared collar helper; `tc11x_close_draft_fixtures.py`'s WORDS / marked-table / ISO legs;
  `tc11x_close_findings.py` (ATHENA owner, harvest keys); `tc11x_close_box_cost.py` (seven sets (a)–(g), compute
  ledger); `tc11x_close_fixtures.py`'s F-CLOSE-SCRIPT (scratch-repo step-0 test) and `--stamp`; the ferry's first-fit,
  cap and manifest law from `tc11x_ferry.py` (re-typed for one tier, staged off-bus).
- `XO/review/attest.sh` → a bash twin for the sweep driver / attestation clauses that must run git out of process.
- `XO/close/close_acts.sh` as the template for TC12's (by-bytes tier blocks, `die` with resume text, tail-bytes check,
  `git add -f`), with TC11's "SOURCES tracked and == HEAD" rule in place of CERTIFIED_TIP if TC12 stays on main.

**Mirror in documents (no code):** `LEANS.md` layout and §10 disposition table; `LEANS_AMENDMENTS.md` /
`AMENDMENTS_PROPOSED.md`; `REGISTRATION_PLAN.md` §3 stage table with order constraints; the review JSON shape with
`drafted_sha / revised_sha / counts / critic_pass`; the judge record + corrected close brief.

**Newly written for TC12 (nothing on disk does it):**
- the sweep driver (U9-15);
- the R0 census record for a tier with three unfinished predecessors (U9-4);
- the X-reads record and the vendor/copy step for X's sources and parquet (U9-11);
- the off-bus ferry staging + close-act copy with a re-measured box (U9-6, U9-7);
- the tc11-stamp close step and its old→new sha record (U9-8);
- close_acts step 0 for FOUR tiers of order (U9-21);
- the closure legs specific to `analytics.value_area` and the "VA state as data" adapter rule (U9-12);
- a nested `research_outputs/tierc12/.gitignore` (U9-10).
