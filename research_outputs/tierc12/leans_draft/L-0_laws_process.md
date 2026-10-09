## L-0 · LAWS AND PROCESS

This section reads the contract's LAWS paragraph (:5-9), STEP Q (:10), RULINGS ENACTED (:12-16), the cross-cutting
fixtures of the FIXTURES line (F-DET, F-GRID, F-KEY, import-closure, worktree attestation, :123-124), WHAT THIS IS NOT
(:132-134) and VETOES BY NAME (:135-137). It fixes the resume law, the stage order and commit law, the fixture
harness, the sweep, the stamp and collar helpers, the "no typed number" enforcement, the meaning of "decision module",
and the refusal fixture F-NOT. It owns no registered row. It conforms to ORCHESTRATOR_RULINGS O-1..O-32; one
objection was filed and accepted (O-25).

**Abbreviations.** `M` = `/Users/luis/Naiad` (the main tree, branch `v12-v1-census`). `T12` = `research_outputs/tierc12`.
`T11` = `research_outputs/tierc11`. `XR` = `research_outputs/tierc12/x_rec` (the byte copies of TC11-X, in the main
tree only; every read asserted against `XR/X_REC_MANIFEST.json`). "contract :n" = 1-indexed line n of the STEP Q bytes
of `exchange/queue/2026-10-08_TC12_APOLLO.md` (L-0.1). `E` = the TC12 env shim (`scripts/tierc12_env.py`, owned by
L-D); `E.TP` = `tierc10_panel`, `E.TB` = `tierc2_baseline`, `E.R2` = `tierc2_rules`, `E.R5` = `tierc5_rules` as that
shim exposes them. A RECORD = a file `T12/progress/<record id>.json`. `RESUME_ORDER_T`, `SUBSTAGES_T`, `PARALLEL_T` =
the typed objects of L-0.10. `certified(path)` = `tierc12_progress.certified` (L-0.4): the last record that names a
path. "The reader" = `scripts/tierc12_va_stamps.py`; DOOR 1, DOOR 2 = the two members of `DOORS_T` (L-0.22).
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
whole-file sha is recorded beside the prefix sha and compared by nothing afterwards: the merged ledger itself carries
the prefix, not the whole file (`contract_of_record`, L-0.9), so a BUILT line moves no pinned byte. It is ONE function,
used by every reader; L-X states it in full for the registry (its prefix-pin reading), and the resume suite calls the
same function.
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
  (ii) the second PYTHONHASHSEED twin of F-DET (L-0.20); (iii) the first element of every fixture stream (L-0.14 F).
  The sensitivity seed printed beside every ruler is `T5.SEED`, read by object (`scripts/tierc10_panel.py:92`), per
  O-22.
SOURCE: contract :2-4, :101; the three SAIL cites above (scout U1 §1.10); `scripts/tierc10_panel.py:92`, :143 [read
here]; `scripts/tierc12_progress.py:53` [read here]; O-22.
RIVALS: a per-stage salted seed — not taken: the contract names one seed. Reading "operator 2026-09-24" as a separate
SAIL ruling — not taken: no such document exists; listed for the operator.
FAILS-IF: **F-SEED** (`scripts/tierc12_closure_fixtures.py`, AST) FAILS IF a call whose callee is in the fixture-typed
ruler list (`cluster_boot`, `cluster_boot_diff`, `loao_n`, `default_rng`, and every TC12 wrapper of them) omits its
seed argument or passes a seed expression that does not RESOLVE. A seed expression resolves iff every leaf is the
pin-door seed (or `E.SEED`), an integer draw index, or a `crc32` call; a seed read by key from a sha-pinned X record
is allowed only inside the functions typed `X_SEED_MIRROR_T` (the F-VA-NULL stream builder; `tierc12_era.compute`
with `seed_source = "x"`). Planted mutations: a `cluster_boot(x, c)` call with no `seed=` in a copy of the scorer →
RED; a literal seed in the same call → RED (also caught by F-TYPED); a seed read from an X record in a function
outside `X_SEED_MIRROR_T` → RED. Control that must stay GREEN and is printed: a list seed `[seed, crc32(tag)]` and a
list seed `[seed + draw, crc32(tag)]` with `draw` an integer loop index.

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
`frozen_estate_shas_at_r0`. RESUME: at every session start and at every record gate the census is re-derived by
**F-RESUME** from files only: for each record under `T12/progress/*.json` it verifies every `artifact_shas` path under
the last-record law (L-0.4 (1)) and every recorded transcript, recomputes the ledger of records (COMPLETE-VERIFIED /
PARTIAL / ABSENT) in the order of `RESUME_ORDER_T` (L-0.10 point 3) and prints THE RESUME POINT = the first entry of
`RESUME_ORDER_T` whose record is absent or not COMPLETE-VERIFIED. Derived, never typed, never stored. A non-blocking
child never moves it. The census also prints, with no pass
condition, the branch, the live HEAD, and three booleans read from files: whether each predecessor's report exists
under `exchange/reports/` and its header stands in `exchange/status/LEDGER_APOLLO.md`. A fixture that depends on git
history takes its head as an argument (`--at=<sha>`, the last `tierc12(` commit before the one being made); the live
HEAD goes to stdout only (the daily routine moves it; X's AM-X17 pattern).
SOURCE: TC10 contract :26-33; `T12/progress/TC12-R0.json`, `T12/PROGRESS.json` [read here];
`scripts/tierc12_progress.py:20-22`, :44-45 [read here]; `XR/tierc11x/LEANS_X_AMENDMENTS.md:410` (AM-X17); scout U9
§1.2; O-31, OD-7 (the walk over records, children included).
RIVALS: a hand-kept `resume_point` string (TC11's PROGRESS) — not taken: a typed pointer can disagree with the
records. A census that reads the live HEAD into its transcript — not taken: the transcript would change daily.
FAILS-IF: see L-0.4 (one fixture, F-RESUME).

**L-0.4 VERIFY-OR-QUARANTINE** — "verify-or-quarantine" (contract :5)
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 12] TC11's PROGRESS sha is NOT read through `certified()`: it is read from `progress/TC12-R0.json` → `frozen_estate_shas_at_r0` (or from `close/TC11_STAMP_MAP.json` once applied), as L-D does; `certified()` HALTs on a path no record's `artifact_shas` names.
READING: three status words and no fourth (`STATUSES`, `scripts/tierc12_progress.py:22`; the merger HALTs on any
other, :44-45). A RECORD is **COMPLETE-VERIFIED** iff all of:
- (1) THE LAST-RECORD LAW (OD-4). Every `artifact_shas` path exists and verifies under THE LAST RECORD THAT NAMES IT
  (in `RESUME_ORDER_T`, L-0.10): the working file re-hashes to that record's `{bytes, sha256}`. An EARLIER record's
  entry for the same path is held to the blob at the commit that closed its own record — `git show <closing
  commit>:<path>` re-hashes to the earlier entry, the closing commit of a record being the last commit in
  `28e006b^..<--at>` that touched `progress/<record>.json` (a fixture-side read-only git call). For a path on the
  append-only list (L-0.5) the earlier bytes must also be a byte-prefix of the working file. An UNTRACKED
  (git-ignored) path may be recorded by a later record only if that record's `supersedes[]` carries `{path,
  old_sha256, reason}` (reason = a ruling, an AM id or a stage law); its earlier entry is printed SUPERSEDED and not
  re-hashed. Anything else is a moved artifact.
- (2) `blockers` is empty.
- (3) It holds at least one fixture record, and every fixture record has `exit_code` 0, `legs_red` 0,
  `transcript_drift` false, `transcript_sha_before == transcript_sha_after ==` the transcript's sha now, and a tally
  that agrees with it (`GREEN + NOT RUN == legs_total`, NOT RUN `== legs_not_run`; L-0.14 C).
- (4) Its suites re-pass now (L-0.11). A fixture record typed `provenance: true` is held on (3) alone and is never
  re-run (L-0.14 D).

An `ORDER` STAGE is COMPLETE-VERIFIED iff its parent record and every BLOCKING child are (L-0.10 point 6).
**One helper for every sha-first reader:** `tierc12_progress.certified(rel_path) -> {record, bytes, sha256}` (stdlib
only; walks `T12/progress/*.json` in `RESUME_ORDER_T`; returns the LAST record naming the path; HALT if none). It is
what the shim (P3, the `x_rec` manifest's own sha, TC11's PROGRESS sha), the reader's sha law, the scorer's inputs
(L-X.23) and the registry filer call. No reading takes a sha "from `progress/TC12-R0.json`" by name. `TC12-D.mirror`,
which has no position in `RESUME_ORDER_T`, is walked after it; no other record may name one of its paths.
**Paths the readings themselves re-record** are lawful under (1) and are named as such:
`forward/FORWARD_LEDGER.jsonl` (TC12-REG.ledger-spec, then TC12-L; append-only), `ferry/FERRY_MANIFEST.json` (TC12-L,
then TC12-CLOSE; tracked), `va/stamps/build_manifest.json` (the three stamps children; tracked),
`scripts/tierc12_progress.py` (R0, then TC12-REG; tracked), `LEANS_AMENDMENTS.md`; and the two already moved on
file — `ORCHESTRATOR_RULINGS.md` and `XR/X_REC_MANIFEST.json` (R0, then TC12-LEANS: section H and O-25's one row).
**The FIXTURELESS records** are a closed, typed list — `STEP Q`, `TC12-R0`, `TC12-LEANS` (documents only) — and are
COMPLETE-VERIFIED on (1) and (2) alone; their bytes are re-bound by F-FROZEN-TEXT from TC12-REG on. Every other
record, every dotted child included, has a fixture record. Anything else is **PARTIAL** (present but unverified or
failing) or **ABSENT**. "Built, awaiting verification" is PARTIAL with a blocker. The one record that may stay PARTIAL
through CLOSE is the non-blocking child `TC12-D.mirror` (L-0.10 point 2).
**QUARANTINE:** before a PARTIAL record is rebuilt, its artifacts are MOVED — never deleted, never overwritten — to
`T12/_det_partial_<YYYYMMDD>T<HHMM>Z/<same subpath>` (TC10's form under a `_det_` name, so the directory is already
git-ignored by the nested `**/_det_*/` rule and no ignore file is edited), by the record's builder, and the move is
listed in the record's `notes`. A quarantine directory is never staged and never read by a builder; its one reader is
the scorer, which prints a quarantined regbook sidecar's own numbers beside the rebuilt row (L-0.10 T7). Quarantine
follows `depends_on`, transitively: a record whose `depends_on` closure names a quarantined record becomes PARTIAL
with it.
SOURCE: TC10 contract :12-15 (law items 1-2); `scripts/tierc10_resume_fixtures.py:296-300` (`LEGAL_STATUS`,
`STAGE_KEYS`, `FIXTURE_KEYS`), :4559-4569 (a COMPLETE-VERIFIED record with no fixture is a finding in TC10) [read
here]; the fixtureless precedent: `T11/PROGRESS.json` stages `STEP Q` and `TC11-REG` (`fixtures: []`),
`XR/tierc11x/PROGRESS.json` stages `STEP Q`..`X-LEANS` (no `fixtures` key) [measured here]; O-6, O-31; OD-4, OD-7.
Why (1) is written this way [measured here]: `progress/TC12-R0.json` (last touched by `ac8cb92`) records
`ORCHESTRATOR_RULINGS.md` and `XR/X_REC_MANIFEST.json` at their R0 bytes; commit `7295ab5` appended section H to the
first (the leading `bytes` of today's file, as that record counts them, still hash to its entry) and added O-25's
one row to the second (its `n_files` is now one more than the record's `x_rec.n_files`). `T12/.gitignore`
(`**/_det_*/`) [read here].
RIVALS: TC10's strict law (every COMPLETE-VERIFIED stage needs a fixture record) — not taken for the three document
records: two of them were filed fixtureless before these readings, and a fixture invented after the fact would certify
nothing; the exemption is typed and closed instead of silent. X's fourth word "COMPLETE" — not taken: not in the law.
"Every recorded path re-hashes to its recorded bytes" for every record that names it — not taken: false of the filed
tree since `7295ab5`, and false by design of every path a later record re-files. A `supersedes` entry for tracked
paths too — not taken (OD-4): git already holds the earlier bytes, so the earlier entry is proven, not waived.
FAILS-IF: **F-RESUME** (`scripts/tierc12_resume_fixtures.py --stage=<record id> --at=<sha>`) FAILS IF a recorded
artifact is missing or fails clause (1) — the working file against its last record; an earlier entry against the blob
at its closing commit; an append-only earlier entry against the byte-prefix; an untracked path re-recorded with no
`supersedes` entry; a path of `TC12-D.mirror` named by another record; a record lacks a key of the typed key set
(L-0.9) or carries an illegal status; `certified()` returns, for any path two records name, anything but the entry
the fixture's own walk of `RESUME_ORDER_T` finds last; a COMPLETE-VERIFIED record outside the typed fixtureless list
has no fixture record, a non-zero `exit_code` or `legs_red`, a drifted transcript, a tally that disagrees with
`legs_total` or `legs_not_run`, or a non-empty `blockers`; a `<stem>_rerun.txt` or `<stem>_partial.txt` stands beside
a transcript of record; a quarantine path appears in a record's `artifact_shas`; a record reads COMPLETE-VERIFIED
while its `depends_on` closure names a PARTIAL, ABSENT or quarantined record; a record's `depends_on` lacks a member
of its typed floor (L-0.9). Planted mutations (scratch
copy of the `T12` root and a scratch repository; "a tampered partial must FAIL", TC10 contract :125-126): one byte
flipped in a recorded artifact; a recorded artifact deleted; an earlier record's path whose blob at its closing commit
differs → RED; an untracked path re-recorded with no `supersedes` entry → RED; an append-only path whose later version
rewrites an earlier byte → RED; `certified()` patched to return the FIRST record naming a path → RED; `legs_red` set
to 1; `legs_not_run` one less than the transcript's NOT RUN count; `fixtures` emptied on `TC12-D`; status
`"COMPLETE"`; a `_rerun.txt` planted beside a transcript; a dependent record left COMPLETE-VERIFIED over a quarantined
`depends_on` member; a record copy whose `depends_on` omits the record that certifies a path in its directory's
`READ_SET.json` — each must be caught by its named detector.

**L-0.5 FROZEN TEXTS** — "frozen texts" (contract :5)
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 20] `DISCLOSURES_BUILD.md` (O-34 d): the orchestrator appends a dated `B-n` entry at a stage gate and that stage's record re-records the file; a build writes nothing there.
READING:
- **Byte-frozen** from the instant named: the contract prefix (STEP Q; L-0.1); from the TC12-REG commit: `T12/LEANS.md`,
  `T12/registrations/REGISTRATIONS.json` (filed by a write-once filer that HALTs if the file exists — TC11's law),
  `T12/registrations/REGISTRY_PIN.json`, `T12/pins/CONTRACT_PIN_MAP.json`, `T12/pins/CONTRACT_PINS.json`,
  `T12/pins/PIN_REGISTER.json`, `T12/pins/CONTRACT_TOKENS_UNPINNED.json` (L-0.17), `T12/frozen/FROZEN_ESTATE.json`
  (L-0.6); from their own records: the fourth book's spec `T12/forward/BOOK_SPEC_COMBINED.json`
  (TC12-REG.ledger-spec; O-24), `T12/data/AS_OF_PIN.json` (TC12-D, write-once), the traverse pin record
  `T12/va/TRAVERSE.json` (TC12-V; O-18). `T12/forward/BOOK4_FREEZE.json` (the fourth book's freeze instant, L-L.17)
  is write-once from the record that first names it — `TC12-D`'s: the orchestrator writes it immediately after the
  ledger-spec commit and its gate step adds the path to that record's artifact map; L-D writes nothing for it.
- **Append-only until the TC12-REG commit, then byte-frozen** at the shas `REGISTRATIONS.json` `rulings.sha256` and
  `disclosures.sha256` name: `T12/ORCHESTRATOR_RULINGS.md` and `T12/DISCLOSURES.md`. R0's bytes must be a byte-prefix
  of every later version; only the orchestrator appends (section H; the D-5… entries of L-0.10's TC12-LEANS row).
- **Append-only throughout** (every committed version a byte-prefix of the next): `T12/LEANS_AMENDMENTS.md`,
  `T12/AMENDMENTS_PROPOSED.md`, `T12/DISCLOSURES_BUILD.md`, `T12/forward/FORWARD_LEDGER.jsonl`,
  `T12/scores/SUPERSEDED.jsonl`, `T12/scores/REFILE_LOG.jsonl`.
- **`T12/DISCLOSURES_BUILD.md`** is the running record AFTER the registry freeze (entries `B-1 …`, dated, never
  edited): every build-time disclosure a reading sends "to DISCLOSURES.md" after TC12-REG (L-D.18's fee-page
  observation, L-D.22's moved tick or coarser month) goes there. The report's §9 prints every line of both files.
- **A reading is never re-chosen after a number is seen.** The only route of change after freeze is a dated amendment
  in `LEANS_AMENDMENTS.md`, and an amendment may never follow from a registered rule's outcome. SOURCES: (i) a build
  fact — the code cannot do what a reading says; (ii) a verifier's finding; (iii) an operator veto by name (L-0.23);
  (iv) the contract's own order — AM-1 is the dated V2-versus-X statement of L-V.15, filed at the TC12-LEANS freeze
  with no AP; (v) TRANSCRIPTION against pinned bytes — a fee-page grammar (L-D.18), proposed by the Stage D builder
  as `AP-n` and ruled as `AM-n`, naming the body sha; it may change patterns only. ROUTE for (i), (ii) and (v): a
  builder files a proposal `AP-n` in `AMENDMENTS_PROPOSED.md` (date, reading id, text at issue, evidence path:line,
  proposed text, downstream effect) and the orchestrator rules it. FORM: every heading is
  `## AM-<integer> · <YYYY-MM-DD> (~HH:MMZ) · <reading ids> · <basis>[ · <nickname>]`, with `<basis>` =
  `ruling on AP-<m>` | `contract :32-33 (no AP)` | `operator veto "<token>"`; ids ascend from 1; the body is
  **Text amended / Amended to / Reason / Redone**. A section's nickname (`AM-V2`, `AM-D-FEE-<VENUE>`) may follow in
  the title and is never an id. `--refile=<id>` accepts `AM-<n>` (a heading) or `FIX-<n>` (a key of
  `progress/TC12-FIX.json`). Everything downstream of an amended reading is redone and re-certified;
  `PROGRESS.json` `amendments_of_record` carries the file's sha (`scripts/tierc12_progress.py:57`).
- **Resume item 3.** A registered row's number computed before an interruption, or before an amendment that touches
  the row, is KEPT and printed BESIDE the fresh value with the AM id; it is never re-worded and never dropped. The
  scorer keeps it: a refile appends the superseded leaf whole to `T12/scores/SUPERSEDED.jsonl` and prints it under
  the row's §0 cell, and a regbook rebuilt before TC12-SCORE leaves its quarantined sidecar's `n` and ΣR printed the
  same way (L-X.27; L-0.10 T7). Differing bytes of any other record go to `<stem>_rerun<suffix>` (the no-clobber law).
- **The freeze of LEANS** binds bytes: `sha256(T12/LEANS.md) == REGISTRATIONS.json leans.sha256 ==
  REGISTRY_PIN.json leans_sha256`, and the sha the last review pass names (L-0.12).
