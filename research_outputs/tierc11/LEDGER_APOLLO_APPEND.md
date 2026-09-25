
---

=== STATUS_APOLLO — 2026-09-25 — TIER-C11 · THE ENGINE BOUND TO EVENTS: RANGES NESTED, WARNINGS MEASURED, EVERY ACTION GIVEN ITS TRIGGER ===
LANE      APOLLO (drafted) · HEPHAESTUS (executor) · branch v12-v1-census · seed 20260924
CLASS     NINE REGISTRATIONS, ONE FAMILY, TEXT FROZEN AT STEP Q AND FILED
          BEFORE ANY TC11 BOOK (registry head 6772568b…, REGISTRY_PIN.json).
          m = 9, one fixed bar q/m = 0.1/9 = 0.011111 (1/90);
          8 tests spent — P-SCALP-2 was closed by its own R2 precondition and
          spent none, and fewer tests never loosen the bar (scores/FAMILY.json).
          As-of 2026-09-25T00:00:00Z, one corridor (snapshot tc11_20260925).
          Every «cite» below is re-verified against its source by F-LAR11 and
          every number is traced to its file and field by F-NUM
          (scripts/tierc11_close_fixtures.py).

  THE FAMILY — ONE, AS FILED:
    «exchange/queue/2026-09-24_TC11_APOLLO.md:9»
      | ONE family, m = 9 independently-failable hypotheses (bar 0.10/9)
    «research_outputs/tierc11/scores/FAMILY.json#law»
      | a registration closed by its own precondition or condition spends no test and never loosens the bar

  SAIL · STILL HELD.
    «exchange/queue/2026-09-24_TC11_APOLLO.md:99»
      | (m=9; SAIL still HELD; the forward ledger opened)
    «exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:2-3»
      | Q6 SAIL spec HELD
      | until TC10 autopsied
    Held. Nothing in this tier is a SAIL act; the one SUPPORTED row below is
    an in-sample re-score, not confirmation, and no card change is proposed.

  VERDICTS, each under its own text (the contract's lines, sliced by
  REGISTRATIONS.json text_lines) with its verdict cell and labels
  (scores/SCORES.json rows[].verdict_cell) and its numbers (rows[].stats):
    P-WARN-1
      «exchange/queue/2026-09-24_TC11_APOLLO.md:40-42»
        |  P-WARN-1 [40%, CONDITIONAL]: IF W2's "1h counter-12/89 before +1R" cohort's E[net] is below the
        |     base by a cluster-90% interval excluding zero, score the rule "exit at the 1h counter-12/89 close
        |     while pre-+1R" paired vs v6; ELSE report-only, no slot spent, stated.
      «research_outputs/tierc11/scores/SCORES.json#rows[registration=P-WARN-1].verdict_cell»
        | NOT SUPPORTED
      n 200 (base 200, paired) · point +0.0056 R · CI [-0.0092, +0.0217] · p 0.303424 · clears bar: no
    P-AGE-1
      «exchange/queue/2026-09-24_TC11_APOLLO.md:45-46»
        |  P-AGE-1 [50%] tide-age gate, TRAILING-quantile definition (refuse the OLD band) vs v6; the absolute
        |     definition (refuse age > 206 bars) printed as shadow.
      «research_outputs/tierc11/scores/SCORES.json#rows[registration=P-AGE-1].verdict_cell»
        | SUPPORTED — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: the
        + scored cohort IS TC10 P_AGE_1_TIDE_YOUTH B4 (same function, same
        + trailing edges, same 200 campaigns, anchored by F-CTRL(b)); point
        + known before filing; new campaigns since 2026-09-21T16:00Z: scored 0
        + / base 0)
      n 141 (base 200, two_sample) · point +0.2461 R · CI [+0.1912, +0.2967] · p 0.000250 · clears bar: yes
    P-WIN-1
      «exchange/queue/2026-09-24_TC11_APOLLO.md:47-48»
        |  P-WIN-1 [50%] window-age gate: refuse triggers with arm→trigger lag ≥ 16 bars vs v6; lag 7–15
        |     printed as shadow cut.
      «research_outputs/tierc11/scores/SCORES.json#rows[registration=P-WIN-1].verdict_cell»
        | NOT SUPPORTED — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY
        + (selection_hazard: direction informed by TC6V L-LAG deciles on the
        + same corridor (lag-0 +0.4149, 56-bar decile -0.5796))
      n 137 (base 200, two_sample) · point +0.1753 R · CI [+0.0030, +0.3393] · p 0.036491 · clears bar: no
    P-BRK-4H
      «exchange/queue/2026-09-24_TC11_APOLLO.md:52-54»
        |  P-BRK-4H [45%] the 4h breakout-retest lane: 4h macro death → first HOLD retest on the 89 tap (memory-
        |     line printed beside); stop beyond retest extreme railed 1.0 ATR(4h); tide aligned; v6 management;
        |     vs zero, five assets (seventeen Tier-E).
      «research_outputs/tierc11/scores/SCORES.json#rows[registration=P-BRK-4H].verdict_cell»
        | NOT SUPPORTED — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY
        + (selection_hazard: the best of 7,920 TC10 census cells (4h
        + retest-hold-tap89, CLASSIC5 NET H20 +0.681 ALL n 236 / +0.706
        + holdout n 88; UNSEEN12 +0.064 / +0.272)) · SCALE-IN-SAMPLE (holdout
        + slice, derived: n 112, +0.2234 [-0.0715, +0.5555] p 0.087728; 1 of
        + 112 of its campaigns carry a range read <= the era cut (in-sample;
        + scale_in_sample, die_close_ms<=cut); filed tierE__holdout: n 112,
        + +0.2234 [-0.0715, +0.5555] p 0.087728; frozen-3.0 twin
        + tierE__frozen3: n 232, +0.1651 [+0.0584, +0.2776] p 0.000250; pick
        + stability (4h, first half of tuning vs tuning, CLASSIC5 [L-R.2]):
        + CHANGED on NEARUSDT 2.0->1.75 (63 of 322 campaigns on a changed
        + asset))
      n 322 (vs zero) · point +0.0503 R · CI [-0.0920, +0.2081] · p 0.318170 · clears bar: no
    P-RELAY-1
      «exchange/queue/2026-09-24_TC11_APOLLO.md:55-57»
        |  P-RELAY-1 [45%] ["relay"]: 4h window open+armed; ENTRY on the 1h 9/12 with-trend close inside it;
        |     stop = 4h pivot railed, R on 4h; miss column first-class (windows the relay never activates);
        |     vs the 12/26-triggered base, two-sample.
      «research_outputs/tierc11/scores/SCORES.json#rows[registration=P-RELAY-1].verdict_cell»
        | NOT SUPPORTED
      n 173 (base 200, two_sample) · point +0.2496 R · CI [-0.4412, +1.2600] · p 0.308423 · clears bar: no
    P-SCALP-2
      «exchange/queue/2026-09-24_TC11_APOLLO.md:71»
        |  P-SCALP-2 [30%] vs zero, five assets, holdout era, taker; the maker twin and the 17-asset view Tier-E.
      «research_outputs/tierc11/scores/SCORES.json#rows[registration=P-SCALP-2].verdict_cell»
        | CLOSED BY PRECONDITION (builder's stage status: CLOSED BY R2 (1h:
        + FAIL)) — report-only · no number · no slot spent · beside, Tier-E
        + [§10] (tier TIER-E · a SELECTION, not a result · gates nothing): the
        + tuning-era R2 1h word FAIL (holdout word of record FAIL)
      no number, no slot spent (FAMILY.json spent_test false).
    P-ADD-BRK
      «exchange/queue/2026-09-24_TC11_APOLLO.md:75-76»
        |  P-ADD-BRK [40%]: add when a range ONE LENS BELOW the trade (1h for a 4h campaign) DIES in the trade's
        |     direction after +1R has been touched.
      «research_outputs/tierc11/scores/SCORES.json#rows[registration=P-ADD-BRK].verdict_cell»
        | NOT SUPPORTED · SCALE-IN-SAMPLE (holdout slice, derived: n 77,
        + -0.0453 [-0.1479, +0.0446] p 0.780055; 0 of 77 of its campaigns
        + carry a range read <= the era cut (in-sample;
        + n_adds_scale_in_sample); filed tierE__holdout: n 77, -0.0453
        + [-0.1479, +0.0446] p 0.780055; frozen-3.0 twin tierE__frozen3: n
        + 200, +0.0179 [-0.0510, +0.0962] p 0.363909; pick stability (1h,
        + first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on
        + BTCUSDT 2.0->1.75, SOLUSDT 2.0->1.75, NEARUSDT 2.0->1.75 (115 of 200
        + campaigns on a changed asset))
      n 200 (base 200, paired) · point -0.0202 R · CI [-0.0741, +0.0348] · p 0.730817 · clears bar: no
    P-ADD-SFP
      «exchange/queue/2026-09-24_TC11_APOLLO.md:77-78»
        |  P-ADD-SFP [40%]: add when a swing-failure CONFIRMS at the trend-side boundary of the 1h range (the
        |     deviation back into range in the trade's favour) after +1R.
      «research_outputs/tierc11/scores/SCORES.json#rows[registration=P-ADD-SFP].verdict_cell»
        | NOT SUPPORTED — CI wholly below zero · SCALE-IN-SAMPLE (holdout
        + slice, derived: n 77, -0.0324 [-0.0619, -0.0029] p 1.000000; 0 of 77
        + of its campaigns carry a range read <= the era cut (in-sample;
        + n_adds_scale_in_sample); filed tierE__holdout: n 77, -0.0324
        + [-0.0619, -0.0029] p 1.000000; frozen-3.0 twin tierE__frozen3: n
        + 200, -0.0034 [-0.0071, +0.0000] p 1.000000; pick stability (1h,
        + first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on
        + BTCUSDT 2.0->1.75, SOLUSDT 2.0->1.75, NEARUSDT 2.0->1.75 (115 of 200
        + campaigns on a changed asset))
      n 200 (base 200, paired) · point -0.0200 R · CI [-0.0314, -0.0070] · p 1.000000 · clears bar: no
    P-TP-RNG
      «exchange/queue/2026-09-24_TC11_APOLLO.md:83-86»
        |  P-TP-RNG [35%]: take-profit of the remainder at the approach (0.25 ATR) of the NEXT-HIGHER lens's range
        |     boundary (12h boundary for a 4h campaign) when that lens is IN-RANGE; if the lens above is in
        |     EXPANSION, no take-profit (let the trail run) — paired vs v6; the wall-exit lesson (tail cut) is the
        |     named risk and the D15 tail ratio is printed on the row.
      «research_outputs/tierc11/scores/SCORES.json#rows[registration=P-TP-RNG].verdict_cell»
        | NOT SUPPORTED · SCALE-IN-SAMPLE (holdout slice, derived: n 77,
        + -0.0426 [-0.1563, +0.0737] p 0.727068; 0 of 77 of its campaigns
        + carry a range read <= the era cut (in-sample; scale_in_sample_12h);
        + filed tierE__holdout: n 77, -0.0426 [-0.1563, +0.0737] p 0.727068;
        + frozen-3.0 twin tierE__frozen3: n 200, +0.0243 [-0.0132, +0.0600] p
        + 0.148963; pick stability (12h, first half of tuning vs tuning,
        + CLASSIC5 [L-R.2]): CHANGED on BTCUSDT 1.75->2.0, ETHUSDT 2.0->1.5,
        + SOLUSDT 1.75->2.25 (123 of 200 campaigns on a changed asset))
      n 200 (base 200, paired) · point -0.0200 R · CI [-0.0813, +0.0500] · p 0.743064 · clears bar: no

  RANGE TRADING — THE R2 LAW CLOSES IT ON 5m–1d; 1w FAIL IS PROVISIONAL (Q4):
    «exchange/queue/2026-09-24_TC11_APOLLO.md:16-18»
      |  R2 FEASIBILITY GATE PER LENS [Q-R3 law]: confirmed-range height ÷ round-trip toll (distribution) + the
      |     edge-fade leg; PASS/FAIL printed per lens; a FAIL closes that lens
      + for range trading in this and every
      |     later tier unless the toll model changes (maker twin below is the only reopening path).
    «research_outputs/tierc11/stage_r/STAGE_R.md:35»
      | - The lens verdicts of record per lens: 5m **FAIL** · 15m **FAIL** ·
      + 1h **FAIL** · 4h **FAIL** · 12h **FAIL** · 1d **FAIL** · 1w **FAIL
      + (provisional, n<30)**
    Under that law a FAIL closes the lens for range trading in this and every
    later tier unless the toll model changes, and the maker twin (the only
    reopening path) reads FAIL at every record cell (R2_LENS_VERDICTS.json
    lenses[*].maker_twin): range trading is closed on 5m–1d. 1w reads
    FAIL (provisional, n<30): its counts sit under the floor (n_ranges 6,
    edge_n_ranges 5 < 30) while its measured values clear their bars (median
    height ÷ toll 1626 ≥ 3.0; edge net +1.1236 ATR > 0), so whether it closes
    1w is the operator's question (BUILD §11 Q4). At 1h the edge leg nets
    -0.16760525 ATR (median H20 +0.00000000 - taker toll 0.16760525): Stage S
    is CLOSED BY R2 (1h: FAIL) and P-SCALP-2 spent no slot.

  THE FORWARD LEDGER — OPENED, STANDING, UNSCORED:
    «research_outputs/tierc11/forward/FORWARD_LEDGER.md:5»
      | opening 2026-09-21T16:00:00Z (entry close must be after it)
    «research_outputs/tierc11/forward/FORWARD_LEDGER.md:7»
      | **Standing and UNSCORED until each book's own n >= 30.** No CI, no p, no verdict.
    base v6: n 0 appended; the continuation ETHUSDT long entered 2026-09-18T08:00:00Z
      (at or before the opening) is listed, not counted: stop +2.707180 R.
    frozen 9/12: n 0 appended; OPEN at the pin 2026-09-25T00:00:00Z: SOLUSDT long entered
      2026-09-24T16:00:00Z, marked -0.031452 R, listed, not counted.
    Each book stays UNSCORED until its own n >= 30. A refresh past the pin needs
    the foundation re-rooted on a new snapshot + pin record:
      «research_outputs/tierc11/forward/FORWARD_LEDGER.md:38»
        | a refresh on bars after 2026-09-25T00:00Z needs the foundation re-rooted

  THE PUSH FACT (git, read at draft time):
    The operator's daily publish 4ae8c81 ("exchange: auto-publish 2026-09-25",
    committed 2026-09-25T07:00:11-03:00) pushed the branch:
    origin/v12-v1-census = 4ae8c81.
    At HEAD d307829: 8 of the 9 tierc11 commits are on origin; not on
    origin: d307829.
    This block follows TC10's: TC11's close_acts.sh preconditions stop until
    TC10's report is tracked in exchange/reports/ and TC10's STATUS block is
    committed on this ledger (the ledger keeps tier order).
    - Commits and remote at CLOSE: ⟦STAMP AT CLOSE — replace this bracket with 'N tierc11 commits, M on a remote', read AFTER the push (close_acts.sh step 3); then re-run scripts/tierc11_close_fixtures.py F-LAR11 --stamped⟧.

  ALSO FILED
    - R5 (tier TIER-E · a SELECTION, not a result · gates nothing): v6 is not
      killed in chop at entry — in-range 4h entries net positive, calibrated n
      141 E +0.1677 R (SCALE-IN-SAMPLE: 88 of them read in-sample; holdout
      slice E +0.4133 R), frozen3.0 n 94 E +0.2867 R (stage_r/R5_CHOP.md).
    - P-WARN-1's condition was MET (cohort n 42, delta -0.728647, cluster
      interval [-0.964287, -0.527794]), so its rule was scored, paired — flat.
    - R4, the fractal grid, whole: 180,684 rows (stage_r4/R4_GRID.parquet), Tier-E.
    - Findings not fixed: research_outputs/tierc11/close/S5_FINDINGS_NOT_FIXED.md
      (BUILD §10).
    - The build document: exchange/reports/BUILD_2026-09-24_TIERC11_EVENTS.md
      (FLAGGED: over the 64,000 B wire; close/BOX_COST.md).

  INTEGRITY
    - Fixture sweep of record: 17 suites, 134 fixtures GREEN (PROGRESS.json last_sweep_utc).
    - F-CTRL-a, v6 on the TC11 corridor against tierc6:
      «research_outputs/tierc11/books/FIXTURES_BOOKS.txt:16»
        | WORST ABS DIFF 0.000e+00 (bar EXACTLY 0.000e+00)
    - Worktree attestations: every record under review/attest/ reads GREEN
      (causality, fidelity, fix-head, reproducibility, statistics, trading); the lens reviews at
      04067a0, fix-head at d307829.

  OPEN FOR THE OPERATOR (BUILD §11)
    - Q1 · MINOR-9: rule on the 156 SCORES.json leaves added since the lens
      reviews (none moved) — keep them, or re-file the scorer's record?
    - Q2 · The contract's BUILT stamp: stamp it and re-pin REGISTRATIONS.json,
      REGISTRY_CHECK.json and PROGRESS.json, or leave the contract
      byte-frozen?
    - Q3 · TC10's Q2 (does slippage join the toll of record?) stays open;
      every TC11 row carries the haircut twin beside the toll of record, never
      instead of it.
    - Q4 · R2 1w reads FAIL (provisional, n<30); its counts sit under the
      floor while its measured values clear their bars. Accept it as closing
      1w for range trading, or order a re-measure when the lens has the
      ranges?
    - Q5 · The forward ledger: order the foundation re-rooted on a new
      snapshot and pin record so it can refresh.
    - Q6 · The push and the publish: run TC10's close_acts.sh (its step-6
      `git add` needs -f: FN-M-TC10-ACTS-IGNORED), then TC11's — both are the
      operator's acts.
    - Q7 · The tierc11x lane vendors the pre-AM-1 env shim: align the two
      lanes, or keep them apart?
    - Q8 · The post-hoc candidates the reviews name (the relay in the windows
      v6 enters late; the memory-line first-hold twin): order a forward
      registration, or let them lie?
    - Q9 · Two reading conflicts the fidelity review names (L-W.4 against
      L-1.4 on Tier-E intervals; L-W.1 read as less-or-equal): ratify or
      overrule each.

  THE TIER LINE. TC10's block (staged at
  research_outputs/tierc10/LEDGER_APOLLO_APPEND.md, and required on this
  ledger before this block by close_acts.sh's preconditions) closes on:
    «research_outputs/tierc10/LEDGER_APOLLO_APPEND.md:250-254»
      | TEN TIERS. THE OUT-OF-ASSET TEST (P-GEN-1) DID NOT CLEAR, AND ITS
      |   3 NEVER-TOUCHED ASSETS ALL SIT BELOW ZERO; THE TIME-HOLDOUT SCALPER'S
      |   CI LIES WHOLLY BELOW ZERO; ONE IN-SAMPLE CELL (P-TRG-2, 196/198 SEEN)
      |   CLEARS ITS OWN BAR. SAIL stays HELD (Q6). SAIL-READY remains
      |   card_spec freeze at v6 PLAIN.
  ELEVEN TIERS. ONE IN-SAMPLE RE-SCORE (P-AGE-1, NO NEW CAMPAIGN SINCE THE
  TC10 PIN) CLEARS ITS OWN BAR; SEVEN SCORED ROWS DO NOT; P-SCALP-2 IS CLOSED
  BY R2; THE R2 LAW CLOSES RANGE TRADING ON 5m–1d, 1w PROVISIONAL (Q4). SAIL
  stays HELD; no card change is proposed.
=== END ===
