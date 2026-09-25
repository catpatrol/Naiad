# TC11 SCOUT · SUBSYSTEM D: STATISTICS, SCORING, THE NULL, REGISTRATIONS

Scout: read-only map for the HEPHAESTUS executor of TIER-C11. The contract is
`exchange/queue/2026-09-24_TC11_APOLLO.md` (103 lines, read in full). The TC10 base is
`exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md`. Branch `v12-v1-census`.
Everything below was read from source on 2026-09-24. Signatures and constants were re-checked by
importing `tierc10_panel` against the frozen snapshot. Nothing was scored or written, apart from this file.

---

## 0 · Summary: what to build against

- **All statistics and scoring live in `scripts/tierc10_panel.py` (imported as `TP`).**
  The bootstrap primitives come from `scripts/tierc5.py` through `tierc6` and `tierc7`.
  `analytics/stats.py` is **irrelevant**: it holds only three rolling causal helpers (`zscore`,
  `correlation`, `beta`, 69 lines) and has no bootstrap, CI, or test.
- **`scripts/tierc10_score.py` is a TC10-hardwired driver.** It is useful as a pattern and for a
  few pure helpers, but it cannot drive TC11 as it stands (§6, gap G3).
- **The only resampling is the asset-cluster bootstrap.** There is no block or time bootstrap,
  and there are no campaign-level draws. Clusters are `trade.symbol`. `N_BOOT = 4000`. The CI is
  90% percentile (5th and 95th), and `p_one_sided = (#draws <= 0 + 1)/(n_finite + 1)`.
- **The verdict column in code is CI-only:** SUPPORTED iff `ci_lo > 0`, strictly. The BH bar and
  LOAO are separate columns. Which of the three clauses gate is set by each registration's TEXT.
- **The null of record (R10) is `gaps+order`.** It is a Tier-E random-box permutation null for
  range EVENTS, not for trade books. It yields a percentile of the real value among K=20 draws,
  "never a p-value". It has no base rate, no per-direction split, no lens-above conditioning, and
  covers only the lenses 5m, 4h and 1d.
- **Two blocking code gaps for m = 9:**
  - `TP.score` / `run_cell_n` / `LN.run_lane` call `require_registered` without `family_m`. Its
    default was bound to 6 at definition time, so a filing made with m = 9 HALTs.
  - The canonical registry is hard-wired to `research_outputs/tierc10/registrations`. See G1 and G2.

---

## 1 · Where things live (file:line)

| what | where |
|---|---|
| `SEED=20260921`, `SEED_LINEAGE=20260816` (sensitivity), `N_BOOT=4000` | `scripts/tierc10_panel.py:91-94` |
| `REG_DIR = OUT/"registrations"` (`OUT = research_outputs/tierc10`), `REGISTRY="REGISTRY.jsonl"` | `tierc10_panel.py:96-100` |
| `FAMILY_M = 6` | `tierc10_panel.py:103` |
| `LEANS` L1..L8 (L4 horizons, L6 above-half, L7 FDR, L8 seeds) | `tierc10_panel.py:113-142` |
| `LEAN_PANEL_VERDICT` (RAW carries the verdict; EAR rides beside) | `tierc10_panel.py:150` |
| `substrate()` (refuses the live cache and requires the loaders bound to the env) | `tierc10_panel.py:161` |
| `AS_OF_PIN = OUT/"data"/"AS_OF_PIN.json"` (2026-09-21T16:00:00Z, close ms 1790006400000) | `tierc10_panel.py:240` |
| `corridor_n(panel, pin_close_iso=None, floor_bars=316)` | `tierc10_panel.py:650` |
| `ERA_CUT_ISO="2024-06-30T23:59:59Z"`, `ERA_CUT_MS=1719791999000`, `ERAS=("full","tuning","holdout")` | `tierc10_panel.py:746-748` |
| `era_window(era)`: tuning=(None, CUT], holdout=(CUT+1, None) | `tierc10_panel.py:759` |
| `in_era(ms, era)` / `corridor_era(panel, era, pin_close_iso=None)` | `tierc10_panel.py:771` / `:784` |
| `CONTROL_CARD = T8.Card(name="v6-control")`, `RULERS`, `RUNNERS`, `BASES`, `CONTROL_ARM="(control)"` | `tierc10_panel.py:816-821` |
| `LOAO_LINES=("lineage","excl_zero_campaign")`, `loao_line_clause()` | `tierc10_panel.py:829-841` |
| `class Book(list)` (`.spec` = provenance; lost on slice, filter or `+`) | `tierc10_panel.py:844` |
| `ride_spec(card, roles)`, `CONTROL_RIDE` | `tierc10_panel.py:874`, `:882` |
| `arm_spec(...)` / `_check_spec` / `_require_loao_line` / `_require_era` | `tierc10_panel.py:894` / `:976` / `:1018` / `:1045` |
| `is_control_book(card, roles, panel)` (v6 on a CLASSIC5 subset only) | `tierc10_panel.py:1083` |
| `run_cell_n(card, roles, panel, lo_ms, hi_ms, reg_id=None, text=None, reg_root=None, arm=None, head_of_record=None) -> Book` | `tierc10_panel.py:1095` |
| `above_half_bar(N) = ceil((N+1)/2)`: 3/5, 7/12, 9/17, 2/3 | `tierc10_panel.py:1193` |
| `loao_n(new, base, panel, two_sample=False, seed=SEED, label="", n_boot=N_BOOT)` | `tierc10_panel.py:1234` |
| `ear_expectancy`, `cluster_boot_ear`, `cluster_boot_ear_diff` (equal-asset-risk, new in TC10) | `tierc10_panel.py:1351` / `:1361` / `:1392` |
| `_verdict(ci)` | `tierc10_panel.py:1416` |
| `co_headline(book, seed, n_boot)`, `headline_n(book, label, panel, seed)` | `tierc10_panel.py:1437` / `:1464` |
| `_seed_pair(seed)` returns (seed, 20260816), or (20260816, 20260921) if seed == 20260816 | `tierc10_panel.py:1506` |
| `_payload`, `_payload_sha`, `_registry_lines`, `_chain_ok`, `registry_head`, `_check_head` | `tierc10_panel.py:1539-1672` |
| `register(reg_id, text, prior_pct, arms=None, family_m=6, fields=None, root=None)` | `tierc10_panel.py:1674` |
| `require_registered(reg_id, text, root=None, family_m=6, head_of_record=None)` | `tierc10_panel.py:1800` |
| `require_arm(reg_id, text, arm, panel, lanes=None, head_of_record=None, root=None, family_m=6)` | `tierc10_panel.py:1834` |
| `external_book(trades, gate, lo_ms=None, hi_ms=None) -> Book` | `tierc10_panel.py:1900` |
| `registration_table(root=None)` | `tierc10_panel.py:1939` |
| `_book_sha(book)` = sha256 of sorted [symbol, lane, entry_ms, repr(net_r)] | `tierc10_panel.py:1988` |
| `_mark_scored(rec, root, arm, stamp)` (irreversible `.scored.json`) | `tierc10_panel.py:1998` |
| `_set_change_law(ruler, changes)` / `_rule(book, base, ruler, seed, n_boot)` | `tierc10_panel.py:2039` / `:2062` |
| `_bind_arm(rec, arm, panel, ruler, scored_in_family, book, base)` | `tierc10_panel.py:2090` |
| **`score(reg_id, text, book, panel, base=None, ruler="vs_zero", seed=20260921, arm=None, scored_in_family=True, note="", root=None, n_boot=4000, head_of_record=None, era=None) -> dict`** | `tierc10_panel.py:2173` |
| `reference_row(base, seed, n_boot)` (control only, excluded from m) | `tierc10_panel.py:2412` |
| **`finish_family(rows, family_m=6, canonical_only=True) -> DataFrame`** | `tierc10_panel.py:2465` |
| `LENS_MS`, `lens_edge`, `stamp_n(df, meta, lens="4h", lens_last_closed_ms=None)`, `AS_OF_COLUMNS` | `tierc10_panel.py:2511-2561` |
| `make_put(root, meta, lens)`, `grid_whole(...)` (F-GRID), `check_keys(...)` (F-KEY), `check_det(a,b)` (F-DET), `input_sha(panel)` | `tierc10_panel.py:2563` / `:2592` / `:2628` / `:2661` / `:2692` |
| `cluster_boot(values, clusters, seed=20260816, n_boot=4000)` (draws of the MEAN) | `scripts/tierc5.py:1178` |
| `cluster_boot_diff(va, ca, vb, cb, seed=20260816, n_boot=4000)` (the same asset draw into both books) | `scripts/tierc5.py:1200` |
| `_ci_from(draws, point) -> {point, lo(5th pct), hi(95th pct), p_one_sided}` | `scripts/tierc5.py:1227` |
| `FDR_Q = 0.10` | `scripts/tierc5.py:1156` (re-exported as `T7.FDR_Q`, then `TP.FDR_Q`) |
| `agg(trades, label, key, extra)` / `d15(cell, base)` (the D15 trio) | `scripts/tierc5.py:557` / `:579` |
| cohort-vs-complement interval with a 3-asset cluster floor: `_stat(values, clusters, comp_values, comp_clusters)` | `scripts/tierc7_lab_regime.py:910`; `CI_PCT=90` at :182, `CLUSTER_FLOOR=3` at :183 |
| TC7 CONDITIONAL-registration precedent (P-LAG-1) | `scripts/tierc7.py:923-927` |
| Scoring driver (TC10) | `scripts/tierc10_score.py` (1614 lines), CLI at `:1539` |
| Registration clerk (TC10) | `scripts/tierc10_file_registrations.py` (175 lines) |
| Null model | `scripts/tierc10_null.py` (1085 lines) + `tierc10_null_fixtures.py` |
| Census functions the null reuses | `scripts/tierc10_census.py` (imported as `C`) |
| Tier-E collar implementations | `scripts/tierc10_census.py:351-363, 1552-1591`; `scripts/tierc10_close_regime_prior.py:149-164, 627-660`; `scripts/tierc10_close_p_age_1_tide_youth.py:149-157, 420-432` |

