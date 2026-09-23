# R0 ADDENDUM — the R0.2 ledger as filed, beside the ledger as it stands

> **REPORT-ONLY.** A ledger, not a result: no registration is scored, no verdict file
> is opened, no bar is read. For `BUILD_DRAFT.md` §R0 at CLOSE; the draft itself is not
> edited. Every status, count, commit and blocker below is read from `PROGRESS.json`, its
> committed history, or the git log — none is typed.

- **PROGRESS.json** sha256 `0d66f2d7fe6c338339880368ff854e58bbb2533be54cf2f7448f71d129752afc` — 15 stages; working tree == its newest committed blob: **True**.
- **BUILD_DRAFT.md** sha256 `1ec7b93c5b4590ded7aa7f02621938b101001df9ccdd25c2ef808338a554fa97` — last changed at `f97cded`.
- **Committed ledgers read:** 8 (`git log -- research_outputs/tierc10/PROGRESS.json`), oldest `f97cded`, newest `08a6fce`.

## A · HISTORY — the R0.2 table as filed, verbatim

*REPORT-ONLY · HISTORY, NOT CURRENT.* Copied byte-for-byte from `BUILD_DRAFT.md` §R0.2, lines 64–74. It re-renders byte-identically from `PROGRESS.json` as committed at `f97cded` (F-SL-R0SEAL): at R0.2, 5 COMPLETE-VERIFIED and 4 PARTIAL of 9 stages.

| stage | status | artifacts re-hashed | fixtures, re-run NOW | blockers |
|---|---|---|---|---|
| STEP 0 | **COMPLETE-VERIFIED** | 1 | `TIER-C10 STAGE 0a · RANGEFINDER CENSUS PORT FIXTURES (run 1)` exit 0, 0 red, no drift; `TIER-C10 STAGE 0a · RANGEFINDER CENSUS PORT FIXTURES (run 2, exit-code + reproducibility confirmation)` exit 0, 0 red, no drift | 0 |
| D-CORE | **PARTIAL** | 13 | `TIER-C10 Stage D fixtures — OFFLINE mode (no venue API)` exit 0, 0 red, no drift; `TIER-C10 Stage D fixtures — targeted named legs F-D-1 (matches F-D-1 and F-D-1b), ONLINE; these legs fetch the venue themselves and this mode writes no transcript` exit 1, 1 red, no drift | 7 |
| CENSUS-R{4h,1d} | **PARTIAL** | 372 | `CENSUS-R (TIER-C10 STAGE 0b) census fixtures` exit 0, 0 red, no drift | 3 |
| NULL/gaps-only | **COMPLETE-VERIFIED** | 312 | `F-NULL (scripts/tierc10_null_fixtures.py, --null-root=research_outputs/tierc10/null/gaps_only)` exit 0, 0 red, no drift | 0 |
| NULL/gaps+order | **COMPLETE-VERIFIED** | 312 | `tierc10_null_fixtures.py (F-NULL-COV, F-NULL-BOX, F-NULL-ASOF, F-NULL-SANE, F-NULL-GRID, F-NULL-DET) against --null-root=research_outputs/tierc10/null/gaps_order` exit 0, 0 red, no drift | 0 |
| A (stamps) | **COMPLETE-VERIFIED** | 10 | `Stage A — tierc10_stamps_fixtures.py (run 1 of 2)` exit 0, 0 red, no drift; `Stage A — tierc10_stamps_fixtures.py (run 2 of 2, timed)` exit 0, 0 red, no drift; `Stage A — scratch rebuild (my own extra determinism check; NOT the canonical root)` exit 0, 0 red, no drift | 0 |
| PANEL/gate | **COMPLETE-VERIFIED** | 11 | `TIER-C10 PANEL fixtures (scripts/tierc10_panel_fixtures.py)` exit 0, 0 red, no drift | 0 |
| LANES (B mech) | **PARTIAL** | 2 | `tierc10_lanes_fixtures` exit 0, 0 red, no drift | 7 |
| BRK (B mech) | **PARTIAL** | 2 | `F-BRK (scripts/tierc10_brk_fixtures.py) — 15 fixtures` exit 0, 0 red, no drift | 6 |

## B · AS IT STANDS — the same renderer over PROGRESS.json now (15 stages)

