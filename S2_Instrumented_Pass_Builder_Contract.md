# S-2 — Instrumented Pass 2 (Corrected Simulator + Level/Pattern/Doctrine Families) — Builder Contract

**Phase:** v12 Study · **Tier B** — engine instrumentation + one full re-run. **Trading is UNCHANGED; any instrumentation that moves a traded number is a defect by definition.**
**Engine:** **1.0.10** (instrumentation-only release). Baseline for byte-identity: TC-4 `journal_pass2` traded columns (grid −1,796.9930 / +275.9924 / 2,599 / 10.8503%).
**Inherited by ruling (Amendments 1–2, operator-ratified sequence RC-7r → S-2 → TC-1):** the simulator **wake-order fidelity fix**; the **semantics-delta fixture**; **`c141t213` as a permanent regression tranche**; retired items **R7-1′** (two-line pricing — TC-1's prediction basis) and **R7-12′** (fill-bar bias); predictions **P-2L-a/b/c carried verbatim and still unseen**.
**New families (Report 4 + subsequent rulings):** F1 reject scoring · F2/F3 HTF levels · F4 structure-anchored stop · F5/F6 pattern detectors with registered sweeps · F7 sniper-pocket anatomy · F8 LTF test-and-reclaim in **relative steps** · FH-1 true-depth columns · FH-4 nesting definition grid.

---

## 0. Operator instructions

Same drill: save this contract into the repo → `claude` → `git status` clean, up to date → paste §12. *What you should see, in order:* (a) definitions restatement; (b) the **ledger pre-registration commit** (all predictions, before any run); (c) engine 1.0.10 implemented with unit tests, **including the `c141t213` regression test passing before the grid runs**; (d) the run, twice — **the largest compute of the project** (the reject-population family alone simulates ~230k counterfactual outcomes; hours are normal; leave it running); (e) the fixture table, all MATCH — **F-IDENT2 is the one to look at first** (explained in §7); (f) the scorecard and tables. Any fixture MISMATCH → halt, report, nothing downstream. Send back `s2_results.json`, `S2_MEASUREMENT.md`, the fixture table, the scorecard.

## 1. What this phase is

One instrumented replay on a **wake-order-faithful candidate simulator**, doing four jobs: (1) re-price the trail candidates and deliver the **corrected two-line table** TC-1 registers against; (2) score the **largest untested inheritance** — the zone gate's 229,963 rejected signals; (3) test the two discretionary tools the port left out — **HTF levels** and **pattern detection** — plus the **structure-anchored stop** (the operator's actual stop doctrine, mechanized for the first time); (4) measure the **LTF reclaim add family** and widen the **nesting census**. Everything lands as `s2` columns on existing rows plus sidecar events; the traded book does not move, and F-BYTE proves it.

## 2. What this phase is NOT