Import chain and substrate: `tierc2_baseline` binds `KLINES`/`FUNDING` at import from `engine.data.cache_dir()`, so
`NAIAD_CACHE_DIR` must be exported before python starts. `TP.substrate()` then refuses the live cache.
`import tierc10_census` (and therefore `tierc10_null`) runs `assert_substrate()` at import
(`tierc10_census.py:72-96`). It **HALTs unless NAIAD_CACHE_DIR == `~/.cache/naiad/snapshots/tc10_20260921`** exactly.

---

## 2 · The rulers: exactly what is computed

### 2.1 · Common machinery
- **Cluster = asset** (`t.symbol`). `uniq = np.unique(clusters)` gives K. Each draw is
  `rng.choice(uniq, size=K, replace=True)` with `rng = np.random.default_rng(seed)`. That seeded
  stream is shared by the raw ruler, the two-sample ruler and the EAR ruler, so under one seed they
  see the same asset draws.
- The statistic is the **mean** of `net_r`. This is deliberate: an expectancy claim is a mean
  (`tierc5.py:1159-1175`).
- **CI:** `_ci_from` takes the finite draws only (EAR draws can be NaN). `lo = percentile 5` and
  `hi = percentile 95`, so the "cluster-90% interval" is this CI.
- **p:** `p_one_sided = (sum(d <= 0) + 1) / (len(d) + 1)`. It is **upward** one-sided, i.e.
  P(effect not positive). The minimum is 1/4001 = 0.00024994. No downward p exists anywhere.
- **Seeds:** the ruler seed is passed to `TP.score(seed=...)`, and the sensitivity seed is
  `_seed_pair(seed)[1]` = 20260816. Both are on every row (`seed`, `sens_seed`, `sens_ci_*`,
  `sens_verdict`, `verdict_stable_across_seeds`). **TC11 should pass `seed=20260924`**; the TC10
  driver passed `TP.SEED` (20260921).
- **Too few clusters:** in `loao_n` a leave-out panel with fewer than 2 values or fewer than 2
  distinct assets returns "too few clusters" (no CI). `TP.score` has no floor. The TC7 lab `_stat`
  refuses an interval below 3 assets (C(2K-1,K) resamples: K=2 gives 3, K=3 gives 10, K=5 gives 126).

### 2.2 · `_rule` (`tierc10_panel.py:2062`)
- **vs_zero:** `ci = _ci_from(cluster_boot(rs, symbols, seed), mean(rs))`.
- **With a base:**
  - The pairing key is **`(symbol, lane, entry_ms)`**. `pv` is the per-campaign deltas
    `net_r_arm - net_r_base` over the matched keys.
  - `changes = len(base) > len(pv) or len(book) > len(pv)`.
  - `ci_p` = the one-sample cluster bootstrap of the paired deltas (clustered by symbol).
  - `ci_2 = cluster_boot_diff(book, base)`, with point `mean(book) - mean(base)`.
  - `ci = ci_2 if _set_change_law(ruler, changes) else ci_p`.
- **`_set_change_law`:**

  | ruler | scored two-sample? |
  |---|---|
  | `vs_zero` | never |
  | `two_sample` | always, and its premise is measured: `score()` HALTs if the key sets are identical (P-BE-1 died on this) |
  | `set_change` | two-sample iff `changes`, else PAIRED |

- **There is no ruler that forces PAIRED on a changed set.** The `paired_ci_*` columns are always
  printed beside it (on the matched subset only).
- `d15(book, base)` pairs on `(symbol, entry_ms)`, **without lane**. `_rule` pairs WITH lane.
  **Keep `t.lane` identical to the base's `"card"`** or the paired ruler sees zero pairs.

