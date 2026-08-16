# BUILD — TIER-C3 · THE RAILED BASELINE

**Date** 2026-08-15 · **Branch** `v12-v1-census` · **HEAD at start** `20f23a1` · **Seed** 20260815 · **Drafted** APOLLO · **Executor** HEPHAESTUS

**RATIFIED** operator 2026-08-15 — *"I rule the seven F's on your lean."* This build enacts the seven Tier-C2 findings as card diffs and re-measures.

**CLASS — measurement, not registration. m = 0.** No registration. **No lockbox read** — see §0, where that line turned out to bind harder than anyone expected. No estate write. No live orders. F-KEY on every join. The population is a *complete* replay of one ratified card over one corridor: nothing was selected, swept or promoted, so there is no family to correct over. Any future selection **from** these tables is a new probe and declares its own *m* before it looks.

**Programs (local):** `scripts/tierc3_rules.py` (decision path) · `scripts/tierc3_baseline.py` (program) · `scripts/tierc3_fixtures.py` (transcript). **Tables local** at `research_outputs/tierc3/` — 14 parquet + `build_manifest.json`.

**I9** — `ANALYTICS_VERSION` **1.5.0**, `analytics_sha()` `ea5f02f21ca43b6b71e450b540ff09c807b305971e3eb8cff50bea84c985dc91`. Instrument: **BINANCE USDT-M perpetuals**, `{BTC,ETH,SOL,NEAR,ZEC}USDT.P`, offline cache `~/.cache/naiad/data_cache/klines`.

**V-10 — CLOSED BY RULING.** `DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md` was sought once more and is **ABSENT**. Per F-1, VIZ-4's inline restatement is **promoted to the rules of record** — one line at `exchange/reports/RULES_OF_RECORD_VIZ_IRON_2026-08-15.md`, cited to the VIZ-4 contract §Class. VIZ-3 stops being cited. **The chase is over.**

> **THIS DOCUMENT SUPERSEDES THE VERSION AT COMMIT `af6ebf4`.** An `exchange/**` auto-publish fired from another process while this build was still running and committed *and pushed* the draft — headline **+6.7151 R over 12 trades**. An adversarial audit then found a seal breach and a false attribution, both fixed in code below. **The number in `af6ebf4` is wrong; the number here is the build's.** See F-C3-i.

---

## 0 · THE ONE THING THE OPERATOR MUST READ FIRST

**Two things, and the second one is the interesting one.**

### (1) The yardstick changed sign

| | TIER-C2 (v1) | **TIER-C3 (v3)** |
|---|---:|---:|
| net R | −7.7620 | **+7.7614** |
| expectancy / trade | −0.7762 | **+0.7056** |
| n | 10 | 11 |
| win rate | 10.00% | **45.45%** |
| maxDD (R) | 9.5107 | **4.2697** |

*(The near-mirror of −7.7620 and +7.7614 is a coincidence of this corridor. It means nothing and is stated so no one reads meaning into it.)*

### (2) **It was not the rail.** The build is named for the rail; the rail is worth +0.15 R.

The diffs were switched off one at a time and the corridor re-ridden through the *same* code path. **UNSCORED ATTRIBUTION** — `attribution_unscored.parquet`, F-C3-ABLATE:

| cell | anchor | rail | lead-in | seal floor | n | net R | expectancy | win % | marginal |
|---|---|---:|---:|---|---:|---:|---:|---:|---|
| **V1** | 1H | — | — | — | 10 | **−7.7620** | −0.7762 | 10.00 | *reproduces Tier-C2* |
| **D** | 4h | — | — | ✓ | 10 | +8.6507 | +0.8651 | 40.00 | **+16.4127** vs V1 |
| **C** | 4h | 1.0 | — | ✓ | 10 | +8.8032 | +0.8803 | 50.00 | **+0.1525** vs D |
| **B** | 4h | — | 30d | ✓ | 11 | +7.6062 | +0.6915 | 36.36 | **−1.0445** vs D |
| **A** | 4h | 1.0 | 30d | ✓ | 11 | **+7.7614** | **+0.7056** | 45.45 | **+0.1552** vs B — **THE SHIPPED CARD** |
| A0 | 4h | 1.0 | 30d | ✗ | 12 | +6.7151 | +0.5596 | 41.67 | −1.0463 vs A — *the card literally, F-C3-a* |

**The V1 cell reproduces Tier-C2's filed net R to 2.2e-05**, so every marginal below it is the *diff* and not the fork.

**Read it plainly: moving the structural anchor from the 1H lens to the system's own 4h lens is worth +16.41 R. The 1.0-ATR rail is worth +0.15 R. The 30-day lead-in is worth −1.04 R.** The rail is nearly free — it is cheap insurance that almost never pays out on this corridor, not the engine of the result. **F-3's ruling contained two changes and the estate has been calling the result by the name of the smaller one.** That is finding F-C3-b.

### And the seal did not hold on its own

The corridor starts 2025-10-06 — the day after the sealed lockbox ends. F-5's 30-day lead-in therefore reaches **exactly 30 days into the sealed span**, and F-3's 4h lens quadrupled the anchor lookback's reach in *time*, from 200 hours to 800. Those two rulings met:

> **Executing the card literally quotes the low of the SEALED 4h bar `2025-09-15T12:00Z` as a scored trade's structural anchor** — published in the journal, used as the R denominator, and paid out as the exit price when that stop fires. Every anchor that trade could reach was sealed; **without a lockbox read the trade does not exist at all.**

