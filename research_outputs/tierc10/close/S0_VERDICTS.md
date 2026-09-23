<!-- S0_VERDICTS.md · TIER-C10 CLOSE §0 fragment · built by scripts/tierc10_close_close_s0_verdicts.py · splice over BUILD_DRAFT.md "## 0 · VERDICTS" at CLOSE; this script never edits BUILD_DRAFT.md -->
## 0 · VERDICTS

> **REPORT-ONLY TRANSCRIPTION.** Every value in this section is copied string-for-string, at source precision, from the file and field that `S0_VERDICTS.json` records beside it; F-S0-READ re-reads each one. Nothing here is scored, re-scored, rounded or re-chosen. The verdicts are those of record: `scores/<REG>.rows.json` (the one arm with `scored_in_family` true — its `score_row` and its `beside`) and `scores/FAMILY.json` (`clears_bh_bar`).

Corridor as-of of record `2026-09-21T16:00:00Z` · registry len `6` · registry head `7621a85727969299eb03a481fdf4a61e5455177762286a29695e7d9347d651cd` · seed `20260921` (`REGISTRY_PIN.json`).

### 0.1 · Six registered rows, in order of filing

*REPORT-ONLY — one row per registration, its scored arm only; the Tier-E arms stay in `scores/<REG>.rows.json` and gate nothing.*

| # | registration | prior | arm | panel | era | ruler | n | point | [CI lo, CI hi] | p (one-sided) | verdict | clears BH bar | LOAO above / present vs bar · line | haircut twin E[R] | height-vs-toll (BRK) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `1` | P-GEN-1 | `45`% | unseen12-card-v6 | UNSEEN12 | full | VS ZERO (one-sample asset-cluster) | `286` | `0.099777` | [`-0.154991`, `0.315921`] | `0.271682` | **NOT SUPPORTED** | `false` | `0/12` vs bar `7` · 0/12 above | `0.08460102968246902` | — |
| `2` | P-SPR-2 | `45`% | standalone vs zero · full corridor | CLASSIC5 | full | VS ZERO (one-sample asset-cluster) | `261` | `-0.00593` | [`-0.174617`, `0.165338`] | `0.56036` | **NOT SUPPORTED** | `false` | `0/5` vs bar `3` · 0/5 above | `-0.024325017149030344` | — |
| `3` | P-BE-1 | `40`% | be-floor-1R vs card-v6 (CLASSIC5, full) | — | — | — | — | — | — | — | HALT: P-BE-1 — the arm shares the WHOLE campaign set with its base; the commissioned two-sample ruler's premise failed. File a NEW id under ruler='set_change' and disclose. | — | — | — | — |
| `4` | P-TRG-2 | `40`% | trg-9/12 vs card v6 · CLASSIC5 · full | CLASSIC5 | full | TWO-SAMPLE (the arm CHANGES the campaign set) | `198` | `0.257697` | [`0.108587`, `0.383892`] | `0.005249` | **SUPPORTED** | `true` | `5/5` vs bar `3` · 5/5 above | `0.47558820524675305` · Δ `0.2584377545781942` | — |
| `5` | P-BRK-I1 | `35`% | CLASSIC5-memory-line | CLASSIC5 | full | VS ZERO (one-sample asset-cluster) | `7` | `0.71827` | [`-0.602912`, `1.452261`] | `0.269683` | **NOT SUPPORTED** | `false` | `1/3` vs bar `3` · 1/5 above | `0.8946008804619946` | 1d · verdict_pass `true` · era ALL: height gate PASS + edge-fade leg PASS |
| `6` | P-BRK-S1 | `30`% | P-BRK-S1 vs zero | CLASSIC5 | holdout | VS ZERO (one-sample asset-cluster) | `1836` | `-0.211069` | [`-0.298366`, `-0.144105`] | `1.0` | **NOT SUPPORTED** | `false` | `0/5` vs bar `3` · 0/5 above, 5/5 BELOW | `-0.3727569778166333` | 5m · verdict_pass `false` · era holdout: height gate PASS + edge-fade leg FAIL |

**Beside the table**

