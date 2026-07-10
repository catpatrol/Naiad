# BUILD PROMPT — NAIAD PHASE 1: "Engine + Instrumentation"
### Feed this file to Claude Code inside the `naiad` repository. It is self-contained. · Project Naiad · 2026-07-09
### Governing document: `Naiad_Phase0_Charter.md` v1.0 (RATIFIED). On any conflict, THE CHARTER WINS.

---

## 0. Context and mission

Phase 0 (the charter) is ratified. Your mission in Phase 1: build **one Python engine** that deterministically implements the Secret Sauce Cascade v11.0.2 state machine and the Naiad v0 trading layer, with the full fixture suite green, the journal schema derived from the autopsy question list, the per-asset first-candle table pinned, and the (dormant) forward-collector entrypoint ready for Phase 1.5 activation.

If these files exist in the working directory, read them BEFORE writing code:
- `Naiad_Phase0_Charter.md` (the contract above this one — normative)
- `SS_Cascade_v11_0_2.pine` (reference implementation for `v11_faithful` semantics)
- `SSv11_Execution_Playbook_v1_1.md`, `SSv11_Field_Manual.md` (doctrine context)
- `Prometheus_Stop_Loss_Logic_Learnings.md` (why the journal records what it records)

**Language/stack:** Python 3.11+, pandas/numpy, pytest. Pin exact versions in `requirements.txt`. Single-threaded deterministic computation paths only.

## 1. What this phase is NOT

- NOT tuning. No parameter changes from charter defaults. No performance conclusions.
- NOT the exit race, NOT the characterization campaign (Phase 2), NOT any read of the sealed pre-2022 holdout. **Backfill it; never run signals on it.**
- NOT live paper collection (Phase 1.5 = the operator enabling the schedule you scaffold).
- NOT live trading. No exchange keys, no order endpoints, no secrets of any kind, anywhere.
- NOT XMR, NOT FET, NOT Market Monkey, NOT any data source other than Binance public data.
- Any number this phase prints from the spent window (BTC 2025-10-06 → 2026-07-07) is a plumbing check, never evidence.

## 2. Hard invariants (violating any of these is a failed build)

1. **Closed bars only.** No decision reads the current, unclosed bar of any timeframe.
2. **Confirmed-HTF rule.** The governor/MTF value visible to an exec bar is the most recent higher-timeframe bar whose **close time ≤ that exec bar's open time** (replicates Pine's `expr[1] + lookahead_on` idiom). No exceptions, including display/journal fields.
3. **Fills at next-bar-open** after the signal close. Stop fills at the stop price, or at the bar open when gapped through.
4. **Bit-identical reruns.** Same inputs → byte-identical journal. Hash-verified (F1).
5. **Stops never loosen.** One-way ratchet, property-tested (F3).
6. **Risk rails in every mode.** Halts and sizing caps execute identically in replay and paper (F4).
7. **Every gate gates.** In-path assertions prove the traded set equals the eligible set (F5). A gate without a fixture is a build failure.
8. **UTC everywhere.** All timestamps UTC; bar identity = (symbol, interval, open_time).
9. **Raw candles never committed.** Local cache directory is gitignored; journals and state only on the data branch.
10. **Config-frozen variants.** All parameters live in named config files (`configs/v11_faithful.yaml`, `configs/naiad_v0.yaml`); the engine takes a config id; journal rows carry `config_id` + `engine_version` + `run_id`.
11. **Idempotent journal.** Append-only JSONL, merged by unique key (cell_id, event_type, event_open_time, tranche_id); re-runs and overlaps cannot duplicate or corrupt (rolling re-scan safe).

## 3. Repository layout

```
naiad/
  engine/          # frozen core: indicators, state machine, trading layer, shadows, journal
  configs/         # named frozen variants (yaml)
  fixtures/        # pytest suite F1–F8 + golden files
  research/        # empty in Phase 1 (Phase 2's playground)
  scripts/         # backfill.py · replay.py · tick.py · packet.py · first_candles.py
  .github/workflows/collector.yml   # scheduled hourly; committed DISABLED (see §9 D6)
  LEDGER.md        # copied from charter §6 opening entries; updated by reviewer only
  requirements.txt · README.md (operator-facing, plain language)
```
Journals live on orphan branch `data` under `journal/{cell_id}/YYYY-MM.jsonl` plus `state/{cell_id}.json`.

## 4. Data layer

- **Bulk backfill** from `data.binance.vision` (USDT-M futures klines, monthly then daily zips) for intervals 1m, 5m, 15m, 1h, 4h, 12h; **incremental** top-up via REST `/fapi/v1/klines`. Funding history via `/fapi/v1/fundingRate` (bulk archive where available).
- **Integrity checks** after every backfill: gap scan, duplicate scan, monotonic open_time; write a coverage report per symbol/interval.
- **First-candle table** (`scripts/first_candles.py` → `data_starts.csv` + a table appended to README): programmatically detect each symbol's first available futures candle per interval. **Hard rule for LIT:** `first_valid = max(detected_first_candle, 2025-12-01T00:00Z)` — the LITUSDT symbol carried a different token (Litentry) before 2025; earlier history must never load. Assert in the loader, not just the docs.
- Basket: BTCUSDT, ETHUSDT, SOLUSDT, NEARUSDT, ZECUSDT, JTOUSDT, TAOUSDT, HYPEUSDT, FARTCOINUSDT, LITUSDT (perpetual, USDT-M).

