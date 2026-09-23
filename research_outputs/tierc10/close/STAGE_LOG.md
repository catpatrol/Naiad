# TIER-C10 · §1 STAGE LOG — the lines LAW 6 owed the draft

> **REPORT-ONLY.** A ledger reprint, not a result: no registration is scored, no
> verdict file is opened, no bar is read. These are append-ready lines for
> `research_outputs/tierc10/BUILD_DRAFT.md` §1 (LAW 6: "after EVERY stage: commit + update
> … PROGRESS.json … + one line to the draft"). The script that printed them does not edit
> the draft; they move into §1 at CLOSE.

- **Inputs (read-only):** `research_outputs/tierc10/PROGRESS.json` sha256 `0d66f2d7fe6c338339880368ff854e58bbb2533be54cf2f7448f71d129752afc` (15 stages) · `research_outputs/tierc10/BUILD_DRAFT.md` sha256 `1ec7b93c5b4590ded7aa7f02621938b101001df9ccdd25c2ef808338a554fa97` (§1 holds 5 lines) · `git log --grep='^tierc10' --format='%h %cI %s'` (28 commits; 25 after `f97cded`, 0 of them already in §1).
- **A stage line's commit** is the oldest commit from which the stage's `one_line` has stood VERBATIM in every committed `PROGRESS.json` through the newest (a text filed earlier, replaced, then restored counts from its restoration; `R0_ADDENDUM.md` §E shows every committed ledger). `uncommitted` = the line is in no committed ledger.
- **A commit line** is the commit's subject verbatim, split at `tierc10(<scope>): ` into label and text.
- **Format:** `` - **<stage>** · <commit ISO date> · <one_line verbatim> (`<short sha>`) ``.

## A · The ledger — one line per PROGRESS.json stage (15), in ledger order

*REPORT-ONLY — the ledger's own words.*

- **STEP 0** · 2026-09-22T15:34:14-03:00 · STEP 0 COMPLETE-VERIFIED — pins reconcile PINS-OK 12/12 (Pine v2 ≡ twin/engine ≡ analytics port, key order included: TOUCH_EPS 0.60 / DEV_RETURN_BARS 7 / BREAK_CONFIRM_N 8 / SCALE_MULT 3.0 / ATR_LEN 14); scripts/tierc10_rf_fixtures.py re-ran NOW exit 0, 7/7 GREEN, zero red legs; transcript FIXTURES_RF.txt byte-reproducible (c6d10b8e… before == after == after a 2nd run, no drift); Q-R5 attestation HOLDS (no RangeFinder constant inherited from the SS Breakout Scanner, whose source is not in this repo at all); the Argus note's 0.67 / DEV_RETURN 8 has NO on-disk source anywhere — the only 0.67 in the lane is the fixture's own deliberate sabotage plant. (`3453c87`)
- **D-CORE** · 2026-09-22T15:34:14-03:00 · the four RESUME clauses now exist: CONTRACT_SPECS.json (multipliers; 1000PEPE and 1000BONK per 1000 tokens; normalization proven a pure scaling to 1.07e-11 over 180,013 bars), F-D-4 two-token trap (102 cells, 0 pre-floor bars), F-D-5 data-spend audit (never-touched = PUMPFUN, MNT, SUI), and the tiered haircut twin as an ADDED column. PARTIAL because F-D-1 stays RED pending an operator ruling. (`3453c87`)
- **CENSUS-R{4h,1d}** · 2026-09-22T15:34:14-03:00 · [Q-R3] height-vs-toll and [Q-R4] the acceptance head-to-head are BUILT, and the verdict is filed PER ERA (360 rows, not 120). [Q-R3] is a GATE per LEDGER.md:834, not a table: PASS per era ALL 9 / tuning 13 / holdout 7 of 120. (`3453c87`)
- **NULL/gaps-only** · 2026-09-22T15:34:14-03:00 · NULL/gaps-only COMPLETE-VERIFIED: 4/4 root + 255/255 cell content-shas re-hash MATCH (null_summary d586ba11fdf591c9, grid 74,844 rows, summary 21,384 rows, coverage 1,020 rows, K=20, seed 20260921, PANEL17 x {5m,4h,1d} x frozen3.0); tierc10_null_fixtures.py re-run NOW exits 0 with 6/6 GREEN and ZERO red legs in 485.4s; FIXTURES_NULL.txt byte-identical before and after (8673449481879822…, no drift); every item-4 number reproduces from the parquet (identity 1020/1020 True; 36.368768% / 19.170590% / 12.564398%; own-window 25.618979%; 4h tap89 +0.316799 vs +0.051663 [q25 -0.033036, q75 +0.232937] pctile 90, 1d flip-hold +0.736139 vs -0.120852 pctile 100, 5m DIE -0.819567 vs -0.808219 pctile 40); is_the_contract_null=False is the HONEST reading — only frozen3.0 was commissioned where the module (and the census) require both scale kinds; no artifact carries a verdict or p-value column. (`3453c87`)
- **NULL/gaps+order** · 2026-09-22T15:34:14-03:00 · NULL gaps+order: 259/259 artifact shas re-hash MATCH, shape/commission exact (21,384 / 74,844 / K=20 / PANEL17x3x frozen3.0 / seed 20260921 / summary sha 03a1bffe70d1fd5e), suite re-run NOW exit 0 6/6 GREEN in 483.70s with zero drift in FIXTURES_NULL.txt, and all of item 4's numbers reproduce from the parquet — COMPLETE-VERIFIED; the two variants' verdicts disagree on 3,455 of 19,926 comparable summary cells (sign) and 2,469 (q75 clearance), including one of the four headline cells (5m DIE ALL H20 net), which is APOLLO's ruling to make, not a defect. (`3453c87`)
- **A (stamps)** · 2026-09-22T15:34:14-03:00 · STAGE A — TAPE + STAMPS: COMPLETE-VERIFIED. 8/8 manifest shas re-hash MATCH; suite exit 0, 9 GREEN / 0 RED, 30/30 break legs correctly RED, 14.18 s; F-DET ran against a present byte-identical twin; all six contract stamps present and none all-null; transcript byte-stable across two runs (no drift). Non-blocking findings: manifest's census_code_sha and panel_code_sha are STALE vs disk (upstream edited after the manifest sealed) and the suite cannot see it — but a scratch rebuild under current code reproduces all 8 tables BYTE-IDENTICALLY, so no number moved. (`3453c87`)
- **PANEL/gate** · 2026-09-22T15:34:14-03:00 · PANEL stage COMPLETE-VERIFIED: all 8 manifest content-shas re-hash MATCH (canonical and F-DET twin, byte-identical to each other), suite exits 0 in 45.30 s with 22/22 fixtures PASS and 150/150 break legs RED-as-required, zero [BAD] in any real assertion block, F-CTRL/a worst abs diff EXACTLY 0.000e+00 over 12 columns on n=200, transcript re-filed byte-identically (no drift), and NO registration is filed (REG_DIR does not exist) — so Stage B has not begun. (`3453c87`)
- **LANES (B mech)** · 2026-09-22T21:45:01-03:00 · post-filing repair: F-LANES-GATE restated as the post-filing law (registry == the 6 pinned lines; both lane regs open through the filed door; era break RED at [ERA-GUARD]); F-C10-BE NOT RUN per P-BE-1 §9 from an outcome-free BE_LATCH_CENSUS.json; converse/agree/closing-check defects fixed so the leg cannot be driven GREEN falsely; 15/15 twice, byte-identical. (`899d3e7`)
- **BRK (B mech)** · 2026-09-22T21:45:01-03:00 · real F-C10-HOLD runs in each form's FILED era (S1 5m holdout, I1 1d full, both anchors): 3 detector-level holds per case named by a blind printed rule and hand-verified, 1 real failed hold per case FAILs, plus a FILED-BOOK hand check through the permission gate; rows built SEALED from the filed arms (require_arm first) with own-era [Q-R3] verdict, Tier-E other anchor, 17-asset view, TOLL_ACCOUNTING; seal is a typed allowlist. 20/20 twice; --ready byte-identical twice. The toll print-vs-deduction question stays OPEN (operator). (`899d3e7`)
- **F-C10-RESUME** · 2026-09-22T15:34:14-03:00 · the fixture that makes the LAW OF RESUMPTION checkable. The anchor looks both ways at two levels; an admission that reached the commit record may not be withdrawn by an uncommitted edit; the artifact of record is tracked and anchored on its own blob. (`3453c87`)
- **D-5M** · 2026-09-22T21:45:01-03:00 · all 17 5m tapes exist and re-hash against STAGE_D_MANIFEST.json; offline suite 17/17 twice; every 5m reader cuts at the pin (17/17 tapes; the uncut tierc2 loader is the sabotage); PARTIAL only on F-D-1's operator question, same as D-CORE. (`899d3e7`)
- **CENSUS-R{5m}** · 2026-09-22T21:45:01-03:00 · 119 files / 102 content shas / 17 input shas re-hash; census suite 14/14 twice; null 5m cells both variants 3/3. The 5m height-vs-toll gate FAILS 0/17 (carried on P-BRK-S1's row). (`899d3e7`)
- **B-REG (the six filed)** · 2026-09-22T21:45:01-03:00 · commit 371123f filed the six registrations (registry len 6, head 7621a857…, m = 6); this stage records the texts of record, the tracked pin and the gitignored registry files so they are re-hashed, and the scoring driver's record fixture re-passes 16/16 twice, byte-identical. No registration is scored here. (`899d3e7`)
- **B-CORE** · 2026-09-22T21:51:01-03:00 · B-CORE scored through the filed doors against the pinned dry-run: P-GEN-1 NOT SUPPORTED (UNSEEN12 +0.0998 R, CI [-0.155, 0.316], LOAO 0/12); P-SPR-2 NOT SUPPORTED (-0.0059 R, CI [-0.175, 0.165], LOAO 0/5); P-BE-1 HALT (prescribed, §4) — no verdict; P-TRG-2 clause (a) SUPPORTED (Δ vs v6 +0.2577 R, CI [0.109, 0.384], p 0.00525, LOAO 5/5) pending the BH bar; P-BRK-I1 NOT SUPPORTED (n 7, +0.718 R, CI [-0.603, 1.452], LOAO 1/5). Re-score byte-identical. (`ab7306a`)
- **B-5M** · 2026-09-22T21:57:22-03:00 · P-BRK-S1 NOT SUPPORTED — significantly NEGATIVE: holdout CLASSIC5 n 1836, -0.2111 R, CI [-0.298, -0.144], LOAO 0/5 above, 5/5 BELOW; 17-asset view -0.170 R [-0.205, -0.137]; memory-line anchor -0.199 R [-0.335, -0.073]; 5m height-vs-toll (holdout) FAIL. FAMILY (m = 6 declared, 5 run, bar 0.016667): P-TRG-2 is the ONLY row that clears all three clauses — CI lo 0.109 > 0, LOAO 5/5, p 0.005249 <= 0.016667. P-GEN-1, P-SPR-2, P-BRK-I1, P-BRK-S1 NOT SUPPORTED; P-BE-1 HALT (no verdict). (`08a6fce`)

## B · The commit record — one line per tierc10 commit after `f97cded` not already in §1 (25), oldest first

*REPORT-ONLY — the commit record's own words.*

- **tierc10** · 2026-09-22T10:01:02-03:00 · operator rulings R7-R10 — LAW 4, the BRK panel, P-SPR-2, the null of record (`ffdffce`)
- **tierc10** · 2026-09-22T11:50:11-03:00 · Stage D's four absent artifacts, the lanes BE-latch repair, and [Q-R3]/[Q-R4] (`54cfd60`)
- **round 2** · 2026-09-22T12:17:26-03:00 · BRK derives its verdict row from the book; F-C10-RESUME's anchor looks both ways (`d8a6f81`)
- **CENSUS-R** · 2026-09-22T12:38:26-03:00 · the height-vs-toll verdict is filed PER ERA — 360 rows, not 120 (`a58bafc`)
- **BRK** · 2026-09-22T13:07:08-03:00 · each form reads the [Q-R3] verdict for the era it is judged in (`1359d99`)
- **F-C10-RESUME** · 2026-09-22T15:12:56-03:00 · the fixture that makes the LAW OF RESUMPTION checkable (`590989d`)
- **F-C10-RESUME** · 2026-09-22T15:13:12-03:00 · file the transcript of record — 9 GREEN, 0 RED (`80ecca5`)
- **LAW 6** · 2026-09-22T15:23:49-03:00 · the ledger after the repair phase — every suite re-run, five stages advance (`6b15def`)
- **LAW 6** · 2026-09-22T15:34:14-03:00 · the ledger after the repair phase, rebuilt from the committed R0 base (`3453c87`)
- **LAW 2** · 2026-09-22T15:35:21-03:00 · restore the quarantined kill-partial's ledger record (`2e4d959`)
- **F-C10-RESUME** · 2026-09-22T15:35:44-03:00 · move the anchor to the post-repair ledger, deliberately (`54c519d`)
- **F-C10-RESUME** · 2026-09-22T15:36:03-03:00 · re-file the transcript after the re-pin — 9 GREEN, 0 RED (`ad34e6e`)
- **LAW 6** · 2026-09-22T15:36:44-03:00 · the resume stage records no artifact sha — the self-reference does not converge (`2e92972`)
- **F-C10-RESUME** · 2026-09-22T15:36:44-03:00 · re-pin onto the ledger that drops the circular self-record (`41a5070`)
- **F-C10-RESUME** · 2026-09-22T15:36:48-03:00 · transcript of record after the re-pin (`83f5e29`)
- **F-C10-RESUME** · 2026-09-22T15:37:49-03:00 · leg 1 accuses instead of raising when a stage records no artifact (`fa205c8`)
- **F-C10-RESUME** · 2026-09-22T15:37:53-03:00 · transcript of record — 9 GREEN, 0 RED (`74d9b39`)
- **STAGE B** · 2026-09-22T17:03:36-03:00 · the six registrations are FILED — text before result (`371123f`)
- **STAGE B mech** · 2026-09-22T21:45:01-03:00 · F-C10-HOLD real, F-C10-BE NOT RUN per P-BE-1 §9, the scoring driver (`899d3e7`)
- **F-C10-RESUME** · 2026-09-22T21:45:37-03:00 · transcript of record after the Stage B mech ledger — 9 GREEN, 0 RED (`be157e9`)
- **B-CORE** · 2026-09-22T21:48:14-03:00 · the reviewed dry-run, pinned BEFORE any score — 21 arms, one prescribed HALT (`b29774e`)
- **B-CORE** · 2026-09-22T21:51:01-03:00 · five registrations scored against the pinned dry-run — one SUPPORTED on (a), one prescribed HALT (`ab7306a`)
- **F-C10-RESUME** · 2026-09-22T21:51:26-03:00 · transcript of record after B-CORE — 9 GREEN, 0 RED (`dc30015`)
- **B-5M** · 2026-09-22T21:57:22-03:00 · P-BRK-S1 scored, the family finished at m = 6 — P-TRG-2 alone clears all three clauses (`08a6fce`)
- **F-C10-RESUME** · 2026-09-22T21:57:30-03:00 · transcript of record after B-5M — 9 GREEN, 0 RED (`2416a15`)
