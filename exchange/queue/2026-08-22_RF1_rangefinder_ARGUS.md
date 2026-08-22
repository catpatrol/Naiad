# QUEUE RF-1 v2 — SS12-RANGEFINDER v0 · range lifecycle with DEVIATIONS

Drafted ARGUS 2026-08-22. Executor HEPHAESTUS. Reviewer ARGUS.
RATIFIED: operator, 2026-08-22 — by firing; rulings D-R1a/D-R2a/D-R3b/D-R4 + name
"SS12-RangeFinder". SOURCE: public artifacts of a closed-source system (@sergio_tesla_,
2026-08-10 post + two screenshots); reconstruction, not code access. Display-only;
renders-never-rules; hypotheses route to APOLLO under G-7.
BUILT: PENDING
IDEMPOTENCE NOTE: no prior RF1 queue file existed at firing; this v2 is filed fresh
(the fresh-file path), carrying the v2 designation from the commission itself.

## THE STATE MACHINE (one semantics, twin and Pine)

MS PIVOT [D-R2a]: ATR-ZigZag — reversal >= REV_MIN*ATR(14) confirms a pivot at the
  wick extreme; legs shorter than LEG_MIN*ATR merge. Pivots alternate by construction.
SEED (POTENTIAL, a STOCK): expansion terminal pivot P0 + first counter-pivot P1 that
  fails to exceed it => POTENTIAL range {top,bottom} at wick extremes. POTENTIAL count
  in the status line = currently unresolved candidates [inferred from 6-vs-20].
CONFIRM: first full traverse touching the opposite boundary within TOUCH_EPS*ATR =>
  CONFIRMED; diamond stamped at the touched boundary's bar [observed].
BREACH => PENDING (the correction, his checklist verbatim): a body close beyond a
  CONFIRMED boundary opens a PENDING breach; the range does NOT die yet.
  RESOLUTION, whichever comes first:
   - DEVIATION CONFIRMED: price body-closes back INSIDE within DEV_RETURN_BARS =>
     range SURVIVES and is REDRAWN — boundary extended to the breach extreme; the slab
     original-boundary->extreme renders as a DEVIATION ZONE (navy box) with a diamond
     at confirmation [observed anatomy; his "auto-redraw ... when the deviation
     confirmed"]. Multiple deviations per side permitted; zone extends to the furthest.
   - BREAKOUT CONFIRMED: BREAK_CONFIRM_N consecutive body closes beyond, OR a single
     close beyond by >= BREAK_MARGIN*ATR => range DIES; state = expansion; both dead
     boundaries persist as dashed memory-lines frozen at first later touch [observed];
     control returns to SEED. ("Reaching the next structural level" as a third
     confirmer is [inferred-weak]; NOT implemented in v0, recorded in the contract.)
MIDLINE on confirmed ranges [observed]. STATE ∈ {NEUTRAL, BULL_EXP, BEAR_EXP}.
STATUS LINE, his new confession format [observed]: "N CANDLES · P% RANGE COVERAGE ·
X POTENTIAL · Y CONFIRMED · Z SUPPORTING PIVOTS", coverage = bars inside any confirmed
range (deviation zones count as inside) / total bars.
NOT IN v0 [D-R3b]: internal tracks · measured-move stubs · MTF · alerts · signals.

## PINS — seven, all [VETO], defaults MEASURED in STEP 2, never guessed

LEG_MIN · REV_MIN · TOUCH_EPS · DEV_RETURN_BARS · BREAK_CONFIRM_N · BREAK_MARGIN ·
(ATR_LEN pinned 14, house).

## CALIBRATION TARGETS — quantitative first [observed, his artifacts], geometry second

Q-1 RANGE COVERAGE on our window: 80.6% ± 8pp
Q-2 pivot density: one per 27–30 bars ± 30%
Q-3 confirmed-range density: ~0.75 per 100 bars ± 50% (small-window variance)
Q-4 mean confirmed-range lifetime: 85–110 bars ± 40%
Q-5 >= 1 downside DEVIATION detected at the Jun–Jul 2026 lows region on BTC daily
    [observed: his navy box + checklist "the 60k lows"] with the range surviving it
G-1..G-2 (recent-window geometry, secondary): active-range TOP 83,000±1,500 and LOW
    (post-deviation redraw) 59,300±1,500; midline within 1% of the mean.
