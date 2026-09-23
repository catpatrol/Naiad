# BUILD — TIER-C10 · "UNSEEN RANGES": TWELVE NEW ASSETS (3 NEVER-TOUCHED, 9 DISPLAY-ONLY), THE RANGE CENSUS, SIX REGISTRATIONS

> **DRAFT.** This document lives at `research_outputs/tierc10/BUILD_DRAFT.md` and moves to
> `exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md` **only at CLOSE**
> (LAW 5: a draft under `exchange/` is not a draft). The filed name keeps the 2026-09-21 date —
> one build, one document, however many sessions.

- **Contract of record:** `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md`
  (sha256 `8a0bf279bcab0f27161a7d965535445807f4e713e77d045b0ba124bc7f803c7a`, 9,441 bytes — equal to
  `PROGRESS.json` `contract_of_record`).
- **Original contract:** TIER-C10, ratified by the operator 2026-09-21.
- **Operator rulings:** `research_outputs/tierc10/OPERATOR_RULINGS.md`, sha256
  `a0a08f8761ce9eab678d42d609d7e6563e749c07a6c33b7b17f9a5c4f31ca907` (re-hashed at draft time, 8,696 bytes).
  **Ten rulings:** R1–R6 of 2026-09-21, recovered verbatim from the interrupted session's transcript after its
  scratchpad was destroyed, and R7–R10 of 2026-09-22, appended in `ffdffce`. `PROGRESS.json`
  `operator_rulings.sha256` still cites `70188a0cc32422be…`, the six-ruling file before `ffdffce`. That record is
  stale (finding §5.10).
- **Drafted:** APOLLO. **Executor:** HEPHAESTUS. **Seed:** 20260921, unchanged across the interruption.
- **AS-OF OF RECORD:** 2026-09-21T16:00:00Z, the last closed 4h bar at the first run's start
  (`PROGRESS.json` `as_of_of_record`, `as_of_last_closed_4h_close_ms` 1790006400000). One corridor governs every
  stage (LAW 4, R7).
- **Substrate:** `/Users/luis/.cache/naiad/snapshots/tc10_20260921`, a frozen copy. The live cache is untouched
  (`PROGRESS.json` `live_cache_touched: false`) because a separate live lane commits to it.
- **Reading rule for this document:** a path in brackets is relative to `research_outputs/tierc10/` unless it
  starts with `exchange/`, `scripts/`, `engine/`, `LEDGER.md` or `/`. Every number is read from the file and field
  cited beside it. Where a figure is rounded, the rounding is stated. "Tier-E" means report-only: the row gates
  nothing and holds no slot in m.
- **SIZE — named, as CONVENTIONS §3.2 asks.** This document is over `FLAG_BYTES` = 64,000 B
  (`scripts/publish_exchange.py:160`). Its intended home is `exchange/reports/`. The full CLOSE fragments it
  condenses stay under `research_outputs/tierc10/close/` and are cited by path and sha256 (CONVENTIONS §4.2 pointer
  rule).

---

## 0 · VERDICTS

**THE TWO OUT-OF-SAMPLE TESTS FAILED; ONE IN-SAMPLE CELL CLEARS ITS OWN BAR.**
- **The out-of-asset test did not clear.** P-GEN-1 (card v6 on the twelve admitted assets the card was not built on)
  is NOT SUPPORTED: +0.099777 R, CI [−0.154991, +0.315921], LOAO 0/12. Its never-touched sub-panel (PUMP, MNT, SUI:
  the three assets F-D-5 finds in no register of this estate) sits **wholly below zero**: −0.232839 [−0.351183, −0.160879],
  LOAO 0/3 above, 3/3 BELOW, and each of the three is negative on its own (§0.2).
- **The time-holdout test failed with its CI wholly below zero.** P-BRK-S1, scored on the holdout era only, reads
  −0.211069 [−0.298366, −0.144105], LOAO 5/5 below.
- **The one clear is in sample.** P-TRG-2 is the one cell the contract pre-named. 196 of its 198 campaigns entered at
  or before TIER-C9's as-of, and their count and net equal the TIER-C9 grid row that selected it (§0.3,
  `[close/P_TRG_2_SEEN_SHARE.json]`).
- **The other two:** P-SPR-2 is NOT SUPPORTED, and P-BE-1 HALTed as its own text prescribes.

The ledger's last word before this tier was "NINE TIERS IN-SAMPLE; NOTHING HAS CLEARED ITS OWN BAR"
(`exchange/status/LEDGER_APOLLO.md:2422`). After this tier it reads: **TEN TIERS. THE OUT-OF-ASSET TEST (P-GEN-1) DID
NOT CLEAR, AND ITS 3 NEVER-TOUCHED ASSETS ALL SIT BELOW ZERO; THE TIME-HOLDOUT SCALPER'S CI LIES WHOLLY BELOW ZERO; ONE
IN-SAMPLE CELL (P-TRG-2, 196/198 SEEN) CLEARS ITS OWN BAR.**

### 0.1 · The six, in order of filing

*One row per registration, its scored arm only. Source for every cell: `[scores/<REG>.rows.json rows[i].score_row]`
of the arm with `scored_in_family` true; `clears_bh_bar` from `[scores/FAMILY.json rows[*]]`; the haircut twin from
`beside.haircut_twin` (rounded to 6 dp). The registry has length 6, head `7621a857…`, order of filing as below
`[REGISTRY_PIN.json]`. A cell-for-cell transcription at source precision is `[close/S0_VERDICTS.md]`
(sha256 `6952417e…`, F-S0-READ 0 differences).*

| # | registration · prior | scored arm · panel · era · ruler | n | point (R / campaign) | 90% CI | verdict under its own text | p · `clears_bh_bar` (bar 0.016667) | LOAO line of record (bar) | equal-asset-risk co-headline | haircut twin |
|---|---|---|---:|---:|---|---|---|---|---|---:|
| 1 | P-GEN-1 · 45% | unseen12-card-v6 · UNSEEN12 · full · vs zero | 286 | +0.099777 | [−0.154991, +0.315921] | **NOT SUPPORTED** — fails (a), (b) and (c) | 0.271682 · false | all admitted: 0/12 above (7) · **never-touched** (Tier-E): n 47, −0.232839 [−0.351183, −0.160879], 0/3 above, **3/3 BELOW** | −0.017156 [−0.182654, +0.159051] | +0.084601 |
| 2 | P-SPR-2 · 45% | standalone vs zero · full corridor · CLASSIC5 · full · vs zero | 261 | −0.005930 | [−0.174617, +0.165338] | **NOT SUPPORTED** — its one clause (CI lo > 0) fails | 0.56036 · false | 0/5 above (3) | −0.002961 [−0.175912, +0.170293] | −0.024325 |
| 3 | P-BE-1 · 40% | be-floor-1R vs card-v6 · CLASSIC5 · full · two-sample | — | — | — | **HALT — NO VERDICT.** Prescribed by its §4/§11: the key set did not move (200 paired, 0 book-only, 0 base-only). | — | — | — | — |
| 4 | P-TRG-2 · 40% | trg-9/12 vs card v6 · CLASSIC5 · full · two-sample | 198 (base 200) | Δ +0.257697 | [+0.108587, +0.383892] | **SUPPORTED** (CI-only). In-sample re-score of a TIER-C9 grid pick; beats a base that does not clear zero (§0.3). | 0.005249 · **true** | 5/5 above (3) | Δ +0.250885 [+0.092816, +0.397402] | Δ +0.258438 |
| 5 | P-BRK-I1 · 35% | CLASSIC5-memory-line · CLASSIC5 · full · vs zero | 7 | +0.718270 | [−0.602912, +1.452261] | **NOT SUPPORTED** — CI, LOAO and BH all fail | 0.269683 · false | 1/5 above (3) | +0.373531 [−0.43831, +1.185371] | +0.894601 |
| 6 | P-BRK-S1 · 30% | P-BRK-S1 vs zero · CLASSIC5 · **holdout** · vs zero | 1836 | −0.211069 | [−0.298366, −0.144105] | **NOT SUPPORTED** — (i), (ii) and (iii) all fail; the CI lies wholly below zero | 1.0 · false | 0/5 above (3); 5/5 below | −0.20761 [−0.292728, −0.144147] | −0.372757 |

**Height-vs-toll on the BRK rows** (`beside.brk_sealed_row.height_vs_toll`):

- **P-BRK-I1**, 1d, era ALL: `verdict_pass` true. "era ALL: height gate PASS + edge-fade leg PASS", n_ranges 53, ratio_median 413.99176955.
- **P-BRK-S1**, 5m, era holdout: `verdict_pass` false. "era holdout: height gate PASS + edge-fade leg FAIL", n_ranges 4584, ratio_median 20.67111284.

**F-D-1 is RED, and the three texts that require it print it RED:** P-GEN-1 §7(c), P-SPR-2 §12 and P-TRG-2 §7(e)
(§3.1, §6 Q1). The score rows carry no F-D-1 field: no `scores/*.rows.json` or `SCORE_*.txt` contains the string
"F-D-1", so the RED is carried by the filed texts, not by the rows above.

### 0.2 · Each row, read under its own text

#### P-GEN-1 [45%] — NOT SUPPORTED

- **The three clauses of §6 all fail, each on its own.**
  - (a) CI lower bound −0.154991 is not > 0.
  - (b) p 0.271682 > 0.016667, so `clears_bh_bar` is false `[FAMILY.json rows[0]]`.
  - (c) The LOAO line of record reads "0/12 above" against a bar of 7. Every one of the 12 leave-out intervals straddles zero `[score_row.loao_detail]`.
  - The excl-zero-campaign count is also 0, and no asset has zero campaigns, so the two counts agree and no weak-evidence clear arises.
  - Not a HALT.
- **Beside the verdict** `[score_row]`:
  - Equal-asset-risk co-headline −0.017156 [−0.182654, +0.159051], p 0.566108. **Its point sign is opposite the raw point.** The row's `co_headlines_disagree` is false only because it compares verdicts, not signs.
  - Sensitivity seed 20260816: [−0.165617, +0.320224], p 0.275181, `verdict_stable_across_seeds` true.
  - D15 trio: degenerate by construction (vs zero), printed as None.
  - Haircut twin +0.084601. With-funding companion +0.067733. No sign disagreement.
- **Per-asset campaigns** `[beside.per_asset_n]`: 1000BONK 12, 1000PEPE 19, BNB 44, DOGE 27, ENA 15, HYPE 4, LTC 43, MNT (Bybit) 18, PUMP 8, SUI 21, UNI 39, XMR 36. No asset has zero campaigns.
- **The positive point rests on one asset.** Figures are from `[beside.per_asset_rows]`, raw panel; shares were computed at draft time.
  - BNBUSDT nets +33.4686 R on 44 campaigns, 117.3% of the arm's +28.5362 R.
  - The other eleven assets net −4.9324 R over 242 campaigns, **by subtraction from the arm's net_r**
    (`score_row.net_r` +28.5362 − BNB +33.4686). Summed directly, the eleven `per_asset_rows` net_r values give
    −4.9323: they are filed at 4 dp, so the last digit differs by rounding.
  - 7 of the 12 assets are net negative.
- **Tier-E views**, which hold no slot in m and decide nothing (§9 of the text):
  - PANEL17: n 486, +0.144608 [−0.021461, +0.30915], LOAO 1/17 against a bar of 9. *"THIS ARM IS NOT A GENERALISATION TEST AND MAY NOT BE READ AS ONE"* (§5): five of its seventeen assets are the ones card v6 was built on.
  - NEVER-TOUCHED (PUMP, MNT, SUI), the contract's second LOAO line: n 47, −0.232839 [−0.351183, −0.160879], LOAO
    "0/3 above, 3/3 BELOW" `[rows[2].score_row]`. **Each of the three is negative on its own:** PUMP −0.4182 (n 8),
    MNT −0.2916 (n 18), SUI −0.1119 (n 21) R/campaign `[rows[2].beside.per_asset_rows expectancy_r]`. The CI lies wholly
    below zero. The text caps what it can carry: *"its N is three: it can support nothing on its own"* (§7(a)). With
    three clusters, each leave-out interval is just the span of the two remaining assets' means
    (`loao_detail`: −MNT [−0.418232, −0.111859], −PUMP [−0.291585, −0.111859], −SUI [−0.418232, −0.291585]). So it
    decides nothing. It is still, in the text's words, *"the only fully out-of-sample count on this registration"*,
    and it points below zero.
  - The ARM 3 ⊂ ARM 1 assertion holds: 47/47 keys equal and not broken `[beside_registration.arm3_is_subset_of_arm1]`.
  - LOAO is printed twice, as the contract asks `[beside_registration.loao_printed_twice]`.
- **Caveats the text itself files:**
  - *"THE PANEL'S NICKNAME IS "THE UNSEEN TWELVE" AND THE NICKNAME IS WRONG. Only THREE of the twelve are never-touched."* F-D-5 classes nine of the twelve as display-only (§3.5).
  - *"So ARM 1 is an out-of-sample test BY THE STRONGEST MEASURE THIS BUILD MADE, and it is NOT a virgin-sample test."*
  - The out-of-sample dimension is the ASSET, not the calendar.

#### P-SPR-2 [45%] — NOT SUPPORTED

- **Its one gating clause fails.** §7: *"SUPPORT, and nothing else, IS THIS: on ARM 1, the 90% percentile CI's LOWER bound on the RAW expectancy is STRICTLY greater than zero."* ARM 1's lower bound is −0.174617. This row fails one clause, not three. LOAO and BH ride beside it, "FOLDED INTO NOTHING".
- **Beside the verdict** `[score_row; FAMILY.json rows[3]]`:
  - p 0.56036, `clears_bh_bar` false.
  - LOAO "0/5 above" (bar 3); excl-zero-campaign count 0.
  - Equal-asset-risk co-headline −0.002961 [−0.175912, +0.170293].
  - Sensitivity seed 20260816: [−0.177197, +0.165338], p 0.563359, stable.
  - D15 trio printed as None with its reason.
  - Haircut twin −0.024325.
- **Refusals are counted, not hidden** `[beside.spring_refusals.total]`: signals 282, entered 261, position_open 21, degenerate_R 0, no_struct_anchor 0, UNEXPLAINED 0. Signals split long 145, short 137, and both directions are traded, per R3 and R9.
- **Tier-E era arms and the union arm.** *"Neither is scored, neither fills a slot in m, and neither may be quoted as the lane's verdict."*
  - Tuning: n 165, −0.149015 [−0.334491, +0.038538], LOAO "0/5 above, 1/5 BELOW" (−SOLUSDT [−0.416667, −0.064412]). By §8, a panel wholly below zero is counted as evidence that the arm is WORSE.
  - Holdout: n 96, +0.239998 [−0.050444, +0.473793], LOAO 1/5; the sensitivity lower bound is −0.104634.
  - Union with v6, against v6: Δ −0.111162 [−0.336613, +0.053526], LOAO 0/5.
  - Source: `[rows[1..3].score_row]`.
- **The holdout arm is NOT out of sample for this lane's signal.**
  - The RangeFinder pins it rides were calibrated on BTC in windows inside the holdout era:
    - `engine/rangefinder.py:112-113`: "KEY-B's L-R1 opens Jul 2025"
    - `:137`: "v1 CALIBRATION OF RECORD 2026-08-22"
    - `:569`: `V2_WINDOW_BARS = 1700 # 4h bars: 2025-11-12 → now`
  - The row's `era_note` carries P-BRK-S1's sentence ("where its tuned pins and its chosen band are out of sample"). That sentence is true for P-BRK-S1 and false for this lane.
  - BTC alone contributes +10.4089 R on n 24 in the holdout, against −10.213 on n 33 in tuning `[rows[2], rows[1] beside.per_asset_rows]`.
  - The only era clean of the calibration window is tuning, at −0.149015.
- **Filed caveats.** The text also files: *"A full-corridor row is therefore a POOL of two populations that disagree in sign"* (§10(b)); *"NOTHING ON THIS PANEL IS FRESH DATA"*; and *"Four of this panel's five assets run pins fitted on the fifth"* (§10(g)).
- **The lane's as-of witness, named as §4 requires: F-RNG-ASOF.**
  - `[census/FIXTURES_CENSUS.txt:80]` PASS: 440 cuts over 10 tape × SCALE runs, 0 mismatches.
  - `[:91]` F-RNG-ASOF-SEAL PASS.
- **The superseded draft.** The contract's wording "4h, 5-asset exploration-classic, vs card/standalone" is the superseded draft (R3, confirmed by R9). The text prints it so the change is visible `[close/S0_VERDICTS.md]`.

#### P-BE-1 [40%] — HALT, NO VERDICT (prescribed)

- **The premise failed, so the scored arm halted as its text says it must.**
  - The two-sample premise requires the campaign-key set to MOVE. It did not: `moved` false, n_paired 200, n_book_only 0, n_base_only 0 `[scores/DRYRUN.json arms[7].keys]`. The floor at +1R moves exits only.
  - `TP.score` HALTed with the string filed at `[scores/FAMILY.json scored_slots_halted.P-BE-1]`: *"HALT: P-BE-1 — the arm shares the WHOLE campaign set with its base; the commissioned two-sample ruler's premise failed. File a NEW id under ruler='set_change' and disclose."*
  - `[scores/FINISH.txt]` reads "P-BE-1: NO SCORED ROW — its scored arm HALTED".
