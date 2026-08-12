# LEDGER_APOLLO — append-only lane ledger

**Lane:** APOLLO — engine builds · repo operations · integrity & manifest.
**Adopted:** 2026-08-02, ruling Q-3 A (`FUNNEL_DIONYSUS_W1`). Append-only. Never edit a past entry; a
correction is a NEW entry that names what it supersedes. The central `LEDGER.md` remains the
*evidence* ledger and is untouched by this file — this one carries coordination state only.

**Entry template (naiad-eod format):**

```
=== STATUS_<LANE> — <date> ===
NOW: <2-3 sentences>
LAST EVENT: <date> — <one line>
FACTS: <up to 6 lines, each ending with [verified/ledger/ratified/handoff/unconfirmed-live/open]>
PENDING: <numbered items waiting on the operator>
NEXT: <single next action + owner>
METRICS: operator actions this session = <n> · files re-ingested = <n>
=== END STATUS ===
```

---

=== STATUS_APOLLO — 2026-07-27 ===
NOW: Engine 1.0.11 frozen. Repo at manifest snapshot HEAD 60e00c9, ahead 4 / behind 0 vs origin 70a5be0, worktree clean. THE BIG CORRECTION: the raw price estate was never under OneDrive — it sat unprotected in AppData\Local\naiad\data_cache (633.5 MB, 71 files) for the project's whole life, and now has its first offsite backups on two independent Google Drive accounts.
LAST EVENT: 2026-07-27 — Estate protection established; OneDrive root-caused (quota exhaustion, 21.78 GB tree); 19.61 GB reclaimed across six archived phases (13,502 members, 0 mismatches, reviewer re-hashed 6/6 + 90 sampled members; 25 git-tracked files preserved in place); tree down to ~1.9 GB.
FACTS:
- Integrity at snapshot: 46/46 tracked sources match HEAD; box 19 repo copies match + 2 brief artifacts + 1 stale .gitignore [verified]
- Rulings R-A (cloud sessions scoped to Naiad only), R-B (second-cloud dated non-overwriting archives), R-C (corrections folded, 713dfa7→72b921f amended-SHA on record) [ratified]
- Standing rule: every paste-go opens with a hard environment assertion that halts — read-only included — and no write precedes it; gates written from POST-action state [ledger]
- Routing failures final count on 07-26/27: seven, not three; every labelled paste was halted by its header [ledger]
- %G? reports N when SSH verification is impossible, not only when unsigned — not a signature-presence test [verified]
PENDING:
1. PUSH RULING — unpushed commits were then the only asset without an off-machine copy
2. R-A' proposed, not ruled: cloud-session commits must push same-session or they don't count
3. s3_excursion_substrate.jsonl git-tracked while sibling substrates are fenced — exception or drift?
4. Remaining backup steps: six phase archives to the second cloud · .venv relocation · .gitignore sync exclusions
NEXT: Item 1 (push ruling), then a fresh MANIFEST.json to confirm ahead/behind returns to 0. Owner: operator.
METRICS: operator actions this session = not recorded (predates Q-8) · files re-ingested = not recorded
=== END STATUS ===

**Provenance note (HEPHAESTUS, 2026-08-02):** this seed entry is a synthesis of the lane's standing
status document, carried over unmodified in substance at ledger adoption. Source document:
`docs/history/STATUS — ENGINE (engine builds · repo operations · integrity & manifest).txt`
(2,917 B, updated 2026-07-27 late) — it sat at repo root when this ledger was seeded and was **moved
to `docs/history/` later the same day** by the repo filing pass; the pointer is updated here so it
does not rot. It is dated 2026-07-27 and its PENDING items may since have been resolved — several of
them demonstrably were. **Treat as stale until APOLLO appends a current entry.** [handoff]

---

