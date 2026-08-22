
---

# BUILD — SS12-RANGEFINDER v0 · RANGE LIFECYCLE WITH DEVIATIONS

**Lane** ARGUS (drafted) · Executor HEPHAESTUS · Reviewer ARGUS · **Branch** `v12-v1-census` · **AS OF** window `2026-02-03 → 2026-08-21` (200 complete 1D bars; 2 incomplete days dropped at resample)

**RATIFIED** operator 2026-08-22 — by firing; rulings D-R1a/D-R2a/D-R3b/D-R4 + the name "SS12-RangeFinder". **SOURCE**: public artifacts of a closed-source system (@sergio_tesla_, 2026-08-10 post + two screenshots) — **reconstruction, not code access**. Display-only; renders-never-rules; hypotheses route to APOLLO under G-7. Queue: `exchange/queue/2026-08-22_RF1_rangefinder_ARGUS.md` (v2, filed fresh — no prior RF1 existed; the fresh-file path).

## §0 · WHAT SHIPPED, AND THE ONE CORRECTION THAT DEFINES v2

**The deviation lifecycle is the correction** (his checklist, verbatim law): a body close beyond a CONFIRMED boundary opens a **PENDING breach — the range does NOT die yet**. Within DEV_RETURN_BARS a body close back inside makes a **CONFIRMED DEVIATION**: the range **survives and is redrawn** to the breach extreme, the slab rendering as a navy deviation zone. Only BREAK_CONFIRM_N consecutive closes beyond, or one close beyond by BREAK_MARGIN×ATR, kills it.

**And our tape contains his anatomy.** The twin's range #5 (confirmed 2026-06-24, {59,080 … 67,255.4}) breaches down 06-30, **deviation-confirms 07-01 at 57,758.6 with a redraw** — the navy box at the "60k lows", exactly the checklist's exhibit — survives 50 more bars, then dies UPWARD into the August rally (margin kill 08-20) with its memory-line first-touched 08-21. Q-5 SATISFIED.

## §1 · THE EVIDENCE REGISTER, RULE BY RULE

| rule | class |
|---|---|
| ATR-ZigZag pivots at wick extremes; alternate by construction | [observed] via D-R2a |
| leg-merge law (short legs do not confirm a pivot; leg keeps extending) | [inferred] — pinned in the twin header |
| SEED = expansion-terminal P0 + first counter-pivot P1; {top,bottom} at wick extremes | [observed structure; the FORWARD reading of "fails to exceed" = pre-confirmation invalidation is [inferred], pinned] |
| CONFIRM on first traverse to the opposite boundary within TOUCH_EPS×ATR; diamond at the touched boundary's bar | [observed] |
| BREACH→PENDING; deviation survives+redraws; navy zone; multiple per side, zone to furthest | [observed anatomy + his "auto-redraw … when the deviation confirmed"] |
| breakout by N consecutive closes OR margin; dashed memory-lines frozen at first later touch; control to SEED | [observed] ("next structural level" as a third confirmer: [inferred-weak], NOT in v0, recorded) |
| ONE ACTIVE RANGE, seeding paused while alive | [inferred] — calibration ARBITRATED between this and multi-active; one-active won |
| LATE RETURN (inside again after DEV_RETURN_BARS, no breakout) = breach-lapse, survives, NO redraw | [inferred] — pinned |
| midline; status line "N CANDLES · P% RANGE COVERAGE · X POTENTIAL · Y CONFIRMED · Z SUPPORTING PIVOTS"; POTENTIAL a stock | [observed format; live coverage evaluation [inferred]] |
| NOT IN v0 [D-R3b]: internal tracks · measured-move stubs · MTF · alerts · signals | ruling |

## §2 · CALIBRATION — MEASURED, AND THE RESISTANCE NAMED, NOT FORCED

Grid: coarse 10,240 cells (six free pins × the one-vs-multi ACTIVE reading) + fine pass; deterministic edge-avoiding tie-break. **Chosen set (score 10.7601):**

`LEG_MIN 0.5 · REV_MIN 1.75 · TOUCH_EPS 0.30 · DEV_RETURN_BARS 4 · BREAK_CONFIRM_N 6 · BREAK_MARGIN 1.5 · ONE_ACTIVE · (ATR_LEN 14, house, never swept)`