- **No clause was computed.** Clauses (a), (b) and (c) were never evaluated on A1. This is **not** NOT SUPPORTED: the floor's effect on the scored book was never measured.
- **The filed text prescribes exactly this** `[scores/P-BE-1.rows.json rows[0].text_prescribes]`:
  - *"If it does not move, this registration does NOT quietly become the narrower paired row — it HALTs. That HALT is part of the claim, and it is why the ruler is registered rather than left to the scorer."*
  - *"If A1's two-sample premise fails and A1 HALTs, there is no report-only row on the same population to read instead; a new id must be filed under `set_change` and the reason disclosed."*
- **Tier-E arms** `[rows[1..3].score_row]`. None may stand in for A1 (§11), and *"The two report-only era arms in §11 are thin by construction and nothing may be concluded from either of them"* (§8(8)).
  - A2, tuning: Δ −0.01428 [−0.169724, +0.113622], n 123, LOAO 1/5.
  - A3, holdout: Δ −0.048234 [−0.194894, +0.080484], n 77, LOAO 0/5. *"No pin of this lane was tuned on any era, so the holdout carries no out-of-sample standing here."*
  - A4, pin 2.0 sensitivity: Δ −0.01978 [−0.077213, +0.02383], n 200, LOAO 1/5. It rides the repaired branch and is a different book.
  - All three straddle zero.
- **F-C10-BE: NOT RUN, per §9** (see §1.3).
- **The operator question it raises.** A new id under `set_change` would be a registration *added*. The contract forbids that ("no registration re-worded or added"), so the filing is the operator's to order (§6 Q3). `[PROGRESS.json stages[13].notes[0]]`.
- **Provenance note.** The A1 HALT row carries no key-set counts and no book sha. The "200/200 shared" figure is filed only in `DRYRUN.json arms[7]` (book sha `f72c0815…`, base sha `2bd244bf…`) and in PROGRESS.

#### P-TRG-2 [40%] — SUPPORTED under its own text

- **The deciding clause is CI-only (§5, §8), and it passes.**
  - Lower bound 0.108587 > 0; point Δ +0.257697; upper bound 0.383892 `[rows[0].score_row]`. Nothing else in §5 can change the verdict.
  - Two items are *"REPORTED BESIDE THE VERDICT, AND DECIDING NOTHING"*, and both also clear:
    - LOAO "5/5 above" against a bar of 3. The worst leave-out is −ZECUSDT at [0.070742, 0.276106].
    - `clears_bh_bar` true: p 0.005249 ≤ 0.016667 `[FAMILY.json rows[10]]`, with m declared 6
      `[FAMILY.json family_m_declared]` and 5 run `[scores/FINISH.txt: five verdict rows and one HALTed slot;
      PROGRESS.json stages[14].notes[0] "m stays 6 DECLARED (5 run)"]`.
  - It was final at B-CORE, not "pending the BH bar", which is what `PROGRESS.json` stage 13 says. Print it as "SUPPORTED (CI-only); LOAO and BH beside, both clear", not as a three-clause pass.
- **The premise and the book are right.**
  - The two-sample premise holds: 19 paired, 179 book-only, 181 base-only `[DRYRUN.json arms[11].keys]`.
  - Exactly two fields differ from the control ride: `trg_f` 12→9 and `trg_s` 26→12 `[DRYRUN.json arms[11].trg2_ride_diff]`.
  - The base is card v6 on the same panel and window: base sha `2bd244bf…`, n 200.
- **Beside the verdict:**
  - Equal-asset-risk Δ +0.250885 [+0.092816, +0.397402].
  - Sensitivity seed 20260816: [+0.112037, +0.383892], p 0.004499, stable. **The sensitivity-seed LOAO line reads 4/5**, not 5/5 `[sens_loao_line]`.
  - D15 trio: paired Δ 0.0 [0.0, 0.0] on 19 paired. `max_single_trade_delta_share` is null. *"THE NaN IS NOT A CLEAN BILL AND IT IS NOT AN ADVANTAGE"* (§7(a)). `tail_exit_ratio` 1.2184.
  - Haircut twin Δ +0.258438.
- **The era split** (Tier-E: a *"STABILITY VIEW and nothing more"*, §3):
  - Tuning: Δ +0.188419 [−0.014369, +0.384652], p 0.064484, **NOT SUPPORTED**, LOAO 1/5 `[rows[2]]`.
  - Holdout: Δ +0.484614 [+0.272576, +0.639944], p 0.00025, LOAO 5/5 `[rows[3]]`.
  - **A1 and the era split disagree.** §6 requires the disagreement printed; A1 still governs.
  - The holdout row's `era_note` carries P-BRK-S1's "out of sample" sentence. It does not apply here: *"for THIS registration the label `holdout` is the R1 cut's name, not a claim of out-of-sample."*
- **A2, vs zero** (Tier-E, decides nothing): +0.466414 [+0.171719, +0.892868]. Per §7(d), that question is A2's alone.
- **Read the SUPPORTED together with §0.3.**

#### P-BRK-I1 [35%] — NOT SUPPORTED

- **All three clauses fail, each on its own** `[rows[0].score_row; FAMILY.json rows[14]]`:
  - CI lower bound −0.602912.
  - LOAO "1/5 above" against a bar of 3; only −BTCUSDT's interval is above zero.
  - p 0.269683 > 0.016667.
- **The sample is thin.** n is 7 on 3 of 5 assets: BTC 2, ETH 4, SOL 1; NEAR and ZEC have none `[beside.per_asset_n]`. The excl-zero-campaign count is also 1, so the two LOAO counts agree.
- **Beside the verdict:** equal-asset-risk +0.373531 [−0.43831, +1.185371]; sensitivity seed stable; D15 printed as None.
- **The positive point rests on one trade.** ETH's best trade, +6.1259 R, exceeds the whole book's net of +5.0279 R `[per_asset_rows]`.
- **The 1d height-vs-toll gate on the row reads era ALL: PASS.** The filed text makes the holdout result part of the registration:
  - *"THE GATE IS PASSED ON ERA ALL AND ON ERA TUNING, AND FAILS ON ERA HOLDOUT"*
  - *"The corridor-wide PASS is therefore not evidence that the gate holds on recent bars."*
  - POOLED:CLASSIC5 1d frozen3.0 holdout: FAIL, provisional, 18 ranges, edge NET −0.4360. Tuning: PASS, +0.1537 (§2.1).
- **Era full is not a clean out-of-sample test:** *"THE FULL CORRIDOR IS THEREFORE OUT OF SAMPLE FOR THIS LANE'S CONSTRUCTION AND NOT FOR THE PINS IT RIDES."*
- **Tier-E arms:**
  - The other anchor (band): n 3, +0.351769 [−0.141574, +0.845112], "0/5 above, 1/5 BELOW". It is in sample: its pins were tuned on these assets.
  - PANEL17: n 17 on 8 assets, +0.421903 [−0.112627, +0.988635], LOAO 1/17 against a bar of 9. It carries no height-vs-toll verdict, as filed.
- **Toll.** No toll is stamped on this row (`brk_sealed_row.toll.stamped` false). Its `toll_accounting_status` quotes P-BRK-S1's clause (finding §5.6).
- **The twin exceeds the TC figure because it charges no funding.** Twin +0.894601 against TC +0.718270; the companion with funding is +0.715223.

#### P-BRK-S1 [30%] — NOT SUPPORTED, CI wholly below zero

- **All three §5 legs fail, each on its own** `[rows[0].score_row; FAMILY.json rows[17]]`:
  - (i) The CI [−0.298366, −0.144105] lies entirely below zero.
  - (ii) LOAO line of record (excl-zero-campaign): 0/5 above against a bar of 3. As context, 5/5 panels lie below zero; the worst leave-out is −ZECUSDT at [−0.340222, −0.161607].
  - (iii) p 1.0.
  - Scope: holdout era only, CLASSIC5, n 1836, net −387.5226 R.
- **"Significantly negative" is not a registered reading.** The filed test is one-sided upward. The exact statement is that the CI and 5/5 LOAO panels lie below zero: in §6's words, *"A negative, well-bounded answer on the holdout is a real result and will be reported as one."*
- **Beside the verdict:** equal-asset-risk −0.20761 [−0.292728, −0.144147]; sensitivity seed [−0.287309, −0.143269], stable; haircut twin −0.372757, the same sign.
- **The 5m height-vs-toll gate, era holdout: height PASS, edge-fade FAIL.**
  - Height: ratio_median 20.67111284 on 4,584 ranges. Edge-fade NET −0.5885 ATR at H20 (§2.1). `verdict_pass` false.
  - *"WHICH LEG FAILS MATTERS"*, and the text registers the form knowing this: *"THIS FORM IS BEING REGISTERED WITH ITS OWN FEASIBILITY GATE FAILING ON THE ERA IT IS SCORED IN."* It also says *"It did NOT find an edge."*
- **The toll is a PRINT, not a deduction** `[brk_sealed_row]`.
  - Median toll_pct_of_1r is 17.76028128. Per-asset toll in ATR: BTC 0.46555286, ETH 0.35253641, NEAR 0.20944241, SOL 0.24410209, ZEC 0.23793258.
  - A deduction could only lower every campaign's net_r, so it cannot flip clause (i). Whether to deduct is the operator's call (§6 Q2).
- **Tier-E arms:**
  - 17-asset view: n 6016, −0.170156 [−0.205301, −0.137249], LOAO 0/17.
  - Memory-line anchor: n 1300, −0.198889 [−0.334534, −0.072906].
  - Neither is promoted (`clears_bh_bar` None).
- **Filed caveats:**
  - *"The holdout is out of sample in TIME ONLY."*
  - The band is an executor reading, not an operator ruling: the contract's "(FLIP_HOLD pins)" is a drafting error `[REGISTRATION_PLAN.md:95-98]`.
  - The band was tuned to ribbon127_200, margin 1.0 ATR, hold 3 bars, ttl 400 `[brk_sealed_row.tuned]`.
- **The 5m hold-rate print that §7 promised was never made** (finding §5.4).

### 0.3 · P-TRG-2 — THE SELECTION HAZARD, STATED WITH THE ROW

> **P-TRG-2 is SUPPORTED on its filed ruler and clears the m = 6 bar. It is not independent evidence.** It
> re-measures TIER-C9's finding with a stricter, unamendable apparatus, on almost the same sample.
>
> 1. **The cell was chosen on its p, off a grid run on these same five assets.** Its own text says so: *"THIS CELL
>    CAME OUT OF A SEVEN-CELL GRID RUN ON THESE SAME FIVE ASSETS, AND IT WAS CHOSEN AFTER THAT LOOK"* and *"So the cell
>    was singled out ON ITS p-VALUE, computed on the very seven-cell grid that did the singling out. That is selection
>    on the statistic. Stating it here prices it; it does not launder it"* (§7(a)).
>    - On that grid, trigger-9/12 read n 196, net +94.3989 R, Δ +0.283646 [+0.120596, +0.43569], p 0.002999, LOAO
>      "5/5 above", sharing 19 campaigns with v6 `[research_outputs/tierc9/sweep_grid.parquet]`.
>    - TIER-C9 ruled: *"NO PROMOTION … Under an m = 7 correction the bar would be 0.0143 — trigger-9/12's p = 0.003
>      sits under even that"* (`exchange/reports/BUILD_2026-08-18_TIERC9_HABITAT_PAIRS.md:33`).
> 2. **The sample is almost entirely the same sample:** *"So P-TRG-2 is in large part an IN-SAMPLE RE-SCORE of a cell
>    selected off that grid. What is actually new here is the method, not the data"* (§7(b)).
>    - **The seen share, persisted and fixture-guarded:** `[close/P_TRG_2_SEEN_SHARE.json]` (sha256 `b68083aa…`,
>      60,968 B; `.md` sha256 `5b7ef5d1…`), built by `scripts/tierc10_close_p_trg_2_seen_share.py`; F-SS 9/9 GREEN,
>      every leg with a sabotage RED, run whole twice byte-identical `[close/FIXTURES_CLOSE_p_trg_2_seen_share.txt]`,
>      sha256 `780034a0…`. It rides the scored arm read-only through its registration's door, as the pinned dry-run
>      does. The ridden book's sha `b2276fa4…` equals the dry-run pin (`DRYRUN.json arms[11].book_sha`) and the scored
>      row's `book_sha256`. No score, finish or register is referenced (F-SS-CLOSURE).
>    - **What it finds.** 196 of the 198 campaigns ENTERED AT OR BEFORE TIER-C9's as-of (2026-08-22T00:00:00Z, read
>      from `research_outputs/tierc9/build_manifest.json` and equal to the grid row's `as_of_last_closed_4h`). 0 were
>      open across it. The 196 re-net +94.3989 R. Their n, net_r, gross_r (106.2883), fee_r (6.1309), funding_r
>      (5.7584), best_r (24.8061) and win rate (40.3061%) all **equal the TIER-C9 grid row** for trigger-9/12 at its
>      4-dp precision. Their key overlap with TIER-C9's filed v6 journal (shared 19, cell-only 177, base-only 177)
>      equals the grid's `n_shared` / `n_cell_only` / `n_base_only` (`[P_TRG_2_SEEN_SHARE.json grid_compare,
>      keys_compare]`).
>    - **What it cannot show.** TIER-C9 filed no per-campaign trigger-9/12 journal (its journals on disk are
>      `trade_journal_control` and `trade_journal_p_trg_1`). So this is an aggregate-and-overlap match, **not a
>      key-for-key match** against a TC9 9/12 book. Read "196 were in TC9's grid" as: entered at or before TC9's as-of,
>      with count, net and overlap equal to the grid row.
>    - The corridor spans 2539.3 days on TIER-C9's grid against 2570.0 here `[sweep_grid.parquet as_of_span_days;
>      close/P_AGE_1_TIDE_YOUTH.md]`.
> 3. **Pre-naming did not make it out of sample.** *"What pre-naming does NOT do is make the cell out of sample"*
>    (§4). The 40% prior priced the hypothesis, not the mechanics of re-scoring the same sample.
> 4. **The one unseen month holds too little to test anything.** It holds 2 book campaigns, ZECUSDT
>    2026-08-27T20:00Z (−1.025848 R) and ETHUSDT 2026-08-30T16:00Z (−1.023195 R), both stopped out
>    `[P_TRG_2_SEEN_SHARE.json post]`, and 4 base campaigns `[close/FORWARD_STRIP.md]` (§0.6).
> 5. **The edge sits in the recent era, and "holdout" is only the R1 cut's name.** Before the cut, Δ is +0.188419
>    [−0.014369, +0.384652]: NOT SUPPORTED, LOAO 1/5. After it, Δ is +0.484614 [+0.272576, +0.639944].
>    - The v6 base's own expectancy is −0.010763 before the cut and +0.559314 after
>      `[close/V6_CONTROL_HAIRCUT_TWIN.md, TC-series column]`.
>    - TIER-C9's sweep saw both halves: 64 of the book's 66 post-cut campaigns and 73 of the base's 77 entered at or
>      before TIER-C9's as-of `[P_TRG_2_SEEN_SHARE.json era_cut]`.
> 6. **SUPPORTED means only that it beats a base that does not itself clear zero.** *"a SUPPORTED verdict on A1
>    would establish only that the 9/12 book beats a base that does not itself clear zero. It would not establish that
>    the 9/12 book makes money"* (§7(d)).
>    - v6 against zero on this corridor: [−0.012774, +0.463319], p 0.054486, NOT SUPPORTED
>      `[panel/control_reference.parquet]`.
> 7. **The result is concentrated in one asset.** ZECUSDT carries +52.9031 of the book's +92.3499 R
>    `[rows[0].beside.per_asset_rows]`. Dropping ZEC still leaves the Δ above zero, at [0.070742, 0.276106]. At the
>    sensitivity seed the LOAO line reads 4/5.
> 8. **Only five clusters.** The LOAO bounds repeat across leave-outs: 0.070742 is the lower bound on three of the
>    five `[score_row.loao_detail]`. p 0.00025 on the Tier-E arms is the bootstrap's floor, 1/(B+1) = 1/4001 at
>    B = 4000 (`n_boot` 4000, `[P-TRG-2.rows.json]`; P-BRK-S1's filed text: *"1/4001 = 0.000250"*). Intervals over
>    five clusters are coarse.
> 9. **F-D-1 is RED** (§7(e)).
>
> **What it may be read as.**
> - The only registered cell in ten tiers to clear its own bar (`exchange/status/LEDGER_APOLLO.md:2422`, "NINE TIERS
>   IN-SAMPLE; NOTHING HAS CLEARED ITS OWN BAR"; `[FAMILY.json rows[10]]`), and it clears in sample.
> - A candidate for a genuinely forward test.
>
> **What it may not be read as.**
> - Out-of-sample confirmation.
> - Proof that the 9/12 book makes money.
> - Evidence that trigger swaps help in general: P-TRG-1 (trigger 9/26) failed in TIER-C9, at Δ −0.020525
>   [−0.126834, +0.101122] `[sweep_grid.parquet]`.
> - An unbiased size of the effect. It carries the winner's curse of the cell picked off a grid on its p: the lowest
>   p of the seven (0.002999). It was not the grid's largest Δ point: window-9/89 read +0.386292 against +0.283646
>   `[sweep_grid.parquet two_sample_ci_point, p_one_sided]`.
> - Grounds for any pin refit, card change or SAIL act. The Q6 hold stands.

### 0.4 · The family, and LAW 3's beside-print

- **The family bar.** `family_m_declared` is 6 and `fdr_bar_q_over_m` is 0.016666666666666666, one fixed bar with
  no step-up `[scores/FAMILY.json]`. Five rows were scored in the family and one slot is HALTed.
  - `finish_family` ran with `--allow-halted-slot P-BE-1`, as the filed texts prescribe. P-BE-1 §7: *"CLAUSE (c)
    RESOLVES ON THIS ROW ALONE and does not wait for siblings"*. P-TRG-2 §5: *"at that one fixed bar to EVERY scored
    row it is handed"*. Source: `[PROGRESS.json stages[14].notes[0]]`.
  - **m stays 6 DECLARED: fewer tests never loosen the bar.**
  - `clears_bh_bar` is true on P-TRG-2 alone `[scores/FINISH.txt]`.
- **LAW 3's beside-print is empty by fact.** LAW 3 reads: *"any verdict the interrupted run computed is re-computed and printed BESIDE the fresh value"*.
  The interrupted run filed no registration and so computed no verdict (§R0.1). There is nothing to print beside the
  six.

### 0.5 · The admitted list — printed before any scoring; the twelve are P-GEN-1's panel

*Rule: ≥ TIDE_SLOW (316) + MEM_TTL_BARS (400) = 716 closed 4h bars; excluded: none `[data/STAGE_D_MANIFEST.json
admission]`. The class column is F-D-5 `[data/DATA_SPEND_AUDIT.json]`. The admitted list on disk holds all seventeen.
UNSEEN12 = `panels.UNSEEN_admitted_stems` is the reading under which "the ADMITTED twelve" (contract :90) and "the
ADMITTED LIST … IS P-GEN-1's panel" (:50) agree `[REGISTRATION_PLAN.md:55-58]`. REGISTRATION_PLAN.md:57 cites the
first phrase as "line 92"; that is off by two (line 92 carries "LOAO printed twice (all admitted · never-touched only)").
This panel reading is the executor's, not the operator's, and is put to the operator (§6 Q8).*

| asset | stem | venue | closed 4h bars | F-D-5 class | panel |
|---|---|---|---:|---|---|
| ENA | ENAUSDT | BINANCE_USDTM | 5413 | display-only | UNSEEN12 |
| PUMPFUN | PUMPUSDT | BINANCE_USDTM | 2631 | **never-touched** | UNSEEN12 · lean D-d |
| HYPE | HYPEUSDT | BINANCE_USDTM | 2876 | display-only | UNSEEN12 |
| MNT | MNTUSDT_BYBIT | BYBIT_V5_LINEAR | 6513 | **never-touched** | UNSEEN12 · lean D-c |
| SUI | SUIUSDT | BINANCE_USDTM | 7422 | **never-touched** | UNSEEN12 |
| LTC | LTCUSDT | BINANCE_USDTM | 14684 | display-only | UNSEEN12 |
| XMR | XMRUSDT | BINANCE_USDTM | 14534 | display-only | UNSEEN12 |
| BNB | BNBUSDT | BINANCE_USDTM | 14492 | display-only | UNSEEN12 |
| UNI | UNIUSDT | BINANCE_USDTM | 13167 | display-only | UNSEEN12 |
| PEPE | 1000PEPEUSDT | BINANCE_USDTM | 7410 | display-only | UNSEEN12 |
| DOGE | DOGEUSDT | BINANCE_USDTM | 13586 | display-only | UNSEEN12 |
| BONK | 1000BONKUSDT | BINANCE_USDTM | 6205 | display-only | UNSEEN12 |
| BTC | BTCUSDT | BINANCE_USDTM | 15420 | scored | CLASSIC5 |
| ETH | ETHUSDT | BINANCE_USDTM | 14943 | scored | CLASSIC5 |
| SOL | SOLUSDT | BINANCE_USDTM | 13191 | scored | CLASSIC5 |
| NEAR | NEARUSDT | BINANCE_USDTM | 13004 | scored | CLASSIC5 |
| ZEC | ZECUSDT | BINANCE_USDTM | 14522 | scored | CLASSIC5 |

PUMPFUN → PUMPUSDT and MNT → Bybit v5 linear remain **printed leans, not rulings** `[OPERATOR_RULINGS.md:148-149]`
(§6 Q5). The PANEL PIN gap (R2 "All 17" against the contract's 5-asset pin) is filed as finding **`FN-RUL-L1-1`**
`[close/S5_FINDINGS_NOT_FIXED.md:11, :72]`. R8 supersedes R2 on the operator's word (`OPERATOR_RULINGS.md` `## R8`),
and both BRK texts record the supersession `[close/S0_VERDICTS.md]` (§5.21).