The card has no seal floor. **The CLASS line does** — *"NO lockbox read; 462 sealed days untouched"* — and the estate's own precedent is unambiguous: when Tier-C2's ratified corridor collided with the seal, *"the corridor moved, the seal did not."* So the seal moves nothing here either. **Sealed bars are masked out of anchor eligibility** (`sealed_mask` → `struct_stop_4h(..., forbidden=)`), and a tranche left with no admissible anchor is simply not taken — **2 armings refused, both ETHUSDT long.**

**This is not a card diff and must never be read as one.** It is the CLASS line enacted, it is printed both ways (cell A vs cell A0 above), and it costs the book −1.0463 R by removing one *losing* trade. **The operator can overturn it in one line — F-C3-a.**

*(Found by an adversarial audit after the draft was already published, not by the fixtures. The fixture that would have caught it did not exist and now does: **F-C3-SEAL** resolves every scored trade's anchor back to the bar it was quoted from and asserts that bar is not sealed. v1 was clean here **by arithmetic accident** — a 200-bar 1H lookback reaches 8.3 days and v1's earliest entry was 24 days after the seal.)*

---

## 1 · THE CARD DIFFS, VERBATIM

Everything not listed here **byte-inherits — and the inheritance is by import, not by copy.** `build_4h`, `_crosses`, `armings`, `Frame4h`, `Arming` and the program's loaders, table writer, F-KEY, headline aggregation and the entire Amendment-B1 tape are **bound to Tier-C2's own objects**. **F-C3-INHERIT asserts twelve of those identities with `is`.**

```
STOP ["stop"] [F-3]: structural anchor BEYOND THE NEAREST REAL 4h SWING PIVOT
  (the system's own lens; 1H pivots are RETIRED from this card), offset 0.5 x
  ATR_4h beyond it; RAIL: stop distance = max(pivot distance, 1.0 x ATR_4h at
  entry); R = entry-stop distance; one unit; one position per asset
STOP EXECUTION [F-4]: THE STOP EXECUTES. A bar touching the stop exits AT the
  stop, ADVERSE-FIRST — if one bar touches both the stop and a bell, the stop
  is taken. No intrabar path is modelled.
LEAD-IN [F-5]: armings are admitted from scored_start - 30d; a trade is SCORED
  iff its ENTRY bar lies inside the scored window
STRIPS [F-7]: every display-only continuity strip truncates at 2026-07-07T23:59Z
SEAL FLOOR [CLASS, not a card diff]: no pivot lying on a SEALED bar may be an
  anchor. An anchor is a PRICE that is published, denominates R and is paid out
  on a stop — not a recursion state — so the CLASS line "NO lockbox read" masks
  it. A trade left with no admissible anchor is NOT TAKEN. Printed both ways.
```

**CORRIDOR [F-1/F-2] — UNCHANGED**, `2025-10-06 → 2026-01-31`, held byte-identical to v1 so the v1↔v3 delta is a delta in the **card**, not the corridor. Label carried on every headline row: **"YARDSTICK v3 — PROVISIONAL (one regime, n small)"**.

**UNCHANGED, re-read from Tier-C2's register:** universe · lens 4h · tide 89/316 · window 12/89 with d = 0.75 (strip {0.50, 1.00} reprinted unscored) · trigger 12/26 at close · ride untouched · bell counter-12/89 or 89/316-against · one unit, one position per asset · net of 10 bps round trip (**derived** as 2 × `fee_bps_side`, never typed) + journaled funding · Amendment B1 tape captured-not-consulted. **`PIVOT_LOOKBACK_1H` is inherited but RETIRED** — F-C3-INHERIT proves the name does not occur in `build_pivots_4h` or `struct_stop_4h`.

**The new register rows, each cited to its ruling:**

| constant | value | source |
|---|---:|---|
| `MIN_STOP_ATR` | **1.0** | F-3 ruling. Wider than the estate's own `min_stop_atr: 0.5` (`configs/tc1_B.yaml:53`, G-8c) |
| `PIVOT_LOOKBACK_4H` | **200** | byte-inherited from `engine/trading.py:222` — 200 bars **in the pivot's own lens**, 1h there, 4h here. **This is the row that quadrupled the reach in time.** See F-C3-c |
| `LEAD_IN_DAYS` | **30** | F-5 ruling; the span v1's F-5 itself measured |
| `STRIP_TRUNCATE` | **2026-07-07T23:59:59Z** | F-7 ruling; VR-1's forward edge |
| `SEAL_FLOOR_ON_ANCHOR` | **True** | **not a card diff** — the CLASS line enacted; precedent Tier-C2 §0 |

**Two readings named.** *"REAL 4h swing pivot"* is the estate's own strict `(5,5)` pivot on the 4h series (`engine/s1._pivots`) — same shape, new lens; **F-C3-PIVOT re-tests the strictness on raw bars.** And **the rail does not invent a stop where structure names none**: with no admissible anchor the tranche is refused, because the card rails a *distance*, it does not replace the *anchor*.

---

## 2 · THE FUNNEL v3 — where the system leaks, with the left edge counted

