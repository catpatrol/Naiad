# U1 · THE TC11 §11 RULINGS, THE CLOSE STATE, AND THE BUS — scout map for TIER-C12

Scout: read-only. Observed 2026-10-08T22:50Z–23:10Z (local 19:50–20:10 −03).
Trees: MAIN = `/Users/luis/Naiad` (branch `v12-v1-census`), XWT = `/Users/luis/Naiad/.claude/worktrees/tierc11x` (branch `tierc11x`).
Contract read: `…/scratchpad/tc12/2026-10-08_TC12_APOLLO.md`, 137 lines, 12,209 B, sha256 `861d6050e80e66995e4f9db2855aaf274d63285249c2549e5a0813582095a7bd`.
Every number below was read from the cited file in this session. "M:" = main tree path, "X:" = X-worktree path.
Nothing was written in either tree; both `git status` outputs were identical before and after (checked).

**A fact that changed while I was reading:** at 22:52Z MAIN gained commit `28e006b` —
`tierc12(STEP Q): contract filed verbatim — exchange/queue/2026-10-08_TC12_APOLLO.md sha256 861d6050…`
(1 file, 137 insertions; byte-identical to the scratchpad contract, `cmp` clean). MAIN is therefore now
**15** ahead of `origin/v12-v1-census`, not 14. The commit prefix in use is `tierc12(`.

---------------------------------------------------------------------------------------------------------------
## 1 · FACTS

### 1.1 TC11 BUILD_DRAFT §11 — the nine operator questions, VERBATIM

`M:research_outputs/tierc11/BUILD_DRAFT.md:5986-5996` (file 6,328 lines, 887,648 B, sha256 `e2cc364860d5a11393d0a064bc1637cf5c07e14aaddc857fe30e78b915354233`):

```
## 11 · OPERATOR QUESTIONS STILL OPEN

1. Q1 · MINOR-9: rule on the 156 SCORES.json leaves added since the lens reviews (none moved) — keep them, or re-file the scorer's record?
2. Q2 · The contract's BUILT stamp: stamp it and re-pin REGISTRATIONS.json, REGISTRY_CHECK.json and PROGRESS.json, or leave the contract byte-frozen?
3. Q3 · TC10's Q2 (does slippage join the toll of record?) stays open; every TC11 row carries the haircut twin beside the toll of record, never instead of it.
4. Q4 · R2 1w reads FAIL (provisional, n<30); its counts sit under the floor while its measured values clear their bars. Accept it as closing 1w for range trading, or order a re-measure when the lens has the ranges?
5. Q5 · The forward ledger: order the foundation re-rooted on a new snapshot and pin record so it can refresh.
6. Q6 · The push and the publish: run TC10's close_acts.sh (its step-6 `git add` needs -f: FN-M-TC10-ACTS-IGNORED), then TC11's — both are the operator's acts.
7. Q7 · The tierc11x lane vendors the pre-AM-1 env shim: align the two lanes, or keep them apart?
8. Q8 · The post-hoc candidates the reviews name (the relay in the windows v6 enters late; the memory-line first-hold twin): order a forward registration, or let them lie?
9. Q9 · Two reading conflicts the fidelity review names (L-W.4 against L-1.4 on Tier-E intervals; L-W.1 read as less-or-equal): ratify or overrule each.
```

The same nine stand, re-wrapped, in TC11's STAGED ledger append under "OPEN FOR THE OPERATOR (BUILD §11)"
(`M:research_outputs/tierc11/LEDGER_APOLLO_APPEND.md:213` onward, `OPEN FOR THE OPERATOR (BUILD §11)`); that block will land on
LEDGER_APOLLO saying "open" when the operator runs TC11's close acts.

The TC12 contract enacts **Q1/Q2, Q4, Q6, Q8, Q9** (contract :12-16). **Q3, Q5 and Q7 are not named** (see §2).

### 1.2 The findings behind the questions (the facts each ruling acts on)

Source `M:research_outputs/tierc11/close/S5_FINDINGS_NOT_FIXED.json` (`findings[].text`), printed first-line-only at BUILD_DRAFT.md:5913-5984.

| Q | finding id | text (verbatim from the JSON / BUILD_DRAFT line) |
|---|---|---|
| Q1 | `FN-M-SCORES-LEAVES` (BUILD_DRAFT:5943) | "SCORES.json between the reviewed commit 04067a0 (the lens reviews) and HEAD d307829: 156 leaves added, 0 removed, 3 changed — each changed leaf a string label (.rows[1].verdict_cell, .rows[5].verdict_cell, .rows[8].status_reason); 0 numeric, bool or null leaf moved. The TC11-FIX verifier filed the additions as MINOR-9, awaiting the operator's ruling (TC11_FIX_VERIFY.json verify)." |
| Q2 | `FN-M-QUEUE-STAMP` (BUILD_DRAFT:5945) | "exchange/queue/2026-09-24_TC11_APOLLO.md carries no BUILT line (other queue files do, e.g. exchange/queue/2026-09-22_OR2_oracle_rulings_ARGUS.md). Its sha256 bb38e016a8f3e55c… is pinned by REGISTRATIONS.json contract.sha256, scores/REGISTRY_CHECK.json contract.sha256 and PROGRESS.json contract_of_record — stamping BUILT into the file would change those bytes and break every pin. Whether to stamp (and re-pin), stamp a sibling file, or leave the contract byte-frozen is the operator's word." |
| Q4 | `FN-TRD-17` | "1w is the only lens with a positive edge net (+1.12 ATR) but has n=6 ranges on a fallback pick that is in-sample, so it reads FAIL (provisional, n<30)." |
| Q6 | `FN-M-TC10-FIRST`, `FN-M-TC10-ACTS-IGNORED` (BUILD_DRAFT:5946-5947) | TC10's `close_acts.sh:103` runs `git add "$APP" "$LAR"` without `-f`; both paths match `.gitignore:263` (`research_outputs/tierc10/**`); "stages it but exits 1 … So TC10's script stops at its step 6 after its step 5 has appended TC10's block to exchange/status/LEDGER_APOLLO.md, before its own residue commit and before publish()". Fix named: `git add -f` at `:103`. |
| Q7 | `FN-M-TC11X-SHIM` (BUILD_DRAFT:5944) | the tc11x lane "vendors the env shim from 086d66da — the pre-AM-1 shim. TC11's committed shim scripts/tierc11_env.py is sha256 1526093b25161927…". |
| Q8 | review candidates | "the relay in the windows v6 enters late; the memory-line first-hold twin" (BUILD_DRAFT:5995; :6004 "the reviews' post-hoc candidates are named for the operator, not registered"). |
| Q9 | `FN-FID-10`, `FN-FID-11` | "**Reading conflict:** L-W.4 says the condition block is the only Tier-E place a CI is printed, while L-1.4 prints a CI on every Tier-E row." · "**L-W.1 reads "closed before the 4h bar closes" as ≤,** with no rival reading printed." |

### 1.3 L-W.1 and L-W.4, VERBATIM

`M:research_outputs/tierc11/LEANS.md` — 40,646 B, sha256 `655e1605165e7a66c67f544e5cda421b46aa0b6fcd4cb97a6ad19654479f294f`
(byte-frozen: `LEANS_AMENDMENTS.md:3-4` "stays byte-frozen, because `REGISTRATIONS.json` pins its sha").

`LEANS.md:302-304`:
```
**L-W.1 VISIBILITY** — "only 1h bars CLOSED before the 4h bar closes".
- A 1h bar is visible at a 4h decision instant iff its close ≤ the 4h close.
- F-WARN-ASOF's sabotage reads a 1h bar with close > the 4h close, and it must FAIL.
```

`LEANS.md:324-339`:
```
**L-W.4 W2 COMPARISON GROUPS** — each cohort is compared with its **at-risk set**, with the complement within
that set printed beside.
- "Before +1R" and pre-entry cohorts are compared with the whole v6 book.
- "After +1R" cohorts are compared with the campaigns that reached +1R.
- "9/12 re-cross after entry" is compared with campaigns still open 1h after entry.
- Every post-entry cohort also prints its forward leg, E[final net R − R marked at the event's 1h close], i.e.
  hold vs exit at the event.
- **P-WARN-1 condition** (on the full-corridor v6 book the rule is scored on):
  - Cohort = campaigns with an **in-trade counter 12/89 cross before the +1R latch**.
  - Δ = mean(cohort) − mean(whole book), by `T5.cluster_boot_diff`, seed 20260924. MET iff the cluster-90% hi
    < 0.
  - The condition block is the only Tier-E place a CI is printed.
  - Fixture: the condition-cohort keys == the keys whose rule-book exit_reason is the warn exit, plus the keys
    whose first qualifying cross fell on a mismatch bar (listed).
- **Pre-entry tables:** for each event class (counter-12/89, counter-12/26, with-trend 9/12, with-trend 12/26)
  in (arm close, entry close]: n, P(win) and E[net R] vs the whole book, complement beside. Whole, Tier-E.
```

The rival of L-W.4's CI sentence is `LEANS.md:128-131` (L-1.4): "**Tier-E rows carry no verdict word.** Their CI-only reading is
printed as `would_read_ci_only`, alongside the collar columns `tier = 'TIER-E'`, `selection_not_a_result = 'a SELECTION, not a
result'` and `gates = 'nothing'`. This applies to every non-registered table and every R2 row except the lens verdict of record."

**As built (both readings were built, side by side):** Stage W's document heads its block
"## P-WARN-1 · the condition block (the only Tier-E place a CI is printed)" (`M:research_outputs/tierc11/stage_w/STAGE_W.md:38`) and its
W2 cohort tables carry no interval; the scorer's Tier-E arms carry `would_read_ci_only` (`M:scripts/tierc11_score.py:54-56`).
So "ratify the executor's readings" ratifies: (i) L-W.4's CI sentence scoped to Stage W's descriptive tables;
(ii) L-1.4's CI-only reading on every scorer Tier-E row; (iii) L-W.1's `≤`.

### 1.4 The TC11 "registry files" — every byte that pins the TC11 contract sha

TC11 contract: `M:exchange/queue/2026-09-24_TC11_APOLLO.md` — 103 lines, 8,442 B, sha256
`bb38e016a8f3e55ca3bcc09fec53ba6b8dc40accb60d054f8163d033a898f835`, STEP Q commit `b9ed953`. It carries `RATIFIED:` at `:2`
and **no `BUILT` line** (grep). Nothing after line 103.

Q2 names three files. The disk has more. Tracked files in MAIN naming `bb38e016` (`git grep -c`, `_det_*` excluded):

