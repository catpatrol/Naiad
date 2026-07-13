# Data-Spend Ledger

*Maintained by the REVIEWER only (charter §2). The builder proposes entries in
its session summary; the reviewer decides what lands here. Governing rule:
reading a result spends the data, whether or not you act on it. Never read a
proxy of a measurement we can afford to make for real.*

## Opening entries (charter §6, at ratification 2026-07-09)

| Dataset | Status at ratification |
|---|---|
| BTC, all TFs, 2025-10-06 → 2026-07-07 | **SPENT for validation** (fitted twice: the nine-month study and the v11.0.2 verification cycle). Parity fixtures and characterization only. |
| All assets, first valid candle → 2025-09-30, excluding the row above | **Characterization set.** All tuning lives here and only here. |
| All assets, everything before 2022-01-01 (BTC/ETH ≈ 2019–2021: Covid crash, 2021 blow-off) | **SEALED retro holdout.** Read **once**, against the pre-registered bar in charter §7. The read spends it regardless of outcome. |
| Forward paper journals | **Virgin, renewable.** Honest exactly once per frozen ruleset; each window is a one-shot exam. |

## Entries after ratification

### 2026-07-10 — Phase 1 packet review (naiad_packet_20260710_1303.zip, engine 1.0.0, git c97fc31)

- **Data touched:** BTCUSDT_swing journal 2026-05-01→07-07 and D5 parity artifacts 2025-10-06→2026-07-07 — entirely inside the hard-spent BTC window. **Fresh evidence spent: none.** All numbers handled as plumbing characterization under the spent-window rule.
- **Looks logged:** reviewer recomputed equity, tranches, halts, signal-event decomposition, cost anatomy, ratchet paths, parity cross-consistency, and schema completeness from raw journal bytes. D7 capture/tail table seen and explicitly **not** interpreted (n=10, spent).
- **Verdict:** CONDITIONAL PASS — see `Phase1_Reviewer_Verdict.md`. Conditions at issue: D-1 (summary rows/sha not derived from persisted files), operator D5/F6 TradingView sign-off incl. the V-signature fork (Feb 6 / Jun 22, 5m vs 4H chart), operator charter conformance check.
- **Standing reminders:** Phase 2 partitions pending ratification; collector OFF; the nine-month BTC window is spent and may never serve as out-of-sample validation.

### 2026-07-10 (afternoon) — tickets D-1..D-3 closed; basket backfill complete

- Reviewer re-verified `naiad_packet_20260710_1448.zip` (engine 1.0.0, git c2ae143): formula-reproducible journal_sha256 `5b7e4b333e364af394f55da6840c2d4dd89cc43c70003bcd98dc365e67e5b5ee`, rows 1502, 29/29 per-file digests match, journal delta vs the 1303 packet = the two HALT rows only (D-2 namespacing). Fixtures 25 green incl. F1b.
- Charter now ships in the packet (D-3): reviewer completed the §3.2/§3.3/§3.4 conformance check — config conforms exactly to the ratified grade-split sizing table; the survival-stop-only live line with X-A…X-D shadowed exits **is ratified charter text (§3.3)**; V-births-provisional is charter text (§3.2). Sole open ratification: **halt scope** (charter silent; config default per_cell).
- Known caveat at 1.0.0 (superseded by the evening entry): same-bar reject key collisions drop duplicates — reject counts are lower bounds.
- `--all` backfill complete: 60/60 series, 0 duplicates, one 1-bar gap total (BTC 1m, listing day 2019-09-08). **LIT two-token trap verified on all 6 intervals: first candle 2025-12-23, nothing pre-Lighter.** Verdict condition §5c closed.

### 2026-07-10 (evening) — engine 1.0.1 re-anchor: reject subkeys, collision closed