### 2.3 · LOAO (`loao_n`, `:1234`)
- One panel per declared asset (sorted), each re-scored by **the same ruler as the headline**:
  vs_zero, two_sample via `cluster_boot_diff`, or paired via the deltas.
- For each panel: `excludes_above = ci_lo > 0` and `excludes_below = ci_hi < 0`.
- `loao_line` reads `"{n_above}/{N} above[, {n_below}/{N} BELOW]"`.
- The bar is `above_half_bar(N)` (strict majority). Only "above" panels count.
- **Two counts:**
  - `lineage`: N = the declared panel, and a zero-campaign asset's panel counts against the line.
  - `excl_zero_campaign`: `loao_above_excl_zero_campaign_panels`.
- The registration names one count. It becomes `loao_line_of_record` / `loao_above_of_record` /
  `loao_clears_line_of_record`.

### 2.4 · Equal-asset-risk co-headline
`ear_*` columns: the mean of per-asset means, bootstrapped on the same asset draw. It **gates
nothing** (`LEAN_PANEL_VERDICT`). `co_headlines_disagree` compares verdicts, not signs.

---

## 3 · Verdict, family bar, the three clauses, vocabulary

### 3.1 · The three clauses
- **Code verdict (`_verdict`, `:1416`):** `"SUPPORTED" if ci["lo"] is not None and ci["lo"] > 0 else "NOT SUPPORTED"`.
  It reads NOTHING else: not the point, not p, not LOAO. On a twin ruler the CI is the CI of the
  **Δ vs v6**.
- **The family bar (`finish_family`, `:2465`)** adds these columns to every row:
  - `fdr_m_declared = family_m`
  - `fdr_m_tests_actually_run` (count of scored_in_family rows)
  - `fdr_bar_q_over_m = 0.10/m`
  - `clears_bh_bar = (p_one_sided <= bar)` on scored rows, `None` on Tier-E rows
  - `fdr_note`
- **How the bar is applied:**
  - It is **one fixed bar, with no ranks and no step-up.**
  - Running fewer tests than declared never loosens it. Running more than declared HALTs.
  - One scored row per registration; a duplicate HALTs.
  - A non-canonical-registry row HALTs unless `canonical_only=False`.
  - For m = 9 the bar is **0.10/9 = 0.0111111**.
- **The three clauses** (TC10 language, `research_outputs/tierc10/BUILD_DRAFT.md:84-90, 170-177, 197-203, 217-222`):
  - **(a)** `ci_lo > 0` (the `verdict` column)
  - **(b)** `p_one_sided <= q/m` (`clears_bh_bar`, from FAMILY)
  - **(c)** `loao_clears_line_of_record` (LOAO line of record at or above the above-half bar)
- **Which clauses GATE is set by each registration's filed TEXT, not by code:**
  - P-GEN-1 §6, P-BRK-I1 and P-BRK-S1 §5 required all three.
  - P-TRG-2 §5/§8 and P-SPR-2 §7 were **CI-only**, with LOAO and BH "REPORTED BESIDE THE VERDICT,
    AND DECIDING NOTHING".
  - P-TRG-2 was recorded as "SUPPORTED (CI-only); LOAO and BH beside, both clear". The "three-clause
    pass" framing was corrected as finding #1 (`BUILD_DRAFT.md:1197-1198`).
  - **The TC11 texts must say which rule they use.**
- **The P-TRG-2 row of record:** n 198 vs base 200. Δ +0.257697, CI [+0.108587, +0.383892],
  p 0.005249 ≤ 0.016667, LOAO 5/5 above (4/5 at the sensitivity seed). Ruler TWO-SAMPLE: 19 paired,
  179 book-only, 181 base-only (`scores/P-TRG-2.rows.json` rows[0]).

### 3.2 · Verdict vocabulary actually in use
| label | source |
|---|---|
| `SUPPORTED` / `NOT SUPPORTED` | `TP._verdict` only |
| **HALT** | any door or premise failure. The HALT string is recorded verbatim, with no point, CI or p. Example: P-BE-1 "the arm shares the WHOLE campaign set with its base; the commissioned two-sample ruler's premise failed". FINISH records it as `scored_slots_halted`, and the slot finishes only when named by `--allow-halted-slot`. TC10 wording: "HALT — NO VERDICT, PRESCRIBED". |
| "NOT SUPPORTED — CI WHOLLY BELOW ZERO" | prose only (P-BRK-S1). `BUILD_DRAFT.md:222`: **"'Significantly negative' is not a registered reading. The filed test is one-sided upward."** Downward evidence exists only as `ci_hi < 0` and `loao_excluding_below`. |
| `verdict_stable_across_seeds`, `co_headlines_disagree` | flags only |

### 3.3 · Holdout-era scoring
- The era is a mandatory, hashed part of every arm (`arm_spec(era=...)`).
- It is checked at the doors: `run_cell_n` / `run_lane` window vs `era_window`, `external_book`
  on every `entry_ms`, and `score()` on every campaign of book AND base.
- An era offered to `score(era=...)` that differs from the filing HALTs.
- Ride the window from `TP.corridor_era(panel, era)`, which uses the 4h grid. The holdout window
  starts at the first 4h bar opening at or after 2024-07-01T00:00Z. Membership is by `entry_ms`
  against the instant, not by bar.
- The base must be ridden over the **same (lo, hi)**. `_bind_arm` HALTs on "base: ridden over a
  DIFFERENT window than the book".

---

## 4 · The score row (`TP.score` returns 107 keys; verified on `scores/P-TRG-2.rows.json`)

| group | keys |
|---|---|
| identity | registration, arm, arm_runner, arm_base, arm_lanes, prior_pct, scored_in_family, note, registration_seq, registration_sha256 |
| era | arm_era, era_cut_iso, era_window_lo_ms, era_window_hi_ms, era_first_entry_ms, era_last_entry_ms, era_note |
| headline | n, expectancy_r, net_r, panel_name, n_panel_assets, assets_present, ruler (human), ruler_commissioned, ruler_is_two_sample, set_changes_measured, ci_point, ci_lo, ci_hi, p_one_sided, verdict |
| both rulers | paired_ci_point/lo/hi, two_sample_ci_point/lo/hi, paired_n, unpaired_base_n_lane_keyed, unpaired_base_net_r, whole_book_difference_r |
| EAR | ear_expectancy_r, ear_base_expectancy_r, ear_ci_point/lo/hi, ear_p_one_sided, ear_verdict_would_be, ear_n_finite_draws, sens_ear_ci_lo/hi, co_headlines_disagree, ear_ci_is_new, verdict_carried_by |
| LOAO | loao_panels, loao_excluding_zero/above/below, loao_line, loao_bar_above_half, loao_clears_above_half, loao_clears_3_of_5 (N=5 only), loao_sign_note, loao_detail, loao_worst_drop, loao_mode, loao_seed, loao_label, loao_panel_name, loao_assets_present, loao_zero_campaign_assets, loao_above_excl_zero_campaign_panels, loao_clears_excl_zero_campaign_panels, loao_zero_campaign_note, **loao_line_of_record, loao_above_of_record, loao_clears_line_of_record** |
| D15 (None on vs_zero) | n_paired, paired_delta_expectancy_r, **tail_exit_ratio** (the top-decile MEAN of cell ÷ base: "the D15 tail ratio" P-TP-RNG must print), max_single_trade_delta_share, unpaired_cell_n, unpaired_base_n, d15_note |
| seeds | seed, n_boot, sens_seed, sens_ci_lo/hi, sens_p_one_sided, sens_verdict, sens_loao_line, sens_loao_seed, verdict_stable_across_seeds, seed_note |
| provenance | book_sha256, base_sha256, book_gate_attested, book_window_lo_ms/hi_ms, registration_root_is_canonical, registry_len, registry_head, registry_head_pinned, registry_pin, registry_pin_covers_seq |

