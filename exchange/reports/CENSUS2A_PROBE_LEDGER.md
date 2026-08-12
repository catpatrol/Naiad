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