- **m = `6` declared / `5` run** — N counts the FAMILY.json rows whose `clears_bh_bar` is not null. One fixed bar q/m = `0.016666666666666666` (FAMILY.json `fdr_bar_q_over_m`), no step-up.
- `clears_bh_bar` is `true` on: **P-TRG-2**.
- FAMILY.json `law`: TP.finish_family over every row of the six rows files; clears_bh_bar is a SEPARATE column beside the CI verdict
- **P-BE-1** HALTed at `TP.score`: its row prints FAMILY.json `scored_slots_halted` verbatim and no point, CI or p. Its Tier-E arms are report-only and are not in §0. The filed text, as the rows file carries it: “If A1's two-sample premise fails and A1 HALTs, there is no report-only row on the same population to read instead; a new id must be filed under `set_change` and the reason disclosed.”
- **Haircut twin** (`beside.haircut_twin.twin_expectancy_r`; the two-sample row adds `twin_difference_r` as Δ): HAIRCUT TWIN — an ADDED column beside the TC-series toll, never a replacement; the verdict, CI, p and LOAO are the TC-series row's [VETO 'tiers']
- **P-BRK-I1** LOAO: `3` assets present of `5` declared panels; zero-campaign assets `NEARUSDT,ZECUSDT`; the line of record reads `1/5 above` — dropping an asset with no campaign reproduces the headline; such a panel is counted by the line (N = the DECLARED panel, the lineage's law) and EXCLUDED from loao_above_excl_zero_campaign_panels — both printed; where they disagree the row says so here.
- **P-BRK-S1** toll: PRINT, NOT A DEDUCTION — reported, not changed. The contract reads 'NET OF MEASURED 5m TOLL'; today's net_r is net of FEE and FUNDING only. Authority: a CONTRACT READING. Not changed on executor authority; the operator settles it. Until then the toll is printed on every row, labelled, and the row says it is a print.

#### LAW 3's beside-print — empty, by fact

LAW 3 — `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` lines 16–18:

```text
 3 · registration texts below are FROZEN since 2026-09-21; any verdict the
     interrupted run computed is re-computed and printed BESIDE the fresh value —
     never re-worded, never re-chosen.
```

**Empty by fact, not by omission.** The interrupted run filed no registration, so it computed no verdict: there is nothing to re-compute and print beside the six fresh rows. The record — `BUILD_DRAFT.md` §R0.1, lines 402–403:

> - `draft:registrations`: **no registration text had been drafted, for any of the six lanes.**
>   `research_outputs/tierc10/registrations/` did not exist, and Stage B had not begun.

#### The superseded draft and the supersession of record

*Quoted verbatim from `REGISTRATION_TEXTS.json`; the texts are frozen and nothing here re-words them.*

**P-SPR-2 — superseded draft** — `P-SPR-2.text` characters 2369–2901:

> THE SUPERSEDED DRAFT, printed so the change is visible and not silent. The RESUME contract of 2026-09-22 (exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md, §B) carries P-SPR-2 as: "sharpened spring = deviation-confirm at a CONFIRMED macro boundary, 4h, 5-asset exploration-classic, vs card/standalone" (:94-95; the contract wraps that sentence over two indented lines and the wrap is closed up here — no word is added, removed or reordered). That wording is SUPERSEDED. R3 is later than the contract's frozen text and R9 confirms it.

**P-BRK-I1 — R8 supersedes R2** — `P-BRK-I1.text` characters 1246–2133:

> WHY CLASSIC5, AND THE SUPERSESSION, ON THE RECORD. Operator ruling R8 of 2026-09-22 — "5-asset
> book — the PANEL PIN governs" — SUPERSEDES operator ruling R2 of 2026-09-21 — "All 17" — on the
> operator's own word. Both are filed verbatim in research_outputs/tierc10/OPERATOR_RULINGS.md.
> The RESUME contract of 2026-09-22 (exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:107) carries
> a PANEL PIN reading "both BRK forms score on the 5-asset book per G-7; the 17-asset view is
> Tier-E", and requires the gap against R2 to be filed as a finding rather than silently resolved.
> IT IS FILED HERE, IN THE REGISTRATION ITSELF: this form scores on CLASSIC5 and NOT on the
> seventeen, because R8 says so; the seventeen ride as a report-only arm (§7).
> scripts/tierc10_brk.py scores on whatever panel the registration names (g["panel"]), so this is
> a registration-text decision and no code moved for it.

**P-BRK-S1 — R8 supersedes R2** — `P-BRK-S1.text` characters 1213–1843:

> The scored panel is CLASSIC5 = (BTCUSDT, ETHUSDT, SOLUSDT, NEARUSDT, ZECUSDT), per operator ruling R8 of 2026-09-22 ("5-asset book — the PANEL PIN governs"). R8 SUPERSEDES ruling R2 of 2026-09-21 ("All 17") on the operator's own word, and that supersession is recorded here so the change is visible and not silent. The seventeen-asset view — CLASSIC5 plus ENAUSDT, PUMPUSDT, HYPEUSDT, MNTUSDT_BYBIT, SUIUSDT, LTCUSDT, XMRUSDT, BNBUSDT, UNIUSDT, 1000PEPEUSDT, DOGEUSDT, 1000BONKUSDT — is filed as a Tier-E arm beside the scored row. It is a view. It owns no slot in m and may never be promoted to evidence, whichever way it prints.

### 0.2 · The admitted list

*REPORT-ONLY — transcribed from `data/STAGE_D_MANIFEST.json` `admission` and `panels`; it printed before any scoring and is P-GEN-1's panel.*

- Admission rule (`admission.rule`): >= TIDE_SLOW (316) + MEM_TTL_BARS (400) = 716 closed 4h bars
- Excluded: none — `admission.excluded` is empty

Why the twelve — `REGISTRATION_PLAN.md` lines 55–58:

> `UNSEEN12 admitted = (ENAUSDT, PUMPUSDT, HYPEUSDT, MNTUSDT_BYBIT, SUIUSDT, LTCUSDT, XMRUSDT,
> BNBUSDT, UNIUSDT, 1000PEPEUSDT, DOGEUSDT, 1000BONKUSDT)` — `panels.UNSEEN_admitted_stems`, the only
> reading under which the contract's "the ADMITTED twelve" (line 92) and "the ADMITTED LIST ... IS
> P-GEN-1's panel" (line 50) agree, since the admitted list on disk is all **seventeen**.

**The ADMITTED LIST — P-GEN-1's panel, UNSEEN12 (`panels.UNSEEN_admitted_stems`, in that order):**

| asset | stem | venue | closed 4h bars | admitted |
|---|---|---|---|---|
| ENA | `ENAUSDT` | BINANCE_USDTM | `5413` | `true` |
| PUMPFUN | `PUMPUSDT` | BINANCE_USDTM | `2631` | `true` |
| HYPE | `HYPEUSDT` | BINANCE_USDTM | `2876` | `true` |
| MNT | `MNTUSDT_BYBIT` | BYBIT_V5_LINEAR | `6513` | `true` |
| SUI | `SUIUSDT` | BINANCE_USDTM | `7422` | `true` |
| LTC | `LTCUSDT` | BINANCE_USDTM | `14684` | `true` |
| XMR | `XMRUSDT` | BINANCE_USDTM | `14534` | `true` |
| BNB | `BNBUSDT` | BINANCE_USDTM | `14492` | `true` |
| UNI | `UNIUSDT` | BINANCE_USDTM | `13167` | `true` |
| PEPE | `1000PEPEUSDT` | BINANCE_USDTM | `7410` | `true` |
| DOGE | `DOGEUSDT` | BINANCE_USDTM | `13586` | `true` |
| BONK | `1000BONKUSDT` | BINANCE_USDTM | `6205` | `true` |

**The other admission rows — admitted, not in P-GEN-1's panel:**

| asset | stem | venue | closed 4h bars | admitted | panel |
|---|---|---|---|---|---|
| BTC | `BTCUSDT` | BINANCE_USDTM | `15420` | `true` | CLASSIC5 |
| ETH | `ETHUSDT` | BINANCE_USDTM | `14943` | `true` | CLASSIC5 |
| SOL | `SOLUSDT` | BINANCE_USDTM | `13191` | `true` | CLASSIC5 |
| NEAR | `NEARUSDT` | BINANCE_USDTM | `13004` | `true` | CLASSIC5 |
| ZEC | `ZECUSDT` | BINANCE_USDTM | `14522` | `true` | CLASSIC5 |

The venue / stem leans still open — `OPERATOR_RULINGS.md` lines 148–149:

> - **PUMPFUN → PUMPUSDT** and **MNT → Bybit** remain printed LEANS, not rulings; they need the nod at
>   CLOSE.

### 0.3 · The forward strip

*REPORT-ONLY — the contract's FORWARD STRIP: printed, labeled, never scored. Inlined byte-for-byte from `research_outputs/tierc10/close/FORWARD_STRIP.md` (F-S0-STRIP).*

<!-- BEGIN INLINE close/FORWARD_STRIP.md sha256=a59e438c690987eb69bf24f805c54a4d36ae533d03e7422d499372c19d3872c4 bytes=5786 -->
# TIER-C10 · CLOSE · FORWARD STRIP

**REPORT-ONLY — FORWARD STRIP — NEVER SCORED.** TIER-C10 CLOSE item, contract of record `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md`:114-115: the 5-asset v6 book from TC9's as-of to this corridor's end — printed, labelled, never scored. Counts and sums only: no CI, no p, no verdict, no LOAO, no FDR bar. No registration, score or verdict file was read to build it, and no kline file: every market number below is a column of the filed journal.

## The two as-ofs, as read from files this run

| as-of | value | read from |
|---|---|---|
| **TC9's as-of** (strip start) | `2026-08-22T00:00:00Z` (ms 1787356800000) | `research_outputs/tierc9/build_manifest.json` field `as_of` **and** `research_outputs/tierc9/trade_journal_control.parquet` column `as_of_last_closed_4h` (196 rows, 1 distinct value): equal |
| **this corridor's end** (strip end) | `2026-09-21T16:00:00Z` (last closed 4h bar, close ms 1790006400000) | `research_outputs/tierc10/PROGRESS.json` fields `as_of_of_record` and `as_of_last_closed_4h_close_ms`: agree with each other and with `research_outputs/tierc10/data/AS_OF_PIN.json` |
| contract literal (compared, never used) | `2026-08-22T00:00Z` | `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md`:115 (sha256 `8a0bf279bcab0f27…` == PROGRESS `contract_of_record`): equals TC9's as-of |

## Inputs

- **The book:** `research_outputs/tierc10/panel/control_journal.parquet`, sha256 `fcbf5db0480416b0a5c7f704987980aea220650cb0764d5dd4095611fae64c1c` == `research_outputs/tierc10/PROGRESS.json` stage `PANEL/gate` artifact_shas. 200 campaigns, panel `CLASSIC5`, 5 assets (BTCUSDT, ETHUSDT, NEARUSDT, SOLUSDT, ZECUSDT), lane `card`.
- **The anchor:** `research_outputs/tierc10/panel/FIXTURES_PANEL.txt` (sha256 `163f65bdf21a575c…` == the `PANEL/gate` record), line 35: F-CTRL/b lists 4 live-only campaign(s) against the filed tierc9 journal, all entered after the referee's last bar `2026-08-21T20:00:00Z`.

## Membership

- **ENTERED-IN-STRIP**: `entry_ms >= 1787356800000` (2026-08-22T00:00:00Z), 4 campaign(s).
- **CONTINUATION**: `entry_ms < 1787356800000 <= exit_ms`, 0 campaign(s). TC9's own journal carries 0 `corridor_end` row(s) (exit reasons {"bell_12_89": 4, "stop": 192}), so no v6 campaign was open at TC9's as-of.
- **OPEN-AT-CORRIDOR-END**: exit_reason `corridor_end`, marked to the pin, not realized: 1 campaign(s).
- Note: ETHUSDT long entered 2026-08-30T12:00:00Z was ARMED 2026-08-17T08:00:00Z, inside TC9's window. It is ENTERED-IN-STRIP by the entry predicate, and it is on F-CTRL/b's live-only list.

## The strip (REPORT-ONLY — FORWARD STRIP — NEVER SCORED)

R columns are verbatim from the journal (shortest round-trip repr). `net_r` is the TC-series accounting. `twin net_r` is the ADDED haircut twin.

| label | asset | dir | armed | entered | exited | exit_reason | bars | gross_r | fee_r | funding_r | net_r (TC-series) | twin net_r (ADDED) | twin tier |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| ENTERED-IN-STRIP / CLOSED — realized | ETHUSDT | long | 2026-08-17T08:00:00Z | 2026-08-30T12:00:00Z | 2026-08-30T20:00:00Z | stop | 2 | -1.0 | 0.029816 | 0.001248 | -1.031064 | -1.0417423396773202 | A |
| ENTERED-IN-STRIP / CLOSED — realized | BTCUSDT | long | 2026-09-14T16:00:00Z | 2026-09-14T16:00:00Z | 2026-09-14T20:00:00Z | stop | 1 | -1.0 | 0.10553 | 0.0 | -1.10553 | -1.1477424601980053 | A |
| ENTERED-IN-STRIP / CLOSED — realized | SOLUSDT | long | 2026-09-18T00:00:00Z | 2026-09-18T00:00:00Z | 2026-09-20T00:00:00Z | stop | 12 | 1.498796 | 0.032033 | 0.019861 | 1.446902 | 1.4347296114580608 | B |
| ENTERED-IN-STRIP / OPEN-AT-CORRIDOR-END — marked to the pin, not realized | ETHUSDT | long | 2026-09-18T08:00:00Z | 2026-09-18T08:00:00Z | 2026-09-21T12:00:00Z | corridor_end | 19 | 3.710075 | 0.039565 | 0.027544 | 3.642965 | 3.654683918882855 | A |

## Footer: counts and sums only (REPORT-ONLY — FORWARD STRIP — NEVER SCORED)

Sums are `math.fsum` over the rows above, printed to 6 dp. The rows are verbatim.

| subset | n | Σ gross_r | Σ fee_r | Σ funding_r | Σ net_r (TC-series) | Σ twin net_r (ADDED) |
|---|---:|---:|---:|---:|---:|---:|
| all rows | 4 | +3.208871 | +0.206944 | +0.048653 | +2.953273 | +2.899929 |
| ENTERED-IN-STRIP | 4 | +3.208871 | +0.206944 | +0.048653 | +2.953273 | +2.899929 |
| CONTINUATION | 0 | +0.000000 | +0.000000 | +0.000000 | +0.000000 | +0.000000 |
| CLOSED (realized) | 3 | -0.501204 | +0.167379 | +0.021109 | -0.689692 | -0.754755 |
| OPEN-AT-CORRIDOR-END (marked, not realized) | 1 | +3.710075 | +0.039565 | +0.027544 | +3.642965 | +3.654684 |

| asset | campaigns in strip |
|---|---:|
| BTCUSDT | 1 |
| ETHUSDT | 2 |
| NEARUSDT | 0 |
| SOLUSDT | 1 |
| ZECUSDT | 0 |

## Notes

- `net_r` is the TC-series row of record, carried verbatim. On these rows max |net_r − (gross_r − fee_r − funding_r)| = 1.000e-06. Every R value on these rows is a 6-dp figure, so a residue of up to 1e-6 is rounding in the journal as filed.
- The haircut twin is `tierc10_data.haircut_twin_net_r(asset, gross_r, entry_px, exit_px, r_dist)["net_r_twin"]`. It is gross_r less (taker fee + charter slippage per side) × (entry_px + exit_px) / r_dist, with the stem mapped to the contract asset by the filed Stage D venue table. The filed function charges NO funding, so twin − net_r is not a pure slippage delta. It is an ADDED column and gates nothing.
- An OPEN-AT-CORRIDOR-END row is the journal's own mark at the pinned bar. Its gross_r, fee_r, funding_r, net_r and twin are not realized.
- Every as_of_* column and `warranty` is carried verbatim from the journal. Every row is stamped `as_of_last_closed_4h` = `2026-09-21T16:00:00Z`.
- This strip is not a verdict. It is a printed window of the control book.
<!-- END INLINE close/FORWARD_STRIP.md -->
