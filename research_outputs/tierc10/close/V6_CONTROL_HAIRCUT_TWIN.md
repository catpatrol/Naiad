# V6 CONTROL · HAIRCUT TWIN — an ADDED column (book level)

**REPORT-ONLY · Tier-E · v6 control haircut twin (ADDED column).** No CI, no p, no verdict is computed or printed here; nothing on this page is scored and no registration's verdict is read.

**Clause of record** — `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md`:53-55 (sha256 `8a0bf279bcab0f27161a7d965535445807f4e713e77d045b0ba124bc7f803c7a`): *"The 5-asset control's TC-series accounting stays untouched; its twin is an ADDED column."*

**As of** 2026-09-21T16:00:00Z (the journal's own stamp; bars stamped after it are not read — this file reads no bars).

## Law

- **TC-series (untouched):** panel/control_journal.parquet net_r, mean, verbatim — the TC-series accounting of record, untouched. The toll it carries, `round_trip_bps_used`, is printed beside every row from `data/fee_schedule.json`, unchanged.
- **Haircut twin (ADDED):** per campaign `tierc10_data.haircut_twin_net_r (as filed)` with `risk_px = r_dist`. Cost law, quoted from `data/fee_schedule.json` `haircut_twin_law`: *ADDED, never a replacement: haircut_twin_* keys carry the charter model (per-side taker fee + the charter's per-side slippage tier) beside round_trip_bps_used, which stays the TC-series accounting figure on every row [VETO 'tiers']. twin cost_px = ((FEE_BPS_SIDE + slippage_bps_side) / 10_000) * (entry_px + exit_px); net_r_twin = gross_r - cost_px / risk_px (tierc10_data.haircut_twin_net_r)*
- **Companion:** `twin - funding_r — NOT the filed twin`. The filed twin charges fee + charter slippage and NO funding; the TC-series net_r charges funding. The companion is printed so the two can be read on one footing; it is NOT the filed twin.
- **Eras:** `tierc10_panel.era_window` — a campaign is in an era iff its `entry_ms` is (cut `2024-06-30T23:59:59Z`). The era rows split the ONE full-corridor control book; they are not separate rides.
- **Sign flags:** `sign_disagrees` = sign(twin) ≠ sign(TC); `companion_sign_disagrees` = sign(companion) ≠ sign(TC).

## Tiers (read from `data/fee_schedule.json`)

| stem | asset | tier | slippage bps/side | charter bps/side | charter round trip bps | TC-series round trip bps (untouched) |
|---|---|---|---:|---:|---:|---:|
| BTCUSDT | BTC | A | 2 | 7 | 14 | 10 |
| ETHUSDT | ETH | A | 2 | 7 | 14 | 10 |
| NEARUSDT | NEAR | B | 5 | 10 | 20 | 10 |
| SOLUSDT | SOL | B | 5 | 10 | 20 | 10 |
| ZECUSDT | ZEC | B | 5 | 10 | 20 | 10 |

## Era `full` — the full corridor

*REPORT-ONLY · Tier-E · v6 control haircut twin (ADDED column) · CLASSIC5 · era full.* R units, per campaign.

| key | asset | tier | charter bps/side | n | TC-series expectancy R (untouched) | haircut twin R (ADDED) | twin − TC R | companion R (NOT the filed twin) | twin sign ≠ TC | companion sign ≠ TC |
|---|---|---|---:|---:|---:|---:|---:|---:|:-:|:-:|
| BTCUSDT | BTC | A | 7 | 39 | -0.126742 | -0.115436 | +0.011305 | -0.148491 | no | no |
| ETHUSDT | ETH | A | 7 | 48 | +0.145862 | +0.175217 | +0.029355 | +0.131589 | no | no |
| NEARUSDT | NEAR | B | 10 | 40 | -0.039190 | -0.045286 | -0.006096 | -0.060217 | no | no |
| SOLUSDT | SOL | B | 10 | 36 | +0.270521 | +0.279882 | +0.009362 | +0.247858 | no | no |
| ZECUSDT | ZEC | B | 10 | 37 | +0.851723 | +0.844793 | -0.006929 | +0.826811 | no | no |
| ALL | A:BTC,ETH · B:NEAR,SOL,ZEC | A\|B | mixed | 200 | +0.208717 | +0.217150 | +0.008434 | +0.188157 | no | no |

## Era `tuning` — entries <= `2024-06-30T23:59:59Z`

*REPORT-ONLY · Tier-E · v6 control haircut twin (ADDED column) · CLASSIC5 · era tuning.* R units, per campaign.

| key | asset | tier | charter bps/side | n | TC-series expectancy R (untouched) | haircut twin R (ADDED) | twin − TC R | companion R (NOT the filed twin) | twin sign ≠ TC | companion sign ≠ TC |
|---|---|---|---:|---:|---:|---:|---:|---:|:-:|:-:|
| BTCUSDT | BTC | A | 7 | 26 | -0.468208 | -0.442146 | +0.026062 | -0.488706 | no | no |
| ETHUSDT | ETH | A | 7 | 29 | -0.006406 | +0.054767 | +0.061173 | -0.019956 | YES | no |
| NEARUSDT | NEAR | B | 10 | 23 | -0.258726 | -0.255816 | +0.002911 | -0.279791 | no | no |
| SOLUSDT | SOL | B | 10 | 23 | +0.631394 | +0.655377 | +0.023983 | +0.609517 | no | no |
| ZECUSDT | ZEC | B | 10 | 22 | +0.112000 | +0.113655 | +0.001655 | +0.088537 | no | no |
| ALL | A:BTC,ETH · B:NEAR,SOL,ZEC | A\|B | mixed | 123 | -0.010763 | +0.014494 | +0.025257 | -0.030517 | YES | no |

## Era `holdout` — entries > `2024-06-30T23:59:59Z`

*REPORT-ONLY · Tier-E · v6 control haircut twin (ADDED column) · CLASSIC5 · era holdout.* R units, per campaign.

| key | asset | tier | charter bps/side | n | TC-series expectancy R (untouched) | haircut twin R (ADDED) | twin − TC R | companion R (NOT the filed twin) | twin sign ≠ TC | companion sign ≠ TC |
|---|---|---|---:|---:|---:|---:|---:|---:|:-:|:-:|
| BTCUSDT | BTC | A | 7 | 13 | +0.556192 | +0.537984 | -0.018208 | +0.531940 | no | no |
| ETHUSDT | ETH | A | 7 | 19 | +0.378271 | +0.359062 | -0.019209 | +0.362895 | no | no |
| NEARUSDT | NEAR | B | 10 | 17 | +0.257830 | +0.239548 | -0.018282 | +0.236854 | no | no |
| SOLUSDT | SOL | B | 10 | 13 | -0.367947 | -0.384454 | -0.016507 | -0.392001 | no | no |
| ZECUSDT | ZEC | B | 10 | 15 | +1.936649 | +1.917129 | -0.019519 | +1.909612 | no | no |
| ALL | A:BTC,ETH · B:NEAR,SOL,ZEC | A\|B | mixed | 77 | +0.559314 | +0.540874 | -0.018440 | +0.537466 | no | no |

## Cross-check beside — the twin already filed on P-TRG-2's row

`scores/P-TRG-2.rows.json` carries `beside.haircut_twin` with the v6 base's twin as `twin_expectancy_r − twin_difference_r` (fields read: `arm`, `score_row.arm_era`, `score_row.arm_base`, `beside.haircut_twin.*`; no verdict, CI, p or LOAO field). The ALL rows here must reproduce it. The journal is filed at **6 dp** (measured), so the tolerance is the propagated half-unit bound, not 1e-12 — see the finding below. P-TRG-2's era bases were ridden over their own era windows (tierc10_score: 'never a full-corridor control filtered afterwards'); the n and residual columns below show whether the split of the one book reproduces them.

| era | n here | P-TRG-2 base_n | twin here | P-TRG-2 base twin | abs(Δ) | bound | abs(Δ) ≤ 1e-12 (literal) |
|---|---:|---:|---:|---:|---:|---:|:-:|
| full | 200 | 200 | +0.217150460240 | +0.217150450669 | 9.572e-09 | 5.630e-07 | no |
| tuning | 123 | 123 | +0.014494025339 | +0.014494013868 | 1.147e-08 | 5.672e-07 | no |
| holdout | 77 | 77 | +0.540874375733 | +0.540874369194 | 6.538e-09 | 5.562e-07 | no |

Same residual on the untouched TC-series column and on the companion (the rounding is in the journal, not in the twin):

| era | TC here | P-TRG-2 base TC | abs(Δ) | bound | companion here | P-TRG-2 base companion | abs(Δ) | bound |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| full | +0.208716755000 | +0.208716747416 | 7.584e-09 | 5.000e-07 | +0.188156500240 | +0.188156503352 | 3.112e-09 | 1.063e-06 |
| tuning | -0.010762772358 | -0.010762779607 | 7.250e-09 | 5.000e-07 | -0.030517015312 | -0.030517003313 | 1.200e-08 | 1.067e-06 |
| holdout | +0.559313922078 | +0.559313913959 | 8.119e-09 | 5.000e-07 | +0.537466141967 | +0.537466130883 | 1.108e-08 | 1.056e-06 |

## Findings (not fixed here)

- **F-VT-REUSE-TOL.** The build spec's reuse tolerance, 1e-12, cannot be met from the filed journal: `tierc5.journal_frame` files price and R columns at 6 dp (`r6`), while P-TRG-2's base rode at full precision in memory. The leg asserts the derived bound and prints the literal comparison beside it, un-asserted. For the auditor to ratify.
- **F-VT-TC-PRECISION.** `panel/control_headline.parquet` files `expectancy_r` at 4 dp (`r4`, `scripts/tierc5.py:562`). F-VT-TC compares to it at that precision and holds the exact figure against the sha-verified journal instead; the transcript names which clause catches the 1e-9 sabotage.

## Inputs (sha held against PROGRESS.json)

| input | PROGRESS stage | bytes | sha256 |
|---|---|---:|---|
| `research_outputs/tierc10/panel/control_journal.parquet` | PANEL/gate | 70102 | `fcbf5db0480416b0a5c7f704987980aea220650cb0764d5dd4095611fae64c1c` |
| `research_outputs/tierc10/panel/control_headline.parquet` | PANEL/gate | 31449 | `602b10ef525a829d1b0c6267949243c092e732e33faa173b21bbb21eec1c3e20` |
| `research_outputs/tierc10/data/fee_schedule.json` | D-CORE | 23925 | `3a18b84e0211110b69eb09661b7e9a39db08f41c69ebdc4cc8ca8eb54a07e5cc` |
| `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` | D-CORE | 405715 | `de2e8663bbf101dfb46ad9f77a4969ca73648e78373646c0d17b81b9f9a87421` |
| `research_outputs/tierc10/scores/P-TRG-2.rows.json` | B-CORE | 102709 | `9fa07a0fa1b832ef7a1012a796cfd7fdd73ab2e1275d4faa4340666493c340c8` |

Fixtures: `research_outputs/tierc10/close/FIXTURES_CLOSE_v6_control_twin.txt` (script `scripts/tierc10_close_v6_control_twin.py`).
