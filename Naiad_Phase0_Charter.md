# PROJECT NAIAD — PHASE 0 CHARTER
### v1.0 · RATIFIED 2026-07-09 by the operator
*Amendment log (operator edits at ratification): (1) §1 live-capital caveat added verbatim below. (2) §3.4 pilot entry raised 0.33R → **0.5R**; adds raised to **0.5R** each. (3) §3.5 new sizing shadow: adds at a full 1R. (4) §4 XMR deferred and FET removed — basket is 10 assets. (5) All former [VETO] defaults confirmed as written. One design decision remains flagged inside the Phase 1 build prompt (halt scope, per-cell default) for a one-word veto.*

---

## 1. Mission and hypothesis

**Naiad** is an autonomous **paper-trading** agent and research flywheel built on the Secret Sauce Cascade v11.0.2 momentum system, run across a pre-registered grid of crypto perpetual markets and timeframe mandates. Its first campaign is not profit and not alpha expansion: it is to determine, without self-deception, whether the SSv11 edge survives deterministic execution, realistic costs, and virgin data — and to improve it through a disciplined scientific loop: **observe → hypothesize → test → let results inform the next hypothesis.**

**Operator's ratification caveat (binding):** this project will not trade live capital yet. Once sufficient confidence in SS v11.0.2 has accumulated — or enough data exists to improve it into SSv12 — the agent goes live, through Phase 6's minimum-live gate and no other way.

**The hypothesis, stated as mechanism:** after a confirmed 9/89 EMA regime cross on a governor timeframe, pullbacks into zones built from the governor's own EMAs are systematically absorbed by trend participants; therefore an execution-timeframe reclaim of its 9 EMA with a confirming close (PRIME), occurring inside such a zone, has positive expectancy net of costs. Structure (the governor 89 vs 200 relationship) scales **confidence** — position size, zone depth, and grade — but not permission, because major trends are typically born before structure confirms.

**What this project is not (v0):** no live capital, no exchange keys or secrets anywhere, no order-flow features (Market Monkey Terminal is parked as a named future research axis with its own separate API cost), no automated self-tuning of parameters, no mid-window rule edits, and no additions to the asset grid without a ledger entry and fresh pre-registration.

---

## 2. Roles and operating agreement

Three roles, reproduced deliberately from the Prometheus architecture:

- **Builder — Claude Code.** Lives in the repository. Implements one phase at a time from a written build prompt, commits to a phase branch, never merges.
- **Reviewer — Claude (this Project), under Fable-mode gates.** Scopes before building; **recomputes every headline from raw artifacts** before trusting any report; argues against its own conclusions; verifies before handoff; reports with calibrated confidence. Maintains `LEDGER.md` (the data-spend ledger) and states its contents at every session start. Writes each phase's build prompt as a contract: prior findings, frozen invariants, numbered fixtures, deliverables, pre-registered verdict criteria, and an explicit *"what this phase is not."*
- **Operator — Ludwig.** The hands and the veto. Ferries artifacts between builder and reviewer, approves or vetoes every flagged decision, owns every merge and every gate. Every operational guide is written for a reader with no programming background, with "what this does / what you should see" under every step.

**Session packet convention:** every builder session ends by producing one zip — journals, reports, changed configs, and a one-page manifest — so the ferry job is always one download and one attach.

---

## 3. Frozen v0 specification

### 3.1 Engine principles

Naiad's source of truth is **this charter implemented directly in Python** — not any Pine file. One engine, two named configurations:

- **`v11_faithful`** — reproduces SS Cascade v11.0.2 exactly. Used only for screenshot-parity fixtures and full-window characterization.
- **`naiad_v0`** — the live paper line, per §3.2–3.5 below.

**Hard invariants, fixture-enforced in every execution mode (replay, paper, and any future live):** decisions on closed bars only · fills at next-bar-open · no lookahead · bit-identical reruns · stops never loosen · risk halts and sizing caps active everywhere · **every gate ships with an in-path fixture that fails if the gate is not actually gating production behavior** (the dormant-filter rule) · stop-guarantee-and-repair is the first action of every wake.

