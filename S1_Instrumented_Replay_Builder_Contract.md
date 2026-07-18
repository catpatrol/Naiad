# S-1 — Instrumented Replay (Measure-Only) — Builder Contract

**Phase:** v12 Study · **Tier B** — engine instrumentation + one full re-run. **Trading is UNCHANGED; any instrumentation that moves a traded number is a defect by definition.**
**Baseline measured against:** TC-4 / engine 1.0.8 / `journal_pass2` (config `v12_anchor_g8` sha `97c24125…`, grid evidence hash `6c00f9b4…`, headline 1× **−1,796.993** over 2,599 campaigns).
**Purpose in one line:** journal what every ratified candidate mechanism *would have done* on the exact trades the baseline took — ratchets, harvests, add triggers, re-entry triggers, dead-gate triage, stop-width floors, zone geometries, V thresholds, and the full multi-timeframe picture — so the Tier-C queue (TC-1/2/3/5, aggressive mode) is designed from measurements, not guesses.
**Operator ratifications in force:** move off event-driven protection (B1) · ratchet beacon "protect profit WHILE minimizing stop-outs from predictable LTF noise" (A) · BE-gate retained as the add principle; fix the ratchet, keep the gate (A) · pivot-trail as first candidate, 1H-e89 shadowed (interview) · asymmetric-200 Z3 (B4) · MTF expansion to 15m/30m/1D, open-minded confluence mining (B6) · V priority (C/step-2.1) · re-entry quality bar designed from S-1 (2026-07-17) · dead-gate, drought, and A/B families (RC/TC-4 findings, accepted) · emission-neutrality invariant (2026-07-18 confirm #2).

---

## 0. Operator instructions — plain language

**What this run is.** The engine replays the exact same 4.5 years, takes the exact same trades as the new baseline, and — alongside each trade — writes down what a few dozen candidate rules *would* have done instead: where each candidate stop would have trailed, when each candidate harvest would have banked, which candidate add-triggers would have fired mid-trend, what the refused re-entry signals would have returned. Nothing is traded differently. Think of it as the same diary with a very wide margin, and every margin note priced.

**Why we trust it can't lie.** The acceptance test is mechanical: strip the new margin notes off, and the diary must be **byte-for-byte identical** to the TC-4 baseline. If even one traded number moved, the phase fails loudly.

**Your steps:**
1. Save this contract into the repo (next to `LEDGER.md`).
2. PowerShell → repo → `claude` → `git status` → expect `On branch v12-v1-census`, clean, up to date with origin.
3. Paste the go-paste (§12). Enter.
4. *What you should see, in order:* (a) a data-prep report (30m/1D bars built locally from data you already have — nothing downloaded); (b) a **ledger pre-registration commit** with all eight predictions — before any run; (c) the run, twice — expect the longest compute yet (the enrichment does heavy per-trade work; hours are normal; leave it running); (d) a fixture table, **all MATCH**, led by the byte-identity check; (e) the prediction scorecard and the measurement tables.
5. Any fixture MISMATCH → builder halts, reports, produces nothing downstream.
6. Send back: fixture table, prediction scorecard, `s1_results.json`, `S1_MEASUREMENT.md`. I verify independently before any of it informs a variant slot.

---

## 1. What this phase is

One instrumented replay of the 20-cell grid on the 1.0.8 engine, emitting: (a) an `s1` enrichment object on existing journal rows, and (b) a **sidecar event stream** for counterfactual events that have no baseline row. Output feeds the V4 design and the Tier-C queue. Evidence spend: none beyond what VR-1 already covers (exploration-classic, mined); predictions pre-registered regardless, because that discipline has now paid for itself four phases running.

## 2. What this phase is NOT

- **Not a strategy change.** No traded rule moves. The BE add-gate, the event-driven ratchet, the zone geometry, V thresholds — all trade exactly as 1.0.8. Candidates are *measured*, never *applied*.
- **Not TC-1/2/3/5 or aggressive mode.** Those are Tier-C runs, each with its own pre-registration, designed *from* these tables.
- **Not a variant nomination.** Five slots, operator's call, after the tables land.
- **Not J-1.** The REJECT-row dataclass fix perturbs journal bytes and would break F-BYTE. Carried again, disclosed again. (G-1 *does* ride — see §3.6 — because it cannot touch bytes on any valid run.)
- **Not free of first-order caveats.** Exit/ratchet shadows are computed on the actual entry stream; entry-filter flags are computed on the actual fill set. A really-adopted rule changes the trade set. These tables **rank**; Tier-C **validates**.

## 3. The instrumentation set — engine 1.0.9 (instrumentation-only release)

All implementation confined to the enrichment path (`shadows.py` + a new `s1` module + the sidecar writer + the resampler). `engine/signals.py` and `engine/trading.py` are **byte-untouched** (invariant §4.2; behaviorally enforced by F-BYTE).

### 3.1 Ratchet & harvest candidates (per-tranche scalar outcomes in `s1.ratchet`)

Every candidate reports the same six scalars: `exit_r` (per-unit, gross basis), `exit_i_offset`, `engaged` (bool), `engage_i_offset`, `noise_stopout` (candidate exited AND price resumed ≥1R within 20 exec bars), `capture_pct` (exit_r ÷ mfe_r, winners only). Plus, per candidate, `adds_would_be_eligible` — the count of baseline while-positioned add signals that would have passed the BE-gate under this candidate's stop path (the pyramid-funnel measurement).

| Family | Grid (defaults; veto V2) | Count |
|---|---|---|
| Chandelier: `stop = max(stop, peak − k·ATR_exec)` | k ∈ {1.5, 2.0, 3.0} | 3 |
| Pivot trail (two-phase: baseline stop until engaged at first pivot confirm, then Nth prior confirmed exec pivot ∓ 0.5·ATR) | (L,R) ∈ {(3,3), (5,5)} × N ∈ {2, 3} | 4 |
| EMA trail: `EMA_p(TF) ∓ b·ATR_exec`, engaged on first favourable close beyond the line | (p,TF) ∈ {(89,1h), (89,gov), (200,exec), (200,gov)} × b ∈ {0, 0.5} | 8 |
| R-ladder: at each +1R MFE rung, stop → rung −1 (…+1R→BE, +2R→+1R…) | 1 | 1 |
| Giveback trail: arm at MFE ≥ T, exit at G% giveback of peak | T ∈ {1, 2}R × G ∈ {30, 40, 50}% | 6 |
| Two-phase hybrid: baseline stop → engage at MFE ≥ 1R → hand off to {chandelier k=2, pivot (5,5) N=2} | 2 | 2 |

24 candidates. Grids for k/T/G were pinned from RC-3/RC-4 distributions (median winner MFE, decile structure); the operator's 1H-e89 practice and the Prometheus-winning exec-e200 are both in the EMA family. **Scorecard axis (contract-mandated presentation): capture% vs noise-stopout%, per mandate — a candidate that captures more by shaking out more does not win.**

### 3.2 Dead-gate triage (`s1.deadgate`)

For N ∈ {12h, 24h, 48h} wall-clock (converted to exec bars per mandate) × action ∈ {kill, halve}: counterfactual campaign outcome if, when the working stop has not reached BE on the R1 by N after fill, the campaign is killed (exit at that bar's close) or halved. Six scalars per campaign. Basis: mc=1 campaigns win 2.5%; BE-attainment is the strongest in-flight quality signal measured.

### 3.3 Entry-geometry flags (`s1.entryflags` — booleans, first-order by construction)

Per tranche: `would_reject_anchor_Y` for Y ∈ {0.5, 0.75, 1.0, 1.25} on both anchors (structure-extreme floor; pure fill−Y·ATR), and `would_reject_bps_m` for m ∈ {0.5, 1.0, 2.0} on the **cost-aware floor** `stop_dist_bps < m × roundtrip_cost_bps` (tier fee+slip schedule). 11 booleans. The alternative books are then Tier-A filter recomputes on the S-1 journals.

### 3.4 Zone-geometry shadow (`s1.zone` on every PRIME/CONFIRM signal row, filled AND rejected)

Counterfactual `active_zone` label under: current geometry with `z3_prox` ∈ {0.25, 0.35, 0.50}, and the **operator's asymmetric-200 Z3** `[e200 − a·ATR_gov, e200 + b·ATR_gov]` (direction-adjusted) for (a,b) ∈ {0.25, 0.5} × {0.5, 0.75, 1.0}. 9 labels per signal event. Purpose: break the zone/stage weld (R6: 100% collinear) and make VS-Z3 decidable.

### 3.5 Sidecar event families (`s1_events/<cell>.jsonl` — counterfactual events with no baseline row)

1. **Add-trigger drought family** (while a tranche is open): N-bar breakout continuation (N ∈ {20, 55} exec bars), pullback-touch of exec-e9, 2-ATR extension event, CONFIRM ribbon re-cross while positioned. Each event: trigger id, bar, would-be entry at next open, baseline stop formula, forward outcome to campaign stop / ±10R cap, and whether the BE-gate would have admitted it under the *baseline* stop and under each §3.1 candidate's stop (`admissible_under`).
2. **Re-entry trigger A/B**: every baseline `not_positioned` CONFIRM reject (69,395) — would-be trade at next open, standard stop, outcome to the same horizon set as the traded PRIME re-entries; plus family tag on the traded re-entries so A/B lands on one table.
3. **V-shadow**: read the live V thresholds from config; sweep each of {`climax_mult`, `cap_ext`, `cap_window`, `cap_vol_conf`} one notch and two notches looser, one-at-a-time, plus one all-loose combo (9 variants). Journal every hypothetical firing with forward returns at 5/20/100 exec bars and a would-be-trade outcome at the standard V sizing/stop. No trading.
4. **MTF cross events**: every e9/e89 and e89/e200 cross on any capture-set timeframe occurring while a tranche is open, with the tranche's forward outcome from that bar.

### 3.6 MTF capture (`s1.mtf`) + data prep + G-1

Capture set = {exec, 15m, 30m, 1h, 4h, 12h, 1d} — **instrumentation-only; `MTF_SET` and every signal input untouched.** Per tranche, at entry / MFE bar / exit: distance to e9/e89/e200 of each capture TF in ATR-of-that-TF units, plus structure state (`s2bu`/`s2be`) per TF; and two summaries: fraction of open bars beyond each TF's e200, and per-TF structure-flip-during-trade flags. **Data prep:** build 30m (from 15m) and 1d (from 1h) locally by deterministic OHLCV aggregation — offline, RC-0-verified feasible; aggregation invariants asserted (F-RESAMPLE). **G-1 rides 1.0.9:** the code-level lockbox guard (raise if any requested window exceeds the boundary) is purely protective and byte-inert on valid runs; it closes a register item open since the anchor. **[Veto V3.]**

### 3.7 Ratchet-advancement instrumentation (`s1.advance`) — scores P-S1b

Per tranche: `n_stop_advances` during life, `advances_before_mfe`, `bars_to_first_advance`, `stop_moved_r` (stop_at_exit − stop_at_entry, in R). Settles the non-advancement share of the PROTECTED paradox with direct counts.

### 3.8 Cluster re-measure (`s1.cluster`)

Re-attempt distance from the direction-run's first attempt in **governor-ATR** units; in-cluster flags at k ∈ {0.25, 0.5, 1.0} gov-ATR. (Exec-ATR clustering found a ~zero population; this is the coarser yardstick.)

## 4. Invariants

1. **Emission neutrality (operator-ratified wording):** *the resolved/buffered decision function is byte-frozen at 1.0.8. New S-1 columns never gate row emission — a shadow that cannot resolve at the data edge emits as null on the same rows pass 2 emitted, never as a suppressed row.* Sidecar events likewise never suppress, reorder, or add main-journal rows.
2. `engine/signals.py` and `engine/trading.py` byte-untouched (`git diff` empty on both; F-BYTE enforces behaviorally).
3. All new data lives in exactly two channels: the `s1` object on existing rows, and the sidecar stream. No other schema change.
4. Fresh roots `research_outputs/s1/journal_s1/` (+ `_run2` twin, + `s1_events/`); `journal_pass1` and `journal_pass2` read-only.
5. Candidate budget as pinned in §3 — no silent grid growth, no silent trims (F-GRID).
6. Ledger pre-registration committed before the run; predictions scored verbatim.
7. No network; resampling is local aggregation only. No lockbox contact (G-1 now enforces this in code).
8. Determinism: full run twice; identical.

## 5. Unit conventions

Carried from RC/TC-4 verbatim (cell-R, R/unit, signed `one_r`, bps conversions, `concurrent_open_at_fill`, direction-run/attempt, fill_class). New: candidate `exit_r` is **gross (0×) per-unit** — every candidate table must therefore compare against the baseline's 0× line and print its own 1× proxy using the row's actual `cost/one_r` (stated as a proxy); `capture_pct` = candidate `exit_r ÷ mfe_r` on tranches with `mfe_r ≥ 1`; `noise_stopout` horizon = 20 exec bars, ≥ +1R resumption, matching the ratified shaken-out definition (Q4).

## 6. Fixtures

| # | Fixture | Expected |
|---|---|---|
| F-BYTE | Strip `s1` key + normalize {run_id, engine_version, config_id} → every main-journal row byte-identical to `journal_pass2`, **and row sets/order identical**, all 20 cells | identical |
| F-P2REF | Traded-column recompute from S-1 journals: grid 1× / 0× / campaigns / win rate | −1,796.993 / +275.9924 / 2,599 / 10.8503% |
| F-NULL | Every edge-unresolvable `s1` value is null on an *emitted* row (audited on the 25 buffered/open tranches and the final-window population) | 0 suppressed rows |
| F-GRID | Journaled candidate/param sets == §3 grids exactly | match |
| F-SIDE | Every sidecar event references a valid (cell, bar); A/B sidecar count for `not_positioned` events | 69,395 |
| F-RESAMPLE | 30m/1d aggregation invariants (child-count, high=max, low=min, vol=Σ; span == source span) + resample determinism | 0 violations |
| F-ADV | `s1.advance.stop_moved_r ≥ 0` on every tranche (the ratchet never loosens — P-S1a, now a standing fixture) | 0 violations |
| F-DET | Double-run identity (main + sidecar hashes) | identical |

## 7. Pre-registered predictions — committed before the run

| # | Prediction | Prior | Falsified if |
|---|---|---|---|
| P-S1b | Non-advancement (`advances_before_mfe = 0`) accounts for ≥⅓ of tranches with MFE ≥ +1R that exited at a gross loss | 75% | < ⅓ |
| P-S1-RAT | ≥1 ratchet candidate on swing achieves median capture ≥ 25% on PROTECTED winners with noise-stopout ≤ 20% | 60% | none does |
| P-S1-RAT2 | The best candidate by the two-axis card is **not** event-driven-engaged (i.e., not the exec-e200 family that X-A represents) | 55% | an X-A-style candidate tops the card |
| P-S1-DG | Best dead-gate (N, action) improves grid 1× by ≥ +200 first-order | 55% | < +200 |
| P-S1-AB | CONFIRM-while-flat counterfactual per-unit net ≥ traded PRIME re-entry per-unit net (−0.7554) | 55% | worse |
| P-S1-ADD | ≥1 add-trigger candidate averages ≥ 2 admissible mid-trend firings per mc≥2 campaign under ≥1 ratchet candidate's stop path | 60% | none |
| P-S1-V | Loosest V variant fires ≥ 5× baseline events; AND incremental firings' median forward-20 return is **not** better than baseline V firings' | 70% / 55% | frequency < 5× / incremental > baseline |
| P-S1-Z3 | Asymmetric Z3 (a=0.25, b=0.5) labels ≤ 40% of currently-Z3-labeled fills, and its labeled cohort's realized net/unit ≥ the current Z3 cohort's | 55% | either half |
| P-S1-MTF | ≥1 capture-set confluence (registered forms: entry beyond 1d-e89; 30m structure aligned at entry; ≥80% of open bars beyond 1h-e200) separates campaign expectancy by ≥ 0.5R | 50% | none reaches 0.5R |

The MTF *mining pass* beyond those three registered forms is **exploratory under VR-1** — findings become hypotheses for the next pre-registration, never gates. **[Veto V6.]**

## 8. Deliverables

`S1_MEASUREMENT.md` + `s1_results.json`: the ratchet two-axis scorecard per mandate (capture vs noise-stopout, engagement rates, adds-would-be-eligible funnel) · dead-gate table · entry-flag first-order books (both anchors × Y; bps floor × m) · zone tables (label populations + realized outcomes per counterfactual geometry, by stage) · V table (frequency curve + forward-return profile, baseline vs incremental) · A/B re-entry table · drought table (firings, admissibility under baseline vs candidate stops) · MTF: three registered confluences scored + the exploratory mining annex (clearly labeled) · advancement table scoring P-S1b · gov-ATR cluster table · birth-predictor descriptive table for mc≥2/mc=3 (mandate/asset/zone/grade/retr/stage/MTF-state composition). Every table: per-mandate splits, the intraday era caveat, first-order caveat headers, CIs on cohort expectancies (seed pinned, stated).

## 9. Verdict criteria

**PASS** — 8/8 fixtures; 9/9 predictions scored; both runs identical; tables complete with caveats.
**HALT** — F-BYTE or F-NULL failure (the instrument moved the experiment), F-P2REF mismatch (reader wrong), any fixture violation.
**PARTIAL** — a family not computable as specced: name the missing input, deliver the rest. No estimates.

## 10. Ledger templates

Pre-registration: phase, engine 1.0.9 scope (instrumentation-only + G-1; J-1 carried, disclosed), grids by count (24 ratchet, 6 dead-gate, 11 entry flags, 9 zone labels, 9 V variants, 4 add triggers, capture set 7 TFs), all nine predictions with priors, roots, "trading unchanged; F-BYTE is the proof."
Completion: fixtures, scorecard, hashes, artifact shas, "measurements only — no rule changed; Tier-C designs follow."

## 11. After this phase (for orientation, not execution)

The tables feed, in ratified order: **TC-1** (ratchet rebuild from the two-axis winner) → **TC-2** (re-entry quality bar from the bps-floor + A/B tables) → **TC-5** (1H/5m re-spec, already registered) → **TC-3** (V one-notch re-anchoring if the V table earns it) → aggressive-mode run (unlimited adds + 2.0R rail, with/without stand-down). Each Tier-C: own contract, own G-7 pre-registration, one at a time.

## 12. The go-paste

```
CONTRACT: S-1 — Instrumented Replay, Measure-Only (Tier B; engine 1.0.9 instrumentation-only)

Read S1_Instrumented_Replay_Builder_Contract.md in the repo in full before anything else.
The contract is the authority; this paste is the trigger.

Scope in one line: replay the 20 cells on the 1.0.8 ruleset with trading UNCHANGED,
emitting the s1 enrichment object on existing rows plus the sidecar event stream —
ratchet/harvest candidates, dead-gate triage, entry-geometry flags, zone shadows,
V-shadow, add-trigger and re-entry A/B families, MTF capture, advancement counts.
Byte-identity to journal_pass2 (F-BYTE) is the acceptance test. signals.py and
trading.py are byte-untouched.

Order of work — mandatory:

1. DEFINITIONS (contract §5). Restate in your own words: the two data channels, the
   emission-neutrality invariant, why candidate exit_r compares against the 0x line,
   the capture/noise-stopout scorecard, and what F-BYTE strips before comparing.

2. DATA PREP (contract §3.6). Build 30m and 1d locally by aggregation; run F-RESAMPLE
   checks; print the estate report. No network.

3. LEDGER PRE-REGISTRATION (contract §10) with all nine predictions. COMMIT before
   any run.

4. IMPLEMENT engine 1.0.9: enrichment/s1 module + sidecar writer + resampler + G-1
   lockbox code guard. git diff on engine/signals.py and engine/trading.py must be
   EMPTY. J-1 is explicitly out (it would perturb bytes and break F-BYTE) — carry it,
   disclosed.

5. RUN twice into research_outputs/s1/journal_s1/ (+_run2) and s1_events/. Expect the
   longest compute of the project; do not trim grids to save time (F-GRID).

6. FIXTURES (contract §6, all eight). F-BYTE first.

   *** F-BYTE OR F-NULL FAILURE = THE INSTRUMENT MOVED THE EXPERIMENT. HALT. ***

7. PREDICTIONS (contract §7, all nine). Falsifications as prominent as confirmations.
   The MTF mining beyond the three registered forms goes in a clearly-labeled
   exploratory annex — VR-1 exploration, hypothesis-generating only.

8. ARTIFACTS (contract §8) + completion ledger entry. Commit. Do not push, do not merge.

Do NOT, even if it seems helpful:
 - change any traded rule, config value, signal parameter, or zone geometry
 - let any s1 computation gate, suppress, add, or reorder main-journal rows
 - trim or extend any grid; substitute estimates for missing inputs
 - touch J-1, journal_pass1, journal_pass2, or the lockbox
 - fetch anything over the network

Report back: definitions restatement, estate report, fixture table, prediction
scorecard, s1_results.json, S1_MEASUREMENT.md. The reviewer verifies before any table
touches a variant slot.
```

---

## Appendix — Veto table (defaults stand on silence)

| # | A-priori choice | Default |
|---|---|---|
| V1 | Data channels | `s1` object on existing rows + sidecar stream; no other schema change |
| V2 | Family grids | As pinned in §3 (24/6/11/9/9/4; capture set 7 TFs) |
| V3 | G-1 rides 1.0.9 | **Yes** (byte-inert on valid runs; closes a register item). J-1 carried |
| V4 | Dead-gate N | {12h, 24h, 48h} wall-clock, mandate-converted; actions {kill, halve} |
| V5 | Emission-neutrality wording | As §4.1 (ratified 2026-07-18) |
| V6 | MTF mining pass | Exploratory under VR-1; three registered confluences scored, the rest annexed as hypotheses |

*Contract prepared by the reviewer under Fable-mode, 2026-07-18. Every family traces to a ratified operator ruling or a verified finding; every grid to a measured distribution (RC-3/RC-4) or the operator's stated practice. The acceptance test is the same discipline that caught nothing at TC-4 because there was nothing to catch — which is the only reason any of these numbers will deserve belief.*
