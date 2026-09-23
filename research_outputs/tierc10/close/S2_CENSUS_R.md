## 2 · CENSUS-R

**Tier-E · A SELECTION, not a result · m logged**

- **Digest of record:** `research_outputs/tierc10/census/CENSUS_R_DIGEST.md` · sha256 `281e61639ad6dcb41ee088e9959191feeb02ebfe6b9eaabbb5ed2398fe600dc8` · 206,251 B · 1,896 lines. Every block labelled *verbatim* is that file's own bytes at the line span its label names — selected by heading span, never retyped — and F-S2-SLICE checks each one byte for byte (`research_outputs/tierc10/close/FIXTURES_CLOSE_census_r.txt`).
- **As of** 2026-09-21T16:00:00Z (`research_outputs/tierc10/data/AS_OF_PIN.json`) · substrate `tc10_20260921` · built by `scripts/tierc10_close_close_census_r.py` from filed artifacts only. TIER-E, REPORT-ONLY: nothing below is scored, nothing gates anything, and no registration or verdict is read.
- **The one thing here that is not in the digest:** the *null beside* tables in 2.3. The null stage pooled POOLED:ALL only (`null/<variant>/build_manifest.json` → `commission.pooled`), so the digest prints no null beside its POOLED:CLASSIC5 / POOLED:UNSEEN12 blocks. They are computed here from the filed per-cell null ledgers by the null build's own pooling path (`tierc10_census.grid_rows` per draw, then `tierc10_null.summarise`); F-S2-NULL-ANCHOR proves that path reproduces the filed POOLED:ALL null summary exactly, and that its REAL draw is the census's own sub-pool outcome row.
- **m logged**, read from each table's `m_looks_this_table` (no multiplicity correction; nothing here is a test): acceptance_head_to_head m = 60 · height_toll_verdict m = 6 · outcome_grid m = 7,920 · coverage m = 102 · spring_overlap m = 204 · null_summary (gaps+order) m = 21,384 · null_summary (gaps-only) m = 21,384. This selection adds 448 close-time null cells (112 class rows × 2 horizons × 2 variants).
- **SIZE:** 64,492 B · FLAG_BYTES 64,000 B · BOX_BYTES 16,000,000 B (both read by `ast.literal_eval` from `scripts/publish_exchange.py`) · FLAG: **YES** — over the naming trip-wire: named to the operator at creation, with its intended home (`research_outputs/tierc10/close/`, spliced into the build document's §2 at CLOSE); naming only, never a refusal (`scripts/publish_exchange.py`, the FLAG_BYTES comment).

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L3–L4 + L9–L14*

**TIER-E MEASUREMENT — UNSCORED, GATES NOTHING.** NOTHING — TIER-E MEASUREMENT ONLY. No registration rests on this row, none is implied, and no cell of this grid may be promoted.

- WARRANTY: these numbers are true AS OF the bars named in this row and of no other; the corridor advances with the cache [TC6V-a, carried by TIER-C10]. Pins were calibrated on BTC only (micro 1D/420, v2 4h/1700): every other asset and lens is an extrapolation of frozen pins, FULL history, not the Oracle's 1700-bar window.

> P-BRK-S1 IS SCORED ON THE 5m RETEST-HOLD CLASSES IN THE HOLDOUT ERA. Those rows are FILED in the parquet and are NOT printed, summarised or quoted in any digest, log line or report field: a registration's text is filed before its result is seen. Only the TUNING-era 5m retest-hold rows are printed. Every other class and lens prints full history, as the contract orders.

> era = the ANCHOR bar's close: 'tuning' <= 2024-06-30T23:59:59Z, 'holdout' after it (an anchor beyond the tape's end has no close and is holdout by construction — the tape ends in 2026). 'ALL' = the full-history row the contract orders, filed beside the two era rows, never their sum.

### 2.1 · THE ACCEPTANCE HEAD-TO-HEAD [Q-R4] — digest §A (L32–L183)

The ruling and the no-promotion clause; the three full-history H20 tables (POOLED:ALL · frozen3.0), each with the data's default named under it; the tuning and holdout H20 defaults; the H100 defaults and the digest's own reading. `promoted` reads “NOTHING — the data's default is NAMED; no pin moves [Q-R4]” and `engine_default_after` reads “BREAK_CONFIRM_N=8 · BREAK_MARGIN=1.5 — UNCHANGED” on all 3,600 rows of `research_outputs/tierc10/census/acceptance_head_to_head.parquet` (F-S2-PROMOTE). Left in the digest: L38–L53 · L67–L75 · L79–L87 · L103–L111 · L115–L123 · L139–L147 · L151–L159.

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L34–L37*

> LEDGER.md:835 — *"Q-R4 ACCEPTANCE DEFINITION: (a) — the census measures four candidate operationalisations head-to-head (2-close / 3-close / 6-outside-close stale-run / time-beyond); the engine default is chosen FROM DATA."*

**THE DATA'S DEFAULT IS NAMED BELOW AND NOTHING IS PROMOTED.** NOTHING. Q-R4 NAMES the data's default and moves no pin; the engine default stays BREAK_CONFIRM_N=8 / BREAK_MARGIN=1.5. This table is TIER-E MEASUREMENT — UNSCORED, GATES NOTHING.

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L55–L66 + L77–L78 + L89–L90*

**5m · POOLED:ALL · frozen3.0 · era ALL · H20** (n_episodes = 76,812)

| rule | declared | declare rate | precision (died) | lead vs DIE (bars, median) | median term | toll | NET | hit rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2-close | 47,623 | 0.6200 | 0.5567 | 1.0 | -0.3164 | 0.4415 | **-0.7579** | 0.4072 |
| 3-close | 30,267 | 0.3940 | 0.6084 | 1.0 | -0.3284 | 0.4296 | **-0.7580** | 0.4006 |
| 6-outside-close-stale-run | 8,791 | 0.1144 | 0.7671 | 2.0 | -0.2594 | 0.4160 | **-0.6754** | 0.4094 |
| time-beyond | 11,909 | 0.1550 | 0.6587 | 1.0 | -0.2913 | 0.4265 | **-0.7178** | 0.4032 |
| RangeFinder-DIE | 32,733 | 0.4261 | 1.0000 | 0.0 | -0.3991 | 0.4205 | **-0.8196** | 0.4009 |

> THE DATA'S DEFAULT AT 5m / ALL / H20: **6-outside-close-stale-run** (NET -0.6754 ATR on n = 8,791). **EVERY ONE OF THE FIVE IS NET NEGATIVE HERE — this names the least-bad loser, not a winner, and nothing here supports trading this lens.** NAMED ONLY: no pin moves and the engine default is unchanged.

> THE DATA'S DEFAULT AT 5m / tuning / H20: **6-outside-close-stale-run** (NET -0.6435 ATR on n = 4,636). **EVERY ONE OF THE FIVE IS NET NEGATIVE HERE — this names the least-bad loser, not a winner, and nothing here supports trading this lens.** NAMED ONLY: no pin moves and the engine default is unchanged.

> THE DATA'S DEFAULT AT 5m / holdout / H20: **6-outside-close-stale-run** (NET -0.7775 ATR on n = 4,155). **EVERY ONE OF THE FIVE IS NET NEGATIVE HERE — this names the least-bad loser, not a winner, and nothing here supports trading this lens.** NAMED ONLY: no pin moves and the engine default is unchanged.

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L91–L102 + L113–L114 + L125–L126*

**4h · POOLED:ALL · frozen3.0 · era ALL · H20** (n_episodes = 1,482)

| rule | declared | declare rate | precision (died) | lead vs DIE (bars, median) | median term | toll | NET | hit rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2-close | 957 | 0.6457 | 0.6134 | 2.0 | +0.0004 | 0.0625 | **-0.0621** | 0.4932 |
| 3-close | 668 | 0.4507 | 0.6527 | 2.0 | -0.0791 | 0.0631 | **-0.1422** | 0.4774 |
| 6-outside-close-stale-run | 224 | 0.1511 | 0.7812 | 2.0 | -0.1774 | 0.0615 | **-0.2389** | 0.4777 |
| time-beyond | 270 | 0.1822 | 0.7222 | 1.0 | -0.0745 | 0.0563 | **-0.1308** | 0.4778 |
| RangeFinder-DIE | 706 | 0.4764 | 1.0000 | 0.0 | +0.1085 | 0.0627 | **+0.0459** | 0.5108 |

> THE DATA'S DEFAULT AT 4h / ALL / H20: **RangeFinder-DIE** (NET +0.0459 ATR on n = 706). NAMED ONLY: no pin moves and the engine default is unchanged.

> THE DATA'S DEFAULT AT 4h / tuning / H20: **6-outside-close-stale-run** (NET +0.3279 ATR on n = 127). NAMED ONLY: no pin moves and the engine default is unchanged.

> THE DATA'S DEFAULT AT 4h / holdout / H20: **RangeFinder-DIE** (NET -0.1954 ATR on n = 326). **EVERY ONE OF THE FIVE IS NET NEGATIVE HERE — this names the least-bad loser, not a winner, and nothing here supports trading this lens.** NAMED ONLY: no pin moves and the engine default is unchanged.

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L127–L138 + L149–L150 + L161–L162*

**1d · POOLED:ALL · frozen3.0 · era ALL · H20** (n_episodes = 234)

| rule | declared | declare rate | precision (died) | lead vs DIE (bars, median) | median term | toll | NET | hit rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2-close | 150 | 0.6410 | 0.6133 | 2.0 | +0.3051 | 0.0242 | **+0.2809** | 0.5510 |
| 3-close | 98 | 0.4188 | 0.6735 | 2.0 | +0.2311 | 0.0291 | **+0.2020** | 0.5417 |
| 6-outside-close-stale-run | 38 | 0.1624 | 0.8158 | 2.0 | +0.6234 | 0.0241 | **+0.5993** | 0.5526 |
| time-beyond | 40 | 0.1709 | 0.7750 | 1.0 | +0.7726 | 0.0234 | **+0.7492** | 0.6154 |
| RangeFinder-DIE | 116 | 0.4957 | 1.0000 | 0.0 | +0.2347 | 0.0252 | **+0.2094** | 0.5351 |

> THE DATA'S DEFAULT AT 1d / ALL / H20: **time-beyond** (NET +0.7492 ATR on n = 40). NAMED ONLY: no pin moves and the engine default is unchanged.

> THE DATA'S DEFAULT AT 1d / tuning / H20: **6-outside-close-stale-run** (NET +0.8690 ATR on n = 16 — **PROVISIONAL**: n_declared 16 < PROVISIONAL_MIN_N (30); n_outcome 16 < PROVISIONAL_MIN_N (30) [census lean C-g]). NAMED ONLY: no pin moves and the engine default is unchanged.

> THE DATA'S DEFAULT AT 1d / holdout / H20: **time-beyond** (NET +1.1173 ATR on n = 21 — **PROVISIONAL**: n_declared 21 < PROVISIONAL_MIN_N (30); n_outcome 20 < PROVISIONAL_MIN_N (30) [census lean C-g]). NAMED ONLY: no pin moves and the engine default is unchanged.

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L163–L183*

**THE DATA'S DEFAULT AT H100** — the same law, the longer horizon, so the claim 'named per lens AND HORIZON' is true of the digest and not only of the parquet. `provisional` is the same lean C-g flag as above.