| class | file (M:) | where the sha sits | sha256 of the file now |
|---|---|---|---|
| **registry (Q2-named)** | `research_outputs/tierc11/registrations/REGISTRATIONS.json` (34,228 B) | top-level `contract.sha256` — OUTSIDE every payload and the chain | `648834bf30e20e92713bddef2374ddef1aae843f4d8ba152fc50166c8cc6f1ee` |
| **registry (Q2-named)** | `research_outputs/tierc11/scores/REGISTRY_CHECK.json` (6,880 B) | `contract.sha256`; also `registrations.sha256` = 648834bf… | `aea83bf10b5bbe62ff6c0af542870cd60f5ad8773b6bb61fab45ea465d8f8ed0` |
| **registry (Q2-named)** | `research_outputs/tierc11/PROGRESS.json` (101,683 B) | `contract_of_record.sha256`; `stages[0].artifact_shas["exchange/queue/2026-09-24_TC11_APOLLO.md"].sha256`; `stages[0].one_line` ("sha bb38e016…") | `dbcc08cf60a9dbb5827c65f3728857fcab12df50aeefee7667ba3dbfc205c4fe` |
| **registry (NOT named by Q2)** | `research_outputs/tierc11/registrations/REGISTRY_PIN.json` (308 B) | `contract_sha256` — checked by the scorer's PIN detector (`tierc11_score.py:484-489`) | `ea77921a410db962376412a5f179fd3d9225f81fb5405a788c8077cd46de748f` |
| typed constant | `scripts/tierc11_registrations.py:24` `CONTRACT_SHA`; HALT at `:187-188` | | |
| typed constant | `scripts/tierc11_score.py:220` `CONTRACT_SHA`; findings at `:399-404`, `:484-489` | | `81d99d63f9367268780fe9ec37a0c6af058b03670a83aaff010a93090eab5d68` |
| typed constant | `scripts/tierc11_score_fixtures.py:263` `CONTRACT_SHA_T`; checks `:789`, `:889` | | |
| typed constant | `scripts/tierc11_data.py:174` `CONTRACT_SHA256` (embedded at `:771`, `:2356`; no live-bytes comparison found) | | |
| typed constant | `scripts/tierc11_nest.py:640` (`"contract_sha256"` literal) | | |
| generator HALTs | `scripts/tierc11_close.py:608-611` (contract sha ≠ PROGRESS / ≠ REGISTRATIONS → halt); `:956` (REGISTRY_CHECK); also halts if the contract already carries `^BUILT` | | `246b32cb72479922f7f107c08e76dad830743acbfd0f9558077e7db2337bf81a` |
| data records carrying it | `data/AS_OF_PIN.json`, `data/STAGE_D_MANIFEST.json`, `ranges/SCALE_PICKS.json` (1 each) | "contract" pointer written at build time | |
| documents quoting it | `BUILD_DRAFT.md` (4), `LEANS.md:4` (1), `scores/S0_VERDICTS.md` (1), `scores/FIXTURES_SCORE.txt` (3), `scores/STAGE_SCORE.md` (3), `close/S5_FINDINGS_NOT_FIXED.{json,md}` (3 each), `close/TRACES.json` (2), `close/FIXTURES_CLOSE.txt` (1), `data/FIXTURES_DATA.txt`, `stage_{h,r,s,t_brk,w}/STAGE_*.md` (1 each), `review/LEANS_REVIEW_2026-09-25.json`, `scout/{F,H}_*.md` | prose | |
| 17 script docstrings | `scripts/tierc11_*.py` header lines ("sha256 bb38e016…") | prose | |

Second-order pins (the shas of the registry files themselves):
- `648834bf…` (REGISTRATIONS.json) is a typed constant in THREE scripts: `scripts/tierc11_score.py:224` (`REGISTRATIONS_SHA`),
  `scripts/tierc11_stage_g.py:170` (`REGISTRATIONS_SHA`), `scripts/tierc11_stage_t_brk.py:141` (`REGS_SHA_OF_RECORD`); and in
  `PROGRESS.json` (2), `scores/REGISTRY_CHECK.json`, `scores/S0_VERDICTS.md`, `stage_a/STAGE_A_MANIFEST.json`,
  `stage_t_brk/build_manifest.json`, `close/S5_FINDINGS_NOT_FIXED.{json,md}`.
- `aea83bf1…` (REGISTRY_CHECK.json): `PROGRESS.json`, `scores/SCORE_MANIFEST.json`, `scores/FIXTURES_SCORE.txt`, `scores/STAGE_SCORE.md` (3), `close/TC11_FIX_VERIFY.json`, `close/S5_*`.
- `dbcc08cf…` (PROGRESS.json): `review/attest/fix-head.json`, `close/S5_*`.
- **X pins these too, in 30 tracked X records** (`git -C XWT grep -c` for 648834bf / ea77921a / aea83bf1 / dbcc08cf): e.g.
  `X:research_outputs/tierc11x/PROGRESS.json` (7), `data/TC11_READS_X-FIX.json` (170), `data/TC11_READS_X6.json` (170),
  `data/TC11_READS_X-CLOSE.json` (48), `land/TC11_LANDING_2026-09-25T18-00-48Z.json` (5), `ferry/FERRY_MANIFEST.json` (3),
  `forward/BOOK_SPECS.json:31` (`registrations_sha256`), `registrations/REGISTRY_PIN_X.json` (`law_source.sha256`),
  `BUILD_DRAFT.md` (2). X's own machinery reads its **write-once extracted copies** `X:research_outputs/tierc11x/data/tc11_rec/{LEANS.md,
  registrations/REGISTRATIONS.json, data/AS_OF_PIN.json, data/STAGE_D_MANIFEST.json, data/fee_schedule.json, data/CONTRACT_SPECS.json,
  ranges/SCALE_PICKS.json}` (the extracted REGISTRATIONS.json hashes to 648834bf…), not TC11's live files.

**Structure that decides the cascade** (`REGISTRATIONS.json`, read):
- top keys `tier, contract{path,sha256}, leans{path,sha256}, family_m, family_q, family_bar, seed, registrations[9], chain[9], head, law`.
- each registration: `registration, seq, prior_pct, family_m, family_bar, seed, text_of_record, text_lines [lo,hi], context_of_record[{lines,text}], operative_spec, verdict_rule, text_sha256, sha256`.
- law (verbatim): "texts are the contract's own lines (frozen at STEP Q); operative specs are the executor's readings, filed before any TC11 book was computed; payload sha = sha256(json.dumps(body without shas, sort_keys, ensure_ascii=False)); chain line_sha256 over {seq, registration, sha256, prev}".
- chain head `6772568b31fcfb2d56eb8c80b66dedee4fb5082673369e872972df8f475ec8f9` (= `REGISTRY_PIN.json head` = typed `tierc11_score.py:226`).
- **`text_lines` (contract LINE NUMBERS) are inside the payload** (e.g. P-WARN-1 `[40, 42]`, context `[33, 39]`); the scorer re-cuts
  every slice from the live contract (`tierc11_score.py:418-446`).
- **The filer is write-once**: `scripts/tierc11_registrations.py:244-245` — `raise SystemExit(f"HALT: {tgt} exists — the filing is write-once")`. There is no `--refile` for REGISTRATIONS.json.

Consequence, derived from the code read above (not run): a BUILT stamp **inserted above line 103** shifts line numbers → every
`text_lines` slice mis-cuts → payload shas, chain head and everything pinned to `6772568b…` move. A stamp **appended after line 103**
leaves lines 1..103, the nine slices, nine contexts, nine payload shas and the chain head unchanged; it moves only the whole-file
sha (bb38e016… → new) and therefore the whole-file pins listed above.

### 1.5 The scorer's `--refile`

`M:scripts/tierc11_score.py`:
- `:61-68` — "7. WRITES (no-clobber; --refile to replace a record whose bytes differ): REGISTRY_CHECK.json · SCORES.json · FAMILY.json · BASE_IDENT.json · S0_VERDICTS.md · SCORE_MANIFEST.json".
- `:2648-2665` `def write_outputs(files: dict, out: Path, refile: bool) -> list[str]` — identical bytes are left alone; different bytes go to `<stem>_rerun<suffix>` and "the record is untouched unless --refile"; with `--refile` EVERY differing output is replaced (the flag is not per-file).
- `:189-194` usage: `tierc11_score.py [--regbooks-root=DIR] [--out-dir=DIR] [--refile] [--regbooks-label=TOKEN]`; `--dry-run` writes nothing.
- `:391-393` `def verify_registrations(doc: dict, contract: bytes, pin: dict, leans_bytes: bytes | None = None, file_bytes: bytes | None = None) -> list[str]`.
- Fixtures: `scripts/tierc11_score_fixtures.py … [--refile-transcript] [--root=DIR]` (`:212`, `:3418-3424`); close fixtures likewise (`scripts/tierc11_close_fixtures.py:45`).
- Records as filed: `scores/SCORES.json` 236,946 B sha256 `2c1a664a27abfc320355dcb89b2eff8a7f7637ddc26843e72ab3baf30cbef856`; `scores/S0_VERDICTS.md` 95,613 B sha256 `ea728250249e1f1f548faf315fac22515d653743075d64155c47f1ea06f670aa`. Neither `bb38e016` nor `648834bf` occurs in SCORES.json (grep): a re-pin run should not need to move it, but that is unverified until run.

`M:research_outputs/tierc11/LEANS_AMENDMENTS.md` (9,229 B, sha256 `85f57ce7832b2754cff70fe052dc87dcf4bcf4182f61112c7a1d227df84f0c07`): the amendment law (`:7-8`) —
"an amendment may follow from a build fact (the code cannot do what a reading says) or from a verifier's finding. It may never follow
from a registered rule's outcome." Amendments of record: AM-1 … AM-8 + AM-5 ERRATUM (headings at `:13, :27, :38, :47, :57, :65, :86, :105, :124`).
It is the file that carries changes because LEANS.md is byte-frozen — the precedent for "the pinned file stays, a dated sibling carries the change".

### 1.6 What a BUILT stamp looks like on earlier queue files

Law: `M:exchange/queue/README.md:8-12` (sha256 `1da1562eebd766f8433b47d23eea2fabb613e97c9f45faa2f8da204236861ef9`) —
"6. Execution stamp: `BUILT: <artifact or commit>` on a line of its own once the item is delivered (unbuilt items read `BUILT: PENDING` or
carry no stamp). `RATIFIED` says the work may start; `BUILT` says it finished. `MANIFEST.json` counts the gap between them as
`queue_ratified_unbuilt`". Rule 3 (`:5`): "Every item ends with a stamp line: `RATIFIED: <word> <date>`".

Exemplars (all placed directly under the RATIFIED block near the TOP of the file — i.e. the precedent position would shift line numbers):
- `M:exchange/queue/2026-08-22_RF1_rangefinder_ARGUS.md:8` — `BUILT: exchange/reports/BUILD_2026-08-22_RANGEFINDER_V0.md · 974e9be`, followed at `:9` by a parenthetical "(stamped by OR-2 STEP 10 — queue hygiene, OR1-g — 2026-09-23. The build document names no commit … so the commit is read from git log: …".
- `…RF2…:6` — `BUILT: exchange/reports/BUILD_2026-08-22_RANGEFINDER_V1.md · 6c21a05`; `…RF3…:7` — `…RANGEFINDER_V2.md · 374b9ef`.
- `…2026-09-22_OR2_oracle_rulings_ARGUS.md:6` — `BUILT: exchange/reports/BUILD_2026-09-22_ORACLE_RULINGS.md · or2 commits 00de4e0 … 11bec23 + the STEP 12 publish · F-BR 21/21 … · push WITHHELD (Q-3)`.
- `…2026-09-21_OR1_daily_oracle_ondemand_ARGUS.md:8` — `BUILT: exchange/reports/BUILD_2026-09-21_DAILY_ORACLE.md · code commits … · F-BR-1..17 17/17 · …`.
- Pending form: `008_sail-skeleton.md:12` and `2026-08-16_BR2…:4` — `BUILT: PENDING`.
- No stamp at all: `2026-09-22_TC10_RESUME_APOLLO.md`, `2026-09-24_TC11_APOLLO.md`, `2026-10-08_TC12_APOLLO.md`.
- Shape: `BUILT: <exchange/reports/ build document> · <commit(s)> [· fixture tallies · facts]`. The RF stamps were made by a lane commit
  (`5c5167e or2: step 10 — queue hygiene (OR1-g): RF-1, RF-2, RF-3 stamped BUILT; queue_ratified_unbuilt 8 -> 5 (live)`), not by `publish()`.
- The detector: `M:scripts/reviewer_manifest.py:499-509` `_is_stamped(blob, keyword)` — any line whose stamp value is non-empty and not `PENDING`. `M:exchange/status/MANIFEST.json:42-45` now: `queue_open 5, queue_ratified_unbuilt 5, queue_total 10, queue_unratified 0` (written 07:08 local, before the TC12 file was filed).

### 1.7 The three pending close acts — step by step

None has run. Evidence (all read at HEAD `28e006b`):
- `M:exchange/reports/` holds no `BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md`, no `BUILD_2026-09-24_TIERC11_EVENTS.md`, no `BUILD_2026-09-25_TIERC11X_EXIT_SFP_VALUE.md`, no `BUILDERS_REPORT_HEPHAESTUS_2026-09-23_TC10-STAGE-B-CLOSE.md` (ls). Newest files there: `BUILD_2026-09-22_ORACLE_RULINGS.md`.
- `M:exchange/status/LEDGER_APOLLO.md` — 2,426 lines, 174,090 B, sha256 `cd6ad43a0fe4890635e6d7098d29ae52d4af1268be4466740823701014222d2c`, identical to HEAD, last commit `d1eede0` (auto-publish 2026-08-22). Its last block is `:2355` `=== STATUS_APOLLO — 2026-08-22 — TIER-C9 · THE WINNERS' HABITAT + THE PAIR SWEEP ===`. No TIER-C10, TIER-C11 or TC11-X header. (The X worktree's copy and its `LEDGER.md` are byte-identical to MAIN's — `diff -q`.)
- The three staged appends still carry pending stamps: `M:research_outputs/tierc10/LEDGER_APOLLO_APPEND.md:213` (1), `M:research_outputs/tierc11/LEDGER_APOLLO_APPEND.md:189` (1), `X:research_outputs/tierc11x/LEDGER_APOLLO_APPEND.md:132, :220` (2).
- The three drafts are still in `research_outputs/`: TC10 `BUILD_DRAFT.md` 111,105 B (tracked), TC11 887,648 B (tracked), X 169,771 B (in the X worktree).
- `M:research_outputs/tierc10/close/close_acts.sh:103` still reads `git add "$APP" "$LAR"` (no `-f`): the patch Q6 names has NOT been applied.

