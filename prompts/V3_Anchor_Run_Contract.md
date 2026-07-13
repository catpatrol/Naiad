CONTRACT — v12 STUDY, PHASE V3: ANCHOR RUN (FULL GRID)
Status: RATIFIED BY OPERATOR (Ludwig, 2026-07-13). Builder: save this file as
prompts/V3_Anchor_Run_Contract.md, commit "v3: anchor run contract (ratified)",
push, then execute STAGE 1 ONLY and stop.

AUTHORITY & GATE: V2 closed at 03cf247; V3 open per VR-4 / Charter Addendum.
This is the pre-registered design of the study's first scored backtest and the
baseline for all five named-variant slots. Evidence-spend accounting applies.

STAGE 1 — PRE-FLIGHT (read-only; no scored output; no evidence spend)
F1. Partition map. From the chartered definitions in the repo (quote the
    defining lines verbatim), print per asset: first-valid candle; the date
    spans falling in each evidence class (exploration-classic, lockbox, spent,
    regime-contaminated, forward); and the resulting SCORABLE span per cell
    for this run. Flag any cell whose scorable span is empty.
F2. Engine identity. Engine commit; config = v11_faithful, zone_memory = 3;
    config hash; git-confirm zero engine-code changes since the parity-signed
    1.0.3 merge (38b3f66).
F3. Execution semantics. Print, with code/spec references: the fill rule
    (signal confirmation -> fill bar/price), sizing (0.5R pilot / 0.5R adds +
    1R shadow line), and which cost components the engine models (fees,
    funding, slippage). State plainly what is NOT modeled.
F4. Lockbox guard. State the mechanism preventing any lockbox-window bar from
    being loaded in scored runs, and how the run manifest will prove it
    (per-cell loaded-span assertions). If no mechanism exists, propose the
    minimal one; do not run without it.
F5. Runtime. Estimate wall-clock for one full-grid pass and for the
    determinism double-run; if the double-run is impracticable, propose a
    repeat subset spanning all three mandates.
F6. Warm-up. Confirm warm-up bars (2000 exec / 200 gov per replay policy) are
    drawn from within each cell's scorable span, never from lockbox.
STOP. Report Stage 1 to operator + reviewer. Stage 2 executes only on an
explicit operator go after reviewer check.

STAGE 2 — ANCHOR RUN (on go)
R1. Scope: all 30 cells x their F1 scorable spans. Config frozen per F2.
    Journals regenerated into clean state (regenerate-never-merge).
    Determinism: full double-run (or the F5-ratified subset); per-cell journal
    SHA256 byte-identical between passes.
R2. Scoring: R-unit accounting; per-cell risk halts (d146de6); costs per F3 +
    VD-1 defaults; no scored number presented gross-only.
R3. Annex (characterization-only; excluded from all scored aggregates and all
    hypothesis scoring; labeled CHARACTERIZATION in every artifact): BTC spent
    window (VD-5); regime-contaminated non-BTC spans (VD-3).
R4. Cell card, per cell x partition: campaigns; trades (entries + adds);
    campaign win rate; gross R; net R; expectancy per campaign with 95%
    bootstrap CI (campaign-level resampling, 10,000 draws); max drawdown (R);
    profit factor; top-1 campaign share of net R; strip-best-trade net R;
    strip-best-campaign net R; taxonomy census (NEVER_GREEN / STILLBORN /
    FADED / PROTECTED); TPW / V / X counts; halt events; time-in-market.
    <10 campaigns -> INSUFFICIENT SAMPLE flag, CI still printed.
R5. Rollups: per-mandate and per-asset net R with CI; grade-cohort expectancy
    table (A+ / A / B / C); pooled taxonomy census. Every rollup carries its
    strip-best-campaign line.
R6. Hypothesis scorecard: score H-A1..H-A5 exactly at the pre-registered
    thresholds below; no post-hoc re-thresholding.

PRE-REGISTERED HYPOTHESES (scored partitions only)
H-A1 tail-carried (~85%): removing the single best campaign cuts grid total
     net R by >=25%; and in a majority of net-positive cell-partitions the top
     campaign carries >=30% of that cell's net R.
H-A2 grade gating (~70%): pooled net expectancy per campaign orders
     A-or-better > B > C.
H-A3 cross-asset transfer (~50%): at least two of {ETH, SOL, NEAR, ZEC} show
     positive net total R in exploration-classic in their diagonal mandate.
H-A4 mandate ordering (~60%): pooled per-campaign net expectancy:
     position >= swing >= intraday.
H-A5 stillborn-heavy (~65%): STILLBORN is the single largest taxonomy cohort
     grid-wide.
Falsifications are findings; each narrows the next design.

DELIVERABLES: run manifest (engine commit, config hash, partition map, cost
semantics, per-cell loaded spans proving lockbox untouched); per-cell journals
+ SHA256s; 30 cell cards + annex cards; rollups; hypothesis scorecard;
determinism proof; packet zip for reviewer; drafted ledger entry recording the
evidence spend (exploration-classic FIRST LOOK consumed; run_id + SHA).
Reviewer recomputes all headline numbers from raw journals before any number
is treated as real.

VERDICT CRITERIA: the Stage 2 verdict concerns machinery integrity, not P&L.
PASS = deterministic SHAs, lockbox proof clean, partition map honored, cards
complete. The P&L is evidence, never a pass/fail.

WHAT THIS PHASE IS NOT: no parameter changes; no variant runs (five slots
untouched); no lockbox contact; no re-run against a read partition (that is a
new evidence spend requiring a chartered variant); no engine strategy-code
changes (J-1 stays parked; an F4 guard, if needed, is manifest-level only);
no live-capital implications.

## AMENDMENT A1 — Stage 1 rulings (ratified 2026-07-13)
- Q-1: run config = configs/v12_anchor.yaml — signal block byte-identical to v11_faithful.yaml; trading + shadows blocks from naiad_v0.yaml; v_births_provisional: false (Pine v11.0.2 literal; divergence from naiad_v0 recorded). Manifest must include PROOF: signal-section diff vs v11_faithful = EMPTY; trading/shadows diff vs naiad_v0 = exactly the v_births_provisional line. Stage-1 "BLOCKER B-1" is recorded under Q-1; register name B-1 remains the 12H-swing-mode backlog item.
- Q-2: R3 annex proceeds under narrow exception F4-a — lockbox bars loadable ONLY as indicator warm-up for annex windows; zero signal emission and zero output from any lockbox bar; manifest lists every lockbox span traversed, per annex cell. G-1 REGISTERED: replay path has no code-level lockbox guard; this run protected by window arithmetic + manifest loaded-span assertions; code guard due at next engine touch alongside J-1.
- Q-3: "0.5R pilot" = charter §3.4 grade-table shorthand (authoritative). Manifest states in one paragraph what the shadows layer computes; if it is the §3.4 1R-adds counterfactual, report per cell; else record counterfactual unimplemented and map "1R shadow line" to max_open_campaign_risk_r: 1.0.
- Q-4: month-aligned scored starts per F1; TAOUSDT_swing runs at 30 days with INSUFFICIENT SAMPLE flag.
- R4/R5 amended: every cell card and rollup carries VR-3 cost-stress rows (0x / 1x / 2x), recomputed from per-row journal cost fields; no re-runs.
- Scored grid = 20 cells; the 10 EMPTY cells get structural cards (annex where their evidence class provides one; TAOUSDT_position appears only in the regime-contaminated annex).
