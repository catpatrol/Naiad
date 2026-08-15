# CENSUS-2A · PROBE LEDGER
**Append-only.** Opened 2026-08-12 by HEPHAESTUS under the law of
`CENSUS2A_CLOSEOUT_2026-08-12.md` §5. Corrections are NEW superseding entries; nothing above the
last line is ever edited.

**THE LAW THIS LEDGER SERVES (close-out §5, restated):** *exploration is unlimited; belief is
rationed.* Every probe on the cached parquets runs freely and prints whatever it likes, stamped
**`EXPLORATION — ungated; promotion requires registration`**. No probe result may be cited as a
finding. Every probe is logged here — **question · tables touched · selection surface m · what
looked interesting**. The guard doesn't forbid looking; it prices remembering. Promotion to
TIER-P is by ceremony only: registration with named statistic + prior → scored on data not used
to find it → FDR family declared → witness-correlation printed → TRG or tail-exit-ratio beside
it. **The running sum of m in this ledger is the selection surface FDR charges.**

**HOW TO READ `m`.** `m` counts comparisons whose outcome could have influenced what was kept —
thresholds swept, arms ranked, cells picked because they looked good. Extraction, description,
and display are `m = 0`: no comparison is promoted, so nothing is charged. A probe that sorts a
table to *look* at it is m = 0; a probe that sorts a table and *keeps the top row* is not.

| # | date | probe | tables touched | m | what looked interesting |
|---|------|-------|----------------|---|-------------------------|
| 1 | 2026-08-12 | VIZ-1 extraction — nine payloads | cen3_ledger_lensed · cen3_arm_windows · cen1_ribbon · cen2_refusals · cen5_campaigns · cen6_episodes · cen7_registry_series · cen8_anchor_grid · cen9_cards | **0** | Nothing promoted. Nine display payloads extracted for the design brief; no comparison scored, no arm ranked, no threshold swept. Rows: v1 848 · v2 34 · v3 605 · v4 2,596 · v5 4,500 · v6 4,000 · v7 8 · v8 705 · v9 6,729. |
| 2 | 2026-08-12 | CENSUS-2B / V-ULT-1 first look — event density, the equivalence card, V-ULT occupancy, the enquiry card | census2b `emas` · `ribbons` · `crosses` (35 cells) · cen4_book (cell\|tranche_id) dup=0 · cen5_campaigns (tranche_id) dup=0 | **0** | Nothing promoted. Every table is a complete partition printed whole; no threshold swept, no arm ranked and kept, no row dropped on the strength of its value. Rows: 5a 2,176 · 5b 108+324 · 5c 30 · 5d1 270 · 5d2 10,684 · 5d3 6,571. |
| 3 | 2026-08-14 | CENSUS-2B Part A (A-0..A-4) + W-TB1 Tail Biography — completion audit, i-a refusals, armed-window ledger v2, knot/fan transitions, spring/upthrust stream, and the ±72h biography of the 12.3% tail vs a 1:1 matched control | census2b `refusals` · `windows` · `transitions` · `springs` · `wtb1/{state,tape}` (40 F-KEY assertions, dup=0 on every one) · cen5_campaigns (tranche_id) dup=0 · cen6_verdict_state · _reviewer_box/wf1 (ts_close) | **743,516** | Nothing promoted. m is entirely W-B's motif surface — every k-gram k≤4 over the full BRIDGE alphabet in all three SEQ frames; A-0..A-4, W-A, W-C, W-D, W-E are complete partitions or extractions at m = 0. The I11 guard returns a clean null in all three frames (obs max 0.08477 < null p95 0.08722). Rows: A-1 275,712 · A-2 103,153 · A-3 262,086+318,427 · A-4 227,268 · W-TB1 state 2,640,691 · tape 2,488,744 · cohort 1,628. |

---

### ENTRY 1 · VIZ-1 extraction — nine payloads, selection surface m = 0
**Date:** 2026-08-12 · **Class:** DISPLAY-ONLY / Tier-E · **By:** HEPHAESTUS
**Question:** *What do the census's own instants look like, drawn?* — specifically the nine views
of `DESIGN_BRIEF_CENSUS2A_VIZ_2026-08-12.md` §3, each carrying one money question toward the two
sentences the estate is actually trying to finish: "the system enters when ___" and "the system
exits when ___."

**Tables touched (declared keys, F-KEY asserted on every join):**
`cen3_ledger_lensed` (asset, arming_ts) dup=0 · `cen3_arm_windows` · `cen1_ribbon` ·
`cen2_refusals` · `cen5_campaigns` (tranche_id) dup=0 · `cen6_episodes` ·
`cen7_registry_series` (asset, ts) dup=0 · `cen8_anchor_grid` · `cen9_cards`.