SOURCE: TC10 contract :16-18 (law item 3); contract :32-33 ("amendments dated if they differ"); `T11/LEANS_AMENDMENTS.md:3-8`
(the law this reading extends: "an amendment may follow from a build fact … or from a verifier's finding. It may
never follow from a registered rule's outcome.") [read here]; `XR/tierc11x/LEANS_X_AMENDMENTS.md:1-8`,
`XR/tierc11x/AMENDMENTS_PROPOSED.md:1-6` [read here]; `scripts/tierc11_registrations.py:244-245` (write-once HALT)
[read here]; `T12/DISCLOSURES.md:3-4` ("Entries are dated and never edited") [read here];
`scripts/tierc12_progress.py:55-57` [read here]; O-6; OD-4, OD-16, OD-18.
RIVALS: edit LEANS in place with a changelog — not taken: the registry pins its sha. Let builders amend directly — not
taken: the builder who saw the number would be ruling on the reading. Keep the rulings file byte-frozen from R0 — not
taken (OD-4): section H was appended at `7295ab5`, before the review; the file freezes with the registry, which pins
it. Keep appending build-time disclosures to `DISCLOSURES.md` — not taken: the registry pins that file too.
FAILS-IF: **F-FROZEN-TEXT** (resume suite) FAILS IF a byte-frozen file's sha differs from its pin (the last record
naming it; for the rulings and the disclosures, from the TC12-REG commit on, the two shas `REGISTRATIONS.json`
names); for an append-only file — the two until-REG files included, up to that commit — some `tierc12(` commit's
parent blob is not a byte-prefix of that commit's blob (git plumbing at `--at`); a write-once file
(`REGISTRATIONS.json`, `AS_OF_PIN.json`, `BOOK4_FREEZE.json`) has more than one blob in the range; an `## AM-` heading
does not match the form, the ids do not ascend from 1, or a basis names an `AP-<m>` that is not on file; the LEANS
sha, the registry's two `leans` pins and the review record's last-pass sha are not one value. Planted mutations: a
one-character edit in a scratch copy of `LEANS.md` → RED; an earlier DISCLOSURES entry edited (not appended) in a
scratch repo → RED; a line appended to a scratch `ORCHESTRATOR_RULINGS.md` after a scratch registry commit → RED; a
heading `## AM-V2 · …` (a nickname in the id's place) → RED; the registry filer run against an existing
`REGISTRATIONS.json` must HALT (counted as the catch).

**L-0.6 THE FROZEN ESTATE** — "frozen texts" (contract :5) as it binds the predecessors, and "no re-family of TC11"
(contract :133-134); governed by O-3.
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 18] binds every section: a TC11 or X record is opened only through `E.tc11_record` / `E.x_rec` (L-D.27, O-4); a raw open, or a listing of a `research_outputs/tierc11` or `x_rec` directory, is refused (exit 70), armed fixture processes included.
READING: TC12 moves no byte of the estate O-3 lists. Prevention is L-D's env hook; DETECTION is here. At TC12-REG a
census `T12/frozen/FROZEN_ESTATE.json` is written once by `scripts/tierc12_frozen.py` (stdlib only; walks and hashes; no
git) over the WORKING-TREE bytes of: `research_outputs/tierc10/**`, `research_outputs/tierc11/**`, `scripts/tierc10_*`,
`scripts/tierc11_*`, the two earlier TC contracts in main's `exchange/queue/` (TC10 RESUME, TC11), and X's contract as
the manifest-pinned copy `XR/queue/2026-09-25_TC11X_APOLLO.md` (sha `40e0c4b7…3c3d`, O-25; slices of it are cut from
that copy by L-X.17's law),
`exchange/queue/008_sail-skeleton.md`, `LEDGER.md`, `exchange/status/LEDGER_APOLLO.md`, `exchange/status/CONVENTIONS.md`,
`scripts/publish_exchange.py`, and every `analytics/*.py` plus `analytics/INTERFACE.md` except `analytics/value_area.py`
— each as `{path, bytes, sha256}`; every `__pycache__` directory under those roots by name; the two earlier snapshots
`tc10_20260921` and `tc11_20260925` as a `(path, bytes, mtime_ns)` listing sha (their content hashing is Stage D's
prefix-identity leg, L-D); and `XR/**` against `XR/X_REC_MANIFEST.json` (path set, `n_files`, every sha), the
manifest's own sha and `n_files` read through `certified()` (the sha it returns; `n_files` from the `x_rec` block of
the record it names — the TC12-LEANS record, which re-records the manifest after O-25 added one row). The
entries of `T12/progress/TC12-R0.json` `frozen_estate_shas_at_r0` must equal the census on those paths. For the live
cache and the X worktree "frozen" is proven differently, because other lanes may move them: no TC12 process opens a
path under either (the env hook refuses and logs such an open, L-D.27), and `refs/heads/tierc11x` equals the `x_tip`
recorded at R0. VERDICT at every record gate and at CLOSE: path set and every sha equal to the census — with ONE typed
acceptance (L-0.24): a census path of L-0.24's sets (a)-(f) — and the stamped contract itself, which the same map
lists — is accepted at its census sha OR at the value `T12/close/TC11_STAMP_MAP.json` names for it when that map
reads `applied: true`. IF A PREDECESSOR'S CLOSE ACT LANDS MID-BUILD
(the operator's keystroke, L-0.26), the estate moves by design: the orchestrator files an amendment "FROZEN_ESTATE
re-pinned after <tier>'s close" that lists every moved path with the commit that moved it (a subject starting
`tierc10`, `tierc11(`, `tc11x(`, `exchange: auto-publish`, or the merge of `tierc11x`), a new census
`FROZEN_ESTATE_<k>.json` is written beside (the first is never rewritten), and any TC12 artifact whose `input_sha`
names a moved path is redone. A moved path with no attributing foreign commit is a finding against TC12 and HALTs the
gate.
SOURCE: O-3, O-4, O-25; `T12/progress/TC12-R0.json` [read here]; `XR/X_REC_MANIFEST.json` keys `files[].copy`,
`files[].sha256`, `n_files`, `law`, and its row `copy = research_outputs/tierc12/x_rec/queue/2026-09-25_TC11X_APOLLO.md`
(`read_as` "git object at the certified tip … [O-25]") [measured here]; scout U1 H-3, H-5, H-6; scout U9 H2; OD-4.
RIVALS: `git status` alone — not taken: most of TC10's tree and all TC11 parquet are git-ignored, so porcelain cannot
see them. Walking the X worktree to hash it — not taken: O-4 forbids reading it, and its own close script certifies it.
Pinning the X manifest at its R0 sha — not taken: O-25 added a row after R0; the last record naming it governs.
FAILS-IF: **F-FROZEN** (resume suite) FAILS IF any census path is missing, changed (outside the one typed acceptance)
or joined by a new sibling under a census root (a `_det_*` file, a `*_rerun.*`, a `__pycache__`), the X manifest's
sha or `n_files` is not the certified one, or the `tierc11x` ref moved. Planted mutations (scratch copy of a census
root): one byte flipped in `scores/SCORES.json`; a `_det_x/a.parquet` added; a `__pycache__/a.pyc` added; a
`SCORES_rerun.json` added; a set-(c) script copy at its mapped value while a map copy reads `applied: false`; a file
added to a scratch `x_rec` copy with no manifest row — each RED, naming the path.

**L-0.7 ONE CORRIDOR, ONE SUBSTRATE, ONE PROCESS** — "one corridor" (contract :5); O-5, O-7, O-8, O-9.
READING: One pin for the tier: the value O-7 fixes (the latest 4h bar closed when STEP Q was committed), written once
by Stage D to `T12/data/AS_OF_PIN.json` key `as_of_last_closed_4h_close_ms` and read by object ever after. TC10's law
item 4 offers "re-pin at resume" when Stage D is incomplete; that branch is NOT available to TC12 — the pin was taken
by value at STEP Q, so an incomplete Stage D is rebuilt to the same pin. Every record's `as_of` from TC12-D on is
the pin's ISO string, and every transcript's first line is `as_of_last_closed_4h: <that ISO>`. A suite run at a
record before `TC12-D` in `RESUME_ORDER_T` prints `as_of_last_closed_4h: (pre-substrate stage)` and
`substrate: none`, and its record's `as_of` is null. THE SCORE EDGE is a
second, earlier instant inside the same corridor: TC11's pin, read by object from `T11/data/AS_OF_PIN.json` key
`as_of_last_closed_4h_close_ms` (sha held by L-0.6). In code the two instants are `PIN = E.PIN_MS` and
`W = E.TC11_PIN_MS`. O-9 scores rows whose `entry_close_ms ≤ W` and prints the rows with `W < entry_close_ms ≤ PIN`
as the strip. "One corridor" therefore means: one snapshot (`tc12_20261008`, O-8), one pin record,
two named sub-windows; no table mixes them without saying which edge its rows could see (L-0.13). One process binds
one snapshot: `NAIAD_CACHE_DIR` is exported as an absolute path before python starts and `PYTHONDONTWRITEBYTECODE=1`
always (O-5). Compute: the worker cap and the load rule are O-5's; workers are `spawn` processes that import `E` before
any I/O; results merge in a fixed key order before any write; worker counts and load averages are recorded only in
progress records and the close's cost table, never in an artifact.
SOURCE: TC10 contract :19-20 (law item 4); O-5, O-7, O-8, O-9; `scripts/tierc10_panel.py:634-647` (`stage_d_pin`),
:690-699 ("a pin may only look back") [read here]; `XR/tierc11x/LEANS_X.md:526-534` (LX-0.9) [read here].
RIVALS: re-pin at each stage to the newest closed bar — not taken: O-7. Score to TC12's pin — not taken: O-9.
FAILS-IF: **F-ONE-CORRIDOR** (resume suite) FAILS IF a record's `as_of` (TC12-D onward), a transcript's first
line, or a `build_manifest.json` `as_of` names an instant other than the pin or the score edge; a table's
`as_of_last_closed_4h` values hold a third instant; a manifest's `substrate` is not the snapshot name in Stage D's
manifest. It exempts exactly the records before `TC12-D` in `RESUME_ORDER_T`, whose transcripts must instead open
with the fixed pre-substrate pair; the pair on a transcript of `TC12-D` or later is RED. Planted mutations: a manifest
copy with `as_of` one 4h step later → RED; a table copy stamped with a third instant → RED; a manifest copy naming
`tc11_20260925` as substrate → RED; a Stage V transcript copy headed `(pre-substrate stage)` → RED.

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
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 4] the `depends_on` floor binds every record of every section: the `SUBSTAGES_T` row or `PARALLEL_T` list PLUS the last earlier record certifying each `tc12-record` path of the directory's `READ_SET.json`, computed at the gate from the read set — a section's typed row is the minimum, never the whole.
- [seam 66] one exception to 'an untracked artifact is pinned twice': the ferry's staged CSVs (`ferry/_det_staged/*.csv`) are pinned by carried sha in the tracked `FERRY_MANIFEST.json` and are not in `artifact_shas` (L-L.32).
READING:
- **Progress.** Each record's builder writes `T12/progress/<record id>.json` (the file of `STEP Q` is `STEP_Q.json`)
  with the keys `stage`, `parent`, `status`, `as_of`, `blockers`, `depends_on` [record ids], `artifact_shas`
  {repo-relative path: {bytes, sha256}}, `supersedes` [], `fixtures` [{`suite`, `transcript`, `provenance` (bool),
  `exit_code`, `legs_red`, `legs_not_run`, `legs_total`, `transcript_drift`, `transcript_sha_before`,
  `transcript_sha_after`, `wall_seconds`}], `one_line`, `notes`. `stage` is the record id; `parent` is the `ORDER`
  entry a dotted child extends (null on a parent record); `suite` is the full argv after the interpreter (so a
  parameterised suite is re-runnable verbatim); `transcript` is its repo-relative path; fixture records are appended,
  never inserted; `supersedes` holds `{path, old_sha256, reason}` for UNTRACKED paths only (L-0.4 (1)).
  `depends_on` names every record whose artifact the record's builder read, and has a FLOOR checked from files: a
  child's `SUBSTAGES_T` row; a `PARALLEL_T` parent's list (L-0.10 point 5); and, for a record that writes a
  directory, the last record before it in `RESUME_ORDER_T` that names each `tc12-record` path of that directory's
  `READ_SET.json` (L-0.13). The parent record of a stage with several producers (`TC12-REG`, `TC12-ENV`) is written
  by the orchestrator's gate step from the artifact maps each producer returns. THE TWO RECORDS FILED BEFORE THESE
  READINGS are never rewritten — a rewrite would move their closing commit and with it the blob every path they name
  is held to (L-0.4 (1)) — and are held to the key lists they were filed with, fixture-typed as `PRELAW_KEYS_T`:
  `STEP_Q.json` carries `stage, status, as_of, blockers, commit, artifact_shas, one_line`; `TC12-R0.json` carries
  `stage, status, as_of, blockers, artifact_shas, fixtures, one_line, notes` and its census keys [measured here]. A
  key absent from either reads `parent` null, `depends_on` [], `supersedes` [], `fixtures` [].
  `scripts/tierc12_progress.py` merges the records verbatim, each child under its parent by its longest-prefix rule
  (:29-32), and is the ONLY writer of `T12/PROGRESS.json`. From the TC12-REG commit the same script also holds, as
  data beside `ORDER`, `RESUME_ORDER` and `SUBSTAGES` (L-0.10), the helper `certified()` (L-0.4), and records
  `contract_of_record` as `{path, prefix_bytes, prefix_sha256}` read from `progress/STEP_Q.json` (its line :54
  changes at that commit; the script is re-recorded under L-0.4 (1)), so TC12's own BUILT stamp moves no byte of
  `PROGRESS.json`. TC10's "one line to the draft" is the record's `one_line`, which the close generator renders into
  the report's build log.
- **Commit.** ONE COMMIT PER RECORD GATE: after every record's gate, and before the next starts, the ORCHESTRATOR
  commits; no builder and no reviewer runs a state-changing git command. (A commit made outside a gate — the draft
  and review commits that preceded the LEANS freeze, an amendment committed before its rebuild, T6 — carries the id
  of the record it belongs to.) Subject: `tierc12(<ID>[ <words>]): <sentence>`.
  `<ID>` is the LONGEST record id of `RESUME_ORDER_T` ∪ {`TC12-D.mirror`} — written with or without its `TC12-`
  prefix; `STEP Q` is the one two-token id; `CLOSE` also heads the operator's close-act commits — that is a prefix of
  the text inside the parentheses and is followed by `)` or a space; any words after it are free. The filed subjects
  parse as STEP Q, R0, R0, LEANS, LEANS. A subject never starts `tierc10`,
  `tierc11(` or `tc11x(`: the three pending close scripts count commits by those prefixes. Paths: explicit pathspecs
  only, drawn from `T12/**` (as its nested `.gitignore` leaves visible), `scripts/tierc12_*.py` and
  `analytics/value_area.py`; never `git add -A`, `git commit -a` or a stash; never the two paths dirty at R0 (O-2).
  The add and the commit run in one shell command, so the index is staged only for its duration, and
  `git diff --cached --quiet` is checked before and after (a staged non-exchange path at a `publish()` run makes the
  routine reset the index and skip its publish: `scripts/publish_exchange.py:624-631`). The body ends with the
  session's attribution trailer. Parquet, `_det_*/` and `x_rec/**` are never committed (nested `.gitignore`); an
  untracked artifact is pinned twice — `{bytes, sha256}` of the file in its stage record, and its content sha in its
  directory's tracked `build_manifest.json`.
- **The gate, in order, run PER RECORD:** (1) the builder files its artifacts and its transcripts
  (`--refile-transcript`, once); (2) the record's suites are re-run in fresh processes without that flag (no
  `_rerun.txt`); (3) the builder writes the progress record with the transcript shas before and after; (4) the merger
  runs; (5) F-RESUME and its sibling legs run at `--stage=<record id> --at=<previous tierc12 head>`; (6) the commit.
  The next record starts after (6), except as L-0.10 point 5 allows. The resume suite runs at every record gate from
  `TC12-REG` on; the closure, not and sweep suites run at `ORDER`-stage gates (the gate of the parent record).
  `TC12-ENV.vendor` and `TC12-REG.ledger-spec` therefore have their own commits, and F-VENDOR's "tracked and equal to
  its blob" leg (read at `--at`) runs at the `TC12-ENV` gate, after the vendor commit.
