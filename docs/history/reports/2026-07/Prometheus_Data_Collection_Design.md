# PROMETHEUS — Phase 6.0 Instrumentation Build Spec
## Dramatically expand paper-trade data collection: the full trade record + the market context around it

*Chat Claude → Claude Code handoff, under Fable mode. This spec is **logging-only**: it changes what
we record, never how the strategy decides or sizes. Because no decision logic is touched, it does
**not** spend virgin data and can ship against the currently-frozen ruleset. Written for two readers —
Part A is the plain-English rationale and the decisions the operator needs to make; Part B is the
implementable spec for Claude Code.*

---

# PART A — For the operator

## A1. The core problem, in one sentence

**The engine computes 53 fields for every trade and the paper journal saves 22.** [verified from
`replay.py` `ReplayTrade` dataclass vs the live journal header]. Around **33 already-computed fields
are thrown away** at the moment the trade is written to disk — including every structure predictor
(`base_present`, `wyckoff_score`, `spring_bar_distance`, admission/veto flags), the full stop path,
the position-sizing internals, and — most painfully — the two **stop counterfactuals**
(`r_sig_only`, `r_struct_only`) that tell us what each trade would have done under the other stop.

This is why the Week-1 analysis kept hitting walls: the 4b autopsy's strongest predictors and every
exit counterfactual exist in memory for a few milliseconds and are then deleted before we can learn
from them. **The first and cheapest step is not to compute anything new — it is to stop discarding
what we already compute.**

```
  computed per trade:  ████████████████████████████████████████████████████  53
  saved to journal:    ██████████████████████                                22
  discarded:                                 ██████████████████████████████  ~33
```

## A2. What "cover every aspect + the context around the trade" means here

Two gaps, and one bottleneck.

**Gap 1 — the trade itself.** We save the outcome (R, MFE, MAE, exit reason) but not *why* the trade
was what it was: its grade evidence, its confirmation dynamics, how its stop moved, what it would
have done under the other stop or the other exit stack. Closing this is mostly Tier 0 below (free).

**Gap 2 — the context the trade lived in.** We save almost nothing about the *tape* at the moment we
entered: the volatility regime, how stretched price was from its trend anchor, whether the ribbon was
cleanly trending or chopping, what the higher timeframe looked like, the time of day, and — the big
one — **what BTC was doing when we took an ETH or SOL trade** (crypto is highly correlated; a SOL
short into a BTC-up tape is a completely different bet than one into a BTC-down tape, and our
per-coin siloed harness is blind to this). Closing this is Tiers 1 and 4.

**The bottleneck — data accumulation rate.** The strategy takes ~1 trade/day and we deferred servers,
so labeled data arrives slowly. The two highest-leverage ways to collect *dramatically* more are
therefore not just "more columns" — they are:
- **Log the signals we currently discard.** Every signal that fires while a position is already open
  is thrown away with no record. Logging each one *plus what it would have done* (its counterfactual
  outcome) turns our ~1-taken-trade/day into a much higher signal-observation rate — for free, no new
  fetches. (Tier 2)
- **Log paired exit-stack outcomes.** Running X3 (or a variant) in shadow alongside the live X4 over
  the *same* entries gives a paired comparison, which needs far fewer samples to reach a conclusion
  than comparing two separate live runs. This is also the "alternative-mechanics shadow collection"
  you asked about earlier — it doesn't exist yet; this creates it. (Tier 3)

## A3. The five tiers, in plain English

| Tier | What it does | Answers | Cost | Risk |
|---|---|---|---|---|
| **0** | Save the ~33 fields we already compute | The 4b predictors; stop path; stop counterfactuals | ~free (serialization only) | none |
| **1** | Snapshot the tape at entry (vol, extension, ribbon, HTF, time) | "In what conditions do trades work vs die?" | cheap (from data already in memory) | none |
| **2** | Log skipped signals + what they would have done | "What are we missing by holding one position? Which skipped setups were good?" | medium | none (still logging) |
| **3** | Log a shadow exit stack (X4 live + X3 / base-cover-v2) per entry | "Would a different exit/entry rule do better?" — with paired power | medium | none if pre-registered |
| **4** | Add a shared BTC market-context snapshot to every tick | "Does the BTC tape drive our ETH/SOL outcomes?" | medium (one infra tweak) | low |

Tiers 0 and 1 are no-brainers — pure upside, no risk, no data spend. Tiers 2–4 are the ones where
you have choices (A4).

## A4. Decisions you need to make