---

## 5 · Registrations: frozen, filed, hashed

### 5.1 · The pipeline in TC10
1. **Texts are drafted into `research_outputs/tierc10/REGISTRATION_TEXTS.json`.** It is the text of
   record, read verbatim by everything. The `.md` beside it is an older review render; its text shas
   (e.g. `a4ef625b…` for P-GEN-1) differ from the filed ones, so **do not read texts from the .md**.
   JSON schema, one per id:
   `{"reg_id": str, "prior_pct": int, "text": str (13k–32k chars), "arm_spec_calls": [str, ...], "above_half_bar": int}`.
   `arm_spec_calls` is literal Python source for each arm, for example:
   `'arm_spec(arm="trg-9/12 vs card v6 · CLASSIC5 · full", panel=tierc10_panel.CLASSIC5, ruler="two_sample", scored_in_family=True, lanes=("card",), card=tierc10_panel.CONTROL_CARD, roles=tierc9.Roles(name="trigger-9/12", trg_f=9, trg_s=12), base="card-v6", loao_line="lineage", era="full")'`.
   The score driver rebuilds card and roles from it, and they must round-trip `ride_spec`.
2. **`research_outputs/tierc10/REGISTRATION_PLAN.md`** pins the STRUCTURE before any text: panel,
   N, bar, era, ruler/base, runner, lanes, and which arm owns the slot.
3. **Filing** is `scripts/tierc10_file_registrations.py`:
   - It is a dry run by default; `--file` files.
   - `ORDER` is fixed (`:32`), in the contract's order.
   - `arms_for(rid)` (`:41`) builds the arms with `TP.arm_spec` in code, so no hand-written dict is used.
   - It refuses outright if any `*.scored.json` exists.
   - `TP.register(rid, text, prior_pct, arms=..., family_m=TP.FAMILY_M)` is called per id.
   - It then writes **`research_outputs/tierc10/REGISTRY_PIN.json`**:
     `{tier, stage, as_of_of_record, seed, family_m, n_boot, order_of_filing, registry_len, registry_head, registrations:{rid:{seq, sha256, text_sha256, prior_pct, already_filed, registry_len, registry_head}}, witness_law, texts_artifact}`.
   - `research_outputs/tierc10/**` is gitignored, so the pin must be committed with `git add -f`
     (WITNESS_LAW, `tierc10_panel.py:1515`).
4. **`register()` refuses a filing** that:
   - has an id not matching `^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$`
   - has empty text
   - has no arms
   - has more than 1 scored arm
   - is missing loao_line or era on any arm
   - has loao_line differing across arms
   - has a **TEXT that does not contain the literal `"LOAO LINE OF RECORD: lineage count"` (or `"LOAO LINE OF RECORD: excl-zero-campaign count"`) and no other**
   - has a filed id with different bytes, a filed id whose file is gone, or an id with `.scored.json`

### 5.2 · On-disk schemas (`research_outputs/tierc10/registrations/`)
- **`<REG>.json`:**
  `{registration, text, prior_pct:int, family_m:int, book_spec:{arms:[arm,...]}, fields:{}, seq:int, text_sha256, sha256, sha_law}`.
  - `sha256 = sha256(json.dumps({registration,text,prior_pct,family_m,book_spec,fields}, sort_keys=True, ensure_ascii=False))`
  - `text_sha256 = sha256(text)`
  - The keys of an **arm** are `{arm, scored_in_family, panel[list], panel_name, lanes[sorted list], ruler, base, runner ("run_cell_n"|"external"), loao_line, era}`, plus `ride` for run_cell_n arms: `{card_class, card_fields{all 29 as repr}, roles_class, roles_fields{6}}`.
- **`REGISTRY.jsonl`** has one line per filing:
  `{seq, registration, sha256, prev ("GENESIS"|previous line_sha256), line_sha256 = sha256(json.dumps({seq,registration,sha256,prev}, sort_keys=True))}`.
  The TC10 head is `7621a857…`, with len 6.
- **`<REG>.scored.json`** is written by the first `TP.score`:
  `{registration, seq, registration_sha256, arms:{arm:{book_sha256, base_sha256, n, seed, n_boot}}, law}`.
  A re-score must reproduce it, or it HALTs. A result's existence forbids any (re)filing.
- **Doors take the pin:** `head_of_record=(registry_len, registry_head)` is required under the
  canonical registry. The literal `"UNPINNED"` is an explicit opt-out that rides the row. A pin
  shorter than the registration's seq HALTs as "STALE PIN".

### 5.3 · What "[40%]" means
- It is **`prior_pct`**, the drafter's or operator's subjective probability that the hypothesis is
  SUPPORTED, stated at filing.
- It is an int and part of the hashed payload, and it is printed on every row (`prior_pct`).
- **Nothing computes with it:** there is no Bayesian update and no weighting. The texts say so,
  e.g. P-SPR-2: "the 45% prior is a statement about the operator's belief at filing and is not a
  prediction of the row".

### 5.4 · CONDITIONAL registrations
- **TC10 had none.** The only precedent is TC7's P-LAG-1 (`scripts/tierc7.py:923-927`): "P-LAG-1
  was CONDITIONAL and its condition was evaluated in TC6-V and NOT MET … so it is report-only, is
  not a test, and m is unchanged".
- TC7 then used **m = tests actually run** (`bar = FDR_Q / m` with `m = len(tested)`). That is the
  opposite of TC10's declared-m law.
- **No code path exists for "condition not met, no slot spent"** (gap G4):
  - `tierc10_score.finish_gate` (`:1491`) demands, for every id in order, a rows file with exactly
    one canonical scored row, or a recorded scored-arm HALT named by the operator.
  - `TP.finish_family` would accept 8 of 9 scored rows (8 ≤ 9) and keep bar = 0.10/9.

---

## 6 · The scoring driver: `scripts/tierc10_score.py`

**CLI** (`main`, `:1539`):

