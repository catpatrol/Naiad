# BUILDER'S REPORT — W-F1 WINNER FORENSICS
**Contract:** `exchange/queue/2026-08-03_WF1_winner_forensics_APOLLO.md` (drafted APOLLO, ratified operator 2026-08-03, word "forensics")
**Executor:** HEPHAESTUS · **Run date:** 2026-08-04 · **Branch:** `v12-v1-census`
**Status: COMPLETE. 9/9 fixtures PASS. All three deliverables emitted.**

This report is written zero-context: every gate value, probe, table and hash needed to
re-derive or refute the study is inline.

---

## 0 · HARD ASSERTIONS (run before any read or write)

| assertion | result |
|---|---|
| `git rev-parse HEAD` | `4176f83cd1f5d2558b98878545eceb84db8898f1` ✅ |
| path contains `Users…OneDrive` | `/c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad` ✅ |
| `engine/` | exists ✅ |
| `LEDGER.md` | exists ✅ |
| `exchange/queue/` | exists ✅ |
| `exchange/reports/` | exists ✅ |
| `exchange/status/` | exists ✅ |
| `scripts/publish_exchange.py` | exists ✅ |
| `research_outputs/_unarchived/s3_2026-07-27/journal_s3/scored/` | exists, **753 files** ✅ |

**No exchange subdirectory was missing; none was created.** (On the prior run this gate
HALTED — the journals were absent. ATHENA restored them from
`research_outputs/_archive/s3_2026-07-27.zip`; see
`exchange/reports/2026-08-04_ATHENA_s3-journal-restore.md`.)

**Lockbox:** the scored journal set spans **2019-10 … 2024-06**. Zero files dated
2024-07-01 or later exist in the tree, so no lockbox bar was read. Verified by
enumerating every month filename.

---

## 1 · STEP 0 — SYNTHESIS FILED

`SS_Reassessment_Synthesis_2026-08-03.md` **was attached** and is filed byte-exact:

```
sha256  9d6e7ea747544561af509bbcc845648fa66367cae8157feec1916b18ab4cbff1
bytes   8282
src     SS_Reassessment_Synthesis_2026-08-03.md              (repo root, untracked)
dst     exchange/reports/SS_Reassessment_Synthesis_2026-08-03.md
cmp     IDENTICAL (byte-for-byte)
```

## 2 · STEP 1 — QUEUE ITEM WRITTEN

`exchange/queue/2026-08-03_WF1_winner_forensics_APOLLO.md`, containing exactly the
CONTRACT block, sha256 `a08e36ad96c68948ed10f691d5003e2c6ba339daf6aff8c672be3b85160c8ea0`
(3,934 bytes). Per workflow ruling Q-5 the item **is** the contract; it was then executed
verbatim as STEP 2.

---

## 3 · PROBE VALUES — the event model, measured not assumed

The contract names fields without saying which event carries them. Measured across all
**1,279,720** journal rows:

| evt | rows | role |
|---|---|---|
| REJECT | 647,325 | — |
| TAG | 245,651 | — |
| PRIME | 228,511 | — |
| CONFIRM | 82,542 | — |
| CLUSTER | 42,927 | — |
| **EXIT** | **7,094** | resolution |
| STOP_FILL | 5,031 | — |
| REGIME | 4,801 | — |
| **ENTRY_FILL** | **3,903** | birth (r1 + v) |
| X | 3,861 | — |
| **ADD_FILL** | **3,214** | birth (re_entry) |
| TPW | 2,999 | — |
| STAGE | 1,050 | — |
| HALT | 653 | — |
| V | 158 | — |

**BIRTH** = `evt ∈ {ENTRY_FILL, ADD_FILL}` = 7,117, carries `fill_class`, `s2`, `retr`,
`atr_exec`, `atr_gov`, `px_fill`, `stop`, `zone`, `stage`, `grade`, `qty`, `size_r`,
`concurrent_open_at_fill`.
**EXIT** carries `realized_r`, `exit_reason`, `funding_cum`, `give_back_r`, `mfe_r`,
`mae_r`, `engagement_flags`.
Join key `(cell_id, tranche_id)` in format `c<N>t<N>` — **7,117 birth keys and 7,094 exit
keys, zero duplicates on either side, zero exits without a birth.** The substrate key set
equals the EXIT key set exactly (7,094/7,094, no orphans either way).

The 23 unresolved fills are genuine right-edge truncation: all have `ts_open` in
**2024-06**, the corpus's final month, each after the last EXIT in its own cell.

---

## 4 · FULL FIXTURE TRANSCRIPT (verbatim console output)

