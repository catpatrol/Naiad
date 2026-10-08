# U2 · X's VALUE-AREA IMPLEMENTATION — the source of record for TC12 Stage V

Scout map, read-only. Contract read verbatim: `scratchpad/tc12/2026-10-08_TC12_APOLLO.md`
(sha256 `861d6050e80e66995e4f9db2855aaf274d63285249c2549e5a0813582095a7bd`, 137 lines; the same bytes are
already filed in main at `/Users/luis/Naiad/exchange/queue/2026-10-08_TC12_APOLLO.md`, commit `28e006b`).

Shorthand: **X** = `/Users/luis/Naiad/.claude/worktrees/tierc11x` (branch tierc11x, HEAD
`7b24f835bcbf7430eb0f97b6c39b6b1b233eef11`, verified before and after this scout; status shows only the
pre-existing untracked `research_outputs/tierc11x/close/CERTIFIED_TIP`). **M** = `/Users/luis/Naiad`
(branch v12-v1-census, HEAD `28e006bc`). X's tip is NOT an ancestor of main's HEAD (`git merge-base
--is-ancestor` false). `va.py` = `X/scripts/tc11x_va.py`. `census.py` = `X/scripts/tierc10_census.py`
(byte-identical in M, sha `0e6cb635…`). `rc.py` = `X/analytics/rangefinder_census.py` (identical in M,
`19c5507f…`).

Method caveat: every number below was read from disk this session. I ran one plain `git -C X status`
(an optional index stat refresh is possible; no tree, commit or tracked byte changed). Executors should
use `git --no-optional-locks`.

---------------------------------------------------------------------------------------------------------
## 1 · FACTS

### 1.1 Where the records live, and what is addressable by git

| record | path under X | bytes | sha256 (file) | tracked at 7b24f835? |
|---|---|---:|---|---|
| implementation | `scripts/tc11x_va.py` (2,524 lines) | 158,641 | `3f6a43cbbf7fd71cb374bd9e2b2fd16b1cd9bd52b24437a35fb76b9c171ca422` | yes |
| fixtures | `scripts/tc11x_va_fixtures.py` (2,108 lines) | 115,600 | `dd941ed23971a8ce590443378fbf7870cb631d86b0ea63028521f224299eee3c` | yes |
| range door (L reader) | `scripts/tc11x_ranges.py` | — | `26e829d8990b462fc6f22829a9974a5a291fee462dadf58e1160d749dd127d8d` | yes |
| the pins | `research_outputs/tierc11x/pins/PINS_X.json` | 83,955 | `85e1eeea2d04ffe834b93caf76aae55b1f427ae7935b12a7ecae9d814be7498f` | yes |
| report | `research_outputs/tierc11x/va/X3.md` | 40,822 | `eea131167b827f2763a1564655234ab97d7c3c92e7e02a1ec0f461a4ed5abf08` | yes |
| manifest | `…/va/build_manifest.json` | 182,922 | `769ac0915ee35b8783d99e0d39870f9e164871b81b94b6bb3533204fa28f078b` | yes |
| fixture transcript | `…/va/FIXTURES_X3.txt` (15 GREEN, 0 RED) | 26,702 | `474731ed4044a446fe16a30aaa23a886ca92cd2c757992d159ec173aa3b844b2` | yes |
| stage record | `…/progress/X3.json` (status COMPLETE-VERIFIED) | — | `92b6c49dbc63f737ee421bb0ea53636720f1fd8275d21a0c3d621e1cfd617555` | yes |
| readings | `…/LEANS_X.md` (X3 = lines 1580-1818) | 250,656 | `74a989ee6357e2169f2ad88722b67f1174cf0d080783dc8c77f5f064e3468623` | yes |
| amendments | `…/LEANS_X_AMENDMENTS.md` | 37,205 | `af845b95d1c7699f788aa242af6f5bef0d0f86b92a74a938cb7ca14c9d87d059` | yes |
| builder completions | `…/AMENDMENTS_PROPOSED.md` (AP-11 = lines 558-641) | 95,768 | `a3eb2f2fdb3fa9b786a0f5fe5dc96df86b752a880fc3d6178a3878c080abfc45` | yes |
| `va_series_1h.parquet` | `…/va/` | 36,748,745 | `860b895448dec9e3d53c10a3bf5233f3e94610a4cb983efe02d676ee64a1af7e` | **NO** |
| `va_series_4h.parquet` | `…/va/` | 10,771,152 | `d5881508a02475eb46c180b757e1948466313cb1673d2a909ea9ab5bda25891c` | **NO** |
| `va_series_12h.parquet` | `…/va/` | 3,747,949 | `c2ce9a8f131fac79de5a3890d67aa626fbf1f9d6bf0a27cb4e4fce0014c40359` | **NO** |
| `va_series_1d.parquet` | `…/va/` | 2,025,996 | `1fc7bc75033c4d57a39e3bdae0de4d8bb590e7752894bb0ad329398e106ae1a7` | **NO** |
| `events_va.parquet` | `…/va/` | 20,751,566 | `2c35b15162a1dfa96fa09074688650dd313fd9245836ccb301cfa2eb3aa35848` | **NO** |
| `events_pivot.parquet` | `…/va/` | 1,940,512 | `eb99f3f3760c1883ece3e9dcb3ee1b033a25a4a04993118044d67d98c78a9097` | **NO** |
| `feasibility.parquet` | `…/va/` | 98,554 | `ea8573b3240bb1112521c55f0a52ee2ed7156c598b7665685d0b86eefbecb6f0` | **NO** |
| `two_trades.parquet` | `…/va/` | 1,147,787 | `a03ef1343cc93c9bc093c4f34960978daac51ca24d5160480546d40bf76f91b0` | **NO** |
| `agreement.parquet` | `…/va/` | 75,132 | `7984fb78f9393df19eaeaaee0291edf54a4cf6e3e6859c1e0725b753d8b2e41a` | **NO** |

- The nine parquets are gitignored (`X/research_outputs/tierc11x/.gitignore`: `*.parquet`, `_det_*/`). They
  exist ONLY on this machine's worktree disk. Their file shas above equal the tracked
  `progress/X3.json` → `artifact_shas[<path>].sha256` (all nine re-hashed here, 0 mismatches).
- Content shas (the writer's row-content hash) are in the tracked manifest, `va/build_manifest.json` →
  `sha`: feasibility `c97fc1e8…5e58`, events_va `69e80c25…27f6`, two_trades `5bcd88ee…4d1a`, va_series_4h
  `f54318a4…ef5f`, va_series_1h `65cb12a0…9bcf`, va_series_12h `dc7b176f…0db8`, va_series_1d `6a95c254…05c8`,
  agreement `d8d715ca…bf2d`, events_pivot `51802d92…b6bd`.
- `git show 7b24f835:<path>` returns bytes hashing to the working-tree shas for tc11x_va.py, PINS_X.json,
  X3.md, build_manifest.json, progress/X3.json (checked). The parquets cannot be reached this way.
- None of this exists in main: `M/scripts/tc11x_*` no match; `M/research_outputs/tierc11x` absent;
  `M/analytics/value_area.py` absent.

### 1.2 The lookback pin per lens

| lens | L of record (bars) | PINS_X.json line | pooled mean it rounds | n_dead | whole-tape twin | frozen-3.0 twin |
|---|---:|---:|---:|---:|---:|---:|
| 1h | **71** | 451 | 70.72245467224546 (l.538) | 1434 (l.541) | 66 | 111 |
| 4h | **66** | 674 | 65.89766081871345 (l.761) | 342 (l.764) | 63 | 73 |
| 12h | **53** | 5 | 53.330275229357795 (l.92) | 109 (l.95) | 59 | 101 |
| 1d | **35** | 228 | 35.232142857142854 (l.315) | 56 (l.318) | 42 | 67 |

- Key path: `PINS_X.json` → `L.by_lens.<lens>.L_of_record`. Read in code by `tc11x_ranges.lookback(lens,
  twin="record")` (tc11x_ranges.py:1355-1362), called at va.py:1290 (`L = R.lookback(lens)`). Never typed.
- The same four numbers are restated at: `va/X3.md:31-34` (and the lean line X3.md:9);
  `va/build_manifest.json` → `pins.L.<lens>.record`; the column `L` of every `va_series_<lens>.parquet`
  (constant per file: 71 / 66 / 53 / 35, read here); `FIXTURES_X3.txt:7`. All agree. Memory's 71/66/53/35
  is confirmed.
- **What it was coupled to.** `PINS_X.json:897` (`L.law`): "one L per lens — the CLASSIC5 pooled,
  dead-weighted mean of DIED confirmed-range lives (die_i − confirm_i) on the tuning-era head at each
  asset's pick of record, L = floor(x + 0.5)". I.e. L is the PIVOT machine's mean confirmed-range life, run
  at TC11's calibrated scale picks (per asset × lens: `pins.picks` in the manifest; e.g. 4h 2/2/2/1.75/2 for
  BTC/ETH/SOL/NEAR/ZEC, X3.md:32), on bars whose close ≤ 2024-06-30T23:59:59Z (`era_cut_ms` 1719791999000,
  PINS_X.json:1473). Integer law: `l_pin` (tc11x_ranges.py:835-846). Reading: LEANS_X.md:1582-1606.
- Label carried on every VA row: "a tuning-window L is in-sample for tuning-era VA bars (the L-R.2
  label)" (va.py:200; column `l_label`).
- **There is no 1w L.** `L_LENSES = ("1h","4h","12h","1d")` (tc11x_ranges.py:356); `X_LENSES` has no 1w
  (:352); PINS_X `L.by_lens` has exactly four keys.

