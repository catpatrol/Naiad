TIER-C10 · RESUME-AND-FINISH — self-contained; safe to re-send verbatim
RATIFIED: operator 2026-09-21 (TC10 contract; Q1–Q5 on lean; Q6 SAIL spec HELD
until TC10 autopsied; Q7 CENSUS-R as Stage 0) + 2026-09-22 ("builder session
interrupted… ascertain progress… finish the work"). Drafted: APOLLO. Executor:
HEPHAESTUS. Seed 20260921 UNCHANGED (a resumed run must equal a clean run).
Read-only worktrees for review · as-of warranty stamps · every fixture leg states
its failure condition · every grid whole.
STEP Q: file this paste verbatim to exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md
(sha printed) — the contract then survives any session.

LAW OF RESUMPTION (binding):
 1 · a stage is COMPLETE only if its artifacts exist, manifest shas verify, and its
     fixtures RE-PASS now; anything else is PARTIAL.
 2 · partials are QUARANTINED to research_outputs/tierc10/_partial_<ts>/ — never
     deleted.
 3 · registration texts below are FROZEN since 2026-09-21; any verdict the
     interrupted run computed is re-computed and printed BESIDE the fresh value —
     never re-worded, never re-chosen.
 4 · ONE corridor: the as-of of the COMPLETE Stage D manifest governs every stage;
     if Stage D is not complete, re-pin at resume and redo everything downstream.
 5 · the build doc drafts under research_outputs/tierc10/ and moves to
     exchange/reports/ ONLY at close (a draft under exchange/ is not a draft).
 6 · after EVERY stage: commit + update research_outputs/tierc10/PROGRESS.json
     {stage, status, artifact shas, as_of, fixtures} + one line to the draft.

R0 · PROGRESS CENSUS (read-only; writes only PROGRESS.json): identity v2 · branch
  v12-v1-census · HEAD · `git log --since=2026-09-20` (commits touching tierc10 /
  rangefinder / data) · `git status` (uncommitted files listed) · inventory vs this
  contract per stage: STEP 0 verdict · Stage D per asset×lens (bars, first/last ts,
  sha, gaps) · CENSUS-R tables · Stage A stamps · Stage B computed rows · fixtures.
  PRINT THE STAGE LEDGER (COMPLETE-VERIFIED / PARTIAL / ABSENT); resume at the first
  non-complete stage in this ORDER — core first, heaviest last:
  STEP 0 → D-CORE → CENSUS-R{4h,1d} → A → B-CORE → D-5M → CENSUS-R{5m} → B-5M → CLOSE

STEP 0 · PIN OF RECORD: the Argus note says TOUCH_EPS 0.67 / DEV_RETURN 8; the v2
  Pine inputs read 0.60 / 7 / BREAK_CONFIRM_N 8. Print both, the twin's sha, and its
  pins; HALT if twin ≠ Pine (name which drifted; resume word "pins-ok" after
  Argus's ruling). [Q-R5] grep-attest: the RangeFinder inherits NO values from the
  SS Breakout Scanner (2026-07-29 ruling).

D-CORE · DATA — twelve {ENA PUMPFUN HYPE MNT SUI LTC XMR BNB UNI PEPE DOGE BONK}:
  klines {1h,4h,12h,1d,1w} + funding + fee schedule; plus {1d,1w} for the 5-asset
  panel if absent (P-BRK-I1 needs them). VENUE OF RECORD per asset PRINTED — Binance
  USDT-M perps default; alternate ONLY where Binance lacks history; never spliced;
  funding from the kline venue. XMR (delisted from Binance 2024-02, per charter):
  a venue with a continuous XMR perp WITH funding, else EXCLUDE and name — no spot
  substitution [VETO "xmr"]. Contract multipliers (1000PEPE, 1000BONK, …) printed
  and normalized.
  ADMISSION: ≥ 316+400 closed 4h bars; excluded assets named with counts; the
  ADMITTED LIST prints BEFORE any scoring and IS P-GEN-1's panel.
  COSTS: every row gets the charter model as a HAIRCUT TWIN beside the TC-series
  toll — slippage/side tier A {BTC ETH} 2 bps · tier B {SOL NEAR ZEC LTC BNB DOGE
  UNI SUI XMR} 5 · tier C {ENA PUMPFUN HYPE MNT PEPE BONK} 10 [VETO "tiers"]. The
  5-asset control's TC-series accounting stays untouched; its twin is an ADDED
  column.
  FIXTURES: F-D-1 three assets' bars vs venue API · F-D-2 no synthetic bars ·
  F-D-3 funding coverage per asset · F-D-4 TWO-TOKEN TRAP (LIT precedent): first
  valid candle verified as the INTENDED asset (listing date + source printed;
  prior-asset history hard-floored; price continuity at the floor) — FAILS IF any
  symbol's history predates its intended listing unfloored · F-D-5 DATA-SPEND
  AUDIT: grep LEDGER.md, exchange/status/LEDGER_*.md, the probe ledger,
  Naiad_Phase0_Charter.md and the RangeFinder builds; print {never-touched /
  display-only / scored} per asset (PUMPFUN and HYPE read, not assumed).

CENSUS-R (Tier-E · "a SELECTION, not a result" · m logged · NO registrations):
  twin module-ized as analytics/rangefinder.py, pins = STEP 0 sha, F-RF fixtures
  riding; full history × 17 assets × lens:
  · coverage / confirmed-range density / mean life per asset+lens (REPORT-ONLY);
    SCALE_MULT self-calibrated per asset to 0.75 confirmed ranges / 100 bars,
    printed
  · F-RF-4 spring overlap, both directions
  · OUTCOME TABLES after each event {breach, harden, DIE, memory-touch, flip-hold,
    retest-hold on EMA band} at H20/H100, net of the lens's measured toll
  · NULL MODEL: random-boundary box sets at matched coverage, same tables
  · [Q-R4] the four acceptance operationalisations head-to-head {2-close · 3-close
    · 6-outside-close stale-run · time-beyond} beside the RangeFinder DIE rule
    (8-close OR 1.5 ATR); the data's default named, nothing promoted
  · [Q-R3] HEIGHT-vs-TOLL feasibility per lens (confirmed-range height ÷ round-trip
    toll, distribution) + the EDGE-FADE outcome leg; boundary-fade stays Tier-E
  · F-RNG-ASOF: no feature reads a confirm/redraw stamped after its bar — sabotage
    leg: a leaked redraw must FAIL it.

A · TAPE + STAMPS: every funnel instant of every card stamped {macro state ·
  %-of-range · dist-to-boundary ATR as-of · boundary age · deviations per side ·
  last flip}; captured-not-consulted; import-closure extended to
  analytics/rangefinder.py.

B · REGISTRATIONS — TEXT FROZEN (two-sample · D15 trio · LOAO above-half 3/5 ·
  FDR m=6, independently failable):
  P-GEN-1 [45%] card v6, ALL pins frozen, on the ADMITTED twelve: expectancy vs
    zero, LOAO across the admitted, per-asset rows, raw + equal-risk co-headlines,
    17-asset view beside; LOAO printed twice (all admitted · never-touched only);
    haircut twin on every row.
  P-SPR-2 [45%] sharpened spring = deviation-confirm at a CONFIRMED macro boundary,
    4h, 5-asset exploration-classic, vs card/standalone.
  P-BE-1 [40%] breakeven floor at first tape +1R, SEQUENCED (dip before/after +1R
    from tape order), 5-asset book, vs v6.
  P-TRG-2 [40%] trigger 9/12 replacing 12/26, vs v6 — the one grid pre-naming.
  P-BRK-I1 [35%] INVESTOR: 1d macro DIE → first flip-hold on the memory-line →
    enter; stop beyond retest extreme, rail 1.0 ATR(1d); permission = weekly 12>25
    posture AND daily 12/25 direction; v6 management lens-scaled; net 10 bps +
    funding.
  P-BRK-S1 [30%] SCALPER: 5m macro DIE → first HOLD retest of the 5m 89 or 200/300
    band (FLIP_HOLD pins) → enter at hold close; stop beyond retest extreme, rail
    1.0 ATR(5m); 4h tide aligned; v6 management lens-scaled; NET OF MEASURED 5m
    TOLL.
  PANEL PIN (reviewer's drafting gap, closed before any result is read): both BRK
    forms score on the 5-asset book per G-7; the 17-asset view is Tier-E. If R0
    finds a BRK verdict already computed on another panel, print both — this pin
    governs, and the gap is filed as a finding.
  Each BRK form also prints the OTHER anchor (EMA band ↔ memory-line) as Tier-E,
    and carries its lens's height-vs-toll verdict ON ITS ROW.
  P-AGE-1 (tide-youth), boundary-fade, regime-prior: Tier-E tables only.
  FORWARD STRIP (report-only): the 5-asset v6 book from TC9's as-of
    (2026-08-22T00:00Z) to this corridor's end — printed, labeled, never scored.

D-5M → CENSUS-R{5m} → B-5M: 5m klines for the admitted twelve (heaviest fetch,
  resumable per asset), then the 5m census tables, then P-BRK-S1.

FIXTURES: F-CTRL v6 on 5 assets 0.000e+00 over TC9's corridor, cross-process
  anchored to the filed tierc9 journal (campaigns open at TC9's as-of reported as
  continuations, not diffs) · F-D-1..5 · F-RNG-ASOF · F-RF-4 printed · F-C10-HOLD
  (3 holds per lens hand-verified; a failed hold must FAIL) · F-C10-BE (sequence
  proven on 3 campaigns) · F-C10-TOLL (5m toll read from the grid table, never
  typed) · F-C10-RESUME (every COMPLETE stage re-hashes identical to its
  PROGRESS.json record; a tampered partial must FAIL) · F-DET · F-GRID · F-KEY ·
  import-closure · worktree attestation.

CLOSE: exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md (name unchanged —
  one build, one document, however many sessions).
  · §0 verdicts first: six rows + the admitted list + the forward strip
  · §R0: what the interruption left, what was quarantined, what was redone
  · CENSUS-R tables, with outcome-after-event, the acceptance head-to-head and
    height-vs-toll prominent
  · Stage D manifest incl. the F-D-4 / F-D-5 tables
  · findings-not-fixed · BOX-COST
  LEDGER_APOLLO append: Q6 hold verbatim ("spec held until TC10 autopsied"); m=6;
  the 07-29 RS rulings cited; the slippage-twin question named for the autopsy;
  CENSUS-3 next. publish_exchange; STATE push result; bright paths; final line:
  "Operator: click Sync now."

WHAT THIS PASTE IS NOT: no pin refit · no registration re-worded or added ·
no SAIL act (spec held by operator word) · no trust extended to anything the
interrupted session left.
