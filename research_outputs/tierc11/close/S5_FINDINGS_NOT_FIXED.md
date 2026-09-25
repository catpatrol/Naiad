# TIER-C11 · CLOSE · FINDINGS — REPORTED, NOT FIXED

> **REPORT-ONLY · Tier-E — findings harvested verbatim, measured at build time, or leaned by this CLOSE; nothing here is scored, no verdict is read to choose anything, and nothing is fixed.**
>
> Every finding's status is 'REPORTED, NOT FIXED': it records what THIS build did (report, never fix); it does not claim the item is still open.

- **Contract of record:** `exchange/queue/2026-09-24_TC11_APOLLO.md` sha256 `bb38e016a8f3e55ca3bcc09fec53ba6b8dc40accb60d054f8163d033a898f835`
- **Clause:** line 98 — `crossed · the scalper's twins · adds head-to-head · findings-not-fixed · BOX-COST · LEDGER append`
- **AS-OF OF RECORD:** 2026-09-25T00:00:00Z
- **Ranking law:** operator-owned first, then executor-owned; within each owner the order of harvest: the trading lens's FNF list in its own rank, then the statistics, fidelity, causality and reproducibility candidates, the TC11-FIX verifier's residuals, the stage reports' own findings, TC10's open question and the SAIL hold, then the measured items and this CLOSE's leans.
- **Dedup law:** a fact reported by several sources is ONE finding: the first source in ranking order is the primary and keeps its verbatim text; every other source is listed under also_reported_by with its own verbatim text.
- **Built by:** `scripts/tierc11_close.py`; certified by `scripts/tierc11_close_fixtures.py` F-FNF (json == md; class, owner and source on every finding; ids unique; every harvested text re-extracted from its locator).

## 0 · Inputs, read-only

