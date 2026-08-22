# ROTATION LOG

Append-only record of build documents moved off the exchange bus by
`scripts/rotate_reports.py` (queue 003, D-1). Every entry is a MOVE:
the file is still tracked, still on GitHub, and `git log --follow`
still returns its full history at the new path.

PROVENANCE OF THE 2026-08-15 BLOCK (queue 005 M4, gate 0). Those eight lines were
NOT written by the scheduled sweep. They are a **named-set early rotation**,
operator-ratified 2026-08-15: the CENSUS-2A contract is SPENT, so its eight run
documents were moved three days after they were written rather than after the
pinned 30-day window. `rotate_reports.py --dry-run` on the same day selected
**0 candidates / 93 too young**, which is the correct behaviour and was left
intact -- `AGE_DAYS = 30` was not widened, not flagged, not touched. The named
set was driven through the same D-1 semantics by importing this module's own
primitives (`sha256_file`, `git`, `append_log`), so the hash discipline and the
move-never-destroy invariant are the same code, not a re-implementation.
`CENSUS2A_CLOSEOUT_2026-08-12.md` was deliberately excluded and stays on the bus:
it is the pickup document.

| rotated | file | new path | sha256 |
|---|---|---|---|
| 2026-08-15 | `BUILD_2026-08-12_CENSUS2A_RUN_1.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_1.md` | `4eb5beb21c1771fcbc71805af0ba7aedc1478d23098f99b00e4e73dcd9f90485` |
| 2026-08-15 | `BUILD_2026-08-12_CENSUS2A_RUN_2.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_2.md` | `fef8adc86fa6b9ed0ef0909075c3482a4cf884286bcade5d5b31f5c24c526b99` |
| 2026-08-15 | `BUILD_2026-08-12_CENSUS2A_RUN_3.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_3.md` | `2de36f28d23713e7d93ee72adb97544431cb64e62c636de486dcacddacfa782e` |
| 2026-08-15 | `BUILD_2026-08-12_CENSUS2A_RUN_4.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_4.md` | `a29bcb890f308a8703c60202dc93d8f59da686b5ca092d816dea2ebacf245025` |
| 2026-08-15 | `BUILD_2026-08-12_CENSUS2A_RUN_5.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_5.md` | `0af4b2ba4321157628eeeb86e741327a02c9f94dedf1c447a271f1c29f47be6f` |
| 2026-08-15 | `BUILD_2026-08-12_CENSUS2A_RUN_6.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_6.md` | `4abb0076f020f9e790c0db542aa28009fb96d4ba250b74bcc12d0e5b357f311c` |
| 2026-08-15 | `BUILD_2026-08-12_CENSUS2A_RUN_7.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_7.md` | `473ed3cd411c813cc17c1829a2a7549d95d189250541f936f5d66256ec7ebed7` |
| 2026-08-15 | `BUILD_2026-08-12_CENSUS2A_RUN_8.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_RUN_8.md` | `bd53072ff61ee322554a1c235c2bb6ddb5c64b4761339f923dfeacb90c2f7e46` |

PROVENANCE OF THE 2026-08-22 BLOCK (box-cleanup brief, operator go 2026-08-18; executed
2026-08-22). A **named-set early rotation**, not the scheduled sweep. The operator's
retention law for this sweep is: KEEP-HOT = all of `exchange/status/**` + `LEDGER.md` +
queue items not BUILT-and-spent + a working set named by the operator + the newest NOTE
per lane pair + anything under 14 days old with no nameable successor document. Everything
else rotates.

**FINDING F-2, recorded here because this log is where it will be looked for: the scheduled
sweep is INOPERABLE and has been since 2026-08-15.** `rotate_reports.py --dry-run` on the
real tree does not select 0 candidates -- it **HALTS, exit 2**, before classifying anything:
*"the unacted-inbox exemption has no source ... exchange/DIGEST.md contains no heading naming
an inbox ... six unacted notes are unprotected, the first becoming a candidate 2026-09-03."*
Ruling 007 retired the DIGEST; D-1's exemption input died with it. The script is behaving
correctly -- it refuses to guess rather than rotate an unacted note -- but the consequence is
that **no automatic rotation can run at all until the operator rules where the unacted-inbox
list now lives.** `AGE_DAYS = 30` was NOT widened, NOT flagged and NOT touched by this sweep.
Reported, not fixed: the fix is a queue-003 amendment, which ATHENA drafts and the operator
ratifies. 0