**Selection surface m = 0.** No comparison was promoted. Sorting in V6 (by MFE) and V7 (by
median) is display ordering over a *fixed, complete* set of rows — no row was kept or dropped on
the strength of its value, and no threshold was swept. The v6 top-4000 cap is a byte-budget
truncation of a view whose declared subject IS the upper tail, recorded in the payload's
`downsample_rule`; it selects for *drawability*, not for outcome favourability, and it is
disclosed rather than silent.

**What looked interesting — recorded, NOT claimed:**
- The toll band is wide enough, drawn to scale, that a visible share of every outcome axis sits
  inside it. This is the census's own arithmetic made visual; it is not a new result.
- V7's anchor rows put the EMA clock's whole p30–p70 box against the same axis as the alternative
  anchors. What that box's position means is a Tier-P question and is not answered here.
- V9's mean hysteresis run length prints beside a stated memoryless reference of 1.0. It is
  printed, not tested.

**Provenance:** payload shas in `D:/Naiad/research_outputs/census2a/viz_payloads/*.json` `meta`
blocks; renders in `.../viz/`; both listed in `BUILD_2026-08-12_CENSUS2A_VIZ1.md`.
**Stamp:** `EXPLORATION — ungated; promotion requires registration.`

---

### ENTRY 2 · CENSUS-2B / V-ULT-1 first look, selection surface m = 0
**Date:** 2026-08-12 · **Class:** DISPLAY-ONLY / Tier-E · **By:** HEPHAESTUS
**Question:** *Does the fast ribbon behave differently depending on what the ultra-long ribbons
are doing?* — the operator's "secret sauce is a momentum system" paste, made descriptive. Plus
three supporting looks: where each of the six ribbons even moves (event density), what an EMA
length means as a duration rather than a number (the equivalence card), and what VH and UH spend
their time doing (occupancy).

**Tables touched (declared keys, F-KEY asserted on every join):**
`census2b/emas/{asset}/{tf}` · `census2b/ribbons/{asset}/{tf}` · `census2b/crosses/{asset}/{tf}`
(35 cells, F-KEY `(asset, tf, pair_class, pair, event, dir, ts_ms)` dup=0 on every one) ·
`cen4_book` keyed `cell|tranche_id` dup=0 · `cen5_campaigns` keyed `tranche_id` dup=0 and
`(asset, ts_ms, mandate)` dup=0.

**Selection surface m = 0.** No comparison was promoted. Every stratification in §5 is a
*complete partition of a fixed population*, printed whole: all three VH+UH orientation strata,
all three FAST pairs, both timeframes, all six families, all six states × orientations. No
threshold was swept — every constant is VETO-pinned by the contract and none was tuned here. No
row was kept or dropped on the strength of its value. The winners/losers split in 5(d)(iii) uses
census-2A's **own** `outcome_sign` label, imported whole, not a cut invented here. The one
exclusion — 72 campaigns whose entry predates VH's warm-up on 5m — is forced by the warm-up law,
is 1.1 % of the book, and is printed rather than silent.

**What looked interesting — recorded, NOT claimed:**
- Conditioning FAST-ribbon crosses on VH+UH orientation moved the terminal-H100 distribution
  *not at all* that a reader could see: across all 18 strata (3 pairs × 3 orientations × 2 tfs),
  every median sits **inside** the measured toll band and `%>0` stays within 47.9–50.1 %. This is
  a description of one measurement, on one ruler, at one horizon. It is not a result about the
  operator's system, and it registers nothing.
- `UH` returns `flat` for 95.1 % of warm bars against `VH`'s 23.4 %. That is a fact about a
  20-bar window applied to lines spanning 1.18× in length, not a fact about the tape.
- 66–68 % of VH knot episodes "expand" on the very next bar, against 2.5–5.2 % for UH. The knot
  and expansion definitions are near-tautological at VH scale and are not at UH scale.
- The toll in ATR units is ~0.29–0.35 on 5m against census-2A's 0.026–0.059 on 4h. Any LTF table
  that quotes the 4h toll understates its own cost by roughly an order of magnitude.

**Provenance:** `D:/Naiad/research_outputs/census2b/firstlook/*.parquet` with
`firstlook/TIER_E.json` carrying the class header and the m-accounting note; shas in
`census2b_manifest.json`; full transcript in `BUILD_2026-08-12_CENSUS2B_VULT1.md` §6.
**Stamp:** `EXPLORATION — ungated; promotion requires registration.`