| asset | dir | seen | in-win | lead-in | tide | d | trig | entered | scored | leak tide | leak d | leak no-trig | **leak sealed** |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTCUSDT | long | 8 | 6 | 2 | 0 | 0 | 0 | 0 | 0 | **8** | 0 | 0 | 0 |
| BTCUSDT | short | 8 | 7 | 1 | 5 | 3 | 3 | 3 | 3 | 3 | 2 | 0 | 0 |
| ETHUSDT | long | 5 | 3 | 2 | 2 | 2 | 2 | **0** | 0 | 3 | 0 | 0 | **2** |
| ETHUSDT | short | 5 | 4 | 1 | 2 | 1 | 1 | 1 | 1 | 3 | 1 | 0 | 0 |
| NEARUSDT | long | 5 | 3 | 2 | 1 | 1 | 1 | 1 | **1** | 4 | 0 | 0 | 0 |
| NEARUSDT | short | 5 | 4 | 1 | 3 | 3 | 2 | 2 | 2 | 2 | 0 | 1 | 0 |
| SOLUSDT | long | 5 | 4 | 1 | 1 | 1 | 0 | 0 | 0 | 4 | 0 | 1 | 0 |
| SOLUSDT | short | 6 | 5 | 1 | 3 | 3 | 3 | 3 | 3 | 3 | 0 | 0 | 0 |
| ZECUSDT | long | 3 | 3 | 0 | 3 | 3 | 1 | 1 | 1 | 0 | 0 | 2 | 0 |
| ZECUSDT | short | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 |
| **ALL** | | **54** | **43** | **11** | **20** | **17** | **13** | **11** | **11** | **34** | **3** | **4** | **2** |

`leak_position_open = 0` · `leak_no_struct_anchor = 0` · `leak_degenerate_R = 0` · `entered_lead_in = 0`. F-KEY asserts five reconciliation identities plus `entered == entered_scored + entered_lead_in`.

**The tide is still the whole funnel** — 34 of 54, still removed *by direction, wholesale*. **In-window armings are 43, identical to v1's 43**: the lead-in added armings without disturbing the ones v1 counted.

### THE F-5 TRIPLE, and what the left edge was worth

| | |
|---|---:|
| armings **in window** | 43 |
| armings **in the lead-in** | 11 |
| of those, passed tide **and** d | **4** |
| scored trades | **11** |
| scored trades **armed in the lead-in** | **1** |
| lead-in trades entered and unscored | **0** |
| in-window triggers blocked by an open position | **0** |

**v1's F-5 predicted the first two exactly** — its §9 said *"4 armings passed tide + d in the 30 days before, 2 of them triggered inside the scored window."* v3 measures **4** and **2 triggered**; of those two, **one survives the seal floor and one does not.** The complete account: ETHUSDT long armed 2025-09-11 → **refused, every reachable anchor sealed**; ETHUSDT long armed 2025-10-01 → **refused, same**; NEARUSDT long armed 2025-10-02 → entered 2025-10-08, **scored, −1.0418**; SOLUSDT long armed 2025-10-02 → **never triggered**.

**The one trade the lead-in bought is a loser.** The edge correction cost 1.04 R. **It is a correction, not a gift, and it went the unhelpful way** — a lead-in that only ever added winners would deserve suspicion.

### The `d` sensitivity strip — UNSCORED, counts only, both populations

| population | d = 0.50 | **d = 0.75 (ratified)** | d = 1.00 |
|---|---:|---:|---:|
| in-window armings (v1-comparable) | 15 / 16 · 93.75% | **13 / 16 · 81.25%** | 10 / 16 · 62.50% |
| in-window + lead-in | 19 / 20 · 95.00% | **17 / 20 · 85.00%** | 14 / 20 · 70.00% |

The first row reproduces v1's strip exactly. No R is attached to any row.

---

## 3 · THE HEADLINE v3

> **YARDSTICK v3 — PROVISIONAL (one regime, n small)**
> **SCORED 2025-10-06 → 2026-01-31 · 5 assets · both directions · 11 trades**

| | value |
|---|---:|
| **net R** | **+7.7614 R** |
| **expectancy / trade** | **+0.7056 R** |
| **win rate** | **45.45%** (5 of 11) |
| **maxDD (R)** | **4.2697 R** |
| tail concentration (top-decile share of winning mass) | 71.83% — one trade of eleven |
| gross R · fee R · funding R | +7.5788 · 0.3849 · −0.5675 |
| best trade · strip-best net R | **+10.0526** · **−2.2912** |

**The yardstick is +0.7056 R per trade, and it is positive. Strip the single best trade and it is −2.2912 R over ten.** Hold both numbers together or hold neither.

| cut | key | n | net R | expectancy | win % | maxDD R |
|---|---|---:|---:|---:|---:|---:|
| asset | BTCUSDT | 3 | −3.1606 | −1.0535 | 0.0 | 3.1606 |
| asset | ETHUSDT | 1 | **+10.0526** | +10.0526 | 100.0 | 0.0000 |
| asset | NEARUSDT | 3 | −1.1349 | −0.3783 | 33.3 | 1.1349 |
| asset | SOLUSDT | 3 | +0.1785 | +0.0595 | 66.7 | 1.0161 |
| asset | ZECUSDT | 1 | +1.8257 | +1.8257 | 100.0 | 0.0000 |
| direction | long | 2 | +0.7839 | +0.3920 | 50.0 | 1.0418 |
| direction | short | 9 | **+6.9775** | +0.7753 | 44.4 | 4.2697 |
| exit | stop | 6 | −6.2345 | −1.0391 | 0.0 | 6.2345 |
| exit | bell_12_89 | 5 | **+13.9959** | +2.7992 | 100.0 | 0.0000 |
| exit | bell_89_316 · corridor_end | 0 | — | — | — | — |