## 5. Engine specification — signal layer (both configs)

Replicate v11.0.2 semantics exactly. Cross-check every rule against the Pine file; where the Pine comments cite the spec (§4.x), mirror that logic. Key semantics that MUST match:

- **EMA** = standard recursive EMA, alpha = 2/(len+1), seeded at series start; warm-up per F7 makes seed effects negligible. **ATR** = Wilder smoothing (RMA) of true range, length 14 — not SMA, not EMA. **Volume MA** = SMA(20).
- **Cross** semantics: crossover(a,b) ⇔ a>b now AND a≤b on the prior bar (mirror for crossunder).
- **Governor layer:** regime = gov 9 vs 89; stage = gov 89 vs 200; aligned vs provisional cross classification; arming per charter §3.2 (`provisionalArming` on; provisional zones Z1+Z2; upgrade on stage confirm in campaign direction; opposite confirmed cross ends campaign).
- **Zones and tags:** Z1/Z2/Z3 bands from confirmed governor EMAs ± multiples of confirmed governor ATR; per-zone tag bars and running tag extremes; fresh-episode detection; zoneMemory 5 when exec=5m else 3; innermost-priority active zone (Z3>Z2>Z1).
- **PRIME / CONFIRM / grades / C:** exactly charter §3.2, including the Z3 ribbon-separation waiver, the 5-bar cooldown, tfAlign per mandate {4H gov→1H, 1H gov→5m, 12H gov→4H}, C gated by structure+zone and **never traded** in naiad_v0 (journal-only).
- **Sniper leg + `retr`:** origin = governor-series extreme (lookback 55 governor bars at cross); terminus = post-cross favorable extreme, frozen at first Z2/Z3 tag or R1 fire; pocket 0.5–0.786; `retr` = tag-extreme retracement fraction of the leg (null when no leg; V-born campaigns have no leg).
- **Capitulation V:** climax ≥3.5× vol MA with extension ≥1.0× gov ATR beyond gov 89; far-band reclaim within 10 exec bars on ≥1.2× vol MA; births/reverses a provisional campaign.
- **TPW and CLUSTER:** journal-only events (never block, never trade). **Failure X:** 3 consecutive exec closes beyond the far governor band edge → campaign dead.

## 6. Engine specification — trading layer (naiad_v0 only)

- **Books:** each of the 30 cells runs its own paper book, initial equity **$10,000**, 1R = 0.5% of current cell equity at stop distance. Portfolio views are aggregation in reports.
- **⚑ FLAGGED DECISION #1 (operator veto, default = as written):** halts (−2R/day, −4R/week, UTC calendar) apply **per cell**, not portfolio-wide — rationale: a bad BTC day must not silence LIT's data collection; cross-cell coupling would contaminate per-cell characterization. If the operator prefers portfolio-wide halts, say so and it becomes a config flag.
- **Sizing:** charter §3.4 table verbatim (pilot 0.5R; grade/tier multipliers; adds 0.5R each; add eligibility = every prior tranche at/beyond breakeven under the current ratchet stop; ≤3 tranches; open campaign risk ≤1R asserted in-path).
- **Costs:** fees 5 bps/side taker; slippage per charter §5 tiers applied to every fill; funding accrued on open notional at each funding timestamp from the historical table (replay) or live endpoint (paper).
- **Stops are orders:** stop-guarantee-and-repair runs first on every wake; simulated stop fills per invariant 3.

## 7. Shadow lines (computed every bar, never traded — all six per charter §3.5)

Entry-variant (exec 9/89 cross trigger) · structure ladder (strict / tiered / unthrottled) · stop anchors (trigger-bar extreme; vol-at-engagement buffer) · sizing counterfactuals (full-1R-at-R1; pilot-0.5R-with-1R-adds) · candidate-exit shadow stops (X-A pure e200 trail 0.5×ATR buffer with engagement guard; X-B trail+TPW-partial; X-C trail+extension-partial; X-D mechanized Playbook stack) · funnel log with reject reasons. Shadow outcomes are journal columns, not separate books.

## 8. Journal schema

