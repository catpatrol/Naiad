## L-0 · LAWS AND PROCESS

This section reads the contract's LAWS paragraph (:5-9), STEP Q (:10), RULINGS ENACTED (:12-16), the cross-cutting
fixtures of the FIXTURES line (F-DET, F-GRID, F-KEY, import-closure, worktree attestation, :123-124), WHAT THIS IS NOT
(:132-134) and VETOES BY NAME (:135-137). It fixes the resume law, the stage order and commit law, the fixture
harness, the sweep, the stamp and collar helpers, the "no typed number" enforcement, the meaning of "decision module",
and the refusal fixture F-NOT. It owns no registered row. It conforms to ORCHESTRATOR_RULINGS O-1..O-24 as written;
one objection is filed at the end (O-3/O-4, where X's contract can be read from).

**Abbreviations.** `M` = `/Users/luis/Naiad` (the main tree, branch `v12-v1-census`). `T12` = `research_outputs/tierc12`.
`T11` = `research_outputs/tierc11`. `XR` = `research_outputs/tierc12/x_rec` (the byte copies of TC11-X; every read
asserted against `XR/X_REC_MANIFEST.json`). "contract :n" = 1-indexed line n of the STEP Q bytes of
`exchange/queue/2026-10-08_TC12_APOLLO.md` (L-0.1). `E` = the TC12 env shim (`scripts/tierc12_env.py`, owned by L-D);
`E.TP` = `tierc10_panel`, `E.TB` = `tierc2_baseline` as that shim exposes them.
**Tags.** [read here] = the cited source was opened and read while drafting. [measured here] = a sha, byte count or
line count taken from files while drafting (structural; no outcome of any book was computed for this section).
**The fixture dialect** used in every FAILS-IF below is L-0.14's: a BREAK leg of named plants that must each turn RED,
then the REAL leg.

---------------------------------------------------------------------------------------------------------------
### A · Identity

**L-0.1 THE CONTRACT OF RECORD AND ITS PREFIX PIN** — "STEP Q: file this paste verbatim to
exchange/queue/2026-10-08_TC12_APOLLO.md (sha printed)." (contract :10)
READING: STEP Q is done and is never repeated: commit `28e006bc5def421bd65e3835a95a2905c4e21b93`, one path. The
contract of record is the bytes of that file AS FILED AT STEP Q. Their length `N` and sha256 are read from
`T12/progress/STEP_Q.json` key `artifact_shas["exchange/queue/2026-10-08_TC12_APOLLO.md"]` (`bytes`, `sha256`), never
typed in code. THE PREFIX PIN: every TC12 reader of the contract (the pin door of L-0.17, the registry filer, the
scorer's verifier, the close generator) reads the file, takes its first `N` bytes, HALTs unless `sha256(prefix)`
equals the STEP Q sha, and cuts every line slice from the prefix by TC11's slice law: `text = "\n".join(lines[a-1:b])`,
1-indexed, inclusive, leading whitespace kept, no trailing newline, UTF-8. THE TAIL: the bytes after byte `N` are
empty or consist only of whole lines beginning `BUILT: `, each ending in a newline; anything else HALTs. The
whole-file sha is recorded beside the prefix sha and compared by nothing afterwards. It is ONE function, used by every
reader; L-X states it in full for the registry (its prefix-pin reading), and the resume suite calls the same function.
No TC12 act writes the file before CLOSE; TC12's own BUILT stamp is an operator close act and is appended after the
prefix (L-X places the step).
SOURCE: contract :10; `T12/progress/STEP_Q.json` [read here]; `git show --stat 28e006b` (scout U9 §1.1);
`exchange/queue/README.md:8-12` (rule 6, "on a line of its own") [read here]; the slice law
`XR/tierc11x/REGISTRATION_PLAN.md:20-27` [read here]; the lesson `T11/BUILD_DRAFT.md:5945` (FN-M-QUEUE-STAMP) [read
here]; scout U1 R-18.
RIVALS: (a) pin the whole-file sha only (TC11's way) — not taken: that pin is what turned TC11's BUILT stamp into a
multi-file cascade (L-0.24). (b) keep a sibling copy of the contract under `T12/` — not taken: two texts of record.
FAILS-IF: **F-CONTRACT** (`scripts/tierc12_resume_fixtures.py`) FAILS IF the file is shorter than `N`, `sha256(first N
bytes)` differs from the STEP Q sha, the tail holds anything but whole `BUILT: ` lines, or a reader's slice extends
past byte `N`. Planted mutations (scratch copies): one byte flipped inside the prefix → RED; a line inserted at line 3
→ RED; a tail line that is not a `BUILT: ` line → RED. Control that must stay GREEN and is printed: a `BUILT: x` line
appended after the prefix.

**L-0.2 RATIFICATION, THE "maker" RULING, SAIL, LANE, SEED** — "RATIFIED: operator 2026-10-08 — "proceed with paste
for builder according to your suggestions, including maker as toll of record for scalper mode" (verbatim; RULING
"maker" of record). SAIL remains HELD (operator 2026-09-24). Drafted: APOLLO. Executor: HEPHAESTUS. Seed 20261008."
(contract :2-4)
READING:
- **The ruling.** The operator's words exist in TC12 only as a line-cited quote of contract :2-3. Every document that
  states the "maker" ruling renders that quote from the prefix bytes (cite + verbatim lines); none retypes it. Its
  operative content — maker bps on entry and targets for the SCALPER family (contract :101) — is L-S's.
- **SAIL.** No file in the repo pairs "SAIL" with the date 2026-09-24 (scout U1 §1.10, git grep). The parenthesis is
  read as the operator's ratification of the TC11 contract on that date (`exchange/queue/2026-09-24_TC11_APOLLO.md:2`),
  whose CLOSE clause (:99) says "SAIL still HELD", itself restating the hold of
  `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:2-3` and :143. TC12 performs no SAIL act (L-0.30, leg SAIL), and
  the ledger append cites those three places.
- **Lane and tag.** The commissioning lane is APOLLO, so the ledger the close appends to is
  `exchange/status/LEDGER_APOLLO.md`. Code prints each reading it applies as `[LEAN-HEPHAESTUS] L-<S>.<n> …`; the tag
  is read by object (`LEAN_TAG`, `scripts/tierc10_panel.py:143`).
- **Seed.** The tier seed is the contract's (:4), read through the pin door (L-0.17) and asserted equal to
  `T12/PROGRESS.json` key `seed`. It is (i) passed explicitly to every ruler and bootstrap call — no def-time default
  is relied on (`T5.cluster_boot` defaults to the lineage seed, `TP.loao_n` to TC10's: `XR/tierc11x/LEANS_X.md:416-419`);
  (ii) the second PYTHONHASHSEED twin of F-DET (L-0.20); (iii) the seed of every seeded fixture sample (L-0.14). The
  sensitivity seed printed beside every ruler is `T5.SEED`, read by object (`scripts/tierc10_panel.py:92`), per O-22.
SOURCE: contract :2-4, :101; the three SAIL cites above (scout U1 §1.10); `scripts/tierc10_panel.py:92`, :143 [read
here]; `scripts/tierc12_progress.py:53` [read here]; O-22.
RIVALS: a per-stage salted seed — not taken: the contract names one seed. Reading "operator 2026-09-24" as a separate
SAIL ruling — not taken: no such document exists; listed for the operator.
FAILS-IF: **F-SEED** (`scripts/tierc12_closure_fixtures.py`, AST) FAILS IF a call whose callee is in the fixture-typed
ruler list (`cluster_boot`, `cluster_boot_diff`, `loao_n`, `default_rng`, and every TC12 wrapper of them) omits its
seed argument or passes one that does not resolve to the pin door. Planted mutations: a `cluster_boot(x, c)` call with
no `seed=` in a copy of the scorer → RED; a literal seed in the same call → RED (also caught by F-TYPED).

---------------------------------------------------------------------------------------------------------------
### B · The resume law

"resume law (R0 census · verify-or-quarantine · frozen texts · one corridor · draft off-bus · commit + PROGRESS.json
per stage)" (contract :5-6). The law's text of record is TC10's LAW OF RESUMPTION items 1-6 and its R0 paragraph
(`exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:11-33` [read here]); the TC12 contract names it by its six tags, and
each tag is read below.

**L-0.3 R0 CENSUS** — "R0 census" (contract :5)
READING: R0 is a read-only census whose only write is a progress record. TC12's R0 of record is filed:
`T12/progress/TC12-R0.json` (commit `ac8cb92`) — a fresh tier (no TC12 artifact before STEP Q), three predecessor
close acts pending, `head_at_r0`, the two paths dirty at R0 that are not TC12's, `x_tip`, the X byte-copy counts and
`frozen_estate_shas_at_r0`. RESUME: at every session start and at every stage gate the census is re-derived by
**F-RESUME** from files only: for each record under `T12/progress/*.json` it re-hashes every `artifact_shas` path and
every recorded transcript, recomputes the stage ledger (COMPLETE-VERIFIED / PARTIAL / ABSENT, in the order of `ORDER`,
`scripts/tierc12_progress.py:20-21`) and prints THE RESUME POINT = the first `ORDER` entry whose record is absent or
not COMPLETE-VERIFIED. The resume point is derived, never typed and never stored. The census also prints, with no pass
condition, the branch, the live HEAD, and three booleans read from files: whether each predecessor's report exists
under `exchange/reports/` and its header stands in `exchange/status/LEDGER_APOLLO.md`. A fixture that depends on git
history takes its head as an argument (`--at=<sha>`, the last `tierc12(` commit before the one being made); the live
HEAD goes to stdout only (the daily routine moves it; X's AM-X17 pattern).
SOURCE: TC10 contract :26-33; `T12/progress/TC12-R0.json`, `T12/PROGRESS.json` [read here];
`scripts/tierc12_progress.py:20-22`, :44-45 [read here]; `XR/tierc11x/LEANS_X_AMENDMENTS.md:410` (AM-X17); scout U9 §1.2.
RIVALS: a hand-kept `resume_point` string (TC11's PROGRESS) — not taken: a typed pointer can disagree with the
records. A census that reads the live HEAD into its transcript — not taken: the transcript would change daily.
FAILS-IF: see L-0.4 (one fixture, F-RESUME).

**L-0.4 VERIFY-OR-QUARANTINE** — "verify-or-quarantine" (contract :5)
READING: three status words and no fourth (`STATUSES`, `scripts/tierc12_progress.py:22`; the merger HALTs on any
other, :44-45). A stage is **COMPLETE-VERIFIED** iff all of: (1) every `artifact_shas` path exists and re-hashes to its
recorded `bytes` and `sha256`; (2) `blockers` is empty; (3) it holds at least one fixture record and every record has
`exit_code` 0, `legs_red` 0, `transcript_drift` false and `transcript_sha_before == transcript_sha_after ==` the
transcript's sha now; (4) its suites re-pass now (L-0.11). The FIXTURELESS pre-stages are a closed, typed list —
`STEP Q`, `TC12-R0`, `TC12-LEANS` (documents only) — and are COMPLETE-VERIFIED on (1) and (2) alone; their bytes are
re-bound by F-FROZEN-TEXT from TC12-REG on. Anything else is **PARTIAL** (present but unverified or failing) or
**ABSENT**. "Built, awaiting verification" is PARTIAL with a blocker. QUARANTINE: before a PARTIAL stage is rebuilt,
its artifacts are MOVED — never deleted, never overwritten — to `T12/_partial_<YYYYMMDD>T<HHMM>Z/<same subpath>` (TC10's
form, e.g. `research_outputs/tierc10/_partial_20260922T0955Z`), by the stage's builder, and the move is listed in the
record's `notes`. A quarantine directory is never staged and never read by a builder. A stage that read a quarantined
artifact (by the order of L-0.10) becomes PARTIAL with it.
SOURCE: TC10 contract :12-15 (law items 1-2); `scripts/tierc10_resume_fixtures.py:296-300` (`LEGAL_STATUS`,
`STAGE_KEYS`, `FIXTURE_KEYS`), :4559-4569 (a COMPLETE-VERIFIED record with no fixture is a finding in TC10) [read
here]; the fixtureless precedent: `T11/PROGRESS.json` stages `STEP Q` and `TC11-REG` (`fixtures: []`),
`XR/tierc11x/PROGRESS.json` stages `STEP Q`..`X-LEANS` (no `fixtures` key) [measured here]; O-6.
RIVALS: TC10's strict law (every COMPLETE-VERIFIED stage needs a fixture record) — not taken for the three document
stages: two of them were filed fixtureless before these readings, and a fixture invented after the fact would certify
nothing; the exemption is typed and closed instead of silent. X's fourth word "COMPLETE" — not taken: not in the law.
FAILS-IF: **F-RESUME** (`scripts/tierc12_resume_fixtures.py --stage=<STAGE> --at=<sha>`) FAILS IF a recorded artifact
is missing or its bytes or sha differ; a record lacks a key of the typed key set or carries an illegal status; a
COMPLETE-VERIFIED record outside the typed fixtureless list has no fixture record, a non-zero `exit_code` or
`legs_red`, a drifted transcript, or a non-empty `blockers`; a `<stem>_rerun.txt` or `<stem>_partial.txt` stands
beside a transcript of record; a quarantine path appears in a later record's `artifact_shas`. Planted mutations
(scratch copy of the `T12` root; "a tampered partial must FAIL", TC10 contract :125-126): one byte flipped in a
recorded artifact; a recorded artifact deleted; `legs_red` set to 1; `fixtures` emptied on `TC12-D`; status
`"COMPLETE"`; a `_rerun.txt` planted beside a transcript — each must be caught by its named detector.

**L-0.5 FROZEN TEXTS** — "frozen texts" (contract :5)
READING:
- **Byte-frozen** from the instant named: the contract prefix (STEP Q; L-0.1); `T12/ORCHESTRATOR_RULINGS.md` (R0; its
  sha is an R0 artifact and `PROGRESS.json` `rulings_of_record`, so a sustained objection is recorded in LEANS's review
  disposition or as a dated amendment, never by editing that file); from the TC12-REG commit: `T12/LEANS.md`,
  `T12/registrations/REGISTRATIONS.json` (filed by a write-once filer that HALTs if the file exists — TC11's law),
  `T12/registrations/REGISTRY_PIN.json`, `T12/pins/CONTRACT_PIN_MAP.json`, `T12/pins/CONTRACT_PINS.json`,
  `T12/pins/PIN_REGISTER.json` (L-0.17), `T12/frozen/FROZEN_ESTATE.json` (L-0.6); from their own stages:
  `T12/data/AS_OF_PIN.json` (TC12-D, write-once), the traverse pin record (TC12-V; O-18) and the fourth book's spec
  (L-L; O-24).
- **Append-only** (every committed version is a byte-prefix of the next): `T12/DISCLOSURES.md`,
  `T12/LEANS_AMENDMENTS.md`, `T12/AMENDMENTS_PROPOSED.md`, and the forward ledger (L-L).
- **A reading is never re-chosen after a number is seen.** The only route of change after freeze: a builder files a
  proposal `AP-n` in `AMENDMENTS_PROPOSED.md` (date, reading id, text at issue, evidence path:line, proposed text,
  downstream effect); the orchestrator rules it into `LEANS_AMENDMENTS.md` as
  `## AM-n · <date> (~HH:MMZ) · <reading ids> · ruling on AP-n` with **Text amended / Amended to / Reason / Redone**.
  The law is TC11's, verbatim: "an amendment may follow from a build fact (the code cannot do what a reading says) or
  from a verifier's finding. It may never follow from a registered rule's outcome." TC12 adds one source: an operator
  veto by name (L-0.23). Everything downstream of an amended reading is redone and re-certified;
  `PROGRESS.json` `amendments_of_record` carries the file's sha (`scripts/tierc12_progress.py:57`).
- **Resume item 3.** A registered row's number computed before an interruption, or before an amendment that touches
  the row, is KEPT and printed BESIDE the fresh value with the AM id; it is never re-worded and never dropped (the
  scorer's no-clobber law, L-X: differing bytes go to `<stem>_rerun<suffix>`).
- **The freeze of LEANS** binds bytes: `sha256(T12/LEANS.md) == REGISTRATIONS.json leans.sha256 ==
  REGISTRY_PIN.json leans_sha256`, and the sha the last review pass names (L-0.12).
SOURCE: TC10 contract :16-18 (law item 3); `T11/LEANS_AMENDMENTS.md:3-8` [read here];
`XR/tierc11x/LEANS_X_AMENDMENTS.md:1-8`, `XR/tierc11x/AMENDMENTS_PROPOSED.md:1-6` [read here];
`scripts/tierc11_registrations.py:244-245` (write-once HALT) [read here]; `T12/DISCLOSURES.md:3-4` ("Entries are
dated and never edited") [read here]; O-6.
RIVALS: edit LEANS in place with a changelog — not taken: the registry pins its sha. Let builders amend directly — not
taken: the builder who saw the number would be ruling on the reading.
FAILS-IF: **F-FROZEN-TEXT** (resume suite) FAILS IF a byte-frozen file's sha differs from its pin; for an append-only
file, some `tierc12(` commit's parent blob is not a byte-prefix of that commit's blob (git plumbing at `--at`); the
LEANS sha, the registry's two `leans` pins and the review record's last-pass sha are not one value. Planted mutations:
a one-character edit in a scratch copy of `LEANS.md` → RED; an earlier DISCLOSURES entry edited (not appended) in a
scratch repo → RED; the registry filer run against an existing `REGISTRATIONS.json` must HALT (counted as the catch).

**L-0.6 THE FROZEN ESTATE** — "frozen texts" (contract :5) as it binds the predecessors, and "no re-family of TC11"
(contract :133-134); governed by O-3.
READING: TC12 moves no byte of the estate O-3 lists. Prevention is L-D's env hook; DETECTION is here. At TC12-REG a
census `T12/frozen/FROZEN_ESTATE.json` is written once by `scripts/tierc12_frozen.py` (stdlib only; walks and hashes; no
git) over the WORKING-TREE bytes of: `research_outputs/tierc10/**`, `research_outputs/tierc11/**`, `scripts/tierc10_*`,
`scripts/tierc11_*`, the two earlier TC contracts in main's `exchange/queue/` (TC10 RESUME, TC11),
`exchange/queue/008_sail-skeleton.md`, `LEDGER.md`, `exchange/status/LEDGER_APOLLO.md`, `exchange/status/CONVENTIONS.md`,
`scripts/publish_exchange.py`, and every `analytics/*.py` plus `analytics/INTERFACE.md` except `analytics/value_area.py`
— each as `{path, bytes, sha256}`; every `__pycache__` directory under those roots by name; the two earlier snapshots
`tc10_20260921` and `tc11_20260925` as a `(path, bytes, mtime_ns)` listing sha (their content hashing is Stage D's
prefix-identity leg, L-D); and `XR/**` against `XR/X_REC_MANIFEST.json` (path set, `n_files`, every sha). The
entries of `T12/progress/TC12-R0.json` `frozen_estate_shas_at_r0` must equal the census on those paths. For the live
cache and the X worktree "frozen" is proven differently, because other lanes may move them: no TC12 process opens a
path under either (the hook's open log, L-D), and `refs/heads/tierc11x` equals the `x_tip` recorded at R0. VERDICT at
every stage gate and at CLOSE: path set and every sha equal to the census. IF A PREDECESSOR'S CLOSE ACT LANDS MID-BUILD
(the operator's keystroke, L-0.26), the estate moves by design: the orchestrator files an amendment "FROZEN_ESTATE
re-pinned after <tier>'s close" that lists every moved path with the commit that moved it (a subject starting
`tierc10`, `tierc11(`, `tc11x(`, `exchange: auto-publish`, or the merge of `tierc11x`), a new census
`FROZEN_ESTATE_<k>.json` is written beside (the first is never rewritten), and any TC12 artifact whose `input_sha`
names a moved path is redone. A moved path with no attributing foreign commit is a finding against TC12 and HALTs the
gate.
SOURCE: O-3, O-4; `T12/progress/TC12-R0.json` [read here]; `XR/X_REC_MANIFEST.json` keys `files[].copy`, `files[].sha256`,
`n_files`, `law` [measured here]; scout U1 H-3, H-5, H-6; scout U9 H2.
RIVALS: `git status` alone — not taken: most of TC10's tree and all TC11 parquet are git-ignored, so porcelain cannot
see them. Walking the X worktree to hash it — not taken: O-4 forbids reading it, and its own close script certifies it.
FAILS-IF: **F-FROZEN** (resume suite) FAILS IF any census path is missing, changed or joined by a new sibling under a
census root (a `_det_*` file, a `*_rerun.*`, a `__pycache__`), or the `tierc11x` ref moved. Planted mutations (scratch
copy of a census root): one byte flipped in `scores/SCORES.json`; a `_det_x/a.parquet` added; a `__pycache__/a.pyc`
added; a `SCORES_rerun.json` added — each RED, naming the path.

**L-0.7 ONE CORRIDOR, ONE SUBSTRATE, ONE PROCESS** — "one corridor" (contract :5); O-5, O-7, O-8, O-9.
READING: One pin for the tier: the value O-7 fixes (the latest 4h bar closed when STEP Q was committed), written once
by Stage D to `T12/data/AS_OF_PIN.json` key `as_of_last_closed_4h_close_ms` and read by object ever after. TC10's law
item 4 offers "re-pin at resume" when Stage D is incomplete; that branch is NOT available to TC12 — the pin was taken
by value at STEP Q, so an incomplete Stage D is rebuilt to the same pin. Every stage record's `as_of` from TC12-D on is
the pin's ISO string, and every transcript's first line is `as_of_last_closed_4h: <that ISO>`. THE SCORE EDGE is a
second, earlier instant inside the same corridor: TC11's pin, read by object from `T11/data/AS_OF_PIN.json` key
`as_of_last_closed_4h_close_ms` (sha held by L-0.6); O-9 scores entries whose bar closes at or before it and prints
(score edge, pin] as the strip. "One corridor" therefore means: one snapshot (`tc12_20261008`, O-8), one pin record,
two named sub-windows; no table mixes them without saying which edge its rows could see (L-0.13). One process binds
one snapshot: `NAIAD_CACHE_DIR` is exported as an absolute path before python starts and `PYTHONDONTWRITEBYTECODE=1`
always (O-5). Compute: the worker cap and the load rule are O-5's; workers are `spawn` processes that import `E` before
any I/O; results merge in a fixed key order before any write; worker counts and load averages are recorded only in
progress records and the close's cost table, never in an artifact.
SOURCE: TC10 contract :19-20 (law item 4); O-5, O-7, O-8, O-9; `scripts/tierc10_panel.py:634-647` (`stage_d_pin`),
:690-699 ("a pin may only look back") [read here]; `XR/tierc11x/LEANS_X.md:526-534` (LX-0.9) [read here].
RIVALS: re-pin at each stage to the newest closed bar — not taken: O-7. Score to TC12's pin — not taken: O-9.
FAILS-IF: **F-ONE-CORRIDOR** (resume suite) FAILS IF a stage record's `as_of` (TC12-D onward), a transcript's first
line, or a `build_manifest.json` `as_of` names an instant other than the pin or the score edge; a table's
`as_of_last_closed_4h` values hold a third instant; a manifest's `substrate` is not the snapshot name in Stage D's
manifest. Planted mutations: a manifest copy with `as_of` one 4h step later → RED; a table copy stamped with a third
instant → RED; a manifest copy naming `tc11_20260925` as substrate → RED.

**L-0.8 DRAFT OFF-BUS** — "draft off-bus" (contract :5)
READING: The report exists only as `T12/BUILD_DRAFT.md` until the operator's close act moves it to
`exchange/reports/BUILD_2026-10-08_TIERC12_VALUE_AREA.md` (contract :126; the LAW 5 move: copy, shas equal, the draft
removed). Nothing TC12 writes lands under `exchange/` before CLOSE except the STEP Q contract (O-1): the ledger append
is staged at `T12/LEDGER_APOLLO_APPEND.md`; the row CSVs are staged under `T12/ferry/` and the ferry of record is a
close act (O-24); `exchange/rows/tierc12/` does not exist during the build. Reason on disk: the 07:00 routine stages
all of `exchange/` and pushes the branch (`scripts/daily_routine.py:1489`; `scripts/publish_exchange.py:603`, :745) —
"a draft under exchange/ is not a draft" (TC10 contract :21-22).
SOURCE: TC10 contract :21-22 (law item 5); O-1, O-24; the three cited script lines [read here]; scout U1 H-1.
RIVALS: write the CSVs to `exchange/rows/tierc12/` as built — not taken: the routine would publish evidence the next
morning and shrink the box X's ferry of record is about to measure (scout U1 H-9).
FAILS-IF: **F-OFFBUS** (resume suite) FAILS IF, at `--at`, the union of paths of the commits whose subject starts
`tierc12(` holds any path under `exchange/` other than the contract in the STEP Q commit; a file exists at
`exchange/rows/tierc12` or at the report's destination; a file under `exchange/` has the sha of a TC12 stage artifact
other than STEP Q's; a non-fixture TC12 source opens a path under `exchange/` for writing (AST: a write-mode `open`,
`write_text`, `write_bytes`, `to_csv`, `copy*` or `replace` whose target resolves under `exchange/`). Planted
mutations: a scratch repo with a `tierc12(TC12-L)` commit adding `exchange/rows/tierc12/a.csv` → RED; a scratch tree
with the draft copied to the report's destination → RED; a planted `(ROOT / "exchange" / "rows").mkdir()` in a copy of
the ferry stager → RED.

**L-0.9 COMMIT + PROGRESS.json PER STAGE** — "commit + PROGRESS.json per stage" (contract :5-6); O-1, O-2, O-6.
READING:
- **Progress.** Each stage's builder writes `T12/progress/<STAGE>.json` with keys `stage, status, as_of, blockers,
  artifact_shas {repo-relative path: {bytes, sha256}}, fixtures [{suite, exit_code, legs_red, legs_total,
  transcript_drift, transcript_sha_before, transcript_sha_after, wall_seconds}], one_line, notes`; fixture records are
  appended, never inserted; `suite` is the full argv after the interpreter (so a parameterised suite is re-runnable
  verbatim). `scripts/tierc12_progress.py` merges the records verbatim in `ORDER` and is the ONLY writer of
  `T12/PROGRESS.json`. TC10's "one line to the draft" is the record's `one_line`, which the close generator renders
  into the report's build log.
- **Commit.** After every stage, and before the next starts, the ORCHESTRATOR commits; no builder and no reviewer runs
  a state-changing git command. Subject: `tierc12(<STAGE>): <sentence>`, where `<STAGE>` is an `ORDER` entry written
  with or without its `TC12-` prefix (the filed R0 commits read `tierc12(R0)`). A subject never starts `tierc10`,
  `tierc11(` or `tc11x(`: the three pending close scripts count commits by those prefixes. Paths: explicit pathspecs
  only, drawn from `T12/**` (as its nested `.gitignore` leaves visible), `scripts/tierc12_*.py` and
  `analytics/value_area.py`; never `git add -A`, `git commit -a` or a stash; never the two paths dirty at R0 (O-2).
  The add and the commit run in one shell command, so the index is staged only for its duration, and
  `git diff --cached --quiet` is checked before and after (a staged non-exchange path at a `publish()` run makes the
  routine reset the index and skip its publish: `scripts/publish_exchange.py:624-631`). The body ends with the
  session's attribution trailer. Parquet, `_det_*/` and `x_rec/**` are never committed (nested `.gitignore`); an
  untracked artifact is pinned twice — `{bytes, sha256}` of the file in its stage record, and its content sha in its
  directory's tracked `build_manifest.json`.
- **The gate, in order:** (1) the builder files its artifacts and its transcripts (`--refile-transcript`, once);
  (2) the stage's suites are re-run in fresh processes without that flag (no `_rerun.txt`); (3) the builder writes the
  progress record with the transcript shas before and after; (4) the merger runs; (5) F-RESUME and its sibling legs
  run at `--at=<previous tierc12 head>`; (6) the commit. The next stage starts after (6).
- **What cannot be enforced here** is stated, not hidden: the daily routine pushes the whole branch whenever its SSH
  route works, so `tierc12(` commits reach origin without an operator act (it pushed TC11's the same way). The count
  "N commits, M on a remote" is read from git at close, never typed.
SOURCE: TC10 contract :23-24 (law item 6); O-1, O-2, O-6; `scripts/tierc12_progress.py` [read here];
`scripts/tierc10_resume_fixtures.py:297-300` [read here]; `T12/.gitignore` [read here]; root `.gitignore:44`, :263-264,
:287-288 [read here]; `scripts/publish_exchange.py:603`, :627, :745 [read here]; scout U1 H-1, H-2, H-8; scout U9 §1.9.
RIVALS: builders commit their own stages — not taken: one writer of history, and a builder's half-made `git add` is
exactly what the routine resets. A hand-edited PROGRESS.json (TC11) — not taken: O-6.
FAILS-IF: **F-COMMIT** (resume suite, range `28e006b^..<--at>`) FAILS IF a `tierc12(` commit touches a path outside
the allow-list (plus the contract, STEP Q only), or either R0-dirty path; a commit with another subject touches a TC12
path; a subject does not name an `ORDER` stage; a body lacks the trailer; the index is non-empty when the suite runs.
**F-PROGRESS** FAILS IF `PROGRESS.json` is not byte-equal to the merger's output re-derived into a scratch directory,
or a record's stage is not in `ORDER`. Planted mutations (scratch repos and copies): a `tierc12(X)` commit touching
`research_outputs/tierc11/a.txt` → RED; a subject `tierc11(BUILT-STAMP)` on a TC12 path → RED; one key of
`PROGRESS.json` hand-edited → RED; a record with status `"COMPLETE"` → the merger's HALT (counted as the catch).

**L-0.10 THE STAGE ORDER AND TEXT-BEFORE-RESULT** — "families declared by MECHANISM before the look" (contract :8) and
"commit + PROGRESS.json per stage" (:5-6)
READING: The order of record is `ORDER` in `scripts/tierc12_progress.py:20-21`: STEP Q · TC12-R0 · TC12-LEANS ·
TC12-REG · TC12-D · TC12-ENV · TC12-V · TC12-C · TC12-G · TC12-R · TC12-S · TC12-L · TC12-SCORE · TC12-FIX ·
TC12-REVIEW · TC12-CLOSE. Each stage must FILE the following (and be COMPLETE-VERIFIED and committed) before the next
may start:

| stage | reading owner | must file before the next may start |
|---|---|---|
| STEP Q | L-0.1 | the contract (filed, `28e006b`) |
| TC12-R0 | L-0.3 | the census record, the nine scout maps, `XR/X_REC_MANIFEST.json`, the rulings, the disclosures (filed, `ac8cb92`, `c3129e9`) |
| TC12-LEANS | all sections | `T12/LEANS.md` (nine sections, review disposition filled), `T12/review/LEANS_REVIEW_<date>.json` (every lens and pass, drafted and revised shas), `T12/review/WORKTREE_ATTEST_LEANS.jsonl` (L-0.12), `T12/DISCLOSURES.md` appended |
| TC12-REG | L-X, L-0.5, L-0.6, L-0.17 | `registrations/REGISTRATIONS.json` + `REGISTRY_PIN.json`; the three pin files; `frozen/FROZEN_ESTATE.json`; the fourth book's spec text if L-L files it here; the harness `scripts/tierc12_fx.py`, `tierc12_pins.py`, `tierc12_units.py`, `tierc12_frozen.py`; the registry, pins, resume and closure (AST legs) transcripts. **No bar is read and no book exists at or before this commit.** |
| TC12-D | L-D | the snapshot, its manifest, the pin record, the fee schedule, the contract specs, their transcripts |
| TC12-ENV | L-D, L-0.12-0.16, L-0.22 | `scripts/tierc12_env.py`; `tierc12_tables.py`, `tierc12_asof.py`, `tierc12_worktree_attest.py`; the env, tables, closure, attest transcripts |
| TC12-V | L-V | `analytics/value_area.py`, the VA door, the per-bar VA tables per lens, the mirror record (HALT on disagreement), **the traverse pins, frozen**, the nest table |
| TC12-C | L-C | the v6 book on the scored window and its strip; F-CTRL |
| TC12-G | L-G | the regbooks of P-ADM-1 and P-BRD-1; the admission Tier-E grids |
| TC12-R | L-R | the regbooks of P-DIR-1 and P-SFP-VA-1; the range Tier-E tables |
| TC12-S | L-S | the regbook of P-SCALP-3, its twins and its miss table |
| TC12-L | L-L | the four-book ledger, the era tables, the ferry staged off-bus with its forecast |
| TC12-SCORE | L-X | the five score rows, the family record, the persisted draws |
| TC12-FIX | L-0.11 | every residual finding disposed (FIXED / CARRIED / ruled as AM-n); the full sweep GREEN |
| TC12-REVIEW | L-0.12 | one GREEN attestation per lens at the TC12-FIX commit; the judge record; fixes; a `fix-head` attestation if any commit followed |
| TC12-CLOSE | L-X, L-0.24 | the draft, findings-not-fixed, box and compute cost, the staged append, `close/close_acts.sh` (never run), the tc11-stamp proof |

Building in parallel is allowed only for TC12-G, TC12-R and TC12-S, after TC12-V and TC12-C are COMPLETE-VERIFIED
(disjoint directories and progress records; one machine-wide worker cap, O-5); their commits still land in `ORDER`.
**SUB-STAGES.** A stage may file more than one record. A sub-stage's id is `<ORDER entry>.<tag>` (X's form:
`X-FOUND.books`, `X-FOUND.ranges`), which the merger sorts under its parent by its longest-prefix rule
(`scripts/tierc12_progress.py:29-32`). No stage id exists outside `ORDER` and its dotted children. The rule is not
cosmetic: an id such as `TC12-VENDOR` has no entry of its own and is matched by the prefix `TC12-V`, so the filed
merger would place it at Stage V's position, after TC12-ENV [measured here, by re-deriving `stage_key` on the name].
A vendoring referee, a mirror step or any other pre-step a section needs is therefore a dotted child of the `ORDER`
stage whose gate it belongs to (a frozen referee text: `TC12-REG.vendor`; a Stage D mirror: `TC12-D.mirror`).
**TEXT BEFORE RESULT** — six orderings, each checked:
- (T1) the commit that first adds `REGISTRATIONS.json` is an ancestor of every commit that first adds a file under a
  book directory (the directories the stage table's owners name for C, G, R, S, L, SCORE); and every book directory's
  `build_manifest.json` carries `registry_head` == `REGISTRY_PIN.json` `head` and `leans_sha256` == the frozen LEANS
  sha, both read by the builder from the files at build time. A builder HALTs when the registry is absent.
- (T2) every FITTED pin is committed before the first book that reads it: the traverse (TC12-V) before TC12-R and
  TC12-S (O-18).
- (T3) the fourth book's spec is committed before its first ride (O-24).
- (T4) the ferry's priority order and the report's "whole versus pointed-to" choice are LEANS text (L-L, L-X), so they
  are frozen at TC12-REG, before any verdict.
- (T5) no registered row's bootstrap of record is run before TC12-SCORE, and TC12-SCORE starts only when TC12-C, -G,
  -R, -S and -L are all COMPLETE-VERIFIED — no verdict is on the table while another registered book is being built.
- (T6) an amendment is committed before the artifact it changes is rebuilt.
- (T7) THE REBUILD LAW: once a registered row's regbook is filed, it is rebuilt only under a filed `AP-n` that names
  a build fact or a verifier's finding (L-0.5) — never because of what the book shows; the superseded regbook's sha
  and the AP id stay in the stage record's `notes`, and the superseded file is quarantined (L-0.4), not deleted.
SOURCE: `scripts/tierc12_progress.py:20-21` [read here]; the form `XR/tierc11x/REGISTRATION_PLAN.md:334-375` [read
here]; O-6, O-18, O-24; scout U9 H8.
RIVALS: score each family as its book completes — not taken: a verdict seen mid-build is the look the law forbids for
the rows still open. Stage D before REG (X's order) — not taken: `ORDER` as filed puts the texts first, and no
registration needs a bar (the pin is known by value, the lookbacks are read from `XR`, the traverse is cited by object).
FAILS-IF: **F-ORDER** (resume suite) FAILS IF, at `--at`, an ancestry of T1, T2, T3 or T6 fails
(`git merge-base --is-ancestor`); a book manifest lacks or mis-states `registry_head` or `leans_sha256`; a file under
the score directory is first added by a commit that is not a descendant of the commits adding the five regbook
manifests (T5); a regbook manifest's content sha changes between two `tierc12(` commits with no `AP-n` id in that
stage record's `notes` (T7). Planted mutations (scratch repos): a book manifest committed before the registry → RED;
a manifest whose `registry_head` is another hex → RED; the traverse pin committed after a range-book manifest → RED;
a regbook manifest changed in a second commit with no AP id → RED.

**L-0.11 THE SWEEP DRIVER** — "a stage is COMPLETE only if its … fixtures RE-PASS now" (TC10 contract :12-13, named
by contract :5 "verify-or-quarantine") and "F-DET hash-identical" (contract :123)
READING: No sweep driver exists in either predecessor (scout U9 §1.4); TC12 files one:
`scripts/tierc12_sweep_fixtures.py` (a fixture module: it may use `subprocess`, and it is outside the decision glob).
THE ROLL is a list of INVOCATIONS, never typed: for each stage in `ORDER`, the `suite` strings of that stage's fixture
records, in record order. TOTALITY: the set of script names in the roll equals the set of
`scripts/tierc12_*_fixtures.py` on disk minus the sweep itself. Each invocation runs once, sequentially (never two at
a time: suites spawn their own F-DET twins and workers under the O-5 cap), in a fresh process, with
`~/venvs/naiad/bin/python -B`, cwd = `M`, `PYTHONDONTWRITEBYTECODE=1`, `NAIAD_CACHE_DIR` = the absolute snapshot path
read from Stage D's manifest, `PYTHONHASHSEED` UNSET (hash randomisation left on, so an order-dependent transcript
shows as drift), no `--refile-transcript`, no leg filter. Before TC12-D is COMPLETE-VERIFIED the variable points at a
per-run scratch directory — never unset, never the future snapshot path (`engine/data.py:39-48` falls back to the live
cache when unset and `mkdir`s whatever it is given) — and the sweep asserts that directory is empty afterwards.
GREEN iff, for every invocation: exit code 0; the transcript's sha after == before == the record's
`transcript_sha_after`; no `_rerun.txt` or `_partial.txt` appeared; the transcript's tally line reads zero RED and its
GREEN count equals the record's `legs_total`. The sweep's own transcript `T12/sweep/FIXTURES_SWEEP_<STAGE>.txt` lists,
per invocation, the name, the tally and the transcript sha — no wall time and no load (those go to stdout and to
`T12/sweep/clock/<STAGE>.json`, which is not an artifact and which the gate copies into the progress record).
WHEN: the full sweep is of record at TC12-FIX, again at the `fix-head` of TC12-REVIEW, and once inside the
reproducibility lens with `--root=<scratch>`; an ordinary stage gate re-runs that stage's own invocations plus the
resume suite. SCOPE LAW for every fixture that enumerates "all modules" or "all tables" (resume, closure, typed, not,
sweep): it takes `--stage=<STAGE>` and its scope is the union of `artifact_shas` paths of stages up to that one, so
an earlier stage's transcript stays reproducible after later stages add files; the latest stage's run additionally
flags any matching file on disk that no stage records (UNRECORDED).
SOURCE: TC10 contract :12-13; scout U9 §1.4 ("there is NO sweep driver script in either tree"; the gate method
`XR/tierc11x/progress/X-FIX.json` `gate_method.no_refile`); `scripts/tierc11_closure_fixtures.py:1161-1171`, :1213-1222
[read here]; `engine/data.py:39-48` [read here]; `XR/tierc11x/LEANS_X_AMENDMENTS.md:561` (AM-X26, an enumerating
fixture turned RED by a later record).
RIVALS: a gate agent running suites by hand (both predecessors) — not taken: the roll and its result would live in a
session, not in the repo. A non-fixture python driver — not taken: it would need a subprocess allowance in the
decision glob.
FAILS-IF: **F-SWEEP** FAILS IF any clause of GREEN fails or totality fails. Planted mutations (scratch root with
shadow suites): a suite exiting 1; a transcript of record bent by one byte (a `_rerun.txt` must appear and be caught);
an unrolled `tierc12_zz_fixtures.py` on disk; a roll entry whose script is missing; an invocation run with a leg
filter (a `_partial.txt` appears) — each RED by its named detector.

---------------------------------------------------------------------------------------------------------------
### C · The other laws of lines 6-9

**L-0.12 READ-ONLY REVIEW WORKTREES · THE WORKTREE ATTESTATION** — "read-only review worktrees" (contract :6);
"worktree attestation" (contract :124)
READING: Two review events are attested, each in the form its object allows.
- **TC12-REVIEW (the built artifacts): the detached-worktree attestation, mandatory.** A lens without a GREEN record
  is not a review. Tool: `scripts/tierc12_worktree_attest.py`, a fork of `scripts/tierc11_worktree_attest.py` (its
  open/close protocol and findings kept) plus X's four clauses and two clauses neither predecessor had. Run by the
  ORCHESTRATOR from the main tree; the lens agent works inside the printed path between the two calls, exports the two
  env variables of O-5, returns its findings to the orchestrator and writes nothing in the worktree.
  `… tierc12_worktree_attest.py --commit <sha> --lens <name> --open` does, in order: (1)
  `git worktree add --detach M/.claude/worktrees/tc12-review-<lens> <sha>` (HALT if the path or an open record exists;
  the lens name must match the tool's `LENS_RX`; never a `wf_*` name); (2) copies into the worktree every
  `T12/**/*.parquet` of the main tree that is not under a `_det_*` directory and not under `x_rec/`, recording a
  per-file sha map; (3) copies read-only (mode `TC10_MODE`) exactly the frozen-estate records the lineage reads at
  import from its own tree — at least `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` (read by
  `tierc10_panel.resolve_unseen12()` at import, `scripts/tierc10_panel.py:322`), plus whatever `E.import_audit()` lists
  (L-D) — each held to the main tree's bytes; (4) reads the REVIEWED COMMIT's own record,
  `git show <sha>:research_outputs/tierc12/PROGRESS.json`, every stage's `artifact_shas` (the last stage recording a
  path governs), and files `STAGED != RECORD`, `STAGED NOT IN RECORD`, `RECORDED NOT STAGED`, `NO RECORD`; (5) records
  BEFORE with X's four clauses, each through `git --no-optional-locks -C <worktree>`: `rev-parse HEAD`;
  `rev-parse --abbrev-ref HEAD` (detached iff it prints `HEAD`); `status --porcelain=v1 --untracked-files=all`;
  `status --porcelain=v1 --ignored=matching` (its sha256 and line count); (6) X-REC clause: the main tree's `XR/` is
  verified against `XR/X_REC_MANIFEST.json`, whose own sha must be the one the reviewed commit's record certifies;
  (7) SNAPSHOT clause: a `(path, bytes, mtime_ns)` listing sha of the snapshot named by the reviewed commit's Stage D
  manifest. `… --lens <name> --close [--out-dir=DIR]` records AFTER the same way and is RED on any one of: HEAD ≠ the
  reviewed sha, or not detached, or porcelain non-empty, before or after; the ignored listing's sha after ≠ before
  (this is what catches a `__pycache__`); a staged file changed, vanished, or a staged-class file appeared; a staged
  estate record or its main-tree bytes moved; the X-REC verification failing at open or close; the snapshot listing
  sha moved; the worktree unreadable or not removed. It then removes the worktree and writes
  `T12/review/attest/<event>/<lens>.json` (`verdict`, `findings`, `fails_if`) in the MAIN tree, outside the reviewed
  tree. Exit 0 iff GREEN. `<event>` is `build` or `fix-head`. The set of lens names with a GREEN record must equal the
  set the judge record `T12/review/BUILD_REVIEW_<date>.json` names. `T12/review/attest/**` is typed out of every
  enumerating fixture's artifact class from the start.
- **TC12-LEANS (the readings): the hash-bound attestation, of record.** The reviewed object is text.
  `T12/review/WORKTREE_ATTEST_LEANS.jsonl` (X's `WORKTREE_ATTEST_REG.jsonl` form) holds a header (law, stage, the
  review JSON's path and sha); one `bind` record per reviewed file with `bytes`, `sha256`, the sha the review's last
  pass names, and — if bytes were appended after that pass — `bound_prefix_bytes`, `bound_prefix_sha256` and
  `appended_after_pass {bytes, sha256, what}`; and one `review` record per lens or pass naming its `cwd`, `head` and
  whether the reviewed files were tracked, or the literal `"not recorded"`. Where the orchestrator committed the draft
  before the review and a lens ran in a detached worktree at that commit, that lens's record also carries the tool's
  GREEN record path. Where it did not, the record says `detached: false`, and the report's findings carry the line
  "LEANS reviewed uncommitted: HASH-BOUND ONLY". In both cases the freeze binds bytes (L-0.5).
SOURCE: `scripts/tierc11_worktree_attest.py` (sha256 `96bfbab8…`; `STAGE_GLOBS` :65, `TC10_STAGED` :70, `state` :90,
`commit_record` :175, `wt_path` :239, `open_wt` :247, `close_wt` :277) [read here]; `XR/tierc11x/review/attest.sh`
(the four clauses, :24-37) [read here]; `XR/tierc11x/review/WORKTREE_ATTEST_REG.jsonl`, `WORKTREE_ATTEST.jsonl` [read
here]; `XR/tierc11x/LEANS_X.md:469-481` (LX-0.7) and :2317 [read here]; `T11/LEANS.md:531-535` (L-F.3) [read here];
`T11/review/attest/fidelity.json` (record shape) [measured here]; scout U9 §1.6, C2 ("Neither covers reads of X's
records or of a new snapshot"); AM-X26.
RIVALS: X's bash-only attestation for the build review — not taken: it cannot see whether the ignored parquet under
review are the bytes the commit records. Requiring the detached check for the LEANS review — not taken as the form of
record: the tool does not exist before the readings do, and X's filed precedent binds text by hash; the stronger form
is recorded when it happened and its absence is a printed finding, never a silent GREEN.
FAILS-IF: **F-ATTEST** (`scripts/tierc12_attest_fixtures.py`, on real scratch worktrees named
`tc12-review-fixture-<tag>`, removed by the tool) FAILS IF any RED class above is not caught by its named detector.
Planted mutations, one at a time: a tracked file touched; an untracked file created; a `__pycache__/x.pyc` created
(the ignored-listing clause must catch it); HEAD moved to another commit; a branch attached (`checkout -b`); a staged
parquet with one byte flipped; a staged parquet deleted; a new parquet of the staged class; a staged file whose sha is
not the record's at open; a staged estate record changed; one byte flipped in a scratch `x_rec` copy (the tool run
with `--xrec-root=<scratch>`); a file touched in a scratch snapshot copy. For the LEANS event: a one-byte edit to a
scratch `LEANS.md` after the last pass → the bind record's sha equality RED.

**L-0.13 AS-OF WARRANTY STAMPS** — "as-of warranty stamps" (contract :6)
READING: Every parquet TC12 writes carries the nine columns of `TP.AS_OF_COLUMNS`, non-null on every row: the four of
`tierc8.stamp` (`as_of_last_closed_4h`, `as_of_panel_start`, `as_of_span_days`, `warranty`) and the five `stamp_n`
adds (`as_of_lens`, `as_of_last_closed_bar`, `as_of_panel`, `as_of_n_assets`, `as_of_substrate`).
- **IMPORT, not mirror.** The stamps are `E.TP.stamp_n`, reached only through `put` from `E.TP.make_put(root, meta,
  lens)`, which writes through `TB.write_table`. The env door `scripts/tierc12_env.py` is the ONE TC12 module that
  imports `tierc10_panel`; every other module reaches it as `E.TP`. The import is held SAFE by four facts read from the source (sha256 `40b660cd…`) and re-proven by
  fixture: (i) the module imports only the lineage (`tierc9`, `tierc8`, `tierc7`, `tierc7_rules`, `tierc6`,
  `tierc6_rules`, `tierc5`, `tierc2_baseline`; :72-79) — not `tierc10_data`, not the census; (ii) its only
  import-time side effects are two `sys.path` inserts (:69-70) and `_U12 = resolve_unseen12()` (:322), a READ of
  `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` that HALTs on a broken record and writes nothing; (iii) its
  writers (`register` :1674, `_mark_scored` :1998, `run`'s manifest :2949) are functions whose default roots lie
  under `research_outputs/tierc10` (:96-101) and which TC12 never calls; (iv) `tierc2_baseline` binds its tape paths
  at import from `NAIAD_CACHE_DIR` (`scripts/tierc2_baseline.py:205-206`).
- **The wrapper.** `scripts/tierc12_tables.py` `make_put(root, meta, lens)` HALTs unless `root` resolves under `T12`,
  `meta` carries `last_closed_4h_close`, `panel_start`, `span_days`, `panel_name`, `n_assets` and `substrate` (so
  `stamp_n`'s fallbacks at :2551-2553 — "CLASSIC5", `len(CLASSIC5)`, `substrate()` — are never what stamps a table),
  and `lens` is a key of `TP.LENS_MS` (:2511-2512); it then returns `E.TP.make_put(...)`. No non-fixture TC12 source
  calls `.to_parquet`, `TB.write_table` or a `TP` registry door directly.
- **What each column says.** `meta` is the corridor meta of the build that produced the rows — the dict
  `E.TP.corridor_n(panel, pin_close_iso)` returns (:650-733). A table of the scored window is stamped with the SCORE
  EDGE (`pin_close_iso` = TC11's pin); a strip table, a VA table and every table that reads past the score edge is
  stamped with the PIN (L-0.7). `as_of_lens` is the lens of the row's own clock (the bar whose close is the row's
  instant: 4h for a v6-derived book, 5m for the scalper's orders, the lens itself for a per-bar VA table);
  `as_of_last_closed_bar` is `lens_edge(hi, lens)` (:2515-2525; 1w Monday-anchored), or the tape's own measured edge
  passed as `lens_last_closed_ms` when the tape ends earlier — `stamp_n` HALTs if an edge falls after the corridor end
  (:2546-2548). A table whose rows belong to another panel than the build's is stamped with its own `meta_` (:2573-2576).
  A member of another lens carried on a row (the V5 vector) carries that member's own bar-close column (L-V names it);
  the nine stamps do not stand in for it.
- **Manifests.** Every directory holding parquet has one `build_manifest.json` written by the same helper: `sha`
  (content sha per table), `keys`, `skipped_empty`, `input_sha`, `seed`, `as_of`, `substrate`, `code_sha`,
  `contract_sha256`, `leans_sha256`, `registry_head`, `amendments_of_record`, `pins` — sorted keys, and none of
  `TP.VOLATILE_META` (:625) or any other clock field.
SOURCE: `scripts/tierc10_panel.py:2510-2588` [read here]; `scripts/tierc8.py:96-111` [read here];
`scripts/tierc2_baseline.py:155-188` [read here]; the import facts at the lines cited [read here];
`XR/tierc11x/LEANS_X.md:431-436`, :482-483 [read here]; O-3, O-5; scout U9 §1.7.
RIVALS: MIRROR the nine columns into TC12 code, held equal by reading `AS_OF_COLUMNS` with `ast` — not taken:
`tierc10_panel` is in every TC12 process regardless (the control ride, the corridor and the book sha are its
functions), so a mirror removes no import and adds a second implementation of `lens_edge` that F-KEY, which checks
names and nulls, could not tell from the first. Import `tierc10_panel` directly in each builder — not taken: one door.
FAILS-IF: **F-WARRANTY** (`scripts/tierc12_tables_fixtures.py`) FAILS IF (a) IMPORT-SAFETY: in a fresh subprocess, a
`(path, bytes, mtime_ns)` census of `research_outputs/tierc10`, `research_outputs/tierc11`, `scripts/`, `analytics/`
taken before and after `import tierc12_env` differs, or the hook's write log is non-empty, or the set of frozen-estate
files opened at import is not the typed one; (b) `E.TP` is not the module loaded from `scripts/tierc10_panel.py` at the
sha L-D pins, or `E.TP.AS_OF_COLUMNS` is not the fixture-typed tuple; (c) the wrapper accepts a root outside `T12`, a
`meta` missing a required key, or an unknown lens; (d) AST: a non-fixture TC12 source other than the env door imports
`tierc10_panel`; any calls `.to_parquet` / `write_table` outside the wrapper, or calls a `TP` registry door. Planted mutations: a `put` bypass
(`df.to_parquet(...)`) in a shadow builder → (d) RED and the table fails F-KEY; a `meta` without `substrate` → (c)
RED; a shadow env that writes a file under `research_outputs/tierc10/` at import → (a) RED; a scored-window table
stamped with the pin instead of the score edge → RED under F-KEY's stamp-truth leg (L-0.21).
UNVERIFIED: fact (ii) says which estate file the import reads when run alone; what `import tierc12_env` reads in full
depends on L-D's import windows and is established by leg (a) at TC12-ENV.

**L-0.14 EVERY FIXTURE LEG STATES ITS FAILURE CONDITION** — "every fixture leg states its failure condition"
(contract :6-7); "FIXTURES (each states its failure condition)" (contract :114)
READING: One harness, `scripts/tierc12_fx.py` (stdlib only), a COPY — never an import — of the harness of record in
`scripts/tierc11_closure_fixtures.py`: `say` (deterministic line → transcript, temp paths scrubbed), `clock` (stdout
only), `prove(fid, title, break_if, real_if, break_leg, real_leg)`, `plants(rows)`, `file_transcript(out, body,
refile)` and the `main` protocol.
- **The leg law.** Every fixture is one `prove` call. The BREAK leg runs first and must go RED, or the fixture is VOID
  and counts RED; a break leg that raises proves nothing (VOID). A break leg is `plants(rows)`, rows =
  `(name, expected detector substring, thunk → findings)`, judged ONE AT A TIME: caught only if a finding NAMES THE
  INTENDED DETECTOR; no finding = the plant passed (VOID); a crash = a FIXTURE DEFECT (VOID); a `SystemExit` is a
  finding carrying its own text. The transcript prints, for every fixture: `<FID> — <title>`,
  `  [BREAK] FAILS IF: …`, `  [BREAK] deliberate violation -> RED (correct): …`, `  [REAL]  FAILS IF: …`,
  `  [PASS|FAIL] <FID>: …`, and the tally `  N GREEN, M RED`.
- **BANNED:** self-comparison; one example where cardinality was possible; a check whose claim is not the design's
  claim. **Production against production:** a sabotage is planted INSIDE the production function (a shadow copy of
  the source, or a monkeypatched object in the production call path), never in the comparator; a leg whose two sides
  are both fresh oracles tests nothing in production. Hook legs run in subprocesses. Truncated-tape legs build fresh
  arrays, never through a symbol-keyed memo. An as-of leg that holds a fitted pin holds it at its filed value on every
  prefix and says it does not test the fit.
- **Hand-verified samples** ("3 … hand-verified", contract :117-120) are chosen by a rule fixed in the owning
  section's text before any book exists, never after a look: for a requirement with named categories, the first row
  of each category in ascending `(asset, instant_ms)` order (an empty category prints NONE-EXISTS and asserts the
  book's count of it is zero); for an uncategorised sample, `numpy.random.default_rng(<tier seed>)` draws over the
  key-sorted population. The transcript prints the rule and the chosen keys.
- **Fixture-typed literals are a second object.** A fixture types its own commission (expected cells, columns, names,
  the pin line) and compares production against it; it never reads the production module's own constant as its
  referee. Each suite prints its typed literals in its header.
- **Transcripts** are `T12/<dir>/FIXTURES_<X>.txt`; first line `as_of_last_closed_4h: <pin ISO>`, then the banner and
  `seed … · substrate … · pin …`. They carry no clock, no temp path, no absolute home path, no source line number, no
  worker count, no load, no live HEAD. NO-CLOBBER: an absent transcript with no `--refile-transcript` is a finding and
  nothing is written; identical bytes are silent; different bytes without the flag go to `<stem>_rerun.txt`, the
  record untouched, RED; a leg-filtered run writes `<stem>_partial.txt`. Exit 1 on any RED, VOID or transcript finding.
  "Byte-identical across runs" is held by four runs of every transcript in fresh processes with hash randomisation on:
  the filing run, the stage gate's re-run, the TC12-FIX sweep, and the reproducibility lens's re-run.
- Every stage that runs a fixture files a transcript, and its progress record carries the sha before and after.
SOURCE: `scripts/tierc11_closure_fixtures.py` (sha256 `68253ed1…`): the law :73-84, `say` :169-172, `clock` :175-176,
`prove` :183-204, `plants` :207-238, `file_transcript` :1161-1171, `main` :1174-1222, `AS_OF_LINE` :115 [read here];
`XR/tierc11x/LEANS_X.md:2282-2299` (LX-F.1) and :2309 (the key-order selection rule of F-SFP) [read here]; O-3 (why a
copy: importing that file runs `import tierc11_env`, which arms TC11's hooks).
RIVALS: import TC11's harness — not taken: O-3. A pytest suite — not taken: no BREAK-first law, and pytest writes
caches into the tree.
FAILS-IF: **F-FX-MIRROR** (closure suite) FAILS IF `ast.dump` of `say`, `clock`, `prove`, `plants` or
`file_transcript` in `scripts/tierc12_fx.py` differs from the same function parsed from the TEXT of
`scripts/tierc11_closure_fixtures.py` (its sha asserted from the census). **F-FX-FORM** FAILS IF, by AST over every
`scripts/tierc12_*_fixtures.py`, a `prove` call has an empty `break_if` or `real_if`, a `plants` row is not a triple
with a non-empty detector string, or a fixture's break leg is not a `plants` call; or a transcript of record has a
fixture block lacking either `FAILS IF:` line. Planted mutations: `plants` in a harness copy changed to count a crash
as a catch → F-FX-MIRROR RED; a `prove(…, break_if="", …)` in a suite copy → RED; a transcript copy with one
`[REAL]  FAILS IF:` line removed → RED.

**L-0.15 EVERY GRID PRINTED WHOLE · F-GRID** — "every grid printed WHOLE" (contract :7); "F-GRID counts asserted"
(contract :123)
READING: A GRID is any table whose rows are the cells of a declared cross of axes (the contract's: the breadth ×
own-band grid :59, the crossed table :60, the VA chop table :68, the two-trades conditioning :76-79, and every other
table an owning section declares as a cross).
- **Declared.** The builder declares `AXES` — an ordered mapping axis → tuple of levels, each level an enum string or
  a value read by object, never a typed number — and derives the cell list as the product in axis order; the cell id
  is the `¦`-joined `axis:level` tokens (the filed form: `age:on¦win:on¦ratr:off`, `T11/stage_g/STAGE_G.md:197`). The
  declared count is the product of the axes' cardinalities, COMPUTED. A cell that cannot exist by construction is
  still a row, with `n = 0` and `nan_reason = "absent by construction: <why>"`.
- **Empty cells are printed.** A cell with no member is a row with `n = 0`, every statistic NaN and a non-null
  `nan_reason`; it is never dropped.
- **Asserted, against a second object.** The fixture types the axes' levels, the full cell list and the count, and
  calls `TP.grid_whole(declared=<the fixture's list>, written, cell_col="cell", require_cols=<n, the collar columns,
  the nine stamps>, require_false=("promotable",))`: exact set equality, no duplicate, no extra, lengths equal. It
  also asserts the fixture's count == the product of the fixture's cardinalities == the builder's computed count; for
  a grid that partitions a population, Σ `n` over its cells == the population's row count read from the book; and no
  grid holds a verdict column.
- **Printed whole.** Wherever a grid is printed in a document of record (a stage document, the draft), every cell is
  printed — no top-k, no ellipsis, no filtered view. The table is preceded by the marker
  `<!-- grid: <ID> cells=<count read from the parquet> -->` and has exactly that many data rows with the parquet's
  cell ids. A document may point to a per-row file by path and sha (rows are not a grid); a grid is never abbreviated.
SOURCE: `scripts/tierc10_panel.py:2592-2625` (`grid_whole`) [read here]; `XR/tierc11x/LEANS_X.md:485-486`, :2315 (F-GRID
row; "NaN without `nan_reason`") [read here]; `T11/stage_g/STAGE_G.md:197` [read here].
RIVALS: print only non-empty cells — not taken: a missing cell and an empty cell would look alike. Type the count in
the builder — not taken: the builder would then assert its own number.
FAILS-IF: **F-GRID** (helper legs in `tierc12_fx.py`, run by each owning stage's suite per grid) FAILS IF a cell is
missing, undeclared or duplicated; a count equality fails; a partition's Σ `n` differs from the population; a
statistic is NaN without `nan_reason`; a collar or stamp column is absent or null; `promotable` is True on any row; a
verdict column exists; a printed grid's row count or cell ids differ from the parquet's. Planted mutations (copies): a
dropped cell; an added cell; a duplicated cell; an `n = 0` row removed; a NaN with its `nan_reason` nulled;
`promotable = True` on one row; one member row moved to no cell (partition off by one); a printed table with one row
deleted — each RED.

**L-0.16 THE SELECTION COLLAR** — ""a SELECTION, not a result" on every non-registered table" (contract :7)
READING: A REGISTERED table is a table a frozen reading names as a row of record: the five score rows of §0 (contract
:126), each registered row's regbook of record and its base arm, and the mirror's licence record if L-V names it so.
The typed list `REGISTERED_TABLES_T` is assembled from those readings at freeze. EVERY OTHER parquet TC12 writes — the
9/12 book, every twin, shadow, slice and strip, every Tier-E grid, the per-bar VA and nest tables, the traverse
table, the ledger and era tables — carries the collar; the tables helper HALTs on a table that neither carries it nor
is on the typed list.
- **The helper** is `collar(df, would, m)` in `scripts/tierc12_tables.py`, a mirror of X's `collar` with one column
  added. It writes, in this order: `tier = "TIER-E"`; `selection_not_a_result = "a SELECTION, not a result"`;
  `gates = "nothing"`; `would_read_ci_only`; `m_looks_this_table` (the count of CI-bearing cells in that table);
  `m_note` (X's sentence, verbatim); and `promotable = False`. X carried `promotable` on grids only; the contract's
  "no promotion from any Tier-E table" (:133) names every table, so TC12 carries it on every collared table.
- **`would_read_ci_only`** takes one of TC11's four values and nothing else: "CI above zero (lo > 0)", "CI includes
  zero", "CI wholly below zero (hi < 0)", "no interval". A descriptive table prints no interval ("no interval",
  `m_looks_this_table` zero); a scorer-computed Tier-E row prints its CI-only reading (L-0.28). No collared table
  holds a verdict word or a column named for a verdict, a cleared bar or a spent test.
- **In documents**, every markdown table is preceded, within the three lines above its header, by the registered
  marker `<!-- registered: <id> -->` (score documents and §0 only) or by the line
  "TIER-E — a SELECTION, not a result — gates nothing". A Tier-E statistic printed INSIDE a §0 row carries that string
  inline.
SOURCE: `XR/scripts/tc11x_exit.py:1175-1185` (`collar`), `XR/scripts/tc11x_books.py:131-138` (`M_NOTE`, `COLLAR`,
`COLLAR_COLS`) [read here, as text]; `scripts/tierc11_score.py:258-263` (`COLLAR`, `CI_READINGS`, the forbidden key
pattern) [read here, as text]; `XR/tierc11x/LEANS_X.md:814-830` (LX-1.4) [read here]; `T11/LEANS.md:128-131` [read
here]; scout U1 §1.12 (TC11 collared a per-campaign Tier-E table, `g_campaign_gates.parquet`).
RIVALS: TC11's three-column dict — not taken: it drops `m_looks_this_table`, the record of how many ways the tape was
cut. Collar only aggregate tables (X's practice for journals) — not taken: a copied row of a Tier-E twin would carry
no mark, and a blanket rule with a typed exemption list is checkable by totality; it cannot flatter.
FAILS-IF: **F-COLLAR** (helper legs, run per directory by each stage's suite, and a mirror leg in the tables suite)
FAILS IF a parquet not on `REGISTERED_TABLES_T` lacks a collar column, holds a null in one, a `would_read_ci_only`
outside the four values, `promotable` True, or a verdict-like column; a table on the typed list carries the collar; a
document table has neither marker nor collar line; the helper's column tuple, its SELECTION string or its `m_note`
differ from `COLLAR_COLS`, `COLLAR["selection_not_a_result"]` and `M_NOTE` read by `ast.literal_eval` from the TEXT of
`XR/scripts/tc11x_books.py` (never executed), or its `tier` / `gates` strings and the four readings differ from
`COLLAR` and `CI_READINGS` read the same way from `scripts/tierc11_score.py`. Planted mutations (copies): a collar
column dropped; `would_read_ci_only = "SUPPORTED"`; `promotable = True` on one row; a `verdict` column added; a
document table with its collar line deleted; the helper's `m_note` changed by one word — each RED.

**L-0.17 NO NUMBER TYPED THAT A FILE CAN SUPPLY** — "no number typed that a file can supply" (contract :8); also
"F-TRAV greps for typed constants → FAIL" (:43) and "F-TOLL (maker bps read, never typed …)" (:121)
READING: Every number a TC12 non-fixture source uses comes through a DOOR from the file that supplies it. The doors:
- **The contract** — `scripts/tierc12_pins.py`, reading the prefix (L-0.1) with the filed map
  `T12/pins/CONTRACT_PIN_MAP.json`: one row per pin, `{pin, lines [a, b], regex (one capture group), type ∈ {int,
  fraction, word, iso, str}, word_map (for a word such as "half", contract :71), also [{lines, regex}], veto}`.
  Values are parsed exactly (`fractions.Fraction` on the captured text) and converted to float only at the use site.
  Where a value stands in two places of the contract (a stage line and the VETOES line :135-137, or a family header's
  bar and "0.10 ÷ m" :9), `also` holds the second citation and the pin door HALTs unless both parse to one value. The
  derived values are filed as `T12/pins/CONTRACT_PINS.json`; at every run the pin door re-derives them from the prefix and
  HALTs unless equal to the filed file. The map is DATA, so no contract line number is typed in code.
- **X's records** — e.g. the lookbacks `XR/tierc11x/pins/PINS_X.json` `L.by_lens.<lens>.L_of_record` (O-15), each
  read with its sha asserted against the manifest.
- **Stage D's records** — the pin, the tick (`price_tick`, O-20), the fee schedule's bps (O-19).
- **Fitted pins** — the traverse (O-18), read by object from its frozen record.
- **Lineage objects** — read by attribute, never retyped: `RC.ATR_LEN` (`scripts/tierc2_rules.py:121`),
  `RC.WARMUP_BARS`, `TP.N_BOOT` (`scripts/tierc10_panel.py:94`), `TP.LENS_MS` (:2511), `TP.ERA_CUT_MS` (:747),
  `P.PROFILE_ROWS` and `P.VALUE_AREA` (`analytics/profile.py:21-22`), the write rounding's decimals (the default of
  `TB._round_floats`' `nd`, `scripts/tierc2_baseline.py:162`, read from the signature). Where the contract also states
  such a value (70% of volume, :29, against `P.VALUE_AREA`), the lineage object is what code reads at run time and the
  pin door asserts the two equal.
`T12/pins/PIN_REGISTER.json` lists every pin of every door: `{pin, source, door, consumers [stage], witness}`.
**THE ALLOW-LIST** (the reading's own definition of "not a number a file can supply"; these literals parameterise no
book, and they are the one place this section fixes numbers no file states): in a scanned source an `ast.Constant` of
type `int` or `float` (bool excluded; complex always a finding) is permitted only if (A) it is STRUCTURAL — the
integers 0, 1, 2 or the floats 0.0, 1.0 (index, arity, sign, identity) — or (B) it is the whole right-hand side of a
module-level assignment in `scripts/tierc12_units.py`, whose name → value map must EQUAL the fixture-typed table
`UNITS_T` = {`PCT_PER_UNIT`: 100, `BPS_PER_UNIT`: 10000, `BYTES_PER_MB`: 1000000} (the third is X's filed reading of
"2 MB" as decimal megabytes, `XR/scripts/tc11x_ferry.py:177`); that module holds nothing else, and the table moves
only by a dated amendment. Additional rules: (C) a sub-expression built only from numeric literals must fold to a structural
value (no `2 * 2 * 2`); (D) a numeric string handed to `int`, `float`, `Decimal`, `Fraction`, `np.float64`,
`json.loads`, `ast.literal_eval` or `eval` is a finding; (E) a parameter default is a literal like any other; (F)
PRESENTATION — a numeric literal anywhere inside an f-string's subtree (a clip such as a short sha, a width) renders
text and is not scanned; (G) REFEREED TEXT — a literal inside vendored text proven byte-identical to its committed
referee outside the declared hunks, or inside a function proven AST-identical to its filed source, is the referee's
and is held by that equality fixture (L-D's F-VENDOR and port legs; F-FX-MIRROR here); a literal inside a declared
hunk is scanned like any other.
SCOPE: `analytics/value_area.py` and every COMPUTATION module — every non-fixture `scripts/tierc12_*.py` that is
neither a process tool nor a renderer. PROCESS TOOLS are a typed, closed list whose exemption is EARNED: the fixture
proves by AST that each imports none of `tierc12_env`, `numpy`, `pandas`, the lineage or `analytics`, so it cannot
compute on a bar — `scripts/tierc12_fx.py`, `tierc12_progress.py` (filed at R0; its one number is the header's seed
label, held equal to the contract pin by F-RESUME), `tierc12_worktree_attest.py`, `tierc12_frozen.py`. RENDERERS (the
close generator's modules, named by L-X) are held on their OUTPUT instead: L-X's trace law requires every digit of §0
and of the append to re-derive from a record. Fixture modules are exempt by law (L-0.14: the commission is typed).
Consequence for `analytics/value_area.py`: its functions take every parameter as a required keyword argument with no
default, and it holds structural literals only.
**THE LIMIT, stated before the build:** the structural set collides with these contract pins — the rail's 1.0 (:71,
:98), the fill's 1 tick (:94), the family counts m = 2 and m = 1 (:52, :64, :82), the breadth cut's numerator 2
(:58) and the ferry cap's 2 (:112). The static scan cannot tell a typed copy of those from structure. They are held
by the FLOW leg alone.
**THE FLOW LEG.** For every contract pin and every fitted pin in the register, the consuming stage's suite bends the
pin AT ITS DOOR, inside production (the loaded pin object monkeypatched, the comparator untouched), re-runs the
smallest production function that reads it on a seeded sample, and requires the output to move as the register's
`witness` says. A pin whose bend moves nothing is `PIN-NOT-READ`.
**TOTALITY of the contract.** Every digit run in the prefix's operative lines is either inside one map row's capture
or listed in `T12/pins/CONTRACT_TOKENS_UNPINNED.json` with its class (an id such as a registration or stage label, a
date, a prior, a hand-sample count, a quoted history figure).
SOURCE: contract :8, :43, :121; `XR/scripts/tc11x_sfp_fixtures.py:970-1035` (`_numeric_literal`, `kin_ast`),
:1440-1500 (`x2_T_literals`, `trav_flow` — the bend-in-production precedent), `XR/scripts/tc11x_ranges_fixtures.py:671-695`
(`typed_pin_literals`) [read here, as text]; the lineage objects at the lines cited [read here]; O-15, O-18, O-19,
O-20, O-22 ("parsed from the contract's stage headers, never typed"); scout U9 §1.8 (constants of
`publish_exchange.py` read by `ast.literal_eval`, never imported).
RIVALS: X's site-targeted scans only (named argument positions) — not taken as the whole law: they catch a typed time
stop but not a typed threshold elsewhere; kept as each owning fixture's extra leg (F-TRAV, F-TOLL). Ban every numeric
literal — not taken: unbuildable (indices). A larger structural set — not taken: each added value hides one more pin.
FAILS-IF: **F-TYPED** (closure suite, AST, `--stage` scope) FAILS IF a scanned source holds a numeric literal that
none of (A), (B), (F), (G) permits, violates (C)-(E), `tierc12_units.py` differs from `UNITS_T`, or a process tool's
exemption is unearned. **F-PINS** (pins suite) FAILS IF the pin door's
re-derivation differs from `CONTRACT_PINS.json`, an `also` citation disagrees, a map row's slice sha moved, or a digit
run of the operative lines is unaccounted. **F-TYPED-FLOW** (each consuming stage's suite) FAILS IF a bent pin moves
nothing or moves the wrong thing; **F-TYPED-TOTAL** (at TC12-FIX) FAILS IF a registered pin has no GREEN flow leg.
Planted mutations: a `0.25` typed in a copy of a stage module → F-TYPED RED; `float("1.5")` → RED; `K = 2 + 1` → RED;
a default `def f(n=8)` → RED; an extra row in a `tierc12_units.py` copy → RED; `import numpy` added to a copy of a
process tool → UNEARNED RED; a literal typed inside a declared hunk of the vendored shim → RED (rule (G) does not
cover hunks); a map row deleted → F-PINS RED
(unaccounted token); a regex changed to capture the neighbouring number → F-PINS HALT; a pin replaced by a typed
literal of EQUAL value inside a shadow copy of its consumer → the bend moves nothing → `PIN-NOT-READ` RED (this is
the leg that holds the colliding pins).

**L-0.18 FAMILIES BY MECHANISM** — "families declared by MECHANISM before the look, each independently failable, bar
= 0.10 ÷ m per family; a registration closed by precondition spends no test." (contract :8-9)
READING (law level; the statistic, the verdict words and F-FAM's legs are L-X's, under O-22):
- **The families are the contract's three stage headers** — ADMISSION (:52), RANGE-STATE (:64), SCALPER (:82). Name,
  m and the header's own bar are parsed from those three lines and q from :9 by the pin door, which HALTs unless
  each header's bar equals q ÷ m exactly (fractions) and the number of registration ids standing under each header
  (:53, :57 · :65, :69 · :83) equals that header's m. Nothing is typed.
- **"Declared by mechanism before the look"** = two filings, both before any book: the contract at STEP Q, and the
  registry at TC12-REG, where each of the five payloads carries its `mechanism` paragraph. F-ORDER (T1) proves the
  order.
- **"Each independently failable"** = each row is scored alone against its own family's bar; no row's verdict reads
  another row's statistic; there is no best-of and no pooled family statistic; a family's bar does not change with
  the number of tests actually run.
- **"Closed by precondition spends no test"** = a row whose filed precondition is not met writes STATUS only: no
  bootstrap is run for it, its cell carries no number, m and the bar stand (O-22).
SOURCE: contract :8-9, :52, :64, :82; O-22; `T11/LEANS.md:122-124` (the conservative argument) [read here];
`XR/tierc11x/LEANS_X.md:721-724` [read here]; scout U7 R3.
RIVALS: bar = q ÷ (rows actually scored) — not taken: it loosens the bar after a closure. One family of five — not
taken: the contract declares three.
FAILS-IF: **F-FAM** is L-X's. Its parse leg is fixed here: FAILS IF the pin door's parsed (family, m, bar, ids) differs
from the fixture-typed referee table, or a header's bar ≠ q ÷ m. Planted mutations: a header copy reading a different
bar → the pin door's HALT; a registry copy scoring a SCALPER row at an ADMISSION bar → RED.

---------------------------------------------------------------------------------------------------------------
### D · The cross-cutting fixtures of the FIXTURES line

**L-0.19 THE CONTRACT'S FIXTURE LIST IS A TOTALITY** — "FIXTURES (each states its failure condition): F-CTRL
0.000e+00 cross-process · F-D-2/3 · … · F-KEY · import-closure · worktree attestation." (contract :114-124)
READING: Every fixture the contract names on :114-124 exists under its contract name, as at least one fixture block
in a transcript of record, PASS at TC12-FIX, with both `FAILS IF:` lines. The names are parsed from the prefix by the
pin door (tokens of the form `F-<NAME>`, the pair written `F-D-2/3` read as two, and the two unprefixed names
`import-closure` and `worktree attestation`) and compared with a fixture-typed referee list. Owners: F-CTRL (L-C);
F-D-2, F-D-3 (L-D); F-VA-ASOF, F-VA-RAW, F-VA-MIRROR, F-STATE, F-TRAV, F-NEST-ASOF (L-V); F-GATE, F-BRD (L-G); F-DIR,
F-SFP (L-R); F-SCALP, F-TOLL (L-S, on L-D's fee file); F-LEDGER (L-L); F-FAM (L-X); F-DET, F-GRID, F-KEY (the law here
— L-0.20, L-0.15, L-0.21 — and one instance per directory or grid in each owning stage's suite); import-closure
(L-0.22: F-CLOSURE, F-HOOK-ESCAPE, F-WALL); worktree attestation (L-0.12: F-ATTEST and the records). A contract name
maps to its blocks by a typed pattern table (TC11's form: the name `import-closure` matches blocks whose id starts
`F-CLOSURE`). Fixtures the readings add beyond the contract's are listed after them in the report's roll, never mixed
in.
SOURCE: contract :114-124; `scripts/tierc11_close.py:2021` (the name → pattern table) [read here];
`XR/tierc11x/LEANS_X.md:2301-2302` ("The contract's twelve come first, then the ones these readings need") [read here].
RIVALS: let each section rename its fixtures freely — not taken: a reader holding the contract could not find them.
FAILS-IF: **F-ROLL** (sweep suite, at TC12-FIX) FAILS IF the parsed name list differs from the referee, a contract
name matches no fixture block in any transcript of record, or a matched block is not PASS. Planted mutations: a
transcript copy with its F-TRAV block removed → RED; a contract-prefix scratch copy with one fixture name added →
RED (parse ≠ referee).

**L-0.20 F-DET** — "F-DET hash-identical" (contract :123)
READING: TC10's variant (i), per parquet directory, as TC11 and X ran it. For every directory a stage writes parquet
into, the suite runs the stage's builder twice, each in a fresh subprocess that imports `E` before any I/O, into
`<dir>/_det_<stage>/seed_<s>/` (git-ignored), under `PYTHONHASHSEED` = "1" (TC11 L-F.1's first twin) and
`PYTHONHASHSEED` = the tier seed. THE TIER SEED DRIVES EVERY RULER IN BOTH TWINS; only the interpreter's hash seed
differs. GREEN iff: both exit 0; the file set of each twin equals the fixture-typed file set and the canonical
directory's; every file is byte-identical twin to twin and twin to canonical; every parquet's content sha
(`TB._content_sha`: sha256 of `to_csv(index=False)` of the table as written — floats rounded to the lineage's
decimals, mergesorted by its declared key) is equal; `TP.check_det(twin, canonical)` is GREEN on the directory's
manifest (same table set, no content sha moved, an independent byte re-hash of every parquet pair, equal `input_sha`);
and no clock-like key or column exists in any manifest or parquet — a worker count or a load average counts as a
clock (the name pattern is the fixture-typed copy of X's `CLOCK_NAME_RX`). Seeded draws (the scorer's persisted
bootstrap draws) are parquet like any other and are held byte-equal. Documents of record that a builder renders
(stage `.md`) are in the file set.
SOURCE: `T11/LEANS.md:520-521` (L-F.1) [read here]; `XR/tierc11x/LEANS_X.md:2314` [read here];
`XR/scripts/tc11x_books_fixtures.py:203-204` (`CLOCK_NAME_RX`), :1629-1765 (the implementation and its four plants)
[read here, as text]; `scripts/tierc10_panel.py:2661-2689` (`check_det`) [read here];
`scripts/tierc2_baseline.py:155-188` [read here].
RIVALS: one in-process double build — not taken: it shares the interpreter's hash seed and memo state. Compare
content shas only — not taken: the bytes are the output; the sha is the build's claim about them.
FAILS-IF: **F-DET** (helper legs in `tierc12_fx.py`; one instance per parquet directory in the owning stage's suite)
FAILS IF any clause of GREEN fails. Planted mutations: one byte bent in a copy of a rendered document; one float moved
by one unit of the last rounded decimal in a parquet copy (the content sha must move); an `elapsed_s` field planted
in a manifest copy; a HASH-ORDER plant — a builder twin that appends a line built from iterating a `set`, run under
the two hash seeds, whose bytes must differ — each RED by its named detector.

**L-0.21 F-KEY** — "F-KEY" (contract :124)
READING: F-KEY has three filed meanings and TC12's is their union. (1) Origin: a join key must be DECLARED and UNIQUE
before the join (`TB.assert_key`, which HALTs inside `write_table`). (2) TC10's TOTALITY over one output root
(`TP.check_keys`): every parquet in the directory has a declared key in that directory's `build_manifest.json`; no
manifest key lacks its table (a ghost); no key duplicates; every table carries every as-of column, none null. (3)
TC11's and X's COMMISSION: per table the fixture types the key, the column list in order, the required (non-null)
columns and the null-iff flags, and holds the manifest's content sha equal to `TB._content_sha` of the table read
back. FOR TC12, per parquet directory (the lineage's checker globs `root/*.parquet` without recursion): all of (1)-(3),
plus STAMP TRUTH — `as_of_n_assets` equals the number of assets of the panel the table declares and `as_of_panel`
names it; `as_of_last_closed_4h` is the edge L-0.13 assigns that table (the score edge or the pin); `as_of_substrate`
is the Stage D manifest's snapshot name — plus COLLAR TOTALITY (L-0.16) on the same pass.
SOURCE: `scripts/tierc2_baseline.py:191-201` [read here]; `scripts/tierc10_panel.py:2628-2658` [read here];
`scripts/tierc10_panel_fixtures.py:3122-3232` (the stamp-truth leg: "a 17-asset table is stamped as_of_panel=CLASSIC5")
[read here]; `scripts/tierc11_books_fixtures.py:102-111` [read here]; `XR/scripts/tc11x_books_fixtures.py:1530-1600`
[read here, as text]; `XR/tierc11x/LEANS_X.md:2316` [read here]. The contracts name F-KEY without defining it (TC10
:126, TC11 :94, TC12 :124).
RIVALS: `TP.check_keys` alone — not taken: it checks names and nulls, not that a stamp is TRUE of the rows, nor the
column list.
FAILS-IF: **F-KEY** (helper legs; one instance per parquet directory) FAILS IF a table is undeclared, a declared key
is a ghost or duplicates, a stamp column is absent or null, a typed-required column holds a null, a nullable column's
nulls disagree with its typed flag, the column list is not the typed one, a manifest content sha is not the table's,
or a stamp is untrue. Planted mutations (copies): a duplicated row; `as_of_last_closed_4h` dropped; a required column
nulled on one row; a null-iff column filled where its flag says null; an undeclared parquet added to a scratch root;
a manifest copy with a ghost key; a 17-asset table copy stamped with the five-asset panel; a scored-window table copy
stamped with the pin — each RED by its named detector.

**L-0.22 IMPORT-CLOSURE AND THE MEANING OF "DECISION MODULE"** — "STAGE V · THE VALUE AREA, MODULE-IZED
(analytics/value_area.py; decision modules import NOTHING from it — import-closure extends to it)" (contract :25-26);
"import-closure" (contract :124)
READING: Three registered rows decide ON value-area state (P-DIR-1 :65-66, P-SFP-VA-1 :69-73, P-SCALP-3 :85-98), and
the contract forbids decision modules to import the module that computes it. The two hold together under TC11's
filed closure law, extended by one name: **value-area state enters decision code only as DATA** — as columns of the
filed Stage V tables, or as arrays a typed RUNNER obtains from a door's verified accessor — never as a call into the
module. Three classes, by typed lists:
- **THE GLOB** = every `scripts/tierc12_*.py` whose stem does not end `_fixtures`.
- **DOORS** (`DOORS_T`) = the only modules that import `analytics.value_area`. Its members are the Stage V door
  scripts L-V names (at drafting: `scripts/tierc12_va.py` and `scripts/tierc12_va_stamps.py`); L-V's names govern, and
  no glob pattern stands in for the typed list. A door's place must be EARNED — its source imports the module — or it
  is a hole. A door trades nothing: no table it files holds a column of `TRADE_COLS_T` (`net_r`, `gross_r`, `fee_r`,
  `funding_r`, `entry_px`, `stop_px`, `exit_reason`).
- **RUNNERS** (`RUNNERS_T`) = modules that import a DOOR and never the module. A runner's place must be EARNED (its
  source imports a door) and it is bound by three conditions: (R-i) it touches the door only through the typed
  accessor names `ACCESSORS_T` that L-V files (at drafting `pins`, `cell`, `licence`, `traverse`, `stamp`) — any other
  attribute of the door is a finding; (R-ii) its own source holds no import of, and no name or attribute equal to,
  `value_area` or `volume_profile`; (R-iii) every value-area fact it uses is one the accessor has held equal to the
  filed table (L-V's accessor law: recompute, pass through the write function, HALT unless every row equals the
  table), so nothing reaches a trade that is not on file. Runners are named by their owning sections and are limited
  by `NEVER_RUNNER_T` below: only a builder of a VALUE-AREA TRADE (the P-SFP-VA-1 book, the P-SCALP-3 book, Stage R's
  Tier-E value-area tables) may be one — "nothing else may trade a range" (contract :41).
- **DECISION MODULES** = every member of the glob that is neither a door nor a runner. A module the fixture does not
  name defaults to DECISION and is scanned. For a decision module the contract's sentence holds in its strong form:
  neither the module nor a door is in its import closure, directly or transitively. `NEVER_RUNNER_T`, typed here, are
  the modules that MUST be decision modules: the env; the tables, as-of and pin helpers; the data stage; the v6
  control and book builders (the card's ride stays value-area-blind, as the lineage stayed range-blind); the gate
  builders of P-ADM-1, P-BRD-1 and P-DIR-1 (gates are post-filters, O-21: P-DIR-1 reads the 4h state as a filed stamp
  column); the ledger; the registry; the scorer; the close generator.
- **FORBIDDEN to every decision module, and to the lineage it imports:** by exact name `analytics.value_area`,
  `analytics.profile`, `analytics.rangefinder_census`; by substring `rangefinder`, `tierc10_census`, `tierc10_stamps`,
  `tierc10_null`, `tierc11_nest`. FORBIDDEN to every member of the glob, doors and runners included: those five
  range-machine substrings and `analytics.rangefinder_census` (a constant of the range machine is read from its
  source text, never by import), and any module whose name starts `tc11x_` (O-4) or `tierc11_` (O-3; TC12's shim is a
  vendored copy, L-D). The package `analytics` itself and its
  `vwap`, `volatility`, `structure`, `momentum` submodules ARE in every process (the lineage imports them:
  `scripts/tierc2_baseline.py:79-82`), so the ban is by exact submodule, never on `analytics`.
- **Five legs.** (i) FRESH INTERPRETER, one per decision module: after `import <module>`, `sys.modules` holds no
  forbidden name, no door and no runner, and the module loaded from `scripts/<name>.py`. This leg is what catches a
  TRANSITIVE reach — a decision module importing a door or a runner. One interpreter per runner too: the only
  forbidden names it may hold are `analytics.value_area` and `analytics.profile`, and only because a door loaded them.
  (ii) AST over each decision source and the static repo closure of its imports:
  no `Import` / `ImportFrom` of a forbidden name anywhere (function bodies included); no constant-string
  `import_module` / `__import__`; no non-constant import site other than a door L-D declares; no `exec` / `eval` /
  `compile`; no `sys.modules` reach; no attribute chain or `getattr` ending in `value_area` or `profile` on a name
  bound to the `analytics` package; no `.top` / `.bottom` read of a range object. (iii) DATA-ONLY: outside the doors,
  no TC12 source holds an `ast.Name` whose id, or an `ast.Attribute` whose attr, EQUALS `volume_profile` or
  `value_area` (string constants and path literals are not names and are not scanned); in a runner, every attribute
  read on a door's alias is a member of `ACCESSORS_T`; no module of `NEVER_RUNNER_T` is in `RUNNERS_T`.
  (iv) HOOK-ESCAPE over every member of the glob: `E.hook_escapes(src)` finds nothing —
  no pyarrow-native I/O, no os-level out-of-process call — and `subprocess` appears only at the typed call sites
  `SUBPROC_SITE_T`: the attestation tool's one `git` helper (subcommands within `worktree`, `rev-parse`, `status`,
  `show`) and whatever single site L-D declares for the snapshot clone. (v) THE ANALYTICS WALL on
  `analytics/value_area.py`: `numpy` is its only non-stdlib import, and of the stdlib it imports only members of the
  fixture-typed no-I/O set `VA_IMPORTS_T` (`__future__`, `dataclasses`, `typing`, `math`, `enum`) — O-15's "numpy
  only" read as "nothing of the repo, nothing third-party but numpy, nothing that performs I/O"; the two scans of
  `tests/test_analytics.py` (no `engine` import :124-127; none of its banned I/O tokens and no `open(` call :147-160)
  find nothing, re-implemented by the fixture as its own object; `analytics/__init__.py` is byte-unchanged and holds no
  `value_area` token; `value_area.py` is not in `_MODULES` (read by `ast.literal_eval` from `analytics/__init__.py:118-120`);
  and `analytics_sha()` recomputed by the fixture's own loop equals the value printed in `analytics/INTERFACE.md:8-9`.
SOURCE: contract :25-26, :124; O-15; `scripts/tierc11_closure_fixtures.py:9-47` (the decision-set law, earned
exemptions, the default), :118-124, :144-148, :246-248, :293-309 [read here]; `scripts/tierc11_env.py:1200-1255`
(`hook_escapes`) [read here]; `XR/scripts/tc11x_books_fixtures.py:194-201` (`FORBIDDEN_EXACT_TYPED`) and
`XR/tierc11x/LEANS_X.md:384-405` (why `analytics` cannot be banned whole; "only `tc11x_va` imports `analytics.profile`")
[read here]; `tests/test_analytics.py:120-160` [read here]; `analytics/__init__.py:118-136` [read here];
`analytics/rangefinder_census.py` precedent (scout U9 §1.5); scout U9 C3, U9-12, U9-13.
RIVALS: (a) "decision module" = only the three modules that trade on VA state — not taken: a typed inclusion list
leaves every new module outside the scan; the glob-minus-typed-exemptions rule fails closed. (b) FILE-ONLY — no
runner at all; every consumer reads filed columns — not taken: tables are rounded at write (L-0.13), so a level read
back from a table can sit on the other side of a close that equals it to the last decimal (the round trap L-V
documents), and the only cure — a second, exact representation of every level in the tables — has no filed
precedent, while the runner form is TC11's filed and reviewed law. It stays the stricter alternative, and it is what
the gates use. (c) X's form — the closure covers the card's path only and a value-area trade builder imports the
module itself — not taken: a builder holding the module can profile any window it likes; under (R-i)-(R-iii) it can
only read what Stage V filed. (d) ban `analytics` whole (X's leg (ii)) — not taken: it could never pass on the lineage.
FAILS-IF: **F-CLOSURE** (`scripts/tierc12_closure_fixtures.py --stage=<STAGE>`; legs (i)-(iii)), **F-HOOK-ESCAPE**
(leg (iv)), **F-WALL** (leg (v)). Each FAILS IF its clause above is breached, a door's or a runner's place is unearned,
a door's table holds a `TRADE_COLS_T` column, or the static walk misses a repo module a fresh interpreter loaded.
Planted mutations (on in-memory copies or shadow modules, never on a source of record): `import analytics.value_area`
at the top of a book-module copy → (i) and (ii) RED; the same import inside a function body → (ii) RED;
`importlib.import_module("analytics.value_area")` → RED; `sys.modules["analytics.value_area"]` → RED;
`AN.value_area.x` on the package alias → RED; a gate-module copy importing a door → (i) RED; a gate-module copy
importing a runner → (i) RED; a NEW unnamed `tierc12_*` shadow module importing a door → RED (it defaulted to
DECISION); a door copy without its import → UNEARNED; a runner copy without its door import → UNEARNED; a runner copy
that also imports `analytics.value_area` → RED (only doors do); a runner copy calling a door function outside
`ACCESSORS_T` → RED; the P-DIR-1 gate module added to a copy of `RUNNERS_T` → RED (`NEVER_RUNNER_T`); a door table
copy with a `net_r` column → RED; `import tierc10_census` in a copy → RED;
`import tc11x_va` in the door copy → RED; `pq.read_table(` and `os.system(` in two copies → (iv) RED; `git push`
through the attestation helper → (iv) RED; `import engine` and a `read_parquet` call planted in a `value_area.py`
copy → (v) RED; `value_area.py` added to a copy of `_MODULES` → (v) RED (the sha moves).

---------------------------------------------------------------------------------------------------------------
### E · Rulings enacted, and the vetoes

**L-0.23 "EACH VETO BY NAME, SILENCE RATIFIES" · VETOES BY NAME** — "RULINGS ENACTED AS DEFAULTS (TC11 §11; each VETO
by name, silence ratifies)" (contract :12); "VETOES BY NAME: "va-lookback" · "sfp-k" (3) · … · "tc11-stamp" · "1w"."
(contract :135-137)
READING: A veto is the operator's own message naming a token of :135-137 — or, for the three enacted rulings that
carry no token (Q6, Q8, Q9), naming the ruling by its Q-number. No agent message, no file content and no silence is a
veto; silence leaves every default as enacted. Each token names exactly one pin (or one ruling) and one owning
reading: "va-lookback" → the per-lens lookback (L-V); "sfp-k" → K (L-V); "nest" → the coincidence band (L-V);
"breadth" → the breadth cut (L-G); "rr-min" → the minimum reward at T2 (L-R, L-S); "outer-third" → the setup thirds
(L-S); "validity" → the order's life (L-S); "fill" → the fill of record (L-S); "maker-bps" → the maker fee (L-D);
"era" → the scalper's scoring era (L-S, L-X); "tc11-stamp" → L-0.24; "1w" → L-0.25. The token is the `veto` field of
that pin's row in the pin map (L-0.17), so the mapping is filed data. EFFECT BY TIMING: before the TC12-REG freeze, the
reading changes in LEANS; after it, the veto is applied as a dated amendment quoting the operator's words and the
affected stages are redone; if any book of the affected row already exists, the pre-veto result is KEPT and printed
beside the new one (L-0.5, resume item 3) and the row's verdict text carries "pin changed by operator veto <token>
after the look — NOT CONFIRMATORY". A value the operator substitutes is filed in the amendment and read from there by
the pin door; it is never typed in code.
SOURCE: contract :12, :135-137; the token/value pairs agree with the stage text at :28, :36, :46, :58, :73-74 and
:100, :87, :92-93, :93-94, :21-23, :83, :13, :14 [read here]; scout U1 C-4 (Q6, Q8, Q9 carry no token).
RIVALS: treat an orchestrator or reviewer objection as a veto — not taken: the contract gives the veto to the operator.
Apply a post-look veto silently — not taken: it cannot be told from tuning.
FAILS-IF: **F-VETO** (pins suite) FAILS IF a token of :135-137 has no pin-map row or two; a token's parenthesised
value (where the line gives one) does not parse equal to its stage-text citation; an amendment that changes a pin
names no operator quote. Planted mutations: a map copy with the "sfp-k" row's `veto` cleared → RED; a contract-prefix
scratch copy where the VETOES line's value differs from the stage line → the pin door's HALT.

**L-0.24 Q1/Q2 · "tc11-stamp"** — "Q1/Q2 keep SCORES.json leaves; stamp TC11 BUILT and re-pin its registry files
["tc11-stamp"]" (contract :13); O-10.
READING:
- **Q1.** No byte of `T11/scores/SCORES.json` moves in TC12. Its sha is the R0 value
  (`T12/progress/TC12-R0.json` `frozen_estate_shas_at_r0`), re-asserted at every gate (F-FROZEN), at CLOSE and inside
  the cascade below. The leaves added since the lens reviews stand as filed (`T11/BUILD_DRAFT.md:5943`). No TC11
  scorer is run in place, with or without `--refile` (O-3).
- **Q2 — when and by whom.** During the build no TC11 byte moves. The stamp and the re-pin are steps of TC12's
  `close_acts.sh`, after its step 0 has proven the TC10, TC11 and X blocks landed by bytes in that order (O-12): they
  are the operator's keystrokes.
- **Q2 — where.** One line, APPENDED as the last line of `exchange/queue/2026-09-24_TC11_APOLLO.md` (the file is 103
  lines and ends in a newline [measured here]): `BUILT: <TC11's report path under exchange/reports/> · <the tierc11(
  commits, read from git at the act>` — the queue README's rule-6 form in the shape of the filed exemplars. Lines 1
  to the present last line stay byte-identical, so the nine `text_lines` slices, their contexts, the nine payload shas
  and the chain head do not move.
- **Q2 — what moves.** "Its registry files" = the bytes that pin the contract's WHOLE-FILE sha and are checked by a
  TC11 verifier — the smallest set under which TC11's own registry verifier passes on the stamped file: (a)
  `T11/registrations/REGISTRATIONS.json`, the one leaf `contract.sha256` (outside every payload and the chain),
  replaced in place and asserted byte-equal to a fresh render of the same document in the filer's form (the filer is
  write-once and is not run); (b) `T11/registrations/REGISTRY_PIN.json` `contract_sha256`; (c) the typed constants
  `scripts/tierc11_registrations.py:24`, `scripts/tierc11_score.py:220` and :224, `scripts/tierc11_score_fixtures.py:263`,
  `scripts/tierc11_stage_g.py:170`, `scripts/tierc11_stage_t_brk.py:141`; (d) `T11/scores/REGISTRY_CHECK.json` and the
  other records TC11's own scorer regenerates from those pins — regenerated in the scratch clone and carried into the
  main tree as proven post-images, behind the assertion that `SCORES.json`, `FAMILY.json` and `BASE_IDENT.json` are
  byte-identical before and after; (e) the transcripts and manifests that print a moved sha, likewise; (f)
  `T11/PROGRESS.json` (`contract_of_record`, the STEP Q artifact sha and line, `registrations_of_record`, and the
  shas of everything moved). Every other quote of the old sha — the data records, `scripts/tierc11_data.py:174`,
  `scripts/tierc11_nest.py:640`, docstrings, stage documents, TC11's published report, X's records — is HISTORICAL:
  untouched and listed.
- **Q2 — the proof.** At TC12-CLOSE the executor runs the whole cascade in a SCRATCH CLONE of the repository outside
  both trees (the ignored TC11 parquet staged into it as the attestation tool stages them), never in the main tree,
  and files `T12/close/TC11_STAMP_PROOF.txt` and `T12/close/TC11_STAMP_MAP.json` (old → new sha for every moved file;
  the historical list). GREEN = the invariances above, plus every suite of TC11's last sweep (the list read from
  `T11/PROGRESS.json` `stages[*].fixtures[*].suite`) exiting 0 in the clone. `scripts/tierc11_close.py` and its
  fixtures are outside the cascade and their HALT is printed as EXPECTED: that generator refuses a contract that
  already carries a `BUILT` line (`scripts/tierc11_close.py:960-961`). The mechanics — the prove and apply phases of
  the stamp script, its ALLOWED and NEVER-moved sets, and the rule that no TC11 code runs in the main tree (the act
  copies proven post-images) — are L-X's reading of the same phrase; this reading fixes what any mechanics must meet.
- **Q2 — if the proof is not GREEN,** `close_acts.sh` carries NO stamp step, the map is filed with `applied: false`,
  the report's findings read "tc11-stamp NOT APPLIED: <first RED>", and the ruling returns to the operator. No partial
  re-pin is ever written.
SOURCE: contract :13; O-10, O-12; `T11/BUILD_DRAFT.md:5943`, :5945, :5989 (Q2's own words name three files) [read
here]; the pins at the script lines cited [measured here: `grep` of the two shas]; `T11/registrations/REGISTRY_PIN.json:3`,
`T11/scores/REGISTRY_CHECK.json:4`, :158 [read here]; `scripts/tierc11_registrations.py:244-246` [read here];
`scripts/tierc11_score.py:2648-2652` [read here]; `exchange/queue/README.md:8-12` and the exemplar stamps (scout U1
§1.6); scout U1 R-1..R-5.
RIVALS: (a) the literal three files of Q2's sentence — not taken: `REGISTRY_PIN.json` and five typed constants would
stay at the old sha, TC11's scorer and score fixtures would go RED on their next run, and "re-pin" would be false of
TC11's own check. (b) the stamp under the RATIFIED block, where the exemplars sit — not taken: it shifts every line
cite (O-10). (c) no TC11 byte moves, a sibling record only — that is the veto's outcome and the not-GREEN outcome,
not the default. (d) stamp during the build — not taken: O-10.
FAILS-IF: **F-TC11-STAMP** (legs defined here; hosted by the close suite, L-X) FAILS IF, after the cascade in a
scratch clone: (i) any line up to the contract's pre-stamp last line differs; (ii) a payload sha or the chain head
differs; (iii) `SCORES.json`, `FAMILY.json` or `BASE_IDENT.json` differ by a byte; (iv) a moved file is absent from
the map or a mapped file did not move; (v) a file outside (a)-(f) moved; (vi) a swept TC11 suite exits non-zero.
Planted mutations: the stamp INSERTED at line 3 → (i) and (ii) RED; one byte of `SCORES.json` flipped in the clone →
(iii) RED; one typed constant left at the old sha → (vi) RED (the scorer's HALT); an extra TC11 file touched → (v) RED.
UNVERIFIED: that TC11's swept suites all re-pass after the re-pin. Nothing but the scratch-clone run at TC12-CLOSE
establishes it.

**L-0.25 Q4 · "1w"** — "Q4 accept 1w FAIL (provisional) as closing 1w for range trading ["1w"]" (contract :14); O-11.
READING: 1w is closed for range trading in TC12 and no re-measure is ordered. (i) No trade, order, setup or
event-outcome row of any range form — the swing failure, the breakout-retest, the 1d-edge take-profit venue, the
scalper — has lens 1w, registered or Tier-E. (ii) No feasibility row and no licence word exists for 1w (the mirror's
five words name none: contract :39-41). (iii) The 1w member of the V5 vector (:45) is a CAPTURED-ONLY stamp: printed
on funnel instants under the collar, read by no gate, no permission, no direction guard, no conditioning axis.
SOURCE: contract :14, :39-41, :45; O-11; `T11/stage_r/R2_LENS_VERDICTS.json` key `lenses.1w` (the provisional FAIL)
and finding FN-TRD-17 (scout U1 §1.2, §1.11).
RIVALS: print a 1w cell in the Tier-E two-trades tables "for completeness" — not taken: a closed lens gets no cell.
FAILS-IF: **F-NOT, leg 1W** (L-0.30's suite) FAILS IF a table holding a trade, order or event-outcome column has a
row whose lens is 1w; a decision module's typed list of VA columns read holds a 1w column; or a runner calls an
accessor with the 1w lens. Planted mutations: a 1w
row added to a range-table copy → RED; a condition on the 1w state added to a gate copy → RED.

**L-0.26 Q6 · THE CLOSE ACTS** — "Q6 the close acts remain the operator's keystrokes" (contract :14-15); O-12.
READING: The executor WRITES `T12/close/close_acts.sh` and never runs it: its only executions are `bash -n` and its
step 0 against scratch repositories outside both trees (X's F-CLOSE-SCRIPT form; L-X). The executor never runs
`git push`, `git merge` or `publish()`, never moves a report under `exchange/`, never appends to
`exchange/status/LEDGER_APOLLO.md`, never runs or patches a predecessor's `close_acts.sh` (the `-f` patch TC10's
script needs is the operator's). TC12's step 0 requires the TC10, TC11 and X blocks by bytes in that order. "STATE
push" (contract :130) is the result the script prints and a stamp bracket in the report filled at the act. What this
ruling cannot reach is stated in L-0.9: the daily routine's push.
SOURCE: contract :14-15, :130; O-12; `T11/LEANS.md:537-542` (L-F.4) and `XR/tierc11x/LEANS_X.md:2480-2502` (LX-C.5)
[read here]; scout U1 §1.7 (the three scripts, none run), H-2.
RIVALS: none taken; running any step "to test it" in the main tree is the act itself.
FAILS-IF: **F-NOT, leg ACTS** FAILS IF any TC12 source, fixtures included, holds an argv or shell string whose git
subcommand is `push` or `merge`, an `import publish_exchange` (its constants are read as text), a call named
`publish`, or a subprocess whose argv names a `close_acts.sh` other than under `bash -n` or with a cwd asserted
outside both trees. Planted mutations: `git(["push", "origin", …])` in a copy of the attestation tool → RED;
`import publish_exchange as p` in a copy of the close generator → RED; `subprocess.run(["bash", <the main tree's
close_acts.sh>])` in a fixture copy → RED.

**L-0.27 Q8 · NO POST-HOC CANDIDATE** — "Q8 post-hoc candidates lie, EXCEPT the combined refusal, pre-named here from
TC11's crossed table and labelled pre_seen" (contract :15-16); O-13.
READING: (i) The two candidates TC11's reviews named (`T11/BUILD_DRAFT.md:5995`) are not registered, not re-run and
not printed with a verdict word in TC12. (ii) TC12's registry holds exactly the five ids the contract names (:53,
:57, :65, :69, :83); nothing found in a TC12 Tier-E table is registered, promoted or given a verdict word in this
tier, and the close append carries the standing line that a later registration drawn from a TC12 Tier-E table is
`pre_seen` on TC12's bars (the form X filed). (iii) P-ADM-1 is the one exception: pre-named from the cell
`age:on¦win:on¦ratr:off` of `T11/stage_g/STAGE_G.md:197` — the contract's "cell 110 @ +0.515" (:55) names that row
by its kept count and its mean — and labelled `pre_seen` (O-23; the label text is L-G's and L-X's).
SOURCE: contract :15-16, :55; O-13, O-23; `T11/BUILD_DRAFT.md:5995` [read here]; `T11/stage_g/STAGE_G.md:197` [read
here]; `XR/tierc11x/LEANS_X.md:2468-2470` [read here]; `T12/DISCLOSURES.md` D-4.
RIVALS: register the best Tier-E cell found during the build as a sixth row "labelled pre_seen" — not taken: the
exception is the contract's one, named before the look.
FAILS-IF: **F-NOT, leg POST-HOC** FAILS IF the set of ids in the filed registry is not the fixture-typed five; a
collared table holds `promotable` True or a verdict word. Planted mutations: a sixth payload in a registry copy → RED;
a Tier-E row copy carrying a verdict word → RED.

**L-0.28 Q9 · VISIBILITY AND TIER-E INTERVALS** — "Q9 ratify the executor's readings of L-W.4 / L-W.1." (contract
:16); O-14.
READING: Two laws carry into TC12.
- **Visibility (L-W.1, read as ≤).** A quantity of lens L — a bar's values, an indicator at that bar, a VA row stamped
  at that bar — is visible at instant τ iff that bar's CLOSE ≤ τ. The index law, implemented once in
  `scripts/tierc12_asof.py` and used by every cross-lens join in TC12:
  `asof_index(closes_ms, τ) = numpy.searchsorted(closes_ms, τ, side="right") − 1`, with `closes_ms = open_ms +
  TP.LENS_MS[L]`; the result is −1 (nothing visible) before the first close; a bar closing EXACTLY at τ is visible;
  a bar still forming is never read. It is a mirror of `tierc10_census.asof_index`, which a decision module may not
  import (L-0.22). τ is the instant the owning reading names. This is not the lineage's exec-open law
  (`engine.htf.map_htf_to_exec`: higher-lens close ≤ the exec bar's OPEN), which stays as it is inside the v6 ride
  and is not used for any new TC12 join.
- **Tier-E intervals (L-W.4, scoped by L-1.4, as TC11 built both).** A scorer-computed Tier-E row prints its
  interval's CI-only reading in `would_read_ci_only` and no verdict word; a descriptive stage table prints no interval.
SOURCE: contract :16; O-14; `T11/LEANS.md:302-304` (L-W.1), :324-339 (L-W.4), :128-131 (L-1.4) [read here];
`scripts/tierc10_census.py:894-900` [read here]; `T12/scout/U6_range_scalper_machinery.md:282-289` (the two as-of
laws differ by one bar at a boundary) [read here]; scout U1 §1.3 (both readings were built side by side).
RIVALS: strict `<` — not taken: Q9 ratifies `≤`. Import `tierc10_census.asof_index` — not taken: it is the range
machine's module. Print an interval on every Tier-E table — not taken: Q9 ratifies L-W.4's scope.
FAILS-IF: **F-ASOF** (tables suite) FAILS IF (a) on seeded instants per lens pair, `asof_index` differs from a
from-scratch linear scan for the last close ≤ τ; (b) at a τ equal to a higher-lens close, the lower-lens bar closing
at τ is not the one returned; (c) production against production: a join's output on full tapes differs from its
output on tapes cut at τ. Planted mutations, inside the production function: `side="left"` → (b) RED;
`closes_ms = open_ms` (the bar still forming is read — L-W.1's own sabotage) → (a) and (c) RED.

**L-0.29 Q3, Q5, Q7 — NOT ENACTED BY NAME** — the contract enacts "Q1/Q2 … Q4 … Q6 … Q8 … Q9" (contract :13-16) and
is silent on TC11 §11's Q3, Q5 and Q7 (`T11/BUILD_DRAFT.md:5990`, :5992, :5994).
READING: "Silence ratifies" covers the rulings the contract enacts, not the three it does not name; each stays an
open operator question, carried to the report, with a default the build takes.
- **Q3** (does slippage join the toll of record?) — stays open. Default: the charter-slippage twin is printed beside
  every row and never instead of the toll of record (contract :23 "taker and charter tiers unchanged"; :102).
- **Q5** (re-root the forward ledger so it can refresh) — enacted in fact, not by name, by Stage D's new snapshot and
  pin, Stage L's re-ride (contract :108-110) and O-24 (TC12's own ledger file opened on the bytes of X's; TC11's and
  X's never appended in place). The report says "in fact, not by name".
- **Q7** (align the X lane's vendored env shim with TC11's, or keep the lanes apart) — default: apart. TC12 runs one
  env of its own (L-D), imports no `tc11x_` and no `tierc11_` module (L-0.22), mirrors what it needs of X (O-4), and
  prints the shim difference X disclosed as a disclosure, not a decision.
SOURCE: contract :12-16; `T11/BUILD_DRAFT.md:5986-5996` [read here]; O-4, O-24; scout U1 C-3, R-10.
RIVALS: read the silence as ratifying TC11's leans on all nine — not taken: the contract lists which it enacts.
FAILS-IF: n/a (definition); the three questions are rows of the report's open-questions section, and F-NOT's legs
hold the two defaults that are code (no foreign-tier import, L-0.22; the twin beside, L-X).

---------------------------------------------------------------------------------------------------------------
### F · The refusals

**L-0.30 WHAT THIS IS NOT → F-NOT** — "WHAT THIS IS NOT: no entry-cross research · no trail-offset tuning · no adds ·
no pivot-range trades · no 5m signal source · no new assets by list · no SAIL act · no promotion from any Tier-E
table · no re-family of TC11." (contract :132-134; the drafting brief cites :130-132, which are CLOSE's last lines)
READING: Each clause is a refusal with a detector. `scripts/tierc12_not_fixtures.py --stage=<STAGE>` runs the AST legs
from TC12-ENV on and the DATA legs over the tables in scope (L-0.11's scope law); a data leg with no table in scope
prints "NO TABLE IN SCOPE" and is not counted GREEN until TC12-FIX, where every leg must have a table.
- **ENTRY-CROSS.** The only roles objects a TC12 ride uses are the two filed ones: v6's (`T9.V6_ROLES`) and the 9/12
  book's (the second forward book; roles as filed in `T11/books/build_manifest.json` key `roles`). The scalper's 5m
  EMA pair (:89) is timing, one pair, read from the pin door. FAILS IF a non-fixture source constructs or
  `dataclasses.replace`s a roles object with an EMA period, or iterates candidate periods; or a book table's distinct
  `roles_name` values are not within the two filed names. Mutations: a `replace(T9.V6_ROLES, …)` with a period
  keyword in a copy → RED; a book-table copy with a third `roles_name` → RED.
- **TRAIL-OFFSET and ADDS.** Every v6-derived ride in TC12 (control, strip, gated books, ledger books, Tier-E v6
  twins) uses a card whose `TP.ride_spec(card, roles)` fields equal the FILED card fields
  (`XR/tierc11x/forward/BOOK_SPECS.json` `books.v6.ride_spec`, the same dict TC10 filed) on every key of the
  fixture-typed `TRAIL_FIELDS_T` (`anchor_offset`, `trail`, `trail_extra_buf_atr`, `trail_l`, `trail_r`,
  `trail_min_advance_atr`, `trail_arm_after_r`) and `ADD_FIELDS_T` (`adds_max`, `add_size`). The range
  trades have no trail (:73, :100): a range or scalp trade's stop never moves after entry and its position never
  grows. FAILS IF a ride's spec differs on such a key; a non-fixture source passes one of those names as a keyword or
  assigns it; a v6-derived journal has `n_adds` above zero on any row; a range or scalp trade row shows a stop move
  or a second entry fill (the columns L-R and L-S name). Mutations: `replace(TP.CONTROL_CARD, anchor_offset=…)` in a
  copy → RED; a journal copy with one `n_adds` raised → RED; a range-trade copy with a moved stop → RED.
- **PIVOT-RANGE.** No TC12 module — no door and no runner either — imports the range machine (L-0.22's substring list, plus
  `engine.rangefinder`), and every range trade's edge is a VA edge of the filed Stage V table at its as-of bar.
  FAILS IF such an import exists anywhere in the glob, or a range trade row's edge price is not the VAH or VAL of its
  as-of VA row. Mutations: `import tierc10_census` in a door copy → RED; a trade-row copy whose edge is shifted off
  the VA level → RED.
- **5m SIGNAL SOURCE.** 5m data may serve only the scalper's TRIGGER timing (:89-91), fills, the walk of stops,
  targets and the time stop, the as-of clock and the miss accounting. No 5m-native structure or indicator originates
  a signal: there is no 5m value area, range, pivot or tide; the only 5m indicator is the trigger's EMA pair; 5m
  prices may be compared with 1h and 4h level columns and with order prices. FAILS IF (a) a 5m kline path appears in
  the env hook's open log of a stage build outside the typed list `FIVE_MIN_READERS_T` — TC12-D, TC12-S, and any
  stage whose owning reading declares at freeze a 5m WALK read (the resolution of same-bar order) and names it; (b) a
  Stage V table holds a 5m lens; (c)
  the scalper source's `ema`-family call sites are not exactly the fixture-typed two, or any has a literal period;
  (d) the scalper's PERMISSION column (:85-86), recomputed by the fixture from the filed 1h and 4h VA tables in a
  process that opens no 5m file, differs on any row. Mutations: a 5m tape load planted in a shadow copy of a range
  module run in a subprocess → (a) RED; a third `ema` site in a scalper copy → (c) RED; a permission clause reading
  a 5m EMA state in a shadow scalper → (d) RED.
- **NEW ASSETS BY LIST.** The universe is read, never typed: the five home assets by object (`TP.CLASSIC5`), the
  twelve by Stage D's manifest as resolved from TC10's Stage D table (:20). FAILS IF a non-fixture source holds a
  string constant that equals a symbol, stem or asset name of the manifest's admission rows or matches the venue
  symbol pattern; the snapshot's or the manifest's stem set differs from TC11's certified set; an asset outside it
  appears in any table. Mutations: a typed symbol string in a copy → RED; a table copy with an eighteenth asset → RED.
- **SAIL.** FAILS IF `exchange/queue/008_sail-skeleton.md` moved from its census sha, a `tierc12(` commit touches it,
  or a TC12 source holds a path naming the SAIL repository or that work order as a write target. Mutations: one byte
  appended to a scratch copy → RED; a planted `Path.home() / "naiad-sail"` write in a copy → RED.
- **PROMOTION.** L-0.16 and L-0.27: `promotable` False on every collared table; exactly five registry ids; no verdict
  word outside the five rows. Mutations as there.
- **RE-FAMILY OF TC11.** FAILS IF TC11's `FAMILY.json`, `REGISTRATIONS.json` or `SCORES.json` moved (F-FROZEN; the
  close-act re-pin of L-0.24 moves only whole-file contract-sha pins and proves m, the bar, the payloads and the head
  unmoved); a TC11 registration id appears in TC12's registry; or a TC12 table prints, for a TC11 id, anything but
  TC11's filed verdict cell quoted from `SCORES.json` by JSON path with TC11's own bar. Where the contract asks for a
  TC11 row as a shadow ("OLD alone · stale alone", :56), a recomputation on TC12's bar is a collared Tier-E row with
  no verdict word (`T12/DISCLOSURES.md` D-4 names the hazard). Mutations: a shadow-row copy carrying a verdict word
  for a TC11 id at a TC12 bar → RED; a registry copy holding a TC11 id → RED.
- **1W, ACTS, POST-HOC** — the legs of L-0.25, L-0.26, L-0.27 live in the same suite.
SOURCE: contract :132-134, :56, :73, :85-91, :100; the 29 filed card fields `XR/tierc11x/forward/BOOK_SPECS.json`
`books.v6.ride_spec` and `research_outputs/tierc10/registrations/P-TRG-2.json` `book_spec.arms[0].ride.card_fields`
(`T12/scout/U3_env_books_control.md:14`); `scripts/tierc9.py:119` (`V6_ROLES`) [read here],
`T11/books/build_manifest.json` `roles` (scout U3 :12-15); the journal schema's `n_adds` column (scout U3 :96);
`scripts/tierc11_env.py:1160-1162` (`opened_paths`) [read here];
`exchange/queue/008_sail-skeleton.md` (scout U1 §1.10); O-11, O-13.
RIVALS: a prose "what this is not" section in the report only (both predecessors) — not taken: the contract lists
refusals; a list nobody checks refuses nothing.
FAILS-IF: **F-NOT** — the legs above, each with its failure condition and its planted mutations.

---------------------------------------------------------------------------------------------------------------
### The suites this section defines

| suite (invocation) | fixtures | transcript | first filed |
|---|---|---|---|
| `scripts/tierc12_resume_fixtures.py --stage=<S> --at=<sha>` | F-CONTRACT · F-RESUME · F-FROZEN-TEXT · F-FROZEN · F-ONE-CORRIDOR · F-OFFBUS · F-COMMIT · F-PROGRESS · F-ORDER | `T12/resume/FIXTURES_RESUME_<S>.txt` | TC12-REG |
| `scripts/tierc12_pins_fixtures.py` | F-PINS · F-VETO · the parse leg of F-FAM | `T12/pins/FIXTURES_PINS.txt` | TC12-REG |
| `scripts/tierc12_closure_fixtures.py --stage=<S>` | F-CLOSURE · F-HOOK-ESCAPE · F-WALL · F-TYPED · F-SEED · F-FX-MIRROR · F-FX-FORM | `T12/closure/FIXTURES_CLOSURE_<S>.txt` | TC12-REG (AST legs); TC12-ENV (fresh-interpreter legs) |
| `scripts/tierc12_tables_fixtures.py` | F-WARRANTY · F-ASOF · the helper and mirror legs of F-COLLAR, F-GRID, F-KEY, F-DET | `T12/env/FIXTURES_TABLES.txt` | TC12-ENV |
| `scripts/tierc12_attest_fixtures.py` | F-ATTEST | `T12/closure/FIXTURES_ATTEST.txt` | TC12-ENV |
| `scripts/tierc12_not_fixtures.py --stage=<S>` | F-NOT (nine clauses + 1W, ACTS, POST-HOC) | `T12/closure/FIXTURES_NOT_<S>.txt` | TC12-ENV |
| `scripts/tierc12_sweep_fixtures.py --stage=<S>` | F-SWEEP · F-ROLL (at TC12-FIX) | `T12/sweep/FIXTURES_SWEEP_<S>.txt` | TC12-ENV |
| each stage's own suite (owned by its section) | per parquet directory: F-KEY · F-DET · F-COLLAR; per grid: F-GRID; per pin consumed: F-TYPED-FLOW | the stage's transcript | that stage |

F-TYPED-TOTAL and the full F-SWEEP are of record at TC12-FIX. F-TC11-STAMP is hosted by the close suite (L-X).

---------------------------------------------------------------------------------------------------------------
### REGISTRATION SPEC

None. L-0 owns no registered row. The five rows are specified by their owners: P-ADM-1 and P-BRD-1 (L-G), P-DIR-1 and
P-SFP-VA-1 (L-R), P-SCALP-3 (L-S); the family law they share is L-0.18 and L-X.

---------------------------------------------------------------------------------------------------------------
### OPEN TO OPERATOR

1. **Q3 — does slippage join the toll of record?** Default if silent: no; the charter-slippage twin is printed beside
   every row, never instead of the toll (L-0.29).
2. **Q5 — the forward ledger re-rooted.** Default if silent: read as enacted in fact by Stage D, Stage L and O-24;
   TC11's and X's ledger files are never refreshed in place (L-0.29).
3. **Q7 — the X lane's vendored shim.** Default if silent: the lanes stay apart; TC12 vendors its own env and prints
   X's disclosed drift (L-0.29).
4. **"tc11-stamp" — which bytes "re-pin its registry files" moves.** Q2's own sentence names three files; TC11's
   verifier is only satisfied if a fourth registry file and typed constants in six TC11 scripts move too. Default if
   silent: the larger set of L-0.24, applied only as an operator close act and only if the scratch-clone proof is
   GREEN; otherwise not applied and said so. The veto "tc11-stamp" withholds the whole step.
5. **Vetoes of Q6, Q8, Q9 have no token.** Default: a veto of one of them is the operator's message naming its
   Q-number (L-0.23).
6. **The push.** The daily routine pushes the whole branch when its SSH route works; every `tierc12(` commit then
   reaches origin with no operator act. Only the operator can change the routine. Default if silent: the build
   proceeds and the report states the push fact read from git (L-0.9).
7. **"SAIL remains HELD (operator 2026-09-24)".** No document of that date names SAIL. Default: the date is read as
   the TC11 contract's ratification, and all three filed hold lines are cited (L-0.2).

---------------------------------------------------------------------------------------------------------------
### INTERFACE ASSUMPTIONS

- **L-D (substrate + env).** `scripts/tierc12_env.py` is a vendored shim (no `tierc11_` module imported) that exposes
  `E.TP` (`tierc10_panel`, at a pinned sha), `E.TB`, the lineage, `E.OUT` = `T12`, the pin read from
  `T12/data/AS_OF_PIN.json`, `E.hook_escapes`, `E.opened_paths()`, `E.import_audit()`; arms a hook that refuses writes
  into the O-3 estate, `XR/`, both earlier snapshots and `exchange/`, and logs opens per stage; re-roots
  `TP.AS_OF_PIN`, `TP.STAGE_D_MANIFEST` and the import-time `_U12` panel resolution to TC12's records. Stage D's
  manifest carries the snapshot's name and absolute path; `T12/data/AS_OF_PIN.json` carries
  `as_of_last_closed_4h_close_ms`. L-D declares the one subprocess site of the snapshot clone for `SUBPROC_SITE_T`,
  and any dynamic-import door of the env. L-D pins `scripts/tierc10_panel.py`'s sha and proves the pin (O-7).
  **A conflict to settle at assembly:** L-D's draft names stages `TC12-VENDOR` and `TC12-D-MIRROR`. Neither is in
  `ORDER`; under L-0.10 they are the dotted children `TC12-REG.vendor` and `TC12-D.mirror` (the first name would
  otherwise be sorted at Stage V by the filed merger). L-D's vendored shim and ported functions hold literals under
  L-0.17's rule (G), not as findings.
- **L-V (value area).** The Stage V door scripts L-V names (`scripts/tierc12_va.py`, `scripts/tierc12_va_stamps.py`)
  are the members of `DOORS_T`, listed by name; each imports `analytics.value_area` (earned) and files no table with a
  `TRADE_COLS_T` column, so any event-outcome or two-trades table is computed outside the doors. L-V files the
  accessor names (`ACCESSORS_T`) and the accessor law (recompute, pass through the write function, HALT unless equal
  to the filed table on every row); an accessor takes keys — asset, lens, instants, a price to locate — never a tape
  or a window of the caller's choosing. L-V's draft says books and gates may also use the accessor: under L-0.22 the
  gates and the v6 book builders are `NEVER_RUNNER_T` and read the filed stamp tables instead. L-V's `TC12-V5` (the
  stamps written after each book stage) is, under L-0.10, a dotted child of that book's own stage, not a stage id. `analytics/value_area.py`
  is numpy-only, keyword-only, default-free and holds structural literals only (L-0.17, L-0.22 leg (v)). L-V says
  whether the mirror's licence record is a registered table (collar-exempt), names the traverse pin record, and names
  the per-member bar-close columns of the V5 vector.
- **L-X (statistics + registrations + close).** The prefix-pin function of L-0.1 in full (its own reading of contract
  :10) and the tc11-stamp's mechanics (its own reading of contract :13) — L-0.1 and L-0.24 state the same laws at
  ruling level and add nothing that contradicts them. The registry's files and keys (`leans.sha256`, `head`, the five
  payloads with `mechanism`); F-REG and F-FAM; the verdict-word pattern used by F-COLLAR and F-NOT; the list
  `REGISTERED_TABLES_T`; the scorer's no-clobber law; the close generator (its modules are the RENDERERS of L-0.17,
  held by L-X's digit trace), `close_acts.sh` (which hosts L-0.24's step and L-0.1's stamp of TC12's own contract),
  F-TC11-STAMP's hosting suite, the report layout and its whole-versus-pointed choice.
- **L-C (control).** The book directories and the two roles names; F-CTRL; that every ride's `TP.ride_spec` is
  available to F-NOT.
- **L-G, L-R, L-S.** Each names its book directories, its grids' axes, its hand-sample categories, the columns F-NOT
  reads (lens, edge price, stop moves, entry fills), the pins it consumes with their flow-leg witnesses, whether its
  walk reads 5m children (`FIVE_MIN_READERS_T`), and — for the scalper — the typed list of VA columns it reads and
  its two `ema` call sites. L-R and L-S name which of their modules are RUNNERS (`RUNNERS_T`: the P-SFP-VA-1 builder,
  the P-SCALP-3 builder, Stage R's Tier-E value-area tables) or declare that they read filed columns only; L-G's two
  gate builders and L-R's P-DIR-1 gate builder are decision modules and read stamp columns. L-R reads the FLIP_HOLD pins and builds the gaps-and-order null WITHOUT importing a module
  of the range machine (pins as filed data; the null mirrored and held to X's filed tables, O-4). If a reading needs
  such an import it must say so, and L-0.22 and L-0.30's PIVOT-RANGE leg gain a typed, earned exception at assembly —
  never a silent one.
- **L-L (ledger + era + ferry).** The fourth book's spec is filed before its ride (T3); the ferry is staged under
  `T12/ferry/` and its priority order is LEANS text (T4).
- **The orchestrator.** Commits each stage (L-0.9); runs the attestation tool (L-0.12); assembles `DOORS_T`,
  `RUNNERS_T`, `ACCESSORS_T`, `FIVE_MIN_READERS_T`,
  `REGISTERED_TABLES_T` and the pin map from the nine sections at freeze; rules amendments.

---------------------------------------------------------------------------------------------------------------
### OBJECTIONS

**OBJECTION O-3 / O-4 — where X's contract can be read from.**
- *The fact.* O-3 lists "the three earlier contracts in `exchange/queue/`" as byte-frozen estate, and O-4 says X is
  read ONLY from the byte copies under `x_rec/`. Main's `exchange/queue/` holds two earlier TC contracts
  (`2026-09-22_TC10_RESUME_APOLLO.md`, `2026-09-24_TC11_APOLLO.md`) [measured here: `ls`]. X's contract
  `exchange/queue/2026-09-25_TC11X_APOLLO.md` is not in main (it arrives with X's merge) and is not among the files of
  `XR/X_REC_MANIFEST.json`, whose paths are all under `research_outputs/tierc11x/` or `scripts/tc11x_*.py` [measured
  here]. The bytes do exist as a blob at the certified tip in the shared object store, and hash to the sha X's records
  pin: `git --no-optional-locks -C /Users/luis/Naiad show 7b24f835…:exchange/queue/2026-09-25_TC11X_APOLLO.md` →
  sha256 `40e0c4b7…` [measured here].
- *Why it matters.* TC12 inherits laws whose text of record is X's contract — the standing ferry law (its :42-44) and
  the family and fixture phrasing X's readings quote. Under O-4 as written those lines can only be cited second-hand,
  through `XR/tierc11x/LEANS_X.md` and the slices in `XR/tierc11x/registrations/REGISTRATIONS_X.json`; and the census of
  L-0.6 can hold two contracts, not three.
- *The reading proposed.* (a) O-3's count reads "the two earlier TC contracts in main's `exchange/queue/`, and X's
  contract at the certified tip"; (b) X's contract is read by `git show <x_tip>:<path>` with its sha asserted — an
  object read that opens no file of the X worktree and writes nothing — and that read is added to O-4's allowed
  sources by name.
- *Drafted under the ruling as written.* Every citation of X's contract in this section goes through an `XR` record
  that quotes it; L-0.6's census lists the two contracts main holds and proves the X ref unmoved instead.