*REPORT-ONLY · the ledger as it stands.* The five columns of §A, printed by the same renderer, so each row reads beside its R0.2 row. The fixtures column lists every fixture record the ledger holds for the stage. Now: 13 COMPLETE-VERIFIED, 2 PARTIAL.

| stage | status | artifacts re-hashed | fixtures, re-run NOW | blockers |
|---|---|---|---|---|
| STEP 0 | **COMPLETE-VERIFIED** | 1 | `TIER-C10 STAGE 0a · RANGEFINDER CENSUS PORT FIXTURES (run 1)` exit 0, 0 red, no drift; `TIER-C10 STAGE 0a · RANGEFINDER CENSUS PORT FIXTURES (run 2, exit-code + reproducibility confirmation)` exit 0, 0 red, no drift | 0 |
| D-CORE | **PARTIAL** | 15 | `TIER-C10 Stage D fixtures — OFFLINE mode (no venue API)` exit 0, 0 red, no drift; `TIER-C10 Stage D fixtures — targeted named legs F-D-1 (matches F-D-1 and F-D-1b), ONLINE; these legs fetch the venue themselves and this mode writes no transcript` exit 1, 1 red, no drift; `tierc10_data_fixtures --offline (F-D-1 / F-D-1b NOT RUN; the ONLINE suite keeps F-D-1 RED by design)` exit 0, 0 red, no drift | 8 |
| CENSUS-R{4h,1d} | **COMPLETE-VERIFIED** | 399 | `tierc10_census_fixtures` exit 0, 0 red, no drift | 0 |
| NULL/gaps-only | **COMPLETE-VERIFIED** | 312 | `tierc10_null_fixtures` exit 0, 0 red, no drift | 0 |
| NULL/gaps+order | **COMPLETE-VERIFIED** | 312 | `tierc10_null_fixtures` exit 0, 0 red, no drift | 0 |
| A (stamps) | **COMPLETE-VERIFIED** | 10 | `Stage A — tierc10_stamps_fixtures.py (run 1 of 2)` exit 0, 0 red, no drift; `Stage A — tierc10_stamps_fixtures.py (run 2 of 2, timed)` exit 0, 0 red, no drift; `Stage A — scratch rebuild (my own extra determinism check; NOT the canonical root)` exit 0, 0 red, no drift | 0 |
| PANEL/gate | **COMPLETE-VERIFIED** | 11 | `TIER-C10 PANEL fixtures (scripts/tierc10_panel_fixtures.py)` exit 0, 0 red, no drift | 0 |
| LANES (B mech) | **COMPLETE-VERIFIED** | 4 | `tierc10_lanes_fixtures` exit 0, 0 red, no drift; `tierc10_lanes_fixtures (post-filing repair; run whole twice)` exit 0, 0 red, no drift | 0 |
| BRK (B mech) | **COMPLETE-VERIFIED** | 7 | `tierc10_brk_fixtures` exit 0, 0 red, no drift; `tierc10_brk_fixtures (real F-C10-HOLD + READY + cleanup; run whole twice)` exit 0, 0 red, no drift | 0 |
| F-C10-RESUME | **COMPLETE-VERIFIED** | 0 | `tierc10_resume_fixtures` exit 0, 0 red, no drift | 0 |
| D-5M | **PARTIAL** | 2 | `tierc10_data_fixtures --offline, the 5m legs (run twice)` exit 0, 0 red, no drift | 1 |
| CENSUS-R{5m} | **COMPLETE-VERIFIED** | 1 | `tierc10_census_fixtures (the legs covering 5m, run twice)` exit 0, 0 red, no drift; `tierc10_null_fixtures 5m legs, gaps+order (null of record, R10)` exit 0, 0 red, no drift; `tierc10_null_fixtures 5m legs, gaps-only` exit 0, 0 red, no drift | 0 |
| B-REG (the six filed) | **COMPLETE-VERIFIED** | 11 | `tierc10_score_fixtures (F-SC-RECORD holds the filed record against REGISTRY_PIN.json: length, head, order, per-reg seq/payload/text sha; run whole twice)` exit 0, 0 red, no drift | 0 |
| B-CORE | **COMPLETE-VERIFIED** | 17 | `tierc10_score_fixtures (driver certification; run whole twice)` exit 0, 0 red, no drift | 0 |
| B-5M | **COMPLETE-VERIFIED** | 5 | `tierc10_score_fixtures (driver certification; run whole after B-5M)` exit 0, 0 red, no drift | 0 |