| target | value | band | verdict |
|---|---:|---|---|
| Q-1 coverage | 60.0% | [72.6, 88.6] | **RESISTS** (viol 1.58) |
| Q-2 bars/pivot | 9.09 | [19.95, 37.05] | **RESISTS** (viol 1.27) |
| Q-3 confirmed/100 bars | 1.50 | [0.38, 1.12] | **RESISTS** (viol 1.00) |
| Q-4 mean lifetime (bars) | 45.7 | [51, 154] | near-miss (viol 0.10; censored lifetimes excluded, disclosed) |
| Q-5 Jun–Jul downside deviation, survived | **TRUE** | binary | **SATISFIED** |
| G-1 last-range top | 67,255.4 | 83,000±1,500 | see below |
| G-2 low (post-deviation redraw) | 57,758.6 | 59,300±1,500 | misses the floor by 41 pts (viol 0.03) |

**Which rule the resistance names** (the commission's own protocol — report, do not force): Q-1/Q-2 pull opposite ways under the pinned SEED law — coverage wants dense pivots, cadence wants sparse — because **potentials INVALIDATE in trends before they can confirm**, so ranges seed one leg tall and small. The reference's giant active range (top 83k = a February-class high) cannot arise under this seed law inside a 200-day window, which also explains G-1: **his active range predates any window that starts in February**; his 20-CONFIRMED status line is a longer chart's count. The suspect is the seed/invalidate reading, recorded for RF-2; the top-3 sets and the full scoreboard print in the twin's `--calibrate` run. The multi-active reading was built, swept, and **lost** — the arbitration is in the grid, not in taste.

## §3 · FIXTURES — 6/6 GREEN, EVERY BREAK LEG RED FIRST

Transcript filed at `research_outputs/rangefinder/FIXTURES.txt`. The prove() law: the break leg runs FIRST and must go red or the fixture is void.

- **F-RF-1 DETERMINISM** — identical input → byte-identical 57-event log; break: one perturbed bar changes the log (the equality has teeth).
- **F-RF-2 TARGETS** — Q5 satisfied AND residuals equal the exported calibration-of-record (the DISCLOSED subset); break: REV_MIN×3 loses Q5, pivots collapse to 2.
- **F-RF-3 LIFECYCLE LEGALITY** — seeds 5 = confirmed 3 + invalidated 0 + superseded 2 + unresolved 0 (the stock conserves); every deviation carries breach + in-window return + same-bar redraw; every die carries its N-closes or margin; ≤1 memory-touch per side; break: a planted redraw-without-deviation is caught by name.
- **F-RF-4 SPRING KINSHIP** — **1/1 twin bottom-deviations satisfy the house spring shape** (sweep below the pre-breach 20-bar extreme, body-close back above — computed independently from raw bars); **1/7 independent springs fall inside a deviation episode** (the six others fire outside range life — the discriminating fact for P-SPR-1 sharpening). Break: corrupting the return-close rule drops the match to 0/1.
- **F-RF-5 PINE/TWIN PARITY** — all six pine input defaults EXACTLY equal the calibrated pins; break: a corrupted default is caught with both values printed.
- **F-RF-6 PINE STRUCTURE** — v6 · titled "SS12-RangeFinder v0" · max_boxes/lines/labels 500 · six [VETO] tooltips with evidence classes · display-only reconstruction header crediting the source · no request.security / alertcondition / signal plots; break: version corruption caught.

## §4 · FINDINGS — REPORTED, NOT FIXED

**RF-a · Q-1/Q-2/Q-3 RESIST and the seed law is the named suspect** — RF-2 material, not a v0 force.
**RF-b · THE PINE CARRIES A DISCLOSED, MEASURED SIMPLIFICATION**: a SINGLE candidate potential where the twin holds a candidate list (the terminal test itself now reads pivot extremes, twin-law). Simulated bar-for-bar on the calibration tape: pivots 22 == twin, confirms 3 == twin, the Q-5 chapter IDENTICAL (confirm 06-24 → bottom deviation 07-01 → margin death 08-20), coverage 34.0% vs the twin's 60.0% — the single slot occupies itself with candidates the twin supersedes, and the first two chapters diverge. F-RF-5/6 pin defaults and structure, not runtime parity — **the operator TV-eyeball is the parity fixture and it is PENDING** (the ledger carries it).
**RF-c · G-2 misses its band floor by 41 points** — our Binance wick prints 57,758.6 where the reference (unknown feed) reports a 59,300-class redraw; feed divergence or a shallower reference deviation; not reconcilable from public artifacts.
**RF-d · coverage's live-evaluation reading** (a pending-breach bar counts uncovered until the deviation confirms) is one of two defensible readings; retroactive evaluation would raise Q-1 a few points. Pinned, disclosed, not tuned.

## §4b · THE REVIEW — WHICH RAN IN FRONT OF THE PUBLISH

Three adversarial lenses in read-only worktrees. **Two Pine BLOCKERs found and repaired before anything shipped**: the seed path was DEAD (`prevPivPx` never assigned on the live branches — a lens-built bar-loop simulator proved the indicator as first written rendered NOTHING, 0 seeds on a tape where the twin makes 5) and `newPivot()` mutated a global from inside a function (compile-fatal in every Pine version). Also repaired: the memory-line freeze law (was extend-forever), the seed terminal test (bar extremes → pivot extremes, twin-law), ZigZag warm-up parity (22 pivots now == twin), F-RF-3's die legality (an evidence-free planted death PASSED the first draft — now caught by name, with the break leg planting one), F-RF-2's self-comparison (residuals now hard-coded literals of record), the Q-4 band mis-encoding ([51,144] → the queue's [51,154]) and censored-lifetime bias (excluded, disclosed; chosen set UNCHANGED, re-swept), one side-vocabulary split in the export ("bot"/"bottom"), non-strict JSON (NaN), the non-chronological event log (pivots now carry `knowable_at`, log sorted), the same-bar confirm/invalidate tie (pinned: the close outranks the wick), and the box-cost after-arithmetic double-counting the already-committed queue file. The status-line's full-history-vs-200-bar window mismatch is now disclosed in the Pine itself.

## §5 · DISPOSITION + BOX-COST

| PATH | EXISTS | TRACKED | PROTECTED BY | BOX COST |
|---|---|---|---|---|
| `scripts/rangefinder_twin.py` | yes | hand commit this session | CL-13 explicit paths | 0 B, non-box |
| `scripts/rangefinder_fixtures.py` | yes | same | same | 0 B, non-box |
| `pine/SS12_RangeFinder_v0.pine` | yes | same | same | 0 B, non-box |
| `research_outputs/rangefinder/` (json 11,905 B sha256 `fd1fca889d06ad1fd1315755ab2e0586c25605352b8c58cbdb0657eb06ab2a22` + FIXTURES.txt) | yes | no — gitignore line added THIS session (the tc9 lesson applied at birth) | local only, OFF-BUS | n/a |
| `exchange/queue/2026-08-22_RF1_rangefinder_ARGUS.md` | yes | publish | publish guard | 3,539 B |
| `exchange/reports/NOTE_ARGUS_to_APOLLO_2026-08-22_P-RNG_slate.md` | yes | publish | same | 1,312 B |
| `exchange/reports/BUILD_2026-08-22_RANGEFINDER_V0.md` | yes | publish | same | ≈ 11,600 B |
| `exchange/status/LEDGER_ARGUS.md` | yes | publish, append-only | same | +≈ 3,300 B |

### BOX-COST — constants read LIVE from `publish_exchange`

| | before | after |
|---|---:|---:|
| `exchange/**` | 2,400,258 B · 15.00% (the queue file already committed inside this figure — review-caught double-count removed) | ≈ 2,416,600 B · 15.10% |
| **tick set** — governs | 2,659,556 B · 16.62% | ≈ 2,675,900 B · 16.72% |
| level | OK (warn 40% / refuse 70%) | OK — the other lane's rotation moved ~1.1 MB to docs/history between builds |

This paste ≈ 11,600 B ≈ 0.07% of the box. The 64,000 B naming trip-wire does not fire for any file this build ships.

---

*End of build document. SS12-RangeFinder v0 · the deviation lifecycle correction, found on our own tape at the 60k lows · pins MEASURED, resistance NAMED (the seed law), never forced · 6/6 fixtures with red-first break legs · deviation≈spring kinship 1/1 and 1/7 · display-only, renders-never-rules · operator TV-eyeball parity PENDING · two Pine BLOCKERs caught by the pre-publish review, repaired in place.*