**Monthly equity (R), exit-stamped:** 2025-10 · n 1 · −1.0418 · cum −1.0418 | 2025-12 · n 6 · +8.7355 · cum +7.6937 | 2026-01 · n 4 · +0.0677 · cum **+7.7614**. *(No November row — nothing resolved there. The wider stop pushed v1's November resolution into December: median hold went from **6 bars to 23**, max from **84 to 210**.)*

**Three caveats, all structural:** **n = 11**, every per-asset row n ≤ 3, and **no confidence interval is printed, deliberately** — a bootstrap CI on eleven campaigns would dress an anecdote as a measurement. **The tail metric is near-degenerate** and is named rather than suppressed. **Nine of eleven trades are shorts** — this still measures **one regime**, and a positive number from one regime is not a positive expectancy.

### THE DELTA TABLE — v1 vs v3, per arming

Joined on `(asset, direction, arm_ms)`, **outer**. v1's side is read from the **filed** `research_outputs/tierc2/trade_journal.parquet` (content-sha `58071cf2b4d0c6e7`, the figure v1's §7 recorded) and **never recomputed**. **10 rows `both`, 1 row `v3_only`, 0 rows `v1_only` — no v1 trade was lost.**

| asset · arming | R ÷ ATR v1 → v3 | stop px v1 → v3 | exit v1 → v3 | reason v1 → v3 | net R v1 → v3 | Δ |
|---|---|---|---|---|---|---:|
| BTC short 12-06 | 1.594 → 2.182 | 91812.40 → 92614.30 | 12-08 → 12-09 | stop → stop | −1.0373 → −1.0222 | +0.015 |
| BTC short 12-29 | 1.033 → 1.575 | 88107.14 → 88581.34 | 12-30 → 12-30 | stop → stop | −1.0829 → −1.0545 | +0.028 |
| BTC short 12-31 | 0.585 → 1.197 | 88057.26 → 88531.46 | 01-01 → 01-01 | stop → stop | −1.1743 → −1.0839 | +0.090 |
| **ETH short 10-29** | **0.525 → 1.000** | 3944.67 → **3981.94** | 10-29 → **12-03** | **stop → bell** | **−1.0954 → +10.0526** | **+11.148** |
| NEAR long 10-02 | — → 1.000 | — → 2.886939 | — → 10-09 | — → stop | — → −1.0418 | *new* |
| NEAR short 11-16 | 2.164 → 3.191 | 1.841343 → 1.891343 | 12-09 → **12-28** | **stop → bell** | −1.0124 → +0.9230 | +1.935 |
| NEAR short 12-29 | 1.474 → 1.913 | 1.561921 → 1.575921 | 01-01 → 01-01 | stop → stop | −1.0208 → −1.0161 | +0.005 |
| SOL short 10-30 | 1.404 → 2.702 | 160.480 → 166.010 | 11-12 → **12-03** | **stop → bell** | −1.0310 → +0.8526 | +1.884 |
| SOL short 12-05 | 1.992 → 2.552 | 139.588 → 141.378 | 12-09 → 12-09 | stop → stop | −1.0204 → −1.0161 | +0.004 |
| SOL short 12-11 | 1.183 → 2.697 | 135.435 → 141.205 | 12-11 → **01-02** | **stop → bell** | −1.0362 → +0.3420 | +1.378 |
| ZEC long 12-24 | **1.044 → 1.000** | 434.499 → **435.087** | 01-07 → 01-07 | bell → bell | +1.7487 → +1.8257 | +0.077 |

**The mechanism, in one line: four of ten shared armings changed exit reason from `stop` to `bell_12_89`.** The other six moved by 0.004–0.090 R, which is only the toll shrinking against a wider R. Shared delta **+16.5652**; the ETH row alone is **+11.1480 — 71.8% of the whole 15.5234 swing.**

**THE FLAGGED ROW is pinned by arithmetic, not by hand.** The program finds the tightest v1 R/ATR and then **asserts** it is ETHUSDT short 2025-10-29 — if a re-run moved that row the build HALTs rather than flagging a different trade.

**The F-3 row is not a new price path.** v1's own bell-only counterfactual for it was **+19.1618 R against R = 41.1318** = 788.161 price units; v3's realised outcome is **+10.0526 R against R = 78.4037** = 788.161 price units. **Identical path, different denominator** (|diff| = 3.97e-05, asserted by F-C3-PIVOT). v1 already knew the trade was right; the wider stop is what let it be *held* — and per §0, the width came from the **lens**, not the rail: even without the rail that trade's 4h pivot stop (3965.20) sat above the excursion that killed it in v1 (3962.55).

**ZEC is the counter-example worth keeping.** Its 4h anchor sat *nearer* than v1's 1H anchor (0.651 ATR vs 1.044), so on ZEC the 4h lens **narrowed** R and only the rail pushed it back to 1.000. **The 4h lens does not uniformly widen the stop.**

### Stop geometry v3 — the rail, proven

| | median | min | max |
|---|---:|---:|---:|
| **R ÷ ATR(4h) — v3** | **1.913** | **1.000** | 3.191 |
| R ÷ ATR(4h) — v1 | 1.293 | 0.525 | 2.164 |
| **toll as % of 1R — v3** | **3.06%** | 1.07% | **9.49%** |
| toll as % of 1R — v1 | 3.28% | 1.70% | **19.36%** |

**F-C3-RAIL asserts `R ≥ 1.0 × ATR` on every one of the eleven trades individually**, re-derives `stop = the farther of {pivot stop, rail stop}` per trade, checks `R = max(pivot_dist, rail_dist)` to 1e-6, and confirms `rail_binding` is arithmetic rather than a label. **The rail bound on 3 of 11** — widening those stops by 0.214, 0.059 and 0.349 ATR. Zero rows sit under the v3 rail; zero under G-8c. In v1, 2 of 10 sat under the v3 floor. The worst toll bite halved.