### 3.2 Entries (naiad_v0)

- **Arming:** every confirmed governor 9/89 cross arms a campaign. Stage-aligned cross (89 on the regime side of the 200) = **full tier**. Stage-misaligned cross = **provisional tier**: zones Z1+Z2 only, grade ceiling B, half size. A mid-campaign 89×200 confirm in the campaign direction upgrades provisional → full. The expectation window **never expires**; a campaign dies only on Failure X or an opposite confirmed cross.
- **Zones** (× governor ATR, from confirmed governor bars): Z1 = governor-9 ± 0.25 · Z2 = governor-89 ± 0.35 · Z3 = governor 89–200 band ± 0.35 pad (full tier only). Zone memory: 5 exec bars on 5m execution; 3 otherwise. One tag to any armed zone is sufficient; all zones are legal for initiation (doctrine preference Z3 > Z2 > Z1 is expressed through the journal and grading, not prohibition).
- **Live trigger — PRIME:** exec close crosses over/under its 9 EMA on the prior bar, plus a confirming close now (second close at-or-beyond the first), with minimum bar range 0.5× exec ATR, minimum 9/89 ribbon separation 0.5× exec ATR (waived in Z3), 5-bar cooldown.
- **Grades:** A+ = tag extreme inside (sniper pocket 0.5–0.786 of the arming leg ∩ zone) · A = sub-governor alignment timeframe agrees (`tfAlign`: swing→1H, intraday→5m, position→4H) · B = otherwise, and the hard ceiling for provisional campaigns · C = confirm-only late entry, structure- and zone-gated — **journaled, never traded** · V = capitulation reversal, births a provisional campaign. The `retr` field (measured retracement fraction of the arming leg) is journaled on every PRIME.
- **Adds:** later zone-tag PRIMEs (R2+) and CONFIRM re-crosses while positioned, per v11.0.2 native logic. Failure X = 3 consecutive exec closes beyond the far governor band edge → flat, campaign dead, no re-entry until fresh arming.

### 3.3 Exits (naiad_v0)

- **Survival stop:** tag/signal-bar extreme ∓ 0.5× exec ATR, ratcheting one-way on every entry event (v11.0.2 native). In Naiad the stop is an order, not a reference line.
- **Harvest logic is a raced family, not a belief.** In Phase 2, deterministic exit variants race over frozen entries, incumbent as control, one mechanism axis per variant, on at least two contrasting regime windows: (X-A) pure two-phase structure trail — survival stop untouched until a closed bar sits beyond the exec 200, then trail the 200 with an ATR buffer — the **pre-registered starting hypothesis**; (X-B) trail + TPW partial; (X-C) trail + extension partial (≥2 ATR beyond exec 9); (X-D) the full Playbook stack, mechanized. **Asymmetric evaluation rule, pre-registered:** any variant that reduces give-back is rejected if tail capture (share of trades with MFE > 5R realized above 3R) falls by more than 10% relative. The tail-capture line outranks the give-back line in every exit report.

### 3.4 Sizing (deterministic table — as amended at ratification)

1R (one risk unit) = **0.5% of paper equity** at stop distance. Pilot entry = **0.5R**, then multiplied by grade/tier:

| Signal | Campaign tier | Size |
|---|---|---|
| A+ / A PRIME (R1) | Full | 1.0 × pilot = 0.50R |
| B PRIME (R1) | Full | 0.5 × pilot = 0.25R |
| Any PRIME (R1) | Provisional | 0.5 × pilot = 0.25R (B-cap) |
| V | Provisional at birth | 0.5 × pilot = 0.25R |
| C | any | no trade — journal only |
| Adds (R2+/CONFIRM) | any | **0.5R each**, only while **every** prior tranche sits at/beyond breakeven after the ratchet |

