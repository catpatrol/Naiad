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

## 2026-07-15 — V3 RECOMPUTE R1–R10 — Tier A, journals-only
- Basis: engine 1.0.7 (2f260e1), config v12_anchor (a3917ea5…), scored partition, 20 cells.
- Evidence spend: NONE (VR-1 exploration-classic, first look already consumed).
- Engine delta: NONE (read-only phase; no code, config, or replay touched).
- Fixtures: F1–F9 ALL MATCH (10/10 checks; F1 counted as campaigns + tranches). F1 3456/8387 · F2 −5756.9093 · F3 +1345.3095 · F4 −12859.1281 · F5 PROTECTED 3381/STILLBORN 2076/NEVER_GREEN 1830/FADED 1100 · F6 A+ 39/A 1153/B 1954/C 0 · F7 8365 · F8 45 · F9 0.
- F9 = 0 with signal.max_r_count = 0: the reviewer's reading is UPHELD. signals.py:368 (`rcap_ok = max_rc == 0 or r_count < max_rc`) makes the r_cap branch unreachable at max_rc = 0. The signal layer is NOT capping PRIMEs; unlimited adds remains a trading-config-only change (trading.max_tranches), not Pine-parity-bound.
- Predictions scored: P-R1 [FALSIFIED — X-A gross delta swing +528.92, position −97.23 (loses), intraday −421.47] P-R2 [CONFIRMED — V share of Σwins 0.60% vs 1.30% share of campaigns; under-, not over-represented] P-R6 [CONFIRMED — Z2 stage-1 100.0%, but see degeneracy below] P-R7 [CONFIRMED — tranche_cap rejects 145,749 ≫ 500] P-R9 [CONFIRMED — def_full 1× = −592.3839, still net negative].
- Determinism: script re-run hash 2640decda9bb23c4c98e9280907962902d06546065d9c89bacd2afbb293eac71 — identical [Y]. Component hashes: recompute.json 9bdea8ef…, V3_RECOMPUTE_R1_R10.md ca73bac2…. Seed 20260715 pinned, 10,000 resamples, campaign-level.
- PARTIAL items (named gaps, no estimates substituted): R4 "median MFE at first trigger" — mfe_r is whole-life MFE (shadows.py:167); trigger bar index never journaled. Missing field: mfe_at_tpw_r / mfe_at_ext_r on the EXIT row. R4 "extension before their exit" — engagement_flags.ext_before_exit is computed over [fill_i, camp_end], not [fill_i, exit_i] (shadows.py:190-194), so it is mis-windowed and cannot be narrowed post hoc; missing field: ext_i_offset, or a correctly-windowed boolean, on the EXIT row.
- Builder findings not previously registered (each recomputed from raw bytes, none affecting a fixture):
  (a) ZECUSDT_intraday traded on NEGATIVE realized equity from 2022-11-02 (min −2,732.24, final −2,719.97); 717 of its 1,414 tranches carry a negative one_r (= r_pct × equity, trading.py:367) with inverted qty sign. The §4 signed formula reproduces F3/F4 exactly, so this is journaled faithfully and is NOT a reader artifact — but a bankrupt-cell-keeps-trading path is a finding about the anchor run and every R-denominated quantity on those rows is measured against a negative unit.
  (b) engagement_flags.ext_before_exit is MISNAMED: it means ext_before_CAMPAIGN_DEATH. tpw_before_exit (via Tranche.first_tpw_i, trading.py:412-415) is strict; the two flags are named as a pair but measure different windows and must not be compared.
  (c) TPW essentially never fires while positioned: 2 of 1,581 R4-population tranches (0.13%); independent timestamp scan finds only 16 of 2,999 TPW event rows falling inside any open same-dir tranche window. A TPW-armed harvest rule would almost never trigger on this run; the 2-ATR extension is the only viable arming trigger of the two.
  (d) R6 zone×stage is NEARLY DEGENERATE: Z2 fills are 100% stage-1 (0 stage-2), Z3 fills are 100% stage-2 (0 stage-1). Two of six Z1/Z2/Z3×stage cells are structurally empty. P-R6 is confirmed trivially, not marginally; any Z2-vs-Z3 expectancy read is confounded with a stage effect and cannot be separated from these journals.
  (e) R3 'ratcheted-≥-BE' is empty BY CONSTRUCTION for the gross-loss population (a stop at/beyond BE cannot fill at a gross loss) — a tautology of the filter, not evidence the ratchet never reaches breakeven.