---

### ENTRY 3 · CENSUS-2B Part A (A-0..A-4) + W-TB1 Tail Biography, selection surface m = 743,516
**Date:** 2026-08-14 · **Class:** DISPLAY-ONLY / Tier-E · **By:** HEPHAESTUS
**Question:** *Who are the winners, and what did they have for brunch?* — the 12.3% tail of the
resolved book (814 campaigns, gross_R > 0) photographed for ±72h around birth against an exactly
matched 1:1 loser control, on four lenses, with the full census-2B event grammar as a tape. Plus the
sequential substrate the biography reads from: an i-a refusal stream on the pared pairs, an armed-
window ledger v2 on 12_89/12_26, a knot/fan transition ledger, and a spring/upthrust event stream.
And, first, the completion audit that certifies what census-2B actually contains.

**Tables touched (declared keys, F-KEY asserted on every table and every join):**
`census2b/{emas,ribbons,crosses}/{asset}/{tf}` (read-only) · `census2b/refusals/{asset}/{tf}` ·
`census2b/windows/{asset}/{tf}` keyed `(asset, tf, dir, arming_ts_ms)` dup=0 ·
`census2b/transitions/{asset}/{tf}_{knots,fans}` · `census2b/springs/{asset}/{tf}` ·
`census2b/wtb1/state/{asset}/{tf}` keyed `(ckey, lens, ts_ms)` dup=0 ·
`census2b/wtb1/tape/{asset}/{tf}` keyed `(ckey, lens, ts_ms, src_ts_ms, kind, token)` dup=0 —
**40 F-KEY assertions across the capture, 0 duplicates** · `cen5_campaigns` keyed `tranche_id` dup=0 ·
`_reviewer_box/wf1/*USDT_*.json` for `ts_close`/`hold_s` (the exit timestamp census-2A computed and
did not persist) · `cen6_verdict_state` keyed `(asset, member, ts)`.

**Selection surface m = 743,516, and all of it is W-B.** A-0 through A-4, W-A, W-C, W-D and W-E are
**m = 0**: every one is an extraction or a complete partition of a fixed population, printed whole.
No threshold was swept — every constant is VETO-pinned by the contract and none was tuned here, and
where a pinned constant turned out to be inert or vacuous (the kiss grammar on slow pairs; RIBBON_C
on the BR) it was **measured and reported, not adjusted**. No arm was ranked and kept. No row was
dropped on the strength of its value. W-E sorts the winner cohort by `gross_R` and prints the top 20
to *look* at them, which the law of this ledger prices at 0.

**W-B is charged the whole surface: 743,516.** It enumerates every ordered event k-gram with k ≤ 4
over the full BRIDGE alphabet in all three ratified SEQ frames, in the 24h before birth — 288,857
distinct motifs in `absolute`, 262,219 in `gov_relative`, 192,440 in `tier`. Under this ledger's own
rule the probe could have been charged 0, since nothing is kept; the contract charges the full count
instead, because the motif table is what a future registration would be drawn **from**. The
conservative number is the one recorded. Note for whoever charges FDR against it: 743,516 counts
*(frame, motif)* pairs, and the three frames are three spellings of one event sequence, so a case can
be made for 288,857. That question is filed, not answered.

**What looked interesting — recorded, NOT claimed:**
- The I11 max-statistic guard returns a **clean null in all three frames**. The largest
  winners-vs-control gap any of 7,113 usable motifs achieves (0.08477, `absolute`) sits **below** the
  gap the largest-of-7,113 reaches on permuted labels (null p95 = 0.08722). `admissible = False`
  everywhere — and, per F-25 of the build document, could not have been True at 2,000 permutations
  regardless, because the BH bar q/m ≈ 4×10⁻⁷ is 1,239× below the p-value floor of 1/2001.
- A-2's headline is negative where it is curtain-clean. The arming-anchored fate split (+1.82 ATR
  TRIGGERED vs −1.22 ABORTED at H100 on 5m) is **circular** — fate is decided inside the window. The
  trigger-anchored median, the only anchor a decision could act on, is negative at both horizons on
  5m/15m/30m under **both** trigger readings, against a 0.28 ATR toll.
- W-D's 7× headline is exposure. "27.1% of winners vs 3.8% of controls show a long-EMA loss→reclaim"
  becomes 0.374 vs 0.305 per 100 **open** hours and reverses on e2618/e4618; median hold is 112.4h
  against 2.2h. In the ≥24h duration-matched band the controls are higher.