Max 3 tranches per campaign. Total open campaign risk ≤ 1R at any moment (enforced by ratchet math, with a fixture). Hard halts: −2R/day, −4R/week — breaker-tested in replay and paper. Journal attributes profit and heat **per tranche**.

### 3.5 Shadow and telemetry lines (computed every tick, never traded)

1. **Entry variant:** the 5m 9/89 cross (CONFIRM-style) as alternative trigger, with its own hypothetical stop.
2. **Structure ladder:** strict (v11.0.0 — aligned crosses only) · tiered (the live line) · unthrottled (every cross, full zones, full size).
3. **Stop anchors:** trigger-bar-extreme anchor; volatility-at-engagement buffer variant.
4. **Sizing counterfactuals:** (a) full 1R at R1, no pyramid; (b) **pilot 0.5R with every add at a full 1R** (operator amendment) — same triggers, same breakeven eligibility, bigger tranches. Together with the live line these bracket the sizing space: heavy-entry / middle path / heavy-adds.
5. **Candidate exits:** every X-variant's hypothetical exit price on every trade (shadow stops).
6. **Funnel log:** every sub-threshold trigger event with its reject reason — the evidence base for any future, pre-registered gate-strictness change.

---

## 4. The grid: assets × mandates

**Mandates:** swing (4H governor / 5m exec) · intraday (1H / 1m) · position (12H / 15m). A cell activates only once its governor has ≥ 200 confirmed bars of history (EMA warm-up) and exec data is complete.

**Basket (frozen at ratification; venue = Binance USDT-M perpetual):**

| Asset | History class | Notes |
|---|---|---|
| BTC | deep (2019→) | Reference market; parity fixtures live here |
| ETH | deep (2019→) | |
| SOL | multi-year | |
| NEAR | multi-year | |
| ZEC | multi-year | |
| JTO | ~2023-12→ | |
| TAO | ~2024→ | |
| HYPE | young (~2024-12→) | Forward-mostly evidence |
| FARTCOIN | young (~2025→) | Forward-mostly evidence |
| LIT (Lighter) | youngest (~2025-12→) | **Two-token trap:** the Binance symbol LITUSDT belonged to Litentry until 2025-01-31. The engine hard-floors LIT's first valid candle at the Lighter perp listing; symbol history before it is a different asset and must never be loaded. 12H mandate barely warmed up. |

*Removed at ratification: **XMR** (deferred — delisted from Binance 2024-02; inclusion would require a second-venue integration, available later as a named expansion) and **FET** (operator decision).*

Builder pins each asset's exact first-candle date programmatically in Phase 1; the table is then frozen into `LEDGER.md`. Grid = **10 assets × 3 mandates = 30 cells**.

**Multiplicity protocol:** the primary verdict at every gate is **pooled** across the grid. Per-cell results are characterization, readable only past a floor of **≥ 20 trades per cell**. Best-cell selection after the fact is recognized as self-deception and prohibited; any cell-conditional rule must be set a priori as a named variant and validated forward.

---

## 5. Cost model — no cost-free number ever stands alone

Every report prints each headline metric beside its **haircut twin**, plus a bootstrap confidence interval and the **strip-the-best-trade** line.

- **Fees:** 0.05% taker per side (10 bps round trip); builder confirms the current Binance USDT-M schedule at Phase 1 and records it in `LEDGER.md`.
- **Funding:** backtests apply *actual historical* funding to holding periods (free from Binance); forward paper applies live funding.
- **Slippage** per side (confirmed at ratification): tier A (BTC, ETH) 2 bps · tier B (SOL, NEAR, ZEC, JTO, TAO) 5 bps · tier C (HYPE, FARTCOIN, LIT) 10 bps.

---

## 6. Data-spend ledger — opening entries

*Governing rule: reading a result spends the data, whether or not you act on it. Never read an approximation (proxy) of a measurement we can afford to make for real.*