### 0.6 · The forward strip — REPORT-ONLY, NEVER SCORED

*The 5-asset v6 book from TC9's as-of to this corridor's end.*
- TC9's as-of, 2026-08-22T00:00:00Z, is read from `research_outputs/tierc9/build_manifest.json` `as_of` and equals the
  journal column. The contract literal was compared and is equal.
- The end is 2026-09-21T16:00:00Z `[PROGRESS.json]`.
- The book is `[panel/control_journal.parquet]` (sha `fcbf5db0…` = PANEL/gate record).
- Built by `scripts/tierc10_close_forward_strip.py`. Full page: `[close/FORWARD_STRIP.md]`, sha256 `a59e438c…`;
  fixtures 9/9 PASS, 27/27 break legs RED `[close/FIXTURES_CLOSE_forward_strip.txt]`.
- No CI, p, verdict, LOAO or bar.

| label | asset | dir | armed | entered | exited | exit | bars | net_r (TC-series) | twin net_r (ADDED) |
|---|---|---|---|---|---|---|---:|---:|---:|
| ENTERED / CLOSED | ETHUSDT | long | 2026-08-17T08:00Z | 2026-08-30T12:00Z | 2026-08-30T20:00Z | stop | 2 | −1.031064 | −1.041742 |
| ENTERED / CLOSED | BTCUSDT | long | 2026-09-14T16:00Z | 2026-09-14T16:00Z | 2026-09-14T20:00Z | stop | 1 | −1.10553 | −1.147742 |
| ENTERED / CLOSED | SOLUSDT | long | 2026-09-18T00:00Z | 2026-09-18T00:00Z | 2026-09-20T00:00Z | stop | 12 | +1.446902 | +1.434730 |
| ENTERED / **OPEN AT CORRIDOR END** (marked, not realized) | ETHUSDT | long | 2026-09-18T08:00Z | 2026-09-18T08:00Z | 2026-09-21T12:00Z | corridor_end | 19 | +3.642965 | +3.654684 |

- **Footer** `[FORWARD_STRIP.md]`: 4 campaigns, 0 continuations. No v6 campaign was open at TC9's as-of: TC9's own
  journal holds 0 `corridor_end` rows.
  - Closed (realized): n 3, Σ net_r −0.689692.
  - Open, marked to the pin: +3.642965.
  - All: +2.953273, twin +2.899929.
- **By asset:** BTC 1, ETH 2, SOL 1, NEAR 0, ZEC 0.
- **Anchor.** The ENTERED set equals F-CTRL/b's four live-only campaigns `[panel/FIXTURES_PANEL.txt:35]`.
- **One armed early.** The ETH campaign entered 2026-08-30 was armed 2026-08-17, inside TC9's window.
- **This is a window, not evidence.** Four campaigns, one of them open, carry no weight either way.

---

## R0 · WHAT THE INTERRUPTION LEFT

### R0.1 · The interruption

The 2026-09-21 builder session (`730798c3-4e2c-4d67-8a9b-be6f9aae52f5`) was killed by an **API 529 at
2026-09-22T01:06:58Z**. Its final workflow, `tc10-stage-0ab-prep-v2`, journals `agentCount` 15
(`~/.claude/projects/-Users-luis-Naiad/730798c3-…/workflows/wf_404100c3-7bd.json`). Thirteen of those agents completed
and **two died on the same 529**:

- `review:census#1`: the adversarial review of the CENSUS-R module never ran in that session. The resume later ran
  review rounds on CENSUS-R; the digest cites "review round 3" `[census/CENSUS_R_DIGEST.md:196]`.
- `draft:registrations`: **no registration text had been drafted, for any of the six lanes.**
  `research_outputs/tierc10/registrations/` did not exist, and Stage B had not begun.

The session's scratchpad was destroyed with it. It held the only copies of `OPERATOR_RULINGS.md`,
`REGISTRATION_DRAFTS.md`, `foundations_result.json` and `STEP0_RECORD.md`. The session transcript and the workflow
journals survived and were mined on 2026-09-22. The operator's six rulings were recovered verbatim and are now filed
**inside the build tree**, so the next interruption cannot take them.

### R0.2 · The stage ledger — at R0, and as it stands

**At R0 (history, not current).** R0 re-ran every fixture suite on 2026-09-22 and independently re-hashed 1,035
artifact content-shas. The result:
- 5 COMPLETE-VERIFIED: STEP 0, NULL/gaps-only, NULL/gaps+order, A, PANEL.
- 4 PARTIAL: D-CORE, CENSUS-R, LANES, BRK.
- None of the four was partial because a number had moved:
  - D-CORE lacked four RESUME-clause artifacts: F-D-4, F-D-5, the haircut twin and the contract multipliers.
  - CENSUS-R lacked [Q-R3] and [Q-R4].
  - LANES carried a confirmed defect.
  - BRK lacked height-vs-toll, a row printer and a `build_manifest.json`.

That table is kept verbatim at `[close/R0_ADDENDUM.md §A]`, sha256 `0df7a920…`. It re-renders byte-identically from
the `f97cded` ledger, which is its F-SL-R0SEAL.

**As it stands** (`[PROGRESS.json]`, 15 stages; the moves are read from the committed ledger history in
`[close/R0_ADDENDUM.md §C]`):

| stage | at R0 (`f97cded`) | now | moved to COMPLETE-VERIFIED at | blockers now |
|---|---|---|---|---:|
| STEP 0 | COMPLETE-VERIFIED | COMPLETE-VERIFIED | — | 0 |
| D-CORE | PARTIAL | **PARTIAL** (F-D-1 only) | — still PARTIAL | 8 (4 superseded by the 8th; see below) |
| CENSUS-R{4h,1d} | PARTIAL | COMPLETE-VERIFIED | `6b15def` | 0 |
| NULL/gaps-only | COMPLETE-VERIFIED | COMPLETE-VERIFIED | — | 0 |
| NULL/gaps+order | COMPLETE-VERIFIED | COMPLETE-VERIFIED | — | 0 |
| A (stamps) | COMPLETE-VERIFIED | COMPLETE-VERIFIED | — | 0 |
| PANEL/gate | COMPLETE-VERIFIED | COMPLETE-VERIFIED | — | 0 |
| LANES (B mech) | PARTIAL | COMPLETE-VERIFIED | `899d3e7` | 0 |
| BRK (B mech) | PARTIAL | COMPLETE-VERIFIED | `899d3e7` | 0 |
| F-C10-RESUME | (not in R0) | COMPLETE-VERIFIED | born CV at `6b15def` | 0 |
| D-5M | (not in R0) | **PARTIAL** (F-D-1 only) | — still PARTIAL | 1 |
| CENSUS-R{5m} | (not in R0) | COMPLETE-VERIFIED | born CV at `899d3e7` | 0 |
| B-REG (the six filed) | (not in R0) | COMPLETE-VERIFIED | born CV at `899d3e7` | 0 |
| B-CORE | (not in R0) | COMPLETE-VERIFIED | born CV at `ab7306a` | 0 |
| B-5M | (not in R0) | COMPLETE-VERIFIED | born CV at `08a6fce` | 0 |

**13 COMPLETE-VERIFIED, 2 PARTIAL.** Both PARTIALs rest on the same single cause: **F-D-1 stays RED pending the
operator's REST-or-ARCHIVE word** (§6 Q1).
- D-CORE's `blockers` still list entries 1–4 ("F-D-4 … ABSENT", "F-D-5 … ABSENT", "HAIRCUT TWIN … ABSENT",
  "MULTIPLIERS … ABSENT"). Its entry 8 reads *"REPAIRED 2026-09-22: F-D-4, F-D-5, the tiered haircut twin and
  contract multipliers are built and filed; those four clauses no longer block"* `[PROGRESS.json stages[1].blockers]`.
- **Entries 1–4 are superseded, not open.** They stay printed because PROGRESS is not edited here.
- F-C10-RESUME, re-run for the transcript of record `2416a15`, reads *"1,090 recorded artifact content-sha(s) across 13
  COMPLETE-VERIFIED stage(s) re-hashed, every one a MATCH (865,181,642 B total)"* and "9 GREEN, 0 RED"
  `[FIXTURES_RESUME.txt:120, :224]`.

**What the repairs were** (commits in the windows `[close/R0_ADDENDUM.md §C]` names; a window names candidates, not an
attribution):
- R7–R10 were filed in `ffdffce`.
- Stage D's four absent artifacts, the lanes BE-latch repair, and [Q-R3]/[Q-R4] landed in `54cfd60`.
- The BRK verdict row derived from the book, `d8a6f81`.
- The height-vs-toll verdict filed per era, 360 rows not 120, `a58bafc`.
- BRK reading its own era's [Q-R3], `1359d99`.
- The F-C10-RESUME fixture and its transcripts: `590989d` … `74d9b39`.
- The Stage B mechanics repair after filing, `899d3e7`.

### R0.3 · Quarantined, disclosed, restored

**Quarantined** to `research_outputs/tierc10/_partial_20260922T0955Z/` (LAW 2: never deleted). These are two
kill-partials from filtered fixture runs that the 529 interrupted `[_partial_20260922T0955Z/README.md]`:
- `lanes/FIXTURES_LANES_partial.txt` (4,692 B): a filtered `be_latch lanes_gate spr_build` run.
- `panel/FIXTURES_PANEL_partial.txt` (6,552 B), reading `FIXTURE SUMMARY 1/1 PASS {"F-LAW4-GATE": true}`.

Each recorded a few legs, not a suite, and sat beside the transcript of record, where its "1/1 PASS" could be misread
as a verdict.
- `2e4d959` ("LAW 2: restore the quarantined kill-partial's ledger record") put the quarantine's ledger record back.
- F-C10-RESUME-2 re-hashes both. They agree three ways: fixture literal, disk bytes and PROGRESS record
  `[FIXTURES_RESUME.txt:131]`.
- The contract's "a tampered partial must FAIL" is proven by planting one appended byte in a copy of the lanes
  partial `[FIXTURES_RESUME.txt:124]`.

**Disclosed, not moved:** `census/smoke/` and `null/smoke/`.
- They are legitimate smoke roots with their own manifests, but they carry full lookalike filenames.
- They were built before the R1 bands and the era split, so their contents are now wrong in substance.
- Both suites fall back to a smoke root only when the full root has no manifest, so the default resolves correctly
  today.
- **Still in place at this draft.** At CLOSE: rebuild them, or quarantine them under `_partial_<ts>/` per LAW 2. The
  operator chooses; nothing is deleted (§5.12).

### R0.4 · What was redone

- **At R0, nothing was recomputed, because nothing had moved.** The corridor never moved: AS_OF
  2026-09-21T16:00:00Z, substrate frozen, `live_cache_touched: false`. What R0 did redo was every fixture suite in the
  build, which is what LAW 1 means by COMPLETE.
- **R7 confirmed that reading.** *"Corridor pin only."* LAW 4 protects the as-of pin; it does not order the
  destruction of stages that verify clean `[OPERATOR_RULINGS.md:87-99]`.
- **After R0, only missing things were built.** The four Stage D report artifacts, [Q-R3] and [Q-R4] (built new, not
  re-computed), the LANES and BRK repairs, D-5M, CENSUS-R{5m}, and all of Stage B.
- **No stage that was COMPLETE-VERIFIED at R0 moved a byte.** F-C10-RESUME-1 re-hashes every recorded artifact.

**Secured.** R0's most urgent finding was not a bug. `git status` showed all fifteen `scripts/tierc10_*.py`,
`analytics/rangefinder_census.py` and the three Stage-0a rangefinder edits as untracked or modified. There was one TC10
commit in the whole resume window: 29,913 lines that a second 529 would have taken. They were committed as `d19f857`
before any further work.

### R0.5 · The stage log — LAW 6