### 1.3 The profile recipe (bit-exact to the house function)

Oracle: `analytics.profile.volume_profile(high, low, volume, bins=100, value_area=0.70)` —
`M/analytics/profile.py:113-172`, sha256 `1c0a7519ddd4c37963163e1dc302788d142c74f741a82d8022742595a8eb3e18`,
**byte-identical in M and X**. X imports it behind three pins (va.py:118-152): that file sha,
`analytics.analytics_sha()` = `ea5f02f21ca43b6b71e450b540ff09c807b305971e3eb8cff50bea84c985dc91`,
`ANALYTICS_VERSION` = `"1.5.0"` (M/analytics/__init__.py:74).

- **Window.** VA(t) = profile over bars `t−L+1 .. t` of the lens's OWN tape (va.py:423-436; rows =
  `T − L + 1 + arange(L)`). First valid VA at bar index L−1 (va.py:442; checked on the 4h file: first
  `va_valid` at i = 65 for all five assets). A bar-COUNT window: gaps are counted, never filled
  (census.py:580-582), so L bars can span more than L·step of clock.
- **Bins.** 120 rows = `P.PROFILE_ROWS` (profile.py:21; va.py:168), **range-relative**: edges =
  `linspace(min low, max high, 121)` of the window (profile.py:126,132; va.py:355-362). Not tick-based, not
  ATR-based (ATR-scaled rows were rejected: LEANS_X.md:1640). Measured from the filed series: median bin
  width 0.0727 ATR (1h), 0.0702 (4h), 0.0628 (12h), 0.0508 (1d); median VA width (VAH−VAL)/ATR 4.081 / 3.894
  / 3.491 / 2.776.
- **Volume spread.** Each bar's volume is spread UNIFORMLY over its [low, high]: per bin, overlap of the
  bin with the bar's range ÷ the sum of overlaps (profile.py:141-148; va.py:384-391). A doji (high == low)
  puts all volume in bin `min(int((a − lo)/(hi − lo)·bins), bins − 1)` (profile.py:142-144). Bars with a
  non-finite field or volume ≤ 0 are skipped (profile.py:137-140). Declared approximation
  (`APPROXIMATION`, profile.py:17).
- **POC.** `argmax(hist)` — the FIRST maximum, i.e. a tie goes to the LOWEST price bin (profile.py:154;
  va.py:394).
- **70% band.** `VALUE_AREA` = 0.70 (profile.py:22). Start at the POC bin; while accumulated < 70% of total
  and a side remains: compare the next bin up with the next bin down (−1.0 sentinel at a boundary); **`up
  >= down` → extend UP, so a tie goes UP**; else extend down (profile.py:155-166; va.py:396-411). One bin
  per step, contiguous by construction.
- **Levels are bin CENTERS** (profile.py:168-170; va.py:412-414): VAH = center of the top included bin, VAL
  = center of the bottom one. The outer bin EDGES are filed as a twin (`val_edge`, `vah_edge`; half a bin
  wider each side; va.py:415-416).
- **Degenerate windows.** `hi <= lo` → POC = lo, no VA (NaN); zero total volume → all NaN (profile.py:127-
  130, 150-152; va.py:413-414).
- **Time-at-price twin (TPO).** Each bar adds +1 to every row its [low, high] touches (row index by
  searchsorted-right − 1, clipped); same rows, same expansion, same centers (va.py:326-340, 370-377).
  Filed as `tpo_poc / tpo_val / tpo_vah`.
- **Vectorisation.** `va_core` reproduces `np.linspace`'s arithmetic (`arange·step + lo`, last edge = hi)
  and accumulates bar by bar in window order (va.py:343-420). F-VA-EQ: 0 differing rows on the whole
  BTCUSDT 1h tape (61,689 windows) and 4,000 sampled windows over the 20 cells (FIXTURES_X3.txt, F-VA-EQ
  PASS line). Interpreter read here: Python 3.12.14, numpy 2.1.3, pandas 2.2.3, pyarrow 18.1.0.
- **Volume source per lens** (va.py:294-322): 1h / 4h / 12h = the native snapshot file
  `klines/{sym}_{lens}.parquet`; 1d = Stage D's derived `klines/{sym}_1d.parquet` (4h volume summed per
  complete UTC day). Columns `open_time:int64, open, high, low, close, volume:float64`. Before any VA:
  `open_time == tape.t0` row for row and high/low equal the tape's, else HALT (va.py:311-315). A lens's
  profile never reads another interval's bars (the finer-substrate build is a twin, `hs_*`).
  Snapshot: `~/.cache/naiad/snapshots/tc11_20260925/klines/` (pin 1790294400000 = 2026-09-25T00:00:00Z).
  A `{sym}_1w.parquet` file exists there for the five home assets (BTCUSDT_1w: 367 rows, with volume) but
  X never opened it.

### 1.4 ATR_L

- `tape.atr = engine.indicators.atr(h, l, c, 14)` on the WHOLE tape (census.py:626; asserted at
  tc11x_ranges.py:600; length `RC.ATR_LEN` = 14, rc.py:132).
- `atr = rma(true_range, 14)`; `rma`: alpha = 1/14, recursive, **seeded with the first value** (no SMA
  seed); `true_range[0] = high[0] − low[0]` (`M/engine/indicators.py:31-54`, sha `91805c04…`, identical in X).