- **Directories and transcripts.** One writer script per parquet directory; one `build_manifest.json` per directory;
  one transcript per fixture record; a suite serving several records takes `--stage=<record id>` and files a
  transcript of its own per record (the suites table below; the other sections' rows are in their own readings) —
  never a leg filter. The one typed exception is `SHARED_DIRS_T = ("research_outputs/tierc12/va/stamps",)`: the reader
  writes it at three records; its `build_manifest.json` is cumulative and re-recorded by each stamps child (lawful
  under L-0.4 (1)); the helper legs F-KEY / F-DET / F-COLLAR on a shared directory are SCOPED — they evaluate on a
  scratch VIEW holding the tables that the records up to `--stage` name and the manifest restricted to them, and call
  `TP.check_keys` / `TP.check_det` on that view.
- **What cannot be enforced here** is stated, not hidden: the daily routine pushes the whole branch whenever its SSH
  route works, so `tierc12(` commits reach origin without an operator act (it pushed TC11's the same way). The count
  "N commits, M on a remote" is read from git at close, never typed.
SOURCE: TC10 contract :23-24 (law item 6); O-1, O-2, O-6, O-31; OD-4, OD-7; `scripts/tierc12_progress.py` (:20-22,
:29-32, :54) [read here]; `T12/progress/STEP_Q.json`, `T12/progress/TC12-R0.json` (their key lists) [measured here];
the filed subjects `git log 28e006b^..HEAD` — `tierc12(STEP Q)`, `tierc12(R0)` twice, `tierc12(LEANS draft)`,
`tierc12(LEANS review)` [measured here]; `scripts/tierc10_resume_fixtures.py:297-300` [read here]; `T12/.gitignore`
[read here]; root `.gitignore:44`, :263-264, :287-288 [read here]; `scripts/publish_exchange.py:603`, :627, :745 [read
here]; scout U1 H-1, H-2, H-8; scout U9 §1.9.
RIVALS: builders commit their own stages — not taken: one writer of history, and a builder's half-made `git add` is
exactly what the routine resets. A hand-edited PROGRESS.json (TC11) — not taken: O-6. One commit per `ORDER` stage
with its children folded in — not taken: a child labelled with its parent's id defeats F-ORDER's ancestry tests; the
vendored referee must be at HEAD before its parent's gate runs, and the ledger spec must be a proper descendant of
the registry commit. Rewriting the two pre-law records to the full key set — not taken: it would re-close them at a
later commit.
FAILS-IF: **F-COMMIT** (resume suite, range `28e006b^..<--at>`) FAILS IF a `tierc12(` commit touches a path outside
the allow-list (plus the contract, STEP Q only), or either R0-dirty path; a commit with another subject touches a TC12
path; the parsed `<ID>` of a subject is not a record id; a commit that touches `progress/<child>.json` is labelled with
another record's id; a body lacks the trailer; the index is non-empty when the suite runs.
**F-PROGRESS** FAILS IF `PROGRESS.json` is not byte-equal to the merger's output re-derived into a scratch directory;
a record's `stage` is neither an `ORDER` entry nor a `SUBSTAGES_T` id, or its `parent` is not the `ORDER` entry its id
extends; a record after the two pre-law ones lacks a key of the typed set, or a pre-law record's keys differ from
`PRELAW_KEYS_T`; `contract_of_record` carries a whole-file sha. Planted mutations (scratch repos and copies): a
`tierc12(TC12-D)` commit touching `research_outputs/tierc11/a.txt` → RED; a subject `tierc11(BUILT-STAMP)` on a TC12 path
→ RED; a subject whose first token is not a record id → RED; a child commit labelled with its parent's id while it
touches the child's record → RED; one key of `PROGRESS.json` hand-edited → RED; a record copy of `TC12-V.trades`
whose `parent` names another stage → RED; a post-law record copy lacking `depends_on` → RED; a `STEP_Q.json` copy
rewritten to the full key set → RED (`PRELAW_KEYS_T`); a `BUILT: x` line appended to a scratch contract copy must
leave the re-derived `PROGRESS.json` byte-equal (control, printed); a record with status `"COMPLETE"` → the merger's
HALT (counted as the catch).

**L-0.10 THE STAGE ORDER AND TEXT-BEFORE-RESULT** — "families declared by MECHANISM before the look" (contract :8) and
"commit + PROGRESS.json per stage" (:5-6)
READING: The stage list of record is `ORDER` in `scripts/tierc12_progress.py:20-21`: STEP Q · TC12-R0 · TC12-LEANS ·
TC12-REG · TC12-D · TC12-ENV · TC12-V · TC12-C · TC12-G · TC12-R · TC12-S · TC12-L · TC12-SCORE · TC12-FIX ·
TC12-REVIEW · TC12-CLOSE. Each stage, with the dotted children THE SUB-STAGE LAW below types, must FILE the following
and be COMPLETE-VERIFIED and committed; which record may start when is points 3-5 of that law.

| stage | reading owner | must file (children named in gate order) |
|---|---|---|
| STEP Q | L-0.1 | the contract (filed, `28e006b`) |
| TC12-R0 | L-0.3 | the census record, the nine scout maps, `XR/X_REC_MANIFEST.json`, the rulings, the disclosures (filed, `ac8cb92`, `c3129e9`) |
| TC12-LEANS | all sections | `T12/LEANS.md` (nine sections, review disposition filled), `T12/review/LEANS_REVIEW_<date>.json` (every lens and pass, drafted and revised shas), `T12/review/WORKTREE_ATTEST_LEANS.jsonl` (L-0.12), `T12/LEANS_AMENDMENTS.md` (holding AM-1, L-0.5), `T12/AMENDMENTS_PROPOSED.md`, `T12/DISCLOSURES.md` appended with D-5..D-12 (the drafters' and reviewers' disclosures; OD-18). The record re-records the rulings and the X manifest at their current shas (OD-4), with `x_rec {n_files, bytes}` and a note naming O-25's one added row |
| TC12-REG | L-X, L-0.5, L-0.6, L-0.17 | exactly `REG_SET` (fixture-typed; what the commit ADDS): `REGISTRATION_PLAN.md`; `registrations/{REGISTRATIONS.json, REGISTRY_PIN.json, ATTEST_REG.json, FIXTURES_REG.txt}`; `pins/{CONTRACT_PIN_MAP.json, CONTRACT_PINS.json, PIN_REGISTER.json, CONTRACT_TOKENS_UNPINNED.json, FIXTURES_PINS.txt}`; `frozen/FROZEN_ESTATE.json`; `resume/FIXTURES_RESUME_TC12-REG.txt`; `closure/FIXTURES_CLOSURE_TC12-REG.txt`; `progress/TC12-REG.json`; the scripts `tierc12_{fx, units, pins, frozen, registrations}.py` and `tierc12_{registrations, pins, resume, closure}_fixtures.py`. The commit also MODIFIES (does not add) `scripts/tierc12_progress.py` (L-0.9) and `PROGRESS.json`. **No bar is read and no book exists at or before this commit.** Then the child `TC12-REG.ledger-spec` (L-L): the fourth book's spec and the five-line ledger, in a commit of its own that is a proper descendant of the registry commit |
| TC12-D | L-D | the snapshot, its manifest, the pin record, the fee schedule with `FEE_GRAMMAR.json` and `FEE_SOURCE.json`, the contract specs, the sealed `data/FLAT_BAR_ATTEST.json` (its capture reads the venue's bulk archive read-only inside `--fetch`, nothing saved), their transcripts; `forward/BOOK4_FREEZE.json` (the orchestrator's, L-0.5). Its child `TC12-D.mirror` blocks nothing |
| TC12-ENV | L-D, L-0.12-0.16, L-0.22, L-X | first the child `TC12-ENV.vendor` (the vendored referee, its own commit); then the parent: `scripts/tierc12_env.py`; `tierc12_tables.py`, `tierc12_asof.py`, `tierc12_worktree_attest.py`; the suites `tierc12_{tables, attest, not, sweep}_fixtures.py`; the env, tables, attest, closure, not and sweep transcripts; last the child `TC12-ENV.score-build` (the regbook interface and the scorer's code; no TC12 book is read) |
| TC12-V | L-V | ALL of Stage V's code as artifacts of the record `TC12-V` — `analytics/value_area.py`, `scripts/tierc12_va.py` (DOOR 1), `tierc12_va_trades.py` (DOOR 2), `tierc12_va_stamps.py`, `tierc12_va_fixtures.py`, `tierc12_va_stamps_fixtures.py` (the children file tables, records and transcripts only, so DOORS_T's EARNED check has DOOR 2's source at this gate); DOOR 1's tables: the per-bar VA tables per lens, the event and regime tables, the mirror record (HALT on disagreement), **the traverse pins, frozen**; then the child `TC12-V.trades` (DOOR 2); and, each after the books it stamps, the children `TC12-V.stamps.c`, `.r`, `.s` (the reader's stamp tables) |
| TC12-C | L-C, L-G | first the child `TC12-C.tide` (the tide and breadth series); then the v6 book on the scored window and its strip; F-CTRL |
| TC12-G | L-G | the regbooks of P-ADM-1 and P-BRD-1; the admission Tier-E grids |
| TC12-R | L-R | the children `TC12-R.dir` (the regbook of P-DIR-1, the chop tables), `TC12-R.sfp` (the range walk, the regbook of P-SFP-VA-1), `TC12-R.tables` (the 1d take-profit venue); then the parent's index `stage_r/STAGE_R.md` |
| TC12-S | L-S | the regbook of P-SCALP-3, its twins and its miss table |
| TC12-L | L-L | the four-book ledger, the era tables, the ferry staged off-bus with its forecast |
| TC12-SCORE | L-X | the five score rows, the family record, the persisted draws |
| TC12-FIX | L-0.11 | every residual finding disposed (FIXED / CARRIED / ruled as AM-n); the full sweep GREEN |
| TC12-REVIEW | L-0.12 | one GREEN attestation per lens at the TC12-FIX commit; the judge record; fixes; a `fix-head` attestation if any commit followed |
| TC12-CLOSE | L-X, L-0.24 | the draft, findings-not-fixed, box and compute cost, the staged append, `close/close_acts.sh` (never run), the tc11-stamp proof |

**THE SUB-STAGE LAW** (ids, records, gates, the resume point, `depends_on`; O-31, OD-7). Every section conforms to it.
1. **Record ids.** `ORDER` in `scripts/tierc12_progress.py` is the stage list of record. A sub-stage is a dotted child
   `<ORDER entry>.<tag>` (X's form: `X-FOUND.books`, `X-FOUND.ranges`); its record is `T12/progress/<id>.json` and its
   `stage` key is the id. No id exists outside `ORDER` and the table `SUBSTAGES_T` below without a dated amendment.
   The merger sorts a child under its parent by its longest-prefix rule (`scripts/tierc12_progress.py:29-32`) [checked
   on every id below]. The rule is not cosmetic: an id such as `TC12-VENDOR` has no entry of its own and is matched
   by the prefix `TC12-V`, so the filed merger would place it at Stage V's position [measured here, by re-deriving
   `stage_key` on the name]. A vendored referee, a mirror step or any other pre-step is therefore a dotted child of
   the `ORDER` stage whose gate it belongs to (the frozen referee text: `TC12-ENV.vendor`; the Stage D mirror:
   `TC12-D.mirror`).
2. **`SUBSTAGES_T`:**

   | child id | owner | blocking | depends_on | what it files (directory) |
   |---|---|---|---|---|
   | `TC12-REG.ledger-spec` | L-L | yes | `TC12-REG` | `forward/BOOK_SPEC_COMBINED.json`, `forward/FORWARD_LEDGER.jsonl` (five lines), `tierc12_forward_spec.py`, `tierc12_forward_fixtures.py` |
   | `TC12-D.mirror` | L-D | **NO — the only non-blocking child** | `TC12-D` | `data/MIRROR_ATTEST.json` (PARTIAL allowed through CLOSE; harvested as a finding) |
   | `TC12-ENV.vendor` | L-D | yes | `TC12-D` | `vendor/tierc11_env@1526093b.py`, `vendor/README.md`, `scripts/tierc12_vendor.py`, `env/LINEAGE_PINS.json`, `scripts/tierc12_env_fixtures.py`, `env/FIXTURES_ENV_VENDOR.txt` (F-VENDOR [referee] runs from that suite at this record) |
   | `TC12-ENV.score-build` | L-X | yes | `TC12-ENV` | `scripts/tierc12_regbook.py`, `tierc12_score.py`, `tierc12_score_fixtures.py` (the scorer's code and its synthetic and anchor legs; no TC12 book is read), and `env/SIZE_MEASURED.json`, written by the score suite's F-VERDICT [SIZE] leg and read by the scorer at its certified sha |
   | `TC12-V.trades` | L-V builds, L-R defines | yes | `TC12-V` | `va/trades/**` (DOOR 2) |
   | `TC12-C.tide` | L-G | yes | `TC12-ENV` | `tide/**`, `scripts/tierc12_tide.py`, `scripts/tierc12_tide_fixtures.py` (committed with it, before `tierc12_books.py` exists) |
   | `TC12-V.stamps.c` | L-V | yes | `TC12-V`, `TC12-C` | `va/stamps/VA_STAMPS_{v6,trg912}.parquet` |
   | `TC12-R.dir` | L-R | yes | `TC12-V`, `TC12-C`, `TC12-V.stamps.c`, `TC12-ENV.score-build` | `regbooks/P-DIR-1/**`, `stage_r/dir/**` |
   | `TC12-R.sfp` | L-R | yes | `TC12-V`, `TC12-ENV.score-build` | `scripts/tierc12_rangewalk.py`, `regbooks/P-SFP-VA-1/**`, `stage_r/sfp/**` |
   | `TC12-R.tables` | L-R | yes | `TC12-V`, `TC12-C`, `TC12-ENV.score-build` | `stage_r/tables/**` (the 1d take-profit venue, L-R.30) |
   | `TC12-V.stamps.r` | L-V | yes | `TC12-R.sfp`, `TC12-R.tables` | `va/stamps/VA_STAMPS_<book>.parquet` for Stage R's books (L-V.19) |
   | `TC12-V.stamps.s` | L-V | yes | `TC12-S` | `va/stamps/VA_STAMPS_<book>.parquet` for Stage S's books |

3. **`RESUME_ORDER_T`** — the order in which records are gated and committed. It is held as data in
   `scripts/tierc12_progress.py` (`RESUME_ORDER`, with `SUBSTAGES`, beside `ORDER`, which stays the stage list of
   record; added at the TC12-REG commit, which modifies that script) and typed again in the resume fixture as its
   second object: `STEP Q` · `TC12-R0` · `TC12-LEANS` · `TC12-REG` · `TC12-REG.ledger-spec` · `TC12-D` ·
   `TC12-ENV.vendor` · `TC12-ENV` · `TC12-ENV.score-build` · `TC12-V` · `TC12-V.trades` · `TC12-C.tide` · `TC12-C` ·
   `TC12-V.stamps.c` · `TC12-G` · `TC12-R.dir` · `TC12-R.sfp` · `TC12-R.tables` · `TC12-R` · `TC12-V.stamps.r` ·
   `TC12-S` · `TC12-V.stamps.s` · `TC12-L` · `TC12-SCORE` · `TC12-FIX` · `TC12-REVIEW` · `TC12-CLOSE`.
   `TC12-D.mirror` is in no position: it may be gated at any time after `TC12-D`.
4. **THE RESUME POINT** = the first entry of `RESUME_ORDER_T` whose record is absent or not COMPLETE-VERIFIED.
   Derived, never typed, never stored. A non-blocking child never moves it.
5. **Start law.** A record may START iff every earlier entry of `RESUME_ORDER_T` is COMPLETE-VERIFIED — EXCEPT the
   parallel set `PARALLEL_T` = {`TC12-G`, `TC12-R.dir`, `TC12-R.sfp`, `TC12-R.tables`, `TC12-R`, `TC12-V.stamps.r`,
   `TC12-S`, `TC12-V.stamps.s`}, each of which may start once every entry through `TC12-V.stamps.c` and every record
   in its own `depends_on` are COMPLETE-VERIFIED (`TC12-G`: `TC12-C`, `TC12-C.tide`, `TC12-V.stamps.c`,
   `TC12-ENV.score-build`; `TC12-S`: `TC12-V`, `TC12-C.tide`, `TC12-R.sfp`, `TC12-ENV.score-build` — it imports
   `tierc12_rangewalk.fee_per_fraction`, filed at `TC12-R.sfp` with F-SFP-MIRROR GREEN). Commits still land in
   `RESUME_ORDER_T` order. One machine-wide worker cap (O-5). Wherever a reading says "after `<STAGE>` is
   COMPLETE-VERIFIED" as a START condition it means the RECORD `<STAGE>.json` and the children that precede the
   starter in `RESUME_ORDER_T` — never the stage-complete predicate of point 6 (TC12-V's stamps children `.r` and `.s`
   close after Stages R and S by design).
6. **Parent records.** Every `ORDER` stage files a parent record `<STAGE>.json`. Its `artifact_shas` are the files no
   child records: the stage's own artifacts, its index document where it has children (`stage_r/STAGE_R.md` = three
   pointers), and the transcripts of the L-0 suites run at its gate. An `ORDER` STAGE is COMPLETE-VERIFIED iff its
   parent record and every BLOCKING child are. The parent record of a stage with several producers (`TC12-REG`,
   `TC12-ENV`, `TC12-L`) is written by the orchestrator's gate step from the artifact maps each producer returns.
7. **One commit per record gate**, subject `tierc12(<record id>): …`; the grammar and the gate, run per record, are
   L-0.9's.
8. **Record keys** — L-0.9's list.
9. **Quarantine follows `depends_on`,** transitively (L-0.4): a record whose `depends_on` closure names a quarantined
   record becomes PARTIAL with it. Quarantine directories are `T12/_det_partial_<YYYYMMDD>T<HHMM>Z/`.
10. **Directory and transcript law** — L-0.9's, with its one typed exception `SHARED_DIRS_T`.
11. **Pre-substrate header.** A suite run at a record before `TC12-D` in `RESUME_ORDER_T` prints
    `as_of_last_closed_4h: (pre-substrate stage)` and `substrate: none`; F-ONE-CORRIDOR exempts exactly those records
    (L-0.7).
12. **Fixtureless records** stay the typed three (`STEP Q`, `TC12-R0`, `TC12-LEANS`). Every child has a fixture
    record.
**TEXT BEFORE RESULT** — seven orderings, each checked:
- (T1) the commit that first adds `REGISTRATIONS.json` is an ancestor of every commit that first adds a file under a
  book directory (the directories the stage table's owners name for `TC12-V.trades`, C, G, R, S, L, SCORE); and every
  book directory's `build_manifest.json` carries `registry_head` == `REGISTRY_PIN.json` `head`,
  `registrations_sha256` == the sha of `REGISTRATIONS.json` and `leans_sha256` == the frozen LEANS sha, each read by
  the builder from the files at build time. A builder HALTs when the registry is absent.
- (T2) every FITTED pin is committed before the first book that reads it: the traverse (TC12-V) before TC12-R and
  TC12-S (O-18).
- (T3) the fourth book's spec is committed before its first ride (O-24).
- (T4) the ferry's priority order and the report's "whole versus pointed-to" choice are LEANS text (L-L, L-X), so they
  are frozen at TC12-REG, before any verdict.
- (T5) no registered row's bootstrap of record is run before TC12-SCORE, and TC12-SCORE starts only when TC12-C, -G,
  -R, -S, -L and the three stamps children are COMPLETE-VERIFIED — no verdict is on the table while another
  registered book is being built. (The scorer's CODE is filed earlier, at `TC12-ENV.score-build`, with its transcript
  under `env/`; nothing is written under `scores/` before TC12-SCORE.)
- (T6) an amendment is committed before the artifact it changes is rebuilt.
- (T7) THE REBUILD LAW: once a registered row's regbook is filed, it is rebuilt only under a filed `AP-n` that names
  a build fact or a verifier's finding (L-0.5) — never because of what the book shows; the superseded regbook's sha
  and the AP id stay in the record's `notes`, the superseded files are quarantined (L-0.4), not deleted, and the
  scorer prints the superseded sidecar's n and ΣR beside the row (L-X.27).
SOURCE: `scripts/tierc12_progress.py:20-21`, :29-32 [read here]; the form `XR/tierc11x/REGISTRATION_PLAN.md:334-375`
[read here]; O-5, O-6, O-18, O-24, O-31; OD-7, OD-16; scout U9 H8.
RIVALS: score each family as its book completes — not taken: a verdict seen mid-build is the look the law forbids for
the rows still open. Stage D before REG (X's order) — not taken: `ORDER` as filed puts the texts first, and no
registration needs a bar (the pin is known by value, the lookbacks are read from `XR`, the traverse is cited by object).
New top-level ids for the pre-steps (`TC12-VENDOR`, a stamps stage) — not taken: O-31. One stamps record under
Stage V — not taken (OD-7): each stamps child closes after the books it stamps, so three records, each with its own
`depends_on`. The vendored referee at the registration stage — not taken: O-31 puts it inside TC12-ENV, after TC12-D.
FAILS-IF: **F-ORDER** (resume suite) FAILS IF, at `--at`, an ancestry of T1, T2, T3 or T6 fails
(`git merge-base --is-ancestor`); a book manifest lacks or mis-states `registry_head`, `registrations_sha256` or
`leans_sha256`; a file under the score directory is first added by a commit that is not a descendant of the commits
adding the five regbooks' `STATUS.json` (BUILT or closed by precondition) and the three stamps children's records
(T5); a regbook manifest's content sha
changes between two `tierc12(` commits with no `AP-n` id in that record's `notes` (T7); the commits that first add
the records' files are not in `RESUME_ORDER_T` order (`TC12-D.mirror` excepted: anywhere after `TC12-D`'s); a record
id on disk is in neither `ORDER` nor `SUBSTAGES_T`; the script's `RESUME_ORDER` / `SUBSTAGES` data differ from the
fixture-typed second object. (When a builder STARTED is not on file; the start law is the orchestrator's to keep, and
what is checked is its trace — the commit order and each record's `depends_on`.) Planted mutations (scratch repos):
a book manifest committed before the registry → RED; a manifest
whose `registry_head` is another hex → RED; the traverse pin committed after a range-book manifest → RED; a regbook
manifest changed in a second commit with no AP id → RED; `progress/TC12-G.json` first added before
`progress/TC12-V.stamps.c.json` → RED; a record file `TC12-VENDOR.json` planted → RED; a file under `scores/` added
before the record of `TC12-V.stamps.s` → RED.

**L-0.11 THE SWEEP DRIVER** — "a stage is COMPLETE only if its … fixtures RE-PASS now" (TC10 contract :12-13, named
by contract :5 "verify-or-quarantine") and "F-DET hash-identical" (contract :123)
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 64] the ferry suite's `--of-record` invocation is an act-mode run of the close acts; its transcript `ferry/of_record/F_ROWS_AT_CLOSE.txt` belongs to no record and neither the sweep nor F-ROLL counts it as a transcript of record.
READING: No sweep driver exists in either predecessor (scout U9 §1.4); TC12 files one:
`scripts/tierc12_sweep_fixtures.py` (a fixture module: it may use `subprocess`, and it is outside the decision glob).
THE ROLL is a list of INVOCATIONS, never typed: for each record in `RESUME_ORDER_T` (then `TC12-D.mirror`, if its
record exists), the `suite` strings of that record's fixture records, in record order. Two kinds of entry are LISTED
BY NAME AND NOT RUN: the sweep's own invocations, and a fixture record typed `provenance: true`
(`data/FIXTURES_MIRROR.txt`, the only one — its transcript's sha must still equal the record's; L-0.14 D). TOTALITY:
the set of script names in the roll equals the set of `scripts/tierc12_*_fixtures.py` on disk minus the sweep itself.
Each invocation runs once, sequentially (never two at
a time: suites spawn their own F-DET twins and workers under the O-5 cap), in a fresh process, with
`~/venvs/naiad/bin/python -B`, cwd = `M`, `PYTHONDONTWRITEBYTECODE=1`, `NAIAD_CACHE_DIR` = the absolute snapshot path
read from Stage D's manifest, `PYTHONHASHSEED` UNSET (hash randomisation left on, so an order-dependent transcript
shows as drift), no `--refile-transcript`, no leg filter. Before TC12-D is COMPLETE-VERIFIED the variable points at a
per-run scratch directory — never unset, never the future snapshot path (`engine/data.py:39-48` falls back to the live
cache when unset and `mkdir`s whatever it is given) — and the sweep asserts that directory is empty afterwards.
`--root`: every `tierc12_*_fixtures.py` accepts `--root=DIR` (all writes, transcripts and twins under DIR); the sweep
appends it to each recorded invocation when it runs inside the reproducibility lens, and the transcript written under
DIR must then be byte-equal to the transcript of record.
GREEN iff, for every invocation: exit code 0; the transcript's sha after == before == the record's
`transcript_sha_after`; no `_rerun.txt` or `_partial.txt` appeared; the transcript's tally line reads zero RED and
`GREEN + NOT RUN == legs_total` with NOT RUN equal to the record's `legs_not_run`. The sweep's own transcript
`T12/sweep/FIXTURES_SWEEP_<S>.txt` lists, per invocation, the name, the tally and the transcript sha — no wall time
and no load (those go to stdout and to `T12/sweep/_det_clock/<record id>.json`, which the nested `**/_det_*/` rule
already ignores, which is not an artifact, and which the gate copies into the progress record).
WHEN: the sweep suite runs at the gate of every `ORDER` stage from TC12-ENV. Before TC12-FIX its roll is the stretch
of `RESUME_ORDER_T` that closed since the last such gate — the records after the previous `ORDER` parent and before
this stage's parent record (the children gated in between; the roll may be empty, and is then printed as such). The
record being gated is not rolled: its record does not exist until step (3) of its gate, and its invocations are
re-run by step (2) (L-0.9). THE FULL SWEEP — every record before the one being gated — is of record at TC12-FIX,
again at the `fix-head` of TC12-REVIEW, and once inside the reproducibility lens with `--root=<scratch>`. SCOPE LAW for every fixture that enumerates "all modules" or "all tables" (resume, closure,
typed, not, sweep, and any stage suite that enumerates modules or tables of later stages): it takes
`--stage=<record id>` and its scope is the union of `artifact_shas` paths of the records up to that one in
`RESUME_ORDER_T` (for `TC12-D.mirror`, which has no position: the records up to `TC12-D`, and itself — whenever it is
gated), so an earlier record's transcript stays reproducible after later records add files; the latest
record's run additionally flags any matching file on disk that no record names (UNRECORDED). Stage V's transcript
therefore never enumerates a later stage's modules or tables: the legs that must (F-TRAV [a], [e]; F-VA-PINS [e]) are
helper legs, one instance per builder or book in the CONSUMING stage's suite (L-0.14).
SOURCE: TC10 contract :12-13; scout U9 §1.4 ("there is NO sweep driver script in either tree"; the gate method
`XR/tierc11x/progress/X-FIX.json` `gate_method.no_refile`); `scripts/tierc11_closure_fixtures.py:1161-1171`, :1174-1222
(`--root=`, the tally line, the `_partial` name) [read here]; `engine/data.py:39-48` [read here];
`XR/tierc11x/LEANS_X_AMENDMENTS.md:561` (AM-X26, an enumerating fixture turned RED by a later record); `T12/.gitignore`
[read here]; OD-17.
RIVALS: a gate agent running suites by hand (both predecessors) — not taken: the roll and its result would live in a
session, not in the repo. A non-fixture python driver — not taken: it would need a subprocess allowance in the
decision glob. An online or drive-dependent leg inside a rolled transcript, re-run at every sweep — not taken (OD-17):
the roll would depend on the network and on a mounted drive.
FAILS-IF: **F-SWEEP** FAILS IF any clause of GREEN fails, totality fails, or a provenance transcript's sha differs
from its record. Planted mutations (scratch root with shadow suites): a suite exiting 1; a transcript of record bent
by one byte (a `_rerun.txt` must appear and be caught); an unrolled `tierc12_zz_fixtures.py` on disk; a roll entry
whose script is missing; an invocation run with a leg filter (a `_partial.txt` appears); a shadow transcript whose
NOT RUN count is one more than its record's `legs_not_run`; a shadow provenance transcript bent by one byte — each
RED by its named detector.

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
  `git show <sha>:research_outputs/tierc12/PROGRESS.json`, every record's `artifact_shas` (the last record naming a
  path, in `RESUME_ORDER_T`, governs — L-0.4 (1)), and files `STAGED != RECORD`, `STAGED NOT IN RECORD`, `RECORDED
  NOT STAGED`, `NO RECORD`; (5) records
  BEFORE with X's four clauses, each through `git --no-optional-locks -C <worktree>`: `rev-parse HEAD`;
  `rev-parse --abbrev-ref HEAD` (detached iff it prints `HEAD`); `status --porcelain=v1 --untracked-files=all`;
  `status --porcelain=v1 --ignored=matching` (its sha256 and line count); (6) X-REC clause — the review's whole X
  binding: the MAIN tree's `XR/` (it is git-ignored and exists nowhere else; `E.X_REC` resolves there from any
  worktree, L-D.26) is verified against `XR/X_REC_MANIFEST.json`, whose own sha is the one `certified()` returns at
  the reviewed commit;
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
records or of a new snapshot"); AM-X26; `T12/.gitignore` (`x_rec/**` ignored, the manifest excepted) [read here];
OD-4 (the manifest's sha through `certified()`).
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
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 15] a law of every spawning builder: each spawned worker calls `E.read_set()` and returns it with its result and the parent merges them, so the VA-wall predicate L-D.26 evaluates inside `read_set()` is seen where a worker's exit code is not.
READING: Every parquet TC12 writes carries the nine columns of `TP.AS_OF_COLUMNS`, non-null on every row: the four of
`tierc8.stamp` (`as_of_last_closed_4h`, `as_of_panel_start`, `as_of_span_days`, `warranty`) and the five `stamp_n`
adds (`as_of_lens`, `as_of_last_closed_bar`, `as_of_panel`, `as_of_n_assets`, `as_of_substrate`).
- **IMPORT, not mirror.** The stamps are `E.TP.stamp_n`, reached only through the two writers of
  `scripts/tierc12_tables.py` below. The env door `scripts/tierc12_env.py` is the ONE TC12 module that
  imports `tierc10_panel`; every other module reaches it as `E.TP`. The import is held SAFE by four facts read from the source (sha256 `40b660cd…`) and re-proven by
  fixture: (i) the module imports only the lineage (`tierc9`, `tierc8`, `tierc7`, `tierc7_rules`, `tierc6`,
  `tierc6_rules`, `tierc5`, `tierc2_baseline`; :72-79) — not `tierc10_data`, not the census; (ii) its only
  import-time side effects are two `sys.path` inserts (:69-70) and `_U12 = resolve_unseen12()` (:322), a READ of
  `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` that HALTs on a broken record and writes nothing; (iii) its
  writers (`register` :1674, `_mark_scored` :1998, `run`'s manifest :2949) are functions whose default roots lie
  under `research_outputs/tierc10` (:96-101) and which TC12 never calls; (iv) `tierc2_baseline` binds its tape paths
  at import from `NAIAD_CACHE_DIR` (`scripts/tierc2_baseline.py:205-206`).
- **The wrapper: two writers and no third.** `scripts/tierc12_tables.py` owns exactly two parquet writers; no other
  non-fixture TC12 source calls `.to_parquet`, `TB.write_table` or a `TP` registry door.
  1. **`put`** — from `make_put(root, meta, lens) -> (put, W, K, SK)`, the 6-dp table writer through
     `E.TB.write_table` (declared key, the nine stamps, the collar unless the table is on `REGISTERED_TABLES_T`).
     `make_put` HALTs unless `root` resolves under `T12` (or under a `_det_*` twin root or a fixture's `--root`),
     HALTs if `root` resolves under `regbooks/`, and HALTs unless `meta` carries `last_closed_4h_close`,
     `panel_start`, `span_days`, `panel_name`, `n_assets` and `substrate` (so `stamp_n`'s fallbacks at :2551-2553 —
     "CLASSIC5", `len(CLASSIC5)`, `substrate()` — are never what stamps a table) and `lens` is a key of `TP.LENS_MS`
     (:2511-2512); it then returns `E.TP.make_put(...)`. The lineage's skip-empty law stands (an empty frame is not
     written and is listed under `skipped_empty`; :2577-2580).
  2. **`put_regbook(reg_dir, arm, df, *, meta, lens, kind) -> {path, content_sha, n}`** — HALT unless `reg_dir`
     resolves to `…/regbooks/<registration id>/` (under `T12`, under a `_det_*` twin root, or under a fixture's
     `--root`); `kind ∈ {base, scored, ladder, strip, tierE}` and agrees with the arm's name; the key `[symbol,
     entry_close_ms]` (`[arm, symbol, entry_close_ms]` when `kind == "strip"`) asserted unique by `E.TB.assert_key`;
     rows mergesorted on the key; the nine stamps by `E.TP.stamp_n`; the collar iff `kind ∈ {strip, tierE}` (asserted
     equivalent to "the arm is not on `REGISTERED_TABLES_T`"); **FULL FLOAT — no `_round_floats`**; a zero-row frame
     IS written, with the full schema; atomic `.tmp` then `os.replace`; `content_sha = E.TB._content_sha` of the
     full-float frame. It is TC11's `write_regbook` law (`scripts/tierc11_stage_g.py:1168-1178`) and the ONE
     `.to_parquet` call site in non-fixture TC12 code. Its only caller is `tierc12_regbook.write_arm` (L-X.24).

  Why two: `TB.write_table` rounds every float column before it writes (`scripts/tierc2_baseline.py:162-178`), and a
  base arm must hash, on `repr(float)`, to the book sha TC11 filed for the same campaigns (L-X.25) — TC11 wrote its
  arms at full float. A regbook arm through `put` could never hold that identity.
- **What each column says.** `meta` is the corridor meta of the build that produced the rows — the dict
  `E.TP.corridor_n(panel, pin_close_iso)` returns (:650-733). A table of the scored window is stamped with the SCORE
  EDGE (`pin_close_iso` = TC11's pin); a strip table, a VA table and every table that reads past the score edge is
  stamped with the PIN (L-0.7). `as_of_lens` is the lens of the row's own clock (the bar whose close is the row's
  instant: 4h for a v6-derived book, 5m for the scalper's orders, the lens itself for a per-bar VA table);
  `as_of_last_closed_bar` is `lens_edge(hi, lens)` (:2515-2525; 1w Monday-anchored), or the tape's own measured edge
  passed as `lens_last_closed_ms` when the tape ends earlier — `stamp_n` HALTs if an edge falls after the corridor end
  (:2546-2548). A table whose rows belong to another panel than the build's is stamped with its own `meta_` (:2573-2576).
  A member of another lens carried on a row (the V5 vector) carries that member's own bar-close column — L-V.20's
  `<ℓ>_bar_close_ms`; the nine stamps do not stand in for it.
- **Manifests.** Every directory holding parquet has one `build_manifest.json` written by the same helper: `sha`
  (content sha per table), `keys`, `skipped_empty`, `input_sha`, `seed`, `as_of`, `substrate`, `code_sha`,
  `contract_sha256` (the STEP Q prefix sha, L-0.1 — never the whole-file sha), `leans_sha256`, `registry_head`,
  `registrations_sha256`, `amendments_of_record`, `pins` — sorted keys, and none of `TP.VOLATILE_META` (:625) or any
  other clock field. A regbook directory's manifest is written through L-X.24's `tierc12_regbook.write_manifest`
  (declared key per arm, content shas, `registry_head`, `registrations_sha256`).
- **The open log, `READ_SET.json`.** Beside every `build_manifest.json` it writes, the manifest helper writes
  `<dir>/READ_SET.json` = the sorted union of `E.read_set()` over the builder process and its spawn workers (each
  worker returns its set with its result; merged in key order), plus `licence_reads` (the reader's log of its
  `licence` calls, L-V.2). `E.read_set() -> {class: sorted paths}` (L-D.26) holds every READ open since the hook was
  armed whose class is one of `tc12-snapshot`, `tc10-allow`, `tc11-allow`, `x-rec`, or `tc12-record` (a path under
  `T12/` outside any `_det_*` segment); paths repo-relative, or snapshot-relative for the snapshot. In a directory of
  `SHARED_DIRS_T` the file is `READ_SET_<record id>.json`. It is a member of the directory's determinism set and is
  re-derived in the F-DET twin. It is THE object these legs read: L-0.30's 5m leg (a) and its LICENCE leg; F-SCALP (g)
  READ-SET; L-D.27's verified-read law; L-L.9's declared snapshot read set; the `VA-BLIND` clause of L-0.22; the
  `depends_on` floor of L-0.9. (The referee's own log is the in-memory dict of ONE process; a fixture is another
  process and never saw a spawn worker's opens — hence a file.)
SOURCE: `scripts/tierc10_panel.py:2510-2588` [read here]; `scripts/tierc8.py:96-111` [read here];
`scripts/tierc2_baseline.py:155-188` [read here]; `scripts/tierc11_stage_g.py:1168-1178` (`write_regbook`:
`TP.stamp_n`, the collar for `tierE`, then `to_parquet` — no `write_table`, no rounding) [read here]; the import
facts at the lines cited [read here]; `scripts/tierc11_env.py:1161-1163` (`opened_paths`, one process's dict) [read
here]; `XR/tierc11x/LEANS_X.md:431-436`, :482-483 [read here]; O-3, O-5; OD-5; scout U9 §1.7.
RIVALS: MIRROR the nine columns into TC12 code, held equal by reading `AS_OF_COLUMNS` with `ast` — not taken:
`tierc10_panel` is in every TC12 process regardless (the control ride, the corridor and the book sha are its
functions), so a mirror removes no import and adds a second implementation of `lens_edge` that F-KEY, which checks
names and nulls, could not tell from the first. Import `tierc10_panel` directly in each builder — not taken: one door.
Every parquet through the rounding writer — not taken (OD-5): the base arm's book identity is on full-float bytes.
Each book stage writing its arms with its own `to_parquet` — not taken: one full-float site, typed and guarded.
FAILS-IF: **F-WARRANTY** (`scripts/tierc12_tables_fixtures.py`) FAILS IF (a) IMPORT-SAFETY: in a fresh subprocess, a
`(path, bytes, mtime_ns)` census of `research_outputs/tierc10`, `research_outputs/tierc11`, `scripts/`, `analytics/`
taken before and after `import tierc12_env` differs, or the hook's write log is non-empty, or the set of frozen-estate
files opened at import is not the typed one; (b) `E.TP` is not the module loaded from `scripts/tierc10_panel.py` at the
sha L-D pins, or `E.TP.AS_OF_COLUMNS` is not the fixture-typed tuple; (c) `make_put` accepts a root outside `T12` or
under `regbooks/`, a `meta` missing a required key, or an unknown lens; `put_regbook` accepts a directory that is not
a `regbooks/<registration id>/`, a `kind` outside the five or at odds with the arm's name, or a duplicated key;
(d) AST: a non-fixture TC12 source other than the env door imports `tierc10_panel`; any calls `.to_parquet` /
`write_table` outside the wrapper's two writers, or calls a `TP` registry door; `put_regbook` has a caller other than
`tierc12_regbook.write_arm`; (e) FULL FLOAT: an arm written by `put_regbook` and read back differs from the frame
handed in on any float bit, or a zero-row frame leaves no file; (f) OPEN LOG: a directory's `READ_SET.json` omits a
path a spawn worker opened, or differs from its F-DET twin's. Planted mutations: `put_regbook` called with a root
under `T12/books/` → (c) RED; `put` called with a root under `regbooks/` → (c) RED; a `df.to_parquet(…)` bypass in a
shadow builder → (d) RED and the table fails F-KEY; `_round_floats` applied inside a `put_regbook` copy → (e) RED; a
`meta` without `substrate` → (c) RED; a worker's read set dropped at the merge in a shadow helper → (f) RED; a shadow
env that writes a file under `research_outputs/tierc10/` at import → (a) RED; a shadow env binding `TP` to a copy of
the panel module with one stamp column renamed → (b) RED; a scored-window table stamped with the pin instead of the
score edge → RED under F-KEY's stamp-truth leg (L-0.21).
UNVERIFIED: fact (ii) says which estate file the import reads when run alone; what `import tierc12_env` reads in full
depends on L-D's import windows and is established by leg (a) at TC12-ENV.

**L-0.14 EVERY FIXTURE LEG STATES ITS FAILURE CONDITION** — "every fixture leg states its failure condition"
(contract :6-7); "FIXTURES (each states its failure condition)" (contract :114)
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 3] `NOT_RUN_FIDS_T`, as assembled at the freeze: L-D's F-MIRROR and the body-file leg of F-TOLL [data]. A generic 'a leg that cannot run prints NOT RUN' sentence in any other section earns no entry; such a leg reads FAIL.
- [seam 31] the one non-transcript file a fixture suite writes: `env/SIZE_MEASURED.json`, by the score suite's F-VERDICT [SIZE] leg at `TC12-ENV.score-build`, under the transcript no-clobber law.
READING: One harness, `scripts/tierc12_fx.py` (stdlib only), a COPY — never an import — of the harness of record in
`scripts/tierc11_closure_fixtures.py`: `say` (deterministic line → transcript, temp paths scrubbed), `clock` (stdout
only), `prove(fid, title, break_if, real_if, break_leg, real_leg)`, `plants(rows)`, `file_transcript(out, body,
refile)` and the `main` protocol; plus the wrapper `not_run` (C) and the HELPER LEGS — F-KEY, F-DET, F-COLLAR, F-GRID
(L-0.21, L-0.20, L-0.16, L-0.15) and L-V's F-TRAV `[a]`, `[e]` and F-VA-PINS `[e]` — which take the shim, pandas and
their directory, grid, builder or book as ARGUMENTS from the calling suite. The harness itself imports nothing but
the stdlib: that is what lets the pre-substrate suites use it, and what earns its place among the process tools
(L-0.17).
- **A. The leg law.** A leg is one `prove` call and one transcript block; `legs_total` counts blocks. A fixture with
  lettered legs files one block per leg. The BREAK leg runs first and must go RED, or the leg is VOID and counts RED;
  a break leg that raises proves nothing (VOID). A break leg is `plants(rows)`, rows =
  `(name, expected detector substring, thunk → findings)`, judged ONE AT A TIME: caught only if a finding NAMES THE
  INTENDED DETECTOR; no finding = the plant passed (VOID); a crash = a FIXTURE DEFECT (VOID); a `SystemExit` is a
  finding carrying its own text. The transcript prints, for every block: `<block id> — <title>`,
  `  [BREAK] FAILS IF: …`, `  [BREAK] deliberate violation -> RED (correct): …`, `  [REAL]  FAILS IF: …`,
  `  [PASS|FAIL] <block id>: …`.
- **B. Block id** = `<FID>` or `<FID> [<qualifier>]`; `FID` matches `F-[A-Z0-9]+(-[A-Z0-9]+)*`; `<qualifier>` =
  `<leg>`, or `<instance>`, or `<leg> · <instance>`, with `<leg>` = `<letter> <NAME>` or `<NAME>` and `<instance>` a
  registration id, arm, book, directory or grid id; no bracket inside a qualifier. Examples: `F-SCALP [a HAND-3]`,
  `F-GATE [SET · P-ADM-1]`, `F-KEY [stage_g]`, `F-TRAV [e · P-SFP-VA-1__scored]`, `F-TOLL [data a]`,
  `F-LEDGER [PREFIX]`, `F-NEST-ASOF [v6]`. The block id is the `fid` handed to `prove`.
- **C. Leg states.** PASS and FAIL come from `prove` (a VOID fixture counts FAIL). **NOT RUN** is a third state,
  written by the wrapper `not_run(fid, title, reason)` outside `prove` (it prints the block header and
  `  [NOT RUN] <fid>: <reason>`); it is never PASS. The tally line is `  N GREEN, M RED, K NOT RUN`; the fixture
  record carries `legs_not_run`; a transcript is GREEN iff zero RED and `GREEN + NOT RUN == legs_total` with NOT RUN
  equal to the record's. A NOT RUN block of a contract-named FID is RED at TC12-FIX. NOT RUN is lawful only for a
  leg whose OWNING READING names the condition under which it cannot run — an absent provenance input (the mirror
  drive; a saved fee-page body) — and `reason` is that condition; the FIDs that may ever print it are the
  fixture-typed `NOT_RUN_FIDS_T`, assembled from those readings at freeze, so no other leg can leave a gate unrun.
  **CLOSED-NO-BOOK** is a PASS, not a fourth state: a fixture whose population is the book of a registration that
  reads CLOSED_BY_PRECONDITION runs its SYNTHETIC legs unchanged and, for each REAL-BOOK leg, its real leg prints
  `CLOSED-NO-BOOK <registration id>` and asserts from files that `regbooks/<id>/STATUS.json` says
  `CLOSED_BY_PRECONDITION` and lists no arm (BREAK plant: a STATUS copy reading `BUILT`, or listing an arm →
  detector `CLOSED-STATUS`). F-ROLL prints such a fixture `PASS (row closed by precondition: real legs
  CLOSED-NO-BOOK)`. A data leg of F-NOT whose only tables belong to a closed registration is CLOSED-NO-BOOK by the
  same rule, never `NO TABLE IN SCOPE`. Which legs of a fixture are synthetic and which are real-book is stated by
  its owning reading.
- **D. No fixture leg makes a network call, and no drive-dependent leg is part of a transcript of record.** A
  transcript typed PROVENANCE (`data/FIXTURES_MIRROR.txt`, the only one) is recorded by sha with `provenance: true`,
  is excluded from the sweep's byte-identity roll and is listed there by name.
- **E. The contract-name → block map** is L-0.19's.
- **BANNED:** self-comparison; one example where cardinality was possible; a check whose claim is not the design's
  claim. **Production against production:** a sabotage is planted INSIDE the production function (a shadow copy of
  the source, or a monkeypatched object in the production call path), never in the comparator; a leg whose two sides
  are both fresh oracles tests nothing in production. Hook legs run in subprocesses. Truncated-tape legs build fresh
  arrays, never through a symbol-keyed memo. An as-of leg that holds a fitted pin holds it at its filed value on every
  prefix and says it does not test the fit.
- **F. Fixture randomness.** Every fixture stream is `numpy.random.default_rng([SEED, crc32("<suite tag>|<block
  id>")])`, `<suite tag>` = the suite's stem without `tierc12_` and `_fixtures` (`va`, `stage_r`, `scalp`, `tide`, …).
  Each seeded leg states its count `n` in the OWNING reading as a fixture-typed literal (where X or the lineage filed
  a count for the mirrored leg, that count, with its source) and prints it in the transcript header. Which seed
  expressions resolve is F-SEED's rule (L-0.2).
- **G. THE HAND-SAMPLE LAW (one law, every section)** ("3 … hand-verified", contract :117-120). The sample is chosen
  by a rule frozen in the owning reading before any book exists: categories first — the first row of each named
  category in the reading's stated key order.
  (1) A category with no member prints `NONE-EXISTS <category>`, asserts from the population that its count is zero,
  and its slot is taken by the next unchosen row in key order, printed `FILL`.
  (2) If the population holds `n < k` rows (`k` = the contract's count), ALL `n` are verified, the leg prints
  `ONLY <n> EXIST (contract count <k>)` and asserts the population's count equals `n`; `n = 0` prints
  `EMPTY POPULATION` with the same assertion.
  (3) The leg is GREEN in every such case; a shortfall, or an empty CONTRACT-NAMED category (F-SFP's POC fill or
  time-stop exit), is printed `FINDING: …` and carried to the report as a finding-not-fixed owned by the operator.
  (4) No hand-sample leg is RED or VOID on the size or composition of a population; only a mismatch between the
  fixture's derivation and production is RED.
  A sample that has no categories is a seeded draw under F over the key-sorted population. The transcript prints the
  rule and the chosen keys.
- **Fixture-typed literals are a second object.** A fixture types its own commission (expected cells, columns, names,
  the pin line, a seeded leg's count) and compares production against it; it never reads the production module's own
  constant as its referee. Each suite prints its typed literals in its header.
- **H. Every `tierc12_*_fixtures.py` accepts `--root=DIR`** (all writes, transcripts and twins under DIR); the sweep
  appends it to each recorded invocation when it runs inside the reproducibility lens.
- **I. Header and transcripts.** Transcripts are `T12/<dir>/FIXTURES_<X>.txt` (each suite's row of its owner's suites
  table names the file). First line `as_of_last_closed_4h: <pin ISO>`; at a record before TC12-D:
  `as_of_last_closed_4h: (pre-substrate stage)` and `substrate: none` (L-0.10 point 11); then the banner and
  `seed … · substrate … · pin …`. They carry no clock, no temp path, no absolute home path, no source line number, no
  worker count, no load, no live HEAD. NO-CLOBBER: an absent transcript with no `--refile-transcript` is a finding and
  nothing is written; identical bytes are silent; different bytes without the flag go to `<stem>_rerun.txt`, the
  record untouched, RED; a leg-filtered run writes `<stem>_partial.txt`, and no gate runs one (a suite that serves
  several records is scoped by `--stage`, L-0.9). Exit 1 on any RED, VOID or transcript finding.
  "Byte-identical across runs" is held by four runs of every transcript of record in fresh processes with hash
  randomisation on: the filing run, the record gate's re-run, the TC12-FIX sweep, and the reproducibility lens's
  re-run.
- Every record that runs a fixture files a transcript, and its progress record carries the sha before and after.
SOURCE: `scripts/tierc11_closure_fixtures.py` (sha256 `68253ed1…`): the law :73-84, `say` :169-172, `clock` :175-176,
`prove` :183-204 (two outcomes, appended to `PASSED` / `FAILED`), `plants` :207-238, `file_transcript` :1161-1171,
`main` :1174-1222 (the tally line and `--root=`), `AS_OF_LINE` :115 [read here]; `XR/tierc11x/LEANS_X.md:2282-2299`
(LX-F.1) and :2309 (the key-order selection rule of F-SFP) [read here]; O-3 (why a copy: importing that file runs
`import tierc11_env`, which arms TC11's hooks); OD-17.
RIVALS: import TC11's harness — not taken: O-3. A pytest suite — not taken: no BREAK-first law, and pytest writes
caches into the tree. A hand-sample leg that is RED when a registered book comes out small — not taken (OD-17): the
size of a book is an outcome, and a fixture that stops the build on it hands a decision to someone who has seen the
book. NOT RUN counted as PASS, or left unrecorded — not taken: a leg nobody ran proves nothing, and a tally that hides
it cannot be re-derived. A new state inside `prove` — not taken: `prove` stays AST-identical to its referee.
FAILS-IF: **F-FX-MIRROR** (closure suite) FAILS IF `ast.dump` of `say`, `clock`, `prove`, `plants` or
`file_transcript` in `scripts/tierc12_fx.py` differs from the same function parsed from the TEXT of
`scripts/tierc11_closure_fixtures.py` (its sha asserted from the census), or the harness imports anything outside the
stdlib. **F-FX-FORM** FAILS IF, by AST over every `scripts/tierc12_*_fixtures.py`, a `prove` call has an empty
`break_if` or `real_if`, a `plants` row is not a triple with a non-empty detector string, a leg's break leg is not a
`plants` call, a `not_run` call names an FID outside `NOT_RUN_FIDS_T`, a suite does not parse `--root=`, a
`default_rng` seed is not of F's form, or a suite imports a module of the fixture-typed network list (`socket`,
`ssl`, `http`, `urllib.request`, `requests`, `ftplib`); or a transcript of record has a block id outside B's grammar,
a PASS or FAIL block lacking either `FAILS IF:` line, a NOT RUN block that is not exactly its header and its
`[NOT RUN]` line, or a tally line not of C's form. Planted mutations: `plants` in a harness copy changed to count a
crash as a catch → F-FX-MIRROR RED; `import pandas` added to a harness copy → RED; a `prove(…, break_if="", …)` in a
suite copy → RED; a transcript copy with one `[REAL]  FAILS IF:` line removed → RED; a block id `F-GATE (P-ADM-1)` in
a transcript copy → RED; `not_run("F-SCALP [a HAND-3]", …)` in a suite copy → RED; `import urllib.request` in a suite
copy → RED; a tally line without its NOT RUN count → RED.

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
  A report may point to a grid printed whole in its stage document; that is not an abbreviation — the pointer row
  carries the stage document's path, its sha and the grid's cell count, and which grids the report prints whole and
  which it points to is frozen in L-X.28, before any verdict (L-0.10 T4).
SOURCE: `scripts/tierc10_panel.py:2592-2625` (`grid_whole`) [read here]; `XR/tierc11x/LEANS_X.md:485-486`, :2315 (F-GRID
row; "NaN without `nan_reason`") [read here]; `T11/stage_g/STAGE_G.md:197` [read here].
RIVALS: print only non-empty cells — not taken: a missing cell and an empty cell would look alike. Type the count in
the builder — not taken: the builder would then assert its own number.
FAILS-IF: **F-GRID** (helper legs in `tierc12_fx.py`, run by each owning stage's suite per grid) FAILS IF a cell is
missing, undeclared or duplicated; a count equality fails; a partition's Σ `n` differs from the population; a
statistic is NaN without `nan_reason`; a collar or stamp column is absent or null; `promotable` is True on any row; a
verdict column exists; a printed grid's row count or cell ids differ from the parquet's; a report's pointer row names
a stage document that does not print that grid whole, or carries another sha or cell count. Planted mutations
(copies): a dropped cell; an added cell; a duplicated cell; an `n = 0` row removed; a NaN with its `nan_reason`
nulled; `promotable = True` on one row; one member row moved to no cell (partition off by one); a printed table with
one row deleted; a pointer row whose stage document has that grid truncated — each RED. On the directory of a
registration closed by precondition the instance is CLOSED-NO-BOOK (L-0.14 C).

**L-0.16 THE SELECTION COLLAR** — ""a SELECTION, not a result" on every non-registered table" (contract :7)
READING: A REGISTERED table is a table a frozen reading names as a row of record: the five score rows of §0 (contract
:126); each registered row's regbook of record and its base arm, and the arms a registered row's `verdict_rule` reads
(P-SCALP-3's `ladder__touch`, `ladder__deep`) — that is, every regbook arm of kind `scored`, `base` or `ladder`; and
the mirror's licence record `T12/va/VA_MIRROR.json` (L-V.17). The typed list `REGISTERED_TABLES_T` is assembled from
those readings at freeze. EVERY OTHER parquet TC12 writes — the 9/12 book, every twin, shadow, slice and strip (every
regbook arm of kind `strip` or `tierE`), every Tier-E grid, the per-bar VA tables and their stamps, the two-trades
tables, the traverse table, the ledger and era tables — carries the collar; the tables helper HALTs on a table that
neither carries it nor is on the typed list.
- **The helper** is `collar(df, would, m)` in `scripts/tierc12_tables.py`, a mirror of X's `collar` with one column
  added. It writes, in this order: `tier = "TIER-E"`; `selection_not_a_result = "a SELECTION, not a result"`;
  `gates = "nothing"`; `would_read_ci_only`; `m_looks_this_table` (= the number of intervals — `lo`, `hi` pairs — the
  table holds, every leave-one-asset-out panel counted; the scorer's count over `SCORES.json beside[]` is L-X.14's);
  `m_note` (X's sentence, verbatim); and `promotable = False`. X carried `promotable` on grids only; the contract's
  "no promotion from any Tier-E table" (:133) names every table, so TC12 carries it on every collared table.
- **`would_read_ci_only`** takes one of TC11's four values and nothing else: "CI above zero (lo > 0)", "CI includes
  zero", "CI wholly below zero (hi < 0)", "no interval". A descriptive table prints no interval ("no interval",
  `m_looks_this_table` zero); a scorer-computed Tier-E row prints its CI-only reading (L-0.28). No collared table or
  leaf holds a verdict word, or a key or column named for a verdict, a cleared bar or a spent test: the forbidden-name
  pattern is `verdict|clears|spent_test` (case-insensitive) — TC11's pattern widened from `clears_bar` to `clears`,
  so that a boolean such as `clears_literal_bar` cannot sit in a Tier-E leaf.
- **In documents**, every markdown table is preceded, within the three lines above its header, by the registered
  marker `<!-- registered: <id> -->` or by the line "TIER-E — a SELECTION, not a result — gates nothing". The
  registered marker is allowed in score documents, §0, and §4's verbatim re-quote of P-SCALP-3's `verdict_text`
  (L-X.28), and nowhere else. A Tier-E statistic printed INSIDE a §0 row carries the collar string inline.
SOURCE: `XR/scripts/tc11x_exit.py:1175-1185` (`collar`), `XR/scripts/tc11x_books.py:131-138` (`M_NOTE`, `COLLAR`,
`COLLAR_COLS`) [read here, as text]; `scripts/tierc11_score.py:258-263` (`COLLAR`, `CI_READINGS`, and at :263
`FORBIDDEN_TIER_E_KEY_RX = verdict|clears_bar|spent_test`) [read here, as text]; the literals read from that script
are pinned by the sha of their AST node, never by the file's sha (L-0.24); `XR/tierc11x/LEANS_X.md:814-830` (LX-1.4)
[read here]; `T11/LEANS.md:128-131` [read here]; scout U1 §1.12 (TC11 collared a per-campaign Tier-E table,
`g_campaign_gates.parquet`).
RIVALS: TC11's three-column dict — not taken: it drops `m_looks_this_table`, the record of how many ways the tape was
cut. Collar only aggregate tables (X's practice for journals) — not taken: a copied row of a Tier-E twin would carry
no mark, and a blanket rule with a typed exemption list is checkable by totality; it cannot flatter.
FAILS-IF: **F-COLLAR** (helper legs, run per directory by each stage's suite, and a mirror leg in the tables suite)
FAILS IF a parquet not on `REGISTERED_TABLES_T` lacks a collar column, holds a null in one, a `would_read_ci_only`
outside the four values, `promotable` True, a column (or, in a collared JSON leaf, a key) matching
`verdict|clears|spent_test`, or an `m_looks_this_table` that is not the fixture's own count of the table's intervals;
a table on the typed list carries the collar; a document table has neither marker nor collar line, or carries the
registered marker outside score documents, §0 and §4's re-quote; the helper's column tuple, its SELECTION string or
its `m_note` differ from `COLLAR_COLS`, `COLLAR["selection_not_a_result"]` and `M_NOTE` read by `ast.literal_eval`
from the TEXT of `XR/scripts/tc11x_books.py` (never executed), or its `tier` / `gates` strings and the four readings
differ from `COLLAR` and `CI_READINGS` read the same way from `scripts/tierc11_score.py`. Planted mutations (copies):
a collar column dropped; `would_read_ci_only = "SUPPORTED"`; `promotable = True` on one row; a `verdict` column added;
a `clears_literal_bar` key added to a collared leaf; an interval-bearing row added with `m_looks_this_table` left
unchanged; a document table with its collar line deleted; the registered marker placed above a §5 table; the helper's
`m_note` changed by one word — each RED.

**L-0.17 NO NUMBER TYPED THAT A FILE CAN SUPPLY** — "no number typed that a file can supply" (contract :8); also
"F-TRAV greps for typed constants → FAIL" (:43) and "F-TOLL (maker bps read, never typed …)" (:121)
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 6] an 'asserted equal' whose second object is not on file at TC12-REG is asserted by the pin's CONSUMER at its own stage's gate, never by the stdlib-only pin door at filing.
- [seam 35] the pin register filed at TC12-REG carries `lineage` rows (sha256 of `ast.dump(node)`) for the literals L-X reads from `scripts/tierc11_score.py` (the sixteen columns, `HAIRCUT_TOL`, `SUM_TOL`, `NET_LAW_TOL`, `EXIT_FLAGS`) and the pin-map rows `fam.q`, `fam.<stage letter>`, `seed` and `loao.line`.
- [seam 39] the contract token `0.000e+00` (:49, :114) is a PRINT-FORMAT token: classed in `CONTRACT_TOKENS_UNPINNED.json`, never a pin; F-CTRL passes iff the worst difference `== 0.0`.
- [seam 45] for a second-object pin held equal to a filed value (`adm.lag_cut`, `adm.abs_cut`, `adm.preseen_cell`, `ctrl.sum_net_r`) a bend that HALTs the build at its assertion counts as flow.
- [seam 63] `PIN_REGISTER` consumers name `TC12-REG.ledger-spec` and `TC12-L` for `ledger.*`, `adm.lag_cut` and `seed`, and `TC12-L` / `TC12-CLOSE` for `ferry.*`.
READING: Every number a TC12 non-fixture source uses comes through a DOOR from the file that supplies it. The doors:
- **The contract** — `scripts/tierc12_pins.py`, reading the prefix (L-0.1) with the filed map
  `T12/pins/CONTRACT_PIN_MAP.json`: one row per contract pin, `{pin, lines [a, b], regex (one or more capture groups),
  type (a tuple of the regex's arity; members ∈ {int, fraction, word, iso, str}), word_map (for a word such as "half",
  contract :71), also [{lines, regex, group (optional: the capture group of this citation that must equal the row's
  value when arities differ)}]}`. No `veto` field here. A multi-group row's value is a tuple.
  Values are parsed exactly (`fractions.Fraction` on the captured text) and converted to float only at the use site.
  Where a value stands in two places of the contract (a stage line and the VETOES line :135-137, or a family header's
  bar and "0.10 ÷ m" :9), `also` holds the second citation and the pin door HALTs unless both parse to one value. The
  derived values are filed as `T12/pins/CONTRACT_PINS.json`; at every run the pin door re-derives them from the prefix
  and HALTs unless equal to the filed file. The map is DATA, so no contract line number is typed in code. The pin door
  is stdlib-only: it runs at TC12-REG, before any substrate, and imports neither the shim nor the lineage. Where a row
  says its value is "asserted equal to" another object, the door makes that comparison itself when the object is a
  literal of a frozen file — read as TEXT (`ast`) or as JSON, with the file's manifest sha or the literal's node sha
  asserted — and otherwise the pin's consumer makes it at its own stage, as that pin's flow-leg witness.
- **X's records** — e.g. the lookbacks `XR/tierc11x/pins/PINS_X.json` `L.by_lens.<lens>.L_of_record` (O-15), each
  read with its sha asserted against the manifest.
- **Stage D's records** — the pin, the tick (`price_tick`, O-20), the fee schedule's bps (O-19).
- **Fitted pins** — the traverse (O-18) — the door is `tierc12_va_stamps.traverse` (L-V.2): `traverse(name) ->
  (value, source)` HALTs unless `T12/va/TRAVERSE.json` is at its certified sha, and its `source = {path, key, sha256,
  value}` is what a book manifest files as `time_stop_source`. No consumer opens that file itself.
- **Lineage objects** — read by attribute, never retyped: `E.R2.ATR_LEN` (`scripts/tierc2_rules.py:121`),
  `E.R5.WARMUP_BARS` (`scripts/tierc5_rules.py:233`), `E.TP.N_BOOT` (`scripts/tierc10_panel.py:94`), `E.TP.LENS_MS`
  (:2511), `E.TP.ERA_CUT_MS` (:747), `PROFILE_ROWS` and `VALUE_AREA` of `analytics.profile`
  (`analytics/profile.py:21-22`; by attribute inside a door, as text anywhere else — L-0.22), the write rounding's
  decimals (the default of `TB._round_floats`' `nd`, `scripts/tierc2_baseline.py:162`, read from the signature). Where
  the contract also states such a value (70% of volume, :29, against `VALUE_AREA`), the lineage object is what code
  reads at run time and the pin door asserts the two equal. A literal read by `ast` from a TC11 script that TC12's own
  close acts move is pinned by the sha of its AST node (`sha256(ast.dump(node))`), never by the file's sha (L-0.24).

`T12/pins/PIN_REGISTER.json` lists every pin of EVERY door, one row each: `{pin, kind ∈ {contract, x_record, stage_d,
fitted, lineage, ruling}, source {path, key or lines}, door, consumers [record ids], witness, veto (a token of
:135-137 or null)}`. A `ruling` row has no value. `witness` names what must move when the pin is bent at its door.
**PIN NAMES OF RECORD** (sections use these and no other): `seed`; `fam.q`, `fam.<stage letter>`; `ctrl.sum_net_r`
(:49); `va.accept_n`, `va.accept_margin_atr` (:35); `va.sfp_k` (:36, also :135); `va.nest_frac` (:45, also :135);
`va.value_area_pct` (:29); `va.mirror_words` (:39-40); `va.licence_set` (:41); `va.lookback.<lens>` (x_record / the 1w
row `source_lens: 1d`; value in `VA_PINS.json by_lens.<lens>.L_bars`); `adm.old_quantile`, `adm.lag_cut` (:54);
`adm.preseen_cell` (:55, two groups); `adm.abs_cut` (:56); `brd.cut` (:58, two groups; also :135); `rr_min` (:73; also
:100 and :135-136 — ONE pin for both range rows; `scalp.rr_min` is not a name); `sfp.rail_atr`, `sfp.t1_fraction`
(:71); `sfp.t2_offset_atr` (:72); `chop.n_bands` (:68); `tp1d.approach_atr` (:80); `two_trades.horizons` (:79, two
groups, asserted equal to X's `pins.laws.horizons`); `book.trg912_periods` (:44, two groups, asserted equal to R912's
`trg_f`, `trg_s`); `grid.x16_shape` (:60, asserted equal to the four axes' cardinalities); `grid.brd_levels` (:59,
asserted equal to (0, N)); `scalp.third_long_max`, `scalp.third_short_min` (:87; also :136 by `group`);
`scalp.ema_fast`, `scalp.ema_slow` (:89); `scalp.trigger_prox_atr` (:90); `scalp.validity_bars` (:92; also :136);
`scalp.fill_ticks` (:94; also :136); `scalp.deep_atr` (:94-95); `scalp.stop_beyond_atr` (:97); `scalp.rail_atr`
(:98); `scalp.t1_fraction`, `scalp.t2_offset_atr` (:99); `scalp.era` (:83; also :137); `loao.line` (:106, two groups);
`ledger.opening` (:109); `ledger.n_min` (:110); `ferry.bus_dir` (:111); `ferry.cap_mb` (:112);
`fee.maker_bps_side.<VENUE>` (stage_d: `data/fee_schedule.json venues[<VENUE>].maker_bps_side`); `traverse.<lens>`,
`traverse.1h.in_5m_bars` (fitted); `ruling.tc11_stamp`, `ruling.1w` (ruling). Every name is a register row; a name
of kind `contract` (the seed, the family rows and every name cited to a contract line) is also a map row; the VETOES
tokens name register rows through `VETO_ROWS_T` (L-0.23).
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
compute on a bar by itself — `scripts/tierc12_fx.py` (its helper legs run only inside a fixture suite, on the objects
that suite hands them, L-0.14), `tierc12_progress.py` (filed at R0; its one number is the header's seed label, held
equal to the contract pin by F-RESUME), `tierc12_worktree_attest.py`, `tierc12_frozen.py`. RENDERERS (the
close generator's modules, named by L-X) are held on their OUTPUT instead: L-X's trace law requires every digit of §0
and of the append to re-derive from a record. Fixture modules are exempt by law (L-0.14: the commission is typed).
Consequence for `analytics/value_area.py`: its functions take every parameter as a required keyword argument with no
default, and it holds structural literals only.
**THE LIMIT, stated before the build:** the structural set collides with these contract pins — the rail's 1.0 (:71,
:98), the fill's 1 tick (:94), the family counts m = 2 and m = 1 (:52, :64, :82), the breadth cut's numerator 2
(:58) and the ferry cap's 2 (:112). The static scan cannot tell a typed copy of those from structure. They are held
by the FLOW leg alone.
**THE FLOW LEG.** For every contract pin and every fitted pin in the register, the consuming record's suite bends the
pin AT ITS DOOR, inside production (the loaded pin object monkeypatched, the comparator untouched), re-runs the
smallest production function that reads it on a seeded sample, and requires the output to move as the register's
`witness` says. A pin whose bend moves nothing is `PIN-NOT-READ`. The sample's rule and its count `n` are stated by
the reading that owns the witness (L-0.14 F). Whatever block hosts a bend — `F-TYPED-FLOW`, or a leg of the owner's
own fixture — it prints one line per pin, `  [FLOW] <pin> @ <door>: <witness> moved`, and F-TYPED-TOTAL reads those
lines. Where the pin's only consumer builds the book of a registration that reads CLOSED_BY_PRECONDITION, the bend
runs on the owner's synthetic tape if its reading provides one and is otherwise CLOSED-NO-BOOK (L-0.14 C);
F-TYPED-TOTAL accepts either.
**TOTALITY of the contract.** Every digit run in the prefix's operative lines is either inside one map row's capture
or listed in `T12/pins/CONTRACT_TOKENS_UNPINNED.json` with its class (an id such as a registration or stage label, a
date, a prior, a hand-sample count, a quoted history figure, a `lens name`, a `ruling or section id`, a `tier id`).
SOURCE: contract :8, :43, :121; `XR/scripts/tc11x_sfp_fixtures.py:970-1035` (`_numeric_literal`, `kin_ast`),
:1440-1500 (`x2_T_literals`, `trav_flow` — the bend-in-production precedent), `XR/scripts/tc11x_ranges_fixtures.py:671-695`
(`typed_pin_literals`) [read here, as text]; the lineage objects at the lines cited [read here] — `WARMUP_BARS` is
assigned at `scripts/tierc5_rules.py:233` and re-exported by `tierc6_rules` and `tierc7_rules`; `scripts/tierc2_rules.py`
holds `ATR_LEN` and no `WARMUP_BARS` [measured here: `grep`]; O-15, O-18, O-19, O-20, O-22 ("parsed from the
contract's stage headers, never typed"); scout U9 §1.8 (constants of `publish_exchange.py` read by
`ast.literal_eval`, never imported).
RIVALS: X's site-targeted scans only (named argument positions) — not taken as the whole law: they catch a typed time
stop but not a typed threshold elsewhere; kept as each owning fixture's extra leg (F-TRAV, F-TOLL). Ban every numeric
literal — not taken: unbuildable (indices). A larger structural set — not taken: each added value hides one more pin.
FAILS-IF: **F-TYPED** (closure suite, AST, `--stage` scope) FAILS IF a scanned source holds a numeric literal that
none of (A), (B), (F), (G) permits, violates (C)-(E), `tierc12_units.py` differs from `UNITS_T`, or a process tool's
exemption is unearned. **F-PINS** (pins suite) FAILS IF the pin door's
re-derivation differs from `CONTRACT_PINS.json`; an `also` citation disagrees; a row's `type` arity differs from its
regex's group count; a map row's slice sha moved; a map row's pin is not a name of record, a name of record has no
register row, or a register row's `kind` is outside the six; a digit run of the operative lines is unaccounted; a
register row, or the text of the filed registry, carries the census sha (whole or abbreviated) of a path in L-0.24's
sets (a)-(f) — checked at filing, because the registry is write-once; or the pin door imports anything outside the
stdlib. **F-TYPED-FLOW** (each consuming record's suite) FAILS IF a bent pin
moves nothing or moves the wrong thing; **F-TYPED-TOTAL** (sweep suite, at TC12-FIX) FAILS IF a contract or fitted pin
of the register is named by no `[FLOW]` line of a PASS block (a CLOSED-NO-BOOK block of its consumer counting), or a
range book has no GREEN `F-TRAV [e · <book>]` instance.
Planted mutations: a `0.25` typed in a copy of a stage module → F-TYPED RED; `float("1.5")` → RED; `K = 2 + 1` → RED;
a default `def f(n=8)` → RED; an extra row in a `tierc12_units.py` copy → RED; `import numpy` added to a copy of a
process tool → UNEARNED RED; a literal typed inside a declared hunk of the vendored shim → RED (rule (G) does not
cover hunks); a map row deleted → F-PINS RED (unaccounted token); a regex changed to capture the neighbouring number
→ F-PINS HALT; a two-group row typed with a one-member `type` → F-PINS RED; a map row renamed `scalp.rr_min` → F-PINS
RED (not a name of record); a registry copy whose spec text cites the file sha of `T11/registrations/REGISTRATIONS.json`
→ F-PINS RED; a pin replaced by a typed literal of EQUAL value inside a shadow copy of its consumer →
the bend moves nothing → `PIN-NOT-READ` RED (this is the leg that holds the colliding pins); a transcript copy with
one pin's `[FLOW]` line removed → F-TYPED-TOTAL RED.

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
FAILS-IF: the contract's **F-FAM** blocks (`[PLANTED]` at TC12-ENV.score-build; `[PARSE]`, `[REAL]` at TC12-SCORE) are
L-X's (L-X.15). The parse at the REGISTRATION stage is this section's block **F-FAM-PINS** (pins suite, TC12-REG — a
different FID, so F-ROLL never counts it as F-FAM): FAILS IF the pin door's parsed (family, m, bar, ids) differs
from the fixture-typed referee table, a header's bar ≠ q ÷ m, or a payload of the filed registry carries a family, m
or bar other than the parse gives its id. Planted mutations: a header copy reading a different bar → the pin door's
HALT; a header copy with a second registration id under SCALPER → RED (ids ≠ m); a registry copy whose SCALPER
payload carries the ADMISSION bar → RED.

---------------------------------------------------------------------------------------------------------------
### D · The cross-cutting fixtures of the FIXTURES line

**L-0.19 THE CONTRACT'S FIXTURE LIST IS A TOTALITY** — "FIXTURES (each states its failure condition): F-CTRL
0.000e+00 cross-process · F-D-2/3 · … · F-KEY · import-closure · worktree attestation." (contract :114-124)
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 2] L-0.17's rule governs the hosting map: one `F-TYPED-FLOW [<pin>]` block per consumed pin is hosted in the consuming record's suite — `TC12-REG.ledger-spec`, `TC12-V`, `TC12-V.trades` (DOOR 2's pins), `TC12-R.dir`, `TC12-R.tables`, `TC12-S`, `TC12-L` beside `TC12-G` and `TC12-R.sfp` — and F-ROLL and F-TYPED-TOTAL expect those blocks.
- [seam 30] a `CLOSED-NO-BOOK` block (row closed by precondition) or a block asserting zero instants (empty frame) satisfies 'one F-NEST-ASOF block per stamp table' in the roll.
- [seam 32] `F-KEY [scores]` is hosted at `TC12-SCORE` (`scores/DRAWS.parquet` has a declared key).
- [seam 60] L-S.31's wording governs the scalper's leg classes: (n) PIN-NOT-READ is judged on the tapes of (i) ALWAYS; a real-tape instance is printed when the row is BUILT (a zero moved-count there is printed, never RED).
READING: Every fixture the contract names on :114-124 exists under its contract name, as at least one fixture block
in a transcript of record, PASS at TC12-FIX, with both `FAILS IF:` lines. The names are parsed from the prefix by the
pin door (tokens of the form `F-<NAME>`, the pair written `F-D-2/3` read as two, and the two unprefixed names
`import-closure` and `worktree attestation`) and compared with a fixture-typed referee list. Owners: F-CTRL (L-C);
F-D-2, F-D-3 (L-D); F-VA-ASOF, F-VA-RAW, F-VA-MIRROR, F-STATE, F-TRAV, F-NEST-ASOF (L-V); F-GATE, F-BRD (L-G); F-DIR,
F-SFP (L-R); F-SCALP (L-S); F-TOLL (L-D data and reader halves, L-S book half); F-LEDGER (L-L); F-FAM (L-X); F-DET,
F-GRID, F-KEY (the law here — L-0.20, L-0.15, L-0.21 — and one instance per directory or grid in each owning
record's suite); import-closure (L-0.22: F-CLOSURE, F-HOOK-ESCAPE, F-WALL; and L-D's F-CLOSURE-ENV); worktree
attestation (L-0.12: F-ATTEST and the records).
**THE NAME → BLOCK MAP** (L-0.14 E; typed in the sweep suite): the contract name `F-<X>` matches the blocks whose FID
is EXACTLY `F-<X>` for F-D-2, F-D-3, F-VA-ASOF, F-VA-RAW, F-VA-MIRROR, F-STATE, F-TRAV, F-GATE, F-BRD, F-DIR, F-SFP,
F-SCALP, F-TOLL, F-NEST-ASOF, F-LEDGER, F-FAM, F-DET, F-GRID, F-KEY; `F-CTRL` matches every FID with the prefix
`F-CTRL`; `import-closure` matches the FIDs {`F-CLOSURE`, `F-HOOK-ESCAPE`, `F-WALL`, `F-CLOSURE-ENV`};
`worktree attestation` matches `F-ATTEST`. (So `F-SFP-ASOF`, `F-SFP-MIRROR`, `F-STATE-X`, `F-NEST-KEYS`,
`F-LEDGER-FMT`, `F-FAM-PINS`, `F-ATTEST-ORDER` are the readings' additions and are rolled after the contract's.) A
contract name is PASS at TC12-FIX iff EVERY block of its FID(s) in every transcript of record is PASS and every
REQUIRED qualifier is present: F-GATE — `P-ADM-1`, `P-BRD-1`; F-TOLL — `data`, `reader`, `book`; F-TRAV — one
`[e · <book>]` block per range book (held by F-TYPED-TOTAL); F-NEST-ASOF — one block per stamp table. A NOT RUN
block of a contract-named FID is RED at TC12-FIX. A fixture whose population is the book of a registration that
reads CLOSED_BY_PRECONDITION is rolled `PASS (row closed by precondition: real legs CLOSED-NO-BOOK)` (L-0.14 C).
Fixtures the readings add beyond the contract's are listed after them in the report's roll, never mixed in.
SOURCE: contract :114-124; `scripts/tierc11_close.py:2019-2022` (TC11's name → pattern table: exact patterns, and
`^F-CLOSURE` for import-closure), :2045 (its block-id pattern admits no space or bracket) [read here];
`XR/tierc11x/LEANS_X.md:2301-2302` ("The contract's twelve come first, then the ones these readings need") [read
here]; OD-17.
RIVALS: let each section rename its fixtures freely — not taken: a reader holding the contract could not find them.
Match by prefix (TC11's form for one name) — not taken as the rule: `F-SFP` would be "found" through `F-SFP-MIRROR`
and `F-LEDGER` through `F-LEDGER-FMT`; the one prefix kept is `F-CTRL`, a family by design.
FAILS-IF: **F-ROLL** (sweep suite, at TC12-FIX) FAILS IF the parsed name list differs from the referee; a contract
name matches no fixture block in any transcript of record; a matched block is not PASS; a required qualifier is
absent; a NOT RUN block of a contract-named FID stands; or a block prints CLOSED-NO-BOOK for a registration whose
`STATUS.json` reads `BUILT`. Planted mutations (transcript-set copies): the F-TRAV blocks removed → RED; a
contract-prefix scratch copy with one fixture name added → RED (parse ≠ referee); every `F-SFP [...]` block removed
while `F-SFP-MIRROR` stays PASS → RED (a sibling FID is not the fixture); the block `F-GATE [SET · P-BRD-1]` and its
sibling P-BRD-1 blocks removed → RED (required qualifier); a `CLOSED-NO-BOOK P-SCALP-3` line beside a STATUS copy
reading `BUILT` → RED. Control that must stay GREEN and is printed: a FAIL block `F-LEDGER-FMT` leaves the name
F-LEDGER untouched (it is RED as its own, added fixture).

**L-0.20 F-DET** — "F-DET hash-identical" (contract :123)
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 68] F-DET [forward] compares the TC12-L writer's outputs only; `BOOK_SPEC_COMBINED.json`, `BOOK4_FREEZE.json` and `FIXTURES_LEDGER_SPEC.txt` are twin INPUTS, outside the file-set equality (L-L.18).
READING: TC10's variant (i), per parquet directory, as TC11 and X ran it. For every directory a record writes parquet
into, the suite runs that directory's one writer script (L-0.9) twice, each in a fresh subprocess that imports `E`
before any I/O, into `<dir>/_det_<stage>/seed_<s>/` (git-ignored), under `PYTHONHASHSEED` = "1" (TC11 L-F.1's first
twin) and `PYTHONHASHSEED` = the tier seed. THE TIER SEED DRIVES EVERY RULER IN BOTH TWINS; only the interpreter's
hash seed differs. GREEN iff: both exit 0; the file set of each twin equals the fixture-typed file set and the
canonical directory's; every file is byte-identical twin to twin and twin to canonical; every parquet's content sha
(`TB._content_sha`: sha256 of `to_csv(index=False)` of the table as written — regbook arms at full float, every other
table at the lineage's rounding — mergesorted by its declared key) is equal; `TP.check_det(twin, canonical)` is
GREEN on the directory's manifest (same table set, no content sha moved, an independent byte re-hash of every parquet
pair, equal `input_sha`); and no clock-like key or column exists in any manifest or parquet — a worker count or a
load average counts as a clock (the name pattern is the fixture-typed copy of X's `CLOCK_NAME_RX`). THE FILE SET:
outside `regbooks/` the lineage's skip-empty law stands, so the fixture-typed file set of a directory is the typed
set minus the manifest's `skipped_empty`, each skipped name asserted empty by the fixture's own count; a regbook
directory holds every arm its spec names, empty or not (a zero-row parquet at the full schema and its sidecar,
L-X.24). The directory's `READ_SET.json` (L-0.13) is in the set: the twin must have opened what the build of record
opened. Seeded draws (the scorer's persisted bootstrap draws) are parquet like any other and are held byte-equal.
Documents of record that a builder renders (stage `.md`) are in the file set. On a directory of `SHARED_DIRS_T` the
leg is SCOPED to the tables the records up to `--stage` name (L-0.9). On the regbook directory of a registration
closed by precondition the instance is CLOSED-NO-BOOK (L-0.14 C).
SOURCE: `T11/LEANS.md:520-521` (L-F.1) [read here]; `XR/tierc11x/LEANS_X.md:2314` [read here];
`XR/scripts/tc11x_books_fixtures.py:203-204` (`CLOCK_NAME_RX`), :1629-1765 (the implementation and its four plants)
[read here, as text]; `scripts/tierc10_panel.py:2661-2689` (`check_det`), :2577-2580 (an empty frame is skipped and
listed) [read here]; `scripts/tierc2_baseline.py:155-188` [read here]; OD-5.
RIVALS: one in-process double build — not taken: it shares the interpreter's hash seed and memo state. Compare
content shas only — not taken: the bytes are the output; the sha is the build's claim about them.
FAILS-IF: **F-DET** (helper legs in `tierc12_fx.py`; one instance per parquet directory in the owning stage's suite)
FAILS IF any clause of GREEN fails. Planted mutations: one byte bent in a copy of a rendered document; one float moved
by one unit of the last rounded decimal in a parquet copy (the content sha must move); the last bit of one float
moved in a regbook-arm copy (its full-float content sha must move); a name listed under `skipped_empty` in a manifest
copy while its frame holds a row; an empty arm's zero-row parquet deleted from a regbook twin; one path dropped from
a twin's `READ_SET.json`; an `elapsed_s` field planted in a manifest copy; a HASH-ORDER plant — a builder twin that
appends a line built from iterating a `set`, run under the two hash seeds, whose bytes must differ — each RED by its
named detector.

**L-0.21 F-KEY** — "F-KEY" (contract :124)
READING: F-KEY has three filed meanings and TC12's is their union. (1) Origin: a join key must be DECLARED and UNIQUE
before the join (`TB.assert_key`, which HALTs inside `write_table` and, for a regbook arm, inside `put_regbook` on
`[symbol, entry_close_ms]` — `[arm, symbol, entry_close_ms]` on `strip`). (2) TC10's TOTALITY over one output root
(`TP.check_keys`): every parquet in the directory has a declared key in that directory's `build_manifest.json`; no
manifest key lacks its table (a ghost); no key duplicates; every table carries every as-of column, none null. (3)
TC11's and X's COMMISSION: per table the fixture types the key, the column list in order, the required (non-null)
columns and the null-iff flags, and holds the manifest's content sha equal to `TB._content_sha` of the table read
back — the table as written: a regbook arm at full float, every other table at the lineage's rounding. FOR TC12, per
parquet directory (the lineage's checker globs `root/*.parquet` without recursion): all of (1)-(3),
plus STAMP TRUTH — `as_of_n_assets` equals the number of assets of the panel the table declares and `as_of_panel`
names it; `as_of_last_closed_4h` is the edge L-0.13 assigns that table (the score edge or the pin); `as_of_substrate`
is the Stage D manifest's snapshot name — plus COLLAR TOTALITY (L-0.16) on the same pass. A regbook directory is a
parquet directory like any other: its manifest declares the key per arm and its empty arms are tables (L-X.24). On a
directory of `SHARED_DIRS_T` the leg is SCOPED (L-0.9); on the regbook directory of a registration closed by
precondition the instance is CLOSED-NO-BOOK (L-0.14 C).
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
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 14] at `--stage=TC12-REG`, before `TC12-ENV.vendor` files `env/LINEAGE_PINS.json`, leg (ii)'s TC10-layer disclosure is stated as EMPTY (nothing on file to read), never guessed.
- [seam 16] the two L-D detectors — the pin as an int or ISO string, and a tick string literal or a float `x - tick` compare — follow every module: the closure suite's AST sweep re-runs them over every non-fixture `tierc12_*` source on file at each `ORDER`-stage gate (the same legs on a wider scope; no new block id).
- [seam 29] the reader's import of `tierc12_progress` (stdlib-only, for `certified()`) is lawful and is not a finding of the AST legs.
- [seam 62] leg (iii) VA-BLIND keys on a directory's ONE parquet writer (the manifest's `source_script`), not on the directory's `READ_SET.json`: `forward/` is written by `tierc12_forward.py`, which lawfully opens the two `.c` stamp tables, while the VA-blind `tierc12_forward_spec` is held blind by AST and `SPEC_READS_T` (L-L.3).
READING: Three registered rows decide ON value-area state (P-DIR-1 :65-66, P-SFP-VA-1 :69-73, P-SCALP-3 :85-98), and
the contract forbids decision modules to import the module that computes it. The two hold together in the strong
form O-29 rules: **value-area facts enter every module that builds a book, a gate, an order or a score ONLY AS FILED
DATA** — columns of the Stage V tables the doors file, each sha-asserted before use — never as a call into the
module, and never through a module that holds it. The class law, by typed lists:
1. **THE GLOB** = every `scripts/tierc12_*.py` whose stem does not end `_fixtures`.
2. **`DOORS_T = ("tierc12_va", "tierc12_va_trades")`**, typed in the closure fixture. They are the only GLOB members
   that import `analytics.value_area` or `analytics.profile`; each is EARNED (its source imports
   `analytics.value_area`); each imports `tierc12_env` first. A door writes Stage V tables and collared Tier-E tables
   only: DOOR 1 under `T12/va/`, DOOR 2 under `T12/va/trades/`. A door never writes under `regbooks/`, files no
   order, gate or score, files no table holding a column of `TRADE_COLS_T = (net_r, gross_r, fee_r, funding_r,
   entry_px, stop_px, exit_reason)`, and is imported by no module other than `tierc12_va_fixtures.py`.
   - **DOOR 1 `scripts/tierc12_va.py`** (record `TC12-V`): series, TPO twin, ATR, the V2 machine's states and events,
     regimes, the per-bar columns, the nest columns, the traverse legs and pin, `VA_PINS.json`, the mirror record,
     `va_stack`.
   - **DOOR 2 `scripts/tierc12_va_trades.py`** (record `TC12-V.trades`): the only place the V2 machine is run on
     permuted volume or on scheduled boxes — (a) the volume null of L-V.23; (b) the gaps+order@va_regime schedule and
     its box events (L-R.29), by `value_area.va_machine` on arrays held constant at each box's edges; (c) the Tier-E
     two-trades tables of L-R.26-L-R.29 (the retest scan, the outcome ledger, the base rate, the lens-above
     partition, the per-draw statistics). It reads Stage V's filed tables through the reader (sha-asserted) and the
     tapes through `E`. **L-R keeps the DEFINITIONS** (L-R.26..L-R.29); L-V carries the builder, the files and the
     record (L-V.2, L-V.23, L-V.24).
3. **The reader `scripts/tierc12_va_stamps.py` is NOT a door.** It is a DECISION module: data-only, it imports
   neither the module nor a door and recomputes nothing (its API is L-V.2's). Every filed Stage V table is asserted
   against the sha its record carries (through `certified()`) before use.
4. **Every other GLOB member is a DECISION module, with no exemption** — the P-SFP-VA-1, P-SCALP-3 and take-profit
   builders included. A module the fixture does not name defaults to DECISION and is scanned. For a decision module
   the contract's sentence holds in its strong form: neither the module nor a door is in its import closure, directly
   or transitively, and neither is in its process at exit. No decision module carries a copy of the V2 machine, a
   profile, or an acceptance / swing-failure / lapse test. A consumer may compare a price with a filed LEVEL; it
   never re-derives a lens STATE or EVENT.
5. **`VA_BLIND_T`** (typed; a member may not import the reader nor open a path under `T12/va/`; proven by AST and
   from its directory's `READ_SET.json`, L-0.13) = `tierc12_books, tierc12_tide, tierc12_stage_g, tierc12_data,
   tierc12_env, tierc12_vendor, tierc12_tables, tierc12_asof, tierc12_pins, tierc12_units, tierc12_tick,
   tierc12_registrations, tierc12_forward_spec, tierc12_era, tierc12_pct`. The card's ride stays value-area-blind, as
   the lineage stayed range-blind; the two admission gates read no value-area column.
6. **`VA_MODULE_FIXTURES_T = ("tierc12_va_fixtures",)`** — the only `_fixtures` module that may import
   `analytics.value_area` or a door. Any `_fixtures` module may import `analytics.profile` (the house function, frozen
   estate) as an independent referee of a hand derivation; no non-fixture module but a door may. CUT-TAPE LEGS: no
   suite outside Stage V imports or spawns a door. Stage V's suite owns PREFIX IDENTITY (L-V's F-VA-ASOF `[d]`: a
   filed row at bar k equals a door rebuild on tapes cut at close_k, at seeded cuts and at the era cut); every as-of
   leg of every other suite cuts the FILED tables by `known_close_ms ≤ cut` through the reader, re-runs its own
   production function on them, and leans on that identity.

- **FORBIDDEN to every decision module:** by exact name `analytics.value_area`, `analytics.profile`,
  `analytics.rangefinder_census` and each `DOORS_T` name; by substring `rangefinder`, `tierc10_census`,
  `tierc10_stamps`, `tierc10_null`, `tierc11_nest`. FORBIDDEN to every member of the glob, doors included: those five
  range-machine substrings and `analytics.rangefinder_census` (a constant of the range machine is read from its
  source text, never by import), and any module whose name starts `tc11x_` (O-4) or `tierc11_` (O-3; TC12's shim is a
  vendored copy, L-D). The package `analytics` itself and its
  `vwap`, `volatility`, `structure`, `momentum` submodules ARE in every process (the lineage imports them:
  `scripts/tierc2_baseline.py:79-82`), so the ban is by exact submodule, never on `analytics`; `analytics/__init__.py`
  imports no submodule and no lineage module imports `analytics.profile` [measured here], so a clean decision process
  holds neither.
- **The closure legs** (six blocks: `F-CLOSURE [i]`, `[i-b]`, `[ii]`, `[iii]`; `F-HOOK-ESCAPE`; `F-WALL`).
  (i) FRESH INTERPRETER, one per decision module: after `import <module>`, `sys.modules` holds no
  `analytics.value_area`, no `analytics.profile`, no `DOORS_T` name, no forbidden name, and the module loaded from
  `scripts/<name>.py`. This leg is what catches a TRANSITIVE reach — a decision module importing something that
  imports a door.
  (i-b) EXIT. The shim registers an exit check (L-D.26 hunk 7, code) in every process that imports it. At exit, with
  `stem` = the stem of `sys.modules["__main__"].__file__` (a spawn worker inherits its parent's; a process with no
  such file has the empty stem), the hook logs `BLOCKED:va-wall <name>` and forces exit 70 if (1) `stem ∉ DOORS_T ∪
  VA_MODULE_FIXTURES_T` and `sys.modules` holds `analytics.value_area` or a `DOORS_T` name; or (2) `stem ∉ DOORS_T`,
  `stem` does not end `_fixtures`, and `sys.modules` holds `analytics.profile` (clause (2) exempts the doors by name:
  a door is the one non-fixture module that may hold the house profile, point 2). Every stage builder and every F-DET
  twin exits through this check, and a spawn worker — whose exit code a pool does not read — is held to the same
  predicate when it hands back its read set (L-D.26), so a door reached lazily at run time, which leg (i) cannot
  see, fails that record's gate. The
  fixture's own side: the shim's typed tuples `VA_WALL_DOORS` and `VA_WALL_FIXTURES`, read as text by `ast`, equal
  `DOORS_T` and `VA_MODULE_FIXTURES_T`; and each of leg (i)'s fresh interpreters exits 0 with no `BLOCKED:va-wall`
  line.
  (ii) AST over each decision source and the static repo closure of its imports:
  no `Import` / `ImportFrom` of a forbidden name anywhere (function bodies included); no constant-string
  `import_module` / `__import__`; no non-constant import site other than a door L-D declares; no `exec` / `eval` /
  `compile`; no `sys.modules` reach; no attribute chain or `getattr` ending in `value_area` or `profile` on a name
  bound to the `analytics` package; no `.top` / `.bottom` read of a range object. THE TC10 CLAUSE: modules named
  `tierc10_*` are TC10's layer — DISCLOSED (name, path, sha from `T12/env/LINEAGE_PINS.json`) and NOT WALKED for
  forbidden imports. The function-local range imports they hold — `scripts/tierc10_brk.py:2357` (in
  `macro_signals`), `:2380` (in `grid_toll_atr`) and `scripts/tierc10_lanes.py:1246` (in
  `spring_signals_from_census`), each `import tierc10_census as C` — are typed `TC10_LAZY_RANGE_T` by (module,
  enclosing function name), and the fixture FAILS IF the AST's set differs from the typed one. Leg (i) proves none of
  them is loaded by an import, and F-NOT's PIVOT-RANGE leg (L-0.30) that no TC12 source calls one of those functions.
  COVERAGE: every repo module a fresh interpreter loaded is in the walk or in the disclosed TC10 layer. (This walk is
  not L-D.29's pinning walk, which does not stop at the TC10 layer.)
  (iii) DATA-ONLY: outside `DOORS_T` no GLOB source holds an `ast.Name` id or `ast.Attribute` attr equal to
  `volume_profile`, `value_area`, `va_series`, `va_machine`, `va_columns`, `va_traverse`, `va_coincidence` or
  `null_volume` (string constants and path literals are not names and are not scanned). VA-BLIND: no `VA_BLIND_T`
  source imports the reader, and no `READ_SET.json` of a directory a `VA_BLIND_T` member writes holds a path under
  `T12/va/`. DOOR OUTPUT: no table a door files holds a `TRADE_COLS_T` column, no door write root resolves under
  `regbooks/`, and the only module importing a door is `tierc12_va_fixtures.py`.
  (iv) HOOK-ESCAPE over every member of the glob: `E.hook_escapes(src)` finds nothing —
  no pyarrow-native I/O, no os-level out-of-process call — and `subprocess` appears only at the typed call sites
  `SUBPROC_SITE_T` (typed, closed, one pinned call site each; `hook_escapes` findings are filtered by exactly these):
  `tierc12_data.clone_snapshot` (`cp -cpR`); `tierc12_worktree_attest.git` (subcommands `worktree`, `rev-parse`,
  `status`, `show`); `tierc12_close.git_ro` (read-only verbs `rev-parse`, `log`, `ls-files`, `ls-tree`, `cat-file`,
  `show`, `merge-base`, each with `--no-optional-locks`); `tierc12_tc11_stamp.run` (`git worktree add --detach` /
  `git worktree remove --force` on the scratch proof tree, and the interpreter running TC11's suites with cwd
  asserted inside that tree). Fixture modules may use `subprocess` (read-only git; twins; scratch repositories). No
  other non-fixture module holds a subprocess site.
  (v) THE ANALYTICS WALL on
  `analytics/value_area.py`: `numpy` is its only non-stdlib import, and of the stdlib it imports only members of the
  fixture-typed no-I/O set `VA_IMPORTS_T` (`__future__`, `dataclasses`, `typing`, `math`, `enum`) — O-15's "numpy
  only" read as "nothing of the repo, nothing third-party but numpy, nothing that performs I/O"; the two scans of
  `tests/test_analytics.py` (no `engine` import :124-127; none of its banned I/O tokens and no `open(` call :147-160)
  find nothing, re-implemented by the fixture as its own object; `analytics/__init__.py` is byte-unchanged and holds no
  `value_area` token; `value_area.py` is not in `_MODULES` (read by `ast.literal_eval` from `analytics/__init__.py:118-120`);
  and `analytics_sha()` recomputed by the fixture's own loop equals the value printed in `analytics/INTERFACE.md:8-9`.
SOURCE: contract :25-26, :124; O-15, O-29; OD-2; `scripts/tierc11_closure_fixtures.py:9-47` (the decision-set law,
earned exemptions, the default; :19-21 "tierc10_* modules are TC10's layer … they are disclosed, not walked", the walk
at :456-460), :118-124, :144-148, :246-248, :293-309 [read here]; `scripts/tierc10_brk.py:2357`, :2380 and
`scripts/tierc10_lanes.py:1246` with their enclosing `def` lines (:2332, :2371; :1231) [read here, as text];
`scripts/tierc11_env.py:1200-1255` (`hook_escapes`; `_ESC_MODULES` at :1202 holds `subprocess`), :725-728 (the shim
imports `tierc10_brk` and `tierc10_lanes` as `BK`, `LN`) [read here]; `XR/scripts/tc11x_books_fixtures.py:194-201`
(`FORBIDDEN_EXACT_TYPED`) and `XR/tierc11x/LEANS_X.md:384-405` (why `analytics` cannot be banned whole; "only
`tc11x_va` imports `analytics.profile`") [read here]; `tests/test_analytics.py:120-160` [read here];
`analytics/__init__.py:118-136` [read here]; `analytics/rangefinder_census.py` precedent (scout U9 §1.5); scout U9
C3, U9-12, U9-13.
RIVALS: (a) "decision module" = only the three modules that trade on VA state — not taken: a typed inclusion list
leaves every new module outside the scan; the glob-minus-typed-doors rule fails closed. (b) An exemption for the
value-area trade builders — a builder that holds a door in its own process and takes arrays from it, on the earned
form TC11 used for its nest module — not taken: O-29. A process that holds the door holds the module and can profile
any window it likes; what reaches a trade must be on file. The round trap that form was meant to cure (tables are
rounded at write, so a level read back can sit on the other side of a close that equals it to the last decimal) is
answered by L-V.24: the filed value is the level of record, and no consumer re-derives a state from filed levels.
(c) X's form — the closure covers the card's path only and a value-area trade builder imports the module itself —
not taken: O-29, for the same reason. (d) Ban `analytics` whole (X's leg (ii)) — not taken: it could never pass on
the lineage. (e) A cut-mode subprocess of the door for the consumers' as-of legs — not taken (OD-2): no suite outside
Stage V spawns a door; they cut the filed tables and lean on Stage V's prefix identity. (f) A second copy of the V2
machine in a Stage R module for the scheduled boxes — not taken (OD-2): one machine, run by DOOR 2. (g) Walk the TC10
layer for forbidden imports — not taken: `tierc10_brk` and `tierc10_lanes` are in every shim-armed closure and hold
function-local range imports, so the leg would be RED on the real tree by construction; TC11's filed law discloses
that layer and does not walk it.
FAILS-IF: **F-CLOSURE** (`scripts/tierc12_closure_fixtures.py --stage=<S>`; blocks `[i]`, `[i-b]`, `[ii]`, `[iii]`),
**F-HOOK-ESCAPE** (leg (iv)), **F-WALL** (leg (v)). At `--stage=TC12-REG` the suite runs `[ii]` and `[iii]` only (no
module then in scope reaches the lineage, asserted); legs (i), (i-b), (iv) and (v) need the shim and first run at
TC12-ENV, and (v)'s clauses on `value_area.py` bind from the record that files it. Each FAILS IF its clause above is
breached; a door's place is unearned; a third module imports `analytics.value_area` without being typed in
`DOORS_T`; a door's table holds a `TRADE_COLS_T` column, a door writes under `regbooks/`, or a door is imported
outside `tierc12_va_fixtures.py`; the AST's set of TC10 lazy range imports differs from `TC10_LAZY_RANGE_T`; or the
static walk misses a repo module a fresh interpreter loaded that the disclosed TC10 layer does not hold.
Planted mutations (on in-memory copies or shadow modules, never on a source of record) —
`[i]`: a P-SFP builder copy importing `tierc12_va` → (i) RED; `import analytics.value_area` at the top of a
book-module copy → (i) and (ii) RED; a NEW unnamed `tierc12_*` shadow module importing a door → RED (it defaulted to
DECISION).
`[i-b]`: a shadow builder with a run-time lazy door import, run as a subprocess → exit 70 at (i-b); a shadow
non-fixture module importing `analytics.profile` → exit 70; a shim-text copy whose `VA_WALL_DOORS` lacks DOOR 2 → RED.
`[ii]`: a scalper copy importing `analytics.value_area` inside a function body → (ii) RED;
`importlib.import_module("analytics.value_area")` → RED; `sys.modules["analytics.value_area"]` → RED;
`AN.value_area.x` on the package alias → RED; `import tierc10_census` in a copy → RED; `import tc11x_va` in a door
copy → RED; a fourth function-local range import planted in a text copy of `tierc10_brk.py` → RED (the typed set
differs); a shadow lineage module outside both the walk and the TC10 layer loaded by a fresh interpreter → RED
(coverage).
`[iii]`: a decision-module copy holding the name `va_machine` → (iii) RED; a `tierc12_books` copy importing the
reader → `VA-BLIND` RED; a third module importing `analytics.value_area` that is not typed in `DOORS_T` → RED; a
door copy without its import → UNEARNED; a DOOR 2 copy writing under `regbooks/` → RED; a door table copy with a
`net_r` column → RED.
F-HOOK-ESCAPE: `pq.read_table(` and `os.system(` in two copies → (iv) RED; `git push` through the attestation helper
→ (iv) RED; a `subprocess.run` in a builder copy, outside `SUBPROC_SITE_T` → (iv) RED.
F-WALL: `import engine` and a `read_parquet` call planted in a `value_area.py` copy → (v) RED; `value_area.py` added
to a copy of `_MODULES` → (v) RED (the sha moves).

---------------------------------------------------------------------------------------------------------------
### E · Rulings enacted, and the vetoes

**L-0.23 "EACH VETO BY NAME, SILENCE RATIFIES" · VETOES BY NAME** — "RULINGS ENACTED AS DEFAULTS (TC11 §11; each VETO
by name, silence ratifies)" (contract :12); "VETOES BY NAME: "va-lookback" · "sfp-k" (3) · … · "tc11-stamp" · "1w"."
(contract :135-137)
READING: A veto is the operator's own message naming a token of :135-137 — or, for the three enacted rulings that
carry no token (Q6, Q8, Q9), naming the ruling by its Q-number. No agent message, no file content and no silence is a
veto; silence leaves every default as enacted. The token is the `veto` field of the register rows (L-0.17) — the
register, because it covers every door and `va-lookback`, `maker-bps`, `tc11-stamp` and `1w` name no contract
number — so the mapping is filed data. Each token names the register rows of **`VETO_ROWS_T`** (typed in F-VETO): `va-lookback` → every
`va.lookback.<lens>`; `sfp-k` → `va.sfp_k`; `nest` → `va.nest_frac`; `breadth` → `brd.cut`; `rr-min` → `rr_min`;
`outer-third` → `scalp.third_long_max`, `scalp.third_short_min`; `validity` → `scalp.validity_bars`; `fill` →
`scalp.fill_ticks`; `maker-bps` → every `fee.maker_bps_side.<VENUE>`; `era` → `scalp.era`; `tc11-stamp` →
`ruling.tc11_stamp`; `1w` → `ruling.1w`. Owning readings: the lookbacks, K and the coincidence band (L-V); the
breadth cut (L-G); the minimum reward at T2 — ONE pin for both range rows (L-R, L-S); the setup thirds, the order's
life and the fill of record (L-S); the maker fee (L-D); the scalper's scoring era (L-S, L-X); `tc11-stamp` → L-0.24;
`1w` → L-0.25. EFFECT BY TIMING: before the TC12-REG freeze, the
reading changes in LEANS; after it, the veto is applied as a dated amendment quoting the operator's words (L-0.5,
basis `operator veto "<token>"`) and the affected records are redone; if any book of the affected row already
exists, the pre-veto result is KEPT and printed beside the new one (L-0.5, resume item 3) and the row's verdict text
carries "pin changed by operator veto <token> after the look — NOT CONFIRMATORY". A value the operator substitutes
is filed in the amendment and read from there by the pin door; it is never typed in code. TWO EFFECTS STATED NOW,
because the tokens carry no value: `era` vetoed without a substitute → the full-corridor book becomes `scored`, the
holdout its Tier-E slice, the row re-filed by amendment; `1w` vetoed → Q4 is NOT ENACTED: no 1w cell is built either
way, the report and the append drop the closure sentence and carry the operator's quote.
SOURCE: contract :12, :135-137; the token/value pairs agree with the stage text at :28, :36, :46, :58, :73-74 and
:100, :87, :92-93, :93-94, :21-23, :83, :13, :14 [read here]; scout U1 C-4 (Q6, Q8, Q9 carry no token).
RIVALS: treat an orchestrator or reviewer objection as a veto — not taken: the contract gives the veto to the operator.
Apply a post-look veto silently — not taken: it cannot be told from tuning. One pin per token, in the contract map —
not taken: `outer-third` names two pins, `va-lookback` and `maker-bps` name one row per lens and per venue from X's
and Stage D's records, and `tc11-stamp` and `1w` name rulings with no value.
FAILS-IF: **F-VETO** (pins suite) FAILS IF the set of register rows carrying a token differs from
`VETO_ROWS_T[token]`; a token of :135-137 has no row; a token's parenthesised value (where the line gives one) does
not parse equal to its stage-text citation; or an amendment that changes a pin names no operator quote. Planted
mutations: a register copy with the `va.sfp_k` row's `veto` cleared → RED; a register copy with `rr-min` on a second
row → RED; a register copy lacking the `ruling.1w` row → RED; a scratch amendment changing `brd.cut` with no quoted
operator words → RED; a contract-prefix scratch copy where the VETOES line's value differs from the stage line → the
pin door's HALT.

**L-0.24 Q1/Q2 · "tc11-stamp"** — "Q1/Q2 keep SCORES.json leaves; stamp TC11 BUILT and re-pin its registry files
["tc11-stamp"]" (contract :13); O-10.
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 33] L-X.34 defines the map: `close/TC11_STAMP_MAP.json` also carries `head_at_proof` and `proof` ∈ {GREEN, RED, PROOF ENVIRONMENT DEFECT}; `--apply` rewrites it with `applied: true`; the BUILT line is composed by the close generator and handed to the stamp tool as an argument.
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
  other records TC11's own scorer regenerates from those pins — regenerated in the scratch proof tree and carried into
  the main tree as proven post-images, behind the assertion that `SCORES.json`, `FAMILY.json` and `BASE_IDENT.json` are
  byte-identical before and after; (e) the transcripts and manifests that print a moved sha, likewise; (f)
  `T11/PROGRESS.json` (`contract_of_record`, the STEP Q artifact sha and line, `registrations_of_record`, and the
  shas of everything moved). Every other quote of the old sha — the data records, `scripts/tierc11_data.py:174`,
  `scripts/tierc11_nest.py:640`, docstrings, stage documents, TC11's published report, X's records — is HISTORICAL:
  untouched and listed.
- **Q2 — the proof.** At TC12-CLOSE the executor runs the whole cascade in a scratch proof tree (a detached linked
  worktree, L-X.34), never in the main tree: a DETACHED LINKED WORKTREE of the main repository at `HEAD` under a
  scratch directory outside both trees (`git worktree add --detach`; removed with `--force` at the end; no ref and no
  main-tree file moves), so that TC11's `_main_tree()` resolves the real main tree and the TC10 allow-list is read
  there read-only, as in TC11's certified lens runs; TC11's ignored parquet and `TC10_STAGED` are staged by the attest
  tool's globs. A `[PRE]` leg first runs TC11's sweep on the UNSTAMPED proof tree and must be GREEN; a RED PRE leg is
  reported `PROOF ENVIRONMENT DEFECT` and is not a tc11-stamp result. The executor then files
  `T12/close/TC11_STAMP_PROOF.txt` and `T12/close/TC11_STAMP_MAP.json` (old → new sha for every moved file; the
  historical list). GREEN = the invariances above, plus every suite of TC11's last sweep (the list read from
  `T11/PROGRESS.json` `stages[*].fixtures[*].suite`) exiting 0 in the proof tree. `scripts/tierc11_close.py` and its
  fixtures are outside the cascade and their HALT is printed as EXPECTED: that generator refuses a contract that
  already carries a `BUILT` line (`scripts/tierc11_close.py:960-961`). The mechanics — the prove and apply phases of
  the stamp script, its ALLOWED and NEVER-moved sets, and the rule that no TC11 code runs in the main tree (the act
  copies proven post-images) — are L-X's reading of the same phrase; this reading fixes what any mechanics must meet.
- **Q2 — if the proof is not GREEN,** `close_acts.sh` carries NO stamp step, the map is filed with `applied: false`,
  the report's findings read "tc11-stamp NOT APPLIED: <first RED>", and the ruling returns to the operator. No partial
  re-pin is ever written.
- **No TC12 pin is a whole-file sha of a path in sets (a)-(f).** TC12's own close act moves those files, and a TC12
  pin on one of their file shas would re-create, one tier down, the defect this ruling exists to cure. (1) A literal
  read by AST from one of the set-(c) scripts (`scripts/tierc11_registrations.py`, `tierc11_score.py`,
  `tierc11_score_fixtures.py`, `tierc11_stage_g.py`, `tierc11_stage_t_brk.py`) is pinned by
  `sha256(ast.dump(node))`, recorded per literal in `pins/PIN_REGISTER.json` (kind `lineage`) at TC12-REG — never by
  the file's sha. (2) `T11/registrations/REGISTRATIONS.json` is pinned by its chain head VALUE
  (`T11/registrations/REGISTRY_PIN.json["head"]`, asserted equal to the head recomputed from the payloads) plus the
  payload sha of each registration read; no reading and no registration spec cites that file's own sha. (3)
  `E.tc11_record` accepts `T11/PROGRESS.json` at its R0 sha OR at the value `T12/close/TC11_STAMP_MAP.json` names for
  it when that map reads `applied: true`; F-FROZEN accepts a census path of sets (a)-(f) at its census sha or at its
  mapped value under the same condition (L-0.6). (4) The merged ledger names the contract by its prefix (L-0.9), so
  TC12's own BUILT stamp moves no byte of `T12/PROGRESS.json`.
SOURCE: contract :13; O-10, O-12; `T11/BUILD_DRAFT.md:5943`, :5945, :5989 (Q2's own words name three files) [read
here]; the pins at the script lines cited [measured here: `grep` of the two shas]; `T11/registrations/REGISTRY_PIN.json:3`,
`T11/scores/REGISTRY_CHECK.json:4`, :158 [read here]; `scripts/tierc11_registrations.py:244-246` [read here];
`scripts/tierc11_score.py:2648-2652` [read here]; `exchange/queue/README.md:8-12` and the exemplar stamps (scout U1
§1.6); scout U1 R-1..R-5. O-10 says "scratch clone": it is read here as a scratch tree outside both trees, because
a clone cannot run TC11's suites — in a clone `.git` is a directory, so `_main_tree()` returns the clone itself
(`scripts/tierc11_env.py:218-230`), and the TC10 records TC11's suites read through `tc10_record` (`MAIN_TREE / rel`,
:1170-1176) are untracked in main and absent from any clone [read here; `git ls-files` returns none of the
`TC10_ALLOW` paths, measured here]; TC11's own certified runs were in linked worktrees. That reading of O-10 is
listed for the orchestrator. The whole-file-sha law: the lesson `T11/BUILD_DRAFT.md:5945` (FN-M-QUEUE-STAMP).
RIVALS: (a) the literal three files of Q2's sentence — not taken: `REGISTRY_PIN.json` and five typed constants would
stay at the old sha, TC11's scorer and score fixtures would go RED on their next run, and "re-pin" would be false of
TC11's own check. (b) the stamp under the RATIFIED block, where the exemplars sit — not taken: it shifts every line
cite (O-10). (c) no TC11 byte moves, a sibling record only — that is the veto's outcome and the not-GREEN outcome,
not the default. (d) stamp during the build — not taken: O-10.
FAILS-IF: **F-TC11-STAMP** (legs defined here; hosted by the close suite, L-X) FAILS IF (0) PRE: the unstamped sweep
is not GREEN in the proof tree (reported `PROOF ENVIRONMENT DEFECT`, never as a tc11-stamp result); and, after the
cascade in the proof tree: (i) any line up to the contract's pre-stamp last line differs; (ii) a payload sha or the
chain head differs; (iii) `SCORES.json`, `FAMILY.json` or `BASE_IDENT.json` differ by a byte; (iv) a moved file is
absent from the map or a mapped file did not move; (v) a file outside (a)-(f) moved; (vi) a swept TC11 suite exits
non-zero; (vii) a row of `PIN_REGISTER.json`, or a filed registration spec, pins a path of sets (a)-(f) by its
whole-file sha; (viii) the proof tree is not a detached linked worktree outside both trees, or is still registered
after the run. Planted mutations: a proof tree with one staged TC10 record withheld → (0) RED, printed as the
environment defect; the stamp INSERTED at line 3 → (i) and (ii) RED; one byte of `SCORES.json` flipped in the proof
tree → (iii) RED; a moved file dropped from a map copy → (iv) RED; an extra TC11 file touched → (v) RED; one typed
constant left at the old sha → (vi) RED (the scorer's HALT); a register copy pinning `scripts/tierc11_score.py` by
file sha → (vii) RED; the proof run pointed at a plain clone → (viii) RED.
UNVERIFIED: that TC11's swept suites all re-pass after the re-pin. Nothing but the proof-tree run at TC12-CLOSE
establishes it.

**L-0.25 Q4 · "1w"** — "Q4 accept 1w FAIL (provisional) as closing 1w for range trading ["1w"]" (contract :14); O-11
as amended by O-28.
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 67] leg 1W (c) judges by AST and by the declared VA read list — never by `READ_SET` paths or by a table's presence in a staged CSV (the ferry opens every tabular file whole and names no `1w_` column).
READING: 1w is closed for range trading in TC12 and no re-measure is ordered. (i) No trade, order, setup or
event-outcome row of any range form — the swing failure, the breakout-retest, the 1d-edge take-profit venue, the
scalper — has lens 1w, registered or Tier-E: no 1w range cell, trade, traverse row or feasibility row exists. (ii) No
feasibility row and no licence word exists for 1w (the mirror's five words name none: contract :39-41). (iii) The 1w
block (built on the 1d pin's bar count, labelled BORROWED, O-28) is read in exactly two places, both Tier-E: the V5
stamp columns, and the lens-above conditioning axis of the 1d two-trades tables (L-R.27). It is read by no gate, no
permission, no direction guard, no licence, no time stop, no order and no registered construction. The two readers
are typed by (module, table): `ONEW_READERS_T` = ((`scripts/tierc12_va_stamps.py`, `va/stamps/VA_STAMPS_*.parquet`),
(`scripts/tierc12_va_trades.py`, `va/trades/TWO_TRADES_*.parquet`)); and DOOR 2's read is exactly the five columns
`1w_state`, `1w_val`, `1w_vah`, `1w_pct`, `1w_bar_close_ms` of the reader's stamp at the 1d event's known-at close —
the last COMPLETE week closed at or before it, never a week still forming (L-R.27).
SOURCE: contract :14, :39-41, :45, :76-79 ("conditioned on the lens above" has no other object at 1d); O-11, O-28;
OD-3; `T11/stage_r/R2_LENS_VERDICTS.json` key `lenses.1w` (the provisional FAIL) and finding FN-TRD-17 (scout U1
§1.2, §1.11).
RIVALS: print a 1w cell of its OWN in the Tier-E two-trades tables "for completeness" — not taken: a closed lens gets
no cell; 1w appears there only as the lens ABOVE the 1d rows. Leave the 1d rows unconditioned (every 1d event in one
cell) — not taken: O-28; the contract's conditioning clause would have no object at 1d.
FAILS-IF: **F-NOT, leg 1W** (L-0.30's suite) FAILS IF (a) a table holding a `TRADE_COLS_T` column, an order column
or an event-outcome column (one computed from bars after the event's known-at close) has a row whose OWN lens is 1w;
(b) a registered row's declared VA columns hold a `1w_` column; (c) any GLOB module outside `ONEW_READERS_T` reads a
`1w_` column (AST: a string constant matching `^1w_`, or the lens literal `"1w"` handed to `bars`, `events`,
`regimes`, `licence` or `traverse`; plus each stage's declared VA read list); (d) DOOR 2 reads a `1w_` column outside
the five named, or writes a 1w-derived value into a table other than the `TWO_TRADES_*` set. Planted mutations: a
condition on `1w_state` added to a copy of the P-DIR-1 gate → RED; a 1w column read by a copy of the P-SFP-VA-1
builder → RED; a sixth 1w column read by a copy of DOOR 2 → RED; a 1w row added to a range-table copy → RED.

**L-0.26 Q6 · THE CLOSE ACTS** — "Q6 the close acts remain the operator's keystrokes" (contract :14-15); O-12.
READING: The executor WRITES `T12/close/close_acts.sh` and never runs it: its only executions are `bash -n` and runs
of a SCRATCH COPY with every path and cwd asserted outside both trees: step 0 (`--check`) against scratch
repositories, and steps 1-7 against a sandbox clone with a local bare origin, cut before `publish()`. The generated
file in the main tree is never executed by the executor. The scratch copy is produced by the same generator with two
typed substitution points — the step-2 ferry planner call and the step-4 stamp call are replaced by stubs that write
their expected outputs (a copy list naming one planted CSV; a planted `BUILT:` line with no re-pin) — and proves
ORDER and the STOP guards only; the real planner is proven by F-ROWS `[ACT]` and the real stamp by F-TC11-STAMP.
THE ACTS' TEXT lives in `scripts/tierc12_close_acts_template.py`: string constants holding the text of
`close_acts.sh` and nothing else — no call, no subprocess, no import beyond `__future__`; imported only by
`tierc12_close.py`. The executor never runs
`git push`, `git merge` or `publish()`, never moves a report under `exchange/`, never appends to
`exchange/status/LEDGER_APOLLO.md`, never runs or patches a predecessor's `close_acts.sh` (the `-f` patch TC10's
script needs is the operator's). TC12's step 0 requires the TC10, TC11 and X blocks by bytes in that order. "STATE
push" (contract :130) is the result the script prints and a stamp bracket in the report filled at the act. What this
ruling cannot reach is stated in L-0.9: the daily routine's push.
SOURCE: contract :14-15, :130; O-12 ("writes … and never runs it"; it is silent on a scratch copy); OD-18;
`T11/LEANS.md:537-542` (L-F.4) and `XR/tierc11x/LEANS_X.md:2480-2502` (LX-C.5) [read here]; scout U1 §1.7 (the three
scripts, none run), H-2.
RIVALS: running any step "to test it" in the main tree — not taken: it is the act itself. A static law only, with no
sandbox run of steps 1-7 — not taken (OD-18): the order of the acts and their STOP guards are then asserted by
nobody. The sandbox run with the real ferry planner and the real stamp — not taken: neither can run in a clone
(their inputs are git-ignored), and each has a fixture of its own. The acts' text as a constant inside the close
generator — not taken: a module that holds push and publish strings beside code that calls subprocess cannot be
told, by AST, from one that runs them.
FAILS-IF: **F-NOT, leg ACTS** FAILS IF any TC12 source, fixtures included, holds an argv or shell string whose git
subcommand is `push` or `merge`, an `import publish_exchange` (its constants are read as text), or a call named
`publish` — EXEMPT, by a typed list of one, the string constants of `scripts/tierc12_close_acts_template.py` (and the
generated `close/close_acts.sh`); or that module holds anything but string constants (a call, a subprocess, an import
beyond `__future__`) or is imported by a module other than `tierc12_close.py`; or a subprocess's argv names a
`close_acts.sh` in any form but two — under `bash -n`, or a scratch copy run with its cwd asserted outside both
trees. Planted
mutations: `git(["push", "origin", …])` in a copy of the attestation tool → RED; a `git push` string in any other
TC12 source → RED; a call added to a copy of the template module → UNEARNED RED; `import publish_exchange as p` in a
copy of the close generator → RED; `subprocess.run(["bash", <the main tree's close_acts.sh>])` in a fixture copy →
RED.

**L-0.27 Q8 · NO POST-HOC CANDIDATE** — "Q8 post-hoc candidates lie, EXCEPT the combined refusal, pre-named here from
TC11's crossed table and labelled pre_seen" (contract :15-16); O-13.
READING: (i) The two candidates TC11's reviews named (`T11/BUILD_DRAFT.md:5995`) are not registered, not re-run and
not printed with a verdict word in TC12. (ii) TC12's registry holds exactly the five ids the contract names (:53,
:57, :65, :69, :83); nothing found in a TC12 Tier-E table is registered, promoted or given a verdict word in this
tier, and the close append carries the standing line that a later registration drawn from a TC12 Tier-E table is
`pre_seen` on TC12's bars (the form X filed). (iii) P-ADM-1 is the one exception: pre-named from the cell
`age:on¦win:on¦ratr:off` of `T11/stage_g/STAGE_G.md:197` — the contract's "cell 110 @ +0.515" (:55) names that row
by its kept count and its mean — and labelled `pre_seen`; it alone prints the IN-SAMPLE RE-SCORE label, because its
kept book's mean is on file (O-30; the three cell templates, keyed by registration id, are L-X.13's).
SOURCE: contract :15-16, :55; O-13, O-23, O-30; `T11/BUILD_DRAFT.md:5995` [read here]; `T11/stage_g/STAGE_G.md:197` [read
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
`scripts/tierc10_census.py:894-900` [read here]; `scripts/tierc10_census_fixtures.py:1286-1295` (the filed leg and
its sample) [read here, as text]; `T12/scout/U6_range_scalper_machinery.md:282-289` (the two as-of
laws differ by one bar at a boundary) [read here]; scout U1 §1.3 (both readings were built side by side).
RIVALS: strict `<` — not taken: Q9 ratifies `≤`. Import `tierc10_census.asof_index` — not taken: it is the range
machine's module. Print an interval on every Tier-E table — not taken: Q9 ratifies L-W.4's scope.
FAILS-IF: **F-ASOF** (tables suite; blocks `[a]`, `[b]`, `[c]`) FAILS IF (a) on the seeded instants of each (home
asset, lens of `E.TP.LENS_MS`) tape, `asof_index` differs from a from-scratch linear scan for the last close ≤ τ; (b)
at a τ equal to a
higher-lens close, the lower-lens bar closing at τ is not the one returned; (c) production against production: a
join's output on full tapes differs from its output on tapes cut at τ (`E.load_asof_at(stem, lens, τ)`, fresh
arrays), on the instants of (a). THE SAMPLE of (a), a fixture-typed literal (L-0.14 F): the count the lineage filed
for the leg this one mirrors — per tape, 400 instants drawn by the leg's stream between one step before the first
open and three steps after the last, plus the first 50 bar closes and the 50 instants one millisecond before them
(`scripts/tierc10_census_fixtures.py:1293-1294`). Planted mutations, inside the production function:
`side="left"` → (b) RED; `closes_ms = open_ms` (the bar still forming is read — L-W.1's own sabotage) → (a) and (c)
RED.

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
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 53] leg LICENCE derives the licensed pair from the LANE and the toll — lane `scalp_va_1h` → lens 1h; maker entry and targets → `maker` — never from a sidecar's `lens`, which on P-SCALP-3 is the 5m clock.
READING: Each clause is a refusal with a detector, and each is one leg — one block `F-NOT [<LEG>]` — of
`scripts/tierc12_not_fixtures.py --stage=<S>`: ENTRY-CROSS, TRAIL-OFFSET, ADDS, PIVOT-RANGE, 5M, NEW-ASSETS, SAIL,
PROMOTION, RE-FAMILY, 1W, ACTS, POST-HOC, LICENCE. The suite runs from TC12-ENV on. A leg's AST clauses bind from
that first run. A DATA clause is IN FORCE at `--stage=<S>` once a record up to `S` names a table it reads (L-0.11's
scope law); until then it prints "NO TABLE IN SCOPE" inside its block and adds nothing to the block's word. At
TC12-FIX every data clause must be in force — else its block is RED — with one exception: a data clause whose only
tables belong to a registration that reads CLOSED_BY_PRECONDITION is CLOSED-NO-BOOK by L-0.14 C (it asserts the
STATUS record instead), never "NO TABLE IN SCOPE".
- **ENTRY-CROSS.** The only roles objects a TC12 ride uses are the two filed ones: v6's (`T9.V6_ROLES`) and the 9/12
  book's (the second forward book; roles as filed in `T11/books/build_manifest.json` key `roles`). The scalper's 5m
  EMA pair (:89) is timing, one pair, read from the pin door. FAILS IF a non-fixture source constructs or
  `dataclasses.replace`s a roles object with an EMA period, or iterates candidate periods; or a book table's distinct
  `roles_name` values, or the `roles_name` a stage manifest files for one of its mirrored rides, are not within the
  two filed names. Mutations: a `replace(T9.V6_ROLES, …)` with a period keyword in a copy → RED; a book-table copy
  with a third `roles_name` → RED.
- **TRAIL-OFFSET.** Every v6-derived ride in TC12 (control, strip, gated books and their re-ride disclosures, the
  take-profit venue, ledger books, Tier-E v6 twins) uses a card whose `TP.ride_spec(card, roles)` fields equal the
  FILED card fields (`XR/tierc11x/forward/BOOK_SPECS.json` `books.v6.ride_spec`, the same dict TC10 filed) on every
  key of the fixture-typed `TRAIL_FIELDS_T` (`anchor_offset`, `trail`, `trail_extra_buf_atr`, `trail_l`, `trail_r`,
  `trail_min_advance_atr`, `trail_arm_after_r`). The spec of each mirrored ride is read from the `ride_spec` its
  stage manifest files (the control card and roles, by object — L-C, L-G.18, L-R.5, L-R.30, L-L). The range trades
  have no trail (:73, :100): a range or scalp trade's stop never moves after entry. FAILS IF a filed `ride_spec`
  differs on such a key, or a mirrored ride files none; a non-fixture source passes one of those names as a keyword
  or assigns it; a range or scalp trade row shows a stop move (the columns L-R and L-S name). Mutations:
  `replace(TP.CONTROL_CARD, anchor_offset=…)` in a copy → RED; a manifest copy whose `ride_spec.trail_r` differs →
  RED; a range-trade copy with a moved stop → RED.
- **ADDS.** The same rides equal the filed card on every key of the fixture-typed `ADD_FIELDS_T` (`adds_max`,
  `add_size`), and a range or scalp position never grows. FAILS IF a filed `ride_spec` differs on such a key; a
  non-fixture source passes one of those names as a keyword or assigns it; a v6-derived journal has `n_adds` above
  zero on any row; a range or scalp trade row shows a second entry fill (the columns L-R and L-S name). Mutations:
  `replace(TP.CONTROL_CARD, adds_max=…)` in a copy → RED; a journal copy with one `n_adds` raised → RED; a
  scalp-trade copy with a second entry fill → RED.
- **PIVOT-RANGE.** No TC12 module — no door either — imports the range machine (L-0.22's substring list, plus
  `engine.rangefinder`), and every range trade's edge is a VA edge of the filed Stage V tables. The edge is compared
  with the level the owning reading names: P-SCALP-3 — the in-force `val` / `vah` of `va_bars_1h` row `k1`;
  P-SFP-VA-1 and its 1d cell — `E` of the trade's `va_events` row, itself asserted equal to the in-force `vah` /
  `val` of `va_bars_<lens>` row `t0 − 1`. FAILS IF such an import exists anywhere in the glob; a TC12 source
  references an attribute of `E.BK` or `E.LN` whose function body holds one of `TC10_LAZY_RANGE_T` (L-0.22); or a
  range trade row's edge price is not that level. Mutations: `import tierc10_census` in a door copy → RED; a call of
  `E.BK.macro_signals` planted in a builder copy → RED; a P-SFP-VA-1 trade-row copy whose edge is the entry bar's own
  `vah` where that differs from `E` → RED; a scalp trade-row copy whose edge is shifted off the level → RED.
- **5m SIGNAL SOURCE.** 5m data may serve only the scalper's TRIGGER timing (:89-91), fills, the walk of stops,
  targets and the time stop, the as-of clock and the miss accounting. No 5m-native structure or indicator originates
  a signal: there is no 5m value area, range, pivot or tide; the only 5m indicator is the trigger's EMA pair; 5m
  prices may be compared with 1h and 4h level columns and with order prices. FAILS IF (a) a 5m kline path appears in
  a directory's `READ_SET.json` (L-0.13) outside the typed list `FIVE_MIN_READERS_T` — the directories of TC12-D and
  TC12-S, and of any record whose owning reading declares at freeze a 5m WALK or FILL read and names it (at this
  pass: `stage_r/sfp/`, for the conditioned maker twin's fill child and the remaining 5m children of that 4h bar — the fill-bar walk, L-R.24); (b) a
  Stage V table holds a 5m lens; (c)
  the scalper source's `ema`-family call sites are not exactly the fixture-typed two, or any has a literal period;
  (d) the scalper's PERMISSION column (:85-86), recomputed by the fixture from the filed 1h and 4h VA tables in a
  process that opens no 5m file, differs on any row. Mutations: a 5m tape load planted in a shadow copy of the Stage
  G builder run in a subprocess → (a) RED (its `READ_SET.json` gains a 5m path); a Stage V table copy with a `5m`
  lens row → (b) RED; a third `ema` site in a scalper copy → (c) RED; a permission clause reading a 5m EMA state in a
  shadow scalper → (d) RED.
- **NEW ASSETS BY LIST.** The universe is read, never typed: the five home assets by object (`E.CLASSIC5`), the
  twelve by Stage D's manifest as resolved from TC10's Stage D table (:20). FAILS IF a non-fixture source holds a
  string constant that equals a symbol, stem or asset name of the manifest's admission rows or matches the venue
  symbol pattern; the snapshot's or the manifest's stem set differs from TC11's certified set; an asset outside it
  appears in any table. Mutations: a typed symbol string in a copy → RED; a table copy with an eighteenth asset → RED.
- **SAIL.** FAILS IF `exchange/queue/008_sail-skeleton.md` moved from its census sha, a `tierc12(` commit touches it,
  or a TC12 source holds a path naming the SAIL repository or that work order as a write target. Mutations: one byte
  appended to a scratch copy → RED; a planted `Path.home() / "naiad-sail"` write in a copy → RED.
- **PROMOTION.** L-0.16 and L-0.27: `promotable` False on every collared table; exactly five registry ids; no verdict
  word outside the five rows. FAILS IF `promotable` is True on any row of a collared table, a collared table or leaf
  holds a verdict word or a name matching `verdict|clears|spent_test`, or a TC12 document prints a verdict word
  (L-X's pattern) for anything but one of the five registered rows or a predecessor's filed cell quoted by JSON path
  (RE-FAMILY below). Mutations: `promotable = True` on one row of a Tier-E table copy →
  RED; a Tier-E leaf copy carrying `SUPPORTED` → RED; a stage-document copy with a verdict word beside a Tier-E grid
  cell → RED.
- **RE-FAMILY OF TC11.** FAILS IF TC11's `FAMILY.json`, `REGISTRATIONS.json` or `SCORES.json` moved (F-FROZEN; the
  close-act re-pin of L-0.24 moves only whole-file contract-sha pins and proves m, the bar, the payloads and the head
  unmoved); a TC11 registration id appears in TC12's registry; or a TC12 table prints, for a TC11 id, anything but
  TC11's filed verdict cell quoted from `SCORES.json` by JSON path with TC11's own bar. Where the contract asks for a
  TC11 row as a shadow ("OLD alone · stale alone", :56), a recomputation on TC12's bar is a collared Tier-E leaf with
  no verdict word (the scorer's `arm__shadow_…` leaf, L-X.14; `T12/DISCLOSURES.md` D-4 names the hazard). Mutations:
  a shadow-leaf copy carrying a verdict word for a TC11 id at a TC12 bar → RED; a registry copy holding a TC11 id →
  RED.
- **LICENCE** — "the Q-R3 law licenses exactly {VA-4h taker, VA-1d taker, VA-1h maker}; nothing else may trade a
  range" (:40-41); the licence set is L-V.17's. FAILS IF a regbook arm or stage table holding a `TRADE_COLS_T` column
  with a value-area lane (`sfp-va-*`, `scalp_va_*`) has a sidecar `(lens, toll)` whose trade of record is outside
  `VA_MIRROR.json licence_set`, unless the arm is on the fixture-typed list `ORDERED_TWINS_T` = {P-SFP-VA-1
  `tierE__maker_conditioned` and `tierE__maker_assumed` (:75); P-SCALP-3's all-taker twin COLUMN (:102);
  `tierE__panel17` rows of the twelve (:84)}; or a range builder's directory `READ_SET.json` holds no
  `licence_reads` entry for its own pair. Mutations: a `lens = 12h` arm copy → RED; a 1h taker arm shipped as
  `scored` → RED; a range directory's `READ_SET.json` copy with its `licence_reads` emptied → RED.
- **1W, ACTS, POST-HOC** — the legs of L-0.25, L-0.26, L-0.27 live in the same suite, one block each.
SOURCE: contract :132-134, :40-41, :56, :73, :75, :84, :85-91, :100, :102; the 29 filed card fields
`XR/tierc11x/forward/BOOK_SPECS.json` `books.v6.ride_spec` and
`research_outputs/tierc10/registrations/P-TRG-2.json` `book_spec.arms[0].ride.card_fields`
(`T12/scout/U3_env_books_control.md:14`); `scripts/tierc9.py:119` (`V6_ROLES`) [read here],
`T11/books/build_manifest.json` `roles` (scout U3 :12-15); the journal schema's `n_adds` column (scout U3 :96);
`scripts/tierc11_env.py:1161-1163` (`opened_paths`: one process's dict, hence the filed `READ_SET.json`) [read here];
`scripts/tierc10_brk.py:2332`, :2371 and `scripts/tierc10_lanes.py:1231` (the three functions of
`TC10_LAZY_RANGE_T`) [read here, as text]; `exchange/queue/008_sail-skeleton.md` (scout U1 §1.10); O-11, O-13, O-28,
O-29; OD-17, OD-18.
RIVALS: a prose "what this is not" section in the report only (both predecessors) — not taken: the contract lists
refusals; a list nobody checks refuses nothing. Comparing every range trade's edge with the entry bar's own VA row —
not taken: a swing failure's edge is the frozen edge of the profile in force before the probe opened, which the
entry bar's re-rolled profile generally is not. A fourth leg state "no table in scope" — not taken: a block is PASS,
FAIL or NOT RUN (L-0.14 C); an out-of-scope data clause is a printed line inside a block.
FAILS-IF: **F-NOT** — the thirteen legs above, one block each, each with its failure condition and its planted
mutations.

---------------------------------------------------------------------------------------------------------------
### The suites this section defines

One row per invocation; `T12/` is implied in transcript paths; every suite accepts `--root=DIR` (L-0.14 H).

| invocation | record | transcript | hosts |
|---|---|---|---|
| `tierc12_resume_fixtures.py --stage=<id> --at=<sha>` | every record from TC12-REG | `resume/FIXTURES_RESUME_<id>.txt` | F-CONTRACT, F-RESUME, F-FROZEN-TEXT, F-FROZEN, F-ONE-CORRIDOR, F-OFFBUS, F-COMMIT, F-PROGRESS, F-ORDER |
| `tierc12_pins_fixtures.py` | TC12-REG | `pins/FIXTURES_PINS.txt` | F-PINS, F-VETO, F-FAM-PINS |
| `tierc12_closure_fixtures.py --stage=<S>` | ORDER stages from TC12-REG | `closure/FIXTURES_CLOSURE_<S>.txt` | at TC12-REG: F-TYPED, F-SEED, F-FX-MIRROR, F-FX-FORM, F-CLOSURE [ii], [iii]; from TC12-ENV: also F-CLOSURE [i], [i-b], F-HOOK-ESCAPE, F-WALL |
| `tierc12_tables_fixtures.py` | TC12-ENV | `env/FIXTURES_TABLES.txt` | F-WARRANTY, F-ASOF, the helper mirrors of F-COLLAR, F-GRID, F-KEY, F-DET |
| `tierc12_attest_fixtures.py` | TC12-ENV | `closure/FIXTURES_ATTEST.txt` | F-ATTEST |
| `tierc12_not_fixtures.py --stage=<S>` | ORDER stages from TC12-ENV | `closure/FIXTURES_NOT_<S>.txt` | F-NOT (ENTRY-CROSS, TRAIL-OFFSET, ADDS, PIVOT-RANGE, 5M, NEW-ASSETS, SAIL, PROMOTION, RE-FAMILY, 1W, ACTS, POST-HOC, LICENCE) |
| `tierc12_sweep_fixtures.py --stage=<S>` | ORDER stages from TC12-ENV | `sweep/FIXTURES_SWEEP_<S>.txt` | F-SWEEP; at TC12-FIX also F-ROLL, F-TYPED-TOTAL |
| each record's own suite (owned by its section) | that record | that record's transcript | helper legs, one instance each — per parquet directory: F-KEY, F-DET, F-COLLAR; per grid: F-GRID; per pin consumed: a flow leg (F-TYPED-FLOW or the owner's own block, L-0.17) |

The helper legs live in `tierc12_fx.py` (L-0.14); "the helper mirrors" in the tables suite are those legs run on
synthetic tables with their own plants, so that each helper is itself proven before a stage relies on it.
F-TYPED-TOTAL, F-ROLL and the full F-SWEEP are of record at TC12-FIX. F-TC11-STAMP is hosted by the close suite
(L-X). The other sections' invocations, records and transcripts are stated in their own readings; the sweep reads
every one of them from the records, never from a typed list (L-0.11).

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
   verifier is only satisfied if a fourth registry file and the typed constants of five TC11 scripts (L-0.24, set
   (c)) move too. Default if silent: the larger set of L-0.24, applied only as an operator close act and only if the
   proof in the scratch proof tree is GREEN (its PRE leg included); otherwise not applied and said so. The veto
   "tc11-stamp" withholds the whole step.
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
  the lineage under the referee's own aliases (`E.TP` `tierc10_panel` at a pinned sha, `E.TB`, `E.D`, `E.BK`, `E.LN`,
  `E.T9` … `E.R2`), `E.OUT` = `T12`, `E.PIN_MS` read from `T12/data/AS_OF_PIN.json`, `E.TC11_PIN_MS`,
  `E.ERA_CUT_MS`, `E.SEED`, `E.CLASSIC5`, `E.X_REC` (rooted on the MAIN tree), `E.load_asof_at(stem, iv, cut_ms)`
  (any instant ≤ the pin), `E.hook_escapes`, `E.opened_paths()`, `E.import_audit()`, `E.read_set()` and
  `E.tc11_record` (which accepts TC11's PROGRESS at its R0 sha or at its stamped value, L-0.24); arms a hook that
  refuses writes into the O-3 estate, `XR/`, both earlier snapshots and `exchange/`; registers the VA-wall exit check
  of L-0.22 (i-b) with the typed tuples `VA_WALL_DOORS`, `VA_WALL_FIXTURES`, the line `BLOCKED:va-wall` and exit 70
  — with clause (2) exempting the doors, as L-0.22 words it; re-roots `TP.AS_OF_PIN`, `TP.STAGE_D_MANIFEST` and the
  import-time `_U12` panel resolution to TC12's records. Stage D's manifest carries the snapshot's name and absolute
  path; `T12/data/AS_OF_PIN.json` carries `as_of_last_closed_4h_close_ms`. The one subprocess site L-D declares for
  `SUBPROC_SITE_T` is `tierc12_data.clone_snapshot`; L-D declares any dynamic-import door of the env and files
  `T12/env/LINEAGE_PINS.json` (the disclosed TC10 layer's names, paths and shas). L-D pins
  `scripts/tierc10_panel.py`'s sha and proves the pin (O-7). L-D's children are `TC12-ENV.vendor` and `TC12-D.mirror`
  (O-31); F-MIRROR's transcript `data/FIXTURES_MIRROR.txt` is the one PROVENANCE transcript, and no leg of
  `data/FIXTURES_DATA.txt` needs the network or the drive. L-D's vendored shim and ported functions hold literals
  under L-0.17's rule (G), not as findings. Build-time disclosures after the registry freeze go to
  `T12/DISCLOSURES_BUILD.md`.
- **L-V (value area).** The two door scripts (`tierc12_va.py`, `tierc12_va_trades.py`) are `DOORS_T`;
  `tierc12_va_stamps.py` is the data-only reader, a decision module; the Tier-E two-trades tables are DOOR 2's and
  hold no `TRADE_COLS_T` column. The reader's API is L-V.2's (`bars`, `events`, `regimes`, `instants_of`, `stamp`,
  `licence`, `traverse`), each read sha-asserted through `certified()`; `traverse(name)` is the fitted-pin door and
  `licence` logs its reads into `READ_SET.json`. The V5 stamp tables are Stage V tables filed by the reader under
  `TC12-V.stamps.c/.r/.s` at `va/stamps/VA_STAMPS_<book>.parquet`. Stage V's suite owns prefix identity (F-VA-ASOF
  `[d]`) and hosts no leg that enumerates a later stage's modules or tables. `analytics/value_area.py`
  is numpy-only, keyword-only, default-free and holds structural literals only (L-0.17, L-0.22 leg (v)).
  `va/VA_MIRROR.json` is a registered record (collar-exempt); the traverse pin record is `va/TRAVERSE.json`; the
  per-member bar-close column of the V5 vector is `<ℓ>_bar_close_ms`.
- **L-X (statistics + registrations + close).** The prefix-pin function of L-0.1 in full (its own reading of contract
  :10) and the tc11-stamp's mechanics (its own reading of contract :13; the proof tree is a detached linked worktree)
  — L-0.1 and L-0.24 state the same laws at ruling level and add nothing that contradicts them. The registry's files
  and keys (`leans.sha256`, `rulings.sha256`, `disclosures.sha256`, `head`, the five payloads with `mechanism`);
  `REG_SET` and the two attestations; F-REG and the F-FAM blocks; the verdict-word pattern used by F-COLLAR and
  F-NOT; the three cell templates; the list `REGISTERED_TABLES_T`; `tierc12_regbook.write_arm`, the one caller of
  `put_regbook`, and the regbook layout (every named arm written, empty or not); the scorer's write law
  (`scores/SUPERSEDED.jsonl`, `--refile`); the close generator (its modules — `tierc12_close.py` and the text-only
  `tierc12_close_acts_template.py` — are the RENDERERS of L-0.17, held by L-X's digit trace), `close_acts.sh` (which
  hosts L-0.24's step and L-0.1's stamp of TC12's own contract), F-CLOSE-SCRIPT's stubbed sandbox run, F-TC11-STAMP's
  hosting suite, the report layout and its frozen whole-versus-pointed map.
- **L-C (control).** The book directories and the two roles names; F-CTRL; that every ride's `ride_spec` and
  `roles_name` are in its book manifest for F-NOT; `tierc12_books.py` is on `VA_BLIND_T`.
- **L-G, L-R, L-S.** Each names its book directories, its grids' axes, its hand-sample categories and which of its
  fixture legs are synthetic and which real-book, the columns F-NOT reads (lens, edge price and the level it is
  compared with, stop moves, entry fills), the pins it consumes — under the pin names of record — with their
  flow-leg witnesses and sample counts, whether its walk reads 5m children (`FIVE_MIN_READERS_T`), and — for the
  scalper — the typed list of VA columns it reads and its two `ema` call sites. Every builder of theirs is a
  decision module that reads filed columns through the reader; L-G's two modules are on `VA_BLIND_T`. L-G and L-R
  file `ride_spec` and `roles_name` for every mirrored ride, and no gate ships a re-ride arm. L-R reads the FLIP_HOLD
  pins and DEFINES the gaps-and-order null WITHOUT importing a module of the range machine (pins as filed data; the
  schedule mirrored and held to X's filed tables, O-4); the null's box machine is run by DOOR 2.
- **L-L (ledger + era + ferry).** The fourth book's spec is filed at `TC12-REG.ledger-spec`, before its ride (T3);
  `forward/BOOK4_FREEZE.json` is read by the TC12-L builder; the ferry is staged under `T12/ferry/` and its priority
  order is LEANS text (T4); `tierc12_forward_spec`, `tierc12_era` and `tierc12_pct` are on `VA_BLIND_T`.
- **The orchestrator.** Commits each record (L-0.9); runs the attestation tool (L-0.12); assembles `DOORS_T`,
  `VA_BLIND_T`, `FIVE_MIN_READERS_T`, `REGISTERED_TABLES_T`, the pin map and the pin register from the nine sections
  at freeze, with `NOT_RUN_FIDS_T`; rules amendments. At the freeze it also writes the TC12-LEANS record (which
  re-records the rulings and the X manifest), files AM-1 in `LEANS_AMENDMENTS.md` and D-5..D-12 in `DISCLOSURES.md`;
  at the TC12-REG commit it changes `scripts/tierc12_progress.py` (`RESUME_ORDER`, `SUBSTAGES`, `certified()`, the
  prefix form of `contract_of_record`); after the ledger-spec commit it writes `forward/BOOK4_FREEZE.json`.

---------------------------------------------------------------------------------------------------------------
### OBJECTIONS

OBJECTION O-3 / O-4 — accepted as O-25.