The named set was driven through D-1 semantics by importing this
module's own primitives (`sha256_file`, `git`), so the hash discipline and the
move-never-destroy invariant are the same code, not a re-implementation. Queue work orders
land in `docs/history/queue/`; reports keep D-1's `YYYY-MM` date bucket, so four
2026-07 documents land in `docs/history/reports/2026-07/` rather than all in one folder --
that is what makes the layout reproducible by the script later.

| rotated | file | new path | sha256 |
|---|---|---|---|
| 2026-08-22 | `001_condensed-project-history.md` | `docs/history/queue/001_condensed-project-history.md` | `736142faee1b55d006239dba78a6f4582973f10e28dff725272d7f88a5eb88bf` |
| 2026-08-22 | `002_backup-and-publish-guards.md` | `docs/history/queue/002_backup-and-publish-guards.md` | `ba38bee14054ed18889f59d095c542dc2d3ebc725562858fb0c22d256041f9fa` |
| 2026-08-22 | `004_move-clone-out-of-onedrive.md` | `docs/history/queue/004_move-clone-out-of-onedrive.md` | `85d902df3a20a88b875b3cbcc7fee227aa8e39009ecc9cd965806d6c9fe78e79` |
| 2026-08-22 | `2026-08-03_WF1_winner_forensics_APOLLO.md` | `docs/history/queue/2026-08-03_WF1_winner_forensics_APOLLO.md` | `0d47beb784aefd9729c261199d086aac6b56fbaa52e6f57df958ba9722e9782a` |
| 2026-08-22 | `2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md` | `docs/history/queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md` | `f962705ce1ac4ae1724810a4115b599c23430beb35608b010330cd497681fb29` |
| 2026-08-22 | `2026-08-06_MC1_may26_program_APOLLO.md` | `docs/history/queue/2026-08-06_MC1_may26_program_APOLLO.md` | `2411b76d08676568f3c4d865bd46027c2637d8d3a278639a040c3012bee603a9` |
| 2026-08-22 | `2026-08-12_CENSUS2A_v0.3_RESOLVED_APOLLO.md` | `docs/history/queue/2026-08-12_CENSUS2A_v0.3_RESOLVED_APOLLO.md` | `5cd8ab57a1501607f43f6e60e2c702d2c0fe6fd85eef2e86187cb12f29189c2b` |
| 2026-08-22 | `2026-08-16_BR1_brief_redesign_ARGUS.md` | `docs/history/queue/2026-08-16_BR1_brief_redesign_ARGUS.md` | `d153ad518aa53059fd588b94a57c948a5e78494e45d61aa9d01c63331a4dceba` |
| 2026-08-22 | `2026-08-16_BR1b_oracle_topup_ARGUS.md` | `docs/history/queue/2026-08-16_BR1b_oracle_topup_ARGUS.md` | `c8c85d5ed78e762fbb4fd64cf18f03b817d6e7cc6c0a7d3b2a011469dc700101` |
| 2026-08-22 | `2026-08-02_HEPHAESTUS_report_ai-operating-system.md` | `docs/history/reports/2026-08/2026-08-02_HEPHAESTUS_report_ai-operating-system.md` | `574bb9ac40e994f1b9fecd2aa996d8cdaf4e8f666e04c4c71f0867f1e1c2daa7` |
| 2026-08-22 | `2026-08-02_HEPHAESTUS_report_backup-catchup-and-reminders.md` | `docs/history/reports/2026-08/2026-08-02_HEPHAESTUS_report_backup-catchup-and-reminders.md` | `24b7e17346b092479defc7023c5694c0bb557585156762c6a5418780d4e38d67` |
| 2026-08-22 | `2026-08-02_HEPHAESTUS_report_coverage-and-identity.md` | `docs/history/reports/2026-08/2026-08-02_HEPHAESTUS_report_coverage-and-identity.md` | `cdddf08cc388fc3cd384360f4c2c0eb756549d0995cc7a1e70d7e1a7a24187c2` |
| 2026-08-22 | `2026-08-02_HEPHAESTUS_report_disposition-inventory.md` | `docs/history/reports/2026-08/2026-08-02_HEPHAESTUS_report_disposition-inventory.md` | `464025f381ea3197220e2fca083822bd782d5875d1ca8efd82b9a4494e241045` |
| 2026-08-22 | `2026-08-02_HEPHAESTUS_report_exchange-slimming.md` | `docs/history/reports/2026-08/2026-08-02_HEPHAESTUS_report_exchange-slimming.md` | `b452a883d2d2568ba6131979420c8605e5b47301d407b37d18c01b18ee92d84d` |
| 2026-08-22 | `2026-08-02_HEPHAESTUS_report_exchange-v1-build.md` | `docs/history/reports/2026-08/2026-08-02_HEPHAESTUS_report_exchange-v1-build.md` | `0c82fd4b2ac6096786eb824f860673fe4a934fa403203bc83f092dc3c5e8ec20` |
| 2026-08-22 | `2026-08-02_HEPHAESTUS_report_tc5-archive-and-scaffolding.md` | `docs/history/reports/2026-08/2026-08-02_HEPHAESTUS_report_tc5-archive-and-scaffolding.md` | `c1e101a32a1b39b05de5dbb10ec586b3cb1d05289724344ee284f2b9cbf87c39` |
| 2026-08-22 | `2026-08-03_HEPHAESTUS_report_retention-fix-and-alarm.md` | `docs/history/reports/2026-08/2026-08-03_HEPHAESTUS_report_retention-fix-and-alarm.md` | `ca7d9f9ef1cb596277c0f2091b908052f8d01799f24f0c09daa2204926829cea` |
| 2026-08-22 | `2026-08-04_ATHENA_handoff_orphan-data-files.md` | `docs/history/reports/2026-08/2026-08-04_ATHENA_handoff_orphan-data-files.md` | `8883f55d0543468f641d4d76f8bc445aa421e4fb9e2a06732d44e40d968dc662` |
| 2026-08-22 | `2026-08-04_ATHENA_s3-journal-restore.md` | `docs/history/reports/2026-08/2026-08-04_ATHENA_s3-journal-restore.md` | `d484f606694346c92c5ec8e361a869136b59792c46c5a96f8ef4fb0fdff63115` |
| 2026-08-22 | `2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md` | `docs/history/reports/2026-08/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md` | `acf8353bfe6d4832ec65adadab6550dcfacde8375b3d6b490731d50091c4e920` |
| 2026-08-22 | `ACCEPTANCE_MEMORY-RESTRUCTURE_2026-08-03.md` | `docs/history/reports/2026-08/ACCEPTANCE_MEMORY-RESTRUCTURE_2026-08-03.md` | `39e700bdd0090b8eb545d7a033185397a6a9261ccbdb4a889ff59a32c3d06deb` |
| 2026-08-22 | `APOLLO_LANE_STATUS_2026-08-15.md` | `docs/history/reports/2026-08/APOLLO_LANE_STATUS_2026-08-15.md` | `d936ba84a4b1017df7efdeceb13af7da57d953e2dc5161dcb4afaa2101519e4a` |
| 2026-08-22 | `APOLLO_LANE_UPDATE_and_CENSUS2_STATUS_2026-08-12.md` | `docs/history/reports/2026-08/APOLLO_LANE_UPDATE_and_CENSUS2_STATUS_2026-08-12.md` | `78cd04bfad915900022709c344c05bdf52d35c9c8d740120860e5a41d156a98f` |
| 2026-08-22 | `ARGUS_PANTHEON_REPORT_2026-08-06.md` | `docs/history/reports/2026-08/ARGUS_PANTHEON_REPORT_2026-08-06.md` | `7b33d084b99eb8f9180158c67e785742550d148b2aec664f406fa99512969535` |
| 2026-08-22 | `ATHENA_STATUS_2026-08-01.md` | `docs/history/reports/2026-08/ATHENA_STATUS_2026-08-01.md` | `af1cffaeb5d233ab7abc6de2bab28a87413fa5fb77d818318607c866d126797d` |
| 2026-08-22 | `BACKUP_BUILD_2026-07-28.md` | `docs/history/reports/2026-07/BACKUP_BUILD_2026-07-28.md` | `f7f327fa31e58b35140f9203b6c06fa6f8429d81d9c1222ebaf4d5ff7b6f3506` |
| 2026-08-22 | `BRIEF2_CALIBRATION_2026-08-05.json` | `docs/history/reports/2026-08/BRIEF2_CALIBRATION_2026-08-05.json` | `29763231e9811f9351f24751ecd8ed432222b81cff0064554598765b368b0458` |
| 2026-08-22 | `BRIEF_ARGUS_PINE_SSV12T_2026-08-16.md` | `docs/history/reports/2026-08/BRIEF_ARGUS_PINE_SSV12T_2026-08-16.md` | `861c3643c3254e28562b2636e923c4b8bc7f38dd974ee6faab39d18dc64c2cc7` |
| 2026-08-22 | `BUILDERS_REPORT_APOLLO_2026-08-03_WF1.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_APOLLO_2026-08-03_WF1.md` | `263242aa58f012cce7a7c2fa71b631181e0d7786f83b813362ec6c97930a5a23` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-03_CONVENTIONS.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-03_CONVENTIONS.md` | `5511c487148ea7a209d2ab05b58e691d6f686463a4967c11163906895c40d9f4` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-03_T4-SNAPSHOT.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-03_T4-SNAPSHOT.md` | `13cef6853b7159eb230d786f870b51f2eb96cd13cc98fa17deb01de96b1b5e0d` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-03_WRAPUP.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-03_WRAPUP.md` | `6fa7f8f357c08ae15a33fc696f393c8e6bc541fecd67c237d6a07f39a82d85dc` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-04_ANALYTICS-ARCHIVES-AND-EXCHANGE-SIZING.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_ANALYTICS-ARCHIVES-AND-EXCHANGE-SIZING.md` | `a1c50edbad20c07589a2f6dc0145c31d89716e706394a1d7e7969b19958107d3` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-04_ARCHIVE-VERIFY-AND-QUEUE-002.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_ARCHIVE-VERIFY-AND-QUEUE-002.md` | `b7b03c82d2cd36c6d497ce77fd389c39cc082eebf590a0f7dcb3b9f2f6946001` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-04_CONVENTIONS-MERGE-AND-ARCHIVE-AUDIT.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_CONVENTIONS-MERGE-AND-ARCHIVE-AUDIT.md` | `0a978416d28c78c5350b85d4a0371fcf9a06b98f87ec483cf2cbed666a238101` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-04_EXCHANGE-GUARD-ENFORCEMENT.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_EXCHANGE-GUARD-ENFORCEMENT.md` | `613079f6a657afdc5f39bf8b41d40215313333af7ce58419f94e76d79006ab62` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SEQ8.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SEQ8.md` | `52965917430f1038b044d7996112375f9baeb69d23fccbfa8e8fe5ffbdeaef76` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SIDECARS-AND-LANE-CLOSE.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SIDECARS-AND-LANE-CLOSE.md` | `c6f017bb75ca07386213d51135be9acbba594830f8348b02c7c6d12aee659392` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-04_TC5-OFFSITE-AND-PHASE-MODE-READ.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_TC5-OFFSITE-AND-PHASE-MODE-READ.md` | `e92ec1f8d8ec70ed53c7e677ccf38a5c27d6cb600373a4246ee13f6cd122228a` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-06_ARCHIVE-RELOCATION-D.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-06_ARCHIVE-RELOCATION-D.md` | `e1809c325d81969f9c3058aa6e62e07c1567b4684bb8543d9e55827d980274d9` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-11_BULK-RELOCATION-SEQ8-UNARCHIVED.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_BULK-RELOCATION-SEQ8-UNARCHIVED.md` | `4a5d30ac28ca89ba5e063908d59435e55e3f0d53d458c56e516502be0e1d9c61` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-002.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-002.md` | `b5823b475299fd2c5633c9027501848c64c2e382af8b7532d8d53481e2ab4945` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-003-FILED.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-003-FILED.md` | `827e736e7adaf12a3211f80253fe62947ae97ddd5c32b6dfaaae515bd4fcad1d` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-003-RATIFIED.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-003-RATIFIED.md` | `78d761f19880a06068d9cea39e93ccf3a999c5111719c213b7c665d76f0c809d` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-003.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-003.md` | `8df8f0cd9837cfe2a3a5a714330cf3c5ba8a677514e62ef5e92c3ec3efe08e73` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-11_R1-R2-R3.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_R1-R2-R3.md` | `0241fed64089867c766d0102f08c91b86e9348276ed5b9f0d0fbdbbd35c5ea1c` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-12_BACKUP-PATH-REROUTE.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_BACKUP-PATH-REROUTE.md` | `f9c55c7b36b09ca4ad4ca22bf01b51fa9537e7f16ab59f72e8222455d4db013d` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-12_CLOSEOUT.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_CLOSEOUT.md` | `4c37f6644a2aa0f48934e0cda5a3f7dee981b1be331f8dac1de9c3126387f064` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-12_FILE-UNTRACKED.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_FILE-UNTRACKED.md` | `148c9f1224b1fbdf322aa6dd8634e89efb551128f24d580ae9283c2ed8547030` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-12_O1-O3-O4-TIDY.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_O1-O3-O4-TIDY.md` | `0bc107719b8c1b8c075d489f2b4efa2b726b1efa2e0fbeff2fedb23426b3a86d` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-12_ONEDRIVE-CENSUS.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_ONEDRIVE-CENSUS.md` | `3d17b50d1a738461aab8cb4b3d1d33ff74d3c89198395ca67d8605a0ab096605` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-12_PHASE-0.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_PHASE-0.md` | `e0361a2c5f9a6b7eaca6bee37147d7629fdf70ac6d0513f9810eec7f753f23f9` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-FILED-AND-D0A.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-FILED-AND-D0A.md` | `1208bcd5597855bdc3411c378041fec00df28755bda569928b54a8939c4b3ce6` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-HALT.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-HALT.md` | `9b4bee4cfacc210399f49f142723193df421188047250aadf3913830493299a6` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-PHASE-A.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-PHASE-A.md` | `b6cc80557b197195457247e712e9c58f6300e2c0dc5ff73fb377a594abd201b6` |
| 2026-08-22 | `BUILDERS_REPORT_HEPHAESTUS_2026-08-14_M2-RESTORE.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-14_M2-RESTORE.md` | `3c4ab61dbb2f731bab5a5df69aeb6c75ec27fb30353b80f64ceba7df5cd94c7f` |
| 2026-08-22 | `BUILDERS_REPORT_HERMES_2026-08-05_FIRST_RUN.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HERMES_2026-08-05_FIRST_RUN.md` | `812c6fa11ddc3429530ccfbee4848f2267ded60306196b4316f0ad082d4c1f86` |
| 2026-08-22 | `BUILDERS_REPORT_HERMES_2026-08-12_CYCLE.md` | `docs/history/reports/2026-08/BUILDERS_REPORT_HERMES_2026-08-12_CYCLE.md` | `3d46b2813ce7a21c6b1368f9aca30661a680a65a531840efacd16c20e157da88` |
| 2026-08-22 | `BUILD_2026-08-12_CENSUS2A_PASTE1.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_PASTE1.md` | `40df86678783d6ce239e2d756484db8a7c4778606840feab79034836c915609a` |
| 2026-08-22 | `BUILD_2026-08-12_CENSUS2A_VIZ1.md` | `docs/history/reports/2026-08/BUILD_2026-08-12_CENSUS2A_VIZ1.md` | `085797128636dc3299fa71425742d91deafe500af4bc609e5363b0cf57985c98` |
| 2026-08-22 | `BUILD_APOLLO_2026-08-06_MC1.md` | `docs/history/reports/2026-08/BUILD_APOLLO_2026-08-06_MC1.md` | `c9d1973a168c8ae6bbda23dd3a12f32e02ca7bf2e643de1b055a561268815dff` |
| 2026-08-22 | `CENSUS2A_CONTRACT_DRAFT_v0.2_2026-08-12.md` | `docs/history/reports/2026-08/CENSUS2A_CONTRACT_DRAFT_v0.2_2026-08-12.md` | `34ae7989085e956f9e010ab49f46d1a509c35424f7af5dbe8ad7a6e6d6d24d23` |
| 2026-08-22 | `CENSUS2A_CONTRACT_v0.3_RESOLVED_2026-08-12.md` | `docs/history/reports/2026-08/CENSUS2A_CONTRACT_v0.3_RESOLVED_2026-08-12.md` | `b0da051b894fc8586fab466fcf99cb0390763551d0d67bbac83743abc1547a6a` |
| 2026-08-22 | `CONTRACT_V4_2026-07-28.md` | `docs/history/reports/2026-07/CONTRACT_V4_2026-07-28.md` | `2af9167bdf4733b085bf206e5bd93b5d7290b1aabfa72a31bf5d692ebcdcf514` |
| 2026-08-22 | `DESIGN_BRIEF_CENSUS2A_VIZ_2026-08-12.md` | `docs/history/reports/2026-08/DESIGN_BRIEF_CENSUS2A_VIZ_2026-08-12.md` | `9baa5a4e105b93cfc9b761bb2083a73cb67296b4306636c335494a93ae0a49a5` |
| 2026-08-22 | `EXCURSION_EPISODES_2026-08-06.json` | `docs/history/reports/2026-08/EXCURSION_EPISODES_2026-08-06.json` | `b95d4a7a3294176a0e5fa5972e5bd504d44c5246d34228b4e3be764584d1b951` |
| 2026-08-22 | `FIXUP_2026-07-28.md` | `docs/history/reports/2026-07/FIXUP_2026-07-28.md` | `ef8d7cacc9086325b1dbf77a73559599eac74e4e1fe62823566762fe8f85d0ed` |
| 2026-08-22 | `MC1_results.json.pointer.md` | `docs/history/reports/2026-08/MC1_results.json.pointer.md` | `f6f2678d7b4d965c24f96213317e7e4f3efcd039626a44309afead6a1eb38c18` |
| 2026-08-22 | `MC1_tables.md` | `docs/history/reports/2026-08/MC1_tables.md` | `6e2e2d4d0437e54d638b73b49447afabcdef982d7ab912a0f6b3be365443a6f2` |
| 2026-08-22 | `NOTE_ARGUS_to_APOLLO_2026-08-03_census_candidates.md` | `docs/history/reports/2026-08/NOTE_ARGUS_to_APOLLO_2026-08-03_census_candidates.md` | `9cfdd09434aba20d542f68369a6eef6f25cd9020898382b8feab9d4308929c81` |
| 2026-08-22 | `NOTE_ATHENA_2026-08-12_ALL-LANES_STATUS-REFRESH.md` | `docs/history/reports/2026-08/NOTE_ATHENA_2026-08-12_ALL-LANES_STATUS-REFRESH.md` | `b0e4d65a64f71d106c7f0ca95b5ccc3796347fd08c9d1179d66aa577548c1f9b` |
| 2026-08-22 | `NOTE_ATHENA_2026-08-12_CROSS-LANE-RECONCILIATION.md` | `docs/history/reports/2026-08/NOTE_ATHENA_2026-08-12_CROSS-LANE-RECONCILIATION.md` | `869d899cc2029521bbfd70dde97801d9af31d0c09f06a461bfa43e5a9bf6059d` |
| 2026-08-22 | `NOTE_DIONYSUS_to_APOLLO_2026-08-04_range_detection_scoping.md` | `docs/history/reports/2026-08/NOTE_DIONYSUS_to_APOLLO_2026-08-04_range_detection_scoping.md` | `649e280c58c6dace2571a2ec6766fd5bc53a90a3455bf93a87bc13b8d7f58218` |
| 2026-08-22 | `PUSH_2026-07-28.md` | `docs/history/reports/2026-07/PUSH_2026-07-28.md` | `52c132bbec9f31b8a9ead8b97315c4889d103ab8c52ac7807cb29eae70e6c1a4` |
| 2026-08-22 | `SESSION_SUMMARY_ARGUS_2026-08-06_BOXHYGIENE.md` | `docs/history/reports/2026-08/SESSION_SUMMARY_ARGUS_2026-08-06_BOXHYGIENE.md` | `d82cf505befdf643d3f223629a07e92578832e8335990e8bfcb6665d3dbd2e19` |
| 2026-08-22 | `SESSION_SUMMARY_ARGUS_2026-08-06_C6.md` | `docs/history/reports/2026-08/SESSION_SUMMARY_ARGUS_2026-08-06_C6.md` | `1e5d9353e59a5bfc309fe20af588a9de7424555bbefe88b7c6cd3de2bd529c12` |
| 2026-08-22 | `SESSION_SUMMARY_ATHENA_2026-08-03_MEMORY-SCOPING.md` | `docs/history/reports/2026-08/SESSION_SUMMARY_ATHENA_2026-08-03_MEMORY-SCOPING.md` | `8fc41d535b9bde8fe65265b13379b930f9d6eddae626041491cbad85d1781d31` |
| 2026-08-22 | `SESSION_SUMMARY_ATHENA_2026-08-03_MEMORY-WORKSTREAM.md` | `docs/history/reports/2026-08/SESSION_SUMMARY_ATHENA_2026-08-03_MEMORY-WORKSTREAM.md` | `79a18965541a57f1231a046f40ae8f3dd6bbd151fc54b83876d99d608d58543e` |
| 2026-08-22 | `SESSION_SUMMARY_DIONYSUS_2026-08-04_SEQ_rulings.md` | `docs/history/reports/2026-08/SESSION_SUMMARY_DIONYSUS_2026-08-04_SEQ_rulings.md` | `bd051e621345f86cdb34fb85e22cf9d99340532eb5a2b01c8ff352de623d181c` |
| 2026-08-22 | `SESSION_SUMMARY_HEPHAESTUS_2026-08-04_SEQ8.md` | `docs/history/reports/2026-08/SESSION_SUMMARY_HEPHAESTUS_2026-08-04_SEQ8.md` | `8cfe50791b339a3279532f88b79cb2c31bac9747d4bd85107e885d0c5af2add5` |
| 2026-08-22 | `SETUP_2026-07-28.md` | `docs/history/reports/2026-07/SETUP_2026-07-28.md` | `0469a5e26836acc766e7c89e82fcc638ff563c98a7ffbc858c669ffb04f8b186` |
| 2026-08-22 | `SS_Reassessment_Synthesis_2026-08-03.md` | `docs/history/reports/2026-08/SS_Reassessment_Synthesis_2026-08-03.md` | `9d6e7ea747544561af509bbcc845648fa66367cae8157feec1916b18ab4cbff1` |
| 2026-08-22 | `STATUS_ATHENA_2026-08-11_LANE-CLOSE.md` | `docs/history/reports/2026-08/STATUS_ATHENA_2026-08-11_LANE-CLOSE.md` | `0e759efc31b6f588055e18b501292c553243ad191312fe92435ffaf88b29547b` |
| 2026-08-22 | `STATUS_ATHENA_2026-08-11_LANE-CLOSEOUT.md` | `docs/history/reports/2026-08/STATUS_ATHENA_2026-08-11_LANE-CLOSEOUT.md` | `f0cffd6ee40b2fcffae9bd0279123866df3cdd9b5fcb150a55cc9a2f30284080` |
| 2026-08-22 | `WF1_discriminants.json.pointer.md` | `docs/history/reports/2026-08/WF1_discriminants.json.pointer.md` | `a8665abbfddc85f4b900942ad1d56268e154093888395c8a6ce894d25cf22aab` |
| 2026-08-22 | `WF1_tables.md` | `docs/history/reports/2026-08/WF1_tables.md` | `c6501ddb11289bf5d689acc54fc41ffeae0ccb4940f48b77848919c3ea127025` |
