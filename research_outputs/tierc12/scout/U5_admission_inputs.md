# U5 — THE ADMISSION FAMILY'S INPUTS (TC12 STAGE G) — scout map

Scout: read-only. Contract read verbatim: `scratchpad/tc12/2026-10-08_TC12_APOLLO.md`, sha256
`861d6050e80e66995e4f9db2855aaf274d63285249c2549e5a0813582095a7bd` (137 lines) — byte-identical to
`/Users/luis/Naiad/exchange/queue/2026-10-08_TC12_APOLLO.md` (same sha; main HEAD moved to `28e006b`
"tierc12(STEP Q)" while this scout ran). Stage G = contract lines 52-62.

Trees: MAIN `/Users/luis/Naiad` (branch v12-v1-census) = **M/**; X worktree
`/Users/luis/Naiad/.claude/worktrees/tierc11x` (HEAD `7b24f835bcbf7430eb0f97b6c39b6b1b233eef11`) = **X/**.
Every number below was read this session from the cited file. Numbers marked **[scout-derived]** were
computed by this scout from a filed table (the code path is stated); they are orientation, not records.

---------------------------------------------------------------------------------------------------
## 1 · FACTS

### 1.1 THE TIDE and its AGE
- **Tide** = sign(EMA89 − EMA316) of the 4h close, two-state (+1 / −1), defined only from bar index 316
  of the asset's own tape. `M/scripts/tierc7_lab_regime.py:306-350` `tide_streak(sym) -> (state, run, start)`;
  `TIDE_WARM_BARS = RC.WARMUP_BARS` (316) `:179`. EMA = `engine.indicators.ema` (`M/engine/indicators.py:17`),
  seeded at the series start (never NaN) — hence the warm floor (docstring `:313-318`).
- **Tide AGE** = `run[j]`: consecutive 4h bars ending at j on which `state` has not changed; **the flip
  bar counts as bar 1**; `run = -1` below the warm floor (`:309-311`, `:338-347`). **Units: 4h bars.**
- **Left-censoring**: `start[j] == TIDE_WARM_BARS` marks the one streak per asset already running at the
  warm floor; its run is a LOWER bound (`:316-318`; `tierc11_books.py:363-368`).
- **Read at the campaign's ENTRY bar** `entry_i` (the bar whose close is the entry price; `entry_ms` is
  that bar's OPEN, the decision instant is `entry_close_ms = entry_ms + 4h`):
  `M/scripts/tierc11_books.py:363-368` `entry_streak(t) -> (run, left_censored, state)`;
  `M/scripts/tierc11_stage_g.py:309-312` `age_of(t)`. Reading of record: TC11 LEANS L-G.1,
  `M/research_outputs/tierc11/LEANS.md:357-369`.
- In v6 the entry bar IS the trigger bar (first 12/26 cross of the window; `entry_px = f.c[ti]`,
  `entry_i = ti`): `M/scripts/tierc9.py:389-404`, `tierc11_stage_g.py:471-480`.
- **The OTHER tide age on disk (NOT of record; disclosure only)**: `tierc9.tide_streak_age(t, roles)`
  `M/scripts/tierc9.py:537-560` — read at the ARM bar, THREE-state tide (tide_f>tide_s AND close>tide_s).
  Swapping it in is F-DEF's sabotage DEF-AGE (`tierc11_stage_g_fixtures.py` header).
- All 200 v6 campaigns ride WITH the two-state tide at entry (`tierc9.py:1391-1395` HALTs otherwise).

### 1.2 THE AGE BANDS (names, cut points)
- Names: `STREAK_LABELS = ("B1 YOUNG tide", "B2 EARLY tide", "B3 MATURE tide", "B4 OLD tide")`
  `tierc7_lab_regime.py:446-447`; codes `BAND_CODES = ("B1","B2","B3","B4")` `tierc11_books.py:158`.
- Cut points = the three quartile edges `STREAK_BAND_QUANTILES = (0.25, 0.50, 0.75)` `:181` of the
  **bar-pooled** CLASSIC5 streak distribution (each panel bar votes; episode-pooled is "NOT USED",
  `:648-657`).
- Assignment: `_streak_band(run, edges) = int(np.digitize(float(run), edges))` `:456-459`
  (right=False): **B1 run < q25 · B2 q25 ≤ run < q50 · B3 q50 ≤ run < q75 · B4 OLD run ≥ q75**.
  `run <= 0` → None. YOUNG ∪ EARLY ⇔ `run < q50`.
- F-EDGE holds the comparators at the boundary: "OLD: run == q75 refused; >206: 206 kept, 207 refused;
  lag >= 16: 15 kept, 16 refused" (`M/research_outputs/tierc11/stage_g/FIXTURES_STAGE_G.txt:51`).

### 1.3 "TRAILING q75, THE CUT OF RECORD" — exact window and as-of rule
- Pool: `tierc9._trailing_pool(lo_ms, hi_ms)` `M/scripts/tierc9.py:1290-1315` — for each asset in
  `RC.UNIVERSE` (= CLASSIC5: `tierc7_rules.py:91` `UNIVERSE = V6.UNIVERSE` ← `tierc2_rules.py:56-57,111` (BTC, ETH, SOL, NEAR, ZEC)), every 4h bar inside [lo, hi] with
  `run > 0`; values `sk_v`, bar-open times `sk_t`, mergesorted by time.
- Edges: `tierc9._trailing_edges(pool, at_ms)["streak_bar"]` `:1318-1328` =
  `np.quantile(pool["sk_v"][:i2], (0.25,0.5,0.75))` with `i2 = searchsorted(sk_t, at_ms, side="right")`,
  i.e. **every pooled bar with open_ms ≤ the entry bar's open, the entry bar itself (all five assets'
  bars at that open) included**; `None` while the prefix holds < `RC.PROVISIONAL_MIN_N` = 30 bars.
  `at_ms = f.open_ms[entry_i]` (`tierc11_books.py:371-375`).
- So "trailing" = **EXPANDING from the corridor's panel start, not a rolling window**; quantile =
  numpy's default linear interpolation (edges can be non-integer: e.g. 223.25, 363.5 —
  `M/research_outputs/tierc10/close/P_AGE_1_EDGES.parquet` `streak_edges_trailing`).
- Pool start is PINNED: `pool_lo_ms = 1567958400000` (2019-09-08T16:00:00Z) —
  `X/research_outputs/tierc11x/forward/BOOK_SPECS.json` key `books.gated-v6-oldtide.gate.pool_lo_ms`;
  `X/research_outputs/tierc11x/books/build_manifest.json:180`; = `TP.corridor_n(CLASSIC5)`'s panel start
  (`min` of the first opens, `M/scripts/tierc10_panel.py:681`).
- Causality: prefix-only; adding bars at the END cannot move a past band (X asserts it: TIDE-PREFIX,
  `X/scripts/tc11x_books.py:1084-1093`).
- Evolution of the trailing edges (P_AGE_1_EDGES.parquet, 7 rows, col `streak_edges_trailing`):
  2020-01-01 [35.0,107.0,199.5] · 2021 [86.0,189.0,363.5] · 2022 [97.0,233.0,472.0] · 2023
  [102.0,237.0,453.0] · 2024 [93.0,217.0,402.0] · 2025 [89.0,208.0,402.0] · 2026 [90.0,210.0,404.0]
  (`M/research_outputs/tierc10/close/P_AGE_1_TIDE_YOUTH.md` Table 3).
- Over the 200 v6 entries q75 ranges 188.0…602.0, q50 80.0…289.0, q25 31.0…119.0 **[scout-derived:
  min/max of `tide_edge_q*` in g_campaign_gates.parquet]**; 0 campaigns unbanded
  (`STAGE_G.md:122`); smallest pooled prefix at a v6 entry 577 bars (`X4_stamps.parquet` `edge_pool_n`
  row BTC 2020-01-27; X4 builder resolution, `X/…/era/X4.md:1591`).

### 1.4 "THE ABSOLUTE-206 CUT"
- 206 = the **whole-corridor bar-pooled MEDIAN (q50) edge** of the CLASSIC5 streak — the B2 EARLY / B3
  MATURE boundary, NOT the OLD edge, and a LOOK-AHEAD number:
  `M/research_outputs/tierc10/close/P_AGE_1_BAR_BANDS.parquet` row basis "bar-pooled — USED", band 1,
  `edge_hi_bars = 206.0` ("bar-pooled quartiles [88.0, 206.0, 396.0]").
  Same on TC11's corridor: `M/research_outputs/tierc11/books/build_manifest.json`
  `anchors.f_age_anchor.whole_corridor_streak_edges_for_the_shadow_caveat` =
  `{tc10_window: [88.0,206.0,396.0], tc11_corridor: [88.0,206.0,396.0]}`.
- Origin of the number as a gate: TC11 contract `M/exchange/queue/2026-09-24_TC11_APOLLO.md:45-46`
  "the absolute definition (refuse age > 206 bars) printed as shadow".
- Law as built: `abs_refused(run) = int(run) > 206` (`tierc11_stage_g.py:162`, `:326-328`); label
  `ABS_LABEL` `:176-178`. Typed in TC11 (`ABS_TIDE_CUT = 206`); X READS IT BY OBJECT from the P-AGE-1
  registration text by regex: `X/scripts/tc11x_books.py:347-362` `abs_tide_cut()`.
- Filed shadow book: `M/research_outputs/tierc11/regbooks/P-AGE-1/tierE__shadow_abs206.parquet`
  n **80**, ΣR **+48.803986**, mean +0.6100; refused n 120, mean −0.0666, ΣR −7.9964
  (`STAGE_G.md:59`); two-sample Δ **+0.406012** CI [+0.058250, +0.808688] p 0.022744, LOAO 2/5
  (`SCORES.json` rows[P-AGE-1].tier_e[arm=tierE__shadow_abs206]).
  Every OLD campaign is also >206 (59/59); 61 non-OLD campaigns are >206 **[scout-derived crosstab of
  `age_abs206_refused` × `age_old_refused`, g_campaign_gates.parquet]**.

### 1.5 THE OLD-GATED BOOK AS FILED
Two filed forms of the same rule (P-AGE-1's scored arm):
- **TC11 regbook (scored, in-sample)**: `M/research_outputs/tierc11/regbooks/P-AGE-1/scored.parquet`
  file sha256 `6440a6e0d14cfbf1c62df19246a066d0f7086a1e64aae3bb0ced8c2b2a624dca`;
  **n 141 · Σ net_r +63.464130732724186 · mean +0.45010021796258287** (`scored.json`; `SCORES.json`
  stats.sum_net_r / mean_net_r); canonical-CSV `book_sha256 d008fa5086ce14f578403c083169e28c5870701fd37f3cb2b03c5474f04f22d8`;
  `TP._book_sha 4ccddc79a34afdf8511847a06175b202c8e8fb295fde7c3fe7095c6bf399bee3` (`STAGE_G.md:47`).
  Refused cohort n 59, mean −0.384010, ΣR −22.656566 (`STAGE_G.md:58`, `:66`).
- **Base**: `regbooks/P-AGE-1/base.parquet` file sha `dbfe4788610b11cc70ef64be31aac95949b921f086eaeb66b4535fbbad7af4ce`
  (byte-identical to P-WIN-1/base.parquet), n 200, ΣR +40.80756457414756, mean +0.20403782287073777,
  book_sha256 `f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8`,
  `TP._book_sha f3c68f544bcda52c909374105dabbdc773c9bffa4b66b2ef7e0f35ac9b369132`.
- **Δ vs v6 (verdict of record)**: two-sample Δ **+0.2460623950918451**, cluster-90% CI
  **[+0.19118979196542596, +0.29665616046817667]**, p = 1/4001 = **0.00024993751562109475** (0 of 4000
  draws ≤ 0), deciding bound (44th smallest) +0.18313257424342969, n_clusters 5; LOAO 5/5; haircut twin
  +0.245569 [0.190183, 0.296962]; sens seed 20260816 identical verdict —
  `M/research_outputs/tierc11/scores/SCORES.json` rows[registration=P-AGE-1].stats.{main,sens,haircut,loao}.
  Verdict cell: "SUPPORTED — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen …)" at bar 0.10/9
  (`S0_VERDICTS.md:12`). Era slices (Tier-E): tuning n 81 vs 123, Δ +0.152275 [0.003114, 0.296952]
  p 0.044239, LOAO 1/5; holdout n 60 vs 77, Δ +0.319533 [0.209452, 0.407542] p 0.000250, LOAO 5/5.
  Concentration: top trade ZECUSDT entry_ms 1777608000000 +25.060483 R = 39.5 % of the scored ΣR;
  point without it +0.195181 (`SCORES.json` …concentration).
- **X5 forward-ledger book `gated-v6-oldtide` ("of record", the third book)**: frozen spec
  `X/research_outputs/tierc11x/forward/BOOK_SPECS.json` sha256
  `72a1f52359c66084d22f8bc99b0cd35e7edd89db2751f4859f559c8b1f51cac3` — gate.refuse "tide_band == 'B4'",
  band_quantiles [0.25,0.5,0.75], min_pool_bars 30, **none_band "HALT"**, pool_lo_ms 1567958400000,
  kind "POST-FILTER (TC11 L-1.5) … no re-ride into a freed slot", p_age_1_payload_sha256 e01a89ea…;
  chain `FORWARD_LEDGER.jsonl` sha `4a6da7e89a3cf5f0127f76aca0d2ae12d218ffc06417c6528c70210092cfa4c5`,
  4 lines, head `61ea177fadcc82ba…`; rows appended 0·0·0, `n_reride_differs` 0·0
  (`X/…/forward/FORWARD_LEDGER.md`). Opening 2026-09-21T16:00:00Z (ms 1790006400000).

### 1.6 THE WINDOW AGE and "16"
- `lag = entry_i − arm_i` in 4h bars: `tierc11_stage_g.py:331-332` `lag_of(t)`; `win_refused(lag) = lag >= 16`
  `:335-336`; `LAG_CUT = 16` `:163`; `SHADOW_LAG = (7, 15)` `:164`; bands
  `LAG_BANDS = (("0",0,0),("1-6",1,6),("7-15",7,15),(">=16",16,None))` `tierc11_books.py:157`.
  Arm = the 12/89 window cross (`tierc9.py:168-200` armings9); trigger = first 12/26 cross in
  [arm_i, window_end) (`tierc9.py:223-230`).
- **Where 16 comes from**: only from APOLLO's contract text — `M/exchange/queue/2026-09-24_TC11_APOLLO.md:47`
  "refuse triggers with arm→trigger lag ≥ 16 bars vs v6; lag 7–15 printed as shadow cut". TC11 LEANS says
  so in words: "The 16 cut has no on-disk provenance, and v6 lag 7–15 holds 4/200, so ≥16 ≈ ≥7"
  (`LEANS.md:371-374`; registration `selection_hazard`, REGISTRATIONS.json P-WIN-1). Direction informed by
  TC6V L-LAG deciles (lag-0 +0.4149, 56-bar decile −0.5796); P-LAG-1 NOT MET.
- Lag bands, whole (`STAGE_G.md:167-170`, `g_lag_bands.parquet`):
  0: n 52 mean +0.4306 ΣR +22.3888 · 1-6: n 81 +0.3934 +31.8633 · 7-15: n 4 −0.5695 −2.2781 ·
  ≥16: n 63 −0.1772 −11.1665. Exactly ONE campaign sits at lag 16; lags 7,8,10,11 hold one each; max 193
  **[scout-derived value_counts of `lag`, g_campaign_gates.parquet]**.
- **Stale-alone book as filed**: `regbooks/P-WIN-1/scored.parquet` file sha
  `824c5e08ca79511fea96b98d65b74e8e7209f36379d881a2ff02f927db08241c`, n **137**, ΣR **+51.97401862719062**,
  mean +0.37937239873861767, book_sha256 `fd3f407ad6b1867039bb24a42816678e4992b9204ed65971058e48fa2bdabbfe`,
  TP sha `aa0216e7…` (`STAGE_G.md:49`). Two-sample Δ **+0.1753345758678799** CI
  **[+0.002963561089636302, +0.33925603239869473]** p 146/4001 = **0.03649087728067983**, deciding bound
  −0.021314; LOAO 2/5 → **NOT SUPPORTED** at 0.10/9 (`SCORES.json` rows[P-WIN-1].stats.main;
  `S0_VERDICTS.md:13`). Sens seed p 0.038990.

### 1.7 "TC11's CROSSED TABLE" — found, printed WHOLE, cell 110 identified
File: `M/research_outputs/tierc11/stage_g/STAGE_G.md:172-198` "The three gates crossed 2 × 2 × 2 [L-G.3]";
tables `g_grid_partition.parquet` (file sha `977ed42f60f0a6a21471faa62ccc00ee44bad555221bd7d24bd8603b7ec74917`,
content sha `d786f529…`) and `g_grid_books.parquet` (file sha
`b2c786e0e7204e1be49c31c0ed7eae7e61365e61ae608dd0efcbe0f4e3b7b51b`, content sha `cce5f1cc…`).
Bits (`GRID_FLAGS`, `tierc11_stage_g.py:220`): **A = P-AGE-1 OLD (run ≥ trailing q75) · W = lag ≥ 16 ·
S = r_over_atr > 2.2**. Tier-E, collared, no CI, no verdict.

(a) THE PARTITION (v6 split by the three refusal flags) — `g_grid_partition.parquet`:

| cell | age_old | lag_ge16 | ratr_gt2p2 | n | mean_net_r | sum_net_r | win_pct |
|---|---|---|---|---:|---:|---:|---:|
| A0\|W0\|S0 | F | F | F | 81 | +0.540539 | +43.783651 | 39.506173 |
| A0\|W0\|S1 | F | F | T | 29 | +0.442193 | +12.823585 | 51.724138 |
| A0\|W1\|S0 | F | T | F | 23 | −0.004752 | −0.109290 | 26.086957 |
| A0\|W1\|S1 | F | T | T | 8 | +0.870773 | +6.966185 | 50.000000 |
| A1\|W0\|S0 | T | F | F | 21 | −0.305059 | −6.406248 | 23.809524 |
| A1\|W0\|S1 | T | F | T | 6 | +0.295505 | +1.773031 | 50.000000 |
| A1\|W1\|S0 | T | T | F | 22 | −0.825121 | −18.152664 | 4.545455 |
| A1\|W1\|S1 | T | T | T | 10 | +0.012931 | +0.129315 | 30.000000 |

(b) THE EIGHT GATE BOOKS (v6 minus the union of the refused sets of the gates ON) — `g_grid_books.parquet`:

| cell | age | win | ratr | n | mean_net_r | sum_net_r | win_pct | n_refused | sum_net_r_refused |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| age:off\|win:off\|ratr:off | F | F | F | 200 | +0.204038 | +40.807565 | 34.500000 | 0 | 0.000000 |
| age:off\|win:off\|ratr:on | F | F | T | 147 | +0.130037 | +19.115450 | 29.931973 | 53 | +21.692115 |
| age:off\|win:on\|ratr:off | F | T | F | 137 | +0.379372 | +51.974019 | 40.145985 | 63 | −11.166454 |
| age:off\|win:on\|ratr:on | F | T | T | 102 | +0.366445 | +37.377403 | 36.274510 | 98 | +3.430161 |
| age:on\|win:off\|ratr:off | T | F | F | 141 | +0.450100 | +63.464131 | 40.425532 | 59 | −22.656566 |
| age:on\|win:off\|ratr:on | T | F | T | 104 | +0.419946 | +43.674362 | 36.538462 | 96 | −2.866797 |
| **age:on\|win:on\|ratr:off** | **T** | **T** | **F** | **110** | **+0.514611** | **+56.607236** | 42.727273 | 90 | −15.799671 |
| age:on\|win:on\|ratr:on | T | T | T | 81 | +0.540539 | +43.783651 | 39.506173 | 119 | −2.976087 |

**"cell 110 @ +0.515"** = row `age:on|win:on|ratr:off` of table (b): the three bits are
(age gate ON, window gate ON, far-stop gate OFF) = "1,1,0"; **n in the cell is also 110**; **+0.515 is
`mean_net_r` = E[net R] per campaign of the gated BOOK** (+0.514611; `STAGE_G.md:197` prints +0.5146) —
**not** a Δ vs v6, not a CI, no p. It is the only +0.5146 in `M/research_outputs/tierc11/BUILD_DRAFT.md`
(line 5547). Its book = v6 minus (OLD ∪ stale): 90 refused (A1W0 27 + A0W1 31 + A1W1 32).
Point Δ vs v6 = 0.514611 − 0.204038 = **+0.310573** [scout-derived subtraction; NO interval is filed for
this book — it has no regbook, only this aggregate row].
Orientation **[scout-derived from g_campaign_gates.parquet (6-dp table), groupby]**:
- kept 110: tuning n 63 ΣR +6.957485 mean +0.110436 · holdout n 47 ΣR +49.649754 mean +1.056378;
  per asset n / ΣR: BTC 16 / +13.334725 · ETH 29 / +11.356392 · NEAR 21 / −0.433343 · SOL 18 / +3.095296 ·
  ZEC 26 / +29.254169 (top trade ZEC +25.060483 is IN the kept book = 44.3 % of its ΣR).
- refused 90: ΣR −15.799673, mean −0.175552; tuning 60 / −8.281306 · holdout 30 / −7.518367.
- **the stale-only increment over the OLD-gated book (A0,W1): n 31, ΣR +6.856895, mean +0.221190**
  (tuning 18 / +4.505034 · holdout 13 / +2.351861): the fourth book has a HIGHER mean (+0.5146 vs
  +0.4501) but a LOWER ΣR (+56.6072 vs +63.4641) than the third.

### 1.8 THE FAR-STOP FINDING ("refusing forfeited +21.69R")
- Definition: `r_over_atr = r_dist / ATR14_4h(entry)`; "far structural stop" ⇔ `r_over_atr > 2.2`
  (strict): `ratr_of(t) = t.r_dist / t.atr_at_entry` `tierc11_stage_g.py:343-344`;
  `ratr_refused(r) = r > 2.2` `:347-348`; `RATR_CUT = 2.2` `:165`; LEANS L-G.3 `LEANS.md:376-384`;
  contract `2026-09-24_TC11_APOLLO.md:49` "structure-distance (r_dist > 2.2 ATR) as admission/priority".
  `r_dist` = the v6 structural stop distance, `RC.struct_stop_4h(pv4, ti, entry_px, d, atr,
  min_stop_atr=CARD.entry_rail_atr)` (`tierc11_stage_g.py:436-446`), railed ≥ 1.0 ATR (so r_over_atr ≥ 1).
- Source row: gate `L-G.3/ratr_admission`, `STAGE_G.md:62` / `g_gate_rows.parquet`: n_gated 147, ΣR
  +19.1155; **n_refused 53, mean +0.4093, ΣR +21.6921**; forfeit_note "on per-campaign expectancy only;
  the gate forfeits +21.6921 R total"; = gate-book row `age:off|win:off|ratr:on`
  (sum_net_r_refused +21.692115). Regbook `P-WIN-1/tierE__ratr_admission.parquet` (file sha `92be97b1…`,
  book_sha256 `dcfffefb…`): two-sample Δ −0.074001 CI [−0.206129, +0.067420] p 0.808548.
- TC11's PRIORITY book ran the OPPOSITE direction to TC12's text: a window whose first trigger has
  r_over_atr > 2.2 is PASSED and replaced by the first later same-direction 12/26 cross with
  r_over_atr ≤ 2.2 (prefer the NEARER stop): `replay_g(priority_cut=2.2)` `tierc11_stage_g.py:449-534`;
  n 165, ΣR +18.392480, 18 substitutions, outcomes {entered 147, passed_no_substitute 35,
  passed_substituted 18} (`STAGE_G.md:202-203`); Δ −0.092568 CI [−0.206882, +0.058703].
- **One-position rule, measured**: "position_open rejections v6 0, priority 0 … 'asset flat' never binds
  and the re-ride rival is 0 for every gate" (`STAGE_G.md:205`; `build_manifest.json:121-122`
  `n_position_open_v6 = 0`, `n_position_open_priority = 0`); rival log is the placeholder row
  (`STAGE_G.md:683-685`, `g_rivals.parquet` 1 row). Cross-asset same-close collisions: v6 10 closes / 21
  campaigns / max 3 assets, "binds: no — one position per ASSET, no portfolio cap" (`STAGE_G.md:647`).

### 1.9 THE TWO-SAMPLE-vs-v6 SCORING DESIGN (refusals that REMOVE trades)
- Ruler: `T5.cluster_boot_diff(va, ca, vb, cb, seed, n_boot)` `M/scripts/tierc5.py:1200-1224` — an
  **ASSET-cluster bootstrap**: each draw picks `len(uniq)` assets WITH replacement from the union of
  both arms' assets (5), takes ALL campaigns of the picked assets **into both arms with the SAME asset
  draw**, statistic = `mean(net_r gated draw) − mean(net_r base draw)` (per-campaign expectancy
  difference). **Not paired on kept trades; the resampled unit is the asset (5 clusters), never the trade.**
  Called at `M/scripts/tierc11_score.py:985-993` (`ruled("two_sample", …)`), point =
  `mean(va) − mean(vb)`.
- Interval / p: `T5._ci_from` `tierc5.py:1227-1236` — CI = 5th…95th percentile of the finite draws;
  `p_one_sided = (#draws ≤ 0 + 1)/(B + 1)`. Exact-p and deciding bound: `tierc11_score.py:955-970` `ci_of`
  (rank `floor((B+1)·bar)`).
- Constants TC11: `N_BOOT = 4000`, `SEED = 20260924`, `SEED_SENS = 20260816`
  (`M/scripts/tierc11_env.py:125-127`); family `FAMILY_M = 9`, `BAR = 0.10/9` (`tierc11_score.py:230-233`).
- Verdict law: `verdict_of_record(lo, hi, p)` `tierc11_score.py:1160-1167` — SUPPORTED iff CI lo > 0 AND
  p ≤ bar. Beside, deciding nothing: LOAO (`:1013-1048`, bar ceil((N+1)/2) = 3/5), sens seed, haircut twin,
  D15, concentration, era slices. Premises: SC-16 "a gate is a post-filter" `gate_findings` `:914`;
  SC-6 identical key sets flagged; refused cohort = base keys absent from the scored arm (SC-5).
- Post-filter law: `apply_gate(book, refused)` `tierc11_stage_g.py:408-411` — the SAME Trade objects,
  row-identical; LEANS L-1.5 `LEANS.md:141-150`. Forfeit note only when mean(refused) > 0.
- X adds on the face of every interval: "with 5 asset clusters the percentile bootstrap's one-sided size
  is ≈ 2× nominal under exchangeable clusters" (`X/scripts/tc11x_era.py:194-195` SIZE_FOOTNOTE; LX-1.2 (e)).

### 1.10 X4's "COMPOSITION TERM" and BREADTH
- X4 = `X/scripts/tc11x_era.py` (sha256 `f1b42be4b7012ae3c7166cf0d51195bb9c505abc126b8a68e6af49c7649b597b`),
  records `X/research_outputs/tierc11x/era/` — Tier-E only, `promotable = False` on every row.
- **Composition term** = `C_S` of the E-2 Shapley decomposition Δ = E_h − E_b = C_S (cell-weight shift)
  + W_S (within-cell change) + N (off-support), on fixed thirds (LX-X4.11; `tc11x_era.py:1584` `decompose`).
  Breadth, calendar sides of record (n_b 109, n_h 77; `X4.md:28`; `X4_tables.parquet` table E-2, block
  breadth, reading calendar): Δ +0.517948 [−0.143093, +1.121938]; **C_S +0.133382 [−0.002655, +0.261456]
  (includes 0)**; W_S +0.381127 [−0.266691, +0.991165]; N +0.003438. Tuning-twin C_S +0.077189
  [−0.079523, +0.173832]. Twins whose C_S interval lies above 0 (calendar): breadth:b10 +0.197805
  [+0.020814, +0.399969]; breadth:pool17 +0.162546 [+0.025229, +0.284400]; breadth:per_asset +0.196783
  [+0.039876, +0.345856]; cross (breadth × own age) +0.321657 [+0.164360, +0.489324] (`X4.md:39-44`).
  **Every X4 sentence reads "NO RESOLVED LATE-ERA EDGE — UNRESOLVED"** (0 of 5 resolved, `X4.md:11-17`).
  (The propensity rival also prints a column named "composition": −0.1067 calendar / −0.0668 tuning-twin,
  a point reweight with no CI, `X4.md:119-124` — a different object, opposite sign.)
- **X4's breadth of record (LX-X4.6, `X/…/LEANS_X.md:1883-1906`; `tc11x_era.py:684-775`)**: over
  **PANEL17**, member bar must have `open == entry_ms` (misaligned listed member HALTs); warm = run > 0;
  YOUNG/EARLY = `run < q50` with q50 = the trailing CLASSIC5-pooled edge at the entry bar; a member is
  **UNDETERMINED** iff left-censored at the instant AND run < q50 → out of numerator AND denominator;
  `breadth = young_determined / n_eff`, `n_eff = n_warm − n_undetermined`, floor `BREADTH_FLOOR = 5`
  (`tc11x_era.py:164`); thirds decided in integers (`third_share`, `:405-407`). Twins: breadth-10
  (CLASSIC5 + LTC XMR BNB UNI DOGE), leave-own-out, 17-pool edges, per-asset edges, censored-as-young.
  PANEL17 stems (klines opened, `era/build_manifest.json` `snapshot_files_opened`): 1000BONK, 1000PEPE,
  BNB, BTC, DOGE, ENA, ETH, HYPE, LTC, MNTUSDT_BYBIT, NEAR, PUMP, SOL, SUI, UNI, XMR, ZEC.
- **E-1 breadth thirds are NON-MONOTONE** (`X4_tables.parquet` table E-1 block breadth; `X4.md:576-615`):

  | third (share) | tuning n / E[R] / ΣR / CI | holdout n / E[R] / ΣR / CI |
  |---|---|---|
  | T1 (< 1/3) | 37 / −0.222654 / −8.238190 / [−0.540792, +0.206201] | 24 / −0.312682 / −7.504365 / [−0.673935, +0.297310] |
  | T2 ([1/3, 2/3)) | 43 / +0.483926 / +20.808804 / [+0.001596, +0.893301] | 33 / +1.459684 / +48.169579 / [+0.467482, +2.581875] |
  | T3 (≥ 2/3) | 40 / −0.340441 / −13.617625 / [−0.579087, −0.047957] | 20 / +0.073309 / +1.466173 / [−0.542621, +0.617621] |
  | unbanded | 3 / −0.092270 / −0.276810 | 0 |

  The contract's 2/5 cut falls INSIDE X4's middle third. HIGH breadth (T3) is also poor in tuning.
- E-4 cross (breadth thirds × own {YE, MAT, OLD}) is near-diagonal, every cell n < 30
  (`X4.md:1518-1521`): tuning counts T1 3/12/22 · T2 18/11/14 · T3 28/7/5; holdout T1 2/13/9 · T2 19/9/5 ·
  T3 15/2/3. "At this n the cross cannot separate panel-young from own-young."
- **Per campaign, X4 files the 17-breadth**: `X/…/era/X4_stamps.parquet` (200 rows, file sha
  `e647a9f782a204ba70c8307d8b7fcce744528b433dd7f908a276ca31f0e95683`, content sha `8dd0e6fc…`), cols
  `breadth_n_listed, breadth_n_warm, breadth_n_undetermined, breadth_n_eff, breadth_young, breadth_share,
  breadth_third, breadth_members_warm, breadth_members_undetermined, own_run, own_band, own_age3,
  edge_q25/q50/q75, edge_pool_n, b10_*, loo_*, p17_*, pa_*, cy_*`. Its `own_band` equals TC11's
  `tide_band` 200/200 (F-TIDE-X, `FIXTURES_X4.txt:32`; re-checked by this scout's merge).
- **[scout-derived, X4_stamps ⋈ g_campaign_gates on (symbol, entry_ms)]** home assets warm at the entry
  bar: 5 warm on 184 campaigns, 4 on 2, 3 on 12, 2 on 2; a home member UNDETERMINED (censored and young) on
  8; **20 campaigns have fewer than five warm-and-determined home assets — all in 2020, all tuning (last:
  2020-12-29), Σ net_r +15.089267** (the 16 with < 5 warm: ΣR +10.765796 = X4's breadth:b10 "unbanded"
  tuning row, n 16 ΣR 10.765796).

### 1.11 IS A PER-ASSET PER-BAR TIDE-BAND SERIES FILED?  **No — neither for 5 nor for 17.**
- Filed tide data are per-CAMPAIGN only (`g_campaign_gates.parquet`, `books/v6_campaigns.parquet`,
  `X4_stamps.parquet`) or distributional (`P_AGE_1_BAR_BANDS/EDGES`, X4 all-bar occupancy shares
  `occ_bars/occ_total` in `X4_tables.parquet`). A find over tierc10/, tierc11/, tierc11x/ outputs for
  per-bar tide/band/breadth tables returned none.
- In-memory producers that TC12 must mirror to file one: `LR.tide_streak(sym)` (symbol-keyed memo over
  `T7.frame`, `tierc7_lab_regime.py:306`); X's pure `tide_law(close)` (`tc11x_era.py:416-437`); X's
  `bar_cells(inp)` (`:831-1013`) which builds `RUN[G×17]`, `CEN[G×17]`, `EDG[G×3]` (the trailing CLASSIC5
  q25/q50/q75 at every grid bar by cumulative histogram `_hq`, `:813-828`, asserted == np.quantile) on
  BTC's 4h grid — but writes only third-cells, not the series.

### 1.12 THE ERA BOUNDARY
- `ERA_CUT_ISO = "2024-06-30T23:59:59Z"` / `ERA_CUT_MS = _iso_ms(ERA_CUT_ISO)` —
  `M/scripts/tierc10_panel.py:746-747`; `ERA_CUT_MS = 1_719_791_999_000` `M/scripts/tierc11_env.py:128-129`
  and `X/scripts/tc11x_env.py:147-148` (each asserted == TP's, `tierc11_env.py:991`).
- Law: era = the entry (or event-anchor) bar's **CLOSE**; tuning iff close ≤ cut, holdout after —
  `tierc11_env.py:1047-1055` `era_of`; LEANS L-1.3 `LEANS.md:95-101`; Stage G seam
  `era_of_entry(entry_ms) = E.era_of(entry_ms + 4h)` `tierc11_stage_g.py:351-354`. `TP.in_era`
  (bar OPEN) is NOT used. Straddling entry bars: 0. v6: tuning 123 (ΣR −1.3238), holdout 77 (ΣR +42.1314)
  (`STAGE_G.md:102-103`).
- "A registration naming no era is scored on the full corridor; tuning/holdout slices Tier-E"
  (`LEANS.md:99-100`). P-ADM-1 and P-BRD-1 name no era.

### 1.13 SHADOWS / ARMS ALREADY FILED (all in `M/research_outputs/tierc11/regbooks/`)
| arm | n | Σ net_r | book_sha256 (canonical CSV) | parquet file sha256 |
|---|---:|---:|---|---|
| P-AGE-1/scored (OLD alone) | 141 | +63.464131 | d008fa5086ce…f04f22d8 | 6440a6e0d14c…2a624dca |
| P-AGE-1/base = P-WIN-1/base (v6) | 200 | +40.807565 | f41bfaf02b86…369468a8 | dbfe4788610b…bad7af4ce |
| P-AGE-1/tierE__shadow_abs206 | 80 | +48.803986 | 2c1e47eec765…e385d169 | f12cef30cad2…a31726bb |
| P-AGE-1/tierE__refused_cohort | 59 | −22.656566 | 0569170404a1…0e2d9838 | 71b6444b0dbc…344edeb5 |
| P-AGE-1/tierE__tuning / __holdout | 81 / 60 | +11.462516 / +52.001614 | 4acc5b91… / f7331ba5… | 0c2efa51… / e9e4bed0… |
| P-WIN-1/scored (stale alone) | 137 | +51.974019 | fd3f407ad6b1…bdabbfe | 824c5e08ca79…db08241c |
| P-WIN-1/tierE__refused_cohort | 63 | −11.166454 | 7a97b32895c7…b3bacf6 | a92c55895964…7900d89b |
| P-WIN-1/tierE__shadow_lag7_15 | 196 | +43.085655 | f624bffc3bae…66d7fae | 4b308d854a30…778f589c |
| P-WIN-1/tierE__tuning / __holdout | 81 / 56 | +8.022567 / +43.951452 | 862fc6fd… / 7cdb206b… | d5dbd141… / 797b440c… |
| P-WIN-1/tierE__ratr_admission | 147 | +19.115450 | dcfffefbddad…033201c8 | 92be97b10f21…266147b9 |
| P-WIN-1/tierE__ratr_priority | 165 | +18.392480 | a10416bd49c4…403a7f3 | 50a2cc140c54…021befd9 |
(`STAGE_G.md:901-931`; full shas there and in each sidecar `<arm>.json`; file shas re-hashed this session.)
**NOT filed**: any per-trade book for the COMBINED refusal (only the aggregate row in g_grid_books), any
breadth-5 quantity, any breadth refusal, any slot-arbitration book.

### 1.14 SIGNATURES TC12 can import or must mirror
`M/scripts/tierc11_stage_g.py` (sha256 `17235ed2078ad37ab84a241ce9b0c96e30a2ec2ddbbfda545c4638e2b770b77a`):
```
registrations() -> dict                                  :259
v6_replay(lo: int, hi: int) -> tuple[list, dict]         :285   (book, {sym: arms}) held to V6_BOOK_SHA
key_of(t) -> tuple                                       :302   (symbol, entry_ms)
age_of(t) -> tuple[int, bool]                            :309   (run, left_censored) at ENTRY bar
edges_of(t, pool: dict)                                  :315   [q25,q50,q75] | None
old_refused(run: int, edges) -> bool                     :321   band == 3 (B4)
abs_refused(run: int) -> bool                            :326   run > 206
lag_of(t) -> int                                         :331   entry_i - arm_i
win_refused(lag: int) -> bool                            :335   lag >= 16
lag7_15_refused(lag: int) -> bool                        :339
ratr_of(t) -> float ; ratr_refused(r: float) -> bool     :343 / :347   (> 2.2)
era_of_entry(entry_ms: int) -> str                       :351
band_code(run: int, edges) -> str                        :357
facts_of(t, pool: dict) -> dict ; facts_frame(book, pool) -> pd.DataFrame   :364 / :398
refused_keys(facts, gate: str) -> set ; apply_gate(book, refused: set) -> list   :402 / :408
replay_g(sym, lo_ms, hi_ms, *, refuse=None, priority_cut=None, pool=None) -> tuple[list, list]   :449
replay_book(lo, hi, **kw) ; refuse_hook(gate: str, pool: dict)               :537 / :547
blocker_of(arm, trades_sym) ; rival_rows(arms, v6, pool, facts) -> pd.DataFrame   :569 / :579
haircut(stem, net_r, fee_r) -> float ; regbook_frame(book, pool) -> pd.DataFrame   :611 / :631
canonical_csv(df) -> bytes ; book_sha256(df) -> str      :683 / :703
write_regbook(d, reg, arm, kind, ruler, era_scope, …)    :1168
REQUIRED (16 cols) :180-182 · GATES :209-218 · GRID_FLAGS :220 · COLLAR :173-174
```
`M/scripts/tierc11_books.py` (sha `e025499d92b25231c676aaac17abffedba4dcc9d4821174fcd9f3566bd821313`):
`tide_pool(lo, hi) -> dict` :358 · `entry_streak(t) -> (run, cens, state)` :363 ·
`trailing_edges(t, pool)` :371 · `band_of(run, edges) -> int|None` :378 (HALTs on a null band under warm
edges) · `lag_band(lag) -> str` :389 · `known_window_end(end_i, hi_i)` :396 · `v6_book(lo, hi)` :289 ·
`corridor(pin_close_iso=None)` :254.
Lineage (by object): `tierc7_lab_regime.tide_streak / _streak_band / STREAK_LABELS /
STREAK_BAND_QUANTILES / TIDE_WARM_BARS` (sha `4d19cf0095ebf2593b3008caf9c9af032a75515dda8507da5154308e977682a5`);
`tierc9._trailing_pool / _trailing_edges / tide_streak_age / replay9 / card_candidates9 / armings9`
(sha `663eef3107909221a6a651343363bad5c7d7730dd9adb92495d3f1e262c5b3c3`);
`tierc5.cluster_boot / cluster_boot_diff / _ci_from / d15` (sha `ad912b385cc8dd2e5291af3b79c520760ae8c91764af8e3eee56c6b3dd295a6f`).
Scorer `M/scripts/tierc11_score.py` (sha `81d99d63f9367268780fe9ec37a0c6af058b03670a83aaff010a93090eab5d68`):
`ci_of(draws, point)` :955 · `ruled(ruler, a, b, col, seed, n_boot)` :973 · `loao(…)` :1013 ·
`clears_bar(p)` :1151 · `verdict_of_record(lo, hi, p)` :1160 · `gate_findings(a, b, tag)` :914 ·
`gate_block(a, b)` :1206 (BAR is a module constant `:232` — must be re-parameterised, never imported).
X (mirror only): `tide_law(close) -> (state, run, start, e_f, e_s)` `tc11x_era.py:416` ·
`_band(run, edges)` :587 · `third_share(y, n)` :405 · `_stamp_one(inp, dv, sym, entry_ms, direction)` :600 ·
`stamp_campaigns(inp, camps)` :804 · `_hq(cum, n, q)` :813 · `bar_cells(inp, replay_at=())` :831 ·
`derive(inp) -> Derived` :517 · dataclasses `Tape` :371, `Inputs` :389 · `abs_tide_cut()`
`tc11x_books.py:347`.

### 1.15 RECORDS TC12 WILL PIN (sha256 by `shasum -a 256`, this session)
MAIN:
- `M/research_outputs/tierc11/registrations/REGISTRATIONS.json` `648834bf30e20e92713bddef2374ddef1aae843f4d8ba152fc50166c8cc6f1ee`
  (P-AGE-1 payload `e01a89ea7e6fda864f7002a450abd1a4e92424c44d1a9626f6641814e7d35879`, P-WIN-1 payload
  `d19a42a329be3bfeea73c3c628bf515f5d0fa2fb8facd3fcac795b0186525084`); `REGISTRY_PIN.json`
  `ea77921a410db962376412a5f179fd3d9225f81fb5405a788c8077cd46de748f` (head `6772568b…`).
- `M/research_outputs/tierc11/LEANS.md` `655e1605165e7a66c67f544e5cda421b46aa0b6fcd4cb97a6ad19654479f294f`;
  `LEANS_AMENDMENTS.md` `85f57ce7832b2754cff70fe052dc87dcf4bcf4182f61112c7a1d227df84f0c07`;
  `M/exchange/queue/2026-09-24_TC11_APOLLO.md` `bb38e016a8f3e55ca3bcc09fec53ba6b8dc40accb60d054f8163d033a898f835`.
- `stage_g/STAGE_G.md` `440509bc8c00bc32b48f745a8f76ca1b6c6d6ddb08f708432790ec164e2d0187`;
  `stage_g/build_manifest.json` `a9277d05fac2b8000a2b6cc6c2d344417efe183a36d309e718e15e37245e8122`;
  `stage_g/FIXTURES_STAGE_G.txt` `30389af6bd53b557892fc1af085b66eac25bdb8cdd6a03c2c8a9e8229ea179ae` (9 GREEN, 0 RED).
- `stage_g/g_campaign_gates.parquet` `c5a5f486df5709c0386e8733c9cc2490b1a15e6416b6f5adf45efcae608674d6` (content `196ddc1c…`);
  `g_grid_partition.parquet` `977ed42f…ec74917`; `g_grid_books.parquet` `b2c786e0…3b7b51b`;
  `g_gate_rows.parquet` `f7e4b5557f11aacbc8fbade03148eb5a10cdeea9840120822643233bfa499121`;
  `g_lag_bands.parquet` `0e747f962c56747c4867432ece2d1a6bd584d1cd09147f34886ed8179c578ecc`;
  `g_tide_bands.parquet` `ba26f34ae39afab1108a207f71cbc547e0d6a04348fb7bb50c26420d3db91bb3`;
  `g_rivals.parquet` `e65f8dbf473f30cb7da2bee0fbcc3c3f452a3c576dd7b3af47a2e77b2de6d58d`;
  `g_priority_windows.parquet` `5cdbfa847f154cf887413c7cdbfe5adfd5514d0a1d1c745ebb93e0416fed1e4a`;
  `g_collisions.parquet` `9fe7993fa555dac9183ea5794839a0e9cbffa13a0de56cb1bfbde739f23be3a6`.
  (All match `M/research_outputs/tierc11/PROGRESS.json` stages[TC11-G].artifact_shas.)
- regbooks: see 1.13 (+ sidecars `P-AGE-1/scored.json` `75ea0a19…`, `P-WIN-1/scored.json` `c9b254f9…`,
  STATUS `5593031c…` / `66ce56d1…`).
- `books/v6_campaigns.parquet` `aab06934ae92689ef2e0fcc6b857350cf397ddca7a0a57e180960c51669b28e5`
  (content `a5d0c57087c9…`), `books/v6_journal.parquet` `deb70b099593f0a8096f3437e0a1aa5dfb5d6a9835dc596d161303ee86b42a5c`.
- `scores/SCORES.json` `2c1a664a27abfc320355dcb89b2eff8a7f7637ddc26843e72ab3baf30cbef856`;
  `scores/FAMILY.json` `3fa36bd482eac4de729b0e1ff2a66e7becbc30f2646ce16fc0df8fc369b2fd73`.
- `M/research_outputs/tierc10/close/P_AGE_1_TIDE_YOUTH.parquet` `377c73effb1d23af95075bb53a297fc6387c515db5769cabb41684b293b3750f`;
  `P_AGE_1_BAR_BANDS.parquet` `b501e543226fae5ea16d7abbd845c222b1bfa5fef1376967435adbf0fa67ea69`;
  `P_AGE_1_EDGES.parquet` `8c2395703bd0eee6f8bca1fb3c65bbb6b683941930a77b9c1ebb4cabb3d424d1`;
  `P_AGE_1_TIDE_YOUTH.md` `b1c5a7bc5c4f5c7db98187dc6ca1720329cb6d6e0b21d1360d9449ed6512a56f`.
X:
- `X/scripts/tc11x_era.py` `f1b42be4b7012ae3c7166cf0d51195bb9c505abc126b8a68e6af49c7649b597b`;
  `tc11x_era_fixtures.py` `4429dec5586893d4cad4bc9dfe5110dd69d0a9ef0e470bf0270dbe04186660d0`;
  `tc11x_pct.py` `49809c070ed00223a345edc51b5d83355f229a6b1372495038ff42aeba204bb7`;
  `tc11x_books.py` `26870ff97317801fdf9c4874e1f41cdac69bacbf9263198e623e19ab19913b2b` (per BOOK_SPECS.json path_modules).
- `X/research_outputs/tierc11x/era/X4.md` `aac2be88b8d71f46c232a1976cd5d06dd5ded91b3356976050a48344e9557be8`;
  `X4_stamps.parquet` `e647a9f7…f0e95683`; `X4_tables.parquet`
  `fda7a280b76e295b5faf06119061e3243461c50c6d0d941daecf1b4715a1e5b0` (content `4f01ec8f…`, 1458 rows);
  `era/build_manifest.json` `0ad7f6eac56a003bbcc694115f54f347dcb2d20895da414d1615410cfc34a642`;
  `era/FIXTURES_X4.txt` `2c942f8c855835ebaa5a3dc778be0f360064673ed27c96d15bdbe857a08e4e58` (8 GREEN, 0 RED).
- `X/research_outputs/tierc11x/LEANS_X.md` `74a989ee6357e2169f2ad88722b67f1174cf0d080783dc8c77f5f064e3468623`.
- `X/…/forward/BOOK_SPECS.json` `72a1f523…8b1f51cac3`; `FORWARD_LEDGER.jsonl` `4a6da7e8…92cfa4c5`;
  `FORWARD_LEDGER.md` `64d4529670d1fcc730b194f2e7d885df05f7fb004c9dc45c0cec3b5656eb6572`.

### 1.16 SCHEMAS of the tables TC12 will read
- **`stage_g/g_campaign_gates.parquet`** (200 rows, key [symbol, entry_ms], floats 6 dp):
  symbol:string, entry_ms:int64, entry_close_ms:int64, direction:int64, arm_i:int64, arm_ms:int64,
  entry_i:int64, era:string, net_r:double, tide_streak_entry:int64, tide_left_censored:bool,
  tide_edge_q25:double, tide_edge_q50:double, tide_edge_q75:double, tide_band:string,
  tide_streak_age_arm:int64, tide_streak_age_arm_censored:bool, arm_band_on_entry_edges:string,
  arm_old_on_entry_edges:bool, arm_age_gt206:bool, lag:int64, lag_band:string, r_over_atr:double,
  age_old_refused:bool, age_abs206_refused:bool, win_refused:bool, lag7_15_refused:bool,
  ratr_refused:bool, grid_cell:string ("A0|W1|S0"), + collar (tier, selection_not_a_result, gates) + the
  nine as-of stamps (as_of_last_closed_4h, as_of_panel_start, as_of_span_days:double, warranty, as_of_lens,
  as_of_last_closed_bar, as_of_panel, as_of_n_assets:int64, as_of_substrate).
- **`g_grid_partition.parquet`** (8, key [cell]): cell, age_old:bool, lag_ge16:bool, ratr_gt2p2:bool,
  n:int64, mean_net_r, sum_net_r, win_pct:double, nan_reason:string, collar, stamps.
  **`g_grid_books.parquet`** (8, key [cell]): cell, age_gate_on, win_gate_on, ratr_gate_on:bool, n,
  mean_net_r, sum_net_r, win_pct, nan_reason, n_refused:int64, sum_net_r_refused:double, collar, stamps.
- **`g_gate_rows.parquet`** (5, key [gate]): gate, registration, rule, caveat, n_base, sum_net_r_base,
  n_gated, sum_net_r_gated, mean_net_r_gated, n_refused, mean_net_r_refused, sum_net_r_refused,
  forfeit_note, rival_count_rejection_log:int64, rival_count_self_refused:int64, reride_n,
  reride_sum_net_r, reride_mean_net_r, reride_admitted_not_in_v6, reride_v6_not_taken, collar, stamps.
- **regbook arm** (e.g. `P-AGE-1/scored.parquet`): the 16 REQUIRED — symbol:string, entry_ms:int64,
  entry_close_ms:int64, direction:**int8**, entry_px, stop_px, r_dist:double, exit_close_ms:int64,
  exit_reason:string, net_r, gross_r, fee_r, funding_r, haircut_net_r:double, era:string, lane:string —
  then extras arm_ms, arm_i, entry_i, exit_ms:int64, exit_px:double, exit_event_ms:int64,
  exit_event_stamp:string, atr_at_entry, mfe_r:double, n_advances:int64, harvested, reached_1r:bool,
  slip_bps_side:double, slippage_tier:string, lag:int64, r_over_atr:double, tide_streak_entry:int64,
  tide_edge_q75:double, tide_band:string, tide_streak_age_arm:int64, priority_substitute:bool,
  harvest_close_ms:Int64, + stamps. Sidecar keys: `SIDECAR_KEYS` `tierc11_stage_g.py:187-189`.
- **`books/v6_campaigns.parquet`** (200, key [symbol, entry_ms]): symbol, entry_ms, book, roles_name,
  lane, direction:int64, arm_i, arm_open_ms, arm_close_ms, entry_i, entry_open_ms, entry_close_ms, exit_i,
  exit_ms, exit_close_ms, exit_event_ms, exit_event_stamp, exit_reason, open_at_asof:bool, entry_px,
  stop_px, r_dist, atr_at_entry, r_over_atr, r_over_atr_gt_2p2:bool, lag, lag_band, window_end_i,
  window_end_close_ms, window_open_at_asof:bool, harvested, harvest_i, harvest_close_ms, reached_1r,
  latch_1r_i, latch_1r_open_ms, net_r, gross_r, fee_r, funding_r, era_of_entry,
  entry_bar_straddles_era_cut:bool, tide_state_entry, tide_streak_entry, tide_left_censored,
  tide_trailing_edge_q25/q50/q75, tide_band, tide_band_label, tide_abs_gt206:bool, tide_streak_age_arm,
  tide_streak_age_arm_censored, entered_after_tc10_pin:bool, continuation:bool, + stamps.
  On this file: exit_reason {stop 196, bell_12_89 4}; open_at_asof 0; window_open_at_asof 3;
  continuation 1; entered_after_tc10_pin 0.
- **`P_AGE_1_BAR_BANDS.parquet`** (8): basis, basis_used:bool, band:int64, band_label, edge_lo_bars,
  edge_hi_bars:double, n_units:int64, unit, unit_share_pct, median_streak_bars, median_streak_days,
  n_campaigns_v6:double, n_left_censored:double, share_<5 assets>:double, provisional, … + collar/stamps.
  **`P_AGE_1_EDGES.parquet`** (7): as_of:string, vol_rel_edges_trailing, streak_edges_trailing,
  vol_rel_edges_whole_corridor, streak_edges_whole_corridor: list<double>, …
  **`P_AGE_1_TIDE_YOUTH.parquet`** (5: bands 01..04 + 99-ALL): dimension, band, band_label, n, net_r,
  expectancy_r, win_rate_pct, …, n_left_censored, streak_bars_at_entry_min/median/max, banding, …
- **`X4_stamps.parquet`** (200, key [symbol, entry_ms]): see 1.10 list; also vol_*, fund_*, btc_* stamps,
  `cell__<block>` strings, era, cal_side, lane, collar (+ would_read_ci_only, m_looks_this_table, m_note,
  promotable:bool), stamps (as_of_panel = PANEL17).
- **`X4_tables.parquet`** (1458, key [table, block, reading, cell, side]): tables {E-1 376, E-2c 236,
  E-3 224, E-1d 188, E-4 184, E-4d 92, E-3p 80, E-2 44, D-1 32, E-2p 2}; stats n, n_b, mean_r, sum_r,
  p_win, ci_lo, ci_hi, delta, delta_ci_lo/hi, c_s, w_s, c_s_ci_lo/hi, w_s_ci_lo/hi, n_term, occ_*, ….

---------------------------------------------------------------------------------------------------
## 2 · CONTRACT-vs-DISK

1. **"refuse a trigger when the tide age at the entry bar is in the OLD band"** — disk gates CAMPAIGNS,
   not triggers: every TC11 gate is a POST-FILTER of the v6 book (`apply_gate`, L-1.5); the trigger-level
   evaluation exists only as the Tier-E re-ride hook (`refuse_hook`, `tierc11_stage_g.py:547-566`). On
   TC11's corridor the two coincide (rival 0, re-ride book == post-filter book for all five gates,
   `STAGE_G.md:58-62` reride_admitted_not_in_v6 = 0).
2. **"the OLD band (trailing q75, the cut of record)"** — "trailing" on disk is an EXPANDING pooled-CLASSIC5
   prefix from 2019-09-08T16:00Z (no window length), entry bar inclusive, ≥ 30 bars; comparator `>=`.
   The tide age is the two-state entry-bar run, not the arm-bar three-state age that also exists on disk.
   Two treatments of an unbanded campaign are on disk: Stage G treats it as NOT refused
   (`old_refused` returns False when edges is None, `:321-323`); X5's frozen spec says `none_band: "HALT"`
   (BOOK_SPECS.json). (0 unbanded on the corridor, so neither has ever fired.)
3. **"the window age (entry_i − arm_i) ≥ 16 bars"** — identical on disk; but "16" is a typed constant
   whose only provenance is the TC11 contract's own sentence (`LEANS.md:373` "no on-disk provenance").
   The contract's law "no number typed that a file can supply" can be met only by reading it from
   REGISTRATIONS.json P-WIN-1 `text_of_record` ("lag ≥ 16 bars") / the TC12 contract line 54.
4. **"Label pre_seen (TC11 crossed table cell 110 @ +0.515)"** — the disk has TWO crossed tables; the cell
   is in the GATE-BOOK table (b), not the partition (a). "110" is both the bit pattern (age on, win on,
   ratr off) and n. "+0.515" is the book's E[net R] (0.514611), not an effect size: the implied point Δ vs
   v6 is +0.310573 and **no interval, p, LOAO or per-trade book was ever filed for it**.
5. **"Shadows printed: OLD alone · stale alone · the absolute-206 cut"** — OLD alone and stale alone exist
   as filed regbooks (1.13). "The absolute-206 cut" on disk is a shadow of P-AGE-1 ALONE (refuse run >
   206; n 80). Whether TC12 means that arm, or the combined refusal with 206 substituted for the trailing
   OLD edge (run > 206 OR lag ≥ 16), is not said. 206 is the whole-corridor MEDIAN on TC10's and TC11's
   corridors ([88.0, 206.0, 396.0] both); on TC12's longer corridor the whole-corridor median need not
   still be 206.
6. **"both two-sample vs v6 — they remove trades"** — disk: asset-cluster bootstrap of the difference of
   per-campaign MEANS, same asset draw into both books, 5 clusters. The contract gives the family
   (m = 2, bar 0.05) but not the verdict clause; TC11's is two-clause (CI lo > 0 AND p ≤ bar).
7. **"(m=2, bar 0.05)"** — the same numbers that were NOT SUPPORTED at TC11's bar read differently at
   0.05: stale-alone's filed p is 0.036491 with CI lo +0.002964 (> 0). "No re-family of TC11" (contract
   :133-134) means the stale-alone SHADOW must carry no verdict word.
8. **"breadth = share of the five home assets whose tide band is YOUNG or EARLY"** — no five-asset breadth
   exists on disk. X4's breadth is over PANEL17 with an UNDETERMINED class and a floor n_eff ≥ 5; its
   constant-membership twin is breadth-10. The contract is silent on (a) which edges band the other four
   assets, (b) unwarm members, (c) left-censored members, (d) whether the campaign's own asset counts.
   20 of 200 campaigns (all 2020) have < 5 warm-and-determined home assets.
9. **"direction informed by X4's composition term"** — X4's breadth composition term (C_S +0.1334) has an
   interval that INCLUDES 0 on the reading of record; it is positive-and-resolved only on three twins;
   X4's sentence for breadth is "NO RESOLVED LATE-ERA EDGE — UNRESOLVED". C_S measures an ERA shift in
   cell weights, not the E[R] of low-breadth trades; the "refuse low" direction actually comes from E-1's
   T1 row (−0.22 / −0.31), and E-1 is non-monotone (T3 also negative in tuning).
10. **"Tier-E: the whole breadth {0..5} × own-band grid; breadth-17 twin"** — the 17-breadth per campaign
    is filed for TC11's 200 campaigns (X4_stamps), so the twin has an oracle there; nothing exists for the
    extension or per bar.
11. **"the crossed table 2×2×2×2 (OLD · stale · far stop · low breadth)"** — TC11 printed its cross two
    ways (partition and gate books); the contract names one table.
12. **"far-stop PRIORITY simulated as slot arbitration (when two armings compete for an asset, prefer the
    farther structural stop…)"** — on disk two armings NEVER compete for an asset: `n_position_open_v6 = 0`
    over the whole corridor (v6's windows of one asset are disjoint; a window gives at most one entry).
    The only priority book on disk prefers the NEARER stop inside one window and is an in-window
    substitution, not an arbitration. As literally written the simulation is an identity (book ≡ v6).
13. **"refusing forfeited +21.69R"** — matches `sum_net_r_refused +21.692115` (53 campaigns with
    r_over_atr > 2.2, mean +0.4093). "Far" has a filed pin: 2.2 ATR14_4h, strict `>`.
14. **Which corridor is scored** — Stage C (contract :48-50) re-rides v6 on the extended corridor and calls
    the extension "the forward strip, never scored"; Stage G says nothing. Every filed number that the
    pre_seen label quotes (110, +0.515) lives on TC11's corridor (hi + 1 = 1790294400000).
15. **Per-asset per-bar tide bands** (needed for breadth, for the {0..5} grid, and for Stage S's regime
    columns "breadth · 4h tide age", contract :102-103) — not filed anywhere.

---------------------------------------------------------------------------------------------------
## 3 · READINGS NEEDED (candidate leans, to freeze BEFORE building)

**R-G1 · the tide age of record.** Options: (a) entry-bar two-state run `LR.tide_streak(sym)[1][entry_i]`
(TC11 L-G.1); (b) arm-bar three-state `T9.tide_streak_age`. **Recommend (a)** — it is the filed pin
(P-AGE-1, X5 BOOK_SPECS lineage_functions); (b) printed as the F-DEF disclosure only.

**R-G2 · "trailing q75".** Options: (a) TC11's law verbatim — expanding CLASSIC5 bar-pooled prefix from
`pool_lo_ms = 1567958400000`, bars with open ≤ the entry bar's open, ≥ 30, np.quantile linear,
OLD ⇔ run ≥ q75; (b) a rolling window; (c) whole-corridor edges. **Recommend (a)**, with `pool_lo_ms`
READ from X's BOOK_SPECS.json and asserted against the extended corridor's panel start (HALT on a move),
and the 200 TC11 campaigns' (run, q25, q50, q75, band) asserted equal to g_campaign_gates on the extended
substrate (TIDE-PREFIX). Unbanded campaign: **recommend X5's `none_band: HALT`** (a None band at a v6
entry means the floors diverged) over Stage G's silent "not refused".

**R-G3 · the stale cut and its source.** Options: (a) type 16; (b) read it by object from the TC11
registration text (P-WIN-1 `text_of_record` "lag ≥ 16 bars") and HALT unless the TC12 contract line says
the same number; lag = entry_i − arm_i in 4h bars, comparator `>=`. **Recommend (b)** (X's
`abs_tide_cut()` precedent; satisfies "no number typed that a file can supply").

**R-G4 · refusal = post-filter or in-replay.** Options: (a) POST-FILTER of the v6 book (L-1.5): gated =
v6 minus (OLD ∪ stale), same Trade objects, no entry admitted into a freed slot; re-ride with the refusal
hook printed beside as Tier-E with the rival count; (b) refuse inside the replay. **Recommend (a)** — the
filed law of both TC11 (regbooks) and X5 (the third ledger book), it is what makes the pre_seen cell
reproducible to 0.000e+00, and it cannot gain trades the base never took.

**R-G5 · the scored corridor.** Options: (a) TC11's corridor (hi + 1 = 2026-09-25T00:00Z): base =
the filed v6 book (n 200, TP sha f3c68f54…), P-ADM-1's scored arm must then equal cell 110 (n 110,
ΣR +56.607236) exactly; campaigns of the extension go only to the forward strip / ledger; (b) the whole
extended corridor. **Recommend (a)** — it is what "the forward strip, never scored" and "verdict disclosed
as in-sample" describe, it reuses the filed pin, and it keeps the extension unseen for the ledger's fourth
book. Print the extended-corridor twin Tier-E. (Cross-check with the control/corridor scout.)

**R-G6 · the verdict clause, seed and draws.** Options: (a) TC11 L-1.4's rule with the family bar
swapped: SUPPORTED iff CI lo > 0 AND p ≤ 0.10/2, `T5.cluster_boot_diff`, N_BOOT by object (4000), seed
20261008 (contract line 4), sensitivity seed 20260816 beside, exact p (`20(k+1) ≤ B+1`, deciding rank
200), LOAO / haircut / era slices / concentration beside and deciding nothing; (b) CI-only; (c) p-only.
**Recommend (a)**. Fixture: the mirrored scorer at TC11's seed 20260924 must reproduce SCORES.json's
P-AGE-1 and P-WIN-1 `stats.main` exactly.

**R-G7 · "the absolute-206 cut" shadow.** Options: (a) refuse run > 206 ALONE (TC11's filed arm, n 80);
(b) run > 206 OR lag ≥ 16 (the like-for-like shadow of the combined refusal); (c) both. Source of 206:
(i) typed; (ii) read by object from P-AGE-1's text (X's law) and cross-checked against
P_AGE_1_BAR_BANDS `edge_hi_bars` = 206.0; (iii) recomputed as the extended corridor's whole-corridor
median. **Recommend (c) with (ii)**: (a) anchors to book_sha256 2c1e47ee… on TC11's corridor, (b) is the
informative shadow; never (iii) — print the extended corridor's whole-corridor median beside as a
disclosure. Comparator strict `>`. Label carried: "look-ahead; the median edge, not the OLD edge".

**R-G8 · breadth-5, the banding of the other assets.** Options: (a) each home asset's run at the bar whose
open == the entry open, banded on the SAME trailing CLASSIC5-pooled edges as P-AGE-1 at that bar
(YOUNG/EARLY ⇔ run < q50); (b) per-asset own-history edges; (c) 17-pool edges. **Recommend (a)** (one
banding law for the whole family; X4 LX-X4.6's pin); (b)/(c) are X4's twins — print if cheap.

**R-G9 · breadth-5, unwarm and left-censored members, and the denominator.** Options:
(a) LITERAL: y = number of the five that are warm, run < q50 and NOT left-censored-at-the-instant
(X4's determined-young); denominator FIXED at 5; refuse iff y < 2, decided in integers (5·y < 2·5);
(b) X4's law transplanted: breadth = y / n_eff with n_eff = warm − undetermined, undefined (gate silent)
when n_eff < 5; (c) face-value bands (a censored young member counts young — the lab's "censored-as-young").
**Recommend (a)**: it is the contract's own fraction, adds no typed constant, reuses X4's censoring pin
("the streak's eventual length is never read"), and admits least on unconfirmed youth. It cannot flatter:
the 20 campaigns it treats differently from (b) sum to +15.09 R [scout-derived], so the reading that
refuses more of them is the conservative one. Print (b) and (c) as twins; print n_warm / n_undetermined /
member list per row. Affects only 2020 entries.

**R-G10 · does the campaign's own asset count in breadth?** Options: (a) yes — "the five home assets";
(b) leave-own-out. **Recommend (a)** of record, **(b) printed as the twin** (X4: the own term is a
mechanical 1/n share and breadth is near-collinear with own age).

**R-G11 · P-BRD-1's disclosures.** Print, beside the row: the overlap of the breadth-refused set with OLD
and with stale (n, ΣR of refused∧OLD, refused∧¬OLD), the breadth-17 twin, and the label "direction
informed by X4 (E-1 T1; composition term C_S +0.1334 [−0.003, +0.261], sentence UNRESOLVED) — selection
hazard". **Recommend** making these mandatory columns of the gate row (the L-1.5 gate-row law extended).

**R-G12 · the crossed table's layout.** Options: (a) the 16-cell PARTITION by the four flags; (b) the 16
GATE BOOKS (v6 minus the union of the refusals switched on); (c) both. **Recommend (c)** (TC11's L-G.3
precedent; F-GRID asserts 16 + 16; n = 0 cells carry NaN and a nan_reason). Far-stop bit = r_over_atr >
2.2 read by object from TC11's record (RATR_CUT / L-G.3); it is a FLAG and a hypothetical gate-book
column only — never a registered refusal.

**R-G13 · the far-stop priority as slot arbitration.** Options: (a) literal: the competition set is the
v6 ride's `position_open` rejection log; when it is empty the arbitration book IS v6 and the table says so
("0 competitions; identity"), with TC11's two filed far-stop books printed beside as context;
(b) an in-window rule preferring a LATER, farther-stopped cross (needs either a wait or knowledge of a
later trigger: a new entry rule); (c) a cross-asset cap. **Recommend (a)** and file a finding for APOLLO:
(b) is entry-cross research the contract forbids (:132) and would need a typed rule; (c) has no cap on
disk. Count asserted on both corridors.

**R-G14 · the regbook interface.** **Recommend** mirroring TC11's (16 REQUIRED columns, canonical-CSV
`book_sha256` law, sidecar keys, STATUS.json) so TC12's "OLD alone" and "stale alone" shadows hash to
d008fa50… and fd3f407a… on TC11's corridor (a free cross-tier anchor) and the fourth ledger book has a
per-trade file.

**R-G15 · the fourth-vs-third disclosure.** The combined book beats the OLD-gated book on mean and loses
on ΣR (stale-only increment n 31, ΣR +6.86 [scout-derived]; L-1.5's forfeit note would not fire because
mean(all 90 refused) < 0). **Recommend** printing the increment cohort and "forfeits +X R vs the
OLD-gated book" on P-ADM-1's gate row.

**R-G16 · era slices.** **Recommend** TC11 L-1.3 unchanged: full corridor scored; tuning / holdout by the
entry bar's CLOSE, `ERA_CUT_MS` by object from TP, Tier-E.

---------------------------------------------------------------------------------------------------
## 4 · HAZARDS

Determinism / substrate
- **H1** `tierc11_env` HALTs unless `NAIAD_CACHE_DIR` is the TC11 snapshot (`tierc11_env.py:193-210`) and
  clamps the corridor to TC11's AS_OF_PIN (`:981-982`). `import tierc11_stage_g` (→ tierc11_books →
  tierc11_env) is therefore impossible under a TC12 snapshot; TC10's `tierc10_close_*` scripts HALT at
  import (`tierc11_books.py` docstring :32-33). TC12 needs its own shim and MIRRORED seams.
- **H2** `LR.tide_streak`, `T9.frame`, `T9.role_arrays`, `LR._CUTS` are symbol-keyed memos bound to the
  cache at import — one process serves one snapshot and cannot take a truncated/spiked tape (X's reason
  for the pure route, `LEANS_X.md:1872-1877`). Cross-corridor anchors must be cross-process.
- **H3** The trailing edges depend on `pool_lo` and on EVERY pooled bar's run, and the run depends on the
  EMA seed at each tape's first bar. A top-up that re-fetches early klines, changes a first bar, or moves
  the panel start silently moves q25/q50/q75 at every entry (and every breadth value) while F-CTRL on the
  v6 book could still pass. Needed: pool_lo assertion + TIDE-PREFIX on the 200 filed campaigns.
- **H4** Flags are computed at FULL precision and the tables are written at 6 dp
  (`tierc11_books.py` PRECISION note :83-87). Re-deriving a flag from the 6-dp table can flip a boundary
  case; identity checks must read Trade objects. q75 is often non-integer.
- **H5** Three sha laws coexist: `TP._book_sha` (sorted [symbol, lane, entry_ms, repr(net_r)]), the
  canonical-CSV `book_sha256`, and parquet CONTENT sha vs FILE sha (STAGE_G.md's "Files" list prints
  content shas; PROGRESS.json prints file shas). Pin each by name.

Causality (look-ahead)
- **H6** Whole-corridor edges (`LR.cuts`) in place of trailing ones; a pool prefix taken to the entry
  CLOSE (admits bars opening at entry_close — "one-bar-ahead", F-DEF DEF-EDGE); 206 itself (a
  whole-corridor number); `armings9` scans the whole tape for `window_end_i` (`tierc9.py:181-183`,
  repaired by `known_window_end`); a censored streak's eventual length; a breadth member bar whose open is
  not the entry open; reading the 17 by PANEL17 admission instead of warmth at the instant.
- **H7** `era_of` by bar OPEN (`TP.in_era`) instead of CLOSE moves campaigns across the cut (F-EDGE).

Selection / inference
- **H8** P-ADM-1's point is fully pre-seen (n 110, +0.5146, Δ +0.3106); its only new information is the
  interval. With 5 clusters a draw's sign depends only on five per-asset sums, the bootstrap's one-sided
  size is ≈ 2× nominal, and ZEC's single +25.06 R trade is 44 % of the kept ΣR.
- **H9** P-BRD-1 is not unseen either: the breadth-17 quantity is filed per campaign, and **this scout
  computed, as orientation, X4's PANEL17 share at the contract's cut — share < 0.4: n 76, ΣR −11.7261,
  mean −0.1543 (39 of them OLD); ≥ 0.4: n 121, ΣR +52.8105, mean +0.4365; undefined 3** [scout-derived,
  X4_stamps ⋈ g_campaign_gates]. The breadth readings above were recommended on text and filed pins, but
  the executor must freeze them without tuning on this, and the label must say the direction was visible.
- **H10** Breadth is near-collinear with own tide age (X4 pitfalls, `X4.md:1576-1584`, collinearity at :1581); a breadth refusal
  largely re-refuses OLD campaigns. Without the overlap split, P-BRD-1 re-scores P-AGE-1.
- **H11** Moving from m = 9 to m = 2 changes words for unchanged numbers (stale alone: p 0.0365). Shadows
  must be collared, no verdict word (`would_read_ci_only`).
- **H12** The combined refusal's stale leg removes a positive-ΣR cohort (H/R-G15); mean-based two-sample
  scoring rewards that. Print ΣR beside every mean.

Isolation / frozen records / operator acts
- **H13** X worktree: certified tip 7b24f835 must not gain a file or commit; it already shows one
  untracked file (`research_outputs/tierc11x/close/CERTIFIED_TIP`). Importing X modules from the worktree
  would write `__pycache__` unless PYTHONDONTWRITEBYTECODE is set, and `tc11x_env` guards the TC11 snapshot
  too. Vendor X4's laws into the main tree, pinned by the sha of `tc11x_era.py`; read X records by
  absolute path only.
- **H14** Never call `build()` / `main()` of `tierc11_stage_g.py`, `tierc11_score.py`, `tc11x_era.py`:
  they write into `research_outputs/tierc11|tierc11x` (frozen; TC11's and TC10's operator close acts are
  pending). MAIN currently shows a modified tracked file
  `research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt` and untracked pine/HTML files —
  not TC12's to touch or commit.
- **H15** Ledger overlap: the forward ledger opens at 2026-09-21T16:00Z, before TC11's pin. On disk no
  campaign entered in between (`entered_after_tc10_pin = 0`, `g_arrivals.parquet` placeholder), so no
  campaign is both scored in-sample and appended forward; this must be re-asserted, not assumed, when the
  fourth book is opened.
- **H16** Post-filter ≠ re-ride on a longer tape: rival 0 holds on TC11's corridor only; the extension
  must re-count (`n_reride_differs`, X5's law).

---------------------------------------------------------------------------------------------------
## 5 · REUSE PLAN

IMPORT BY OBJECT (lineage, through a TC12 env shim modelled on `tierc11_env` / `tc11x_env`):
- `tierc7_lab_regime`: `tide_streak`, `_streak_band`, `STREAK_LABELS`, `STREAK_BAND_QUANTILES`,
  `TIDE_WARM_BARS`.  `tierc9`: `_trailing_pool`, `_trailing_edges`, `tide_streak_age`, `replay9`,
  `card_candidates9`, `frame`, `role_arrays`, `V6_ROLES`.  `tierc7_rules`: `struct_stop_4h`,
  `PROVISIONAL_MIN_N`.  `tierc5`: `cluster_boot_diff`, `cluster_boot`, `_ci_from`, `d15`.
  `tierc10_panel`: `ERA_CUT_MS`, `N_BOOT`, `run_cell_n`, `CONTROL_CARD`, `_book_sha`, `loao_n`.

MIRROR (copy the law into a TC12 module, cite the source line, hold equal by fixture; cannot be imported
because of H1):
- from `tierc11_stage_g.py`: `key_of, age_of, edges_of, old_refused, abs_refused, lag_of, win_refused,
  ratr_of, ratr_refused, era_of_entry, band_code, facts_of, facts_frame, refused_keys, apply_gate,
  replay_g (+ refuse_hook), blocker_of, rival_rows, haircut, regbook_frame, canonical_csv, book_sha256,
  write_regbook, collar, stats, era_slice_rows`; the F-EDGE comparators.
- from `tierc11_books.py`: `tide_pool, entry_streak, trailing_edges, band_of, lag_band`.
- from `tierc11_score.py`: `ci_of, ruled, loao, verdict_of_record, clears_bar, gate_findings, gate_block,
  two_sample_premise` — with the family (m, bar) as PARAMETERS.
- from `tc11x_books.py`: `abs_tide_cut()` (read-by-object pattern, extended to the 16), `prefix_band_findings`.
- from `tc11x_era.py` (for breadth and the per-bar series): `tide_law`, `_band`, `third_share`-style
  integer decisions, `_hq`, the RUN/CEN/EDG construction of `bar_cells` (:831-900), the member loop and
  alignment HALT of `_stamp_one` (:684-748), `Tape` / `Inputs`.

READ AS ORACLES (pinned by sha; never written):
- `stage_g/g_campaign_gates.parquet` — the 200 campaigns' facts (run, edges, band, lag, r_over_atr, flags).
- `regbooks/P-AGE-1/{scored,base,tierE__shadow_abs206}` and `regbooks/P-WIN-1/scored` — book_sha256 anchors.
- `stage_g/g_grid_books.parquet` + `g_grid_partition.parquet` — cell 110 and the 2×2×2 margins that the
  2×2×2×2 must collapse to.
- `scores/SCORES.json` — P-AGE-1 / P-WIN-1 `stats.main` for the scorer-mirror fixture.
- `registrations/REGISTRATIONS.json` — the texts supplying 206 and 16.
- `tierc10/close/P_AGE_1_BAR_BANDS.parquet` — 206.0 cross-check; `P_AGE_1_TIDE_YOUTH.parquet` — band n's.
- `X/…/era/X4_stamps.parquet` — breadth-17 (young, n_eff, share), own_band, edges per campaign;
  `X4_tables.parquet` — E-1 / E-2 / E-4 rows quoted in the P-BRD-1 label.
- `X/…/forward/BOOK_SPECS.json` — `pool_lo_ms`, the third book's gate spec (template for the fourth).

NEWLY WRITTEN:
- the P-ADM-1 regbook (scored = v6 minus (OLD ∪ stale); base; shadows OLD-alone, stale-alone, abs206
  [alone and OR-stale]; tuning / holdout; refused cohort; the stale-only increment cohort);
- the breadth module: per-asset per-bar tide table (asset, bar open, state, run, left_censored, panel
  q25/q50/q75, band) for the five and for the seventeen; breadth-5 per bar and per campaign; the P-BRD-1
  regbook; the {0..5} × own-band grid; breadth-17 / leave-own-out / face-value / n_eff twins;
- the 2×2×2×2 partition and gate-book tables; the slot-arbitration simulation with its competition count;
- the family record (m = 2, bar 0.05, seed 20261008) and the gate rows with the overlap and forfeit columns;
- fixtures: F-GATE (refused set == the text; un-gated book must FAIL), F-BRD (three bars recomputed
  independently, incl. one 2020 bar with < 5 warm home assets and one with a censored member), F-EDGE
  (q75, 206/207, 15/16, breadth 1/5 vs 2/5), TIDE-PREFIX, the cell-110 anchor, the scorer-mirror anchor,
  F-GRID 16 + 16.