| lens | era | default rule | NET (H100) | n declared | provisional | all five NET negative? |
|---|---|---|---:|---:|---|---|
| 5m | ALL | **6-outside-close-stale-run** | -0.767752 | 8,791 | no | **YES** |
| 5m | tuning | **6-outside-close-stale-run** | -0.762992 | 4,636 | no | **YES** |
| 5m | holdout | **6-outside-close-stale-run** | -0.823169 | 4,155 | no | **YES** |
| 4h | ALL | **time-beyond** | +0.922898 | 270 | no | no |
| 4h | tuning | **time-beyond** | +1.332671 | 143 | no | no |
| 4h | holdout | **time-beyond** | +0.280114 | 127 | no | no |
| 1d | ALL | **6-outside-close-stale-run** | +1.390168 | 38 | no | no |
| 1d | tuning | **6-outside-close-stale-run** | +1.426973 | 16 | **YES** | no |
| 1d | holdout | **time-beyond** | +1.504314 | 21 | **YES** | no |

**WHAT THE HEAD-TO-HEAD ACTUALLY SHOWS.** The close-count axis barely binds: the RangeFinder dies on the 1.5-ATR MARGIN, not on its 8-close pin, in
- **1d**: margin 95 (81.9%) vs n_closes 21 (18.1%) of 116 deaths
- **4h**: margin 582 (82.4%) vs n_closes 124 (17.6%) of 706 deaths
- **5m**: margin 28,528 (87.2%) vs n_closes 4,205 (12.8%) of 32,733 deaths

So BREAK_CONFIRM_N = 8 is very nearly a dead letter at these pins, and the four candidate operationalisations are mostly re-cutting a decision the MARGIN has already made. Precision rises monotonically with strictness (2-close is the loosest and least precise; the stale-run the strictest and most precise), and the later, stricter rules take the better NET in most cells — but this is a DIRECTION the data leans, not a mandate, and it is not promoted.

### 2.2 · HEIGHT-vs-TOLL [Q-R3] — digest §B (L184–L732), the POOLED verdict rows of B.3

The gate: the ruling, the two legs, their conjunction and the sample floor. Then, out of B.3's whole grid of 360 filed rows, the 54 POOLED rows (every pool × lens × scale kind × era — the verdict is keyed on the era, so every era is shown). F-S2-PARQUET checks every printed `verdict_pass`, `ratio_median` and `edge_net_h20` against `research_outputs/tierc10/census/height_toll_verdict.parquet` (54 POOLED keys there) on (lens, scale_kind, asset, era). Left in the digest: L188–L191 · L193 · L196–L244 · L247–L321 · L327–L359 · L369–L419 · L429–L479 · L489–L539 · L549–L599 · L609–L659 · L669–L731.

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L186–L187 + L192–L192 + L194–L195 + L246–L246*

> LEDGER.md:834 — *"Q-R3 PLAYBOOK-R TIMING: (a) — detection and gating first; a range-trading contract is drafted ONLY IF the height-vs-toll feasibility gate AND the edge-fade outcome leg both pass."*

- **THE HEIGHT GATE** — PASS iff n_ranges >= 30 AND median(ratio) >= 3.0 AND share(ratio < 1) <= 0.1.
- **THE EDGE-FADE LEG** — [LEAN-HEPHAESTUS R3-b] PASS iff trading TOWARD THE FAR BOUNDARY from the NEAR 20% of the range is NET POSITIVE at H20, pooled over the lens, WITHIN THE ROW'S OWN ERA: net = median(term) - toll_atr > 0, AND the sample clears the floor (edge_n_ranges >= 30, edge_n >= 30) IN THAT ERA. The near edge is where a range trade is actually taken; if the edge is not there it is nowhere.
- **THE CONJUNCTION** — LEDGER.md:834 — 'a range-trading contract is drafted ONLY IF the height-vs-toll feasibility gate AND the edge-fade outcome leg both pass'. verdict_pass = gate_height_pass AND gate_edge_fade_pass.
- **THE SAMPLE FLOOR** — BOTH legs carry a SAMPLE FLOOR: gate_height needs n_ranges >= 30, gate_edge_fade needs edge_n_ranges >= 30 confirmed ranges AND edge_n >= 30 in-range entries.

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L323–L326 + L360–L368 + L420–L428 + L480–L488 + L540–L548 + L600–L608 + L660–L668*

**THE WHOLE GRID, ROW BY ROW, EVERY ERA.** `prov` = provisional under lean C-g, applied WITHIN the era. A PROVISIONAL row is FILED and readable as data and is REFUSED by `height_vs_toll_verdict()` unless the caller passes `allow_provisional=True`. The reader takes the era as an argument — `height_vs_toll_verdict(lens, asset=…, scale_kind=…, era=…)` — and the dict it returns states the era it was judged on in `era` and `era_judged`.

| lens | scale | asset | **era** | n ranges | ratio median | share<1 | HEIGHT | edge n | edge ranges | edge median term | toll | edge NET (H20) | EDGE-FADE | prov | **VERDICT** |
|---|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---|---|
| 1d | calibrated | POOLED:ALL | ALL | 221 | 316.49 | 0 | PASS | 3,716 | 210 | -0.1370 | 0.0274 | -0.1644 | FAIL | no | **FAIL** |
| 1d | calibrated | POOLED:ALL | tuning | 122 | 326.19 | 0 | PASS | 1,766 | 116 | +0.0739 | 0.0249 | +0.0490 | PASS | no | **PASS** |
| 1d | calibrated | POOLED:ALL | holdout | 99 | 302.45 | 0 | PASS | 1,950 | 103 | -0.3910 | 0.0315 | -0.4225 | FAIL | no | **FAIL** |
| 1d | calibrated | POOLED:CLASSIC5 | ALL | 91 | 319.56 | 0 | PASS | 1,258 | 87 | -0.1748 | 0.0274 | -0.2022 | FAIL | no | **FAIL** |
| 1d | calibrated | POOLED:CLASSIC5 | tuning | 58 | 342.89 | 0 | PASS | 766 | 56 | +0.0718 | 0.0249 | +0.0469 | PASS | no | **PASS** |
| 1d | calibrated | POOLED:CLASSIC5 | holdout | 33 | 276.26 | 0 | PASS | 492 | 35 | -0.6630 | 0.0315 | -0.6945 | FAIL | no | **FAIL** |
| 1d | calibrated | POOLED:UNSEEN12 | ALL | 130 | 314.59 | 0 | PASS | 2,458 | 123 | -0.1210 | 0.0265 | -0.1475 | FAIL | no | **FAIL** |
| 1d | calibrated | POOLED:UNSEEN12 | tuning | 64 | 318.23 | 0 | PASS | 1,000 | 60 | +0.0795 | 0.0238 | +0.0557 | PASS | no | **PASS** |
| 1d | calibrated | POOLED:UNSEEN12 | holdout | 66 | 308.51 | 0 | PASS | 1,458 | 68 | -0.2851 | 0.0304 | -0.3155 | FAIL | no | **FAIL** |
| 1d | frozen3.0 | POOLED:ALL | ALL | 121 | 436.87 | 0 | PASS | 3,855 | 118 | -0.0960 | 0.0248 | -0.1208 | FAIL | no | **FAIL** |
| 1d | frozen3.0 | POOLED:ALL | tuning | 70 | 446.25 | 0 | PASS | 1,773 | 69 | +0.0590 | 0.0221 | +0.0369 | PASS | no | **PASS** |
| 1d | frozen3.0 | POOLED:ALL | holdout | 51 | 426.34 | 0 | PASS | 2,082 | 56 | -0.2815 | 0.0304 | -0.3118 | FAIL | no | **FAIL** |
| 1d | frozen3.0 | POOLED:CLASSIC5 | ALL | 53 | 413.99 | 0 | PASS | 1,423 | 52 | +0.0689 | 0.0248 | +0.0441 | PASS | no | **PASS** |
| 1d | frozen3.0 | POOLED:CLASSIC5 | tuning | 35 | 413.99 | 0 | PASS | 982 | 35 | +0.1758 | 0.0221 | +0.1537 | PASS | no | **PASS** |
| 1d | frozen3.0 | POOLED:CLASSIC5 | holdout | 18 | 459.33 | 0 | FAIL | 441 | 21 | -0.4057 | 0.0304 | -0.4360 | FAIL | **YES** | **FAIL** |
| 1d | frozen3.0 | POOLED:UNSEEN12 | ALL | 68 | 499.89 | 0 | PASS | 2,432 | 66 | -0.2079 | 0.0242 | -0.2320 | FAIL | no | **FAIL** |
| 1d | frozen3.0 | POOLED:UNSEEN12 | tuning | 35 | 512.44 | 0 | PASS | 791 | 34 | -0.1204 | 0.0202 | -0.1405 | FAIL | no | **FAIL** |
| 1d | frozen3.0 | POOLED:UNSEEN12 | holdout | 33 | 426.34 | 0 | PASS | 1,641 | 35 | -0.2689 | 0.0302 | -0.2992 | FAIL | no | **FAIL** |
| 4h | calibrated | POOLED:ALL | ALL | 1,341 | 115.04 | 0 | PASS | 24,785 | 1,294 | -0.0629 | 0.0676 | -0.1305 | FAIL | no | **FAIL** |
| 4h | calibrated | POOLED:ALL | tuning | 757 | 112.96 | 0 | PASS | 14,694 | 730 | -0.0927 | 0.0599 | -0.1526 | FAIL | no | **FAIL** |
| 4h | calibrated | POOLED:ALL | holdout | 584 | 115.84 | 0 | PASS | 10,091 | 573 | -0.0241 | 0.0824 | -0.1065 | FAIL | no | **FAIL** |
| 4h | calibrated | POOLED:CLASSIC5 | ALL | 517 | 115.23 | 0 | PASS | 8,930 | 499 | -0.1535 | 0.0676 | -0.2211 | FAIL | no | **FAIL** |
| 4h | calibrated | POOLED:CLASSIC5 | tuning | 335 | 119.54 | 0 | PASS | 6,139 | 325 | -0.2045 | 0.0599 | -0.2644 | FAIL | no | **FAIL** |
| 4h | calibrated | POOLED:CLASSIC5 | holdout | 182 | 107.38 | 0 | PASS | 2,791 | 177 | -0.0241 | 0.0824 | -0.1065 | FAIL | no | **FAIL** |
| 4h | calibrated | POOLED:UNSEEN12 | ALL | 824 | 114.87 | 0 | PASS | 15,855 | 795 | -0.0131 | 0.0587 | -0.0718 | FAIL | no | **FAIL** |
| 4h | calibrated | POOLED:UNSEEN12 | tuning | 422 | 109.27 | 0 | PASS | 8,555 | 405 | -0.0080 | 0.0552 | -0.0633 | FAIL | no | **FAIL** |
| 4h | calibrated | POOLED:UNSEEN12 | holdout | 402 | 119.42 | 0 | PASS | 7,300 | 396 | -0.0247 | 0.0725 | -0.0972 | FAIL | no | **FAIL** |
| 4h | frozen3.0 | POOLED:ALL | ALL | 709 | 184.38 | 0 | PASS | 21,902 | 696 | -0.0689 | 0.0665 | -0.1353 | FAIL | no | **FAIL** |
| 4h | frozen3.0 | POOLED:ALL | tuning | 386 | 180.89 | 0 | PASS | 12,729 | 380 | -0.0907 | 0.0586 | -0.1492 | FAIL | no | **FAIL** |
| 4h | frozen3.0 | POOLED:ALL | holdout | 323 | 189.00 | 0 | PASS | 9,173 | 322 | -0.0423 | 0.0880 | -0.1303 | FAIL | no | **FAIL** |
| 4h | frozen3.0 | POOLED:CLASSIC5 | ALL | 298 | 169.50 | 0 | PASS | 7,430 | 291 | -0.1592 | 0.0665 | -0.2257 | FAIL | no | **FAIL** |
| 4h | frozen3.0 | POOLED:CLASSIC5 | tuning | 196 | 169.50 | 0 | PASS | 5,075 | 190 | -0.2760 | 0.0582 | -0.3341 | FAIL | no | **FAIL** |
| 4h | frozen3.0 | POOLED:CLASSIC5 | holdout | 102 | 172.38 | 0 | PASS | 2,355 | 103 | +0.0942 | 0.0880 | +0.0062 | PASS | no | **PASS** |
| 4h | frozen3.0 | POOLED:UNSEEN12 | ALL | 411 | 203.30 | 0 | PASS | 14,472 | 405 | -0.0223 | 0.0614 | -0.0837 | FAIL | no | **FAIL** |
| 4h | frozen3.0 | POOLED:UNSEEN12 | tuning | 190 | 212.46 | 0 | PASS | 7,654 | 190 | +0.0211 | 0.0586 | -0.0375 | FAIL | no | **FAIL** |
| 4h | frozen3.0 | POOLED:UNSEEN12 | holdout | 221 | 202.92 | 0 | PASS | 6,818 | 219 | -0.0677 | 0.0682 | -0.1359 | FAIL | no | **FAIL** |
| 5m | calibrated | POOLED:ALL | ALL | 65,366 | 14.56 | 0.00039776 | PASS | 1,243,785 | 63,557 | +0.1784 | 0.5591 | -0.3807 | FAIL | no | **FAIL** |
| 5m | calibrated | POOLED:ALL | tuning | 35,681 | 14.90 | 0.00056052 | PASS | 690,108 | 34,661 | +0.2203 | 0.4875 | -0.2671 | FAIL | no | **FAIL** |
| 5m | calibrated | POOLED:ALL | holdout | 29,685 | 14.18 | 0.00020212 | PASS | 553,677 | 28,899 | +0.1236 | 0.7133 | -0.5897 | FAIL | no | **FAIL** |
| 5m | calibrated | POOLED:CLASSIC5 | ALL | 26,008 | 13.80 | 0.00080744 | PASS | 479,728 | 25,243 | +0.1819 | 0.5591 | -0.3772 | FAIL | no | **FAIL** |
| 5m | calibrated | POOLED:CLASSIC5 | tuning | 16,503 | 14.78 | 0.00103012 | PASS | 309,629 | 16,013 | +0.2257 | 0.4875 | -0.2618 | FAIL | no | **FAIL** |
| 5m | calibrated | POOLED:CLASSIC5 | holdout | 9,505 | 12.25 | 0.00042083 | PASS | 170,099 | 9,231 | +0.0985 | 0.7133 | -0.6148 | FAIL | no | **FAIL** |
| 5m | calibrated | POOLED:UNSEEN12 | ALL | 39,358 | 15.03 | 0.00012704 | PASS | 764,057 | 38,314 | +0.1762 | 0.4777 | -0.3015 | FAIL | no | **FAIL** |
| 5m | calibrated | POOLED:UNSEEN12 | tuning | 19,178 | 14.97 | 0.00015643 | PASS | 380,479 | 18,648 | +0.2158 | 0.4211 | -0.2053 | FAIL | no | **FAIL** |
| 5m | calibrated | POOLED:UNSEEN12 | holdout | 20,180 | 15.09 | 9.911e-05 | PASS | 383,578 | 19,668 | +0.1336 | 0.6351 | -0.5015 | FAIL | no | **FAIL** |
| 5m | frozen3.0 | POOLED:ALL | ALL | 32,738 | 24.27 | 3.055e-05 | PASS | 999,378 | 32,546 | +0.1774 | 0.5411 | -0.3637 | FAIL | no | **FAIL** |
| 5m | frozen3.0 | POOLED:ALL | tuning | 17,987 | 24.97 | 0 | PASS | 546,878 | 17,869 | +0.2158 | 0.4656 | -0.2498 | FAIL | no | **FAIL** |
| 5m | frozen3.0 | POOLED:ALL | holdout | 14,751 | 23.54 | 6.779e-05 | PASS | 452,500 | 14,678 | +0.1308 | 0.7034 | -0.5725 | FAIL | no | **FAIL** |
| 5m | frozen3.0 | POOLED:CLASSIC5 | ALL | 13,025 | 23.26 | 7.678e-05 | PASS | 376,297 | 12,929 | +0.1671 | 0.5411 | -0.3740 | FAIL | no | **FAIL** |
| 5m | frozen3.0 | POOLED:CLASSIC5 | tuning | 8,441 | 24.93 | 0 | PASS | 239,620 | 8,382 | +0.1968 | 0.4656 | -0.2688 | FAIL | no | **FAIL** |
| 5m | frozen3.0 | POOLED:CLASSIC5 | holdout | 4,584 | 20.67 | 0.00021815 | PASS | 136,677 | 4,548 | +0.1149 | 0.7034 | -0.5885 | FAIL | no | **FAIL** |
| 5m | frozen3.0 | POOLED:UNSEEN12 | ALL | 19,713 | 24.95 | 0 | PASS | 623,081 | 19,617 | +0.1843 | 0.4863 | -0.3020 | FAIL | no | **FAIL** |
| 5m | frozen3.0 | POOLED:UNSEEN12 | tuning | 9,546 | 25.00 | 0 | PASS | 307,258 | 9,487 | +0.2302 | 0.4221 | -0.1919 | FAIL | no | **FAIL** |
| 5m | frozen3.0 | POOLED:UNSEEN12 | holdout | 10,167 | 24.92 | 0 | PASS | 315,823 | 10,130 | +0.1370 | 0.6408 | -0.5038 | FAIL | no | **FAIL** |

