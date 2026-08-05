# BUILDER'S REPORT — SEQ-8 · THE CASCADE EVENT EXTRACT

**Contract:** `exchange/queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md` (ratification word: **"extract"**, spoken by the operator in the run instruction)
**Executor:** HEPHAESTUS · **Run date:** 2026-08-04 · **Branch:** `v12-v1-census` · **Environment:** local Windows Claude Code
**Status: COMPLETE — 8/8 fixtures PASS. D1–D6 all emitted. P-SEQ-ii scored: REPLICATES.**

Written zero-context: every number below is measured in this run and traceable to a named file, not carried from memory.

---

## 0 · HARD ASSERTIONS (run before any read or write)

| assert | expected | actual | result |
|---|---|---|---|
| `git rev-parse HEAD` printed | — | `8d1095dbf0589304038e42c1949aff7120df3d0b` | **PASS** |
| path contains `Users…OneDrive…naiad` | — | `C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad` | **PASS** |
| `engine/` exists | yes | yes | **PASS** |
| `scripts/census_build.py` exists | yes | yes | **PASS** |
| `exchange/{queue,reports,status}/` exist | yes | all three | **PASS** |
| census exploration substrate present | yes | `research_outputs/census/` — 4 JSONL + manifest, row counts match the manifest exactly | **PASS** |
| no lockbox read | none | none — every read is `open_time < CEIL_MS` | **PASS** |

Two environment facts found and worked around rather than assumed:

- **The interpreter in every docstring does not exist.** `.venv/` is absent (deleted 2026-07-28, `SETUP_2026-07-28.md` §A4). The working interpreter is **`C:\venvs\naiad\Scripts\python.exe`** — Python 3.12.10, numpy 2.1.3, pandas 2.2.3, pyarrow 18.1.0, i.e. the pinned `requirements.txt` set exactly. System `python` has no numpy and would have failed on import.
- **Klines cache present:** `C:\Users\luisf\AppData\Local\naiad\data_cache\klines`, 60 parquet files. `*_30m.parquet` and `*_1d.parquet` are absent for every asset and that is **correct, not a gap** — `census_build.RESAMPLE` derives them from 15m and 1h.

---

## 1 · WHAT WAS BUILT