1. **How far to go now.** Recommendation: ship **Tier 0 + Tier 1 immediately** (they're free and
   unblock everything), then **Tier 2** next (it's the biggest data-throughput win). Tiers 3–4 can
   follow once 0–2 are validated.
2. **Cross-asset context (Tier 4): lightweight or full?** *Lightweight* = each coin's tick also
   fetches BTC 1-hour candles and records a 3-field BTC snapshot (one extra fetch per tick, no
   architecture change). *Full* = run all three coins in one tick with a single shared candle fetch
   and a shared market snapshot. Recommendation: **lightweight now** — it delivers ~90% of the value
   with none of the re-architecture, and we can consolidate later.
3. **Shadow arm (Tier 3): which variant to shadow?** X3 (the 0.25×ATR trail — the committed exit's
   sibling) is the natural first shadow because it directly tests the give-back/tail-capture question
   from Week 1. The `base-cover-v2` entry variant (§8.1 of the Week-1 report) is the natural *entry*
   shadow. Recommendation: **shadow X3 first** (exit question is live and cheap via the existing
   race harness), add the entry variant as a second parallel agent later.

## A5. The one hard guardrail

Collecting more data is not permission to tune against the current window. **Logging ≠ tuning.** This
spec records; it does not change any threshold. The Week-1 window stays characterization-spent, and
any change suggested by the *new* data must still be built as a named frozen variant and validated on
*fresh* paper. Shadow arms (Tier 3) are collected forward and their evaluation bar is pre-registered
before we look. This keeps the alpha-narrowing discipline intact while we widen the lens.

---

# PART B — For Claude Code (implementable spec)

## B0. Principles and constraints

- **Freeze-safe / logging-only.** Do not modify any file in the decision path
  (`birth_filter.py`, `structure.py`, `sfp_engine.py`, `wyckoff.py`, entry/gate/sizing logic, or the
  stop lifecycle *math*). All changes are in serialization, a new context-capture helper, and the
  paper runner's orchestration. The `_lifecycle` return may be *extended* (add tracked values) but
  its exit decisions must be byte-identical (see B7 acceptance test 1).
- **Append-only schema.** New columns are appended; never reorder or rename the existing 22. Add a
  `schema_version` column so future readers can branch on format. This keeps every existing
  `paper_journal*.csv` and the Week-1 analysis valid.
- **Symbol as a first-class column.** Add `symbol` to every row (currently the coin is implicit in
  the filename). This enables single-read pooled analysis instead of the manual 3-file merge done in
  Week 1.
- **No new data dependency for Tiers 0–3.** Every field in Tiers 0–2 is derivable from the
  `PipelineResult` already in memory (`candles`, `ribbon`, `signals`, `health`, `atr`, `e200`,
  `sep_atr`) or from the `ReplayTrade`/birth-candidate objects. Only Tier 4 fetches anything new.
- **Confirm exact column names in-repo.** This spec names arrays I verified are referenced in
  `replay.py` (`ribbon["atr"|"e200"|"sep_atr"|"bull_cross"|"bear_cross"]`, `signals["dir"|"gate_*"|
  "cap_*"|"is_r1_*"|"fail_*"|"stop_*"]`, `candles` OHLC+`open_time`, `health` list). For any field
  needing `e9`/`e89` or the 4H/MTF arrays, confirm the actual column/attribute names before use and,
  if a source is genuinely absent, emit the column as null rather than fabricating it.

## B1. Tier 0 — Persist the full `ReplayTrade` (near-free)

`simulate_arm` (paper path) already populates the full `ReplayTrade`, including the meta/evidence
dict (`replay.py` L449–464), `sep_atr_at_mfe`/`leg_vol_ratio_at_mfe` (L511–513), `post_exit_cont_atr`
(L514–518), `mfe_atr`/`mae_atr` (L507–508), `stop_path` (via `record_path=True`, L441), and the
counterfactuals `r_sig_only`/`r_struct_only` (L520–523). The paper harness discards them only in
`paper_live.py`'s `_JOURNAL_COLS`.

**Change:** expand the serializer to write these currently-dropped, already-computed fields
(group → columns):

- **Identity/timing:** `arm`, `symbol`, `signal_bar`, `signal_ts`, `entry_bar`, `trigger_bar`,
  `confirm_bar`, `bars_to_confirm` (= `confirm_bar − trigger_bar`).
- **Structure evidence (the 4b predictors):** `base_present`, `base_cover_v1`, `base_cover_v2`,
  `spring_linked`, `spring_bar_distance`, `wyckoff_phase`, `wyckoff_score`, `contrary_sfp_count`,
  `gate_modes_disagree`.
- **Admission/birth:** `admission_mode`, `modes` (admitted_by), `gate_exempt_spring`, `vetoed`,
  `veto_reason`, `birth_status` (CONFIRMED/EXPIRED — surface from the candidate if not already on the
  trade).
- **Stops (full picture):** `stop_initial_sig`, `stop_initial_struct`, `stop_source_at_exit`,
  `risk_px`, and `stop_path_json` (JSON-encode the `list[(bar, price, source)]`).
- **Sizing internals:** `budget_mult`, `leverage_flag`, `size_truncated`,
  `implied_leverage_untruncated`, `exit_stack`.
- **Excursion detail:** `mfe_atr`, `mae_atr`, `sep_atr_at_mfe`, `leg_vol_ratio_at_mfe`.
- **Counterfactuals (stop choice):** `r_sig_only`, `r_struct_only`.

**Implementation:** the cleanest form is to serialize `ReplayTrade` generically (e.g. `asdict` +
whitelist) rather than a hand-maintained 22-name tuple, so future field additions are captured
automatically. Keep the existing 22 names/positions first (append new columns after), and encode
lists/dicts as compact JSON strings.

## B2. Tier 1 — Entry-context snapshot (cheap, no fetch)

Add a helper `capture_entry_context(res, entry_bar, trigger_bar, confirm_bar, direction) -> dict`
that reads the in-memory pipeline arrays and returns the fields below. Call it in `simulate_arm`
where the trade is built (it has `res` and the bars). Compute at the **entry bar** unless noted.

| column | source array | definition | question it answers |
|---|---|---|---|
| `atr_at_entry` | `ribbon["atr"]` | ATR at entry | absolute vol |
| `atr_pct_at_entry` | derived | `atr / entry_px` | relative vol |
| `atr_pct_rank` | `ribbon["atr"]` | percentile of `atr[eb]` in trailing 200 bars | vol regime (expanding/normal/contracting) |
| `sep_atr_at_entry` | `ribbon["sep_atr"]` | fast-ribbon separation at entry | how stretched the fast EMAs were |
| `sep_atr_at_confirm` | `ribbon["sep_atr"]` | separation at `confirm_bar` | birth confirmation strength |
| `e200_dist_atr` | `ribbon["e200"]`,`atr` | `(entry_px − e200)·dir / atr` | extension from the trend anchor (large + = entering stretched) |
| `ribbon_state` | `e9`/`e89`/`e200`* | ordering + slope signs → `stacked_bull` / `stacked_bear` / `mixed` / `compressed` | trend structure at entry |
| `dir_pipeline_at_entry` | `signals["dir"]` | pipeline's own trend label | does it agree with the trade direction? |
| `gate_state_at_entry` | `signals["gate_long"/"short"]` | gate on/off for the trade side | gate context |
| `htf_gate_state`* | 4H/MTF arrays* | higher-timeframe gate/trend at entry (null if unavailable) | does HTF alignment predict outcome? |
| `health_leg_vol_ratio_at_entry` | `health[eb]` | leg vol ratio | momentum-quality context |
| `health_degraded_at_entry` | `health[eb]` | `transition_event == "health_degraded"` | entering into deterioration? |
| `dist_to_swing_hi_atr` / `dist_to_swing_lo_atr` | pivots/`structure` | distance to nearest recent pivot high/low, in ATR | overhead room / resistance |
| `hour_utc`, `dow` | `entry_ts` | session/time | time-of-day effects |
| `bars_since_last_trade` | runner state | spacing to prior taken trade | clustering |
| `account_equity_at_entry`, `drawdown_at_entry` | `state` | portfolio state at entry | does drawdown state affect behavior? |

\* `e9`/`e89`, the pivot helper, and the 4H/MTF gate: confirm the real names in-repo; emit null if a
source truly doesn't exist rather than inventing a value.

**Lifecycle-path fields** (extend `_lifecycle`'s tracked values — decisions unchanged; only add
recording): `time_to_mfe_bars` (= `mfe_bar − entry_bar`), `mae_before_mfe_r` (worst adverse
excursion *before* the MFE bar — track a running min up to `mfe_bar`), `trail_engaged`
(`"ema_trail"` appears in `stop_path`), `bars_to_trail_engage` (first `ema_trail` bar − entry bar,
else null), `n_stop_moves` (= `len(stop_path) − 1`), and `e200_dist_atr_at_mfe`
(`(mfe_px − e200[mfe_bar])·dir / atr[mfe_bar]` — this directly explains give-back: a large value
means the trail was sitting far below the peak).

## B3. Tier 2 — Log skipped signals + their counterfactual outcome (throughput multiplier)

Today, `paper.py` marks entries skipped for `in_position`/`concurrency`/`eod` and `continue`s
*before* computing their exit; `paper_live.py` then persists only rows with a `trade_id`, so skipped
signals vanish. Change:

1. In the paper runner, for **every** entry the engine produced (taken or not), compute the full
   `_lifecycle` result (the lifecycle is concurrency-independent — `replay.py` documents this — so
   this is a valid counterfactual of "what if this signal had been taken standalone").
2. Persist skipped signals as journal rows with `taken = false`, `skip_reason ∈
   {in_position, concurrency, eod, vetoed}`, the **full entry-context snapshot** (B2), and their
   counterfactual outcome fields prefixed `cf_` (`cf_r`, `cf_mfe_r`, `cf_mae_r`, `cf_exit_reason`,
   `cf_bars_held`). Taken trades carry `taken = true` and their real outcome as before (and may also
   carry the same `cf_` fields for cross-checking, which should equal the realized values).
3. Add `concurrent_open` (0/1 under the single-position rule) and, when skipped for `in_position`,
   `blocking_trade_id` (which open trade held the slot) so the opportunity cost is attributable.

This roughly multiplies labeled observations per unit time and directly measures the cost of the
single-position constraint (a live design question) without changing that constraint.

## B4. Tier 3 — Paired exit-stack shadow (within-sample power + the shadow collection)

The engine already races stacks over frozen entries (`run_exit_race`, `replay.py` L592). Reuse that
pattern inside the tick: over the **same** entry set, run the live stack (X4) *and* a shadow stack
(X3 first — see A4.3), and log both outcomes per entry as paired columns: `r_x4` (= the live `r`),
`r_x3`, plus each stack's `exit_reason`, `mfe_r`, `give_back_r`. The live account/state continues to
be driven **only** by X4 — the shadow is recorded, never traded. Pre-register the comparison metric
and sample floor before evaluating (e.g. "paired ΣR difference over ≥N closed trades across ≥M
regimes, tail-adjusted"). Later, add the `base-cover-v2` *entry* variant as a second parallel agent
(its own state/branch) rather than an in-tick shadow, since it changes which entries exist.

## B5. Tier 4 — Cross-asset market-context snapshot (the one infra change)

**Lightweight (recommended):** in each coin's tick, additionally fetch BTC 1-hour candles (one extra
`get_or_fetch`) and compute a small BTC snapshot at the trade's entry time:
`btc_ret_24h_at_entry`, `btc_e200_dist_atr_at_entry`, `btc_trend_state` (BTC ribbon_state). Attach to
every row (for BTC trades these equal the coin's own values). This captures the dominant cross-asset
driver with no re-architecture.

**Full (later):** run all three coins in a single scheduled job with one shared candle fetch and a
shared `market_snapshot` object, eliminating the redundant BTC fetch and enabling richer cross-asset
fields (e.g. BTC–alt correlation, relative strength). Defer unless the lightweight snapshot proves
its worth.

## B6. Schema, versioning, and a data dictionary

- Add `schema_version` (start `"6.0"`) and `symbol` to every row.
- Write a committed **`data_dictionary.md`** describing every column: source, formula, units, and the
  question it answers (Part B tables are the seed). This is part of "good data collection" — undated,
  undocumented columns rot. Update it in the same PR whenever a column is added.
- Provide a small **merge utility** (or a documented one-liner) that reads all per-coin journals into
  one master frame keyed by `symbol` + `trade_id`, so pooled analysis is a single read. (This
  replaces the manual 3-file concat done in Week 1.)
- Keep values machine-clean: booleans as `true/false`, missing as empty/`null` (never `"NaN"` text),
  lists/dicts as compact JSON. Timestamps ISO-8601 UTC.

## B7. Acceptance tests (the verify-before-handoff gate)

Do not consider this done until all pass:

1. **No behavior change (critical).** Re-run the pre-run BTC window with the new build and assert the
   **original 22 columns are byte-identical** to the current output. This proves the instrumentation
   did not alter any entry, exit, or sizing decision. If any legacy column differs, a decision-path
   change leaked in — stop and fix.
2. **Internal-consistency invariants**, asserted on every row: `give_back_r ≈ mfe_r − r`
   (taken rows); `risk_px > 0`; `stop_low ≤ entry_px ≤ stop_high` never violated on entry;
   `bars_held = exit_bar − entry_bar`; `trail_engaged` true ⟺ `"ema_trail" ∈ stop_path`;
   `atr_pct_rank ∈ [0,1]`; `taken=false` rows have `cf_*` populated and no realized `pnl_pct`.
3. **Hand-verify a sample of new context fields.** Pick ~3 trades and manually recompute
   `e200_dist_atr`, `atr_pct_rank`, `sep_atr_at_entry`, and `e200_dist_atr_at_mfe` from the candles,
   confirming the logged values match (guards against off-by-one bar-index errors — logging the wrong
   bar's context is the main failure mode here).
4. **Counterfactual sanity.** For taken trades, the `cf_r` computed via the skipped-path lifecycle
   must equal the realized `r` (same standalone lifecycle) — a mismatch means the counterfactual and
   live paths diverged.
5. **Round-trip.** The merge utility reads all coins into one frame with the expected column set and
   row counts equal to per-file counts.

## B8. Suggested sequencing

1. **PR-1 (Tier 0 + B6 schema):** generic full-`ReplayTrade` serialization, `symbol`,
   `schema_version`, `data_dictionary.md`, merge utility. Acceptance tests 1, 2, 5. *This alone
   recovers the 4b predictors and the stop counterfactuals — the highest-value, lowest-risk step.*
2. **PR-2 (Tier 1):** entry-context snapshot + lifecycle-path fields. Acceptance tests 2, 3.
3. **PR-3 (Tier 2):** skipped-signal + counterfactual logging. Acceptance tests 2, 4.
4. **PR-4 (Tier 3):** X3 shadow via the race harness. Pre-register the metric.
5. **PR-5 (Tier 4, lightweight):** BTC market-context snapshot.

Ship PR-1 and PR-2 before the next analysis window so the *next* week of paper data arrives fully
instrumented. Everything after is additive.

---

## Appendix — Proposed column catalog (grouped)

*Legacy 22 kept verbatim and first. New columns appended. `[T0/T1/T2/T3/T4]` = tier; `*` = confirm
source name in-repo or emit null.*

**Legacy (unchanged):** `trade_id, dir, kind, grade, entry, entry_px, stop_signal, stop_struct,
stop_chosen, exit, exit_px, exit_reason, r, wr, mfe_r, mae_r, give_back_r, bars_held,
post_exit_cont_atr, leverage, deploy_scale, pnl_pct`

**Meta [T0]:** `schema_version, symbol, arm, taken, skip_reason`

**Timing/birth [T0]:** `signal_bar, signal_ts, entry_bar, trigger_bar, confirm_bar, bars_to_confirm,
birth_status, admission_mode, modes, gate_exempt_spring, vetoed, veto_reason`

**Structure evidence [T0]:** `base_present, base_cover_v1, base_cover_v2, spring_linked,
spring_bar_distance, wyckoff_phase, wyckoff_score, contrary_sfp_count, gate_modes_disagree`

**Stops/sizing [T0]:** `stop_source_at_exit, risk_px, stop_path_json, budget_mult, leverage_flag,
size_truncated, implied_leverage_untruncated, exit_stack`

**Excursion detail [T0]:** `mfe_atr, mae_atr, sep_atr_at_mfe, leg_vol_ratio_at_mfe`

**Stop counterfactuals [T0]:** `r_sig_only, r_struct_only`

**Entry context [T1]:** `atr_at_entry, atr_pct_at_entry, atr_pct_rank, sep_atr_at_entry,
sep_atr_at_confirm, e200_dist_atr, ribbon_state*, dir_pipeline_at_entry, gate_state_at_entry,
htf_gate_state*, health_leg_vol_ratio_at_entry, health_degraded_at_entry, dist_to_swing_hi_atr*,
dist_to_swing_lo_atr*, hour_utc, dow, bars_since_last_trade, account_equity_at_entry,
drawdown_at_entry, concurrent_open, blocking_trade_id`

**Lifecycle path [T1]:** `time_to_mfe_bars, mae_before_mfe_r, trail_engaged, bars_to_trail_engage,
n_stop_moves, e200_dist_atr_at_mfe`

**Skipped-signal counterfactual [T2]:** `cf_r, cf_mfe_r, cf_mae_r, cf_exit_reason, cf_bars_held`

**Exit-stack shadow [T3]:** `r_x4, r_x3, exit_reason_x3, mfe_r_x3, give_back_r_x3`

**Cross-asset [T4]:** `btc_ret_24h_at_entry, btc_e200_dist_atr_at_entry, btc_trend_state`

---

*Prepared by chat Claude under Fable mode, 2026-07-14. Logging-only; freeze-safe; does not spend the
Week-1 window. Companion to `Prometheus_Paper_Analysis_Week1.md`. Hand to Claude Code for
implementation; the acceptance tests (B7) are the completion bar.*