| Dataset | Status at ratification |
|---|---|
| BTC, all TFs, 2025-10-06 → 2026-07-07 | **SPENT for validation** (fitted twice: the nine-month study and the v11.0.2 verification cycle). Parity fixtures and characterization only. |
| All assets, first valid candle → 2025-09-30, excluding the row above | **Characterization set.** All tuning lives here and only here. |
| All assets, everything before 2022-01-01 (BTC/ETH ≈ 2019–2021: Covid crash, 2021 blow-off) | **SEALED retro holdout.** Read **once**, against the pre-registered bar in §7. The read spends it regardless of outcome. |
| Forward paper journals | **Virgin, renewable.** Honest exactly once per frozen ruleset; each window is a one-shot exam. |

---

## 7. Pre-registered verdict bars and the kill doctrine

**Two levels, kept separate.** A **variant-level verdict** is binding in one narrow sense: the number reads as it reads — a fail cannot be argued into a pass after the fact, and a fail is itself a useful data point. **Project-level decisions** belong to the operator: every failure routes to autopsy → diagnosis → **one named, a-priori change** → new frozen variant → forward A/B, looping as long as the operator chooses. Nothing in this charter forces abandonment. What is forbidden is unregistered mid-window edits (they destroy attribution and silently spend data) and any touch to **gate integrity** — the assertion that the code enforces exactly what we believe it enforces. **Gate strictness** is a legitimate dial, adjustable only as a named variant justified by funnel-log evidence.

**Bars (ratified):**

1. **In-sample sanity floor (characterization set):** pooled cost-adjusted expectancy must exceed 0, or the entry definition is redesigned before any forward deployment. A system that fails on the data it was born from is dead on arrival.
2. **Retro out-of-sample bar (holdout, one shot):** pooled cost-adjusted mean ≥ +0.05R · at least half of half-year windows positive · positive in ≥ 2 regime classes · strip-best-trade result ≥ 0. **Evaluability condition:** ≥ 60 trades and ≥ 4 windows, else the verdict records as "underpowered — no read" (the data is still spent).
3. **Forward promotion / pre-live bar:** ≥ 8 two-week windows spanning ≥ 2 regimes · pooled cost-adjusted expectancy > 0 · strip-best-trade printed · per-cell claims only past the §4 floor.
4. **Minimum-live** is a separate, deliberate gate after (3): the smallest real size whose purpose is measuring fills and slippage — with its own risk limits and its own pre-registered success criteria. Not a gradient. Per the operator's ratification caveat, it opens only on the operator's confidence call regarding SS v11.0.2 or its data-driven successor.
5. **Component kills (standing):** any gate or signal shown by autopsy to gate nothing or add nothing is removed, celebrated, and logged. Falsification is a deliverable.

---

## 8. Journal schema — derived from the autopsy, not the other way around

Phase 1 writes the full autopsy question list first and derives columns from it; a **dry-run autopsy on week-one output** is a fixture. Seed questions the journal must be able to answer: where does the loss live by cohort (NEVER_GREEN ≤0 · STILLBORN <0.5R · FADED 0.5–1R · PROTECTED ≥1R)? What are the entry set's MFE/MAE distributions per cell, grade, zone, tier, and `retr` band? What fraction of trades die before each candidate harvest mechanism engages (pre-engagement death share)? What is each exit's capture ratio and tail capture? Did volatility expand between ratchet and exit on trail-stopped winners, and what did post-exit continuation do? Per-tranche: did adds improve or worsen campaign outcomes vs both sizing shadows? What did every shadow line (entry variant, structure ladder, stop anchors) return on identical data?

Minimum columns: the SS11 JSON superset (evt/dir/grade/rc/zone/px/stop/atr/stage/`retr`/t) + cell id, tier, tranche id, fill px, fees, funding paid, mfe_r, mae_r, give_back_r, post-exit continuation, ATR at entry/ratchet/exit, engagement flags, every shadow-stop and shadow-entry price, exit reason, cohort tag.

---

## 9. Fixture manifest