*One line per tierc10 commit, oldest first, subject verbatim `[git log --since=2026-09-21 --grep=tierc10]`. The
fifteen stage one_lines are filed verbatim at `[close/STAGE_LOG.md §A]`, sha256 `01865838…`. The draft's former §1
stopped at `f97cded`; that gap is finding §5.13.*

- `c7b157d` 2026-09-22T09:21 · STEP Q + rulings recovery: the contract and the operator's words survive the session.
- `d19f857` 09:51 · commit the whole build tree — LAW 6 was breached for every stage.
- `f97cded` 09:52 · R0: the stage ledger — PROGRESS.json, the LAW-2 quarantine, the draft's R0 sections.
- `ffdffce` 10:01 · operator rulings R7-R10 — LAW 4, the BRK panel, P-SPR-2, the null of record.
- `54cfd60` 11:50 · Stage D's four absent artifacts, the lanes BE-latch repair, and [Q-R3]/[Q-R4].
- `d8a6f81` 12:17 · round 2: BRK derives its verdict row from the book; F-C10-RESUME's anchor looks both ways.
- `a58bafc` 12:38 · CENSUS-R: the height-vs-toll verdict is filed PER ERA — 360 rows, not 120.
- `1359d99` 13:07 · BRK: each form reads the [Q-R3] verdict for the era it is judged in.
- `590989d` 15:12 · F-C10-RESUME: the fixture that makes the LAW OF RESUMPTION checkable.
- `80ecca5` 15:13 · F-C10-RESUME: file the transcript of record — 9 GREEN, 0 RED.
- `6b15def` 15:23 · LAW 6: the ledger after the repair phase — every suite re-run, five stages advance.
- `3453c87` 15:34 · LAW 6: the ledger after the repair phase, rebuilt from the committed R0 base.
- `2e4d959` 15:35 · LAW 2: restore the quarantined kill-partial's ledger record.
- `54c519d` 15:35 · F-C10-RESUME: move the anchor to the post-repair ledger, deliberately.
- `ad34e6e` 15:36 · F-C10-RESUME: re-file the transcript after the re-pin — 9 GREEN, 0 RED.
- `2e92972` 15:36 · LAW 6: the resume stage records no artifact sha — the self-reference does not converge.
- `41a5070` 15:36 · F-C10-RESUME: re-pin onto the ledger that drops the circular self-record.
- `83f5e29` 15:36 · F-C10-RESUME: transcript of record after the re-pin.
- `fa205c8` 15:37 · F-C10-RESUME: leg 1 accuses instead of raising when a stage records no artifact.
- `74d9b39` 15:37 · F-C10-RESUME: transcript of record — 9 GREEN, 0 RED.
- `371123f` 17:03 · STAGE B: the six registrations are FILED — text before result.
- `899d3e7` 21:45 · STAGE B mech: F-C10-HOLD real, F-C10-BE NOT RUN per P-BE-1 §9, the scoring driver.
- `be157e9` 21:45 · F-C10-RESUME: transcript of record after the Stage B mech ledger — 9 GREEN, 0 RED.
- `b29774e` 21:48 · B-CORE: the reviewed dry-run, pinned BEFORE any score — 21 arms, one prescribed HALT.
- `ab7306a` 21:51 · B-CORE: five registrations scored against the pinned dry-run — one SUPPORTED on (a), one prescribed HALT.
- `dc30015` 21:51 · F-C10-RESUME: transcript of record after B-CORE — 9 GREEN, 0 RED.
- `08a6fce` 21:57 · B-5M: P-BRK-S1 scored, the family finished at m = 6 — P-TRG-2 alone clears all three clauses.
- `2416a15` 21:57 · F-C10-RESUME: transcript of record after B-5M — 9 GREEN, 0 RED.
- *CLOSE* (this draft and the `close/` fragments): **uncommitted at this draft** (§8).

Two commit subjects, `ab7306a` and `08a6fce`, say "on (a)" and "all three clauses" of P-TRG-2. They are verbatim and
cannot be changed. Under P-TRG-2's own text the verdict is CI-only, and LOAO and BH ride beside it (§0.2).

---

## 1 · STAGE B — FILING, MECHANICS, THE DRY-RUN, THE SCORE

### 1.1 · The six, filed text-before-result (`371123f`)

- **The filing.** Registry length 6, head `7621a85727969299…`, m = 6. Order of filing: P-GEN-1, P-SPR-2, P-BE-1,
  P-TRG-2, P-BRK-I1, P-BRK-S1 `[REGISTRY_PIN.json]`.
- **The texts of record** are `[REGISTRATION_TEXTS.json]`. Each filed `registrations/<REG>.json` text is byte-equal to
  its entry there, and every payload and text sha recomputes. Verifiers checked this for all six at close.
- **The human-readable companion is stale.** `[REGISTRATION_TEXTS.md]` contains **none** of the six texts verbatim and
  still reads "STATUS: NOTHING IS FILED" `[close/S5_FINDINGS_NOT_FIXED.json measured.i]`. It must not be read as the
  texts (finding §5.9).
- **B-REG fixtures.** F-SC-RECORD holds the record against `REGISTRY_PIN.json`: 16/16 twice
  `[PROGRESS.json stages[12].fixtures]`.
- **Rulings the texts carry:**
  - R8: the BRK panel is CLASSIC5 and supersedes R2.
  - R9: P-SPR-2 runs full corridor, both ways.
  - R1: the era cut is 2024-06-30T23:59:59Z (`1719791999000` ms). This is an executor lean on R1's "search data from
    past runs to tune".

### 1.2 · The mechanics repairs (`899d3e7`)

- **LANES.** Filing the registrations turned a pre-filing invariant RED: F-LANES-GATE asserted an empty registry, and
  the post-filing baseline was 12/13, exit 1.
  - F-LANES-GATE was restated as the post-filing law: the registry equals the 6 pinned lines, and both lane
    registrations open through the filed door.
  - Converse, agree and closing-check defects were fixed, so the leg cannot be driven GREEN falsely.
  - Now 15/15 twice, byte-identical, with 79/79 break legs RED `[PROGRESS.json stages[7].fixtures[1].note;
    lanes/FIXTURES_LANES.txt:317]`.
- **BRK.** The post-filing baseline was 16/17 (F-BRK-GATE asserted "no BRK registration filed").
  - Rows are now built SEALED from the filed arms, with `require_arm` first.
  - Each row reads its own era's [Q-R3] verdict and carries the Tier-E other anchor, the 17-asset view and
    TOLL_ACCOUNTING. The seal is a typed allowlist.
  - Now 20/20 twice, 63 break legs RED, 0 void `[PROGRESS.json stages[8].fixtures[1].note;
    brk/FIXTURES_BRK.txt:491]`.

### 1.3 · F-C10-BE — NOT RUN, as P-BE-1 §9 prescribes

- **What §9 says.** *"if P-BE-1's filed book contains no tie and no 4h/5m mismatch latch bar, the leg must report NOT
  RUN with that reason. It must NOT substitute a synthetic bar or relabel a dip_first case to reach three."*
- **What the book contains.** The outcome-free latch census on A1 `[lanes/BE_LATCH_CENSUS.json]`, re-derived on the
  row byte-identical, sha `96dfd0b7…` `[scores/P-BE-1.rows.json rows[0].beside.f_c10_be]`:
  - 200 campaigns and 103 latch bars.
  - dip-before 36, **dip-after 0**, print-no-dip 67, tie 0, 4h/5m mismatch 0.
  - Journal = module = hand walk on 103/103.
- **The decision was the text's, before the look.** `decision` NOT RUN; `operator_question` false. The lane harness,
  rule and census legs PASS and print `[NOT RUN]` with the §9 reason `[lanes/FIXTURES_LANES.txt:238-299]`.
- **The contract's "sequence proven on 3 campaigns" is unmet on real campaigns, by the text's own prior terms.** It is
  NOT a PASS.
- **Finding.** dip-after 0 of 103 means the latch-bar fill branch that §6 repaired was never reached on this corridor.
  The §6 claim that the pin-1.0 repair changes nothing therefore holds here only vacuously (§5.5).

### 1.4 · F-C10-HOLD — real, in each form's filed era

`[brk/FIXTURES_BRK.txt:58, :110, :137]` PASS on three legs:

- **Synthetic and real, per lens.**
- **REAL, FILED ERA, per lens.** Three detector-level holds per case, named by a blind printed rule inside each form's
  filed era: S1 5m holdout, I1 1d full, both anchors.
  - Each is hand-verified on the census tape against the module and the filed pins.
  - Each asset's first hold is re-derived by hand, and one real failed hold per case must FAIL.
- **REAL, FILED BOOK.** The first three campaigns of each filed CLASSIC5 arm's book are walked by hand: hold, entry,
  stop and permission. For P-BRK-I1, the weekly 12>25 posture and the daily 12/25 lifecycle are included.
- **Sabotage that must go RED:**
  - The era collar dropped.
  - The entry moved to the touch bar.
  - The permission gate removed.
  - The S1 tide read with its sign flipped.
  - The earliest hold silently dropped.

### 1.5 · The driver, and the dry-run pinned before any score (`b29774e`)

- **The driver.** `scripts/tierc10_score.py` defaults to the dry run. Its certification reads *"16/16 PASS · 26/26
  break legs RED"* `[scores/FIXTURES_SCORE.txt:173]`.
- **The dry run's law** `[scores/DRYRUN.json law]`: *"DRY-RUN — NOT A RESULT. Every arm is ridden to its Book through
  the door its registration names and bound as TP.score would bind it AHEAD of its result marker; TP.score,
  TP.finish_family and TP._mark_scored are never called … no outcome (no sum, no mean, no CI, no p) is computed or
  printed."*
- **What it pinned.** 21 arms. One HALT, `DRYRUN.json halts`: *P-BE-1 'be-floor-1R vs card-v6 (CLASSIC5, full)' —
  the arm shares the WHOLE campaign set with its base.* The HALT was known before any score and is prescribed by the
  text.
- **The scores followed the pin.**
  - B-CORE (`ab7306a`) scored five registrations against the pinned books.
  - B-5M (`08a6fce`) scored P-BRK-S1 and ran `finish_family`.
  - Every scored arm's `book_sha256` equals its dry-run pin.
- **LAW 1's re-pass.** Each stage was re-scored a second time against the pinned dry-run. All rows files, all
  `.scored.json` files and `FAMILY.json` re-wrote **byte-identical** `[PROGRESS.json stages[13..14].fixtures]`.

### 1.6 · P-BE-1's prescribed HALT, and the question it raises

- **The HALT is the registration working as filed.** The ruler was registered, not left to the scorer, so that an
  unmoved key set could not quietly become the narrower paired row.
- **What §11 orders next.** A new id under `set_change`, with the reason disclosed.
- **Why this tier cannot do it.** "WHAT THIS PASTE IS NOT" forbids adding a registration.
- **The operator's call** (§6 Q3): order a new id, or let HALT — NO VERDICT stand as P-BE-1's record.
  - Either way, **a new id would be filed after this look.** A2–A4 are already known and all straddle zero. The new
    row would have to carry them beside it (P-SPR-2 §11's rule against a quiet re-file after a disappointing row
    states the same principle).

### 1.7 · The haircut twin on every row — and what it does not charge

- **Where the twin rides.** `beside.haircut_twin` is present on every scored or Tier-E arm that has a score row: 20 of
  21 arm rows. The 21st is P-BE-1's HALTed A1 `[close/S5_FINDINGS_NOT_FIXED.json measured.ii]`.
- **No sign flips on the registration rows.** `sign_disagrees_with_tc` is false on all 20.
- **The filed twin charges fee plus charter slippage and NO funding.** Every row's `funding_note` reads: *"the filed
  twin charges fee + charter slippage and NO funding; the companion column subtracts the campaign's funding_r and is
  NOT the filed twin"*.
- **So the twin can sit above the TC-series net even though its per-side cost is higher.**
  - It is above the TC-series net on **8 of 20** arms: P-BE-1 rows 1 and 3, all three P-BRK-I1 arms, and P-TRG-2 rows
    0–2. On all 8, the with-funding companion is at or below TC.
  - Its per-side cost is higher on every asset: round trip 14/20/30 bps against the TC-series 10.
- **The v6 control's own book-level twin** is filed as an ADDED column `[close/V6_CONTROL_HAIRCUT_TWIN.md]` (§3.6). In
  the **tuning era the twin flips the control's sign**: TC −0.010763, twin +0.014494, companion −0.030517.
- **The slippage-twin question is named for the autopsy, not answered** (§6 Q7, LEDGER_APOLLO append).

---

## 2 · CENSUS-R — Tier-E · A SELECTION, not a result · m logged

*Digest of record: `[census/CENSUS_R_DIGEST.md]`, sha256 `281e6163…`, 206,251 B. The close selection is
`[close/S2_CENSUS_R.md]`, sha256 `d401eee9…`, 64,492 B, **itself over FLAG_BYTES**. It carries 24 byte-exact spans,
F-S2-SLICE 9/9 GREEN `[close/FIXTURES_CLOSE_census_r.txt:93]`. Every table below is copied from those two files.*

- **m, read from each table's `m_looks_this_table`:** acceptance 60 · height_toll_verdict 6 · outcome_grid 7,920 ·
  coverage 102 · spring_overlap 204 · null_summary 21,384 per variant.
- **The collar.** P-BRK-S1's scoring ground (5m retest-hold, holdout era) is **FILED and never printed**.
- **The warranty.** Pins were calibrated on BTC only. Every other asset and lens is an extrapolation of frozen pins.

### 2.1 · HEIGHT-vs-TOLL [Q-R3] — a GATE, not a table

- **The ruling.** LEDGER.md:834: *"Q-R3 PLAYBOOK-R TIMING: (a) — detection and gating first; a range-trading contract
  is drafted ONLY IF the height-vs-toll feasibility gate AND the edge-fade outcome leg both pass."*
- **The gate's legs.**
  - HEIGHT passes iff n_ranges ≥ 30, median(height ÷ round-trip toll) ≥ 3.0, and share(ratio < 1) ≤ 0.1.
  - EDGE-FADE [LEAN R3-b] passes iff fading toward the far boundary from the near 20% of the range is net positive at
    H20 *within the row's own era*, on at least 30 confirmed ranges.
  - The verdict is keyed on the era: 360 rows `[census/height_toll_verdict.parquet]`.

**Across the whole 360-row grid the conjunction passes on 9 rows over era ALL, 13 over tuning and 7 over holdout,
of 120 each** `[PROGRESS.json stages[2].one_line]`. **At 5m, single assets pass 0/17 on the holdout and 0/17 on ALL,
on both scales.** The tuning-era passes (frozen3.0 2/17: 1000PEPEUSDT, ENAUSDT; calibrated 1/17: 1000PEPEUSDT) are
in-sample and are not evidence `[census/height_toll_verdict.parquet, 5m single-asset rows]`. PROGRESS's "FAILS 0/17"
`[stages[11].one_line]` is the holdout figure carried on P-BRK-S1's row; it is not era-free.

**The height gate does no work; the toll bites through the outcome leg.**
- Pooled over ALL, frozen3.0, the median height ÷ toll ratio is 436.87 at 1d, 184.38 at 4h and 24.27 at 5m. The share
  of ratios below 1 is at or near 0 everywhere `[digest B.1]`.
- *"THE HEIGHT FLOOR DOES NO WORK BECAUSE THE DETECTOR PINS THE HEIGHT."* REV_MIN = 1.75 × SCALE_MULT selects which
  ranges confirm, so the height is near-constant in ATR. What moves the ratio is the toll.

**The POOLED verdict rows, frozen3.0 (the scale of record)** `[close/S2_CENSUS_R.md §2.2]`:

