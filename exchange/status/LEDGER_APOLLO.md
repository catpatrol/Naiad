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

=== STATUS_APOLLO — 2026-08-12f ===
NOW: CENSUS-2A run 3. The session opened on an infrastructure HALT (D:\Naiad had been moved to
D:\Archive\Naiad); restored on the operator's word, 123 files / 5,229,264,513 B verified identical.
Amendment A1 written to the queue item verbatim, ratified body byte-identical. PX-1(b) executed.
A1-FAN enacted. R-F11 fixed. P-REL-1b scored SUPPORTED-PROVISIONAL — the census's first
registration to survive its own mandated splits. CEN-6 is BLOCKED on an unnamed [VETO].
LAST EVENT: 2026-08-12 — run 3: rulings block executed; CEN-1/2/3 re-run; CEN-6 blocked
FACTS:
- PX-1(b) EXECUTED: PAXGUSDT dropped from D:, 23,636,729 bytes (23.6 MB) freed, klines/ parent
  removed, marked DROPPED in the manifest, re-fetchable via --stage cen0b. The deletion was
  WITHHELD while the estate was displaced — the archived tree was the only copy [verified]
- A1-FAN ENACTED: cross classes 200_500 (6,715 events) and 300_500 (5,480) added; FAN true on
  38.35% of 529,061 events (up 104,688 / down 98,228), KNOT true on 2.63%, both together 710.
  Columns only, nothing scored. FAN's six-EMA membership {9,89,200,300,450,500} is the BUILDER'S
  READING — the ruling names only KNOT's five explicitly and says "six-EMA" for FAN; correct by
  name if a different six was meant [verified]
- P-FAN-1 [60%] FILED next-cycle, UNSCORED: "armings stamped FAN=true at the arming instant show
  higher terminal ATR-return than FAN=false armings, asset-cluster 90% CI excl. 0, both directions"
  — text filed here, to be worded finally by the operator before it is scored [filed]
- P-REL-1b [50%, POST-HOC-INFORMED, LABEL PERMANENT] = SUPPORTED-PROVISIONAL. TREAT 301 vs CONTROL
  294 on explicit predicates (the first-mover label had contaminated run-2's control arm by 33%:
  146 of 440). H100 +0.1869 CI [+0.0638,+0.2887] EXCL-0; H500 +0.6399 EXCL-0; BOTH directions
  EXCL-0; late half EXCL-0, early half straddles; LOAO 4/5. Materially stronger than the
  mis-specified predecessor (which had H500 straddling and LOAO 1/5) [verified]
- CEN-6 BLOCKED: the v0.2 -> v0.3 compression KEPT the noun phrases and DELETED the parenthetical
  "(close beyond + hold h bars [VETO] vs deviation-reclaim)". The [VETO] constant h appears nowhere
  in the ratified body and was never valued. Sweeping h and promoting a winner would be selecting a
  [VETO] by search, which §N forbids. It cascades: CEN-6 -> CEN-4's verdict-open -> CEN-5b's v0 band
  [verified]
- MANDATORY DISCLOSURE for CEN-6 when it runs: LEDGER.md:311 records P-PD1/P-PD2/P-PD4 FALSIFIED,
  "the pattern detectors as gridded do not graduate". Reusing D1/D3/D4 as a LOCATION object is
  legitimate; as a promoted signal it re-runs a falsified test. LEDGER.md:315 P-PD3 CONFIRMED —
  "Z2's deficit concentrates in-range (-0.33R)" — is the part CEN-4 actually wants [verified]
- R-F11 FIXED: run-2's 151,718 lattice-A stream pooled JTO 3,812 + TAO 1,348 into a panel-labelled
  count. Panel-only is 146,558; annex 5,160 printed separately, never added. No panel arming's
  depth moved [verified]
- INFRASTRUCTURE: D:\Naiad was moved outside the repo's doing (daily_routine.py sweeps flat files
  only, skips directories, last ran 07:00). The census cannot survive its residency root vanishing
  mid-run; cause unidentified [verified]
PENDING:
1. NAME h — the acceptance hold length, [VETO]. CEN-6, CEN-4 and CEN-5b are blocked until it is
   valued by the operator. Recommend also auditing the other v0.2->v0.3 compressions for the same
   kind of dropped definition; CEN-6's loss was found only because the stage was reached