```
W-F1 WINNER FORENSICS
==============================================================================

=== INGEST ===
  checkpoints: 20 cached, 0 computed
  births total: 7117
  substrate rows: 7094

=== FIXTURES ===
  [PASS] F-WF1a: r1=3825 + v=78 + re_entry=3214 = 7117 fills; 7094 resolved + 23 excluded
  [PASS] F-WF1b: stopout (exit_reason in stop/stop_gap) = 5016, expect 5016
  [PASS] F-WF1c: substrate join covers 7094/7094 resolved tranches

  n=7094  floor(0.1*n)=709
  L (bottom 709): realized_r <= -0.852774   range [-3.975249, -0.852774]
  W (top    709): realized_r >= 0.067318   range [0.067318, 193.463416]
  [PASS] F-WF1d: decile sizes W=709 L=709; count(r<=-0.852774)=709, count(r>=0.067318)=709;
                 cut multiplicities 1/1 -> no tie straddles either boundary
  time split at median ts_open = 2022-06-10T03:55:00Z  -> early 3547 / late 3547
  [PASS] F-WF2: 40 Section-A features attested curtain-clean, all populated on every birth;
                0 post-fill fields present in the Section-A list; 1 rejected as post-fill
                (engagement_flags: 0 births carry it)

=== SECTION A ===
  Section-A family: 84 tests, 15 FDR-surviving, 12 CANDIDATE
  Annex family:     11 tests, 0 FDR-surviving
  [PASS] F-WF3: full Section-A table (84 rows x 11 stats) recomputed at seed 20260803:
                byte-identical, sha256 7097b523394acdf1 == 7097b523394acdf1
  [PASS] F-WF4: panel 6897 + annex 197 = 7094 resolved; annex assets (JTOUSDT, TAOUSDT)
                excluded from panel sums
  [PASS] F-WF5: BH recomputed by explicit formula for 3 rows (ranks [1, 5, 78]) of m=78
                tested rows (6 no-contrast rows excluded from the family); recomputed q ==
                reported q for all 3 ([0.0006, 0.0006, 0.9748])

=== TRG ===
  [PASS] F-WF6: unfiltered book driven through trg_for(): kept 7094/7094, top-decile 709/709,
                retained R 3035.949713 of 3035.949713 -> TRG = 100.0% exactly
  atr_exec_bps                           keep 0.500  dExp +0.0500 R  TRG 50.6%
  atr_gov_bps                            keep 0.500  dExp +0.0143 R  TRG 46.2%
  fill_class=re_entry                    keep 0.549  dExp +0.0137 R  TRG 39.7%
  fill_class=r1                          keep 0.538  dExp +0.0177 R  TRG 39.6%
  zone=Z3                                keep 0.733  dExp -0.0043 R  TRG 65.0%

=== SECTION B (post-birth; NOT curtain-clean) ===
  median hold  W 128.48 h   L 0.08 h   ratio 1541.80x
  |funding|/|pnl| median (dimensionless)  W 0.0352   L 0.0000

  secondary r1-only: n=3814 decile=381 candidates=20
  sensitivity v-excluded: n=7016 decile=701 candidates=11

=== PREDICTIONS ===
  P-WF1 [70%] PREMISE-FALSE
  P-WF2 [65%] CONFIRMED
  P-WF3 [55%] CONFIRMED
  P-WF4 [60%] CONFIRMED
  P-WF5 [50%] CONFIRMED

=== FIXTURE SUMMARY ===
  9/9 pass
```

`F-WF1` is reported as four sub-fixtures (a–d) because the contract bundles reconciliation,
stopout, join coverage and decile sizing into one line; each is separately falsifiable.

---

## 5 · POPULATION AND DECILES

| quantity | value |
|---|---|
| journal files | 753 |
| journal rows scanned | 1,279,720 |
| fills | **7,117** = r1 **3,825** + v **78** + re_entry **3,214** |
| resolved | **7,094** |
| unresolved, excluded-and-counted | **23** |
| stopout `exit_reason ∈ {stop, stop_gap}` | **5,016** (stop 4,995 + stop_gap 21) — contract's expectation hit exactly |
| substrate rows / join coverage | 7,094 / **7,094 (100%)** |
| decile size `floor(0.1 × 7094)` | **709** |
| **L** (bottom 709) | `realized_r ∈ [-3.975249, -0.852774]` |
| **W** (top 709) | `realized_r ∈ [0.067318, 193.463416]` |
| boundary ties | **none** — each cut value occurs exactly once; `count(r ≤ L_cut) = 709`, `count(r ≥ W_cut) = 709` |
| time split at median `ts_open` | `2022-06-10T03:55:00Z` → 3,547 early / 3,547 late |
| book total R | −351.15 (mean −0.0495 R) |
| top-decile total R | **3,035.949713** |