- Reviewer re-verified `naiad_packet_20260710_1506.zip` (engine 1.0.1, commit da31062): 29/29 digests; journal_sha256 `c4dfe16c1ee5ce5883abc14162d39be5595cf45c75f1444f2b601f498a4acf2f` reproduced from raw bytes by the documented formula; rows 1503 = newline count; run_id `bac9c0aa12eafa5d` uniform.
- Independent field-level delta vs 1.0.0: after normalizing run_id / engine_version / subkey families, exactly **one** row differs — the restored 2026-07-02T20:00 REJECT (max_tranches), persisted beside its twin (`trade_ADD_prime` / `trade_ADD_confirm`). Zero rows lost. Economics invariant: exits 10 · pnl −380.96 · equity 9619.04 · halts 2 · fees 182.08. Parity journals regenerated at 1.0.1 (no version mixing). Fixtures 26 green (incl. F8b) on the operator machine.
- **Reject-count caveat lifted:** counts are exact from 1.0.1 onward.
- **Operational rule adopted (CHANGELOG 1.0.1):** a key-schema change regenerates into clean journal files, never merges — the idempotent writer strands rows under retired keys (373 stale rows observed and wiped in the builder's first attempt). Any engine bump after collector-on is therefore a deliberate data-branch **migration**, to be governed in the Phase 2 protocol.
- Cosmetics parked for the next natural engine touch (non-blocking): D7 header prints stale "engine 1.0.0" (its run_id/rows/sha are current); packet MANIFEST `git_rev` stamps the last commit, not tree state — should mark dirty trees.
- **Anchors for collector launch:** engine 1.0.1 @ `da31062` · journal_sha256 `c4dfe16c…` · fixtures 26. Phase 1 remaining: F6 operator sign-off · halt-scope ratification · CI-green glance on `da31062`.

## v12 Study — opened 2026-07-10
- Charter: V12_Study_Charter_Addendum_v1.0.md (VR-1..VR-5 ratified; governor-TF axis pre-registered)
- Evidence classes: spent | regime-contaminated | exploration-classic | lockbox | forward(Naiad)
- Spent: BTCUSDT 2025-10-06 -> 2026-07-07 (six intervals) - characterization only
- Regime-contaminated: all non-BTC assets 2025-10-06 -> 2026-07-07 - exploration-eligible, lockbox-ineligible
- Exploration-classic: all study candles <= 2024-06-30
- LOCKBOX: 2024-07-01 -> 2025-10-05, all assets, all intervals - SEALED. Integrity ops only. Opens once, at V8.
- Study right edge: 2026-07-07 23:59:59 UTC. Forward data belongs to Naiad.
- Variant budget: 5 named slots. Study closes at lockbox verdict or 2026-10-31.
- Regime taxonomy frozen: BTC 12H 89v200 stage x BTC 30d realized-vol terciles (thresholds fit on exploration-classic only)
- Spend at open: zero (census pending)

## 2026-07-10 — Engine 1.0.2: cache no-shrink invariant
- Incident: BTCUSDT 5m/1h kline caches truncated to [2025-03-01, 2026-07-08) by parity_pack --backfill; attribution recomputed and verified by reviewer; estate repaired by census same day; evidence spend: zero.
- Root cause: exists()-masked load failure + conditional history merge + non-atomic whole-file save (engine/data.py).
- Fix: merge-in-save + atomic replace + loud load failures, klines and funding; invariant "caches never shrink via the save path" fixture-enforced (N1-N5). Engine 1.0.1 -> 1.0.2.
- Accepted residuals: concurrent last-writer may drop the other writer's fresh rows (refetchable); deleted file recreated via engine path starts at warm-up anchor (coverage_ok is the detector); row deletion = delete file + census --extend.
- V1 packet review: still PENDING. This entry does not close V1.

## 2026-07-11 — v12 V1 census: CLOSED (PASS) · Engine 1.0.2: MERGED
- V1 verdict: PASS. Reviewer recomputed all headlines from raw artifacts: three-way reconciliation (census.json / DATA_CENSUS / retrieval_meta) zero fails across ~600 fields; boundaries = VR-1 epochs exactly; only the four ratified evidence classes exist; 26,711,569 rows recomputed independently; hash chain intact end to end.
- Gaps: 1 listing_edge (BTC 1m, 2019-09-08 19:00) + 5 exchange_side (funding, all at 2026-06-24 04:00, refetched 2x) + 0 download_hole. External anchors: HYPE listing confirmed to the minute and LIT floor to the day vs Binance announcements; SOL funding-grid shift = FTX week (2022-11-09 -> 11-18).
- Operator spot check: 33 rows -> 26 OK / 0 mismatch / 7 unavailable (TradingView intraday lookback tiers; pattern tracks TF x depth, not the estate). Spent era covered by parity 3A (30/30) + coverage cross-check (577/49). FARTCOIN/TAO first-candle date checks waived with cause (pipeline externally validated 2x; coverage_ok is the standing detector; V2 re-touches FARTCOIN).
- Correction on record: pre-2022 is exploration-classic per VR-1; grep confirmed no code restriction (CHANGELOG carries the dated note).
- Engine 1.0.2 merged into v12-v1-census (--no-ff): no-shrink invariant live, N1-N5 green, suite 40/40.
- Evidence spend to date: zero. Estate open for V2 (parity completion) -> V3+.

## 2026-07-11 — 3C verdict-criterion amendment: RATIFIED
- Old: "engine and chart event streams identical."
- New (operator-ratified, verbatim): "Engine and chart event streams identical, except at knife-edge state forks — divergences traceable to a boundary comparison within float tolerance of a zone edge or EMA crossing — each identified to its forking bar, documented, and bounded in aggregate below 0.5% of events."
- Basis: 2026-06-23 break root-caused to a state fork. Evidence: D0 delta EMPTY (deployed == committed, sha 0ade9d01...); v11.3 fresh-compile replicates deployed behavior; deployed chart fires zoneless adds on Jun 24; hair-width tag observed at Jun 24 07:10 (margin 1.6 pts, 0.0025% of price). No engine or Pine change warranted.
- Measured fork rate: 3 of 5,309 events (0.06%) - inside the 0.5% bound.
- Jun 22 window: flips to PASS-with-documented-fork when Q4b names the forking bar.

## 2026-07-11 — Halt scope: RATIFIED per_cell
- Final open Phase-0 charter decision, closed by operator word (2026-07-11).
- Rationale of record: one cell's bad day cannot silence another cell's data collection; portfolio-wide halts remain queued as Phase-2 Experiment E1.

## 2026-07-12 — Engine 1.0.3: input-parity conformance (root cause of the 3C break)
- Root cause: engine hardcoded zone_memory=5; deployed Pine runs zoneMemory=3 (operator-verified on deployed and v11.3 charts). Bands, EMAs, logic proven identical; one constant forked hadPrimeEp/activeZone state.
- Ruling: parity target is the deployed chart; engine conforms. zone_memory -> 3 all mandates/configs; input-parity fixture family added (drift can no longer recur silently).
- Journal: mem=5 parity journal ARCHIVED as v12 named-variant seed ("zoneMemory-5" candidate: 18 extra entries, 2 regrades, 4,360 stop-divergent bars over 9 months). Parity journal REGENERATED at mem=3; diff vs validated shadow = ZERO.
- Correction to 2026-07-11 criterion entry: the Jun-23 instance was config divergence, not a float fork; the criterion stands as law; measured float-fork count post-conformance: pending re-verify, expected 0.
- Reviewer record: theories 2-7 falsified by measurement; theory 1 ("engine is the deviant") confirmed by the operator's Inputs reading.

## 2026-07-12 — TradingView parity sign-off (Runbook Step 3 / F6): CLOSED — PASS
- Instrument: deployed SS Cascade v11.0.2 (= v11.3 logic), inputs at defaults (Zone memory = 3, operator-verified). Engine 1.0.3 (input-parity conformance); parity journal run_id 1869ff70..., SHA 4c734317...ce92de, 5,446 rows; I3 diff vs validated shadow = ZERO.
- 3A: 30/30 4H governor crosses exact. 3B: 11/11 12H by EMA geometry; 0/11 native prints = design.
- 3C, six case windows: Jul 2-6 PASS · Jun 14-16 PASS · Jun 22-23 PASS (former break resolved by 1.0.3; phantom mem=5 events removed; chart == journal) · May 16-26 PASS (two regrades "-"->C glyph-verified: 05-17 13:50, 05-29 21:25) · Feb 6 Tier-2 PASS · Dec 4-13 Tier-2 PASS (lone V verified in campaign context). Tiers: 1 = chart-verified; 2 = past TradingView intraday horizon, covered by I3 shadow equivalence.
- 3D: Outcome C on both doctrine dates (no V printed on any chart or TF; engine agrees). V census: 1 firing in 9 months (2025-12-12 15:25, short @ 90,795).
- Knife-edge criterion (bf92eaa) stands as law; measured float-fork count post-conformance = 0 — every prior divergence traced to the zone_memory constant, corrected in 1.0.3 and fixture-pinned.
- Errata: E-1 on record (SSv12_SPEC_ERRATA.md). J-1 (REJECT stage dataclass default) parked for next engine touch.
- Operator sign-off: Ludwig, 2026-07-12. Reviewer: all headline numbers recomputed from raw artifacts.
- STEP 3 CLOSED. Collector switch-on (Step 5) UNBLOCKED. v12 Study V2 gate SATISFIED; V3 (anchor run) OPEN.

## 2026-07-12 — CORRECTION: v12 gate status in the parity sign-off entry above
- The sign-off entry of this date (commit cd91ded) closes with "v12 Study V2 gate SATISFIED; V3 (anchor run) OPEN." That claim is incorrect and is superseded by this entry, per VR-4.
- Correct status: v12 Study V2 = parity legs (3B/3C/3D) SATISFIED plus the ETH+FARTCOIN cross-asset spot check, which remains OUTSTANDING. V3 (anchor run) opens only on its completion.
- All other content of the sign-off entry stands unchanged and reviewer-verified: every line through the operator sign-off matches the ratified reference byte-for-byte; only the final status claim diverges, and the ratified v12 status bullet is absent. This entry supplies it.
- Cause: the committed text matches the pre-correction draft; the ratified corrected block (reviewer handoff 2026-07-12, §2/§3.1) was not the version pasted. Ledger is append-only: the original entry is retained as written; this entry supersedes its final claim.
- Operator: Ludwig, 2026-07-12. Reviewer: correction cross-checked against VR-4, the ratified handoff, and a line-by-line diff of the committed block.

## 2026-07-13 — v12 Study V2 gate: CLOSED — PASS
- Final V2 item per VR-4 / Charter Addendum line 172: ETH+FARTCOIN cross-asset parity spot check. Result: PASS.
- Protocol: engine 1.0.3 (input-parity), 4H governor crosses, inputs at defaults (Zone memory = 3), UTC. Operator verified each printed cross on deployed TradingView v11.3.
- ETHUSDT: 10 most-recent 4H governor crosses (span 2026-04-28 → 2026-07-02), all confirmed on-chart, direction exact. Listing floor organic.
- FARTCOINUSDT: 10 most-recent 4H governor crosses (span 2026-05-13 → 2026-07-11), all confirmed on-chart, direction exact. First-valid candle 2024-12-20T16:00Z reached organically (detected_first == first_valid, floor_overridden = False); LIT-class trap correctly did NOT fire — single-identity asset, no ticker-sharing history, EMA-200 fully warmed.
- Operator also independently verified regime-tint (EMA89×EMA200) flips against chart (e.g. 2026-05-17 20:00 → full bear); engine and chart agree on both governor and regime layers.
- 20/20 rows verified clean across both assets. No mismatch.
- V2 requirement census: parity 3B CLOSED, 3C CLOSED, 3D CLOSED, ETH+FARTCOIN spot check CLOSED. V2 gate SATISFIED in full.
- STEP: v12 Study V2 CLOSED. V3 (anchor run) OPEN.
- Operator sign-off: Ludwig, 2026-07-13. Reviewer: spot-check events and floor status recomputed from engine artifacts; operator performed chart verification.

## 2026-07-13 — v12 V3 anchor run: EXECUTED — evidence spend recorded
- Evidence spend: exploration-classic FIRST LOOK consumed, 20 scored cells (grid per Stage-1 F1 + A1 Q-4 month-aligned starts; TAOUSDT_swing 30d INSUFFICIENT SAMPLE by design).
- Config: v12_anchor (sha256 a3917ea58a1a7e05…), signal byte-identical to v11_faithful, trading/shadows byte-identical to naiad_v0, v_births_provisional=false (Pine literal). Engine 1.0.7 (2f260e1); strategy-code delta vs parity-signed 38b3f66 = the four ratified fixes per the G-3..G-6 bullet below, each pinned-stamp parity-proven.
- Determinism: full double-run, per-cell journal SHA256 ALL IDENTICAL across 47 runs.
- Grid evidence hash (sha256 over sorted per-cell journal SHAs): 261bd6a1c988dc66aeef85a4920e8f805f4adf8e8dda8f578af7509c572deb6d
- Scored grid net R (1x): -5756.9093 over 3456 campaigns; strip-best-campaign -5871.3612.
- Annex (CHARACTERIZATION only): BTC spent 3 cells; regime-contaminated 24 cells (8 assets). F4-a lockbox warm-up traversal disclosed per cell in manifest; zero journal rows with lockbox open times (first_journal_ts >= window start, all annex cells).
- G-1 registered: no code-level lockbox guard on the replay path; run protected by window arithmetic + manifest loaded-span assertions; code guard due at engine 1.0.8 with J-1 (per the G-6 ruling: first post-anchor-run engine touch).
- G-2 registered: LIT cache contamination (31,680 pre-Lighter bars); LIT annex deferred pending estate remediation.
- G-3/G-4/G-5+G-5b/G-6: four latent trading-layer states surfaced by deep history, each halted, bar-level diagnosed, operator-ratified, shipped as engines 1.0.4/1.0.5/1.0.6/1.0.7 with fail-then-pass fixtures and pinned-stamp parity byte-identity proofs (signed SHA 4c734317...ce92de reproduced four consecutive times). Death-transition family closed at 1.0.5; sibling family closed by enumeration at 1.0.7.
- Partial-consumption record (verbatim per rulings): run-15 halt (G-5) — 7 scored-cell journals written (BTC swing/intraday/position, ETH swing/intraday/position, SOL_swing); run-21 halt (G-6) — 3 more (SOL_intraday, SOL_position, NEAR_swing), 10 total; one-line summaries incl. end equity seen by builder only; values withheld from operator/reviewer.
- G-6 mismatch at the relaunch checkpoint (SOL_position) — ACCEPTED (operator + reviewer, 2026-07-13): one relocated null-valued REJECT row (ts_open 14:00->13:45, reject_reason gap_through_stop->max_tranches, 2023-06-30), the ratified G-6 semantics on a fill-time-rejected sibling pair; zero trading/P&L/equity divergence; four aggregate pairs identical; other 9 cells 9/9 exact; baseline hash updated to 13b84c6b….
- DISCLOSURE: during mismatch verification the reviewer saw two SOL_position aggregates (terminal equity, realized-R total) — bounded, deliberate, recorded; design was frozen pre-run so no hypothesis threshold is affected.
- Final relaunch partial-look checkpoint: 10/10 MATCH (stripped-field canonicalization on record in the manifest).
- Data: census estate, offline, zero fetches. Hypothesis scorecard H-A1..H-A5 in research_outputs/v3_anchor/ (numbers not restated here pending review).
- Reviewer recomputation COMPLETE (2026-07-13): 47 per-cell SHAs, grid evidence hash (sorted-by-cell concatenation), all grid/asset/mandate/grade/taxonomy/annex rollups, strip-best, best campaign (BTCUSDT_swing c197, +114.4519R, 2023-08-16), all five hypothesis verdicts, lockbox max scored open 2024-06-30T22:02Z, and the 10-cell partial-look hashes independently reproduced from raw journals. Grade census: 310 ungraded = 45 V-initiated + 265 no-filled-R1; 21 dual-entry campaigns; scorer earliest-fill rule verified. Headline (1x): -1.6658R/campaign, CI [-2.0407,-1.3597], win 11.28%, grid -5756.9093R / 3456 campaigns; 0x +1345.3095 — cost stack flips the sign. H-A1 INDETERMINATE · H-A2 PASS-partial (C void by design) · H-A3 FAIL · H-A4 PASS · H-A5 FAIL. Per charter: evidence about the mechanical ruleset only. Machinery verdict: PASS.