| flag | behaviour |
|---|---|
| `--dry-run` (default) | rides and binds every filed arm and prints per-arm facts. It never calls `TP.score`, writes no `.scored.json`, and prints no outcome. `OUTCOME_TOKENS` are scanned for by F-SC-NOSCORE. Transcript: `--out T.txt`. Per-arm record: `--json-out D.json`, keys `{law, arms[{registration, arm, arm_index, seq, door, runner, ruler, base, lanes, era, window, window_ms, panel_name, n_panel, n_campaigns, per_asset, per_lane, zero_campaign_assets, keys{n_paired, n_book_only, n_base_only, n_pair_score_law, moved}, book_sha, base_sha, book_content_sha, base_content_sha, base_n, base_per_asset, bind_checks, bind_ok, bind_halt, halt, loao_bar, loao_line, book_spec, card, scored_in_family}], beside_registration, halts}` |
| `--score --only REG...` | runs `TP.score` on every filed arm, in filed order |
| `--stage B-CORE` / `--stage B-5M` | TC10-specific staging |
| `--finish` | runs `TP.finish_family(family_m=TP.FAMILY_M)` |
| `--expect D.json` | refuses any Book whose `(book_sha, base_sha)` differs from the reviewed dry run |
| `--continue-after-scored-halt`, `--allow-halted-slot REG...` | operator's word |

`TP.substrate()` runs first.

**`score_registration`** (`:1284`):
- Pass 1 rides every arm (door first) and checks the Books before anything is scored.
- Pass 2 calls `TP.score(..., seed=TP.SEED, head_of_record=reg["head"], era=arm["era"])`.
- It attaches `beside` = {per_asset_n, per_asset_rows (`TP.headline_n`), haircut_twin (`haircut_twin_block`, `:1204`), …}.
- It files **`research_outputs/tierc10/scores/<REG>.rows.json`**:
  `{registration, seq, registration_sha256, registry_head_of_record, as_of_last_closed_4h, seed, n_boot, law, rows:[{arm, score_row, beside, scored_in_family} | {arm, halt, at, scored_in_family, text_prescribes, beside?}], beside_registration}`.
- It refuses to overwrite a rows file with different bytes. Return codes: 0 all rows, 3 a Tier-E
  HALT, 2 the scored arm HALTed.

**`finish`** (`:1451`) files **`scores/FAMILY.json`**
`{family_m_declared, fdr_bar_q_over_m, rows_files_sha256, rows[all rows incl. Tier-E, with the FDR columns], scored_slots_halted, law}`.
The transcripts are `scores/SCORE_<REG>.txt` and `scores/FINISH.txt`, and the fixtures are
`scores/FIXTURES_SCORE.txt` (F-SC-RECORD, CARD, DOOR-FIRST, BIND, NOSCORE, ROWS, DET, TWIN, TRG2,
SPRING, GEN1, FINISH, PRESCRIBED, JSON, LANES-CARD, BESIDE).

**Not reusable for TC11 as written (G3):**
- It hardwires the six ids and `load_record`'s pin at the TC10 paths.
- `door_kind` (`:444`) knows only lanes ⊆ {card, spring} or {brk-s1, brk-i1}, and HALTs
  "no door for external arm" on anything new (relay, scalp, brk-4h, add).
- `TEXT_PRESCRIBES` is keyed to P-BE-1, `finish_gate` says "ALL SIX", the seed is `TP.SEED`, and
  `TP.FAMILY_M` is used.

**Reusable pure helpers:** `rows_bytes`/`_jsonable` (`:1178-1201`), `haircut_twin_block`,
`per_asset_rows`, `key_sets` (`:579`), `sha256_bytes`/`sha256_file`, `Printer` (`:868`), and the
two-pass ride-then-score structure.

---

## 7 · The null of record: `gaps+order` (R10)

**The ruling** (`research_outputs/tierc10/OPERATOR_RULINGS.md` §R10, ~l.125):
- "gaps+order — the leak-reduced one."
- `gaps-only` is filed and printed beside it, never deleted.
- The two variants disagree by sign on 3,455 of 19,926 comparable summary cells.
- "K=20 resolves a percentile to 5 points at best. It is a DESCRIPTION, never a p-value."

**What it permutes, per (asset, lens, scale_kind) and per draw d** (`tierc10_null.py` docstring and LEANS N-a..N-i, `:166-219`):
1. `real_box_set` (`:239`) reads the real confirmed macro ranges: each LIFE (`die_i - confirm_i`;
   the last one may be censored), its HEIGHT in ATR of its confirm bar, and the m+1 GAPS.
   `sum(lives) + sum(gaps) = n`.
2. `schedule(real, rng, keep_order)` (`:293`):
   - It draws `perm = rng.permutation(m+1)` of the gaps, then `u = rng.random(m)` (%-positions),
     then, for gaps+order only (`keep_order=False`), `rng.permutation(m)` of the (life, height) pairs.
   - A lead gap shorter than `RC.ATR_LEN` is swapped with the first qualifying one.
   - The alive-bar count equals the real one exactly (F-NULL-COV).
3. `draw_rng(seed, draw, asset, lens, scale_kind)` (`:286`) returns
   `np.random.default_rng([seed + draw, crc32("asset|lens|scale_kind")])`.
   `SEED = C.SEED = 20260921` and `K_DEFAULT = 20`. `REAL_DRAW = -1` is the real row in the same table.
4. `box_bounds` (`:335`): `bottom = close[confirm] - u*height_atr*atr[confirm]` (static box, no redraw).
5. `static_box_machine` (`:356`) walks breach / harden / DIE with the frozen pins. The corpses are
   fed to the real leash (`RC.flips_and_leash`) for memory-touch-2s and flip-hold, and to the
   census's `retest_holds` for the band classes.
6. **The same outcome road as the census:** `C.census_events` (`tierc10_census.py:1267`), then
   `C.outcome_ledger` (`:1352`), then `C.grid_rows` (`:1403`).
   - `term = sgn*(c[k+H]-c[k])/atr[k]` from the CLOSE of `known_at`; MFE and MAE are in ATR.
   - `H ∈ HORIZONS = (("H20",20),("H100",100))` in bars of the lens (`:123`). The row is censored
     if `k+H > n-1` and the horizon is never shortened.
   - `toll_atr_evt = (bps/1e4)*c[k]/atr[k]`, with bps from `C.toll_bps_for(stem)`
     (`fee_schedule.json round_trip_bps_used`).
   - `net = median_term - toll_atr`.
7. `summarise(grid)` (`:597`), per `NULL_SUMMARY_KEY = [asset, lens, scale_kind, cls, era, horizon, stat]`
   with `stat ∈ (median_term, net, hit_rate, hit_rate_net, median_mfe, median_mae)`, produces
   `real, real_n, n_draws, n_draws_valid, null_n_events_median, null_median, null_q25, null_q75, null_iqr, null_min, null_max, real_minus_null_median, real_pctile_in_null` (mid-rank: `100*(#null<real + 0.5*#null==real)/valid`),
   plus `nan_reason, pctile_law, pins_status, printable, own_window_overlap_pct_mean, n_identity_perm, n_distinct_schedules, schedule_diag_law, schedule_variant`, the as-of columns and the collar columns.