7,094 is not divisible by 10, so a modulo bucketer would yield 710/709/710/… — the explicit
head-709/tail-709 slice is what produces exact deciles.

---

## 6 · F-WF2 CURTAIN AUDIT

**40 features attested curtain-clean**, each read from the BIRTH event or derived solely
from the birth timestamp. Full per-feature attestation table is in `WF1_tables.md §F-WF2`.
Summary of sources:

- 8 categorical contract fields (`symbol`, `mandate`, `dir`, `fill_class`, `grade`, `zone`, `stage`, `concurrent_open_at_fill`) — read from `ENTRY_FILL`/`ADD_FILL`, all non-null on all 7,117 births.
- 3 numeric (`retr`, `atr_exec_bps`, `atr_gov_bps`) — bps forms use the BIRTH `px_fill`.
- 2 annex (`session_bucket`, `dow`) — derived from BIRTH `ts_open`.
- 27 varying `s2` boolean flags — the engine writes `s2` at fill time (`engine/s2.py`), snapshotting the level/detonation state as of the fill bar.

**REJECTED — 1 feature, and this is a contract defect:**

| feature | evidence | disposition |
|---|---|---|
| `engagement_flags` | **NULL on all 7,117 births; non-null on all 7,094 EXITs.** Its five subkeys (`ext_before_exit`, `ext_i_offset`, `mfe_at_ext_r`, `tpw_before_exit`, `xa_engaged_before_exit`) all describe what happened *during* the trade. | Removed from Section A, demoted to Section B. |

The contract lists `engagement_flags` among the Section-A categoricals. Including it would
have leaked outcome into a "discriminant at birth" and produced a spectacular, meaningless
separation. **This is the single most consequential thing the curtain audit caught.**

---

## 7 · SECTION A RESULTS

Family = **84 tests**, of which **78 carry contrast** and enter the BH family; 15
FDR-surviving; **12 CANDIDATE** (CI excludes zero + FDR-surviving + panel sign-consistent +
time-stable). Bootstrap 10,000 resamples at seed 20260803, BH-FDR q\* = 0.10.

### The 12 CANDIDATES

| discriminant | prev/med W | prev/med L | Δ (W−L) | 95% CI | q | panel |
|---|---|---|---|---|---|---|
| `fill_class=r1` | 0.6135 | 0.1932 | **+0.42031** | [+0.37518, +0.46686] | 0.000600 | 5/5 |
| `fill_class=re_entry` | 0.3780 | 0.8054 | **−0.42736** | [−0.47391, −0.38082] | 0.000600 | 5/5 |
| `zone=Z1` | 0.6827 | 0.4739 | **+0.20875** | [+0.15797, +0.25811] | 0.000600 | 5/5 |
| `zone=Z3` | 0.1932 | 0.4076 | **−0.21439** | [−0.25952, −0.16784] | 0.000600 | 5/5 |
| `mandate=intraday` | 0.7560 | 0.8886 | −0.13258 | [−0.17066, −0.09309] | 0.000600 | 5/5 |
| `mandate=swing` | 0.1932 | 0.0987 | +0.09450 | [+0.05783, +0.13117] | 0.000600 | 5/5 |
| `mandate=position` | 0.0508 | 0.0127 | +0.03808 | [+0.01975, +0.05642] | 0.000600 | 5/5 |
| `stage=1` | 0.4767 | 0.3695 | +0.10719 | [+0.05501, +0.15797] | 0.000600 | 5/5 |
| `stage=2` | 0.5233 | 0.6305 | −0.10719 | [−0.15797, −0.05501] | 0.000600 | 5/5 |
| `atr_exec_bps` (median) | 18.6066 | 10.3007 | **+8.30588** | [+7.04036, +9.94932] | 0.000600 | 5/5 |
| `atr_gov_bps` (median) | 153.3947 | 97.4401 | **+55.95459** | [+47.57060, +67.36405] | 0.000600 | 5/5 |
| `FLAG@s2.levels.1d.lo_fresh=False` | 0.7913 | 0.8420 | −0.05078 | [−0.09168, −0.00987] | 0.083200 | 5/5 |

**Read "12" with care — they are ~6 distinct effects.** Complementary levels are counted
as separate rows: `fill_class=r1`/`=re_entry` are one finding stated twice, as are
`zone=Z1`/`=Z3` and `stage=1`/`=2`; the three `mandate` levels are one three-way effect.
The distinct findings are: **fill class · zone depth · stage · mandate · vol-at-birth
(both atr measures) · one 1d-level freshness flag.**