*(Two legs of this fixture — `under_c3_rail` and `under_g8c_rail` — are consistency checks derived from the same `r_dist`, not independent tests. The independent test is the per-trade re-derivation from raw bars in F-C3-PIVOT. Named so the PASS is not read as more than it is.)*

### The bell-only counterfactual — UNSCORED, reprinted

Riding every trade to its bell and honouring no stop gives **−0.0919 R** against the headline's **+7.7614 R**. **In v1 the comparison ran the other way** (+14.8733 bell-only vs −7.7620 stopped). **Do not subtract them.** The populations differ (11 vs 10, different occupancy), and a large part of the cross-version swing is pure R re-denomination of *identical price paths* — the same paths measured against a different denominator, which is exactly what the ETH reconciliation above demonstrates. What can be said: **under the v3 card the stop no longer costs the book money; under the v1 card it cost 22.6 R.** Neither number is scored.

### The lineage row — CENSUS RIDE-ONLY

*(Pinned + labelled historical per CONVENTIONS §6.4 leg 3.)* **Source** CENSUS-2A CEN-5, `BUILD_2026-08-12_CENSUS2A_RUN_6.md` §2.3 · **Era** 2019-10-01 → 2024-06-30 · **Ruler** gross R, size-free, **not** net of toll. loss 5,829 · med −1.0415 | win 814 · mean **+9.4458** | ALL 6,643 · med −1.0324 · mean **+0.3072**. **Not comparable** — different corridor, card, ruler and denominator. Printed for lineage.

---

## 4 · THREE TRADES, HAND-VERIFIED END TO END (F-C3-PIVOT)

Chosen adversarially: **the flagged F-3 row**, **the largest rail widening**, and **the largest R/ATR**. Every leg re-derived from raw 4h bars — including that the anchor **is** a strict `(5,5)` swing pivot, that it was **confirmed by the entry bar**, that it is the **nearest eligible** one beyond entry, and that its **own bar is not sealed**.

| | **ETHUSDT short** (F-3 row) | **ZECUSDT long** (widest rail) | **NEARUSDT short** (widest R) |
|---|---|---|---|
| arming (12/89) | 2025-10-29T16:00Z | 2025-12-24T16:00Z | 2025-11-16T12:00Z |
| tide | e89 4016.83 **<** e316 4115.92, close 3903.54 ✓ | e89 423.13 **>** e316 416.47, close 443.54 ✓ | e89 2.448629 **<** e316 2.459515, close 2.341 ✓ |
| d at cross | 1.444952 ≥ 0.75 ✓ | 1.490507 ≥ 0.75 ✓ | 1.013086 ≥ 0.75 ✓ |
| trigger (12/26) | same bar ✓ | 2025-12-24T20:00Z ✓ | 2025-12-05T08:00Z ✓ |
| entry = bar close | 3903.540000 | 448.450000 | 1.736000 |
| **4h anchor, strict (5,5)** | high **3926.00** @ 2025-10-18T04:00Z | low **446.43** @ 2025-11-28T00:00Z | high **1.867** @ 2025-11-30T16:00Z |
| raw bars around it | prev5 max 3882.00 · next5 max 3907.92 | prev5 min 482.50 · next5 min 450.62 | prev5 max 1.866 · next5 max 1.866 |
| confirmed / lookback / **sealed?** | ✓ · 64 ≤ 200 · **no** | ✓ · 156 ≤ 200 · **no** | ✓ · 23 ≤ 200 · **no** |
| pivot stop (±0.5 ATR) | 3965.201844 | 439.748581 | 1.891343 |
| rail stop (±1.0 ATR) | **3981.943688** | **435.087161** | 1.784686 |
| **stop taken** | **RAIL** 3981.943688 | **RAIL** 435.087161 | **PIVOT** 1.891343 |
| R · R/ATR | 78.403688 · **1.000000** | 13.362839 · **1.000000** | 0.155343 · **3.190712** |
| exit | bell 12/89 2025-12-03T16:00Z @ 3126.78 | bell 12/89 2026-01-07T20:00Z @ 469.38 | bell 12/89 2025-12-28T08:00Z @ 1.594 |
| **F-4 adverse-first** | 210 bars, worst 3962.55 vs 3981.94 ✓ | 84 bars, worst 435.18 vs 435.087 — **by 0.09** ✓ | 138 bars, worst 1.885 vs 1.891343 ✓ |
| **net R** | +9.907187 − 0.044834 − (−0.190248) = **+10.052601** | +1.566284 − 0.034343 − (−0.293782) = **+1.825723** | +0.914106 − 0.010718 − (−0.019629) = **+0.923016** |

**Read the ZEC line.** Its 84-bar ride came within **0.093 price units** of the rail stop and did not touch it. **A wider stop works by surviving excursions it barely survives** — that is a property of one regime's noise, not a law.

**All three reconcile to the journal at 1e-6. 10/10 fixtures PASS.**

---

## 5 · THE ANALYTICS TAPE (Amendment B1) — captured, never consulted

**640 rows**, one per `(asset, ts)`: **43 arming · 10 trigger · 5 exit · 582 daily-00:00Z spine**. *"5 exit" is not six exits missing* — **all eleven exit instants are in the tape**; six are labelled `arming`, because a `bell_12_89` exit **is** a counter 12/89 cross, i.e. the opposite direction's arming on that very bar. Eight spine bars collapse likewise (590 daily bars → 582 labelled `spine`).