**Classes (`tierc10_census.py:145-151`):** `breach, harden, DIE, memory-touch-v1, memory-touch-2s,
flip-hold, retest-hold-ribbon89_127, retest-hold-ribbon127_200, retest-hold-tap89, retest-hold-tap127,
retest-hold-tap200`. Sign law (`:199-208`): +1 is the breach/DIE direction, and flip-hold is signed
by polarity.
- ERAS are `("ALL","tuning","holdout")` by ANCHOR close (`:164-180`). The census spells the full
  history "ALL" and the panel spells it "full".
- The 5m retest-hold rows outside tuning are collared unprintable (`COLLAR_5M_RETEST`, `printable()`).

**Files:** `research_outputs/tierc10/null/gaps_order/{null_grid,null_summary,null_coverage,leans}.parquet`,
`build_manifest.json`, `FIXTURES_NULL.txt`, and `cells/`. `gaps_only/` sits beside it.
- `null_grid` has 74,844 rows by 54 columns, `NULL_GRID_KEY=[asset,lens,scale_kind,cls,era,draw,horizon]`,
  and draws -1..19.
- `null_summary` has 21,384 rows by 43 columns.
- The assets are PANEL17 plus `POOLED:ALL`, over lenses 5m, 4h and 1d.

**CLI:**
`tierc10_null.py [--assets PANEL17|CLASSIC5|UNSEEN12|SYM,..] [--lenses 5m,4h,1d] [--scale-kind both|frozen3.0|calibrated] [--draws K] [--seed S] [--variant gaps+order|gaps-only] [--out DIR] [--census-root DIR] [--force] [--merge-only]`.

**What it does NOT do (relevant to R4):**
- It produces no base rate. `grep base_rate scripts/tierc10_*.py` is empty; the only base rate in
  the estate is `tierc7_lab_weave.py:777`, bar-share profitable.
- It gives no per-direction row: sgn is folded into `term`. The ledger does carry `side` and `sgn`,
  so a per-direction table is `C.grid_rows(led[led.sgn == ±1], …)` on the same ledger.
- It gives no conditioning on the lens above.
- It covers no lenses beyond `C.LENSES = ("5m","4h","1d")`; 1d is derived from 4h. The snapshot
  does hold 15m, 1h, 12h and 1w kline files for all five home assets.
- It produces no CI and no verdict.
- Available as-of machinery for L+1 conditioning: `C.asof_index(tape_Lplus1, known_close_ms)`
  (`:894`) returns the last closed L+1 bar, and `C.stamps_at(tape, view, idx)` (`:906`) returns
  state, %-of-range, distance, age and so on.

---

## 8 · Tier-E and "a SELECTION, not a result"

**Tier-E** means a measurement that is report-only, unscored, owns no slot in m, and can neither
rescue nor contradict a scored row. It comes in two forms:

1. **A Tier-E arm of a registration.** `arm_spec(..., scored_in_family=False)` is scored through
   `TP.score` with a full row (CI, p, verdict), but `clears_bh_bar` is `None` in FAMILY. Examples
   are P-GEN-1's panel17 view and P-TRG-2's era arms.
2. **A Tier-E table (census, null, lab).** It carries a **collar in columns**, because "a caption
   does not survive a copy of the row". Three styles exist:
   - **Census/null style** (`tierc10_census.py:351-363, 1573-1591`): `tier = "TIER-E MEASUREMENT — UNSCORED, GATES NOTHING"`, `gates = "NOTHING — TIER-E MEASUREMENT ONLY. No registration rests on this row, none is implied, and no cell of this grid may be promoted."`, `m_looks_this_table = len(df)`, `m_note`, `in_sample`, plus the as-of stamp columns (`C.stamp`, `:1552`).
   - **Close style, the literal convention** (`tierc10_close_regime_prior.py:149-164`): `COLLAR_COLS = ("tier","selection_not_a_result","m_selections_this_table","in_sample","gates")` with `SELECTION = "a SELECTION, not a result — report-only; no row here is a test, a verdict or a lane, and no cell may be promoted to one"`. `check_collar` (`:637`) FAILS if a collar column is missing or null, `gates != "nothing"`, tier lacks "TIER-E", or `selection_not_a_result` lacks "SELECTION, not a result". It also fails if `m_selections_this_table != len(df)` or **any verdict/ci/p column exists** (`FORBIDDEN_EXACT/PREFIX/SUBSTR`, `forbidden_columns` at `:627`).
   - **The P-AGE-1 variant** (`tierc10_close_p_age_1_tide_youth.py:149-157, 420-432`): a `BANNED_RX` for verdict, clears_bh, `^p_`, `_p$` and ci columns.
   - Older precedent is `tierc8_an2.SELECTION` (`:195`) and `tierc9.SELECTION_NOTE` (`:948`).
3. **Grids are reported whole:** `TP.grid_whole(declared, written, cell_col, require_cols, require_false, label)` (F-GRID).

---

## 9 · Recipes for TC11

### 9.0 · Process preamble (a new `scripts/tierc11_score.py` or similar)

```python
# export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 PYTHONDONTWRITEBYTECODE=1  (BEFORE python)
import sys, json
from pathlib import Path
ROOT = Path("/Users/luis/Naiad"); sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
import tierc10_panel as TP, tierc9 as T9, tierc5 as T5

OUT11 = ROOT / "research_outputs" / "tierc11"
SEED11, M11 = 20260924, 9
# [G2] the canonical registry is a MODULE GLOBAL read at call time -> repoint it BEFORE any door
TP.REG_DIR = OUT11 / "registrations"          # run_cell_n/run_lane/_check_head/finish_family then treat it as canonical
# [G1] require_registered/require_arm bind family_m=6 at def time; score()/run_cell_n()/LN.run_lane() don't pass it
TP.require_registered.__defaults__ = (None, M11, None)        # (root, family_m, head_of_record)
TP.require_arm.__defaults__ = (None, None, None, M11)         # (lanes, head_of_record, root, family_m)
# (print both as [LEAN-HEPHAESTUS]; or wrap score() in a tierc11 module — the TC10 files are not edited)
TP.substrate()
PIN = json.loads((OUT11 / "REGISTRY_PIN.json").read_text())   # written by the tierc11 clerk after register()
HEAD = (PIN["registry_len"], PIN["registry_head"])
TEXTS = json.loads((OUT11 / "REGISTRATION_TEXTS.json").read_text())
```

Filing (the clerk), once per id and in a fixed order, before any look:
`TP.register(rid, TEXTS[rid]["text"], TEXTS[rid]["prior_pct"], arms=[TP.arm_spec(...), ...], family_m=9)`.
The text MUST contain `TP.loao_line_clause("lineage")`. Then write the pin and commit it with `git add -f`.

### 9.1 · (i) A paired-vs-v6 rule that keeps the campaign set (P-ADD-BRK, P-ADD-SFP, P-TP-RNG, P-WARN-1's rule)