| lens | pool | era | n ranges | ratio median | HEIGHT | edge ranges | edge NET (H20, ATR) | EDGE-FADE | prov | **VERDICT** |
|---|---|---|---:|---:|---|---:|---:|---|---|---|
| 1d | ALL | ALL | 121 | 436.87 | PASS | 118 | −0.1208 | FAIL | no | **FAIL** |
| 1d | ALL | tuning | 70 | 446.25 | PASS | 69 | +0.0369 | PASS | no | **PASS** |
| 1d | ALL | holdout | 51 | 426.34 | PASS | 56 | −0.3118 | FAIL | no | **FAIL** |
| 1d | CLASSIC5 | ALL | 53 | 413.99 | PASS | 52 | +0.0441 | PASS | no | **PASS** |
| 1d | CLASSIC5 | tuning | 35 | 413.99 | PASS | 35 | +0.1537 | PASS | no | **PASS** |
| 1d | CLASSIC5 | holdout | 18 | 459.33 | FAIL | 21 | −0.4360 | FAIL | **YES** | **FAIL** |
| 1d | UNSEEN12 | ALL | 68 | 499.89 | PASS | 66 | −0.2320 | FAIL | no | **FAIL** |
| 1d | UNSEEN12 | tuning | 35 | 512.44 | PASS | 34 | −0.1405 | FAIL | no | **FAIL** |
| 1d | UNSEEN12 | holdout | 33 | 426.34 | PASS | 35 | −0.2992 | FAIL | no | **FAIL** |
| 4h | ALL | ALL | 709 | 184.38 | PASS | 696 | −0.1353 | FAIL | no | **FAIL** |
| 4h | ALL | tuning | 386 | 180.89 | PASS | 380 | −0.1492 | FAIL | no | **FAIL** |
| 4h | ALL | holdout | 323 | 189.00 | PASS | 322 | −0.1303 | FAIL | no | **FAIL** |
| 4h | CLASSIC5 | ALL | 298 | 169.50 | PASS | 291 | −0.2257 | FAIL | no | **FAIL** |
| 4h | CLASSIC5 | tuning | 196 | 169.50 | PASS | 190 | −0.3341 | FAIL | no | **FAIL** |
| 4h | CLASSIC5 | holdout | 102 | 172.38 | PASS | 103 | +0.0062 | PASS | no | **PASS** |
| 4h | UNSEEN12 | ALL | 411 | 203.30 | PASS | 405 | −0.0837 | FAIL | no | **FAIL** |
| 4h | UNSEEN12 | tuning | 190 | 212.46 | PASS | 190 | −0.0375 | FAIL | no | **FAIL** |
| 4h | UNSEEN12 | holdout | 221 | 202.92 | PASS | 219 | −0.1359 | FAIL | no | **FAIL** |
| 5m | ALL | ALL | 32,738 | 24.27 | PASS | 32,546 | −0.3637 | FAIL | no | **FAIL** |
| 5m | ALL | tuning | 17,987 | 24.97 | PASS | 17,869 | −0.2498 | FAIL | no | **FAIL** |
| 5m | ALL | holdout | 14,751 | 23.54 | PASS | 14,678 | −0.5725 | FAIL | no | **FAIL** |
| 5m | CLASSIC5 | ALL | 13,025 | 23.26 | PASS | 12,929 | −0.3740 | FAIL | no | **FAIL** |
| 5m | CLASSIC5 | tuning | 8,441 | 24.93 | PASS | 8,382 | −0.2688 | FAIL | no | **FAIL** |
| 5m | CLASSIC5 | holdout | 4,584 | 20.67 | PASS | 4,548 | −0.5885 | FAIL | no | **FAIL** |
| 5m | UNSEEN12 | ALL | 19,713 | 24.95 | PASS | 19,617 | −0.3020 | FAIL | no | **FAIL** |
| 5m | UNSEEN12 | tuning | 9,546 | 25.00 | PASS | 9,487 | −0.1919 | FAIL | no | **FAIL** |
| 5m | UNSEEN12 | holdout | 10,167 | 24.92 | PASS | 10,130 | −0.5038 | FAIL | no | **FAIL** |

The calibrated scale passes only 1d tuning, on all three pools, and fails every other pooled row
`[close/S2_CENSUS_R.md §2.2]`. So UNSEEN12 does pass once on a pool: 1d calibrated tuning, +0.0557
(`S2_CENSUS_R.md:134`).

**Read this table plainly:**
- **No range-trading contract may be drafted at 5m on any pool, nor at 4h on any pool beyond one pool-era cell:** the
  4h CLASSIC5 frozen3.0 holdout row, at +0.0062 ATR.
- **The other passes are single-asset cells, not pools.** 19 single-asset 4h rows pass across the three eras and two
  scales. Six of the seven holdout-era passes are single-asset 4h calibrated cells: 1000PEPE +0.0576, BNB +0.1871,
  DOGE +0.0979, ENA +0.1873, ETH +0.0840, LTC +0.2182 (edge NET H20, ATR); the seventh is the CLASSIC5 pool row above
  `[census/height_toll_verdict.parquet]`. They are a selection over 360 rows (`m_looks_this_table` 6), not grounds for a
  contract.
- **The one pooled 1d frozen row that passes on full history (CLASSIC5) reverses on the holdout.** It is +0.0441 on
  ALL and −0.4360 on the holdout, where it fails both legs on 18 ranges.
- **At frozen3.0, UNSEEN12 never passes on any era; at the calibrated scale it passes 1d tuning only** (+0.0557, above).
  UNSEEN12 is not an out-of-sample panel in this census: 9 of its 12 assets are display-only (F-D-5), and the pins
  were calibrated on BTC.
- **P-BRK-I1 carries the ALL row, P-BRK-S1 the 5m CLASSIC5 holdout row** (§0.2).

### 2.2 · THE ACCEPTANCE HEAD-TO-HEAD [Q-R4] — the data's default NAMED, nothing promoted

- **The ruling.** LEDGER.md:835: *"Q-R4 ACCEPTANCE DEFINITION: (a) — the census measures four candidate
  operationalisations head-to-head (2-close / 3-close / 6-outside-close stale-run / time-beyond); the engine default is
  chosen FROM DATA."*
- **Nothing is promoted.** `promoted` reads "NOTHING — the data's default is NAMED; no pin moves [Q-R4]", and
  `engine_default_after` reads "BREAK_CONFIRM_N=8 · BREAK_MARGIN=1.5 — UNCHANGED", on all 3,600 rows
  `[census/acceptance_head_to_head.parquet; F-S2-PROMOTE]`.

**POOLED:ALL · frozen3.0 · era ALL · H20** (NET = median term − toll, in ATR) `[close/S2_CENSUS_R.md §2.1]`:

| rule | 5m declared | 5m precision | 5m **NET** | 4h declared | 4h precision | 4h **NET** | 1d declared | 1d precision | 1d **NET** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2-close | 47,623 | 0.5567 | −0.7579 | 957 | 0.6134 | −0.0621 | 150 | 0.6133 | +0.2809 |
| 3-close | 30,267 | 0.6084 | −0.7580 | 668 | 0.6527 | −0.1422 | 98 | 0.6735 | +0.2020 |
| 6-outside-close-stale-run | 8,791 | 0.7671 | **−0.6754** | 224 | 0.7812 | −0.2389 | 38 | 0.8158 | +0.5993 |
| time-beyond | 11,909 | 0.6587 | −0.7178 | 270 | 0.7222 | −0.1308 | 40 | 0.7750 | **+0.7492** |
| RangeFinder-DIE (8-close OR 1.5 ATR) | 32,733 | 1.0000 | −0.8196 | 706 | 1.0000 | **+0.0459** | 116 | 1.0000 | +0.2094 |

**The data's default, per lens × era × horizon** (named only; provisional = n < 30):

| lens | ALL · H20 | tuning · H20 | holdout · H20 | ALL · H100 |
|---|---|---|---|---|
| 5m | 6-outside-close-stale-run (−0.6754), **all five NET negative** | stale-run (−0.6435), all negative | stale-run (−0.7775), all negative | stale-run (−0.767752), all negative |
| 4h | RangeFinder-DIE (+0.0459) | stale-run (+0.3279) | RangeFinder-DIE (−0.1954), **all five negative** | time-beyond (+0.922898) |
| 1d | time-beyond (+0.7492) | stale-run (+0.8690, PROVISIONAL n 16) | time-beyond (+1.1173, PROVISIONAL n 21) | stale-run (+1.390168) |

**What the head-to-head actually shows.** The close-count axis barely binds, because the RangeFinder dies on its
1.5-ATR MARGIN rather than its 8-close pin:
- 1d: 95 of 116 deaths (81.9%).
- 4h: 582 of 706 (82.4%).
- 5m: 28,528 of 32,733 (87.2%).

So BREAK_CONFIRM_N = 8 is very nearly a dead letter at these pins. Precision rises with strictness. **At 5m every rule
loses, so the "default" there is the least-bad loser.** This is a direction the data leans, not a mandate.

### 2.3 · OUTCOME AFTER EVENT — real beside the null of record

**How to read these tables** `[close/S2_CENSUS_R.md §2.3; digest §5]`:
- **Term.** Measured in ATR from the close of the bar the event is *known* at, over H bars of the lens. Censored,
  never shortened.
- **NET.** The median term minus the row's measured toll. A pooled row quotes the binding (max) per-asset toll [C-f].
- **The null.** Of record is **gaps+order** (R10): *"It cuts the measured own-window overlap from 25.62% to 7.97%"*.
  The contract-literal gaps-only null is filed beside it in the fragment. K = 20 draws; `pct` is where the real median
  sits among them. **K=20 resolves a percentile to 5 points at best. It is a DESCRIPTION, never a p-value.**
- **Sub-pool nulls were computed at close.** The null stage pooled POOLED:ALL only, so the CLASSIC5 and UNSEEN12
  nulls were computed at CLOSE by the null build's own pooling path. That path reproduces all 2,376 filed POOLED:ALL
  null rows exactly (F-S2-NULL-ANCHOR).
- **TUNED** marks a band whose hold pins were tuned per R1. *n<30* is provisional.
- **H20 only here; H100 is in the fragment.** Every table below prints H20. The same pools, lenses and eras at H100
  (n, median and NET H100, and the H100 nulls, both variants) are `[close/S2_CENSUS_R.md §2.3, L206–L571]`, one
  POOLED:CLASSIC5 / POOLED:UNSEEN12 block per lens × era.

**5m · frozen3.0 · era ALL · H20**

| class | C5 n | C5 med H20 | C5 **NET H20** | C5 null g+o med [q25, q75] pct | U12 n | U12 med H20 | U12 **NET H20** | U12 null g+o med [q25, q75] pct |
|---|---:|---:|---:|---|---:|---:|---:|---|
| breach | 29,755 | -0.294 | **-0.758** | -0.252 [-0.282, -0.237] pct 15 | 47,056 | -0.333 | **-0.752** | -0.221 [-0.232, -0.202] pct 0 |
| harden | 16,732 | +0.162 | **-0.298** | +0.108 [+0.076, +0.131] pct 95 | 27,346 | +0.202 | **-0.219** | +0.095 [+0.065, +0.116] pct 100 |
| DIE | 13,023 | -0.389 | **-0.810** | -0.326 [-0.346, -0.303] pct 0 | 19,710 | -0.406 | **-0.786** | -0.316 [-0.345, -0.295] pct 0 |
| memory-touch-v1 | 25,599 | +0.003 | **-0.362** | +0.053 [+0.038, +0.075] pct 0 | 38,694 | +0.060 | **-0.277** | +0.084 [+0.069, +0.095] pct 15 |
| memory-touch-2s | 17,051 | +0.116 | **-0.282** | +0.173 [+0.147, +0.195] pct 5 | 25,845 | +0.121 | **-0.240** | +0.186 [+0.177, +0.204] pct 0 |
| flip-hold | 10,793 | -0.121 | **-0.513** | -0.093 [-0.119, -0.073] pct 25 | 15,903 | -0.092 | **-0.448** | -0.101 [-0.121, -0.080] pct 65 |

