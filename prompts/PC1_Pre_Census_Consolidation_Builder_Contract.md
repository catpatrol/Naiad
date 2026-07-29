# PC-1 — Pre-Census Consolidation — Builder Contract

**Phase:** v12 Study · **Mixed tier, staged** — Stage 1 read-only diagnostics · Stage 2 record (ledger + provenance commits) · Stage 3 estate remediation (destructive + engine-touching, operator-authorised) · Stage 4 Tier-A journal arithmetic. **One contract, one go-paste, four staged blocks with halt gates.**
**Basis:** operator rulings 2026-07-29 (all tiers of the pending-decision list); ENGINE↔BRIEF handoffs of 2026-07-27/28; CENSUS-1b completion (ratified PASS, `98fe613`).
**Why this phase exists:** the project is about to redefine Secret Sauce and then run a census against that definition. Before either, the decks must be clear: three unverified integrity claims are outstanding, the estate carries known contamination, the ledger asserts one thing the engine ingestion proved wrong, and two free journal tests are queued that inform work already scheduled. PC-1 closes all of it in one builder session.
**What PC-1 is not:** it is **not** the census, it is **not** the Secret Sauce definition, and it changes **no trading rule**. The only engine edit is a single data-admission constant, explicitly authorised (§3.3).

---

## 0. Operator instructions — plain language

You paste **one** block (§10) into your **local** Claude Code. The builder then works through four stages by itself, stopping only if something is wrong or a genuine decision is needed. You do not need to babysit it or take screenshots — every stage writes a machine-readable report into `_reviewer_box/pc1/`, and you drag those files to me at the end.

What the four stages do, in order:

1. **Look and report** (changes nothing). Answers three open questions: is a correction entry I referenced actually in the ledger? Are there really two as-of defects in the census builder? Does a timestamp discrepancy in the record need fixing? Also checks whether the `analytics/` package has landed.
2. **Write the record** (reversible until pushed). Appends the ledger entries I drafted — four corrections, your rulings from this session, and one new standing rule — then commits Report 7 and the Atlas for provenance.
3. **Fix the LIT data** (destructive, you authorised it). Deletes six contaminated files, raises the engine's data floor to the correct date, re-downloads, verifies, and bumps the engine version. **The order matters** — reversing two steps makes every LIT load fail.
4. **Two free measurements** (changes nothing). Runs the two journal tests you ratified.

**It halts and asks you** only in the four situations listed in §3.0. Otherwise it runs to completion and hands back a report.

---

## 1. What this phase is

Five jobs, one session:

1. **Close three open integrity questions** — the D8 correction's presence in the ledger, the asserted as-of defects in `scripts/census_build.py`, and the manifest-mtime discrepancy against the ledger's "Chain:" sentence.
2. **Correct the record** — four substantive corrections the engine ingestion produced, the most important of which is that a *ratified graduation basis* is currently half un-representable in the engine.
3. **Preserve the reasoning** — commit Report 7 and Cascade Atlas v2, the documents that justify the next census's design.
4. **Remediate the estate** — purge the LIT synthetic padding, retire the two-floor design, and find the mechanism so it cannot silently recur.
5. **Run two free tests** — the LPS-qualified split and the tested-vs-untested stop-anchor split, both pure journal arithmetic, both feeding TC-2 and the ratcheting-structural follow-up.

## 2. What this phase is NOT

Not the census (CENSUS-1c and CENSUS-2a/2b are separate and come after the Secret Sauce definition) · not a rule change (no trading logic is touched; the sole engine edit is `LIT_FLOOR_MS`, a data-admission constant) · not new evidence spend (Stage 4 reads journals already produced on exploration-classic; the lockbox is not opened, not sampled, not "checked") · not a re-run of any phase (no substrate is rebuilt) · not a place to fix the as-of defects if found (Stage 1 **characterises** them; remediation is scoped separately once we know what they are) · not authorised to delete anything beyond the six named LIT files.

## 3. Construction

### 3.0 Halt gates — the only four times the builder stops

| Gate | Condition | Action |
|---|---|---|
| **H1** | Environment assertion fails (§3.1) | Halt immediately. **Write nothing.** Exit 2. |
| **H2** | Stage 1 finds an as-of defect that touches any **published** CENSUS-1 or CENSUS-1b number | Halt **before Stage 2**. The ledger batch needs a correction entry only the reviewer can draft. |
| **H3** | LIT pre-flight (§3.3 step 1) does not match the documented state | Halt **before any deletion**. Report the actual state. |
| **H4** | Any fixture MISMATCH (§5) | Halt at that point, report, produce nothing downstream in that stage. |
| **H5** | Re-backfill fails or returns fewer bars than the pre-flight expectation | Halt after purge. **Recoverable** — LIT data is re-downloadable; report and await instruction. |