```python
A = TP.arm_spec("add-brk vs card-v6 · CLASSIC5 · <era>", TP.CLASSIC5, ruler="set_change",
                scored_in_family=True, lanes=("card",), base="card-v6",
                loao_line="lineage", era="<full|holdout>")          # external runner: NO card/roles
# never ruler="two_sample" here: it HALTs when the key set does not move (P-BE-1, TC10)
gate = TP.require_arm(rid, TEXT, A["arm"], TP.CLASSIC5, lanes=("card",), head_of_record=HEAD)  # DOOR FIRST
lo, hi, meta = TP.corridor_era(TP.CLASSIC5, A["era"])
trades = my_runner(lo, hi)            # campaigns keep t.lane == "card" and v6's entry_ms; net_r INCLUDES the add legs
book = TP.external_book(trades, gate, lo, hi)
base = TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, TP.CLASSIC5, lo, hi)   # the control: no paperwork
row = TP.score(rid, TEXT, book, TP.CLASSIC5, base=base, ruler="set_change", seed=SEED11,
               arm=A["arm"], scored_in_family=True, head_of_record=HEAD, era=A["era"])
```

- **Statistic when the keys are identical** (`row["ruler_is_two_sample"] is False`,
  `set_changes_measured False`, `paired_n == n == len(base)`): the mean of per-campaign
  `net_r_arm - net_r_v6`, with a 90% percentile CI from an asset-cluster bootstrap of the deltas.
- **If the rule moves the key set** (an early exit that lets a new trigger in), set_change becomes
  **two-sample** automatically and the row says so. `paired_ci_*` stays beside it (A3).
- The D15 trio rides; `tail_exit_ratio` is P-TP-RNG's "D15 tail ratio".
- **Prints BESIDE the verdict:** P-ADD-BRK vs P-ADD-SFP head-to-head as a Tier-E table, or as an
  arm of each other's registration with `scored_in_family=False`. Neither may promote the other.

### 9.2 · (ii) A two-sample admission gate that removes trades (P-AGE-1, P-WIN-1; P-RELAY-1 is two-sample vs the base as well)

```python
A = TP.arm_spec("age-gate trailing vs card-v6 · CLASSIC5 · <era>", TP.CLASSIC5, ruler="two_sample",
                scored_in_family=True, lanes=("card",), base="card-v6", loao_line="lineage", era="<era>")
S = TP.arm_spec("age-gate absolute>206 shadow", TP.CLASSIC5, ruler="two_sample", scored_in_family=False,
                lanes=("card",), base="card-v6", loao_line="lineage", era="<era>")   # Tier-E shadow arm
gate = TP.require_arm(rid, TEXT, A["arm"], TP.CLASSIC5, lanes=("card",), head_of_record=HEAD)  # BEFORE any ride
lo, hi, _ = TP.corridor_era(TP.CLASSIC5, A["era"])
base = TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, TP.CLASSIC5, lo, hi)
kept = [t for t in base if not refused(t)]         # or a replay whose trigger is refused
book = TP.external_book(kept, gate, lo, hi)
row = TP.score(rid, TEXT, book, TP.CLASSIC5, base=base, ruler="two_sample", seed=SEED11,
               arm=A["arm"], scored_in_family=True, head_of_record=HEAD, era=A["era"])
```

- **Statistic:** `mean(book) - mean(base)` via `T5.cluster_boot_diff`, with the SAME asset draw
  into both books and `uniq = union of assets`. The LOAO is two-sample.
- **The premise is measured on keys:** HALT if the gate removed nothing.
- **Note:** a bare filtered list has no provenance. It must pass through `external_book(…, gate)`,
  and `require_arm` must precede the ride.
- **P-RELAY-1:** 1h-close entries give different `entry_ms`, so the keys are disjoint and the
  premise holds. Its "miss column" (windows the relay never activates) is BESIDE the row.

### 9.3 · (iii) A standalone lane vs zero (P-BRK-4H; P-SCALP-2 on the holdout)

```python
A = TP.arm_spec("P-SCALP-2 vs zero · taker", TP.CLASSIC5, ruler="vs_zero", scored_in_family=True,
                lanes=("scalp",), base="zero", loao_line="lineage", era="holdout")
V = TP.arm_spec("P-SCALP-2 17-asset view", TP.panel17(), ruler="vs_zero", scored_in_family=False,
                lanes=("scalp",), base="zero", loao_line="lineage", era="holdout")      # Tier-E, LOAO bar 9
gate = TP.require_arm(rid, TEXT, A["arm"], TP.CLASSIC5, lanes=("scalp",), head_of_record=HEAD)
lo, hi, _ = TP.corridor_era(TP.CLASSIC5, "holdout")      # every entry_ms must be > 1719791999000
book = TP.external_book(scalp_runner(lo, hi), gate, lo, hi)
row = TP.score(rid, TEXT, book, TP.CLASSIC5, base=None, ruler="vs_zero", seed=SEED11,
               arm=A["arm"], scored_in_family=True, head_of_record=HEAD, era="holdout")
```

- **Statistic:** a one-sample asset-cluster bootstrap of mean `net_r`, with the LOAO vs zero.
- D15 is None, "DEGENERATE BY CONSTRUCTION". The EAR co-headline rides.
- The maker twin goes as a separate Tier-E arm with its own lanes and book, or in `beside`.

### 9.4 · P-WARN-1's condition (W2, Tier-E) and the family

Nearest existing helper: the cohort vs its complement.

```python
d = T5.cluster_boot_diff(coh_r, coh_sym, comp_r, comp_sym, seed=SEED11, n_boot=4000)
ci = T5._ci_from(d, mean(coh_r) - mean(comp_r)); condition_met = ci["hi"] is not None and ci["hi"] < 0
```

`tierc7_lab_regime._stat` does the same, but with the default seed 20260816 and a 3-asset floor.

Finish:
- `fam = TP.finish_family(all_rows, family_m=9)` gives bar = 0.0111111.
- **Override `fam["fdr_note"]`:** it embeds LEANS["L7"], which reads "0.10/6 = 0.016667" (G1).
- Then write `scores/FAMILY.json` in the TC10 schema.

---

## 10 · GAPS: what the existing code cannot do today

- **G1 · family_m = 9 HALTs at every door.**
  - `score()` (`tierc10_panel.py:2215`), `run_cell_n()` (`:1137`) and `LN.run_lane()` (`tierc10_lanes.py:1107`, `TP.require_arm`) all call
    `require_registered`/`require_arm` without `family_m`. The defaults were bound to 6 at definition
    time (verified: `__defaults__ == (None, 6, None)` and `(None, None, None, 6)`).
  - `_verify_record` then HALTs with "filed under family m=9, the scorer declares m=6".
  - `finish_family(family_m=9)` works, but `fdr_note` prints the L7 text with "0.10/6".
