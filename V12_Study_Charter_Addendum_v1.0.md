# v12 Study — Charter Addendum v1.0
**Date:** 2026-07-10 · **Status:** RATIFIED (operator confirmation of VR-1…VR-5, this date)
**Parent document:** Naiad Phase 0 Charter v1.0 · **Governs:** v12 Study phases V0–V9
**Amends nothing in the Naiad paper line.** This addendum charters a sibling research
workstream that shares the data estate and the `v11_faithful` engine configuration.

---

## 1. Purpose

Characterize SS Cascade v11.0.2 across the full pre-registered asset grid and all
available deep history, in order to (a) put confidence intervals and a regime
climatology around the edge estimated on the spent BTC development window, and
(b) surface at most five named improvement candidates, exactly one lockbox
validation shot for the survivors. Outputs target the operator's discretionary
playbook and a future pre-registered successor configuration (SSv12 candidate) —
never the running Naiad paper line mid-window (parent charter: no mid-window rule
edits; no automated self-tuning).

---

## 2. Ratified decisions

### VR-1 — Evidence partition (ratified)

All timestamps are candle **open time, UTC**. The class of a candle is a pure
function of (symbol, open time):

| Class | Definition | Rules |
|---|---|---|
| **exploration-classic** | open time ≤ 2024-06-30 23:59:59, all assets | Free to mine, plot, iterate. |
| **LOCKBOX** | 2024-07-01 00:00:00 → 2025-10-05 23:59:59, all assets | **Sealed.** Opens once, at V8, against pre-written verdict criteria. |
| **spent** | BTCUSDT only, 2025-10-06 00:00:00 → 2026-07-07 23:59:59 | Characterization only, forever. Anchor row of every comparison table. |
| **regime-contaminated** | all non-BTC assets, 2025-10-06 → 2026-07-07 | Exploration-eligible, lockbox-ineligible (virgin eyes, shared macro regime with the spent study). |
| **forward** | open time > 2026-07-07 23:59:59 | Naiad's domain. The v12 Study never reads it. |

**Study right edge: 2026-07-07 23:59:59 UTC, all assets.**

**Lockbox integrity rule (metadata yes, values no).** Permitted operations on
lockbox rows before V8: row counts, timestamp continuity and gap checks,
duplicate detection, file hashing. Forbidden before V8: any quantity derived
from open/high/low/close/volume values — no means, ranges, returns, indicator
values, signals, or plots. Enforced by a loader guard (see V1 build prompt,
invariant I3 and fixture F3).

**Known consequences, accepted at ratification:**
- Exploration is majors-heavy. LIT (floor 2025-12-23) contributes **zero**
  exploration-classic and **zero** lockbox rows; its entire study footprint is
  the regime-contaminated slice. HYPE and FARTCOIN are expected to contribute
  little or no exploration-classic history (census will pin exact first
  candles). These assets function as validation-only / contaminated-only; all
  panel findings are therefore held to a **structural** standard (mechanism-level
  claims) rather than absolute-expectancy claims, per the survivorship-bias
  discussion of record.
- Tercile thresholds and any other fitted constant used for labeling are fitted
  on **exploration-classic only** (see VR-5), so no post-lockbox information
  leaks into lockbox-period labels.

### VR-2 — Multiplicity budget and stopping rule (ratified; date is a default)

Maximum **5 named variants** enter Phase V7. The study closes at the lockbox
verdict or on **2026-10-31**, whichever comes first. *(The date is a reviewer
default set at ratification — veto window open, see §9.)* Variants are named,
human-ratified, pre-registered with mechanism, prediction, metric, and pass
threshold before any variant run. No automated parameter search.

### VR-3 — Cost model (ratified)

The Naiad charter cost model (fees + funding + slippage) is reused unchanged.
Every reported results table carries **0× / 1× / 2×** cost rows. The stress rows
stand in for era differences in market microstructure; no era-specific cost
modeling in v0 of the study.

### VR-4 — Sequencing and gates (ratified)