Outside these four, the builder proceeds autonomously through all four stages.

### 3.1 Stage 1 — read-only diagnostics

**Environment assertion first, before anything else, including reads.** Assert: working directory resolves to the local working clone (a `C:\Users\…OneDrive…` / `/c/Users/…OneDrive…` path), `git rev-parse HEAD` succeeds, and `engine/`, `research_outputs/`, `LEDGER.md` all exist. On failure: exit 2, write nothing. *(Rationale: a misrouted read-only paste silently succeeds and returns plausible nonsense — this is the documented failure mode from 2026-07-26/27.)*

Then, writing only to `_reviewer_box/pc1/stage1_diagnostics.json`:

- **D1 — D8 correction presence.** `grep -n "0.98" LEDGER.md` and `grep -n -i "CORRECTION" LEDGER.md`. Report whether a ledger entry exists recomputing the D8 cascade ratios (the entry naming 0.98–1.33, the 1h 1.19 / 4h 1.33 rungs). Report its line number, or state ABSENT. **Why this matters:** the pushed CENSUS-1b completion entry references that correction as having happened; if it is absent, origin carries a dangling reference and the superseded 0.98–1.01 figure.
- **D2 — as-of defect characterisation.** The ENGINE→BRIEF handoff (2026-07-28, §5) asserts *two verified as-of defects of the "decision-instant vs anchor-instant" class* exist in `scripts/census_build.py`. The claim is delegated-agent-tagged and gives no specifics. **Locate them or refute the claim.** For each defect (or for the refutation): `file:line`, the mechanism in one sentence, the fields affected, the deliverables affected, and — decisively — **whether any published CENSUS-1 or CENSUS-1b number is touched**. Note our own F-ASOF fixture passed on the 12h→5m as-of mapping, so if defects exist they are elsewhere. **If any published number is touched → H2.**
- **D3 — manifest mtime vs "Chain:" sentence.** Compare the mtimes of CENSUS-1's substrate build manifests against the timestamp of the G-7 pre-registration commit `495abc8`. Report the delta. Also quote `LEDGER.md`'s "Chain:" sentence verbatim and the four cited precedent lines establishing that, for Tier-A/B census phases, pre-registration binds **analysis**, not the build. **Do not edit the ledger in this stage** — the reviewer rules on the wording from the report.
- **D4 — `analytics/` landing check.** Does `analytics/` exist in the repo? If yes: its version string, `analytics_sha()` output if callable, module list, and whether it imports anything from `engine/`. If no: state ABSENT.
- **D5 — S-3 journal availability.** Confirm `research_outputs/_archive/s3_2026-07-27.zip` exists and report its manifest (member list, sizes, sha256 if recorded). Stage 4 needs an un-archive; report whether it is intact **before** Stage 4 depends on it.

### 3.2 Stage 2 — the record

Append the blocks in **Appendix A** verbatim to the end of `LEDGER.md`, in the order given, altering no existing line. Then stage and commit.

Conditional: **if D1 reported ABSENT**, also append Appendix A-0 (the D8 catch-up entry) *first*, before the others.

Then commit for provenance, in the repo root unless a `docs/` convention is already established for reports (check `git ls-files` and follow the existing convention): `Report_7_CENSUS_1b_The_Decision-Grade_Census.md` and `Cascade_Atlas_CENSUS_1b_v2.html`. **Atlas v1 is deliberately excluded** — v2 preserves all of v1's visuals and supersedes it; one copy of the story.

Commit message: `docs: PC-1 record batch — four corrections, RS interview rulings, standing rule G-11, Report 7 + Atlas v2 provenance`. **Do not push** — the push decision is the operator's at the end of the session.

### 3.3 Stage 3 — LIT remediation (destructive; operator-authorised 2026-07-29)

**The order is not optional.** Reversing steps 1 and 2 makes the existing store illegal under the new floor and every LIT load raises `AssertionError`.