JSONL, one row per event. Minimum fields: `run_id, engine_version, config_id, cell_id, symbol, tf_gov, tf_exec, ts_open, ts_close, evt` (REGIME/STAGE/TAG/PRIME/CONFIRM/V/TPW/CLUSTER/X/ENTRY_FILL/ADD_FILL/STOP_FILL/EXIT/HALT), `dir, tier, grade, rc, zone, retr, px_signal, px_fill, stop, atr_exec, atr_gov, tranche_id, size_r, fees, funding_cum, slippage, mfe_r, mae_r, give_back_r, postexit_cont_1_5_20, exit_reason, cohort` (NEVER_GREEN/STILLBORN/FADED/PROTECTED), `engagement_flags, shadow{entry_alt, ladder_strict, ladder_unthrottled, stop_alt_anchor, stop_alt_volbuf, size_full_r1, size_big_adds, exit_XA, exit_XB, exit_XC, exit_XD}, reject_reason` (funnel rows). Before coding the schema, write `fixtures/autopsy_questions.md` (charter §8 seed list, expanded to ≥20 questions) and map every question → columns; unmapped questions are a build failure.

## 9. Deliverables

- **D1** `engine/` implementing §5–§8, both configs.
- **D2** `data_starts.csv` + README table (all 10 symbols × 6 intervals, LIT floor asserted).
- **D3** `scripts/backfill.py` and `scripts/replay.py` with `--config --cell --start --end`; README usage with what-you-should-see.
- **D4** Fixture suite green (§10) with `pytest` one-command run.
- **D5** **Parity pack** for operator sign-off: `research_outputs/parity/crosses_4h.csv`, `crosses_12h.csv` (every confirmed BTC governor cross 2025-10-06→2026-07-07: timestamp, direction, tier) + `case_windows.md` printing the engine's event sequence for May 16→26, Jul 2→6, Jun 14–16, Jun 22, Feb 6, Dec 4–13 — formatted so the operator can check them against TradingView bar-by-bar.
- **D6** `scripts/tick.py` + `.github/workflows/collector.yml` (hourly, concurrency-guarded, rolling 48h re-scan, committing journal/state to the `data` branch) — **delivered with the schedule commented out**; a README section titled "Phase 1.5: turning the collector on" tells the operator exactly which line to un-comment and what the first successful run looks like.
- **D7** Dry-run autopsy: run replay on BTC swing cell, 2026-05-01→2026-07-07 (**spent window — plumbing only**), then `research_outputs/dryrun_autopsy.md` answering every question in `autopsy_questions.md` from the journal alone. Empty/zero-filled/type-trapped columns are a failed fixture (F8).
- **D8** Session packet: `scripts/packet.py` zips journals + reports + configs + a one-page manifest.

## 10. Fixtures (numbered; all must pass)

- **F1 determinism:** two replay runs, identical args → identical SHA-256 of journal.
- **F2 no-lookahead:** (a) synthetic-data test proving HTF visibility only after HTF close per invariant 2; (b) truncation test: replay to T with data ending at T equals the first T-portion of a longer run.
- **F3 ratchet property test:** across all replays, stop series per side is monotone; randomized-input property test included.
- **F4 rails:** constructed scenario breaches −2R intraday → engine halts in replay AND via tick.py path; journal shows HALT row; no further entries that day.
- **F5 gate integrity:** in-path assertions — traded set ≡ eligible set (tier caps, grade table, C-never-trades, add-eligibility, ≤1R cap); a deliberately broken gate in a test double must fail loudly.
- **F6 parity:** D5 produced; acceptance = operator confirms the 4H/12H cross lists and the six case windows against TradingView. Numeric tolerance: cross timestamps exact to the bar; EMA/ATR values within 0.05% after F7 warm-up.
- **F7 warm-up:** every replay refuses to emit signals until ≥2,000 exec bars AND ≥200 governor bars of history precede the window.
- **F8 journal completeness:** D7 report generated with zero unmapped questions and zero empty columns.

## 11. Phase verdict criteria

Phase 1 is DONE when: F1–F5, F7, F8 green in CI · D1–D8 present · F6 signed off by the operator · the reviewer has recomputed D5/D7 claims from the raw journal in a fresh session. Only then may the operator enable D6 (Phase 1.5).

## 12. Iteration protocol

1. Deliver working increments; commit to branch `phase-1`, never merge (merging is the operator's act).
2. The operator pastes test/tool output verbatim; fix with minimal diffs; never refactor unrelated code while fixing; keep a CHANGELOG.
3. If any instruction here conflicts with the charter or with a §2 invariant, STOP and say so before writing code; propose the nearest compliant alternative.
4. Flag every a-priori design decision not covered by this contract with "⚑ OPERATOR VETO" in your summary, with your default and rationale.

## 13. Operator setup (plain language, before pasting this to Claude Code)

1. Create a **public** GitHub repository named `naiad` (public = unlimited scheduled-workflow minutes). *What you should see:* an empty repo page with a green "Code" button.
2. Add the five reference files from §0 plus this build prompt to the repo (GitHub web: "Add file → Upload files"). *What you should see:* the files listed on the repo front page.
3. Open Claude Code pointed at a local clone of the repo (or the repo directly, per your usual workflow) and paste the full text of this file as the task.
4. When the builder reports done: run the commands it lists in README (each has "what this does / what you should see"), then run `python scripts/packet.py` and attach the resulting zip to the reviewer session.
5. Do NOT enable the collector schedule until the reviewer confirms Phase 1 verdict criteria (§11).

*End of Phase 1 build prompt.*
