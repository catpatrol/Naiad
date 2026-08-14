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

**RUNNING SELECTION SURFACE after this entry: 0.**
