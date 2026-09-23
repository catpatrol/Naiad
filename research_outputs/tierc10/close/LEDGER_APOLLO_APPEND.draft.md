TIER-C10 · CLOSE · LEDGER_APOLLO APPEND — DRAFT, NOT APPENDED
drafted by scripts/tierc10_close_close_ledger_append.py · REPORT-ONLY: it reads filed
records, scores nothing, re-words nothing, and writes nothing under exchange/.
The text between the two ~~~~ marker lines is a SOURCE-QUOTE DRAFT of the
append, re-verified by the F-LA legs. It is NOT the append of record: the
CLOSE appends research_outputs/tierc10/LEDGER_APOLLO_APPEND.md, certified by
F-LAR (scripts/tierc10_close_ledger_append_root.py). Appending is the CLOSE
step's act (contract :137-139, quoted in full below), after the
operator's word — not this script's. The commission, verbatim:
  «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:137-139»
    | LEDGER_APOLLO append: Q6 hold verbatim ("spec held until TC10 autopsied"); m=6;
    |   the 07-29 RS rulings cited; the slippage-twin question named for the autopsy;
    |   CENSUS-3 next.

SOURCES READ THIS RUN (sha256 · bytes · path)
  4d58d591668badffc34624e81feddf106ac94a92ca64aceafd4f871e84d31c76 · 259298 · LEDGER.md
  8a0bf279bcab0f27161a7d965535445807f4e713e77d045b0ba124bc7f803c7a · 9441 · exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md
  cd6ad43a0fe4890635e6d7098d29ae52d4af1268be4466740823701014222d2c · 174090 · exchange/status/LEDGER_APOLLO.md
  0d66f2d7fe6c338339880368ff854e58bbb2533be54cf2f7448f71d129752afc · 267607 · research_outputs/tierc10/PROGRESS.json
  3afce077146807127072ae68f9c816e0263505aa625cf1610763ea37eb91ca94 · 178729 · research_outputs/tierc10/REGISTRATION_TEXTS.json
  469a08756913c2855a5d80419842b34e50a04b0efb0d4e2f8d579d0c4cfbcf92 · 81277 · research_outputs/tierc10/close/S0_VERDICTS.json
  499f3843de176fbe6ec175d0fdae788bb3bc182ee2a1deaff762a19f7098ba8e · 19355 · research_outputs/tierc10/close/V6_CONTROL_HAIRCUT_TWIN.parquet
  3a18b84e0211110b69eb09661b7e9a39db08f41c69ebdc4cc8ca8eb54a07e5cc · 23925 · research_outputs/tierc10/data/fee_schedule.json
  aa0e8c496fd6b883a3c01947047c4845eb72935ca17368cffee9c8593a7bc4a2 · 113715 · research_outputs/tierc10/scores/FAMILY.json
  b40af065177695e36e755d183ef74e7328d77eb799ed3abbb668ff7d69b6b678 · 84044 · research_outputs/tierc10/scores/P-BE-1.rows.json
  f3ae88d0be366f127bacfe0f8092cdef07d17559ea3b3db6d6c1edd6c306111a · 111150 · research_outputs/tierc10/scores/P-BRK-I1.rows.json
  994bcaa69906aae8a1659d953c0984da636cb496808dd17ab91ddf3ea3c33ff0 · 118556 · research_outputs/tierc10/scores/P-BRK-S1.rows.json
  047097ec5aeefbe8aa63cf2b1a677015540497a41e43b0152e609426a2baf87d · 123091 · research_outputs/tierc10/scores/P-GEN-1.rows.json
  febff33a1ad91e3663cb75fc7db54fe7901d7a8493503e3e6e6aa065da6bc23e · 111310 · research_outputs/tierc10/scores/P-SPR-2.rows.json
  9fa07a0fa1b832ef7a1012a796cfd7fdd73ab2e1275d4faa4340666493c340c8 · 102709 · research_outputs/tierc10/scores/P-TRG-2.rows.json