### 2.3 · OUTCOME AFTER EVENT — digest §5 (L1045–L1858), POOLED:CLASSIC5 and POOLED:UNSEEN12, beside their nulls

The method and the two filed null variants; then 12 blocks — POOLED:CLASSIC5 beside POOLED:UNSEEN12, frozen3.0, eras ALL and holdout, every lens — each followed by its own pooled null, gaps+order (the null of record) first. Left in the digest: the other 42 blocks of §5 (POOLED:ALL with its filed null, the tuning era, the calibrated SCALE) and its closing note.

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L1047–L1051*

Term / MFE / MAE are measured in ATR from the CLOSE of the bar the event is KNOWN at (`known_at`), over H bars OF THE LENS, CENSORED and never shortened [L4]. NET = median term - the row's measured toll; a pooled row quotes the BINDING (max) per-asset toll [C-f]. The null's `median [q25, q75]` is across K draws and `pct` is the mid-rank percentile of the real value among them — a DESCRIPTION of where the real number sits, NEVER a p-value. `n<30` flags the lineage's provisional floor.

- null variant `gaps-only`: 21,384 summary rows filed at `research_outputs/tierc10/null/gaps_only/`
- null variant `gaps+order`: 21,384 summary rows filed at `research_outputs/tierc10/null/gaps_order/`

The null of record, from `research_outputs/tierc10/OPERATOR_RULINGS.md` §R10 (L125–L138):

*Tier-E · report-only · verbatim from `OPERATOR_RULINGS.md` · L127–L131 + L137–L137*

**Ruled: "gaps+order — the leak-reduced one."**

- `gaps+order` is the null of record. It cuts the measured own-window overlap from **25.62% to
  7.97%** over 1,020 draws, so the foil is fairer.
- `gaps-only` — the contract-literal design — remains **filed and printed beside it**, never deleted.
- **K=20 resolves a percentile to 5 points at best. It is a DESCRIPTION, never a p-value.**

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L1321–L1331*

### POOLED:CLASSIC5 · 5m · frozen3.0 · era `ALL`

| class | n H20 | med H20 | toll | **NET H20** | n H100 | med H100 | **NET H100** | flags |
|---|---|---|---|---|---|---|---|---|
| breach | 29,755 | -0.294 | 0.464 | **-0.758** | 29,749 | -0.413 | **-0.877** |  |
| harden | 16,732 | +0.162 | 0.460 | **-0.298** | 16,730 | +0.274 | **-0.187** |  |
| DIE | 13,023 | -0.389 | 0.420 | **-0.810** | 13,019 | -0.461 | **-0.882** |  |
| memory-touch-v1 | 25,599 | +0.003 | 0.365 | **-0.362** | 25,591 | -0.025 | **-0.390** |  |
| memory-touch-2s | 17,051 | +0.116 | 0.398 | **-0.282** | 17,048 | -0.083 | **-0.481** |  |
| flip-hold | 10,793 | -0.121 | 0.392 | **-0.513** | 10,790 | -0.168 | **-0.560** |  |

*Tier-E · report-only · COMPUTED AT CLOSE, not in the digest · null beside POOLED:CLASSIC5 · 5m · frozen3.0 · era ALL · median term, K = 20 draws*

| class | null gaps+order (H20) · of record | null gaps-only (H20) | null gaps+order (H100) · of record | null gaps-only (H100) |
|---|---|---|---|---|
| breach | -0.252 [-0.282, -0.237] pct 15 | -0.245 [-0.265, -0.229] pct 10 | -0.304 [-0.337, -0.241] pct 5 | -0.295 [-0.339, -0.202] pct 5 |
| harden | +0.108 [+0.076, +0.131] pct 95 | +0.092 [+0.073, +0.139] pct 90 | +0.141 [+0.087, +0.221] pct 85 | +0.141 [+0.063, +0.220] pct 80 |
| DIE | -0.326 [-0.346, -0.303] pct 0 | -0.323 [-0.357, -0.292] pct 10 | -0.331 [-0.381, -0.314] pct 15 | -0.342 [-0.440, -0.272] pct 10 |
| memory-touch-v1 | +0.053 [+0.038, +0.075] pct 0 | +0.058 [+0.040, +0.082] pct 5 | +0.064 [+0.000, +0.101] pct 10 | +0.051 [+0.024, +0.088] pct 5 |
| memory-touch-2s | +0.173 [+0.147, +0.195] pct 5 | +0.176 [+0.153, +0.194] pct 0 | +0.103 [+0.052, +0.167] pct 0 | +0.119 [+0.093, +0.166] pct 0 |
| flip-hold | -0.093 [-0.119, -0.073] pct 25 | -0.095 [-0.121, -0.075] pct 25 | -0.142 [-0.180, -0.079] pct 30 | -0.137 [-0.184, -0.077] pct 40 |

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L1589–L1599*

### POOLED:UNSEEN12 · 5m · frozen3.0 · era `ALL`

| class | n H20 | med H20 | toll | **NET H20** | n H100 | med H100 | **NET H100** | flags |
|---|---|---|---|---|---|---|---|---|
| breach | 47,056 | -0.333 | 0.419 | **-0.752** | 47,044 | -0.406 | **-0.825** |  |
| harden | 27,346 | +0.202 | 0.421 | **-0.219** | 27,341 | +0.247 | **-0.174** |  |
| DIE | 19,710 | -0.406 | 0.381 | **-0.786** | 19,703 | -0.530 | **-0.910** |  |
| memory-touch-v1 | 38,694 | +0.060 | 0.337 | **-0.277** | 38,679 | +0.065 | **-0.271** |  |
| memory-touch-2s | 25,845 | +0.121 | 0.360 | **-0.240** | 25,840 | +0.036 | **-0.324** |  |
| flip-hold | 15,903 | -0.092 | 0.356 | **-0.448** | 15,901 | -0.233 | **-0.590** |  |