1. **Pre-flight (read-only).** For each of the six `LITUSDT_*.parquet` stores in the kline cache: total rows, first `open_time`, rows before `1_766_448_000_000` (2025-12-23T00:00Z), count of rows with `volume == 0`, count of distinct close values, and sha256 of the file. Write to `_reviewer_box/pc1/lit_preflight.json`. **Expected** (from the 2026-07-28 handoff): all six begin exactly at 2025-12-01T00:00Z; 40,832 total pre-charter rows across the six; every such row flat at close 0.592 with zero volume. **Any material deviation → H3.**
2. **Purge.** Delete the six `LITUSDT_*.parquet` files. *(The no-shrink save path means deletion is the only removal primitive.)*
3. **Refloor.** Set `engine/cells.py:42` to `LIT_FLOOR_MS = 1_766_448_000_000  # 2025-12-23T00:00:00Z (charter I1)`, retiring the two-floor design so the engine line matches charter invariant I1 and `study/loader.py:36`.
4. **Version bump.** Bump `engine/version.py` to `1.0.12`. Record the resulting commit sha in the ledger entry (Appendix A-4 template). *(Rationale: we have a live case — `3d28325` — of one version string denoting two distinct byte states. Bump **and** cite the sha.)*
5. **Re-extend.** Re-run `scripts/backfill.py` for LITUSDT across all six intervals. It should begin at the detected listing (2025-12-23 17:30). **Failure or short return → H5.**
6. **Verify (fixture F-PC-LIT, §5).**
7. **Provenance diagnostic — find the mechanism, do not merely clean the symptom.** Determine how constant-value zero-volume rows entered the store. Search `engine/data.py` and `scripts/backfill.py` for gap-filling operations (`reindex`, `ffill`, `fillna`, `asfreq`, forward-fill, or any reconstruction of a complete time index). Establish whether any path can synthesise flat rows from a stale price. Test the competing hypothesis on record (bulk-zip append concatenating whole archives without trimming to `start_ms`) by inspecting whether Binance's own December-2025 LIT archive contains such rows. Report the mechanism, or state explicitly **UNLOCATED** with the paths eliminated. **This must not silently recur on the next mid-month listing.**
8. **Republish.** Re-run and re-publish `brief_2026-07-27`, and refresh the `_reviewer_box` copy. *(Only the LIT percentile / rank / bar-count fields change; levels and volume-weighted quantities were never affected — zero volume contributes zero weight.)*

Commit: `chore: LIT estate remediation — purge synthetic padding, retire two-floor design, engine 1.0.12`. **Do not push.**

### 3.4 Stage 4 — the two free journal tests (Tier-A)

Un-archive `research_outputs/_archive/s3_2026-07-27.zip` to a working location (not into `research_outputs/s3/` — keep the archive authoritative). Verify integrity per fixture F-PC-JOURNAL. **Note for later:** CENSUS-1c's Phase 0 will need this same un-archive; leave it in place and record the path so that work is not repeated.

**T1 — the LPS-qualified split.** Wyckoff's Last Point of Support: after a spring (a flush below a level that reverses), price returns to test that low on **lower volume** and holds — the test that qualifies the reversal. Hypothesis: re-entry fills preceded by an LPS-qualified structure outperform those that are not. Operationalisation, **[VETO — confirm against the Level doc §1.2 and cite the section verbatim in the report before computing]**: for each re-entry fill in the S-3/TC-1 journals, look back a pinned window; qualify the fill as LPS if (a) a prior low was approached within a pinned ATR tolerance, (b) that low was **not broken on a closing basis**, and (c) the test bar's volume was below the volume of the bar that made the original low. Split expectancy (R, and net-of-toll bps) by qualified vs unqualified, with bootstrap CIs and the sample counts printed.

**T2 — tested vs untested stop anchors.** From the Level doc §1.4: a structural stop sits behind a pivot low; that anchor may be a level price has already visited and held (**tested**), or a fresh one (**untested**). Hypothesis: tested anchors survive better. Operationalisation **[VETO — same procedure, cite §1.4]**: for each fill carrying a structural stop, classify its anchor by whether price had previously approached within a pinned ATR tolerance and held. Report stop-hit rate, expectancy, and MAE distribution by class, with CIs.

Both tests: **dual units (R and bps), net-of-toll, sample counts printed, CIs on every number, and per-asset breakdown on the five-asset scorable panel** (BTC, ETH, SOL, NEAR, ZEC — JTO and TAO are thin annexes, reported but never weighted). Write `_reviewer_box/pc1/stage4_journal_tests.json`.

**Tier-A discipline note:** journal arithmetic requires no G-7 pre-registration. The predictions in §7 are reviewer discipline, not a registration; they are stated before computing and scored honestly either way.

## 4. Definitions to pin before computing

Restate in the Stage 4 report, in the builder's own words: **re-entry** (a fill with nothing open, versus an *add* which increases an open position — nomenclature is fixed) · **structural stop anchor** · **tested vs untested** · **LPS qualification** (all three thresholds, each marked [VETO]) · **expectancy** (R and bps, net of the round-trip toll) · **the five-asset scorable panel** and why JTO/TAO are annexes.

**Standing correction to carry:** exploration-classic is a **five-asset** panel. FARTCOIN, HYPE and LIT have **zero** scorable days; JTO (205d) and TAO (80d) are slivers. Any cross-asset replication argument has **five** independent units, not ten.