=== STATUS_APOLLO — 2026-08-10 ===
NOW: The 9-day staleness is closed. This entry lands the owed append (re-priming 08-05 + rulings
08-06 + the synthesis filing) and carries the MC-1 v2 run executed locally on branch v12-v1-census
at HEAD 7a3a881. The P-SEQ-ii ledger-entry check owed since 08-04 is discharged with a NEGATIVE
finding: the entry does not exist in `LEDGER.md` and never did.
LAST EVENT: 2026-08-10 — MC-1 v2 (THE MAY-26 PROGRAM) executed end to end by HEPHAESTUS: D-1 D-3
D-4 D-5 D-6 D-7 D-8 built, F-MC1..F-MC11 run, three registrations scored before their result tables.
FACTS:
- Re-priming after context loss recorded 2026-08-05; rulings 2026-08-06 = MC defaults (every *Lean*
  of MC-1..7, §3.4) + rule set v0.2 (§1.2) + the path committed to memory (§3.1) [ratified]
- Amendment 2026-08-06 "continuous queryability before/after the cross" honoured by D-3(a)/(f); the
  offered lockbox change was DECLINED as unnecessary — the dossier is ops-class and the seal was
  NOT modified by this contract [ratified]
- `SS_SYSTEM_SYNTHESIS_2026-08-06.md` was NOT attached to the MC-1 paste; the resident copy is
  filed and hashed sha256 f184f105c0612128c9ed5819d72fe6ff0c2d123378b0923d08b90bc856c4c7f2,
  31,822 B, 0 CR bytes — byte-identical filing re-asserted, not overwritten [verified]
- P-SEQ-ii: `grep -c "P-SEQ" LEDGER.md` -> 0 over 871 lines. The entry is ABSENT, not divergent —
  neither CONFORMS nor a diff. Registration text and the ordering-anomaly note exist only outside
  the evidence ledger and are reproduced verbatim in the build document [verified]
