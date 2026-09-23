# P-TRG-2 · THE SEEN SHARE — REPORT-ONLY — TIER-E — NEVER SCORED

*Built by `scripts/tierc10_close_p_trg_2_seen_share.py`. It rides P-TRG-2's scored arm to its Book through the registration's own door, as the pinned dry-run does, and splits the book at TIER-C9's as-of. It computes counts and sums only: no CI, no p, no verdict. `TP.score`, `finish_family`, `register` and `_mark_scored` are never referenced (F-SS-CLOSURE).*

## The claim, as worded by the builder

196 of the 198 campaigns of P-TRG-2's scored book ENTERED AT OR BEFORE TIER-C9's as-of (2026-08-22T00:00:00Z); their count, net_r, gross_r, fee_r, funding_r, best_r and win rate EQUAL the TIER-C9 grid row for trigger-9/12 at its 4-dp precision, and their key overlap with TIER-C9's FILED v6 journal equals the grid's shared / cell-only / base-only. TIER-C9 filed no per-campaign trigger-9/12 journal, so this is an aggregate-and-overlap match, not a key-for-key match against a TC9 9/12 book.

## The book

- Arm: `trg-9/12 vs card v6 · CLASSIC5 · full` · window 2019-09-08T16:00:00Z → 2026-09-21T16:00:00Z.
- n 198, Σ net_r +92.3499 R. Exit reasons: bell_12_89 7, stop 191.
- Book sha256 `b2276fa487119ef12a8e0434e54f9b77efbfb7ee387b3cb35d2955043c371a8f`. Dry-run pin (`scores/DRYRUN.json arms[11].book_sha`) equal: True. Scored row (`scores/P-TRG-2.rows.json rows[0].score_row.book_sha256`) equal: True.
- TIER-C9's as-of: 2026-08-22T00:00:00Z (research_outputs/tierc9/build_manifest.json .as_of == research_outputs/tierc9/sweep_grid.parquet as_of_last_closed_4h).

## The split at TIER-C9's as-of

| side | n | Σ net_r (R) |
|---|---:|---:|
| AT-OR-BEFORE-TC9-ASOF | 196 | +94.3989 |
| AFTER-TC9-ASOF | 2 | -2.0490 |
| open across the as-of | 0 | — |

**The AFTER campaigns (the unseen month):**

| asset | dir | entered | exited | exit | net_r |
|---|---|---|---|---|---:|
| ZECUSDT | 1 | 2026-08-27T20:00:00Z | 2026-08-28T12:00:00Z | stop | -1.025848 |
| ETHUSDT | 1 | 2026-08-30T16:00:00Z | 2026-08-30T20:00:00Z | stop | -1.023195 |

**Per asset (at-or-before / after):** BTCUSDT 40/0 · ETHUSDT 47/1 · NEARUSDT 39/0 · SOLUSDT 34/0 · ZECUSDT 36/1

## Held against TIER-C9's grid row for trigger-9/12 (`research_outputs/tierc9/sweep_grid.parquet`)

| field | at-or-before, here | TC9 grid row | equal at 4 dp |
|---|---:|---:|---|
| n | 196 | 196 | True |
| net_r | 94.3989 | 94.3989 | True |
| gross_r | 106.2883 | 106.2883 | True |
| fee_r | 6.1309 | 6.1309 | True |
| funding_r | 5.7584 | 5.7584 | True |
| best_r | 24.8061 | 24.8061 | True |
| win_rate_pct | 40.3061 | 40.3061 | True |

**Key overlap with TIER-C9's FILED v6 journal** (`research_outputs/tierc9/trade_journal_control.parquet`, key asset · lane · entry_ms):

| count | here | TC9 grid row | equal |
|---|---:|---:|---|
| shared (n_shared) | 19 | 19 | True |
| cell_only (n_cell_only) | 177 | 177 | True |
| base_only (n_base_only) | 177 | 177 | True |

TIER-C9 journals on disk: `trade_journal_control.csv`, `trade_journal_control.parquet`, `trade_journal_p_trg_1.parquet`. None is a trigger-9/12 book, so no key-for-key match against one is possible.

## The R1 era cut (2024-06-30T23:59:59Z)

- Book campaigns after the cut: 66; of those, entered at or before TIER-C9's as-of: 64.
- v6 base campaigns after the cut: 77; of those, at or before TIER-C9's as-of: 73.

## The v6 base, held against TIER-C9's filed v6 journal

- Here, at or before the as-of: n 196, Σ net_r +38.7901. TIER-C9 filed: n 196, Σ net_r +38.8044.
- Campaigns on both sides: 196; on one side only: 0.
- Carried by funding_r alone (gross_r and fee_r exact): ZECUSDT 2026-08-17T04:00:00Z, funding_r 0.0 → 0.014324, net_r -1.039899 → -1.054223.
- Unattributed differences: 0.
- F-CTRL/b's line (`research_outputs/tierc10/panel/FIXTURES_PANEL.txt:34`): `[NB ] FILED tierc9/trade_journal_control: funding_r moved on 1 closed campaign(s) — ZECUSDT 2026-08-17T04:00:00Z: funding_r 0.0 -> 0.014324, net_r -1.039899 -> -1.054223 [ATTRIBUTION: the referee rode on funding stale at 2026-08-15; Stage D's top-up supplied the stamps. Substrate drift, not code.]`
- v6 after the as-of (the forward strip's window): 4 campaigns.

## Sources read this run (sha256 · bytes)

- `research_outputs/tierc10/PROGRESS.json` · `0d66f2d7fe6c338339880368ff854e58bbb2533be54cf2f7448f71d129752afc` · 267607
- `research_outputs/tierc10/REGISTRATION_TEXTS.json` · `3afce077146807127072ae68f9c816e0263505aa625cf1610763ea37eb91ca94` · 178729
- `research_outputs/tierc10/REGISTRY_PIN.json` · `4facddb8b6d2ee0017cccb46fc59187494af5591b8760b0245507c6621f17244` · 2897
- `research_outputs/tierc10/panel/FIXTURES_PANEL.txt` · `163f65bdf21a575ccc4bba8c70dd6949e88aa0d91a20abdcd726f4fbaab54642` · 63265
- `research_outputs/tierc10/panel/control_journal.parquet` · `fcbf5db0480416b0a5c7f704987980aea220650cb0764d5dd4095611fae64c1c` · 70102
- `research_outputs/tierc10/scores/DRYRUN.json` · `13958abb0c75ee2cfaa8bf2df9d0f7569bbb286d85fa49a32339d8b90c15672c` · 77280
- `research_outputs/tierc10/scores/P-TRG-2.rows.json` · `9fa07a0fa1b832ef7a1012a796cfd7fdd73ab2e1275d4faa4340666493c340c8` · 102709
- `research_outputs/tierc9/build_manifest.json` · `4b39053ec87d4317e196a7d04d8fa77353b4b056e0bdfcab3f2668af86ebdc78` · 10919
- `research_outputs/tierc9/sweep_grid.parquet` · `6246de7a2704ef9df88a8eec56cb67a2a678265230148f59c6c1a888753afd35` · 40012
- `research_outputs/tierc9/trade_journal_control.parquet` · `bb630003a313d62f5fa04895d9288deb80e265dffafa2267365cabf0bc14f1d8` · 66511

*The per-campaign list (all 198 campaigns: asset, lane, direction, entry_ms, entry_ts, exit, exit reason, net_r, side) is in `P_TRG_2_SEEN_SHARE.json` under `campaigns`.*