## 5. Fixtures — any MISMATCH halts that stage (H4)

| # | Fixture | Expected |
|---|---|---|
| **F-PC-ENV** | Environment assertion (§3.1) | Local working-clone path confirmed; else exit 2, nothing written |
| **F-PC-LEDGER** | Append-only: after appending Appendix A, every pre-existing line of `LEDGER.md` is byte-identical to a pre-append snapshot | 0 deletions, 0 modifications; only additions |
| **F-PC-ENGBYTE** | After Stage 3, `git diff` on `engine/` shows changes **only** in `cells.py` (one constant) and `version.py` (one string) | No other engine file differs by a single byte |
| **F-PC-LIT** | Post-refloor, per interval: first `open_time` ≥ 1_766_448_000_000 · zero rows before the floor · zero rows with close == 0.592 and volume == 0 · first real bar carries non-zero volume | All six intervals pass |
| **F-PC-JOURNAL** | S-3 un-archive integrity: extracted row counts match the archived manifest; `tranche_id` count = 7,094 per F-SUB | Exact |
| **F-PC-DET** | Stage 4 analysis run twice → `stage4_journal_tests.json` byte-identical after normalising timing/path fields | Identical |

**F-PC-ENV and F-PC-ENGBYTE are the ones that poison everything.** A misrouted session produces plausible nonsense; an unintended engine edit breaks byte-identity guarantees every prior phase depends on.

## 6. Discipline

1. **No number is reported that was not computed this session from the artifact itself.** Inherited figures are cited as inherited, with their source.
2. **CIs on every estimate** (bootstrap, 10,000 resamples, seed 20260721 — the pinned project seed). An estimate whose CI spans zero is reported as such, never as an effect.
3. **Net-of-cost or it is not a result.** Gross-only findings are not findings.
4. **Five-asset replication arithmetic** (§4). Never size power against a ten-asset basket.
5. **No lockbox bar is read, resampled, or computed on** — including "just to check the pipeline."
6. **Stage 1 characterises; it does not fix.** If as-of defects are found, remediation is scoped as its own work once their shape is known.
7. **Nothing is pushed.** All stages commit locally; the push is the operator's decision at session end.

## 7. Predictions for Stage 4 (reviewer discipline, not a G-7 registration)

| # | Prediction | Prior | Falsified if |
|---|---|---|---|
| P-T1 | LPS-qualified re-entries show higher net-of-toll expectancy than unqualified, sign-stable on ≥3 of the 5 panel assets | 50% | not sign-stable, or the pooled CI spans zero |
| P-T2 | Tested stop anchors show a **lower stop-hit rate** than untested anchors, pooled CI excluding zero | 55% | CI includes zero, or the sign reverses |
| P-T2b | Tested anchors also show higher expectancy (the stronger claim — survival need not imply profit) | 40% | pooled CI includes zero |

Priors are the reviewer's, set before computing. P-T2/P-T2b are deliberately split because the C7b precedent is explicit in this project: **a location property surviving does not imply the outcome pays.**

## 8. Deliverables

Into `_reviewer_box/pc1/`: `stage1_diagnostics.json` · `lit_preflight.json` · `lit_postflight.json` (including the provenance-diagnostic verdict) · `stage4_journal_tests.json` · `PC1_REPORT.md` (a plain-language summary: what was found, what was changed, what remains open) · plus a `STATUS_ENGINE` block in the fixed project format for relay to the orchestrator.

## 9. Verdict, artifacts, ledger

**PASS** — all six fixtures MATCH, four stages complete, Stage 1's five diagnostics answered, LIT verified clean, Stage 4 scored honestly against §7. **PARTIAL** — Stage 4 blocked by journal-recovery problems but Stages 1–3 complete (report and stop; Stage 4 re-scopes). **HALT** — any of H1–H5. Ledger: Appendix A batch (Stage 2) + the LIT remediation record with real numbers (Stage 3, template A-4) + PC-1 completion. **Commit each stage separately; do not push, do not merge.**

## 10. The go-paste

**→ WHERE TO PASTE: your LOCAL Claude Code — the session whose `pwd` shows a `C:\Users\…OneDrive…` path (either the PowerShell CLI already inside the repo, or the desktop Code tab). NOT a cloud session.**