*Tier-E · report-only · COMPUTED AT CLOSE, not in the digest · null beside POOLED:UNSEEN12 · 5m · frozen3.0 · era ALL · median term, K = 20 draws*

| class | null gaps+order (H20) · of record | null gaps-only (H20) | null gaps+order (H100) · of record | null gaps-only (H100) |
|---|---|---|---|---|
| breach | -0.221 [-0.232, -0.202] pct 0 | -0.227 [-0.238, -0.214] pct 0 | -0.267 [-0.313, -0.212] pct 0 | -0.261 [-0.303, -0.232] pct 0 |
| harden | +0.095 [+0.065, +0.116] pct 100 | +0.109 [+0.077, +0.125] pct 100 | +0.135 [+0.084, +0.192] pct 95 | +0.136 [+0.105, +0.188] pct 85 |
| DIE | -0.316 [-0.345, -0.295] pct 0 | -0.311 [-0.335, -0.298] pct 0 | -0.380 [-0.426, -0.288] pct 0 | -0.367 [-0.398, -0.305] pct 0 |
| memory-touch-v1 | +0.084 [+0.069, +0.095] pct 15 | +0.074 [+0.067, +0.087] pct 15 | +0.133 [+0.099, +0.175] pct 10 | +0.131 [+0.097, +0.159] pct 10 |
| memory-touch-2s | +0.186 [+0.177, +0.204] pct 0 | +0.189 [+0.169, +0.200] pct 0 | +0.169 [+0.116, +0.214] pct 0 | +0.171 [+0.110, +0.193] pct 0 |
| flip-hold | -0.101 [-0.121, -0.080] pct 65 | -0.108 [-0.119, -0.094] pct 80 | -0.129 [-0.185, -0.055] pct 5 | -0.136 [-0.192, -0.115] pct 10 |

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L1348–L1358*

### POOLED:CLASSIC5 · 5m · frozen3.0 · era `holdout`

| class | n H20 | med H20 | toll | **NET H20** | n H100 | med H100 | **NET H100** | flags |
|---|---|---|---|---|---|---|---|---|
| breach | 10,668 | -0.223 | 0.602 | **-0.825** | 10,662 | -0.253 | **-0.855** |  |
| harden | 6,085 | +0.000 | 0.593 | **-0.593** | 6,083 | +0.077 | **-0.515** |  |
| DIE | 4,583 | -0.398 | 0.547 | **-0.945** | 4,579 | -0.334 | **-0.880** |  |
| memory-touch-v1 | 9,142 | -0.001 | 0.461 | **-0.463** | 9,134 | -0.098 | **-0.560** |  |
| memory-touch-2s | 5,990 | +0.107 | 0.514 | **-0.407** | 5,987 | -0.077 | **-0.591** |  |
| flip-hold | 3,732 | -0.044 | 0.508 | **-0.552** | 3,729 | -0.069 | **-0.577** |  |

*Tier-E · report-only · COMPUTED AT CLOSE, not in the digest · null beside POOLED:CLASSIC5 · 5m · frozen3.0 · era holdout · median term, K = 20 draws*

| class | null gaps+order (H20) · of record | null gaps-only (H20) | null gaps+order (H100) · of record | null gaps-only (H100) |
|---|---|---|---|---|
| breach | -0.185 [-0.245, -0.159] pct 45 | -0.203 [-0.232, -0.184] pct 40 | -0.164 [-0.227, -0.040] pct 15 | -0.161 [-0.216, -0.093] pct 15 |
| harden | +0.084 [+0.033, +0.136] pct 15 | +0.053 [+0.028, +0.099] pct 15 | +0.061 [-0.014, +0.155] pct 55 | +0.064 [-0.056, +0.134] pct 55 |
| DIE | -0.264 [-0.308, -0.231] pct 5 | -0.267 [-0.309, -0.217] pct 5 | -0.198 [-0.318, +0.000] pct 25 | -0.146 [-0.242, -0.050] pct 5 |
| memory-touch-v1 | +0.012 [+0.000, +0.051] pct 15 | +0.042 [+0.005, +0.080] pct 10 | -0.010 [-0.052, +0.083] pct 10 | +0.028 [+0.000, +0.086] pct 0 |
| memory-touch-2s | +0.135 [+0.094, +0.175] pct 30 | +0.158 [+0.108, +0.192] pct 25 | +0.024 [-0.000, +0.117] pct 10 | +0.109 [+0.039, +0.183] pct 0 |
| flip-hold | -0.059 [-0.112, -0.008] pct 55 | -0.074 [-0.113, -0.012] pct 65 | -0.037 [-0.145, +0.039] pct 40 | -0.034 [-0.088, +0.094] pct 35 |

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L1616–L1626*

### POOLED:UNSEEN12 · 5m · frozen3.0 · era `holdout`

| class | n H20 | med H20 | toll | **NET H20** | n H100 | med H100 | **NET H100** | flags |
|---|---|---|---|---|---|---|---|---|
| breach | 24,558 | -0.308 | 0.570 | **-0.878** | 24,546 | -0.385 | **-0.955** |  |
| harden | 14,394 | +0.203 | 0.563 | **-0.360** | 14,389 | +0.249 | **-0.314** |  |
| DIE | 10,164 | -0.388 | 0.539 | **-0.928** | 10,157 | -0.390 | **-0.929** |  |
| memory-touch-v1 | 20,117 | +0.017 | 0.463 | **-0.446** | 20,102 | +0.062 | **-0.402** |  |
| memory-touch-2s | 13,288 | +0.110 | 0.501 | **-0.391** | 13,283 | +0.000 | **-0.501** |  |
| flip-hold | 8,111 | -0.066 | 0.497 | **-0.563** | 8,109 | -0.212 | **-0.708** |  |

*Tier-E · report-only · COMPUTED AT CLOSE, not in the digest · null beside POOLED:UNSEEN12 · 5m · frozen3.0 · era holdout · median term, K = 20 draws*

| class | null gaps+order (H20) · of record | null gaps-only (H20) | null gaps+order (H100) · of record | null gaps-only (H100) |
|---|---|---|---|---|
| breach | -0.184 [-0.206, -0.170] pct 0 | -0.194 [-0.208, -0.171] pct 0 | -0.188 [-0.286, -0.114] pct 5 | -0.191 [-0.257, -0.134] pct 5 |
| harden | +0.065 [+0.036, +0.085] pct 100 | +0.084 [+0.054, +0.122] pct 100 | +0.082 [-0.002, +0.162] pct 90 | +0.087 [+0.039, +0.180] pct 95 |
| DIE | -0.281 [-0.300, -0.263] pct 5 | -0.266 [-0.285, -0.223] pct 0 | -0.252 [-0.337, -0.216] pct 10 | -0.266 [-0.294, -0.197] pct 5 |
| memory-touch-v1 | +0.058 [+0.025, +0.082] pct 15 | +0.054 [+0.027, +0.066] pct 25 | +0.136 [+0.111, +0.168] pct 20 | +0.104 [+0.074, +0.170] pct 15 |
| memory-touch-2s | +0.167 [+0.135, +0.194] pct 5 | +0.163 [+0.149, +0.178] pct 5 | +0.140 [+0.063, +0.217] pct 8 | +0.131 [+0.067, +0.174] pct 8 |
| flip-hold | -0.080 [-0.110, -0.051] pct 65 | -0.051 [-0.119, -0.026] pct 40 | -0.085 [-0.148, +0.000] pct 0 | -0.102 [-0.163, -0.035] pct 15 |

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L1359–L1374*

### POOLED:CLASSIC5 · 4h · frozen3.0 · era `ALL`

| class | n H20 | med H20 | toll | **NET H20** | n H100 | med H100 | **NET H100** | flags |
|---|---|---|---|---|---|---|---|---|
| breach | 584 | +0.102 | 0.061 | **+0.041** | 581 | +0.569 | **+0.509** |  |
| harden | 289 | -0.037 | 0.059 | **-0.096** | 287 | -0.384 | **-0.443** |  |
| DIE | 295 | +0.033 | 0.063 | **-0.030** | 294 | +0.670 | **+0.609** |  |
| memory-touch-v1 | 531 | -0.091 | 0.059 | **-0.150** | 527 | -0.114 | **-0.172** |  |
| memory-touch-2s | 370 | -0.145 | 0.060 | **-0.205** | 369 | -0.158 | **-0.217** |  |
| flip-hold | 247 | +0.216 | 0.056 | **+0.159** | 247 | +0.555 | **+0.499** |  |
| retest-hold-ribbon89_127 | 267 | +0.506 | 0.063 | **+0.443** | 264 | +0.707 | **+0.645** | TUNED |
| retest-hold-ribbon127_200 | 258 | +0.520 | 0.065 | **+0.455** | 257 | +0.654 | **+0.590** | TUNED |
| retest-hold-tap89 | 236 | +0.747 | 0.066 | **+0.681** | 234 | +0.888 | **+0.823** | TUNED |
| retest-hold-tap127 | 221 | +0.591 | 0.067 | **+0.524** | 219 | +0.528 | **+0.463** | TUNED |
| retest-hold-tap200 | 191 | -0.086 | 0.057 | **-0.143** | 190 | +0.180 | **+0.125** | TUNED |

*Tier-E · report-only · COMPUTED AT CLOSE, not in the digest · null beside POOLED:CLASSIC5 · 4h · frozen3.0 · era ALL · median term, K = 20 draws*

| class | null gaps+order (H20) · of record | null gaps-only (H20) | null gaps+order (H100) · of record | null gaps-only (H100) |
|---|---|---|---|---|
| breach | +0.014 [-0.126, +0.143] pct 65 | +0.026 [-0.209, +0.161] pct 65 | +0.144 [-0.123, +0.972] pct 60 | +0.266 [+0.011, +0.654] pct 60 |
| harden | +0.154 [-0.199, +0.397] pct 30 | -0.024 [-0.243, +0.160] pct 50 | -0.261 [-0.789, +0.660] pct 35 | -0.305 [-0.611, +0.168] pct 40 |
| DIE | +0.146 [+0.062, +0.367] pct 20 | +0.183 [-0.003, +0.272] pct 35 | +0.566 [-0.007, +0.957] pct 55 | +0.531 [+0.019, +0.873] pct 60 |
| memory-touch-v1 | -0.021 [-0.134, +0.114] pct 40 | -0.022 [-0.263, +0.038] pct 35 | +0.028 [-0.201, +0.255] pct 30 | -0.163 [-0.371, +0.103] pct 60 |
| memory-touch-2s | -0.098 [-0.298, +0.141] pct 35 | +0.024 [-0.174, +0.147] pct 30 | -0.186 [-0.427, +0.067] pct 55 | -0.381 [-0.578, -0.166] pct 75 |
| flip-hold | +0.025 [-0.065, +0.167] pct 80 | +0.104 [-0.078, +0.230] pct 65 | +0.311 [+0.138, +0.444] pct 85 | +0.165 [-0.049, +0.408] pct 80 |
| retest-hold-ribbon89_127 | +0.262 [+0.100, +0.469] pct 75 | +0.209 [+0.068, +0.343] pct 85 | +0.561 [+0.201, +0.830] pct 70 | +0.479 [+0.089, +0.785] pct 70 |
| retest-hold-ribbon127_200 | +0.213 [+0.069, +0.452] pct 80 | +0.281 [+0.030, +0.446] pct 80 | +0.440 [+0.006, +0.583] pct 80 | +0.029 [-0.303, +0.513] pct 75 |
| retest-hold-tap89 | +0.380 [+0.211, +0.630] pct 85 | +0.240 [+0.110, +0.460] pct 90 | +0.559 [+0.264, +0.834] pct 75 | +0.480 [+0.020, +0.862] pct 75 |
| retest-hold-tap127 | +0.346 [-0.109, +0.481] pct 85 | +0.234 [+0.090, +0.421] pct 85 | +0.382 [+0.090, +0.825] pct 55 | +0.174 [-0.302, +0.730] pct 70 |
| retest-hold-tap200 | -0.006 [-0.185, +0.280] pct 50 | +0.127 [-0.149, +0.301] pct 40 | +0.241 [-0.196, +0.931] pct 48 | +0.095 [-0.351, +0.586] pct 50 |

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L1627–L1642*

