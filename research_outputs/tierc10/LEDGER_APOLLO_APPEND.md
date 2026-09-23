
---

=== STATUS_APOLLO — 2026-09-22 — TIER-C10 · "UNSEEN RANGES": TWELVE NEW ASSETS (3 NEVER-TOUCHED, 9 DISPLAY-ONLY), THE RANGE CENSUS, SIX REGISTRATIONS ===
LANE      APOLLO (drafted) · HEPHAESTUS (executor) · branch v12-v1-census · seed 20260921
CLASS     SIX REGISTRATIONS, TEXT FROZEN, FILED BEFORE THE LOOK (371123f;
          registry len 6, head 7621a857…, REGISTRY_PIN.json). FDR m = 6
          DECLARED: 5 scored, 1 slot HALTed as its own text prescribes;
          one fixed bar q/m = 0.016667, and fewer tests never loosen it
          (scores/FAMILY.json family_m_declared, fdr_bar_q_over_m).
          As-of 2026-09-21T16:00:00Z, one corridor. Resumed after the
          building session was killed mid-run; nothing it left was
          trusted. Every «cite» below is re-verified against its source
          and every number is traced to its file and field by F-LAR
          (scripts/tierc10_close_ledger_append_root.py).

  Q6 · THE SAIL SPEC HOLD, VERBATIM.
    «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:2-3»
      | Q6 SAIL spec HELD
      | until TC10 autopsied
    «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:137»
      | Q6 hold verbatim ("spec held until TC10 autopsied")
    «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:143»
      | no SAIL act (spec held by operator word)
    Held. Nothing in this tier is a SAIL act; a registration clearing
    its bar is a verdict, not a SAIL act.

  VERDICTS, each under its own text (scores/<REG>.rows.json scored
  arm; scores/FAMILY.json clears_bh_bar):
    P-GEN-1  [45%] NOT SUPPORTED. Card v6 on the admitted twelve:
      n 286, +0.099777 R/campaign, CI [-0.154991, +0.315921],
      p 0.271682, LOAO 0/12 above (bar 7).
      The positive point is ONE ASSET: BNB nets +33.4686 R of the
      arm's +28.5362 R (per_asset_rows; score_row.net_r).
      NEVER-TOUCHED VIEW (Tier-E; the contract's second LOAO line):
      n 47, -0.232839, CI [-0.351183, -0.160879], LOAO 0/3 above, 3/3 BELOW.
      Each of the three is negative on its own: PUMP -0.4182,
      MNT -0.2916, SUI -0.1119 R/campaign (rows[2] per_asset_rows).
      The text caps what three assets can carry:
      «research_outputs/tierc10/REGISTRATION_TEXTS.json#P-GEN-1.text»
        | its N is three: it can
        | support nothing on its own
      and it calls the panel's nickname wrong:
      «research_outputs/tierc10/REGISTRATION_TEXTS.json#P-GEN-1.text»
        | THE PANEL'S NICKNAME IS "THE UNSEEN TWELVE" AND THE NICKNAME IS WRONG. Only THREE of the twelve
        | are never-touched.
      F-D-5: 3 never-touched (PUMPFUN MNT SUI), 9 display-only.
    P-SPR-2  [45%] NOT SUPPORTED. Standalone spring vs zero, full
      corridor, both ways (R3/R9): n 261, -0.005930 R,
      CI [-0.174617, +0.165338], LOAO 0/5 above. It fails its ONE
      clause (CI lo > 0). The Tier-E "holdout" arm (+0.239998) is NOT
      out of sample for this signal: the RangeFinder pins it rides were
      calibrated on BTC inside that era (BUILD §0.2).
    P-BE-1   [40%] HALT — NO VERDICT, PRESCRIBED. The floor at +1R
      moves exits only: 200/200 campaign keys paired with v6, 0 book-only,
      0 base-only (scores/DRYRUN.json arms[7].keys). The two-sample
      premise failed, and the text HALTs rather than quietly become the
      paired row. Its Tier-E arms all straddle zero. F-C10-BE NOT RUN
      per its §9: dip-before 36, dip-after 0, tie 0, mismatch 0, of 103 latch bars
      (lanes/BE_LATCH_CENSUS.json counts). A new id under set_change is
      the OPERATOR's to order; this contract adds no registration.
    P-TRG-2  [40%] SUPPORTED (CI-only; LOAO and the BH column ride
      beside, and both clear). Trigger 9/12 vs v6, CLASSIC5, full:
      n 198 vs base 200, Δ +0.257697 R, CI [+0.108587, +0.383892],
      p 0.005249 <= 0.016667, LOAO 5/5 above (4/5 at the sensitivity
      seed).
    P-BRK-I1 [35%] NOT SUPPORTED. 1d memory-line flip-hold:
      n 7 on 3 of 5 assets, +0.718270 R, CI [-0.602912, +1.452261],
      p 0.269683, LOAO 1/5 above. ETH's best trade alone (+6.1259 R)
      exceeds the book (+5.0279 R). Its 1d height-vs-toll gate PASSES
      on era ALL and FAILS on the holdout (POOLED:CLASSIC5 frozen3.0:
      edge NET -0.4360, 18 ranges, provisional).
    P-BRK-S1 [30%] NOT SUPPORTED — CI WHOLLY BELOW ZERO. 5m band-hold
      scalper, holdout only: n 1836, -0.211069 R,
      CI [-0.298366, -0.144105], LOAO 0/5 above, 5/5 BELOW, p 1.0.
      Its 5m gate: height PASS, edge-fade FAIL (edge NET -0.5885 ATR).
      The measured toll (median 17.76% of 1R) is a PRINT, not
      deducted; a deduction could only lower it.

  THE ONE THAT CLEARS, PRICED. P-TRG-2 is the cell TC9's grid lit,
  and the contract's one pre-naming:
    «exchange/status/LEDGER_APOLLO.md:2371-2374»
      | trigger-9/12 +94.40 R
      |     (CI [+0.121,+0.436], p=0.003, LOAO 5/5, sharing only 19 of 196
      |     campaigns with v6). A SELECTION, not a result. The next tier may
      |     pre-name ONE cell before the look; this one did not.
    «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:98»
      | P-TRG-2 [40%] trigger 9/12 replacing 12/26, vs v6 — the one grid pre-naming.
    - The sample is almost all already seen. 196 of its 198 campaigns
      entered at or before TC9's as-of (2026-08-22T00:00:00Z), and they
      re-net +94.3989 R. Their count, net, gross, fee, funding, best
      trade, win rate and key overlap with TC9's filed v6 journal
      (19 shared) all equal TC9's grid row for the cell. TC9 filed no
      per-campaign 9/12 journal, so this is an aggregate match, not a
      key-for-key one (close/P_TRG_2_SEEN_SHARE.json; F-SS 9/9 GREEN).
    - The unseen month holds 2 of its campaigns, both stopped out
      (close/P_TRG_2_SEEN_SHARE.json post), and 4 of v6's
      (close/FORWARD_STRIP.md).
    - Its own text:
      «research_outputs/tierc10/REGISTRATION_TEXTS.json#P-TRG-2.text»
        | So P-TRG-2 is in
        | large part an IN-SAMPLE RE-SCORE of a cell selected off that grid.
    - The tuning era alone is NOT SUPPORTED: Δ +0.188419,
      CI [-0.014369, +0.384652], LOAO 1/5 above. The edge sits after the
      R1 cut, and TC9 saw both sides of it: 64 of the book's 66
      post-cut campaigns entered at or before TC9's as-of.
    - SUPPORTED means only that it beats a v6 base which does not
      itself clear zero (v6 vs zero CI [-0.012774, +0.463319],
      panel/control_reference.parquet). It does not show that the 9/12
      book makes money.
    - ZEC carries +52.9031 of its +92.3499 R (per_asset_rows).
    Read it as the only registered cell in ten tiers to clear its own
    bar (TC9's last word, below; FAMILY.json rows[10]), and as a
    candidate for a genuine forward test. It is not out-of-sample
    confirmation, and not grounds for a card change or a SAIL act.

  THE 2026-07-29 RS RULINGS, CITED:
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
    Q-R5 — ATTESTED at STEP 0:
      «research_outputs/tierc10/PROGRESS.json#stages[stage=STEP 0].one_line»
        | Q-R5 attestation HOLDS (no RangeFinder constant inherited from the
        + SS Breakout Scanner, whose source is not in this repo at all)
    Q-R4 — MEASURED, the data's default NAMED per lens × era × horizon,
      NOTHING PROMOTED: "BREAK_CONFIRM_N=8 · BREAK_MARGIN=1.5 — UNCHANGED"
      on all 3,600 rows (census/acceptance_head_to_head.parquet
      engine_default_after). The RangeFinder dies on its margin, not its
      close count, in 81.9% / 82.4% / 87.2% of deaths (1d / 4h / 5m;
      close/S2_CENSUS_R.md §2.1), so the 8-close pin is nearly a dead
      letter. At 5m all five rules are net negative.
    Q-R3 — A GATE, filed per era:
      «research_outputs/tierc10/PROGRESS.json#stages[stage=CENSUS-R{4h,1d}].one_line»
        | [Q-R3] is a GATE per LEDGER.md:834, not a table: PASS per era ALL 9 / tuning 13 / holdout 7 of 120.
      5m single assets pass 0/17 on the holdout and 0/17 on ALL. The
      tuning-era passes (2/17 frozen3.0, 1/17 calibrated) are
      in-sample and are not evidence (census/height_toll_verdict.parquet).
      The height leg does no work, because the detector pins the
      height; the toll bites through the edge leg. NO range-trading
      contract is draftable at 5m on any pool, nor at 4h on any pool
      beyond one pool-era cell (CLASSIC5 holdout, frozen3.0, +0.0062).
      The other passes are single-asset cells (19 at 4h; 6 of the 7
      holdout-era passes): a selection over 360 rows (m logged), not
      grounds for a contract. The one 1d CLASSIC5 pool pass on full
      history (+0.0441) reverses on the holdout (-0.4360).

  THE SLIPPAGE-TWIN QUESTION — NAMED FOR THE AUTOPSY, NOT ANSWERED.
    - The twin: every row carries the charter tier model beside the
      TC-series toll: slippage per side tier A 2.0 / B 5.0 / C 10.0 bps,
      so a round trip of 14.0 / 20.0 / 30.0 bps against the TC-series
      10.0 bps, which is left untouched (data/fee_schedule.json).
    - It charges NO funding:
      «research_outputs/tierc10/scores/P-GEN-1.rows.json#rows[0].beside.haircut_twin.funding_note»
        | the filed twin charges fee + charter slippage and NO funding
    - So a "haircut" can read ABOVE the TC-series net. It does on
      8 of 20 arms (close/S5_FINDINGS_NOT_FIXED.json measured.ii). On
      P-TRG-2's scored arm it is +0.475588 against +0.466414.
    - On the v6 control's tuning era it flips the book's sign:
      TC -0.010763, twin +0.014494, with funding -0.030517
      (close/V6_CONTROL_HAIRCUT_TWIN.parquet).
    - No registration row flips sign (0/20).
    FOR THE AUTOPSY: does the charter tier model replace the TC-series
    flat toll for SAIL, and must the twin carry funding?

  ALSO FILED
    - CENSUS-R, Tier-E and a SELECTION: 7,920 outcome cells beside the
      gaps+order null of record (R10); H20 and H100 in
      close/S2_CENSUS_R.md §2.3.
    - Admitted 12/12 (P-GEN-1's panel) + CLASSIC5 5/5; none excluded
      (data/STAGE_D_MANIFEST.json admission).
    - The forward strip: v6 after TC9's as-of, 4 campaigns.
      3 closed for -0.689692 R; 1 open, marked +3.642965 R
      (close/FORWARD_STRIP.parquet). Never scored.
    - P-AGE-1, boundary-fade and regime-prior as Tier-E tables.
    - F-D-4: 102 cells, 0 pre-floor bars. F-D-5: never-touched =
      PUMPFUN, MNT, SUI.
    - The build document:
      exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md.

  INTEGRITY
    - 15 stages: 13 COMPLETE-VERIFIED, 2 PARTIAL (PROGRESS.json).
      D-CORE and D-5M are PARTIAL on F-D-1 alone.
    - F-CTRL/a, in process against tierc6:
      «research_outputs/tierc10/panel/FIXTURES_PANEL.txt:13»
        | WORST ABS DIFF = 0.000e+00 (bar EXACTLY 0.000e+00) over 12 columns; n=200
      F-CTRL/b, cross-process against the filed tierc9 journal, PASSES
      with one attributed funding drift:
      «research_outputs/tierc10/panel/FIXTURES_PANEL.txt:34»
        | funding_r moved on 1 closed campaign(s) — ZECUSDT 2026-08-17T04:00:00Z: funding_r 0.0 -> 0.014324, net_r -1.039899 -> -1.054223
      That drift is why v6 at or before TC9's as-of re-nets +38.7901 R
      here against TC9's filed +38.8044 R (close/P_TRG_2_SEEN_SHARE.json).
    - F-C10-RESUME:
      «research_outputs/tierc10/FIXTURES_RESUME.txt:224»
        | 9 GREEN, 0 RED (9 fixture(s) run)
      «research_outputs/tierc10/FIXTURES_RESUME.txt:120»
        | 1,090 recorded artifact content-sha(s) across 13 COMPLETE-VERIFIED stage(s) re-hashed, every one a MATCH
    - Scores re-write byte-identical on re-score:
      «research_outputs/tierc10/PROGRESS.json#stages[stage=B-CORE].fixtures[0].note»
        | all 5 rows files + all 5 .scored.json re-wrote BYTE-IDENTICAL
      «research_outputs/tierc10/PROGRESS.json#stages[stage=B-5M].fixtures[0].note»
        | re-wrote P-BRK-S1.rows.json, P-BRK-S1.scored.json and FAMILY.json BYTE-IDENTICAL
    - Commits and remote: ⟦STAMP AT CLOSE — replace this bracket with 'N tierc10 commits, M on a remote', read AFTER the CLOSE commit and push; F-LAR traces both through git; then re-run F-LAR⟧.
    - Worktree attestation is unconditional: all 28 review worktrees
      sit at a6da1b9 (close/S5_FINDINGS_NOT_FIXED.json measured.v).
      Named, not fixed.

  OPEN FOR THE OPERATOR (BUILD §6)
    - Q1 · F-D-1: REST or ARCHIVE?
    - Q2 · The 5m toll: print, or deduction?
    - Q3 · P-BE-1: order a new set_change id, or let HALT — NO VERDICT
      stand?
    - Q4 · The 5m hold rate: collared, or not? The collared reading
      was declared; the print was not made.
    - Q5 · PUMPFUN -> PUMPUSDT and MNT -> Bybit: ratify the leans, or
      name an exclusion?
    - Q6 · The push destination and consent to push and publish. R6
      granted the push; the destination is unnamed. The executor lean
      names /Volumes/LaCie/Repo Clone/naiad-backups; that is not the
      operator's word.
    - Q7 · Named for the autopsy: the slippage twin, above.
    - Q8 · Ratify or overrule three executor readings: the R1 era cut
      instant (1719791999000 ms = 2024-06-30T23:59:59Z); F-C10-RESUME
      hashing artifacts, not transcripts (PROGRESS.json
      f_c10_resume_law); and UNSEEN12 = the contract's twelve among the
      seventeen admitted, the reading under which these two agree:
      «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:90»
        | on the ADMITTED twelve
      «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:50»
        | ADMITTED LIST prints BEFORE any scoring and IS P-GEN-1's panel.

  NEXT · CENSUS-3.
    «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:139»
      | CENSUS-3 next.

  THE TIER LINE. TC9 closed on:
    «exchange/status/LEDGER_APOLLO.md:2422-2423»
      | NINE TIERS IN-SAMPLE; NOTHING HAS CLEARED ITS OWN BAR. SAIL-READY
      |     remains card_spec freeze at v6 PLAIN.
  TEN TIERS. THE OUT-OF-ASSET TEST (P-GEN-1) DID NOT CLEAR, AND ITS
  3 NEVER-TOUCHED ASSETS ALL SIT BELOW ZERO; THE TIME-HOLDOUT SCALPER'S
  CI LIES WHOLLY BELOW ZERO; ONE IN-SAMPLE CELL (P-TRG-2, 196/198 SEEN)
  CLEARS ITS OWN BAR. SAIL stays HELD (Q6). SAIL-READY remains
  card_spec freeze at v6 PLAIN.
=== END ===