~~~~~~~~ BEGIN APPEND — the bytes from the next line up to END APPEND ~~~~~~~~

---

=== STATUS_APOLLO — 2026-09-22 — TIER-C10 · UNSEEN RANGES · RESUME-AND-FINISH ===
LANE      APOLLO (drafted) · HEPHAESTUS (executor) · branch v12-v1-census · seed 20260921
CLASS     6 REGISTRATIONS, TEXT FROZEN · FDR m = 6 DECLARED, 5 SCORED,
          1 SLOT HALTED AS ITS FILED TEXT PRESCRIBES. As-of 2026-09-21T16:00:00Z.
          Contract of record exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md
          (sha 8a0bf279bcab0f27…, = PROGRESS.json contract_of_record: True).
          Every quote below is verbatim and cited «path:line» or «path#field»;
          every number is read from the file named beside it.

  Q6 · THE SAIL SPEC HOLD, VERBATIM — BOTH PLACES THE CONTRACT STATES IT,
  AND THE LIMIT IT SETS ON THIS TIER:
    «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:2-3»
      | Q6 SAIL spec HELD
      | until TC10 autopsied
    «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:137»
      | Q6 hold verbatim ("spec held until TC10 autopsied")
    «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:143»
      | no SAIL act (spec held by operator word)
    The hold is quoted, not lifted. Nothing in this tier acts on SAIL;
    a registration clearing its bar below is a verdict, not a SAIL act.

  §0 · THE 6 — READ, NOT RE-SCORED: the scored row of record per
  registration, from research_outputs/tierc10/close/S0_VERDICTS.json
  (built first by scripts/tierc10_close_close_s0_verdicts.py), every cell held
  against an independent read of scores/FAMILY.json + scores/<REG>.rows.json:
    P-GEN-1   [45%]  NOT SUPPORTED
        'unseen12-card-v6' · UNSEEN12 · era full · n 286
        VS ZERO (one-sample asset-cluster)
        point +0.099777 R · CI [-0.154991, +0.315921] · p 0.271682
        clears_bh_bar false · LOAO 0/12 above (above of record 0 vs bar 7)
    P-SPR-2   [45%]  NOT SUPPORTED
        'standalone vs zero · full corridor' · CLASSIC5 · era full · n 261
        VS ZERO (one-sample asset-cluster)
        point -0.005930 R · CI [-0.174617, +0.165338] · p 0.560360
        clears_bh_bar false · LOAO 0/5 above (above of record 0 vs bar 3)
    P-BE-1    [40%]  HALT — NO VERDICT
        'be-floor-1R vs card-v6 (CLASSIC5, full)' · halted at TP.score;
        the slot finishes WITHOUT a row:
        «research_outputs/tierc10/scores/FAMILY.json#scored_slots_halted.P-BE-1»
          | HALT: P-BE-1 — the arm shares the WHOLE campaign set with its
          + base; the commissioned two-sample ruler's premise failed. File a
          + NEW id under ruler='set_change' and disclose.
        and what the filed text prescribes for this HALT:
        «research_outputs/tierc10/scores/P-BE-1.rows.json#rows[0].text_prescribes[0]»
          | If it does not move, this registration does NOT quietly become the
          + narrower paired row — it HALTs. That HALT is part of the claim,
          + and it is why the ruler is registered rather than left to the
          + scorer.
        «research_outputs/tierc10/scores/P-BE-1.rows.json#rows[0].text_prescribes[1]»
          | If A1's two-sample premise fails and A1 HALTs, there is no
          + report-only row on the same population to read instead; a new id
          + must be filed under `set_change` and the reason disclosed.
    P-TRG-2   [40%]  SUPPORTED
        'trg-9/12 vs card v6 · CLASSIC5 · full' · CLASSIC5 · era full · n 198
        TWO-SAMPLE (the arm CHANGES the campaign set)
        point +0.257697 R · CI [+0.108587, +0.383892] · p 0.005249
        clears_bh_bar true · LOAO 5/5 above (above of record 5 vs bar 3)
    P-BRK-I1  [35%]  NOT SUPPORTED
        'CLASSIC5-memory-line' · CLASSIC5 · era full · n 7
        VS ZERO (one-sample asset-cluster)
        point +0.718270 R · CI [-0.602912, +1.452261] · p 0.269683
        clears_bh_bar false · LOAO 1/5 above (above of record 1 vs bar 3)
    P-BRK-S1  [30%]  NOT SUPPORTED · CI ENTIRELY BELOW ZERO
        'P-BRK-S1 vs zero' · CLASSIC5 · era holdout · n 1836
        VS ZERO (one-sample asset-cluster)
        point -0.211069 R · CI [-0.298366, -0.144105] · p 1.000000
        clears_bh_bar false · LOAO 0/5 above, 5/5 BELOW (above of record 0 vs bar 3)

  FAMILY · m = 6 DECLARED (scores/FAMILY.json family_m_declared) ·
    bar q/m = 0.016666666666666666 (fdr_bar_q_over_m) ·
    5 scored rows of 20 family rows (scored_in_family) · halted slots 1: P-BE-1.
    The contract's m, and the record's reason it does not shrink:
    «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:89»
      | FDR m=6, independently failable
    «research_outputs/tierc10/PROGRESS.json#stages[stage=B-5M].notes[0]»
      | m stays 6 DECLARED (5 run): fewer tests never loosen the bar.

  THE 07-29 RS RULINGS, CITED — LEDGER.md, located by pattern search at
  draft time (grep -n equivalent): the heading, the Q-R3 / Q-R4 / Q-R5
  bullets, the ratification:
    «LEDGER.md:829»
      | ## 2026-07-29 — Range-and-Structure layer: interview rulings + session ratifications
    «LEDGER.md:834»
      | Q-R3 PLAYBOOK-R TIMING: (a) — detection and gating first; a
      + range-trading contract is drafted ONLY IF the height-vs-toll
      + feasibility gate AND the edge-fade outcome leg both pass.
    «LEDGER.md:835»
      | Q-R4 ACCEPTANCE DEFINITION: (a) — the census measures four candidate
      + operationalisations head-to-head (2-close / 3-close / 6-outside-close
      + stale-run / time-beyond); the engine default is chosen FROM DATA.
    «LEDGER.md:836»
      | Q-R5 SCANNER DISPOSITION: operator ruling supersedes both drafted
      + options. The new range-detection logic inherits NO starting values
      + from the SS Breakout Scanner.
    «LEDGER.md:846»
      | - Reviewer: Claude (Fable-mode), 2026-07-29. Operator: ratified.
    Where TIER-C10 carried them — the contract's anchor, then the record:
    [Q-R5]
      «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:38-39»
        | [Q-R5] grep-attest: the RangeFinder inherits NO values from the
        |   SS Breakout Scanner (2026-07-29 ruling).
      «research_outputs/tierc10/PROGRESS.json#stages[stage=STEP 0].one_line»
        | Q-R5 attestation HOLDS (no RangeFinder constant inherited from the
        + SS Breakout Scanner, whose source is not in this repo at all)
    [Q-R4]
      «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:75-77»
        | [Q-R4] the four acceptance operationalisations head-to-head {2-close · 3-close
        |     · 6-outside-close stale-run · time-beyond} beside the RangeFinder DIE rule
        |     (8-close OR 1.5 ATR); the data's default named, nothing promoted
      «research_outputs/tierc10/PROGRESS.json#stages[stage=CENSUS-R{4h,1d}].one_line»
        | [Q-R3] height-vs-toll and [Q-R4] the acceptance head-to-head are BUILT
    [Q-R3]
      «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:78-79»
        | [Q-R3] HEIGHT-vs-TOLL feasibility per lens (confirmed-range height ÷ round-trip
        |     toll, distribution) + the EDGE-FADE outcome leg; boundary-fade stays Tier-E
      «research_outputs/tierc10/PROGRESS.json#stages[stage=CENSUS-R{4h,1d}].one_line»
        | [Q-R3] is a GATE per LEDGER.md:834, not a table: PASS per era ALL 9 / tuning 13 / holdout 7 of 120.
      «research_outputs/tierc10/PROGRESS.json#stages[stage=CENSUS-R{5m}].one_line»
        | The 5m height-vs-toll gate FAILS 0/17 (carried on P-BRK-S1's row).
      on each BRK form's row (REPORT-ONLY — the gate as carried, read):
      P-BRK-I1 · lens 1d · era ALL · verdict_pass True
        «research_outputs/tierc10/scores/P-BRK-I1.rows.json#beside_registration.brk_sealed_row.height_vs_toll.reason»
          | era ALL: height gate PASS + edge-fade leg PASS
      P-BRK-S1 · lens 5m · era holdout · verdict_pass False
        «research_outputs/tierc10/scores/P-BRK-S1.rows.json#beside_registration.brk_sealed_row.height_vs_toll.reason»
          | era holdout: height gate PASS + edge-fade leg FAIL

  THE SLIPPAGE-TWIN QUESTION — NAMED FOR THE AUTOPSY, NOT ANSWERED HERE:
    QUESTION: "does the charter tier model replace the TC-series flat toll for SAIL, and must the twin carry funding?"
    The clause that put a twin on every row:
    «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:51-55»
      | COSTS: every row gets the charter model as a HAIRCUT TWIN beside the TC-series
      |   toll — slippage/side tier A {BTC ETH} 2 bps · tier B {SOL NEAR ZEC LTC BNB DOGE
      |   UNI SUI XMR} 5 · tier C {ENA PUMPFUN HYPE MNT PEPE BONK} 10 [VETO "tiers"]. The
      |   5-asset control's TC-series accounting stays untouched; its twin is an ADDED
      |   column.
    EVIDENCE — TIER-E · REPORT-ONLY · the twin gates nothing:
    «research_outputs/tierc10/scores/P-GEN-1.rows.json#rows[0].beside.haircut_twin.law»
      | HAIRCUT TWIN — an ADDED column beside the TC-series toll, never a
      + replacement; the verdict, CI, p and LOAO are the TC-series row's [VETO
      + 'tiers']
    «research_outputs/tierc10/data/fee_schedule.json#haircut_twin_law»
      | ADDED, never a replacement: haircut_twin_* keys carry the charter
      + model (per-side taker fee + the charter's per-side slippage tier)
      + beside round_trip_bps_used, which stays the TC-series accounting
      + figure on every row [VETO 'tiers'].
    «research_outputs/tierc10/data/fee_schedule.json#haircut_twin_law»
      | net_r_twin = gross_r - cost_px / risk_px
    the tiers (research_outputs/tierc10/data/fee_schedule.json haircut_twin_tiers):
      tier A {BTC ETH} 2.0 bps/side
      tier B {SOL NEAR ZEC LTC BNB DOGE UNI SUI XMR} 5.0 bps/side
      tier C {ENA PUMPFUN HYPE MNT PEPE BONK} 10.0 bps/side
    per asset (fee_schedule.json assets[]):
      TC-series toll · round_trip_bps_used · 10.0 x17 · of 17 assets
      charter twin · haircut_twin_round_trip_bps · A 14.0 x2 · B 20.0 x9 · C 30.0 x6
      twin round trip > TC toll on 17/17 assets
    every arm row that carries a twin — expectancy R per campaign, as filed.
    IN = the registration's scored arm, -- = a Tier-E arm; twin+fund = the
    with-funding companion, which is NOT the filed twin; flags =
    sign_disagrees_with_tc / companion_sign_disagrees_with_tc:
      P-GEN-1  #0 IN  n 286   TC +0.099777  twin +0.084601  twin+fund +0.067733  twin<=TC flags False/False  'unseen12-card-v6'
      P-GEN-1  #1 --  n 486   TC +0.144608  twin +0.139148  twin+fund +0.117290  twin<=TC flags False/False  'panel17-card-v6'
      P-GEN-1  #2 --  n 47    TC -0.232839  twin -0.265944  twin+fund -0.269944  twin<=TC flags False/False  'never-touched-card-v6'
      P-SPR-2  #0 IN  n 261   TC -0.005930  twin -0.024325  twin+fund -0.021998  twin<=TC flags False/False  'standalone vs zero · full corridor'
      P-SPR-2  #1 --  n 165   TC -0.149015  twin -0.168970  twin+fund -0.163773  twin<=TC flags False/False  'standalone vs zero · tuning era'
      P-SPR-2  #2 --  n 96    TC +0.239998  twin +0.224284  twin+fund +0.221679  twin<=TC flags False/False  'standalone vs zero · holdout era'
      P-SPR-2  #3 --  n 425   TC +0.097555  twin +0.090697  twin+fund +0.079597  twin<=TC flags False/False  'union with card v6 vs card v6'
      P-BE-1   #1 --  n 123   TC -0.025042  twin -0.000239  twin+fund -0.044853  twin>TC  flags False/False  'be-floor-1R vs card-v6 (CLASSIC5, tuning) [Tier-E]'
      P-BE-1   #2 --  n 77    TC +0.511080  twin +0.493717  twin+fund +0.489217  twin<=TC flags False/False  'be-floor-1R vs card-v6 (CLASSIC5, holdout) [Tier-E]'
      P-BE-1   #3 --  n 200   TC +0.188937  twin +0.197940  twin+fund +0.168363  twin>TC  flags False/False  'be-floor-2R sensitivity vs card-v6 (CLASSIC5, full) [Tier-E]'
      P-TRG-2  #0 IN  n 198   TC +0.466414  twin +0.475588  twin+fund +0.446496  twin>TC  flags False/False  'trg-9/12 vs card v6 · CLASSIC5 · full'
      P-TRG-2  #1 --  n 198   TC +0.466414  twin +0.475588  twin+fund +0.446496  twin>TC  flags False/False  'trg-9/12 vs zero · CLASSIC5 · full'
      P-TRG-2  #2 --  n 132   TC +0.177656  twin +0.198949  twin+fund +0.158114  twin>TC  flags False/False  'trg-9/12 vs card v6 · CLASSIC5 · tuning era'
      P-TRG-2  #3 --  n 66    TC +1.043928  twin +1.028866  twin+fund +1.023261  twin<=TC flags False/False  'trg-9/12 vs card v6 · CLASSIC5 · holdout era'
      P-BRK-I1 #0 IN  n 7     TC +0.718270  twin +0.894601  twin+fund +0.715223  twin>TC  flags False/False  'CLASSIC5-memory-line'
      P-BRK-I1 #1 --  n 3     TC +0.351769  twin +0.510048  twin+fund +0.348581  twin>TC  flags False/False  'CLASSIC5-tierE-band'
      P-BRK-I1 #2 --  n 17    TC +0.421903  twin +0.517225  twin+fund +0.415994  twin>TC  flags False/False  'PANEL17-tierE-memory-line'
      P-BRK-S1 #0 IN  n 1836  TC -0.211069  twin -0.372757  twin+fund -0.373465  twin<=TC flags False/False  'P-BRK-S1 vs zero'
      P-BRK-S1 #1 --  n 6016  TC -0.170156  twin -0.427683  twin+fund -0.428533  twin<=TC flags False/False  'P-BRK-S1 17-asset view'
      P-BRK-S1 #2 --  n 1300  TC -0.198889  twin -0.325258  twin+fund -0.326226  twin<=TC flags False/False  'P-BRK-S1 memory-line anchor'
    COUNTS: 20 of 21 arm rows carry a twin (without: P-BE-1#0 (HALTed)) ·
      flags: sign_disagrees_with_tc 0/20 · companion_sign_disagrees_with_tc 0/20 ·
      twin > TC on 8/20 · of those 8, twin+fund <= TC on 8/8
    the twin's funding, in the rows' own words (the same note on 20/20 twin rows):
    «research_outputs/tierc10/scores/P-GEN-1.rows.json#rows[0].beside.haircut_twin.funding_note»
      | the filed twin charges fee + charter slippage and NO funding; the
      + companion column subtracts the campaign's funding_r and is NOT the
      + filed twin
    the arms ridden against card-v6 — the Δ as filed, TC / twin / twin+fund:
      P-SPR-2  #3 --  base_n 200  TC Δ -0.111162  twin Δ -0.126453  twin+fund Δ -0.108559  'union with card v6 vs card v6'
      P-BE-1   #1 --  base_n 123  TC Δ -0.014280  twin Δ -0.014733  twin+fund Δ -0.014336  'be-floor-1R vs card-v6 (CLASSIC5, tuning) [Tier-E]'
      P-BE-1   #2 --  base_n 77   TC Δ -0.048234  twin Δ -0.047157  twin+fund Δ -0.048249  'be-floor-1R vs card-v6 (CLASSIC5, holdout) [Tier-E]'
      P-BE-1   #3 --  base_n 200  TC Δ -0.019780  twin Δ -0.019211  twin+fund Δ -0.019793  'be-floor-2R sensitivity vs card-v6 (CLASSIC5, full) [Tier-E]'
      P-TRG-2  #0 IN  base_n 200  TC Δ +0.257697  twin Δ +0.258438  twin+fund Δ +0.258340  'trg-9/12 vs card v6 · CLASSIC5 · full'
      P-TRG-2  #2 --  base_n 123  TC Δ +0.188419  twin Δ +0.184455  twin+fund Δ +0.188631  'trg-9/12 vs card v6 · CLASSIC5 · tuning era'
      P-TRG-2  #3 --  base_n 77   TC Δ +0.484614  twin Δ +0.487992  twin+fund Δ +0.485795  'trg-9/12 vs card v6 · CLASSIC5 · holdout era'
    the 5-asset v6 control's own twin — research_outputs/tierc10/close/V6_CONTROL_HAIRCUT_TWIN.parquet
      (sha 499f3843de176fbe…, 18 rows; TIER-E · REPORT-ONLY; key ALL per era):
      v6 ALL · era full    · n 200   TC +0.208717  twin +0.217150  twin+fund +0.188157  twin>TC  flags False/False
      v6 ALL · era tuning  · n 123   TC -0.010763  twin +0.014494  twin+fund -0.030517  twin>TC  flags True/False
      v6 ALL · era holdout · n 77    TC +0.559314  twin +0.540874  twin+fund +0.537466  twin<=TC flags False/False
      V6 COUNTS over all 18 rows: sign_disagrees 2/18 · companion_sign_disagrees 0/18 ·
      twin > TC on 10/18 · of those 10, twin+fund <= TC on 10/10
    beside it, the 5m toll on P-BRK-S1's row is a PRINT:
    «research_outputs/tierc10/scores/P-BRK-S1.rows.json#beside_registration.brk_sealed_row.toll_accounting_status»
      | PRINT, NOT A DEDUCTION — reported, not changed. The contract reads
      + 'NET OF MEASURED 5m TOLL'; today's net_r is net of FEE and FUNDING
      + only.
    The autopsy owns the answer. Nothing here replaces the TC-series toll;
    every verdict above is the TC-series row's.

  THE TIER LINE — read from scores/FAMILY.json and scores/<REG>.rows.json,
  nothing typed. TC9 closed on:
    «exchange/status/LEDGER_APOLLO.md:2422»
      | NINE TIERS IN-SAMPLE; NOTHING HAS CLEARED ITS OWN BAR.
    TIER-C10: 1 OF THE m = 6 DECLARED CLEARS ITS OWN BAR — P-TRG-2,
    THE ONE CELL THE CONTRACT PRE-NAMED; ITS TUNING ERA ALONE DOES NOT.
    AND ITS OWN FILED TEXT CALLS IT, IN LARGE PART, AN IN-SAMPLE RE-SCORE:
    «research_outputs/tierc10/REGISTRATION_TEXTS.json#P-TRG-2.text»
      | (b) THE SAMPLE IS ALMOST ENTIRELY THE SAME SAMPLE. TIER-C9's corridor ran 2019-09-08T16:00:00Z to
      | as-of 2026-08-22T00:00:00Z, span 2539.3 days (`as_of_span_days` on every row of that grid).
      | TIER-C10's CLASSIC5 corridor has the identical start and a span of 2570.0 days. The genuinely new
      | tape is 30.7 days — about 1.2% of the corridor, roughly 184 4h bars per asset. So P-TRG-2 is in
      | large part an IN-SAMPLE RE-SCORE of a cell selected off that grid.
    P-TRG-2's SCORED arm 'trg-9/12 vs card v6 · CLASSIC5 · full' is SUPPORTED (CI-only); LOAO and BH beside, both clear:
      CI (the deciding clause) verdict SUPPORTED — CI [+0.108587, +0.383892], lo > 0 true
      LOAO (beside, deciding nothing) 5/5 above — line of record clears true
      BH (beside, deciding nothing) p 0.005249 <= bar 0.016667 — clears_bh_bar true
    Its TUNING-ERA arm 'trg-9/12 vs card v6 · CLASSIC5 · tuning era' reads NOT SUPPORTED
      (Δ +0.188419, CI [-0.014369, +0.384652], p 0.064484, LOAO 1/5 above) · P-TRG-2.rows.json rows[2]
    Its HOLDOUT-ERA arm 'trg-9/12 vs card v6 · CLASSIC5 · holdout era' reads SUPPORTED
      (Δ +0.484614, CI [+0.272576, +0.639944], p 0.000250, LOAO 5/5 above) · P-TRG-2.rows.json rows[3]
    It is the cell TC9's grid lit, and the contract's one pre-naming:
    «exchange/status/LEDGER_APOLLO.md:2371-2374»
      | trigger-9/12 +94.40 R
      |     (CI [+0.121,+0.436], p=0.003, LOAO 5/5, sharing only 19 of 196
      |     campaigns with v6). A SELECTION, not a result. The next tier may
      |     pre-name ONE cell before the look; this one did not.
    «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:98»
      | P-TRG-2 [40%] trigger 9/12 replacing 12/26, vs v6 — the one grid pre-naming.
    TIER-C10 scored it on panel CLASSIC5 (5 assets), as-of 2026-09-21T16:00:00Z.

  NEXT · CENSUS-3.
    «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:139»
      | CENSUS-3 next.
    Carried to it, not ruled here:
    · the new id the HALTed slot's own words ask for is the operator's to order:
      «research_outputs/tierc10/PROGRESS.json#stages[stage=B-CORE].notes[0]»
        | adding a registration is outside the contract ('no registration
        + re-worded or added'), so that filing is the OPERATOR's to order.
    · the slippage-twin question above, and the 5m toll print-vs-deduction;
    · D-CORE PARTIAL and D-5M PARTIAL (PROGRESS.json):
      «research_outputs/tierc10/PROGRESS.json#stages[stage=D-CORE].one_line»
        | PARTIAL because F-D-1 stays RED pending an operator ruling.
      «research_outputs/tierc10/PROGRESS.json#stages[stage=D-5M].one_line»
        | PARTIAL only on F-D-1's operator question, same as D-CORE.

  INTEGRITY  drafted by scripts/tierc10_close_close_ledger_append.py — REPORT-ONLY:
    FAMILY.json rows_files_sha256 re-hash 6/6 on disk before a field was read;
    §0 (research_outputs/tierc10/close/S0_VERDICTS.json) agrees cell-for-cell with that read;
    every «cite» above is re-verified against its source by the F-LA legs
    (research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append.txt);
    this block was DRAFTED, not appended — F-LA-NOWRITE holds LEDGER_APOLLO.md's
    bytes across the run. SAIL stays HELD (Q6).
=== END ===
~~~~~~~~ END APPEND ~~~~~~~~