**F-C3-6 — no consultation — remains a property, not a promise**, and is now proved over **both** modules in the decision path: AST import scan of `tierc3_rules.py` (`['__future__','dataclasses','engine.s1','numpy','tierc2_rules']` — zero analytics) **and** of `tierc2_rules.py`; an import-closure walk whose project members are exactly `{engine.indicators, tierc2_rules, tierc3_rules}`; `engine/`↛`analytics/` (invariant I-B), so the closure cannot reach a registry symbol by any path; and zero tape column names in either source.

**Two tape facts, raw material, conditioned on nowhere:** the **single-wall stamp is still mostly non-identifying** — `multi` on **35 of 43** armings and **426 of 582 (73.2%)** spine instants, with nulls only in `wall_dist_atr` where `wall_family = "none"`. That is v1's F-6 unchanged, and **F-6 was ruled for the next TC, not this one.** And **the one lead-in-armed scored trade has NULL arming-instant tape columns by construction** — the tape does not cross into the sealed span. Disclosed, never back-filled.

**Q6c is why this tape exists and why it is inert.** This baseline is the unconditioned population of fills the stillbirth counterfactual needs.

---

## 6 · DISPLAY-ONLY STRIPS — F-7 enacted

> **DISPLAY-ONLY — hypothesis generation only, never evidence**

| window | span | trades | net R | expectancy | win % | maxDD R |
|---|---|---:|---:|---:|---:|---:|
| census-scored era | exploration-classic → 2024-06-30 | 127 | +145.4539 | +1.1453 | 18.90% | 39.5073 |
| pinning window | 2026-02-01 → **2026-07-07** | 15 | +12.2566 | +0.8171 | 13.33% | 10.3163 |
| **SEALED LOCKBOX** | 2024-07-01 → 2025-10-05 | **—** | **NOT COMPUTED** | | | |

**F-7 is enacted and proved, not declared.** F-C3-5 asserts each strip's last exit is at or before 2026-07-07T23:59:59Z — CENSUS_ERA 2024-06-07T16:00Z, PINNING **2026-06-22T12:00Z**. v1's strip ran to 2026-08-11 with its last 35 days past that edge.

**The lead-in applies to every window**, each admitting armings from its own start − 30d, with entries in a strip's lead-in excluded from that strip. One code path, so the strips ride the identical card. *(PINNING's lead-in lies wholly inside the scored corridor — noted; the strips live in their own table and are never pooled into `headline.parquet`.)* The census-era strip moved from +34.89 R to +145.45 R under the same card change: **not evidence, only a reminder that the change is not marginal.**

---

## 7 · FIXTURE TRANSCRIPT

**10/10 PASS** — `{"F-C3-1", "F-C3-INHERIT", "F-C3-RAIL", "F-C3-PIVOT", "F-C3-SEAL", "F-C3-ABLATE", "F-C3-4", "F-C3-5", "F-C3-6", "F-KEY"}` all `true`. Reproduce: `~/venvs/naiad/bin/python scripts/tierc3_fixtures.py` (304 lines, local).

| fixture | verdict | evidence |
|---|---|---|
| **F-C3-1** gates | PASS | HEAD · remote `catpatrol/Naiad` · pwd == `$HOME/Naiad` · no cloud-sync token · branch · venv. **ESTATE READY over THREE spans** — corridor (1h 2,832 / 4h 708 per asset), **F-5 lead-in** (720 / 180), **F-7 strip** (3,768 / 942) — all 5 assets × {1h, 4h}, **gaps = 0**, monotonic. |
| **F-C3-INHERIT** | PASS | **12 identities asserted with `is`.** 15 unchanged register values matched; toll **derived**; corridor proved byte-identical to v1; F-7 truncation proved as a diff; `PIVOT_LOOKBACK_1H` proved **retired** (absent from both v3 stop functions). Card v3 echoed verbatim. |
| **F-C3-RAIL** | PASS | **All 11 trades asserted individually.** R/ATR range **1.000000 → 3.190693**. 0 under the v3 rail, 0 under G-8c; v1's filed table read for contrast (2 of 10 under the v3 floor). |
| **F-C3-PIVOT** | PASS | Three trades from raw bars (§4) — strict `(5,5)` re-tested, causal confirmation, lookback, nearest-eligible, rail arithmetic, exit, **F-4 adverse-first over the whole ride**, net R to 1e-6, plus the **cross-version reconciliation** to 3.97e-05. |
| **F-C3-SEAL** *(new — the fixture this build lacked)* | PASS | Every scored trade's anchor **resolved back to its own bar from the raw 4h series** and asserted not sealed: **0 of 11 sealed**, every stored `anchor_bar_ms` agreeing with the independent re-derivation. **2 armings refused** because every reachable anchor was sealed. v1 re-derived on its 1H grid for contrast: **0 of 10** — clean by arithmetic accident, not by design. |
| **F-C3-ABLATE** *(new)* | PASS | **The V1 cell reproduces Tier-C2's filed net R to 2.2e-05** over the same 10 trades, so every marginal is the diff and not the fork. Six cells printed (§0). UNSCORED. |
| **F-C3-4** determinism | PASS | Full re-run into `research_outputs/tierc3_run2/`; **all 14 content-hashes identical and the counts block identical**. Normalized fields: `['elapsed_s']` and the output root path; *no computed value is normalized*. Seed 20260815 printed and **unused** — determinism is structural. |
| **F-C3-5** era exclusions | PASS | **Every `_ms`/`ts` column of every filed table enumerated, not a curated tuple** — v1's scan was a hand-written list and v3's first draft silently dropped `arm_ms` from it, which is how a test passes by construction. Each column judged by the rule that applies to it: entries/exits/tape in-corridor and lockbox-free; `arm_ms` **licensed** by F-5 with its 1 pre-corridor row named; `anchor_bar_ms` **never sealed**. **F-7 asserted** on both strips. `lead_in_trades` empty and outcome-free. |
| **F-C3-6** no consultation | PASS | AST scan of **both** decision modules · import closure · `engine/`↛`analytics/` · zero tape column names (§5). |
| **F-KEY** | PASS | Asserted in-program **and re-asserted against the 13 written tables** — 0 duplicates. Plus six funnel reconciliation identities and `headline.net_r == sum(journal.net_r)`. |