```
ENVIRONMENT ASSERTION — RUN THIS FIRST AND HALT IF IT FAILS.
Confirm all of: (a) pwd resolves under C:\Users\...OneDrive... (or /c/Users/...OneDrive...),
(b) git rev-parse HEAD succeeds, (c) engine/, research_outputs/ and LEDGER.md all exist.
If ANY fails: print the actual pwd and HEAD, write NOTHING, exit 2, and stop.
No read, no write, no commit happens before this passes.

CONTRACT: PC-1 — Pre-Census Consolidation (staged; Stage 3 is destructive and operator-authorised)

Read PC1_Pre_Census_Consolidation_Builder_Contract.md in the repo in full first. The contract is
the authority; this paste is the trigger. Work through all four stages autonomously. Stop ONLY on
halt gates H1-H5 (contract section 3.0). Write machine-readable reports into _reviewer_box/pc1/
so the operator drags files rather than screenshots terminals.

STAGE 1 — read-only diagnostics (changes nothing). D1 D8-correction presence in LEDGER.md ·
D2 locate-or-refute the two asserted as-of defects in scripts/census_build.py, and state whether
any PUBLISHED CENSUS-1/1b number is touched (if yes -> HALT H2 before Stage 2) · D3 manifest
mtimes vs commit 495abc8 and the ledger "Chain:" sentence (report only, do not edit) ·
D4 analytics/ landing + version/sha · D5 S-3 archive integrity.
-> _reviewer_box/pc1/stage1_diagnostics.json

STAGE 2 — the record. Append Appendix A blocks VERBATIM to the end of LEDGER.md, altering no
existing line (if D1 = ABSENT, append A-0 first). Commit LEDGER.md plus Report 7 and Cascade
Atlas v2 for provenance (Atlas v1 excluded deliberately). Message:
"docs: PC-1 record batch - four corrections, RS interview rulings, standing rule G-11,
Report 7 + Atlas v2 provenance". DO NOT PUSH.

STAGE 3 — LIT remediation. ORDER IS NOT OPTIONAL. Pre-flight the six LITUSDT parquet stores and
write lit_preflight.json (deviation from the documented state -> HALT H3) -> purge the six files
-> set engine/cells.py:42 LIT_FLOOR_MS = 1_766_448_000_000 -> bump engine/version.py to 1.0.12 ->
re-run scripts/backfill.py for LITUSDT (failure/short -> HALT H5) -> verify F-PC-LIT -> run the
PROVENANCE DIAGNOSTIC (find how flat zero-volume rows were synthesised; report the mechanism or
state UNLOCATED with paths eliminated) -> re-publish brief_2026-07-27 and refresh the
_reviewer_box copy. Commit: "chore: LIT estate remediation - purge synthetic padding, retire
two-floor design, engine 1.0.12". DO NOT PUSH.

STAGE 4 — two Tier-A journal tests. Un-archive research_outputs/_archive/s3_2026-07-27.zip to a
working location (leave it in place afterwards; CENSUS-1c Phase 0 needs the same un-archive).
T1 LPS-qualified re-entry split · T2 tested-vs-untested stop anchors. Cite the Level doc sections
1.2 and 1.4 verbatim and confirm the [VETO] thresholds BEFORE computing. Dual units, net of toll,
CIs on every number, five-asset panel (BTC/ETH/SOL/NEAR/ZEC; JTO/TAO reported never weighted).
Score against contract section 7 honestly either way.
-> _reviewer_box/pc1/stage4_journal_tests.json

Do NOT, even if it seems helpful: push anything · read/resample/compute on any lockbox bar
(2024-07-01 onward) including to "check the pipeline" · delete anything beyond the six named LIT
files · edit any engine file other than cells.py:42 and version.py · FIX the as-of defects if
found (characterise only) · substitute an estimate for a missing value · report a gross-only
number as a result.

Report back: PC1_REPORT.md (plain language: found / changed / still open), the four JSON
artifacts, the fixture table, Stage 4 scored against the predictions, and a STATUS_ENGINE block
in the fixed project format.
```

---

## Appendix A — ledger blocks (append verbatim, in this order)

### A-0 — CONDITIONAL, append only if Stage 1 D1 reports ABSENT

```markdown
## 2026-07-29 — CATCH-UP: the D8 cascade-ratio correction, recorded

- The CENSUS-1b completion entry (commit 7a7df1f, pushed) references a D8 cascade-ratio correction as having been committed. Stage 1 of PC-1 found no such entry in LEDGER.md. This entry supplies it, and the reference in that completion entry should be read as pointing here.
- CORRECTION. The CENSUS-1 reconciliation (770860b) stated the D8 cascade rungs show "remaining favorable ~= remaining adverse per rung (0.98-1.01) - a timing SCHEDULE, not an EDGE." That figure was carried from the state-of-project report and was NOT recomputed before commit. Recomputed from census_results.json (D8.per_followon_tf, remaining_mfe_atr_100 / remaining_mae_atr_100): MFE/|MAE| = 5m 1.028 / 15m 1.012 / 30m 1.030 / 1h 1.191 / 4h 1.326 / 12h 0.994 / 1d 0.984 - range 0.98 to 1.33, not 0.98-1.01.
- Substantive consequence. Fast rungs (5m/15m/30m) and slow rungs (12h/1d) are near-symmetric; the MID rungs are favorable-skewed (1h 1.19, 4h 1.33; n=67,218 and 28,165). The "symmetric noise -> timing not edge" reading was overstated at the 1h/4h rungs. CENSUS-1b subsequently priced this net-of-toll and CONFIRMED the 4H rung at quality ratio 1.071, CI [1.053, 1.090] - a finding that exists only because the figure was recomputed.
- Reviewer recompute-miss owned: a figure was committed from a prior artifact without this-session recomputation, contra standing discipline. Ledger is append-only; 770860b's line stands and this entry supersedes its D8 ratio.
- Reviewer: Claude (Fable-mode), recorded 2026-07-29.
```