## C · WHAT MOVED — status at R0.2 beside status now

*REPORT-ONLY.* **moved at** = the first committed ledger that records COMPLETE-VERIFIED right after a committed PARTIAL record (the ledger commit that moved the stage). **repair window** = the tierc10 commits in (last PARTIAL record, move] — the candidates the git log names, NOT an attribution. **born** = the first committed ledger that holds the stage.

| stage | at R0.2 | now | born | moved PARTIAL → COMPLETE-VERIFIED at | repair window | blockers now |
|---|---|---|---|---|---|---|
| STEP 0 | **COMPLETE-VERIFIED** | **COMPLETE-VERIFIED** | COMPLETE-VERIFIED at `f97cded` | — never PARTIAL in a committed ledger | — | 0 |
| D-CORE | **PARTIAL** | **PARTIAL** | PARTIAL at `f97cded` | — still PARTIAL | — | 8 |
| CENSUS-R{4h,1d} | **PARTIAL** | **COMPLETE-VERIFIED** | PARTIAL at `f97cded` | `6b15def` · 2026-09-22T15:23:49-03:00 (last PARTIAL record `f97cded`) | 8: `ffdffce` `54cfd60` `d8a6f81` `a58bafc` `1359d99` `590989d` `80ecca5` `6b15def` | 0 |
| NULL/gaps-only | **COMPLETE-VERIFIED** | **COMPLETE-VERIFIED** | COMPLETE-VERIFIED at `f97cded` | — never PARTIAL in a committed ledger | — | 0 |
| NULL/gaps+order | **COMPLETE-VERIFIED** | **COMPLETE-VERIFIED** | COMPLETE-VERIFIED at `f97cded` | — never PARTIAL in a committed ledger | — | 0 |
| A (stamps) | **COMPLETE-VERIFIED** | **COMPLETE-VERIFIED** | COMPLETE-VERIFIED at `f97cded` | — never PARTIAL in a committed ledger | — | 0 |
| PANEL/gate | **COMPLETE-VERIFIED** | **COMPLETE-VERIFIED** | COMPLETE-VERIFIED at `f97cded` | — never PARTIAL in a committed ledger | — | 0 |
| LANES (B mech) | **PARTIAL** | **COMPLETE-VERIFIED** | PARTIAL at `f97cded` | `899d3e7` · 2026-09-22T21:45:01-03:00 (last PARTIAL record `2e92972`) | 6: `41a5070` `83f5e29` `fa205c8` `74d9b39` `371123f` `899d3e7` | 0 |
| BRK (B mech) | **PARTIAL** | **COMPLETE-VERIFIED** | PARTIAL at `f97cded` | `899d3e7` · 2026-09-22T21:45:01-03:00 (last PARTIAL record `2e92972`) | 6: `41a5070` `83f5e29` `fa205c8` `74d9b39` `371123f` `899d3e7` | 0 |
| F-C10-RESUME | — (not in R0.2) | **COMPLETE-VERIFIED** | COMPLETE-VERIFIED at `6b15def` | — never PARTIAL in a committed ledger | — | 0 |
| D-5M | — (not in R0.2) | **PARTIAL** | PARTIAL at `899d3e7` | — still PARTIAL | — | 1 |
| CENSUS-R{5m} | — (not in R0.2) | **COMPLETE-VERIFIED** | COMPLETE-VERIFIED at `899d3e7` | — never PARTIAL in a committed ledger | — | 0 |
| B-REG (the six filed) | — (not in R0.2) | **COMPLETE-VERIFIED** | COMPLETE-VERIFIED at `899d3e7` | — never PARTIAL in a committed ledger | — | 0 |
| B-CORE | — (not in R0.2) | **COMPLETE-VERIFIED** | COMPLETE-VERIFIED at `ab7306a` | — never PARTIAL in a committed ledger | — | 0 |
| B-5M | — (not in R0.2) | **COMPLETE-VERIFIED** | COMPLETE-VERIFIED at `08a6fce` | — never PARTIAL in a committed ledger | — | 0 |