*(5m retest-hold rows outside the tuning era are P-BRK-S1's collared scoring ground and are not printed.)*

**4h · frozen3.0 · era ALL · H20**

| class | C5 n | C5 med H20 | C5 **NET H20** | C5 null g+o med [q25, q75] pct | U12 n | U12 med H20 | U12 **NET H20** | U12 null g+o med [q25, q75] pct |
|---|---:|---:|---:|---|---:|---:|---:|---|
| breach | 584 | +0.102 | **+0.041** | +0.014 [-0.126, +0.143] pct 65 | 886 | -0.096 | **-0.148** | -0.083 [-0.223, +0.082] pct 45 |
| harden | 289 | -0.037 | **-0.096** | +0.154 [-0.199, +0.397] pct 30 | 484 | +0.072 | **+0.022** | +0.001 [-0.176, +0.138] pct 60 |
| DIE | 295 | +0.033 | **-0.030** | +0.146 [+0.062, +0.367] pct 20 | 402 | +0.144 | **+0.095** | +0.042 [-0.155, +0.134] pct 75 |
| memory-touch-v1 | 531 | -0.091 | **-0.150** | -0.021 [-0.134, +0.114] pct 40 | 709 | +0.191 | **+0.143** | +0.151 [+0.049, +0.273] pct 60 |
| memory-touch-2s | 370 | -0.145 | **-0.205** | -0.098 [-0.298, +0.141] pct 35 | 509 | +0.028 | **-0.015** | +0.121 [-0.017, +0.283] pct 30 |
| flip-hold | 247 | +0.216 | **+0.159** | +0.025 [-0.065, +0.167] pct 80 | 331 | -0.044 | **-0.084** | +0.054 [-0.045, +0.116] pct 25 |
| retest-hold-ribbon89_127 *(TUNED)* | 267 | +0.506 | **+0.443** | +0.262 [+0.100, +0.469] pct 75 | 354 | +0.120 | **+0.073** | +0.080 [-0.003, +0.155] pct 65 |
| retest-hold-ribbon127_200 *(TUNED)* | 258 | +0.520 | **+0.455** | +0.213 [+0.069, +0.452] pct 80 | 346 | -0.104 | **-0.155** | -0.095 [-0.237, +0.064] pct 40 |
| retest-hold-tap89 *(TUNED)* | 236 | +0.747 | **+0.681** | +0.380 [+0.211, +0.630] pct 85 | 300 | +0.107 | **+0.064** | +0.022 [-0.141, +0.094] pct 85 |
| retest-hold-tap127 *(TUNED)* | 221 | +0.591 | **+0.524** | +0.346 [-0.109, +0.481] pct 85 | 285 | -0.018 | **-0.063** | +0.051 [-0.134, +0.113] pct 40 |
| retest-hold-tap200 *(TUNED)* | 191 | -0.086 | **-0.143** | -0.006 [-0.185, +0.280] pct 50 | 248 | +0.341 | **+0.291** | +0.150 [+0.103, +0.435] pct 65 |

**1d · frozen3.0 · era ALL · H20**

| class | C5 n | C5 med H20 | C5 **NET H20** | C5 null g+o med [q25, q75] pct | U12 n | U12 med H20 | U12 **NET H20** | U12 null g+o med [q25, q75] pct |
|---|---:|---:|---:|---|---:|---:|---:|---|
| breach | 105 | +0.582 | **+0.558** | +0.364 [-0.165, +0.889] pct 65 | 126 | -0.078 | **-0.097** | -0.091 [-0.281, +0.337] pct 60 |
| harden | 55 | -0.750 | **-0.775** | -0.001 [-0.600, +0.247] pct 25 | 62 | +0.251 | **+0.231** | -0.144 [-0.328, +0.332] pct 70 |
| DIE | 50 | +0.346 | **+0.323** | +0.437 [+0.136, +0.607] pct 40 | 64 | +0.152 | **+0.127** | +0.073 [-0.415, +0.604] pct 50 |
| memory-touch-v1 | 79 | +0.628 | **+0.603** | +0.182 [-0.098, +0.405] pct 80 | 93 | +0.477 | **+0.453** | +0.047 [-0.207, +0.426] pct 80 |
| memory-touch-2s | 53 | +0.583 | **+0.559** | +0.097 [-0.311, +0.274] pct 90 | 69 | +0.656 | **+0.633** | -0.047 [-0.222, +0.176] pct 90 |
| flip-hold | 44 | +0.970 | **+0.948** | +0.105 [-0.087, +0.322] pct 95 | 48 | +0.552 | **+0.525** | +0.085 [-0.150, +0.381] pct 85 |
| retest-hold-ribbon89_127 *(TUNED)* | 42 | +0.444 | **+0.418** | +0.131 [-0.014, +0.365] pct 80 | 50 | -0.003 | **-0.021** | -0.082 [-0.336, +0.296] pct 55 |
| retest-hold-ribbon127_200 *(TUNED)* | 38 | +0.368 | **+0.344** | -0.249 [-0.359, +0.020] pct 90 | 48 | -0.170 | **-0.189** | -0.178 [-0.422, -0.088] pct 55 |
| retest-hold-tap89 *(TUNED)* | 35 | +0.425 | **+0.399** | +0.130 [-0.032, +0.272] pct 80 | 42 | +0.007 | **-0.010** | -0.102 [-0.378, +0.093] pct 55 |
| retest-hold-tap127 *(TUNED)* | 31 | +0.440 | **+0.420** | -0.075 [-0.298, +0.167] pct 88 | 39 | -0.127 | **-0.145** | -0.298 [-0.485, -0.090] pct 72 |
| retest-hold-tap200 *(TUNED; C5 n<30)* | 28 | -0.265 | **-0.294** | -0.319 [-0.503, -0.161] pct 55 | 31 | +0.252 | **+0.233** | -0.255 [-0.776, +0.243] pct 80 |

**4h · frozen3.0 · era holdout · H20**

| class | C5 n | C5 med H20 | C5 **NET H20** | C5 null g+o med [q25, q75] pct | U12 n | U12 med H20 | U12 **NET H20** | U12 null g+o med [q25, q75] pct |
|---|---:|---:|---:|---|---:|---:|---:|---|
| breach | 201 | -0.579 | **-0.656** | -0.238 [-0.507, +0.323] pct 20 | 479 | -0.245 | **-0.312** | -0.056 [-0.213, +0.035] pct 20 |
| harden | 100 | +0.702 | **+0.626** | +0.201 [-0.037, +0.598] pct 90 | 263 | -0.015 | **-0.082** | +0.016 [-0.083, +0.183] pct 45 |
| DIE | 101 | -0.299 | **-0.370** | -0.249 [-0.657, +0.215] pct 50 | 216 | -0.079 | **-0.145** | +0.002 [-0.262, +0.138] pct 40 |
| memory-touch-v1 | 203 | -0.091 | **-0.158** | +0.115 [+0.028, +0.289] pct 20 | 402 | -0.073 | **-0.128** | +0.201 [+0.054, +0.315] pct 15 |
| memory-touch-2s | 131 | +0.252 | **+0.181** | +0.083 [-0.184, +0.315] pct 65 | 281 | -0.070 | **-0.121** | +0.085 [-0.106, +0.261] pct 30 |
| flip-hold | 87 | +0.962 | **+0.904** | -0.171 [-0.383, +0.211] pct 95 | 181 | +0.176 | **+0.136** | +0.259 [+0.038, +0.394] pct 35 |
| retest-hold-ribbon89_127 *(TUNED)* | 97 | +0.506 | **+0.426** | +0.266 [+0.085, +0.721] pct 68 | 191 | +0.496 | **+0.431** | +0.324 [+0.123, +0.451] pct 80 |
| retest-hold-ribbon127_200 *(TUNED)* | 94 | +0.671 | **+0.597** | +0.333 [-0.048, +0.771] pct 60 | 185 | -0.129 | **-0.185** | -0.132 [-0.281, +0.066] pct 50 |
| retest-hold-tap89 *(TUNED)* | 88 | +0.786 | **+0.706** | +0.480 [+0.265, +0.775] pct 75 | 158 | +0.338 | **+0.272** | +0.086 [-0.021, +0.373] pct 70 |
| retest-hold-tap127 *(TUNED)* | 83 | +0.116 | **+0.039** | -0.143 [-0.366, +0.722] pct 60 | 149 | +0.041 | **-0.016** | +0.047 [-0.132, +0.110] pct 45 |
| retest-hold-tap200 *(TUNED)* | 63 | +0.068 | **-0.004** | +0.204 [-0.118, +0.489] pct 35 | 120 | +0.195 | **+0.134** | +0.232 [+0.052, +0.527] pct 50 |

**1d · frozen3.0 · era holdout · H20** *(almost every cell is provisional, n < 30)*

| class | C5 n | C5 med H20 | C5 **NET H20** | C5 null g+o med [q25, q75] pct | U12 n | U12 med H20 | U12 **NET H20** | U12 null g+o med [q25, q75] pct |
|---|---:|---:|---:|---|---:|---:|---:|---|
| breach | 40 | +0.203 | **+0.177** | +0.298 [-0.588, +0.744] pct 40 | 65 | +0.409 | **+0.387** | -0.030 [-0.323, +0.708] pct 70 |
| harden | 21 | -0.594 | **-0.620** | +0.129 [-1.139, +0.465] pct 40 | 33 | -0.334 | **-0.360** | -0.095 [-0.854, +0.464] pct 35 |
| DIE | 19 | +0.255 | **+0.231** | +0.320 [-0.510, +0.580] pct 45 | 32 | +0.840 | **+0.813** | +0.433 [+0.020, +1.130] pct 60 |
| memory-touch-v1 | 37 | +0.400 | **+0.374** | +0.058 [-0.397, +0.589] pct 70 | 49 | +0.681 | **+0.657** | +0.075 [-0.034, +0.351] pct 98 |
| memory-touch-2s | 23 | +0.314 | **+0.285** | +0.119 [-0.166, +0.273] pct 80 | 33 | +0.708 | **+0.685** | -0.153 [-0.308, +0.123] pct 90 |
| flip-hold | 19 | +0.854 | **+0.832** | +0.038 [-0.176, +0.805] pct 75 | 28 | +0.726 | **+0.702** | +0.110 [-0.347, +0.808] pct 70 |
| retest-hold-ribbon89_127 *(TUNED)* | 16 | +0.352 | **+0.326** | +0.102 [-0.332, +0.541] pct 65 | 24 | -0.093 | **-0.117** | -0.370 [-0.556, +0.051] pct 60 |
| retest-hold-ribbon127_200 *(TUNED)* | 12 | +0.179 | **+0.148** | -0.539 [-1.435, +0.243] pct 70 | 22 | -0.000 | **-0.023** | -0.179 [-0.905, +0.634] pct 60 |
| retest-hold-tap89 *(TUNED)* | 13 | +0.019 | **-0.008** | +0.287 [-0.213, +0.853] pct 35 | 18 | -0.390 | **-0.410** | -0.636 [-1.156, +0.025] pct 55 |
| retest-hold-tap127 *(TUNED)* | 9 | -0.089 | **-0.128** | -0.219 [-1.077, +0.205] pct 55 | 17 | -0.362 | **-0.388** | -0.387 [-0.905, +0.289] pct 50 |
| retest-hold-tap200 *(TUNED)* | 11 | -0.503 | **-0.534** | -0.849 [-1.087, -0.070] pct 65 | 13 | -0.564 | **-0.585** | -0.528 [-0.845, +0.031] pct 45 |

**What these tables show, and do not:**
- **At 5m every class is NET negative on both panels.** The real DIE median sits at the null's 0th percentile on both.
- **At 4h, the tuned retest-hold bands on CLASSIC5 are the strongest positive NET in the 4h era-ALL table.** They are
  not the strongest in the census: 1d flip-hold CLASSIC5 reads +0.948 on ALL, and 4h flip-hold CLASSIC5 +0.904 on the
  holdout. On 4h era ALL, tap89 is +0.681 and ribbon127_200 is +0.455. **But the pins were TUNED, and they do not carry to UNSEEN12:** tap89 +0.064, ribbon127_200
  −0.155.
- **At 1d, most classes are NET positive on CLASSIC5,** and the null of record sits well below many of them. The
  cells are small, and the holdout is almost wholly provisional.
- **None of this is a result.** It is a selection over 7,920 outcome cells.

### 2.4 · Coverage · density · life, and F-RF-4

**Per asset, frozen3.0** `[close/S2_CENSUS_R.md §2.4]`. Each lens column reads coverage % of all bars · confirmed
ranges per 100 bars · mean life in bars. The last column is the 4h calibrated SCALE, which is in-sample by construction.
**SCALE_MULT for 5m and 1d** is not reprinted here: the per-asset 5m and 1d calibrated SCALE columns are
`[close/S2_CENSUS_R.md §2.4, L580–L601 (5m) and L624–L645 (1d)]`, and the calibrator's whole grid stays in the digest
(`census/CENSUS_R_DIGEST.md` L803–L860).

| asset | 5m | 4h | 1d | 4h SCALE cal |
|---|---|---|---|---:|
| BTCUSDT | 45.84 · 0.383 · 122.6 | 29.98 · 0.409 · 76.4 | 36.05 · 0.428 · 83.7 | 2 |
| ETHUSDT | 42.73 · 0.393 · 111.5 | 33.21 · 0.422 · 81.0 | 15.79 · 0.362 · 46.1 | 2 |
| SOLUSDT | 39.51 · 0.386 · 105.8 | 32.68 · 0.402 · 84.6 | 23.62 · 0.546 · 46.8 | 2 |
| NEARUSDT | 41.72 · 0.362 · 119.1 | 29.72 · 0.446 · 70.0 | 37.12 · 0.369 · 106.5 | 2 |
| ZECUSDT | 41.15 · 0.383 · 111.1 | 32.42 · 0.420 · 80.0 | 45.35 · 0.537 · 85.8 | 2 |
| ENAUSDT | 39.40 · 0.373 · 109.6 | 25.01 · 0.443 · 59.6 | 23.53 · 0.111 · 217.0 | 2.25 |
| PUMPUSDT | 34.81 · 0.410 · 88.4 | 37.13 · 0.266 · 141.3 | 17.39 · 0.458 · 41.0 | 2.25 |
| HYPEUSDT | 40.82 · 0.393 · 108.1 | 25.70 · 0.522 · 52.5 | 1.67 · 0.418 · 4.5 | 1.75 |
| MNTUSDT_BYBIT | 39.01 · 0.428 · 94.4 | 33.67 · 0.476 · 75.1 | 47.60 · 0.461 · 104.8 | 2 |
| SUIUSDT | 40.69 · 0.377 · 111.6 | 36.12 · 0.404 · 92.8 | 30.02 · 0.243 · 17.5 | 1.75 |
| LTCUSDT | 43.45 · 0.371 · 120.7 | 40.99 · 0.436 · 97.0 | 23.39 · 0.531 · 48.9 | 2 |
| XMRUSDT | 45.57 · 0.357 · 132.0 | 48.95 · 0.275 · 181.8 | 50.31 · 0.124 · 408.7 | 1.5 |
| BNBUSDT | 39.78 · 0.395 · 104.1 | 46.80 · 0.338 · 144.2 | 32.56 · 0.331 · 99.4 | 1.75 |
| UNIUSDT | 40.05 · 0.381 · 108.7 | 37.60 · 0.418 · 92.7 | 45.19 · 0.410 · 112.3 | 2 |
| 1000PEPEUSDT | 43.92 · 0.365 · 123.7 | 42.55 · 0.405 · 108.2 | 28.36 · 0.567 · 55.8 | 1.75 |
| DOGEUSDT | 45.59 · 0.351 · 133.2 | 43.01 · 0.339 · 129.8 | 25.76 · 0.442 · 61.1 | 1.75 |
| 1000BONKUSDT | 38.89 · 0.387 · 104.1 | 40.34 · 0.322 · 134.8 | 52.27 · 0.484 · 114.6 | 1.75 |

**F-RF-4 · spring / upthrust overlap, both directions, frozen3.0** `[digest §2; census/spring_overlap.parquet]`.
`bottom` = springs, `top` = upthrusts. The census reproduces the v1 suite's 8/8, 6/8 and 6/25
`[census/FIXTURES_CENSUS.txt]`.

| lens | side | hardens | law reclaim | also sweep the look | house shapes | inside an episode |
|---|---|---:|---:|---:|---:|---:|
| 1d | bottom | 82 | 82 | 53 | 1,219 | 35 |
| 1d | top | 35 | 35 | 28 | 1,694 | 24 |
| 4h | bottom | 378 | 378 | 249 | 8,579 | 214 |
| 4h | top | 397 | 397 | 305 | 9,898 | 261 |
| 5m | bottom | 21,417 | 21,417 | 15,606 | 392,387 | 11,930 |
| 5m | top | 22,662 | 22,662 | 16,900 | 415,466 | 13,331 |

### 2.5 · The Tier-E tables of contract line 113 — P-AGE-1 · boundary-fade · regime-prior

*"P-AGE-1 (tide-youth), boundary-fade, regime-prior: Tier-E tables only."* None of these has a registration, a
verdict, a p, a CI or a bar. All are in sample.

**P-AGE-1 · tide-youth** `[close/P_AGE_1_TIDE_YOUTH.md]`, sha256 `b1c5a7bc…`; fixtures 7/7, 14/14 break legs RED.
- **Definition, an executor reading with no new pin.** Tide-youth is the age of the 4h tide at the entry bar,
  `tierc7_lab_regime.tide_streak`. It is banded by the regime lab's own quartiles, with TRAILING causal edges exactly
  as TC9's TC7-g.
- **Book.** The lab's v6 book equals `panel/control_journal.parquet` exactly (F-AGE-BOOK).

| band | n | net R | expectancy R | win % | share of card net R % |
|---|---:|---:|---:|---:|---:|
| B1 YOUNG tide *(provisional, n < 30)* | 25 | +11.7692 | +0.4708 | 52.0 | 28.2 |
| B2 EARLY tide | 60 | +34.6369 | +0.5773 | 40.0 | 83.0 |
| B3 MATURE tide | 56 | +17.9938 | +0.3213 | 35.7 | 43.1 |
| B4 OLD tide | 59 | −22.6566 | −0.3840 | 20.3 | −54.3 |
| ALL | 200 | +41.7433 | +0.2087 | 34.5 | 100.0 |

**Look-ahead measured.** Band counts under whole-corridor edges are 23/57/62/58, against 25/60/56/59 trailing. The
2020-01-01 streak edges were [35.0, 107.0, 199.5] trailing, against [88.0, 206.0, 396.0] whole-corridor. **TC9's filed
`tc7g_tide_streak_bands` counts its campaigns on the look-ahead edges** (finding §5.14).

**Boundary-fade = the census EDGE-FADE leg.** The contract equates them (:78-79, "boundary-fade stays Tier-E"), and the
table is `[census/edge_fade.parquet]`, 55,440 rows. It is labelled "edge-fade" on disk. Near edge only, POOLED:ALL ·
frozen3.0 · era ALL · H20, NET in ATR by range age at entry `[digest B.2]`:

| lens | 0-5 | 5-10 | 10-20 | 20-40 | 40-80 | 80+ | near-edge n | ranges |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 5m | −0.2612 | −0.3138 | −0.3380 | −0.3714 | −0.3735 | −0.3810 | 999,378 | 32,546 |
| 4h | −0.1918 | −0.0610 | −0.0854 | −0.0121 | −0.0821 | −0.1779 | 21,902 | 696 |
| 1d | −0.0108 | −0.2947 | −0.4661 | +0.0405 | +0.3767 | −0.3757 | 3,855 | 118 |

**The 5m fade worsens monotonically with range age.** No 4h bucket is positive.

**Regime-prior** `[close/REGIME_PRIOR.md]`, sha256 `cb793efc…`; fixtures 8/8 GREEN, 8/8 sabotages RED.
- **The prior is quoted whole and never parsed.** ARGUS note item 2
  (`exchange/reports/NOTE_ARGUS_to_APOLLO_2026-08-22_P-RNG_slate.md`): *"~80% of BTC daily time in-range — offered as a
  REGIME PRIOR for exit studies, not as a rule; our window measures 60.0% under the v0 reconstruction"*.
- **Table 1 copies coverage verbatim**, 102 rows. For example, BTCUSDT 1d `bars_in_live_range_pct` is 36.862592 on
  frozen3.0 and 35.539120 calibrated.
- **Table 2 crosses the v6 CLASSIC5 book by 4h macro state at entry and at exit.** The entry marginal equals the
  Stage-A table exactly (F-RP-ANCHOR):

| state | n at entry | E[R] by entry state | n at exit | E[R] by exit state |
|---|---:|---:|---:|---:|
| NEUTRAL (a confirmed range alive) | 94 | +0.296646 | 83 | −0.425079 |
| BULL_EXP | 66 | +0.219842 | 67 | +0.728606 |
| BEAR_EXP | 40 | −0.016275 | 50 | +0.564166 |
| ALL | 200 | +0.208717 | 200 | +0.208717 |

- **The largest cell** is NEUTRAL→NEUTRAL: n 68, −0.466931.
- **`rf4h_in_range` adds nothing.** It equals `macro_state == NEUTRAL` on 200/200 stamps at entry and at exit, the
  stamps' four-valued collapse [LEAN S-a].
- **In-sample control cuts, not claims.**

---

## 3 · STAGE D MANIFEST — including the F-D-4 and F-D-5 tables

*The full manifest is `[data/STAGE_D_MANIFEST.md]`, 65,336 B; the close selection is `[close/S3_STAGE_D.md]`,
sha256 `eca42576…`, with ten byte-exact spans, F-S3 8/8 PASS and 31/31 plants RED
`[close/FIXTURES_CLOSE_stage_d.txt]`. All 15 D-CORE artifacts re-hash MATCH against `PROGRESS.json`. Every table below
is REPORT-ONLY.*

### 3.1 · Status — F-D-1 is RED, and D-CORE and D-5M stay PARTIAL on it alone

- **The filed ONLINE run** `[data/FIXTURES_STAGE_D.txt:77]` reads `[FAIL]`: 3 bars differ, all XMRUSDT. The bars are
  4h 2025-01-14T12:00Z, 1h 2024-10-28T20:00Z and 5m 2024-10-28T20:00Z. The offline suite lists F-D-1 as NOT RUN and
  passes 17/17 `[data/FIXTURES_STAGE_D_OFFLINE.txt]`.
- **R5 does not settle it.** *"The USDT pair, either on Binance or Bybit"* names the pair and permits the venue. **It
  does not choose between the venue's REST API and its BULK ARCHIVE**, and those two publish different bars on incident
  stamps.
- **No bar is rewritten either way without the narrower word** (§6 Q1).
- **P-BRK-S1 is not reached by it:** it pins substrate `tc10_20260921` `[PROGRESS.json stages[10].blockers[0]]`.

### 3.2 · Venue of record

- **Binance USDT-M perpetuals for 16 of the 17.**
- **MNT is Bybit v5 linear**, stem MNTUSDT_BYBIT. It is absent from Binance USDT-M, so the whole tape is Bybit: one
  venue, never spliced [LEAN D-c].
- **PUMPFUN → PUMPUSDT** [LEAN D-d]. `PUMPBTCUSDT` is rejected by name: *"baseAsset PUMPBTC != PUMP: a different
  asset"*.
- **Two contract premises are stale.**
  - XMR: *"STALE — XMRUSDT is a TRADING Binance USDT-M PERPETUAL (listed 2020-02-03T08:00:00Z); the WHOLE tape is
    Binance, no alternate venue is used"*. The contract's "delisted from Binance 2024-02" premise does not hold.
  - HYPE: the alternate-venue clause is not triggered.
- Source: `[close/S3_STAGE_D.md "Venue of record"]`.

### 3.3 · Contract multipliers

- **The venue publishes no multiplier field.** The multiplier lives in the baseAsset name [LEAN D-l]: *"EVERY PRICE ON
  1000PEPEUSDT IS QUOTED PER 1000 TOKENS AND EVERY PRICE ON 1000BONKUSDT IS QUOTED PER 1000 TOKENS."*
- **Normalization is a pure scaling.** It is proven to 1.07e-11 over 180,013 bars `[PROGRESS.json stages[1].one_line]`,
  so no R, ATR-height or log-return statistic can move. The capture is `[data/CONTRACT_SPECS.json]`, sha `275b218d…`.

### 3.4 · F-D-4 · THE TWO-TOKEN TRAP (the LIT precedent)

*FAILS IF any symbol's history predates its intended listing unfloored. Listing source: the venue's own
onboardDate / launchTime, captured write-once in `VENUE_PROBE.json` before the first bar was fetched
`[close/S3_STAGE_D.md, spliced from STAGE_D_MANIFEST.md]`.*

| asset | symbol | intended base = venue baseAsset | listing | first 4h bar | predates the listing instant | predates the hard floor | hard-floored, every lens |
|---|---|---|---|---|---|---|---|
| BTC | BTCUSDT | BTC | 2019-09-08T17:55Z | 2019-09-08T16:00Z | True | **False** | True |
| ETH | ETHUSDT | ETH | 2019-11-27T07:45Z | 2019-11-27T04:00Z | True | **False** | True |
| SOL | SOLUSDT | SOL | 2020-09-14T07:00Z | 2020-09-14T04:00Z | True | **False** | True |
| NEAR | NEARUSDT | NEAR | 2020-10-15T08:00Z | 2020-10-15T08:00Z | False | **False** | True |
| ZEC | ZECUSDT | ZEC | 2020-02-05T08:00Z | 2020-02-05T08:00Z | False | **False** | True |
| ENA | ENAUSDT | ENA | 2024-04-02T12:30Z | 2024-04-02T12:00Z | True | **False** | True |
| PUMPFUN | PUMPUSDT | PUMP | 2025-07-10T07:30Z | 2025-07-10T04:00Z | True | **False** | True |
| HYPE | HYPEUSDT | HYPE | 2025-05-30T10:30Z | 2025-05-30T08:00Z | True | **False** | True |
| MNT | MNTUSDT (Bybit) | MNT | 2023-10-02T05:40:55Z | 2023-10-02T04:00Z | True | **False** | True |
| SUI | SUIUSDT | SUI | 2023-05-03T00:00Z | 2023-05-03T16:00Z | False | **False** | True |
| LTC | LTCUSDT | LTC | 2020-01-09T08:05Z | 2020-01-09T08:00Z | True | **False** | True |
| XMR | XMRUSDT | XMR | 2020-02-03T08:00Z | 2020-02-03T08:00Z | False | **False** | True |
| BNB | BNBUSDT | BNB | 2020-02-10T08:00Z | 2020-02-10T08:00Z | False | **False** | True |
| UNI | UNIUSDT | UNI | 2020-09-18T07:00Z | 2020-09-18T04:00Z | True | **False** | True |
| PEPE | 1000PEPEUSDT | 1000PEPE | 2023-05-05T00:00Z | 2023-05-05T16:00Z | False | **False** | True |
| DOGE | DOGEUSDT | DOGE | 2020-07-10T09:00Z | 2020-07-10T08:00Z | True | **False** | True |
| BONK | 1000BONKUSDT | 1000BONK | 2023-11-22T14:00Z | 2023-11-22T12:00Z | True | **False** | True |

- **Result: PASS.** Cells checked: 102 (17 assets × 6 lenses). **Bars before a floor: 0.** Intended asset confirmed
  17/17. Floor bars rebuilt exactly from their 5m children: 17/17.
- **Floor seams: 0 exist**, so the continuity arm binds on nothing and is proven by its BREAK leg alone [LEAN D-i].
- **Re-measured at CLOSE through `load_asof`:** 102 cells, 0 pre-floor bars `[close/S3_STAGE_D.md "F-D-4 tally"]`.
- **"Predates the listing instant: True" is the bar that contains the listing.** It is the floor bar itself, not
  prior-asset history.

### 3.5 · F-D-5 · THE DATA-SPEND AUDIT {never-touched / display-only / scored}

- **Corpus:** 65 files, grepped whole `[data/DATA_SPEND_AUDIT.json]`.
- **Class is decided by the registers, read as literals, not by hit counts:**
  - the TC-series scored universe, `scripts/tierc2_rules.py` `REGISTER['UNIVERSE']`;
  - the Oracle display roster, `scripts/oracle_daily.py` `REGISTER['ROSTER']`, 18 symbols;
  - the frozen study basket, `engine/cells.py` `SYMBOLS`.
- **A never-touched asset must have zero `root_book` hits.** The rule is one-directional and conservative.

| asset | class | TC-series scored universe | Oracle display roster | frozen study basket | grep hits |
|---|---|---|---|---|---:|
| BTC | scored | True | True | True | 242 |
| ETH | scored | True | True | True | 156 |
| SOL | scored | True | True | True | 134 |
| NEAR | scored | True | True | True | 129 |
| ZEC | scored | True | True | True | 191 |
| ENA | display-only | False | True | False | 6 |
| **PUMPFUN** | **never-touched** | False | False | False | 9 |
| HYPE | display-only | False | True | True | 65 |
| **MNT** | **never-touched** | False | False | False | 7 |
| **SUI** | **never-touched** | False | False | False | 0 |
| LTC | display-only | False | True | False | 6 |
| XMR | display-only | False | True | False | 9 |
| BNB | display-only | False | True | False | 7 |
| UNI | display-only | False | True | False | 6 |
| PEPE | display-only | False | True | False | 4 |
| DOGE | display-only | False | True | False | 6 |
| BONK | display-only | False | True | False | 4 |

- **Counts:** scored 5, display-only 9, never-touched 3. **Never-touched = PUMPFUN, MNT, SUI.** This is P-GEN-1's
  second LOAO panel.
- **PUMPFUN and HYPE were read, not assumed.** The contract required it.
  - PUMPFUN's hits are in `exchange/status/LEDGER_ARGUS.md:545` and the oracle roster probe. The ledger line
    (*"PUMPFUN MNT ZCAT, none has a Binance perpetual"*) contradicts the venue probe, which found PUMPUSDT TRADING.
    It is spliced as filed.
  - HYPE is display-only: it is in the roster and the basket, never in a scored book.

### 3.6 · The tiered haircut twin — and the v6 control's own twin

**The tiers are the contract clause, parsed, not typed** `[data/fee_schedule.json haircut_twin_tiers]`. The charter
line (`Naiad_Phase0_Charter.md:114`) names a different roster. The TC-series round trip of 10 bps is **untouched on all
17**.

| tier | slippage bps / side | assets | charter round trip (fee 5 + slippage, per side ×2) |
|---|---:|---|---:|
| A | 2.0 | BTC ETH | 14 bps |
| B | 5.0 | SOL NEAR ZEC LTC BNB DOGE UNI SUI XMR | 20 bps |
| C | 10.0 | ENA PUMPFUN HYPE MNT PEPE BONK | 30 bps |

- **Cost law** `[fee_schedule.json haircut_twin_law]`: `net_r_twin = gross_r - cost_px / risk_px`, where
  `cost_px = ((FEE_BPS_SIDE + slippage_bps_side) / 10_000) * (entry_px + exit_px)`. **No funding term.**
- **The 5-asset v6 control's twin is an ADDED column** (contract :53-55) `[close/V6_CONTROL_HAIRCUT_TWIN.md]`,
  fixtures 5/5 GREEN, 9/9 breaks RED. R per campaign:

| era | n | TC-series (untouched) | haircut twin (ADDED) | companion = twin − funding (NOT the filed twin) | twin sign ≠ TC |
|---|---:|---:|---:|---:|---|
| full | 200 | +0.208717 | +0.217150 | +0.188157 | no |
| tuning | 123 | −0.010763 | +0.014494 | −0.030517 | **YES** |
| holdout | 77 | +0.559314 | +0.540874 | +0.537466 | no |

- **Per asset, full era** (TC / twin): BTC −0.126742 / −0.115436 · ETH +0.145862 / +0.175217 · NEAR −0.039190 /
  −0.045286 · SOL +0.270521 / +0.279882 · ZEC +0.851723 / +0.844793.
- **The ETH tuning row also flips:** TC −0.006406, twin +0.054767.
- **The reuse tolerance was relaxed.** The spec asked for 1e-12, which cannot be met because the journal files R at
  6 dp. The leg asserts a derived bound of 5.630e-07; the measured difference is 9.572e-09.

### 3.7 · As-of hazards, and the two publications

- **Klines past the pin.** 14 of the 102 kline files hold 6 rows past the pin: every 5m file except PUMPUSDT,
  MNTUSDT_BYBIT and SUIUSDT [LEAN D-e].
  - `tierc10_data.load_asof` cuts them. `tierc2_baseline.load_klines` reads the whole file and would read past the pin.
  - D-5M certifies that every 5m reader cuts at the pin, with the uncut loader as the sabotage
    `[PROGRESS.json stages[10].one_line]`.
- **Funding.** A print belongs to the hour its stamp floors to [LEAN D-g]. The largest offset past the hour is 47 ms.
- **The panel is publication-heterogeneous.** At 4h, 5m and 1h:
  - identical to REST: BTC ETH SOL NEAR ZEC SUI LTC;
  - identical to the ARCHIVE: ENA XMR BNB UNI PEPE DOGE BONK;
  - identical to both: PUMP, HYPE;
  - single publication: MNT (Bybit).
- **The archive is no clean alternative.** At 4h it lacks 120 bars the snapshot holds, and it publishes nothing before
  2020 `[close/S3_STAGE_D.md "publications disagree"]`.

### 3.8 · F-D-3 · funding coverage per asset — pointer, not reprinted

- **The fixture:** `[PASS] F-D-3: 17 panel assets: funding present, non-empty, last stamp within ONE observed funding
  interval of the kline edge 2026-09-21T16:00:00Z` `[data/FIXTURES_STAGE_D_OFFLINE.txt:48]`.
- **The per-asset table** is the 17 `funding` rows of `[close/S3_STAGE_D.md "Per asset × lens", L120–L250]`: each gives
  prints as-of, first and last stamp, rows past the pin, and gaps. All 17 read 0 past the pin, gaps "— (coverage OK)",
  and re-measured OK.

---

## 4 · FIXTURES — the transcripts of record

| suite | transcript (sha256[:16]) | reads |
|---|---|---|
| STEP 0 · RF port | `FIXTURES_RF.txt` `c6d10b8e40019a85` | 7/7 GREEN; PINS-OK 12/12; [Q-R5] holds |
| Stage D offline | `data/FIXTURES_STAGE_D_OFFLINE.txt` `8295ce69725c0a8a` | 17/17 PASS; F-D-1/F-D-1b NOT RUN |
| Stage D online | `data/FIXTURES_STAGE_D.txt` `fd302025991fe5d5` | 18/19; **F-D-1 RED by design** |
| CENSUS-R | `census/FIXTURES_CENSUS.txt` `a675bb2fed6f4836` | 14/14 GREEN (F-RNG-ASOF, F-RNG-ASOF-SEAL, F-RF-4, F-C10-ACC, F-C10-HT, F-C10-HT-ERA, F-C10-COLLAR, F-C10-TOLL, F-GRID, F-DET …) |
| NULL gaps-only / gaps+order | `null/*/FIXTURES_NULL.txt` `bf514670…` / `68a8654c…` | 6/6 and 6/6 GREEN |
| A · stamps | `stamps/FIXTURES_STAMPS.txt` `778127ffc81adc93` | 9 GREEN, 0 RED (F-STAMP-CLOSURE, F-KEY, F-DET) |
| PANEL | `panel/FIXTURES_PANEL.txt` `163f65bdf21a575c` | 22/22; **F-CTRL/a 0.000e+00 over 12 columns, n 200** (in process, against `tierc6.run_cell`, `:13`); **F-CTRL/b** cross-process against the filed tierc9 journal PASSES with one attributed drift (`:34`, below); F-KEY |
| LANES | `lanes/FIXTURES_LANES.txt` `eb1d62669016c9a3` | 15/15; F-C10-BE [NOT RUN] per §9 |
| BRK | `brk/FIXTURES_BRK.txt` `10ed919e9d9ee522` | 20/20; F-C10-HOLD ×3, F-C10-TOLL, F-BRK-ROW |
| SCORE driver | `scores/FIXTURES_SCORE.txt` `9a83da67a91a36bd` | 16/16, 26/26 break legs RED; `.scored.json` untouched by the suite |
| F-C10-RESUME | `FIXTURES_RESUME.txt` `d36cf42e8dc40deb` | 9 GREEN, 0 RED; 1,090 artifact shas MATCH; tampered partial FAILs |
| CLOSE builders (13) | `close/FIXTURES_CLOSE_*.txt` | forward strip 9/9 · P-AGE-1 7/7 · regime-prior 8/8 · v6 twin 5/5 · S0 10/10 · stage log 7/7 · census-R 9/9 · stage D 8/8 · findings 6/6 · box-cost 5/5 · F-LA ledger source-quote draft 11/11 (30/30 sabotages RED) · **F-SS P-TRG-2 seen share 9/9** · **F-LAR ledger append of record 9/9** — **all run whole twice, byte-identical** |
| F-SS · the seen share | `close/FIXTURES_CLOSE_p_trg_2_seen_share.txt` `780034a0dccd4125` | 9/9 GREEN; every leg's sabotage RED; builds `close/P_TRG_2_SEEN_SHARE.{json,md}` (§0.3) |
| F-LA · ledger source-quote draft | `close/FIXTURES_CLOSE_ledger_append.txt` `18d49d1eb050d3d3` | 11/11 GREEN, 30/30 sabotages RED, over `close/LEDGER_APOLLO_APPEND.draft.md` `fea0d6519bfea034`, which is **NOT the append** (§8) |
| F-LAR · the append of record | `close/FIXTURES_CLOSE_ledger_append_root.txt` (sha in PROGRESS.json, stage CLOSE — it reads git state, so it moves with every commit) | 9/9 GREEN over **`LEDGER_APOLLO_APPEND.md` `d6a58f5c2901f177`** (14,925 B): 25 cites verified by F-LA's own `verify_quote`, 86 traced literals, every digit of the prose covered, 18 word claims, 1 pending stamp (§8) |

- **F-CTRL, both halves.** The contract asks for F-CTRL "0.000e+00 over TC9's corridor, cross-process anchored to the
  filed tierc9 journal" (contract :120-121).
  - **F-CTRL/a is the 0.000e+00.** It runs in process: `run_cell_n(v6-control, V6_ROLES, CLASSIC5)` against
    `tierc6.run_cell(CARD_V6)`, worst abs diff 0.000e+00 over 12 columns, n 200 `[panel/FIXTURES_PANEL.txt:13]`.
  - **F-CTRL/b is the cross-process anchor, and it is not a zero.** It PASSES with one attributed drift: *"funding_r
    moved on 1 closed campaign(s) — ZECUSDT 2026-08-17T04:00:00Z: funding_r 0.0 -> 0.014324, net_r -1.039899 ->
    -1.054223 [ATTRIBUTION: the referee rode on funding stale at 2026-08-15; Stage D's top-up supplied the stamps.
    Substrate drift, not code.]"* `[:34]`. gross_r, fee_r and mfe_r are exact on all 196 closed campaigns `[:33]`.
  - **What the drift explains.** v6 at or before TIER-C9's as-of re-nets +38.7901 R here against TIER-C9's filed
    +38.8044 R. F-SS-V6 re-derives the same single attribution, campaign by campaign
    `[close/P_TRG_2_SEEN_SHARE.json v6_base_vs_tc9_filed]`.
- **F-C10-TOLL:** all 1,649 quotes returned by `get_toll` equal the toll re-derived from raw bars. It reads
  `outcome_grid.parquet` and never types a value `[census/FIXTURES_CENSUS.txt:420]`.
- **Import-closure** reaches no rangefinder, stamps or census module from `tierc7_rules` or `tierc9`
  `[stamps/FIXTURES_STAMPS.txt:61-72]`. **Name drift:** the contract names `analytics/rangefinder.py`; the port on disk
  is `analytics/rangefinder_census.py`, covered by the "anything named rangefinder" rule.
- **Worktree attestation is an attestation, not a check.** `F-WORKTREE-ATTEST` is set true unconditionally. All 28
  registered worktrees sit at `a6da1b9` (2026-07-09) and reach none of the 28 tierc10 commits
  `[panel/FIXTURES_PANEL.txt:352-355; close/S5_FINDINGS_NOT_FIXED.json measured.v]`. Nothing on disk records the
  worktree each TC10 review ran in (§5.11).

---

## 5 · FINDINGS — REPORTED, NOT FIXED

*The full harvest is `[close/S5_FINDINGS_NOT_FIXED.md]`, sha256 `1fc8a068…`. It holds 81 findings: 44 harvested verbatim
with source path and field, 6 measured at build time, and 31 leans. Each has an owner and the status "REPORTED, NOT
FIXED". The ones that bear on reading this build:*

1. **P-TRG-2's clear is an in-sample re-score of a grid pick** (§0.3). It is framed in PROGRESS and two commit subjects
   as a "three-clause" pass. Under its text the verdict is CI-only.
2. **The equal-asset-risk transcript line mis-prints on every `SCORE_*.txt`.** "EAR x [lo, hi]" pairs the arm's EAR
   level with the CI of the Δ against the base. Example: `SCORE_P-BE-1.txt` A3 reads "EAR 0.525813 [-0.166269,
   0.079973]", while the true Δ point is `ear_ci_point` −0.026386. `rows.json` is internally correct. **Quote EAR from
   `rows.json`, never from the transcript.**