### A-1 — Four corrections from the engine ingestion

```markdown
## 2026-07-29 — CORRECTIONS from the engine-source ingestion (four items)

- **Origin.** The 2026-07-25 engine-ingestion session read the engine source directly for the first time and checked standing claims against it. Most survived; four did not. No measured number changes. What changes is what the numbers LICENSE US TO BUILD.

- **C-1. The D5 graduation basis is narrowed — a ratified claim is half un-representable.** CENSUS-1b's P-1b-D5 was ratified as "robust on 12h/1d." The engine has NO 1D timeframe: INTERVAL_MS and MTF_SET stop at 12h, and only the S-1 instrumentation layer resamples a daily frame (outside the frozen map). A 1D-anchored result therefore has no engine destination without an extension that would need its own pre-registration. REVISED BASIS: 12H PRIMARY (ratio-of-medians AND per-record-median both clear 1.0: 1.079 / 1.066); 4H SECONDARY with the skew caveat stated (per-record-median 0.985 - the typical single trade is break-even; the edge lives in the right tail); 1H EXCLUDED (0.944, below 1.0 on every measure); 1D EXCLUDED from the graduation basis, retained as diagnostic only. Convergence worth noting: scoping D5 to 12H scopes it to the POSITION mandate - the same mandate where S-2b's structural stop is robustly positive (+488.19 grid / +224.61 strip-best). Two independent lines now point at one mandate.

- **C-2. Lens is not governor.** The census's four "governor lenses" {1H, 4H, 12H, 1D} are MEASUREMENT FRAMES applied in analysis. The engine's governors are fixed per mandate: 1H intraday, 4H swing, 12H position. Translating any lens result into a rule requires an explicit lens-to-mandate mapping PLUS an engine-representable check. STANDING CONVENTION ADDED: every MTF table prints an "engine-representable" column alongside its absolute and governor-relative coordinates. Consequence already realised: the absolute-4H D8 rung means a different object per mandate (swing = the governor itself, pre-entry; intraday = one rung above; position = one rung below), which is why the D8 lens split is a prerequisite to any add rule.

- **C-3. The exec-grid discrepancy is pinned to TC-2.** cells.py specifies the intraday mandate's exec frame as 1m, while 1m is excluded by ruling and the census exec grid is 5m. This is a live inconsistency between the frozen cell grid and the study's exec floor. It is PINNED TO TC-2, which inherits the intraday mandate. Until TC-2 resolves it, any intraday run must carry an explicit TC-5-style runtime patch, declared in that phase's registration - never assumed.

- **C-4. Toll and funding are separate costs, and only one of them is priced.** The round-trip toll is a per-asset constant, verified drift-free across charter, engine and census (it reconstructs exactly from fees + slippage, and the CENSUS-1b mapping is identical to the one CENSUS-1's D5 used). FUNDING IS NOT IN THE TOLL. It accrues per funding interval for the whole hold, it is genuinely additive, and its data grid is NON-UNIFORM: SOL changes cadence four times (8h -> 4h -> 2h -> 8h) and JTO/TAO run on a 4h grid, so any assumed uniform 8h cadence mis-prices three of seven assets. CONSEQUENCE: D5 was measured at REGIME-SCALE horizon (hold to governor flip, capped 2,000 exec bars ~ 6.9 days). Rough arithmetic puts the 4H lens ratio at ~1.04 under ~10 bps cumulative funding and ~1.00 under ~21 bps. FUNDING COULD ERASE THE D5 EDGE ENTIRELY AND IS CURRENTLY UNMEASURED. It must be priced from real timestamped records (the funding_df loader path already exists) before D5 graduates to a Tier-C.

- Reviewer: Claude (Fable-mode), 2026-07-29. Operator: ratified.
```

### A-2 — RS interview rulings and session ratifications