**Collinearity that further compresses this** (measured on the 7,117 births):
`mandate ⟷ tf_exec ⟷ tf_gov` are exact aliases; `stage ≈ tier` at 99.79% (only 15 rows
separate them); and `atr_exec_bps`/`atr_gov_bps` are strongly mandate-stratified (median
intraday 15.27 / swing 34.77 / position 61.83 bps). **The vol-at-birth signal and the
mandate signal are substantially the same fact.**

### FDR-surviving but NOT candidate (3)

`symbol=BTCUSDT` (Δ −0.169252, q 0.000600), `symbol=SOLUSDT` (Δ +0.097320, q 0.000600),
`symbol=NEARUSDT` (Δ +0.064880, q 0.003343). All three fail the panel gate **structurally,
not empirically**: the panel test conditions on asset, so for the feature `symbol` the
indicator is constant inside every per-asset subset and the contrast is undefined. These
rows are marked `panel_applicable: false` with an explicit note rather than shown as a
failed replication. Asset composition differs sharply between W and L and that is a real
observation — it simply cannot be validated by a per-asset panel.

### Annex family (own FDR family, 11 tests)

**Zero FDR survivors.** Neither session-hour-UTC bucket nor day-of-week discriminates.
Session buckets: ASIA_00_07 / EU_08_12 / US_13_20 / LATE_21_23.

### s2 flags

39 boolean leaves exist on births; 27 vary across the resolved book; 6 rows are constant
across W∪L and carry no contrast (excluded from the FDR family and marked
`⚠︎NO-CONTRAST`). **Exactly one s2 flag reaches CANDIDATE**, at q = 0.0832 — the weakest
survivor in the table.

---

## 8 · TRG — TAIL-RETENTION GAUGE (the load-bearing result)

Filter = keep only trades carrying the winner-side value. TRG = share of the **unfiltered**
book's top-decile total R (3,035.949713) that survives.

| discriminant | filter | kept | Δexpectancy R | Δexpectancy net bps | top-decile kept | **TRG** |
|---|---|---|---|---|---|---|
| _(none — unfiltered)_ | keep all | 7,094 (100%) | 0.0000 | 0.0000 | 709/709 | **100.0%** |
| `atr_exec_bps` | ≥ 19.290675 (book median) | 3,547 (50.0%) | +0.0500 | +4.767 | 346/709 | **50.6%** |
| `atr_gov_bps` | ≥ 160.754176 (book median) | 3,547 (50.0%) | +0.0143 | +3.207 | 336/709 | **46.2%** |
| `fill_class=re_entry` | `!= re_entry` | 3,892 (54.9%) | +0.0137 | +3.620 | 441/709 | **39.7%** |
| `fill_class=r1` | `== r1` | 3,814 (53.8%) | +0.0177 | +4.871 | 435/709 | **39.6%** |
| `zone=Z3` | `!= Z3` | 5,198 (73.3%) | −0.0043 | +6.962 | 572/709 | **65.0%** |

**Every filter destroys more tail than book.** The `fill_class=r1` filter keeps 53.8% of
the book and 61.4% of the winners *by count* — yet only **39.6% of their R**. Mechanism,
verified independently:

| top-decile rows | n | sum R | mean R | max R |
|---|---|---|---|---|
| kept by `r1` | 435 | 1,202.79 | 2.765 | 97.70 |
| dropped | 274 | 1,833.16 | **6.690** | **193.46** |

The dropped winners are **2.4× larger on average** and carry **60.4% of the tail R from
38.6% of the tail count**. The tail is brutally concentrated — the top 100 trades hold
**71.0%** of the 3,035.95 R, and of the 25 largest winners the r1 filter drops 18 (954.5 R).
The single largest trade in the book (`ETHUSDT_swing c61t75`, R = 193.46) is
`fill_class=re_entry`, `zone=Z3` — **dropped by both categorical filters.**

**So `re_entry` is simultaneously the modal loser and the source of the largest winners.**
A discriminant can be entirely correct about central tendency and anti-correlated with the
extreme right tail. Buying +0.0177 R of expectancy costs 60% of the tail. This is exactly
the failure the TRG exists to expose, and it is the study's headline.

---

## 9 · SECTION B — OUTCOME ANATOMY (NOT CURTAIN-CLEAN, never a discriminant)