V0 (this addendum) and V1 (census) start immediately, parallel to Naiad Phase 1
closure. **V3 and everything after are blocked** until: Naiad parity steps 3B,
3C, 3D pass, **plus** a cross-asset parity spot check on **ETHUSDT and
FARTCOINUSDT** (defaults; recent windows where TradingView still holds LTF
history; a handful of governor crosses each, engine vs. chart). *(Spot-check
asset choice is a reviewer default — veto window open, §9.)*

### VR-5 — Regime taxonomy (ratified; frozen here)

Every timestamp in the study carries one of six regime labels, computed from
BTC and applied market-wide (regimes are treated as market weather shared by
all assets):

- **Structure stage:** BTC 12H EMA-89 vs EMA-200. Bull-structure when 89 > 200,
  bear-structure otherwise, evaluated on confirmed 12H bars.
- **Volatility tercile:** trailing 30-day realized volatility of BTC daily
  log returns (UTC daily closes), annualized (×√365). Tercile boundaries are
  fitted **once, on exploration-classic BTC only**, then frozen and applied to
  all periods including the lockbox at V8.

Label = (stage × vol tercile) → 6 regimes. Frozen at this ratification; any
change is a charter amendment.

---

## 3. Pre-registered analysis axis: governor timeframe (added at ratification)

**Question of record:** how do expectancy and realized payoff compare across
governor timeframes 1H, 4H, 12H?

**The confound, stated plainly:** the three mandates vary governor and
execution timeframe together (1H/1m, 4H/5m, 12H/15m). A mandate-level
difference cannot by itself be attributed to the governor. The mandates also
vary effective zone-memory duration silently: zoneMemory is 3 *execution*
bars, i.e. 3 minutes (intraday), 15 minutes (swing), 45 minutes (position).

**Tier 1 — mandate diagonal (free).** The V4 cell cards for the three
mandates as actually traded, reported per asset and pooled per governor.
Answers "which mandate, as traded."

**Tier 2 — controlled factorial (adds 20 cells).** Execution timeframe fixed
at 5m; governor varied across {1H, 4H, 12H} on every asset (the 4H/5m column
is the existing swing mandate). Holding execution fixed also holds zone-memory
duration fixed. Answers "what does the governor itself contribute."

**Metrics (both tiers):** expectancy per campaign in R with bootstrap CI ·
hit rate · payoff ratio (mean winner R ÷ |mean loser R|) · tail-capture ·
campaign frequency · **R-throughput per month** · strip-best-trade line ·
0×/1×/2× cost rows. Per-trade expectancy alone misranks systems with different
trade frequencies; throughput is the tiebreaker of record.

**Power rule:** cells with fewer than 20 campaigns are reported but flagged
insufficient-N. Cross-governor claims are asserted only where 95% bootstrap
intervals separate. The 12H rows are expected to be campaign-poor; "cannot
distinguish" is an admissible and reportable outcome.

**Slot rule:** this axis is descriptive. Any mandate redefinition it suggests
becomes a named variant, consumes one of the five VR-2 slots, and must pass
the lockbox.

---

## 4. Stop-loss and exit research scope (confirmed at ratification)

- **Shadow-stop schema from the first V4 run.** Every simulated trade journals
  its MFE/MAE excursion path and the hypothetical exit point of every candidate
  exit variant. All subsequent exit research is offline re-simulation of the
  journal; it costs no new data.
- **Size-the-prize rule (Prometheus, binding):** exit variants may claim named
  VR-2 slots only after the V5 loss-attribution split (cohorts NEVER_GREEN /
  STILLBORN / FADED / PROTECTED) shows exits own a material share of the loss
  for the v11 entry set. In v10 they owned ~17%; slots are not spent on the
  minority owner.
- **Tail-capture acceptance rule (Prometheus rule 9, binding):** any exit
  variant that reduces give-back is rejected if tail-capture falls beyond a
  pre-registered tolerance. The profile is tail-carried; the exit's prime
  directive is not to choke the tail.