| input | bytes | sha256 |
|---|---:|---|
| `exchange/queue/2026-09-22_OR2_oracle_rulings_ARGUS.md` | 14220 | `6f355354a8f523e243da9dd56d0c66d7d425e605459f41cb66b6ddc3b4a3381c` |
| `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` | 9441 | `8a0bf279bcab0f27161a7d965535445807f4e713e77d045b0ba124bc7f803c7a` |
| `exchange/queue/2026-09-24_TC11_APOLLO.md` | 8442 | `bb38e016a8f3e55ca3bcc09fec53ba6b8dc40accb60d054f8163d033a898f835` |
| `exchange/status/LEDGER_APOLLO.md` | 174090 | `cd6ad43a0fe4890635e6d7098d29ae52d4af1268be4466740823701014222d2c` |
| `research_outputs/tierc10/LEDGER_APOLLO_APPEND.md` | 14925 | `1288b59bae687f6a56f31cd75d958dc53400af78f4c7ff77ede3965972d5021e` |
| `research_outputs/tierc10/close/close_acts.sh` | 6823 | `3f5c868ba089965ae3dad120c9293b9375dde992df5043dcfecea2b02e4440f8` |
| `research_outputs/tierc11/LEANS.md` | 40646 | `655e1605165e7a66c67f544e5cda421b46aa0b6fcd4cb97a6ad19654479f294f` |
| `research_outputs/tierc11/PROGRESS.json` | 101683 | `dbcc08cf60a9dbb5827c65f3728857fcab12df50aeefee7667ba3dbfc205c4fe` |
| `research_outputs/tierc11/books/FIXTURES_BOOKS.txt` | 20970 | `336a2163e9bd8df8fd40d1fdb6949a0251529c0f34a5c025e4ff6b3d31b45c10` |
| `research_outputs/tierc11/close/COMPUTE_LEDGER.json` | 4342 | `b5f0b2495672e0ffac95c710314cd04924ea3de8fb1540730a9eaee5f09b2d8f` |
| `research_outputs/tierc11/close/TC11_FIX_VERIFY.json` | 26595 | `96a1b6e579bf34cd76872da6f43eafe8c42c84906802a901c53836faca2740dd` |
| `research_outputs/tierc11/forward/FORWARD_LEDGER.jsonl` | 3442 | `e53328add9e71f1c6198f724a131565a2a10ad2ad1600c36a74c6676f7ada288` |
| `research_outputs/tierc11/forward/FORWARD_LEDGER.md` | 2981 | `52e839001f7ad6f1e13533a6d6745488dc587d11db25c3bfe6b0de66823413ec` |
| `research_outputs/tierc11/registrations/REGISTRATIONS.json` | 34228 | `648834bf30e20e92713bddef2374ddef1aae843f4d8ba152fc50166c8cc6f1ee` |
| `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | 95099 | `ec8849d36d916ecc42434719523986f5e67b4bc08aa463f63f043b0c6d199dae` |
| `research_outputs/tierc11/review/attest/causality.json` | 586 | `c1f1135743e95e5c28dc87902c202627b9207dcafce1e31fc748b877358690bc` |
| `research_outputs/tierc11/review/attest/fidelity.json` | 584 | `751de56bbc295d8696bd70d1cb6cd63b070a5c32ff23d30c3ca8c8cf05e46184` |
| `research_outputs/tierc11/review/attest/fix-head.json` | 22775 | `b3e18835b67db4f4c38520139fd7f8c915c17e0ae43f1e4aaf8c40569e2e3021` |
| `research_outputs/tierc11/review/attest/reproducibility.json` | 598 | `640761f83404248dac309dc5237c8225f0f8039cd01607b8bab48d0fff4b6c8b` |
| `research_outputs/tierc11/review/attest/statistics.json` | 588 | `2f3d9af2b49bff134515cd490f1cf2bade167cc50ea3b7afe20cf7c14f68117c` |
| `research_outputs/tierc11/review/attest/trading.json` | 582 | `0b8ced3bc0b4c647a680db03ef2bd51222b5fb7b832130a63cc22947d1052490` |
| `research_outputs/tierc11/scores/FAMILY.json` | 3313 | `3fa36bd482eac4de729b0e1ff2a66e7becbc30f2646ce16fc0df8fc369b2fd73` |
| `research_outputs/tierc11/scores/REGISTRY_CHECK.json` | 6880 | `aea83bf10b5bbe62ff6c0af542870cd60f5ad8773b6bb61fab45ea465d8f8ed0` |
| `research_outputs/tierc11/scores/SCORES.json` | 236946 | `2c1a664a27abfc320355dcb89b2eff8a7f7637ddc26843e72ab3baf30cbef856` |
| `research_outputs/tierc11/stage_a/STAGE_A.md` | 124369 | `8528fbe89bc9b8d3ea460f14be325407c7ba223fedf90afb6cfea0219ae6a70f` |
| `research_outputs/tierc11/stage_h/STAGE_H.md` | 122701 | `a79b4f0e972d7c11edd55d896f0f409910b8a84cedd4f58aba4241e66e2f06be` |
| `research_outputs/tierc11/stage_r/R2_LENS_VERDICTS.json` | 7185 | `82cc3ec6ddd588c9fbd8402def471438a0c931590606b9a2a6cc3a97572f3087` |
| `research_outputs/tierc11/stage_r/R5_CHOP.md` | 21172 | `601b932ae452aed921a938919317a3d8bb6ed43dda2efff7fc935212081f4f16` |
| `research_outputs/tierc11/stage_r/STAGE_R.md` | 753284 | `b664479f91c9041cc9b70965e8d8c0b1efeab0180c7c1e1fa2c3932d160a2af0` |
| `research_outputs/tierc11/stage_r4/STAGE_R4.md` | 776776 | `cc2f8a6d251cbc800a00264a9e34f4f5c136f36803ea599dec2a246ac37aa6d9` |
| `research_outputs/tierc11/stage_s/STAGE_S.md` | 36694 | `1eca265b18bfff278441ce340f255c31a007b1e18aea742e60c96713a5454163` |
| `research_outputs/tierc11/stage_t_brk/STAGE_T_BRK.md` | 1902042 | `c73b0c74bfe5e8910232422bb085b40c81e73f464c20d64dc5c295f9afb9bb30` |
| `research_outputs/tierc11/stage_t_relay/STAGE_T_RELAY.md` | 107321 | `70a9803cec476427abd040be5fda6a714176202c0889fcff5a0033a08fedd93e` |
| `research_outputs/tierc11/stage_w/STAGE_W.md` | 80923 | `48816cb2ab56e6a52f6950f35359a2a7edaa2a1a54c80315b594249affee9d4e` |
| `scripts/publish_exchange.py` | 44358 | `15eec3d0bf0420200d94fc3087e4868a59eecb5cdb1fc21e01b8c80daae8a65b` |

## 1 · Counts and index

| class | operator | executor | total |
|---|---:|---:|---:|
| HARVESTED | 30 | 24 | 54 |
| MEASURED | 6 | 1 | 7 |
| LEAN | 0 | 11 | 11 |
| all | 36 | 36 | 72 |

| rank | id | class | owner | source | locator |
|---:|---|---|---|---|---|
| 1 | `FN-TRD-01` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 1 under `## Findings-not-fixed for the build doc (ranked)` |
| 2 | `FN-TRD-02` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 2 under `## Findings-not-fixed for the build doc (ranked)` |
| 3 | `FN-TRD-03` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 3 under `## Findings-not-fixed for the build doc (ranked)` |
| 4 | `FN-TRD-04` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 4 under `## Findings-not-fixed for the build doc (ranked)` |
| 5 | `FN-TRD-05` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 5 under `## Findings-not-fixed for the build doc (ranked)` |
| 6 | `FN-TRD-06` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 6 under `## Findings-not-fixed for the build doc (ranked)` |
| 7 | `FN-TRD-07` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 7 under `## Findings-not-fixed for the build doc (ranked)` |
| 8 | `FN-TRD-08` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 8 under `## Findings-not-fixed for the build doc (ranked)` |
| 9 | `FN-TRD-09` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 9 under `## Findings-not-fixed for the build doc (ranked)` |
| 10 | `FN-TRD-10` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 10 under `## Findings-not-fixed for the build doc (ranked)` |
| 11 | `FN-TRD-11` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 11 under `## Findings-not-fixed for the build doc (ranked)` |
| 12 | `FN-TRD-12` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 12 under `## Findings-not-fixed for the build doc (ranked)` |
| 13 | `FN-TRD-14` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 14 under `## Findings-not-fixed for the build doc (ranked)` |
| 14 | `FN-TRD-15` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 15 under `## Findings-not-fixed for the build doc (ranked)` |
| 15 | `FN-TRD-16` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 16 under `## Findings-not-fixed for the build doc (ranked)` |
| 16 | `FN-TRD-17` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 17 under `## Findings-not-fixed for the build doc (ranked)` |
| 17 | `FN-STA-2` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=statistics].report` · numbered item 2 under `## Findings-not-fixed candidates for the build doc (facts, not defects)` |
| 18 | `FN-STA-8` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=statistics].report` · numbered item 8 under `## Findings-not-fixed candidates for the build doc (facts, not defects)` |
| 19 | `FN-FID-1` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=fidelity].report` · bold-bullet item 1 under `## Findings-not-fixed candidates (facts for the operator, not defects)` |
| 20 | `FN-FID-7` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=fidelity].report` · bold-bullet item 7 under `## Findings-not-fixed candidates (facts for the operator, not defects)` |
| 21 | `FN-FID-10` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=fidelity].report` · bold-bullet item 10 under `## Findings-not-fixed candidates (facts for the operator, not defects)` |
| 22 | `FN-FID-11` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=fidelity].report` · bold-bullet item 11 under `## Findings-not-fixed candidates (facts for the operator, not defects)` |
| 23 | `FN-FID-12` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=fidelity].report` · bold-bullet item 12 under `## Findings-not-fixed candidates (facts for the operator, not defects)` |
| 24 | `FN-CAU-2` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=causality].report` · numbered item 2 under `### Findings-not-fixed candidates for the build doc (facts, not defects)` |
| 25 | `FN-CAU-6` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=causality].report` · numbered item 6 under `### Findings-not-fixed candidates for the build doc (facts, not defects)` |
| 26 | `FN-REP-3` | HARVESTED | operator | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=reproducibility].report` · bullet item 3 under `## Findings-not-fixed candidates for the build doc` |
| 27 | `FN-STG-R-3` | HARVESTED | operator | `research_outputs/tierc11/stage_r/STAGE_R.md` | bullet item 3 under `## Findings not fixed (for the operator) [L-R.4]` |
| 28 | `FN-STG-A-8` | HARVESTED | operator | `research_outputs/tierc11/stage_a/STAGE_A.md` | bullet item 10 under `## 10 · Findings (derived in-build; findings-not-fixed for the build doc)` |
| 29 | `FN-H-TC10-Q2` | HARVESTED | operator | `research_outputs/tierc11/LEANS.md` | the line starting `- TC10's operator question Q2` |
| 30 | `FN-H-SAIL` | HARVESTED | operator | `exchange/queue/2026-09-24_TC11_APOLLO.md` | the line starting `(m=9; SAIL still HELD` |
| 31 | `FN-M-SCORES-LEAVES` | MEASURED | operator | `research_outputs/tierc11/scores/SCORES.json` | git show <reviewed>:SCORES.json vs HEAD:SCORES.json, leaf by leaf |
| 32 | `FN-M-TC11X-SHIM` | MEASURED | operator | `git:df0b5c4` | git log -1 df0b5c4 (the pinned commit whose subject names the vendored shim) |
| 33 | `FN-M-QUEUE-STAMP` | MEASURED | operator | `exchange/queue/2026-09-24_TC11_APOLLO.md` | grep ^BUILT; the three pins compared |
| 34 | `FN-M-TC10-FIRST` | MEASURED | operator | `exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md` | path exists; ledger header grep |
| 35 | `FN-M-TC10-ACTS-IGNORED` | MEASURED | operator | `research_outputs/tierc10/close/close_acts.sh` | the bare 'git add' line; git check-ignore -v --no-index on each path it adds |
| 36 | `FN-M-EXCHANGE-SWEEP` | MEASURED | operator | `exchange/` | git diff --name-only -- exchange |
| 37 | `FN-TRD-13` | HARVESTED | executor | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=trading].report` · fnf item 13 under `## Findings-not-fixed for the build doc (ranked)` |
| 38 | `FN-CAU-1` | HARVESTED | executor | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=causality].report` · numbered item 1 under `### Findings-not-fixed candidates for the build doc (facts, not defects)` |
| 39 | `FN-CAU-3` | HARVESTED | executor | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=causality].report` · numbered item 3 under `### Findings-not-fixed candidates for the build doc (facts, not defects)` |
| 40 | `FN-CAU-4` | HARVESTED | executor | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=causality].report` · numbered item 4 under `### Findings-not-fixed candidates for the build doc (facts, not defects)` |
| 41 | `FN-CAU-5` | HARVESTED | executor | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=causality].report` · numbered item 5 under `### Findings-not-fixed candidates for the build doc (facts, not defects)` |
| 42 | `FN-REP-2` | HARVESTED | executor | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=reproducibility].report` · bullet item 2 under `## Findings-not-fixed candidates for the build doc` |
| 43 | `FN-REP-5` | HARVESTED | executor | `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` | `result.reviews[lens=reproducibility].report` · bullet item 5 under `## Findings-not-fixed candidates for the build doc` |
| 44 | `FN-FIX-A` | HARVESTED | executor | `research_outputs/tierc11/close/TC11_FIX_VERIFY.json` | `verify` · bold-bullet item 1 under `## 6. Remaining defects` |
| 45 | `FN-FIX-B` | HARVESTED | executor | `research_outputs/tierc11/close/TC11_FIX_VERIFY.json` | `verify` · bold-bullet item 2 under `## 6. Remaining defects` |
| 46 | `FN-FIX-C` | HARVESTED | executor | `research_outputs/tierc11/close/TC11_FIX_VERIFY.json` | `verify` · bold-bullet item 3 under `## 6. Remaining defects` |
| 47 | `FN-FIX-D` | HARVESTED | executor | `research_outputs/tierc11/close/TC11_FIX_VERIFY.json` | `verify` · bold-bullet item 4 under `## 6. Remaining defects` |
| 48 | `FN-FIX-E` | HARVESTED | executor | `research_outputs/tierc11/close/TC11_FIX_VERIFY.json` | `verify` · bold-bullet item 5 under `## 6. Remaining defects` |
| 49 | `FN-FIX-F` | HARVESTED | executor | `research_outputs/tierc11/close/TC11_FIX_VERIFY.json` | `verify` · bold-bullet item 6 under `## 6. Remaining defects` |
| 50 | `FN-STG-R-2` | HARVESTED | executor | `research_outputs/tierc11/stage_r/STAGE_R.md` | bullet item 2 under `## Findings not fixed (for the operator) [L-R.4]` |
| 51 | `FN-STG-TB-2` | HARVESTED | executor | `research_outputs/tierc11/stage_t_brk/STAGE_T_BRK.md` | bullet item 2 under `## 10 · Findings (disclosures, not fixed; no rule was changed after a number was seen)` |
| 52 | `FN-STG-TB-4` | HARVESTED | executor | `research_outputs/tierc11/stage_t_brk/STAGE_T_BRK.md` | bullet item 4 under `## 10 · Findings (disclosures, not fixed; no rule was changed after a number was seen)` |
| 53 | `FN-STG-TB-5` | HARVESTED | executor | `research_outputs/tierc11/stage_t_brk/STAGE_T_BRK.md` | bullet item 5 under `## 10 · Findings (disclosures, not fixed; no rule was changed after a number was seen)` |
| 54 | `FN-STG-TB-7` | HARVESTED | executor | `research_outputs/tierc11/stage_t_brk/STAGE_T_BRK.md` | bullet item 7 under `## 10 · Findings (disclosures, not fixed; no rule was changed after a number was seen)` |
| 55 | `FN-STG-A-2` | HARVESTED | executor | `research_outputs/tierc11/stage_a/STAGE_A.md` | bullet item 2 under `## 10 · Findings (derived in-build; findings-not-fixed for the build doc)` |
| 56 | `FN-STG-A-4` | HARVESTED | executor | `research_outputs/tierc11/stage_a/STAGE_A.md` | bullet item 5 under `## 10 · Findings (derived in-build; findings-not-fixed for the build doc)` |
| 57 | `FN-STG-A-6` | HARVESTED | executor | `research_outputs/tierc11/stage_a/STAGE_A.md` | bullet item 7 under `## 10 · Findings (derived in-build; findings-not-fixed for the build doc)` |
| 58 | `FN-STG-H-1` | HARVESTED | executor | `research_outputs/tierc11/stage_h/STAGE_H.md` | bullet item 1 under `## 9 · Findings (stage-intrinsic, derived from the tables above)` |
| 59 | `FN-STG-H-3` | HARVESTED | executor | `research_outputs/tierc11/stage_h/STAGE_H.md` | bullet item 3 under `## 9 · Findings (stage-intrinsic, derived from the tables above)` |
| 60 | `FN-STG-H-4` | HARVESTED | executor | `research_outputs/tierc11/stage_h/STAGE_H.md` | bullet item 4 under `## 9 · Findings (stage-intrinsic, derived from the tables above)` |
| 61 | `FN-M-ATTEST-UNTRACKED` | MEASURED | executor | `research_outputs/tierc11/review/attest/fix-head.json` | git ls-files --error-unmatch |
| 62 | `LEAN-CLOSE-1` | LEAN | executor | `scripts/tierc11_close.py` | LEANS_CLOSE |
| 63 | `LEAN-CLOSE-2` | LEAN | executor | `scripts/tierc11_close.py` | LEANS_CLOSE |
| 64 | `LEAN-CLOSE-3` | LEAN | executor | `scripts/tierc11_close.py` | LEANS_CLOSE |
| 65 | `LEAN-CLOSE-4` | LEAN | executor | `scripts/tierc11_close.py` | LEANS_CLOSE |
| 66 | `LEAN-CLOSE-5` | LEAN | executor | `scripts/tierc11_close.py` | LEANS_CLOSE |
| 67 | `LEAN-CLOSE-6` | LEAN | executor | `scripts/tierc11_close.py` | LEANS_CLOSE |
| 68 | `LEAN-CLOSE-7` | LEAN | executor | `scripts/tierc11_close.py` | LEANS_CLOSE |
| 69 | `LEAN-CLOSE-8` | LEAN | executor | `scripts/tierc11_close.py` | LEANS_CLOSE |
| 70 | `LEAN-CLOSE-9` | LEAN | executor | `scripts/tierc11_close.py` | LEANS_CLOSE |
| 71 | `LEAN-CLOSE-10` | LEAN | executor | `scripts/tierc11_close.py` | LEANS_CLOSE |
| 72 | `LEAN-CLOSE-11` | LEAN | executor | `scripts/tierc11_close.py` | LEANS_CLOSE |