### POOLED:UNSEEN12 · 4h · frozen3.0 · era `ALL`

| class | n H20 | med H20 | toll | **NET H20** | n H100 | med H100 | **NET H100** | flags |
|---|---|---|---|---|---|---|---|---|
| breach | 886 | -0.096 | 0.052 | **-0.148** | 876 | +0.016 | **-0.036** |  |
| harden | 484 | +0.072 | 0.049 | **+0.022** | 477 | -0.118 | **-0.167** |  |
| DIE | 402 | +0.144 | 0.049 | **+0.095** | 399 | -0.303 | **-0.351** |  |
| memory-touch-v1 | 709 | +0.191 | 0.048 | **+0.143** | 705 | +0.091 | **+0.045** |  |
| memory-touch-2s | 509 | +0.028 | 0.043 | **-0.015** | 505 | -0.037 | **-0.080** |  |
| flip-hold | 331 | -0.044 | 0.040 | **-0.084** | 328 | +0.005 | **-0.035** |  |
| retest-hold-ribbon89_127 | 354 | +0.120 | 0.047 | **+0.073** | 349 | +0.883 | **+0.836** | TUNED |
| retest-hold-ribbon127_200 | 346 | -0.104 | 0.052 | **-0.155** | 342 | +0.693 | **+0.641** | TUNED |
| retest-hold-tap89 | 300 | +0.107 | 0.043 | **+0.064** | 295 | +0.890 | **+0.847** | TUNED |
| retest-hold-tap127 | 285 | -0.018 | 0.044 | **-0.063** | 281 | +0.956 | **+0.912** | TUNED |
| retest-hold-tap200 | 248 | +0.341 | 0.050 | **+0.291** | 243 | +0.212 | **+0.162** | TUNED |

*Tier-E · report-only · COMPUTED AT CLOSE, not in the digest · null beside POOLED:UNSEEN12 · 4h · frozen3.0 · era ALL · median term, K = 20 draws*

| class | null gaps+order (H20) · of record | null gaps-only (H20) | null gaps+order (H100) · of record | null gaps-only (H100) |
|---|---|---|---|---|
| breach | -0.083 [-0.223, +0.082] pct 45 | -0.001 [-0.078, +0.065] pct 25 | -0.058 [-0.419, +0.423] pct 55 | -0.171 [-0.429, +0.390] pct 60 |
| harden | +0.001 [-0.176, +0.138] pct 60 | +0.011 [-0.099, +0.110] pct 65 | +0.084 [-0.579, +0.620] pct 45 | +0.065 [-0.385, +0.346] pct 35 |
| DIE | +0.042 [-0.155, +0.134] pct 75 | +0.108 [-0.017, +0.206] pct 60 | +0.197 [-0.347, +0.361] pct 25 | -0.034 [-0.451, +0.337] pct 30 |
| memory-touch-v1 | +0.151 [+0.049, +0.273] pct 60 | +0.195 [+0.109, +0.282] pct 50 | +0.261 [+0.035, +0.442] pct 40 | +0.281 [-0.023, +0.434] pct 30 |
| memory-touch-2s | +0.121 [-0.017, +0.283] pct 30 | +0.087 [-0.014, +0.241] pct 35 | +0.087 [-0.366, +0.328] pct 40 | -0.090 [-0.325, +0.299] pct 55 |
| flip-hold | +0.054 [-0.045, +0.116] pct 25 | +0.139 [-0.051, +0.227] pct 25 | +0.107 [-0.255, +0.491] pct 40 | +0.186 [-0.154, +0.353] pct 35 |
| retest-hold-ribbon89_127 | +0.080 [-0.003, +0.155] pct 65 | +0.079 [-0.020, +0.230] pct 60 | +0.609 [-0.093, +0.783] pct 95 | +0.541 [-0.196, +0.942] pct 70 |
| retest-hold-ribbon127_200 | -0.095 [-0.237, +0.064] pct 40 | -0.095 [-0.272, +0.097] pct 50 | +0.452 [+0.177, +0.668] pct 80 | +0.502 [+0.098, +0.825] pct 60 |
| retest-hold-tap89 | +0.022 [-0.141, +0.094] pct 85 | +0.009 [-0.058, +0.129] pct 70 | +0.061 [-0.318, +0.549] pct 100 | +0.030 [-0.368, +0.891] pct 75 |
| retest-hold-tap127 | +0.051 [-0.134, +0.113] pct 40 | -0.079 [-0.202, +0.097] pct 65 | +0.585 [+0.216, +0.848] pct 75 | +0.499 [+0.023, +0.786] pct 80 |
| retest-hold-tap200 | +0.150 [+0.103, +0.435] pct 65 | +0.233 [+0.061, +0.467] pct 70 | +0.278 [+0.211, +0.684] pct 28 | +0.311 [+0.176, +0.516] pct 25 |

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L1391–L1406*

### POOLED:CLASSIC5 · 4h · frozen3.0 · era `holdout`

| class | n H20 | med H20 | toll | **NET H20** | n H100 | med H100 | **NET H100** | flags |
|---|---|---|---|---|---|---|---|---|
| breach | 201 | -0.579 | 0.076 | **-0.656** | 198 | -0.880 | **-0.952** |  |
| harden | 100 | +0.702 | 0.076 | **+0.626** | 98 | +1.545 | **+1.470** |  |
| DIE | 101 | -0.299 | 0.071 | **-0.370** | 100 | -0.217 | **-0.287** |  |
| memory-touch-v1 | 203 | -0.091 | 0.068 | **-0.158** | 199 | -0.095 | **-0.161** |  |
| memory-touch-2s | 131 | +0.252 | 0.071 | **+0.181** | 130 | +0.468 | **+0.398** |  |
| flip-hold | 87 | +0.962 | 0.057 | **+0.904** | 87 | +0.145 | **+0.088** |  |
| retest-hold-ribbon89_127 | 97 | +0.506 | 0.080 | **+0.426** | 94 | -0.005 | **-0.083** | TUNED |
| retest-hold-ribbon127_200 | 94 | +0.671 | 0.074 | **+0.597** | 93 | +0.028 | **-0.044** | TUNED |
| retest-hold-tap89 | 88 | +0.786 | 0.080 | **+0.706** | 86 | +0.328 | **+0.248** | TUNED |
| retest-hold-tap127 | 83 | +0.116 | 0.077 | **+0.039** | 81 | +0.028 | **-0.044** | TUNED |
| retest-hold-tap200 | 63 | +0.068 | 0.072 | **-0.004** | 62 | -0.108 | **-0.176** | TUNED |

*Tier-E · report-only · COMPUTED AT CLOSE, not in the digest · null beside POOLED:CLASSIC5 · 4h · frozen3.0 · era holdout · median term, K = 20 draws*

| class | null gaps+order (H20) · of record | null gaps-only (H20) | null gaps+order (H100) · of record | null gaps-only (H100) |
|---|---|---|---|---|
| breach | -0.238 [-0.507, +0.323] pct 20 | -0.235 [-0.453, -0.052] pct 25 | +0.310 [-0.294, +0.829] pct 15 | +0.113 [-0.300, +0.627] pct 15 |
| harden | +0.201 [-0.037, +0.598] pct 90 | +0.123 [-0.023, +0.596] pct 85 | -0.309 [-1.251, +1.123] pct 85 | -0.008 [-0.602, +1.022] pct 90 |
| DIE | -0.249 [-0.657, +0.215] pct 50 | +0.057 [-0.137, +0.336] pct 15 | +0.065 [-0.923, +0.607] pct 35 | -0.088 [-0.838, +1.136] pct 50 |
| memory-touch-v1 | +0.115 [+0.028, +0.289] pct 20 | +0.019 [-0.308, +0.192] pct 45 | +0.308 [-0.037, +0.769] pct 20 | -0.199 [-0.501, +0.611] pct 55 |
| memory-touch-2s | +0.083 [-0.184, +0.315] pct 65 | +0.163 [-0.017, +0.300] pct 50 | +0.716 [+0.026, +1.164] pct 40 | +0.257 [-0.627, +0.910] pct 60 |
| flip-hold | -0.171 [-0.383, +0.211] pct 95 | +0.131 [-0.439, +0.594] pct 95 | +0.234 [-1.412, +0.756] pct 45 | -0.076 [-0.949, +0.443] pct 65 |
| retest-hold-ribbon89_127 | +0.266 [+0.085, +0.721] pct 68 | +0.306 [+0.120, +0.486] pct 75 | +0.480 [-0.490, +0.636] pct 30 | +0.308 [-0.234, +0.681] pct 40 |
| retest-hold-ribbon127_200 | +0.333 [-0.048, +0.771] pct 60 | +0.331 [+0.103, +0.848] pct 60 | -0.060 [-0.322, +0.236] pct 60 | -0.086 [-0.388, +0.054] pct 65 |
| retest-hold-tap89 | +0.480 [+0.265, +0.775] pct 75 | +0.225 [+0.117, +0.425] pct 98 | +0.653 [-0.303, +1.114] pct 35 | +0.231 [-0.235, +0.654] pct 55 |
| retest-hold-tap127 | -0.143 [-0.366, +0.722] pct 60 | +0.264 [-0.123, +0.745] pct 50 | +0.147 [-0.145, +0.574] pct 38 | +0.004 [-0.630, +0.357] pct 52 |
| retest-hold-tap200 | +0.204 [-0.118, +0.489] pct 35 | +0.122 [-0.091, +0.404] pct 40 | +0.234 [-0.127, +0.869] pct 35 | -0.116 [-0.630, +0.375] pct 50 |

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L1659–L1674*

### POOLED:UNSEEN12 · 4h · frozen3.0 · era `holdout`

| class | n H20 | med H20 | toll | **NET H20** | n H100 | med H100 | **NET H100** | flags |
|---|---|---|---|---|---|---|---|---|
| breach | 479 | -0.245 | 0.067 | **-0.312** | 469 | -0.668 | **-0.734** |  |
| harden | 263 | -0.015 | 0.067 | **-0.082** | 256 | +0.618 | **+0.551** |  |
| DIE | 216 | -0.079 | 0.067 | **-0.145** | 213 | -0.753 | **-0.818** |  |
| memory-touch-v1 | 402 | -0.073 | 0.056 | **-0.128** | 398 | +0.038 | **-0.016** |  |
| memory-touch-2s | 281 | -0.070 | 0.051 | **-0.121** | 277 | -0.025 | **-0.076** |  |
| flip-hold | 181 | +0.176 | 0.040 | **+0.136** | 178 | -0.082 | **-0.122** |  |
| retest-hold-ribbon89_127 | 191 | +0.496 | 0.065 | **+0.431** | 186 | +1.021 | **+0.960** | TUNED |
| retest-hold-ribbon127_200 | 185 | -0.129 | 0.056 | **-0.185** | 181 | +0.726 | **+0.671** | TUNED |
| retest-hold-tap89 | 158 | +0.338 | 0.066 | **+0.272** | 153 | +0.979 | **+0.914** | TUNED |
| retest-hold-tap127 | 149 | +0.041 | 0.057 | **-0.016** | 145 | +1.063 | **+1.006** | TUNED |
| retest-hold-tap200 | 120 | +0.195 | 0.061 | **+0.134** | 115 | -0.215 | **-0.276** | TUNED |

