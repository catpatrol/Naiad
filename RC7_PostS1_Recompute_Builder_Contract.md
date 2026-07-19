# RC-7 — Post-S-1 Recompute — Builder Contract

**Phase:** v12 Study · **Tier A** (arithmetic over existing S-1 journals + sidecars). **No engine execution, no config change, no network, no evidence spend** (VR-1; the S-1 first look is consumed).
**Basis:** S-1 journals (`research_outputs/s1/journal_s1/` + `s1_events/`), engine 1.0.9, verified PASS 2026-07-18; baseline traded columns byte-identical to TC-4 (`journal_pass2`). Baseline headline: **−1,796.9930 / +275.9924 / 2,599 campaigns / 10.8503%**.
**Operator ratifications in force (2026-07-19):** D-2 = **two-line** exit architecture for TC-1 (this phase prices it — the S-1 +584/+389 figures are fold-in-frozen, a different form); D-1, D-3…D-11 defaults; D-12 closed (30m as-of proven clean; **JTO/TAO 1d rows are seed-biased → flag + exclude from 1d aggregates**); confluence-graded sizing as pre-registered count tiers; LTF reclaim-proxy preview approved; fractal program FH-1…FH-4; dual-coordinate MTF reporting convention; full-symmetry confluence matrix (the 15m guarantee).

---

## 0. Operator instructions