| quantity | W | L | book |
|---|---|---|---|
| median holding time | **128.48 h** | **0.083 h** (300 s) | 2.44 h |
| holding p25 / p75 | 257,460 / 795,720 s | 120 / 1,800 s | 1,440 / 56,745 s |
| median `give_back_r` | 6.4803 | 1.8068 | 1.7207 |
| median `funding_cum` (USD) | 0.2452 | 0.0000 | 0.0000 |
| median &#124;funding&#124;/&#124;pnl&#124; (dimensionless) | **0.0352** | 0.0000 | 0.0000 |

**exit_reason mix — near-deterministic, and a caveat on the whole design:**

| exit_reason | W n (share) | L n (share) | book n |
|---|---|---|---|
| stop | 0 (0) | **698 (0.9845)** | 4,995 |
| stop_gap | 0 (0) | 11 (0.0155) | 21 |
| opposite_cross | **447 (0.6305)** | 0 (0) | 719 |
| failure_x | 260 (0.3667) | 0 (0) | 1,352 |
| campaign_died | 1 (0.0014) | 0 (0) | 4 |
| v_reversal | 1 (0.0014) | 0 (0) | 3 |

**L is 709/709 stop-type; W is 0/709 stop-type.** Conditioning on the realized_r deciles is
very nearly conditioning on exit type. Every Section-A discriminant should be read as
"what predicts *being stopped out* versus *exiting on a cross*" — which is the honest
statement of what this study can support.

MFE/MAE at horizons (substrate, bps medians) — W and L are near-identical early and diverge
only late, consistent with the holding-time gap:

| horizon | MFE W | MFE L | MAE W | MAE L |
|---|---|---|---|---|
| h10 | 28.108 | 10.474 | −19.604 | −17.013 |
| h20 | 43.449 | 15.637 | −24.666 | −21.874 |
| h50 | 85.740 | 25.536 | −32.552 | −32.660 |
| h100 | 138.840 | 35.735 | −38.113 | −45.945 |
| exit | 1555.289 | 5.097 | −49.276 | −16.680 |

At h10–h50 the **MAE is essentially the same for winners and losers** — at h50 the losers'
drawdown is marginally *smaller*. Winners are not identifiable by early adverse excursion.

Funding per mandate: position W median 2.9682 USD / 10.2% of pnl; swing W 0.4376 / 4.7%;
intraday W 0.2192 / 3.1%.

---

## 10 · SECONDARY BOOKS

| book | n | decile | L cut | W cut | CANDIDATES |
|---|---|---|---|---|---|
| PRIMARY (all resolved, v included) | 7,094 | 709 | −0.852774 | 0.067318 | 12 |
| SECONDARY r1-only (contracted) | 3,814 | 381 | −0.641185 | 0.152609 | 20 |
| SENSITIVITY v-excluded (defect D3) | 7,016 | 701 | −0.854794 | 0.071533 | 11 |

---

## 11 · PREDICTIONS, SCORED HONESTLY

| id | stated | prediction (verbatim) | verdict |
|---|---|---|---|
| **P-WF1** | 70% | ">=1 s2 slow-stack flag is a CANDIDATE discriminant favouring W on >=3 panel assets." | **PREMISE-FALSE** |
| **P-WF2** | 65% | "fill_class=re_entry is over-represented in L with CI excluding zero." | **CONFIRMED** |
| **P-WF3** | 55% | "deep zones (Z1/Z2) over-represented in W with CI excluding zero." | **CONFIRMED** |
| **P-WF4** | 60% | "median holding time of W >= 5x that of L." | **CONFIRMED** |
| **P-WF5** | 50% | "median &#124;funding_cum&#124;/&#124;realized_r&#124; for W is < 10%." | **CONFIRMED** (on the corrected ratio) |

- **P-WF1 — premise false, not falsified.** No s2 leaf is a slow-stack flag. `s2` on births carries exactly two blocks: `det` (30m/1h detonation bits) and `levels` (4h/12h/1d pivot blocks) — 71 leaves, 39 boolean. The slow-stack construct (F1 = 1D aligned `e89 > e200`, F2 = 12H aligned, F4 = price beyond lens e89) is defined in `scripts/census_build.py` / `scripts/census_analyze.py` over the CENSUS **arming-anchor** table, a different artefact; grep for `slow.stack` returns 30 hits across CENSUS docs and **zero in `engine/`**. No e89/e200 value exists in the journals or the substrate. The prediction cannot be evaluated as written. Tested the whole s2 flag family in its place: 27 varying flags, **1 CANDIDATE** (`s2.levels.1d.lo_fresh`, q = 0.0832). Had "slow-stack" merely meant "some s2 flag", the prediction would still have failed the "≥3 panel assets" bar only barely — the one survivor is panel-consistent 5/5 but is the weakest row in the table.
- **P-WF3** — confirmed via Z1 (+0.20875, CI excludes zero). Z2 alone is **not** significant (Δ −0.00141, CI [−0.03385, +0.03244], q 0.9748); the "deep zone" effect is entirely Z1.
- **P-WF4** — confirmed overwhelmingly: ratio is **1,541.8×**, not 5×. But see §9 — this is close to a restatement of the exit-type split.
- **P-WF5** — see defect D4 below. On the literal mixed-unit expression the figure is 1.6118 (meaningless as a "%"); on the dimensionless twin it is **0.0352**, comfortably under the 10% bar, matching the prediction's evident intent.