| | TC10 | TC11 | TC11-X |
|---|---|---|---|
| script | `M:research_outputs/tierc10/close/close_acts.sh` 120 lines, 6,823 B, sha256 `3f5c868ba089965ae3dad120c9293b9375dde992df5043dcfecea2b02e4440f8`; **untracked and git-ignored** (`.gitignore:263`) — local disk only | `M:research_outputs/tierc11/close/close_acts.sh` 140 lines, 9,675 B, sha256 `7f601f8106f61fa857f79a0c95cea3edf74fe28cf34653ca5d4c7e931b78e2ba`; tracked; "Generated by scripts/tierc11_close.py (do not hand-edit)" | `X:research_outputs/tierc11x/close/close_acts.sh` 331 lines, 23,780 B, sha256 `02191457023d062a757f42d980f6b0ecc31ce127be8b3606e50b7e642d4d1940`; tracked on `tierc11x`; run "from the MAIN tree" |
| step 0 | branch `v12-v1-census`; clean INDEX; draft, report, append, ledger present; destinations absent; stamp pending (`:41-47`) | + TC10's report exists AND tracked, a `TIER-C10 · ` header in the ledger, ledger == HEAD (`:49-53`); clean index; 14 SOURCES present, tracked and == HEAD (`:41, :55-59`); destination absent; no `TIER-C11 · ` header yet (`:61`); stamp pending; **F-LAR11 re-run on the pre-stamp append "as the sources stand NOW"** (`:63-65`); `--check` exits here | main on `v12-v1-census`, clean index; `tierc11x` tip == `close/CERTIFIED_TIP` (40-hex); X worktree HEAD == that sha, on branch `tierc11x`, **clean besides `close/CERTIFIED_TIP`** (`:132-141`); TC10's and TC11's COMMITTED stamped appends each occur exactly once in the COMMITTED ledger, TC10's offset < TC11's, **by BYTES** (`:143-178`); ledger == HEAD; X's header not yet in it; merge path allow-list (`:108-121, :181-183`); `$DOC` absent; **`research_outputs/tierc11x` must NOT exist in the main tree** (`:185`); draft placeholders filled; stamps pending; `F-LEDGER-FMT --check` (`:192`) |
| then | 1 `git push origin v12-v1-census` (bare, `set -e`) + verify origin == HEAD · 2 LAW 5: `cp` draft → `exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md` (sha equal), `git rm` the draft, commit `tierc10(CLOSE): LAW 5 — …`, push · 3 `mv` the builder's report into `exchange/reports/` · 4 fill the stamp `N tierc10 commits, M on a remote` (subjects starting `tierc10`), re-run `scripts/tierc10_close_ledger_append_root.py` (F-LAR; rewrites `close/FIXTURES_CLOSE_ledger_append_root.txt`) · 5 `cat "$APP" >> LEDGER_APOLLO.md` · 6 `git add "$APP" "$LAR"` + commit (**exits 1 here per FN-M-TC10-ACTS-IGNORED**) · 7 `publish()` · 8 bright paths + "Operator: click Sync now." | 1 push (`|| die`) · 2 LAW 5 → `exchange/reports/BUILD_2026-09-24_TIERC11_EVENTS.md`, commit `tierc11(CLOSE): LAW 5 — …`, push · 3 fill the stamp `N tierc11 commits, M on a remote` (subjects starting `tierc11(`), `F-LAR11 --stamped` · 4 append to the ledger · 5 `git add -- "$APP" "$LAR"`, commit · 6 `publish()`, push result STATED · 7 bright paths + final line | 1 **the ferry of record** (AM-X21) in the X worktree: `tc11x_ferry.py --stage=X-CLOSE --pin-merge-target`, then `--fresh --stage=X-CLOSE`, then F-ROWS; commits bus files on `tierc11x` (tip may move by exactly one commit, `:249`) · 2 `git merge --no-ff tierc11x`; dies if the merge touched `research_outputs/tierc11/` (`:259-260`) · 3 `git push origin v12-v1-census` · 4 LAW 5 → `exchange/reports/BUILD_2026-09-25_TIERC11X_EXIT_SFP_VALUE.md` · 5 `tc11x_close_fixtures.py --stamp --push-sha --ferry-head --report`, `F-LEDGER-FMT --stamped` · 6 append, tail checked byte for byte · 7 `git add -f -- "$APP" "$LAR"`, commit · 8 `publish()` · 9 bright paths + final line |
| ledger header | `=== STATUS_APOLLO — 2026-09-22 — TIER-C10 · "UNSEEN RANGES": …` | `=== STATUS_APOLLO — 2026-09-25 — TIER-C11 · THE ENGINE BOUND TO EVENTS: …` | `=== STATUS_APOLLO — 2026-09-25 — TIER-C11 · TC11-X — THE EXIT, …` (deliberately passes TC10's regex `TIER-C\d+ · `) |
| staged append | 255 lines, 14,925 B, sha256 `1288b59bae687f6a56f31cd75d958dc53400af78f4c7ff77ede3965972d5021e` | 253 lines, 16,732 B, sha256 `227317d1097c0f4e551ed90b717c09aa559a13006cb29e20c078a3e6d16414e1` | 260 lines, 16,154 B, sha256 `c63f7a18e2c4540f8ef8eddb178918252a7a6a50f43317b0a051ae41364db9e3` |
| «cites» re-verified at close | 7 → TC10 contract; **4 → `LEDGER.md` (lines 829, 834, 835, 836)**; **2 → `exchange/status/LEDGER_APOLLO.md` (2422-2423)**; 4 → TC10 PROGRESS.json; 3 → REGISTRATION_TEXTS.json; 2 FIXTURES_PANEL; 2 FIXTURES_RESUME; 1 P-GEN-1.rows.json | **12 → `exchange/queue/2026-09-24_TC11_APOLLO.md` BY LINE** (e.g. `:9`, `:16-18`, `:40-42`, `:45-46`, `:47-48`, `:99`); **9 → `scores/SCORES.json` by JSON path**; **3 → `forward/FORWARD_LEDGER.md` (`:5`, `:7`, `:38`)**; `stage_r/STAGE_R.md:35`; `scores/FAMILY.json#law`; `books/FIXTURES_BOOKS.txt`; TC10's append `:250-254`; TC10 contract `:2-3` | 8 LEANS_X.md, 7 review/CLOSE_BRIEF.json, 6 X contract, 5 SCORED_X.md, 4 BUILD_REVIEW, 3 land/TC11_LANDING…18-00-48Z.md, X-FIX.json, LEANS_X_AMENDMENTS.md, **1 → `exchange/status/LEDGER_APOLLO.md:2422-2423`** |

Push state (git):
- `origin/v12-v1-census` = `ac8d8da` ("exchange: auto-publish 2026-09-26"); reflog: pushed 2026-09-26 07:00:07 −0300; before it `4ae8c81` 2026-09-25 07:00:20. MAIN HEAD `28e006b`; **15 ahead** (14 `exchange: auto-publish` 2026-09-27 … 2026-10-08 + the tierc12 STEP Q commit).
- **All 10 `tierc11(` commits are already on the remote** (each is an ancestor of `origin/v12-v1-census`) — the 07:00 auto-publish pushed the branch, not the operator's close acts. 32 commits have subjects starting `tierc10`.
- `tierc11x`: tip `7b24f835bcbf7430eb0f97b6c39b6b1b233eef11` == `X:research_outputs/tierc11x/close/CERTIFIED_TIP` (untracked, the one allowed dirty path); merge base with main `e97ad7390c6212273b0e06daf33a463d4106c9d1`; 18 commits beyond it; **no remote branch** (`git branch -r` lists no `origin/tierc11x`) — the whole X lane is local only.
- Remote: `git@github.com:catpatrol/Naiad.git`. **Every push since 2026-09-27 has failed**: each DAILY's §10 reads "publish did not complete: committed <sha> but push failed: ssh: connect to host github.com port 22: Undefined error: 0" (2026-09-23, -24, -27, -29, -30, 10-02, -04 … 10-08; pushed only on 09-25 and 09-26). Step 1 of every close acts script is a push, so none can pass step 1 until the SSH route works.

### 1.8 The two modified-but-uncommitted files in MAIN

`git -C M status` (tracked changes only): `exchange/status/daily/DAILY_2026-10-08.md`, `research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt`.
1. `exchange/status/daily/DAILY_2026-10-08.md` (+21 lines): the daily routine's own "## 10. Publish" and "## 11. Mailbox" sections, "Appended after the publish step ran; these bytes are published by the next run, not this one." (carries today's push-failure text). The next `publish()` — the 07:00 routine or whichever close act runs first — commits it (TC11 named this class `FN-M-EXCHANGE-SWEEP`, BUILD_DRAFT:5948).
2. `research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt` (3 lines changed, 15,919 B, mtime Sep 23 11:36, sha256 `266b94d7…`): TC10's F-LAR transcript re-run after commit `68cde3e` updated two of the sources it lists — `FIXTURES_RESUME.txt` 1622ea6b… → `e8af6dee…` and `PROGRESS.json` 310d4dd6… → `e0abf4ca…` (both equal the files' current shas) — and the F-DET digest 376d0884… → 3cbfefda…. Both versions end `FIXTURE SUMMARY 9/9 GREEN`. TC10's close acts step 4 re-runs that script (rewriting the file again) and step 6 commits it. **It is TC10's residue; not TC12's to commit, restore or stash.**

