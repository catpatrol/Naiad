# ARGUS — CLOSING REPORT TO THE PANTHEON
### Lane: ARGUS (analytics toolkit · daily brief · volume filter) · Reviewer: ARGUS · Builder: HEPHAESTUS
### Compiled 2026-08-06 · For: the operator · APOLLO · ATHENA · DIONYSUS · HERMES · HEPHAESTUS

Provenance tags: `[verified]` recomputed or read first-hand · `[builder]` from a builder report with fixtures · `[ratified]` operator ruling · `[open]` unresolved.

---

## §0 · THE HEADLINE, IN FIVE LINES

The analytics pack is **built, chart-certified against the operator's own TradingView charts, and released for use.** `ANALYTICS_VERSION` **1.5.0**, `analytics_sha` `ea5f02f2…`, suite **286 passed / 1 skipped**, zero failures.

The daily brief renders in two stages — market monitor and decision instrument — with a confluence engine, a volume filter, a de-peg layer and a hinge-shaped trade board. It runs three times a day and writes a tracked, self-describing archive.

**Eight census candidates** are routed to APOLLO, each with a deflation gauge stated in advance.

Nothing in this lane claims edge. Confluence measures **agreement between tools**; R:R measures **geometry**. Whether any of it predicts anything is census work under G-7, unchanged.

---

## §1 · WHAT IS CERTIFIED, AND WHAT DELIBERATELY IS NOT

Certification here means one thing precisely: **the arithmetic reproduces what the operator sees on his own charts**, read on closed candles, on `BINANCE:<SYM>USDT.P` perpetuals, 1h substrate, `hlc3` source.

| recipe | status | evidence |
|---|---|---|
| RSI · StochRSI · MACD · Awesome Oscillator · ATR | **CERTIFIED** | 72/72 across 9 candles, 3 assets, 5 timeframes, two independent sittings |
| `resample_ohlcv` | **CERTIFIED** | 40/40 raw OHLC fields, 8 of them resampled — matches TradingView's own aggregation |
| `rolling_vwap` | **CERTIFIED, both substrates** | 1D 14/14 · 1h 28/28 |
| `anchored_vwap`, including σ | **CERTIFIED** | 42/42, worst delta 0.0495, worst 0.0083 bps |
| `vw_sigma_bands` geometry | **VERIFIED** | 54 triples, every one symmetric at exact integer multiples |
| `volume_profile` · `low_volume_nodes` · `va_nesting` | **FIXTURE-VERIFIED, not chart-certified** ⚠ | excluded from the gate **by design** — see below |

**Why the profile family was excluded, recorded so a later cycle does not read it as an oversight and "fix" it:** our profile spreads each bar's volume uniformly across its range — a declared approximation over klines. TradingView's is a *different* approximation over data we do not hold. Comparing them certifies nothing whichever way it comes out: agreement would be a coincidence of two approximations, disagreement uninformative about either. They carry a permanent `approximation` chip and both lists print on every rendered page, because once the warning banner comes down the never-certified recipes become the ones most likely to be mistaken for verified.

**What certification does not mean.** Nothing about prediction has been established. The banner change moved a claim about arithmetic, not a claim about edge.

---

## §2 · THE FINDINGS THAT TRAVEL BEYOND THIS LANE

Six results here are not about VWAPs at all. They are about how this project measures things.

### 2.1 An indicator that had never once produced a number

`stoch_rsi` returned **all-NaN on every input, for its entire life** — 100% null across every asset and every timeframe in the capture before the fix. One of the four oscillators the contract commissions.

The cause was mundane: `sma` is cumsum-based, so one leading NaN poisons everything after it, and RSI's warm-up always supplies one. **The cause of it going unnoticed is the important part.** The causality fixture compared an all-NaN series to an all-NaN series and passed. It could not fail.

> **A guard that cannot fail is not a guard.** There is now a fixture asserting each series function actually *produces numbers* — the property the causality test had silently assumed. `[builder]`

### 2.2 Mutation testing found it, and nothing else could have

Nineteen of the original twenty-one causality fixtures caught a deliberately injected non-causal mutant. Two did not, and investigating those two is what surfaced §2.1.

Separately, the naive truncation-prefix form proved **vacuous on all five** functions whose signatures it does not fit — measured against sabotaged implementations, it certifies non-causal code as green. Each was rebuilt in the form its signature admits; **11 of 11 behaviour-changing mutants caught.** `[builder]`