---

## 12 · CONTRACT DEFECTS — handled and reported, never silently patched

**D1 · `engagement_flags` is post-fill.** Listed as a Section-A categorical; NULL on all
7,117 births. Rejected by F-WF2, demoted to Section B. *Fix applied: excluded from Section A.*

**D2 · "s2 slow-stack flag" does not exist** in these journals (see P-WF1). *Fix applied:
P-WF1 scored PREMISE-FALSE; full s2 flag family tested in its place.*

**D3 · The v-class instruction is self-contradictory.** The contract says `v=78` is
"EXCLUDED and counted", then says rank **ALL 7,094** resolved and take `floor(0.1*n)` = 709.
`floor(0.1 × 7094) = 709` only if v is **included**; excluding it gives n = 7,016 and a
decile of 701. *Resolution: the primary book follows the contract's own stated arithmetic
(all 7,094, v included, 709/709). The v-excluded book is computed and reported in full as
a sensitivity. Both are in the deliverables — the operator can rule either way without a
re-run.*

**D4 · P-WF5's ratio mixes units.** `funding_cum` is **USD**; `realized_r` is in **R**.
`|funding_cum|/|realized_r|` is USD/R and cannot be read as the "%" the prediction asserts.
*Resolution: both reported. The dimensionless twin `|funding_cum|/|pnl_usd|` (identically
`|funding_in_R|/|realized_r|`) is used for scoring, and the literal figure is retained in
the tables marked `⚠︎ MIXED UNITS`.*

**D5 · `concurrent_open_at_fill` is near-degenerate** — 7,099 zeros vs 18 ones (99.75%).
Retained in Section A per the contract and tested, but it cannot support inference; the 18
positives are structurally biased (all `fill_class=r1`, 16/18 `zone=Z3`). Marked
`⚠︎deg` in the tables.

---

## 13 · INDEPENDENT VERIFICATION

Four independent read-only auditors re-derived the study from raw, each instructed to
refute rather than confirm, none permitted to import or execute `wf1_forensics.py`.

**Every headline reproduced bit-for-bit.** C1 deciles, C2 population, C3 all eight point
estimates to 6 dp, C4 TRG (39.618254% and 46.218534%, exact), C5 holding times, C6 funding
ratio. All 20 per-cell checkpoints were validated field-by-field against a fresh raw
re-extraction (~180k comparisons): **0 diffs, 0 missing rows.** Published
`substrate_sha256` re-verifies. Boundary-tie, duplicate-key and unresolved-fill attacks all
failed to break anything.

**Defects the audit found in the machinery, which I then FIXED and re-ran:**

| defect | fix |
|---|---|
| **F-WF6 was a vacuous tautology** — the unfiltered row hardcoded `TRG_pct: 100.0` and then asserted it equalled 100.0, never calling `trg_for()`. The one quantity a reader most needs validated (the TRG denominator) was untested. | Now driven through `trg_for()` via a keep-all sentinel; asserts kept-count, top-decile count, retained R **and** Δexpectancy = 0. |
| **F-WF1d was tautological** — `len(W_rows) == 709` is always true for a fixed-length slice; no tie check was ever performed despite the transcript claiming "no boundary ties". | Now counts `r ≤ L_cut`, `r ≥ W_cut` and both cut multiplicities. |
| **F-WF2 and F-WF5 were unconditional `True`.** | F-WF2 now asserts birth-population and zero post-fill leakage; F-WF5 recomputes q by explicit formula and asserts equality with the reported value. |
| **Zero-information tests inflated the FDR family.** 6 Section-A rows are constant across W∪L; their bootstrap is identically zero and p forced to 1.0. They consumed BH slots, inflating every q by ×1.0769 (8 such rows in r1-only, ×1.1053). | No-contrast rows excluded from the family and marked `⚠︎NO-CONTRAST`. **m corrected 84 → 78; headline q corrected 0.000646 → 0.000600.** No FDR or CANDIDATE verdict flipped. |
| **TRG top-5 selection was a unit artefact** — ranking on `|point|` compared a proportion in [0,1] against a median delta in basis points, so `atr_*_bps` topped the table by unit convention regardless of effect size. | Ranking now uses the scale-free rank-biserial (2·AUC−1). The numerics still rank first, now on merit: `atr_exec_bps` +0.4715 vs `fill_class=re_entry` −0.4274. |
| **`symbol=*` panel rows were misleading** — rendered as `panel 0/5` / a row of `0.0000`, reading as a failed replication of a structurally impossible test. | Marked `panel_applicable: false` with an explicit note; shown as `n/a`. |
| **`WF1_full_rows.json` was misnamed** — it held discriminant tables, not the 7,117-row fill book. | Renamed `WF1_discriminant_tables.json`; the manifest now names the per-cell checkpoints as the row-level book. Stale file removed. |