Five new scripts, none of which edits `engine/` or `census_build.py`. Engine **1.0.12** byte-untouched (live constant read from `engine/version.py`; note `census_build.py`'s docstring still says 1.0.11 — reported below).

| script | role |
|---|---|
| `scripts/seq8_extract.py` | D1 raw event stream · D6 warmup table |
| `scripts/seq8_views.py` | D2 eight cascade views · cross-view agreement · D5 arrivals panel |
| `scripts/seq8_atlas.py` | F-SEQ4 Atlas re-derivation · the third P-SEQ-ii scoring frame |
| `scripts/seq8_outcomes.py` | D3 outcome substrate + cascade→birth join · D4 route matrix |
| `scripts/seq8_fixtures.py` | F-SEQ1 … F-SEQ8 |

**I1 and I2 are satisfied structurally, not by restatement.** `seq8_extract.py` *imports* `census_build` and reads `CEIL_MS`, `ASSET_STARTS`, `TF_MS`, `TFS`, `RESAMPLE`, `ATR_LEN`, `HORIZONS` and the resampler `_resample` from it. No census constant is re-typed anywhere. If the census machinery moves, this extract moves with it or fails loudly. The s1 resampler is called, never reimplemented (ARGUS hazard F-1R-*).

**The loader is proven equal to the census loader, per asset × TF, not sampled.** `assert_census_parity()` compares `open_time, open, high, low, close, e9, e89, e200, atr` array-for-array against `census_build.load_tf`. **49/49 frames identical.** Without that probe, F-SEQ1 would be a comparison of an artifact against itself.

---

## 2 · PROBE VALUES — measured, not assumed

```
exploration ceiling   1719792000000  (2024-07-01T00:00:00Z)   [census_build.CEIL_MS]
lattice A             {9, 89, 200}   pairs 9_89, 89_200, 9_200
lattice B             {12, 25}       pair  12_25
HTF orientation       EMA 300, 450 on {1h, 4h, 12h, 1d}
warmup rule           seed residual (1-alpha)^k < 1e-3  ->  EMA300 = 1037 bars, EMA450 = 1555 bars
assets                BTCUSDT ETHUSDT JTOUSDT NEARUSDT SOLUSDT TAOUSDT ZECUSDT
D1 events             288,711        (149,804 lattice A · 138,907 lattice B)
D2 cascades           950,145 depth>=2 across 8 views; 540,761 singletons counted, not emitted
D3 outcome rows       950,145
D4 route cells        257
join rows             301,018        6,831 of 7,117 distinct births joined; 0 orphans
extract runtime       93.9 s   views 86.6 s   outcomes 109.7 s
```

**Event-class coverage (I4).** The census machinery computes cross detectors only, so cross detectors only are emitted — no new detector was built. Against the Q1c taxonomy (memory Entry 19, operator 2026-07-29), the **gap list is the deliverable**:

| Q1c class | emitted | note |
|---|---|---|
| EMA/EMA cross | **YES** | both lattices, both directions, all 7 census TFs |
| EMA/EMA test-and-reject | no | no detector exists in the census machinery; I4 forbids building one here |
| price test-and-bounce | no | nearest existing relative is D10 termini (`census_termini.jsonl`), which are pivots, not test-and-bounce events |
| S/R flip | no | no detector exists |
| ribbon-state episode | no | episodes are intervals, not events; `continuation.jsonl` carries a ribbon-separation flag but no episode object exists |

**1 of 5 Q1c classes is emitted.** Four remain unbuilt and are a scoping question for the operator, not a defect of this run.

---

## 3 · FULL FIXTURE TRANSCRIPT (verbatim console output)

```
========================================================================
SEQ-8 FIXTURE TRANSCRIPT
========================================================================

=== FIXTURES ===
  [PASS] F-SEQ1: 280 asset x TF x class x dir cells reconciled against census_outcomes.jsonl; 0 diffs; totals 149802 census == 149802 extract (census-filter applied). The raw stream additionally retains 2 event(s) the census filter drops at the right edge — kept and flagged, never silently dropped.
  [PASS] F-SEQ2: ceiling 1719792000000 (2024-07-01T00:00:00Z) read from census_build.CEIL_MS; max timestamp per file: seq8_cascade_birth_join.jsonl=1719781200000, seq8_cascades.jsonl=1719792000000, seq8_events.jsonl=1719792000000, seq8_outcomes.jsonl=1719788400000 — all <= ceiling (a bar opening before the ceiling may CLOSE on it)
  [PASS] F-SEQ3: 301018 join rows; 6831 of 7117 distinct (cell_id,tranche_id) births joined; orphans join->journal = 0; 286 births fall inside no cascade span (a real outcome, not an orphan). RULE: birth joins a cascade iff (a) cell symbol == cascade asset, (b) the cell's governor TF is a rung of the cascade (MANDATES: intraday->1h, swing->4h, position->12h), and (c) birth ts_open lies within [first rung bar_close, terminus bar_close]. Restricted to lattice A / 9_89 (the cross the engine trades).
  [PASS] F-SEQ4: Atlas re-derived from census1b_termini_enriched.jsonl under its OWN recipe: seq_total=2378 (published 2378), 20/20 published values reproduced exactly (6 signatures, 8 frontier cells, 4 transition column totals, monotone_pct). The literal fixture wording cannot hold: the Atlas is a TERMINUS-ANCHORED STAR over 14,560 pivot termini, not a window-chained view over cross events — the diff is itemized on 5 axes in seq8_atlas_replication.json:diff_vs_D2.
  [PASS] F-SEQ5: curtain-clean list contains 7 column groups, none of which is an outcome column (0 leaks); 4 column groups explicitly labelled post-curtain. Anchor rule re-derived on 96 sampled termini across 5 assets: 0 violations of 'first exec bar whose open >= the terminus bar close'.
  [PASS] F-SEQ6: warmup rule: seed residual (1-alpha)^k < 1e-3 -> EMA300 needs 1037 bars, EMA450 needs 1555 bars. 98 asset x TF x length cells audited, 0 inconsistencies; 0 e300/e450 values on a non-HTF timeframe (must be 0); across the event stream 3132 null vs 33602 warmed 300/450 readings. 13 cells NEVER warm within the substrate: JTOUSDT/4h/e450, JTOUSDT/12h/e300, JTOUSDT/12h/e450, JTOUSDT/1d/e300, JTOUSDT/1d/e450, NEARUSDT/1d/e450, SOLUSDT/1d/e450, TAOUSDT/4h/e300, TAOUSDT/4h/e450, TAOUSDT/12h/e300, TAOUSDT/12h/e450, TAOUSDT/1d/e300, TAOUSDT/1d/e450
  [PASS] F-SEQ7: 9 artifacts compared across a full independent re-run (seq8 vs seq8_run2); 0 differ. python 3.12.10, numpy 2.1.3. No seed is used anywhere in this extract — nothing is sampled, bootstrapped or shuffled, so there is no seed to print. NORMALIZATION DISCLOSURE: the three manifests are compared via their sha256 BLOCKS, not as files, because each carries a wall-clock `elapsed_s` that cannot be byte-stable; every bulk artifact they name is compared by its own sha256, and seq8_arrivals.json / seq8_event_counts.json / seq8_warmup.json are compared RAW. NO computed value is normalized (precedent: census1b_det.py F1b-DET).
  [PASS] F-SEQ8: query over D1 alone (no re-extraction, no recomputation of any indicator): bull 9_89 5m->15m->4h, each step within 48h, with 12h e89>e200 as-of the 4h arrival — 3931 ordered triples across the whole substrate: BTCUSDT=829, ETHUSDT=1165, JTOUSDT=77, NEARUSDT=596, SOLUSDT=745, TAOUSDT=0, ZECUSDT=519. Worked instance for hand-inspection: BTCUSDT 5m 2020-02-16T22:35:00Z -> 15m 2020-02-17T00:15:00Z (+1.83h) -> 4h 2020-02-18T20:00:00Z (+47.5h), 12h bits '111111x' (index 1 = e89>e200 = 1). The cross-timeframe state travels ON the atom, which is what makes across-time-AND-across-timeframes patterns minable without re-extraction.

=== FIXTURE SUMMARY ===
  8/8 pass
```

### F-SEQ8 hand-inspection, done independently of the fixture

Re-read straight from `seq8_events.jsonl` for the three named atoms:

```
5m   2020-02-16T22:35:00Z  close=9850.99   e9=9811.672252  e89=9810.897255  e9>e89=True
15m  2020-02-17T00:15:00Z  close=9926.38   e9=9902.641562  e89=9900.924520  e9>e89=True
4h   2020-02-18T20:00:00Z  close=10174.32  e9=9896.710184  e89=9835.579891  e9>e89=True
     mtf 12h = 111111x  on all three  ->  bit 1 (e89>e200) = 1
```

All three are genuine bull 9/89 crosses (fast above slow at the cross bar), the ordering and both gaps hold, and the 12h trend alignment is read off the atom itself. The trailing `x` on the 12h bit string is `e300>e450` and is correctly unknown: in Feb 2020 BTC's 12h EMA300 had not yet warmed under the stated rule. The claim in the contract — that across-time-**and**-across-timeframes patterns are minable from D1 without re-extraction — holds as demonstrated.

---

## 4 · DELIVERABLES

### D1 · RAW EVENT STREAM — `seq8_events.jsonl`, 288,711 rows, 167,105,389 B

One row per cross event, **no chaining of any kind**. Each row carries: asset, TF, lattice, event class, direction, `ts`/`ts_iso`, bar close, bar index, the four OHLC stamps, the event bar's own full EMA state (`e9 e89 e200 e12 e25 e300 e450`) plus ATR, the exec anchor (`exec_idx`, `exec_ts`, `p0`), two honesty flags (`exec_anchor_ok`, `atr_ok`), and `mtf` — a 7-bit orientation string **for every one of the 7 timeframes**, gathered as-of the last closed bar of that TF at the event bar's close.

The `mtf` block is what makes the atom self-sufficient: bit order is `e9>e89 · e89>e200 · e9>e200 · e12>e25 · close>e89 · close>e200 · e300>e450`, with `x` where an input is NaN. It is the reason F-SEQ8's query needs no second pass over price.

**Atom-independence is literal.** The two events the census filter drops at the right edge (ETHUSDT 1h 9_200 up at 2024-06-30T23:00Z; JTOUSDT 1d 89_200 down at 2024-06-30T00:00Z — both cross bars *close* exactly on the ceiling, so no exec bar exists to anchor them) are **retained and flagged**, not dropped. A raw stream that silently loses events is not raw.

### D2 · CASCADE VIEWS — `seq8_cascades.jsonl`, 950,145 rows, 789,501,107 B

Eight views = {24h, 48h, 72h, 1W} × {window-chained, direction-consistent}. Chaining is on `bar_close_ms` — the instant a cross becomes knowable — never on bar open. Each rung must be a **new** timeframe; depth-complete to 7, no 3-rung truncation. Every cascade carries all three frames, plus `monotone`/`shuffle`, the Rewire family label, per-step sojourn in ms and exec bars, and leap latency to each governor lens.

| view | cascades (depth≥2) | singletons | monotone |
|---|---:|---:|---:|
| 24h \| window_chained | 155,674 | 28,800 | 79.42% |
| 48h \| window_chained | 172,648 | 11,388 | 75.32% |
| 72h \| window_chained | 178,066 | 5,932 | 73.35% |
| 1W \| window_chained | 183,054 | 940 | 69.95% |
| 24h \| direction_consistent | 65,107 | 123,718 | 84.95% |
| 48h \| direction_consistent | 65,193 | 123,344 | 84.97% |
| 72h \| direction_consistent | 65,201 | 123,321 | 84.97% |
| 1W \| direction_consistent | 65,202 | 123,318 | 84.97% |

Singletons are **counted and reported, never silently dropped** — a 1-rung cascade adds nothing over the D1 atom it contains, so it is not re-emitted, but its count is on the record.

**Cross-view agreement — this is the answer to the operator's standing SEQ-1 question.**

| comparison | same depth | same rung string |
|---|---:|---:|
| 72h vs 1W, direction_consistent | 99.998% | 99.998% |
| 48h vs 72h, direction_consistent | 99.985% | 99.985% |
| 48h vs 1W, direction_consistent | 99.983% | 99.983% |
| 72h dir-consistent vs 1W window-chained | 8.45% | 8.02% |
| 48h dir-consistent vs 1W window-chained | 8.45% | 8.01% |
| 24h dir-consistent vs 1W window-chained | 8.29% | 7.86% |

**The window barely matters; the rule decides everything.** Under direction-consistent chaining, quadrupling the window from 24h to 1W changes the cascade population by 95 cascades out of ~65,200 (0.15%) and leaves 99.98% of events in an identically-shaped cascade. Under window-chained, the same change moves singletons from 28,800 to 940 and monotone share from 79.4% to 70.0%. The two rules agree with each other on about 8% of events.

The mechanism is plain: counter-direction crosses on fast timeframes arrive every few hours, so a direction-consistent cascade almost always terminates on a counter-direction event long before any of these windows expires. The window is not doing the work — it is not even reached.

**This is a direct, counted answer to the operator's gate** (*"is a time-based definition of a cascade a good definition at all? does the data suggest a less arbitrary one?"*): a time window is a poor primary definition because within this range it is nearly inert under the rule that respects direction, and dominant under the rule that ignores it. The less arbitrary object the data points to is *the direction-consistent episode*, whose boundary is set by price behaviour (a counter-direction cross) rather than by a chosen number of hours. **Registered as an observation from counts, not as a claim** — it is outside P-SEQ-ii and carries no stamp.

### D3 · OUTCOME SUBSTRATE — `seq8_outcomes.jsonl`, 950,145 rows, 790,256,704 B — **EMITTED, EMBARGOED (I6)**

Per cascade terminus: MFE **and** MAE at the census horizons {20, 100, 500} exec bars, in bps and in ATR, with truncation flags; `p0`/ATR basis at the terminus anchor; `cleared_tier`, `cleared_tier_at_tf`, `time_to_tier_clearance_ms`, `survival_to_next_tf`. Not analyzed, not ranked, not promoted in this run. The embargo is **structural**: all outcome maths lives in `seq8_outcomes.py`, and the file that scores the one registered claim (`seq8_views.py` / `seq8_atlas.py`) never opens an outcome column.

**The cascade→birth join — rule stated, never silent.** A birth joins a cascade iff **(a)** the journal cell's symbol equals the cascade's asset, **(b)** the cell's *governor* timeframe appears as a rung of that cascade (`engine/cells.py` MANDATES: intraday→1h, swing→4h, position→12h), and **(c)** the birth's `ts_open` falls inside `[first rung bar_close, terminus bar_close]`. Births are `evt ∈ {ENTRY_FILL, ADD_FILL}`. Join key is **`(cell_id, tranche_id)`** — `tranche_id` alone yields only 6,682 distinct values for 7,117 births and collides across cells.

Restricted to lattice A / 9_89, because that is the cross the engine actually trades; joining fills to a `12_25` or `89_200` cascade would assert a relationship the engine never had.

Journals were confirmed again to carry **no EMA-lattice state whatsoever** — W-F1's P-WF1 premise-false stands. This join is therefore the only bridge between cascade-world and trade-world, which is why the rule is printed rather than buried.

### D4 · ROUTE-VS-OUTCOME MATRIX AT THE 4h ARRIVAL — `seq8_d4_route_matrix.json`, 257 cells — **EMITTED, EMBARGOED (I6)**

Source rung × MFE/MAE quartiles (p25/median/p75) at each horizon, per asset and per view, with the source tier labelled. Built from the two emitted files so it cannot drift from them. **No reading of these distributions appears in this report.**

### D5 · ARRIVALS PANEL — `seq8_arrivals.json` + `seq8_atlas_replication.json` — the one scored claim. See §5.

### D6 · WARMUP COVERAGE — `seq8_warmup.json`, 98 asset × TF × length cells

`engine.indicators.ema` seeds at the first finite value and is **never NaN after bar 0**, so I3's "NaN until full warmup" required a rule the repo does not have. Three conflicting conventions exist (`L` bars in `sma`/`rolling_min`; `length-1` with a mean seed in `analytics/momentum.py`; `L+2` in `brief2.py`), none of them about convergence. Rather than pick a round multiple, the rule is stated arithmetically and printed: **bar `k` is warmed when the seed's residual weight `(1-alpha)^k` falls below 1e-3** → EMA300 = 1037 bars, EMA450 = 1555 bars. Only the new 300/450 columns are masked; masking 9/89/200 would fork them from the census and break F-SEQ1.

**13 cells NEVER warm inside the substrate** and are marked with a literal `NEVER`, not a null: JTO 4h/450, JTO 12h/300+450, JTO 1d/300+450, NEAR 1d/450, SOL 1d/450, TAO 4h/300+450, TAO 12h/300+450, TAO 1d/300+450. Any future cut conditioned on `e300>e450` at those cells is unscorable, and the `mtf` bit is `x` there by construction.

---

## 5 · P-SEQ-ii — THE ONE REGISTERED CLAIM, SCORED

**Claim:** *the leap (arrival at 4h directly from ≤30m) is the dominant 4h activation mode, and 1h arrivals are predominantly adjacent* — replicating in pure counts, sign-consistent on ≥5 of the 7 census assets, per lens. Proposed prior 75%. Outcome-free: no outcome column is opened anywhere in the scoring path.

Definitions were **taken from the Atlas, not re-invented** — `Cascade Rewire.html` `drawArrivals()`: an arrival is a transition read at its destination; *adjacent* is `TFS.index(src) == TFS.index(dest) - 1`; a *leap* is a source ≥2 ladder positions below. Redefining them would have made the replication vacuous.

### Verdict: **REPLICATES**

| frame | limb A · leap dominant at 4h | limb B · adjacent dominant at 1h | verdict |
|---|---|---|---|
| **`atlas_star`** — the frame the finding was made in | **7/7** | **7/7** | **REPLICATES** |
| D2 `direction_consistent`, all 4 windows, depth-complete | **7/7** | **7/7** | **REPLICATES** |
| D2 `window_chained`, depth-complete | 0–3 / 7 | 7/7 | no |
| D2, 3-rung truncated | 7/7 | 0/7 | no |

Per-asset in the `atlas_star` frame (leap / total at 4h, then adjacent / total at 1h):

| asset | 4h leap | 1h adjacent |
|---|---|---|
| BTCUSDT | 73/105 | 187/245 |
| ETHUSDT | 58/95 | 193/254 |
| JTOUSDT | 6/7 | 19/27 |
| NEARUSDT | 44/65 | 142/193 |
| SOLUSDT | 53/78 | 124/172 |
| TAOUSDT | 1/2 | 4/6 |
| ZECUSDT | 53/82 | 151/214 |

**Why three frames, and why that is not fishing.** P-SEQ-ii is a *replication* claim about a finding made on a specific object. Scoring it only on the new D2 cascades would test a different proposition and call it a replication, so the Atlas frame is the one that scores it — and it is the frame where both limbs clear the bar on all seven assets, well above the ≥5 requirement. The other two frames are reported **beside** it because the contract's D2 is explicitly depth-complete, and the disagreement between frames is itself the deliverable the operator asked D2 to expose. The scoring frame was fixed before the numbers were read; all four rows are printed, including the two where the claim fails.

**TAO (n=2) and JTO (n=7) are thin.** They agree directionally, but a 7/7 that includes a 1-of-2 asset should be read as *5 solid + 2 thin*, not as seven independent confirmations. The claim clears the bar on the five majors alone.

### The structural finding underneath — reported as an observation, not a claim

The leap is **anchor-relative, not a property of cascades**. In the Atlas's terminus-anchored star only *forward* crosses count, so a lens whose cross fell **before** the terminus leaves a hole in the ladder — and a 4h arrival then reads as a jump from the fast tier. Chain the same events depth-complete and that hole fills: across the whole substrate the rung immediately feeding 4h is 1h in **5,736** cases against 3,344 from the fast tier (1,279 · 30m, 1,057 · 15m, 1,008 · 5m) and 246 from above.

Symmetrically, 3-rung truncation *destroys* limb B: a cascade that visits 30m before 1h pushes 1h out of the top three, so the surviving 1h arrivals are disproportionately those reached by a leap. Truncation manufactures leaps at 4h and suppresses adjacency at 1h — in opposite directions, from the same cause.

Both effects are counted, both are printed, and neither is a promotion. This is exactly what the operator's SEQ-1 gate was built to catch, and it is the reason D1 bakes in no chaining at all.

---

## 6 · CURTAIN AUDIT (F-SEQ5)

Structure copied from W-F1's audit, substituting "at or before the event bar" for "at or before the fill".

**Curtain-clean — 7 column groups, each with its attestation**

| columns | attestation |
|---|---|
| `asset` `lattice` `event_class` `view` `dir` | cascade identity, fixed at construction |
| `depth` `rungs_absolute` `rungs_gov_relative` `rungs_tier` | read from event bars at or before the terminus bar close |
| `init_tf` `init_ts` `term_tf` `term_ts` `span_ms` | event timestamps at/before the terminus |
| `monotone` `shuffle` `family_first3` `sig_first3` | derived from the rung string alone |
| `sojourn_ms` `sojourn_exec_bars` | gaps between rungs already realised |
| `source_into_*` `latency_to_*` | derived from rungs at/before the terminus |
| `term_exec_idx` `p0_terminus` `atr_basis` | the first exec bar OPEN at/after the terminus bar close — the first tradeable instant |

**Post-curtain — labelled, never mixed into the descriptive set:** `mfe_*`/`mae_*` (the outcome), `trunc_h*`, `time_to_tier_clearance_ms`/`cleared_tier`/`survival_to_next_tf`, and the join's `birth_keys`.

**Violations: 0.** The anchor rule was re-derived from raw price on 96 sampled termini across 5 assets — every one satisfied "first exec bar whose open ≥ the terminus bar close", with no off-by-one.

---

## 7 · CONTRACT DEFECTS — handled and reported, never silently patched

**1. F-SEQ4 cannot pass as literally worded.** The fixture presumes 2,378 is a `{48h, window-chained, 3-rung-truncated}` view over cross events. It is not: it is a **terminus-anchored star** over 14,560 confirmed (5,5) pullback termini, 9_89 only, aligned-direction only, `lag_exec_bars ≤ 576` measured from `exec_idx_confirm`. A chained view over cross events is a different object over a different population; equality would indicate a bug, not correctness. Handled via the fixture's own escape clause — the Atlas was re-derived under its own recipe and reproduced **exactly (20/20 published values)**, and the diff is itemized on five axes in `seq8_atlas_replication.json`. No generator for the Atlas `const D` blob exists in the repo; this is a re-derivation from substrate, not a port.

Two errors in the published Atlas were found while reproducing it and are reported, not corrected in place:
- the prose label *"48 hours after the low"* is wrong by `PIVOT_R = 5` lens bars — the window is measured from the **confirm** bar;
- `monotone_pct = 83.6` is attached in prose to the 2,378 ≥3-rung population, but 83.6% is the figure for the **≥2-rung** population (n = 4,725); for the 2,378 it is 83.01%. Two populations, one number.

**2. F-SEQ3's "zero orphans both ways" is not symmetric.** It is asserted in the direction that is falsifiable — every joined `(cell_id, tranche_id)` must exist in the journals: **0 orphans**. The reverse is not an orphan condition: **286 births fall inside no 9_89 cascade span**, which is a real and correct outcome (the engine traded when no cascade was open), and forcing it to zero would mean inventing cascades. Reported as `births_never_joined`.

**3. I3 ({12,25}) vs I4 (no new detectors).** No `crossover`/`crossunder` on 12 or 25 exists anywhere in the repo — `brief2.py` emits one last-bar boolean `ema12_above_ema25` on {1d,1w}, display-only. Resolved by running the **existing** primitive over the new pair as `"12_25": (12,25)`, adding no detector logic. Whether 12×200, 12×89 or 25×200 are in scope is **unspecified by the contract and currently out of scope** — an operator question.

**4. "Full warmup" had no repo definition.** See §4 · D6. A rule was stated arithmetically and printed rather than assumed.

**5. Tier grammar does not exist anywhere in the repo.** No definition, no named tiers, no mapping — and the operator explicitly demoted it in SEQ-2 (*"an early categorization … not the language of cascades"*). It was therefore **constructed by the builder** from the only authority available: the operator's own named regions in the SEQ-2 ruling (30m-chop · 1H-stair · 4h-12h-slow) plus Q1c's trend tier:

```
FAST  = 5m, 15m, 30m      STAIR = 1h      SLOW = 4h, 12h      TREND = 1d
```

Labelled **BUILDER-DEFINED, pending stamp** in `seq8_views_summary.json`. It is also what makes "leap" mean what the Atlas says it means: FAST → SLOW, skipping STAIR. Governor-relative steps were likewise implemented from the standing convention (`LEDGER.md:771`) because no step-index function exists in code.

**6. "Per lens" in D5 is ambiguous.** Read as the two lenses the claim names — 4h arrivals and 1h arrivals — and scored separately for each, across all eight views and all three frames.

---

## 8 · FINDINGS REPORTED, NOT FIXED

1. **`research_outputs/seq8/` is NOT gitignored.** `git check-ignore` returns no match. The contract says these bulk artifacts are not pushed; the only thing keeping them out of a push is that `publish_exchange.publish()` stages `exchange/` alone. They will show as untracked indefinitely. **No ignore rule was added** — precedent (census1b, `_unarchived`) is that ignore rules land under a named authorization. Operator ruling requested.
2. **`census_build.py`'s docstring says engine 1.0.11; the live constant is 1.0.12.** Cosmetic, but it is the file every census-family script cites for provenance.
3. **The canonical journal is staging, not evidence.** `research_outputs/_unarchived/s3_2026-07-27/journal_s3/scored/` (753 files, 1.4 GB) is gitignored, untracked, and exists on this machine only. D3's join depends on it. `_reviewer_box/wf1/*.json` (used here) is likewise local-only. If this machine is lost, the join is not reproducible without re-running S-3.
4. **`research_outputs/census_run2/` holds only `build_manifest.json`** — the four JSONL are absent, so any future census run2 byte-comparison must rebuild first.
5. **The 1d governor lens has no journal counterpart.** Mandates cover 1h/4h/12h only, so `1d` cascades can never join a birth. `TAOUSDT_position` does not exist; HYPE/FARTCOIN/LIT have no journals at all. Empty by construction, not by defect.
6. **P-SEQ-ii is not registered in `LEDGER.md`** (`grep -c "P-SEQ"` → 0). The contract commissions scoring it in this run and the operator's SEQ-7 ruling registered it, so it was scored as commissioned; but `LEDGER.md:806-815` requires scored verdicts to postdate the registration commit. The builder does not write to `LEDGER.md` — the entry is proposed in the session summary for the reviewer to land.
7. **`scripts/publish_exchange.py` has no `__main__`.** Running it as a script is a silent no-op; it must be invoked as a library. Already documented in `CONVENTIONS.md:264-269`; re-confirmed here.

---

## 9 · VERSIONS, HASHES, COMMITS

```
python            3.12.10   (C:\venvs\naiad\Scripts\python.exe)
numpy             2.1.3
pandas            2.2.3
pyarrow           18.1.0
engine            1.0.12    (engine/version.py — byte-untouched this run)
branch            v12-v1-census
HEAD at start     8d1095dbf0589304038e42c1949aff7120df3d0b
seed              none — nothing in this extract is sampled, bootstrapped or shuffled
extract_version   seq8-extract-1.0.0
census substrate  census_outcomes.jsonl daf488acef40a2ab… (read-only; not rebuilt)
```

| artefact | sha256 (first 16) | bytes |
|---|---|---|
| `research_outputs/seq8/seq8_events.jsonl` | `2bdc5c56c054e27c` | 167,105,389 |
| `research_outputs/seq8/seq8_cascades.jsonl` | `13195287eceab160` | 789,501,107 |
| `research_outputs/seq8/seq8_outcomes.jsonl` | `7f096222aac6f339` | 790,256,704 |
| `research_outputs/seq8/seq8_cascade_birth_join.jsonl` | `63777ca872115ba0` | 122,363,043 |
| `research_outputs/seq8/seq8_arrivals.json` | `16fef0c4771633bb` | 669,814 |
| `research_outputs/seq8/seq8_d4_route_matrix.json` | `f45b6d426e19c104` | 193,545 |
| `research_outputs/seq8/seq8_warmup.json` | `c9a68c6ca0654a53` | 24,994 |
| `research_outputs/seq8/seq8_event_counts.json` | `9584aaadf0454e1a` | 27,067 |
| `research_outputs/seq8/seq8_atlas_replication.json` | `c4ecf5dcf76c0303` | 9,841 |
| `research_outputs/seq8/seq8_views_summary.json` | `6379f734dade0d25` | 9,096 |
| `research_outputs/seq8/seq8_fixtures.json` | `6b24aa64e36a1be3` | 6,611 |
| `research_outputs/seq8/seq8_extract_manifest.json` | `07aa3fde63f7c049` | 3,980 |
| `research_outputs/seq8/seq8_outcomes_manifest.json` | `ca883a49e4fc69d2` | 3,499 |

Total `research_outputs/seq8/` = **1,783.5 MB** across 15 files. `research_outputs/seq8_run2/` is the F-SEQ7 determinism pass, same size, 11 files.

---

## 10 · FILE DISPOSITION

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY |
|---|---|---|---|---|---|
| `scripts/seq8_extract.py` | yes | untracked | not committed | no | NOT PROTECTED |
| `scripts/seq8_views.py` | yes | untracked | not committed | no | NOT PROTECTED |
| `scripts/seq8_atlas.py` | yes | untracked | not committed | no | NOT PROTECTED |
| `scripts/seq8_outcomes.py` | yes | untracked | not committed | no | NOT PROTECTED |
| `scripts/seq8_fixtures.py` | yes | untracked | not committed | no | NOT PROTECTED |
| `research_outputs/seq8/**` (15 files, 1,783.5 MB) | yes | untracked — **not ignored, see finding 1** | not committed | no | NOT PROTECTED |
| `research_outputs/seq8_run2/**` (11 files, 1,783.5 MB) | yes | untracked — **not ignored, see finding 1** | not committed | no | NOT PROTECTED |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SEQ8.md` | yes | untracked | see §11 | see §11 | GitHub only |
| `exchange/reports/SESSION_SUMMARY_HEPHAESTUS_2026-08-04_SEQ8.md` | yes | untracked | see §11 | see §11 | GitHub only |
| `census1b_termini_enriched.jsonl` (read-only input) | yes | ignored — `.gitignore:74 /census1b_termini_enriched.jsonl` | n/a | no | NOT PROTECTED |
| `research_outputs/_unarchived/s3_.../journal_s3/scored/` (read-only input) | yes | ignored — `.gitignore:101 research_outputs/_unarchived/**` | n/a | no | NOT PROTECTED — staging only |
| `_reviewer_box/wf1/*.json` (read-only input) | yes | ignored — `.gitignore:80 _reviewer_box/` | n/a | no | NOT PROTECTED |
| `.gitignore` | yes | tracked, **modified & unstaged — deliberately left so** | not committed | no | GitHub only |

**Committed ≠ pushed. Pushed ≠ backed up.**

The five `scripts/seq8_*.py` files are **deliberately left uncommitted**. W-F1 §18 established that commit-no-push is unachievable on this branch — `publish()` pushes the whole branch ref, so any commit made before a publish travels to `origin` regardless. This contract drops the clause and accepts the script commit riding the publish; leaving the scripts uncommitted until the operator decides is the one option that does not force that choice now.

`.gitignore` is left modified-and-unstaged on purpose: staging it would put a non-`exchange/` path in the index, and `publish_exchange.guard()` would FLAG the publish, reset the index and skip the push.

---

## 11 · PUBLISH RESULT

See the session summary's closing block and the on-screen close for the exact publish status, staged path list, and whether the push SUCCEEDED.
