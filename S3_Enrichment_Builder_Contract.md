# S-3 — Cell-B Enrichment & Cross-Run Excursion Substrate — Builder Contract

**Phase:** v12 Study · **Tier B** (instrumentation only — trading UNCHANGED; any capture that moves a traded number is a defect). **Engine: 1.0.11** (the TC-1 engine; no logic change — S-3 turns the `s2`-style capture block **on** over the cell-B configuration).
**Basis:** TC-1 verified PASS, cell-B (`research_outputs/tc1/B/`), engine 1.0.11, structural-stop architecture. Builder confirmed (2026-07-20): cell-B journals carry `retr` and the 1.0.8 base fields but **no `s2` capture block** (emission was off); a re-run with capture on leaves traded columns **byte-identical** (empirically checked: 918 rows, 0 differences after stripping capture + normalizing the 3 run-identity stamps).
**Two operator principles in force (2026-07-20), both load-bearing here:**
- **P-CIRC (the circular-topology diagnosis):** the pyramid did not fail; a *coupling* failed — the add gate depends on the ratchet, the ratchet on a new PRIME, the PRIME on a pullback the trend withholds. The redesign will **break the dependency**, keeping "add to a winner" as a cornerstone. S-3 must therefore capture, at every winning moment, the *independent* (non-PRIME) conditions an add could have keyed on.
- **P-KEEP (data is permanent evidence):** no run is discarded as flawed-system output. Excursion (how far price ran favorably/adversely after a trigger) is architecture-independent and outlives every stop/exit choice. S-3 builds the **cross-run comparison substrate** so S-1, TC-1's arms, S-3, and every future iteration can be joined and compared — including to detect *deterioration* and read its cause from the excursion record.

---

## 0. Operator instructions

Save this contract into the repo → `claude` → `git status` clean → paste §11. *What you should see, in order:* (a) definitions restatement; (b) the **G-7 pre-registration commit** (config sha + all prediction rows, before any run); (c) engine confirmed unchanged + capture toggled on; (d) the cell-B re-run, twice for determinism (fast — one config, not the full grid); (e) fixtures, all MATCH — **F-BYTE first** (traded columns unmoved); (f) the deliverable tables and the scorecard. Any fixture MISMATCH → halt, report, produce nothing downstream. Send back `s3_results.json`, `S3_ENRICHMENT.md`, the fixture table, the scorecard.

## 1. What this phase is

An instrumented re-run of the **winning** book (cell-B, the structural stop) that finally writes the rich per-trade record TC-1 never emitted, doing five jobs: (1) the **per-trade anatomy** the operator asked for — which trades reached profit, which reversed, by how much (point-3 table, on the winning book); (2) the **retracement-depth study** — which pullback depth pays, at full sample (the oldest open question); (3) **re-score every known confluence on the B book** — the signals were measured on a losing book; re-price them on a winning one; (4) **P-CIRC capture** — the decoupled-add evidence: at every +1R moment, the full independent signal/structure state; (5) **P-KEEP substrate** — a keyed, architecture-independent excursion table built to join S-1, all TC-1 arms, and future runs. Trading does not move; F-BYTE proves it.

## 2. What this phase is NOT

Not a rule change (no trading logic differs; this is the same 1.0.11 that produced cell-B, capture on) · not the census (the multi-governor MTF-stack study is the *next* phase; S-3 is enrichment on one existing book, Mode A) · not a new-add-mechanism test (S-3 gathers the raw material to *design* a decoupled add; testing one is a later Tier-C) · not a slot decision · not free of the in-sample / first-order caveats (everything here describes the exploration-classic window under the current entries; it ranks and reveals, it does not validate out-of-sample).

## 3. Engine 1.0.11 — capture toggled on (no logic change)