**Transfer:** a new fixture should be shown to *fail* on a deliberate break before it is trusted to pass. No census fixture has been mutation-tested.

### 2.3 A function that published a value and then revised it

`resample_ohlcv` inferred bar spacing from a median. When the median was decidable but unrepresentative, it emitted a bucket and **later revised it** — a causality violation worse than the one the amendment was written to fix. Closure is now proved only by a bar in a strictly later bucket. Measured cost before adoption: **20 asset/timeframe combinations, identical bucket counts.** `[builder]`

### 2.4 The z-score is scale-free in time — and it corrected the reviewer

An anchored σ grows as **√t**. But price's displacement from the anchored mean grows as **√t** as well, from the same walk and the same anchor. They cancel, so the **reading** is approximately scale-free even while the **width** is not.

Measured on the operator's own captures, same asset, same Month anchor:

| anchor age | σ | z |
|---|---|---|
| 29 bars | 313.40 | **+2.01** |
| 114 bars | 583.39 | **+1.94** |

**σ grew 86%. The reading moved 3.7%.** `[verified]`

This killed the reviewer's proposed period-relative maturity floor, whose entire justification was that a young σ inflates the σ-label and manufactures false signals. It does not. What survives: floors are justified by **sampling noise alone**, and band **widths** are comparable only at **comparable ages** — so anchor age now prints beside every σ width.

### 2.5 A category error in a baseline

Cycle 4 compared price's time beyond ±1σ/±2σ/±3σ (~50 / ~9.5 / ~0.4%) against a normal distribution's 31.7 / 4.6 / 0.27 and concluded the tails were "roughly double."

**Those Gaussian figures describe independent draws.** Price relative to a VWAP is a persistent, autocorrelated series — once beyond a band it tends to stay, because trending is what carried it there. A time-fraction measures **persistence**, not tail fatness. Withdrawn, deleted, and a fixture keeps it out. `[builder]`

**The replacement is the decision-relevant unit:** one excursion beyond a band until price returns inside it is **one decision**, however many bars it spans. Measured over 8,760 hourly bars across ten assets: **~122 σ2 episodes and ~12 σ3 episodes per asset-window per year**, median length 2 bars.

### 2.6 The instrument is part of the measurement

The same bar read on TradingView's `BTCUSD` **INDEX** instead of the Binance perpetual gives a 7-day rolling VWAP of 63,786.76 against our 63,737.7. The 49-point gap is **1.51× the collapse tolerance** — so the wrong instrument produces a **separate registry level**, not a rounding difference. In a system that scores by counting agreement, that is **one tool counted twice**. `[verified]`

---

## §3 · WHAT THE VOLUME FILTER ACTUALLY DID — measured, and smaller than first claimed

The contract's headline question was whether including volume evidence in the confluence scoring **moves the operator's decisive levels**. Cycle 2 answered "a line moved on 10 of 10 assets, 20 of 20 sides." That was overstated twice, and the corrected figure is the honest one:

| | count |
|---|---|
| **relocations** (≥ one cluster width) | **6** |
| refinements (< one cluster width) | 14 |

Median move **0.044 ATR** against a cluster width of 0.15. **Seventy per cent of what was counted as movement is the same structure re-centred inside its own cluster.** `[builder]`

Six genuine relocations across ten assets is a real effect and a modest one. It is stated in this form so no lane inherits the inflated version.

---

## §4 · WHAT SHIPPED, BEYOND THE RECIPES

**The confluence engine.** Every layer emits levels into a registry — anchored and rolling VWAPs with 1/2/3σ bands, windowed volume profiles with POC/VAH/VAL and low-volume nodes, structure (confirmed pivots, period opens, prior extremes), and Secret Sauce zone and governor edges. Near-duplicates collapse at 0.02 daily-ATR; the rest cluster at 0.15; each cluster scores by counted members plus tool-family diversity — **never fitted**. Registry runs **131–169 levels per asset**.

**Dual scoring.** Every capture computes areas and lines **twice** — with and without the volume families — and records both. That is what makes §3 measurable at all, and it is the live rehearsal of the question the census will eventually score.