**Suite:** `pytest fixtures tests -m "not slow"` → **323 passed, 1 skipped, 1 deselected, exit 0**, measured **with and without** this build's three scripts and its outputs and identical both ways. *(The count was 314 earlier in this session; commit `7176b6d "ruling 007"` landed from another lane mid-build and added `tests/test_bus_health.py`. Nothing here touched an existing test.)*

---

## 8 · FINDINGS — NOT FIXED

**F-C3-a · THE SEAL FLOOR IS TAKEN, AND IT IS NOT A CARD DIFF.** §0. The card has no floor; executed literally it quotes the low of the sealed bar 2025-09-15T12:00Z as a scored trade's anchor, R denominator and exit price — and that trade has **no** admissible anchor otherwise, so it exists only by a lockbox read. The CLASS line forbids that, and Tier-C2 §0's precedent is that the seal does not move. **Both numbers are on the record: with the floor +7.7614 / 11; without it +6.7151 / 12** (cells A and A0). **Ruling needed: ratify the floor as standing law — an anchor is a price, not a state — or overturn it and accept the sealed read with the disclosure.** Related: the F-5 lead-in inherently reaches 30 days into the seal whenever a corridor starts adjacent to it; **moving future corridor starts 30 days later would close the whole class.**

**F-C3-b · The build is named for the diff that did not move the number.** §0. Anchor lens **+16.4127 R**; rail **+0.1525 R**; lead-in **−1.0445 R**. Every downstream sentence in the estate that credits "the rail" for the sign change is wrong, including this document's own title. **Ruling needed: rename, or ratify the name as historical and record the attribution beside it.** The practical consequence is larger than the naming: **the object a multiplier must beat is the 4h-anchor card, and the rail is a cheap insurance rider on top of it.**

**F-C3-c · The lookback reading is load-bearing and unruled.** F-3 moved the anchor to the 4h lens; the inherited constant is *200 bars in the pivot's own lens* — 200 hours on 1h, **800 hours** on 4h. **That quadrupling is what let the anchor search reach into the seal at all.** The time-equivalent reading (50 bars) is a different card: **only 5 of 11 trades get the same anchor under it.** Counts are in `anchor_lookback_disclosure.parquet` with **no R attached to either reading** — a swept parameter with an outcome beside it is a selection surface. *(An auditor argued the magnitude should be on the record anyway. Both costs are real: withholding it leaves the operator ruling blind, printing it invites picking the better cell. Held at counts; the operator can commission the magnitude as its own probe with m declared first.)* **Ruling needed: pin the lookback in the card, in bars or in hours.**

**F-C3-d · The result still rests on one trade.** ETHUSDT 2025-10-29 is **+11.1480 of the 15.5234 swing (71.8%)** and **10.05 of the 7.76 net R**. Four of ten shared armings changed `stop → bell`; the rest moved by the toll. **This is the same concentration v1 reported from the other side** — v1's bell-only gap was 89.5% that one trade. **Ruling needed: is an 11-trade, one-regime, one-dominant-trade result an acceptable bar for a multiplier to beat?** **PROVISIONAL** is carried on every headline row until it is answered.

**F-C3-e · The estate now holds two rails for one concept.** G-8c rails at `min_stop_atr = 0.5`; the v3 card at **1.0**. Both live, unequal, related nowhere. **Ruling needed: reconcile, or name them as deliberately distinct objects** the way `TC-2` and `Tier-C2` had to be.

**F-C3-f · The 4h lens is not uniformly wider, and one trade proves it.** ZECUSDT's 4h anchor sat *nearer* than its 1H anchor (0.651 vs 1.044 ATR); only the rail restored R to 1.000. Any future card text should say **railed**, not *wider*.

**F-C3-g · No Stage B was built, and the estate's only live-paper artefacts still enact the SUPERSEDED card.** Stage B was not commissioned for Tier-C3 and was not built — but `configs/tierc2_paper.yaml` and `research_outputs/tierc2/heartbeat.json` still ride the **v1** card: 1H anchor, no rail, no lead-in. **The live paper line is one full card version behind the yardstick.** Not fixed — wiring a v3 paper profile is a separate authorised act. **Named because a forward paper line quietly running a superseded card is exactly the kind of drift the estate's conventions exist to catch.**

**F-C3-h · The cross-version bell-only comparison is not like-for-like.** Different populations, and a large share of the swing is R re-denomination of identical paths. Printed unscored. **Do not subtract them.**

**F-C3-i · `exchange/**` auto-publishes, so a build document is published the instant it is written.** A draft of *this* document — headline **+6.7151 / 12**, pre-audit — was committed **and pushed** by an auto-publish from another process at `af6ebf4` while this build was still running. Nothing was lost and no guard failed; the guard did precisely what it is specified to do. But **a draft under `exchange/reports/` is not a draft**, and the superseded number is now in the branch history and on the remote. **Ruling needed: draft build documents outside `exchange/` and move them in when final, or accept that intermediate states are part of the published record.**