Moved PARTIAL → COMPLETE-VERIFIED since R0: 3 (CENSUS-R{4h,1d}, LANES (B mech), BRK (B mech)).

## D · THE REMAINING PARTIALS — blockers verbatim

*REPORT-ONLY.* Each blocker is `PROGRESS.json`'s string, byte-for-byte, one bullet each, in the ledger's order; nothing is summarised, merged or dropped.

### D-CORE — PARTIAL · 8 blockers

- RESUME CLAUSE F-D-4 (TWO-TOKEN TRAP) — no artifact, no fixture leg. LEGS[] in scripts/tierc10_data_fixtures.py has no F-D-4 entry. STAGE_D_MANIFEST.json/.md contain zero occurrences of 'two-token', 'first_valid', 'hard_floor', 'hard-floor', 'continuity', 'price_continuity', 'predates', 'intended'. Verdict PARTIAL-in-substance / ABSENT-as-artifact: listing date + source ARE printed per file row (137 'listing' occurrences; every kline row carries listing + source + publication) and PUMPBTCUSDT IS rejected by name in venue_rejections with LEAN D-d, but the hard-floor check, the price-continuity-at-the-floor check and the F-D-4 table itself do not exist. The contract demands it (resume paste line 135: 'Stage D manifest incl. the F-D-4 / F-D-5 tables'); research_outputs/tierc10/BUILD_DRAFT.md:86 carries only the placeholder '*Including the F-D-4 two-token-trap table and the F-D-5 data-spend audit.*'
- RESUME CLAUSE F-D-5 (DATA-SPEND AUDIT) — ABSENT outright. No fixture leg in LEGS[]. Zero occurrences of 'never-touched', 'display-only', 'data-spend', 'spend' in STAGE_D_MANIFEST.json and .md. Nothing under research_outputs/tierc10/ carries the classification except the BUILD_DRAFT.md placeholder line. No {never-touched / display-only / scored} table exists per asset for the 17, so PUMPFUN and HYPE are neither read nor assumed — they are simply unclassified.
- RESUME CLAUSE COSTS HAIRCUT TWIN (tiered slippage per side, A/B/C = 2/5/10 bps) — ABSENT from Stage D. fee_schedule.json carries zero occurrences of 'slip', 'Slip', 'SLIP', 'haircut', 'Haircut', 'multiplier'; its per-asset key set is exactly ['asset','funding_interval_hours_observed_modal','funding_interval_hours_observed_tail','funding_spacing_hours_histogram','kind','round_trip_bps_used','source','stem','symbol','taker_bps_side_used','venue','venue_note'] with a FLAT taker_bps_side_used=5.0 and round_trip_bps_used=10.0 for all 17 assets and no slippage column at all. The tier concept exists elsewhere in the estate but for a DIFFERENT roster: Naiad_Phase0_Charter.md:114 reads 'tier A (BTC, ETH) 2 bps · tier B (SOL, NEAR, ZEC, JTO, TAO) 5 bps · tier C (HYPE, FARTCOIN, LIT) 10 bps' and scripts/v3_scorer.py:309 repeats '2/5/10 bps' as a modeled-note string. The resume paste's TC10 assignment (tier B += LTC BNB DOGE UNI SUI XMR; tier C = ENA PUMPFUN HYPE MNT PEPE BONK) appears nowhere on disk outside the contract text itself.
- RESUME CLAUSE CONTRACT MULTIPLIERS (1000PEPE, 1000BONK) printed and normalized — ABSENT. Zero occurrences of 'multiplier', 'contractSize', 'contract_size', 'quantity_multiplier', 'notional', 'per_unit' in STAGE_D_MANIFEST.json; zero of 'multiplier'/'normali' in STAGE_D_MANIFEST.md; zero of 'multiplier'/'contractSize'/'quantityPrecision'/'filters' in VENUE_PROBE.json (the probe never captured the field). The manifest prints the symbols (venues rows: asset PEPE -> symbol 1000PEPEUSDT; asset BONK -> symbol 1000BONKUSDT) and their prices, but never states that the contract is per 1000 tokens and never normalizes. Any downstream cross-asset price or height comparison will be off by 1000x for these two.
- F-D-1 STAYS RED pending an operator ruling that does not yet exist. Re-run NOW it is RED (exit 1). Operator ruling R5 of 2026-09-21 ('The USDT pair, either on Binance or Bybit', recovered verbatim in research_outputs/tierc10/OPERATOR_RULINGS.md) does not distinguish the venue's REST API from its BULK ARCHIVE, which is the actual disagreement. This is the designed red, not a break — but it is an open operator dependency on the stage.
- CARRIED AS-OF HAZARD: 14 of the 102 kline files hold rows past the pin — every 5m file except PUMPUSDT, MNTUSDT_BYBIT and SUIUSDT, 6 rows each (opens 16:00, 16:05, 16:10, 16:15, 16:20, 16:25Z). Item 3's literal law ('no kline file holds a row after 1790006400000') is FALSE at file level. It holds at loader level. The manifest discloses this itself (as_of_hazards.kline_law, LEAN D-e) and warns that tierc2_baseline.load_klines reads the WHOLE file, so any TC10 lane loading through it instead of tierc10_data.load_asof reads past the pin. Not repairable in this stage (no deletion primitive, prefixes are never rewritten) but it is a live trap for Stage A and downstream.
- TRANSCRIPT BYTE-REPRODUCIBILITY IS DISPROVEN, and could not be tested directly. FIXTURES_STAGE_D.txt is only rewritten by a FULL online run with no leg arguments; --offline writes FIXTURES_STAGE_D_OFFLINE.txt instead and a named-leg run writes nothing (main() guards on `if not want`). So my two runs left it byte-identical (69a22de8... before and after) without exercising the builders' claim. But F-D-1b's own census moved between the filed run and mine — {'archive-only': 74, 'both': 215, 'rest': 28, 'rest-only': 105} became {'archive-only': 74, 'both': 223, 'rest': 20, 'rest-only': 105} — so 8 bars the venue's bulk archive did not publish on 2026-09-21 it does publish on 2026-09-22. A full re-run's transcript CANNOT be byte-identical to the filed one, because the venue's archive backfills.
- REPAIRED 2026-09-22: F-D-4, F-D-5, the tiered haircut twin and contract multipliers are built and filed; those four clauses no longer block. What remains is F-D-1's operator ruling: REST or ARCHIVE.