## 2 · The findings, ranked — operator-owned first

#### FN-TRD-01

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 1 · the reviewer's class MEASURED
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 1 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-1 · MEASURED · operator.** One theme across five instruments: v6's losses sit in late entries into old trends.
- P-AGE-1's refused OLD band: n59, −22.66 R. P-WIN-1's lag ≥16: n63, −11.17 R.
- 32 campaigns are in both sets and carry −18.02 R. Inside lag <16 the age gate still separates them: OLD −0.17 vs not-OLD +0.52.
- The relay activates in exactly v6's 67 lag ≥7 windows plus 2 others; v6 made −13.13 R there.
- In the same 61 long-lag windows, 9/12 made +6.39 R where v6 made −9.06 R.
- Every W2 pre-entry cohort is essentially the lag ≥7 set: all 67 lag ≥7 campaigns have a pre-entry 1h cross, and the four event classes all read −0.17 to −0.20. The pre-entry tables measure lag, not the events.
- Within lag 1–6, the 21 campaigns with any pre-entry 1h cross made −0.062, against +0.496 for the 112 without one.
~~~

#### FN-TRD-02

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 2 · the reviewer's class MEASURED
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 2 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-2 · MEASURED · operator.** How robust P-AGE-1's SUPPORTED is.
- The two-sample difference is positive on every asset (+0.153 ZEC to +0.351 BTC). That is why p = 1/4001: it is the 5-cluster floor, not 1-in-4000 evidence.
- Tuning slice: +0.152, p 0.044, LOAO 1/5. Holdout slice: +0.320, p 0.00025.
- Refused cohort by era: tuning n42 at −0.304, holdout n17 at −0.581.
- The OLD band was positive in tuning on ETH (+0.030, n11) and ZEC (+0.384, n7), and in 2020 (+0.551, n10). It was negative every year from 2021 to 2026.
- On ZEC the gate forfeits +2.37 R in total (OLD mean +0.296, n8).
- The result is pre-seen and there are 0 new campaigns since the TC10 pin, so the forward ledger is the only confirmation path.
~~~

- also reported by: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=fidelity].report` · bold-bullet item 3 under `## Findings-not-fixed candidates (facts for the operator, not defects)`

~~~text
- **P-AGE-1 is the only SUPPORTED row, and it is a pre-seen re-score.** Zero campaigns entered after the TC10 pin, so the forward ledger has no fresh evidence yet. The refused cohort averages −0.384 R (n 59).
~~~

#### FN-TRD-03

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 3 · the reviewer's class MEASURED + HARVESTED
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 3 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-3 · MEASURED + HARVESTED · operator.** P-RELAY-1 is a different lane, not a better entry.
- In the 69 windows both traded: relay +93.71 R vs v6 −13.13 R.
- In 104 windows v6 never entered: relay −15.23 R.
- The relay structurally cannot act in the 131 lag 0–6 windows, where v6 made +53.94 R (Tier-E `miss_v6`: +0.412 [+0.149, +0.656], 5/5).
- The relay's ΣR of +78.48 is three ETH trades: +32.75 (2026-08-18), +28.55 (2020-07-21), +19.39 (2025-07-05). Without them it is −2.21 R. Dropping ETH in LOAO gives −0.254.
- Those winners had R of only 0.78–2.24% of price (rail-bound ATR in quiet tape). Summing per-trade % returns at equal notional, the relay made +70.8% vs v6's +152.1%.
- Candidate for a new registration on forward data: v6 on lag <7 plus the relay elsewhere. The arithmetic sum is about +132 R before position conflicts, and it is post hoc here.
~~~

- also reported by: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=statistics].report` · numbered item 1 under `## Findings-not-fixed candidates for the build doc (facts, not defects)`

~~~text
1. **P-RELAY-1: what a reader must be told.**
   - NOT SUPPORTED is correct. The +0.25 point is ETH alone: without ETH it is −0.254 [−0.594, +0.060].
   - The width of the CI is real disagreement between assets, not an artifact.
   - The relay trades 104 windows that v6 never entered; those average −0.146.
   - v6's campaigns in the 131 windows the relay missed average +0.412 (the miss column), against −0.190 for v6 in the windows the relay did take.
   - Comparing relay and v6 window by window instead (69 shared windows) gives +1.548 [−0.098, +3.108], p 0.076. This is not filed and is carried by BTC +2.04 and ETH +5.14 per window.
~~~

- also reported by: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=fidelity].report` · bold-bullet item 6 under `## Findings-not-fixed candidates (facts for the operator, not defects)`

~~~text
- **P-RELAY-1:** 104 of 173 relays are in windows v6 never entered. The median lead over v6's trigger is 166 1h bars (about 7 days). v6 campaigns in the missed windows average +0.41 R (n 131).
~~~

#### FN-TRD-04

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 4 · the reviewer's class LEAN
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 4 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-4 · LEAN · operator.** Why P-WARN-1 is flat.
- Any cohort selected on an adverse path before +1R must end lower, so the condition was near-certain to be met and carried little information.
- The warn exit marks at −0.498 R against a final −0.525 R, so holding instead of exiting is worth −0.027 R.
- The rule saved +7.74 R on 36 losers and forfeited −6.63 R on 6 winners.
- One trade (ETH 2021-08-28, Δ −2.10) is 1.89× the whole ΣΔ.
- Future conditional registrations should condition on the forward leg, not on the cohort's final R.
- The same survivorship bias explains C3 (+1.11 vs −0.88); its tuning-era forward leg is −0.003.
~~~

- also reported by: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=statistics].report` · numbered item 4 under `## Findings-not-fixed candidates for the build doc (facts, not defects)`

~~~text
4. **The P-WARN-1 condition was nearly guaranteed to be met.**
   - 74% of the cohort never reached +1R, against 48.5% of the whole book.
   - Campaigns that never reach +1R average −0.95 regardless of any cross; those without the cross average −1.02, worse than the cohort.
   - The rule itself adds +0.0056/campaign (total +1.12 R over 42 exits), and one trade's Δ is 1.89 times the total Δ.
~~~

#### FN-TRD-05

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 5 · the reviewer's class MEASURED
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 5 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-5 · MEASURED · operator.** The calibrated scale underperforms frozen 3.0.
- Calibration puts every CLASSIC5 pick at 1.5–2.25, giving roughly 2× the ranges of frozen 3.0.
- All four range-consuming registrations read better at frozen 3.0:

| registration | calibrated | frozen 3.0 |
|---|---|---|
| P-BRK-4H | +0.050 | +0.165 |
| P-ADD-BRK | −0.020 | +0.018 |
| P-ADD-SFP | −0.020 | −0.003 |
| P-TP-RNG | −0.020 | +0.024 |

- At 1h, R2 at frozen 3.0 in the holdout reads taker −0.0068 and maker +0.0888, which is a PASS (`R2_FEASIBILITY.md:568`, `:570`). The only reopening path for the scalper lives at frozen 3.0, which is not the verdict of record.
~~~

- also reported by: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=statistics].report` · numbered item 5 under `## Findings-not-fixed candidates for the build doc (facts, not defects)`

~~~text
5. **P-BRK-4H depends on the scale reading.**
   - The frozen-3.0 twin (Tier-E, fully causal, but it is the scale the selected TC10 cell used) reads +0.165 [+0.058, +0.278], p 1/4001.
   - The 17-asset view reads +0.117 [+0.021, +0.231] with LOAO 15/17. The holdout slice reads +0.223, p 0.088. The tuning slice reads −0.042.
   - The calibrated-scale reading (L-R.2) is what turns a strong twin into NOT SUPPORTED.
~~~

#### FN-TRD-06

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 6 · the reviewer's class MEASURED
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 6 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-6 · MEASURED · operator.** The holdout era is a trend regime, not just an out-of-sample slice. Every trend book is near flat in tuning and strongly positive in holdout:

| book | tuning | holdout |
|---|---|---|
| v6 | −0.011 | +0.547 |
| 9/12 | +0.178 | +1.028 |
| P-BRK-4H | −0.042 | +0.223 |
| relay | +0.317 | +0.719 |
~~~

#### FN-TRD-07

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 7 · the reviewer's class MEASURED
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 7 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-7 · MEASURED · operator.** v6 vs 9/12.
- v6 without its top trade: +15.75 R; without its top 3: −2.14 R. The single ZEC trade of 2026-05-01 (+25.06 R) is 61% of the book.
- 9/12 without its own top 3: +40.91 R. It beats v6 on 4 of 5 assets and in both eras (tuning +23.45 vs −1.32; holdout +68.87 vs +42.13).
~~~

#### FN-TRD-08

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 8 · the reviewer's class MEASURED
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 8 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-8 · MEASURED · operator.** R4 fractal thesis.
- At 4h, 12h aligned expansion beats 12h in-range mid for both event types, both eras and both scales.
  - Retest-hold breakout: +0.376 vs −0.039 (frozen 3.0: +0.729 vs +0.168).
  - Swing-failure: +0.239 vs −0.474.
- But the gaps+order null reproduces the aligned cell (breakout real +0.376 vs null median +0.570, percentile 30). The 12h trend does the work, not the range event.
- At H100 the aligned breakout cell turns to −0.297.
- At 1h no cell is net positive. The 12h and 1d cells are too thin to read.
~~~

#### FN-TRD-09

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 9 · the reviewer's class MEASURED
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 9 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-9 · MEASURED · operator.** R5 read by direction.
- In-range 4h entries overall are positive: 141 at +0.168. So v6 is not "killed in chop" at entry.
- Entries in the third of the range nearest the boundary the trade must break earn about zero: 4h n85 at +0.062 (tuning −0.086, holdout +0.305); 12h n57 at +0.008.
- Mid-third entries do well: 4h n55 at +0.354; 12h n44 at +0.325.
~~~