- Prefix-invariant (`Tape.head`, census.py:552-557: "atr[:t] IS the prefix's own ATR; a tail would not be").
- The ATR used at a bar t is `atr[t]` (it includes bar t's own true range).
- `analytics.volatility.atr` is NOT this ATR: rc.py's header states the package's own ATR is SMA-seeded
  with a NaN warm-up and that using it "would move every event sha"; the port therefore takes ATR as an
  argument.

### 1.5 The causal convention

- Series: VA(t) uses bars ≤ t and is "known at close[t]" (va.py:28-29, 424-425). The filed row at index `i`
  carries VA(i) in `poc / val / vah`.
- Judging: **close[t] is compared with VA(t−1)**, never the self-inclusive VA(t) (`ref_arrays(…, "prev")`,
  va.py:535-541; LEANS_X.md:1655-1668). The filed flag `close_in_va_prev` is exactly
  `val[i−1] <= close[i] <= vah[i−1]` (re-derived here on 4h: 0 mismatches on four assets, 1 on ZECUSDT at
  i = 8337, a 6-dp rounding artefact — see hazard H7).
- The frozen edge of an episode is `E = VAH(t0−1)` / `VAL(t0−1)` (va.py:630-632); the regime height is
  `VAH(r0−1) − VAL(r0−1)` (va.py:968-977). Both are the same rule: the VA that JUDGED the bar, which is the
  VA of the previous bar.
- X's own "what would make this wrong" list (va.py:70-71): "a close judged against the self-inclusive VA(t)
  (a breakout bar drags VAH to its own close)".

### 1.6 The episode machine (X's event semantics)

`va_episodes(c, h, l, atr, VAL, VAH, law: EpLaw = EpLaw()) -> {"episodes", "regimes", "counters"}`
(va.py:544-646). `EpLaw` (va.py:520-527) fields and record values: `ref="prev"`, `frozen=True`,
`ret_k=DEV_RETURN` (7), `die_parity=False`, `rearm=True`. Twins in `EP_LAWS` (va.py:530-532): `die_parity`,
`no_rearm`, `moving_edge`, `self_inclusive`, `k1`, `k3`. **No filed law combines `die_parity` with `ret_k=3`.**

Constants, all read by object:

| constant | value | source |
|---|---:|---|
| `DEV_RETURN_BARS` (SFP return window) | 7 | rc.py:140; va.py:171 |
| `BREAK_CONFIRM_N` (closes to accept) | 8 | rc.py:141; va.py:172 |
| `BREAK_MARGIN` (DIE-parity twin) | 1.5 | rc.py:144; va.py:173 |
| `FLIP_HOLD_MARGIN` | 1.0 | rc.py:157; va.py:174 |
| `FLIP_HOLD_BARS` | 6 | rc.py:158; va.py:175 |
| `MEM_TTL_BARS` | 400 | rc.py:159; va.py:176 |
| `SFP_K_TWINS` | (1, 3) | va.py:187 (the reading's own literals) |
| `COINCIDENCE_ATR` | 0.25 | va.py:189 (typed literal, VA edge vs PIVOT box) |
| horizons | H20 = 20, H100 = 100 bars of the lens | census.py:123 |

One pass in bar order; a bar that resolves an episode does nothing else.

- **Idle bar** (no episode pending; requires a valid VA(t−1)):
  - the first valid bar starts the first value regime (index L);
  - `VAL(t−1) <= c[t] <= VAH(t−1)` (closed interval): if any side is disarmed, **re-arm BOTH sides**
    (`rearm_closes`) and start a new regime if none is alive;
  - close beyond a side that is **disarmed**: nothing happens, counted `blocked_disarmed`;
  - close beyond an **armed** side: a breach opens, `t0 = t`, `E` = that edge of VA(t0−1), `closes = 1`,
    `extreme = h[t]` (top) / `l[t]` (bottom).
- **Pending bar**: `extreme` is updated with this bar's high/low FIRST; then `beyond = c[t] > E` (top) /
  `c[t] < E` (bottom), strict.
  - beyond: `closes += 1`; **accept when `closes >= 8`** (by = `n_closes`, at `t0 + 7`); DIE-parity twin
    only: also accept when `abs(c[t] − E) >= 1.5·atr[t]` (by = `margin`), on the open bar too.
  - not beyond (a close AT or inside E): **SFP iff `t − t0 <= ret_k`**, else **lapse**.
- **Acceptance** disarms ITS side only and ends the alive regime (`die_i = t`).
- An SFP or a lapse changes no armed flag.
- Signs: SFP top → −1 (short), bottom → +1 (long); acceptance top → +1, bottom → −1 (va.py:643-645).
- `drift_back` (a filed column) flags an SFP whose close is beyond E; it is 0 on every frozen-edge law and
  non-zero only on the moving-edge twin (794 at 4h, X3.md:63).

Record counts, CLASSIC5 summed (X3.md:42,55,69,83; manifest `event_counts`):

| lens | breaches | SFP | accept | lapse | open at end | re-arm closes | blocked (disarmed) | regimes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1h | 14441 | 8956 | 5485 | 0 | 0 | 5481 | 64066 | 5486 |
| 4h | 3692 | 2216 | 1474 | 0 | 2 | 1473 | 16657 | 1478 |
| 12h | 1329 | 785 | 544 | 0 | 0 | 538 | 5116 | 543 |
| 1d | 763 | 417 | 343 | 0 | 3 | 340 | 2165 | 345 |

Over the 20 cells: 20,225 breaches, 12,374 SFP, 7,846 acceptances, `accept_by_margin` 0,
`rearm_blocked_by_pending` 15, `margin_equality_touches` 0. At the record pins a lapse is unreachable
(8 ≤ 7 + 1; rc.py:142-143; F-VA-INV).

Twins that matter for TC12 (events_va row counts by `variant`, read here):

| lens | variant | sfp rows | accept rows | note |
|---|---|---:|---:|---|
| 4h | record | 2216 | 1474 | 8 closes only; return ≤ 7 |
| 4h | die_parity | 2139 | 1605 | 1217 accepts by margin, 388 by 8 closes |
| 4h | k3 | 1734 | 1474 | lapses 482 (X3.md:68) |
| 4h | k1 | 1042 | 1474 | lapses 1174 |
| 4h | moving_edge | 2771 | 1198 | |
| 4h | self_inclusive | 2140 | 1426 | |
| 1h | die_parity | 8622 | 6062 | |
| 1h | k3 | 6947 | 5485 | lapses 2009 |
| 1d | die_parity | 414 | 372 | |
| 1d | k3 | 326 | 343 | lapses 91 |

Two identities checked on the parquet: (i) the 4h `k3` SFP rows equal the 4h `record` SFP rows with
`bars_out <= 3`, row for row on (asset, side, t0, end_i, E) — `ret_k` only relabels sfp ↔ lapse, the path
is unchanged; (ii) record 4h SFP `bars_out` distribution: 1 → 1042, 2 → 434, 3 → 258, 4 → 159, 5 → 141,
6 → 107, 7 → 75.

### 1.7 The breakout-retest (VA side of record)

After an acceptance (anchor), with level = the frozen E: a qualifying touch at bar j is `low[j] <= E` with
`close[j−1] > E` (mirrored for a bottom) (va.py:689-701); scanned over `(anchor, min(anchor + 400, next
acceptance of EITHER side − 1, n − 1)]` (va.py:704-728); verdict at a touch: `truncated` if `j + 6 >= n`;
`failed` iff any close in `j..j+6` is through the level by MORE than `1.0·atr[k]` (strict `<`), or the
level is unreadable; else `hold` (va.py:674-686). **The first HOLD is the event, known at `touch + 6`**; a
truncated verdict ends the scan; every evaluated touch is a row (`cls` `retest-touch` / `retest-hold`).
Trade sign: top → +1 (long), bottom → −1. 4h record: 695 holds, 748 failed, 1 truncated (X3.md:55).

### 1.8 Regimes and the feasibility leg

- Value regime = the re-arm close (or the first valid bar) to the next acceptance; geometry runs
  `r0 .. die − 1` (va.py:968-977; AP-11 items 4-5).
- Adapter `walk` (va.py:928-965) feeds the census's gate functions UNFORKED: `C.height_rows`
  (census.py:2636-2656), `C.height_grid` (:2659-2704), `C.edge_arrays` (:2710-2735), `C.edge_gate`
  (:2863-2896), `C.verdict_rows` (:2899-3001).
- **Height leg**: `ratio = height_px / ((bps/10000)·close[r0])` with `height_px = VAH(r0−1) − VAL(r0−1)`;
  PASS iff `n_ranges >= 30` AND `median(ratio) >= 3.0` AND `share(ratio < 1) <= 0.10` (census.py:2153-2156,
  2165, 2690-2692).
- **Edge-fade leg ("edges respected")**: entries = every regime bar whose close is inside VA(t−1), exact
  mid dropped; restricted to the NEAR 20% on each side (`EDGE_NEAR_FRAC` 0.2, census.py:2168; deciles 0-1
  and 8-9, :2747-2750); direction toward the far edge (`pct < 0.5` → long, :2722); outcome `term =
  sgn·(c[t+20] − c[t])/atr[t]`, censored never shortened (:2490-2501); `net = round(median term, 8) −
  round(toll_atr, 8)` with `toll_atr = (bps/10000)·c[t]/atr[t]`, pooled toll = the BINDING max of the
  per-asset medians (:2765-2773); PASS iff `edge_n >= 30` AND `edge_n_ranges >= 30` AND `net > 0`
  (:2884-2886).
- `verdict_pass = gate_height_pass AND gate_edge_fade_pass`, judged within ONE era (:2974).
- Words (`_word`, va.py:1750-1756): `PASS`; `FAIL`; `FAIL (provisional, n<30)`.
- **The row of record per lens** (va.py:1727-1728, 1743-1746): `scale_kind == "va_regime"` AND `asset ==
  "POOLED:CLASSIC5"` AND `era == "holdout"` AND `toll == "taker"` → `of_record_for_detector = True` on
  exactly 4 of the 432 rows. The maker row is NOT flagged of record; it is "the maker twin beside".
- The 1h `lens_word` is the long string "FAIL — maker twin PASSES (the reopening path; needs a toll-model
  change the operator rules)"; the short two-word value is in `would_read`.

**Tolls** (va.py:1232-1240; `fee_schedule.json` sha `6febe170d423b0ef37dca9fe95a7316e4259ef5a77e576cafa6781d581c1968b`,
identical at `M/research_outputs/tierc11/data/` and X's `data/tc11_rec/data/` copy):

- taker `toll_bps` = **10.0 = ROUND TRIP** (`round_trip_bps_used`; 5.0 bps per side, `taker_bps_side_used`);
- maker `toll_bps` = **4.0 = ROUND TRIP** (`maker_round_trip_bps`; 2.0 bps per side, `maker_bps_per_side`,
  top-level key at fee_schedule.json:767 and on every asset row), zero slippage, BOTH legs maker;
- `maker_kind`: "ASSUMPTION — Binance USDT-M VIP0 maker per README; the engine books every fill as taker;
  this is a TWIN, never the toll of record [L-1.2]". MNT (Bybit) carries the same figure as an assumption.
- In the parquet: `toll_bps` is 10.0 on every taker row and 4.0 on every maker row, all six panels.

**THE FULL POOLED:CLASSIC5 GRID** — `va/feasibility.parquet`, `asset == "POOLED:CLASSIC5"`, 72 rows
(4 lenses × 2 tolls × 3 eras × 3 scale_kinds). gH = height gate, gE = edge-fade gate; `va_perbar` rows
carry a distribution only and no verdict. `*` marks `of_record_for_detector`.

| lens | toll | era | scale_kind | bps | n_ranges | ratio_median | edge_n | edge_n_ranges | edge_median_h20 | edge_toll_atr | edge_net_h20 | gH | gE | word (`would_read`) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|:-:|:-:|---|
| 1h | maker | ALL | va_lblock | 4 | 4007 | 126.2602 | 56217 | 3993 | 0.099729 | 0.054200 | +0.045529 | T | T | PASS |
| 1h | maker | ALL | va_perbar | 4 | – | 126.0739 | – | – | – | – | – | – | – | no verdict |
| 1h | maker | ALL | va_regime | 4 | 5486 | 161.5441 | 55634 | 5404 | 0.098539 | 0.054234 | +0.044305 | T | T | PASS |
| 1h | maker | tuning | va_lblock | 4 | 2628 | 132.4995 | 36445 | 2621 | 0.098534 | 0.049429 | +0.049105 | T | T | PASS |
| 1h | maker | tuning | va_perbar | 4 | – | 132.2184 | – | – | – | – | – | – | – | no verdict |
| 1h | maker | tuning | va_regime | 4 | 3554 | 170.2478 | 36073 | 3505 | 0.097969 | 0.049489 | +0.048479 | T | T | PASS |
| 1h | maker | holdout | va_lblock | 4 | 1379 | 117.6044 | 19772 | 1375 | 0.104438 | 0.064551 | +0.039886 | T | T | PASS |
| 1h | maker | holdout | va_perbar | 4 | – | 116.5936 | – | – | – | – | – | – | – | no verdict |
| 1h | maker | holdout | va_regime | 4 | 1932 | 147.9765 | 19561 | 1901 | 0.102664 | 0.064663 | +0.038001 | T | T | **PASS** |
| 1h | taker | ALL | va_lblock | 10 | 4007 | 50.5041 | 56217 | 3993 | 0.099729 | 0.135500 | −0.035771 | T | F | FAIL |
| 1h | taker | ALL | va_perbar | 10 | – | 50.4295 | – | – | – | – | – | – | – | no verdict |
| 1h | taker | ALL | va_regime | 10 | 5486 | 64.6177 | 55634 | 5404 | 0.098539 | 0.135586 | −0.037047 | T | F | FAIL |
| 1h | taker | tuning | va_lblock | 10 | 2628 | 52.9998 | 36445 | 2621 | 0.098534 | 0.123572 | −0.025039 | T | F | FAIL |
| 1h | taker | tuning | va_perbar | 10 | – | 52.8873 | – | – | – | – | – | – | – | no verdict |
| 1h | taker | tuning | va_regime | 10 | 3554 | 68.0991 | 36073 | 3505 | 0.097969 | 0.123723 | −0.025755 | T | F | FAIL |
| 1h | taker | holdout | va_lblock | 10 | 1379 | 47.0417 | 19772 | 1375 | 0.104438 | 0.161378 | −0.056941 | T | F | FAIL |
| 1h | taker | holdout | va_perbar | 10 | – | 46.6374 | – | – | – | – | – | – | – | no verdict |
| 1h | taker | holdout | va_regime `*` | 10 | 1932 | 59.1906 | 19561 | 1901 | 0.102664 | 0.161658 | −0.058994 | T | F | **FAIL** |
| 4h | maker | ALL | va_lblock | 4 | 1076 | 260.5087 | 13805 | 1071 | 0.159412 | 0.026338 | +0.133074 | T | T | PASS |
| 4h | maker | ALL | va_perbar | 4 | – | 257.0921 | – | – | – | – | – | – | – | no verdict |
| 4h | maker | ALL | va_regime | 4 | 1478 | 338.2818 | 13660 | 1450 | 0.162145 | 0.026484 | +0.135661 | T | T | PASS |
| 4h | maker | tuning | va_lblock | 4 | 705 | 270.7778 | 9048 | 703 | 0.157267 | 0.023501 | +0.133766 | T | T | PASS |
| 4h | maker | tuning | va_perbar | 4 | – | 270.9644 | – | – | – | – | – | – | – | no verdict |
| 4h | maker | tuning | va_regime | 4 | 969 | 356.0952 | 8945 | 951 | 0.159725 | 0.023628 | +0.136097 | T | T | PASS |
| 4h | maker | holdout | va_lblock | 4 | 371 | 240.7630 | 4757 | 372 | 0.170637 | 0.030884 | +0.139753 | T | T | PASS |
| 4h | maker | holdout | va_perbar | 4 | – | 231.9831 | – | – | – | – | – | – | – | no verdict |
| 4h | maker | holdout | va_regime | 4 | 509 | 305.2091 | 4715 | 502 | 0.170637 | 0.030909 | +0.139728 | T | T | PASS |
| 4h | taker | ALL | va_lblock | 10 | 1076 | 104.2035 | 13805 | 1071 | 0.159412 | 0.065845 | +0.093567 | T | T | PASS |
| 4h | taker | ALL | va_perbar | 10 | – | 102.8368 | – | – | – | – | – | – | – | no verdict |
| 4h | taker | ALL | va_regime | 10 | 1478 | 135.3127 | 13660 | 1450 | 0.162145 | 0.066210 | +0.095935 | T | T | PASS |
| 4h | taker | tuning | va_lblock | 10 | 705 | 108.3111 | 9048 | 703 | 0.157267 | 0.058753 | +0.098514 | T | T | PASS |
| 4h | taker | tuning | va_perbar | 10 | – | 108.3857 | – | – | – | – | – | – | – | no verdict |
| 4h | taker | tuning | va_regime | 10 | 969 | 142.4381 | 8945 | 951 | 0.159725 | 0.059070 | +0.100655 | T | T | PASS |
| 4h | taker | holdout | va_lblock | 10 | 371 | 96.3052 | 4757 | 372 | 0.170637 | 0.077209 | +0.093427 | T | T | PASS |
| 4h | taker | holdout | va_perbar | 10 | – | 92.7933 | – | – | – | – | – | – | – | no verdict |
| 4h | taker | holdout | va_regime `*` | 10 | 509 | 122.0836 | 4715 | 502 | 0.170637 | 0.077272 | +0.093365 | T | T | **PASS** |
| 12h | maker | ALL | va_lblock | 4 | 446 | 418.7195 | 4735 | 443 | −0.064370 | 0.014097 | −0.078467 | T | F | FAIL |
| 12h | maker | ALL | va_perbar | 4 | – | 415.3586 | – | – | – | – | – | – | – | no verdict |
| 12h | maker | ALL | va_regime | 4 | 543 | 583.4135 | 4672 | 529 | −0.063939 | 0.014088 | −0.078027 | T | F | FAIL |
| 12h | maker | tuning | va_lblock | 4 | 292 | 444.2063 | 3106 | 290 | −0.116868 | 0.013072 | −0.129940 | T | F | FAIL |
| 12h | maker | tuning | va_perbar | 4 | – | 437.3615 | – | – | – | – | – | – | – | no verdict |
| 12h | maker | tuning | va_regime | 4 | 355 | 605.7697 | 3060 | 345 | −0.108702 | 0.013072 | −0.121775 | T | F | FAIL |
| 12h | maker | holdout | va_lblock | 4 | 154 | 380.0443 | 1629 | 156 | 0.021621 | 0.017502 | +0.004120 | T | T | PASS |
| 12h | maker | holdout | va_perbar | 4 | – | 375.9224 | – | – | – | – | – | – | – | no verdict |
| 12h | maker | holdout | va_regime | 4 | 188 | 548.0833 | 1612 | 186 | 0.014145 | 0.017447 | −0.003302 | T | F | **FAIL** |
| 12h | taker | ALL | va_lblock | 10 | 446 | 167.4878 | 4735 | 443 | −0.064370 | 0.035241 | −0.099612 | T | F | FAIL |
| 12h | taker | ALL | va_perbar | 10 | – | 166.1435 | – | – | – | – | – | – | – | no verdict |
| 12h | taker | ALL | va_regime | 10 | 543 | 233.3654 | 4672 | 529 | −0.063939 | 0.035220 | −0.099159 | T | F | FAIL |
| 12h | taker | tuning | va_lblock | 10 | 292 | 177.6825 | 3106 | 290 | −0.116868 | 0.032681 | −0.149548 | T | F | FAIL |
| 12h | taker | tuning | va_perbar | 10 | – | 174.9446 | – | – | – | – | – | – | – | no verdict |
| 12h | taker | tuning | va_regime | 10 | 355 | 242.3079 | 3060 | 345 | −0.108702 | 0.032681 | −0.141383 | T | F | FAIL |
| 12h | taker | holdout | va_lblock | 10 | 154 | 152.0177 | 1629 | 156 | 0.021621 | 0.043754 | −0.022132 | T | F | FAIL |
| 12h | taker | holdout | va_perbar | 10 | – | 150.3690 | – | – | – | – | – | – | – | no verdict |
| 12h | taker | holdout | va_regime `*` | 10 | 188 | 219.2333 | 1612 | 186 | 0.014145 | 0.043617 | −0.029472 | T | F | **FAIL** |
| 1d | maker | ALL | va_lblock | 4 | 336 | 498.1795 | 2212 | 325 | −0.188736 | 0.009426 | −0.198162 | T | F | FAIL |
| 1d | maker | ALL | va_perbar | 4 | – | 481.4622 | – | – | – | – | – | – | – | no verdict |
| 1d | maker | ALL | va_regime | 4 | 345 | 700.9188 | 2186 | 331 | −0.188736 | 0.009436 | −0.198172 | T | F | FAIL |
| 1d | maker | tuning | va_lblock | 4 | 219 | 549.1415 | 1426 | 212 | −0.322767 | 0.008597 | −0.331364 | T | F | FAIL |
| 1d | maker | tuning | va_perbar | 4 | – | 503.4281 | – | – | – | – | – | – | – | no verdict |
| 1d | maker | tuning | va_regime | 4 | 223 | 742.3217 | 1411 | 217 | −0.326271 | 0.008640 | −0.334911 | T | F | FAIL |
| 1d | maker | holdout | va_lblock | 4 | 117 | 443.7202 | 786 | 115 | 0.070057 | 0.010880 | +0.059177 | T | T | PASS |
| 1d | maker | holdout | va_perbar | 4 | – | 441.1357 | – | – | – | – | – | – | – | no verdict |
| 1d | maker | holdout | va_regime | 4 | 122 | 644.2071 | 775 | 116 | 0.070209 | 0.010903 | +0.059306 | T | T | PASS |
| 1d | taker | ALL | va_lblock | 10 | 336 | 199.2718 | 2212 | 325 | −0.188736 | 0.023565 | −0.212301 | T | F | FAIL |
| 1d | taker | ALL | va_perbar | 10 | – | 192.5849 | – | – | – | – | – | – | – | no verdict |
| 1d | taker | ALL | va_regime | 10 | 345 | 280.3675 | 2186 | 331 | −0.188736 | 0.023589 | −0.212326 | T | F | FAIL |
| 1d | taker | tuning | va_lblock | 10 | 219 | 219.6566 | 1426 | 212 | −0.322767 | 0.021493 | −0.344260 | T | F | FAIL |
| 1d | taker | tuning | va_perbar | 10 | – | 201.3712 | – | – | – | – | – | – | – | no verdict |
| 1d | taker | tuning | va_regime | 10 | 223 | 296.9287 | 1411 | 217 | −0.326271 | 0.021600 | −0.347871 | T | F | FAIL |
| 1d | taker | holdout | va_lblock | 10 | 117 | 177.4881 | 786 | 115 | 0.070057 | 0.027200 | +0.042857 | T | T | PASS |
| 1d | taker | holdout | va_perbar | 10 | – | 176.4543 | – | – | – | – | – | – | – | no verdict |
| 1d | taker | holdout | va_regime `*` | 10 | 122 | 257.6828 | 775 | 116 | 0.070209 | 0.027257 | +0.042952 | T | T | **PASS** |

`share_ratio_lt_1` is 0.0000 and `provisional` False on every verdict row above.

**The five mirror words and the exact row that yields each** (filter common to all five:
`asset == "POOLED:CLASSIC5"` · `era == "holdout"` · `scale_kind == "va_regime"`; word = column
`would_read`):

| contract word | extra filter | `would_read` | `of_record_for_detector` | `edge_net_h20` | also in tracked manifest |
|---|---|---|---|---:|---|
| 4h taker PASS | lens 4h, toll taker | PASS | True | +0.093365 | `va_lens_verdicts.4h.word` = "PASS" |
| 1d taker PASS | lens 1d, toll taker | PASS | True | +0.042952 | `va_lens_verdicts.1d.word` = "PASS" |
| 1h maker PASS | lens 1h, toll maker | PASS | **False** | +0.038001 | `va_lens_verdicts.1h.maker_twin` = "PASS" |
| 12h FAIL | lens 12h, toll taker | FAIL | True | −0.029472 | `va_lens_verdicts.12h.word` = "FAIL" |
| 1h taker FAIL | lens 1h, toll taker | FAIL | True | −0.058994 | `va_lens_verdicts.1h.word` starts "FAIL — maker twin PASSES …" |

What the other rows the unit asked about read:
- **12h MAKER, holdout, va_regime: FAIL** (net −0.003302; `va_lens_verdicts.12h.maker_twin` = "FAIL"). Its
  L-block twin PASSES (+0.004120). 12h maker ALL and tuning: FAIL.
- **1d MAKER, holdout, va_regime: PASS** (+0.059306). 1d maker ALL and tuning: FAIL.
- **1d taker is a HOLDOUT-ONLY pass**: ALL −0.212326 FAIL, tuning −0.347871 FAIL.
- 4h PASSES in all three eras at both tolls. 1h maker PASSES in all three eras; 1h taker FAILS in all three.
- Per-asset rows (`panel` = `ASSET:<sym>`, 360 rows) exist for every (lens, scale_kind, era, toll).
- X3.md prints the same four lens rows at lines 106, 108, 110, 112; the close draft restates them at
  BUILD_DRAFT.md:355-361.

Derived from the filed columns (toll_atr is linear in bps): the break-even round-trip toll of the holdout
edge leg is `edge_median_term_h20 ÷ (taker edge_toll_atr ÷ 10)` = 1h **6.35 bps**, 4h 22.08 bps, 12h
3.24 bps, 1d 25.76 bps (manifest `va_lens_verdicts` medians 0.1026641 / 0.1706368 / 0.0141450 / 0.0702091;
tolls 0.1616583 / 0.0772716 / 0.0436175 / 0.0272573).

### 1.9 two_trades.parquet

11,520 rows, key `cell` = `lens|detector|trade|variant|direction|era|panel|horizon`; all rows `toll ==
"taker"`, `toll_bps == 10.0`, `promotable == False`.

- Trades: `swing_failure` (entry at the SFP's back-inside close, sign toward value) and
  `breakout_retest` (entry at `touch + 6`, sign with the acceptance); detectors `va`, `pivot`, and the base
  rate `base | every_bar`.
- Outcome road: `term = sgn·(c[k+H] − c[k]) / atr[k]` from the known_at close, H20 / H100 in bars of the
  lens, censored never shortened; MFE / MAE beside (census.py:1352-1394). Statistics: `stats_rows`
  (va.py:867-924): `net = round(median_term, 8) − round(toll_atr, 8)`; pooled toll = binding max.
- VA variants filed (swing_failure): record, wick, k1, k3, moving_edge, self_inclusive, die_parity,
  no_rearm, tpo, bins100, edges, L_whole_tape, L_frozen3.0, L_per_asset, house_substrate. (breakout_retest):
  record, die_parity, no_rearm, moving_edge, self_inclusive, band_law, one_shot, live_edge, tpo, bins100,
  edges, the three L twins, house_substrate (va.py:219-223).
- FLIP_HOLD pins: margin 1.0, hold 6, TTL 400 (§1.6). The band-law twin uses `C.RETEST_PINS` (margin 1.0,
  hold 3, ttl 400, grid sha `2135ca66…`).
- **The null**: VA null of record = `tr_tercile_lblock` — a true-range-tercile-stratified L-block volume
  PERMUTATION with random phase, K = 20, `default_rng([20260925 + draw, crc32("asset|lens|va")])`
  (va.py:1125-1169); prices untouched. `gaps+order` is the PIVOT null (random box location;
  `NL.schedule(keep_order=False)` on the machine's confirmed ranges, tierc10_null.py:239-293). The two
  answer different questions (va.py:195-197). A percentile is a description, never a p-value.
- "L+1 conditioning is not built" (va.py:206; X3.md:19).
- Rows the TC12 SFP family will be compared against already exist: e.g. POOLED 4h `va|swing_failure|k3`,
  holdout: long H20 n 289 net +0.2645, short H20 n 312 net +0.1967; `die_parity` holdout: long H20 n 341
  net +0.0709, short H20 n 383 net +0.0898 (read here; a SELECTION, Tier-E).

### 1.10 Anything resembling a traverse

- **No VA traverse exists.** Nothing in va.py, the VA parquets or X3.md measures an edge-to-edge duration
  of price inside value.
- The only traverses are PIVOT-machine quantities in `PINS_X.json` → `T`, lenses 1h and 4h ONLY
  (`T_LENSES`, tc11x_ranges.py:355):
  - (A) of record, `confirm_i − p1_bar`, T = ceil(median), pooled CLASSIC5 tuning head: **1h 13** (l.904;
    n 1437, median 13.0), **4h 13** (l.1173; n 345);
  - (B1) in-range traverse, touch → first OPPOSITE touch, touch law `TOUCH_EPS` 0.60·ATR against the as-of
    box at t−1, open leg dropped (`b_traverses`, tc11x_ranges.py:787-810): 1h 13 (n 1513), 4h 16 (n 303);
  - (B2) transit and (C) chain: distributions only; (D) "the harden-anchored time to the far boundary" was
    **REFUSED: it is an outcome of the X2 event class** (LEANS_X.md:1260).
  - integer law `t_pin` (tc11x_ranges.py:819-832); holdout distribution printed Tier-E, "T is never fit on
    them" (1h ceil-median 13, 4h 15).

### 1.11 Schemas (pyarrow, read here)

`va_series_{1h,4h,12h,1d}.parquet` — identical 61-column schema; rows 284,713 / 71,180 / 23,729 / 11,860
(391,482 in all); key `[asset, open_ms]`; five assets (4h rows: BTC 15440, ETH 14963, ZEC 14542, SOL 13211,
NEAR 13024); floats rounded to 6 dp by the writer:

```
asset:string  lens:string  i:int64  open_ms:int64  close_ms:int64  era:string  L:int64  bins:int64
value_area:double  close:double  atr:double  volume:double  poc:double  val:double  vah:double
val_edge:double  vah_edge:double  window_lo:double  window_hi:double  va_valid:bool
close_in_va_prev:bool  tpo_{poc,val,vah}:double  b100_{poc,val,vah}:double  Lwhole_{poc,val,vah}:double
Lfrozen_{poc,val,vah}:double  Lasset_{poc,val,vah}:double  hs_{poc,val,vah}:double  hs_excluded:bool
hs_defined:bool  L_per_asset:int64  L_whole_tape:int64  L_frozen3_0:int64  l_label:string
n_cells_this_table:int64  + collar (tier, selection_not_a_result, gates, would_read_ci_only,
m_looks_this_table, m_note)  + nine as-of stamps (as_of_last_closed_4h, as_of_panel_start,
as_of_span_days, warranty, as_of_lens, as_of_last_closed_bar, as_of_panel, as_of_n_assets, as_of_substrate)
```

`events_va.parquet` — 424,698 rows, 54 columns, key `[lens, variant, asset, cls, side, i, anchor_i]`:

```
lens variant asset side:string  t0:int64  E:double  extreme:double  closes:int64  bars_out:int64
end_i:int64  end_kind:string(sfp|accept|open)  by:string(n_closes|margin|"")  E_end:double  episode:int64
drift_back:bool  cls:string(episode|sfp|accept|retest-touch|retest-hold)  i:int64  anchor_i:int64
known_at:int64  sgn:int64  level:double  verdict:string  seq:int64  window_end:int64  retest_law:string
known_close_ms:int64  bad_atr:bool  toll_atr_evt:double  era:string  cens_H20:bool  term_H20 mfe_H20
mae_H20:double  cens_H100:bool  term_H100 mfe_H100 mae_H100:double  n_cells_this_table  disclosure
+ collar + nine as-of stamps
```
`i`, `t0`, `end_i`, `known_at`, `anchor_i` are BAR INDICES of the lens tape, not timestamps; join
`(asset, i)` to `va_series_<lens>` for `open_ms / close_ms`. `episode` rows exist only for `variant ==
"record"`. `era` and the outcome columns are EMPTY on the twin variants' `accept` rows (finding
FN-FIX-X3-V7: 104,961 rows, BUILD_DRAFT.md:1013).

`feasibility.parquet` — 432 rows, 75 columns, key `[lens, scale_kind, asset, era, toll]`: lens, scale_kind
(va_regime | va_lblock | va_perbar), asset, era, era_law, era_boundary_ms (1719791999000), n_ranges,
ratio_median, ratio_d1..d9, share_ratio_lt_1, height_atr_median, toll_atr_median, gate_height_pass, edge_n,
edge_n_ranges, edge_median_term_h20, edge_toll_atr, edge_net_h20, edge_hit_rate_net, gate_edge_fade_pass,
both fail_reason columns, the three pinned floors, provisional, verdict_pass, toll, toll_bps,
toll_bps_source, panel, n_units, n_mid_tie, unit, **would_read**, n_bars_perbar,
**of_record_for_detector**, **lens_word**, null_pctile_ratio_median, null_pctile_edge_net_h20, ledger_line,
+ collar + as-of. Counts: lens 108 each; scale_kind 144 each; era 144 each; toll 216 each; asset 72 each.

`two_trades.parquet` — 11,520 rows, 58 columns: cell, lens, detector, trade, variant, direction, era, panel,
horizon, horizon_bars, lane, n_events, n, n_censored, n_bad_atr, toll_atr_all, median_term, mean_term,
q25_term, q75_term, hit_rate, hit_rate_net, median_mfe, median_mae, toll_atr, net, binding_over_n_assets,
provisional, nan_reason, base_net, net_minus_base, null_pctile_net, null_pctile_median_term,
null_n_draws_valid, null_variant_of_record, promotable, registered_as, l_label, disclosure, toll, toll_bps,
toll_bps_source + collar + as-of.

`agreement.parquet` — 792 rows, 56 columns, key `[lens, panel, era, measure]` (VA against the PIVOT box; no
lens-against-lens measure). `events_pivot.parquet` — 41,758 rows, 47 columns.

### 1.12 A volume-profile module already exists in main, and how it differs

- `M/analytics/profile.py` (316 lines, sha `1c0a7519…`, identical to X's copy): `volume_profile` (the
  oracle above), `windowed_profile`, `low_volume_nodes`, `naked_poc_registry`, `relative_volume`;
  constants `PROFILE_ROWS` 120, `VALUE_AREA` 0.70, `WINDOW_SUBSTRATE`.
- Differences from X's value area: `volume_profile` handles ONE slice and has no opinion on which bars
  ("as-of correctness is the caller's", profile.py:116-118); its default `bins` is 100, not 120;
  `windowed_profile` is a clock window in DAYS selected by bar OPEN time (`t > as_of − W` and `t <= as_of`,
  profile.py:214), on a finer substrate (1m/5m/15m), with a coverage refusal; there is NO rolling series, NO
  state machine, NO events, NO TPO twin, NO ATR.
- `M/analytics/nesting.py` (`va_nesting`, `ADJACENT_PAIRS` 7d↔30d↔90d↔365d) compares value areas across
  WINDOW SCALES by overlap fraction; it is not the lens ladder's boundary coincidence.
- `M/analytics/INTERFACE.md` (sha `70c3f368…`, identical in X): profile family is "FIXTURE-VERIFIED, NOT
  chart-certified" (l.243), excluded from the chart gate by design (l.245-250).
- Package rules a new `analytics/value_area.py` meets (`M/tests/test_analytics.py:118-161`, which globs
  EVERY `analytics/*.py`): F-AN-3 — no line matching `^\s*(from|import)\s+engine\b` in the raw source;
  F-AN-4 — none of `read_parquet`, `requests`, `urllib`, `os.environ`, `socket`, nor an `open(` call, in the
  code tokens. INTERFACE.md I-B also bars imports from `scripts/`.
- `analytics._MODULES` (__init__.py:118-120) lists ten files; `rangefinder_census.py` lives in the package
  but is deliberately NOT in that tuple so `analytics_sha()` stays put (rc.py header, "NOT IN
  analytics._MODULES, ON PURPOSE").

### 1.13 X3 readings and VA-touching amendments

- Readings: LEANS_X.md LX-X3.1 (L, :1582), X3.2 (composite, :1608), X3.3 (bins, :1636), X3.4 (70%, centers,
  :1642), X3.5 (TPO twin, :1649), X3.6 (VA(t−1), frozen E, :1655), X3.7 (acceptance, re-arm, :1670), X3.8
  (SFP, :1682), X3.9 (retest, :1693), X3.10 (feasibility, :1708), X3.11 (two trades, :1756), X3.12
  (agreement, :1779), X3.13 (nulls, :1793), X3.14 (the ledger line, :1811).
- AM-X11 (LEANS_X_AMENDMENTS.md:243-268) rules in AP-11's seventeen builder completions, among them: re-arm
  judged on IDLE bars only; the hold uses the machine's strict comparator; "next acceptance" is of either
  side; first regime starts at the first bar with a valid VA(t−1); regime geometry excludes its acceptance
  bar; DIE parity accepts at `>=` 1.5 ATR, the open bar included; the lens word carries the
  maker-reopening sentence; per-bar twin rows carry no verdict.
- AM-X12 (:272) maker-twin sentence placement. AM-X19 (:443) "a traverse value LANDED" rule (T ABSENT, L
  ABSENT). AM-X20 (:461) the feasibility twins are va_regime / va_lblock / va_perbar; a TPO feasibility
  twin is a finding-not-fixed. AM-X22 (:507) and AM-X27 (:575) ferry classes of `va/two_trades` and
  `va/agreement`. AM-X13 (:291) `va/events_*` are POINTED.
- The standing ledger lines (LEANS_X.md:1811-1818, 2468-2470; staged in LEDGER_APOLLO_APPEND.md:159-183):
  "No registration until the value-area detector's edges-respected leg passes"; "a VA PASS licenses only
  that lens × detector × toll"; "any later registration drawn from an X Tier-E grid (X1 cells, X2 twins, X3
  events and feasibility, X4 cells) carries pre_seen for bars ≤ 2026-09-25T00:00Z".

---------------------------------------------------------------------------------------------------------
## 2 · CONTRACT-vs-DISK

C1. **"research_outputs/tierc11x/va/, scripts, shas printed"** (V1). In the tree TC12 is built in (main)
that path does not exist; X is unmerged. The nine parquets are untracked even in X, so they are reachable
only by absolute worktree path; their shas of record are the tracked `progress/X3.json`.

C2. **"Lookback per lens = X's pin … FROZEN here as bars"** (V1). Disk carries four pins (71/66/53/35).
**No 1w pin exists**, while V5 orders "the VA vector at 1h, 4h, 12h, 1d, 1w".

C3. **"decoupled from the pivot detector"** (V1). On disk the pin IS the pivot detector's mean died-range
life at the calibrated picks (PINS_X.json:897). Decoupling is possible only by freezing the integers.

C4. **"CAUSAL: the VA stamped at bar t uses volume from bars ≤ t only"** (V1). True of X's series. But X
never judges close[t] against that VA: every state, event, %-of-value and height uses VA(t−1). The contract
is silent on which VA a close is judged against.

C5. **"ACCEPTED above/below: 8 consecutive closes beyond the edge OR one close ≥ 1.5 ATR_L beyond"** (V2).
X's law of RECORD is 8 closes ONLY (X's own contract: "Acceptance outside value = 8 consecutive closes
beyond", `X/exchange/queue/2026-09-25_TC11X_APOLLO.md:30`; LEANS_X.md:1670-1672). The OR-clause is X's
`die_parity` TWIN. At 4h it moves acceptances 1474 → 1605, of which 1217 (75.8%) come by margin.

C6. **"a probe that closes back inside within K=3 closes = SWING FAILURE"** (V2). X's record is 7
(`DEV_RETURN_BARS`); 3 is X's `k3` TWIN (`t − t0 <= 3`). With K = 3 a third outcome appears that the
contract does not name: a probe returning on closes 4..7 (X's "lapse": 482 at 4h under the record
acceptance, X3.md:68; 400 under die-parity, counted here as the 4h `die_parity` SFP rows with
`bars_out > 3`: 277 tuning + 123 holdout).

C7. **"X's semantics asserted equal on the 4h holdout sample"** (V2). No filed X stream IS the contract's
machine: `EP_LAWS` has `die_parity` and `k3` separately, never combined. A derived target exists (R10
below).

C8. **"ACCEPTED decays to INSIDE when the re-rolled VA contains the close"** (V2). X has no ACCEPTED state
and no decay; it has a per-side armed flag, re-armed (BOTH sides) by an IDLE close inside VA(t−1). A close
inside the live VA while an opposite-side episode is pending does not re-arm (15 bars in 20 cells).

C9. **"INSIDE / PROBING / ACCEPTED … Columns at every instant: state"** (V2). X files EVENTS and a boolean
`close_in_va_prev`; it files no per-bar state column. X's machine also has situations the three words do
not cover (a resolving bar; both sides disarmed; warm-up).

C10. **"signed edge distance (ATR_L) · VA age · POC distance"** (V2). X has an UNSIGNED nearer-edge distance
(`va_view.dist_atr`, va.py:1216), a regime age only inside the adapter (`ir_age = t − r0`), and no POC
distance.

C11. **"reproduce X's feasibility verdicts from X's records — 4h taker PASS · 1d taker PASS · 1h maker PASS
· 12h FAIL · 1h taker FAIL"** (V3). All five reproduce (table in §1.8). But: "1h maker PASS" is NOT a row
of record in X (`of_record_for_detector` False; it is the "maker twin"); the 1h word of record is a long
sentence, not "FAIL"; "12h FAIL" names no toll (taker FAIL and maker FAIL both hold on va_regime, while the
12h maker L-block twin PASSES); "1d taker PASS" holds on the holdout only.

C12. **"the Q-R3 law licenses exactly {VA-4h taker, VA-1d taker, VA-1h maker}"** (V3). X's ledger line
says a PASS "licenses only that lens × detector × toll" and that any later VA registration is `pre_seen`
for bars ≤ 2026-09-25T00:00Z. The contract labels P-ADM-1 `pre_seen` but carries no such label on
P-SFP-VA-1 or P-SCALP-3.

C13. The licence was measured on a different object from what TC12 trades: record (8-close) regimes,
entries in the outer **20%** of value, a fixed H20 exit, both legs at one toll. P-SCALP-3 uses the outer
third (33/67), POC / far-edge targets, and "maker bps per side on entry and targets; taker on the stop".
The 1h holdout edge leg breaks even at 6.35 bps round trip; one maker leg plus one taker leg is 7.0 bps
(2.0 + 5.0).

C14. **"TRAVERSE TABLE: per lens, the median bars for price to travel edge-to-edge while INSIDE … read,
never typed"** (V4). No such quantity exists for the value area on disk. X's T (13 / 13) is a pivot confirm
traverse for 1h and 4h only.

C15. **"`data/fee_schedule.json` must carry maker_bps_side per venue"** (Stage D). `M/data/fee_schedule.json`
does not exist. The fee file X read is `research_outputs/tierc11/data/fee_schedule.json`; its key is
`maker_bps_per_side` (2.0), flat across venues and declared an ASSUMPTION; X's reader renames it
`maker_bps_side` in memory only (tc11x_env.py:1289).

C16. **"null gaps+order (R10)"** on the VA two-trades (Stage R Tier-E). `gaps+order` is defined on the
pivot machine's boxes. X's VA null of record is the volume permutation `tr_tercile_lblock`.

C17. **"conditioned on the lens above"** (Stage R Tier-E). X: "L+1 conditioning is not built".

C18. **"BOUNDARY COINCIDENCE (an edge of L within 0.25 ATR_L of an edge of L+1)"** (V5). X's 0.25·ATR
coincidence is VA edge against the PIVOT box on the SAME lens, same side, inclusive (va.py:1069-1070). The
lens-ladder form is TC11's L-R.5 (`M/research_outputs/tierc11/LEANS.md:224-237`: ladder
1h→4h→12h→1d→1w, either boundary of L+1, 1w NA).

C19. **"Twelve new assets: 1h/4h/1d"** (V5). X built the value area for CLASSIC5 only; L is a CLASSIC5
pooled pin; the feasibility words are CLASSIC5 words.

C20. **"F-VA-RAW … on 3 windows; a shifted volume column must FAIL"** and **"F-VA-ASOF (profile including
bar t+1 must FAIL)"**. Both exist in X under other names: F-VA (tc11x_va_fixtures.py:273-381; windows
ETHUSDT 1h t=39619, BTCUSDT 4h t=10649, NEARUSDT 1d t=527) and F-VA-ASOF's break plant (a window shifted
one bar forward inside `va_windows`).