F1 determinism (bit-identical rerun) · F2 no-lookahead · F3 stop-never-loosens in every mode · F4 halts fire in replay **and** paper · F5 gate integrity: deployed entry set == filter output; tier caps and sizing table enforced in-path · F6 **screenshot parity**: the engine's `v11_faithful` replay reproduces every confirmed 4H and 12H BTC governor cross of 2025-10-06 → 2026-07-07 (timestamp, direction, tier), plus event-level sequences in the named case windows (May 16→26 short · Jul 2→6 longs · Jun 14–16 · Jun 22 V · Feb 6 V · Dec 4–13 chop), plus 5m spot-checks from Apr 26 '26 on · F7 EMA warm-up: every replay seeds ≥ 2,000 bars before its window · F8 journal completeness dry-run (no empty or type-trapped columns).

*Parity note: TradingView's BTCUSDT.P feed is Binance futures data, so exact parity is achievable; expect a short calibration loop on EMA seeding and timestamp alignment before F6 passes — that is what the fixtures are for.*

---

## 10. Repository and deployment

**One repository.** The backtester and the paper agent must be the *same engine* — identical fill model, identical gates — because any drift between a "research repo" and a "production repo" silently invalidates the transfer of every backtest result to the live paper line (the dormant-filter failure at repository scale). Separation of concerns happens *inside* the repo: `engine/` (frozen, fixture-gated core) · `configs/` (named frozen variants) · `research/` (notebooks, sweeps, reports — allowed to be messy) · `fixtures/` · journals on an **orphan data branch**. Raw candles are **never committed** — Binance is the durable archive; the agent re-fetches on demand (bulk history via data.binance.vision, live via REST). Workflow file lives on the default branch and checks out the code branch at runtime; concurrency guard on; hourly idempotent rolling re-scan (tolerates missed/duplicate runs); public repo for unlimited Actions minutes; the ~60-day scheduled-workflow pause is neutralized by normal research activity plus a calendar note. Zero secrets, zero exchange keys, anywhere, until the minimum-live gate.

---

## 11. Phase plan

- **Phase 0 — this charter.** Ratified 2026-07-09 → repo bootstrap.
- **Phase 1 — engine + instrumentation.** Python port with both configs; invariants and full fixture manifest (F1–F8, parity certified on BTC); journal schema from the autopsy list; per-asset first-candle table pinned; dry-run autopsy.
- **Phase 1.5 — forward collector live, week one, in parallel.** The full grid starts collecting on frozen `naiad_v0` defaults the moment F1–F5 pass — *before* tuning finishes. Calendar time is the one input that cannot be parallelized later; the untuned v0 exercises the whole pipeline, its windows are virgin evidence, and it becomes the champion for the first A/B.
- **Phase 2 — characterization campaign** (fenced per §6): MFE/MAE and `retr` distributions (the sniper-pocket question answered from all crosses, not just winners), exit-family race, cost sensitivity, funnel analysis → one tuned candidate frozen as **naiad_v1** (named variant).
- **Phase 3 — retro out-of-sample**, one shot, naiad_v1 vs the §7.2 bar.
- **Phases 4–5 — the flywheel.** Champion vs challenger forward A/B on virgin paper; promotion only on the bar; then repeat: collect → diagnose offline → one a-priori change → A/B forward.
- **Phase 6 — minimum-live**, its own gate, on the operator's call per §1.

---

## 12. Standing instructions (paste into Project instructions)

Claude operates as independent reviewer under Fable-mode gates — scope before building, recompute every headline from raw artifacts, argue against its own conclusions, verify before handoff, report with calibrated confidence. Claude maintains `LEDGER.md` and states it at every session start. Build prompts are contracts with invariants, numbered fixtures, deliverables, verdict criteria, and "what this phase is not." Claude assumes the operator has no programming background and writes every operational instruction step-by-step with expected outputs. Claude flags every a-priori design decision for operator veto, never lets a cost-free or interval-free number stand alone, prints the strip-best-trade line by default, and treats falsification as a deliverable.

---

*Charter v1.0 — ratified. The Phase 1 build prompt (`Naiad_Phase1_Build_Prompt.md`) is the governing contract for the next builder session.*