- **G2 · The canonical registry is `research_outputs/tierc10/registrations`.**
  - Any other root is "throwaway". `run_cell_n` (`tierc10_panel.py:1158-1163`) and `LN.run_lane` (`tierc10_lanes.py:1111-1117`)
    refuse the real replay: "opens the gate onto a STUBBED replay only".
  - `finish_family(canonical_only=True)` HALTs on the rows.
  - Fix: repoint `TP.REG_DIR` (a module global read at call time) before any call. The alternative,
    filing TC11 into the TC10 chain as seq 7..15, mixes two families in one registry.
- **G3 · `tierc10_score.py` is TC10-only** (§6). A TC11 driver with doors for the new lanes
  (card-with-adds, card-with-tp, card-gated, relay, brk-4h, scalp) is needed.
  `tierc10_brk.FILED_ARMS` and `ready_run` are bound to P-BRK-I1/S1.
- **G4 · No CONDITIONAL-registration path.**
  - `register()` has no condition field (a condition can go in the text or `fields`, but nothing reads it).
  - `finish_gate` demands a scored row or a named HALT for every id.
  - "Condition not met" needs a new record type and a finish rule.
- **G5 · The null and census cannot produce R4's grid as asked.**
  - No base rate.
  - No per-direction rows (possible by filtering the ledger on `sgn`).
  - No lens-above conditioning.
  - Lenses only 5m/4h/1d, whereas R4 wants 1h, 4h, 12h and 1d, with L+1 up to 1w.
  - No SFP/"deviation confirmed" class: "harden" is the nearest.
  - No "retest that HOLDS" on the memory-line as a separate class: flip-hold is the memory-line
    hold, and retest-hold-tapNN are the bands.
  - Null draws are fixed at K=20 by default, and the output is a percentile, not a test.
- **G6 · A new as-of would break the census.**
  - `tierc10_census` HALTs at import on any snapshot other than `tc10_20260921`.
  - `TP.corridor_n` caps the corridor at TC10's `AS_OF_PIN` (2026-09-21T16:00Z), through the module
    global `TP.AS_OF_PIN`.
  - "latest closed 4h bar, one as-of pin" beyond 2026-09-21 needs a new snapshot, a repointed pin,
    and a different census guard.
  - Only `tc10_20260921` exists under `~/.cache/naiad/snapshots/`.
- **G7 · No forced-PAIRED ruler** (see §2.2). `two_sample` HALTs on an unchanged set.
- **G8 · The code emits only SUPPORTED/NOT SUPPORTED.** "Significantly NEGATIVE" has no code path
  and no downward p.
- **G9 · A Tier-E table cannot carry a CI.** The close-style collar forbids ci/p/verdict columns, but
  P-WARN-1's trigger is "a cluster-90% interval excluding zero" computed on a W2 Tier-E cohort.
  Either the W2 condition row is its own non-collared artifact, or the collar check is relaxed for
  that one table (state it).
- **G10 · The contract text cannot be filed verbatim.**
  - `register()` requires the literal LOAO clause in the TEXT and an era and loao_line per arm.
  - The contract's registration lines (frozen at STEP Q) contain none of these.
- **G11 · Tolls.**
  - TC-series `net_r` is net of fee (5 bps a side, `RC.FEE_BPS_SIDE`) and funding only. The
    measured slippage toll was a "PRINT, NOT A DEDUCTION" in TC10 (P-BRK-S1; `BUILD_DRAFT.md:228-229`).
  - The TC11 phrases "net of L's toll", "taker toll (record)" and "maker toll" need a toll model.
    No maker-fill model exists in the scorer.
  - The haircut twin (`tierc10_data.haircut_twin_net_r`) charges fee plus charter slippage, with no
    funding.
- **G12 · Seeds.** `TP.SEED`, the `C.SEED` null default and the `tierc10_score` driver all use
  20260921. TC11's 20260924 must be passed explicitly to `TP.score(seed=)`, to `loao_n` through
  score, and to `tierc10_null --seed`.

---

## 11 · AMBIGUITIES (contract phrase quoted)

- **A1 · "registrations are ONE family, m = 9 independently-failable hypotheses (bar 0.10/9), text frozen at STEP Q"**
  - Is the registration TEXT the contract line itself, or are full texts drafted later, before the look?
  - The TC10 texts were separate 13k–32k-char documents with the LOAO clause, era and arms.
  - The contract lines name no era, no LOAO line and no arm names.
- **A2 · P-WARN-1: "E[net] is below the base by a cluster-90% interval excluding zero"**
  - Is "the base" the whole book (the cohort is a subset, so the samples overlap) or the complement
    (TC7 lab `_stat`)?
  - Which seed? Which era?
  - "ELSE report-only, no slot spent, stated": does m become 8 (bar 0.0125, TC7 practice) or stay
    at 9 declared (bar 0.0111, TC10 law "fewer tests never loosen")?
- **A3 · "paired vs v6"** (P-WARN-1's rule, P-TP-RNG, adds). If an early exit or take-profit moves
  the campaign key set, TC10's `set_change` law scores it two-sample. Should the row stay "paired"
  regardless (the paired CI only), or follow the law?
- **A4 · Era is unstated for 8 of 9.** Only P-SCALP-2 says "holdout era", yet `arm_spec` requires one.
  - P-BRK-4H's "HOLD retest on the 89 tap" uses retest pins tuned on the 5m tuning era (margin 1.0,
    hold 3, ttl 400; `tierc10_census.resolve_retest_pins`). The 4h tap89 was also selected after the
    full-history null showed percentile 100 (R10).
  - P-AGE-1's 206 and P-WIN-1's 16 were read off full-corridor TC10 tables.
- **A5 · "TRAILING-quantile definition (refuse the OLD band) … absolute definition (refuse age > 206 bars)".**
  - OLD = B4, above the q75 edge (whole-corridor 396).
  - 206 is the q50 edge (the B3 lower edge, `close/P_AGE_1_TIDE_YOUTH.md:55-56`).
  - The two definitions refuse different bands (B4 vs B3+B4), so the "shadow" is not the same cut.
- **A6 · "each removes trades → two-sample" / F-GATE "removes only the trades its text names".**
  If a refused trigger leaves the window armed and a later trigger enters, the gated book is not a
  strict subset of v6.
- **A7 · R4 "base rate, null (gaps+order), per direction"** conditioned on L+1.
  - "Base rate" is undefined. Is it the unconditional outcome from every bar of L, from every event
    of the class, or the L+1-state marginal?
  - Should the null condition on the REAL L+1 state at each null anchor, or re-randomize L+1?
- **A8 · The verdict rule per registration.** Is it CI-only (the P-TRG-2 style) or three-clause
  (the P-GEN-1/BRK style)? The contract names neither.
- **A9 · P-RELAY-1 "vs the 12/26-triggered base".** This is presumably the card v6 control
  (`CONTROL_RIDE`, trigger 12/26) on the same era window. It is not "v6 restricted to the windows
  the relay could act in".
- **A10 · P-TP-RNG "take-profit of the remainder".** The remainder after the 89/316 de-risk "keep"
  harvest, or after the v6 band harvest? The paired delta's meaning depends on it.
