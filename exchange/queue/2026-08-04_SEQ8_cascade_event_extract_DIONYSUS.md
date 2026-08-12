# CONTRACT — SEQ-8 · The Cascade Event Extract
**Drafted:** DIONYSUS, 2026-08-04, on explicit operator instruction (one-time Q-5 drafting exception granted by operator this date; ratification stamp still required).
**RATIFIED: operator, 2026-08-06** — "stamp seq8". Drafted by DIONYSUS. Executor: HEPHAESTUS.
BUILT: `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SEQ8.md`. Verified present 2026-08-12. (Verdict criteria still owed — see the open defect above; that is a drafting debt, not an execution one.)
**Executor:** HEPHAESTUS · **ENVIRONMENT: local Windows Claude Code** (the repo containing `_reviewer_box/` and the data estate; assert before any write, halt on mismatch)
**Authority chain:** SEQ interview rulings, operator 2026-08-04 (SEQ-1 C+windows · SEQ-2 D · SEQ-3 B+multiTF meaning · SEQ-4 b+c+d · SEQ-5 a · SEQ-6 b · SEQ-7 promote-(ii)-park-rest · SEQ-8 a). Record: `exchange/reports/SESSION_SUMMARY_DIONYSUS_2026-08-04_SEQ_rulings.md`.

> ⚠ **OPEN DEFECT, recorded beneath the stamp and not a condition on it — owner: DIONYSUS.**
> This contract carries **no verdict criteria**. `CONVENTIONS.md` requires every queue item to state
> what outcome constitutes acceptance; this one states fixtures and deliverables but never says what
> result would mean the work succeeded or failed. The defect was found by the HERMES queue audit of
> 2026-08-05, which found three of four items incomplete against the same standard.
>
> **Consequence for the executor, stated plainly:** run the contract, report every result against its
> fixtures, and **do not declare a verdict.** A conclusion drawn against an unstated bar is a bar
> invented after seeing the data, which is the one thing this project's method exists to prevent.
> DIONYSUS supplies the criteria before any finding here is treated as settled.

## §0 Hard assertions (run before any read or write)
`git rev-parse HEAD` printed · **path ends with `C:/Naiad` AND does not contain `OneDrive`** (amended 2026-08-12, queue 004 Phase A; two-sided because two complete clones coexist until Phase B, and the former `Users…OneDrive…naiad` form would now halt every valid session and admit every invalid one) · `engine/` exists · `scripts/census_build.py` exists · `exchange/{queue,reports,status}/` exist · census exploration substrate present. HALT on any failure; report, do not create.

## §1 Purpose, plain language
Produce the raw substrate that lets Naiad study *sequences* of Secret Sauce events across time AND across timeframes — without baking any arbitrary definition of "a cascade" into the data. Today's sequence numbers chain events with a 48-hour window chosen for convenience; the operator's ruling requires that cascade definitions become **views computed on top of a raw event stream**, so any future definition can be recomputed without re-extraction. This extract is also the bridge substrate joining cascade-world to trade-world (the journals carry no EMA-lattice state — W-F1 P-WF1 premise-false), and the same stream serves the range-detection program (G-RD2).