- Reviewer cross-checks reproduced independently from raw bytes (not read as inputs): grid net −5756.9093, 0× +1345.3095, expectancy −1.6658, win 11.28%, campaigns 3456, strip-best −5871.3612, best campaign BTCUSDT_swing c197 +114.4519, grade census 310 ungraded = 45 V-initiated + 265 no-filled-R1, and Report 1's 2,899 per-tranche resumption count (per-event denominator: 2,461 of 7,057 events).
- Artifacts: scripts/v3_recompute.py, V3_RECOMPUTE_R1_R10.md, recompute.json.
- Operator ratification: 2026-07-15 (D1, D2, D4–D9 on silence; D3 VS-Z3 HELD — z3_prox unchanged at 0.35, not implemented this phase).
- Open: G-7 (in-sample iteration budget untracked) logged this phase.
- G-7 [OPEN]: No counter — code-level or ledger-level — on tuned exploration-classic re-runs. The five named-variant slots bind only at the lockbox; nothing tracks Tier-C iteration on mined data. Mitigation: every Tier-C exploration-classic run gets a pre-registered ledger line (config sha + hypothesis + prediction) BEFORE it runs. Logged 2026-07-15 on operator ratification of D7.

## 2026-07-17 — RC RECOMPUTE RC-0–RC-6 — Tier A, journals + filesystem inventory
- Basis: engine 1.0.7 (2f260e1), config v12_anchor (a3917ea5…), scored partition, 20 cells. Primary basis scored-clean (19 cells, ZECUSDT_intraday excluded per G-8); scored-20 carried as reference on every table.
- Evidence spend: NONE (VR-1, first look already consumed). Engine delta: NONE (read-only; journals + local kline parquet caches only, no replay/config/engine/network touch).
- Fixtures: F1–F10 ALL MATCH (12/12 checks; F1 and F4 counted as two each). F1 3456 campaigns / 8387 tranches · F2 −5756.9093 · F3 +1345.3095 · F4 ZEC_intraday 1414 tranches / 717 neg-one_r · F5 ZEC_intraday net 1× −663.1247 · F6 scored-clean 1× −5093.7846 (= F2 − F5) · F7 7057 stop-exit events · F8 145749 tranche_cap(max_tranches) rejects · F9 45 V-initiated campaigns · F10 2899 per-tranche resumption.
- Predictions scored: P-RC1a [CONFIRMED — re-entries 77.30% of 4335 ADD_FILL rows ≥70%] P-RC1b [FALSIFIED — true-add per-unit gross 0.2341 < re-entry 0.4325] P-RC1c [FALSIFIED — top-10 split 5 stacked (max_conc=3) / 5 serial; the falsifier "≥5 stacked" is met] P-RC2 [CONFIRMED — no cell besides ZEC_intraday crossed zero] P-RC3 [CONFIRMED — swing median mfe_bps 27.81 > cost 19.91; intraday 10.03 < 19.62] P-RC4 [CONFIRMED — net/unit non-monotone, max at D6 stop/ATR∈[1.26,1.37), inside 0.75–1.50] P-RC5 [CONFIRMED — drop-Z1 first-order Δ +3889.67 ≥ +1500] P-RC6 [FALSIFIED — expectancy not monotone: att1 −1.716 > att2 −2.133 < att3 −1.629, inversion at 2→3].
- Scored-clean certification: CERTIFIED — no cell other than ZECUSDT_intraday (min equity −2732.24, 1 zero-crossing) crossed zero. Four intraday cells near-missed (<20% of 10000 initial): ETH_intraday min 2.36, BTC_intraday 56.65, SOL_intraday 43.48, NEAR_intraday 94.81. Basis valid; phase ran to completion (no §8 HALT).
- Determinism: double-run byte-identical [Y]. sha256(rc_recompute.json) = 94273bca31824d6f603a3974519f31df92a2be8a7dc58c2647646ee1a2302abd · sha256(RC_RECOMPUTE_RC0_RC6.md) = 3e590621eef7eeb186436e2beeb378146d8b54f0f7a59051f28e28dca82159ac · OUTPUT_HASH = bbd8536c00bbb01457fd6c05a297c5102327ea95352cbae8e3b5dcd916d4115b. Seed 20260716 pinned, 10,000 resamples, campaign-level.
- Builder findings (each from raw bytes; none affects a fixture; all observational — selection effects are NOT causal, per the RC-1 caveat):
  (a) The add/re-entry split decomposes Report 1's "adds carry the edge (+0.47/unit)": on scored-clean the gross-0× per-unit edge lives in RE-ENTRIES (0.4325/unit), not true adds (0.2341/unit). But re-entries are catastrophic net (−2.5179/unit) and carry −4218.67 of the −5093.78 scored-clean loss — the dominant loss driver — because a re-entry fires after equity erosion where one_r (= r_pct × equity) is small, inflating cost/one_r. Decomposition sums exactly to F6: R1 −582.40 + true_add −292.14 + re_entry −4218.67 + V −0.59.
  (b) By max_concurrent, only the stacked-pyramid cohort is profitable: mc=1 1885 camps −4806.69 (exp −2.55, win 2.5%), mc=2 879 −838.06 (−0.95, 17.3%), mc=3 113 +550.97 (+4.88, win 72.6%). Buckets sum to F6. This is a survivorship read (reaching mc=3 requires two ratchet-to-BE adds, i.e. a trend), not a causal effect of stacking.
  (c) Top-10 by cell-R are all 3-tranche, but structurally SPLIT — 5 true stacked pyramids (max_concurrent=3), 5 serial re-entries / partial-stacks — refuting Report 1's "all top-10 are full 3-tranche ladders [pyramids]." #1 = BTCUSDT_swing c197 +114.45 (R1 + 2 true adds), consistent with the R1–R10 best-campaign cross-check.
  (d) RC-4 supports a stop-distance floor: the tightest decile D1 (stop/ATR < 0.586) is catastrophic (net −8.89/unit, cost 10.72/unit — same tiny-one_r mechanism as re-entries); D2 onward net/unit is −0.56…−1.16, best (least-negative) at D6 (stop/ATR 1.26–1.37).
  (e) RC-5: Z1-initiated campaigns are 2038/2877 = 70.8% of scored-clean campaigns and carry ~76% of the loss; drop-Z1 first-order lifts 1× from −5093.78 to −1204.12 (Δ +3889.67), half-size-Z1 to −3148.95.
  (f) RC-6: attempt-2+ re-tries are almost never clustered near the first attempt — in-cluster share of attempts 2+ is 2.4% (k=0.5) / 4.5% (k=1.0) / 6.6% (k=1.5). A 3-strike CLUSTER rule (in-cluster attempts 4+) would remove near-zero cell-R: it is nearly a mechanical non-event on this run — sizes TC-2 before it is designed.
  (g) RC-0: all 10 assets (7 scored + HYPE, FARTCOIN, LIT) carry {1m,5m,15m,1h,4h,12h}; 30m and 1d are ABSENT for every asset; 15m present for every asset. Both absent TFs are locally resamplable (30m from 15m/1m, 1d from 1h/1m) — feasibility only, resampling is S-1 data-prep, out of scope. Zero gaps>2×TF anywhere.
- PARTIAL items: none — every RC-0…RC-6 field was journaled or on the filesystem.
- Artifacts: scripts/rc_recompute.py, RC_RECOMPUTE_RC0_RC6.md, rc_recompute.json. Not pushed, not merged (builder-typed, append-only).
- Next: TC-4 contract (guards + schema/nomenclature fix + re-anchor), then risk-mode interview (on RC-1/RC-3), then S-1 on clean journals.