- **Fidelity bound, stated:** stop fills are simulated at execution-bar
  resolution (gaps fill at next bar open). 1m cells give the finest stop
  simulation; this bound is quoted alongside any stop-geometry finding.

---

## 5. Evidence classes and ledger mechanics

Ledger classes of record: `spent | regime-contaminated | exploration-classic |
lockbox | forward(Naiad)`. The LEDGER.md append for this ratification is a
**builder deliverable** in V1 (D6), executed verbatim from §8 below — never a
manual paste (a prior manual paste corrupted the ledger with escaped markdown).

---

## 6. Phase map

- **V0 — Charter addendum & pre-registration.** This document. *Done at ratification.*
- **V1 — Data census & integrity gate.** Complete the estate, verify it, tag partitions, seal the lockbox guard, append the ledger. **Gate: no analysis until green.**
- **V2 — Parity completion.** Naiad 3B/3C/3D + ETH/FARTCOIN spot check. **Gate: hard.**
- **V3 — Anchor run.** BTC spent window through `v11_faithful`; first mechanical numbers on the window; discretion-premium estimate vs. the screenshot record.
- **V4 — Frozen panel survey, exploration only.** v11.0.2 untouched; cell cards for all runnable cells + Tier 1/Tier 2 governor axis. Null hypothesis: the edge is BTC-window-specific.
- **V5 — Decomposition.** Funnels, cohorts, regimes, grades, MAE/MFE, shadow stops.
- **V6 — Hypothesis register → named variants.** ≤ 5 slots, each with mechanism, prediction, metric, threshold.
- **V7 — Variant trials, exploration only.** v11.0.2 always runs as control; near-ties adopt both-arms-forever.
- **V8 — Lockbox validation.** One shot. Verdict criteria written before the box opens.
- **V9 — Transfer.** Playbook amendments + Pine update, journaled forward (the true out-of-sample for discretionary claims); Naiad adoption only at a window boundary with fresh pre-registration.

---

## 7. What this study is not

Not a Naiad change. Not parameter self-tuning. Not open-ended optimization (the
stopping rule exists because tail-carried systems absorb infinite tinkering).
Not a verdict on the operator's discretionary edge — only on the mechanical
ruleset. Not a consumer of any candle after 2026-07-07. Not a path to live
capital except through the parent charter's Phase 6 minimum-live gate.

---

## 8. LEDGER.md append block (builder executes verbatim in V1, deliverable D6)

```
## v12 Study — opened 2026-07-10
- Charter: V12_Study_Charter_Addendum_v1.0.md (VR-1..VR-5 ratified; governor-TF axis pre-registered)
- Evidence classes: spent | regime-contaminated | exploration-classic | lockbox | forward(Naiad)
- Spent: BTCUSDT 2025-10-06 -> 2026-07-07 (six intervals) - characterization only
- Regime-contaminated: all non-BTC assets 2025-10-06 -> 2026-07-07 - exploration-eligible, lockbox-ineligible
- Exploration-classic: all study candles <= 2024-06-30
- LOCKBOX: 2024-07-01 -> 2025-10-05, all assets, all intervals - SEALED. Integrity ops only. Opens once, at V8.
- Study right edge: 2026-07-07 23:59:59 UTC. Forward data belongs to Naiad.
- Variant budget: 5 named slots. Study closes at lockbox verdict or 2026-10-31.
- Regime taxonomy frozen: BTC 12H 89v200 stage x BTC 30d realized-vol terciles (thresholds fit on exploration-classic only)
- Spend at open: zero (census pending)
```

---

## 9. Open defaults subject to operator veto

1. **Study stop date 2026-10-31** (VR-2). Name another date to override.
2. **Cross-asset parity spot-check assets: ETHUSDT + FARTCOINUSDT** (VR-4).
3. **Census spot-check burden: 3 candles per asset (30 total), escalating to 10
   for any asset with a single mismatch** — an operationalization of the
   ratified "~10 per asset" that trades operator hours for an escalation
   trigger without losing rigor. Say the word to restore the full 100.

Silence past the start of V2 confirms the defaults.