---------------------------------------------------------------------------------------------------------
## 3 · READINGS NEEDED (candidate leans, each with a recommendation)

**R1 · Where L is read and what is frozen.** Options: (a) read `PINS_X.json` `L.by_lens.<lens>.L_of_record`
and hold it equal to `va/build_manifest.json` `pins.L.<lens>.record` and to the parquet column `L`;
(b) type 71/66/53/35. *Recommend (a)*: a filed pin, three concordant sources, sha-held (`85e1eeea…`); freeze
the integers and never re-derive them from a pivot run. Twins (whole-tape, frozen-3.0, per-asset) are not
carried.

**R2 · The 1w lookback.** Options: (a) no 1w VA, the 1w columns NA with the reason; (b) X's law at 1w —
needs the pivot machine (contradicts "decoupled"), and TC11's 1w picks are whole-window fallbacks (in-sample
everywhere; 309-367 weekly bars; 2-3 confirmed ranges per asset at the pick, per-asset means 24.3 / 12.0 /
29.0 / 9.0 / 28.7 in `M/research_outputs/tierc11/ranges/SCALE_GRID.parquet`); (c) carry X's coarsest filed
pin, 35 bars; (d) a calendar equivalent (35 d = 5 weekly bars). *Recommend (c)*, filed as a dated amendment
under the "va-lookback" veto and labelled "not X's pin; X built no 1w series": it reuses a filed integer,
is tuning-fit (carries no holdout information, unlike (b)), and leaves a usable sample. 1w is stamp-only
(ruling Q4), so no verdict rests on it. (a) is the fallback if the operator vetoes.