```markdown
## 2026-07-29 — Range-and-Structure layer: interview rulings + session ratifications

- **RS INTERVIEW (five questions, operator-ruled).**
  - Q-R1 WALL FAMILIES: (a) — dual independent families (pivot-clusters + SS-cross-clusters), agreement COUNTED never weighted, wall-family redundancy gauge built in.
  - Q-R2 FAMILY SCOPE: (a) — fast {5m,15m,30m,1h} + slow {4h,12h,1d}; mid {30m-1h} measured FOR CONDEMNATION, so the "untradeable" reading becomes a datum rather than an assumption.
  - Q-R3 PLAYBOOK-R TIMING: (a) — detection and gating first; a range-trading contract is drafted ONLY IF the height-vs-toll feasibility gate AND the edge-fade outcome leg both pass.
  - Q-R4 ACCEPTANCE DEFINITION: (a) — the census measures four candidate operationalisations head-to-head (2-close / 3-close / 6-outside-close stale-run / time-beyond); the engine default is chosen FROM DATA.
  - Q-R5 SCANNER DISPOSITION: operator ruling supersedes both drafted options. The new range-detection logic inherits NO starting values from the SS Breakout Scanner. The scanner is preserved as a RECORD of an earlier effort and deployed as a CONTROL ARM: its closed-bar rectangle core ported deterministically with constants FROZEN AS-IS, run as-of over exploration-classic, then (i) compared against the new dual-family walls as a control group and (ii) graded on its own precision by pre-registered criteria. Bias on record: the scanner was partly trained to detect rounded bottoms and its constants were eyeball-tuned on two charts (ONDO 4h / INJ 4h per source comments); the saucer module and the intrabar/wall-clock components are excluded from the port so the arm is an uncontaminated rectangle benchmark. New-detector constants are derived CLEAN-ROOM under sensitivity-strip discipline.

- **CENSUS-1c SCOPE RULINGS (phase deferred; rulings binding when drafted).** Q-1: the 1D lens IS included in the D8 split, labelled DIAGNOSTIC-ONLY and loud, since 1D has no engine destination. Q-2: the D8 eligibility window is measured at all three widths (first-bar / N-bar / full-period), with FIRST-BAR as the anchored default because that is what the ratified 1.071 already means. Q-3: Phase 0 (the price-space cross-cluster confluence triage) is FOLDED INTO CENSUS-1c as a job, SEQUENCED FIRST, so its verdict gates whether the expensive confluence backfill harness is built at all. Phase 0 is re-labelled "Tier-A WITH A JOURNAL READ" - not free: it requires the S-3 un-archive, a tranche_id join, a pre-registered exec-grid flooring convention (71.7% of fills sit on the excluded 1m grid), and a TIME-SCOPED as-of cluster window.

- **SEQUENCING RATIFIED — and CHANGED.** The census no longer comes next. New order: PC-1 (this contract) -> SECRET SAUCE DEFINITION (specify the strategy precisely, so the census measures a fixed object rather than a moving one) -> CENSUS-2a (capture and structure: RS layer, EMA lattice, wall families, scanner control arm, range feasibility) -> CENSUS-2b (confluence and outcomes: CCL, H-RVX, harvest and pyramid conditioners) -> Tier-C runs as V2 COMPONENT VALIDATIONS -> Secret Sauce Trading Engine V2 spec. CENSUS-2 is SPLIT into 2a/2b on ratification: the single phase had grown to plausibly three phases wearing one name, with a wide anti-fishing surface and one failure able to stall everything. OPEN: whether CENSUS-1c survives as a standalone phase or folds into CENSUS-2a - deferred until the Secret Sauce definition exists, because the definition may change what 1c should measure.

- **ALSO RATIFIED.** The V2 roadmap shape (Layers 0-4: cost floor / regime + balance coordinate / location / point / campaign), with the D5 and D8 Tier-Cs reframed as component validations rather than standalone patches. The free journal mini-contract (LPS-qualified split, tested-vs-untested stop anchors) GO - executed as PC-1 Stage 4. LIT purge-and-refloor AUTHORISED with the version-bump rider (PC-1 Stage 3).

- Reviewer: Claude (Fable-mode), 2026-07-29. Operator: ratified.
```

### A-3 — Standing rule G-11

