# V3 Anchor Forensics — Stop, Exit & Entry Logic
**Scope:** post-hoc excavation of the V3 anchor run (engine 1.0.7 / 2f260e1, config v12_anchor a3917ea5…, 20 scored cells, 8,387 resolved tranches, 3,456 campaigns, exploration-classic).
**Charter basis:** VR-1 — exploration-classic is "free to mine, plot, iterate." Lockbox untouched. Anything graduating to engine logic requires a pre-registered variant slot.
**Provenance:** all inputs recomputed from raw journals during reviewer verification (grid −5,756.91 net cell-R reproduced to 4 decimals). "cell-R" = R weighted by tranche size; "R/unit" = per-unit-risk basis. Gross = costs added back.

## 1. Stop census (Q1) — two lenses, one discrepancy, one hypothesis
**Field lens** (exit-row stop vs entry stop), 8,365 stop/stop_gap exits (99.7% of ALL exits — exit logic *is* stop logic):
| class | n | share | net/unit med | gross/unit med |
|---|---|---|---|---|
| stop unchanged ("initial") | 6,060 | 72% | −1.58 | −0.83 |
| ratcheted, below BE | 667 | 8% | −0.88 | −0.31 |
| ratcheted, ≥ BE | 1,638 | 20% | +0.69 | +1.34 |
Split is stable across mandates (71–73% initial).

**Economic lens** (gross loss actually paid): full −1R loss **1%** · partial loss **74%** · ~breakeven 0% · profitable stop exit **25%**.

**Discrepancy:** the field lens says stops rarely move; the economics say full-risk losses almost never occur. The exit-row `stop` field's timing semantics (stop-at-fill vs stop-after-bar-update) is unresolved from journals → **S-1 pin item**. The economic lens is authoritative (derived from verified realized_r).

**Hypothesis H-S1 (de-ratchet):** re-arms clear and re-place stops (G-4 mechanism, Pine-literal). The "ratchet" may not be monotone across campaign re-arms — candidate explanation for 47% of +1R-MFE tranches dying at a loss. Quantify in S-1: count de-ratchet events and their P&L.

## 2. Shaken-out population (Q2)
Post-exit favorable continuation (per-unit R, 20 exec bars), stop exits only:
| class | cont20 median | ≥ +1R | ≥ +2R |
|---|---|---|---|
| initial | +0.23 | 36% | 23% |
| ratch<BE | +0.26 | 32% | 17% |
| ratch≥BE | +0.14 | 31% | 17% |
**Resumption pool: 2,899 stop-outs (35%) resumed ≥1R within 20 bars; forfeited continuation ≈ +4,429 cell-R** (capped 10R/unit) — 77% the size of the entire grid loss. Median stop-out resumes (+0.23R). The stop sits inside the noise band.

## 3. Ratchet substitution vs enrichment (Q3)
Engine shadowed two substitute stop families per tranche (counterfactual exit R journaled):
| family | grid gross cell-R | better on | swing Δ | intraday Δ | position Δ |
|---|---|---|---|---|---|
| ACTUAL ratchet | +1,345 | — | — | — | — |
| stop_alt_anchor | +408 | 16% | **+100** | −722 | −315 |
| stop_alt_volbuf | +246 | 11% | **+192** | −923 | −368 |
**Wholesale substitution: FALSIFIED.** Both families destroy intraday/position. **Swing-only volbuf enrichment: LIVE** (+192 gross on a swing book grossing +284 → ~+68%). Enrichment beats substitution.

## 4. Shadow inventory (Q4) — yes, and richer than chartered
Per-tranche `shadow` dict, 100% coverage: `entry_alt_{px,stop,t}` (alternate entry) · `exit_XA..XD` (four exit variants — semantics unpinned, S-1 item) · `stop_alt_anchor{,_exit_r}` + `stop_alt_volbuf{,_exit_r}` (used in §3) · `ladder_strict`, `ladder_unthrottled_{grade,size_r}`, `size_big_adds`, `size_full_r1` (sizing counterfactuals). Charter §3.4 1R-adds counterfactual: recorded unimplemented as a scored line; recomputable offline (manifest Q-3).

## 5. Harvest — the unasked-for centerpiece
- 3,381 tranches (40%) reached ≥ +1R/unit open profit. **Median capture: 6% of peak.** 62% kept <25% of peak.
- **PROTECTED cohort is net-negative**: Σ −649 cell-R, median −0.70/unit net.
- **1,581 tranches (47% of PROTECTED) reached +1R and still exited at a gross loss** (Σ −1,224 net).
- **Oracle exit** (every tranche exits at its MFE): +9,225 gross vs actual −5,757 net → **~15,000 cell-R lives between what trades touched and what the system kept.** Prometheus's "harvest is the silent failure point," now measured: the harvest gap dwarfs even costs.