Untracked in MAIN (not TC12's): `pine/SS12_*_v12_6.pine`, `pine/SS_Anchor_v12_T_0.pine`, five HTML/dir items under `research_outputs/`.

### 1.9 The bus conventions the CLOSE names

**publish_exchange / publish()** — `M:scripts/publish_exchange.py` (898 lines, sha256 `15eec3d0bf0420200d94fc3087e4868a59eecb5cdb1fc21e01b8c80daae8a65b`):
- `:565` `def publish(repo, date_str, remote="origin", log=print, allow_oversize=None)` → dict with `status` ∈ {`PUBLISHED`, `NOTHING`, `FLAGGED`, `REFUSED`, `ERROR`}, plus `offenders, staged, commit, branch, error, pushed, bytes, fraction, tick_bytes, tick_fraction, budget, heartbeat, largest, oversize_override, bus_health, over_flag, mailbox`. "Never raises."
- What it does: `git add -- exchange` (`:603`) → reads the WHOLE index back (`:620`) → `guard()` (`:187`: every staged path must start with `exchange/`; else **`git reset`** (mixed) and status `FLAGGED`, `:624-631`) → size budget → `git commit -m "exchange: auto-publish {date}"` (`:49, :737`) → **`git push origin <branch>`** (`:745`; the whole branch, every local commit) → MAILBOX refresh in `finally`.
- Constants (the file is the source of record; "never a copy", CONVENTIONS §3.2): `SCOPE = "exchange/"` (`:48`), `BOX_BYTES = 16_000_000` (`:95`), `WARN_FRACTION = 0.40` (`:109`), `REFUSE_FRACTION = 0.70` (`:110`), `OVERRIDE_ENV = "NAIAD_ALLOW_OVERSIZE_PUBLISH"` (`:111`), `TICK_EXTRA = ("LEDGER.md",)` (`:128`), `FLAG_BYTES = 64_000` (`:160`).
- `:201` `def budget(total_bytes, box=BOX_BYTES)` → `("REFUSE", frac)` iff `frac > 0.70`; `("WARN", frac)` iff `frac >= 0.40`; else `("OK", frac)`. Measured on the **TICK SET** = the `exchange/` INDEX + `LEDGER.md`. So **WARN from 6,400,000 B; REFUSE above 11,200,000 B**. WARN only prints (`:708-712`); REFUSE resets the index and publishes nothing unless overridden (`:713-729`).
- The invocation of record: CONVENTIONS §3.4 (`M:exchange/status/CONVENTIONS.md:413`):
  `~/venvs/naiad/bin/python -c "import sys; from pathlib import Path; R=Path('.').resolve(); sys.path.insert(0,str(R/'scripts')); import publish_exchange as p; r=p.publish(R,'<YYYY-MM-DD>'); print(r['status'], r['commit'], r['pushed'], r['offenders'])"`
  and `:415` "Do NOT `git add` or `git commit` exchange files separately — let the guard do it"; `:419` "A `git add` of any file OUTSIDE `exchange/**` in the same paste goes nowhere … Commit non-exchange paths explicitly, in their own authorized commit."

**The box now** (measured at HEAD `28e006b`, the index): `exchange/` 2,640,127 B in 116 files + `LEDGER.md` 259,298 B = **2,899,425 B = 18.121 %** of 16,000,000 → 3,500,575 B below WARN, 8,300,575 B below REFUSE. Largest box files: `exchange/status/LEDGER_APOLLO.md` 174,090; `LEDGER_ATHENA.md` 143,605; `BUILD_2026-08-12_CENSUS2B_VULT1.md` 105,838.
Pending adds ahead of TC12 (read from disk): TC10 111,105 + 35,597 + ~14,786 stamped; TC11 887,648 + ~16,572 stamped; X 169,771 + 16,154 + its contract 5,058 + its rows.
**X's ferry is a first-fit to just under WARN**: X's own forecast (`X:research_outputs/tierc11x/ferry/BOX_FORECAST_CLOSE.md:145-147`) reads "The box after the forecast's ferry, on the merge target: 5,134,272 B = 32.09% (OK); with the reservation 6,397,755 B (OK) … WARN from 6,400,000 B: the slack below it is 2,244 B" · "WRITTEN at the forecast: 19; HELD FOR ATHENA: **k = 80**". (That forecast pinned main at `6f34939`, before the 14 auto-publishes and the TC12 queue file.)

**The other limits**: the trip-wire — "Any box-bound file over 64,000 B is flagged to the operator by name, with its intended home, at the moment it is created" (CONVENTIONS `:360`), a naming duty, never a refusal. The per-file cap — `M:exchange/README.md:21` "**1 MB per-file cap.** No single file under `exchange/**` may exceed 1,048,576 bytes." and `:20` "**Text only.** Markdown, JSON, plain text." (CONVENTIONS `:478`). TC11's generator used 1,000,000 B for the same cap (BUILD_DRAFT:6270) and "HALTs over it".

**"draft off-bus" and LAW 5**: `M:exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:21-22` (LAW OF RESUMPTION, item 5) — "the build doc drafts under research_outputs/tierc10/ and moves to exchange/reports/ ONLY at close (a draft under exchange/ is not a draft)." Item 6 (`:23-24`): "after EVERY stage: commit + update research_outputs/tierc10/PROGRESS.json {stage, status, artifact shas, as_of, fixtures} + one line to the draft."

**"STATE push"**: `M:research_outputs/tierc11/LEANS.md:542` — "**No push without the operator's word.** "STATE push" = state the push result plainly." X: `X:…/LEANS_X.md:2499-2500` — "**The executor never pushes, never calls `publish()` in either tree, and never merges.** "STATE push" means the push result is stated plainly." CONVENTIONS `:399` "states on screen whether the push SUCCEEDED."

**"bright paths"**: CONVENTIONS `:407` — "On-screen output stays short and displays, in BRIGHT COLOURS, the exact filenames and full repo paths the operator must carry." Implemented as `printf '\033[1;33m%s\033[0m\n' <paths…>` (`M:…/tierc11/close/close_acts.sh:132-139`).

**"Operator: click Sync now."**: printed last by the acts script (`…tierc11/close/close_acts.sh:140`); AM-X28 (`X:…/LEANS_X_AMENDMENTS.md:593-599`): it is BOTH the report's last line and the script's last screen line, and "must NOT appear in the LEDGER_APOLLO append's bytes".

**The LEDGER_APOLLO append format** (TC10's law, `M:scripts/tierc10_close_ledger_append_root.py`, sha256 `08c0d289e8c9600b87d3d92e3c220a0bc8285786bcbb3f59355f73500db51114`):
- `:84` `SEP = "\n---\n\n"`; `:554` `def check_format(block: str) -> tuple` requires: block starts with SEP; then regex
  `=== STATUS_APOLLO — \d{4}-\d{2}-\d{2} — TIER-C\d+ · [^\n]+ ===\nLANE      [^\n]+\nCLASS     `; ends `"\n=== END ===\n"` with exactly one `=== END ===`; and `"Operator: click Sync now."` not in the block.
- Cites: `«path:L1-L2»` (or `«path#json.path»`) followed by `| ` verbatim lines (`+ ` marks a wrap continuation); `M:scripts/tierc10_close_close_ledger_append.py` `:616 cite_of(q)`, `:626 render_quote(indent, q)`, `:978 parse_quotes(text)`, `:1012 verify_quote(q, src)`. X copied these (never imports): `X:scripts/tc11x_close_fixtures.py:124 check_format`, `:171 parse_quotes`, `:205 verify_quote`, `:526 fill_stamps`, `:567 derive_values`.
- A number known only after the push is a `⟦STAMP AT CLOSE — …⟧` bracket, filled by the acts script and re-certified.
- CONVENTIONS `:324`: "Every build document ENDS by appending the session's STATUS entry to the commissioning lane's ledger (`exchange/status/LEDGER_<LANE>.md`) in the same session." `M:exchange/status/README.md:7` "Append, never rewrite".

**READMEs**: `M:exchange/README.md` (sha256 `69f80fb2…`) `:6-8` "This directory is the **visibility bus**. It is pushed to GitHub automatically … Evidence and study artifacts are NOT published this way — they keep the per-authorization push rule (ruling Q-2 A)."; `:31-32` push scope. `M:exchange/reports/README.md` (sha256 `f1010973…`) `:6` "One file per run. A re-run gets a new file, never an overwrite of the old one."

**The daily 07:00 auto-publish**: launchd agent `com.naiad.daily` (loaded; `launchctl list` shows it, last exit 1), plist `~/Library/LaunchAgents/com.naiad.daily.plist` — `/Users/luis/venvs/naiad/bin/python /Users/luis/Naiad/scripts/daily_routine.py`, WorkingDirectory `/Users/luis/Naiad`, `Hour 7, Minute 0` local (−03), `RunAtLoad false`. It writes `exchange/status/daily/DAILY_<date>.md`, `MANIFEST_<date>.json`, `HEARTBEAT.md`, `MANIFEST.json`, rolls the 7-file window to `research_outputs/_daily_archive/`, then calls `publish_exchange.publish(ROOT, today)` at `M:scripts/daily_routine.py:1489`. Registry: `M:exchange/status/CADENCE.md:11-13`. **Also** `com.naiad.estate` (Sundays 08:00) and `com.naiad.workflow` (Sundays 08:30) call `publish()` (`M:scripts/backup_estate.py:1422`; commits `6c4b4a6` 08:00:43 and `08b47a6` 08:30:09 on Sunday 2026-09-27 confirm). Next fires: 2026-10-09 07:00 −03 (10:00Z); Sunday 2026-10-11 08:00 and 08:30.

**The ferry law (X6, "standing, from this build on")**: `X:exchange/queue/2026-09-25_TC11X_APOLLO.md:42-44` (sha256 `40e0c4b716b978ab913e3900db01502b0113b93ece16afa60a8079d7d0203c3d`). X's readings: `LEANS_X.md:2184-2198` LX-X6.2 (path `exchange/rows/<tier>/<source path, extension dropped, '/' → '__'>.csv`; "Written **only in the worktree**. Never in the main tree's `exchange/`, which the 07:00 routine would sweep (daily_routine.py:1489)"); `:2200-2202` LX-X6.3 serializer `pandas.to_csv(index=False, lineterminator="\n", encoding="utf-8")`; `:2204-2216` LX-X6.4 cap "**2,000,000 B on the CSV alone**" (`X:scripts/tc11x_ferry.py:177` `CAP_BYTES = 2_000_000`), whole rows only, pointer in `FERRY_MANIFEST.json` rendered as `ROWS_MANIFEST.md`; `:2233-2260` LX-X6.7 the box guard ("**A file whose ferry would push the projected box across WARN is NOT written.** It is listed … as **"HELD FOR ATHENA"**", "REFUSE is never overridden"); `:2262-2268` LX-X6.8 the four conflicts filed for ATHENA (1 MiB cap vs 2 MB; invariant 3; the evidence rule; the hand-commit rule); AM-X14/15/17/21 (`LEANS_X_AMENDMENTS.md:318-427, :478-503`): a close reservation before the first-fit, the box measured at the MERGE TARGET pinned BY SHA, and "**The ferry of record for the bus is a CLOSE ACT**". `exchange/rows/` does not exist in MAIN today; X's worktree holds `exchange/rows/tierc11/` (8 files) and `exchange/rows/tierc11x/` (7 files, incl. `sfp__X2_trades_1h.csv` 1,999,149 B).

### 1.10 SAIL — what it is, where HELD is recorded

- What: `M:exchange/reports/BRIEF_ATHENA_SAIL_REPO_2026-08-17.md:1-10` — "THE PROMETHEUS-SAIL REPOSITORY … Mission: stand up the live-weather paper harness." · "**SAIL is a body, never a brain.** It imports the ratified Naiad card and executes it; it re-implements nothing."
- The work order: `M:exchange/queue/008_sail-skeleton.md` (66,843 B, sha256 `cdca8596829a4381c5879098e4f905fcf90541feec838cb88527150634342b3e`): `:3-6` RATIFIED "for DEC-1..DEC-5, D-4 (strengthened), D-9, F-SAIL-8 and the REGISTER addition ONLY … D-1..D-8 and F-SAIL-1..7, 9, 10 … are PENDING CONFIRMATION — see D-0, which HALTS before any code."; `:12` `BUILT: PENDING`; `:882-885` "## D-0 · EXECUTION RECORD — 2026-08-22 · **D-0 RAN on 2026-08-22. IT IS OPEN.** … `~/naiad-sail` does not exist".
- The HOLD: `M:exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:2-3` "RATIFIED: operator 2026-09-21 (TC10 contract; Q1–Q5 on lean; Q6 SAIL spec HELD until TC10 autopsied; …" and `:143` "no SAIL act (spec held by operator word)"; restated by `M:exchange/queue/2026-09-24_TC11_APOLLO.md:99` "(m=9; SAIL still HELD; the forward ledger opened)"; `X:…/2026-09-25_TC11X_APOLLO.md:54` "no sail". The standing line on the ledger is TC9's: `M:exchange/status/LEDGER_APOLLO.md:2422-2423` "NINE TIERS IN-SAMPLE; NOTHING HAS CLEARED ITS OWN BAR. SAIL-READY remains card_spec freeze at v6 PLAIN."
- **"operator 2026-09-24"**: no file in the repo pairs "SAIL" with "2026-09-24" on one line (`git grep`, excluding `docs/history` and `_reviewer_box`). The only 2026-09-24 operator act that holds SAIL is the ratification of the TC11 contract (`…TC11_APOLLO.md:2` "RATIFIED: operator 2026-09-24") whose CLOSE clause `:99` says "SAIL still HELD". There is no separate ruling document of that date.

### 1.11 The Q-R3 law — verbatim, and every restatement

- **The ruling** — `M:LEDGER.md:834` (file 921 lines, 259,298 B, sha256 `4d58d591668badffc34624e81feddf106ac94a92ca64aceafd4f871e84d31c76`), under `:829` "## 2026-07-29 — Range-and-Structure layer: interview rulings + session ratifications":
  ```
    - Q-R3 PLAYBOOK-R TIMING: (a) — detection and gating first; a range-trading contract is drafted ONLY IF the height-vs-toll feasibility gate AND the edge-fade outcome leg both pass.
  ```
- **TC10's contract** — `…TC10_RESUME_APOLLO.md:78-79`: "· [Q-R3] HEIGHT-vs-TOLL feasibility per lens (confirmed-range height ÷ round-trip toll, distribution) + the EDGE-FADE outcome leg; boundary-fade stays Tier-E". TC10's append is REQUIRED to cite `LEDGER.md` 834 (`tierc10_close_ledger_append_root.py:582` `("Q-R3", "LEDGER.md", 834, 834)`, inside `REQUIRED` at `:581-584`).
- **TC11's contract** — `…TC11_APOLLO.md:16-18`: "R2 FEASIBILITY GATE PER LENS [Q-R3 law]: confirmed-range height ÷ round-trip toll (distribution) + the edge-fade leg; PASS/FAIL printed per lens; a FAIL closes that lens for range trading in this and every later tier unless the toll model changes (maker twin below is the only reopening path)."
- **TC11's reading** — `LEANS.md:199-208` (L-R.4): "**TC10's [Q-R3] gate unchanged**, including its floor law (a leg under its floor FAILS): the height leg: n_ranges ≥ 30, median(height ÷ toll) ≥ 3.0, share(ratio < 1) ≤ 0.10; AND the edge-fade leg: fade from the outer 20% toward the far boundary, edge_n_ranges ≥ 30 and edge_n ≥ 30, median H20 term − toll > 0, within one era. **Lens verdict of record = the CLASSIC5 pooled row, HOLDOUT era, calibrated scale, taker toll.** **Two words: PASS; FAIL.** An under-floor FAIL prints "FAIL (provisional, n<30)". Any FAIL closes that lens for range trading per the contract; … A taker FAIL with a maker-twin PASS reads "FAIL — maker twin PASSES (the reopening path; needs a toll-model change the operator rules)"."
- **TC11's verdict** — `M:research_outputs/tierc11/stage_r/R2_LENS_VERDICTS.json` (7,185 B, sha256 `82cc3ec6ddd588c9fbd8402def471438a0c931590606b9a2a6cc3a97572f3087`), keys `as_of_last_closed_4h, disclosure, law, lenses{5m,15m,1h,4h,12h,1d,1w}, record{era:holdout, panel:POOLED:CLASSIC5, scale_kind:calibrated, toll:taker}`: every lens FAIL on the PIVOT detector, maker twin FAIL on every lens; `1w`: `n_ranges 6`, `edge_n_ranges 5`, `edge_net_h20 1.1236002`, `pick_window "whole-tape (fallback)"`, maker/charter twins "FAIL (provisional, n<30)". BUILD_DRAFT:339: "Under the [Q-R3] law a FAIL closes the lens for range trading in this and every later tier unless the toll model changes, and the maker twin — the only reopening path — fails on every lens too."
- **X's restatement (in data)** — `X:research_outputs/tierc11x/va/feasibility.parquet` (98,554 B, sha256 `ea8573b3240bb1112521c55f0a52ee2ed7156c598b7665685d0b86eefbecb6f0`; **git-ignored, on disk only**), columns of record:
  - `verdict_law`: "LEDGER.md:834 — 'a range-trading contract is drafted ONLY IF the height-vs-toll feasibility gate AND the edge-fade outcome leg both pass'. verdict_pass = gate_height_pass AND gate_edge_fade_pass. JUDGED ON ERA = 'holdout', AND ON NO OTHER: both legs are computed on this era's bars and both sample floors are applied within it [LEAN R3-f]."
  - `gates_what`: "NOTHING IS SCORED HERE. This row gates ONE thing and it is not a score: whether a range-trading contract may be DRAFTED under LEDGER.md:834. … AND IT GATES THAT FOR ERA = 'holdout' ONLY: the same panel is filed three ways (ALL / tuning / holdout) and the three verdicts differ. A form scored on the holdout must read the holdout row [LEAN R3-f; review round 3]."
  - `ledger_line`: "No registration until the value-area detector's edges-respected leg passes (LX-X3.14): a ledger line, not an action; a VA PASS licenses only that lens × detector × toll, and any later VA registration is pre_seen for bars <= 2026-09-25T00:00Z"
  - `min_n_law`: "BOTH legs carry a SAMPLE FLOOR: gate_height needs n_ranges >= 30, gate_edge_fade needs edge_n_ranges >= 30 confirmed ranges AND edge_n >= 30 in-range entries."; `gate_law_sha` `6b53434fcff30273c5df007d89c7fc0982ec5d639a3c39f0bde58196c3d56ee9`.
- **X's reading** — `LEANS_X.md:1811-1818` (LX-X3.14): "Reading: a **ledger line, not an action**. No registration may ever be drafted from the VA detector until its edge-fade ("edges respected") leg PASSES on the lens verdict of record. … **A VA PASS licenses only that lens × detector × toll** [statistics 11]. Any later VA registration would be `pre_seen` for bars ≤ 2026-09-25T00:00Z: X3's two-trades table prints those very outcomes on the full corridor, and 4 lenses × 2 tolls give 8 chances at a PASS."
- **X's standing pre_seen line** — `LEANS_X.md:2468-2470`, quoted into X's staged append: "any later registration drawn from an X Tier-E grid (X1 cells, X2 twins, X3 events and feasibility, X4 cells) carries pre_seen for bars ≤ 2026-09-25T00:00Z; a VA PASS licenses only that lens × detector × toll".
- **The VA words on disk** (`va/feasibility.parquet`, `asset == "POOLED:CLASSIC5"`, `scale_kind == "va_regime"`; `of_record_for_detector` True only on the holdout·taker rows; taker `toll_bps` 10.0, maker 4.0):

  | lens | era | taker `verdict_pass` (edge_net_h20) | maker `verdict_pass` (edge_net_h20) | `lens_word` (holdout·taker row of record) |
  |---|---|---|---|---|
  | 1h | holdout | False (−0.058994) | True (+0.038001) | "FAIL — maker twin PASSES (the reopening path; needs a toll-model change the operator rules)" |
  | 1h | ALL / tuning | False (−0.037047 / −0.025755) | True (+0.044305 / +0.048479) | — |
  | 4h | holdout | **True (+0.093365)**, n_ranges 509 | True (+0.139728) | "PASS" |
  | 4h | ALL / tuning | True (+0.095935 / +0.100655) | True (+0.135661 / +0.136097) | — |
  | 12h | holdout | False (−0.029472) | False (−0.003302) | "FAIL" |
  | 12h | ALL / tuning | False / False | False / False | — |
  | 1d | holdout | **True (+0.042952)**, n_ranges 122 | True (+0.059306) | "PASS" |
  | 1d | **ALL / tuning** | **False (−0.212326 / −0.347871)** | **False (−0.198172 / −0.334911)** | — |

  The `va_lblock` twin at 12h reads maker True / taker False on the holdout (X BUILD_DRAFT:360 "FAIL / PASS"). X has **no 1w and no 5m VA record** (lenses 1h, 4h, 12h, 1d only: `va_series_{1h,4h,12h,1d}.parquet`).
- **Where the maker toll in those rows comes from**: `toll_bps_source` = `research_outputs/tierc11/data/fee_schedule.json[<asset>].maker_round_trip_bps`. That file (`M:research_outputs/tierc11/data/fee_schedule.json`, 38,721 B, tracked, sha256 `6febe170d423b0ef37dca9fe95a7316e4259ef5a77e576cafa6781d581c1968b`) already carries, per asset, `maker_bps_per_side 2.0`, `maker_round_trip_bps 4.0`, `maker_kind "ASSUMPTION — Binance USDT-M VIP0 maker per README; the engine books every fill as taker; this is a TWIN, never the toll of record [L-1.2]"`, `maker_source [README.md:150 …, scripts/v3_recompute.py:965 …]`.

### 1.12 Pins this unit hands TC12 (path · sha256)

| record | sha256 |
|---|---|
| `M:exchange/queue/2026-10-08_TC12_APOLLO.md` (137 lines, 12,209 B, commit `28e006b`) | `861d6050e80e66995e4f9db2855aaf274d63285249c2549e5a0813582095a7bd` |
| `M:exchange/queue/2026-09-24_TC11_APOLLO.md` | `bb38e016a8f3e55ca3bcc09fec53ba6b8dc40accb60d054f8163d033a898f835` |
| `M:exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` | `8a0bf279bcab0f27161a7d965535445807f4e713e77d045b0ba124bc7f803c7a` |
| `X:exchange/queue/2026-09-25_TC11X_APOLLO.md` (not in MAIN until X merges) | `40e0c4b716b978ab913e3900db01502b0113b93ece16afa60a8079d7d0203c3d` |
| `M:research_outputs/tierc11/BUILD_DRAFT.md` | `e2cc364860d5a11393d0a064bc1637cf5c07e14aaddc857fe30e78b915354233` |
| `M:research_outputs/tierc11/LEANS.md` / `LEANS_AMENDMENTS.md` | `655e1605…f294f` / `85f57ce7…0c07` (full values above) |
| `M:research_outputs/tierc11/close/S5_FINDINGS_NOT_FIXED.md` | `58d8d9b416d2780719b77384c52fa5b57602afc5c130f3aa8d5d7260b8996c31` |
| `M:research_outputs/tierc11/stage_g/STAGE_G.md` (the crossed table, `:174-198`) | `440509bc8c00bc32b48f745a8f76ca1b6c6d6ddb08f708432790ec164e2d0187` |
| `M:research_outputs/tierc11/stage_r/R2_LENS_VERDICTS.json` | `82cc3ec6ddd588c9fbd8402def471438a0c931590606b9a2a6cc3a97572f3087` |
| `M:LEDGER.md` / `M:exchange/status/LEDGER_APOLLO.md` | `4d58d591…1c76` / `cd6ad43a…2d2c` |
| `M:exchange/status/CONVENTIONS.md` | `42b2cdd6ae4fa5cd85548c133862ac25ddad9c7dd3910b63555a5b628f8a226e` |
| `M:scripts/daily_routine.py` | `969ee13d64f45ceee95d05093f2b0dc5f7244ae8380b35dd7cafb6f8ff36998b` |
| `X:research_outputs/tierc11x/LEANS_X.md` / `LEANS_X_AMENDMENTS.md` | `74a989ee6357e2169f2ad88722b67f1174cf0d080783dc8c77f5f064e3468623` / `af845b95d1c7699f788aa242af6f5bef0d0f86b92a74a938cb7ca14c9d87d059` |
| `X:research_outputs/tierc11x/BUILD_DRAFT.md` | `0555cafc1129cdda6c12f39885e1e84fd8e567d7dbcf179452e0b08d84a43e6e` |
| X certified tip (`close/CERTIFIED_TIP`) | `7b24f835bcbf7430eb0f97b6c39b6b1b233eef11` |

P-ADM-1's pre-naming source, as filed (`STAGE_G.md:197`; also BUILD_DRAFT:5547):
`| age:on¦win:on¦ratr:off | yes | yes | no | 110 | +0.5146 | +56.6072 | 42.7273 |  | 90 | -15.7997 | TIER-E | a SELECTION, not a result | nothing |`
and the far-stop forfeit (`STAGE_G.md:192`): `| age:off¦win:off¦ratr:on | … | 147 | +0.1300 | +19.1155 | … | 53 | +21.6921 | …`.
Tables behind it: `M:research_outputs/tierc11/stage_g/g_campaign_gates.parquet` (200 × 41; sha256[:16] `c5a5f486df5709c0`) with
`symbol:object, entry_ms:int64, entry_close_ms:int64, direction:int64, arm_i:int64, arm_ms:int64, entry_i:int64, era:object, net_r:float64, tide_streak_entry:int64, tide_left_censored:bool, tide_edge_q25/q50/q75:float64, tide_band:object, tide_streak_age_arm:int64, tide_streak_age_arm_censored:bool, arm_band_on_entry_edges:object, arm_old_on_entry_edges:bool, arm_age_gt206:bool, lag:int64, lag_band:object, r_over_atr:float64, age_old_refused:bool, age_abs206_refused:bool, win_refused:bool, lag7_15_refused:bool, ratr_refused:bool, grid_cell:object` + collar and as-of columns;
`g_gate_rows.parquet` (5 × 32; `f7e4b5557f11aacb`); `g_age_crosstab.parquet` (25 × 20; `f35db296c0aa6683`).

---------------------------------------------------------------------------------------------------------------
## 2 · CONTRACT-vs-DISK

**C-1 · "re-pin its registry files" (:13).** Q2 names three files (REGISTRATIONS.json, REGISTRY_CHECK.json, PROGRESS.json). The disk pins the
contract sha in a fourth registry file the scorer checks (`REGISTRY_PIN.json contract_sha256`), in five typed script constants
(§1.4), and the sha of REGISTRATIONS.json itself is typed in three more scripts (`tierc11_score.py:224`, `tierc11_stage_g.py:170`,
`tierc11_stage_t_brk.py:141`). REGISTRATIONS.json is **write-once** (`tierc11_registrations.py:244-245`); it has no refile path. The
contract does not say which of these move.

**C-2 · "stamp TC11 BUILT" (:13).** The queue convention's stamp names the build document under `exchange/reports/`. TC11's document is
not there: it is still `research_outputs/tierc11/BUILD_DRAFT.md`, and only the operator's close acts move it. A stamp written today can
truthfully name only commits (`6f34939` and the nine before it), or a path that does not exist yet. And every exemplar stamp sits near
the TOP of its file — the position that would break TC11's line-pinned registrations and the 12 line-cites of TC11's staged ledger
append, which TC11's own close acts re-verify at step 0 (F-LAR11, "as the sources stand NOW").

**C-3 · "RULINGS ENACTED AS DEFAULTS (TC11 §11 …)" names Q1/Q2, Q4, Q6, Q8, Q9 (:12-16). Q3, Q5, Q7 are silent.**
- Q5 (re-root the forward ledger so it can refresh) is enacted in fact by Stage D (a new corridor) and Stage L ("all four books … re-ridden on the bars since 2026-09-21T16:00Z"), but not by name.
- Q7 (the X lane vendors the pre-AM-1 env shim; align or keep apart) becomes live the moment TC12 imports both TC11's env (`scripts/tierc11_env.py`, sha `1526093b…`) and X's value-area code (which ran under `X:…/vendor/tierc11_env@086d66da.py`).
- Q3 (slippage in the toll of record) stays open; the contract keeps the twin ("TWINS on every row: all-taker · charter slippage", :102).

**C-4 · "each VETO by name" (:12).** Veto tokens exist for Q1/Q2 (`"tc11-stamp"`) and Q4 (`"1w"`). Q6, Q8 and Q9 carry no token in the VETOES line (:135-137).

**C-5 · "SAIL remains HELD (operator 2026-09-24)" (:3-4).** No ruling document of that date names SAIL. The disk carries the hold as the operator's 2026-09-21 Q6 word (TC10 contract :2-3, :143) and as the CLOSE clause of the TC11 contract ratified 2026-09-24 (`:99`).

**C-6 · "the Q-R3 law licenses exactly {VA-4h taker, VA-1d taker, VA-1h maker}; nothing else may trade a range" (:40-41).**
- The ruling itself (LEDGER.md:834) speaks of a contract being DRAFTED only if both legs pass; it names no detector.
- TC11's contract text (`:16-18`) closes "**that lens** for range trading in this and every later tier unless the toll model changes"; TC11's verdict is FAIL at 4h and 1d on the pivot detector. The per-detector licence is X's reading (LX-X3.14: "licenses only that lens × detector × toll"), filed Tier-E. TC12's ratified contract adopts X's reading; nothing on disk records that TC11's lens-level closure was thereby narrowed to the pivot detector.
- **1d taker PASSES on the holdout row only**; the same panel's ALL and tuning rows read False (−0.212326, −0.347871). X's own law string says a form "scored on the holdout must read the holdout row" and the row gates "FOR ERA = 'holdout' ONLY". The contract's Tier-E 1d cells sit beside a full-corridor registration (P-SFP-VA-1, "full corridor", :69).
- The 4h taker PASS holds on ALL, tuning and holdout; the 1h maker PASS holds on all three.
- "1h maker PASS" and "1h taker FAIL" are one row on disk whose `lens_word` is the compound string "FAIL — maker twin PASSES (…)", not two words.
- The 1h maker PASS is computed at 4.0 bps round trip, a value TC11 files as an ASSUMPTION (§1.11).

**C-7 · P-SFP-VA-1 and P-SCALP-3 carry no in-sample label in the contract (:69-75, :83-106); P-ADM-1 ("pre_seen"), P-BRD-1 and P-DIR-1 ("direction informed by …") do.** X's standing line (LEANS_X.md:2468-2470, and the `ledger_line` column of every feasibility row) says any later registration drawn from X3's events and feasibility "carries pre_seen for bars ≤ 2026-09-25T00:00Z". The contract's CLOSE asks for "the five rows with their labels" and "in-sample labels carried" (:126-130).

**C-8 · "`data/fee_schedule.json` must carry maker_bps_side per venue; if absent, add it" (:21-23).** No `data/fee_schedule.json` exists at the repo root. The files are `research_outputs/tierc10/data/fee_schedule.json` (23,925 B, sha256 `3a18b84e…`, git-ignored) and `research_outputs/tierc11/data/fee_schedule.json` (tracked, `6febe170…`). The TC11 file has `maker_bps_per_side` (not `maker_bps_side`), keyed per ASSET (not per venue), value 2.0, marked ASSUMPTION. TC10's F-LAR reads TC10's copy at its close (`tierc10_close_ledger_append_root.py:94, :168`); X's ferry points at TC11's copy by sha (`tc11x_ferry.py:223`).

**C-9 · "FERRY … → exchange/rows/tierc12/ as CSV, 2 MB cap; files that would push the box past WARN are held and LISTED for ATHENA" (:111-112).** `exchange/README.md:21` caps every file under `exchange/**` at 1,048,576 B and `:20` says text only; X filed that conflict for ATHENA (Q-A1, LX-X6.8) and it is unruled. After X's close the box is forecast 2,244 B under WARN (§1.9), so "would push the box past WARN" is true of nearly every TC12 row file — and of TC12's own report.

**C-10 · "Source of record = TC11-X's filed implementation (research_outputs/tierc11x/va/, scripts, shas printed)" (:27-28).** In MAIN, `research_outputs/tierc11x/` and `scripts/tc11x_*.py` do not exist (X is unmerged). In the X worktree the `va/*.parquet` files are git-ignored (`X:research_outputs/tierc11x/.gitignore`: `*.parquet`, `_det_*/`) — they are in no commit and will not arrive in MAIN even after the merge. Tracked under `va/`: only `FIXTURES_X3.txt`, `X3.md`, `build_manifest.json`.

**C-11 · "the VA vector at 1h, 4h, 12h, 1d, 1w" (:45-46) and "Lookback per lens = X's pin, read from its records" (:28).** X has no 1w value area (and no 5m). X's printed range-life row is "L 1h/4h/12h/1d 71/66/53/35" (X BUILD_DRAFT:379). There is no X pin to read for 1w.

**C-12 · "F-CTRL … Σ net_r 40.807566 at its pin" (:49).** `books/v6_campaigns.parquet` sums to 40.807566 (200 rows; read here). TC11's documents print both `40.807566` (BUILD_DRAFT:244) and `+40.807565` (BUILD_DRAFT:362, :5565, :5780). The contract's figure matches the parquet.

**C-13 · "F-LEDGER (append-only on the three existing books; the fourth re-hashes)" (:122).** The three existing books live in two files in two trees with two chain schemas: TC11's `M:research_outputs/tierc11/forward/FORWARD_LEDGER.{jsonl,md}` (v6, 9/12; chain keys `prev` / `line_sha256`) and X's `X:research_outputs/tierc11x/forward/FORWARD_LEDGER.{jsonl,md}` (the gated book; `prev_sha256` / `entry_sha256`) — X's AM-X9 (b) records the difference. TC11's staged append cites TC11's `FORWARD_LEDGER.md` at lines 5, 7 and 38.

**C-14 · "publish_exchange; STATE push; bright paths" (:130).** Read against LEANS L-F.4 and LX-C.5 these are things the acts script does and states; the executor has never been granted a push, and the SSH route has failed on every run since 2026-09-27.

**C-15 · "commit + PROGRESS.json per stage" (:5-6) against the 07:00 routine.** `publish()` reads the whole index and, on any staged non-exchange path, runs `git reset` and skips the publish.

---------------------------------------------------------------------------------------------------------------
## 3 · READINGS NEEDED (candidate leans; freeze before building)

**R-1 · "tc11-stamp": WHEN is the stamp made, and by whom?**
Options: (a) now, in-build; (b) as a step of TC12's own close acts, after TC10's, TC11's and X's blocks have landed; (c) not at all (the veto).
**Recommend (b).** Reasons: only after TC11's close can the stamp truthfully name `exchange/reports/BUILD_2026-09-24_TIERC11_EVENTS.md`; TC11's step 0 re-verifies 12 line-cites into that file and requires its own sources == HEAD; X's close ferry re-reads TC11's tree; Q6 already makes close acts the operator's keystrokes. During the build TC12 pins TC11's contract at `bb38e016…` throughout. The executor proves the act beforehand in a scratch clone outside both trees.

**R-2 · "tc11-stamp": WHERE in the file does the line go?**
Options: (a) under the RATIFIED block (the precedent position); (b) appended after line 103.
**Recommend (b).** It keeps lines 1..103 byte-identical, so the nine `text_lines` slices, nine contexts, nine payload shas and the chain head `6772568b…` do not move, and no «cite» into the contract shifts. README rule 6 asks only for "a line of its own".

**R-3 · "re-pin its registry files": WHICH bytes move?**
Options: (a) literal Q2 — the three named files only (leaves `REGISTRY_PIN.json` and the typed constants at the old sha, so TC11's scorer, score fixtures and close generator go RED/HALT on any re-run); (b) the registry set that keeps TC11's own verifier green — `REGISTRATIONS.json contract.sha256` (one leaf; chain untouched), `REGISTRY_PIN.json contract_sha256`, `REGISTRY_CHECK.json` (by the scorer's `--refile`), `PROGRESS.json` (`contract_of_record`, the STEP Q artifact sha, `registrations_of_record`, the moved artifact shas) + the typed constants `tierc11_registrations.py:24`, `tierc11_score.py:220, :224`, `tierc11_score_fixtures.py:263`, `tierc11_stage_g.py:170`, `tierc11_stage_t_brk.py:141`; everything else that quotes the old sha (data records, stage documents, the published build document, S5, TRACES, X's 30 records) declared HISTORICAL and listed; (c) no TC11 byte moves — a dated sibling record (the LEANS_AMENDMENTS precedent) names old sha → new sha with the invariance proof.
**Recommend (b), executed under R-1 (b), with (c)'s record written as well** (old → new for every moved sha, and the list of what was left historical). It is the smallest set under which "re-pin" is true of TC11's own checks. The orchestrator should know (b) edits six TC11 scripts and so moves their shas in TC11's manifests; if that is judged outside "no re-family of TC11 / frozen texts", fall back to (c) and say the stamp was not applied.

**R-4 · Rebuild order for R-3 (b)** (derived from the code; to be proven in the scratch clone before it is staged): 1 append the stamp → new contract sha · 2 `tierc11_registrations.py:24` · 3 the one `contract.sha256` leaf of REGISTRATIONS.json, asserted byte-equal to `build()`'s rendering → new file sha · 4 `REGISTRY_PIN.json` · 5 the remaining typed constants · 6 `tierc11_score.py --refile`, asserting `SCORES.json`, `FAMILY.json`, `BASE_IDENT.json` byte-identical before and after (else HALT: that is Q1) · 7 `--refile-transcript` for the score, stage_g, stage_t_brk (and stage_a manifest) suites · 8 PROGRESS.json · 9 the whole TC11 roll re-passes (its last sweep: "17 suites, 134 fixtures GREEN") · 10 the historical list. **Recommend freezing this order as the lean and filing the proof transcript.**

**R-5 · Q1 "keep SCORES.json leaves": the action.**
**Recommend:** no byte of `scores/SCORES.json` moves in TC12; its sha `2c1a664a…` is pinned at R0 and re-asserted at close and inside R-4 step 6; the ruling is recorded in TC12's ledger append. A scorer `--refile` is never run except inside R-4, behind that assertion.

**R-6 · Q4 "1w": the action.**
**Recommend:** 1w is closed for range trading — no 1w cell in any registered or Tier-E range trade (swing failure, breakout-retest, take-profit venue), and no re-measure is ordered. The 1w entry of the V5 vector is a captured-not-consulted stamp. Where its lookback comes from is the value-area unit's reading (C-11); this unit only records that X supplies none.

**R-7 · Q6: the executor's boundary.**
**Recommend (reuse L-F.4 + LX-C.5):** the executor writes `research_outputs/tierc12/close/close_acts.sh`, never runs it, never pushes, never calls `publish()`, never merges; a fixture runs `bash -n` and step 0 against scratch repositories only (X's F-CLOSE-SCRIPT). "STATE push" = a `⟦STAMP AT CLOSE⟧` in the report plus the script's printed result.

**R-8 · Q8: the action.**
**Recommend:** neither post-hoc candidate (the relay in late windows; the memory-line first-hold twin) is registered or re-run. P-ADM-1 carries `pre_seen`, citing `STAGE_G.md:197` (n 110, mean +0.5146, ΣR +56.6072; refused 90, ΣR −15.7997) by path, line and sha; its verdict cell uses TC11's label form "<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (<hazard>)" (LEANS.md:125-127).

**R-9 · Q9: what is carried forward.**
**Recommend:** (i) cross-lens visibility in TC12 is L-W.1's `≤` — a lower-lens bar is visible at a higher-lens decision instant iff its close ≤ that instant — with a sabotage leg reading `>` that must FAIL; (ii) scorer Tier-E rows print `would_read_ci_only` under the collar and no verdict word (L-1.4); descriptive stage tables print no interval (L-W.4's scope). Both are the as-built TC11 behaviour.

**R-10 · Q3, Q5, Q7 (not enacted by name).**
**Recommend:** Q3 — stays open; the charter-slippage twin beside every row, never instead of the toll (AM-7's law). Q5 — read as enacted by Stages D and L, said so in LEANS and in the ledger append. Q7 — keep the lanes apart: TC12 runs ONE env of its own; X's value-area code is vendored at the certified tip with its sha, and the shim difference (`086d66da…` vs `1526093b…`) is printed as a disclosure. None of the three is silently decided; each is listed for the operator.

**R-11 · The licence, and the era each form reads (C-6).**
Options for 1d cells: (a) the contract's words as written; (b) each form reads the feasibility row of its own scoring era.
**Recommend (b):** the mirror prints the three eras beside each licence; any 1d cell scored on the full corridor carries the ALL-era word (False) in its row and is Tier-E in any case; P-SFP-VA-1 (full corridor, 4h taker) reads PASS on ALL, tuning and holdout; P-SCALP-3 (holdout, 1h maker) reads the holdout row. This cannot flatter a result. TC11's lens-level closure is recorded as standing for the pivot detector ("no pivot-range trades").

**R-12 · F-VA-MIRROR "HALT if the mirror disagrees on any word".**
**Recommend:** the five words are five `(lens, toll)` cells of `va/feasibility.parquet` at `asset == "POOLED:CLASSIC5"`, `era == "holdout"`, `scale_kind == "va_regime"`, compared on `verdict_pass` (4h·taker True, 1d·taker True, 1h·maker True, 12h·taker False, 1h·taker False), with the file's sha asserted first. The 1h `lens_word` string is printed, not string-matched. The `va_lblock` twin and the 12h maker word are printed beside and decide nothing.

**R-13 · Labels on P-SFP-VA-1 and P-SCALP-3 (C-7).**
**Recommend:** both carry `pre_seen` for bars ≤ 2026-09-25T00:00Z, citing `LEANS_X.md:2468-2470`; "4 lenses × 2 tolls = 8 chances at a PASS" is printed on the row. Reuses a filed X pin; cannot flatter.

**R-14 · Where TC12 reads X from, and where X's material may live in MAIN (C-10).**
**Recommend:** read X only by absolute path in the X worktree (parquets) and by `git show 7b24f835…:<path>` (tracked text), each sha asserted against X's committed manifests; copy what the build depends on into TC12's own tree (`research_outputs/tierc12/vendor/…`, sha-manifested) at R0. **Never create `research_outputs/tierc11x/`, `scripts/tc11x_*.py`, `exchange/rows/tierc11/` or `exchange/rows/tierc11x/` in MAIN.**

**R-15 · TC12's bus rows: where and when (C-9).**
Options: (a) write `exchange/rows/tierc12/` in MAIN during the build; (b) stage the CSVs off-bus under `research_outputs/tierc12/ferry/` and make the ferry of record a close act (X's AM-X21), run after X's block has landed, pinned at the then-HEAD by sha, reserving TC12's own report and append first, with a forecast printed at build time.
**Recommend (b).** (a) is swept by the 07:00 routine and shrinks the box X's certified ferry will measure. Under (b) the honest forecast is "nearly all HELD FOR ATHENA", which the contract already provides for.

**R-16 · Caps.**
**Recommend:** report cap 1,000,000 B (TC11's reading, the stricter of the two on disk), the generator HALTing over it; row cap 2,000,000 B on the CSV alone, whole rows (X's `CAP_BYTES`); every constant read from `publish_exchange.py` by `ast`, never typed; the 1 MiB conflict re-filed for ATHENA, not decided.

**R-17 · Tier order for TC12's close.**
**Recommend:** step 0 refuses unless TC10's, TC11's and X's committed stamped appends each occur exactly once in the committed ledger, in that byte order (X's by-bytes law; a header grep cannot tell TC11 from TC11-X), X is merged, and the ledger == HEAD. X's script does not itself refuse a ledger that already carries a later tier, so the order is TC12's to keep.

**R-18 · TC12's own contract pin, so this question is not asked a fourth time.**
**Recommend:** TC12's registry pins the STEP Q bytes as a PREFIX — `sha256(first 12,209 B) == 861d6050…` and 137 lines — beside the whole-file sha, and every text slice is cut from that prefix. A BUILT line appended later then moves no pin. Commit subjects start `tierc12(`; none starts `tierc10` or `tierc11(` (those feed the other tiers' stamp counts).

**R-19 · The forward ledger's home (C-13).**
**Recommend:** TC12 appends to neither TC11's nor X's ledger file. Its own ledger under `research_outputs/tierc12/forward/` chains onto their heads by sha and proves "append-only" by re-deriving their existing lines. (Detail belongs to the ledger unit; the constraint comes from the pending close acts.)

**R-20 · The fee file (C-8).**
**Recommend:** TC12 writes its own `research_outputs/tierc12/data/fee_schedule.json`; TC10's and TC11's copies are never edited. TC11's `maker_bps_per_side 2.0` is printed as the pin X's verdict was computed at, beside whatever Stage D reads from the venue. (Detail belongs to the Stage D unit.)

**R-21 · The ledger append's header and required content.**
**Recommend:** `=== STATUS_APOLLO — <draft date> — TIER-C12 · THE VALUE-AREA TIER … ===` + `LANE      ` + `CLASS     ` under TC10's `check_format`; required cites: the "maker" ruling verbatim (`exchange/queue/2026-10-08_TC12_APOLLO.md:2-3`), SAIL HELD (`:3-4` and TC10 `:2-3`), the families (`:52`, `:64`, `:82`), each registration's text by line, X's standing pre_seen line, the enacted defaults (`:12-16`), and a tier line citing X's landed block.

---------------------------------------------------------------------------------------------------------------
## 4 · HAZARDS

**H-1 · The 07:00 routine (and Sunday 08:00 / 08:30) sweeps `exchange/**` and resets a dirty index.** Any file TC12 leaves under `exchange/` is committed as "exchange: auto-publish <date>". Any non-exchange path left STAGED at that minute makes `publish()` run `git reset` (the executor's staging is discarded, the worktree is untouched) and skip the publish. It also moves MAIN's HEAD once a day, so nothing may pin "main HEAD" except by recorded sha (X's AM-X17). Next fire 2026-10-09 10:00Z.

**H-2 · When the SSH route comes back, the first `publish()` pushes the whole branch** — every `tierc12(` commit made so far goes to origin without an operator act (this is how all ten `tierc11(` commits reached origin). Not preventable from inside the build; it must be stated, and the "N commits, M on a remote" stamp must be read from git after the push, never typed.

**H-3 · Three things in MAIN block X's close acts outright:** a path `research_outputs/tierc11x` (`close_acts.sh:185`); any change inside the X worktree other than `close/CERTIFIED_TIP`, including a `__pycache__` or a stray file (`:140-141`); a `tierc11x` tip that is not the certified sha (`:136`). Running X's scripts from the X worktree without `PYTHONDONTWRITEBYTECODE=1`, or with outputs defaulting into its `research_outputs/tierc11x/`, would do the second. `git stash` is shared across worktrees.

**H-4 · X's value-area records exist only as git-ignored files in the X worktree** (`va/*.parquet`, 9 files, ~77 MB). They are in no commit and on no remote; the `tierc11x` branch itself has no remote. Removing the worktree after the merge deletes the mirror's source. Copy and sha-pin at R0.

**H-5 · Line-number cites are live tripwires until the three closes land.** Do not edit: `LEDGER.md` at or above line 836 (TC10 cites 829, 834-836); `exchange/status/LEDGER_APOLLO.md` (TC10 and X cite 2422-2423; all three scripts need it == HEAD); `exchange/queue/2026-09-24_TC11_APOLLO.md` lines 1-103 (12 cites + the registry slices); `research_outputs/tierc11/scores/SCORES.json` (9 cites); `research_outputs/tierc11/forward/FORWARD_LEDGER.md` (3 cites); `scores/FAMILY.json`, `stage_r/STAGE_R.md`, `books/FIXTURES_BOOKS.txt`; `research_outputs/tierc10/LEDGER_APOLLO_APPEND.md` (TC11 cites 250-254); TC11's 14 SOURCES (`close_acts.sh:41`), which must stay == HEAD.

**H-6 · TC10's residue.** `research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt` is modified and uncommitted by design of TC10's flow. A `git add -A`, `git commit -a`, `git checkout -- .` or `git stash` in MAIN would capture or destroy it. Stage tierc12 paths by name only. TC10's script still lacks `-f` at `:103`; that is the operator's patch.

**H-7 · A re-pin made before TC11's and X's closes** changes what X's ferry of record reads (`PROGRESS.json`, the TC11 tree), makes TC11's published build document describe a state that no longer holds (`FN-M-QUEUE-STAMP`), and makes TC11's generator HALT on any re-run (`tierc11_close.py:608-611` and its `^BUILT` check). Whether X's close would stay green was not run here; treat it as unproven.

**H-8 · Commit subjects.** TC10's stamp counts subjects starting `tierc10`; TC11's counts `tierc11(`; X's counts `tc11x(`. A TC12 commit titled, say, `tierc11(BUILT-STAMP)` made before those closes would be counted as one of theirs.

**H-9 · Box order.** X's ferry fills the box to within ~2 kB of WARN on the box it measures at ITS close. Rows committed to MAIN by TC12 before that shrink X's written set (its forecast already flips `sfp/X2_trades_1h` to HELD). After it, TC12's report alone crosses WARN (publish prints WARNING, still publishes; REFUSE only above 11,200,000 B). `NAIAD_ALLOW_OVERSIZE_PUBLISH` is never set.

**H-10 · A flattering read of the licence.** The 1d value-area PASS is a holdout-only word (ALL −0.212326, tuning −0.347871); the 1h maker PASS rests on a 2.0 bps-per-side ASSUMPTION; P-SFP-VA-1's and P-SCALP-3's outcomes were already printed by X3's two-trades table on bars ≤ 2026-09-25T00:00Z. Each must appear on the row it qualifies.

**H-11 · Determinism.** Any fixture that reads the live MAIN HEAD, the live ledger tail or the live box size changes with the daily commit; pin by sha and print a live-HEAD line with no pass condition (AM-X17's pattern). `.gitignore` line numbers are cited by other lanes (`:44`, `:263`, `:287`): append at the end only, or use a nested `.gitignore` as X did.

**H-12 · TC11's write-once and no-clobber laws.** `tierc11_registrations.py --file` HALTs on an existing filing; the scorer without `--refile` writes `<stem>_rerun` files beside the record (new untracked files under `research_outputs/tierc11/scores/`). An exploratory scorer run in MAIN leaves debris in TC11's tree; use `--dry-run` or `--out-dir` outside the repo.

---------------------------------------------------------------------------------------------------------------
## 5 · REUSE PLAN

**Import / call unchanged (read-only):**
- `scripts/publish_exchange.py` — constants by `ast.literal_eval` only (X's `tc11x_ferry.publish_constants(path)` at `X:scripts/tc11x_ferry.py:626` is the pattern); `budget()` semantics mirrored (`level()` `:644`, `warn_line()` `:655`). `publish()` itself is called only inside the operator's acts script, by the §3.4 invocation.
- `scripts/tierc10_close_ledger_append_root.py`: `SEP` (`:84`), `check_format` (`:554`), `check_cites` (`:570`); `scripts/tierc10_close_close_ledger_append.py`: `cite_of` (`:616`), `render_quote` (`:626`), `parse_quotes` (`:978`), `verify_quote` (`:1012`). TC11 exec's TC10's source for the format law; X copies it (never imports). TC10's `REQUIRED` list (`:581-584`) and `check_required` (`:587`) are TC10-specific — not reusable.

**Mirror (same shape, new file under `scripts/tierc12_*.py`):**
- The registry: TC11's `REGISTRATIONS.json` + `REGISTRY_PIN.json` law (payload sha, chain, write-once filer) with X's per-family fields (`X:…/registrations/REGISTRY_PIN_X.json`: `families[{family, m, q, bar}]`, `leans_bound_prefix`), plus R-18's prefix pin.
- The scorer's no-clobber `write_outputs(files, out, refile)` and `--dry-run` law (`tierc11_score.py:2648`, `:186-188`).
- The close generator: `scripts/tierc11_close.py` — `build_findings` (`:828`), `render_append` (`:1199`), `render_draft` (`:1523`), `render_box_md` (`:2537`), `render_acts` (`:2587`); fixtures `scripts/tierc11_close_fixtures.py` (F-S0-NINE, F-NUM, F-FEAS-0, F-LAR11, F-BOXCOST, F-FNF, F-CLOSE-ORDER, F-DET).
- The acts script: X's is the fuller template — by-bytes tier check (`close_acts.sh:143-178`), the ferry of record as step 1 with `ferry_restore` undo (`:77-100`), stamps through `--stamp` + `--stamped`, `git add -f` for the residue, the ledger tail checked byte for byte (`:298-302`). TC12 adds: X's block as a third required tier; no merge step; and, if R-1 (b) is taken, the TC11 stamp-and-re-pin step before `publish()`.
- The ferry: `X:scripts/tc11x_ferry.py` — `flat_name(rel)` (`:481`), `identity_class(df, asset_cols, book_axes)` (`:495`), `to_csv_bytes(df)` (`:543`), `cut(csv, n_rows, cap)` (`:566`), `project(order, base, C)` (`:666`), `plan_holds(...)` (`:753`), `box_now(C, root)` (`:853`), the reader law for F-ROWS RT (`:185-190`). Vendor at the certified tip; do not import from the X worktree path.

**Newly written:**
- `research_outputs/tierc12/close/close_acts.sh` and its scratch-repo fixture.
- The TC11 stamp-and-re-pin script with its invariance proof (lines 1..103 unchanged → slices, payloads, chain head unchanged; `SCORES.json` byte-identical) and the old → new sha record.
- The R0 census of the close state: the facts of §1.7-1.8 re-read at build start (HEAD, origin, the three stamps pending, the two dirty files, the box), written into `research_outputs/tierc12/PROGRESS.json`.
- TC12's ledger append (`research_outputs/tierc12/LEDGER_APOLLO_APPEND.md`) with the content of R-21.
- The vendor manifest for everything read from X (path, sha, bytes, whether tracked at `7b24f835…` or disk-only).

**Never touched by TC12's build:** anything under `research_outputs/tierc10/`, `research_outputs/tierc11/`, the X worktree, `exchange/status/LEDGER_APOLLO.md`, `LEDGER.md`, `exchange/queue/2026-09-2*`, `scripts/tierc10_*`, `scripts/tierc11_*`, `scripts/publish_exchange.py`, `exchange/status/CONVENTIONS.md`.
