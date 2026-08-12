# MC-1 v2 · THE MAY-26 PROGRAM — feasibility map, QUERYABLE ops dossier, similarity
#           family, scoped-lift outcomes, winner stacks, ratchet substrate
RATIFIED: operator 2026-08-06 ("MC defaults + 25ema in 1m") + amendment 2026-08-06
("continuous queryability before/after the cross"; lockbox change offered, DECLINED as
unnecessary — dossier is ops-class). Drafted: APOLLO. Executor: HEPHAESTUS.
BUILT: `exchange/reports/BUILD_APOLLO_2026-08-06_MC1.md` + `MC1_results.json`. Verified present 2026-08-12.
Seed 20260806. All constants [VETO].

AUTHORITY: MC-1..7 rulings (SS_SYSTEM_SYNTHESIS_2026-08-06.md §3.4) + memory #20.
SCOPED EMBARGO LIFT: SEQ8 cascade->trade bridge + D3/D4 outcome tables OPEN for the
populations named in D-4/D-5/D-6/D-7 ONLY. All other embargo intact.

REGISTRATIONS — verbatim, scored this run, printed in the build document BEFORE their
result tables (F-MC6):
  P-i   [55%] Leap-family cascades (4h-tier arrival from the FAST tier, pullback-
        anchored frame) carry higher curtain-cut per-lens MFE net of matched MAE than
        stair-arrival cascades, sign-consistent on >=3 of 5 panel assets.
  P-iii [60%] Grind-signature births (5m->15m->30m context, no slow-tier arrival within
        the episode) are over-represented in the W-F1 bottom decile vs top, CI excl. 0.
  P-iv  [45%] Among 4h arrivals, leap-source outperforms stair-source AFTER conditioning
        on ATR-percentile at arrival (vol-matched buckets), >=3 of 5 assets.

INVARIANTS:
  I1 EVIDENCE/OPS WALL. Every SCORED table: max ts <= the printed exploration ceiling.
     The dossier (D-3) is OPS-CLASS: fetched data under research_outputs/mc1/ops_klines/
     (NEVER the estate); every dossier artifact headed "DISPLAY-ONLY — lockbox-era data —
     hypothesis generation only, never evidence".
  I2 Existing s1 resampler for intra-lattice TFs. 1W/1M derived from 1d, pinned:
     weeks open Monday 00:00 UTC, months calendar-UTC; convention printed on every
     1W/1M table; NOT chart-parity-certified, say so.
  I3 EMA warmup convention = SEQ8's exact rule (cite script line). NaN before warm,
     never backfilled. 1m set = {25,89,200,300,450}.
  I4 Counted never fitted; no probability claims beyond the registrations.
  I5 Any filter-like readout prints TRG; ride-only control prints FIRST in D-7.
  I6 Kiss-v0 (derived, event-sampled; limitation printed): |eA-eB| <= 0.25*ATR(tf),
     then re-expansion >= 0.75*ATR within 10 bars, no sign change. [VETO x3]
  I7 CAUSALITY IN THE DOSSIER: every as-of computation consumes ONLY data <= its as-of
     instant; endpoint_only analytics functions are SLICED per INTERFACE.md. A dossier
     row must be reproducible as "what was knowable then".

