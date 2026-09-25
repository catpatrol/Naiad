# TIER-C11 · STAGE S — THE SCALPER RETUNED: CLOSED BY R2 (1h: FAIL)

as_of_last_closed_4h: 2026-09-25T00:00:00Z · substrate tc11_20260925 · seed 20260924 · pin 1790294400000

Contract of record: `exchange/queue/2026-09-24_TC11_APOLLO.md` (sha256 bb38e016…), STAGE S. Registration P-SCALP-2 (seq 6, payload sha c4e7ea0064bf…): vs zero, CLASSIC5, holdout era, taker. Readings built: L-S.1 (the precondition), L-R.4 (the lens verdict of record and its two words), L-1.2 (the maker twin, the reopening path), LEANS §10 (the tuning-era word beside). Not built: L-S.2 (the form) and AM-7 (no trade row exists to price). Source: `scripts/tierc11_stage_s.py`.

## 0 · The verdict

**CLOSED BY R2 (1h: FAIL).** The R2 lens verdict of record at 1h (CLASSIC5 pooled, holdout era, calibrated scale, taker toll) is **FAIL**. Stage S re-derived it from the row's printed columns under the [Q-R3] law (§2); the printed labels agree with the columns.

- **Stage S STOPS [L-S.1]: no scalper book, no maker twin (fill assumed or fill conditioned), no 17-asset view, no regime gate, no tuning slice, no frozen-3.0 twin, no refused-entry count and no target/stop ratio distribution were built; P-SCALP-2's §0 row reads the verdict, with no number and no slot spent.**
- **P-SCALP-2's §0 cell reads:** CLOSED BY R2 (1h: FAIL) — no number, no slot spent (m = 9 unchanged, the bar 0.10/9 not loosened) [L-S.1, L-1.4].
- **The maker-twin word (the reopening path):** FAIL. Reopening path: none — the maker twin of the record row reads FAIL too, so no reopening path exists at 1h ('FAIL — maker twin PASSES (the reopening path; needs a toll-model change the operator rules)' is read only when the maker twin of the same row passes) [L-R.4, L-1.2].
- **Beside, Tier-E [LEANS §10]** (tier TIER-E · a SELECTION, not a result · gates nothing): the tuning-era R2 1h word FAIL (holdout word of record FAIL). It decides nothing.
- `regbooks/P-SCALP-2/STATUS.json`: status `CLOSED_BY_PRECONDITION`, reason `CLOSED BY R2 (1h: FAIL)`, arms `[]`.

## 1 · The 1h R2 row of record, whole

From `research_outputs/tierc11/stage_r/R2_LENS_VERDICTS.json` (sha256 `82cc3ec6ddd588c9fbd8402def471438a0c931590606b9a2a6cc3a97572f3087`), `lenses['1h']`, all 26 fields; the file's `record` block is `{"era": "holdout", "panel": "POOLED:CLASSIC5", "scale_kind": "calibrated", "toll": "taker"}`.

| field | value |
|---|---|
| charter_twin | FAIL |
| edge_median_term_h20 | 0.0 |
| edge_n | 12044 |
| edge_n_ranges | 771 |
| edge_net_h20 | -0.16760525 |
| edge_toll_atr | 0.16760525 |
| era | holdout |
| fallback_members |  |
| maker_twin | FAIL |
| members | BTCUSDT,ETHUSDT,SOLUSDT,NEARUSDT,ZECUSDT |
| n_ranges | 816 |
| pick_window | tuning |
| pool | POOLED:CLASSIC5 |
| provisional | False |
| ratio_median | 46.2355442 |
| scale | calibrated |
| scale_in_sample | OUT-OF-SAMPLE (holdout; the causal slice of a tuning pick) |
| share_ratio_lt_1 | 0.0 |
| stability_changed_members | BTCUSDT,SOLUSDT,NEARUSDT |
| tier_e_all_word | FAIL |
| tier_e_note | the tuning / ALL words are Tier-E twins: 'a SELECTION, not a result' |
| tier_e_tuning_word | FAIL |
| toll | taker |
| toll_bps_rt | 10.0 |
| verdict | FAIL |
| word | FAIL |

