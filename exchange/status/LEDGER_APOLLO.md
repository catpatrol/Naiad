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