```markdown
## 2026-07-29 — STANDING RULE G-11: file-copy instructions must name destination filenames explicitly

- **Origin.** An ambiguous multi-file copy instruction produced 14 byte-identical prefixed duplicates in the project context box, degrading context-audit quality and creating competing copies of the record.
- **Rule.** Any instruction that copies, moves, or files more than one artifact MUST enumerate each destination filename explicitly. A pattern, a directory, or "copy these across" is insufficient. This applies to project-box uploads, repo filing, archive extraction, and reviewer-box drops alike.
- **Corollaries.** (1) One-paste-complete-manifest: a filing instruction lists every file it intends to produce, so the result can be diffed against the intent. (2) A loose scratch copy of content already committed is deleted once committed - a duplicate of the record reads as a competing copy later.
- **Numbering note.** G-10 is RESERVED for the BRIEF lane's Forward Validation Protocol, currently drafted under the number G-9 - which collides with the ratified G-9 (relative fixture tolerances, 2026-07-22). The renumber is relayed to that lane; this rule takes G-11 to avoid a second collision. Two rules sharing a number corrupts the governance index permanently, which is why the gap is preferred to the risk.
- Reviewer: Claude (Fable-mode), 2026-07-29. Operator: ratified.
```

### A-4 — LIT remediation record (TEMPLATE — the builder completes it with real numbers after Stage 3)

```markdown
## 2026-07-29 — LIT estate remediation executed: synthetic padding purged, two-floor design retired, engine 1.0.12

- **Authorisation.** Operator, 2026-07-29, on the escalation upheld in the 2026-07-28 ENGINE-to-BRIEF handoff. Destructive and engine-touching; executed under PC-1 Stage 3 in the mandated order (purge BEFORE refloor - reversing them makes the existing store illegal and every LIT load raises AssertionError).
- **What was actually there (pre-flight, measured).** [BUILDER: per-interval table - total rows, first open_time, rows before the charter floor, zero-volume count, distinct-close count, sha256 of each purged file.] Documented expectation was 40,832 pre-charter rows across six intervals, all flat at close 0.592 with zero volume.
- **CORRECTION TO THE G-2 REGISTER.** The register describes these rows as "pre-Lighter (Litentry) 1m bars" (scripts/v3_scorer.py:314). They are NOT another asset's price history: every row is a constant-value zero-volume placeholder (single distinct close, zero volume throughout), most plausibly a forward-fill seeded from a stale price. Real Lighter LIT opens at 3.734 with volume on 2025-12-23 17:00. The register's characterisation is wrong on the record and is corrected here; the remediation differs accordingly.
- **Why the loader guard never fired, and structurally never could.** engine/data.py raised only when min(open_time) < LIT_FLOOR_MS. The store began EXACTLY AT the floor, not before it - the guard was one step too loose in precisely the direction that made it inert. The two-floor design was the defect: the build prompt specified max(detected_first, 2025-12-01), and the padding filled exactly the gap the looser floor opened. Retired by this remediation; the engine line now matches charter invariant I1 and study/loader.py.
- **Study impact: NONE, and this is verified rather than assumed.** The study loader carries its own correct floor (2025-12-23, invariant I1) and floors requests independently; DATA_CENSUS and data_starts report LIT's first bar as 2025-12-23 on all six intervals; no study artifact ever scored LIT (the LIT annex was excluded, with estate remediation named as the precondition). LIT additionally has ZERO exploration-classic days, so there was no scorable data to contaminate.
- **Ops impact, measured not asserted.** ATR(14) LEVEL unchanged to five decimals (22 leading days wash out of a Wilder average over 239 bars); ATR PERCENTILE moved 63.2% -> 61.5% with 22 zero-true-range days entering the percentile base; VWAP and volume-profile layers unaffected (zero volume contributes zero weight). Honest statement: percentile, rank and bar-count fields were wrong; levels and volume-weighted quantities were not.
- **Post-remediation state.** [BUILDER: per-interval first open_time, row counts, F-PC-LIT result, brief re-publication confirmation.]
- **Engine change.** engine/cells.py LIT_FLOOR_MS set to 1_766_448_000_000 (2025-12-23T00:00:00Z); engine/version.py bumped to 1.0.12; commit sha [BUILDER: fill]. Version bumped AND sha cited because this project has a live case (3d28325) of one version string denoting two distinct byte states. No trading logic was touched; F-PC-ENGBYTE confirms engine/ differs only in these two files.
- **Provenance of the padding.** [BUILDER: the mechanism, or UNLOCATED with the paths eliminated.] This must not silently recur on the next mid-month listing.
- Reviewer: Claude (Fable-mode), 2026-07-29. Operator: authorised.
```

---

*Contract prepared by the reviewer under Fable-mode, 2026-07-29. PC-1 exists because the next two pieces of work — defining Secret Sauce, then measuring it — should start from a record that is true, an estate that is clean, and a set of open questions that is empty. It answers three integrity questions, corrects four claims (one of which is a ratified graduation basis that the engine cannot currently support), purges a contamination that never reached the study but was one loose guard away from doing so, and runs two free tests whose results feed a phase already in the queue. Nothing here is a rule change and nothing here is evidence spend. It is the clearing of the decks.*