The same row in `research_outputs/tierc11/stage_r/R2_FEASIBILITY.parquet` (content sha256 `2545d290133c5d7b76553acd2793122fb40a929a35ca0f406b889411000cb2eb`, equal to Stage R's build_manifest), all 59 columns; it equals the JSON row on every shared field (21 checked).

| column | value |
|---|---|
| cell | POOLED:CLASSIC5\|1h\|holdout\|calibrated\|taker |
| panel | POOLED:CLASSIC5 |
| lens | 1h |
| era | holdout |
| scale_kind | calibrated |
| toll | taker |
| pooled | True |
| n_members | 5 |
| members | BTCUSDT,ETHUSDT,SOLUSDT,NEARUSDT,ZECUSDT |
| scale_mult | null |
| toll_bps_rt_min | 10.0 |
| toll_bps_rt_max | 10.0 |
| n_ranges | 816 |
| ratio_median | 46.2355442 |
| ratio_d1 | 19.89618571 |
| ratio_d2 | 28.10622566 |
| ratio_d3 | 34.70036807 |
| ratio_d4 | 41.65503768 |
| ratio_d5 | 46.2355442 |
| ratio_d6 | 53.73104454 |
| ratio_d7 | 64.74069208 |
| ratio_d8 | 80.21108179 |
| ratio_d9 | 103.15555316 |
| share_ratio_lt_1 | 0.0 |
| height_atr_median | 3.94028245 |
| toll_atr_median | 0.0864487 |
| height_leg_would_pass | True |
| edge_n | 12044 |
| edge_n_ranges | 771 |
| edge_median_term_h20 | 0.0 |
| edge_toll_atr | 0.16760525 |
| edge_net_h20 | -0.16760525 |
| edge_hit_rate_net | 0.48289605 |
| edge_leg_would_pass | False |
| under_floor | False |
| fail_reasons | net -0.167605 <= 0 |
| census_would_pass | False |
| word | FAIL |
| is_lens_verdict_of_record | True |
| verdict | FAIL |
| would_read | null |
| pick_window | tuning |
| scale_in_sample | OUT-OF-SAMPLE (holdout; the causal slice of a tuning pick) |
| fallback_members |  |
| stability_changed | True |
| stability_changed_members | BTCUSDT,SOLUSDT,NEARUSDT |
| tier | R2 LENS VERDICT OF RECORD [L-R.4] |
| selection_not_a_result | n/a — the lens verdict of record, not a selection |
| gates | range trading on this lens in this and every later tier unless the toll model changes [contract R2]; at 1h also Stage S [L-S.1] |
| tc10_would_read | null |
| tc10_would_pass | null |
| tc10_n_ranges | null |
| tc10_ratio_median | null |
| tc10_edge_n | null |
| tc10_edge_n_ranges | null |
| tc10_edge_net_h20 | null |
| tc10_note | not measured by TC10 (lens / toll / panel) |
| as_of_last_closed_4h | 2026-09-25T00:00:00Z |
| as_of_substrate | tc11_20260925 |

## 2 · The re-derivation [L-S.1 ← L-R.4, the [Q-R3] law]

| leg | clause | printed column | printed value | law | holds |
|---|---|---|---|---|---|
| height | n_ranges >= 30 | n_ranges | 816 | >= 30 | yes |
| height | median(height / toll) >= 3.0 | ratio_median | 46.2355442 | >= 3.0 | yes |
| height | share(ratio < 1) <= 0.10 | share_ratio_lt_1 | 0.0 | <= 0.10 | yes |
| edge | edge_n_ranges >= 30 | edge_n_ranges | 771 | >= 30 | yes |
| edge | edge_n >= 30 | edge_n | 12044 | >= 30 | yes |
| edge | median H20 term - toll > 0 | edge_net_h20 | -0.16760525 | > 0 | NO |

- Net identity [SS-2]: round(round(0.0, 8) − round(0.16760525, 8), 8) = -0.16760525 == printed edge_net_h20 -0.16760525: holds.
- Height leg: holds. Edge leg: FAILS. Under a floor: no. Re-derived taker word: **FAIL**.
- Printed: word `FAIL` · provisional `False` · maker_twin `FAIL` · verdict `FAIL`. L-R.4 reads the verdict as record_verdict(taker FAIL, maker FAIL) = `FAIL`. The labels agree with the columns.
- The gate opens only on the exact word `PASS` [SS-3]: **FAIL → gate CLOSED**.

## 3 · The words beside the verdict of record

Each row re-derived by Stage S from R2_FEASIBILITY.parquet's printed columns and matched against the JSON field that prints it. Only the first row is the verdict of record; the others are Tier-E (tier TIER-E · a SELECTION, not a result · gates nothing).

| role | panel · era · scale · toll | n_ranges | ratio_median | share<1 | edge_n | edge ranges | median H20 | toll ATR | net H20 | re-derived | printed in JSON |
|---|---|---|---|---|---|---|---|---|---|---|---|
| verdict of record [L-R.4] | POOLED:CLASSIC5 · holdout · calibrated · taker | 816 | 46.2355442 | 0.0 | 12044 | 771 | +0.00000000 | +0.16760525 | -0.16760525 | FAIL | `word` = FAIL |
| maker twin — the reopening path [L-1.2] | POOLED:CLASSIC5 · holdout · calibrated · maker | 816 | 115.58886049 | 0.0 | 12044 | 771 | +0.00000000 | +0.06704210 | -0.06704210 | FAIL | `maker_twin` = FAIL |
| charter twin [L-1.1] | POOLED:CLASSIC5 · holdout · calibrated · charter | 816 | 26.2698845 | 0.0 | 12044 | 771 | +0.00000000 | +0.23464735 | -0.23464735 | FAIL | `charter_twin` = FAIL |
| tuning-era word beside [§10], Tier-E | POOLED:CLASSIC5 · tuning · calibrated · taker | 1437 | 55.51948052 | 0.0 | 23897 | 1371 | +0.08344812 | +0.12035377 | -0.03690565 | FAIL | `tier_e_tuning_word` = FAIL |
| ALL-era word beside, Tier-E | POOLED:CLASSIC5 · ALL · calibrated · taker | 2253 | 51.59590951 | 0.0 | 35941 | 2140 | +0.05947917 | +0.13482148 | -0.07534231 | FAIL | `tier_e_all_word` = FAIL |

## 4 · The 1h CLASSIC5 R2 block, re-derived, whole — Tier-E but the ★ row

`research_outputs/tierc11/stage_s/S_R2_1H.parquet` — 108 cells = 6 panels × 3 eras × 2 scales × 3 tolls. `would_read` = the [Q-R3] law on the row's printed columns; `R2 word` = the word R2 printed for that row (`word` on the record row, `would_read` elsewhere). Collar [L-1.4]: every row but ★ carries tier TIER-E · a SELECTION, not a result · gates nothing. The ★ row is the lens verdict of record and carries Stage R's record collar verbatim: tier `R2 LENS VERDICT OF RECORD [L-R.4]` · `n/a — the lens verdict of record, not a selection` · gates `range trading on this lens in this and every later tier unless the toll model changes [contract R2]; at 1h also Stage S [L-S.1]`. Its word of record lives in S_GATE.json / STATUS.json, and Stage S reads its gate from the JSON of record, never from this table.

| ★ | panel | era | scale | toll | n_ranges | ratio_median | share<1 | edge_n | edge ranges | median H20 | toll ATR | net H20 | height | edge | floor | would_read | R2 word | agree |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|  | POOLED:CLASSIC5 | ALL | calibrated | taker | 2253 | 51.59590951 | 0.00000000 | 35941 | 2140 | +0.05947917 | +0.13482148 | -0.07534231 | holds | fails | — | FAIL | FAIL | yes |
|  | POOLED:CLASSIC5 | ALL | calibrated | maker | 2253 | 128.98977378 | 0.00000000 | 35941 | 2140 | +0.05947917 | +0.05392859 | +0.00555058 | holds | holds | — | PASS | PASS | yes |
|  | POOLED:CLASSIC5 | ALL | calibrated | charter | 2253 | 30.17662159 | 0.00000000 | 35941 | 2140 | +0.05947917 | +0.18875007 | -0.12927090 | holds | fails | — | FAIL | FAIL | yes |
|  | POOLED:CLASSIC5 | ALL | frozen3.0 | taker | 1088 | 84.73722839 | 0.00000000 | 31066 | 1081 | +0.08509583 | +0.13256882 | -0.04747299 | holds | fails | — | FAIL | FAIL | yes |
|  | POOLED:CLASSIC5 | ALL | frozen3.0 | maker | 1088 | 211.84307098 | 0.00000000 | 31066 | 1081 | +0.08509583 | +0.05302753 | +0.03206830 | holds | holds | — | PASS | PASS | yes |
|  | POOLED:CLASSIC5 | ALL | frozen3.0 | charter | 1088 | 49.65431993 | 0.00000000 | 31066 | 1081 | +0.08509583 | +0.18559635 | -0.10050052 | holds | fails | — | FAIL | FAIL | yes |
|  | POOLED:CLASSIC5 | tuning | calibrated | taker | 1437 | 55.51948052 | 0.00000000 | 23897 | 1371 | +0.08344812 | +0.12035377 | -0.03690565 | holds | fails | — | FAIL | FAIL | yes |
|  | POOLED:CLASSIC5 | tuning | calibrated | maker | 1437 | 138.79870130 | 0.00000000 | 23897 | 1371 | +0.08344812 | +0.04814151 | +0.03530661 | holds | holds | — | PASS | PASS | yes |
|  | POOLED:CLASSIC5 | tuning | calibrated | charter | 1437 | 32.59169568 | 0.00000000 | 23897 | 1371 | +0.08344812 | +0.16849528 | -0.08504716 | holds | fails | — | FAIL | FAIL | yes |
|  | POOLED:CLASSIC5 | tuning | frozen3.0 | taker | 712 | 87.76236189 | 0.00000000 | 20169 | 708 | +0.05708380 | +0.11933163 | -0.06224783 | holds | fails | — | FAIL | FAIL | yes |
|  | POOLED:CLASSIC5 | tuning | frozen3.0 | maker | 712 | 219.40590473 | 0.00000000 | 20169 | 708 | +0.05708380 | +0.04773265 | +0.00935115 | holds | holds | — | PASS | PASS | yes |
|  | POOLED:CLASSIC5 | tuning | frozen3.0 | charter | 712 | 52.16621765 | 0.00000000 | 20169 | 708 | +0.05708380 | +0.16706429 | -0.10998049 | holds | fails | — | FAIL | FAIL | yes |
| ★ | POOLED:CLASSIC5 | holdout | calibrated | taker | 816 | 46.23554420 | 0.00000000 | 12044 | 771 | +0.00000000 | +0.16760525 | -0.16760525 | holds | fails | — | FAIL | FAIL | yes |
|  | POOLED:CLASSIC5 | holdout | calibrated | maker | 816 | 115.58886049 | 0.00000000 | 12044 | 771 | +0.00000000 | +0.06704210 | -0.06704210 | holds | fails | — | FAIL | FAIL | yes |
|  | POOLED:CLASSIC5 | holdout | calibrated | charter | 816 | 26.26988450 | 0.00000000 | 12044 | 771 | +0.00000000 | +0.23464735 | -0.23464735 | holds | fails | — | FAIL | FAIL | yes |
|  | POOLED:CLASSIC5 | holdout | frozen3.0 | taker | 376 | 80.12122307 | 0.00000000 | 10897 | 375 | +0.15250004 | +0.15930185 | -0.00680181 | holds | fails | — | FAIL | FAIL | yes |
|  | POOLED:CLASSIC5 | holdout | frozen3.0 | maker | 376 | 200.30305767 | 0.00000000 | 10897 | 375 | +0.15250004 | +0.06372074 | +0.08877930 | holds | holds | — | PASS | PASS | yes |
|  | POOLED:CLASSIC5 | holdout | frozen3.0 | charter | 376 | 46.18776177 | 0.00000000 | 10897 | 375 | +0.15250004 | +0.22302259 | -0.07052255 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:BTCUSDT | ALL | calibrated | taker | 522 | 30.73891198 | 0.00000000 | 7750 | 491 | +0.21675802 | +0.13482148 | +0.08193654 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:BTCUSDT | ALL | calibrated | maker | 522 | 76.84727994 | 0.00000000 | 7750 | 491 | +0.21675802 | +0.05392859 | +0.16282943 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:BTCUSDT | ALL | calibrated | charter | 522 | 21.95636570 | 0.00000000 | 7750 | 491 | +0.21675802 | +0.18875007 | +0.02800795 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:BTCUSDT | ALL | frozen3.0 | taker | 223 | 54.02244076 | 0.00000000 | 6677 | 223 | +0.29240970 | +0.13256882 | +0.15984088 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:BTCUSDT | ALL | frozen3.0 | maker | 223 | 135.05610189 | 0.00000000 | 6677 | 223 | +0.29240970 | +0.05302753 | +0.23938217 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:BTCUSDT | ALL | frozen3.0 | charter | 223 | 38.58745768 | 0.00000000 | 6677 | 223 | +0.29240970 | +0.18559635 | +0.10681335 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:BTCUSDT | tuning | calibrated | taker | 347 | 33.28236663 | 0.00000000 | 5183 | 329 | +0.26837417 | +0.12035377 | +0.14802040 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:BTCUSDT | tuning | calibrated | maker | 347 | 83.20591657 | 0.00000000 | 5183 | 329 | +0.26837417 | +0.04814151 | +0.22023266 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:BTCUSDT | tuning | calibrated | charter | 347 | 23.77311902 | 0.00000000 | 5183 | 329 | +0.26837417 | +0.16849528 | +0.09987889 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:BTCUSDT | tuning | frozen3.0 | taker | 152 | 58.22398281 | 0.00000000 | 4619 | 152 | +0.32355874 | +0.11933163 | +0.20422711 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:BTCUSDT | tuning | frozen3.0 | maker | 152 | 145.55995702 | 0.00000000 | 4619 | 152 | +0.32355874 | +0.04773265 | +0.27582609 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:BTCUSDT | tuning | frozen3.0 | charter | 152 | 41.58855915 | 0.00000000 | 4619 | 152 | +0.32355874 | +0.16706429 | +0.15649445 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:BTCUSDT | holdout | calibrated | taker | 175 | 26.13428681 | 0.00000000 | 2567 | 162 | +0.08150832 | +0.16760525 | -0.08609693 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:BTCUSDT | holdout | calibrated | maker | 175 | 65.33571704 | 0.00000000 | 2567 | 162 | +0.08150832 | +0.06704210 | +0.01446622 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:BTCUSDT | holdout | calibrated | charter | 175 | 18.66734772 | 0.00000000 | 2567 | 162 | +0.08150832 | +0.23464735 | -0.15313903 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:BTCUSDT | holdout | frozen3.0 | taker | 71 | 46.31893440 | 0.00000000 | 2058 | 71 | +0.20455162 | +0.15930185 | +0.04524977 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:BTCUSDT | holdout | frozen3.0 | maker | 71 | 115.79733599 | 0.00000000 | 2058 | 71 | +0.20455162 | +0.06372074 | +0.14083088 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:BTCUSDT | holdout | frozen3.0 | charter | 71 | 33.08495314 | 0.00000000 | 2058 | 71 | +0.20455162 | +0.22302259 | -0.01847097 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ETHUSDT | ALL | calibrated | taker | 441 | 45.94507836 | 0.00000000 | 6707 | 420 | +0.07441301 | +0.10526433 | -0.03085132 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ETHUSDT | ALL | calibrated | maker | 441 | 114.86269589 | 0.00000000 | 6707 | 420 | +0.07441301 | +0.04210573 | +0.03230728 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:ETHUSDT | ALL | calibrated | charter | 441 | 32.81791311 | 0.00000000 | 6707 | 420 | +0.07441301 | +0.14737006 | -0.07295705 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ETHUSDT | ALL | frozen3.0 | taker | 231 | 65.77025635 | 0.00000000 | 5788 | 227 | +0.14645039 | +0.10566689 | +0.04078350 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:ETHUSDT | ALL | frozen3.0 | maker | 231 | 164.42564089 | 0.00000000 | 5788 | 227 | +0.14645039 | +0.04226676 | +0.10418363 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:ETHUSDT | ALL | frozen3.0 | charter | 231 | 46.97875454 | 0.00000000 | 5788 | 227 | +0.14645039 | +0.14793364 | -0.00148325 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ETHUSDT | tuning | calibrated | taker | 301 | 49.51373162 | 0.00000000 | 4553 | 289 | +0.04888677 | +0.09936581 | -0.05047904 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ETHUSDT | tuning | calibrated | maker | 301 | 123.78432906 | 0.00000000 | 4553 | 289 | +0.04888677 | +0.03974632 | +0.00914045 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:ETHUSDT | tuning | calibrated | charter | 301 | 35.36695116 | 0.00000000 | 4553 | 289 | +0.04888677 | +0.13911213 | -0.09022536 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ETHUSDT | tuning | frozen3.0 | taker | 153 | 69.54896545 | 0.00000000 | 4014 | 150 | +0.05796932 | +0.10009045 | -0.04212113 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ETHUSDT | tuning | frozen3.0 | maker | 153 | 173.87241362 | 0.00000000 | 4014 | 150 | +0.05796932 | +0.04003618 | +0.01793314 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:ETHUSDT | tuning | frozen3.0 | charter | 153 | 49.67783246 | 0.00000000 | 4014 | 150 | +0.05796932 | +0.14012663 | -0.08215731 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ETHUSDT | holdout | calibrated | taker | 140 | 41.99527534 | 0.00000000 | 2154 | 131 | +0.11620715 | +0.11394882 | +0.00225833 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:ETHUSDT | holdout | calibrated | maker | 140 | 104.98818836 | 0.00000000 | 2154 | 131 | +0.11620715 | +0.04557953 | +0.07062762 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:ETHUSDT | holdout | calibrated | charter | 140 | 29.99662524 | 0.00000000 | 2154 | 131 | +0.11620715 | +0.15952835 | -0.04332120 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ETHUSDT | holdout | frozen3.0 | taker | 78 | 60.53193493 | 0.00000000 | 1774 | 77 | +0.30884124 | +0.11318288 | +0.19565836 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:ETHUSDT | holdout | frozen3.0 | maker | 78 | 151.32983732 | 0.00000000 | 1774 | 77 | +0.30884124 | +0.04527315 | +0.26356809 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:ETHUSDT | holdout | frozen3.0 | charter | 78 | 43.23709638 | 0.00000000 | 1774 | 77 | +0.30884124 | +0.15845603 | +0.15038521 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:SOLUSDT | ALL | calibrated | taker | 441 | 59.19506463 | 0.00000000 | 6705 | 419 | +0.06119992 | +0.07520122 | -0.01400130 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:SOLUSDT | ALL | calibrated | maker | 441 | 147.98766157 | 0.00000000 | 6705 | 419 | +0.06119992 | +0.03008049 | +0.03111943 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:SOLUSDT | ALL | calibrated | charter | 441 | 29.59753231 | 0.00000000 | 6705 | 419 | +0.06119992 | +0.15040244 | -0.08920252 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:SOLUSDT | ALL | frozen3.0 | taker | 203 | 99.86675399 | 0.00000000 | 6260 | 202 | -0.00746668 | +0.07787760 | -0.08534428 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:SOLUSDT | ALL | frozen3.0 | maker | 203 | 249.66688498 | 0.00000000 | 6260 | 202 | -0.00746668 | +0.03115104 | -0.03861772 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:SOLUSDT | ALL | frozen3.0 | charter | 203 | 49.93337700 | 0.00000000 | 6260 | 202 | -0.00746668 | +0.15575520 | -0.16322188 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:SOLUSDT | tuning | calibrated | taker | 261 | 72.80774934 | 0.00000000 | 4507 | 250 | +0.08747802 | +0.06663825 | +0.02083977 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:SOLUSDT | tuning | calibrated | maker | 261 | 182.01937335 | 0.00000000 | 4507 | 250 | +0.08747802 | +0.02665530 | +0.06082272 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:SOLUSDT | tuning | calibrated | charter | 261 | 36.40387467 | 0.00000000 | 4507 | 250 | +0.08747802 | +0.13327651 | -0.04579849 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:SOLUSDT | tuning | frozen3.0 | taker | 130 | 114.86589940 | 0.00000000 | 4107 | 129 | -0.08622160 | +0.06860029 | -0.15482189 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:SOLUSDT | tuning | frozen3.0 | maker | 130 | 287.16474850 | 0.00000000 | 4107 | 129 | -0.08622160 | +0.02744011 | -0.11366171 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:SOLUSDT | tuning | frozen3.0 | charter | 130 | 57.43294970 | 0.00000000 | 4107 | 129 | -0.08622160 | +0.13720057 | -0.22342217 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:SOLUSDT | holdout | calibrated | taker | 180 | 44.48724251 | 0.00000000 | 2198 | 170 | -0.01826370 | +0.09645163 | -0.11471533 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:SOLUSDT | holdout | calibrated | maker | 180 | 111.21810627 | 0.00000000 | 2198 | 170 | -0.01826370 | +0.03858065 | -0.05684435 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:SOLUSDT | holdout | calibrated | charter | 180 | 22.24362125 | 0.00000000 | 2198 | 170 | -0.01826370 | +0.19290327 | -0.21116697 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:SOLUSDT | holdout | frozen3.0 | taker | 73 | 77.82410165 | 0.00000000 | 2153 | 74 | +0.18890490 | +0.09450511 | +0.09439979 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:SOLUSDT | holdout | frozen3.0 | maker | 73 | 194.56025412 | 0.00000000 | 2153 | 74 | +0.18890490 | +0.03780205 | +0.15110285 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:SOLUSDT | holdout | frozen3.0 | charter | 73 | 38.91205082 | 0.00000000 | 2153 | 74 | +0.18890490 | +0.18901023 | -0.00010533 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | ALL | calibrated | taker | 438 | 69.19099204 | 0.00000000 | 6896 | 419 | -0.09690265 | +0.06475088 | -0.16165353 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | ALL | calibrated | maker | 438 | 172.97748011 | 0.00000000 | 6896 | 419 | -0.09690265 | +0.02590035 | -0.12280300 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | ALL | calibrated | charter | 438 | 34.59549602 | 0.00000000 | 6896 | 419 | -0.09690265 | +0.12950175 | -0.22640440 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | ALL | frozen3.0 | taker | 211 | 122.85614281 | 0.00000000 | 5987 | 211 | -0.13550734 | +0.06612832 | -0.20163566 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | ALL | frozen3.0 | maker | 211 | 307.14035702 | 0.00000000 | 5987 | 211 | -0.13550734 | +0.02645133 | -0.16195867 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | ALL | frozen3.0 | charter | 211 | 61.42807140 | 0.00000000 | 5987 | 211 | -0.13550734 | +0.13225664 | -0.26776398 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | tuning | calibrated | taker | 264 | 78.16202837 | 0.00000000 | 4483 | 252 | -0.05374057 | +0.05896125 | -0.11270182 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | tuning | calibrated | maker | 264 | 195.40507092 | 0.00000000 | 4483 | 252 | -0.05374057 | +0.02358450 | -0.07732507 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | tuning | calibrated | charter | 264 | 39.08101418 | 0.00000000 | 4483 | 252 | -0.05374057 | +0.11792250 | -0.17166307 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | tuning | frozen3.0 | taker | 136 | 132.24229227 | 0.00000000 | 3412 | 136 | -0.25742874 | +0.05818948 | -0.31561822 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | tuning | frozen3.0 | maker | 136 | 330.60573067 | 0.00000000 | 3412 | 136 | -0.25742874 | +0.02327579 | -0.28070453 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | tuning | frozen3.0 | charter | 136 | 66.12114613 | 0.00000000 | 3412 | 136 | -0.25742874 | +0.11637896 | -0.37380770 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | holdout | calibrated | taker | 174 | 56.76395762 | 0.00000000 | 2413 | 167 | -0.16618919 | +0.07191667 | -0.23810586 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | holdout | calibrated | maker | 174 | 141.90989405 | 0.00000000 | 2413 | 167 | -0.16618919 | +0.02876667 | -0.19495586 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | holdout | calibrated | charter | 174 | 28.38197881 | 0.00000000 | 2413 | 167 | -0.16618919 | +0.14383333 | -0.31002252 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | holdout | frozen3.0 | taker | 75 | 118.09766996 | 0.00000000 | 2575 | 75 | +0.00000000 | +0.07396001 | -0.07396001 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | holdout | frozen3.0 | maker | 75 | 295.24417491 | 0.00000000 | 2575 | 75 | +0.00000000 | +0.02958400 | -0.02958400 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:NEARUSDT | holdout | frozen3.0 | charter | 75 | 59.04883498 | 0.00000000 | 2575 | 75 | +0.00000000 | +0.14792001 | -0.14792001 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ZECUSDT | ALL | calibrated | taker | 411 | 71.88081937 | 0.00000000 | 7883 | 391 | +0.00989905 | +0.07046334 | -0.06056429 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ZECUSDT | ALL | calibrated | maker | 411 | 179.70204842 | 0.00000000 | 7883 | 391 | +0.00989905 | +0.02818534 | -0.01828629 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ZECUSDT | ALL | calibrated | charter | 411 | 35.94040968 | 0.00000000 | 7883 | 391 | +0.00989905 | +0.14092669 | -0.13102764 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ZECUSDT | ALL | frozen3.0 | taker | 220 | 107.87006659 | 0.00000000 | 6354 | 218 | +0.11770152 | +0.07017917 | +0.04752235 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:ZECUSDT | ALL | frozen3.0 | maker | 220 | 269.67516649 | 0.00000000 | 6354 | 218 | +0.11770152 | +0.02807167 | +0.08962985 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:ZECUSDT | ALL | frozen3.0 | charter | 220 | 53.93503330 | 0.00000000 | 6354 | 218 | +0.11770152 | +0.14035834 | -0.02265682 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ZECUSDT | tuning | calibrated | taker | 264 | 67.09527476 | 0.00000000 | 5171 | 251 | +0.02943456 | +0.07390273 | -0.04446817 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ZECUSDT | tuning | calibrated | maker | 264 | 167.73818690 | 0.00000000 | 5171 | 251 | +0.02943456 | +0.02956109 | -0.00012653 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ZECUSDT | tuning | calibrated | charter | 264 | 33.54763738 | 0.00000000 | 5171 | 251 | +0.02943456 | +0.14780545 | -0.11837089 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ZECUSDT | tuning | frozen3.0 | taker | 141 | 103.71141172 | 0.00000000 | 4017 | 141 | +0.15070691 | +0.07406004 | +0.07664687 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:ZECUSDT | tuning | frozen3.0 | maker | 141 | 259.27852931 | 0.00000000 | 4017 | 141 | +0.15070691 | +0.02962401 | +0.12108290 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:ZECUSDT | tuning | frozen3.0 | charter | 141 | 51.85570586 | 0.00000000 | 4017 | 141 | +0.15070691 | +0.14812007 | +0.00258684 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:ZECUSDT | holdout | calibrated | taker | 147 | 80.58252427 | 0.00000000 | 2712 | 141 | -0.02198472 | +0.06537751 | -0.08736223 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ZECUSDT | holdout | calibrated | maker | 147 | 201.45631068 | 0.00000000 | 2712 | 141 | -0.02198472 | +0.02615100 | -0.04813572 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ZECUSDT | holdout | calibrated | charter | 147 | 40.29126214 | 0.00000000 | 2712 | 141 | -0.02198472 | +0.13075502 | -0.15273974 | holds | fails | — | FAIL | FAIL | yes |
|  | ASSET:ZECUSDT | holdout | frozen3.0 | taker | 79 | 113.71009640 | 0.00000000 | 2337 | 78 | +0.07299762 | +0.06467705 | +0.00832057 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:ZECUSDT | holdout | frozen3.0 | maker | 79 | 284.27524101 | 0.00000000 | 2337 | 78 | +0.07299762 | +0.02587082 | +0.04712680 | holds | holds | — | PASS | PASS | yes |
|  | ASSET:ZECUSDT | holdout | frozen3.0 | charter | 79 | 56.85504820 | 0.00000000 | 2337 | 78 | +0.07299762 | +0.12935410 | -0.05635648 | holds | fails | — | FAIL | FAIL | yes |

Block tally (all 108 rows, the ★ row included; the others Tier-E, a SELECTION, not a result): would_read FAIL 66, PASS 42; agrees with R2 on 108/108 rows.

## 5 · Disclosures

- **The pooled holdout median H20 term prints +0.00000000. The gate state does not depend on its exact value; the verdict word does.** A pooled median lies within the range of its members' medians (up to the averaging of two middle values), here [ASSET:NEARUSDT -0.16618919, ASSET:ETHUSDT +0.11620715]. Each pooled edge toll is the binding (largest) member toll.
  - the record row (the gate): toll +0.16760525 ATR, above every member's median, so the taker edge net is negative for any value the pooled median could take.
  - the maker twin (the reopening path, L-R.4): toll +0.06704210 ATR, below the medians of ETHUSDT +0.11620715, BTCUSDT +0.08150832: a pooled median in (+0.06704210, +0.11620715] would have made the maker twin PASS, and the verdict of record would have read 'FAIL — maker twin PASSES (the reopening path; needs a toll-model change the operator rules)'. The verdict WORD therefore rests on the printed pooled value, not only on its sign.
  - the charter twin (Tier-E): toll +0.23464735 ATR, above every member's median, so the charter edge net is negative for any value the pooled median could take.
- **The printed pooled median is exactly +0.00000000, verified from raw bars (cited, not computed here).** This runner is range-free and reads the median as Stage R printed it. The Stage S verifier's independent re-derivation from the raw 1h klines (2026-09-25, re-run at this repair; ATR re-computed, the range machine supplying only the confirmed-range list at the filed pick) reproduced the record row exactly: n 12044 over 771 ranges, 6012 negative, 15 exactly-zero and 6017 positive H20 terms. Both middle order statistics (0-based indices 6021 and 6022) fall in the zero block, so the median is 0.0 exactly (zeros by member: NEARUSDT 10, ZECUSDT 4, SOLUSDT 1, BTCUSDT 0, ETHUSDT 0).
- Members at the record cell (Tier-E): ASSET:BTCUSDT median +0.08150832 · toll +0.16760525 · net -0.08609693 · FAIL; ASSET:ETHUSDT median +0.11620715 · toll +0.11394882 · net +0.00225833 · PASS; ASSET:SOLUSDT median -0.01826370 · toll +0.09645163 · net -0.11471533 · FAIL; ASSET:NEARUSDT median -0.16618919 · toll +0.07191667 · net -0.23810586 · FAIL; ASSET:ZECUSDT median -0.02198472 · toll +0.06537751 · net -0.08736223 · FAIL.
- **Holdout scale.** The record row's scale is the tuning-era pick, out of sample on the holdout (OUT-OF-SAMPLE (holdout; the causal slice of a tuning pick)); stability-changed members: BTCUSDT,SOLUSDT,NEARUSDT.
- **Provenance.** The JSON of record is the file the scorer reads for P-SCALP-2 (SC-17). R2_FEASIBILITY.parquet's content sha equals Stage R's build_manifest, and the manifest's 1h lens word is `FAIL`.

## 6 · Not built, and why

- **STEP 2, the L-S.2 scalper, is not built.** L-S.1 runs it only on a 1h PASS. Not built: the scored arm (holdout, vs zero, taker), the Tier-E arms (maker fill-assumed, maker fill-conditioned, the 17-asset view, the regime gate of 5m ATR tercile × 1h boundary-age tercile, the tuning slice, the frozen-3.0 twin), the refused-entry counts, and the (target − entry)/(entry − stop) distribution.
- **F-SCALP and F-SCALP-ASOF are not run.** They test a book that does not exist. F-SCALP-GATE, F-GRID, F-KEY and F-DET are run (`FIXTURES_STAGE_S.txt`).
- **The open path [SS-4].** On a 1h verdict of record of `PASS`, this runner halts with GATE-OPEN and writes nothing — only after the cross-file checks [SS-5] pass, so only on a PASS the JSON, R2_FEASIBILITY.parquet and Stage R's manifest agree on (a PASS in the JSON alone halts R2-MANIFEST or JSON-PARQUET). It never files CLOSED on a PASS, and a PASS must re-dispatch Stage S STEP 2.
- **Findings not fixed.** The 1h lens is closed for range trading in this and every later tier unless the operator changes the toll model [contract R2]. The maker twin at the record cell reads FAIL, so no reopening path is open.

## 7 · Lean block

- [LEAN-HEPHAESTUS] L-S.1 the precondition: the R2 lens verdict of record at 1h (CLASSIC5 pooled, holdout, calibrated, taker) == PASS, else 'CLOSED BY R2 (1h: <verdict>)' and STOP — no book, no twin, no Tier-E arm; the tuning-era word printed beside, Tier-E [§10].
- [LEAN-HEPHAESTUS] L-R.4 the [Q-R3] law typed here: height n_ranges >= 30, ratio_median >= 3.0, share_ratio_lt_1 <= 0.10; edge edge_n_ranges >= 30, edge_n >= 30, edge_net_h20 > 0; both legs; under a floor -> 'FAIL (provisional, n<30)'; taker FAIL + maker PASS -> the reopening-path word.
- [LEAN-HEPHAESTUS] SS-1 the gate re-derives the JSON of record's 1h word from its printed columns; a label that disagrees with its columns HALTs LABEL-LAW; a row that is not the verdict of record (pool / era / scale / toll, the record block, members == CLASSIC5, fallback_members within CLASSIC5) HALTs RECORD-SPEC.
- [LEAN-HEPHAESTUS] SS-2 the printed net must be round(round(median,8) - round(toll,8), 8) exactly (NET-ARITH).
- [LEAN-HEPHAESTUS] SS-3 the gate opens only on the exact word 'PASS'; the reason prints the verdict of record verbatim.
- [LEAN-HEPHAESTUS] SS-4 on a PASS this runner HALTs GATE-OPEN and writes nothing (STEP 2, the L-S.2 scalper, is built only on a PASS — re-dispatch) — only after SS-5 passes.
- [LEAN-HEPHAESTUS] SS-5 before acting on the gate, on both paths: JSON row == R2_FEASIBILITY record row, the parquet's content sha and 1h word == Stage R's manifest, the maker / charter / tuning / ALL words == this stage's re-derivation, every block row's word and collar == the law's.
- [LEAN-HEPHAESTUS] SS-6 S_R2_1H.parquet = the whole 1h CLASSIC5 R2 block (108 cells), re-derived, would_read only; every row but the record row collared Tier-E (gates nothing), the record row carrying Stage R's record collar verbatim [L-1.4].
- [LEAN-HEPHAESTUS] SS-7 a CLOSED registration holds no arm: regbooks/P-SCALP-2 holds STATUS.json only (STRAY-BOOK HALT otherwise).

## 8 · Repair log (2026-09-25, the Stage S verifier's report)

- Verifier verdict: the stage's result holds (CLOSED BY R2 (1h: FAIL), no book); 0 BLOCKER, 0 MAJOR, 4 MINOR implementation / report defects, 7 MINOR fixture gaps. No rule moved after a number: the gate, its words, S_GATE.json and STATUS.json are unchanged by the repair.
- D1 FIXED — the ★ row of S_R2_1H carried the Tier-E collar ('gates nothing'), against L-1.4 ('every R2 row except the lens verdict of record'). It now carries Stage R's record collar verbatim; every block row's collar is checked against the typed pair (R2-COLLAR).
- D2 FIXED — the cross-file checks (SS-5) ran on the CLOSED path only, so a PASS printed in the JSON alone reached GATE-OPEN. They now run before the gate is acted on; GATE-OPEN fires only on a PASS the JSON, the parquet and Stage R's manifest agree on.
- D3 FIXED — §5 said the result did not depend on the exact pooled median. True of the gate state, false of the verdict word: a pooled median above the maker twin's binding toll would have read the reopening-path word. Reworded, and the raw-bar zero block cited.
- D4 FIXED IN PART — RECORD-SPEC now requires the CLASSIC5 member set and a fallback_members list within CLASSIC5. NOT required: an empty fallback_members (L-R.2 keeps a whole-tape fallback pick as the calibrated scale of record, labelled IN-SAMPLE; Stage R's own 1w verdict of record pools five fallback members).
- F1-F7 CLOSED in the fixtures: plants for an edge_n_ranges-only floor, the charter and ALL words, each of the 21 JSON / parquet field pairs, a net off by 1e-8, a second flagged row, a stray scored.json; the transcript root-independent; the F-DET plant labels name what they compare. The block-level record-flag check has no plant of its own: the flagged-count check implies it (an equivalent mutant).
