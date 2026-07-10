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