Notes in the ledger: 0.

### D-5M — PARTIAL · 1 blocker

- F-D-1 (online) stays RED pending the operator's REST-or-ARCHIVE word (R5's narrower question); one of its three differing bars is XMRUSDT 5m. Does NOT reach B-5M: P-BRK-S1 pins substrate tc10_20260921.

Notes in the ledger: 0.

## E · STATUS IN EVERY COMMITTED LEDGER

*REPORT-ONLY.* One column per commit that touched `PROGRESS.json`, oldest first, then the working tree. CV = COMPLETE-VERIFIED · P = PARTIAL · `·` = the stage is not in that ledger · ≡ = that ledger carries today's `one_line` verbatim.

| stage | `f97cded` | `6b15def` | `3453c87` | `2e4d959` | `2e92972` | `899d3e7` | `ab7306a` | `08a6fce` | now |
|---|---|---|---|---|---|---|---|---|---|
| STEP 0 | CV ≡ | CV | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV |
| D-CORE | P | P | P ≡ | P ≡ | P ≡ | P ≡ | P ≡ | P ≡ | P |
| CENSUS-R{4h,1d} | P | CV | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV |
| NULL/gaps-only | CV ≡ | CV | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV |
| NULL/gaps+order | CV ≡ | CV | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV |
| A (stamps) | CV ≡ | CV | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV |
| PANEL/gate | CV ≡ | CV | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV |
| LANES (B mech) | P | P | P | P | P | CV ≡ | CV ≡ | CV ≡ | CV |
| BRK (B mech) | P | P | P | P | P | CV ≡ | CV ≡ | CV ≡ | CV |
| F-C10-RESUME | · | CV | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV ≡ | CV |
| D-5M | · | · | · | · | · | P ≡ | P ≡ | P ≡ | P |
| CENSUS-R{5m} | · | · | · | · | · | CV ≡ | CV ≡ | CV ≡ | CV |
| B-REG (the six filed) | · | · | · | · | · | CV ≡ | CV ≡ | CV ≡ | CV |
| B-CORE | · | · | · | · | · | · | CV ≡ | CV ≡ | CV |
| B-5M | · | · | · | · | · | · | · | CV ≡ | CV |