## 6. Entries (Q5) — the leak is geometry and timing, not price
- **Oracle entry** (MAE trough): +7,525 cell-R — hindsight bound only.
- **entry_alt shadow is worse** than actual entries (better on 37%, median −0.93 R-units) → fill prices aren't the leak.
- **Retracement depth is monotone**: net/unit mean −0.69 (retr<0.25) → −0.51 → −0.20 → −0.18 (retr≥0.75). Chasing shallow pullbacks is the worst entry.
- **Stop geometry**: stops <0.5 ATR_exec: n=739 (9% of tranches), mean **−9.16 net/unit, Σ −3,388 cell-R (59% of the grid loss)**; the 0.5–1.0 ATR band is the least-bad (Σ −283). Sub-half-ATR risk geometry is a donation at taker costs.
- Zone Z2 ≥ Z1; provisional ≥ full (E-1's provisional entries are not the problem).
- Adds: gross/unit +0.47 (vs R1 +0.11) — **adds carry the edge** — but pay ~2.4R/unit mean costs. Orphan campaigns (adds into never-filled R1): 265, Σ −817, **−3.08/campaign — worst cohort in the study**. All top-10 campaigns are full 3-tranche ladders; 390 winners, top-20 = 38% of Σwins.

## 7. Cost anatomy
| mandate | cost/unit med (mean) | stopdist/ATR med | fees / slip / funding |
|---|---|---|---|
| swing | 0.47 (1.18) | 1.22 | 60/40/0% |
| intraday | 0.82 (2.07) | 1.36 | 66/34/0% |
| position | 0.27 (0.72) | 1.14 | 60/39/1% |
Fees dominate; funding negligible. Cost stack 7,102 cell-R flips the grid sign (0× +1,345 → 1× −5,757). Maker-fill structures would halve the largest component — a charter-level fill-realism discussion, flagged not proposed.

## 8. Codeable candidates (Q6), ranked by measured bound
| # | rule | bound (cell-R) | basis | caveat |
|---|---|---|---|---|
| C1 | entry gate: stop distance ≥ 0.5 ATR_exec | **+3,388 net** | Σnet of filtered bucket | 47% of filtered still reached +1R; in-sample |
| C2 | half-harvest: bank 50% at +2R | +587 gross | 2,082 tranches reached +2R | path-independent approx |
| C3 | BE-floor: stop→breakeven at +1R MFE | +509 gross | 1,581 loss-exits → ~0 | ignores re-touch dynamics |
| C4 | orphan kill: no adds unless R1 filled | +817 net | Σ orphan cohort | clean; assumes independence |
| C5 | swing-only volbuf stop enrichment | +192 gross (swing) | shadow counterfactual | no add/ratchet interaction |
| C6 | resumption re-entry after stop-out | pool +4,429 | cont20 ≥1R × 35% | trigger undesigned → S-1 |
| C7 | deep-retr entry preference / size tilt | monotone table | conditioning only | filter form undecided |
**Bounds are NOT additive** (overlapping tranches), are in-sample on mined data, and mix gross/net bases. No sign-flip is promised. Every candidate must survive S-1 measurement, then a pre-registered variant slot, then lockbox/forward validation. Variant-seed register now exceeds the five chartered slots → prioritization is an operator decision at V4 design.

## 9. Discretionary lessons (usable immediately, no code)
1. **Up 1R = protect something.** 47% of +1R excursions round-tripped to gross losses; median winner-turned-loser kept 6% of its peak. The measured #1 leak is giveback, not premature exits.
2. **Your stop is where everyone's is.** 1 in 3 stop-outs resumes ≥1R within 20 bars. Place beyond structure + volatility buffer — or pre-plan the re-entry; the resumption pool is nearly the whole loss.
3. **Never add into an unfilled/unworking base** (−3.08/campaign, worst cohort).
4. **Sub-half-ATR stops are donations** (−9.16/unit mean). If structure demands one, the trade isn't takeable at taker costs.
5. **Deep pullbacks beat chases**, monotonically.
6. **The edge lives in full ladders** — every top-10 campaign used all three tranches. Surviving to add twice is the win condition.

## 10. Proposed follow-up: Study S-1 (instrumented replay, measure-only)
Replay exploration-classic with trading UNCHANGED; journal shadow columns only (chartered mining; zero gate implications):
- Families: BE-floor (0.75/1.0/1.5R triggers) · giveback trail (exit at 30/40/50% giveback from peak ≥2R) · swing structural stop + ATR buffer (volbuf direction, swing-tuned) · resumption re-entry (reclaim of stop level within N bars) · min-ATR entry gate (0.5/0.75/1.0).
- Semantics pins: exit-row stop-field timing · stop monotonicity across re-arms (count de-ratchet events → H-S1) · exit_XA–XD meaning.
- Deliverable: per-family counterfactual grid table with per-mandate splits → top performers nominated to variant slots.
**Pre-registered predictions:** P-S1 (~70%) H-S1 confirmed — de-ratchet events exist and account for ≥⅓ of +1R-to-loss round-trips. P-S2 (~65%) BE-floor and giveback-trail beat C2/C3 static bounds when path-aware. P-S3 (~60%) min-ATR gate's realized benefit lands within ±40% of +3,388 after forfeited winners.