Not TC-1 (no rule trades differently) · not a slot decision · **not J-1** (the REJECT-row dataclass fix perturbs journal bytes and would blind F-BYTE — carried a third time, disclosed a third time) · not a zone-geometry redo (S-1's shadow stands) · not sizing adoption (all sizing sequenced post-TC-1 by measurement) · not free of first-order caveats — F4's counterfactual survival ignores rail/halt/equity feedback, F1's would-be outcomes ignore portfolio interaction; every such table prints its caveat header. **These tables rank; TC-1 validates.**

## 3. Engine 1.0.10 — the change set

### 3.1 Simulator wake-order fidelity (the two-halt fix)
`simulate_exit` re-derives candidate exits under the **engine's own event ordering**, per bar: **(1) queued open-flattens** — all five reasons: `failure_x`, `opposite_cross`, `v_reversal`, `equity_floor`, **`campaign_died`** — at the open; **(2) gap** fills at the open; **(3) intra-bar touch**; with **coverage from `fill_i`** (the fill bar included). The old `fill_i+1 / gap→touch→flatten` ordering is retained behind a flag solely for the semantics-delta fixture, then dead.

### 3.2 Regression tranche (permanent)
BTCUSDT_intraday **`c141t213`** under `ema89_gov_b0.0`: the corrected simulator must price the exit as the `campaign_died` open-flatten at **+0.0739R gross** — as a named unit test that runs before any grid run, forever.

### 3.3 Semantics-delta fixture machinery
A pinned tranche set (the 721-member fill-bar class + the 12 death-bar/tie tranches + 200 randomly-seeded controls, seed `20260721`): old-semantics re-pricing must reproduce the S-1 journaled candidate values exactly (proving the old path is faithfully preserved before comparison), then the corrected-vs-old delta per tranche feeds R7-12′.

### 3.4 Data channels
`s2` object on existing rows + `s2_events/<cell>.jsonl` sidecars. The S-1 `s1` columns are **not** re-emitted; analyses join `journal_s1` by `tranche_id` where needed. F-BYTE strips `s2` and the three run-identity stamps only.

## 4. The families

### R7-1′ — Two-line pricing, corrected (TC-1's prediction basis)
Candidates `ema200_gov_b0.5` (the ratified TC-1 form), `ema200_gov_b0.0`, `ema89_gov_b0.0`, priced under §3.1 semantics, **both architectures**: fold-in-frozen (engagement seeds at the standing phase-1 stop; no baseline floor after — the S-1 pinned rule, now on faithful bars) and **two-line** (exit at the earlier of the live native stop and the trail, per the engine's own event order — no derivation shortcut: the simulator walks both lines). Table: grid + per-mandate, 0× / 1×-proxy, **strip-best**, win rate, median capture, noise-stopout, adds-funnel column (== baseline by construction, reason printed), and the population census (identity classes, divergence classes).

### R7-12′ — Fill-bar bias quantification
On the 721-class: Σ(old-semantics candidate exit) vs Σ(engine-truth baseline), per candidate/mandate; the share where the old simulator rode a recovery; reconciliation to §3.3's per-tranche deltas. **This number becomes the standing correction footnote on every S-1 fold-in figure until superseded.**

### F1 — Reject-population scoring (the biggest gate finally faces its rejects)
For every `no_zone`-rejected PRIME signal row (**229,963** — fixture-pinned count): sidecar counterfactual — would-be entry at next open, standard stop formula (signal-bar extreme ∓ 0.5·ATR_exec), outcome under §3.1 semantics to first-touch / ±10R cap / {5, 20, 100}-bar horizons. Report per-unit distributions vs the admitted-R1 population, per mandate, per zone-that-would-have-been (join to S-1's zone shadow where present).

### F2 / F3 — HTF levels: context and events
**F2 (per entry and per signal row):** distance to nearest confirmed HTF pivot high/low above/below — pivots on {4h, 12h, 1d}, (L,R)=(5,5) — in that-TF ATR and in bps; level age (bars since confirm); retest count; **fresh flag** (0 touches); PDH/PDL/PWH/PWL distances (the zero-parameter control family); **headwind flag** = untested level within 0.5 that-TF-ATR against the trade direction. **F3 (sidecar):** every level retest and close-through with forward returns at the F1 horizon set — levels as standalone signals.

### F4 — The structure-anchored stop (doctrine vs port, priced at last)
Per tranche, three variants: stop at the **nearest confirmed pivot low (long) / high (short) beyond entry** on {exec, 30m, 1h}, (L,R)=(5,5), ∓ 0.5·ATR_exec; if no confirmed pivot within 200 detection-TF bars, variant void (null, counted). Counterfactual pricing under §3.1: new `one_r` denominator from the wider distance, survival and exit re-derived, per-unit gross/net-proxy, MFE-reached distribution, and the **shakeout-conversion count** (baseline noise-stopouts that survive to ≥+1R under the structural stop). First-order caveat mandatory (rail/halt/equity feedback ignored; sizing at the wider stop shrinks notional — print both R-basis and bps-basis views).

### F5 / F6 — Pattern detectors, with the four graduation bars
Detection TFs **30m and 1h** (existing frames; cross-scale replication leg on **4h**). Registered sweeps — every cell reported, none trimmed:
- **D1 range compression:** N-bar envelope < k×ATR(TF), N ∈ {20, 40, 80}, k ∈ {2, 3}; emits `range_active`, boundaries, `break_up/down`, `boundary_retest`.
- **D2 ribbon interweave:** |e9−e89| < x×ATR for ≥ M bars, x ∈ {0.15, 0.25}, M ∈ {10, 20}.
- **D3 pivot cluster:** ≥ P confirmed pivots within w×ATR band, P ∈ {3, 4}, w ∈ {0.5, 1.0}; envelope = zone.
- **D4 sweep-reclaim (PO3 core):** exceed an active D1/D3 boundary by ≤ y×ATR then close back inside within b bars, y ∈ {0.25, 0.5}, b ∈ {3, 5}.
Per entry: in-range flag, boundary distances, break-retest flag. Sidecar: all detector events with forward returns. **Graduation bars (F6, all four required):** label-level skill · sign-robustness across ≥⅔ of each sweep · incremental separation on top of the RC-7 lattice · **cross-scale sign replication 1h→4h at scale-relative parameters.**

### F7 — Sniper-pocket anatomy (generalized, n=60 warning in force)
For **every** D4 sweep-reclaim event at a qualifying level (traded or not): `pocket_top/bot`, `width_atr`, sweep depth (ATR and fraction-of-pocket), `reclaim_bars`, and — where a fill exists — `fill_depth_frac`. Deliverable: forward expectancy by penetration-depth decile with **monotonicity and sweep-robustness demanded**; no sub-band cherry-picking. The 60 A+ fills are reported as a (tiny) overlay, never as the estimator.

### F8 — LTF test-and-reclaim add family (relative steps)
While a tranche is open: a **test-and-reclaim event** = price penetrates the mapped e89 or e200 of the TF at governor-relative step **s ∈ {−1, −2, −3}** (per mandate: intraday → 30m/15m/5m; swing → 1h/30m/15m; position → 4h/1h/30m — **not 15m**, per the RC-7r preview), then exec-closes back beyond it within b ∈ {3, 5} exec bars. Fields: step, EMA, penetration depth in that-TF ATR, reclaim bars, admissibility under the baseline stop, forward outcome to campaign end. **The failure-depth hypothesis, registered in relative form:** penetration of the step−1 e200 *without* reclaim within b bars, while positioned, predicts campaign death.

### FH columns and the nesting grid
**FH-1 true depth:** per signal row, the actual active-band edges and tag depth *into the band* (in gov-ATR) — replacing RC-7r's stop-anchored proxy. **FH-4 definition grid:** the swing|intraday and position|swing conditionals recomputed under {active-at-birth · born-within-±N governor bars, N ∈ {6, 12, 24} · same-direction-armed}, per definition per asset, with the same-tape and overlap-era caveats printed.

## 5. Invariants

`engine/signals.py` and `engine/trading.py` **byte-untouched** (git diff empty; F-BYTE enforces behaviorally) · emission neutrality (the resolved/buffered decision byte-frozen at 1.0.8; `s2` never gates row emission; unresolvable → null on emitted rows) · two channels only · fresh roots `research_outputs/s2/` (+`_run2`, +`s2_events/`); all prior roots read-only · registered grids exact (F-GRID) · JTO/TAO 1d rows flagged `seed_biased`, excluded from 1d aggregates · relative-steps and dual-coordinate conventions on every MTF table · ledger pre-registration **before** the run · no network (all frames exist; no new resampling) · determinism: full run twice, identical.

## 6. Definitions

Carried verbatim: cell-R, R/unit, signed `one_r`, bps and toll, fill_class, `mfe_r`, steps-from-governor, capture/noise-stopout, the ±10R cap and {5,20,100} horizons. **New:** the §3.1 event order (the definition of "engine-faithful") · two-line = first touch of either line under that order · headwind (§F2) · pocket depth fraction = sweep depth ÷ pocket width · reclaim event (§F8) · detector parameters as gridded in §4 · void-vs-false (a condition that cannot be evaluated — no pivot, seed-biased 1d — is **void**, never false).

## 7. Fixtures — any MISMATCH halts the phase

| # | Fixture | Expected |
|---|---|---|
| F-BYTE | Strip `s2` + normalize 3 stamps → byte-identical to `journal_pass2`, rows/order, all 20 cells | identical |
| F-P2REF | Traded-column recompute | −1,796.9930 / +275.9924 / 2,599 / 10.8503% |
| F-REG | `c141t213` under `ema89_gov_b0.0`, corrected semantics | **+0.0739R** (the `campaign_died` open-flatten) |
| F-DELTA | Old-semantics re-pricing reproduces S-1 journaled candidate values on the pinned set | exact, before any comparison |
| **F-IDENT2** | **Two-line = fold-in on the FULL zero-advance population — fill-bar and death-bar classes included — under corrected semantics** | **0 violations** |
| F-F1N | F1 sidecar rows | 229,963 exactly |
| F-GRID | Family grids as registered | exact, no trims |
| F-EMIT | Unresolvable `s2` values null on emitted rows; no suppressed rows | 0 |
| F-DET | Double-run identity, journals + sidecars | identical |

**F-IDENT2 is the closure of the two-halt arc.** The original F3 claim was right about the algebra and wrong about the machine; 1.0.10 makes the machine agree with the algebra — and the claim returns as a *full-population* fixture, adjudicated by the simulator rather than asserted by the reviewer. If it fails, something else is unfaithful: halt, report, no pricing.

## 8. Pre-registered predictions

| # | Prediction | Prior | Falsified if |
|---|---|---|---|
| P-2L-a *(carried)* | Two-line grid gross (b0.5) ∈ [500, 650] | 55% | outside |
| P-2L-b *(carried)* | Two-line position 1×-proxy ≥ +300 | 65% | below |
| P-2L-c *(carried; vs corrected fold-in)* | Two-line ≥ fold-in on ≥45% of the advancing population | 55% | <45% |
| P-SD | Corrected fold-in grid 0× < the pinned +584.50 (the old simulator rode fill-bar recoveries) | 65% | ≥ |
| P-F1 | `no_zone` would-be per-unit net < admitted-R1 per-unit net (the biggest gate filters noise, not signal) | 60% | ≥ |
| P-F4 | The 30m structure-stop variant's first-order grid 1× beats the baseline grid 1× | 55% | worse |
| P-PD1 | Boundary-retest entries outperform mid-range entries by ≥ +0.25R | 60% | < |
| P-PD2 | D4 sweep-reclaim events carry positive standalone forward mean | 60% | ≤ 0 |
| P-PD3 | Z2's deficit concentrates in-range: Z2-in-range worse than Z2-out-of-range by ≥ 0.3R | 55% | < |
| P-PD4 | ≥1 detector passes sign-robustness (≥⅔ of sweep) AND 1h→4h sign replication | 60% | none |
| P-F8 | Step −1/−2 reclaim-while-positioned mean ≥ +0.10R; unreclaimed step−1 e200 penetration separation ≤ −0.3R | 55% / 55% | either half |
| P-F2 | Headwind entries underperform by ≥ 0.2R | 55% | < |
| P-NEST | Some widened definition yields swing\|intraday conditioned n ≥ 80 with separation ≥ +0.5R | 50% | none |

## 9. Verdict criteria

**PASS** — 9/9 fixtures; 13/13 rows scored, falsifications first; determinism proven; every caveat header printed. **HALT** — any fixture MISMATCH (F-IDENT2 and F-REG are the two that would indict the fix itself). **PARTIAL** — a family not computable as specced: name the missing input, deliver the rest, no estimates.

## 10. Artifacts + ledger

`engine/` diffs (1.0.10) · `scripts/s2_fixtures.py` incl. the regression test · `research_outputs/s2/` roots + sha manifest · `s2_results.json` · `S2_MEASUREMENT.md` · two ledger entries (pre-registration with all 13 rows and the grids; completion with fixtures, scorecard, hashes, and the line *"R7-1′ delivered — TC-1 registers against this table"*). Commit; **do not push, do not merge**.

## 11. Veto table (defaults stand on silence)

| # | Choice | Default |
|---|---|---|
| V1 | Data channels (`s2` + sidecar; s1 joined, not re-emitted) | As §3.4 |
| V2 | Detector grids | As §4 (D1 3×2 · D2 2×2 · D3 2×2 · D4 2×2; TFs 30m/1h, replication 4h) |
| V3 | F8 steps {−1,−2,−3}, b ∈ {3,5}, EMAs {89, 200} | As §4 |
| V4 | F4 pivot (L,R)=(5,5), variants {exec, 30m, 1h}, 200-bar void rule | As §4 |
| V5 | Nesting N ∈ {6, 12, 24} governor bars | As §4 |
| V6 | Headwind threshold 0.5 that-TF-ATR | As §F2 |
| V7 | F1 horizons {5, 20, 100} bars, ±10R cap | As §6 |
| V8 | J-1 carried (third time, bytes) | Out, disclosed |

## 12. The go-paste

```
CONTRACT: S-2 — Instrumented Pass 2 (Tier B; engine 1.0.10 — corrected simulator + new families)

Read S2_Instrumented_Pass_Builder_Contract.md in the repo in full first. The contract is
the authority; this paste is the trigger.

Scope in one line: replay the 20 cells with trading UNCHANGED on a wake-order-faithful
candidate simulator; deliver the corrected two-line table (TC-1's prediction basis),
score the zone gate's 229,963 rejects, price the structure-anchored stop, run the level
and pattern-detector families, the LTF reclaim family in relative steps, and the widened
nesting grid. F-BYTE proves nothing traded moved.

Order of work — mandatory:

1. DEFINITIONS (contract §6). Restate in your own words: the §3.1 engine event order and
   why it is the definition of faithful; two-line under that order; void-vs-false; the
   four detector graduation bars; relative steps per mandate for F8.

2. LEDGER PRE-REGISTRATION — all 13 prediction rows (three carried verbatim-unseen),
   all grids. COMMIT before implementing anything.

3. IMPLEMENT engine 1.0.10 per §3. Unit tests first — the c141t213 regression test
   (+0.0739R) MUST pass before any grid run. git diff on signals.py and trading.py
   must be EMPTY. J-1 stays out (bytes), disclosed.

4. F-DELTA before the main run: prove the old semantics are faithfully preserved on the
   pinned set, exactly, or the bias comparison is meaningless.

5. RUN twice into research_outputs/s2/. Largest compute of the project (~230k
   counterfactual outcome simulations in F1 alone); do not trim grids to save time.

6. FIXTURES (contract §7). F-IDENT2 first in the report.

   *** F-IDENT2 OR F-REG FAILURE INDICTS THE FIX ITSELF: HALT, REPORT, PRICE NOTHING. ***

7. DELIVERABLES per §4 with every caveat header; relative-steps and dual coordinates on
   all MTF tables; JTO/TAO 1d flagged and excluded; void never counted as false.

8. PREDICTIONS — all 13, falsifications first. ARTIFACTS + both ledger entries per §10.
   Commit. Do not push, do not merge.

Do NOT, even if it seems helpful: change any traded rule or config · re-emit or modify
s1 columns · let any s2 computation gate row emission · trim or extend any grid · touch
J-1, the lockbox, or any prior journal root · fetch anything over the network ·
substitute estimates for missing inputs.

Report back: definitions restatement, fixture table (F-IDENT2 first), the family tables,
the 13-row scorecard, both hashes, s2_results.json. The reviewer verifies before TC-1
cites a single number.
```

---

*Contract prepared by the reviewer under Fable-mode, 2026-07-19. The two-halt arc ends where it should: the claim that broke twice returns as F-IDENT2, judged by a machine that now walks bars in the order the engine does — and `c141t213` stands in the fixture set as the tranche that taught it. Thirteen predictions, three of them written before the halts and never yet seen; eight families, two of them the operator's own hands finally rendered testable. TC-1 waits on the other side of this table.*
