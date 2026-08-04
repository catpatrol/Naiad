# W-F1 · WINNER FORENSICS — Tier-A discriminant study
RATIFIED: operator, 2026-08-03, word "forensics". Drafted: APOLLO. Executor: HEPHAESTUS.
FRAME (ratified "discriminant"): condition on outcome, discriminate at birth; every
discriminant must be decision-curtain-clean; Tail-Retention Gauge mandatory.

POPULATION & JOIN (all previously ruled — do not re-derive):
  journals research_outputs/_unarchived/s3_2026-07-27/journal_s3/scored/ (753 files);
  substrate s3_excursion_substrate.jsonl (7,094 rows); join (cell, tranche_id);
  23 unresolved fills excluded-and-counted; fill_class: r1=3,825 · v=78 (EXCLUDED and
  counted; different birth mechanism) · re_entry=3,214; stopout = exit_reason in
  {stop, stop_gap} (expect 5,016).
DECILES: rank ALL 7,094 resolved tranches by realized_r. W = top 709, L = bottom 709
  (floor(0.1*n); print exact cut values). SECONDARY pair: same on the r1-only book.

SECTION A · DISCRIMINANTS AT BIRTH (curtain-clean ONLY — feature knowable at/before fill):
  categorical: symbol · mandate · dir · fill_class · grade · zone · stage · each s2 flag ·
    engagement_flags · concurrent_open_at_fill · session-hour-UTC bucket [ANNEX] · day-of-
    week [ANNEX];
  numeric: retr · atr_exec/px_fill in bps (vol-at-birth proxy) · atr_gov/px_fill bps.
  STATS: categorical -> prevalence in W vs L, delta-prop, bootstrap 95% CI (10,000, seed
  20260803); numeric -> median delta + CI. Benjamini-Hochberg FDR q=0.10 across the
  Section-A family (annex columns in their own family). PANEL: five-asset
  (BTC/ETH/SOL/NEAR/ZEC) sign-consistency flag per discriminant; JTO/TAO annex rows,
  never pooled. TIME: split at median ts_open; sign-stability flag per discriminant.
  CANDIDATE = CI excludes zero + FDR-surviving + panel sign-consistent + time-stable.

TRG DEMONSTRATION: for the top 5 FDR-surviving discriminants, apply the naive filter
  "keep only trades with the winner-side value"; report delta-expectancy (R AND net-of-
  toll bps) AND TRG = retained share of the UNFILTERED book's top-decile total R.

SECTION B · OUTCOME ANATOMY (post-birth; labelled NOT-curtain-clean, never a discriminant):
  exit_reason mix W vs L · holding time (ts_close - ts_open) distributions · give_back_r ·
  MFE/MAE shapes at horizons from the substrate · FUNDING FIRST READ: funding_cum —
  median, and median |funding_cum|/|realized_r|, W vs L, per mandate.

PREDICTIONS (state verbatim, then score honestly):
  P-WF1 [70%] >=1 s2 slow-stack flag is a CANDIDATE discriminant favouring W on >=3 panel assets.
  P-WF2 [65%] fill_class=re_entry is over-represented in L with CI excluding zero.
  P-WF3 [55%] deep zones (Z1/Z2) over-represented in W with CI excluding zero.
  P-WF4 [60%] median holding time of W >= 5x that of L.
  P-WF5 [50%] median |funding_cum|/|realized_r| for W is < 10% (funding drag material but small).

FIXTURES (HALT loudly on failure):
  F-WF1 reconciliation: 3825+78+3214=7117 fills; 7094 resolved + 23 excluded; decile sizes printed.
  F-WF2 curtain audit: list EVERY Section-A feature + one-line attestation none is post-fill.
  F-WF3 determinism: one full table computed twice at seed 20260803, byte-identical.
  F-WF4 per-asset counts sum to panel totals; annex assets outside panel sums.
  F-WF5 FDR arithmetic: recompute q-values for 3 rows by explicit formula in the report.
  F-WF6 TRG identity: the unfiltered book's TRG = 100.0% exactly.

IMPLEMENTATION: write scripts/wf1_forensics.py (checkpointed per cell to
  _reviewer_box/wf1/<cell>.json, resume-safe; self-checking = the fixtures; sorted
  iteration; no network). Commit scripts/wf1_forensics.py locally (commit-no-push).
DELIVERABLES: exchange/reports/WF1_discriminants.json (<1 MB; big intermediates stay in
  _reviewer_box/wf1/ and are referenced by path+sha) ·
  exchange/reports/WF1_tables.md (full tables, not summaries) ·
  exchange/reports/BUILDERS_REPORT_APOLLO_2026-08-03_WF1.md.