*Tier-E · report-only · COMPUTED AT CLOSE, not in the digest · null beside POOLED:UNSEEN12 · 4h · frozen3.0 · era holdout · median term, K = 20 draws*

| class | null gaps+order (H20) · of record | null gaps-only (H20) | null gaps+order (H100) · of record | null gaps-only (H100) |
|---|---|---|---|---|
| breach | -0.056 [-0.213, +0.035] pct 20 | -0.102 [-0.198, +0.122] pct 15 | -0.181 [-0.797, +0.020] pct 30 | -0.352 [-0.608, +0.225] pct 25 |
| harden | +0.016 [-0.083, +0.183] pct 45 | +0.125 [-0.066, +0.322] pct 30 | +0.443 [-0.340, +0.843] pct 60 | +0.349 [-0.638, +1.022] pct 65 |
| DIE | +0.002 [-0.262, +0.138] pct 40 | +0.070 [-0.111, +0.254] pct 30 | -0.425 [-0.738, -0.147] pct 25 | -0.336 [-0.603, +0.033] pct 25 |
| memory-touch-v1 | +0.201 [+0.054, +0.315] pct 15 | +0.262 [+0.104, +0.432] pct 15 | +0.228 [-0.139, +0.447] pct 30 | +0.136 [-0.108, +0.344] pct 35 |
| memory-touch-2s | +0.085 [-0.106, +0.261] pct 30 | +0.170 [-0.145, +0.377] pct 30 | +0.276 [-0.408, +0.619] pct 35 | -0.117 [-0.591, +0.605] pct 60 |
| flip-hold | +0.259 [+0.038, +0.394] pct 35 | +0.063 [+0.004, +0.293] pct 65 | +0.098 [-0.223, +0.570] pct 35 | +0.313 [-0.082, +0.599] pct 25 |
| retest-hold-ribbon89_127 | +0.324 [+0.123, +0.451] pct 80 | +0.241 [+0.082, +0.468] pct 85 | +0.486 [+0.017, +0.856] pct 80 | +0.046 [-0.496, +0.537] pct 95 |
| retest-hold-ribbon127_200 | -0.132 [-0.281, +0.066] pct 50 | -0.163 [-0.539, +0.095] pct 50 | +0.373 [-0.135, +0.718] pct 75 | +0.041 [-0.225, +0.418] pct 80 |
| retest-hold-tap89 | +0.086 [-0.021, +0.373] pct 70 | +0.190 [-0.021, +0.456] pct 65 | +0.133 [-0.518, +0.669] pct 90 | +0.001 [-0.640, +0.566] pct 90 |
| retest-hold-tap127 | +0.047 [-0.132, +0.110] pct 45 | -0.125 [-0.372, +0.067] pct 65 | +0.447 [-0.633, +1.060] pct 78 | -0.203 [-0.300, +0.489] pct 95 |
| retest-hold-tap200 | +0.232 [+0.052, +0.527] pct 50 | +0.197 [-0.084, +0.366] pct 50 | +0.119 [-0.350, +0.735] pct 30 | -0.168 [-0.401, +0.268] pct 45 |

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L1407–L1422*

### POOLED:CLASSIC5 · 1d · frozen3.0 · era `ALL`

| class | n H20 | med H20 | toll | **NET H20** | n H100 | med H100 | **NET H100** | flags |
|---|---|---|---|---|---|---|---|---|
| breach | 105 | +0.582 | 0.024 | **+0.558** | 101 | +1.522 | **+1.499** |  |
| harden | 55 | -0.750 | 0.024 | **-0.775** | 52 | -2.290 | **-2.313** |  |
| DIE | 50 | +0.346 | 0.023 | **+0.323** | 49 | +1.185 | **+1.163** |  |
| memory-touch-v1 | 79 | +0.628 | 0.025 | **+0.603** | 76 | +0.819 | **+0.794** |  |
| memory-touch-2s | 53 | +0.583 | 0.024 | **+0.559** | 49 | +0.523 | **+0.498** |  |
| flip-hold | 44 | +0.970 | 0.022 | **+0.948** | 40 | +0.258 | **+0.236** |  |
| retest-hold-ribbon89_127 | 42 | +0.444 | 0.026 | **+0.418** | 40 | +1.257 | **+1.231** | TUNED |
| retest-hold-ribbon127_200 | 38 | +0.368 | 0.024 | **+0.344** | 38 | +0.327 | **+0.303** | TUNED |
| retest-hold-tap89 | 35 | +0.425 | 0.026 | **+0.399** | 33 | +0.471 | **+0.445** | TUNED |
| retest-hold-tap127 | 31 | +0.440 | 0.020 | **+0.420** | 31 | +0.383 | **+0.363** | TUNED |
| retest-hold-tap200 | 28 | -0.265 | 0.029 | **-0.294** | 28 | -0.043 | **-0.072** | n<30 · TUNED |

*Tier-E · report-only · COMPUTED AT CLOSE, not in the digest · null beside POOLED:CLASSIC5 · 1d · frozen3.0 · era ALL · median term, K = 20 draws*

| class | null gaps+order (H20) · of record | null gaps-only (H20) | null gaps+order (H100) · of record | null gaps-only (H100) |
|---|---|---|---|---|
| breach | +0.364 [-0.165, +0.889] pct 65 | +0.328 [+0.055, +0.662] pct 65 | +0.658 [-0.613, +1.249] pct 80 | +0.608 [-0.466, +0.877] pct 85 |
| harden | -0.001 [-0.600, +0.247] pct 25 | -0.234 [-0.584, +0.039] pct 15 | -0.505 [-1.485, +1.208] pct 10 | -0.838 [-1.920, -0.149] pct 15 |
| DIE | +0.437 [+0.136, +0.607] pct 40 | +0.066 [-0.379, +0.528] pct 65 | +0.284 [-0.206, +1.082] pct 75 | -0.061 [-0.965, +0.882] pct 80 |
| memory-touch-v1 | +0.182 [-0.098, +0.405] pct 80 | +0.182 [-0.237, +0.312] pct 95 | +0.055 [-0.395, +1.124] pct 60 | -0.233 [-0.669, +0.291] pct 80 |
| memory-touch-2s | +0.097 [-0.311, +0.274] pct 90 | -0.120 [-0.271, +0.305] pct 90 | +0.063 [-0.720, +0.586] pct 70 | +0.360 [-1.049, +0.914] pct 60 |
| flip-hold | +0.105 [-0.087, +0.322] pct 95 | -0.132 [-0.481, +0.216] pct 100 | +1.292 [+0.293, +1.756] pct 25 | +0.436 [-0.835, +1.200] pct 45 |
| retest-hold-ribbon89_127 | +0.131 [-0.014, +0.365] pct 80 | +0.222 [+0.029, +0.345] pct 75 | +0.227 [-0.774, +1.582] pct 65 | -0.473 [-1.104, +0.894] pct 85 |
| retest-hold-ribbon127_200 | -0.249 [-0.359, +0.020] pct 90 | -0.090 [-0.233, +0.144] pct 80 | +0.547 [+0.048, +0.701] pct 30 | +0.423 [+0.041, +1.020] pct 45 |
| retest-hold-tap89 | +0.130 [-0.032, +0.272] pct 80 | +0.141 [-0.168, +0.349] pct 78 | +0.633 [-0.484, +1.893] pct 40 | -0.326 [-1.208, +1.129] pct 70 |
| retest-hold-tap127 | -0.075 [-0.298, +0.167] pct 88 | -0.039 [-0.121, +0.226] pct 80 | +0.383 [-0.023, +0.639] pct 50 | +0.329 [-0.282, +0.393] pct 65 |
| retest-hold-tap200 | -0.319 [-0.503, -0.161] pct 55 | -0.386 [-0.580, -0.081] pct 55 | +0.771 [-0.043, +1.050] pct 25 | +0.523 [-0.788, +1.786] pct 45 |

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L1675–L1690*

### POOLED:UNSEEN12 · 1d · frozen3.0 · era `ALL`

| class | n H20 | med H20 | toll | **NET H20** | n H100 | med H100 | **NET H100** | flags |
|---|---|---|---|---|---|---|---|---|
| breach | 126 | -0.078 | 0.019 | **-0.097** | 120 | -0.056 | **-0.075** |  |
| harden | 62 | +0.251 | 0.020 | **+0.231** | 60 | +0.127 | **+0.108** |  |
| DIE | 64 | +0.152 | 0.025 | **+0.127** | 60 | -0.084 | **-0.109** |  |
| memory-touch-v1 | 93 | +0.477 | 0.024 | **+0.453** | 87 | +0.740 | **+0.716** |  |
| memory-touch-2s | 69 | +0.656 | 0.023 | **+0.633** | 63 | +0.816 | **+0.794** |  |
| flip-hold | 48 | +0.552 | 0.027 | **+0.525** | 44 | -0.270 | **-0.297** |  |
| retest-hold-ribbon89_127 | 50 | -0.003 | 0.019 | **-0.021** | 45 | +0.120 | **+0.103** | TUNED |
| retest-hold-ribbon127_200 | 48 | -0.170 | 0.019 | **-0.189** | 42 | +0.073 | **+0.054** | TUNED |
| retest-hold-tap89 | 42 | +0.007 | 0.017 | **-0.010** | 38 | -0.057 | **-0.074** | TUNED |
| retest-hold-tap127 | 39 | -0.127 | 0.019 | **-0.145** | 36 | +0.318 | **+0.299** | TUNED |
| retest-hold-tap200 | 31 | +0.252 | 0.019 | **+0.233** | 26 | +0.468 | **+0.449** | n<30 · TUNED |

*Tier-E · report-only · COMPUTED AT CLOSE, not in the digest · null beside POOLED:UNSEEN12 · 1d · frozen3.0 · era ALL · median term, K = 20 draws*

| class | null gaps+order (H20) · of record | null gaps-only (H20) | null gaps+order (H100) · of record | null gaps-only (H100) |
|---|---|---|---|---|
| breach | -0.091 [-0.281, +0.337] pct 60 | -0.087 [-0.291, +0.063] pct 50 | -0.360 [-1.492, +0.777] pct 60 | -0.392 [-1.960, +0.495] pct 55 |
| harden | -0.144 [-0.328, +0.332] pct 70 | +0.171 [-0.169, +0.437] pct 60 | -0.041 [-0.846, +1.751] pct 50 | +0.271 [-0.774, +2.247] pct 45 |
| DIE | +0.073 [-0.415, +0.604] pct 50 | -0.393 [-0.492, +0.096] pct 75 | -0.159 [-0.850, +0.481] pct 50 | -0.642 [-2.015, +0.270] pct 60 |
| memory-touch-v1 | +0.047 [-0.207, +0.426] pct 80 | -0.141 [-0.272, +0.078] pct 100 | +0.417 [-0.381, +0.746] pct 70 | -0.337 [-0.917, +0.011] pct 90 |
| memory-touch-2s | -0.047 [-0.222, +0.176] pct 90 | +0.062 [-0.156, +0.224] pct 95 | +0.019 [-0.536, +0.288] pct 85 | -0.514 [-1.079, -0.044] pct 90 |
| flip-hold | +0.085 [-0.150, +0.381] pct 85 | +0.205 [-0.070, +0.243] pct 90 | -0.762 [-1.243, -0.298] pct 80 | -0.742 [-0.984, -0.160] pct 70 |
| retest-hold-ribbon89_127 | -0.082 [-0.336, +0.296] pct 55 | +0.139 [-0.222, +0.258] pct 40 | -0.447 [-1.218, -0.101] pct 85 | -0.427 [-1.327, -0.118] pct 90 |
| retest-hold-ribbon127_200 | -0.178 [-0.422, -0.088] pct 55 | -0.224 [-0.407, -0.060] pct 55 | -0.813 [-1.332, -0.404] pct 85 | -0.826 [-1.347, -0.256] pct 90 |
| retest-hold-tap89 | -0.102 [-0.378, +0.093] pct 55 | +0.064 [-0.323, +0.133] pct 45 | -0.710 [-1.454, +0.031] pct 65 | -0.594 [-1.320, -0.447] pct 90 |
| retest-hold-tap127 | -0.298 [-0.485, -0.090] pct 72 | -0.236 [-0.382, +0.119] pct 65 | -0.948 [-1.903, -0.372] pct 90 | -0.830 [-1.815, -0.357] pct 100 |
| retest-hold-tap200 | -0.255 [-0.776, +0.243] pct 80 | -0.001 [-0.373, +0.268] pct 65 | -0.959 [-1.665, -0.182] pct 90 | -0.526 [-1.736, +0.039] pct 80 |

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L1439–L1454*

