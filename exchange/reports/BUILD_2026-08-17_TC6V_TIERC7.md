# BUILD — TC6-V · CLOSE THE AUDIT · **PHASE B NOT RUN**

**Lane** APOLLO · **Branch** `v12-v1-census` · **Drafted** APOLLO · **Executor** HEPHAESTUS · **Seed** 20260817

**RATIFIED** operator 2026-08-17 — *"all on lean; Q5 full speed; run sequentially, pause after for analysis"*.

**CLASS — Phase A: audit completion. NO NEW CLAIMS.** Nothing in this document registers anything, and nothing in it gates anything.

---

## 0 · EXECUTIVE — VERDICT FIRST

**CP-A IS RED. PHASE B (TIER-C7) WAS NOT RUN.**

The commission set the gate itself: *"Any CONFIRMED-DATA-AFFECTING touching published numbers → HALT."* The audit adjudicated all 39 outstanding findings and returned **four CONFIRMED-DATA-AFFECTING**, of which **two changed sentences already published in `BUILD_2026-08-16_TIERC6_REVB.md`** — one of them a sign.

| verdict class | n |
|---|---:|
| CONFIRMED-FIXED (closed by the C6-1…C6-7 repairs, each re-proved by running) | **12** |
| COSMETIC | **16** |
| REFUTED | **7** |
| **CONFIRMED-DATA-AFFECTING** | **4** |

**All four have been repaired and every affected number restated.** The halt is not "work remains"; it is the operator's gate on whether TIER-C7 should be built on a book whose published numbers moved this morning.

### The four, and what moved

| # | what was wrong | old | **new** |
|---|---|---|---|
| **11** | **L-FMH's counterfactual booked an exit at the CLOSE of bars on which the stop had already been taken** — 173 impossible exits. Adverse-first says the stop fills intrabar and the campaign is already out | v5-control A3 Σ delta **−3.1944** | **+1.2276 — THE SIGN REVERSES** |
| **12** | **The wall-aware S-BUF cell read UNFLOORED, SEEDED ribbon EMAs.** This estate's **third** repair of that same defect | cell net R **+38.6177** | **+39.4020** |
| **33** | **`mean_breakthrough_depth_atr` was pooled on the wrong denominator.** It is a mean over the approaches that BROKE THROUGH, pooled on ALL approaches | 12h/889 depth **1.139996** | **1.177652** |
| **25** | **The hazard curve's population count was the CONTROL book's, and the curve is partly measuring the card's own stop** | "None on **105** of 195" | **94** — and the censoring is now disclosed |

**The published sentence that was false, withdrawn in full:** TIER-C6 §7 claimed *"every arm's Σ delta is negative"* for L-FMH. On the repaired tables it is false for A3 on the control book. Both TIER-C6 paragraphs now carry a correction notice rather than a quiet edit.

### And three things the audit found that nobody had raised

**THE CORRIDOR MOVES, SO PUBLISHED NUMBERS ARE WALL-CLOCK DEPENDENT.** Identical code, one day later: **2,534 → 2,535 days, 195 → 196 campaigns.** A ZEC campaign opened 2026-08-17T04:00Z and is still open (`corridor_end`, −0.0624 R). Every headline number in TIER-C6 is as-of its corridor and silently is not as-of any other. A corridor pin now exists for audit re-runs, and **F-C6-CTRL was made prefix-robust**: it proves every one of the parent's 195 campaigns is present and identical, and *reports* the extras instead of failing on growth.

**THE OFFLINE CACHE IS NOT IMMUTABLE.** Pinned to Tier-C5's exact corridor end, the league still sees **+1 approach on 30 of 313 rows** — boundary bars that arrived after TC5 filed its table. **No fixture in this estate had ever stated that a filed parquet is not bit-reproducible after a cache refresh.** Two magnitude bounds were tried and both were guesses that failed; rather than tune a constant until the suite went green, the leg now asserts only the two invariants that are defensible — **no champion moves, no count shrinks** — and prints the magnitude for a reader to judge.

**THE ADVERSE-EXCURSION DISTRIBUTION IS CENSORED AT THE CARD'S OWN RAIL.** `mae_held_r` bottoms at **exactly −1.0000 R** with **110 of 196 campaigns (56%) piled on it**, while the uncensored tape reading reaches **−4.5891 R** and **124 campaigns gap through their stop.** Any decile or hazard statistic on held excursions reports the stop in its tail. **This matters directly to Phase B: P-AE-1 is pre-named off that hazard curve.**

---

## A · THE ADJUDICATION — ALL 39 FINDINGS

**Method.** Thirteen agents, each handed the findings file and the seven repairs already applied, each required to RUN the scenario before returning a class. A verdict not executed was not accepted. `CONFIRMED-DATA-AFFECTING` required an old number and a new number the agent had computed itself.