DELIVERABLES:
  D-1 WARMUP/FEASIBILITY MATRIX — asset x TF {1m,5m,15m,30m,1h,4h,12h,1d,1W,1M} x EMA
      {9,12,25,89,200,300,450}: first-warm UTC date or NEVER. Overlap with SEQ8 D6
      must reconcile to 0 diffs (F-MC1).
  D-3 MAY-26 QUERYABLE OPS DOSSIER (DISPLAY-ONLY) — BTCUSDT perpetual, fapi.binance.com
      klines (state endpoint + weight budget; instrument string in every header).
      FETCH: 1d from 2019-01-01; 4h/12h from 2024-06-01; 5m/15m/30m/1h from 2025-06-01;
      1m from 2026-02-01. ALL through 2026-08-01. [dates VETO]
      STUDY WINDOW: 2026-02-01 -> 2026-08-01 (the cross +- ~3.5 months).
      EMIT, persisted as parquet under research_outputs/mc1/ops_series/ :
      (a) PER-BAR SERIES per TF across the study window: ts, OHLCV, every feasible EMA
          value, ribbon spreads (9/89, 89/200, 300/450) in ATR units, cross + kiss-v0
          flags on the bar. This is the "query any instant" substrate.
      (b) ANALYTICS REGISTRY SERIES, dual-scored (with/without volume families;
          volume_profile carries its approximation chip): as-of every 00:00 UTC across
          the study window AND as-of every 4H close 2026-05-01 -> 2026-06-15. Persist
          each registry (family, level, score, both variants) under ops_series/registry/.
      (c) CO-LOCATION COUNTS: EMA events within 0.15 daily-ATR [VETO] of a registry
          level, by family, across the window.
      (d) RIBBON STATE SERIES for 5m and 1m long pairs (spread in ATR) — the operator's
          expansion/compression read, as data.
      (e) THE MAY-26 EVENT CARD: the 2026-05-26 4H bear cross stamped with the four D-4
          similarity features (display-only), + the full stack at that instant, + a
          BEFORE-CHRONOLOGY table: every cross/kiss event on every TF in the prior 14
          days [VETO], timestamped, with the registry levels each occurred at.
      (f) QUERY HELPER: query_dossier(ts, tf) in scripts/mc1_program.py returning the
          full stack + nearest registry levels for any instant; one-line pandas recipe
          printed in the build document.
  D-4 SIMILARITY FAMILY (EVIDENCE, exploration-classic) — every 4H trio cross, both
      directions, 7 assets, SEQ8 D1 stream. Stamps [VETO]: SEAL (4H 89/200 agrees or
      crosses within 6 4H bars) · WALL (|price-e89(4h)| <= 0.5*ATR(4h) OR
      |price-e200(1d)| <= 0.5*ATR(1d); state which) · TRAP (>=2 counter-direction
      FAST-tier crosses in prior 24h) · FIRST (no same-direction 4H trio cross in prior
      20 4H bars). similarity_score 0-4; strict core 4/4. Population pyramid per score
      per asset; curtain audit per stamp (F-MC4).
  D-5 OUTCOMES BY TIER (lift, curtain-cut) — per-lens fixed-horizon MFE AND MAE per
      tier per asset; held-in-time split at median event ts; TRG-form tail table
      (F-MC7 identity on tier-0).
  D-6 TRADE JOIN + PROMOTIONS (lift) — bridge join (SEQ8 F-SEQ3 rule verbatim, 0
      orphans); tier membership vs W-F1 deciles; SCORE P-i, P-iii, P-iv exactly as
      registered; all rows printed including failures.
  D-7 WINNER STACKS + RATCHET SUBSTRATE — (a) every bridge-joined top-decile birth in
      a leap-family cascade: full multiTF stack at birth + inter-cross spacings in
      minutes + 1m {25,89,200,300,450} ladder +-3 days (estate 1m, exploration era);
      (b) struct-book winning campaigns: every long-EMA {200,300,450} x {15m,1h,4h}
      test-and-reclaim during campaign life, cushion n in {0.25,0.5,1.0}*ATR; per event
      subsequent-MFE continuation; per campaign the counterfactual stop-to-reclaim-
      structure vs RIDE-ONLY control (control FIRST). Tables only; no rule adopted.
  D-8 HYGIENE — LEDGER_APOLLO append (re-priming 08-05; rulings 08-06 incl. v0.2, path,
      MC defaults + stamps + the continuous-queryability amendment + the declined
      lockbox change; synthesis filing; this run's headline numbers). Then grep
      LEDGER.md for the P-SEQ-ii entry: print registration text + in-entry ordering-
      anomaly note verbatim; state CONFORMS or itemize the diff; fold any diff into
      the append.

FIXTURES (HALT loudly; full transcript in the build document):
  F-MC1  D-1 vs SEQ8 D6 overlap 0 diffs; 3 cells hand-recomputed by explicit formula.
  F-MC2  EVIDENCE WALL: max ts of every scored table <= ceiling (print both); zero
         estate writes (porcelain before/after); every dossier artifact carries the
         DISPLAY-ONLY header.
  F-MC3  Determinism: D-4 stamps + D-5 tier table recomputed, identical (seed 20260806).
  F-MC4  Curtain audit: every stamp from data at/before its event bar; violations
         listed and demoted, never silently kept.
  F-MC5  Join integrity: 0 orphans both ways; join rule cited verbatim from SEQ8.
  F-MC6  Registration ordering: P-i/P-iii/P-iv verbatim BEFORE their result tables.
  F-MC7  TRG identity: tier-0 retains 100.0% exactly.
  F-MC8  1W/1M resample: 2 buckets hand-checked against their 1d members; convention
         header present on every 1W/1M table.
  F-MC9  Full re-run of D-5 hash-identical.
  F-MC10 QUERYABILITY PROOF: retrieve the full stack + nearest levels for
         2026-05-20 08:00 UTC and 2026-04-03 16:00 UTC via query_dossier; print both
         cards; verify the 2026-05-20 EMA values against a direct recomputation from
         the raw fetched klines (exact match required); state that chart parity vs
         TradingView is NOT asserted (operator may spot-check and relay).
  F-MC11 As-of causality probe: recompute one registry (2026-05-26 00:00) twice —
         once correctly sliced, once deliberately fed one future bar — and show the
         guard REJECTS the second (a fixture that can fail).

IMPLEMENTATION: scripts/mc1_program.py — checkpointed per stage to _reviewer_box/mc1/,
resume-safe, sorted iteration, fixtures self-checking. Registry series is the heavy
stage (~180 daily + ~270 4H-close as-of computations): checkpoint per as-of; if budget
runs short finish whole stages, name cached vs remaining, write the build document
honestly, do NOT emit partial scored tables.

OUTPUTS: bulk -> research_outputs/mc1/ (path+size+sha256 pointers in the build doc,
NOT pushed). Text <=1MB -> exchange/reports/: MC1_tables.md, MC1_results.json, and ONE
build document exchange/reports/BUILD_APOLLO_2026-08-06_MC1.md (zero-context, full
fixture transcript, full tables, versions/hashes/commits, findings reported-not-fixed,
six-column file-disposition table WITH BOX-COST column; flag anything over ~1% of
6.39 MB with its intended home).

NOT THIS CONTRACT: no lockbox/seal modification · no lockbox row in any scored table ·
no engine change · no trading rule adopted · no estate write · no new resampler · no
analytics claims beyond counting.