**R3 · Which VA a close is judged against.** Options: VA(t−1) (X record) or the self-inclusive VA(t) (X
twin). *Recommend VA(t−1)*: X's law, and both satisfy "bars ≤ t". Rule for any instant: a price observed
during lens bar b, up to and including its close, is judged against VA(b−1).

**R4 · Frozen or moving edge during a probe.** *Recommend frozen* `E = VAH(t0−1)` / `VAL(t0−1)` (X record).
The moving edge turns 27-37% of SFPs into drift-backs (LEANS_X.md:1660-1661).

**R5 · The acceptance clause.** The contract's text equals X's `die_parity` twin, not X's record. Options:
(a) implement the contract's text and file a dated amendment naming the difference; (b) implement X's
record and file the OR-clause as the twin. *Recommend (a)*, the contract is explicit; print X's record
beside. Detail to freeze with it: `abs(c[t] − E) >= 1.5·atr[t]`, inclusive, `atr[t]` of the same bar,
allowed on the probe's first bar.

**R6 · What "within K=3 closes" counts.** Options: `t − t0 <= 3` (X's `k3` twin; equivalently at most 3
closes beyond the edge before the close back) or `t − t0 <= 2`. *Recommend `t − t0 <= 3`*: it is X's own
literal (va.py:187, 532) and has a filed stream.