#### FN-TRD-10

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 10 · the reviewer's class MEASURED
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 10 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-10 · MEASURED · operator.** P-TP-RNG repeats the wall-exit lesson.
- 36 fills, median at +1.14 R.
- 21 campaigns improved by +21.01 R (win rate 34.5% → 37.5%). 15 worsened by −25.00 R; 9 of those were v6 winners of ≥+2 R that lost −21.78 R between them.
- Tail ratio 0.9486, and the sign flips at frozen 3.0 (+4.87 R).
~~~

- also reported by: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=statistics].report` · numbered item 9 under `## Findings-not-fixed candidates for the build doc (facts, not defects)`

~~~text
9. **P-TP-RNG's named risk showed up:** D15 tail ratio 0.9486 and max Δ share 1.1428. The frozen-3.0 twin is +0.024 [−0.013, +0.060].
~~~

#### FN-TRD-11

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 11 · the reviewer's class MEASURED
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 11 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-11 · MEASURED · operator.** The adds.
- **SFP add** fights the trail. 8 of 25 SFP events arrive only at or after the exit. All 12 admitted adds lost, with a median of 13 hours from add to exit.
- **BRK add** has no gross edge. Across 66 adds (median 2.05 R above entry), the gross add legs total about −0.90 R. Fees and funding of about −3.2 R decide the sign (Σ add_r −4.12). The frozen-3.0 twin is +3.58 R.
~~~

#### FN-TRD-12

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 12 · the reviewer's class MEASURED + HARVESTED
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 12 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-12 · MEASURED + HARVESTED · operator.** P-BRK-4H's harvest, quantified.
- In v6 itself the "harvest" is a de-risk: 51 of 55 harvests are at a loss (median −0.53 R).
- With the same exits and no harvest, the lane would be about +24.64 R (+0.077 per trade) instead of +16.19 R. The difference is holdout +9.12 R, tuning −0.67 R. So the harvest is not why the lane failed.
- The lane is split by side and asset: longs −6.8 R vs shorts +23.0 R, and BTC −14.3 R.
- Candidate: the memory-line first-hold twin is +0.359 [+0.035, +0.702] on n186 and positive in both eras (+0.376 / +0.325). It was chosen from 6 twins, so it is a selection, not a result.
~~~

- also reported by: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=fidelity].report` · bold-bullet item 5 under `## Findings-not-fixed candidates (facts for the operator, not defects)`

~~~text
- **P-BRK-4H:** v6's harvest fires on 215 of 322 campaigns, and 137 of those at a negative unit move (the entry sits next to the harvest band). Tier-E frozen-3.0 twin: +0.165 R, p 0.00025. Tier-E memory-line arm: +0.359 R.
~~~

- also reported by: `research_outputs/tierc11/stage_t_brk/STAGE_T_BRK.md` · bullet item 1 under `## 10 · Findings (disclosures, not fixed; no rule was changed after a number was seen)`

~~~text
- F-1 THE v6 HARVEST FIRES EARLY ON THIS LANE. v6's harvest (50% at the 89/316 band edge, harvest_min_unit_r = -inf) fired on 215/322 scored campaigns; 137 of those harvests were at a NEGATIVE unit move (median over all 215 harvests -0.1457 R; over the 137 negative ones -0.3312 R), a median 3 bars after entry (58 on the very next bar). The lane enters AT the EMA-89 tap, next to the harvest band. This is the registered 'v6 management', built as written; it is the operator's to judge.
~~~

#### FN-TRD-14

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 13 · the reviewer's class MEASURED
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 14 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-14 · MEASURED · operator.** TC10's lone 4h pooled holdout PASS (+0.0062 at frozen 3.0) was a censoring artifact (`R2_FEASIBILITY.md:910`).
- The 20 extra 4h bars made 15 edge anchors measurable that TC10 could not yet score.
- All 15 are between −2.5 and −6.7 ATR, and 14 of them come from one BTC range break.
- The row now reads FAIL (−0.0255). Without those 15 anchors the median is +0.0942 and the net is +0.0058.
- The table shows the flip but does not explain it.
~~~

#### FN-TRD-15

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 14 · the reviewer's class LEAN
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 15 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-15 · LEAN · operator.** With 5 asset clusters, p = 1/4001 only says "the sign holds on all 5 assets". The 0.0111 bar cannot tell that apart from a strong effect.
~~~

- also reported by: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=statistics].report` · numbered item 3 under `## Findings-not-fixed candidates for the build doc (facts, not defects)`

~~~text
3. **P-AGE-1 SUPPORTED on 5 asset clusters:**
   - p = 1/4001 is the bootstrap floor. It is reached because all 5 per-asset Δ are positive (+0.35, +0.17, +0.28, +0.19, +0.15).
   - An exact sign test at the asset level cannot go below 1/32 = 0.031, which is above 1/90. The bar is only reachable through the few-cluster bootstrap.
   - 0 new campaigns since the TC10 pin.
~~~

- also reported by: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=statistics].report` · numbered item 6 under `## Findings-not-fixed candidates for the build doc (facts, not defects)`

~~~text
6. **The bootstrap is coarse with 5 clusters.** There are at most 126 distinct draw values (124 and 125 observed for P-WARN-1), so CIs repeat across seeds; P-WARN-1's CI is identical at both seeds. LOAO with 4 clusters gives repeated bounds, for example P-RELAY-1's CI hi of +1.6566 on 3 dropped panels.
~~~

#### FN-TRD-16

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 15 · the reviewer's class MEASURED
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 16 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-16 · MEASURED · operator.** Forward-ledger pace.
- Both books close about 30 campaigns a year, so n ≥ 30 is roughly 12 months away (around Q3–Q4 2027).
- A refresh past 2026-09-25 needs the foundation re-rooted on a new snapshot; this limit is already filed.
~~~

- also reported by: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=fidelity].report` · bold-bullet item 9 under `## Findings-not-fixed candidates (facts for the operator, not defects)`

~~~text
- **The forward ledger cannot refresh** past the TC11 pin until the foundation is re-rooted on a new snapshot.
~~~

- also reported by: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=causality].report` · numbered item 7 under `### Findings-not-fixed candidates for the build doc (facts, not defects)`

~~~text
7. The forward ledger has 0 appended per book at the pin. A refresh on new bars needs a new snapshot and pin record, as the builder's own LIMIT note says.
~~~

- also reported by: `research_outputs/tierc11/forward/FORWARD_LEDGER.md` · the line starting `LIMIT (finding, not fixed):`

~~~text
LIMIT (finding, not fixed): the foundation is pinned to the TC11 snapshot and pin; a refresh on bars after 2026-09-25T00:00Z needs the foundation re-rooted on a new snapshot + pin record (operator / foundation work).
~~~

- also reported by: `research_outputs/tierc11/stage_t_relay/STAGE_T_RELAY.md` · the line starting `LIMIT (finding, not fixed):`

~~~text
LIMIT (finding, not fixed): the foundation is pinned to the TC11 snapshot and pin; a refresh on bars after 2026-09-25T00:00Z needs the foundation re-rooted on a new snapshot + pin record (operator / foundation work).
~~~

#### FN-TRD-17

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 16 · the reviewer's class MEASURED
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 17 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-17 · MEASURED · operator.** Provisional and split R2 lenses.
- 1w is the only lens with a positive edge net (+1.12 ATR) but has n=6 ranges on a fallback pick that is in-sample, so it reads FAIL (provisional, n<30).
- 1d passes in tuning and fails in holdout (−0.69).
~~~

- also reported by: `research_outputs/tierc11/stage_r/STAGE_R.md` · bullet item 1 under `## Findings not fixed (for the operator) [L-R.4]`

~~~text
- R2 1w: the lens verdict of record is **FAIL (provisional, n<30)** — PROVISIONAL (a leg under its floor: n_ranges 6, edge_n 48, edge_n_ranges 5; floors 30 / 30 / 30). Per the contract a FAIL closes the lens for range trading; a provisional FAIL is listed here for the operator [L-R.4]. Pick window whole-tape (fallback); fallback members BTCUSDT,ETHUSDT,SOLUSDT,NEARUSDT,ZECUSDT.
~~~

#### FN-STA-2

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 17
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=statistics].report` · numbered item 2 under `## Findings-not-fixed candidates for the build doc (facts, not defects)`
- owner basis: a fact for the operator to weigh (the report's own section heading: facts, not defects); no code change is owed

~~~text
2. **P-WIN-1:**
   - Its 90% CI excluding zero is a one-sided 5% statement; the family bar is 1/90.
   - The effect is carried by BTC (+0.52) and ETH (+0.27); NEAR (−0.10) and SOL (−0.09) are negative.
   - LOAO is 2/5, and the holdout slice CI includes zero (+0.238 [−0.014, +0.369]).
   - It also carries a selection hazard.
~~~

- also reported by: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=fidelity].report` · bold-bullet item 4 under `## Findings-not-fixed candidates (facts for the operator, not defects)`

~~~text
- **P-WIN-1:** CI low bound +0.003, but p 0.036 misses the 0.0111 bar.
~~~

#### FN-STA-8

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 18
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=statistics].report` · numbered item 8 under `## Findings-not-fixed candidates for the build doc (facts, not defects)`
- owner basis: a fact for the operator to weigh (the report's own section heading: facts, not defects); no code change is owed

~~~text
8. **P-ADD-SFP boundary cases.**
   - Only 9 campaigns carry adds.
   - The frozen-3.0 twin ([−0.0071, +0.0000]) and the tuning slice have a CI hi of exactly 0 with p 1.0. The Δ is exactly 0 on assets without adds, so "CI includes zero" is a boundary reading.
~~~

- also reported by: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=fidelity].report` · bold-bullet item 8 under `## Findings-not-fixed candidates (facts for the operator, not defects)`

~~~text
- **P-ADD-SFP** acted on only 9 campaigns; its CI is wholly below zero.
~~~