---

## 14 · FINDINGS REPORTED, NOT FIXED

1. **`delta_expectancy_net_bps` is a single-trade artefact.** It is an unweighted mean of per-trade net bps. The book mean is +4.9238 bps but the **median is −64.54**; dropping the single largest trade (`SOLUSDT_swing c39t52`, 35,543.6 net bps) flips the mean to −0.0865. That trade is kept by all five filters, which is why every Δ-bps in the TRG table is positive. **For `zone != Z3` the R and bps columns disagree in sign** (ΔR −0.0043, Δbps +6.962). *Read the R column; treat the bps column as diagnostic only.* Not fixed because the contract explicitly requires "R AND net-of-toll bps" and changing the estimator to a median would silently depart from it. Recommend the operator rule on a median-based or notional-weighted bps statistic for future runs.
2. **The numeric TRG threshold is fragile.** `trg_for` splits at the **book** median. For `atr_gov_bps` the book median (160.754) sits *above* the winners' own median (153.395) — both extreme deciles lie below the book centre, so the relationship is non-monotone and the "winner-side" filter retains only 47.4% of the winner decile. Defensible alternatives span TRG **46%–77%** (`≥ median_L` → 76.57%, midpoint → 60.55%, `≥ median_W` → 47.15%, book median → 46.22%, the reported and worst case). *The reported figure is the most conservative; the operator should rule on the threshold convention.*
3. **`atr_gov_bps`'s TRG shortfall is a count effect, not tail destruction** — its kept vs dropped winners average 4.176 R vs 4.377 R, nearly identical. Only the `fill_class` rows demonstrate genuine tail destruction. `WF1_tables.md` presents them in one table without distinguishing the two mechanisms.
4. **q-values are upper bounds set by `BOOT_N`.** p is floored at 1/10,000; 13 Section-A tests sit exactly on that floor, and the headline q is `1e-4 × 78/13`. At BOOT_N = 100,000 the same tests would report q ≈ 6.5e-5. *Read q as a bound, not a point estimate.*
5. **Complementary levels are counted as independent FDR tests** (24 exact-complement pairs in Section A). The informationally distinct family is ~60, not 78. Correcting would *lower* q further; the current treatment is conservative.
6. **In-sample throughout.** Decile definition, the winner-side sign, and the median split point are all estimated on the same 7,094 rows. There is no holdout. No claim here is out-of-sample validated.
7. **Secondary books inherit the primary time split** rather than their own median. I re-checked both books under their own splits: `n_candidates` stays 20 and 11. No published number changes; the definition is inconsistent.
8. **Checkpoint resume is unvalidated** — `_reviewer_box/wf1/<cell>.json` is trusted whenever present, with no hash check against the source months. All 20 were externally validated this run (0 diffs), but a stale checkpoint would flow into every number with all fixtures still passing. Run with `--rebuild` to force re-extraction.
9. **`F-WF3` is a narrow determinism test** — it re-runs `analyse_family` in-process with a fresh `Boot` and compares 11 projected stat keys. It does not re-run extraction, panel/time, TRG or Section B. Passing means "the bootstrap is seeded", not "the study is end-to-end reproducible". Also, the `np.int16` index dtype makes the stream depend on dtype and numpy version, not the seed alone.
10. **`fill_class` is perfectly collinear with `evt`** (`ENTRY_FILL` = {r1, v}, `ADD_FILL` = {re_entry}) and with substrate `trigger_type`. It is one variable under three names.
11. **The W/L funding contrast is mechanical** — 643 of 709 L rows have `funding_cum` exactly 0 because the median L hold is 300 s (one 5m bar), crossing no funding tick. C6 restates the holding-time gap rather than adding independent evidence.
12. **One auditor disclosed** creating a zero-byte file `./x` in the repo root via a stray probe line and removing it immediately. I verified the tree: no such file exists, `git status` shows no trace.

---

## 15 · VERSIONS, HASHES, COMMITS

