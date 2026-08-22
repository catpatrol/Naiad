
---

# BUILD — SS12-RANGEFINDER v1 · THE OPERATOR'S GRAMMAR

**Lane** ARGUS (drafted) · Executor HEPHAESTUS · Reviewer ARGUS · **Branch** `v12-v1-census` · **Window** `2025-06-28 → 2026-08-21` (420 complete 1D bars — v0 ran 200; KEY-B's L-R1 opens Jul 2025; 2 incomplete days dropped at resample)

**RATIFIED** operator 2026-08-22 — by firing; field-test verdict *"ok, make it better"*; standing leans. Queue: `exchange/queue/2026-08-22_RF2_rangefinder_v1_ARGUS.md`. Lineage: v0 (`BUILD_2026-08-22_RANGEFINDER_V0.md`) preserved; `pine/SS12_RangeFinder_v0.pine` untouched on disk.

## §0 · THE FOUR FIELD DIVERGENCES, EACH NOW A MECHANISM

**C1 · BODY GRAMMAR (default).** Boundaries sit at the defining pivots' BODY extremes; wick territory beyond is deviation-eligible FROM INCEPTION — a terminal-sweep-and-reclaim seed is born WITH its zone (spring-birth). Verified against an independent resample: all five body-mode ranges have `top0/bottom0 == max/min(open,close)` at their defining pivot bars, and inception zones exactly where wick exceeds body. Wick mode reproduces the v0 law bit-for-bit (0 inception events; wick boundaries).
**C2 · PENDING RENDERED.** A breach opens a HOLLOW dashed box that tracks the episode; on return-inside within DEV_RETURN_BARS it HARDENS solid (same box mutated, diamond, boundary redrawn per v0 wick rule); on BREAK_CONFIRM it converts to death. Status line carries "D PENDING".
**C3 · BACKDATING.** On confirmation the left edge extends to the terminal pivot; the log records `born_at` AND `backdated_from` (5/5 confirms in each mode carry exactly one backdate; every `backdated_from` is a logged pivot bar); inception zones classify retroactively at the confirm bar.
**C4/C5 · DIET + COLORS.** Diamonds only at range-confirm + harden; pivot markers a toggle DEFAULT OFF; tiny death triangles; range/deviation/midline colors are INPUTS (defaults tan / orange — the operator's color / orange).

### The operator-chart transcription (KEY-B) vs the machine, body mode

| target | matched | machine box [bottom…top] | residuals (top·bottom) | transcribed deviations |
|---|---|---|---|---|
| L-R1 100,300–124,200 | rid1 (124-bar overlap) | [117,738…119,816]; redrawn [98,889…126,208] | box basis misses; see the finding | top **FOUND@2025-10-07** ext 126,208 (harden — the Oct ATH spike) · bottom **FOUND@2025-10-19** ext 103,470 |
| L-R2 84,600–96,200 | rid3 (61) | [85,094…97,932] redrawn | 1,732 · 494 | top **FOUND@2026-01-18** ext 97,932 · bottom (Dec) **NOT FOUND — the disclosed miss** |
| L-R3 60,800–80,100 | rid5 (77) | [62,868…79,455] redrawn | 645 · 2,068 | bottom **FOUND@2026-02-23** ext 59,800 (inception — the Feb flush) · top **FOUND@2026-04-27** ext 79,455 |
| L-R4 60,100–67,400 | rid8 (63) | [61,022…66,286] box | 1,114 · 922 — both within ±1,500 | bottom **FOUND@2026-07-02** ext 57,759 (harden) · **resolved by the upside BREAKOUT** (top-death 2026-08-20, per the transcription) |

**4/4 ranges matched · 6/7 transcribed deviations found** (evidence pointers anchor-matched to the transcription's own dates after the review caught a first-hit matcher crediting October's spike to a July event).

### THE FINDING — the redraw basis names RF-3

The operator's transcribed boundaries sit BETWEEN the machine's seed box and its wick-redrawn extent. Measured with a REDRAW_BASIS diagnostic (never the default; the queue's wick law ships): **body-basis redraws lift boundary concordance 4/8 → 6/8** (L-R1 top residual 2,008 → 429; L-R4 both boundaries in-tol) at 2.4 coverage points. **The operator's grammar appears to redraw to the breach cluster's BODY edge, not the wick extreme** — C2 pinned "per v0 rules", so the divergence is FILED as the finding, not silently enacted. RF-3's first question is named.

### THE C1 SPLIT — deviations are not all springs

Under body grammar, bottom hardens split: **6/8 sweep the 20-bar wick extreme** (house springs) and **2/8 are body-only breaches** (2025-07-22's shallow breach; 2025-10-19's post-flush retest that could not undercut the flush's own low). Reported both directions (6/25 independent springs fall inside deviation episodes). The reclaim-close invariant holds 8/8 — relabelled definitional after the review named the sweep half tautological.

## §1 · CALIBRATION — KEY-A OBJECTIVE, BODY MODE

Coarse 5,120 + fine, deterministic edge-avoiding tie-break. **Chosen pins** (F-RF-5 pins the pine defaults to these exactly, plus `BOUNDARY_MODE=body`): `LEG_MIN 0.5 · REV_MIN 1.75 · TOUCH_EPS 0.60 · DEV_RETURN_BARS 7 · BREAK_CONFIRM_N 8 · BREAK_MARGIN 1.5` — TOUCH_EPS and BREAK_CONFIRM_N sit at grid edges, disclosed. **Score 3.5507** (v0's record: 10.7601):

| KEY-A target | value | band | verdict |
|---|---:|---|---|
| Q-1 coverage | 71.19% | [72.6, 88.6] | near-miss (viol 0.18) |
| Q-2 bars/pivot | 7.78 | [19.95, 37.05] | **RESISTS** (viol 1.42) — the pivot cadence remains the named suspect |
| Q-3 confirmed/100 bars | 1.19 | [0.38, 1.12] | near-miss (viol 0.17) |
| Q-4 mean lifetime | 68.2 | [51, 154] | **SATISFIED** |

Wick mode at the same pins: 64.05% coverage, 5 chapters — filed beside body in the export. **LATE-RETURN disclosure**: at these pins the breach-lapse state is unreachable (N ≤ DEV+1); the law stays implemented and F-RF-3 exercises it off-defaults.

## §2 · FIXTURES — 8/8 GREEN, EVERY BREAK LEG RED FIRST

Transcript: `research_outputs/rangefinder/FIXTURES_v1.txt`. F-RF-1 determinism (152-event byte identity) · F-RF-2 KEY-A record as HARD-CODED literals, break = REV_MIN×3 drifts all four · F-RF-3 lifecycle legality + harden/backdate laws + the LAPSE path off-defaults; break plants a solid-without-harden AND a die-without-breach, both caught by name · F-RF-4 kinship: reclaim invariant 8/8, spring statistic 6/8 both directions · **F-RF-7 OPERATOR CONCORDANCE** (break = wick mode fails the bar: 4/6 devs, 0 inception events — the body grammar is load-bearing, by a one-event margin on this tape, stated) · F-RF-5 pine parity incl. mode · F-RF-6 structure (8 clauses) · **F-RF-8 PINE-SIM PARITY (new)** — a maintained python port of the pine bar loop must reproduce the twin's chapters EXACTLY in both modes; it does (body 5/71.19%/54, wick 5/64.05%/54); break = doubled REV_MIN diverges.

## §3 · THE REVIEW — WHICH RAN IN FRONT OF THE PUBLISH

Three adversarial lenses in read-only worktrees. **A second consecutive Pine BLOCKER caught pre-publish**: the v1 seed law diverged from the twin (floor bar-guards + na-defaulting terminal tests + per-bar churn — a whole chapter missing from the render in body mode, a phantom box in wick mode). The lens VALIDATED its own three-part repair; applied, the pine sim reproduces the twin exactly — and that port is now **F-RF-8**, a standing fixture, because F-RF-1..7 never execute the pine machine and text checks cannot see a dead render path (the v0 lesson, now law). Also repaired from the lenses: F-RF-3's between-clause had gone INERT on the harden rename (an evidence-free planted death passed; caught by a plant test); the dead `showPivots` input now renders; the memory-line freeze respects "first LATER touch" (death-bar guard); KEY-B's evidence pointers anchor-matched; the lapse-unreachability disclosed; the F-RF-4 tautology named and relabelled; stale v0 banners/window lines fixed. One reviewer note carried: TradingView's `ta.atr` seeds by SMA vs the engine's first-value RMA — warm-up-class only (one confirm bar shifts 18→19), disclosed in the pine header.

## §4 · FINDINGS — REPORTED, NOT FIXED

**RF-c1 · Q-2 RESISTS in both grammars** — the ZigZag reads ~7.8 bars/pivot where the reference claims 27–30; carried from v0, still the seed/pivot-law suspect.
**RF-c2 · THE REDRAW-BASIS DIVERGENCE** (§0) — RF-3's named question; the wick law ships per the queue.
**RF-c3 · L-R2's Dec bottom deviation NOT FOUND** — the machine's rid3 never breached its bottom in December (the Dec low sat inside the body boundary); either a feed divergence (spot vs perp) or the reference's boundary sat higher; unreconcilable from transcription alone.
**RF-c4 · spot-vs-perp** — KEY-B transcribed from BTCUSDT.P; our tape is BTCUSDT spot; inside ±1,500 mostly, disclosed throughout.
**RF-c5 · the pine remains a single-candidate machine** (disclosed since v0); "X POTENTIAL" caps at 1 and "D PENDING" at 0/1; the twin is the machine of record; **operator TV-eyeball PENDING — the final fixture.**

## §5 · DISPOSITION + BOX-COST

| PATH | EXISTS | TRACKED | PROTECTED BY | BOX COST |
|---|---|---|---|---|
| `scripts/rangefinder_twin.py` (v1) · `scripts/rangefinder_fixtures.py` (v1) · `scripts/rangefinder_pine_sim.py` (new) | yes | hand commit this session | CL-13 explicit paths | 0 B, non-box |
| `pine/SS12_RangeFinder_v1.pine` (new) · `pine/SS12_RangeFinder_v0.pine` (untouched) | yes | hand commit / already committed | same | 0 B, non-box |
| `research_outputs/rangefinder/BTCUSD_1d_ranges_v1.json` (63,586 B, sha256 `1016effc68849b520f0a5a83e64f40e14e3394b541b3b063f357f08dc3a08bae`) + `FIXTURES_v1.txt` | yes | no — gitignored (rangefinder/** since RF-1) | local only, OFF-BUS | n/a |
| `exchange/queue/2026-08-22_RF2_rangefinder_v1_ARGUS.md` | yes | publish | publish guard | 2,642 B |
| `exchange/reports/BUILD_2026-08-22_RANGEFINDER_V1.md` | yes | publish | same | ≈ 10,400 B |
| `exchange/status/LEDGER_ARGUS.md` | yes | publish, append-only | same | +≈ 2,900 B |

### BOX-COST — constants read LIVE from `publish_exchange`

| | before | after |
|---|---:|---:|
| `exchange/**` | 2,420,799 B · 15.13% | ≈ 2,436,500 B · 15.23% |
| **tick set** — governs | 2,680,097 B · 16.75% | ≈ 2,695,800 B · 16.85% |
| level | OK (warn 40% / refuse 70%) | OK |

This paste ≈ 10,400 B ≈ 0.07% of the box; the 64,000 B trip-wire does not fire.

---

*End of build document. SS12-RangeFinder v1 · the operator's grammar, body default · KEY-B concordance 4/4 ranges, 6/7 deviations, anchor-honest pointers · the redraw-basis divergence FILED and RF-3 named · the C1 split quantified (6/8 springs, 2/8 body-only) · 8/8 fixtures incl. the new pine-sim parity law · a second Pine BLOCKER caught by the pre-publish review and repaired with the lens's own validated recipe · operator TV-eyeball PENDING.*