3. **A P-BRK-S1-specific `era_note` prints on other lanes' holdout rows** (P-SPR-2, P-BE-1, P-TRG-2): "the era P-BRK-S1
   is scored on, where its tuned pins and its chosen band are out of sample". It is false for those lanes. `scores/*`
   is immutable, so this document carries the qualifier (§0.2).
4. **P-BRK-S1 §7's promised 5m hold-rate print, "Tier-E, collared to the holdout era", was not made.** No hold-rate
   field is on the row or in `brk/BRK_READY.json`. `census/hold_tally.parquet` has no era column, so it is not
   collared. `LEDGER_5M.json:1703` asserts the print; no file supports it. This gates nothing.
5. **F-C10-BE's real-campaign proof is unmet by the text's own terms.** With dip-after 0 of 103, the repaired latch
   fill branch was never exercised (§1.3).
6. **P-BRK-I1 carries no toll stamp** (`toll.stamped` false). Its `toll_accounting_status` quotes P-BRK-S1's "NET OF
   MEASURED 5m TOLL". The module constant is emitted for both BRK forms at `scripts/tierc10_score.py:845`. The 1d
   flip-hold toll is at most 0.021990 ATR (`census/outcome_grid.parquet`, BTC, frozen3.0, era ALL, H20) against stops
   of 2.0326–4.6396 ATR (`brk/BRK_READY_BOOKS.json`, r_dist ÷ atr_at_entry). That is about 1.1% of 1R at most, so there
   is no verdict effect.