## §2 Invariants
I1 Exploration-classic data only; no bar, event or journal row later than the existing census substrate ceiling (assert from the census machinery's own constants; print the ceiling used). No lockbox read of any kind.
I2 Census TF lattice as on disk: {5m,15m,30m,1h,4h,12h,1d}, 30m←15m and 1d←1h resampled by the existing s1 algorithm — **do not build a new resampler** (ARGUS hazard F-1R-*).
I3 Both lattices: {9,89,200} and {12,25}. NEW columns: EMA 300 and 450 on {1h,4h,12h,1d} for HTF orientation — NaN until full warmup, never backfilled.
I4 No new event detectors in this contract: emit the event classes the census machinery already computes (all three cross pairs × both directions at minimum); REPORT which Q1c classes are and are not emitted — the gap list is a deliverable, not a license to improvise.
I5 Counted, never fitted. No weights, no scores, no probability claims.
I6 Analysis embargo: outcome-bearing tables (D3, D4) are EMITTED as substrate but not analyzed/promoted in this run. The only registered claim scored here is P-SEQ-ii (§3 D5, pure counts). Parked registrations (leap outcome edge, grind↔loser join, route-conditioned edge) wait for their stamps.

## §3 Deliverables
**D1 · RAW EVENT STREAM** — per asset × TF × lattice: event_class, direction, ts_utc, price stamp, bar index, plus per-TF EMA-state snapshot at the event (9/89/200, 12/25, 300/450 where warmed). One row per event, no chaining. This is the atom-independence guarantee.
**D2 · CASCADE VIEWS (derived, never baked)** — chaining as a parameter: windows {24h, 48h, 72h, 1W} × rule {window-chained, direction-consistent (counter-direction cross ends the cascade)} = 8 views. Per cascade: rung string in ALL THREE frames (absolute TF · governor-relative steps · tier grammar), depth-complete (no 3-rung truncation), monotone/shuffle flag, per-step sojourn times, leap latency. Plus the cross-view agreement table (how much do the 8 definitions disagree, and where).
**D3 · OUTCOME SUBSTRATE (emitted, embargoed per I6)** — per cascade terminus: per-lens fixed-horizon MFE **and MAE**, curtain-cut flags; event-based outcomes (time-to-tier-clearance, survival-to-next-tier); and the **cascade→birth JOIN table** to journal keys `(cell_id, tranche_id)` — the builder states the exact join rule chosen (from machinery, e.g. birth ts within cascade span on the governor lens) in the report; the rule is reported, never silent.
**D4 · Route-vs-outcome matrix at the 4h arrival** (source rung × curtain-cut MFE/MAE distributions), per asset and per lens. Emitted, embargoed per I6.
**D5 · Arrivals replication panel — the one REGISTERED claim, P-SEQ-ii** (proposed prior 75%, operator may re-stamp): the structural finding "the leap (arrival at 4h directly from ≤30m) is the dominant 4h activation mode, and 1h arrivals are predominantly adjacent" replicates in pure counts, sign-consistent on ≥5 of the 7 census assets, per lens. Scored in this run — it is outcome-free.
**D6 · Warmup coverage table** — per asset × TF: first timestamp at which EMA300/EMA450 are fully warmed (or NEVER within the substrate), so no later study silently consumes unconverged HTF values.

## §4 Fixtures (numbered; each independently falsifiable; full transcript in the report)
F-SEQ1 Event counts reconcile to the census machinery's own cross counts per asset×TF (0 diffs).
F-SEQ2 Max timestamp in every emitted file ≤ the printed exploration ceiling.
F-SEQ3 Join integrity: every joined birth key exists in the journals; zero orphans both ways; join-rule stated.
F-SEQ4 The {48h, window-chained, 3-rung-truncated} view reproduces the Atlas count (2,378 on the same asset/lens set) exactly, or the diff is itemized.
F-SEQ5 Curtain audit: every column marked curtain-clean derives only from data at/before the event bar; violations listed and demoted, never silently kept.
F-SEQ6 EMA300/450 are NaN before full warmup on every asset×TF; zero backfilled values.
F-SEQ7 Determinism: full re-run reproduces every table byte-identical (or hash-identical), seed and versions printed.
F-SEQ8 Worked multiTF example: one query over D1 retrieving a cross-timeframe sequential pattern (e.g., 5m bull cross → 15m bull cross → 4h test-and-hold with 12h e89>e200 aligned) on one asset-month, count verified by hand-inspection in the report — proving the operator's across-time-AND-across-timeframes patterns are minable from this substrate without re-extraction.

## §5 Outputs, filing, publish
Bulk artifacts → `research_outputs/seq8/` (path + size + sha256 for each in the report; NOT pushed). Summaries ≤1 MB → `exchange/reports/`. Two mandatory artifacts per the standing rule: `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_<date>_SEQ8.md` (forensic: gates, probes, full fixture transcript, versions/hashes, findings reported-not-fixed, six-column file-disposition table) and `exchange/reports/SESSION_SUMMARY_HEPHAESTUS_<date>_SEQ8.md` (plain-language decision artifact). Publish via `scripts/publish_exchange.py`; state on screen whether the push SUCCEEDED. **No commit-no-push clause in this contract** — proven unachievable for the published branch (W-F1 §18); the script commit rides the publish, accepted here explicitly. On-screen close: exact filenames + full repo paths in bright colors.

## §6 What this contract is NOT
Not a trading rule, signal, or filter. Not an engine change (engine/ is untouched). Not a registration of any outcome claim beyond P-SEQ-ii. Not new detector construction. Not a lockbox read. Not the range-detection module — it only feeds it. The parked promotions and all D3/D4 analysis wait for the operator's stamps after the Secret Sauce deep-dive.
