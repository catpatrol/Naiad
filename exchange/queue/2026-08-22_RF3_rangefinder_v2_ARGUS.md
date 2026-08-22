# QUEUE RF-3 — SS12-RANGEFINDER v2 · HIERARCHY + FLIPS + THE LEASH

RATIFIED: operator, 2026-08-22 — by firing; field verdict "improving but not quite
there"; operator diagnoses of record: micro-only detection misses macro balances;
grey-arrow flips wanted; dashed-line clutter leashed. Executor HEPHAESTUS, reviewer
ARGUS. Display-only; renders-never-rules. BUILT: PENDING

## CHANGES vs v1

H1 TWO-SCALE HIERARCHY: the identical state machine runs twice —
   MACRO: pins scaled by SCALE_MULT [VETO, calibrate ~2.5–4.0] on LEG_MIN and
   REV_MIN; renders as the primary boxes (operator-blue by default).
   MICRO: v1 pins unchanged; renders dimmed/thin, only while INSIDE a live macro
   range; micro toggle default ON but subordinate.
   CONTAINMENT LAW: micro events never flip global state and never emit macro
   memory-lines; a micro breakout that leaves the live macro is not a micro event at
   all — it is macro business (breach/pending on the macro boundary).
H2 FLIP MARKERS on memory-lines (macro corpses only): first retest approached from
   the side OPPOSITE the boundary's birth side that HOLDS (no body close through by
   FLIP_HOLD_MARGIN*ATR within FLIP_HOLD_BARS [both VETO]) => print ▲ (dead top now
   support) or ▼ (dead bottom now resistance) at the touch bar, tooltip carrying
   pedigree: parent range, death date, retest date. A retest that fails through is a
   memory-touch (line freezes, no flip mark), as before.
H3 THE LEASH: inputs — showMemory (default ON, MACRO ONLY; micro corpses leave no
   lines) · MEM_TTL_BARS [VETO, propose 400] after which an untouched line fades ·
   per-side live cap 6 (oldest culled) · showMidline toggle · pending-box borders
   dashed-orange, distinct from memory-grey.
H4 LEGEND: toggleable mini-table (bottom-right) with one row per glyph: box/hollow/
   slab/◆/midline/dashed/▲▼ flip/state triangles. Plain text, tiny.
H5 SYMBOL SANITY unchanged from v1's diet; confirm diamonds remain the only
   diamonds.

## CALIBRATION — micro pins FROZEN at v1's ruled values (read them from
pine/SS12_RangeFinder_v1.pine inputs; do not refit). Fit ONLY: SCALE_MULT,
FLIP_HOLD_MARGIN, FLIP_HOLD_BARS, MEM_TTL_BARS against:
KEY-C (operator 4h concordance, BTCUSDT.P 4h, transcription-grade ±1,200 USD ±8 bars):
  C-R1 MACRO range Feb–May: TOP 75,000 · BOTTOM 59,900 · midline ≈ 66,500 ·
       dev BOTTOM 57,900–62,000 (Feb flush) · dev TOP 75,000–78,500 (Apr, small)
  C-R2 MACRO range Jun–Aug: TOP 67,300 · BOTTOM 59,900 · dev BOTTOM 57,600–60,300
       (Jul) · resolved by the current upside breakout
  C-R3 Jan shelf visible-left: BOTTOM ≈ 84,500 with dev TOP ≈ 95,000–97,500
  C-F1 FLIP resistance at 84,500±1,500, February (the operator's large grey arrow)
  C-F2 FLIP support at 75,000±1,200, May, at least one of the two operator-marked
       touches detected
  C-Q1 macro count in the Feb–Aug window: 2–4 (not 10) · micro ranges permitted
       inside, dimmed
If any KEY-C row cannot be met, print the residual and name the resisting rule —
report, never force.