- MC-1 headline: D-1 490 cells (F-MC1 0 diffs on all 56 SEQ8-D6 overlap cells, 3 hand-recomputed);
  D-4 1,569 4H lattice-A crosses, strict core 4/4 = 105; D-6 bridge 301,018 rows, 0 orphans
  join->journal, 286 births never joined (SEQ8's own figure); P-i SUPPORTED 3/5, P-iii SUPPORTED
  (L 52.3% vs W 14.0%, CI [0.316,0.448]), P-iv SUPPORTED 3/5 [verified]
PENDING:
1. P-SEQ-ii ledger entry still UNLANDED — the proposed text (prior 75%, verdict REPLICATES 7/7)
   is the reviewer's to land in `LEDGER.md`; the builder does not write to the evidence ledger
2. P-i and P-iv are VIEW-DEPENDENT: both score 3/5 on `24h|window_chained` but 2/5 on all four
   `direction_consistent` views. The registrations named no view. Operator ruling wanted
3. MC-1's §3.4 feasibility premise ("1M carrying {12,25} only, 1W carrying up to 200") does not
   hold under the exploration ceiling — it assumed full-estate bar counts. D-1 measures 1W to
   EMA25 and 1M to EMA12 only
4. `scripts/mc1_program.py` is uncommitted: `publish_exchange.py` stages only `exchange/**`, so
   the program itself cannot ride the auto-publish
NEXT: Operator rules on PENDING 2 (view selection for P-i/P-iv); reviewer lands PENDING 1. Owner:
operator, then APOLLO.
METRICS: operator actions this session = 1 (the MC-1 paste) · files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-12 ===
NOW: CENSUS-2A paste #1 built and run. MC-2 did not exist in any form and has been written
(scripts/mc2_program.py), extended per operator word to pin all six placeholders rather than the
three its commission covered. Constants pinned OUT-OF-SAMPLE on the live era, evidence era printed
beside. The census remains NOT EXECUTABLE: conditions (2) and (3) are open, and placeholder (iv) is
unresolved.
LAST EVENT: 2026-08-12 — MC-2 (extended) + CEN-0(a) executed; F-1/F-PARITY/F-3/F-DET all pass
FACTS:
- MC-2 had no artifact on C: or D:; "drafted, D:-resident" was uncorroborated [verified]
- TRAP fallback >=2 fires on 91.5% live / 92.2% evidence of 4h lattice-A armings — a null gate;
  rejection replicates, the >=5 replacement does not [verified]
- W_max fallback 90 rejected: terminal-leg lag p90 = 108 live / 132 evidence; full relay completes
  on only 14.7% of armings [verified]
- 25_89 earns trigger inclusion, 9_25 does not (2.19x the reference count, net CI straddles 0);
  the incumbent 12_25 also fails the same bar [verified]
- I4 wrong as written: EMA500 evidence-side on 1d is NEVER for ETH/SOL/NEAR/ZEC, 30 bars for BTC;
  the cited MC1_tables.md feasibility matrix has no EMA500 column [verified]
- AUTHORITY block cited CD-1(d)..CD-5(a) as ratifications; estate recorded them as [lean] until the
  operator stamped them 2026-08-12 [ratified]
PENDING:
1. Placeholder (iv) nested pair set UNRESOLVED — no candidate's separation CI excludes 0 in either
   era; operator pins by name [VETO] or it defers into the census population
2. TRAP: adopt >=5 provisionally, drop the stamp from D-CEN2a's discriminants, or re-scope —
   its discriminative power is not established on the era the census scores
3. Amend I4 (EMA500 evidence-side <=12h only) and the AUTHORITY block (cite the stamp, not the lean)
4. Operator review of the live-era pinning decision — the largest judgement call in this paste
5. CEN-0(b) PAXG unfetched by scope decision; price<->level refusal detector (i-b) has no
   implementation anywhere and remains open work
NEXT: Operator performs condition (2) review of this document, then stamps or withholds (3).
Owner: operator.
METRICS: operator actions this session = 3 (scope, network, authority) — files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-12b ===
NOW: SUPERSEDES the 2026-08-12 entry above on three points, following adversarial review of the
paste-#1 build. The review found six defects in the build itself; all are fixed in code and the
affected numbers are restated here. The census remains NOT EXECUTABLE and two of six placeholders
remain unresolved.
LAST EVENT: 2026-08-12 — four-lens adversarial review of MC-2; six build defects fixed; both eras re-run
FACTS:
- SUPERSEDES "adopt >=5 provisionally": TRAP >=5 is WITHDRAWN as a selection artifact. Selection-
  corrected permutation p = 0.287 live / 0.528 evidence against an I8 bar (BH, q=0.10, m=11) of
  0.0091 — inadmissible by 32x. It also fails an asset-cluster bootstrap, CI [-2.333, +0.059].
  The rejection of the >=2 fallback stands: it fires on 91.5% of armings, a descriptive fact [verified]
- SUPERSEDES "W_max = 108": the naive completed-only p90 conditions on survival. Kaplan-Meier gives
  45.1% of armings NEVER completing, so the p90 over armings does not exist; conditional on eventual
  completion W_max = 151 live / 160 evidence, CI [112.8, 186.0], stable across observation caps
  >= 200. W_max is near-non-binding: the counter-arming closes 98.9% of windows first [verified]
- SUPERSEDES "92.2% evidence": that was MC-1's figure, not MC-2's. MC-2 evidence = 92.1%. The two
  populations are NOT the same (MC-1 7 assets floored at ASSET_STARTS; MC-2 5 assets) and the earlier
  claim that they agreed to 4 events was a coincidental cancellation of two differences [verified]
- Build defects fixed: cold-EMA armings (I4 "NaN before warm" was never implemented, and F-PARITY
  concealed it); a lookahead in the query cards (bar containing ts, not last closed bar); a
  non-disjoint arming fate; a reimplemented kiss detector now asserted == mc1_program.kiss_v0; a
  silently redefined outcome-horizon unit; and a manifest rebuild that destroyed 5 of 6 pins [verified]
- 25_89 inclusion SURVIVES the stronger test: asset-cluster CI [0.352,1.527] live / [0.493,1.287]
  evidence. 9_25 excluded in both eras [verified]
PENDING:
1. (ii) TRAP and (iv) nested pair set remain UNRESOLVED — condition (1) of the contract is NOT met
2. The discriminant (net = MFE - MAE) is a position-in-range statistic, invariant to the terminal
   price and ~0.91 correlated with forward range; it should be re-specified before the census scores
   on it. This is the largest open methodological item
3. The selection guard is implemented for (ii) only; three other sweep-and-select stages are unguarded
4. Amend I4 (EMA500 evidence-side <=12h only) and the AUTHORITY block (cite the stamp, not the lean)
5. Operator review of the live-era pinning decision
NEXT: Operator performs condition (2) review, then stamps or withholds (3). Owner: operator.
METRICS: operator actions this session = 3 (scope, network, authority) — files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-12c ===
NOW: CENSUS-2A v0.3 RATIFIED BY EXECUTION. Contract filed as the queue item
(sha b0da051b), programs committed (3a0c35e), and stages CEN-0(b), CEN-1 and CEN-2 ran to
completion with every gating fixture passing. CEN-3..CEN-9 remain; next session starts at CEN-3.
LAST EVENT: 2026-08-12 — run 1: PAXG fetched, substrate built (516,866 events), armed-window
ledger built (848 armings), P-ARM-1 scored NOT SUPPORTED with its confound disclosed
FACTS:
- PAXG's Binance perp begins 2025-03-27, NINE MONTHS AFTER the evidence wall: zero evidence-era
  bars at every interval. It is ANNEX by the contract rule, but the larger consequence is that it
  can never enter a scored table under I1 — so it cannot be the "independent jury" D-D intended
  [verified]
- CEN-1 built the i-b price<->level refusal limb (R-8) — 174,293 events. The object did not exist
  in the estate before this run; same grammar as the ratified i-a, 3 hand-verified per limb [verified]
- ARMING-FATE (disjoint): COMPLETED 595 (median terminal H100 +0.2421), ABORTED 252 (-0.4767),
  ROTTED 1. W_max=151 governs ONE arming in 848 — correctly pinned and nearly inert [verified]
- P-ARM-1 NOT SUPPORTED: WALL-true trigger rate 0.464 vs 0.760, terminal H100 cluster CI
  [-0.2479,-0.0635] excludes zero in the WRONG direction [verified]
- CONFOUND DISCLOSED: WALL-true windows have median width 8 bars vs 30; conditioned on width>=48
  the trigger rates are 1.000 vs 0.985. The trigger-rate limb measures exposure time, not the
  stamp, and cannot be evaluated as written — a hazard framing is required [verified]
- F-GUARD passes in both directions (declines a 12-candidate null sweep at p=0.674, admits a
  planted effect at p=0.0007 and names it) and ran BEFORE any real sweep, per I11 [verified]
PENDING:
1. Operator decision on what PAXG is FOR, given it cannot serve as an evidence-era control
2. P-ARM-1's trigger-rate limb needs a hazard / competing-risk re-specification before it can be
   scored as written; the terminal-return limb stands
3. Registry levels are absent from the i-b refusal limb this run (long EMAs only); they join at CEN-7
4. 8 of 9 registrations remain unscored (CEN-3..CEN-9)
5. Duplicate v0.3 contract in exchange/reports/ alongside the queue item — operator-placed, not
   removed by the builder
NEXT: Run 2 begins at CEN-3 (outcomes). Owner: HEPHAESTUS on the operator's word.
METRICS: operator actions this session = 1 (the v0.3 contract) — files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-12d ===
NOW: CENSUS-2A run 2 complete. CEN-3 (outcomes) ran end to end under the R-1 ruler with both I6
lenses printed, the held-in-time split, the fate-stratified view carrying its mechanical-separation
caveat, and P-REL-1 scored SUPPORTED. Stopped at a stage boundary: CEN-4 is blocked on a forward
dependency, not on budget alone.
LAST EVENT: 2026-08-12 — run 2: CEN-3 done; P-REL-1 SUPPORTED; lens implementation corrected twice
before it was right
FACTS:
- F-PIN held ACROSS SESSIONS: run-1 pins {preflight, F-GUARD, F-PIN, CEN-0b, CEN-1, CEN-2} were all
  present before any run-2 work, and CEN-3 logged "merging into existing manifest (3 stages)" [verified]
- P-REL-1 SUPPORTED: 12_25-triggered windows n=155 vs other n=440, asset-cluster 90% CI
  [+0.0933, +0.2876] excludes zero. First supported registration in the census. The effect clears
  every asset's toll line by 3-7x [verified]
- MY OWN LENS IMPLEMENTATION WAS WRONG TWICE. Attempt 1 gave direction_consistent max_depth=1 for
  all 848 armings (4h 9/89 crosses strictly alternate direction); attempt 2 gave window_chained 23
  chains of mean depth 1,733 (a 24h window never breaks once 5m events are included). Fixed by
  DELEGATING to seq8_views.build_cascades -- cascades are per (asset, event_class), every rung must
  be a NEW timeframe, and chaining is greedy non-overlapping [verified]
- Several per-asset terminal medians do NOT clear the 10 bps toll line in ATR terms (BTC-down
  -0.0012, SOL-down -0.0175 vs tolls 0.058 / 0.028). NEAR-down is the worst cell at -0.2227 [verified]
- COMPLETED's interquartile range straddles zero (-0.155 to +0.704): a completed window is a
  longer-lived one, not a better one [verified]
PENDING:
1. PX-1 (PAXG disposition) — PENDING-OPERATOR. Carried from run 1: PAXG's perp begins 2025-03-27,
   nine months after the evidence wall, so it holds ZERO evidence-era bars and can never enter a
   scored table under I1. It cannot be the independent jury D-D intended. What PAXG is FOR is the
   operator's decision; the builder will not assume it
2. CEN-4 BLOCKED: its chop composite's fifth component (verdict-open) is a CEN-6 output, but the
   contract sequences CEN-4 first. Running on 4 of 5 components would silently change the >=3
   threshold P-CHOP-1 is registered against — a mid-run re-pin, which §N forbids. Options: (a) run
   CEN-6 before CEN-4 [recommended], (b) amend P-CHOP-1 by name, (c) define verdict-open
   independently
3. P-ARM-2 — FILED as a next-cycle registration, prior 55%, UNSCORED. It is the hazard / competing-
   risk successor to P-ARM-1's trigger-rate limb, which run 1 showed is confounded by exposure time
   (WALL-true windows median 8 bars vs 30; conditioned on width>=48 the trigger rates converge to
   1.000 vs 0.985). Builder's reading of the identifier; the operator should correct it if the
   intent differs, and the text is not final until the operator words it
4. CEN-7's i-b registry-levels completion (clarification 2) not started; run-1 covered long EMAs only
5. 7 of 9 registrations remain unscored
NEXT: Operator answers PENDING 2 (the CEN-4/CEN-6 ordering), then run 3 proceeds
CEN-6 -> CEN-4 -> CEN-5 -> CEN-7 -> CEN-8 -> CEN-9. Owner: operator, then HEPHAESTUS.
METRICS: operator actions this session = 1 (the run-2 sequencing paste) — files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-12e ===
NOW: SUPERSEDES the 2026-08-12d entry on four points, following a six-agent adversarial review of
run 2. The census's only SUPPORTED registration is WITHDRAWN, and the run-2 CEN-3 invocation was
found to have silently deleted P-ARM-1 from the manifest. All five required repairs are applied and
re-run. The machinery below CEN-3 was independently verified sound and does NOT need rebuilding.
LAST EVENT: 2026-08-12 — adversarial review of run 2: 2 blockers, 5 majors, 15 minors; repairs applied
FACTS:
- SUPERSEDES "P-REL-1 SUPPORTED": WITHDRAWN — UNSCOREABLE AS WRITTEN. The registration names
  "A-only windows" (armed-but-never-triggered, n=253); the code scored against the 440
  25_89-triggered windows instead, so none of the registered control arm entered. It is also not
  computable as written: A-only windows have no trigger anchor, and that cohort is 252/253 ABORTED
  at median width 4 bars vs 48 — the mechanical separation CEN-3 itself caveats. THE CENSUS NOW HAS
  ZERO SUPPORTED REGISTRATIONS [verified]
- SUPERSEDES "clears every asset's toll line by 3-7x": wrong twice. ETH's own delta is -0.2418, and
  a between-group difference of medians is not a return that pays a toll — both arms pay it [verified]
- SUPERSEDES the run-1 pin language: manifest["pins"] is EMPTY. The six names checked
  {preflight, F-GUARD, F-PIN, CEN-0b, CEN-1, CEN-2} are top-level / fixtures / stages keys. The
  check verified SECTIONS, not pins [verified]
- I12 WAS VIOLATED IN PRACTICE: load_manifest carried {pins, artifacts, fixtures, stages} and not
  registrations, so run-2's CEN-3 DELETED run-1's P-ARM-1 and its mandatory confound disclosure.
  F-PIN passed throughout because it tested a hand-written probe dict, never load_manifest itself.
  Both fixed; F-PIN now asserts 7 sections survive and would fail against the old code [verified]
- Horizons were NOT duration-fixed: max(1,round()) made H20 mean 4h on the 4h frame instead of
  1h40m (2.4x; 7.2x on 12h). Infeasible horizons now emit NaN plus a flag, never a substitute, and
  the realized bar count is persisted [verified]
- build_cascades is NOT non-overlapping: 805/848 armings hold >1 cascade membership, 388 with a
  depth spread, and the shipped depth column was dict-insertion last-write-wins. Tie rule now
  PINNED BY NAME (depth_min) with depth_min/depth_max/n_memberships all emitted [verified]
- The I11 guard had never run on real data. Called now on the asset x direction panel: m=10,
  winner NEARUSDT|down, selection-corrected p=0.0135 against a BH bar of 0.01 -> NOT ADMISSIBLE.
  So run-2's "worst cell" and "only quality ratio below 1.0" statements are UNGATED OBSERVATIONS,
  not findings [verified]
- VERIFIED SOUND, do not re-litigate: the R-1 ruler reproduces to 5e-07 on all 595 anchors x 3
  horizons; zero lookahead at both anchors; zero evidence-wall leakage; 848/848 joins with no row
  multiplication; cluster_ci is a correct asset-cluster bootstrap; MFE-MAE is genuinely retired
  [verified]
PENDING:
1. PX-1 (PAXG disposition) — PENDING-OPERATOR, unchanged from run 1
2. CEN-4 still BLOCKED on the verdict-open forward dependency (CEN-6 first is recommended)
3. P-REL-1b — the successor registration must be worded BY THE OPERATOR with explicit arm
   predicates (has_in_window_12_25 vs the named control) and an explicit anchor rule. The builder
   will not word a registration it is also scoring
4. P-ARM-2 — still filed, prior 55%, UNSCORED (hazard successor to P-ARM-1's confounded limb)
5. Filed-not-fixed: silent horizon truncation (scales badly at 5m/15m in CEN-7/CEN-9); MAE can go
   negative on 1 row; the held-in-time split balances count not time (early 970d vs late 725d, BTC
   29% vs 17%); annex pooled into printed cascade counts against F-11
NEXT: Operator words P-REL-1b and answers the CEN-4/CEN-6 ordering; then run 3.
Owner: operator, then HEPHAESTUS.
METRICS: operator actions this session = 1 (ultracode) — files re-ingested = 0
=== END STATUS ===