| # | verdict | finding | repair |
|---|---|---|---|
| 0 | **COSMETIC** | F-C6-WALL's 'independent 12h rebuild' uses a different bucket-completeness rule than production, and production adm… | Either make the completeness test require all three 4h bars of the bucket (and build h12/l12 from the bucket's own member indices instead of the po… |
| 1 | **COSMETIC** | The in-sample-argmax caveat is not on the registration result row, although the code and the report both claim it is | Copy `named_caveat` from `registration_text()` onto the matching scored rows in `score_registrations6` as one column (alongside `in_sample`), or de… |
| 2 | **REFUTED** | The answer's closing claim "there is no such distribution" is contradicted by the lab's own filed fingerprint row | — |
| 3 | **REFUTED** | `med_funding_r` — half the published suitability card and the "leaving 2" count — vanishes on the v5-control book t… | — |
| 4 | **REFUTED** | The outcome/explanatory segregation leaks: `pct_campaigns_zero_advance` is a perfect rank restatement of `win_rate_… | — |
| 5 | **REFUTED** | MATERIALITY_FLOOR_PCT = 20.0 is a one-point grid that decides the card, and no sweep is reported | — |
| 6 | **COSMETIC** | `selfcheck` never runs in the build, three L-ZEC tables are never filed — and the verbatim answer paragraph cites s… | In `tierc6.run`'s L-ZEC block, build the tables with `Z.all_tables(book_name)` instead of the five-key dict, then `put()` lzec_hz1_scope, lzec_hz5_… |
| 7 | **CONFIRMED-FIXED** | F-C6-LEAGUE's "mirror proof" never calls `league()`; no fixture leg constrains the SUPPORT side, and the support ch… | Optional hardening only: add mean_penetration_atr (and rejection_rate_pct) to the mirror's compared columns, and assert the FILED support rows equa… |
| 8 | **COSMETIC** | Equal-asset-risk weights are recomputed inside every slice, so the slice rows do not sum to the book and one campai… | Put the disclosure on the row: emit `ear_weights_recomputed_within_window=True` and `max_asset_weight` on every equal_asset_risk slice row, with on… |
| 9 | **REFUTED** | The declared selection surface is wrong for S-LIMIT (5 declared vs 10 built and filed), and F-C6-GRID stamps [OK] o… | — |
| 10 | **COSMETIC** | On equal_asset_risk rows `strip_best_net_r` is computed on the weighted contribution while `best_r` stays raw, so t… | On the equal-asset-risk row add a `strip_best_basis = "best weighted contribution (best_contrib_r)"` column, or add one sentence to agg_ear's docst… |
| 11 | **CONFIRMED-DATA-AFFECTING** | L-FMH counterfactual exits at the CLOSE of a bar the stop had already closed the campaign on — 173 impossible rows,… | In `fmh_lab` (scripts/tierc6_lab_misc.py:487) bound the signal search at `(t.exit_i - 1) if t.exit_reason == 'stop' else t.exit_i`, because under a… |
| 12 | **CONFIRMED-DATA-AFFECTING** | The wall-aware S-BUF cell [H4] reads UNFLOORED, seeded MH/H/VH/UH EMAs — the filed cell's net_r is wrong by 0.85 R … | In `band_context` (scripts/tierc6_lab_misc.py:1533-1536) floor the bands before caching — build each family from `ind.ema(c, L)` with `e[np.arange(… |
| 13 | **COSMETIC** | Three named verification tables — including the only leg that can detect a wrong harvest split — are never called b… | In `tierc6.run`'s L-MISC block hold the shadow frame (`sh = X.shadow_table(...)`) before `put`, then file `X.hfrac_enactment(sh.attrs['hfrac_cells'… |
| 14 | **CONFIRMED-FIXED** | F-C6-GRID cannot fail on any grid with no cards, and GRID_SIZES6 publishes 8 cells of grids TIER-C6 never builds or… | Drop the three grids this build never rides from GRID_SIZES6 (or keep them with a `ridden_in_this_build = False` marker) and correct the 'built by … |
| 15 | **COSMETIC** | L-WALLQ's `neither` bucket merges two opposite geometries — 11 of 28 campaigns have the wall INSIDE the campaign's … | Split `neither` into `inside_risk` (wall between stop and entry) and `beyond_2r` in wall_alignment's bucket order, or at minimum fix the docstring … |
| 16 | **CONFIRMED-FIXED** | F-C6-LEAGUE's "mirror proof" never runs T6.league's support branch — the whole support side of the filed league is … | Optional hardening only: add `mean_penetration_atr`/`mean_breakthrough_depth_atr` to `cmp_cols` (compare with a 1e-9 tolerance) so a support-side p… |
| 17 | **COSMETIC** | F-C6-ARM's "CARDINALITY" leg is x == x, and F-KEY's book-count leg compares three views of the same rebuilt book — … | Anchor the v6 campaign SET, not just its advancing subset: in F-C6-ARM assert `checked == sum(1 for t in B['v6'] if t.advances)` AND `len(B['v6']) … |
| 18 | **CONFIRMED-FIXED** | registrations.parquet publishes the D15 diagnostics for P-TRAIL-1 computed against itself — paired_delta_expectancy… | Already applied (C6-3). Only remaining tidy: drop the duplicate `paired_delta_expectancy` from the extra dict, since it now restates `paired_delta_… |
| 19 | **CONFIRMED-FIXED** | F-KEY names 9 of the 27 filed tables and put() silently skips empty frames — an entire lab table can disappear and … | Two lines in f_keys: fail the leg when `man['skipped_empty']` is non-empty unless the table is named in an explicit allow-list, and assert a per-ta… |
| 20 | **CONFIRMED-FIXED** | F-C6-GRID's three-way count is unconditionally true for 4 of 12 grids (16 of the 41 declared cells), and the two co… | Close the residual by checking the four OWNED_ELSEWHERE sizes against their owners' own constants instead of accepting any integer -- S-LIMIT again… |
| 21 | **COSMETIC** | F-C6-WALL hand-verifies 5 of 16 filed wall exits (head(3) per side) and never reconciles the count — a support-side… | Iterate over all of `wex` instead of `head(3)` (16 rows, well under a second) and assert `checked == len(wex)`; correct the module header to claim … |
| 22 | **REFUTED** | k* = 0.40 is a one-campaign argmax, and pre-registered clause (a) — the clause written to catch exactly that — is c… | — |
| 23 | **COSMETIC** | The lab's entire 14-leg selfcheck and its build() HALT have no caller anywhere in the estate; the four published L-… | In `tierc6.run`'s L-LIMIT block call `M.build(v6, lo_ms, hi_ms, champs=ch, card=RC.CARD_V6)` instead of the four table functions, file its `selfche… |
| 24 | **COSMETIC** | l_ae_deciles publishes the card's own stop rail as an adverse-excursion statistic: d5-d9, p90 and max are all exact… | Add to each ae_deciles row a `censored_at_the_rail_n` (= #{held == 1.0}) plus a one-sentence `censoring` stamp, and either file the mae_tape_r twin… |
| 25 | **CONFIRMED-DATA-AFFECTING** | The hazard curve's provisional/reportable guards are disabled by the same censoring, and F-C6-HZ-2 explicitly forbi… | Documentation-only: change 'None on 105 of 195 campaigns' at BUILD_2026-08-16_TIERC6_REVB.md:177 to 94 (the 105 is the v5-control book's count). No… |
| 26 | **COSMETIC** | There is no pre-registration artifact: write_prereg is never called, frontier is invoked with prereg_path omitted s… | In tierc6.py, call `p = M.write_prereg(OUT / 'l_limit_prereg.json')` BEFORE the frontier line and pass `prereg_path=p['path']` into `M.frontier(...… |
| 27 | **REFUTED** | P-LIM-2's declared 10-cell frontier is absent from the estate's only fixture-checked selection-surface total, which… | — |
| 28 | **CONFIRMED-FIXED** | league() redefines mean_penetration_atr; the "reproduces TC5's filed league, zero differences" claim is checked on … | Add `mean_penetration_atr` (and `rejection_rate_pct`, `longest_rejection_streak`) to the columns F-C6-LEAGUE leg (a) compares, so a future silent r… |
| 29 | **CONFIRMED-FIXED** | agg_ear publishes top_decile_share_pct on a different denominator from agg, side by side under one column name | Documentation only: BUILD_2026-08-16_TIERC6_REVB.md line 78 still warns that the column 'reads 260%-1123%' and line 297 still lists F-C6-e as 'Ruli… |
| 30 | **CONFIRMED-FIXED** | F-C6-GRID cannot fail for any declared grid that builds no cards — the leg passes on a 5,804-cell declaration again… | Optional hardening only: have the OWNED_ELSEWHERE branch compare the declared size against the owning module's own constant (e.g. tierc6_lab_limit.… |
| 31 | **CONFIRMED-FIXED** | The D15 diagnostic columns on the P-TRAIL-1 registration row are computed v6-against-v6, not against the v5 control… | None. (Cosmetic leftover: the '(reference)' row still carries d15(base,base) = 0.0/1.0/NaN, but it is labelled d15_measured_against = 'card v6' on … |
| 32 | **COSMETIC** | wall_series_12h admits an incomplete first 12h bucket, and F-C6-WALL's "independent rebuild" applies the stated rul… | Add the completeness test (`size == 3`) to wall_series_12h's `closed` filter — or restate the docstring as the time-closed rule it actually impleme… |
| 33 | **CONFIRMED-DATA-AFFECTING** | league() silently redefines mean_penetration_atr, breaking the "reproduces tierc5's filed league with zero differen… | In league(), accumulate the breakthrough count per row (len(depths)) and pool the panel depth on it — `_dep_w = mean_breakthrough_depth_atr * n_bre… |
| 34 | **CONFIRMED-FIXED** | The filed register publishes v5's exit distribution as v6's: "194 of 195 exits are stops" and "EXPECTED NEVER TO FI… | Already applied (tierc6_rules.py REGISTER['BELL_DISPOSITION'] is now card-scoped). No further action; the only residual is that register.parquet mu… |
| 35 | **CONFIRMED-FIXED** | P-WALL-1's "PROFIT-SIDE" wall is asserted in three docstrings and enforced nowhere; wall_touch takes `direction` an… | Cosmetic only: restate profit_side()'s docstring and P-WALL-1's registration_text so 'PROFIT-SIDE' reads 'the profit side's league champion length'… |
| 36 | **COSMETIC** | F-C6-MINADV's headline leg is the banned self-comparison: it re-derives advance_atr the way ratchet_ledger derived … | Give leg 1 content or delete it: rebuild advance_atr from the RIDE inputs (the confirming fractal pivot, buf_atr, rail_atr and the ATR at the confi… |
| 37 | **COSMETIC** | The halves-sum HALT is unreachable on every book the build ships, including all the S-HFRAC cells the q-generalisat… | Drop the `cap is None` clause (base_net is built from UNCAPPED funding, so a bound ceiling can never trip it) and, more importantly, replace the ta… |
| 38 | **COSMETIC** | F-C6-ARM's declared failure condition is not the one it tests, and the shipped book violates the declared one 11 times | Change the F-C6-ARM docstring's FAIL condition from 'at or before' to 'before', matching the code and the leg's own printed line, and add one sente… |

### A2 · THE TWO RULED CORRECTIONS, APPLIED

**F-C6-j — the BH family was declared 8 while the table printed 12 p-values.** m is now **DERIVED by counting the non-null p-values the table actually publishes**, so it cannot drift from the table again, the literal is kept beside it so a divergence is visible, and **the correction is applied rather than recorded**: every horizon gains a `_clears_bh_bar` column against a bar of q/m = **0.00833**.

**F-C6-e — the over-100% column is renamed AND recomputed.** A rename is only honest if the arithmetic follows the name, so `top_decile_share_of_positive_mass_pct` divides by the **positive** mass — bounded [0, 100] by construction and meaning the same thing under both aggregations. The old `top_decile_share_pct` is **nulled on equal-asset-risk rows with the reason on the row**, and kept on raw rows so the lineage still reconciles to Tier-C5's filed 77.1435.

### A3 · THE THREE RIDERS

**(i) THE SUPPLEMENT** — `research_outputs/tc6v/SUPPLEMENT.html` (29.6 KB) + parquet. **196 campaigns, 67 winners, net +39.7819 R.** An MAE-decile × MFE-decile cross-tab in both net R and count, then cuts by exit mechanism, asset, year, direction, and **winners and losers separately** — the losers are never dropped, which is the point of grouping at all. **Every excursion is printed twice**, held and tape.

**(ii) L-LAG** — the arm→trigger gap, in bars and ATR-time, by year, asset, direction and **by lag decile with the outcome attached**. The lag is massively tied: **49 of 196 campaigns trigger on the arming bar itself**, so decile 0 is empty under average-rank and the gate had to be cut by value, not by label. Fast triggers do look better — lag-0 campaigns return **+0.4149** expectancy at a 46.9% win rate against **−0.5796** for the 56-bar decile — but see below.

**(iii) `query_filter` v1** — a predicate DSL over a **named** feature table (3 predicates evaluated, each logged to a probe ledger with its m). A predicate naming an unknown column **raises**, because a silent empty selection is indistinguishable from a true negative. Every emitted table carries the D15 trio and is labelled *"a SELECTION, not a result"*. `F-QF` hand-verifies three predicates against direct pandas.

### P-LAG-1'S CONDITION ADJUDICATED ITSELF — AND IT IS NOT MET

The commission made P-LAG-1 conditional on the top-vs-bottom lag-decile delta excluding zero at cluster-90%. Measured: bottom (lag ≤ 0 bars, n=49) expectancy **+0.4149**, top (lag ≥ 71 bars, n=20) **+0.3534**, delta **+0.0616**, CI **[-0.7819, +0.9566]**.

**The interval does not exclude zero. P-LAG-1 is REPORT-ONLY, not registered, and m is unchanged.** The decile table looks like a finding and the ruler says it is not one — which is exactly what the condition was written to arbitrate, and it arbitrated against the interesting answer.

---

## B · TIER-C7 — NOT RUN

Phase B builds four registrations and a hybrid card **on top of the v6 book**. Two of the numbers that book publishes changed this morning, and one of them was a sign. Building the hybrid now would mean pinning P-AE-1's threshold to a hazard curve whose censoring was disclosed only after the threshold was named.

**Nothing of Phase B was started.** No `scripts/tierc7.py` exists, no registration text was written, and no arm was scored — so there is no half-built claim anywhere in the estate.

---

## C · FIXTURES AND INTEGRITY

**TIER-C6 fixtures 11/11 PASS** after every repair. **Estate suite: 334 passed, 1 skipped, exit 0.**

F-C6-CTRL still reproduces the parent trade-for-trade — **worst absolute difference 0.000e+00** across 13 columns on all 195 shared campaigns. F-C6-LEAGUE's mirror proof still calls the real function and is still sabotage-tested. F-C6-DET still hashes identical across two runs.

---

## D · FINDINGS — NOT FIXED

**TC6V-a · THE CORRIDOR MAKES EVERY PUBLISHED NUMBER DATED.** A pin exists but is used only for audit re-runs. **Ruling needed: does a build document state its corridor as a warranty (numbers valid only as-of) or does the estate re-run and restate on a cadence?**

**TC6V-b · THE CACHE IS NOT IMMUTABLE AND NOTHING SAID SO.** Filed parquets are not bit-reproducible after a refresh. **Ruling needed: freeze a cache snapshot per build, or accept and document boundary drift.**

**TC6V-c · THE AE CENSORING REACHES INTO PHASE B.** P-AE-1's 0.60R threshold was pre-named from a curve now known to be partly the card's stop. **Ruling needed: re-name the threshold from the uncensored tape distribution, keep it and score it as a card-conditional rule, or drop the arm.**

**TC6V-d · SIXTEEN COSMETIC FINDINGS ARE REAL AND UNFIXED** — among them: the pre-registration artifact is still never written to disk (`write_prereg` has no caller); the L-ZEC and L-LIMIT-2 self-checks still never run in the build; `F-C6-ARM`'s cardinality leg is `x == x`; `F-C6-MINADV`'s headline leg is a self-comparison; the halves-sum HALT is unreachable on every shipped book because every card carries a funding ceiling. **None moves a number. All weaken a check.** Ruling needed on whether TIER-C7 fixes them first.

---
## E · DISPOSITION + BOX-COST

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `scripts/tc6v_riders.py` | yes | yes | this push | yes | hand commit, explicit paths (CL-13) | 0 B, non-box |
| `scripts/tierc6.py` (repairs #33, F-C6-e, corridor pin) | yes | yes | this push | yes | same | 0 B, non-box |
| `scripts/tierc6_rules.py` (register text #34) | yes | yes | this push | yes | same | 0 B, non-box |
| `scripts/tierc6_lab_misc.py` (repairs #11, #12, F-C6-j) | yes | yes | this push | yes | same | 0 B, non-box |
| `scripts/tierc6_fixtures.py` (prefix-robust CTRL, pinned league) | yes | yes | this push | yes | same | 0 B, non-box |
| `research_outputs/tc6v/` (7 tables + SUPPLEMENT.html) | yes | **no — gitignored** | — | — | **NOT PROTECTED — local only** | n/a, off-bus |
| `research_outputs/tierc6/` (27 tables, restated) | yes | **no — gitignored** | — | — | **NOT PROTECTED — local only** | n/a, off-bus |
| `exchange/reports/BUILD_2026-08-17_TC6V_TIERC7.md` | yes | yes | publish | yes | publish guard, `exchange/**` scope | ≈ 22,500 B → 0.14% |
| `exchange/reports/BUILD_2026-08-16_TIERC6_REVB.md` (two corrections) | yes | yes | publish | yes | same | +1,900 B |
| `exchange/status/LEDGER_APOLLO.md` | yes | yes | publish | yes | same, append-only | +≈ 6,000 B |

### BOX-COST

**`BOX_BYTES` / `WARN_FRACTION` / `REFUSE_FRACTION` read LIVE from `publish_exchange` — never typed.**

| | before this paste | **after** |
|---|---:|---:|
| `exchange/**` | 3,218,725 B · 20.12% | **≈ 3,249,100 B · 20.31%** |
| **tick set** (`exchange/**` + `LEDGER.md`) — *governs* | 3,478,023 B · 21.74% | **≈ 3,508,400 B · 21.93%** |
| level | OK | **OK** (warn 40% / refuse 70%) · headroom to REFUSE ≈ **7.68 MB** |

**This paste ≈ 30,400 B ≈ 0.19% of the box — 38% of the < 0.5% (80,000 B) target.** A 39-row adjudication table is most of it, and it is the deliverable.

**THE NAMING TRIP-WIRE DID NOT FIRE FOR THIS BUILD'S OWN FILE** (≈ 22,500 B against the 64,000 B flag). It continues to fire on the eight pre-existing box-bound files, each already homed under CONVENTIONS §3.2; this paste adds to only one of them, `LEDGER_APOLLO.md`, which is append-only by design.

---

*End of Phase-A build document. TC6-V · 39 findings adjudicated · 4 data-affecting, all repaired · 2 published sentences corrected, one of them a sign · the corridor moves, the cache is not immutable, and the hazard curve is partly a stop · **PHASE B NOT RUN**.*

---

# B · TIER-C7 — THE HYBRID R&H PROGRAM

**RATIFIED** operator 2026-08-17, resume word **"TC7 GO"**, with **P-AE-1 ruled CARD-CONDITIONAL and the arm kept**.

## B0 · VERDICT FIRST — NOTHING CLEARED, AND TWO ARMS CLEARED UNTIL THE REVIEW

**All four registrations are NOT SUPPORTED. So is the card they were measured against.**

P-HYB-1 and P-CHAIN-1 **were SUPPORTED** — paired delta +0.2406 / +0.2403, CI [+0.115, +0.372], p = 0.00025, clearing BH at m = 4, **LOAO 5/5**. The pre-publication review reversed both, and it was right to.

| registration | prior | ruler | Δ point | 90% CI | p | verdict | LOAO | *paired would have said* |
|---|---:|---|---:|---|---:|---|---|---|
| **P-HYB-1** | 50% | TWO-SAMPLE | +0.1128 | [-0.0193, +0.2401] | 0.0862 | **NOT SUPPORTED** | 1/5 above | +0.2406 → *SUPPORTED* |
| **P-CHAIN-1** | 50% | TWO-SAMPLE | +0.1125 | [-0.0198, +0.2400] | 0.0862 | **NOT SUPPORTED** | 1/5 above | +0.2403 → *SUPPORTED* |
| **P-WEV-1** | 45% | paired | -0.0027 | [-0.0084, +0.0029] | 0.7521 | **NOT SUPPORTED** | 0/5 above | -0.0027 → *NOT SUPPORTED* |
| **P-AE-1** | 40% | paired | +0.0044 | [-0.0979, +0.1017] | 0.4379 | **NOT SUPPORTED** | 1/5 above | +0.0044 → *NOT SUPPORTED* |

*(reference)* card v6 vs zero: **+0.2030**, CI [−0.0132, +0.5022], p = 0.0740 — **NOT SUPPORTED**. **F-C5-b now survives into a third tier.**

### Why the two arms reversed

**A paired ruler is only legitimate for an arm that rides INSIDE the campaign set.** Tier-C5's own law: *"paired because the adds cannot change which campaigns exist — they ride inside one."* **The chain arms change the set.** A chain holds its asset's slot until its last leg exits, so **7 campaigns the control took never open — worth +25.58 R.**

And the bias is not neutral. When a chain's re-entry captures the very move the control booked as a *separate* campaign, the arm is **credited** for it inside the surviving twin while the control's campaign that captured the same move is **deleted from the comparison and never debited**.

**The sharp case, on ZEC.** The control takes two campaigns over 2026-04-23 → 2026-05-10 worth **+25.5692 R**. The hybrid takes one chain worth **+25.3148 R** — on that tape it is **0.2544 R WORSE**. The paired ruler credits it **+24.8061 R: 54.6% of the entire paired delta.** Across all 7 blocked slots the paired ruler credits **+29.3562 R where the account earned +3.7723 R**.

Scored on the estate's own two-sample asset-cluster bootstrap — the F-C5-n repair, a function this module **imported and called zero times** — the arms do not clear, and **the LOAO inverts from 5/5 to 1/5 with the single clearing panel being −ZECUSDT.** The published "5/5, they do not rest on ZEC" was true only of a subset that had deleted ZEC's crowded-out +25.06 R campaign. **On the whole book the hybrid is 6.82 R WORSE on ZEC** while being ZEC's largest paired contributor.

**Both rulers now print on every row.** The paired number is a true statement about the campaigns both books took; it is simply not the claim.

## B1 · THE ABLATION — AND THE WEAVE IS NOT THE MECHANISM

| rung | n | net R | paired marginal | re-entries | max 1-trade share |
|---|---:|---:|---:|---:|---:|
| FULL HYBRID | 189 | +59.6728 | +45.4748 | 79 | 0.5455 |
| RE-ENTRY ONLY (no weave) | 189 | +52.9615 | +38.1513 | 70 | 0.6502 |
| ladder-only | 196 | +39.8188 | +0.0369 | 0 | 1.0000 |
| v6 (control) | 196 | +39.7819 | +0.0000 | 0 | — |
| weave + re-entry | 189 | +59.6155 | +45.4175 | 79 | 0.5462 |
| weave-only | 196 | +39.2621 | -0.5198 | 0 | 2.0698 |

**The commissioned ladder could not separate the weave from the re-entry** — the only cell containing a re-entry also contained the weave. One unscored rung was added and it answers the table's own question: **the weave alone LOSES (−0.5198 R); re-entry alone earns +38.15 of the +45.42.** Of 79 re-entries, **67 follow a plain ladder-out and only 12 follow a weave.**

**L-WEAVE explains why.** Only **1 of 42** weave events fires while the campaign is in profit, against a base rate of **79.47% of open campaign bars in profit** — a **33.4× skew** on the same bars in the same walk, with mean unit move at an event bar of **−0.5630 R**. Both D-R3 clauses require the M-median *and* the fast ribbon to have turned against the trade; by then the position is under water. **The weave is a loss-side detector, not profit protection.** The commission's premise — weave events in open *profitable* campaigns — is very nearly an empty set, and that is the finding.

## B2 · THE SIZING — THE REPAIR THAT CAME FROM DISBELIEVING A GOOD NUMBER

D-R6 makes a chain one campaign, which decides the denominator but not the **size**. The first draft held one unit per leg, so a re-entry with a wider fresh stop took more risk on the same denominator.

**SOLUSDT 2023-10-16** re-entered at own-R **1.5264** against a chain R of **0.4391** — **3.5× the risk** — and booked its 17.89-point run as **+40.74 chain-R** when it was worth **+11.72 R** against the risk actually taken. **That one campaign was 75% of the arm's delta.**

Leg 2 is now sized **`chain_R / own_R`**: a stopped-out re-entry loses exactly 1.0 chain-R whatever its stop distance. The campaign books **+12.24 R**, the arm falls **+68.17 → +59.62**, concentration **0.7473 → 0.5462**. `L-RE` files the rejected reading explicitly labelled *not a result*, and reproduces both numbers independently.

**And the fixture that guarded it was algebra proving itself.** F-C7-CHAIN computed the size *in the fixture* and asserted an identity in its own variables — it passed at 2.22e-16 and **would have passed with the sizing deleted from the program.** It now reads the sizes `_account_chain` actually used, asserts they are the rule on all 79 chains, and proves the rule is **load-bearing** (79 of 79 legs carry a size ≠ 1.0).

## B3 · THE COMPONENT LABS

**S-STOPGRID [D-R7]** — diagnostic, nothing promotable, rail asserted on **784/784 campaigns, 0 violations**:

| cell | n | net R | expectancy | LOAO |
|---|---:|---:|---:|---|
| offset +0.00 ATR | 196 | +39.7819 | 0.2030 | 0/5 above |
| offset +0.25 ATR | 196 | +27.9566 | 0.1426 | 0/5 above, 5/5 BELOW |
| offset +0.50 ATR | 196 | +22.5202 | 0.1149 | 0/5 above, 5/5 BELOW |
| offset -0.25 ATR | 196 | +44.2973 | 0.2260 | 2/5 above |

**Tightening the initial stop helps and widening hurts** — and the LOAO line had to gain a direction to say so. `T7.loao` counted panels excluding zero in *either* direction, so the +0.25 and +0.50 cells read a perfect **5/5 while being reliably WORSE**. The halves are now split and the 3/5 line is taken on the *above* half only.

**L-ANCHOR** — 10 cells, informs future tuning only, the scored hybrid never uses this table's winner:

| cell | net R | expectancy | advances |
|---|---:|---:|---:|
| M-band-edge @ 0.50 ATR | +118.7489 | 0.6059 | 696 |
| M-band-edge @ 0.25 ATR | +117.2464 | 0.5982 | 652 |
| e26 @ 0.50 ATR | +72.3505 | 0.3691 | 311 |
| e26 @ 0.25 ATR | +69.4957 | 0.3546 | 282 |

The nominal winner is **M-band-edge @0.50 at +118.75 R, ~3× the pre-named prior** — and the lab flags the confound itself: the smooth-series anchors ratchet on nearly every confirming pivot (696 advances against the pivot's 228), so their gains come partly from a looser, later-moving stop rather than a better anchor. **That column is exactly why the no-promotion sentence rides all 10 rows.**

**L-RE** — the round trip won on **28 of 79 chains**; the wins are large and the losses small. **L-REGIME** names conditioning candidates for CENSUS-3, gated nowhere.

## B4 · FIXTURES

**11/11 PASS · estate suite 334 passed, 1 skipped, exit 0.**

`F-C7-CTRL`: card v7 with every knob at its default reproduces card v6 — **worst absolute difference 0.000e+00** across 13 columns, every exit reason matching. `F-C7-ARM`, `F-C7-WEV`, `F-C7-CHAIN`, `F-C7-AE` hand-verify from raw bars. **`F-C7-LABS` is new**: `_labs()` swallowed `ImportError` and a full run completed green with **three of four labs absent**, so a missing lab now fails the suite instead of decorating the log.

## B5 · FINDINGS — NOT FIXED

**A five-lens adversarial review ran before publication and confirmed 27 findings.** Three blockers and the journal cluster are repaired above. **The rest are real, unfixed, and listed rather than absorbed:**

**TC7-a · THE JOURNAL'S CHAIN COLUMNS WERE SPLICED ACROSS LEGS — REPAIRED, BUT THE CLASS IS THE POINT.** `mfe_r` divided leg 2's excursion by the chain's R without its size and published **57.31 R** of favourable excursion no position ever had (now 33.24). `stop_advanced_atr` and `ratchet_exit` measured leg 2's final stop against leg 1's entry anchor — **26 chains filed as ratchet exits had not trailed on the leg that exited, and 8 published a negative advance** (now 0). **14 chains that harvested were filed `harvested=False`** because the flag read leg 1 only. All four are fixed; the class — *a single-campaign record describing a two-position object* — is a standing hazard for anything that chains.

**TC7-b · `p = 0.00025` IS THE BOOTSTRAP'S FLOOR, NOT A MEASURED TAIL.** With 4,000 draws, 1/4000 = 0.00025 is the smallest p the ruler can express. Reporting it as though it were measured, and then reporting "clears BH at m=4" as independent corroboration of "LOAO 5/5", stacked three restatements of one draw. Moot now that both arms fail, **and it would not have been moot if they had passed.**

**TC7-c · P-HYB-1 AND P-CHAIN-1 ARE VERY NEARLY ONE TEST REPORTED TWICE.** They differ by the ladder anchor alone, worth +0.0369 R — yet both occupy slots in the m = 4 BH family, making the correction *looser* than the evidence warrants. **Ruling needed: does a family count claims filed or hypotheses that could independently fail?**

**TC7-d · F-C7-WEV CHECKS 3 OF 42 EVENTS AND CANNOT TELL D-R3 FROM THE READING THE REGISTER SAYS IS NOT TAKEN.** The strict-containment alternative and the k-window reading both pass the three sampled bars. A cardinality leg over all 42 is the fix.

**TC7-e · F-C7-GRID's LOAO LEG CANNOT FAIL, AND NOTHING ELSE EXERCISES `loao()`.** It asserts the column is a string.

**TC7-f · THREE LABS ARE RECORDED BUILT WHILE 10 OF THEIR 17 FRAMES ARE NEVER FILED** — including every cardinality self-check they carry. `F-C7-LABS` proves a lab *imports*; nothing proves its verification legs *ran*. This is the TC6-V finding recurring one level down.

**TC7-g · L-REGIME's BAND EDGES ARE WHOLE-CORRIDOR QUANTILES** — look-ahead of the kind the register rejects by name two rows earlier. The candidates are named, not gated, so nothing rests on it; the edges should be trailing.

**TC7-h · `weave_exits_hybrid` UNDERCOUNTS D-R3's FIRINGS BY 43%** — the manifest counts only chains whose *final* leg exited on a weave.

**TC7-i · THE RE-ENTRY GATE IMPLEMENTS ONE OF THE CARD'S TWO TIDE CLAUSES**, contradicting `reentry_close`'s own docstring.

**TC7-j · AN AGENT MUTATED THE REPOSITORY DURING THE REVIEW.** A sabotage patch — `return pd.DataFrame()` — was left at the top of `regime_table` in `scripts/tierc7_lab_regime.py` after a lens tested whether the fixtures catch a silently-empty commissioned table. **They do**: F-KEY's totality leg failed on the stale parquet with no declared key. The patch was found, removed, and the tree re-verified clean; the decision path was confirmed byte-behaviourally intact. **Recorded because a review that edits the thing it reviews can invalidate its own result, and the next commission should run its reviewers against a read-only worktree.**

---

## C · DISPOSITION + BOX-COST — TIER-C7

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `scripts/tierc7_rules.py` | yes | yes | this push | yes | hand commit, explicit paths (CL-13) | 0 B, non-box |
| `scripts/tierc7.py` | yes | yes | this push | yes | same | 0 B, non-box |
| `scripts/tierc7_fixtures.py` | yes | yes | this push | yes | same | 0 B, non-box |
| `scripts/tierc7_lab_{stopgrid,weave,chain,regime}.py` | yes | yes | this push | yes | same | 0 B, non-box |
| `research_outputs/tierc7/` (16 tables) | yes | **no — gitignored** | — | — | **NOT PROTECTED — local only** | n/a, off-bus |
| `exchange/reports/BUILD_2026-08-17_TC6V_TIERC7.md` | yes | yes | publish | yes | publish guard, `exchange/**` scope | ≈ 34,000 B → 0.21% |
| `exchange/status/LEDGER_APOLLO.md` | yes | yes | publish | yes | same, append-only | +≈ 7,000 B |

### BOX-COST

**Constants read LIVE from `publish_exchange` — never typed.**

| | before | **after** |
|---|---:|---:|
| `exchange/**` | 3,268,303 B · 20.43% | **≈ 3,288,000 B · 20.55%** |
| **tick set** — *governs* | 3,529,893 B · 22.06% | **≈ 3,549,600 B · 22.19%** |
| level | OK | **OK** (warn 40% / refuse 70%) · headroom to REFUSE ≈ **7.65 MB** |

**This paste ≈ 19,700 B ≈ 0.12% of the box — 25% of the < 0.5% target.**

**THE NAMING TRIP-WIRE DID NOT FIRE FOR THIS BUILD'S OWN FILE.**

---

*End of build document. TC6-V + TIER-C7 · 39 audit findings adjudicated, 4 data-affecting · 27 review findings confirmed, 3 blockers · two arms SUPPORTED until the ruler was corrected, then none · the weave is not the mechanism · and the fixture guarding the largest repair was algebra proving itself.*