**The de-peg layer** *(operator-originated, and it replaced the reviewer's framing)*. An anchor is informative not when its estimator settles but **when it unpegs from the next-shorter one.** This is structural: **1 January anchors year, quarter and month simultaneously**, so Y and Q are byte-identical until 1 April; 1 July makes M and Q identical for all of July. Adjacent anchored pairs and anchored↔rolling counterparts now carry a peg state, separation in bps and ATR, σ ratio and both ages. **Redundancy prints rather than being suppressed** — a pegged anchor renders with a chip naming what it duplicates and stating that a de-peg is what makes it informative.

**The hinge** *(operator-originated)*. A σ band is a hinge with two outcomes: pullback to the mean, or genuine rejection sending price to auction toward the dominant POC and the far side of value. Every reversion draft now carries **both targets** with their own distances and R:R, and **expresses no preference between them** — fixture-enforced. Target-A R:R is a constant 2.00 or 3.00 by construction; target-B ranges **0.31 to 24.73**. Choosing between them on today's numbers would be choosing on noise.

**The record.** Captures tracked in `briefs/`, self-describing, embedding the complete rule set and every version and hash that produced them. Three write-once daily partitions plus an excursion table. Measured git growth: **106 MB/yr** — inside the original estimate, and gzipping would have made the repository **1.74× larger** by defeating delta compression.

---

## §5 · IMPLICATIONS PER LANE

### APOLLO — the largest inheritance

**You may now cite `analytics_version` 1.5.0.** `analytics/INTERFACE.md` is the contract: function signatures, pinned conventions, causality classes and the level/value-area/excursion record schemas. The census consumes the **functions plus its own exploration-classic data** — never live captures, which remain display-only forever.

**Three things that will bite if not read first:**

**Causality classes are the contract, not a comment.** `causal` means output at *i* depends only on `[0..i]`. `lag:N` means it is knowable only at *i+N*. **`endpoint_only` means valid only at the array end and it raises if asked for a mid-array value** — `volume_profile` and `percentile_rank` are both endpoint-only, so any historical caller must **slice** rather than index. Caller-side slicing is exactly where as-of contamination enters a census.

**The instrument travels with the number.** §2.6: a reading from an index or a spot pair is a different level, not a rounded one.

**The scorable panel is five assets.** BTC, ETH, ZEC, SOL, NEAR, with two thin annexes and three assets at zero scorable days. Any replication argument has five independent units.

**Eight candidates are routed, each with its deflation gauge:**

| id | question | gauge stated in advance |
|---|---|---|
| **H-VBT** | do exits at confluence-scored VWAP levels retain more of peak excursion than riding to regime break? | must **beat** regime-break riding, not merely exist |
| **CENSUS-1d** | does location confluence carry edge on exploration-classic? | run the primary test with the `ss` family **excluded** — a fill born from an SS zone sits near an SS level by construction |
| **H-VBR** | do σ2/σ3 entries targeting the mean differ in expectancy? | a σ2 touch is by construction "far from the recent mean" — must beat a plain distance-from-mean baseline |
| **H-VDP** | does a de-peg mark or precede regime change? | de-pegs cluster on **fixed calendar dates** for every asset — the null must be a calendar-matched shuffle, or the finding will be the calendar |
| **H-RVX** | do RVWAP crosses confluence with the SS EMA cascade? | two trailing means of one series co-move by construction — matched random-timing null required |
| **H-FSU** | does σ-width-in-ATR predict better than timeframe label or governor step? | it is a volatility ratio — must beat ATR-normalised distance |
| **H-M1X** | do 1m EMA(300)/(450) crosses inform the 5m cascade? | measurement only; **TC-5's permanent 5m entry floor is untouched** |
| **H-VAN** | do scale-confirmed value-area edges behave differently? | nested windows share data; partial dependence |

**⚠ A sample-size warning to establish before registering, not after.** The ~122 σ2 and ~12 σ3 episodes per asset-window per year are **not independent across VWAPs** — one large move puts price beyond σ2 on the 7-day, the 30-day and the weekly anchor at once. The effective sample is closer to episodes-per-**asset**. On a five-asset panel, **σ3 may be too thin for cross-scale replication at all.**

**And a connection to the study's own unsolved problem.** Priority #3, the harvest problem, remains open: 73.67% of trades reaching +1R round-trip into loss, and the winning book wins by riding to regime break rather than by managing winners. **H-VBT aims directly at it.** If confluence-scored VWAP structure supplies credible targets, that is a candidate for the take-profit mechanism the study has been missing. That is why it heads the priority list in §6.

### ATHENA — one question that decides whether today's cleanup counted

**`docs/history/` and the sync selection.** 44 ARGUS artifacts (4.8 MB, 84% of it two capture JSONs) were moved from `exchange/reports/` to `docs/history/argus/`, taking that directory from **87 files / 5.62 MB to 43 files / 830 KB**. Every move was sha-verified both ways; nothing was deleted.

**But `docs/` is tracked, pushed, and not gitignored — and `docs/history/` already held six files before today.** So if `docs/` is inside the sync selection, **the move relocated 4.8 MB from one synced folder to another and the box sees the same bytes.** Only you can read the sync configuration. If `docs/` is included, exclude `docs/history/`. Until then, treat the 85% reduction as a reduction of the **reading surface** — real and worth having — and not as a confirmed reduction of box size. `[builder, open]`

**Three smaller items:** `publish_exchange.py`'s final step pushes the whole branch, so repo-work commits reach origin despite commit-no-push — the operator has accepted the state, and whether whole-branch push should be fixed to a dedicated ref or made explicitly intended is yours. `backup_estate.py` should carry `briefs/` in scope now that a tracked archive exists. And the estate persists a **single volume column**: taker-buy/delta fields exist in Binance's public candles but are not stored, which is what blocks CVD and Coulling-style volume-spread work — a schema question for a future refresh, not a data-source one.

### DIONYSUS — the critique surface

The six findings in §2 are the most useful thing this lane produced for an adversarial reader, and four of them are **failures of verification machinery rather than of code**: a fixture that could not fail, a fixture family that was vacuous, a criterion that was circular, and a baseline that was a category error. **A critique lane's highest-value target here is not the numbers — it is whether the guards guard.**

Three specific invitations: test whether the hinge's refusal to rank actually holds under pressure, or whether a preference leaks in through ordering or presentation. Test whether the "no fitted weights" assertion survives — it is enforced three ways (source scan, AST with no multiplication and no float constant in `score()`, and behaviourally) and that is exactly the kind of belt-and-braces that invites a fourth path nobody checked. And note that the SEQ8 bulk outputs were the only lane output missing from `.gitignore`, which is how a wildcard add swept 3.5 GB into a commit and got the whole branch rejected by GitHub; that gap is now closed.

### HERMES — consolidation

`exchange/reports/` is now **43 files / 830 KB**. Three ARGUS artifacts are retained on the reading surface by design: `INTERFACE_2026-08-06_C6.md` (the census-facing contract, byte-identical to the canonical `analytics/INTERFACE.md`), `SESSION_SUMMARY_ARGUS_2026-08-06_C6.md` (current state of record), and `exchange/status/LEDGER_ARGUS.md`.

**Two routing notes were deliberately held back**, because they are ARGUS-authored but addressed *to* another lane and therefore function as the recipient's inbox item: `NOTE_ARGUS_to_APOLLO_2026-08-03_census_candidates.md` and `NOTE_ARGUS_to_ATHENA_2026-08-03_publish_exchange_push_scope.md`. Both are arguably superseded — the census candidates are re-routed in §5 of this report, and the push-scope question is resolved and accepted. **ARGUS's ruling: both may be archived.** 22 KB; it does not change the headline.

**One residual risk worth a dashboard line:** nothing *enforces* that the exchange copy of `INTERFACE.md` tracks the canonical. It is byte-identical today because this cycle refreshed it, and the header carries `ANALYTICS_VERSION` and `analytics_sha` so a mismatch is detectable — but only to a reader who checks. A fixture asserting the two are identical would close it; that is a code change and belongs to the next build cycle.

### HEPHAESTUS — the standing rules this lane's failures produced

**Scan what the code does, never what it mentions.** Seven occurrences of one bug class, the last two being a firewall guard that flagged a docstring *stating which statistics the function refuses to compute*, and then a field literally named `contains_no_probability_claim` flagged for containing "probability." The promise read as the offence.

**A file must never contain its own sha256** — the row necessarily hashes the previous generation and is permanently one revision stale, so the document can never regenerate to the same bytes.

**Paired handback, always:** a Builder's Report as forensic record and a Session Summary as decision artifact, both standalone, both zero-context, published together. This lane produced a cycle where the two disagreed on whether a capture existed, because the report covered stages 0–4 while the summary covered 0–6.

**And the counter-pattern worth naming, because it is the system working:** the builder refused reviewer instructions on ratified invariants repeatedly across this lane's life — declining to widen a regex to make a failure disappear, refusing to lower a byte-identity bar to a tolerance, checking whether prior work existed before rebuilding it, and correcting the reviewer's own claims from evidence on at least four occasions. A stack whose executor never pushes back is a stack whose reviewer errors all land.

### The operator

The brief runs three times a day — 12:00, 15:00 and 21:30 UTC, session-anchored and timezone-aware — and renders in two parts, monitor then decision instrument, with the full bias scorecard preserved.

**One cost to expect before you meet it in a Monday brief:** under the ratified 60-bar band floor, the weekly anchor's bands are withheld until **Wednesday 12:00 — 35.7% of every week**. Nothing else is affected. The mitigation is your own de-peg logic in reverse: the **7-day rolling VWAP is fully formed throughout**, covering the same span, so you are never without a weekly view — only without a *calendar*-weekly one. Worth watching before deciding whether 60 is right for the weekly anchor specifically.

**Every threshold remains a v1 placeholder** — collapse 0.02, cluster 0.15, LIS 1.5 ATR, family cap 3, maturity floors 16/60, the target-distance buckets — and all are due re-ratification against the calibration report after real use rather than against a reviewer's guess.

---

## §6 · SHOULD THE CENSUS EXPAND? — the honest answer is *prioritise*, not *expand*

The temptation is to absorb all eight candidates. **I recommend against it**, for three reasons that are measurements rather than opinions: the scorable panel is **five assets**; σ3 episodes are **thin and not independent across VWAPs**; and the census already carries a queue blocked on Q-1/Q-2. Adding eight measurement layers to a census that has not answered its existing questions is scope creep wearing the clothes of ambition.

**Recommended order, driven by the prime directive rather than by novelty:**

**First, H-VBT.** It aims at priority #3, the harvest problem — the study's largest unsolved item, where 73.67% of trades reaching +1R round-trip into loss. Nothing else on this list points at a known open wound.

**Second, CENSUS-1d Phase 0** — the free Tier-A proxy. `census_outcomes.jsonl` carries `event_price` and `p0` on all 149,802 rows, so price-space clustering needs no new walk. If location confluence has no signal in the cheap proxy, the expensive backfill is much harder to justify. The cost is recovering the join key from archived S-3 journals.

**Third, H-VDP** — cheap to compute, operator-originated, and its calendar-matched null is the discipline that would catch a whole family of spurious findings.

**Everything else waits.** H-VBR and H-FSU are genuinely interesting and neither points at a known problem; H-RVX, H-M1X and H-VAN are refinements of questions already queued.

---

## §7 · WHAT REMAINS OPEN

| item | owner |
|---|---|
| `docs/history/` sync selection — does the archival move reduce the box or relocate it? | **ATHENA** |
| INTERFACE staleness fixture (assert exchange copy ≡ canonical) | next build cycle |
| Maturity floors 16/60 — re-ratify after real use; watch the weekly anchor's 35.7% | ARGUS + operator |
| Every v1 threshold — re-ratify against calibration, not against the reviewer | ARGUS |
| Custom anchors (VWAP anchored at a significant high or low) — scoped, **not built** | operator to rule |
| Estate delta columns (taker-buy) — blocks CVD and volume-spread work | ATHENA |
| `backup_estate.py` to carry `briefs/` in scope | ATHENA |
| Two held-back routing notes — ARGUS rules they may be archived | HERMES |

---

## §8 · THE FIREWALL, UNCHANGED

Not a signal service. Not sizing advice. Not study evidence. No engine change. No forward scoring. No fitted weights — asserted three ways in the scoring path. No lockbox read for scored evidence.

**Confluence measures agreement between tools, not edge. R:R measures geometry, not probability.** Recording a band excursion, a de-peg or a hinge geometry is **operations**. Computing what fraction revert, any hit rate, any expectancy, is **census work under G-7**.

The archive may be mined for hypotheses. It is never a scoring window.

— ARGUS, 2026-08-06