**R7 · A probe that returns on closes 4..7.** Not a swing failure and not an acceptance. *Recommend*: name
it LAPSE (X's word), state returns to INSIDE, no event for any trade, the side stays armed; count it.

**R8 · Decay of ACCEPTED.** *Recommend X's re-arm verbatim*: the first IDLE close with `VAL(t−1) <= c[t] <=
VAH(t−1)` returns the state to INSIDE and re-arms both sides; closes beyond the accepted side meanwhile
stay ACCEPTED and open no new probe.

**R9 · Deriving the per-bar state from the machine.** *Recommend*, as a pure function of the machine after
bar t: PROBING(side) if an episode is pending; else ACCEPTED(side of the latest acceptance) if any side is
disarmed; else INSIDE; UNDEFINED while VA(t−1) is invalid (bars 0..L−1). A resolving bar takes the state
after resolution. The executor should print how many bars fall in each odd case (SFP bar with a side still
disarmed; both sides disarmed).

**R10 · The equality assertion's sample and target.** *Recommend*: sample = CLASSIC5, 4h, events whose
known-at close is after 2024-06-30T23:59:59Z and ≤ X's pin 2026-09-25T00:00Z. Target = `events_va.parquet`,
`lens == "4h"`, `variant == "die_parity"`, `cls ∈ {sfp, accept}`, era taken by joining `(asset, i)` to
`va_series_4h` (the twin's accept rows have a blank `era`). Expected counts, read here: **555 acceptances
(432 by margin, 123 by 8 closes); 725 closes back inside, of which 602 with `bars_out <= 3` (the V2 swing
failures) and 123 lapses**. Compare (asset, side, t0, end_i, by) exactly and E, extreme at 1e-6. Print X's
record stream beside (509 acceptances, 754 SFPs at K = 7, 602 at K = 3) as the dated difference.
Basis and its limit: that `die_parity` filtered to `bars_out <= 3` IS the combined law follows from the
code (only an acceptance changes an armed flag or a regime, va.py:569-583; `ret_k` only chooses the label
at va.py:610). On disk I verified that identity for record ↔ k3 only, so the executor should assert it for
the combined law with a fresh run of `EpLaw(ret_k=3, die_parity=True)`.

**R11 · ATR_L.** *Recommend* `engine.indicators.atr(h, l, c, 14)` on the whole tape from its first bar,
computed in `scripts/` and HANDED IN to the module; `atr[t]` at the bar judged.

**R12 · Level convention.** *Recommend* bin CENTERS, POC tie to the lowest bin, expansion tie UP, 120
rows, 0.70 — all read by object from `analytics.profile`; EDGES and TPO as printed twins.

**R13 · Volume source and substrate.** *Recommend* lens-own bars: native 1h / 4h / 12h, Stage D's derived
1d, derived 1w; row alignment asserted before any VA.

**R14 · The four columns.** *Recommend*: %-of-value = `100·(c − VAL)/(VAH − VAL)` against the judging VA,
unclamped (X's `pct`); signed edge distance = distance to the NEARER edge in ATR_L, positive inside,
negative beyond, `near_side` beside (TC11 L-R.5's sign law); VA age = `t − r0` of the alive value regime
(X's `ir_age`), NaN while ACCEPTED; POC distance = `(c − POC)/ATR_L`, signed.

**R15 · Stamps at instants that are not a lens close.** *Recommend*: take the last lens bar b* whose close
is ≤ the instant; state = the machine's state after b*; the levels in force for later prices are VA(b*);
print both the judging VA and the in-force VA so no reader has to guess.

**R16 · The mirror's row filter and word column.** *Recommend*: the filter and `would_read` column of §1.8;
"12h FAIL" read as the taker row of record (print the maker row FAIL beside); hold each word also to the
tracked `build_manifest.json` `va_lens_verdicts`; verify the parquet's sha against `progress/X3.json`
first; HALT on any disagreement. Never recompute the verdicts under the V2 machine and call that the mirror.

**R17 · The traverse (V4).** Options: (a) the B1 analog on value regimes — from a bar touching one edge to
the first bar touching the opposite edge, the first leg starting at the regime's first touch, an open leg
dropped; (b) the B2 transit analog; (c) time from a swing failure to the far edge. *Recommend (a)* with:
wick touch against VA(t−1) and no epsilon (no new constant); regimes under the V2 machine; fit on the
tuning era only, pooled CLASSIC5, `T = ceil(median)` by `t_pin`; the holdout distribution printed Tier-E.
*Refuse (c)*: X refused its pivot counterpart as an outcome of the traded event class.

**R18 · The null named for the VA two-trades.** Options: X's VA null of record (`tr_tercile_lblock`), or a
gaps+order analog built on value regimes. *Recommend the VA null of record, named on the row*, with a dated
note that gaps+order is undefined without boxes.

**R19 · The breakout-retest on V2 acceptances.** *Recommend* X's retest law unchanged (frozen E, the touch
law, hold = no close through by more than 1.0·ATR over touch..touch+6, TTL 400, next acceptance of either
side); its filed counterpart is the `die_parity` breakout_retest variant (4h: 770 holds).

**R20 · Which profile sets an SFP trade's POC and far edge** (cross-unit, Stage R). Options: the profile
that defined the faded edge, VA(t0−1), frozen; or the profile at entry. *Recommend VA(t0−1) frozen*, the
entry-profile version printed as a twin: one coherent geometry for the reward test, all of it known before
the probe.

**R21 · pre_seen labels.** *Recommend* carrying X's standing line: P-SFP-VA-1, P-SCALP-3 and P-DIR-1 are
drawn from X3's events and feasibility and are `pre_seen` for bars ≤ 2026-09-25T00:00Z. The orchestrator
should rule on this before the build, since the contract is silent.

**R22 · The module's shape.** *Recommend*: `analytics/value_area.py` pure numpy, no I/O, ATR and arrays
passed in, NOT added to `analytics._MODULES`, constants read from the sibling `analytics.profile` by
object behind the sha pin `1c0a7519…`.

**R23 · The twelve new assets.** *Recommend* the same per-lens L (71 / 66 / 35), Tier-E, with the label
that L and every feasibility word are CLASSIC5 quantities.

---------------------------------------------------------------------------------------------------------
## 4 · HAZARDS

H1. **Self-inclusion.** Judging close[t] against VA(t) lets a breakout bar drag VAH to its own close. X's
structural fixture asserts `E == VAH(t0−1)` on every episode; a prefix test cannot see this defect.

H2. **An unclosed higher-lens bar in a stamp.** A 1d or 1w bar exists only when all of its 4h bars do
(census.py:560-571); a stamp at an intraday instant must use the last bar whose close ≤ the instant.

H3. **Parameter look-ahead.** A traverse (or any pin) fitted on the full corridor leaks holdout
information into P-SCALP-3, which is scored on the holdout. X fitted T and L on the tuning head only.

H4. **The verdicts and the machine are different laws.** X's feasibility words were earned on record
(8-close) regimes. Recomputing them under the V2 machine gives different regimes; only a READ of X's rows
is a mirror.

H5. **The licence is narrower than the trade** (C13): the 1h maker PASS fails above 6.35 bps round trip,
and was measured on the outer 20% with an H20 exit.

H6. **ATR.** `analytics.volatility.atr` is not the engine ATR. A tail-loaded tape re-warms the ATR. Either
moves the 1.5-ATR acceptances and every ATR-scaled column.

H7. **6-dp rounding of the filed series.** X's writer rounds floats to 6 dp. Recomputing a state from the
filed `val / vah` flips exact-edge cases (ZECUSDT 4h i = 8337: close 30.17 against a filed VAH of
30.170000, filed flag False). Compare series at 1e-6 and events from a fresh computation, never from the
filed levels.

H8. **Twin acceptance rows have no era.** Filtering `era == "holdout"` on `variant != "record"` silently
drops every acceptance.

H9. **Volume alignment.** A volume column shifted by one bar moved the histogram by 2.024e-01 relative on
F-VA's first window (FIXTURES_X3.txt, F-VA BREAK line) and raises no error by itself: the shift is inside
the array, so only the raw-slice recompute catches it. Keep both that fixture and the row-for-row
`open_time` assert.

H10. **Substrate drift under the top-up.** X's twenty kline inputs are pinned by sha in the manifest
(`input_sha`). A topped-up snapshot has new file shas; the mirror holds only if every row closing ≤
2026-09-25T00:00Z is unchanged, including the derived 1d (and 1w) files. Assert prefix equality first.

H11. **`analytics_sha()`.** Editing `analytics/profile.py` or adding a file to `_MODULES` moves the sha
that every BRIEF capture prints and that X's F-PROFILE-PIN holds.

H12. **Package scans.** `tests/test_analytics.py` globs every file in `analytics/`: an `import engine`
line, or the tokens `read_parquet`, `requests`, `urllib`, `os.environ`, `socket`, `open(`, fail the suite.

H13. **numpy.** Bit-exactness to `volume_profile` rests on `np.linspace`'s arithmetic, `argmax` first-max
and summation order (numpy 2.1.3 here). A version change can move a level by one bin.

H14. **Bar-count windows across gaps.** L is counted in bars; a missing bar stretches the window in clock
time. Gaps are counted in the tape meta and never filled.

H15. **X must not gain a file.** Importing any `tc11x_*` module from the worktree path arms its hooks,
re-roots census globals to the worktree and can write `__pycache__`. Read bytes only, or `git
--no-optional-locks -C X show 7b24f835:<path>` for tracked files. X's `close_acts.sh` has never been run.

H16. **Seeds.** X's nulls use seed 20260925; TC12's seed is 20261008. Re-running a null under TC12's seed
does not reproduce X's filed percentiles; the record VA path itself uses no RNG.

H17. **Pooled tolls.** The pooled toll is the binding MAX of per-asset medians, not a pooled median; a
re-derivation that pools first gets different nets.

H18. **Selection.** X's two-trades table already prints the 4h and 1d VA swing-failure outcomes for the k3
and die-parity laws, by direction and era, on the same bars P-SFP-VA-1 will score.

---------------------------------------------------------------------------------------------------------
## 5 · REUSE PLAN

**Import (main tree, unchanged):**
- `analytics.profile` — `PROFILE_ROWS`, `VALUE_AREA` by object; `volume_profile` as the bit-exact oracle
  for F-VA-RAW. Pin its sha `1c0a7519…`.
- `engine.indicators.atr` — from `scripts/` only, handed into the module.
- The era law and constants from `scripts/tierc10_census.py` where a script needs them (`era_of`,
  `ERA_BOUNDARY_MS`, `HORIZONS`, `PROVISIONAL_MIN_N`).

**Vendor or mirror into `analytics/value_area.py`** (pure numpy; X's functions have no I/O once `halt` and
the module constants are replaced by arguments):
- `_bin_right`, `va_core`, `va_windows`, `va_series` (va.py:326-450) — the series, volume and TPO modes.
- `EpLaw`, `ref_arrays`, `va_episodes` (va.py:520-646) — instantiate the contract's machine as
  `EpLaw(ret_k=3, die_parity=True)`; keep the record law available for the dated difference.
- `retest_verdict`, `touch_mask`, `scan_retests`, `va_anchors` (va.py:674-764) — the breakout-retest.
- `regime_units` (va.py:968-977) and the `va_view` formulas (va.py:1208-1218) — VA age, %-of-value.
- A byte copy of `tc11x_va.py` named with its sha (X's own precedent:
  `research_outputs/tierc11x/vendor/tierc11_env@086d66da.py`) is the cleanest provenance for the mirror;
  take the bytes with `git show 7b24f835:scripts/tc11x_va.py` (sha `3f6a43cb…`).

**Read as records (absolute X paths, sha-verified against `progress/X3.json`):**
- `PINS_X.json` for L; `va/build_manifest.json` for `pins`, `va_lens_verdicts`, `sha`, `input_sha`.
- `va/feasibility.parquet` for F-VA-MIRROR; `va/events_va.parquet` + `va/va_series_4h.parquet` for the V2
  equality; `va/va_series_<lens>.parquet` for a full-series equality at 6 dp (391,482 rows);
  `va/two_trades.parquet` for the rows printed beside the new Tier-E tables.

**Mirror as fixtures:** F-VA (raw-volume recompute, `loop_profile`, the shifted-volume plant,
tc11x_va_fixtures.py:273-381) → F-VA-RAW; F-VA-ASOF's forward-shifted-window plant → F-VA-ASOF; `my_word`
(:927-936) → F-VA-MIRROR's re-derivation; F-EVT-ASOF's structural leg (`E == VAH(t0−1)`) → F-STATE.

**Newly written (no X counterpart):**
- the per-bar state column and its derivation (R9), signed edge distance, POC distance;
- the VA traverse and its table (R17);
- a 1w series (R2), and VA series for the twelve new assets;
- the lens-ladder boundary coincidence (TC11 L-R.5's form, not X's VA-vs-pivot form);
- the lens-above conditioning of the two trades;
- stamps at non-lens instants and the 5m clock's read of the 1h value area (R15);
- any maker/taker mixed-leg cost arithmetic (X's maker twin is both legs at one toll).