#### FN-FID-1

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 19
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=fidelity].report` · bold-bullet item 1 under `## Findings-not-fixed candidates (facts for the operator, not defects)`
- owner basis: a fact for the operator to weigh (the report's own section heading: facts, not defects); no code change is owed

~~~text
- **Range trading is closed on every lens.** R2 FAILs all seven lenses and the maker twin fails everywhere, so no reopening path exists.
  - 4h now FAILs at the calibrated scale (−0.103), where TC10 passed its holdout.
  - The 12h edge median is −0.113 ATR. That is the lens P-TP-RNG takes profit on.
~~~

- also reported by: `research_outputs/tierc11/stage_s/STAGE_S.md` · bold-bullet item 4 under `## 6 · Not built, and why`

~~~text
- **Findings not fixed.** The 1h lens is closed for range trading in this and every later tier unless the operator changes the toll model [contract R2]. The maker twin at the record cell reads FAIL, so no reopening path is open.
~~~

#### FN-FID-7

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 20
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=fidelity].report` · bold-bullet item 7 under `## Findings-not-fixed candidates (facts for the operator, not defects)`
- owner basis: a fact for the operator to weigh (the report's own section heading: facts, not defects); no code change is owed

~~~text
- **P-ADD-BRK's "refuse below-entry" twin** is byte-identical to its scored arm: no add ever went below entry.
~~~

- also reported by: `research_outputs/tierc11/stage_a/STAGE_A.md` · bullet item 4 under `## 10 · Findings (derived in-build; findings-not-fixed for the build doc)`

~~~text
- F3 P-ADD-BRK: the Tier-E arm(s) ['tierE__refuse_below_entry'] are byte-identical to the scored book (the twin's class holds no admitted add on the data).
~~~

#### FN-FID-10

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 21
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=fidelity].report` · bold-bullet item 10 under `## Findings-not-fixed candidates (facts for the operator, not defects)`
- owner basis: a fact for the operator to weigh (the report's own section heading: facts, not defects); no code change is owed

~~~text
- **Reading conflict:** L-W.4 says the condition block is the only Tier-E place a CI is printed, while L-1.4 prints a CI on every Tier-E row.
~~~

#### FN-FID-11

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 22
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=fidelity].report` · bold-bullet item 11 under `## Findings-not-fixed candidates (facts for the operator, not defects)`
- owner basis: a fact for the operator to weigh (the report's own section heading: facts, not defects); no code change is owed

~~~text
- **L-W.1 reads "closed before the 4h bar closes" as ≤,** with no rival reading printed.
~~~

#### FN-FID-12

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 23
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=fidelity].report` · bold-bullet item 12 under `## Findings-not-fixed candidates (facts for the operator, not defects)`
- owner basis: a fact for the operator to weigh (the report's own section heading: facts, not defects); no code change is owed

~~~text
- **Disclosure items:**
  - The AM-5 mismatch bars: ZECUSDT 2024-10-28T20:00Z plus each asset's first-frame bars.
  - Pick stability changed on: 1h BTC, SOL, NEAR; 12h BTC, ETH, SOL; 4h NEAR.
  - All 1w picks are whole-tape fallbacks (in-sample everywhere).
~~~

#### FN-CAU-2

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 24
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=causality].report` · numbered item 2 under `### Findings-not-fixed candidates for the build doc (facts, not defects)`
- owner basis: a fact for the operator to weigh (the report's own section heading: facts, not defects); no code change is owed

~~~text
2. The P-BRK-4H holdout statistic includes that one campaign whose death anchor was read in-sample (the MINOR-2 case, +2.696 R).
~~~

- also reported by: `research_outputs/tierc11/stage_t_brk/STAGE_T_BRK.md` · bullet item 6 under `## 10 · Findings (disclosures, not fixed; no rule was changed after a number was seen)`

~~~text
- F-6 HOLDOUT ROWS ACTING ON A TUNING-ERA DEATH (disclosure): 1 scored holdout campaign(s) act on a death whose bar closed at or before the era cut (BTCUSDT death close 2024-06-24T08:00:00Z, entry close 2024-07-01T16:00:00Z, net +2.696038 R). The per-row scale_in_sample flag is read at the entry instant (R-TBRK-10; L-R.2 'read at an instant'), so these rows read False; era membership is by the entry close [L-1.3] and is unchanged. Per ridden arm: {'scored': 1, 'tierE__panel17': 5, 'tierE__memline_first_hold': 1, 'tierE__memline_oneshot_flip': 1, 'tierE__frozen3': 1, 'tierE__oneshot_first_touch': 1}. Printed beside the holdout slice in §3. The EXTRA column anchor_scale_in_sample (R-TBRK-11: death close <= cut OR known close <= cut at the calibrated scale, OR the row's flag; False at frozen 3.0) labels these rows True. Holdout rows labelled in-sample per ridden arm, (scale_in_sample, anchor_scale_in_sample): {'scored': (0, 1), 'tierE__panel17': (26, 31), 'tierE__memline_first_hold': (0, 1), 'tierE__memline_oneshot_flip': (0, 1), 'tierE__frozen3': (0, 0), 'tierE__oneshot_first_touch': (0, 1)} (T_BRK_ARMS n_holdout_scale_in_sample / n_holdout_anchor_scale_in_sample).
~~~

#### FN-CAU-6

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 25
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=causality].report` · numbered item 6 under `### Findings-not-fixed candidates for the build doc (facts, not defects)`
- owner basis: a fact for the operator to weigh (the report's own section heading: facts, not defects); no code change is owed

~~~text
6. No relay enters inside its trigger bar: minimum lead is 4h, and none of the 173 relays has zero 4h lead.
~~~

#### FN-REP-3

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 26
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=reproducibility].report` · bullet item 3 under `## Findings-not-fixed candidates for the build doc`
- owner basis: a fact for the operator to weigh (the report's own section heading: facts, not defects); no code change is owed

~~~text
- No campaign enters on the bar that straddles the era cut (bar open 2024-06-30T20:00Z). On this corridor, dating the era by the entry bar's close rather than its open changes no number.
~~~

#### FN-STG-R-3

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 27
- source: `research_outputs/tierc11/stage_r/STAGE_R.md` · bullet item 3 under `## Findings not fixed (for the operator) [L-R.4]`
- owner basis: a fact for the operator to weigh (the report's own section heading: facts, not defects); no code change is owed

~~~text
- R3 / R5 / NEST_GRID calibrated reads are IN-SAMPLE on every tuning-era entry (SCALE-IN-SAMPLE, L-R.2); each aggregated row prints its in-sample count and the holdout slice beside [SR-12].
~~~

- also reported by: `research_outputs/tierc11/stage_t_brk/STAGE_T_BRK.md` · bullet item 3 under `## 10 · Findings (disclosures, not fixed; no rule was changed after a number was seen)`

~~~text
- F-3 SCALE LABELS: 4h fallback (whole-tape, IN-SAMPLE everywhere) picks in the 17-asset view: ['PUMPUSDT', 'HYPEUSDT']; CLASSIC5 4h picks whose first-half-of-tuning pick differs (stability_changed, flagged on every row): ['NEARUSDT']. Every scored tuning-era row is scale-in-sample (210/322); the holdout slice and the frozen-3.0 twin are printed beside (§3).
~~~

- also reported by: `research_outputs/tierc11/stage_a/STAGE_A.md` · bullet item 6 under `## 10 · Findings (derived in-build; findings-not-fixed for the build doc)`

~~~text
- F5 [L-R.2] 1h pick stability: the first-half-of-tuning pick differs from the tuning pick for ['BTCUSDT', 'NEARUSDT', 'SOLUSDT']; every add row of those assets carries stability_changed = True. Scale-in-sample adds on the scored arms: P-ADD-BRK 32/66, P-ADD-SFP 2/12 (all in the tuning era).
~~~

- also reported by: `research_outputs/tierc11/stage_h/STAGE_H.md` · bullet item 5 under `## 9 · Findings (stage-intrinsic, derived from the tables above)`

~~~text
- H-5 SCALE-IN-SAMPLE: every 12h pick of record is a tuning-era pick (BTCUSDT 2.00, ETHUSDT 1.50, NEARUSDT 2.25, SOLUSDT 2.25, ZECUSDT 2.00); the first-half-of-tuning pick differs on BTCUSDT, ETHUSDT, SOLUSDT; the tuning slice is structurally in-sample, the holdout slice and the frozen-3.0 twin are the causal reads (table 1).
~~~

#### FN-STG-A-8

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 28
- source: `research_outputs/tierc11/stage_a/STAGE_A.md` · bullet item 10 under `## 10 · Findings (derived in-build; findings-not-fixed for the build doc)`
- owner basis: a fact for the operator to weigh (the report's own section heading: facts, not defects); no code change is owed

~~~text
- F8 [SA-11] P-ADD-BRK head-to-head arm tierE__head_to_head_vs_p_add_sfp: paired vs P-ADD-SFP/scored on 200 identical keys, ΣΔ -0.041104 (mean -0.000206) — a SELECTION, not a result; neither promoted by the other's failure.
~~~

- also reported by: `research_outputs/tierc11/stage_a/STAGE_A.md` · bullet item 11 under `## 10 · Findings (derived in-build; findings-not-fixed for the build doc)`

~~~text
- F8 [SA-11] P-ADD-SFP head-to-head arm tierE__head_to_head_vs_p_add_brk: paired vs P-ADD-BRK/scored on 200 identical keys, ΣΔ +0.041104 (mean +0.000206) — a SELECTION, not a result; neither promoted by the other's failure.
~~~

#### FN-H-TC10-Q2

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 29
- source: `research_outputs/tierc11/LEANS.md` · the line starting `- TC10's operator question Q2`
- owner basis: an operator question TC10 left open; the executor may not answer it

~~~text
- TC10's operator question Q2 (whether slippage joins the toll of record) stays open.
~~~

#### FN-H-SAIL

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 30
- source: `exchange/queue/2026-09-24_TC11_APOLLO.md` · the line starting `(m=9; SAIL still HELD`
- owner basis: SAIL is the operator's act; the contract holds it

~~~text
 (m=9; SAIL still HELD; the forward ledger opened). publish_exchange; STATE push; final line:
~~~

#### FN-M-SCORES-LEAVES

- **MEASURED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 31
- source: `research_outputs/tierc11/scores/SCORES.json` · git show <reviewed>:SCORES.json vs HEAD:SCORES.json, leaf by leaf
- owner basis: an operator ruling is pending (MINOR-9); the executor may not rule on its own record

~~~text
SCORES.json between the reviewed commit 04067a0 (the lens reviews) and HEAD d307829: 156 leaves added, 0 removed, 3 changed — each changed leaf a string label (.rows[1].verdict_cell, .rows[5].verdict_cell, .rows[8].status_reason); 0 numeric, bool or null leaf moved. The TC11-FIX verifier filed the additions as MINOR-9, awaiting the operator's ruling (TC11_FIX_VERIFY.json verify).
~~~

- also reported by: `research_outputs/tierc11/close/TC11_FIX_VERIFY.json` · `verify` · bold-bullet item 7 under `## 6. Remaining defects`

~~~text
- **MINOR-9 (156 added SCORES.json leaves):** still awaiting the operator's ruling.
~~~

#### FN-M-TC11X-SHIM

- **MEASURED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 32
- source: `git:df0b5c4` · git log -1 df0b5c4 (the pinned commit whose subject names the vendored shim)
- owner basis: a cross-lane alignment the operator orders; the tc11x lane is not this executor's to touch

~~~text
The parallel tc11x lane (commit df0b5c4, pinned — it sits on the local branch tierc11x, not on origin: "tc11x(X-D): the corridor — TC11 pin 2026-09-25T00:00Z, six certified TC11 records extracted to data/tc11_rec, write-once…") vendors the env shim from 086d66da — the pre-AM-1 shim. TC11's committed shim scripts/tierc11_env.py is sha256 1526093b25161927… (PROGRESS.json stage TC11-ENV; on disk 1526093b25161927…). The two lanes do not run one shim; this CLOSE read the lane's pinned commit through git only and changed nothing there.
~~~

#### FN-M-QUEUE-STAMP

- **MEASURED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 33
- source: `exchange/queue/2026-09-24_TC11_APOLLO.md` · grep ^BUILT; the three pins compared
- owner basis: queue hygiene and re-pinning are the operator's call

~~~text
exchange/queue/2026-09-24_TC11_APOLLO.md carries no BUILT line (other queue files do, e.g. exchange/queue/2026-09-22_OR2_oracle_rulings_ARGUS.md). Its sha256 bb38e016a8f3e55c… is pinned by REGISTRATIONS.json contract.sha256, scores/REGISTRY_CHECK.json contract.sha256 and PROGRESS.json contract_of_record — stamping BUILT into the file would change those bytes and break every pin. Whether to stamp (and re-pin), stamp a sibling file, or leave the contract byte-frozen is the operator's word.
~~~

#### FN-M-TC10-FIRST

- **MEASURED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 34
- source: `exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md` · path exists; ledger header grep
- owner basis: the operator runs both close scripts, TC10's first

~~~text
At draft time (HEAD d307829) TC10's CLOSE had not run: exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md existed: no; exchange/status/LEDGER_APOLLO.md carried a TIER-C10 STATUS block: no. TC11's close_acts.sh step 0 STOPS until TC10's report is tracked and its STATUS block committed ("run research_outputs/tierc10/close/close_acts.sh first (the ledger keeps tier order)"); F-CLOSE-ORDER proves each stop in a sandbox clone.
~~~

#### FN-M-TC10-ACTS-IGNORED

- **MEASURED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 35
- source: `research_outputs/tierc10/close/close_acts.sh` · the bare 'git add' line; git check-ignore -v --no-index on each path it adds
- owner basis: TC10's close script is outside this executor's write scope; the operator edits it or adds -f by hand at its step 6 before running it

~~~text
TC10's research_outputs/tierc10/close/close_acts.sh:103 (its step 6; the script itself untracked and git-ignored: local disk only) runs `git add "$APP" "$LAR"` without -f under `set -euo pipefail`; APP = research_outputs/tierc10/LEDGER_APOLLO_APPEND.md (tracked) matches `.gitignore:263` (`research_outputs/tierc10/**`); LAR = research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt (tracked) matches `.gitignore:263` (`research_outputs/tierc10/**`). A `git add` naming a path under an ignored directory stages it but exits 1 ('The following paths are ignored by one of your .gitignore files'); F-CLOSE-ORDER reproduces the exit in a sandbox clone. So TC10's script stops at its step 6 after its step 5 has appended TC10's block to exchange/status/LEDGER_APOLLO.md, before its own residue commit and before publish(): TC10's report is left untracked in exchange/reports/ and the ledger uncommitted. TC11's close_acts.sh step 0 then stops on the TC10 gate (report not tracked / ledger not committed), naming this finding. The fix (`git add -f` at research_outputs/tierc10/close/close_acts.sh:103, the rule .gitignore:263 the reason) is in TC10's script, outside this executor's write scope.
~~~

#### FN-M-EXCHANGE-SWEEP

- **MEASURED** · owner **operator** · status **REPORTED, NOT FIXED** · rank 36
- source: `exchange/` · git diff --name-only -- exchange
- owner basis: the publish acts are the operator's

~~~text
publish() stages ALL of exchange/** (CONVENTIONS §3.4). Uncommitted exchange/ edits at HEAD d307829: exchange/status/daily/DAILY_2026-09-25.md — the daily routine's own appended section, which it says the next publish carries. TC10's close_acts.sh publish step or TC11's, whichever runs first, will commit it.
~~~

#### FN-TRD-13

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 37 · the reviewer's class MEASURED
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=trading].report` · fnf item 13 under `## Findings-not-fixed for the build doc (ranked)`
- owner basis: the trading reviewer's own owner tag on the item

~~~text
**FNF-13 · MEASURED · executor.** The R2 1h median of exactly 0.0 is real.
- 15 exact-zero H20 terms from tick quantization (NEAR 10, ZEC 4, SOL 1) straddle the middle of 12,044 terms: 6,012 are below zero and 6,017 above.
- Excluding the zeros the median is +0.0015. The mean is −0.330 ATR.
- The FAIL holds at any toll, because the law requires net strictly > 0.
~~~

- also reported by: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=fidelity].report` · bold-bullet item 2 under `## Findings-not-fixed candidates (facts for the operator, not defects)`

~~~text
- **The 1h FAIL turns on a pooled median of exactly 0 plus BTC's binding toll.** ETH alone would pass the edge leg (+0.0023). F-FEAS checks the verdict against its printed columns but can never catch a wrong edge statistic.
~~~

- also reported by: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=statistics].report` · numbered item 7 under `## Findings-not-fixed candidates for the build doc (facts, not defects)`

~~~text
7. **P-SCALP-2's closure is robust.**
   - The pooled 1h holdout median term is exactly 0.000000, from exact ties.
   - The CLASSIC5 per-asset medians are BTC +0.082, ETH +0.116, NEAR −0.166, SOL −0.018, ZEC −0.022, all below the taker toll of 0.1676.
   - The tuning-era word, printed beside it, is also FAIL.
~~~

#### FN-CAU-1

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 38
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=causality].report` · numbered item 1 under `### Findings-not-fixed candidates for the build doc (facts, not defects)`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
1. The 1d coincidence columns depend on the 1w lens, whose pick is a whole-tape fallback (in-sample everywhere). 36 of 3,558 holdout v6 nest rows have a 1d coincidence flag True while labelled `1d_scale_in_sample=False`; the 1w columns on the same rows are labelled True. Nothing registered uses 1d coincidence.
~~~

#### FN-CAU-3

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 39
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=causality].report` · numbered item 3 under `### Findings-not-fixed candidates for the build doc (facts, not defects)`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
3. The walk-or-defer choice on mismatch bars (AM-5) uses later prices within the bar, but it affects nothing on this corridor: 0 W1 events, 0 adds, 0 relays fall on a mismatch bar.
~~~

- also reported by: `research_outputs/tierc11/stage_a/STAGE_A.md` · bullet item 1 under `## 10 · Findings (derived in-build; findings-not-fixed for the build doc)`

~~~text
- F1 [AM-5, L-W.0] mismatch bars ridden by the v6 set: 1 bar(s) in 1 campaign(s) — ZECUSDT entered 2024-10-28T08:00:00Z rides 2024-10-28T20:00:00Z; add events moved to a parent close: 0, adds moved: 0 (every arm). Decided by the parent per L-W.0; the walk-or-defer choice reads later prices of the same 4h bar (AM-5 disclosure).
~~~

- also reported by: `research_outputs/tierc11/stage_r/STAGE_R.md` · bullet item 4 under `## Findings not fixed (for the operator) [L-R.4]`

~~~text
- AM-5 (walk-mismatch bars) does not touch this stage's books: NEST_v6 / NEST_trg912 read the UNWALKED 4h ride.
~~~

#### FN-CAU-4

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 40
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=causality].report` · numbered item 4 under `### Findings-not-fixed candidates for the build doc (facts, not defects)`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
4. The "inside its 4h bar" clause of the refuse-post-harvest Tier-E twin (the builder's F7) has 0 affected adds. The only event inside a harvest bar is at the harvest close (BTC, `add_ms` 1751947200000), and it was refused anyway because it came before the latch.
~~~

- also reported by: `research_outputs/tierc11/stage_a/STAGE_A.md` · bullet item 8 under `## 10 · Findings (derived in-build; findings-not-fixed for the build doc)`

~~~text
- F7 [L-A.1, SA-8] P-ADD-BRK: the post-harvest twin's 'inside its 4h bar' clause reads the harvest before its bar's close for an add at an earlier 1h close of that bar — 0 such add(s) on the scored arm, 0 event(s) refused by that clause on tierE__refuse_post_harvest (look-ahead at reading level, inside a Tier-E twin).
~~~

- also reported by: `research_outputs/tierc11/stage_a/STAGE_A.md` · bullet item 9 under `## 10 · Findings (derived in-build; findings-not-fixed for the build doc)`

~~~text
- F7 [L-A.1, SA-8] P-ADD-SFP: the post-harvest twin's 'inside its 4h bar' clause reads the harvest before its bar's close for an add at an earlier 1h close of that bar — 0 such add(s) on the scored arm, 0 event(s) refused by that clause on tierE__refuse_post_harvest (look-ahead at reading level, inside a Tier-E twin).
~~~

#### FN-CAU-5

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 41
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=causality].report` · numbered item 5 under `### Findings-not-fixed candidates for the build doc (facts, not defects)`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
5. F-ADD's `known_at == event bar` assert cannot fail by construction (the builder says so in SA-1). The real guard is the cut-tape leg, which I re-ran GREEN.
~~~

#### FN-REP-2

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 42
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=reproducibility].report` · bullet item 2 under `## Findings-not-fixed candidates for the build doc`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- No TP fill was ever blocked by a stop in any of the 4 TP arms, and the funding ceiling never binds on the 200 base campaigns. Those code paths are exercised only by planted tests, never by the data.
~~~

- also reported by: `research_outputs/tierc11/stage_h/STAGE_H.md` · bullet item 2 under `## 9 · Findings (stage-intrinsic, derived from the tables above)`

~~~text
- H-2 a live, touched TP beaten by the stop on the same bar (STOP -> TP): {'scored': 0, 'tp_post_harvest': 0, 'unguarded': 0, 'frozen3': 0} — the adverse-first order never bound on this corridor.
~~~

#### FN-REP-5

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 43
- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=reproducibility].report` · bullet item 5 under `## Findings-not-fixed candidates for the build doc`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- Suite run times for BOX-COST: R4 831 s, nest 210 s, ride 154 s, score 134 s, W 129 s, R 127 s. The data F-DET has no hash-order sabotage leg.
~~~

#### FN-FIX-A

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 44
- source: `research_outputs/tierc11/close/TC11_FIX_VERIFY.json` · `verify` · bold-bullet item 1 under `## 6. Remaining defects`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- **A. No plant covers the at-close main-tree TC10 re-check.** Deleting `tc10_findings(rec["staged_tc10"], ROOT, " (at close)")` in `scripts/tierc11_worktree_attest.py` leaves F-ATTEST GREEN. The fixer said it cannot be planted without writing the main tree's record, but it can: bend the worktree's staged copy and rewrite `staged_tc10[rel]` in the open record to the bent sha. The re-hash then passes and only the at-close check can fire.
~~~

#### FN-FIX-B

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 45
- source: `research_outputs/tierc11/close/TC11_FIX_VERIFY.json` · `verify` · bold-bullet item 2 under `## 6. Remaining defects`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- **B. F-CLOSURE-ALL static scan has gaps.** None of these is flagged:
  - `getattr(builtins, 'exec')('import tierc10_census')`
  - `object.__getattribute__(r, 'top')`
  - `r.__getattribute__('bottom')`
  - `d = vars(r); d['top']`
~~~

#### FN-FIX-C

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 46
- source: `research_outputs/tierc11/close/TC11_FIX_VERIFY.json` · `verify` · bold-bullet item 3 under `## 6. Remaining defects`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- **C. F-D11-PORT misses an alias.** `r = ROOT; return r / 'research_outputs' / 'tierc10' / 'data'` in `tierc11_data.py` is not flagged, because the detector only follows the literal name `ROOT`.
~~~

#### FN-FIX-D

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 47
- source: `research_outputs/tierc11/close/TC11_FIX_VERIFY.json` · `verify` · bold-bullet item 4 under `## 6. Remaining defects`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- **D. Stale shas appear outside HISTORICAL text in plant narratives.** `FIXTURES_SCORE.txt:109` and `STAGE_SCORE.md:214` name `b1c6275b…` and `30b24b1e…` in the REPORT-STALE-PIN plant descriptions. They are not backticked, so F-REPORT stays silent. Strictly this breaks the grep rule; using a made-up sha in the plant would fix it.
~~~

#### FN-FIX-E

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 48
- source: `research_outputs/tierc11/close/TC11_FIX_VERIFY.json` · `verify` · bold-bullet item 5 under `## 6. Remaining defects`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- **E. By design, no suite checks HEAD's real PROGRESS record.** The F-ATTEST real leg runs on the fixture's view of PROGRESS, so it goes RED only if the view differs, never because HEAD's record lags. The drift against HEAD's real record (currently 15) goes to stdout only. After the refresh commit the orchestrator must read that attest stdout line and see 0; nothing enforces it. The transcript does not depend on the commit: the first three picked plant files are `books/*`, none of them drifting.
~~~

#### FN-FIX-F

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 49
- source: `research_outputs/tierc11/close/TC11_FIX_VERIFY.json` · `verify` · bold-bullet item 6 under `## 6. Remaining defects`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- **F. (pre-existing, not this pass) The data transcript depends on where the main tree lives.** A guard message in the data suite's F-D11-GUARD prints the snapshot path relative to the main tree (`'../.cache/…'`), so a checkout at another path produces a different FIXTURES_DATA line.
~~~

#### FN-STG-R-2

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 50
- source: `research_outputs/tierc11/stage_r/STAGE_R.md` · bullet item 2 under `## Findings not fixed (for the operator) [L-R.4]`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- R3 lanes: the contract's R3 covers every card including the lanes; this build stamps base v6 and 9/12; the lanes are stamped by the `lanes` subcommand (stage_r/lanes/: NEST_<REG>.parquet, NEST_GRID_LANES.md, LANES_MANIFEST.json; SR-15) through the same nest-book door, after the owning stages filed the named-event instant columns (harvest_close_ms, add1_close_ms / add2_close_ms). The door still REFUSES (HALT, naming the counts) any regbook whose own record says a harvest / add / +1R happened with no instant to stamp it [L-R.5 'plus the named events'].
~~~

#### FN-STG-TB-2

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 51
- source: `research_outputs/tierc11/stage_t_brk/STAGE_T_BRK.md` · bullet item 2 under `## 10 · Findings (disclosures, not fixed; no rule was changed after a number was seen)`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- F-2 THE TIDE BAR MATTERS ON 9 SCORED CANDIDATES: the entry bar's tide differs from the previous bar's (1 entered, 8 refused by the tide). BK.tide_4h_for_exec on a 4h frame reads the previous bar (F-BRK-TIDE proves it); the reading of record (the entry bar's own close) is used.
~~~

#### FN-STG-TB-4

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 52
- source: `research_outputs/tierc11/stage_t_brk/STAGE_T_BRK.md` · bullet item 4 under `## 10 · Findings (disclosures, not fixed; no rule was changed after a number was seen)`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- F-4 No campaign of any ridden arm is open at the pin (corridor_end exits: 0); rail-bound stops: 47/322 scored campaigns (a rail-bound R = |entry - (entry - ATR)| carries float rounding against ATR; the law, not a bound, is what F-BRK-ENTRY holds).
~~~

#### FN-STG-TB-5

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 53
- source: `research_outputs/tierc11/stage_t_brk/STAGE_T_BRK.md` · bullet item 5 under `## 10 · Findings (disclosures, not fixed; no rule was changed after a number was seen)`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- F-5 The 17-asset view's CLASSIC5 rows are byte-identical to the scored book (asserted in the build); the engine one-shot memory flip twin is the leash's own evaluation, not bounded by the next death (the engine's law), so its candidacy differs from the scan's window by construction.
~~~

#### FN-STG-TB-7

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 54
- source: `research_outputs/tierc11/stage_t_brk/STAGE_T_BRK.md` · bullet item 7 under `## 10 · Findings (disclosures, not fixed; no rule was changed after a number was seen)`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- F-7 THE BAR-316 FLOOR IS APPLIED AT THE ENTRY BAR (R-TBRK-2; disclosure): campaigns whose DEATH bar is below 316 (a floor on the death would not admit them), per ridden arm (n, ΣR): {'scored': (1, -1.022657), 'tierE__panel17': (1, -1.022657), 'tierE__memline_first_hold': (0, 0.0), 'tierE__memline_oneshot_flip': (0, 0.0), 'tierE__frozen3': (2, -0.726429), 'tierE__oneshot_first_touch': (0, 0.0)}; campaigns whose TOUCH bar is below 316: {'scored': 0, 'tierE__panel17': 0, 'tierE__memline_first_hold': 0, 'tierE__memline_oneshot_flip': 0, 'tierE__frozen3': 0, 'tierE__oneshot_first_touch': 0}. The reading is unchanged.
~~~

#### FN-STG-A-2

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 55
- source: `research_outputs/tierc11/stage_a/STAGE_A.md` · bullet item 2 under `## 10 · Findings (derived in-build; findings-not-fixed for the build doc)`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- F2 [AM-3] P-ADD-BRK scored: 1 acted campaign(s) where the D12 ceiling absorbs tranche funding (Δ != add_r): ETHUSDT 2021-04-08T20:00:00Z Δ -0.023188 = add_r -0.103823 + absorbed 0.080635 − v6 absorbed 0.000000; the paired Δ is scored on net_r (AM-3), never on add_r.
~~~

- also reported by: `research_outputs/tierc11/stage_a/STAGE_A.md` · bullet item 3 under `## 10 · Findings (derived in-build; findings-not-fixed for the build doc)`

~~~text
- F2 [AM-3] P-ADD-SFP scored: 0 acted campaign(s) where the D12 ceiling absorbs tranche funding (Δ != add_r): none; the paired Δ is scored on net_r (AM-3), never on add_r.
~~~

#### FN-STG-A-4

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 56
- source: `research_outputs/tierc11/stage_a/STAGE_A.md` · bullet item 5 under `## 10 · Findings (derived in-build; findings-not-fixed for the build doc)`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- F4 P-ADD-SFP: the 2-add cap never binds on the scored arm (0 events refused at the cap), so a 3rd-add sabotage on it must be a planted row.
~~~

#### FN-STG-A-6

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 57
- source: `research_outputs/tierc11/stage_a/STAGE_A.md` · bullet item 7 under `## 10 · Findings (derived in-build; findings-not-fixed for the build doc)`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- F6 [SA-4] exit_close_ms of every arm is the v6 book of record's (the exit bar's 4h close), so the base arm is the ONE base book the scorer's F-BASE-IDENT demands; the 1h-resolved exit instant is exit_close_1h_ms.
~~~

- also reported by: `research_outputs/tierc11/stage_h/STAGE_H.md` · bullet item 6 under `## 9 · Findings (stage-intrinsic, derived from the tables above)`

~~~text
- H-6 SR-H3 exit_close_ms convention: every regbook here stamps the exit 4h bar's CLOSE (the books/v6_campaigns.parquet convention; the base arm equals that file on the 13 shared columns at its 6 dp); a stage that rides the 1h walk stamps a 1h-resolved exit instant instead — the paired statistic (net_r keyed on (symbol, entry_ms)) does not read it, a cross-stage base-identity check does.
~~~

#### FN-STG-H-1

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 58
- source: `research_outputs/tierc11/stage_h/STAGE_H.md` · bullet item 1 under `## 9 · Findings (stage-intrinsic, derived from the tables above)`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- H-1 the re-ride rival [L-1.5] admits 0 new campaign(s) into slots a TP freed and drops 0 v6 campaign(s): on this corridor the paired set and the re-ride set coincide.
~~~

#### FN-STG-H-3

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 59
- source: `research_outputs/tierc11/stage_h/STAGE_H.md` · bullet item 3 under `## 9 · Findings (stage-intrinsic, derived from the tables above)`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- H-3 fills at the open (the bar opened beyond the level, fill = open) / all fills: {'scored': '0/36', 'tp_post_harvest': '0/5', 'unguarded': '0/36', 'frozen3': '0/32'}.
~~~

#### FN-STG-H-4

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 60
- source: `research_outputs/tierc11/stage_h/STAGE_H.md` · bullet item 4 under `## 9 · Findings (stage-intrinsic, derived from the tables above)`
- owner basis: a fixture / label / code gap the executor can close in a later wave; it moves no registered number

~~~text
- H-4 the entry-side guard (ii) changes 1 campaign(s): ETHUSDT 2023-09-01T04:00 (short): unguarded tp at 2023-09-01T08:00 (level +8.247 bps beyond entry) vs scored tp at 2023-09-01T12:00.
~~~

#### FN-M-ATTEST-UNTRACKED

- **MEASURED** · owner **executor** · status **REPORTED, NOT FIXED** · rank 61
- source: `research_outputs/tierc11/review/attest/fix-head.json` · git ls-files --error-unmatch
- owner basis: the CLOSE commit adds it; a bookkeeping act

~~~text
research_outputs/tierc11/review/attest/fix-head.json — the attestation of the fix commit d307829 (verdict GREEN) — is NOT tracked at HEAD d307829; until the CLOSE commit adds it, it is local disk only. close_acts.sh step 0 requires it committed.
~~~

#### LEAN-CLOSE-1

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · rank 62
- source: `scripts/tierc11_close.py` · LEANS_CLOSE
- owner basis: a lean is the executor's operationalisation; the operator may overrule it

~~~text
[LEAN-HEPHAESTUS] §0.2 is the §0 table of scores/S0_VERDICTS.md copied byte for byte (a verbatim block), never re-rendered: the scorer's cell text, labels included, is the record.
~~~

#### LEAN-CLOSE-2

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · rank 63
- source: `scripts/tierc11_close.py` · LEANS_CLOSE
- owner basis: a lean is the executor's operationalisation; the operator may overrule it

~~~text
[LEAN-HEPHAESTUS] §0.1 opens §0 with R5's plain answer in words, its numbers read from the direction tables of stage_r/R5_CHOP.md (the tracked twin of the git-ignored R5_CHOP_DIRECTION.parquet; alignment and direction-adjusted cells), because the frozen chop table is direction-blind (the trading review's D-2); every calibrated read carries its SCALE-IN-SAMPLE count inline; the words decide nothing.
~~~

#### LEAN-CLOSE-3

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · rank 64
- source: `scripts/tierc11_close.py` · LEANS_CLOSE
- owner basis: a lean is the executor's operationalisation; the operator may overrule it

~~~text
[LEAN-HEPHAESTUS] the append's push fact is stated against the refs at draft time (HEAD and origin named by sha, ancestry read through git, time-invariant); the live fact after the operator's push goes into the one pending stamp, which close_acts.sh fills and F-LAR11 --stamped certifies.
~~~

#### LEAN-CLOSE-4

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · rank 65
- source: `scripts/tierc11_close.py` · LEANS_CLOSE
- owner basis: a lean is the executor's operationalisation; the operator may overrule it

~~~text
[LEAN-HEPHAESTUS] R4's '★ cells' are the contract's three starred L+1 conditions (EXP_ALIGNED*, IN_RANGE_COINCIDENT*, IN_RANGE_MID*) at direction 'both', calibrated scale, cell law record, each row pointing at the STAGE_R4.md lines it copies; every other cell stays in STAGE_R4.md / R4_GRID.parquet.
~~~

#### LEAN-CLOSE-5

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · rank 66
- source: `scripts/tierc11_close.py` · LEANS_CLOSE
- owner basis: a lean is the executor's operationalisation; the operator may overrule it

~~~text
[LEAN-HEPHAESTUS] the BOX-COST rows are the tierc11 commits' paths (b9ed953 included), every PROGRESS.json artifact not among them, the CLOSE's own files, the untracked tierc11 files, the two planned exchange destinations and the snapshot; files a fixture run rewrites are listed, never sized.
~~~

#### LEAN-CLOSE-6

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · rank 67
- source: `scripts/tierc11_close.py` · LEANS_CLOSE
- owner basis: a lean is the executor's operationalisation; the operator may overrule it

~~~text
[LEAN-HEPHAESTUS] the TC11-FIX verifier's residual MINORs are harvested from close/TC11_FIX_VERIFY.json, a verbatim copy of the harness's workflow journal fields, so the harvest reads a file in the repo.
~~~

#### LEAN-CLOSE-7

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · rank 68
- source: `scripts/tierc11_close.py` · LEANS_CLOSE
- owner basis: a lean is the executor's operationalisation; the operator may overrule it

~~~text
[LEAN-HEPHAESTUS] 'the nesting grid whole' (contract CLOSE; LAWS 'every grid reported whole') is printed whole in §2.3: every line under stage_r/NEST_GRID.md's R3 heading and every line of stage_r/lanes/NEST_GRID_LANES.md below its title, in verbatim blocks; the two H2 lines a verbatim block may not carry are re-printed as H4 labels. The document stays under the §4.2 per-file cap (the generator HALTs over it).
~~~

#### LEAN-CLOSE-8

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · rank 69
- source: `scripts/tierc11_close.py` · LEANS_CLOSE
- owner basis: a lean is the executor's operationalisation; the operator may overrule it

~~~text
[LEAN-HEPHAESTUS] every sentence about TC10's CLOSE is time-invariant or dated: the append states the step-0 law (TC11 follows TC10) rather than TC10's state, and its tier line cites TC10's block on LEDGER_APOLLO when that block is there at generation, else TC10's staged file, in words true before and after TC10's CLOSE.
~~~

#### LEAN-CLOSE-9

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · rank 70
- source: `scripts/tierc11_close.py` · LEANS_CLOSE
- owner basis: a lean is the executor's operationalisation; the operator may overrule it

~~~text
[LEAN-HEPHAESTUS] the R2 sentences name the lenses the [Q-R3] law closes (every non-provisional FAIL) apart from the provisional ones (a count under its floor), which stay the operator's question; the generator HALTs if any lens word or maker twin is not FAIL.
~~~

#### LEAN-CLOSE-10

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · rank 71
- source: `scripts/tierc11_close.py` · LEANS_CLOSE
- owner basis: a lean is the executor's operationalisation; the operator may overrule it

~~~text
[LEAN-HEPHAESTUS] F-NUM's coverage law (every digit traced, masked, verified or exempted) binds §0 and the append; every other number of the draft is read by the generator from its record (PROGRESS.json, the transcripts, the findings, COMPUTE_LEDGER.json, BOX_COST) and the verbatim blocks, the R4 ★ table and BOX_COST.json are re-derived by fixtures, but §1.2, §9, §10, §11 and §14.3 carry no digit-by-digit coverage check (the close verifier's m5, left open).
~~~

#### LEAN-CLOSE-11

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · rank 72
- source: `scripts/tierc11_close.py` · LEANS_CLOSE
- owner basis: a lean is the executor's operationalisation; the operator may overrule it

~~~text
[LEAN-HEPHAESTUS] the collar line stands above every table copied from STAGE_W's W2 sections and STAGE_A's head-to-head (the blocks are split before each table); tables that carry the collar in their own cells (STAGE_G's tier · selection_not_a_result · gates columns) or under a file-level collar line copied in the same block (R5_CHOP.md, NEST_GRID.md, NEST_GRID_LANES.md) are copied as they stand; registered books ('book, not a verdict') carry none.
~~~

## 3 · Harvested, then superseded by a later record — listed, not counted

#### SUP-REP-1

- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=reproducibility].report` · bullet item 1 under `## Findings-not-fixed candidates for the build doc`
- superseded because: the TC11-FIX wave fixed it: env/data run in a review worktree (MAJOR-2 of that wave) (`research_outputs/tierc11/close/TC11_FIX_VERIFY.json` fix reads '**MAJOR-2** (env suite fails in a review worktree) | Fixed')

~~~text
- In a read-only worktree, 114 of 121 fixtures re-pass; the other 7 need TC10 records at ROOT (MAJOR-1).
~~~

#### SUP-REP-4

- source: `research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json` · `result.reviews[lens=reproducibility].report` · bullet item 4 under `## Findings-not-fixed candidates for the build doc`
- superseded because: the uncommitted edits were committed in the TC11-FIX commit and re-attested GREEN at it (`research_outputs/tierc11/review/attest/fix-head.json` verdict reads 'GREEN')

~~~text
- As of close, the main tree has uncommitted TC11 edits (scripts and artifacts for stage_a, stage_g, stage_r, stage_t_relay). They were not reviewed here, and any rebuild must be re-attested.
~~~

#### SUP-FIX-MAJOR-3

- source: `research_outputs/tierc11/close/TC11_FIX_VERIFY.json` · `verify` · the line starting `**MAJOR-3 (open, orchestrator's file): PROGRESS.json has not been refreshed.**`
- superseded because: PROGRESS.json was refreshed in the TC11-FIX commit; the fix-head attestation reads it GREEN with no open finding (`research_outputs/tierc11/review/attest/fix-head.json` verdict reads 'GREEN')

~~~text
**MAJOR-3 (open, orchestrator's file): PROGRESS.json has not been refreshed.** A reviewer attesting HEAD today gets RED from 15 staged-class drifts:
~~~

## 4 · What this document is not

- Not a fix list: nothing here was fixed by the CLOSE, and no registered number moved.
- Not a verdict: no finding changes a row of §0; the verdicts are the scorer's (scores/S0_VERDICTS.md).
- Not a promotion: a candidate for a new registration named here is post hoc and is the operator's to order or refuse.