The TC-1 runner calls `run_replay` **with** the capture params (`s2_sidecar_root` set) over the `tc1_B` config. `signals.py` and `trading.py` byte-untouched (git diff empty; F-BYTE enforces behaviorally). The capture block extends the existing `s2` family (S-2's MTF capture) with the P-CIRC and excursion-substrate fields below. J-1 stays out a **fifth** time (byte-identity requires it), disclosed.

## 4. Definitions — pin before coding

Carried verbatim: cell-R, R/unit, signed `one_r`, 0×/1×/2×, toll, fill_class, `mfe_r`/`mae_r` (per-unit, stop-denominated), strip-best, steps-from-governor, dual coordinates, capture/noise-stopout.
**New this phase:**
- **Reached-profit tiers:** per tranche, the peak favorable excursion (MFE) bucketed at {<0, 0–0.5R, 0.5–1R, 1–2R, 2–3R, ≥3R} — the "how far up before reversing" axis the operator asked for.
- **Reversal classification:** for tranches that reached ≥+1R MFE and exited at a loss — the MFE tier reached before reversing, and whether the stop advanced at all before the peak (the PROTECTED-paradox measure, now on the B book).
- **`retr` (already journaled):** the arming-leg retracement depth at entry (fraction of the impulse), per tranche — the pocket-depth axis.
- **P-CIRC state block (new capture):** at the **first bar each tranche's MFE reaches ≥+1R**, journal the full independent-signal snapshot — every one of {9/89, 89/200} cross state and bars-since, EMA-position of price on each captured TF, ribbon separation, whether a PRIME/CONFIRM was *available* that bar — i.e., the conditions a *non-PRIME* add trigger could have keyed on. Purpose: raw material for a decoupled add gate. (The 9/200 cross is a census addition — **not** required here; note if trivially available, do not add a security call for it.)
- **Excursion substrate (new, P-KEEP):** one row per tranche, architecture-independent, keyed for future joins: `run_id`, `arm_id` (A/B/C/D/S1/…), `cell`, `tranche_id`, `trigger_type` (PRIME-R1 / PRIME-add / CONFIRM / C / V), `grade`, `entry_zone`, `retr`, `dir`, and the **excursion path in BOTH bases** — MFE and MAE in **bps** and in **entry-ATR**, at horizons {10, 20, 50, 100 exec bars} and at exit. The join key is `trigger_type × grade × entry_zone × dir`, so any two runs can be laid side by side by trigger character.

## 5. Fixtures — any MISMATCH halts

| # | Fixture | Expected |
|---|---|---|
| F-BYTE | Strip the capture block + normalize 3 stamps → cell-B traded columns byte-identical to the committed `tc1/B` journal, all cells | identical |
| F-P2REF | Cell-B headline recompute (traded) | matches TC-1 cell-B: grid 1× −351.15, 0× +1,164.42, 7,094 tranches, 21.33% win |
| F-CIRC-N | P-CIRC snapshots emitted = count of tranches reaching ≥+1R MFE | equals the reached-≥1R tranche count (no missing/extra) |
| F-SUB | Excursion-substrate row count = total resolved tranches; every row carries both bps and ATR excursion at all horizons | 0 nulls on resolved rows |
| F-DET | Double-run identity, journals + sidecars | identical |

## 6. Deliverables

**D1 — The per-trade anatomy table (point-3, on the winning book).** Cell-B, grid + per-mandate: reached-profit tier histogram; of the ≥+1R population, the reversal classification (reached-then-lost by MFE tier, and the zero-stop-advance share — the PROTECTED paradox on B); win rate by exit reason; median capture of peak. **Print it beside the S-1 (baseline/arm-A) equivalent** so the two books' anatomy sits side by side — the headline comparison the operator asked to see.
**D2 — Retracement-depth expectancy.** Expectancy and MFE by `retr` decile, cell-B, grid + per-mandate, with strip-best and CIs. **The pocket question at full n:** does a band around 0.618–0.786 outperform, and is the effect sign-stable across the decile sweep? Overlay the 60 A+ fills as a (tiny) reference, never as the estimator.
**D3 — Confluence re-scored on B.** The RC-7r joint lattice (30m-aligned × 1d-room × toll-payable) and the full symmetric confluence matrix, **recomputed on the cell-B book**, dual coordinates, per mandate. The question P-KEEP-relevant: which confluence conditions that were negative-but-separating on the losing book are **positive** on the winning one.
**D4 — P-CIRC decoupled-add evidence.** From the +1R-moment snapshots: the frequency of each independent condition (non-PRIME cross states, EMA positions, ribbon states) at winning moments, and — crucially — how often a *pullback-reclaim PRIME was NOT available* at those moments (quantifying the circular freeze directly: the share of winning moments the current add gate structurally could not fire). This is the measured basis for a decoupled add trigger; it designs nothing, it reveals the opportunity.
**D5 — The cross-run excursion substrate.** The keyed table (§4), delivered as `s3_excursion_substrate.jsonl` plus a summary pivot: MFE/MAE (bps and ATR) by `trigger_type × grade × entry_zone`, cell-B. **Include the same pivot computed for S-1 and TC-1 arm A if their journals already carry joinable excursion** (see §8 — if not, the substrate ships cell-B-only and the back-fill is a named follow-up). Purpose per P-KEEP: the permanent comparison layer.
**D6 — One paragraph for the record:** the anatomy delta between the losing book (S-1/A) and the winning book (B) — did the structural stop change the *shape* of how trades win and lose, or just widen the graveyard? The single most important qualitative read of the phase.

## 7. Pre-registered predictions

| # | Prediction | Prior | Falsified if |
|---|---|---|---|
| P-S3-1 | On the B book, the zero-stop-advance share among ≥+1R-then-loss tranches is < the baseline's 90.35% (the static structural stop changes the reversal pathology) | 60% | ≥ 90.35% |
| P-S3-2 | A `retr` band within 0.5–0.8 shows higher expectancy than the shallowest and deepest deciles, sign-stable across the sweep | 55% | not sign-stable, or no mid-band lift |
| P-S3-3 | At least one confluence condition negative on the S-1 book is **positive** on the B book (lattice or matrix) | 60% | none flips positive |
| P-S3-4 | ≥ 50% of +1R winning moments had **no** pullback-reclaim PRIME available that bar (the circular freeze is common, not rare) | 65% | < 50% |
| P-S3-5 | B-book winners' median peak-capture > the baseline's ~6% (wider stop lets winners run further before exit) | 60% | ≤ 6% |

## 8. Builder check embedded (answer in the pre-registration ledger, before the run)

State whether the **S-1 journals** and **TC-1 arm-A journals** carry per-tranche MFE/MAE at fixed horizons in a form joinable to the §4 substrate key. If yes: D5 includes them. If no: D5 ships cell-B-only, and a **back-fill re-emission pass** (re-run S-1 and arm-A with the excursion substrate on — byte-safe, same as this phase) is named as the immediate P-KEEP follow-up. This is the "intermediate step" the operator pre-authorized walking through.

## 9. Verdict criteria

**PASS** — 5/5 fixtures, 6/6 deliverables with caveat headers, 5/5 predictions scored falsifications-first, determinism proven. **HALT** — any fixture MISMATCH; **F-BYTE especially — if a traded column moved, the capture is not inert and nothing is trustworthy.** **PARTIAL** — a deliverable blocked by a genuinely absent field (e.g. S-1 excursion for D5): name it, deliver the rest, no estimates.

## 10. Artifacts + ledger

`scripts/s3_enrich.py` · `research_outputs/s3/` roots (+`_run2`) · `s3_results.json` · `s3_excursion_substrate.jsonl` · `S3_ENRICHMENT.md` · two ledger entries (G-7 pre-registration with all 5 rows, the config sha, and the §8 answer; completion with fixtures, scorecard, and the line *"cross-run excursion substrate live — P-KEEP comparison layer established"*). Commit; **do not push, do not merge.**

## 11. The go-paste

```
CONTRACT: S-3 — Cell-B Enrichment & Cross-Run Excursion Substrate (Tier B; engine 1.0.11, capture on, no logic change)

Read S3_Enrichment_Builder_Contract.md in the repo in full first. The contract is the
authority; this paste is the trigger.

Scope in one line: re-run the winning cell-B book with the capture block ON — write the
per-trade anatomy TC-1 never emitted, the retracement-depth study, the confluences
re-scored on a winning book, the decoupled-add (P-CIRC) evidence, and the permanent
cross-run excursion substrate (P-KEEP). Trading is UNCHANGED; F-BYTE proves it.

Order of work — mandatory:

1. DEFINITIONS (contract §4). Restate in your own words: the reached-profit tiers and
   reversal classification; the P-CIRC +1R-moment snapshot and why it is the raw
   material for a decoupled add gate; the excursion substrate and its join key.

2. G-7 PRE-REGISTRATION — the config sha, all 5 prediction rows, AND the §8 answer
   (whether S-1 / arm-A journals carry joinable excursion). Commit BEFORE the run.

3. CONFIRM engine unchanged (signals.py + trading.py git diff EMPTY) and toggle the
   capture params on over the tc1_B config. J-1 stays out (fifth carry, disclosed).

4. RUN cell-B twice into research_outputs/s3/. One config, not the grid — fast.

5. FIXTURES (§5), F-BYTE first.

   *** F-BYTE FAILURE: HALT — a moved traded column means the capture is not inert.
       Report, produce nothing. ***

6. DELIVERABLES D1–D6 (§6): the anatomy table beside S-1's, the retr-decile study, the
   confluence re-score on B, the P-CIRC evidence, the excursion substrate. Every table:
   in-sample/first-order caveat, denominator stated (struct-R on B).

7. PREDICTIONS (§7), all 5, falsifications first. ARTIFACTS + both ledger entries (§10).
   Commit. Do not push, do not merge.

Do NOT, even if it seems helpful: change any traded rule or config value · add a
security call for the 9/200 cross (that is the census's job) · design or test a new add
mechanism (S-3 reveals the opportunity; it does not build it) · touch J-1, the lockbox,
or any prior journal root · substitute estimates for absent fields.

Report back: definitions restatement, the §8 answer, fixture table (F-BYTE first), D1
beside S-1, D2–D6, the 5-row scorecard, both hashes, s3_results.json.
```

---

*Contract prepared by the reviewer under Fable-mode, 2026-07-20. S-3 does three things at once that the operator's two principles demand: it finally photographs the winning book in the detail TC-1 skipped, it captures — at every winning moment — the independent conditions a non-circular add could key on (P-CIRC, so the pyramid can be rebuilt without the serpent eating its tail), and it lays the first stone of the permanent excursion substrate (P-KEEP, so no run is ever again discarded as flawed-system output and deterioration can be read from the record). The census follows; the redesign follows that; and every one of them will join back to the table S-3 builds.*