7. **P-BRK-I1's `n_polarity_vs_die_mismatch`** (§3, §9.5) is computed but appears in no filed output. The lane's
   n_hold and n_truncated are not published.
8. **`beside.per_asset_rows` on era arms are labelled `window 'full_corridor'`, `in_sample true`.** The labels are
   hard-coded at `scripts/tierc10_panel.py:1477-1486` and `scripts/tierc5.py:573`. The numbers are the era book's.
9. **`REGISTRATION_TEXTS.md` holds 0 of the 6 texts of record verbatim** and still reads "NOTHING IS FILED". The texts
   of record are `REGISTRATION_TEXTS.json` (§1.1).
10. **Stale records.** `PROGRESS.json` `operator_rulings.sha256` (`70188a0c…`, six rulings) against disk (`a0a08f87…`,
    ten), and `PROGRESS.json` `head` `6b15def…` against HEAD `3d55988`.
    - B-CORE's note "finish_family runs after B-5M" is stale; B-5M ran.
    - D-CORE blockers 1–4 are superseded by its own entry 8 (§R0.2).
11. **Worktree attestation is unconditional**, and no review worktree was at a TC10 HEAD (§4).
12. **`census/smoke/` and `null/smoke/` are still in place** with lookalike, pre-era contents. At CLOSE: rebuild them,
    or quarantine them under `_partial_<ts>/` per LAW 2 ("never deleted"). Which of the two is the operator's call; the
    executor removes nothing (§R0.3).
13. **LAW 6 was breached for the draft.** `BUILD_DRAFT.md` §1 stopped at `f97cded` while 25 tierc10 commits followed.
    It is repaired in this draft (§R0.5).
14. **TC9's filed `tc7g_tide_streak_bands` counts campaigns on whole-corridor (look-ahead) edges**, 23/57/62/58 against
    25/60/56/59 trailing (§2.5). This is carried to the autopsy.
15. **The CLOSE builder scripts will turn F-C10-RESUME RED until they are registered.**
    `scripts/tierc10_resume_fixtures.py:3702-3712` requires every `scripts/tierc10_*.py` to be listed in
    `TC_SUITE_FILES` and tracked. **Fourteen** `scripts/tierc10_close_*.py` are untracked (`git status`), including
    the two this repair pass added: `tierc10_close_p_trg_2_seen_share.py` (F-SS) and
    `tierc10_close_ledger_append_root.py` (F-LAR).
16. **The sub-pool nulls (CLASSIC5, UNSEEN12) were never filed by the null stage**, which commissioned POOLED:ALL only.
    §2.3's nulls were computed at CLOSE and anchored against the filed rows.
17. **The v6-twin reuse tolerance** (§3.6), and the 4-dp `control_headline.parquet`. Both are precision limits of the
    filed journal, not drift.
18. **P-SPR-2's era arms were re-ridden on truncated windows, not collared from one book.** The 4h bar opening
    2024-06-30T20:00Z falls in neither era window. No campaign is lost: 165 + 96 = 261.
19. **`LEDGER_ARGUS.md:545`** says PUMPFUN has no Binance perpetual, against the venue probe (§3.5).
20. **The manifest's "LaCie consent needed" is stale on consent.** R6 granted the push; neither file names a
    destination (§6 Q6).
21. **`FN-RUL-L1-1` · the contract's PANEL PIN gap** ("the gap is filed as a finding", contract :110): R2's "All 17"
    against the PANEL PIN's 5-asset book. Filed as `FN-RUL-L1-1` `[close/S5_FINDINGS_NOT_FIXED.md:11, :72, :483]`, owner
    the operator; R8 settles it on the operator's word (`OPERATOR_RULINGS.md` `## R8`). Both BRK forms scored on
    CLASSIC5 (§0.5).
22. *(Repair pass; not in the S5 harvest.)* **Two LEDGER_APOLLO drafts existed; one is the append.** `close/LEDGER_APOLLO_APPEND.draft.md` is F-LA's
    source-quote render. Its header now says it is NOT the append, and its P-TRG-2 line now reads "SUPPORTED (CI-only);
    LOAO and BH beside, both clear" instead of "clears clauses (a), (b) and (c)"
    (`scripts/tierc10_close_close_ledger_append.py`, re-run: 11/11, 30/30 sabotages RED). The append of record is the
    hand condensation `LEDGER_APOLLO_APPEND.md`, which had no fixture until F-LAR (§4, §8).
23. *(Repair pass; not in the S5 harvest.)* **`REGISTRATION_PLAN.md:57` cites the contract's "the ADMITTED twelve" as line 92.** It is line 90 (§0.5).
24. *(Repair pass; not in the S5 harvest.)* **The P-TRG-2 seen share first rested on a session-scratchpad re-ride.** It is now persisted and fixture-guarded
    as `close/P_TRG_2_SEEN_SHARE.{json,md}` (F-SS 9/9). The claim is narrowed to what the files can show: an
    aggregate-and-overlap match with TIER-C9's grid row, not a key-for-key match (§0.3).

---

## 6 · OPERATOR QUESTIONS STILL OPEN

1. **F-D-1 · REST or ARCHIVE?** Which of the venue's two publications is the bar of record? R5 names the pair, not the
   publication. D-CORE and D-5M stay PARTIAL on this alone. No bar is rewritten without the word.
2. **P-BRK-S1's toll · print or deduction?** The census-measured 5m toll is in ATR (median 17.76% of 1R on the scored
   book).
   - Is it converted to R and **deducted** from net_r? That would be a new registration id, per its §7.
   - Or does it stay a labelled **PRINT**?
   - The verdict does not depend on the answer: a deduction only lowers it.
3. **P-BE-1 · a new id under `set_change`?** Adding a registration is outside this contract. Do you order a new filing,
   disclosed and carrying A2–A4 beside it, or does **HALT — NO VERDICT** stand as P-BE-1's record?
4. **The 5m hold rate · collared scoring ground or uncollared print?** The collared reading was declared
   (`OPERATOR_RULINGS.md`, "Still blocked … after R7–R10": *"Executor is proceeding on the conservative reading (collar
   it)"*); the print was not made, and `census/hold_tally.parquet` has no era column to collar (§5.4).
5. **PUMPFUN → PUMPUSDT (Binance) and MNT → MNTUSDT on Bybit v5 linear · ratify, or name an exclusion?** MNT is charged
   the flat Binance-era taker fee, which is an **assumption**. Both scored on P-GEN-1: PUMP 8 campaigns, MNT 18.
6. **The LaCie destination, and the push.** R6 granted permission to push ("Permission to push granted"); the
   destination is unnamed in the operator's words. **[executor lean]** The vault is `/Volumes/LaCie/Repo
   Clone/naiad-backups`, and the default destination would create an empty one (`OPERATOR_RULINGS.md` "Operationalisation
   (EXECUTOR LEANS — not the operator's words)", R6 bullet). Name the destination, and consent to push and publish at
   CLOSE.
   - **0 of 28 tierc10 commits are on any remote.**
   - The 856,462,999-byte snapshot is **NOT PROTECTED** (§8).
7. **Named for the autopsy, not asked here: the slippage twin.**
   - Does the charter tier model replace the TC-series flat toll for SAIL?
   - Must the twin carry funding? It does not today.
   - Q6 holds the SAIL spec until TC10 is autopsied.
8. **Three executor readings: ratify or overrule each.**
   - **The R1 era cut.** R1 says "Feel free to search data from past runs to tune the defaults". The executor read that
     as permission to fit the hold pins on an era cut at `1719791999000` ms = 2024-06-30T23:59:59Z, and scored
     P-BRK-S1 on the holdout after it (`OPERATOR_RULINGS.md` "Operationalisation", R1 bullet). Ratify the cut, or
     overrule it.
   - **The F-C10-RESUME law.** `PROGRESS.json` `f_c10_resume_law`: F-C10-RESUME hashes artifacts, not transcripts. It is
     tagged "[EXECUTOR READING — put to the operator]". Ratify, or overrule.
   - **P-GEN-1's panel.** UNSEEN12 = the contract's twelve among the seventeen admitted (`panels.UNSEEN_admitted_stems`),
     the reading under which "the ADMITTED twelve" (contract :90) and "the ADMITTED LIST … IS P-GEN-1's panel" (:50)
     agree (§0.5). The admitted list on disk holds all seventeen. Ratify, or overrule.

---

## 7 · WHAT THIS BUILD IS NOT

- **Not out of sample for P-TRG-2.** 196 of its 198 campaigns entered at or before TIER-C9's as-of; their count and
  net equal the grid row that chose it `[close/P_TRG_2_SEEN_SHARE.json]`. **Not a SAIL act:** the Q6 hold stands
  (contract :2-3, :143).
- **Not a generalisation result, and the out-of-asset evidence points down.** P-GEN-1's "unseen twelve" holds 3
  never-touched assets and 9 display-only. It did not clear, and its positive point is one asset, BNB. The three
  never-touched assets are each negative, and their CI [−0.351183, −0.160879] lies wholly below zero. On N = 3 it
  decides nothing.
- **Not a pin refit, not a re-worded or added registration, not a promoted census cell.** [Q-R4] names defaults and
  moves nothing. The census is a SELECTION over 7,920 outcome cells.
- **Not a licence for a range-trading contract.** [Q-R3] fails at 5m everywhere, and at 4h on every pool but one era.
  At 1d it fails on the holdout.
- **Not a verdict on P-BE-1's floor.** The floor was never measured on the scored book.
- **Not clean data.** F-D-1 is RED. Two venue mappings are leans. The panel is publication-heterogeneous.
- **Not trusting anything the interrupted session left.** Every stage re-passed NOW, and the partials are quarantined.

---

## 8 · DISPOSITION · BOX-COST

*A PRE-CLOSE SNAPSHOT: regenerate after the CLOSE commit and push. The seven-column table (PATH · EXISTS · TRACKED ·
COMMITTED · PUSHED · PROTECTED BY · BOX COST) for all 161 rows is `[close/S8_DISPOSITION_BOX_COST.md]` (sha in PROGRESS.json, stage CLOSE —
it measures the live tree), 5/5 GREEN. The constants are read by `ast.literal_eval` and never imported: `BOX_BYTES` 16,000,000
(`scripts/publish_exchange.py:95`) and `FLAG_BYTES` 64,000 (`:160`).*

**Git** (`git log --since=2026-09-21`, read-only):
- **28 tierc10 commits**, from `c7b157d` (2026-09-22T09:21:55-03:00) to `2416a15` (21:57:30-03:00).
- One other commit in the window, `3d55988`, is the parallel OR-1 lane's (step D), not TC10.
- HEAD `3d55988` is 29 commits ahead of `origin/v12-v1-census` at `088d475`.
- **0 of the 28 tierc10 commits are contained in any remote-tracking ref.** Nothing of TC10 is on GitHub.

**Workflows and agents on disk** (`~/.claude/projects/-Users-luis-Naiad/<session>/workflows/wf_*.json`, workflows
named `tc10-*`):

| session | role | workflows | agents (`agentCount`) | wall hours (`durationMs`) |
|---|---|---:|---:|---:|
| `730798c3` | the 2026-09-21 build (killed by the 529) | 5 | 47 | 7.05 |
| `a5a776be` | R0 census, repairs, registration texts | 13 | 79 | 8.32 |
| `8f5aa9c8` | unblock BE/HOLD; repair + scorer | 2 | 14 | 2.47 |
| **total, journaled** | | **20** | **140** | **17.85** |

This CLOSE workflow is not yet journaled. Its subagent directory
(`8f5aa9c8-…/subagents/workflows/wf_313565ab-6cb/`) holds 20 agent `.meta.json` files at draft time. The parallel OR-1
lane's workflows are excluded.

**Rows that matter** `[close/S8_DISPOSITION_BOX_COST.md §8.0–8.7]`:

| path | state | protected by | box cost |
|---|---|---|---|
| 53 paths in tierc10 commits | tracked, committed, **not pushed** | NOT PROTECTED | only the contract is box-bound: 9,441 B |
| `research_outputs/tierc10/**` evidence: 102 files + 983 cell files (census/cells 96,700,245 B; null cells 371,194,083 + 373,767,503 B) | **git-ignored** (`.gitignore:263`) | NOT PROTECTED: local disk only, outside `--workflow` | n/a, unsynced |
| `research_outputs/tierc10/close/*` and `scripts/tierc10_close_*.py` | ignored / **untracked** | NOT PROTECTED | n/a |
| `exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md` (PLANNED: this document) | not yet on disk | `publish()` at CLOSE | **FLAGGED**: over 64,000 B (the estimate of 241,562 B assumed every fragment spliced whole; this draft condenses them, and the flag stands) |
| `exchange/status/LEDGER_APOLLO.md` (receives the append) | tracked | — | already 174,090 B, over the wire; append-only, advisory |
| `/Users/luis/.cache/naiad/snapshots/tc10_20260921` | outside the repo, 176 files, 856,462,999 B | **NOT PROTECTED until the LaCie mirror** | n/a |

**Named cost findings:**
- **BC-3.** The contract file `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` was committed by hand in `c7b157d`, not
  by `publish()`. CONVENTIONS asks that exchange files ride only the guard. It will ride the next branch push.
- **At CLOSE** (contract :129-140; every act after the operator's word):
  1. Register the close scripts in `TC_SUITE_FILES` (§5.15), force-add the `close/` fragments past `.gitignore:263`,
     and make the CLOSE commit.
  2. Push the branch, and mirror to the operator's named destination. **State the push result.**
  3. **Fill the append's one pending stamp** with the tierc10 commit count and how many of those commits are on a
     remote, both read now, after step 2. Re-run F-LAR (`scripts/tierc10_close_ledger_append_root.py`); it must read
     9/9 with 0 pending stamps.
  4. Move this draft to `exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md`, and append **exactly the bytes of
     `research_outputs/tierc10/LEDGER_APOLLO_APPEND.md`** that F-LAR certified in step 3 to
     `exchange/status/LEDGER_APOLLO.md`. Before the stamp is filled, that file is sha256 `d6a58f5c2901f177…`, 14,925 B,
     certified 9/9 in `close/FIXTURES_CLOSE_ledger_append_root.txt` (§4). **Do not append**
     `close/LEDGER_APOLLO_APPEND.draft.md`: that is F-LA's source-quote render (§5.22).
  5. `publish_exchange`: it commits and pushes `exchange/**` only. **State its push result.**
  6. List the bright paths: the build document, the LEDGER_APOLLO append, the contract of record, and the `close/`
     fragments the build cites.
  7. End the session message (not the appended bytes) with the contract's final line: "Operator: click Sync now."
  8. Regenerate this table.