### POOLED:CLASSIC5 · 1d · frozen3.0 · era `holdout`

| class | n H20 | med H20 | toll | **NET H20** | n H100 | med H100 | **NET H100** | flags |
|---|---|---|---|---|---|---|---|---|
| breach | 40 | +0.203 | 0.026 | **+0.177** | 36 | +0.067 | **+0.041** |  |
| harden | 21 | -0.594 | 0.026 | **-0.620** | 18 | -0.628 | **-0.653** | n<30 |
| DIE | 19 | +0.255 | 0.024 | **+0.231** | 18 | -1.793 | **-1.816** | n<30 |
| memory-touch-v1 | 37 | +0.400 | 0.026 | **+0.374** | 34 | +0.776 | **+0.749** |  |
| memory-touch-2s | 23 | +0.314 | 0.029 | **+0.285** | 19 | +0.332 | **+0.303** | n<30 |
| flip-hold | 19 | +0.854 | 0.022 | **+0.832** | 15 | -3.571 | **-3.588** | n<30 |
| retest-hold-ribbon89_127 | 16 | +0.352 | 0.027 | **+0.326** | 14 | -1.345 | **-1.371** | n<30 · TUNED |
| retest-hold-ribbon127_200 | 12 | +0.179 | 0.031 | **+0.148** | 12 | -0.152 | **-0.183** | n<30 · TUNED |
| retest-hold-tap89 | 13 | +0.019 | 0.027 | **-0.008** | 11 | -1.436 | **-1.463** | n<30 · TUNED |
| retest-hold-tap127 | 9 | -0.089 | 0.040 | **-0.128** | 9 | +0.614 | **+0.574** | n<30 · TUNED |
| retest-hold-tap200 | 11 | -0.503 | 0.031 | **-0.534** | 11 | +4.106 | **+4.076** | n<30 · TUNED |

*Tier-E · report-only · COMPUTED AT CLOSE, not in the digest · null beside POOLED:CLASSIC5 · 1d · frozen3.0 · era holdout · median term, K = 20 draws*

| class | null gaps+order (H20) · of record | null gaps-only (H20) | null gaps+order (H100) · of record | null gaps-only (H100) |
|---|---|---|---|---|
| breach | +0.298 [-0.588, +0.744] pct 40 | +0.320 [-0.086, +0.891] pct 50 | -1.237 [-3.243, +0.849] pct 60 | -0.874 [-2.256, +1.927] pct 60 |
| harden | +0.129 [-1.139, +0.465] pct 40 | -0.341 [-1.173, +0.349] pct 35 | +0.207 [-1.751, +2.933] pct 40 | -1.013 [-3.008, +1.627] pct 55 |
| DIE | +0.320 [-0.510, +0.580] pct 45 | -0.379 [-0.882, +0.186] pct 75 | -0.863 [-3.143, +0.313] pct 45 | -1.222 [-2.581, -0.331] pct 45 |
| memory-touch-v1 | +0.058 [-0.397, +0.589] pct 70 | -0.106 [-0.668, +0.376] pct 75 | +0.185 [-1.372, +1.651] pct 55 | +0.230 [-0.667, +1.060] pct 65 |
| memory-touch-2s | +0.119 [-0.166, +0.273] pct 80 | -0.168 [-0.741, +0.376] pct 70 | +0.132 [-1.337, +1.554] pct 52 | +0.751 [-0.968, +2.371] pct 40 |
| flip-hold | +0.038 [-0.176, +0.805] pct 75 | -0.268 [-0.654, +0.036] pct 95 | -0.817 [-2.212, +2.226] pct 15 | -1.291 [-3.265, +0.837] pct 20 |
| retest-hold-ribbon89_127 | +0.102 [-0.332, +0.541] pct 65 | +0.019 [-0.340, +0.298] pct 75 | -1.436 [-2.417, +0.880] pct 55 | -1.633 [-2.267, -0.886] pct 65 |
| retest-hold-ribbon127_200 | -0.539 [-1.435, +0.243] pct 70 | -0.232 [-0.773, +0.135] pct 75 | -1.281 [-3.684, +0.614] pct 60 | -1.423 [-2.694, +1.567] pct 62 |
| retest-hold-tap89 | +0.287 [-0.213, +0.853] pct 35 | -0.172 [-0.780, +0.455] pct 65 | -1.342 [-2.050, +3.932] pct 45 | -1.927 [-2.164, -1.328] pct 68 |
| retest-hold-tap127 | -0.219 [-1.077, +0.205] pct 55 | -0.154 [-0.600, +0.172] pct 52 | -1.677 [-3.451, +0.886] pct 72 | -1.218 [-3.051, +0.839] pct 72 |
| retest-hold-tap200 | -0.849 [-1.087, -0.070] pct 65 | -0.773 [-0.970, -0.403] pct 65 | -1.499 [-4.012, +3.061] pct 88 | +0.050 [-2.438, +2.497] pct 85 |

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L1707–L1722*

### POOLED:UNSEEN12 · 1d · frozen3.0 · era `holdout`

| class | n H20 | med H20 | toll | **NET H20** | n H100 | med H100 | **NET H100** | flags |
|---|---|---|---|---|---|---|---|---|
| breach | 65 | +0.409 | 0.021 | **+0.387** | 59 | -0.445 | **-0.465** |  |
| harden | 33 | -0.334 | 0.025 | **-0.360** | 31 | +0.391 | **+0.374** |  |
| DIE | 32 | +0.840 | 0.027 | **+0.813** | 28 | -0.084 | **-0.111** | n<30 |
| memory-touch-v1 | 49 | +0.681 | 0.023 | **+0.657** | 43 | +0.816 | **+0.793** |  |
| memory-touch-2s | 33 | +0.708 | 0.023 | **+0.685** | 27 | +1.132 | **+1.109** | n<30 |
| flip-hold | 28 | +0.726 | 0.024 | **+0.702** | 24 | -0.270 | **-0.294** | n<30 |
| retest-hold-ribbon89_127 | 24 | -0.093 | 0.024 | **-0.117** | 19 | +1.367 | **+1.347** | n<30 · TUNED |
| retest-hold-ribbon127_200 | 22 | -0.000 | 0.022 | **-0.023** | 16 | +0.503 | **+0.481** | n<30 · TUNED |
| retest-hold-tap89 | 18 | -0.390 | 0.020 | **-0.410** | 14 | -2.166 | **-2.182** | n<30 · TUNED |
| retest-hold-tap127 | 17 | -0.362 | 0.026 | **-0.388** | 14 | +0.503 | **+0.477** | n<30 · TUNED |
| retest-hold-tap200 | 13 | -0.564 | 0.021 | **-0.585** | 8 | -0.748 | **-0.767** | n<30 · TUNED |

*Tier-E · report-only · COMPUTED AT CLOSE, not in the digest · null beside POOLED:UNSEEN12 · 1d · frozen3.0 · era holdout · median term, K = 20 draws*

| class | null gaps+order (H20) · of record | null gaps-only (H20) | null gaps+order (H100) · of record | null gaps-only (H100) |
|---|---|---|---|---|
| breach | -0.030 [-0.323, +0.708] pct 70 | -0.116 [-0.736, +0.093] pct 85 | -0.877 [-2.541, +1.057] pct 60 | -0.645 [-2.222, +0.155] pct 52 |
| harden | -0.095 [-0.854, +0.464] pct 35 | +0.189 [-0.436, +0.834] pct 30 | +1.828 [-2.094, +4.218] pct 40 | +0.117 [-1.343, +2.543] pct 55 |
| DIE | +0.433 [+0.020, +1.130] pct 60 | -0.580 [-0.881, -0.008] pct 90 | +0.118 [-1.598, +1.106] pct 45 | -1.671 [-2.950, -0.709] pct 90 |
| memory-touch-v1 | +0.075 [-0.034, +0.351] pct 98 | -0.194 [-0.382, +0.075] pct 100 | +0.080 [-0.674, +0.927] pct 72 | -0.739 [-1.045, -0.145] pct 100 |
| memory-touch-2s | -0.153 [-0.308, +0.123] pct 90 | -0.063 [-0.309, +0.191] pct 100 | -0.466 [-1.242, +0.876] pct 90 | -1.057 [-1.305, -0.242] pct 100 |
| flip-hold | +0.110 [-0.347, +0.808] pct 70 | -0.007 [-0.300, +0.451] pct 90 | -1.620 [-2.335, -0.269] pct 75 | -0.885 [-2.479, -0.297] pct 75 |
| retest-hold-ribbon89_127 | -0.370 [-0.556, +0.051] pct 60 | -0.162 [-0.575, -0.002] pct 55 | -1.896 [-3.489, -0.217] pct 90 | -2.220 [-3.238, -0.463] pct 100 |
| retest-hold-ribbon127_200 | -0.179 [-0.905, +0.634] pct 60 | -0.271 [-0.728, +0.429] pct 70 | -1.223 [-3.381, -0.688] pct 100 | -1.434 [-2.465, -1.035] pct 90 |
| retest-hold-tap89 | -0.636 [-1.156, +0.025] pct 55 | -0.485 [-0.881, -0.063] pct 55 | -2.420 [-3.564, -0.545] pct 60 | -2.392 [-3.595, -1.217] pct 62 |
| retest-hold-tap127 | -0.387 [-0.905, +0.289] pct 50 | -0.391 [-0.921, -0.148] pct 55 | -2.557 [-3.816, -1.554] pct 100 | -2.468 [-3.461, -1.317] pct 95 |
| retest-hold-tap200 | -0.528 [-0.845, +0.031] pct 45 | +0.071 [-0.533, +0.441] pct 20 | -2.056 [-3.429, -0.862] pct 80 | -1.389 [-2.819, -0.676] pct 72 |

### 2.4 · COVERAGE · CONFIRMED-RANGE DENSITY · MEAN LIFE — digest §1 (L733–L860)

The definitions and the per-lens tables. Left in the digest: the SCALE calibrator's whole grid (L803–L860).

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L735–L802*