Same drill, short version: save this contract into the repo → `claude` → `git status` clean → paste §12. *What you should see:* a definitions restatement, then a fixture table where **all eight say MATCH** (the two-line **identity fixture** especially — if it fails, the reviewer's derivation is wrong and the phase halts), then eleven deliverable tables, then a scorecard of nine predictions. Runtime: minutes. Send back `rc7_results.json`, the fixture table, the scorecard.

## 1. What this phase is

Eleven measurements from data already on disk. Three jobs: (1) **price the two-line exit** the operator just ratified, so TC-1's predictions register against numbers instead of hope; (2) close every open verification from Reports 3–4 (strip-best concentration, the joint lattice, per-mandate/era splits, full-symmetry MTF matrix); (3) run the **fractal census** FH-1…FH-4 and the sizing sweeps. Everything feeds the TC-1 contract and the modes interview.

## 2. What this phase is NOT

Not a run (nothing executes), not TC-1 (no rule changes), not S-2 (no new instrumentation — F7/F8 need engine columns and are S-2's), not a slot decision, not a validation of anything (in-sample, first-order, ranks-only — standing caveats print on every table).

## 3. Invariants

Read-only everywhere · scored basis = the 20-cell S-1/TC-4 grid · **JTO/TAO excluded from all 1d-row aggregates** (reported separately, flagged `seed_biased`) · every R aggregate at 0×/1×(proxy where counterfactual)/2× · strip-best on every campaign-level aggregate · 95% bootstrap CIs, 10,000 resamples, seed `20260720`, stated · **dual coordinates on every MTF table** (absolute TF and steps-from-governor) · determinism: script run twice, hashes identical · predictions scored verbatim, falsifications first.

## 4. Definitions — pin before coding

Carried verbatim from prior contracts: cell-R, R/unit, signed `one_r`, `r_0x`/`r_2x`, bps conversions, toll (14/20/30 by tier), fill_class, direction-run, `mfe_r` (per-unit, stop-denominated).

**New this phase:**

- **Two-line exit (per tranche, per trail candidate):** the position exits at the **earlier** of the baseline exit and the candidate trail exit. Mechanically: if `candidate.exit_i_offset` places the trail exit **strictly before** the baseline exit bar → two-line result = candidate (`exit_XL_r = candidate.exit_r`, gross basis); **ties and all other cases → baseline** (`exit_XL_r = realized_r ÷ size_r`, i.e., the journaled outcome, which for stop exits already reflects the live native ratchet). Same-bar tie resolves to baseline (conservative). Non-stop baseline exits (failure-X, opposite-cross, equity-floor: ~0.3%) taken as-is. Gap fills inherit each path's own journaled semantics. Candidates priced: `ema200_gov_b0.5` (the ratified TC-1 form), plus `ema200_gov_b0.0` and `ema89_gov_b0.0` for context.
- **Identity population:** tranches with `s1.advance.n_stop_advances = 0` (~90% expected). On this population frozen = live, therefore **two-line must equal the fold-in candidate exactly** (same exit bar, same R) — fixture F3. This equality is the proof of the derivation; it is not optional.
- **Confluence count (for R7-9b):** number of TRUE among the fixed, pre-named set {30m structure aligned at entry; NOT beyond 1d-e200 at entry (JTO/TAO → condition void, not false); stop_bps ≥ 2×toll}. Tiers: count 0 → ×0.5 · 1 → ×1.0 · 2 → ×1.5 · 3 → ×2.0. **Weights are registered here, not fitted.**
- **Steps-from-governor:** exec = −G steps … governor = 0 … 1d = +K, per mandate's ladder {exec,15m,30m,1h,4h,12h,1d} (positions differ by mandate; print the mapping once per table).
- **Flip-while-positioned (R7-10 proxy):** an mtf-cross sidecar event of the stated TF and direction occurring inside a tranche's open interval. **Label as proxy** — a cross is not a test-and-reclaim; S-2 F8 measures the real thing.

## 5. Fixtures — any MISMATCH halts the phase

| # | Fixture | Expected |
|---|---|---|
| F1 | Baseline recompute from S-1 traded columns (1× / 0× / campaigns / win) | −1,796.9930 / +275.9924 / 2,599 / 10.8503% |
| F2 | Sidecar family counts | re-entry 69,395 · add_trigger 29,270 · mtf_cross 5,267 · v_shadow 3,978 |
| F3 | **Two-line identity** on the zero-advance population, per candidate | exit bar and R equal to fold-in, **0 violations** |
| F4 | Lattice marginal reconciliation: the 30m-aligned split re-derived from lattice rows | −0.549 / −0.939, n 1,650 / 949 |
| F5 | fill_class census | r1 2,456 · true_add 888 · re_entry 2,928 · v 32 |
| F6 | Zero-advance population share | 90.35% (±0.01) of the ≥1R-MFE gross-loser definition set; also report grid-wide share |
| F7 | Coverage: confluence matrix cells emitted | 7 TFs × 3 conditions × 3 mandates × 2 coordinate systems, no omissions (the completeness rule) |
| F8 | Determinism | double-run hashes identical |

## 6. Deliverables

**R7-1 — Two-line pricing table** (the phase's headline). Per candidate × {GRID, swing, intraday, position}: Σ 0×, Σ 1×-proxy, strip-best, win rate, median capture, noise-stopout, and the three-way comparison **baseline vs fold-in vs two-line**; plus the advancing-population split (how often two-line beat / matched / trailed fold-in, and by how much). Caveats printed: first-order; cost proxy; funding-understated-on-long-holds.
**R7-2 — Per-candidate strip-best** for all 24 fold-in candidates (closes Report 3's position-concentration question; position rows first).
**R7-3 — Full symmetric confluence matrix.** Every capture TF × {s2_aligned, beyond_e200, beyond_e89} × per-mandate × dual coordinates; pooled column retained; JTO/TAO 1d rows separate + flagged. This delivers the 15m guarantee — the never-printed `15m_s2_aligned` split included.
**R7-4 — FH-3 discriminator.** The aligned-separation gradient per mandate in steps-from-governor. **Registered verdict rule:** "RELATIVE" if the peak-separation TF sits within ±1 step of the same relative position in ≥2 of 3 mandates; "ABSOLUTE" if 30m peaks in all three; "MIXED" otherwise. The verdict gates C13b's form (repoint-to-30m vs repoint-to-"two-steps-below-governor").
**R7-5 — Joint lattice.** 2×2×2 {30m-aligned × 1d-room × toll-payable}, per mandate + grid, R1-only companion; n, expectancy, CI, Σ, share-of-Σwins per cell.
**R7-6 — FH-1 signal-shape census** per mandate: signal mix per 100 governor bars, retracement quantiles, zone-tag depth in gov-ATR — normalized comparison table.
**R7-7 — FH-2 R-space anatomy** per mandate: `mfe_r`/`mae_r` deciles, PROTECTED shares, winners' capture distributions — the scale-invariance test in the units where fractality would live.
**R7-8 — FH-4 nesting census** per asset: cross-mandate campaign co-occurrence and direction agreement at birth; swing-campaign expectancy conditioned on a same-direction intraday campaign active at its birth (and position | swing). Print the same-tape dependence caveat.
**R7-9 — Sizing sweeps (first-order re-weights only).** (a) Mandate multiplier: M_intraday ∈ {0.25, 0.5, 1.0} × M_position ∈ {1.0, 1.5, 2.0}, swing = 1, with a separate add-size multiplier column. (b) Confluence-count tiers per §4, grid + per-mandate. Caveat header: re-weighting ignores rail/halt/equity-path feedback; the modes interview and a config-only Tier-C own adoption.
**R7-10 — Trigger previews from the existing sidecar** (all labeled PROXY): 30m flips-while-positioned; 15m/30m flips-while-positioned (the LTF-reclaim preview); 1h flips-against-while-positioned (the failure-depth preview) — forward outcomes, counts, per-mandate, dual coordinates.
**R7-11 — Adds-funnel dual print:** baseline funnel (984 admitted / 716 rejected) beside each trail candidate's `adds_would_be_eligible`, with the two-line column = baseline's by construction (state why).

## 7. Pre-registered predictions

| # | Prediction | Prior | Falsified if |
|---|---|---|---|
| P-2L-a | Two-line grid gross (ema200_gov_b0.5) ∈ [500, 650] | 55% | outside |
| P-2L-b | Two-line position 1×-proxy ≥ +300 | 65% | below |
| P-2L-c | On the advancing population, two-line ≥ fold-in on ≥45% of tranches (the earlier-native-exit sometimes helps) | 55% | <45% |
| P-STRIP | Position's best trail candidate remains net-positive (1×-proxy) after strip-best | 60% | flips negative |
| P-LAT | Triple-TRUE lattice cell ≥ +0.8R above triple-FALSE, and ≥ −0.2 expectancy | 60% | either fails |
| P-FH1 | Signal-shape distributions match across mandates after normalization (no median shift > 25%) | 65% | any shifts |
| P-FH2 | `mfe_r` deciles match across mandates within ±20% at the median and 75th pct | 60% | outside |
| P-FH3 | Verdict = RELATIVE | 55% | ABSOLUTE or MIXED |
| P-FH4 | Co-occurrence enrichment ≥ 2× base rate; conditional-outcome separation ≥ +0.3R | 75% / 55% | either half |
| P-PRVW | 15m/30m flips-while-positioned mean outcome > 0; 1h flips-against separation ≤ −0.2R | 60% / 55% | either half |

## 8. Verdict criteria

**PASS** — 8/8 fixtures, 11/11 deliverables with caveat headers, 10/10 prediction rows scored, determinism proven. **HALT** — any fixture MISMATCH; **F3 especially: an identity violation means the two-line derivation itself is wrong — report the violating tranches, price nothing.** **PARTIAL** — a field genuinely absent: name it, name its row, no estimates.

## 9. Output artifacts

`scripts/rc7_recompute.py` · `RC7_RESULTS.md` · `rc7_results.json` · ledger entry (builder-typed, append-only).

## 10. Ledger template

```
[YYYY-MM-DD] RC-7 POST-S1 RECOMPUTE — Tier A, journals+sidecars only
Basis: S-1 journals (engine 1.0.9), baseline = TC-4 pass2. Evidence spend: NONE.
Fixtures F1–F8 [..]  Predictions P-2L-a/b/c, P-STRIP, P-LAT, P-FH1..4, P-PRVW [..]
FH-3 verdict: [RELATIVE/ABSOLUTE/MIXED] → gates C13b form
Two-line (ema200_gov_b0.5): grid 0x [..] / 1x-proxy [..] / strip-best [..] → TC-1 prediction basis
Artifacts: scripts/rc7_recompute.py, RC7_RESULTS.md, rc7_results.json
Next: TC-1 contract (two-line, registered against R7-1); S-2 contract (F1–F8 incl. F7 pocket anatomy, F8 LTF reclaim)
```

## 11. Veto table (defaults stand on silence)

| # | Choice | Default |
|---|---|---|
| V1 | Two-line tie convention (same-bar → baseline) and non-stop-exit handling (as-is) | As §4 |
| V2 | Confluence-tier weights {0.5, 1.0, 1.5, 2.0} by count | As §4 (registered, not fitted) |
| V3 | FH-3 verdict rule | As R7-4 |
| V4 | JTO/TAO 1d handling | Flag + exclude from 1d aggregates, report separately |
| V5 | Candidates priced for two-line | The three named (TC-1 form + two context forms) |

## 12. The go-paste

```
CONTRACT: RC-7 — Post-S-1 Recompute (Tier A — journals + sidecars only)

Read RC7_PostS1_Recompute_Builder_Contract.md in the repo in full first. The contract
is the authority; this paste is the trigger.

Scope in one line: eleven tables from the existing S-1 journals and sidecars — price
the ratified two-line exit, close the open verifications, run the fractal census and
the sizing sweeps. Read-only. No engine execution, no config changes, no network.

Order of work — mandatory:

1. DEFINITIONS (contract §4). Restate in your own words: the two-line exit rule
   including the tie convention, the identity population and WHY equality there is a
   proof of the derivation, the confluence count with its registered tiers, and
   steps-from-governor. Do not proceed until written out.

2. FIXTURES (contract §5, F1–F8), raw bytes only, no prior report as input.

   *** ANY MISMATCH: HALT. F3 (two-line identity) especially — a violation means the
       derivation is wrong; report the violating tranches and price NOTHING. ***

3. DELIVERABLES R7-1..R7-11 (contract §6), caveat headers printed, dual coordinates on
   every MTF table, JTO/TAO 1d rows flagged and excluded from 1d aggregates, the
   completeness rule on the confluence matrix (F7).

4. PREDICTIONS (contract §7), all ten rows, falsifications first.

5. DETERMINISM: run twice, print both hashes.

6. ARTIFACTS (contract §9) + ledger entry (§10). Commit. Do not push, do not merge.

Do NOT, even if it seems helpful: execute replay or any engine code · modify anything ·
fit confluence weights or any parameter to outcomes · trim the matrix to "interesting"
cells · substitute estimates · touch the lockbox.

Report back: definitions restatement, fixture table, the eleven tables, the scorecard,
both hashes, rc7_results.json. The reviewer recomputes independently before TC-1's
contract cites a single number from this phase.
```

---

*Contract prepared by the reviewer under Fable-mode, 2026-07-19. The two-line derivation in §4 is the reviewer's; fixture F3 exists to let the data veto it. The FH-3 verdict rule is registered before anyone sees the per-mandate gradient — which is the only honest order. Eleven tables, zero new evidence spent, and at the end of it TC-1 registers its predictions against measurements instead of adjectives.*