```
python            3.12.10   (C:/venvs/naiad/Scripts/python.exe)
numpy             2.1.3
branch            v12-v1-census
HEAD at start     4176f83cd1f5d2558b98878545eceb84db8898f1
script commit     a22a07a   "W-F1: winner forensics discriminant study"  (LOCAL, NOT PUSHED)
seed              20260803
bootstrap         10,000 resamples
FDR               Benjamini-Hochberg, q* = 0.10, m = 78 tested (Section A); annex m = 11
```

| artefact | sha256 | bytes |
|---|---|---|
| `exchange/reports/WF1_discriminants.json` | `06d2bcfd6498185db0f641614e3b7e8d21922758d369abe4b32846051e9e36b4` | 113,355 |
| `exchange/reports/WF1_tables.md` | `c6501ddb11289bf5d689acc54fc41ffeae0ccb4940f48b77848919c3ea127025` | 29,660 |
| `exchange/reports/SS_Reassessment_Synthesis_2026-08-03.md` | `9d6e7ea747544561af509bbcc845648fa66367cae8157feec1916b18ab4cbff1` | 8,282 |
| `exchange/queue/2026-08-03_WF1_winner_forensics_APOLLO.md` | `a08e36ad96c68948ed10f691d5003e2c6ba339daf6aff8c672be3b85160c8ea0` | 3,934 |
| `scripts/wf1_forensics.py` | `2efb7752ba80dfac828e02d3bc74852878b3eefb639c7fc756d9705fd2f7348f` | 57,846 |
| `_reviewer_box/wf1/WF1_discriminant_tables.json` | `2810774b9c034e2b63f795a55517ff549911cf1ee2e0554fafa2a2e1d0d241e7` | 251,486 |
| `s3_excursion_substrate.jsonl` (input) | `a2cf6f2739e3a2ee6fc3fae05ed12ba6082e64b918ecf69b89dded363652b954` | — |

`WF1_discriminants.json` is **113 KB, within the 1 MB contract ceiling.** Big intermediates
stay in `_reviewer_box/wf1/` and are referenced by path + sha in the JSON manifest.

---

## 16 · FILE DISPOSITION

| path | exists | tracked / untracked / ignored + rule | committed sha | pushed + ref | protected by |
|---|---|---|---|---|---|
| `exchange/queue/2026-08-03_WF1_winner_forensics_APOLLO.md` | yes | tracked | see §17 | yes → `origin/v12-v1-census` | GitHub |
| `exchange/reports/WF1_discriminants.json` | yes | tracked | see §17 | yes → `origin/v12-v1-census` | GitHub |
| `exchange/reports/WF1_tables.md` | yes | tracked | see §17 | yes → `origin/v12-v1-census` | GitHub |
| `exchange/reports/BUILDERS_REPORT_APOLLO_2026-08-03_WF1.md` | yes | tracked | see §17 | yes → `origin/v12-v1-census` | GitHub |
| `exchange/reports/SS_Reassessment_Synthesis_2026-08-03.md` | yes | tracked | see §17 | yes → `origin/v12-v1-census` | GitHub |
| `scripts/wf1_forensics.py` | yes | tracked | **`a22a07a`** | **NO — commit-no-push per contract** | local git only |
| `_reviewer_box/wf1/*.json` (20 per-cell checkpoints) | yes | ignored — `.gitignore:80 _reviewer_box/` | — | no | local disk; regenerable via `--rebuild` |
| `_reviewer_box/wf1/WF1_discriminant_tables.json` | yes | ignored — `.gitignore:80 _reviewer_box/` | — | no | local disk; sha in the JSON manifest |
| `research_outputs/_unarchived/s3_2026-07-27/journal_s3/scored/` (753 files) | yes | ignored — `.gitignore:101 research_outputs/_unarchived/**` | — | no | the phase archive `research_outputs/_archive/s3_2026-07-27.zip` |
| `s3_excursion_substrate.jsonl` | yes | tracked (read-only input, unmodified) | pre-existing | pre-existing | GitHub |
| `.gitignore` | yes | tracked, **modified & uncommitted** (ATHENA restore rule) | — | no — outside `exchange/**` publish scope | working tree only |

`.gitignore` carries the `research_outputs/_unarchived/**` rule added during the ATHENA
restore. It is deliberately left unstaged: `publish_exchange.guard()` checks **all** staged
paths against `exchange/**` and would FLAG the publish, reset the index and skip the push.
It needs a separate decision from the operator.

---

## 17 · PUBLISH RESULT

See the closing section of this run's console output. The publish commit sha and push status
are stated there and in the operator hand-off.