**F-C3-j · Carried, unchanged.** F-6's single-wall stamp is still `multi` on 73.2% of spine instants — ruled for the **next** TC, conditioned on nowhere here. And **m = 0 holds**: the replay is a complete, unranked pass over one ratified card. The moment a cut is picked out of §2, §3 or the attribution table on its R, the selection surface is the number of cells that were available to pick from, and that *m* must be declared **before** the look.

---

## 9 · DISPOSITION + BOX-COST

| item | disposition |
|---|---|
| `scripts/tierc3_rules.py` | **new** — decision path; analytics-free by import closure; Tier-C2's objects bound, not copied |
| `scripts/tierc3_baseline.py` | **new** — replay · tape · tables · delta · attribution |
| `scripts/tierc3_fixtures.py` | **new** — 10/10 PASS, HALTs non-zero |
| `research_outputs/tierc3/` | **built** — 14 parquet + manifest, local, gitignored |
| `research_outputs/tierc3_run2/` | **built, hashed, DATA DISCARDED** per rule R3; `build_manifest.json` retained per refinement D-3 |
| `.gitignore` | **modified** — `research_outputs/tierc3{,_run2}/**` |
| `RULES_OF_RECORD_VIZ_IRON_2026-08-15.md` | **new** — the F-1 promotion; **V-10 closes by ruling** |
| THE HEADLINE | **+0.7056 R / trade over 11 trades**, positive, **PROVISIONAL** |
| THE ATTRIBUTION | **built** — the rail is +0.15 R; the anchor lens is +16.41 R |
| THE SEAL | **held, and now enforced in code** — 0 of 11 anchors sealed, 2 tranches refused, proved per trade by F-C3-SEAL |
| `engine/` · `analytics/` · `scripts/tierc2_*` · `com.naiad.daily` | **UNTOUCHED** — zero diff |
| registrations | **none**, as classed |

### BOX-COST

`exchange/**` measured **2,753,943 B = 17.21%** of the 16,000,000 B box **before this paste**; the governing **tick set** (`exchange/**` + `LEDGER.md`) **3,003,049 B = 18.77%** — state **OK** (warn 40% / refuse 70%).

**This paste adds 50,439 B = 0.315% of the box** — this document (39,334 B), the `LEDGER_APOLLO` append (10,192 B) and the one-line rules-of-record file (913 B) — taking `exchange/**` to **2,804,382 B = 17.53%** and the tick set to **3,063,680 B = 19.15%**, level **OK**, headroom to REFUSE **8,136,320 B**. **Against the < 0.5% target (80,000 B) that is 63% of budget, with ≈ 29 KB unspent.**

*(Two disclosures on those figures. The superseded draft at `af6ebf4` is inside them — it was overwritten in place, not added beside. And the "before" is larger than the 2,725,828 B this session first measured because commit `7176b6d` from another lane landed its own reports into `exchange/**` mid-build; the delta attributed to this paste is this paste's alone.)*

The full fixture transcript (304 lines), the 640-row tape, and the per-trade journal beyond the three in §4 stay **local**. **What is printed whole is what a reader cannot re-derive from a pointer: the card diffs, the attribution, the funnel, the headline, the delta, and the findings.**

**Constants: pin-vs-import per site, per CONVENTIONS §6.4.** `tierc3_rules.py` **defines** the five new values and **inherits** every other by import from `tierc2_rules.REGISTER`. `BOX_BYTES`/`WARN_FRACTION`/`REFUSE_FRACTION` were **read live from `publish_exchange`**, not typed. **Ledger citations in this build are by QUOTE, not by line** — both of Tier-C2's line citations were moved ~50 lines by commit `cf0240b` on the same day, which is precisely the failure the estate's "cite by section, not line" ruling exists to prevent.

---

## 10 · THE LEDGER_APOLLO APPEND

Per the 2026-08-12 `append` ruling — *a report without its ledger entry is an incomplete deliverable* — this document ends by appending the session's STATUS entry to `exchange/status/LEDGER_APOLLO.md`, **in this session**. Quoted by its spine only.

```
=== STATUS_APOLLO — 2026-08-15g ===
NOW: TIER-C3 IS MEASURED. The railed baseline is +0.7056 R per trade over 11
     trades, 2025-10-06 -> 2026-01-31, against TIER-C2's -0.7762 R over 10.
     THE NUMBER CHANGED SIGN — AND IT WAS NOT THE RAIL. Attribution, measured:
     the 1H -> 4h ANCHOR LENS is +16.4127 R; the 1.0-ATR RAIL is +0.1525 R;
     the 30-day LEAD-IN is -1.0445 R. PROVISIONAL: one regime, n = 11, and one
     trade is 71.8% of the swing.
     THE SEAL HELD, BUT NOT BY ITSELF: executing the card literally quotes a
     SEALED bar's low as a scored trade's anchor, R denominator and exit price.
     The CLASS line masks sealed bars out of anchor eligibility. Both numbers
     printed: with the floor +7.7614/11, without it +6.7151/12. F-C3-a.
Q6 DECISION RULE, RE-INVOKED AGAINST v3: Q6c still governs. v3 is a SECOND
     unconditioned population of fills over the same corridor, and its 640-row
     tape is the location record it must be rescored against. No location gate
     is proposed, and none may be until the rescore is done.
PENDING: [F-C3-a..j; a/b/c/d/e need operator rulings]
PROBE LEDGER: m = 0. EXPLORATION — ungated; promotion requires registration.
=== END STATUS ===
```

---

*End of build document. TIER-C3 · measurement, not registration · m = 0 · no outcome, price or anchor drawn from a sealed bar · no registrations. The yardstick is positive, thin, PROVISIONAL — and it was the lens, not the rail.*