- The largest single split in the study: winners are born **fan-complete on FAST** 60.8% vs 51.6%
  (in-knot 38.6% vs 47.3%) on the 1h lens. Every other SR is inside 4.2 points. Read against the
  guard's demonstration that 8.7-point gaps arise here from label noise alone.
- Two pinned constants are measurably out of scale, in new places: the kiss grammar is **inert** on
  five of eleven pared pairs (max reach within k=10 bars, over the whole panel history, is below
  δ=0.75 — the event is impossible, not rare), and `RIBBON_C = 0.5 ATR` makes `br_knot` false for all
  1,628 campaigns on all four lenses because BR width is 15–24 ATR. Neither constant was changed.
- The census-2B completion certificate: 157 cells probed, **100 PRESENT and sha-verified, 0 STALE**,
  the panel complete across {5m,15m,30m,1h,4h,12h}. 1m DEFERRED, named; annex never built, named.

**Provenance:** `D:/Naiad/research_outputs/census2b/{refusals,windows,transitions,springs,wtb1}/`
and `cen2b_completion_audit.parquet`, all sha-pinned in `census2b_manifest.json` (260 artifacts,
2.22 GB, I12 pin-merge with the V-ULT-1 pins verified intact); full transcript in
`BUILD_2026-08-14_CENSUS2B_PARTA_WTB1.md`.
**Stamp:** `EXPLORATION — ungated; promotion requires registration.`

**RUNNING SELECTION SURFACE after this entry: 743,516.**

---

### ENTRY 4 · CENSUS-2B ORACLE (Mac-native rev C), selection surface m = 0

**Date** 2026-08-15 · **Seed** 20260814 · **Class** Tier-E + instrument re-pins · **NO REGISTRATIONS**

**m = 0.** The ORACLE grid is a *complete partition* of the filed census-2B event substrate — 5
lenses × 12 classes × {ALL, 2 directions, 3 orientation states}, 856,877 anchors — computed under
one ruler and printed whole. No cell was selected, ranked, promoted or compared against a
threshold, so there is no family to correct over. The three re-pins are scale decisions applied to
every row alike, not choices among candidates. **Any future selection *from* this grid is a new
probe and must declare its own m before it looks; the number to declare is 313, the count of
non-empty rows.**

**What was measured — recorded, NOT claimed.** The findings are stated once, in the build document
(§1–§6); this entry records only what the ledger exists to record.

- **ENTRY 3's kiss suspicion is now quantified, and the ratified fix does not fix it.** Entry 3
  recorded the grammar inert on five of eleven pared pairs with max reach below δ=0.75. The number:
  **0.6112 ATR**, the largest reach any of the five ever attains across the whole panel and all five
  lenses. No δ ≥ ~0.62 can wake them, and `δ = min(0.75, 0.6 × p95 spread)` cannot produce such a δ
  — it is sized off the spread (p95 2.7–23 ATR) and the cap binds on ten of eleven pairs. The event
  is impossible, not rare. **No constant was changed.**
- **The state window was the real mis-scale**: UH read 92.8% flat at 5m under the global k=20 —
  the column was reporting the lookback, not the ribbon — and 6.1% at k=577. `_v2` beside originals.
- **The knot re-pin changed nothing because nothing was wrong** (0 violations on every cell).
  Entry 3's companion finding, that `RIBBON_C = 0.5` makes `br_knot` false everywhere, is answered
  by demoting BR-dispersion to a reported column rather than by moving a constant.
- **`26_89` was derived, not fabricated and not dropped**, from the pinned `emas/` substrate, and is
  excluded from the reconciliation gate; the rule is licensed by re-deriving `12_26` exactly
  (197,305 = 197,305, 0 mismatched cells). **`12_26 IN-WINDOW`/`bare` is degenerate** — windows tile
  the armed span 100.0000% on all 25 cells. **The 4h lens is three-quarters of a lens**, and its
  VH/UH orientation cut is undefined rather than measured. All four are build-doc §6.

**Provenance:** `~/Naiad/research_outputs/census2b/oracle/`, all artifacts sha-pinned in
`oracle_manifest.json`; built by `scripts/census2b_oracle.py` from the substrate sha-pinned in
`census2b_manifest.json`; full transcript in `BUILD_2026-08-15_CENSUS2B_ORACLE.md`.
**Data born and read local, Mac-era residency v2.**
**Stamp:** `EXPLORATION — ungated; promotion requires registration.`

**RUNNING SELECTION SURFACE after this entry: 743,516.** (m = 0 adds nothing.)
