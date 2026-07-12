# SSv11.3 session packet — 2026-07-11

Two jobs, per the SSv11.3 "Grade Legibility" build contract: (1) parity-break
diagnostics, (2) the display-only Pine patch. **No engine or Pine logic changed.**

## Contents

| File | Deliverable | Notes |
|---|---|---|
| `D0_delta_report.md` | **D0** | v11.0.2 delta report. **Delta BLOCKED** — the deployed-source capture (`pine/SS_Cascade_v11.0.2.pine`, runbook Step 1) was not provided; the project-copy side + H1 verdict are delivered in full. |
| `Q1_phantom_confirm_sweep.txt` | **Q1** | Every zoneless CONFIRM in the dev-window parity journal: **82 rows** (of 475 CONFIRMs). Includes the 2026-06-23 break trio. |
| `Q3_estate_candles.txt` | **Q3** | BTCUSDT 5m OHLC, 2026-06-23 14:00→21:00 UTC, verified estate: **85 bars**. |
| `SS_Cascade_v11_0_2.pine` | v11.0.2 | Committed **project copy** (stands in for the deployed capture, which is pending). |
| `SS_Cascade_v11.3.pine` | **D1** | The patched display successor (VR-A Option 3 / VR-B). |
| `D2_diff_v11.0.2_to_v11.3.patch` | **D2** | Proves I1: only display lines changed; alert blocks byte-identical. |
| `CHANGELOG_v11.3.txt` | **D3** | v11.3 banner changelog; output budget 57→59 (62 with fills). |
| `D6_playbook_erratum.diff` | **D6** | Playbook erratum edits — confined to the two named rows (§3 zone-bands, §4 Z2). |
| `SSv12_SPEC_ERRATA.md` | D0/E-1 | Erratum E-1 register entry (provisional Z2 arming; Z3 not armed). |

## Headline findings

1. **H1 is contradicted by the committed source.** The committed Pine's CONFIRM
   trigger `confirmL = (confirmXL and hadPrimeEp) or gradeCL` (line 545) is
   **ungated** on the add branch — it fires, draws a diamond, and ratchets the
   stop on zoneless CONFIRMs **exactly like the engine**. So the engine is *not*
   the deviant vs the committed Pine. H1 (deployed zone-gates CONFIRM) can only
   hold if the **deployed** chart drifted from the committed source — which the
   missing capture is needed to prove. **Do not draft an engine fix on H1 until
   the capture confirms the deployed source actually differs.**
2. **Q1 sizes the phenomenon:** 82 zoneless CONFIRM adds over the dev window
   (all grade "-"), 77 short / 5 long, mostly Stage 2. These are legitimate adds
   in the committed/engine logic, not phantoms — the 2026-06-23 trio
   (62590.61 / 62586.80 / 62490.50) matches the contract exactly.
3. **E-1 confirmed:** provisional campaigns arm **Z2** (line 428, default
   `provZones="Z1+Z2"`); **Z3 is NOT** armed provisionally (line 429). Documented,
   not changed (I6).

## Outstanding operator actions

- Runbook Step 1: export the deployed source → `pine/SS_Cascade_v11.0.2.pine`,
  then re-run `diff` against `SS_Cascade_v11_0_2.pine` to close D0's delta.
- Runbook Step 4: the two hover readings (Q3 cross-check + the Jun-23 ~10:00
  stop = 63,041.35).
- Runbook Step 5: compile v11.3 (no errors), A/B on a fresh layout at
  2026-06-22 12:00–20:00 UTC; parity layouts stay on v11.0.2 (I4).