Coverage = close inside the alive CONFIRMED macro range's span (boundaries + deviation zones), % of ALL bars. Density = confirmed macro ranges per 100 bars. Life = mean(die_i - confirm_i) over ranges that DIED; still-alive ones excluded and counted. `frozen3.0` is the pin of record [L2]; `calibrated` is IN-SAMPLE BY CONSTRUCTION and is printed beside it, never instead of it.

### 5m

| asset | bars | gaps | cov% f3.0 | dens f3.0 | life f3.0 | SCALE cal | cov% cal | dens cal | life cal | flips f3.0 |
|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 740,137 | 0 | 45.84 | 0.383 | 122.6 | 1.75 | 60.62 | 0.732 | 86.2 | 2275 |
| ETHUSDT | 717,219 | 0 | 42.73 | 0.393 | 111.5 | 1.75 | 59.94 | 0.710 | 87.8 | 2335 |
| SOLUSDT | 633,132 | 0 | 39.51 | 0.386 | 105.8 | 1.75 | 53.35 | 0.809 | 69.9 | 2017 |
| NEARUSDT | 624,192 | 0 | 41.72 | 0.362 | 119.1 | 1.75 | 54.06 | 0.777 | 73.8 | 1935 |
| ZECUSDT | 697,056 | 0 | 41.15 | 0.383 | 111.1 | 1.75 | 55.33 | 0.792 | 73.9 | 2231 |
| ENAUSDT | 259,818 | 0 | 39.40 | 0.373 | 109.6 | 1.75 | 52.28 | 0.811 | 68.7 | 781 |
| PUMPUSDT | 126,246 | 0 | 34.81 | 0.410 | 88.4 | 2 | 47.82 | 0.707 | 71.6 | 452 |
| HYPEUSDT | 138,018 | 0 | 40.82 | 0.393 | 108.1 | 2 | 50.93 | 0.698 | 77.4 | 472 |
| MNTUSDT_BYBIT | 312,593 | 0 | 39.01 | 0.428 | 94.4 | 2 | 47.58 | 0.776 | 64.7 | 995 |
| SUIUSDT | 356,256 | 0 | 40.69 | 0.377 | 111.6 | 1.75 | 53.87 | 0.811 | 70.4 | 1048 |
| LTCUSDT | 704,831 | 0 | 43.45 | 0.371 | 120.7 | 1.75 | 57.69 | 0.748 | 81.2 | 2185 |
| XMRUSDT | 697,632 | 0 | 45.57 | 0.357 | 132.0 | 1.75 | 56.66 | 0.776 | 77.7 | 1956 |
| BNBUSDT | 695,616 | 0 | 39.78 | 0.395 | 104.1 | 2 | 49.64 | 0.700 | 74.7 | 2188 |
| UNIUSDT | 631,980 | 0 | 40.05 | 0.381 | 108.7 | 1.75 | 54.19 | 0.790 | 72.9 | 2007 |
| 1000PEPEUSDT | 355,674 | 0 | 43.92 | 0.365 | 123.7 | 1.75 | 56.73 | 0.765 | 77.9 | 1021 |
| DOGEUSDT | 652,116 | 0 | 45.59 | 0.351 | 133.2 | 1.75 | 59.07 | 0.727 | 85.1 | 1852 |
| 1000BONKUSDT | 297,816 | 0 | 38.89 | 0.387 | 104.1 | 2 | 48.26 | 0.694 | 73.6 | 946 |

### 4h

| asset | bars | gaps | cov% f3.0 | dens f3.0 | life f3.0 | SCALE cal | cov% cal | dens cal | life cal | flips f3.0 |
|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 15,420 | 0 | 29.98 | 0.409 | 76.4 | 2 | 46.60 | 0.720 | 68.2 | 50 |
| ETHUSDT | 14,943 | 0 | 33.21 | 0.422 | 81.0 | 2 | 44.32 | 0.756 | 61.6 | 41 |
| SOLUSDT | 13,191 | 0 | 32.68 | 0.402 | 84.6 | 2 | 43.84 | 0.667 | 69.2 | 49 |
| NEARUSDT | 13,004 | 0 | 29.72 | 0.446 | 70.0 | 2 | 42.51 | 0.715 | 63.6 | 56 |
| ZECUSDT | 14,522 | 0 | 32.42 | 0.420 | 80.0 | 2 | 42.36 | 0.771 | 58.5 | 51 |
| ENAUSDT | 5,413 | 0 | 25.01 | 0.443 | 59.6 | 2.25 | 39.00 | 0.720 | 57.4 | 23 |
| PUMPUSDT | 2,631 | 0 | 37.13 | 0.266 | 141.3 | 2.25 | 22.01 | 0.760 | 32.1 | 8 |
| HYPEUSDT | 2,876 | 0 | 25.70 | 0.522 | 52.5 | 1.75 | 47.60 | 0.765 | 68.0 | 12 |
| MNTUSDT_BYBIT | 6,513 | 0 | 33.67 | 0.476 | 75.1 | 2 | 38.91 | 0.752 | 55.1 | 24 |
| SUIUSDT | 7,422 | 0 | 36.12 | 0.404 | 92.8 | 1.75 | 52.60 | 0.781 | 70.7 | 26 |
| LTCUSDT | 14,684 | 0 | 40.99 | 0.436 | 97.0 | 2 | 45.55 | 0.742 | 64.5 | 50 |
| XMRUSDT | 14,534 | 0 | 48.95 | 0.275 | 181.8 | 1.5 | 68.66 | 0.784 | 91.6 | 32 |
| BNBUSDT | 14,492 | 0 | 46.80 | 0.338 | 144.2 | 1.75 | 55.52 | 0.821 | 70.9 | 37 |
| UNIUSDT | 13,167 | 0 | 37.60 | 0.418 | 92.7 | 2 | 51.04 | 0.706 | 75.3 | 42 |
| 1000PEPEUSDT | 7,410 | 0 | 42.55 | 0.405 | 108.2 | 1.75 | 47.41 | 0.756 | 66.8 | 24 |
| DOGEUSDT | 13,586 | 0 | 43.01 | 0.339 | 129.8 | 1.75 | 63.76 | 0.677 | 97.1 | 39 |
| 1000BONKUSDT | 6,205 | 0 | 40.34 | 0.322 | 134.8 | 1.75 | 49.36 | 0.854 | 62.4 | 15 |

### 1d

| asset | bars | gaps | cov% f3.0 | dens f3.0 | life f3.0 | SCALE cal | cov% cal | dens cal | life cal | flips f3.0 |
|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 2,569 | 0 | 36.05 | 0.428 | 83.7 | 2.25 | 33.79 | 0.779 | 46.6 | 6 |
| ETHUSDT | 2,489 | 0 | 15.79 | 0.362 | 46.1 | 2 | 31.62 | 0.804 | 43.0 | 10 |
| SOLUSDT | 2,197 | 0 | 23.62 | 0.546 | 46.8 | 2.5 | 20.21 | 0.728 | 29.8 | 12 |
| NEARUSDT | 2,166 | 0 | 37.12 | 0.369 | 106.5 | 2 | 34.26 | 0.739 | 50.3 | 7 |
| ZECUSDT | 2,419 | 0 | 45.35 | 0.537 | 85.8 | 2.5 | 31.05 | 0.785 | 41.5 | 9 |
| ENAUSDT | 901 | 0 | 23.53 | 0.111 | 217.0 | 2 | 20.53 | 0.666 | 37.5 | 0 |
| PUMPUSDT | 437 | 0 | 17.39 | 0.458 | 41.0 | 1.75 | 47.14 | 0.686 | 74.0 | 1 |
| HYPEUSDT | 478 | 0 | 1.67 | 0.418 | 4.5 | 2.25 | 19.04 | 0.837 | 26.2 | 0 |
| MNTUSDT_BYBIT | 1,084 | 0 | 47.60 | 0.461 | 104.8 | 2 | 34.41 | 0.830 | 43.3 | 4 |
| SUIUSDT | 1,236 | 0 | 30.02 | 0.243 | 17.5 | 2.5 | 23.95 | 0.728 | 37.0 | 2 |
| LTCUSDT | 2,446 | 0 | 23.39 | 0.531 | 48.9 | 2.25 | 27.56 | 0.777 | 37.9 | 10 |
| XMRUSDT | 2,421 | 0 | 50.31 | 0.124 | 408.7 | 1.5 | 62.78 | 0.620 | 106.2 | 2 |
| BNBUSDT | 2,414 | 0 | 32.56 | 0.331 | 99.4 | 2 | 57.29 | 0.746 | 79.3 | 6 |
| UNIUSDT | 2,193 | 0 | 45.19 | 0.410 | 112.3 | 2.25 | 50.75 | 0.593 | 88.9 | 6 |
| 1000PEPEUSDT | 1,234 | 0 | 28.36 | 0.567 | 55.8 | 2.25 | 30.06 | 0.810 | 39.0 | 3 |
| DOGEUSDT | 2,263 | 0 | 25.76 | 0.442 | 61.1 | 2.25 | 38.62 | 0.751 | 53.8 | 10 |
| 1000BONKUSDT | 1,033 | 0 | 52.27 | 0.484 | 114.6 | 2 | 52.57 | 0.678 | 83.3 | 5 |

### 2.5 · F-RF-4 — SPRING / UPTHRUST OVERLAP — digest §2 (L861–L879), whole

*Tier-E · report-only · verbatim from `CENSUS_R_DIGEST.md` · L863–L879*

Both overlap directions on every (asset, lens, scale kind): how many hardens reclaim by law, how many ALSO sweep the 20-bar extreme (harden -> house shape), and how many house shapes fall INSIDE a harden episode (house shape -> harden). `bottom` = springs, `top` = upthrusts.

| lens | kind | side | hardens | law reclaim | also sweep look | house shapes | inside an episode |
|---|---|---|---|---|---|---|---|
| 1d | calibrated | bottom | 112 | 112 | 76 | 1,219 | 50 |
| 1d | calibrated | top | 78 | 78 | 61 | 1,694 | 50 |
| 1d | frozen3.0 | bottom | 82 | 82 | 53 | 1,219 | 35 |
| 1d | frozen3.0 | top | 35 | 35 | 28 | 1,694 | 24 |
| 4h | calibrated | bottom | 831 | 831 | 580 | 8,579 | 522 |
| 4h | calibrated | top | 853 | 853 | 645 | 9,898 | 574 |
| 4h | frozen3.0 | bottom | 378 | 378 | 249 | 8,579 | 214 |
| 4h | frozen3.0 | top | 397 | 397 | 305 | 9,898 | 261 |
| 5m | calibrated | bottom | 46,392 | 46,392 | 34,422 | 392,387 | 26,309 |
| 5m | calibrated | top | 48,401 | 48,401 | 36,405 | 415,466 | 28,604 |
| 5m | frozen3.0 | bottom | 21,417 | 21,417 | 15,606 | 392,387 | 11,930 |
| 5m | frozen3.0 | top | 22,662 | 22,662 | 16,900 | 415,466 | 13,331 |

### 2.6 · WHAT STAYS IN THE DIGEST

Whole sections not selected: §0 · THE EXECUTOR LEANS, VERBATIM (L15–L31) · §3 · HOLD TALLIES — every one-shot evaluation, per anchor (L880–L922) · §4 · THE R1 HOLD-PIN TUNING — protocol fixed BEFORE the look (L923–L1044) · §6 · PRIOR ESTATE EVIDENCE ON EMA TAPS / HOLDS / RETESTS — CONTEXT ONLY (L1859–L1874) · §7 · ARTIFACTS, KEYS, COST (L1875–L1896). From its title block (L1–L14) only the banner, the warranty, the collar and the era law are spliced above. The digest is the table of record; this section is a reading order, not a result.