2. P-FAN-1 [60%] filed, unscored; final wording is the operator's
3. P-ARM-2 [55%] still filed, unscored (hazard successor to P-ARM-1's confounded limb)
4. FAN's six-EMA membership is a builder's reading pending confirmation
5. ROTATION PROGRAM — filed as a HORIZON WORKSTREAM, not this contract: Hyperliquid as a venue
   candidate, carrying its OWN universe and its OWN evidence wall, NEVER pooled with the Binance
   panel (the PAXG lesson: an asset whose history begins after the wall cannot enter a scored
   table, and a venue is that problem multiplied). The portability battery is the operator's
   tunable-variables question — which constants are venue-invariant and which are fitted to this
   tape. Scoping funnel opens at census close, not before
NEXT: Operator names h; then run 4 proceeds CEN-6 -> CEN-4 -> CEN-5 -> CEN-7 -> CEN-8 -> CEN-9.
Owner: operator, then HEPHAESTUS.
METRICS: operator actions this session = 2 (the run-3 rulings paste; the (a) restore authorisation)
  — files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-12g ===
NOW: CENSUS-2A run 4. h named (Amendment A2, h=2 bars [VETO]), which unblocked CEN-6. CEN-6 ran to
completion: acceptance head-to-head on {1H,4H,12H}, deviation-reclaim branch, trap-rate both ways,
hysteresis, refusal join, and the verdict_state table CEN-4 was blocked on. CEN-4 is now blocked on
a DIFFERENT unnamed [VETO].
LAST EVENT: 2026-08-12 — run 4: A2 named h; CEN-6 complete; CEN-4 blocked on the churn-density cut
FACTS:
- A2 names h = 2 bars [VETO]. The acceptance rule is now complete and CEN-6 ran. Prior queue-item
  content byte-identical; nothing re-pinned [verified]
- CEN-6 accept rate is NEAR-FLAT across the close-set: 1H 0.714, 4H 0.733, 12H 0.740, on 2,532 /
  1,425 / 949 episodes. Which clock rules changes how many excursions exist, barely what fraction
  survive two bars [verified]
- TRAP-RATE DIRECTION DEPENDS ON THE WINDOW'S UNITS. At 10 MEMBER BARS it rises 0.527 -> 0.607 ->
  0.883; at a fixed 48h it FALLS 0.803 -> 0.669 -> 0.540. 10 bars is 10h on 1H and 5 DAYS on 12H,
  so the rising version measured the window growing. On a comparable window the 12H close is the
  LEAST trap-prone. Both columns ship. This is the same duration-vs-bars defect the run-2 review
  found in the CEN-3 horizons, repeated by the builder in a new stage and caught before publication
  [verified]
- AN EPISODE IS A TRANSITION, NOT A STATE. The first CEN-6 draft opened one at every bar closing
  beyond the boundary, so a sustained breakout manufactured 50 episodes of one excursion (28,816 on
  1H). Fixed: 39,110 -> 4,906 episodes. The 0.919 hysteresis it produced was that artifact; the
  real figures are 0.598 / 0.620 / 0.635 against 0.5 memoryless [verified]
- VERDICTS CONSUME REFUSALS: on 1H, deviation-reclaims are preceded by ~3x the price<->level (i-b)
  refusal density of acceptances (0.226 vs 0.072 per episode) -- the contract's "RESPECTED is
  largely a breakout that failed to be born", now measured. The i-b limb built in run 1 is what
  makes it visible. On 12H the i-a relation INVERTS and is reported unexplained [verified]
- CEN-6 used a prior-week H/L envelope, NOT engine/s2.py's D1/D3/D4, because LEDGER.md:311 records
  P-PD1/P-PD2/P-PD4 FALSIFIED -- those detectors are admissible as a LOCATION object but not as a
  promoted signal [verified]
PENDING:
1. CEN-4 BLOCKED on a NEW unnamed [VETO]: the chop composite's churn-density-percentile component
   has no window, no event set and no reference distribution in the contract. Naming the firing cut
   by looking at capture or TRG is a sweep, which §N forbids for a [VETO]. Operator must name it
2. CEN-4 decile ruler, operator's call: realized_r is NOT size-normalised. The book is 66%
   size_r=0.5 / 34% 0.25 and the pooled bottom decile is 692/709 = 97.6% size_r=0.5 -- the
   incumbent "loser decile" is substantially a POSITION-SIZE selector. A size-free ruler
   (realized_r / size_r) moves 145 of 709 members. The pooled decile is also 37.7% BTC, so an
   asset-cluster CI against that denominator compares unequal panels
3. P-FAN-1 [60%] and P-ARM-2 [55%] still filed, unscored; FAN's six-EMA membership still a
   builder's reading
4. ROTATION PROGRAM unchanged: Hyperliquid, own universe, own evidence wall, never pooled;
   portability battery = the tunable-variables question; funnel at census close
NEXT: Operator names the churn cut and rules on the decile ruler; then CEN-4 -> CEN-5 -> CEN-7 ->
CEN-8 -> CEN-9. Owner: operator, then HEPHAESTUS.
METRICS: operator actions this session = 1 (h = 2 bars) — files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-12h ===
NOW: CENSUS-2A run 5. Amendment A3 named A3-CHURN, A3-DECILE, A3-BAND and confirmed the FAN
membership. CEN-4 ran to completion: five components as counts, P-iii-b and P-CHOP-1 both scored
NOT SUPPORTED for different and informative reasons. A3-AUDIT was launched and had not returned at
budget; it is not reported rather than reported thin.
LAST EVENT: 2026-08-12 — run 5: A3 named; CEN-4 complete; P-iii-b and P-CHOP-1 scored
FACTS:
- A3-DECILE MATTERS MORE THAN ANY SINGLE VERDICT. The incumbent pooled-raw loser decile is 97.5%
  size_r=0.5 and 38.6% BTC -- substantially a POSITION-SIZE selector. The size-free per-asset
  cohort is 78.0% / 22.1%. Every earlier result scored against the incumbent book inherits that
  bias, including MC-1's P-iii figures [verified]
- P-iii-b NOT SUPPORTED. Grind prevalence L 0.2209 vs W 0.1526, delta +0.0683, pooled cluster CI
  [+0.0362,+0.1020] EXCL-0; long +0.1013 EXCL-0; SHORT +0.0393 CI [-0.0006,+0.0963] STRADDLES BY
  0.0006. The registered text requires both directions, so the pooled effect being real does not
  carry it. The margin is reported, not rounded [verified]
- P-CHOP-1 NOT SUPPORTED, and this is TRG doing its job: capture 0.5814 (passes >=0.40) at TRG
  0.5466 (fails >=0.85). The composite catches 58% of losers by deleting 45% of the winners' tail
  profit. Reported alone, capture would have looked like a good filter [verified]
- TWO DEFECTS CAUGHT IN MY OWN DRAFT: (a) cluster_ci aggregated with the MEDIAN, which on a 0/1
  indicator is identically 0 -- P-iii-b's proportion delta printed CI [0.0,0.0] until the statistic
  was made explicit (mean for proportions, median for returns); (b) verdict-open was read as
  state=="NONE" and fired on 1 of 6,897 births -- re-read as state=="RESPECTED" (20.2% of bars),
  which is also the state LEDGER.md:315 P-PD3 CONFIRMED points at [verified]
- lens-concordance fires on 94.0% of births -- a component true of nearly everything adds almost no
  discrimination, the same null-gate shape that got the TRAP stamp dropped by R-3. Reported, not
  fixed [verified]
- A3-CHURN's 240 NaNs are the rule working: the component is undefined until an asset has >=90 days
  of its own expanding causal history, and is emitted NaN rather than imputed [verified]
PENDING:
1. A3-AUDIT table (v0.2 -> v0.3 compression diff) still in flight; report next run
2. P-NEST-2 [50%] FILED next-cycle, UNSCORED -- the FORWARD FALSE-POSITIVE question: given a nested
   LTF cross mid-bar, how often does the 4H actually confirm? Run 1 measured nesting prevalence
   backward from armings; the operator's question is the forward conditional, which is a different
   population and cannot be read off the run-1 table
3. THE D:-MOVED INCIDENT IS ROUTED TO ATHENA. On 2026-08-12 D:\\Naiad was moved to D:\\Archive\\Naiad
   by something outside the repo (daily_routine.py sweeps flat files only, skips directories, last
   ran 07:00). Restored on the operator's word, 123 files / 5,229,264,513 B verified identical. The
   census cannot survive its residency root vanishing mid-run; cause unidentified. ATHENA's lane
4. P-FAN-1 [60%] and P-ARM-2 [55%] still filed, unscored
5. ROTATION PROGRAM unchanged: Hyperliquid, own universe, own evidence wall, never pooled;
   portability battery = the tunable-variables question; funnel at census close
NEXT: CEN-5 -> CEN-7 -> CEN-8 -> CEN-9, then the A3-AUDIT table. Owner: HEPHAESTUS.
METRICS: operator actions this session = 1 (the A3 rulings paste) — files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-12i ===
NOW: SUPERSEDES the 2026-08-12h entry on one verdict. The A3-AUDIT returned after run 5's build
document was written and found that two of CEN-4's five composite components were not the
registered objects. P-CHOP-1 is WITHDRAWN. P-iii-b is unaffected and stands.
LAST EVENT: 2026-08-12 — A3-AUDIT returned: 15 needs-word items across 4 slices
FACTS:
- SUPERSEDES "P-CHOP-1 NOT SUPPORTED (capture 0.5814, TRG 0.5466)": WITHDRAWN -- COMPUTED ON A
  MIS-SPECIFIED COMPONENT SET. (a) lens-concordance is PINNED at v0.3:40 as "trailing-24h
  same-rung-string agreement between the two chaining rules, baseline 38.46%"; the build computed a
  count of 4h lattice-A events in 24h firing at <=1 -- an event-density proxy, a different
  quantity, which is why it fired on 94.0%. (b) the ribbon operand is "30m/1h 9/89 spread"
  (v0.2:40) and the build used 1h only. Both feed composite>=3 [verified]
- P-iii-b UNAFFECTED and STANDS: its predicate is no_slow AND churn, neither implicated [verified]
- THE COMPRESSION DROPPED MORE THAN h. 15 needs-word items. Highest severity: TRG's numerator was
  defined on "top-decile profit" when the ruler was MFE-MAE, and R-1 retired that ruler without
  renaming the column -- every TRG threshold (85/85/80%) rides on it; witness-correlation was
  defined only in v0.2:65-67 and exists in NO code; the sabotage fixture lost its defining
  parenthetical ("one future bar -> guard must REJECT") in the same shape as the h incident; CEN-5's
  population lost the word "panel", which would admit annex against F-11 [verified]
- LIVE CONTRADICTIONS: P-NEST-1 is scored by v0.3:124 while R-4 carries the nested object as
  UNCONFIRMED columns-only; P-ARM-1's "trigger-within-151" phrase differs from CEN-2's computed
  min(151, counter-arming), which closes 98.9% of windows; and A1's R-PAXG contradicts the body's
  "PAXG fetch NOW" + F-12, though F-12 was in fact discharged before the deletion [verified]
- STRUCTURAL ROOT: neither draft ever closed a register over its own [VETO]s. Three of v0.2's five
  [VETO] markers lived in module bodies, not section 0, so compressing section 0 could never have
  preserved h. Unrepaired; it will keep producing this failure [verified]
PENDING:
1. NW-5 TRG numerator under R-1 -- blocks P-CHOP-1 re-score, P-RAT-2, P-VBT-1, F-9
2. NW-2 witness-correlation definition -- blocks I8/F-16/CEN-8
3. NW-4 sabotage-fixture construction -- blocks F-10/CEN-8
4. NW-1 CEN-5 population: restore "panel" or rule annex in by name
5. P-NEST-1 scored-vs-columns-only contradiction must be resolved before CEN-8
6. RECOMMEND: close a [VETO] register over the whole contract -- one enumerated list, module
   bodies included -- so the next compression cannot silently drop a constant
NEXT: Operator rules on NW-5 first (it gates three registrations), then CEN-5. Owner: operator.
METRICS: operator actions this session = 1 (the A3 rulings paste) — files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-12j ===
NOW: CENSUS-2A run 6. CEN-5 ran to completion on 6,834 of 7,094 resolved campaigns. P-RAT-2 scored
NOT SUPPORTED (0 of 36 corners); P-VBT-1 NOT SCORED because H-VBT is undefined in both contract
drafts. CEN-7, CEN-8, CEN-9 remain.
LAST EVENT: 2026-08-12 — run 6: CEN-5 complete; two exit registrations resolved
FACTS:
- THE R UNIT RECONSTRUCTS: realized_r = size_r x gross_R + costs, verified on all 7,094 rows
  (median |err| 0.058 vs size_r x gross_R, residual systematically negative = costs). THEREFORE
  A3-DECILE's realized_r/size_r IS gross R, correlation 0.993 -- the operator's size-free ruling is
  correct and CEN-4 used it correctly. One ruler, not two [verified]
- 432 CAMPAIGNS WERE NEARLY LOST SILENTLY. tranche_id is unique only WITHIN a cell (c104t145 exists
  in both BTCUSDT_intraday and ETHUSDT_swing; 378 ids collide). A first draft keyed a dict on
  tranche_id alone and dropped 6.1% of the book. Now carried in a list that cannot collide. This is
  the THIRD appearance of the non-unique-key defect in this census -- a join-key uniqueness
  assertion belongs in the fixture set [verified]
- 260 campaigns excluded AND COUNTED: every one is sub-bar (hold_s < 300s), exiting inside the same
  5m candle it entered, so there is no forward path to ratchet along. Never imputed [verified]
- RIDE-ONLY control: the book is 12.3% winners (814 of 6,643) carrying mean +9.4R against a median
  loser of -1.04R; ALL median -1.0324, mean +0.3072. Any exit study on this book is a study of tail
  preservation [verified]
- P-RAT-2 NOT SUPPORTED: 0 of 36 corners meet both bars. FDR family m=36 DECLARED BEFORE SCORING,
  BH bar 0.00278; the I11 guard is ADMISSIBLE (p_sel 0.0005). TWO CAVEATS THAT MUST NOT BE READ
  PAST: (a) median delta R is +0.0000 for the best corners BY CONSTRUCTION, because most campaigns
  never reclaim the long EMA -- the mean deltas are +0.45R and +0.43R at the 4h/long/wide corners,
  and the registration names neither median nor mean; (b) TRG came back >1 for 30+ corners, because
  TRG is defined as a retention SHARE for a FILTER and a ratchet is an alternative EXIT that can
  exceed the ride. So P-RAT-2's TRG limb IS NOT DECIDABLE AS WRITTEN and the verdict rests on the
  delta limb alone [verified]
- NW-5 HAS NOW LANDED ON A LIVE VERDICT. TRG's numerator was defined (v0.2:64-65) while the ruler
  was MFE-MAE; R-1 retired that ruler and no text renamed the column. It gates P-RAT-2, P-VBT-1,
  P-CHOP-1's re-score and F-9 [verified]
- P-VBT-1 NOT SCORED: H-VBT is a bare NAME in both v0.2:131 and v0.3:103. The estate defines it
  only as "VWAP Band Target -- exits at confluence-scored VWAP levels", and those bands are CEN-7's
  registry output, which has not run. Choosing a band set by outcome is the sweep §N forbids, so
  the arm is not built and the registration is not scored rather than scored on an invented rule
  [verified]
PENDING:
1. NW-5 TRG numerator -- now blocking THREE registrations and one fixture. Highest-value word
2. P-RAT-2's "net terminal R": median or mean? The registration names neither and they disagree in
   sign at the 4h/long/wide corners
3. H-VBT's definition (band set + confluence cut), or drop P-VBT-1 to a printed column
4. NW-2 witness-correlation and NW-4 sabotage fixture both block CEN-8
5. P-NEST-1 scored-vs-columns-only contradiction must be resolved before CEN-8
6. RECOMMEND (repeat): close a [VETO] register over the whole contract, and add a join-key
   uniqueness assertion to the fixture set -- the same key defect has now appeared three times
NEXT: Operator rules on NW-5 and the median/mean question; then CEN-7 -> CEN-8 -> CEN-9.
Owner: operator, then HEPHAESTUS.
METRICS: operator actions this session = 1 (the run-6 sequencing paste) — files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-12k ===
NOW: CENSUS-2A run 7. Amendment A4 appended and the [VETO] REGISTER IS CLOSED -- 39 rows, and the
HALT check finds zero constants in code absent from it. F-KEY and the restored F-10 sabotage both
implemented and passing. A4-WITCORR restored and exercised, and it qualifies the census's one
supported result. CEN-7/8/9 remain.
LAST EVENT: 2026-08-12 — run 7: A4 repair block complete; register closed; three fixtures live
FACTS:
- THE REGISTER IS CLOSED. 39 rows covering every pinned constant and its source (v0.3 §0 / A1 / A2 /
  A3 / A4). The A4-REGISTER HALT check scans every module-level constant in census2a_program.py and
  mc2_program.py: 23 scored constants covered, 39 machinery exemptions named, ZERO absent. The
  structural gap that let h vanish is closed [verified]
- A4-TRG REPAIRS THE METRIC: TRG is for FILTERS only (summed positive terminal ATR-R of the
  unfiltered top decile). Alternative-exit arms print TAIL-EXIT-RATIO, unbounded, no pass-bar this
  cycle. P-RAT-2's NOT SUPPORTED verdict STANDS on its delta limb; its TRG limb is now VOID BY
  DEFINITION and the manifest says so. This closes the run-6 loop where TRG returned >1 [verified]
- F-10 RESTORED VERBATIM AND PASSING: clean as-of 2022-02-03 08:00 -> 36995.50; sabotage rejected
  with "bar closing 2022-02-03 12:00 is in the future of the as-of instant". v0.3 had kept
  "sabotage fixture mandatory" and deleted the parenthetical that said what the test IS -- a
  fixture whose test is unstated cannot fail [verified]
- F-KEY LIVE: assert_key() declares a join's key and asserts uniqueness BEFORE the join, halting on
  violation. Exercised: cen3_ledger_lensed (asset,arming_ts) 848 rows dup=0; cen3_trigger_outcomes
  (asset,dir,arming_ts) 595 rows dup=0. It exists because the non-unique-key defect appeared THREE
  times and every one was caught by reading a count, never by a fixture [verified]
- A4-WITCORR RESTORED AND IT QUALIFIES P-REL-1b. Pairwise sign-agreement across assets 0.60 (6 of
  10 pairs; ETH dissents at -0.0923) against a PANEL RETURN CORRELATION OF 0.6458. The headline
  "LOAO 4 of 5" overstates the replication: five assets correlated at 0.65 are closer to one
  witness than to five. P-REL-1b remains SUPPORTED-PROVISIONAL and the provisional half of that
  label is now load-bearing. This is precisely the print v0.2's I8 required and the v0.3
  compression deleted [verified]
- A4-NEST resolves the contradiction on the record: P-NEST-1 SCORES at CEN-8 as registered on the
  pre-named set; R-4 governs the flags' use as composite stamps only [ratified]
PENDING:
1. CEN-7 -> CEN-8 -> CEN-9 remain; run 8 starts at CEN-7
2. The register's closure is over MODULE-LEVEL constants only. A bare literal inside a function
   body would not be caught; an AST scan of scoring paths is the natural next hardening and is NOT
   implemented
3. The ribbon operand (30m and 1h vs 1h only) is still unvalued and sits in the register's
   known-open list; P-CHOP-1 stays withdrawn until it is named
4. A4-WITCORR is exercised on ONE discriminant; CEN-8 must print it beside every promoted verdict
5. Filed next-cycle and unscored: P-FAN-1 [60%], P-ARM-2 [55%], P-NEST-2 [50%], P-RAT-3 [40%],
   P-VBT-2 [45%]
6. ROTATION PROGRAM unchanged: Hyperliquid, own universe, own evidence wall, never pooled;
   portability battery = the tunable-variables question; funnel at census close
NEXT: CEN-7 (registry as-of + i-b registry-levels completion + two-limb reconciliation), then
CEN-8, then CEN-9. Owner: HEPHAESTUS.
METRICS: operator actions this session = 1 (the A4 rulings paste) — files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-12l ===
NOW: CENSUS-2A IS COMPLETE. CEN-7, CEN-8 and CEN-9 all ran to completion this session. Every module
of the contract (CEN-0b, 1, 2, 3, 4, 5, 6, 7, 8, 9) is run and hash-recorded. THE CENSUS CONTRACT
IS SPENT.
LAST EVENT: 2026-08-12 — run 8: the final three stages; the contract closes
FACTS:
- ALL TEN MODULES RUN. Fixture set at close, all passing: F-GUARD, F-PIN, F-KEY, F-6, F-6-VEC,
  F-PARITY-2, F-10 (restored), F-15, F-16 (restored) [verified]
- CEN-7 COMPLETED THE D-B TWO-LIMB OBJECT for the first time: i-a 175,696 (EMA<->EMA), i-b 168,468
  (long EMAs) + 14,759 (registry RVWAP 7/30/90/365d and sigma bands) = 183,227 i-b total. The
  price<->level limb the estate never had is now complete against both families [verified]
- CO-LOCATION IS RARE: at the pinned 0.15x daily-ATR, a mean of 0.137 of 12 registry levels sit
  within the band, and only 0.7% of instants carry >=2. Registry levels do not cluster at armings
  on this tape -- a finding about the confluence premise itself [verified]
- P-NEST-1 NOT SUPPORTED: TREAT 149 vs CONTROL 699, terminal H100 cluster CI [-0.0513,+0.2292]
  straddles zero. A4-WITCORR beside it: pairwise sign-agreement 0.40 (2 of 5 pairs) against panel
  return correlation 0.6458 [verified]
- P-i' AND P-iv' NOT SCORED: leap-arrival vs stair-arrival is defined in NEITHER draft. MC-1's leap
  family is a CASCADE object; P-i' is a WINDOW recut. Register: known-open. Inventing the split to
  score it is the sweep §N forbids [verified]
- BOTH TIME SPLITS PRINTED (R-SPLIT): count-balanced gives 970.7/724.8 days; duration-balanced gives
  847.8/847.8. The duration split fixes the TIME imbalance and NOT the composition drift -- BTC is
  ~29% of the early half and ~18% of the late half under BOTH. Era and panel composition remain
  entangled [verified]
- FDR FAMILIES DECLARED: entry-lens m=3 (BH 0.03333), exit-lens m=1 (0.10), CEN-5 corners m=36
  (0.00278). WITHDRAWN and NOT-SCORED registrations do NOT shrink m -- they carry no p-value, which
  is not the same as passing [verified]
- CEN-9, THE INSTRUMENT'S OWN CONTROL: EMA-anchored armings median terminal H100 +0.0748 against
  stratified random instants +0.0227 -- an edge of +0.052 ATR. THE PINNED TOLL IS 0.026-0.059 ATR
  PER ASSET, so the entire EMA edge is the size of the round-trip cost. And the prior-extreme sweep
  from below EDGES IT OUT at +0.0845. Descriptive medians, no intervals, registers nothing -- by
  design [verified]
- F-15 PASS: the N=200 quarter-stratified draw reproduces identically under its seed [verified]
- THE CENSUS YIELD: one SUPPORTED-PROVISIONAL result (P-REL-1b, itself qualified by a
  witness-correlation print that had to be restored from a superseded draft) out of nine scored
  hypotheses. Three died to confounds the frame exposed; two to definitions the contract never
  carried. That is the honest yield and the frame is what produced it [verified]
PENDING (all next-cycle; none blocks this contract, which is spent):
1. Filed and unscored: P-FAN-1 [60%], P-ARM-2 [55%], P-NEST-2 [50%], P-RAT-3 [40%], P-VBT-2 [45%],
   and P-CHOP-2 on the newly-valued ribbon operand
2. Needs-word before their registrations can ever be scored: leap/stair arrival (P-i'), ATR buckets
   and "survives" (P-iv'), H-VBT's band rule (P-VBT-2)
3. The register's closure is MODULE-LEVEL only; an AST scan of scoring paths for bare literals is
   the natural next hardening and is NOT implemented
4. The D:-moved incident remains routed to ATHENA; cause unidentified
5. ROTATION PROGRAM unchanged: Hyperliquid, own universe, own evidence wall, never pooled;
   portability battery = the tunable-variables question; the funnel opens NOW, at census close
NEXT: THE PATH's next step is the operator's -- Tier-C / EngineV2, or the rotation funnel. The
census has delivered what it can. Owner: operator.
METRICS: operator actions this session = 1 (the run-8 sequencing paste) — files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-12m ===
NOW: CENSUS-2A VIZ-1 IS DELIVERED. Nine payloads extracted, nine views rendered, the handoff
folder is packed, and the probe ledger is open. CLASS: DISPLAY-ONLY / Tier-E — this build
registers nothing, scores nothing and claims nothing; selection surface m = 0.
LAST EVENT: 2026-08-12 — VIZ-1: the census's instants, drawn
FACTS:
- TIER-E CLASS STATED ON EVERY ARTIFACT. Nine payloads and ten HTML pages each carry the close-out
  §5 footer verbatim with their own payload sha; the probe ledger stamps entry #1
  "EXPLORATION — ungated; promotion requires registration" [verified]
- THE BRIEF AND THE CLOSE-OUT ARE FILED BYTE-EXACT and were verified identical rather than
  re-written: brief 6,067 B sha 9baa5a4e…, close-out 19,464 B sha 5de5fd74… [verified]
- PROBE LEDGER OPEN: exchange/reports/CENSUS2A_PROBE_LEDGER.md, append-only, carrying the §5 law
  and the m-accounting rule. Entry #1 = VIZ-1 extraction, m = 0. RUNNING SELECTION SURFACE: 0 —
  nothing this build did can ever be charged to a future FDR family [verified]
- F-V1 PASS ×9: every payload round-trips json.load, every meta.sha256 re-verifies against a fresh
  hash of its own data block, every payload under the 700,000 B cap (largest 662,099 = 94.6%)
  [verified]
- F-KEY PASS on all three joins: cen3_ledger_lensed (asset, arming_ts) dup=0 · cen5_campaigns
  (tranche_id) dup=0 · cen7_registry_series (asset, ts) dup=0. The fixture exists because the
  non-unique-key defect appeared three times during the census [verified]
- HANDOFF READY: D:/Naiad/research_outputs/census2a/DESIGN_HANDOFF/ — 11 files, 2,454,089 B (nine
  payloads + brief + close-out). Renders at .../viz/ — ten pages, 1,587,395 B, self-contained,
  zero external fetches [verified]
- THE TOLL IS DRAWN ON EVERY OUTCOME AXIS, read from each payload's own meta, never a literal in
  the drawing path. V3 draws it as a ring, so "smaller than its own cost" is geometry, not a
  caption [verified]
- REPORTED NOT FIXED: mae_r and n_reclaims DO NOT EXIST in cen5_campaigns — emitted null, so V6's
  reclaim ticks and MFE/|MAE| glyph cannot be drawn; displacement_atr and the six-EMA ranks are
  RECOMPUTED from 4h frames, not stored anywhere; v6 is truncated to 4,000 of 7,094 by the byte
  cap (disclosed in its own downsample_rule); and there is NO interactivity in the first pass
- WHY RAW SVG: neither matplotlib nor plotly is installed. Installing a package to draw a picture
  is not a thing to do unasked, and self-contained-no-external-fetch is what the brief actually
  requires. First-pass renders are legible and unornamented; Design's versions sit BESIDE them and
  never replace them, per the paste
- BOX-COST: exchange/** was 2,078,416 B = 32.53%; this build adds ~18 KB ≈ +0.28% → ~32.8%. All
  6,470,042 B of payloads, renders and handoff live on D: — not one byte committed [verified]
PENDING (unchanged; the census contract remains SPENT):
1. Filed and unscored: P-FAN-1 [60%], P-ARM-2 [55%], P-NEST-2 [50%], P-RAT-3 [40%], P-VBT-2 [45%],
   P-CHOP-2 on the newly-valued ribbon operand
2. Design's session, if it happens, consumes DESIGN_HANDOFF/ and returns DESIGN_NOTES.md; the
   first-pass renders stand regardless
3. Anything a viewer finds interesting in these nine views is a PROBE, logged in the probe ledger
   with its m — never a finding, and never citable without the Tier-P ceremony
4. The D:-moved incident remains routed to ATHENA; cause unidentified
NEXT: THE PATH's next step is still the operator's — Tier-C / EngineV2, or the rotation funnel.
Owner: operator.
METRICS: operator actions this session = 1 (the VIZ-1 paste) — files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-14a ===
NOW: CENSUS-2B / V-ULT-1 IS BUILT. Six EMA ribbons x seven timeframes x five assets are on D: as
a substrate, with the warm-up law asserted rather than assumed, and the operator's question has
had its first descriptive look. CLASS: substrate + DISPLAY-ONLY / Tier-E. Selection surface
m = 0 — this build registers nothing, scores nothing and claims nothing. The census-2A record is
untouched.
LAST EVENT: 2026-08-14 — census-2B V-ULT-1: the U-VHT data module (contract ratified 2026-08-12)
FACTS:
- THE FEASIBILITY MATRIX RAN FIRST, 630 cells, before one EMA was computed. 45 cells are NEVER
  and were SKIPPED not computed; 14 are OPS-ONLY. The contract's expectation is confirmed and
  sharpened: UH is NEVER on 4h and 12h, VH is NEVER on 12h and OPS-ONLY on 4h. 1m is FULL for
  all 18 lengths on all 5 assets [verified]
- F-B0, A FIXTURE THE CONTRACT DID NOT ASK FOR, settles a real ambiguity: the contract pins
  warm_bars = ceil(3.46*N) and calls it "the SEQ8 rule", but the SEQ8 rule in this estate is
  ceil(log(1e-3)/log(1-alpha)) and they are different expressions. ceil(3.46*N) is >= the exact
  rule for all 18 lengths (delta 0..+30, never negative), so the contract constant is the
  CONSERVATIVE one and is used as written, by name. A FAIL would have halted before stage 1
  [verified]
- WARM-UP ASSERTED, NOT INTENDED. F-B2: 0 cold-head values across 540 series, and every NEVER
  column proved all-NaN. Because the cold head is NaN at the source, crossover/crossunder return
  False there BY CONSTRUCTION — the defect that produced ~50 phantom 4h armings on 2026-08-12
  cannot recur here. F-B3: every family's middle EMA bit-matches a hand-run recursion [verified]
- FIXTURES ALL PASS: F-B0, F-B1 (3/3 hand-recomputed), F-B2, F-B3, F-B4a/b/c/d, F-B5a (re-run
  hash-IDENTICAL), F-B5b (3 hand-verified events per pair class), F-B5c (the copied kiss grammar
  is element-equal to census-2A's original), F-B6 (324 equivalences, 0 span mismatches), F-KEY
  dup=0 on all 35 cross cells and all three census-2A joins [verified]
- A 53-AGENT ADVERSARIAL REVIEW OF THIS PROGRAM RAISED FINDINGS AND A SECOND AGENT PER FINDING
  TRIED TO REFUTE EACH; NINE SURVIVED AND ALL NINE ARE FIXED. The one that mattered: the band
  grammar {enter, exit, reject} is defined entirely against `inside`, so a bar clearing the
  whole band in one move matched nothing and was dropped — 510,584 events, 18.4% of all band
  transitions, concentrated in the FAST cells. `traverse` is now its own class. NO FIXTURE IN
  THIS BUILD COULD HAVE CAUGHT IT: every one asked "is what we emitted correct", none asked "is
  a class missing" [verified]
- THE ENQUIRY CARD RETURNED A CLEAN NULL, AND IT IS NOT A FINDING. Conditioning FAST-ribbon
  crosses on VH+UH orientation: across all 18 strata (3 pairs x 3 orientations x 2 tfs) every
  median terminal-H100 sits INSIDE the measured toll band and %>0 stays within 47.9-50.1%. One
  measurement, one ruler, one horizon, m = 0. Promotion needs the Tier-P ceremony [verified]
- TWO STRUCTURAL OBSERVATIONS, REPORTED NOT FIXED, BOTH ABOUT THE PINNED CONSTANTS RATHER THAN
  THE TAPE: UH returns `flat` for 95.1% of warm bars against VH's 23.4% (k=20 is not scale-
  matched to lines spanning 1.18x in length); and 66-68% of VH knot episodes "expand" on the
  very next bar against 2.5-5.2% for UH, because a knot run ends precisely when width is rising.
  The constants are VETO by name and were NOT changed; the shares are printed as the evidence
  [verified]
- THE TOLL IN ATR UNITS IS TIMEFRAME-DEPENDENT and census-2A's 0.026-0.059 is a 4h figure. On 5m
  the same 10 bps round trip is 0.29-0.35 ATR. A first draft quoted the 4h number beside 5m
  tables and was corrected to measure the toll on each population's own bars [verified]
- 1m IS THE NAMED SKIP, AND THE BUDGET WAS RAM. This machine has 7.6 GB with ~0.8 GB free; a 1m
  cell is 3.65M bars, stage 2 ran at 57% CPU efficiency (paging) without finishing its first
  asset, and stage 3 needs ~1.2 GB peak per asset. Stages 3-5 never read 1m, so no table in the
  build document is affected; the 1m rows of the feasibility matrix are complete [verified]
- SEVEN DEFECTS IN THIS BUILD'S OWN MACHINERY, FOUND AND FIXED: a scoped run overwrote the
  feasibility matrix (now I12-merges); F-B1's sample was hardcoded and crashed on a scoped
  matrix; a killed run left a footer-less parquet the manifest recorded as valid (now atomic
  writes + a readability HALT); pin-merge resurrected that deleted artifact with its stale sha
  (now pruned); the manifest recorded rows: 0 for every artifact (now 15,807,077); it stamped the
  Tier-E tables as SUBSTRATE (now 9 carry the Tier-E class); and `--stage 34`, a missing
  comma, ran nothing and exited 0 [verified]
- BOX-COST: exchange/** was 2,137,089 B = 33.44%; this build adds 115,730 B to
  35.26%, above the contract's <1% target and well below the 40% REFUSE
  line. The overage is the two blocks the contract required verbatim — the 630-cell matrix and
  the full first-look transcript. All 1.71 GB of substrate is on D:, not one byte
  committed [verified]
PENDING (none blocks this contract):
1. THE V-ULT SLATE IS NOT WORDED. Per the paste, no registrations this build; the slate is
   written after the operator reads the first look. Owner: operator
2. `traverse` IS AN ADDITION TO A TAXONOMY THE CONTRACT CALLED "pared by design". Emitted as its
   own class and flagged for veto by name. Owner: operator
3. THE MISSING FIXTURE CLASS: nothing here asserts the event taxonomy is COMPLETE over the
   transitions it claims to cover. A partition check on `pos` would have caught the traverse gap
   on day one. Named, not retrofitted
4. 1m stages 2-4 remain unrun. `--stage 2,3,4 --tfs 1m` on a machine with headroom
5. Whether `k = 20` should be scale-matched per family is an OPERATOR question — changing a VETO
   constant is a ruling, not an edit
6. The annex (JTO/TAO) was not run; the contract made it optional and the budget went to 1m
7. Census-2A's cen4_book tranche_id defect (360 dups; the whole key is cell|tranche_id) is
   recorded but NOT repaired in census-2A's artifacts
NEXT: the operator reads §6 and words the V-ULT slate, rules on `traverse`, or rules on the k=20
scale-match. Owner: operator.
METRICS: operator actions this session = 1 (the CENSUS-2B V-ULT-1 paste) — files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-14b ===
NOW: CENSUS-2B PART A AND W-TB1 ARE BUILT, IN THAT ORDER, AS THE CONTRACT REQUIRED. The completion
certificate A-0 could not obtain from the box now exists and is printed first; the sequential
substrate A-1..A-4 is on D:; and the 12.3% tail has its ±72h biography against a 1:1 matched control.
CLASS: Tier-E substrate + Tier-E descriptive. NO REGISTRATIONS. Selection surface m = 743,516, all of
it W-B's motif surface — and the I11 guard returns a clean null in all three SEQ frames. Tail Bio nomenclature is
NOT ratified; it remains [proposed] as W-TB1 · TAIL BIOGRAPHY, DIONYSUS 2026-08-13, routed to APOLLO.
LAST EVENT: 2026-08-14 — census-2B Part A (A-0..A-4) + W-TB1 tail biography, one build document
FACTS:
- THE CENSUS-2B COMPLETION CERTIFICATE IS PRINTED. A-0 probed 157 cells against the manifest and
  recomputed every sha from the bytes on D:. 100 PRESENT, 0 STALE, 0 PINNED-MISSING, 1.71 GB.
  V-ULT-1 is COMPLETE on the panel across {5m,15m,30m,1h,4h,12h}. The 57 ABSENT cells reconcile
  exactly: 15 panel-1m + 42 annex. 1m DEFERRED, named, per the contract's own instruction [verified]
- A-2 IS THE HEADLINE AND ITS HEADLINE IS NEGATIVE. 103,153 armed windows on five lenses. The
  arming-anchored fate split (+2.48 ATR TRIGGERED vs -1.27 ABORTED at H100 on 5m) is CIRCULAR: fate
  is decided inside the window. The curtain-clean anchor is the trigger, and the median forward R-1
  from the first 12_26 trigger is NEGATIVE at both horizons on 5m/15m/30m, before a 0.28 ATR toll.
  Structural, not empirical: e12 crosses e26 long before e89, so the "trigger" is a re-entry after a
  pullback, arriving 33-43 bars after the displacement already happened [verified]
- THE MOTIF PROBE RETURNED A CLEAN NULL AND COST 743,516. Every k-gram k<=4 over the full BRIDGE
  grammar in all three ratified SEQ frames, 24h before birth, winners vs matched control. The largest
  winners-vs-control gap any motif achieves (0.08477, absolute frame) sits BELOW its own permutation
  null p95 (0.08722), and the same holds in gov_relative and tier. `admissible` is False everywhere
  but is NOT the informative column: at 2,000 permutations the BH bar q/m is 1,239x below the
  p-value floor of 1/2001, so it could not have been True whatever the data said. Nothing promoted;
  the full surface is charged to the probe ledger [verified]
- AN 8-DIMENSION ADVERSARIAL REVIEW RAISED 44 FINDINGS AND A SECOND AGENT PER FINDING TRIED TO REFUTE
  EACH; 6 SURVIVED AND ALL 6 ARE FIXED. The one that mattered: `br_state` stacked the six SR medians
  fast-to-slow and then read `np.diff > 0` as BULL -- which is fast BELOW slow. EVERY bull/bear
  column in W-A and every BR@t0 label in W-E was BACKWARDS; 273,883 rows carried br_orient=BULL with
  an SR-order disorder of 1.000, which on the same function's own ruler is perfectly BEAR-ordered.
  This lane found and fixed five more the review did not reach in time, including the one two
  reviewers independently flagged CRITICAL after it was already gone. ELEVEN defects, all fixed,
  all with measured before/after in the build document [verified]
- THE COHORT IS EXACTLY THE 12.3% TAIL. 814 winners by gross_R > 0 from the resolved panel book,
  mean +9.4458 against a median loser of -1.0332 — byte-for-byte the F1 figures. 814 controls matched
  1:1 and EXACTLY on (asset, direction, entry-quarter, size_r); 0 unmatched, 0 reused, 0 overlap. The
  exact match makes F-W1b's "marginals within 10%" a VACUOUS pass and it is reported as such [verified]
- THE EXIT SIDE WAS NEVER A DATA GAP. Every downstream table since census-2A says campaign exit
  timestamps do not exist. They exist: stage_cen5 computes t1 = t0 + hold_s*1000 and does not persist
  it. W-TB1 reads ts_close/hold_s from the WF1 source JSONs and gets t_exit for all 1,628 campaigns.
  No simulation, no inference. The named gap is closed by reading [verified]
- W-D'S 7x HEADLINE IS AN EXPOSURE ARTIFACT AND SAYING SO IS THE RESULT. "27.1% of winners vs 3.8%
  of controls show a long-EMA loss->reclaim" collapses to 0.374 vs 0.305 events per 100 OPEN HOURS,
  and reverses on e2618/e4618. Median hold is 112.4h for winners against 2.2h for controls, a 50x
  gap. In the >=24h duration-matched band the CONTROLS are higher. Whatever P-REC-1 says, it cannot
  be "winners reclaim more" [verified]
- THE PINNED CONSTANTS DO NOT SCALE, NOW MEASURED IN TWO MORE PLACES. The kiss grammar is INERT on
  five of eleven pared pairs: they touch 61k-820k times each, and the MAXIMUM separation reachable in
  k=10 bars across the whole history is BELOW delta=0.75 (0.42-0.61 ATR). And RIBBON_C = 0.5 ATR is
  vacuous on the BR, whose width is 15-20 ATR at every stage, so the in-knot class is empty by
  construction. Both constants are VETO and NEITHER was changed; both are measured, printed, and
  referred to the operator. With V-ULT-1's k=20/UH finding this is now one pattern, not three notes
  [verified]
- FIXTURES ALL PASS: F-A0R (the restated R-1 ruler is element-for-element identical to census-2A's
  outcome_block, both directions, both horizons, terminal/mfe/mae), F-A1a/b (3 hand-verified, re-run
  hash-IDENTICAL), F-A2a/b/c (0 overlapping windows; arming counts reconcile to the A-0 cross
  artifact with the 4 suppressed re-arms read from the run's OWN stats, not derived; one window
  hand-unpacked per lens), F-A3a/b, F-A4a/b, F-W1a/b, F-KEY dup=0 on every Part-A table and all 20
  W-TB1 state cells [verified]
- HORIZONS ARE DURATION-FIXED AND ONE IS INFEASIBLE. H20 = 1h40m, H100 = 8h20m, converted per lens
  and printed before every outcome table. H20 on 4h is shorter than one bar: it emits NaN and is
  NEVER substituted with one bar, which is why the 4h H20 columns are blank rather than zero [verified]
- BOX-COST: exchange/** was 2,256,225 B = 35.31%; this build adds 112,319 B (document 97,369 +
  probe ledger 6,421 + this entry 8,529) to 2,368,544 B = 37.06%, ABOVE the
  contract's <1% target and well below the 40% REFUSE line. The overage is one contract-required
  block — A-0's verbatim 157-row completion table, 14,859 B, which the contract orders printed FIRST
  and verbatim, and which IS the certificate. W-A prints 2 of 4 lenses, W-C 1 of 4, W-E the identity
  card not 20 event pages, to compensate. The publish also carries 15,571 B of DIONYSUS's own
  uncommitted exchange/ files -- the bus is path-scoped, not lane-scoped -- landing the box at
  37.31%. All 2.22 GB of substrate is on D:, not one byte committed [verified]
PENDING (none blocks this contract):
1. FOUR CONSTANTS NOW MEASURED AS SCALE-MISMATCHED: kiss (eps/delta/k) on slow line pairs, RIBBON_C
   on the BR, k=20 on UH, and the knot/expansion tautology at VH scale. Each is VETO by name.
   Changing any is a ruling, not an edit. Owner: operator
2. NOMENCLATURE_MAP is cited by the W-TB1 contract and does not exist anywhere in the estate. Part A
   pins its own spring/upthrust definitions [VETO N=96, reclaim<=3] so nothing is blocked. File the
   map or drop the citation. Owner: operator
3. "SR-order entropy" had no pinned definition; implemented as the normalised inversion count of the
   six SR medians and stored as sr_order_disorder. Ratify or replace. Owner: operator
4. m = 743,516 counts (frame, motif) PAIRS; the same sequence appears once per SEQ frame. The larger,
   conservative reading was charged. Is the surface 743,516 or 288,857? Owner: operator
5. "both lenses per I6" was read as the two ANCHORS (arming, trigger), both always printed, because
   I6's window lenses are a cascade construct A-2 does not build. Confirm the reading. Owner: operator
6. price_band events are on D: but NOT on the W-TB1 tape and NOT in the motif alphabet — the
   contract's tape enumeration does not name them. In or out. Owner: operator
7. THE COMPLETENESS FIXTURE IS STILL MISSING (V-ULT-1 pending 3, carried). Part A adds disjointness
   and reconciliation fixtures but still nothing asserts a taxonomy is exhaustive over what it covers
8. 1m stages 2-4 remain unrun; the annex (JTO/TAO) was never built. Both named in A-0
NEXT: the operator reads §3.3 (the trigger is negative), §10 (the motif null), §12 (the exposure
artifact), and rules on the four scale-mismatched constants as one question rather than four.
Owner: operator.
METRICS: operator actions this session = 1 (the CENSUS-2B PART A + W-TB1 paste) — files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-15 ===
NOW: THE ORACLE IS BUILT. One grid, a complete partition of the filed census-2B event substrate:
5 lenses x 12 classes x {ALL, 2 directions, 3 orientation states}, 856,877 anchors, m = 0,
toll-honest, printed whole in the build document. The three instrument-scale vetoes are executed:
knot-scale VERIFIED (the substrate was already per-SR), state-scale APPLIED (and it was the real
defect — UH read 92.8% flat at 5m under the global k=20), kiss-scale RUN AND
INERT, with the reason measured rather than guessed.
CLASS: Tier-E + instrument re-pins. NO REGISTRATIONS. m = 0 — the partition is complete and
unranked, so there is no family to correct over. Any selection FROM the grid is a new probe.
LAST EVENT: 2026-08-15 — CENSUS-2B ORACLE rev C, one build document
FACTS:
 1. MAC-ERA RULES v2 ACKNOWLEDGED IN-LANE: identity gate passed (pwd == $HOME/Naiad, no cloud-sync
    marker in the path), data born and read local, nothing touched the LaCie this pass. ATHENA's
    crossing is SALUTED — 425 files / 7.45 GB restored at 0 mismatches, suite 287 passed / 0 failed
    / 1 skipped, census work unblocked. This is the first census build of the Mac era.
 2. PINE v12.0.1 FILED byte-exact: pine/SS_v12_0_1.pine, sha256 af166d92035a3981da0926b589dec6135d5c57a4a4bc49ed833f6b217c068ad9
 3. THE ORACLE GRID IS THE PER-LENS MARK-DEFAULT AUTHORITY for the indicator's next revision. It is
    descriptive, not prescriptive: it says what each class has historically done at each lens under
    one ruler, net of that lens's toll. SS v12.0.2 marks should be argued against it by name and
    lens, not against intuition.
 4. R-3 WAS THE REAL DEFECT. The global k=20 made the state column report the LOOKBACK, not the
    ribbon: UH 92.8% flat at 5m -> 6.1% at k=577. FAST and M
    are unchanged by construction (their k floors at 20), so the correction lands exactly where the
    mis-scale was and nowhere else. _v2 columns sit BESIDE the originals; nothing was overwritten.
 5. R-2 CHANGED NOTHING BECAUSE NOTHING WAS WRONG: <SR>_knot already thresholds that family's own
    width_atr at 0.5, element for element, 0 violations on every cell. The veto ratifies the
    substrate; BR-dispersion is demoted to a reported column and is never a knot definition.
 6. R-1 IS INERT AND THE OPERATOR NEEDS TO RULE. min(0.75, 0.6 x p95 spread) can only LOWER delta,
    and only for a pair whose p95 spread is under 1.25 ATR; all five inert pairs are inert because
    they are WIDE. Measured veer reach NEVER exceeds 0.61 ATR on
    any of them anywhere on the panel, so no delta at or above ~0.62 can ever wake them, and a
    spread-sized delta will never be that low. A working law sizes off the REACH distribution
    (p95 ~ 0.28-0.33). NOT TAKEN HERE — a different law is a different veto.
 7. 26_89 WAS NOT IN THE FILED TAXONOMY (it is a cross-FAMILY adjacency; the taxonomy is 18
    within-family + 5 midline + price/band). Derived this pass from the pinned emas substrate with
    the same crossover rule and feasibility gate, labelled derived<emas> on every row, and excluded
    from F-O1. F-O1b licenses the rule by re-deriving 12_26 exactly: 197,305 = 197,305, 0 mismatched
    cells.
 8. 12_26 IN-WINDOW vs BARE IS DEGENERATE: a window closes on the counter 12_89 cross that arms the
    next one, so windows TILE the armed span — measured 100.0000% union coverage on all 25 cells.
    'bare' can only be the warm-up head: 264 events against 197,041.
 9. THE 4h LENS IS THREE-QUARTERS OF A LENS, for three different reasons: H20 is INFEASIBLE there
    (bars = 0 under the duration-fixed law, NaN, never substituted); knot->fan and spring do not
    exist at 4h because Part A pins its lens lists to [5m,15m,30m,1h]; 2618_4618 is unrealizable
    (EMA-4618 warm-bars exceed 4h history, verdict NEVER on all five assets); and VH/UH orientation
    is vacuous (UH is never warm, so 100% of 4h rows fall to 'mixed'). Each prints its own cause
    per cell rather than showing an empty zero.
10. F-O1 AND F-O1b PASS. Every native cross class, both halves of 12_26, and spring reconcile
    EXACTLY (delta = 0) to the filed crosses/windows/springs inventories; knot->fan is a join and is
    bounded by both parents.
11. BOX-COST is stated in §7 of the build document. The box was ALREADY AT WARN before this paste.
PENDING (operator rulings; none blocks this document):
 1. Re-size the kiss delta off the veer-reach distribution, or accept the five pairs as permanently
    inert and record that. (F-1)
 2. Promote 26_89 into the pinned crosses taxonomy and re-run stage 4, or keep it derived-at-query.
    (F-2)
 3. Redefine IN-WINDOW as a narrower predicate — e.g. inside a TRIGGERED window and before its
    trigger bar — or retire the split. (F-3)
 4. Extend transitions/springs/refusals to 4h, or pin the lens set to [5m,15m,30m,1h] and stop
    asking for 4h rows that cannot exist. (F-4)
 5. state_eps_atr = 0.05 IS THE FOURTH scale-mismatched constant and rev C did not name it. It is
    still global and still unscaled. (F-7)
 6. Carried from 2026-08-14: the completeness fixture is still missing; 1m stages 2-4 unrun; the
    annex (JTO/TAO) never built.
NEXT: the operator reads §1 (the kiss re-pin is inert, and the measurement that says why), §4 (the
grid), and §6 F-3. Owner: operator.
METRICS: operator actions this session = 1 (the CENSUS-2B ORACLE rev C paste) — files re-ingested
= 0 — indicator filed = 1
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-15b ===
NOW: VIZ-2 CATHEDRAL PAYLOADS ARE EMITTED. Four payloads -- the May-26 tape, the twelve station
cards, the terrain and the BTC 1h helix -- F-V3 PASS, m = 0, all local under
research_outputs/census2b/viz_payloads/ with a 7-file DESIGN_HANDOFF_VIZ3. write_payload is
IMPORTED from census2a_viz so the meta block has one implementation across both viz stages.
CLASS: DISPLAY-ONLY / Tier-E exploration. NO REGISTRATIONS. m = 0.
LAST EVENT: 2026-08-15 -- VIZ-2 cathedral payloads, appended to the ORACLE run's close
FACTS:
 1. DESIGN_CONTRACT_VIZ3 DOES NOT EXIST AND NEVER HAS -- zero hits in the working tree and in
    every blob reachable from every commit on every branch, for DESIGN_CONTRACT, VIZ3, VIZ-2,
    cathedral, station card, and helix alike. What governs is a PAIR: DESIGN_BRIEF_CENSUS2A_VIZ
    (whose §3 IS the payload-spec template this build's §3 follows) and BUILD_2026-08-12_CENSUS2A
    _VIZ1 (where the real eleven-key meta block lives). Both are in the handoff.
 2. NO CANONICAL TWELVE EXISTS. The estate's own use of the word is BUILD_2026-08-14 §9 "STATION
    OCCUPANCY -- the six-stage kit, photographed", and that is SIX. The twelve emitted are the
    twelve ORACLE classes, the only twelve-item structure the estate has; the class->stage mapping
    is THIS PASS'S READING and is flagged on the payload. The gate text it selects is verbatim.
 3. TWO RECORDS ARE "THE SIX-RULES RECORD" -- the trade-lifetime six-stage kit S1..S6, and IRON
    RULES IR1..IR6 in the design brief. Both are carried VERBATIM rather than guessing between
    them; stations quote the lifecycle gate, and switching needs no re-run.
 4. S4 and S5 CARRY NO STATION (coverage S1x6, S2x3, S3x2, S6x1). They are post-entry disciplines
    and the ORACLE classes are all events. Their gate text is still emitted in full -- the record
    is complete where the mapping is empty. Forcing a class in would have been invention.
 5. `bell` IS A ROLE ALIAS, NOT AN EVENT. The word occurs exactly once in the estate and names the
    arming. No fifth object was invented; the fifth cross family the dossier does carry (300x450)
    is emitted under its own name.
 6. `fuzz` HAS NO ANCHOR -- zero hits repo-wide. veto_pins is emitted per station; what fuzz was
    to do to those names needs the operator's word.
 7. COLUMNAR ENCODING KEPT EVERY ROW. Object-per-row put the helix at 1.33 MB and the terrain at
    812 KB, both over the 700 KB cap; column arrays fit with ZERO rows dropped -- the terrain would
    otherwise have lost 977 campaigns to a top-N slice.
 8. THE TERRAIN IS SLIGHTLY SURVIVORSHIP-TILTED: 260 resolved WF1 campaigns have no cen5 row and
    257 of them exit on `stop`, all intraday. Dropped upstream by cen5, named here, not corrected.
 9. 542 NULL MFEs WERE ZEROS, not gaps (wf1 reads exactly 0.0 on all 542) -- emitted as 0.0 so they
    do not sort to an arbitrary end and vanish. is_winner is sign(ride_R) > 0; the size-scaled
    realized_r reading would flip 38 of 6,834, so the ruler is stated rather than assumed.
10. F-V3 PASS: all four payloads round-trip json.load and re-hash to their own meta.sha256, all
    under cap; the May-26 timestamps reconcile EXACTLY to the D-CEN2c row (MC1 D3.event_card) and
    the four legs match the anatomy printed in BUILD_APOLLO_2026-08-06_MC1.
PENDING (operator rulings):
 1. Name this viz stage and write its contract, or ratify BUILD_2026-08-15_VIZ2_CATHEDRAL as it.
 2. Rule on the twelve: promote the ORACLE-class reading, or name a real twelve.
 3. Rule on `fuzz`, or drop the word.
 4. THE BUS IS AT THE REFUSE LINE. exchange/** is at ~39.9% of a 40%-refuse box and this paste
    does not fit in what remains. Three cheap ways out, all the operator's: a named-set early
    rotation of the spent census-2A/V-ULT-1 documents (the machinery exists and was ratified for
    exactly this on 2026-08-15), raise BOX_BYTES, or allow_oversize for one paste. NOT overridden
    here -- that would be this lane overruling a ratified guard on its own authority.
NEXT: the operator reads §4 V-1/V-2 and §5 BOX-COST. Owner: operator.
METRICS: operator actions this session = 1 (the VIZ-2 paste) -- files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-15c ===
NOW: THE BOX IS RAISED AND THE VIZ-2 PAPERWORK IS FILED. This entry SUPERSEDES the bus-status half
of 2026-08-15b (which recorded the REFUSE and left the documents waiting); everything 15b says
about the payloads themselves stands unchanged.
CLASS: repo operation + DISPLAY-ONLY / Tier-E filing. NO REGISTRATIONS. m = 0.
LAST EVENT: 2026-08-15 -- operator box ruling ["box", VETO], guard raised, publish retried
FACTS:
 1. OPERATOR RULING ["box", VETO], 2026-08-15: publish_exchange BOX_BYTES 6_390_000 -> 16_000_000,
    WARN_FRACTION 0.25 -> 0.50, REFUSE_FRACTION 0.40 -> 0.80. Named constants, cited to the ruling
    in the commit message and in an in-file comment. THE 30-DAY ROTATION REMAINS SCHEDULED (queue
    003, next ~2026-08-28); AGE_DAYS was NOT touched. The ceiling rises, the housekeeping stays.
 2. exchange/** went from 2,566,419 B = 40.16% REFUSE to 2,568,320 B = 16.05% OK.
    Boundary semantics preserved: exactly 80.0% warns, it does not refuse -- the same literal
    reading the guard has always applied to its own stated limit.
 3. TWO PRIVATE COPIES OF THE CONSTANT WERE FOUND, AND ONE HAD ALREADY GONE STALE.
    scripts/rotate_reports.py imports publish_exchange.BOX_BYTES live -- correct by construction,
    no change. scripts/census2b_report.py held a hand-kept copy that the raise would have made
    wrong by 2.5x on every occupancy figure it prints -- now IMPORTED, one definition in one place.
    scripts/census2b_oracle_report.py is deliberately LEFT PINNED at 6,390,000: it regenerates a
    FILED document whose BOX-COST records the box at filing time, and importing the live constant
    would silently rewrite a historical record with a ceiling that did not exist when it was
    written. A historical report reproduces history.
 4. FULL TEST SUITE GREEN after the raise: 214 passed. No assertion anywhere depends on the old
    thresholds.
 5. THE ATTACHED CONTRACT DID NOT ARRIVE. DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md is
    NOT present anywhere on this machine -- searched ~/Downloads, ~/Desktop, ~/Documents, /tmp and
    the whole repo, by name and by the tokens VIZ3 / CATHEDRAL / DESIGN_CONTRACT. The one prior
    attachment this lane received (SS_v12_0_1.pine) was found in ~/Downloads by exactly this
    method. NOTHING WAS FILED AND NOTHING WAS RECONSTRUCTED: writing the contract from the recon's
    description of what it should say would produce a document that looks ratified and is not.
    Item 2 of the ruling STANDS OPEN -- re-attach and it files in one pass. Finding V-10.
 6. Consequently VIZ-2 finding V-1 is UNCHANGED: as of this filing, DESIGN_CONTRACT_VIZ3 still
    does not exist in the estate, and the governing text remains the design brief + the VIZ-1
    build doc, both already copied into DESIGN_HANDOFF_VIZ3.
 7. FILED THIS PASTE: BUILD_2026-08-15_VIZ2_CATHEDRAL.md (its BOX-COST section rewritten before
    filing to record BOTH halves -- the refusal and the ruling -- rather than filing a statement
    the ruling had already made false), the CENSUS2A_PROBE_LEDGER m=0 line, and 15b.
PENDING (operator):
 1. RE-ATTACH DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md. Blocks nothing; files in one pass.
 2. Carried from 15b: name this viz stage's contract (or ratify the build doc as it); rule on the
    twelve stations; rule on `fuzz`.
NEXT: the operator re-attaches the contract, then reads VIZ-2 §4 V-1/V-2. Owner: operator.
METRICS: operator actions this session = 2 (the VIZ-2 paste, the box ruling) -- files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-15d ===
NOW: CORRECTION TO 15c FACT 3 AND TO BUILD_2026-08-15_VIZ2_CATHEDRAL §5. Both say TWO private
copies of the box constant were found. THE TRUE COUNT IS THREE, plus two stale text sites. An
adversarial sweep run against the raise found what the first pass missed; the fix is commit
905b9fc and the suite is green. Nothing about the ruling, the raise, or the publish changes --
only the completeness of the dependent list I filed.
CLASS: repo operation. NO REGISTRATIONS. m = 0.
LAST EVENT: 2026-08-15 -- box-raise completeness sweep
FACTS:
 1. THE THIRD COPY: scripts/mc1_report.py:20 held BOX_CAPACITY = 6_390_000 -- a private copy under
    a DIFFERENT NAME, which is exactly why a grep for BOX_BYTES did not surface it. Left PINNED
    (it regenerates the MC-1 document filed 2026-08-06; a historical report reproduces history)
    but now LABELLED as historical rather than reading like a constant that should have tracked
    the guard.
 2. A STALE TEXT SITE I INTRODUCED: census2b_report.py:227 hard-coded "WARN line / REFUSE line |
    25 % / 40 %" and printed it directly beside the freshly-imported 16 MB BOX_BYTES -- the table
    contradicted itself, and the raise is what made it do so. Now interpolated from the imported
    WARN_FRACTION / REFUSE_FRACTION.
 3. A STALE POLICY STATEMENT: rotate_reports.py's docstring asserted "warns at 25% and refuses
    above 40%" as CURRENT policy. Rewritten so the measured history stays history, the live
    thresholds are named as imported, and the ruling's point is on the record: the ceiling rose,
    the housekeeping stayed, AGE_DAYS is still 30.
 4. THE LESSON, for the next lane that changes a named constant: grepping the constant's NAME is
    not a completeness check. Two of these five sites do not contain the string "BOX_BYTES" at
    all. Grep the VALUE and the THRESHOLD TEXT as well.
 5. Full suite green after the correction: 214 passed. exchange/** unchanged in substance.
PENDING: unchanged from 15c -- re-attach DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md
(item 2 of the box ruling, still open; nothing blocks on it).
NEXT: the operator re-attaches the contract. Owner: operator.
METRICS: operator actions this session = 2 -- files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-15e ===
NOW: THE PROSE LANE OF THE BOX RAISE IS DONE. The 2026-08-15 ruling changed a constant; four LIVE
documents still described the old one, and one of them was a standing INSTRUCTION that would have
re-manufactured the stale figure on the next HERMES cycle. All four corrected, PRIMER first.
CLASS: repo operation / record maintenance. NO REGISTRATIONS. m = 0.
LAST EVENT: 2026-08-15 -- box-raise prose sweep
FACTS:
 1. ORDERING WAS LOAD-BEARING AND IS WHY PRIMER WENT FIRST. exchange/DIGEST.md has NO generator --
    it is rebuilt by hand each HERMES cycle from PRIMER_HERMES §6. Correcting DIGEST first would
    have been undone by the next cycle, because PRIMER §6.2 still said "against 6,390,000 B".
 2. FOUR LIVE DOCUMENTS CORRECTED:
    - PRIMER_HERMES_2026-08-11_v4.md §2b and §6.2 -- the standing measure-against instruction, now
      16,000,000 B, with the guard named as the place to read it from rather than this line.
    - CONVENTIONS.md §4.2 -- the BOX COST column definition (a MANDATORY column in every future
      build document, which would have carried a dead denominator forever), the capacity statement
      of record, and the 1% trip-wire.
    - DIGEST.md §2 and §6 F-1 -- re-measured against 16 MB and the resolved alarm closed.
    - NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS -- the bus row of today's all-lanes
      broadcast, which is what the three web lanes read.
 3. THE 1% TRIP-WIRE IS THE ONE REAL POLICY CONSEQUENCE AND IT IS FLAGGED, NOT BURIED.
    CONVENTIONS §4.2 flags any artifact over ~1% of the budget to the operator BY NAME. Raising the
    box moved that trip-wire from ~63,900 B to ~160,000 B -- a 2.5x loosening nobody separately
    asked for. It is left PROPORTIONAL because that is how the rule is written, and the consequence
    is now stated in the conventions themselves along with the one-line alternative (state it as an
    absolute ~64,000 B if the intent was a sensitivity rather than a fraction). OPERATOR'S CALL.
    For scale: each of this lane's last three build documents would have tripped the old wire and
    none trips the new one.
 4. F-1 IS CLOSED, AND THE WAY IT CLOSED IS WORTH KEEPING. DIGEST F-1 ("the bus refuses before
    rotation can fire") proposed shortening the 30-day rotation to ~10 days, which would have made
    ~40 reports eligible at once. The ruling went the OTHER way: raise the ceiling, leave the
    housekeeping. No report left the bus earlier than its ratified window -- the outcome the
    redraft would have cost. Recorded as resolved-and-superseded, not deleted.
 5. NOTHING FILED WAS EDITED. Working-tree diff is exactly four files, 54 insertions / 25 deletions,
    and every deletion is a replaced live-policy line. Verified untouched: every LEDGER_*.md, every
    queue/*.md ratified contract, every BUILD_*.md, CENSUS2A_PROBE_LEDGER.md, ROTATION_LOG.md. Line
    endings unchanged (all four were and remain LF).
 6. THE SUPERSEDED NUMBERS SURVIVE AS HISTORY, NOT AS POLICY: 785,732 B headroom, 794,687 B added
    in 24h, the 27.70% reading, ARGUS's 770 KB / 4,024,198 B comparison -- all preserved and
    era-anchored to the then-6.39 MB box rather than erased or silently rescaled. CONVENTIONS'
    "two files outweighed a lane's entire written history five to one" is a RATIO and survives the
    raise untouched; it was not weakened.
 7. REMAINING repo-wide hits on the old figures are all correctly historical: filed BUILDERS_REPORT
    and NOTE documents, ratified queue contracts, append-only ledgers, the two deliberately-pinned
    report generators, and status/daily/DAILY_*.md -- which are dated snapshots of what the guard
    said that day AND self-heal, since daily_routine reads the figure from publish_exchange at run
    time. None is a live instruction.
 8. exchange/** = 2,577,306 B = 16.11% of the 16,000,000 B box. Level OK.
 9. DIGEST WAS EDITED OUT OF CYCLE. It is HERMES's artifact and HERMES retains regeneration
    authority; this pass corrected the figures in place because the alarm it carried was void and
    the web lanes read it live. The next HERMES cycle will rebuild it from the corrected PRIMER.
PENDING (operator):
 1. The 1% trip-wire: leave proportional (~160,000 B, current) or pin absolute (~64,000 B). Fact 3.
 2. Carried: re-attach DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md; name the VIZ stage's
    contract; rule on the twelve stations; rule on `fuzz`.
NEXT: the operator rules on the 1% trip-wire. Owner: operator.
METRICS: operator actions this session = 3 -- files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-15f ===
NOW: THREE DEFECTS IN THE 15e PROSE SWEEP, FOUND BY AN ADVERSARIAL VERIFIER AND FIXED. This entry
SUPERSEDES 15e on two points of fact. The sweep's substance stands; its completeness did not.
CLASS: repo operation / record correction. NO REGISTRATIONS. m = 0.
LAST EVENT: 2026-08-15 -- post-publish verification of the box-raise prose sweep
FACTS:
 1. I CITED THE WRONG SECTION, AND PROPAGATED IT INTO TWO LIVE INSTRUCTION SURFACES. The ~1% naming
    trip-wire and the BOX COST column both live in CONVENTIONS **§3.2** (The file-disposition table,
    line 405ff), NOT §4.2 (The exchange bus, line 577ff). 15e facts 2 and 3 say §4.2 -- WRONG, and
    corrected here rather than edited there. The same wrong reference had been written into
    PRIMER_HERMES §6.2 and DIGEST §2, i.e. into the standing instruction that regenerates the DIGEST
    budget block every cycle: HERMES would have been sent to a section that does not carry the rule
    it was told to apply. Both live surfaces now read §3.2. NOTE: §4.2 is a real section with a real
    rule -- text-only / 1 MB per file, the one publish_exchange quotes on refusal -- so the filed
    reports that cite it are correct and were left alone. My error was the pairing, not the number.
 2. I FIXED ONE OF TWO IDENTICAL CLAIMS IN THE SAME FILE. NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-
    STATUS carried "box at ~37%" TWICE: the geography table (line 30, corrected in 15e) and §4 OPEN
    ITEMS (line 79, MISSED). The missed one was worse than stale: it listed the box as an OPEN item
    owned by "operator word" when the operator had already given that word in the same day's ruling,
    on a broadcast whose whole purpose is telling six lanes what is currently true. Now struck
    through and marked CLOSED with the ruling named.
 3. I RE-STAMPED A SECTION AND LEFT A CONTRADICTION 26 LINES INSIDE IT. DIGEST §2 header now reads
    "measured 2026-08-15, against 16,000,000 B", but its closing paragraph still read "Data is now
    3.05% of the box, down from 8.74%" and "reports/ holds 77 files" -- 6.39-MB-era denominators and
    a stale file count, against the same section's corrected "1.31% (11 files)" and "98 files". Both
    now era-anchored and reconciled, with the 16 MB readings stated beside them. DIGEST §7 F-3
    carried the same un-anchored 8.74%/3.05% pair and got the same treatment.
 4. THE COMMON SHAPE OF ALL THREE: I corrected the line I went looking for and did not re-read the
    surrounding document. Grepping for a VALUE finds the values; it does not find a claim that
    CONTRADICTS a value, an OWNERSHIP row that a ruling has closed, or a second instance further
    down the same file. 15e fact 4 already recorded that grepping a constant's NAME is not a
    completeness check; the sharper form is: **after editing a document, re-read the document.**
 5. WHAT 15e GOT RIGHT AND STANDS: the ordering (PRIMER before DIGEST, because DIGEST has no
    generator); the four documents identified as live; the 1% trip-wire flagged as an operator
    decision rather than silently taken; every superseded figure era-anchored rather than erased;
    nothing filed edited. The verifier independently confirmed the guard's boundary behaviour
    (budget(12,800,000)=WARN, budget(12,800,001)=REFUSE) and found NO other live instruction
    document missed -- CADENCE, RETENTION, HEARTBEAT, MANIFEST.json, every README and every other
    lane's primer are clean, and the live CENSUS2A contract states BOX-COST as a bare fraction
    ("bus additions <1%"), so it tracked the raise for free.
 6. exchange/** = 2,582,800 B = 16.14% of the 16,000,000 B box. Level OK.
PENDING (operator): unchanged from 15e -- the 1% trip-wire (leave proportional at ~160,000 B, or pin
absolute at ~64,000 B); re-attach DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md; name the VIZ
stage's contract; rule on the twelve stations; rule on `fuzz`.
NEXT: the operator rules on the 1% trip-wire. Owner: operator.
METRICS: operator actions this session = 3 -- files re-ingested = 0
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-15 ===
NOW: TIER-C2 IS MEASURED. The forward baseline — the number every multiplier must
     beat — is **−0.7762 R per trade over 10 trades**, 2025-10-06 → 2026-01-31,
     net of a 10 bps round trip and journaled funding. Net R −7.7620 · win rate
     10.0% · maxDD 9.5107 R. **It is NEGATIVE, and it is stated as commissioned.**
     THE SEAL WAS KEPT. The ratified STAGE A corridor (2024-07-01 → 2026-01-31)
     was **79.7% sealed lockbox** — its start date IS `LOCKBOX_START_MS`, and
     LEDGER.md:865 rules the seal governs scored outcome evidence, which is
     exactly what a headline is. Raised mid-build with the arithmetic; operator
     ruled SEAL INTACT. The corridor moved; the seal did not. **462 sealed days
     remain unspent and unread**; no outcome was computed over one of them.
CLASS: measurement, not registration. m = 0. No lockbox spend. No estate write.
       No live orders. engine/ and analytics/ byte-untouched (zero diff).
LAST EVENT: 2026-08-15 — TIER-C2 BASELINE + Amendment B1 analytics tape, ONE build
       document: exchange/reports/BUILD_2026-08-15_TIERC2_BASELINE.md
ARTIFACTS: scripts/tierc2_rules.py (the decision path) · scripts/tierc2_baseline.py
       (the program) · scripts/tierc2_fixtures.py (the transcript) ·
       configs/tierc2_paper.yaml (Stage-B profile). Tables local, gitignored, at
       research_outputs/tierc2/ — funnel · headline · monthly_equity ·
       stop_geometry · trade_journal · strip_d_unscored · display_only_strips ·
       analytics_tape (643 rows) · tape_inventory · build_manifest.json ·
       heartbeat.json. Determinism root research_outputs/tierc2_run2/.
FACTS: [9]
 1. THE TIDE IS THE WHOLE FUNNEL. 27 of 43 armings removed — 63% — and removed by
    DIRECTION, WHOLESALE: every long on BTC/ETH/NEAR/SOL, every short on ZEC. Over
    118 days the panel was one-way. `d` removed 3 more. NOTHING ELSE LEAKED — no
    trigger refused for an open position, none for a missing structural anchor,
    none for a degenerate R. This baseline measures ONE REGIME and cannot separate
    "the rule card is negative" from "shorts were wrong in Q4-2025".
 2. 9 of 10 trades were shorts and ALL NINE DIED AT THE STOP. The single long
    (ZECUSDT, +1.7487 R, belled 12/89) is the single winner.
 3. THE STOP IS UNRAILED AND ONE TRADE CARRIES 89.5% OF THE COUNTERFACTUAL. R comes
    from a 1H pivot but entry from a 4h bar, so R ran 0.52–2.16 × ATR. Bell-only
    (no stop honoured) gives +14.8733 R against the headline's −7.7620 — a 22.6353 R
    gap, of which **20.2572 R is one ETHUSDT trade** entered at R = 0.52 ATR and
    stopped on the very next bar, whose LOW was favourable. Strip it and the stop
    costs 2.38 R across the other nine. The architecture of record carries
    `min_stop_atr = 0.5` (G-8c, configs/tc1_B.yaml:53); THE RULE CARD NAMES NO RAIL.
 4. THE TOLL TAKES UP TO 19.36% OF R. Fixed 10 bps against a stop that can sit half
    an ATR from entry: median toll share 3.28%, max 19.36%, and the two tightest-R
    trades are the two worst net R in the book.
 5. THE TAPE IS CAPTURED-NOT-CONSULTED, PROVED BY IMPORT CLOSURE, NOT BY GREP. The
    decision path is its own module; its AST imports are {engine.indicators,
    engine.s1, numpy, dataclasses}; its 239-module transitive closure contains no
    analytics member; and engine/ imports no analytics module either (invariant
    I-B), so the closure CANNOT reach a registry symbol by any path. The line-grep
    the amendment asks for is printed beside it — and it FAILED on first run,
    matching the module's own prose about not importing analytics. That false
    positive is why the AST scan is the test of record.
 6. SABOTAGE REJECT RE-PROVEN ON THIS CORRIDOR. F-10's lever with extra_bars=1
    raises "CAUSALITY VIOLATION: bar closing 2025-12-04T08:00:00Z is in the future
    of the as-of instant 2025-12-04T04:00:00Z"; and against the real level path a
    7d RVWAP built one bar into the future reads 89,859.14 vs the stored 89,828.12.
    All 30 level series reconciled under ACTUAL endpoint slicing at that instant.
 7. THE SINGLE-WALL STAMP IS 'multi' 73.2% OF THE TIME (427 of 583 spine instants;
    35 of 43 armings). It is raw material, not a finding, and nothing here
    conditions on it — but any location gate built on it would be built on a label
    that says "several".
 8. THE FUNNEL UNDERCOUNTS BY A LEFT EDGE, MEASURED. In the 30 days before the
    scored window, 4 armings passed tide+d and 2 of them triggered INSIDE it —
    trades this baseline does not contain. Against n = 10 that is a potential 20%
    undercount.
 9. 7/7 FIXTURES PASS. Suite `pytest fixtures tests -m "not slow"` = 288 passed,
    1 skipped, exit 0 — unchanged from session start; no existing test touched.
    Full re-run hash-identical on all 9 tables. Seed 20260815 is printed and
    UNUSED: no stochastic step exists, so determinism here is structural.
STAGE B — LIVE PAPER ARMED: one heartbeat executed. POSITIONS: 1 OPEN (NEARUSDT
     short, entry 2026-07-22T00:00Z @ 1.911, stop 1.959687, held 147 bars, mark
     1.635, unrealised +5.6688 R). ARMED AWAITING TRIGGER: 1 (BTCUSDT short since
     2026-08-11T12:00Z, d = 1.601421). configs/tierc2_paper.yaml COMMITTED; the
     com.naiad.daily 07:00 agent is UNTOUCHED (agent_modified: false,
     registered_in_routine_jobs: false) — wiring it into scripts/routine_jobs.json
     is a separate operator act and was NOT taken. NOTE: the rule card is NOT
     expressible in engine/signals.py — `grep -rn 316 engine/*.py` returns ZERO, so
     the 316 leg would fork the frozen Pine port and break F-SIG. The profile
     therefore follows engine config grammar while its EXECUTOR is
     scripts/tierc2_rules.py — bit for bit the module Stage A replayed, so Stage A
     and Stage B cannot disagree.
Q6 DECISION RULE INVOKED: Q6c — "stillbirth counterfactual first: rescore all
     historical fills by range-position BEFORE any location gate becomes law."
     This baseline IS that unconditioned population of fills, and the analytics
     tape IS the location record it must be rescored against. Nothing in the rule
     card read a registry symbol, which is precisely why the counterfactual is
     still answerable. No location gate is proposed here, and none may be adopted
     until it has been scored against this population.
NAMING ["tc-name"]: the parked **TC-2** re-entry-quality bar is RENAMED **TC-RE**
     from this entry forward (HANDOFF_2026-07-22_Census_to_Census1b.md:96;
     docs/memory/claude_project_memory_2026-07-26.md:84-85). It is a DIFFERENT
     OBJECT from Tier-C2, this baseline; no equivalence was ever stated anywhere,
     and the collision is now removed at the name. 60 prior occurrences of "TC-2"
     across 25 files are NOT swept — the instruction was a ledger touch; a
     repo-wide rename is its own authorised act.
PENDING (operator): 7 rulings, all in §9 of the build document —
     F-1 the corridor's permanent shape (post-lockbox for good, or a spend at a
         future gate; "clean corridor"/2026-01-31/the pinning window are new names
         that exist nowhere in the estate before this paste)
     F-2 whether 118 days / n = 10 is an acceptable yardstick window
     F-3 the G-8c stop rail — adopt into the rule card, re-derive R on the entry
         lens, or accept the geometry and say so
     F-4 does the stop EXECUTE — the rule card's "no management of any kind" admits
         both readings and they differ by 22.6 R; read here as "the stop executes",
         with the bell-only alternative printed unscored
     F-5 the funnel's left edge — prepend a warm-arming lead-in, or accept the bias
     F-6 narrow the wall test before any location gate is built on it
     F-7 the VR-1 forward edge — truncate continuity strips at 2026-07-07, or
         ratify that Tier-C forward baselines may read the forward partition for
         display (the pinning strip's last 35 days cross it; printed as
         commissioned, disclosed here)
NEXT: the operator reads §0 (the seal), §3 (the number, and what the stop cost it),
     and §9 F-3/F-4. Owner: operator.
PROBE LEDGER: m = 0. Stamp: EXPLORATION — ungated; promotion requires registration.
BOX: exchange/** = 2,608,293 B = 16.30% before this paste, tick set (exchange/** +
     LEDGER.md) 2,863,304 B = 17.90%. This paste adds 45,692 B = 0.286% of the box
     — exchange/** to 2,653,985 B = 16.59%, tick set to 2,908,996 B = 18.18%, level
     OK (warn 40 / refuse 70). 57% of the <0.5% target; ~34 KB unspent. The full
     fixture transcript, the 643-row tape and the per-trade journal stay LOCAL.
R3: the determinism rerun was hashed against run 1, then its DATA discarded in the
     same session per rule R3; research_outputs/tierc2_run2/build_manifest.json is
     retained per refinement D-3 — discard the data, keep the provenance.
=== END STATUS ===

---

## 2026-08-15 — CARRIED BACKLOG RELOCATED HERE FROM CONVENTIONS §7 (THE GREAT COLLAPSE)

*Filed by HEPHAESTUS during the CONVENTIONS restructure. These items were sitting in the file all
six actors read; they are APOLLO's lane state, and CONVENTIONS §5 rules that lane state lives in the
lane ledger. Nothing is changed — the text is carried verbatim from CONVENTIONS as it stood at
commit a2b69cf, §7.1 and §7.2. CONVENTIONS §7.8 now points here.*

### SS Pine display backlog — MOVED FROM MEMORY #1, full text
*(APOLLO's lane. Display-only; no study impact. Both items are inherited requirements of the
SSv12 Pine deliverable.)*

**B-1 · "SWING MODE"** (operator, 2026-07-10): make 12H governor/regime signals printable in the
SS Pine indicator. Context: v11's `tfGovern` input defaults to 240 and drives all regime tint and
triangles, and the 12H cascade layer is suppressed when chart TF = 720. **Exact semantics —
mandate presets vs un-suppressing the native-TF layer — to be pinned at SSv12 spec time.**

**B-3** (operator, 2026-07-11): in v11.0.2 grade text prints only on R1 PRIMEs, while all R2+ adds
render as identical unlabeled tiny circles (A+ indistinguishable from B). Chartered as **SSv11.3**
— grade-differentiated glyphs (VR-A Option 3, VR-B defaults ratified) plus playbook erratum
corrections for **E-1** (faint-tint / provisional Z2 entries are real in v11.0.2; the code revert
is deferred to a v12 named-variant slot).

**Reminder:** parity charts stay pinned to v11.0.2 until 3C closes.

### SS interview rulings Q1c–Q11 — MOVED FROM MEMORY #19
APOLLO's lane, locked for census design, ledger-backed. **Verbatim text:**
`docs/memory/claude_project_memory_2026-08-03.md`, Entry 19.

Operative summary: full signal taxonomy (Q1c) · sequential fingerprint mining as census headline,
`{9,89,200}` and `{12,25}` in parallel (Q2a) · the anti-fishing package ratified as written (Q3a)
· lenses to 1W measured, 1M display-only (Q4) · verdict shape with hysteresis as registered prior
(Q5) · stillbirth counterfactual first (Q6c) · borders as walls + rectangles, midrange as a
first-class object (Q7c) · PRIME as mandatory control arm (Q8b) · three add-families counted at
winning moments (Q9c) · exit counterfactual leg with the operator's H-RVX-2 prediction (Q10a) ·
volume overlay deferred to 2b (Q11a).

*The standing analytical principles that used to ride with this block — HTF→LTF ordering, HTF
enclosure stamping, signals-as-relationships — were promoted to CONVENTIONS §7.8 as rules, because
they bind every study lane and not only this one.*

=== STATUS_APOLLO — 2026-08-15b ===
NOW: VIZ-4 · THE EMA MANTLE — payloads built, ferried, F-V4 PASS. Four payloads
     (mantle + echo, BTC 1h and 5m), 12.7 MB, local; DESIGN_HANDOFF_VIZ4/ ready
     for the Claude Design session. Class DISPLAY-ONLY / Tier-E, m = 0, no
     registrations, no rule adopted. Echoes are SHOWN, NOT SCORED.
CLASS: Tier-E exploration. m = 0. No registration. census2b/ substrate, analytics/
       and engine/ read-only and untouched.
LAST EVENT: 2026-08-15 — VIZ-4 payloads, one build document:
       exchange/reports/BUILD_2026-08-15_VIZ4_MANTLE.md
CONTRACTS: DESIGN_CONTRACT_VIZ4_EMA_MANTLE_2026-08-15.md FILED to
       exchange/reports/ from the operator's attachment, sha256
       8e8b3264805c9dee92d4bd9ad79ba62e56f1f404175d9a60d82ae9d1b1cdec7c, 3,857 B.
       *** V-10 DOES NOT CLOSE. *** DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md
       is ABSENT — not in exchange/reports/, not in the attachment folder, nowhere
       in the tree; DESIGN_HANDOFF_VIZ3/ holds the four v3_*.json payloads and
       three documents, but NO contract. It was NOT invented and NOT ferried. The
       re-attach item carries a SECOND cycle.
ARTIFACTS: scripts/census2b_viz4.py (new) ·
       research_outputs/census2b/viz_payloads/{v4_mantle_BTC_1h, v4_echo_BTC_1h,
       v4_mantle_BTC_5m, v4_echo_BTC_5m}.json + viz4_manifest.json ·
       research_outputs/census2b/DESIGN_HANDOFF_VIZ4/ (4 payloads + the contract).
       Payload data-block shas: mantle-1h c01bd118df16ae17 · echo-1h 4fd09d4f233f077a
       · mantle-5m 0676e3c1c2502a0e · echo-5m a3f683f437fee134.
FACTS: [6]
 1. A KNOT->FAN MARK ALMOST NEVER STARTS A FAN. F-V4 (d) first asserted every mark
    lands on a fan ONSET and FAILED 2,568 of 2,710. The estate never promised it:
    `fans` splits an ordered run at every direction change, and a ribbon can be
    KNOTTED while `orient` is already bull/bear, so a knot commonly releases into
    a fan ALREADY RUNNING. Measured: only 142/2,710 (5.2%) at 1h and 1,479/37,501
    (3.9%) at 5m begin a new fan. Every mark now carries `at_fan_onset`. This
    bears directly on the contract's M2 question "did an echo precede the fan?" --
    for ~95% of marks the fan predates the knot's release.
 2. THE 1h MANTLE IS A QUARTER UNWOVEN AT THE ROD. e5000 needs 17,300 warm bars
    (WARMFACTOR 3.46) = ~721 days at 1h, so 28.5% of the rod thread is ABSENT,
    8.2% of the whole 1h cloth. At 5m it is 2.4% / 0.7%. Nulls lead unbroken and
    ZERO absent cells were written as exact zeros -- proved, not asserted.
 3. THE PAYLOADS ARE 3-6x THE VIZ-1 700 KB CAP AND THE CONTRACT'S OWN SPEC IS WHY.
    8,000 steps x 18 threads x 2 = 288,000 numbers, plus 49 lags x 8,000 = 392,000;
    no rounding fits that in 700 KB. Reductions taken and stated: disp 3 dp, vel
    5 dp, corr 2 dp (200 levels across [-1,1]), marks COLUMNAR -- which alone cut
    the handoff 18.3 MB -> 12.7 MB. The cap is VIZ-1's module constant, not this
    contract's requirement; the contract sets no byte limit.
 4. "12 AT THE HEM" IS 17 THREADS; THE FABRIC IS 18. Contract §2's axis label vs
    §1/§3's "eighteen EMAs" and RIBBONS FAST = (9,12,26). Read as: the axis spans
    9 -> 5000, and the hem EDGE for the echo is 12/26 exactly as §2 defines it.
    Both facts ship in every payload so no renderer has to guess.
 5. PROVENANCE IS READ, NOT RETYPED. Per-SR smoothing k comes from the ORACLE
    manifest's own pins {FAST 20, M 20, MH 40, H 111, VH 327, UH 577}, law
    k = max(20, round(median_len/8)) -- R-3 owns it. Toll bands are read per cell
    from that cell's transitions tables (1h 0.1355/0.1400, 5m 0.5537/0.5641), so
    the emitter's single global TOLL is re-pointed PER PAYLOAD -- an extension of
    the VIZ-2 re-point pattern, named as an extension.
 6. F-V4 PASS on all six legs; F-KEY 0 duplicates on four joins plus an explicit
    emas/ribbons grid-equality check. Suite 288 passed / 1 skipped / exit 0,
    unchanged; no existing test touched.
PENDING (operator): 4 rulings, all in §4 of the build document --
     F-1 the VIZ-3 contract: re-attach it, or promote VIZ-4's inline restatement
         of the iron rules to the rules of record and stop citing VIZ-3
     F-2 what a knot->fan mark MEANS in the design session's copy: "knot released"
         (what it is) or "fan began" (what it mostly is not)
     F-3 the 700 KB shared cap: raise it for 3D payloads, or cap VIZ-4 by
         steps-per-payload instead
     F-4 e9: keep it in the cloth (as built) or drop it to match §2's axis label
     -- carried from 2026-08-15: the seven TIER-C2 rulings, unchanged.
NEXT: the operator ferries DESIGN_HANDOFF_VIZ4/ into a Claude Design session with
     the §5 opener, and rules on F-1 and F-2. Owner: operator.
PROBE LEDGER: m = 0. Stamp: EXPLORATION — ungated; promotion requires registration.
BOX: exchange/** = 2,722,503 B = 17.02% before this document; tick set 2,981,801 B
     = 18.64%, level OK (warn 40 / refuse 70). This paste adds ~19 KB, ~24% of the
     <0.5% target. The 12.7 MB of payloads never touch the box — local, ferried.
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-15g ===
NOW: TIER-C3 IS MEASURED. THE RAILED BASELINE — the seven F's enacted as card
     diffs — is **+0.7056 R per trade over 11 trades**, 2025-10-06 -> 2026-01-31,
     net of a 10 bps round trip and journaled funding. Net R +7.7614 · win rate
     45.45% (5 of 11) · maxDD 4.2697 R.
     STATED BESIDE ITS PREDECESSOR, WHICH IS THE ONLY WAY IT MEANS ANYTHING:
         TIER-C2 (v1, 1H anchor, no rail)   -0.7762 R / trade   n = 10   win 10.00%
         TIER-C3 (v3, 4h anchor, 1.0 ATR)   +0.7056 R / trade   n = 11   win 45.45%
     SAME CORRIDOR, SAME TIDE, WINDOW, TRIGGER, BELL AND TOLL. THE NUMBER
     CHANGED SIGN. IT IS PROVISIONAL AND IS LABELLED SO ON EVERY HEADLINE ROW —
     "YARDSTICK v3 — PROVISIONAL (one regime, n small)". 9 of 11 trades are
     still shorts, and ONE trade is 71.8% of the swing.
     *** AND IT WAS NOT THE RAIL. *** See FACT 1.
CLASS: measurement, not registration. m = 0. NO lockbox read — enforced in code,
       not asserted in prose (FACT 2). No estate write. No live orders. engine/,
       analytics/ and scripts/tierc2_* byte-untouched.
LAST EVENT: 2026-08-15 — TIER-C3 RAILED BASELINE, one build document:
       exchange/reports/BUILD_2026-08-15_TIERC3_RAILED.md
       *** THAT DOCUMENT SUPERSEDES THE VERSION AT COMMIT af6ebf4. *** An
       exchange/** auto-publish fired from another lane mid-build and committed
       AND PUSHED the draft, whose headline was +6.7151 R over 12 trades. An
       adversarial audit then found a seal breach and a false attribution; both
       are fixed in code and the corrected document is the build's. The guard
       did exactly what it is specified to do — see F-C3-i.
V-10: **CLOSED BY RULING.** DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md was
       sought a third time and is ABSENT. Per F-1, VIZ-4's inline restatement of
       the iron rules is PROMOTED to the rules of record — one line,
       exchange/reports/RULES_OF_RECORD_VIZ_IRON_2026-08-15.md, cited to the VIZ-4
       contract sha256 8e8b3264805c9dee92d4bd9ad79ba62e56f1f404175d9a60d82ae9d1b1cdec7c.
       VIZ-3 stops being cited. The re-attach item is STRUCK, not carried.
ARTIFACTS: scripts/tierc3_rules.py · scripts/tierc3_baseline.py ·
       scripts/tierc3_fixtures.py (all new) · research_outputs/tierc3/ (14 parquet
       tables + manifest, local, gitignored) · .gitignore (tierc3 lines).
       Table content-shas: funnel 391fae98 · headline bd0cca2b · journal 7bf46e07 ·
       delta_v1_v3 de6f0a02 · attribution_unscored d1be133f · stop_geometry ff082da0
       · tape e5ef978a.
FACTS: [8]
 1. IT WAS NOT THE RAIL, AND THE BUILD IS NAMED FOR THE RAIL. The diffs were
    switched off one at a time and the corridor re-ridden through the SAME code
    path (attribution_unscored.parquet, F-C3-ABLATE, UNSCORED):
        V1  1H anchor, no rail, no lead-in      -7.7620 / 10   (reproduces v1)
        D   4h anchor                           +8.6507 / 10   +16.4127 vs V1
        C   4h anchor + rail                    +8.8032 / 10   +0.1525  vs D
        B   4h anchor + lead-in                 +7.6062 / 11   -1.0445  vs D
        A   4h anchor + rail + lead-in (SHIPPED)+7.7614 / 11   +0.1552  vs B
    THE ANCHOR LENS CARRIES THE RESULT. The rail is cheap insurance that almost
    never pays out on this corridor. The V1 cell reproduces Tier-C2's FILED net
    R to 2.2e-05, so every marginal is the DIFF and not the fork. Consequence
    beyond naming: the object a multiplier must beat is the 4h-anchor card.
 2. THE CARD, EXECUTED LITERALLY, READS THE LOCKBOX. F-3 quadrupled the anchor
    lookback's reach in TIME (200 bars = 200 h on 1h, 800 h on 4h) and F-5 pulled
    the first entry to 2025-10-08, two days after the seal closes. The two
    rulings met: the low of the SEALED 4h bar 2025-09-15T12:00Z becomes a scored
    trade's structural anchor — published, used as the R denominator, paid out as
    the exit price — and EVERY anchor that trade could reach is sealed, so
    without a lockbox read the trade does not exist. The CARD has no seal floor;
    the CLASS LINE does. Precedent Tier-C2 §0: "the corridor moved, the seal did
    not." Sealed bars are masked out of anchor eligibility; 2 armings refused.
    BOTH NUMBERS PRINTED: with the floor +7.7614/11, without it +6.7151/12.
    v1 was clean here BY ARITHMETIC ACCIDENT, not by design.
 3. FOUR SURVIVALS DID IT, NOT TEN. Four of the ten shared armings changed exit
    reason stop -> bell_12_89; the other six moved 0.004-0.090 R, which is only
    the toll shrinking against a wider R. ETHUSDT short 2025-10-29 alone is
    +11.1480 of the 15.5234 swing (71.8%) — the SAME trade v1's F-3 was about.
 4. THE F-3 ROW IS NOT A NEW PRICE PATH. v1's own bell-only counterfactual was
    +19.1618 R against R = 41.1318 = 788.161 price units; v3's REALISED outcome
    is +10.0526 R against R = 78.4037 = 788.161. Identical path, different
    denominator, asserted to 3.97e-05. And the width that saved it came from the
    LENS, not the rail: even unrailed, that trade's 4h pivot stop (3965.20) sits
    above the excursion that killed it in v1 (3962.55).
 5. THE RAIL IS PROVED PER TRADE. F-C3-RAIL asserts R >= 1.0 x ATR on every one
    of the eleven individually, re-derives stop = the farther of {pivot, rail} to
    1e-6, and checks rail_binding is arithmetic not a label. R/ATR range
    1.0000 -> 3.1907 (v1: 0.5246 -> 2.1637). Worst toll bite halved, 19.36% of R
    -> 9.49%. Rail BINDING on 3 of 11.
 6. THE 4h LENS DOES NOT UNIFORMLY WIDEN THE STOP. ZECUSDT's 4h anchor sat NEARER
    than its 1H anchor (0.651 ATR vs 1.044), so on that trade the lens NARROWED R
    and only the rail restored it. "Railed" is the true word; "wider" is not.
 7. THE F-5 LEAD-IN CORROBORATED v1's PREDICTION AND COST 1.04 R. v1's F-5 said
    "4 armings passed tide+d in the 30 days before, 2 triggered inside the
    window"; v3 measures 4 and 2 — of which one survives the seal floor and one
    does not. The single trade it bought is a LOSER. An edge correction that only
    ever added winners would deserve suspicion.
 8. 10/10 FIXTURES PASS, including TWO THAT DID NOT EXIST BEFORE THE AUDIT:
    F-C3-SEAL resolves every scored trade's anchor back to the bar it was quoted
    from and asserts that bar is not sealed (0 of 11 sealed) — a min/max-of-
    timestamps era test can never see a sealed PRICE, which is why the first
    draft passed 8/8 while breaching the seal. F-C3-ABLATE proves the fork
    reproduces its parent. Determinism hash-identical across 14 tables AND the
    counts block. F-KEY 0 duplicates on 13 written tables plus six funnel
    reconciliation identities. Suite 323 passed / 1 skipped / 1 deselected —
    measured WITH and WITHOUT this build's files, identical both ways (the count
    moved from 314 because commit 7176b6d landed tests/test_bus_health.py from
    another lane mid-build). The card's unchanged half is Tier-C2's OWN OBJECTS,
    bound by import: F-C3-INHERIT asserts twelve identities with `is`, so a copy
    cannot drift because there is no copy.
Q6 DECISION RULE, RE-INVOKED AGAINST v3: Q6c still governs — "stillbirth
     counterfactual first; rescore all historical fills by range-position BEFORE
     any location gate becomes law." v3 is a SECOND unconditioned population of
     fills over the same corridor, and its 640-row tape is the location record it
     must be rescored against. Nothing in the v3 decision path read a registry
     symbol — proved by AST scan over BOTH decision modules and an import closure
     whose project members are exactly {engine.indicators, tierc2_rules,
     tierc3_rules}. So the counterfactual is still answerable, and it is now
     answerable TWICE over one corridor, once per card version. That is a
     strictly better position than Q6c required and it was not paid for with a
     conditioning. NO LOCATION GATE IS PROPOSED, and none may be until the
     rescore is done.
PENDING (operator): 5 rulings, all in §8 of the build document —
     F-C3-a  THE SEAL FLOOR: ratify it as standing law (an anchor is a price, not
             a state), or overturn it and accept the sealed read with disclosure.
             Related and larger: the F-5 lead-in reaches into the seal WHENEVER a
             corridor starts adjacent to it — moving future corridor starts 30
             days later closes the whole class
     F-C3-b  THE NAME: rename the baseline, or ratify "railed" as historical and
             record the attribution beside it. The rail is +0.15 R
     F-C3-c  PIN THE LOOKBACK in the card, in BARS or in HOURS. 200 bars-in-lens
             (taken) vs 200 hours (50 bars) disagree on the anchor for 6 of 11
             trades, and the bars reading is what let the search reach the seal.
             Counts only, NO R attached to either reading
     F-C3-d  is an 11-trade, one-regime, one-dominant-trade result an acceptable
             bar for a multiplier to beat? PROVISIONAL stands until answered
     F-C3-e  TWO RAILS FOR ONE CONCEPT — G-8c min_stop_atr 0.5 and the v3 card's
             1.0. Reconcile, or name them as deliberately distinct objects the
             way TC-2 / Tier-C2 had to be
     -- also filed, not blocking: F-C3-f (the 4h lens is not uniformly wider),
     F-C3-g (NO STAGE B was built; configs/tierc2_paper.yaml and the heartbeat
     still enact the SUPERSEDED v1 card — the live paper line is one full card
     version behind the yardstick), F-C3-h (the cross-version bell-only
     comparison is not like-for-like; do not subtract them), F-C3-i (exchange/**
     auto-publishes, so a draft build document is published the instant it is
     written — the superseded draft of this build is at af6ebf4 and on the
     remote), F-C3-j (F-6 carried for the next TC; m = 0 — these tables must not
     be mined as if they were a registration).
NEXT: the operator reads §0 (the sign change, the attribution, and the seal
      floor), §3 (the delta table), and §8 F-C3-a and F-C3-b. Owner: operator.
PROBE LEDGER: m = 0. EXPLORATION — ungated; promotion requires registration.
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-16b ===
NOW: TIER-C4 IS MEASURED. THE MEAN CARD — the v3 card plus the LPS-trail ratchet
     and the creek/ice harvest — is +0.6907 R per trade over 11 trades against
     TIER-C3's +0.7056 over 11. THE MEAN DID NOT MOVE. THE SHAPE DID:
         maxDD 4.2697 -> 2.0348 · tail share 71.83% -> 50.76% ·
         net R WITHOUT the best trade -2.2912 -> +1.4184, WHICH CHANGES SIGN.
     The operator asked for "a mean for the average trade" and got one.
     THE PRICE IS THE TAIL, and it is only visible at scale: on the DISPLAY-ONLY
     127-trade census strip the same code path takes +145.4539 R -> -7.0097 R and
     the best trade +165.79 -> +5.85. Display-only, hypothesis generation only,
     and the most informative number in the build. F-C4-a.
     ABLATION (unscored, one code path, five cells): V3 +7.7614 | RATCHET-only
     +7.3262 | HARVEST-only +4.5800 | BOTH +7.5978 | BOTH_NOSEAL +6.5515/12.
     INTERACTION +3.4530 — the two amendments are NOT separable and must not be
     quoted apart. The trail pre-empts the harvest: 9 fills alone, 3 together.
CLASS: measurement, not registration. m = 0. ONE pre-named card, no grid, no
     sweep; the selection guard is LOADED, CALLED and IDLE at m = 0, in the
     manifest. NO lockbox read. No estate write. No live orders. engine/,
     analytics/, scripts/tierc2_* and scripts/tierc3_* byte-untouched.
RIDE-ONLY, PROVED AS AN OUTCOME: the ENTRY half of the ride loop is a hand
     TRANSCRIPTION, not an import, so `is` cannot reach it — and five Tier-C3
     tables therefore come out CONTENT-HASH-IDENTICAL (funnel, lead_in_census,
     lead_in_trades, strip_d_unscored, anchor_lookback_disclosure). Same
     armings, same entries, same entry stops. The bell-only counterfactual is
     byte-identical at -0.0919 R. An INDEPENDENT re-implementation written from
     the card text (scripts/tierc4_independent.py, sharing only the engine's
     EMA/ATR and the raw bars) agrees on all 11 trades.
THE REVIEW RAN BEFORE PUBLICATION, NOT AFTER: six adversarial lenses over the
     three scripts, 18 findings raised, TWELVE REPAIRED. Nothing in the headline
     moved; every repair was to a claim, a fixture, or a rule the code obeyed by
     accident rather than by reading. The recurring shape — a check that
     re-derives a value the way the program derived it and compares it to itself
     — accounted for six of them. The sharpest catch: BOTH_NOSEAL files an
     outcome descended from a SEALED bar while F-C4-SEAL printed a blanket "no
     outcome anywhere in this build", and leg 3 was structurally blind to it
     because the ablation table has no timestamp column — the F-C3-a class
     again, in a table a timestamp test can never reach. Now named, counted and
     bounded (manifest `seal_read`). Recommendation in F-C4-h: a standing
     convention that every fixture leg must name what would have to be true for
     it to FAIL.
PENDING (operator): 5 rulings, all in section 10 --
     F-C4-a  IS A MEAN BOUGHT WITH THE TAIL THE OBJECT THE ESTATE WANTS? If yes,
             the trail needs a rule that lets a runner run, which is a NEW card
             and a new probe, not a tune of this one
     F-C4-b  PIN THE TRAIL'S "BEYOND" in the card. 0.5 ATR (taken, re-pointed
             from the entry anchor's own word) vs 0.0 (the stop at the pivot).
             The pivot buffer, not the rail, set the stop on 14 of 21 advances
     F-C4-c  THE RATCHET RETIRES THE BELL: 11 of 11 scored campaigns exit on a
             stop, 126 of 127 on the display strip. Backstop, or dead law?
     F-C4-d  A MINIMUM ADVANCE INCREMENT, or ratify that any strict improvement
             counts. The smallest advance in the book is 0.002053 ATR and it is
             the one that was PAID OUT
     F-C4-e  IS HALVING THE RUNNER THE INTENT? The harvest's fills NET +1.7282 R
             and the amendment still costs -3.1814 R — the cost is the half that
             was not allowed to run
     -- also filed, not blocking: F-C4-f (not separable), F-C4-g (n = 11, two
     trades), F-C4-h (the fixture-hygiene pattern, three builds running),
     F-C4-i (the "new pivot" gate is on the CONFIRMATION bar — a reading that
     did not bind), F-C4-j (the harvest's "from below" precondition, now in the
     card, 0 of 153 campaigns affected), F-C4-k (the causality leg is sound and
     NOT falsifiable on this corridor's data), F-C4-l (the live paper line is
     now TWO card versions behind), F-C4-m (F-C3-a..e and F-C3-i carried).
PROBE LEDGER: m = 0. EXPLORATION — ungated; promotion requires registration.
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-16c ===
NOW: TIER-C5 IS MEASURED, THE BOX IS OPEN, AND NOTHING WAS SUPPORTED.
RULING, VERBATIM: "open the sealed box, we lose continuity otherwise… we will
     put it to paper trade the Prometheus route… another data stream" ·
     "D15 caveats not hard gates"
     THE YARDSTICK LINEAGE, ALL FOUR, STATED TOGETHER:
       v1  TIER-C2  1H anchor, no rail       -0.7762 R/trade  n=10   118 d SEALED
       v3  TIER-C3  4h anchor + 1.0 rail     +0.7056 R/trade  n=11   118 d SEALED
       v4  TIER-C4  + LPS-trail + harvest    +0.6907 R/trade  n=11   118 d SEALED
       v5  TIER-C5  + funding ceiling 1R     +0.1724 R/trade  n=195  2534 d OPEN
     THE 118-DAY NUMBER WAS NOT WRONG, IT WAS SMALL. Every R is post-2024-07-01:
     pre-wall -7.2687 over 123, post-wall +40.8836 over 72. The operator's own
     post-lockbox read is +1.1964 over 29 — PROVISIONAL, and the best slice in
     the book by a factor of seven.
     *** AND THE CARD ITSELF DOES NOT CLEAR THE ESTATE'S OWN BAR. *** Scored
     through the same asset-cluster ruler as the registrations, the card's
     expectancy CI is [-0.0271, +0.4336], one-sided p 0.0912. On seven years,
     five assets and 195 campaigns this card is not distinguishable from zero
     at q = 0.10. That is F-C5-b and it is the deepest ruling in the document.
     EVERYTHING IS IN-SAMPLE BY CONSTRUCTION. Out-of-sample transfers FORWARD to
     live paper on the Prometheus route (Stage-B interim), which is NOT BUILT.
SEAL: 13,860 formerly-sealed 4h bars readable. 41 campaigns quote an ANCHOR from
     one; 60 ADVANCES quote a RATCHET PIVOT from one, and on 24 campaigns that
     advance is the FINAL stop — the EXIT PRICE came out of the old lockbox. 42
     campaigns quote ANY formerly-sealed price. THE MASK IS PROVED LIVE, not
     merely constant-false: over Tier-C4's corridor the same code path yields 11
     campaigns box-open and 10 box-closed. F-C3-a IS CLOSED — the operator did
     not ratify the seal floor, they removed the seal.
REGISTRATIONS (text before result; ruler DECLARED before scoring — asset-cluster
     90% CI, MEAN; a BUILDER'S READING the operator should confirm):
       (reference) THE CARD v5    n=195  exp +0.1724  CI [-0.0271,+0.4336] NOT SUPPORTED
       P-SPR-1 standalone spring  n=241  exp +0.0882  CI [-0.0373,+0.2389] NOT SUPPORTED
       P-SPR-1 UNION vs CARD      n=420  d   -0.0520  CI [-0.2583,+0.0655] NOT SUPPORTED
       P-CASC-1 card+adds PAIRED  n=195  d   +0.1461  CI [-0.0100,+0.2532] NOT SUPPORTED
     THE UNION VERDICT WAS REVERSED IN REVIEW. The first draft named the arm
     "vs card" and scored it against ZERO; with 2.2x the card's campaigns a
     narrower interval passed while the union was per-campaign WORSE than the
     card (-0.0520 R). FDR: m = 3 (tests RUN, not registrations FILED), q = 0.10,
     bar 0.03333, CORRECTION APPLIED — the bootstrap yields the tail, so no p
     was invented. No arm clears it.
     LOAO: 1 of 5 on every arm, and in each case the panel that excludes zero is
     the one with ZEC DROPPED. ZEC is 84% of the card's book AND the asset whose
     removal flips every arm.
FLEET: 79 LOGGED CELLS (25 shadow across 8 pre-named grids + 54 eligible league
     cells a champion is argmaxed from), ALL REPORTED, NONE PROMOTED. D12 bound
     0 of 195 at unit size, 2 at 2x, 4 at 3x. S-TRAIL +0.25 ATR posts +69.20 vs
     the card's +33.61 and its D15 max-single-trade-delta-share is 1.1562 —
     GREATER THAN ONE: one campaign exceeds the whole net improvement.
LABS: H1 — the harvest is a DE-RISK, never a profit-take: 37 fills, both took
     (-9.1743) and would-have (-14.9127) NEGATIVE, delta +5.7383 R, positive in
     EVERY slice. H2/H7 — the champion wall is EMA 889 on BOTH 12h (62.7%) and
     1d (61.9%); the estate's own tide-slow EMA 316 is the WEAKEST wall on 12h
     at 23.9%. AE STUDY, the most stable number here: a winner goes 0.3105 R
     against you before it goes 1 R for you, and the census era agrees at
     0.3145 — four thousandths apart across two regimes.
REVIEW: seven adversarial lenses run BEFORE publication. 16 REPAIRS. Two changed
     a headline number (an EMA WARM-UP FLOOR the full-water corridor needed and
     no parent did — `ind.ema` SEEDS at the series start, so 23 pre-warm armings
     and 4 scored campaigns had ridden on EMAs that were all the same number;
     and S-SIZE re-capped because D12's 1R cap does not scale). One REVERSED A
     VERDICT. Five fixture legs that could not fail were replaced.
FIXTURES: 11/11 PASS. F-C4-h's convention is the HOUSE RULE from here — every
     leg states what would make it FAIL.
PENDING (operator): 8 rulings, all in section 8 —
     F-C5-a  WHICH NUMBER IS THE YARDSTICK? +0.6907 / +0.1724 / +1.1964, 7x apart
     F-C5-b  THE CARD DOES NOT CLEAR THE ESTATE'S OWN BAR on 195 campaigns.
             Edge that is hard to measure, or a coin that flipped heads?
     F-C5-c  ONE ASSET IS 84% OF THE BOOK and flips every LOAO. Same ruling F-C3-d awaits
     F-C5-d  D12 inert at unit size, live above it — keep as insurance or strike
     F-C5-e  THE BELL FIRES ONCE IN SEVEN YEARS — backstop or dead law
     F-C5-g  S-LIMIT's avg-AE is fitted on the book it is scored against
     F-C5-h  D1-D15 AND H1-H7 HAVE NO SOURCE. H3 and H6 have no content at all.
             Define them or strike the labels (precedent V-6)
     F-C5-i  THE SPRING'S TIDE READING refuses 3,526 sweeps and admits 241.
             Pin "the reclaim is the FIRST inside close" or open the window
     F-C5-k  *** THE LIVE PAPER LINE IS THREE CARD VERSIONS BEHIND AND THE
             RULING JUST MADE IT THE OUT-OF-SAMPLE INSTRUMENT. This moves from
             housekeeping to BLOCKING. ***
     -- also filed: F-C5-f (the fleet's best cell fails its own D15 column),
     F-C5-j (Tier-C4's Trade docstring is falsified by the open seal),
     F-C5-l (F-C3-b/c/e, F-C4-b/i carried).
PROBE LEDGER: card m = 0. LOGGED SELECTION SURFACE 79, written BEFORE the look.
     EXPLORATION — ungated; promotion requires registration and declares its m.
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-16d ===
NOW: SESSION CLOSE. Four stages: TIER-C4 (the mean card), the interview replies
     enacted (seal OPEN, D12, D13(c), D15 DEMOTED to diagnostic), TIER-C5
     (full water), TIER-C5-Q (the queryable book + this report).
THE ARC IN ONE LINE: a card that looked like +0.6907 R/trade over one sealed
     quarter returns +0.1724 over seven open years, CANNOT BE DISTINGUISHED
     FROM ZERO at the estate's own bar (CI [-0.0271,+0.4336], p 0.0912), rests
     84% on ZEC — and is now the first card in this estate that can be
     cross-examined trade by trade without a rebuild. The measurement got worse
     and the instrumentation got much better, and those are the same event.
TC5-Q IS LIVE: 436 campaigns indexed (195 card + 241 spring, 60 add-carrying),
     3,677 instants demanded and 3,677 covered, ZERO missing; tape_full 13,861
     rows = every arming/trigger/sweep/add/advance/harvest/exit PLUS the three
     kinds the commission did not name and a queryable book needs anyway —
     anchor_bar, pivot_bar, retrace, the bars PUBLISHED PRICES are quoted from —
     PLUS a DAILY 00:00Z spine over 6.938 years (the ruling asked for >=3).
     Families: AVWAP set, RVWAP +-1s/+-2s, period extremes, and the league
     champions each on its OWN clock (1h EMA4618, 4h EMA3618, 12h & 1d EMA889),
     each NULL until its EMA has seen its own length — warm on 92.0 / 74.4 /
     81.4 / 61.9 % of rows, FILED.
     `python scripts/query_trade.py <campaign_id>` — median 195 ms, worst 209,
     budget 2,000, 9.6x headroom. It COMPUTES NOTHING; that is why it is fast.
     8/8 fixtures. F-Q-0 asserts all 21 TC5 tables unchanged — the manifest
     against its git blob AND every parquet re-hashed FROM DISK against both
     the committed manifest and the independent re-run. NO SCORED NUMBER MOVED.
*** THE QUERYABLE BOOK IS THE NEW FLOOR FOR REGISTRATION WORDING. *** A
     registration whose predicate cannot be evaluated against campaigns,
     instants and tape_full is one nobody can score without a rebuild. This
     estate has already lost registrations to definitions the contract never
     carried (H-VBT, leap/stair arrival). From here, wording a claim means
     naming the columns it will be scored on.
REVIEWS: THREE adversarial reviews run BEFORE publication (6 lenses on TC4,
     7 on TC5, 5 on TC5-Q). 33 NUMBERED repairs across the session (TC4 12 +
     2 unnumbered, TC5 16, TC5-Q 5). TWO of the TC5-Q five were mine to see
     and I did not: THE CHAMPION EMAs HAD NO WARM-UP FLOOR — verbatim TC5's
     own repair #4, which I fixed in the decision path and then reintroduced
     with EMAs 3-15x longer. ONE VERDICT
     REVERSED (P-SPR-1's union arm was named "vs card" and scored against
     ZERO). TWO HEADLINE NUMBERS CHANGED (an EMA warm-up floor the full-water
     corridor needed and no parent did; S-SIZE re-capped because D12's 1R cap
     does not scale). SIX of sixteen TC5 repairs were ONE defect wearing
     different clothes: a check that re-derives a value the way the program
     derived it and compares it to itself.
FIXTURE CONVENTION ADOPTED AS HOUSE RULE: every leg states inline what would
     have to be true for it to FAIL. It is what exposed that three F-C5-OPEN
     legs had no answer.
PENDING (operator) — the register, TOP first:
  TOP  THE UNIVERSE QUESTION. ZEC is 84% of the book AND the asset whose
       removal flips every registration arm. LEAN: keep the five-asset panel
       AND make "excludes zero on >=3 of 5 leave-one-out panels" part of the
       REGISTERED TEXT rather than a caveat beside it. It would have failed all
       three arms this session, which is the point. Gates every future
       registration
  F-C5-b  THE CARD DOES NOT CLEAR THE ESTATE'S OWN BAR on 195 campaigns over
       seven years. Edge that is hard to measure, or a coin that flipped heads?
  F-C5-k  BLOCKING — the live paper line is THREE card versions behind and the
       seal-open ruling just made it the OUT-OF-SAMPLE INSTRUMENT
  F-C5-a  which number is the yardstick: +0.6907 / +0.1724 / +1.1964, 7x apart
  F-C4-b  LEAN: RATIFY 0.5 ATR as the trail's "beyond" — the card's own word
       for it at the entry anchor; the 0.0 reading parks a stop on a liquidity
       magnet. Buffer-bound on 14 of 21 TC4 advances
  F-C4-c  LEAN: KEEP THE BELL AS A BACKSTOP, do not strike. It fires once in
       seven years because the trail is faster, not because it is wrong
  F-C4-d  LEAN: ADOPT A MINIMUM ADVANCE INCREMENT in principle; the operator
       pins the number, and NOT from this book's outcomes (the smallest advance
       was 0.002053 ATR and it was the one paid out)
  H3, H6  NO DEFINITION ANYWHERE. Define, or strike the labels (precedent V-6)
  -- H1 ANSWERED (harvest = de-risk, +5.7383 R, positive in every slice);
     H2/H7 ANSWERED (champion wall EMA 889 on both slow clocks; EMA 316 the
     WEAKEST wall on 12h); H4/H5 MEASURED not answered, awaiting F-C4-b/d.
  -- also open: F-C5-c, F-C5-d, F-C5-g, F-C5-h, F-C5-i, F-C5-j, F-C3-b/c/e,
     F-C4-i. CLOSED this session: F-C3-a, by ruling.
PROBE LEDGER: card m = 0. TC5's logged selection surface 79, written BEFORE the
     look. TC5-Q registers nothing and scores nothing. EXPLORATION — ungated;
     promotion requires registration and declares its m first.
=== END STATUS ===

=== STATUS_APOLLO — 2026-08-16e ===
LANE      APOLLO · branch v12-v1-census · seed 20260816
CLASS     REPAIR — the sixth adversarial review, applied. No scored number moved.

  A sixth review ran over the FINISHED TIER-C5-Q and confirmed eight findings.
  Four were repairs already applied while it worked. FOUR WERE LIVE, and one
  was a blocker.

  Q-6  BLOCKER · THE COMPLETENESS CONTRACT WAS HALF A CONTRACT.
       F-Q-1's leg asks whether every `_ms` field maps to a kind the ledger
       CARRIES — satisfied by ONE row of a kind. The reviewer kept every
       arming/trigger/exit row and exactly one each of the other seven kinds
       (1,315 rows instead of 3,677; 1,483 real book bars with no snapshot)
       and the whole fixture file returned 8/8 PASS: coverage read 0 missing
       because it is seeded from the frame it checks, and the per-kind rows
       read 1 · 1 · 0 with an [OK] beside each.
       FIX: a CARDINALITY contract — every kind's count re-derived from the
       campaigns table and the three ledgers, never from the instants frame,
       with dedup honoured as DISTINCT (campaign_id, ts) pairs. Replayed
       against the same sabotage it now FAILS seven kinds and the total.
       The dedup itself is now disclosed in the manifest (collapsed 0 of 3,677).

  Q-7  slice_provisional was the CARD lane's year count stamped on SPRING
       rows — 68 campaigns (33 in 2023, 35 in 2024) wearing another lane's
       thinness verdict. Now lane-scoped, with slice_n filed beside the flag.

  Q-8  `--day` filtered on arm/entry/exit only: 314 days carrying 384
       advances, 36 harvests and 18 adds printed "(nothing)" under a header
       reading THE BOOK ON <day>. On 149 (campaign, day) pairs the day was
       not even empty and the moving campaign was simply absent from an
       unqualified table. The filter is now the instant ledger.

  Q-9  THE SEAL VERDICT — a two-flag test carrying the sentence "Tier-C2, C3
       and C4 could have taken it unchanged", FALSE on 332 of the 343 screens
       that printed it (190 of them SPRING, a lane P-SPR-1 registers GENUINELY
       NEW). It also missed campaigns whose ENTRY and HARVEST prices are
       quoted inside the span while the anchor sits outside — SOL 2024-07-07
       paid out on two formerly-sealed closes and printed "quotes no price
       from the old lockbox".
       FIX: `sealed_instants` counts every bar of the campaign's own life in
       the span, off the FULL ledger, against a window READ FROM RC.LOCKBOX_WAS
       rather than a hard-coded copy; `in_tc4_book` is a MEMBERSHIP test
       against C4's filed journal, finding 11/11 of its rows. 96 campaigns
       quote a formerly-sealed price. The test moved OUT of query_trade.py,
       whose stated property is that it computes nothing.

  NEW FIXTURE  F-Q-7 · THE RENDERED CLAIM. F-Q-0..F-Q-6 check what the tool
       COMPUTES; not one read a sentence it PRINTS, and all three tool defects
       lived in that gap. F-Q-7 checks the assertions against the source, the
       named counterexamples by name. Its own first draft forgot the adds
       ledger and disagreed with the filed column on exactly the 19
       add-carrying campaigns — the filed number was right and the check was
       short.

  THE PATTERN, NAMED  Both surviving defects are A CHECK SATISFIED BY ONE
       EXAMPLE — one row of a kind, one flag out of six bars. Sibling to the
       circularity defect: the first compares a thing to itself, the second
       asks "does this exist" when the question was "how many".

  INTEGRITY
    exactly one file moved: campaigns.parquet f946fb5774e8 -> 8680fe93624c.
    instants / advances / harvests / adds / tape_full / coverage re-wrote
    BYTE-IDENTICAL. F-Q-0 still asserts all 21 TC5 tables unchanged against
    the manifest committed at HEAD.
    TC5-Q 9/9 · TC5 11/11 · estate suite 334 passed, 1 skipped, exit 0.
    query latency 33 ms against a 2,000 ms budget.

  SESSION TOTAL  37 numbered repairs across FOUR pre-publication reviews
    (TC4 12 + 2 unnumbered · TC5 16 · TC5-Q 5 + 4).
=== END ===

=== STATUS_APOLLO — 2026-08-16f ===
LANE      APOLLO · branch v12-v1-census · seed 20260816
CLASS     BUILD — TIER-C6 rev B. Measurement + registrations + pre-named labs.
          D15 columns everywhere, gates nowhere. Every grid reported whole.

  THE CARD GOT BETTER AND STILL CANNOT CLEAR ITS OWN BAR.
    card v6 = v5 + trail ARMS AFTER +1R [H5] + MINIMUM ADVANCE 0.05 ATR [F-C4-d].
    195 campaigns, 2,534 days: net +39.8443 R, expectancy +0.2043 (v5 +0.1724).
    Through the estate's own asset-cluster ruler: CI [-0.0132, +0.5085],
    p = 0.0740. Closer to the bar than v5 and on the same side of it.
    F-C5-b SURVIVES INTO v6.

  BOTH REGISTRATIONS REFUSED.
    P-TRAIL-1 [65%]  paired dExp +0.0319  CI [-0.0050, +0.0688]  p 0.0817
    P-WALL-1  [55%]  paired dExp -0.0331  CI [-0.0859, +0.0278]  p 0.8318
    m = 2 tests actually run, q = 0.10, bar 0.05. Neither clears BH.
    Both arms PAIRED — TC5 shipped an arm named "vs card" scored against ZERO
    and the review reversed it; that does not happen here.
    P-WALL-1 loses BY CUTTING THE TAIL (tail_exit_ratio 0.9329). 16 wall exits.

  THE WHY-ZEC ANSWER, IN ONE PARAGRAPH.
    None of the five named hypotheses explains ZEC, and the thing that does is
    one trade. Of 27 EXPLANATORY metrics (8 outcome metrics segregated by
    construction) ZEC is INTERIOR to the other four on 18, DEGENERATE on 3,
    EXTERIOR on 6 — of which 3 fail the materiality floor, 1 separates the
    WRONG WAY (shortest tide streak of the five, most regime flips), leaving 2
    that clear every gate and are economically nil. ZEC books +32.5680 R of
    +39.8443 (81.7%) — and +25.0605 R of THAT, 76.95% of ZEC's net, is a
    SINGLE campaign, 2026-05-01 -> 2026-05-10, 58 bars, 7 advances, 1.63x.
    Strip it: +7.5075 R. Strip 2026: expectancy +0.2531, SECOND of five.
    The question presupposes a distribution that does not exist.

  THE LIMIT FRONTIER — k* = 0.40 ATR, AND THE PRE-REGISTRATION KILLS IT.
    E[R] 0.2056 offered / 0.2344 filled-only against a card at 0.20433. The
    form was written before the look with three falsification clauses; clause
    (c) fires on its own winner — k*'s max_single_trade_delta_share = 41.4008.
    And the limit MISSES THE TRADES THAT PAY: missed-would-have expectancy
    +3.4042 R at k=0.10, 48.69 R forgone at k=0.40 against a 39.84 R book.
    The SPLIT arm is an exact convex combination, so k*(SPLIT) == k*(FULL) and
    prereg clause (b) is UNFALSIFIABLE by construction; effective argmax
    surface is 5 cells, not the declared 10.
    SAIL IS UNBOUND — zero grep hits estate-wide. BLOCKING for clause (c).

  STAGE W — THE LEAGUE GREW A SUPPORT SIDE.
    resistance 12h EMA 889 @ 62.71% · SUPPORT 12h EMA 300 @ 54.55%.
    Support is the WEAKER wall and its champion is a third the length. Every
    prior tier scored shorts against the wall BEHIND them.
    The resistance side reproduces TC5's filed league 313/313, zero differences
    on approaches, rejections, champion flags AND penetration.

  L-SPR-NT — THE ESTATE'S OWN 3,526 IS DEFECTIVE FOUR WAYS.
    admitted 363 SIGNALS (not 241 campaigns) · refused 3,470 (floored; the
    filed 3,526 counts 56 refusals inside the first 316 warm-up bars) ·
    unreclaimed 1,374 (counted nowhere before) · partition closes at 5,207 ·
    episode-collapsed refusals 2,916 (no non-overlap guard).

  ALSO FILED  DEFINITIONS_D_H_2026-08-16.md — every D1-D15 and H1-H7 mapped.
    11 of 15 D-items and 2 of 7 H-items have NO SOURCE OF ANY KIND. D1-D10's
    apparent hits belong to FOUR OTHER CONTRACTS' namespaces. H3 (=50%) and H6
    (=the pins + their comparison grids) are DEFINED THIS TURN by operator
    ruling. Recommended: strike D1-D11, D13(a-b), D14; keep D12/D13(c)/D15
    citing code; keep H1-H7 citing the TC5 relay table. F-C5-h ANSWERED.

  THE REVIEW, AND THE BLOCKER IT FOUND.
    Eight lenses, 55 agents, run BEFORE publication. Seven repairs applied.
    C6-1 BLOCKER: F-C6-LEAGUE's "mirror proof" NEVER CALLED league(). It ran a
      private copy of the predicate, which was an exact algebraic identity
      (ATR invariant, EMA equivariant under negation) and passed all 20 swept
      constant combinations including APPROACH_ATR=0.0. No fixture leg ever
      executed the support branch. The reviewer mutated it, rebuilt, and got
      10/10 PASS while the 12h support champion moved 300 -> 89 and the wall
      book went 16 exits -> 4. REPAIRED to call T6.league on a negated tape;
      sabotage-tested after the repair -> 307 mismatches, all 4 champions move.
    C6-2 mean_penetration_atr SILENTLY REDEFINED under a reproduction claim —
      290 of 313 rows differed. Parent's definition restored; the broke-only
      depth published under its own name.
    C6-3 P-TRAIL-1's D15 was d15(v6, v6), a self-comparison. Now measured
      against the v5 control; max_single_trade_delta_share = 0.4892 — UNDER
      ONE, the only effect in this build not dominated by a single campaign.
    C6-4 top_decile_share_pct carried two denominators under one name.
    C6-5 wall_touch accepted `direction` and never read it. Removed.
    C6-6 F-C6-GRID passed unconditionally on grids that built no cards —
      4 of 12 grids, 16 of 41 declared cells unchecked.
    C6-7 F-KEY named 9 tables while the build filed 27. Now TOTAL, read from
      the manifest: 27 keys covering 27 parquets.
    NO SCORED NUMBER MOVED — every repair was a fixture, a column definition
    or a diagnostic's base.

  THE REVIEW DID NOT FINISH. 31 of 55 verifiers hit the session usage limit.
    39 findings raised and NEVER ADJUDICATED, several corroborated across
    three or four independent lenses. Carried as F-C6-k. A review that stopped
    early is not a review that passed, and 11/11 fixtures does not stand in
    for it. RULING NEEDED: re-run the verifier pass before TIER-C7.

  INTEGRITY  27 tables · 11/11 fixtures · suite 334 passed, 1 skipped, exit 0.
    F-C6-CTRL: the v5 card through v6's FORKED code reproduces TC5's FILED
    journal, WORST ABSOLUTE DIFF 0.0 across 13 columns and every exit_reason.
    F-C6-DET: two runs, 27 tables, 0 sha moved, 0 parquet files differ.

  OPEN, AND THE TOP TWO NEED A WORD.
    F-C6-b  DOES A CARD WHOSE RESULT IS ONE CAMPAIGN ON ONE ASSET CONSTITUTE
            AN EDGE? Lean: keep the panel, and make "≥3 of 5 leave-one-out
            panels exclude zero" part of the REGISTERED TEXT. It would have
            failed every arm this session, which is the point.
    F-C6-c  SAIL UNBOUND — blocking for the limit form's validation clause.
    also open: F-C6-a (card vs its own bar), F-C6-d (unfalsifiable prereg
    clause), F-C6-e (top-decile share > 100% under EAR), F-C6-f (L-FMH cannot
    run on the card book), F-C6-g (in-sample argmax as a decision input),
    F-C6-h (TWO ATTACHED DOCUMENTS DID NOT ARRIVE — the only incomplete
    deliverable), F-C6-i, F-C6-j, F-C6-k.
=== END ===

=== STATUS_APOLLO — 2026-08-17a ===
LANE      APOLLO · branch v12-v1-census · seed 20260817
CLASS     TC6-V PHASE A — audit completion. NO NEW CLAIMS.
          PHASE B (TIER-C7) NOT RUN — CP-A fired.

  CP-A IS RED, BY THE COMMISSION'S OWN GATE.
    All 39 outstanding TIER-C6 findings adjudicated by 13 agents, each
    required to RUN the scenario before returning a class:
      CONFIRMED-FIXED           12   (the C6-1..C6-7 repairs, each re-proved)
      COSMETIC                  16
      REFUTED                    7
      CONFIRMED-DATA-AFFECTING   4   <- the gate
    Two of the four changed sentences already published in
    BUILD_2026-08-16_TIERC6_REVB.md. One of them was a SIGN.

  THE FOUR, REPAIRED AND RESTATED.
    #11 L-FMH's counterfactual booked an exit at the CLOSE of bars on which
        the STOP had already been taken — 173 impossible exits. Adverse-first
        says the stop fills intrabar and the campaign is already out. Search
        now stops one bar short of a stop exit.
        v5-control A3 sum-delta -3.1944 -> +1.2276. THE SIGN REVERSES, and
        the published sentence "every arm's Sigma delta is negative" IS
        WITHDRAWN.
    #12 the wall-aware S-BUF cell read UNFLOORED, SEEDED ribbon EMAs — this
        estate's THIRD repair of that defect. Floored at the family's LONGEST
        member (a band is not defined while only some members are warm).
        cell net R +38.6177 -> +39.4020.
    #33 mean_breakthrough_depth_atr was pooled on ALL approaches when it is a
        mean over the approaches that BROKE THROUGH. Repooled on break counts.
        12h/889 depth (the row P-WALL-1 reads) 1.139996 -> 1.177652.
    #25 the hazard curve's "None on 105 of 195" was the CONTROL book's count;
        v6's is 94. Corrected, and the censoring disclosed (below).

  THREE FINDINGS NOBODY HAD RAISED.
    THE CORRIDOR MOVES. Identical code one day later: 2,534 -> 2,535 days,
      195 -> 196 campaigns (ZEC opened 2026-08-17T04:00Z, still open,
      -0.0624 R). Every TIER-C6 headline is as-of its corridor and silently
      is not as-of any other. Corridor pin added for audit re-runs;
      F-C6-CTRL made PREFIX-ROBUST — proves all 195 parent campaigns present
      and identical, REPORTS the extras instead of failing on growth.
    THE OFFLINE CACHE IS NOT IMMUTABLE. Pinned to TC5's exact corridor end
      the league still sees +1 approach on 30 of 313 rows — boundary bars
      that arrived after TC5 filed. NO FIXTURE IN THIS ESTATE HAD EVER SAID
      a filed parquet is not bit-reproducible after a refresh. Two magnitude
      bounds were tried and both were guesses that failed; rather than tune a
      constant until the suite went green, the leg asserts only what is
      defensible (no champion moves, no count shrinks) and PRINTS the rest.
    THE AE DISTRIBUTION IS CENSORED AT THE CARD'S OWN RAIL. mae_held_r
      bottoms at EXACTLY -1.0000 R with 110 of 196 campaigns (56%) on it;
      the uncensored tape reaches -4.5891 R and 124 campaigns gap through
      their stop. Any decile or hazard statistic on held excursions reports
      the STOP in its tail. P-AE-1's 0.60R threshold was pre-named from that
      curve — which is why this reaches into Phase B.

  A2 APPLIED.
    F-C6-j  m DERIVED from the non-null p-values the table publishes (8 -> 12)
            and the BH bar APPLIED per row at q/m = 0.00833, not just recorded.
    F-C6-e  the over-100% column RENAMED AND RECOMPUTED on POSITIVE MASS,
            bounded [0,100] and comparable across aggregations; the old column
            NULLED on EAR rows with the reason on the row.

  A3 RIDERS, ALL BUILT.
    THE SUPPLEMENT  196 campaigns, 67 winners, net +39.7819 R. MAE x MFE
      cross-tab in net R and count; cuts by exit mechanism / asset / year /
      direction; WINNERS AND LOSERS SEPARATELY. Every excursion printed
      TWICE (held and tape). SUPPLEMENT.html 29.6 KB + parquet.
    L-LAG  arm->trigger in bars and ATR-time, by year/asset/direction and BY
      LAG DECILE with outcome. 49 of 196 campaigns trigger on the arming bar
      itself, so decile 0 is EMPTY under average-rank and the gate had to be
      cut by value. lag-0 expectancy +0.4149 (win 46.9%) vs the 56-bar decile
      -0.5796.
    query_filter v1  predicate DSL over a NAMED feature table; unknown column
      RAISES; every emitted table carries the D15 trio and is labelled "a
      SELECTION, not a result"; every invocation logs its m to a probe ledger
      (m = 3 this build).

  P-LAG-1'S CONDITION ADJUDICATED ITSELF — AND AGAINST THE INTERESTING ANSWER.
    bottom (lag <= 0 bars, n=49) +0.4149 vs top (lag >= 71, n=20) +0.3534,
    delta +0.0616, CI [-0.7819, +0.9566]. DOES NOT EXCLUDE ZERO.
    P-LAG-1 REPORT-ONLY, NOT REGISTERED, m UNCHANGED.

  PHASE B NOT STARTED. No scripts/tierc7.py, no registration text, no arm
    scored. There is no half-built claim anywhere in the estate.

  INTEGRITY  TIER-C6 fixtures 11/11 PASS after every repair. Suite 334
    passed, 1 skipped, exit 0. F-C6-CTRL worst absolute diff 0.000e+00 across
    13 columns on all 195 shared campaigns.

  RULINGS NEEDED BEFORE TIER-C7.
    TC6V-a  does a build document state its corridor as a WARRANTY (numbers
            valid only as-of), or does the estate re-run and restate on a
            cadence?
    TC6V-b  freeze a cache snapshot per build, or accept and document
            boundary drift?
    TC6V-c  P-AE-1: re-name the threshold from the UNCENSORED tape
            distribution, keep it and score it as a CARD-CONDITIONAL rule, or
            drop the arm?
    TC6V-d  do the 16 COSMETIC findings get fixed before TIER-C7? None moves
            a number; all weaken a check.

  RESUME WORD  "TC7 GO" — with a ruling on TC6V-c, since P-AE-1 cannot be
    pre-named from a curve whose censoring is now on the record.
=== END ===

=== STATUS_APOLLO — 2026-08-17b ===
LANE      APOLLO · branch v12-v1-census · seed 20260817
CLASS     TIER-C7 — the hybrid R&H program. Measurement + FOUR registrations.
          Resume word "TC7 GO" given; P-AE-1 ruled CARD-CONDITIONAL, arm kept.

  NOTHING CLEARED — AND TWO ARMS CLEARED UNTIL THE REVIEW REVERSED THEM.
    P-HYB-1   [50%] two-sample +0.1128  CI [-0.0193, +0.2401]  p 0.0862  NOT SUPPORTED  LOAO 1/5
    P-CHAIN-1 [50%] two-sample +0.1125  CI [-0.0198, +0.2400]  p 0.0862  NOT SUPPORTED  LOAO 1/5
    P-WEV-1   [45%] paired     -0.0027  CI [-0.0084, +0.0029]  p 0.7521  NOT SUPPORTED  LOAO 0/5
    P-AE-1    [40%] paired     +0.0044  CI [-0.0979, +0.1017]  p 0.4379  NOT SUPPORTED  LOAO 1/5
    (reference) card v6 vs zero +0.2030 CI [-0.0132, +0.5022]  p 0.0740  NOT SUPPORTED
    F-C5-b SURVIVES INTO A THIRD TIER.

  THE BLOCKER: A PAIRED RULER ON ARMS THAT CHANGE THE CAMPAIGN SET.
    P-HYB-1 and P-CHAIN-1 were SUPPORTED on the paired delta (+0.2406/+0.2403,
    CI [+0.115,+0.372], p 0.00025, BH cleared, LOAO 5/5). The paired ruler is
    legitimate only for an arm that rides INSIDE the campaign set — TC5's own
    law. A chain holds its asset's slot until its last leg exits, so 7 control
    campaigns worth +25.58 R never open, and the bias is DIRECTIONAL: when a
    re-entry captures the very move the control booked as a SEPARATE campaign,
    the arm is credited inside the surviving twin while the control's campaign
    is deleted from the comparison and never debited.
    ZEC 2026-04-23 -> 2026-05-10: control two campaigns +25.5692 R, hybrid one
    chain +25.3148 R — the hybrid is 0.2544 R WORSE and the paired ruler
    credits it +24.8061 R = 54.6% OF THE ENTIRE PAIRED DELTA. Across all 7
    blocked slots: paired credits +29.3562 R where the account earned +3.7723.
    Re-scored on cluster_boot_diff — the F-C5-n repair, a function this module
    IMPORTED AND CALLED ZERO TIMES — both arms fail and LOAO inverts 5/5 -> 1/5
    with the only clearing panel being -ZECUSDT. On the whole book the hybrid
    is 6.82 R WORSE on ZEC. Both rulers now print on every row.

  THE SECOND BLOCKER: THE FIXTURE GUARDING THE LARGEST REPAIR WAS ALGEBRA.
    F-C7-CHAIN computed the leg size IN THE FIXTURE and asserted an identity in
    its own variables. It passed at 2.22e-16 and WOULD HAVE PASSED WITH THE
    SIZING DELETED. It now reads the sizes _account_chain actually used,
    asserts them on all 79 chains, and proves the rule load-bearing (79/79 legs
    carry a size != 1.0). Written by the same hand that wrote the preamble
    banning self-comparison.

  THE SIZING REPAIR ITSELF, FOUND BY DISBELIEVING A GOOD NUMBER.
    D-R6 makes a chain one campaign, which fixes the denominator but not the
    SIZE. One unit per leg let SOL 2023-10-16 re-enter at own-R 1.5264 against
    a chain R of 0.4391 — 3.5x the risk — booking +40.74 R for a move worth
    +11.72 R. That campaign was 75% of the arm's delta. Leg 2 is now sized
    chain_R/own_R; the campaign books +12.24 R, the arm falls +68.17 -> +59.62,
    concentration 0.7473 -> 0.5462.

  THE WEAVE IS NOT THE MECHANISM [D-R3/D-R4].
    weave-only -0.5198 R paired. RE-ENTRY ONLY +38.1513 of the +45.4175 that
    weave+re-entry earns. 67 of 79 re-entries follow a plain LADDER-OUT, 12 a
    weave. The commissioned ladder could not separate them — the only cell with
    a re-entry also had the weave — so one unscored rung was added.
    L-WEAVE says why: 1 of 42 weave events fires in profit against a base rate
    of 79.47% of open bars in profit — a 33.4x skew, mean unit move at an event
    bar -0.5630 R. THE WEAVE IS A LOSS-SIDE DETECTOR, NOT PROFIT PROTECTION,
    and the commission's premise is very nearly an empty set.

  ALSO REPAIRED  the journal's cross-leg columns: mfe_r published 57.31 R of
    excursion no position had (now 33.24); stop_advanced_atr/ratchet_exit
    spliced leg 2's stop onto leg 1's anchor (8 negative advances -> 0, 26
    mis-filed ratchet exits -> 37 correct); 14 chains that harvested were filed
    harvested=False. And T7.loao counted panels excluding zero in EITHER
    direction, so S-STOPGRID's +0.25/+0.50 cells read 5/5 while being reliably
    WORSE — the halves are split and the 3/5 line is taken above only.

  NEW FIXTURE  F-C7-LABS. _labs() swallowed ImportError and a full run
    completed GREEN with THREE OF FOUR LABS ABSENT. A missing lab now fails.

  INTEGRITY  11/11 fixtures · suite 334 passed, 1 skipped, exit 0 · 16 tables.
    F-C7-CTRL: v7 with every knob at default reproduces card v6, WORST
    ABSOLUTE DIFF 0.000e+00 across 13 columns and every exit_reason.

  PROCESS FINDING — AN AGENT MUTATED THE REPO DURING THE REVIEW.
    A sabotage patch (`return pd.DataFrame()`) was left at the top of
    regime_table after a lens tested whether the fixtures catch a silently
    empty commissioned table. THEY DO — F-KEY's totality leg failed on the
    stale parquet with no declared key. Patch removed, tree re-verified, the
    decision path confirmed intact. RULING NEEDED: future reviewers must run
    against a READ-ONLY worktree; a review that edits what it reviews can
    invalidate its own result.

  OPEN  TC7-a..TC7-j (10 findings, listed in the build doc §B5), plus the
    TC6-V set: TC6V-a corridor-as-warranty, TC6V-b cache immutability,
    TC6V-d the 16 cosmetic findings. TC6V-c is CLOSED by the operator's
    card-conditional ruling.

  THE PAUSE POINT, DECLARED. Analysis next, then engine definition, then the
    live-agent discussion. The estate has now run seven tiers and NOTHING has
    cleared its own bar. That is the finding the analysis should start from.
=== END ===
