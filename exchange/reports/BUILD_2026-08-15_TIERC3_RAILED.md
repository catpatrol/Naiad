# BUILD — TIER-C3 · THE RAILED BASELINE

**Date** 2026-08-15 · **Branch** `v12-v1-census` · **HEAD at start** `20f23a1` · **Seed** 20260815 · **Drafted** APOLLO · **Executor** HEPHAESTUS

**RATIFIED** operator 2026-08-15 — *"I rule the seven F's on your lean."* This build enacts the seven Tier-C2 findings as card diffs and re-measures.

**CLASS — measurement, not registration. m = 0.** No registration. **No lockbox read for outcomes** — the 462 sealed days stay unspent. No estate write. No live orders. F-KEY on every join. The population is a *complete* replay of one ratified rule card over one corridor: nothing was selected, swept or promoted, so there is no family to correct over. Any future selection **from** these tables is a new probe and declares its own *m* before it looks.

**Programs (local, this repo):** `scripts/tierc3_rules.py` (the decision path) · `scripts/tierc3_baseline.py` (the program) · `scripts/tierc3_fixtures.py` (the transcript). **Tables live local** at `research_outputs/tierc3/` — `funnel`, `lead_in_census`, `lead_in_trades`, `headline`, `monthly_equity`, `stop_geometry`, `delta_v1_v3`, `anchor_lookback_disclosure`, `trade_journal`, `strip_d_unscored`, `display_only_strips`, `analytics_tape`, `tape_inventory` (all `.parquet`) + `build_manifest.json`.

**I9** — `ANALYTICS_VERSION` **1.5.0**, `analytics_sha()` `ea5f02f21ca43b6b71e450b540ff09c807b305971e3eb8cff50bea84c985dc91`. Instrument: **BINANCE USDT-M perpetuals**, `{BTC,ETH,SOL,NEAR,ZEC}USDT.P`, offline kline cache `~/.cache/naiad/data_cache/klines`.

**V-10 — CLOSED BY RULING.** `DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md` was sought once more and is **ABSENT** (not attached, not in the tree). Per the F-1 ruling, VIZ-4's inline restatement of the iron rules is **promoted to the rules of record** — one line, filed at `exchange/reports/RULES_OF_RECORD_VIZ_IRON_2026-08-15.md`, cited to the VIZ-4 contract §Class. VIZ-3 stops being cited. **The chase is over.**

---

## 0 · THE ONE THING THE OPERATOR MUST READ FIRST

**The yardstick changed sign. v1 was −0.7762 R per trade; v3 is +0.5596 R per trade. And 67% of the improvement is one trade.**

| | TIER-C2 (v1) | **TIER-C3 (v3)** |
|---|---:|---:|
| net R | −7.7620 | **+6.7151** |
| expectancy / trade | −0.7762 | **+0.5596** |
| n | 10 | 12 |
| win rate | 10.00% | **41.67%** |
| maxDD (R) | 9.5107 | **4.2697** |
| bell-only counterfactual (unscored) | +14.8733 | **−2.1634** |

Same corridor, same tide, same window, same trigger, same bell, same toll. **Only the stop changed, plus a 30-day lead-in.** The decomposition is exact and it is the honest reading:

```
  v1 net R                                                    −7.7620
  + the 10 SHARED armings, re-stopped under the v3 card       +16.5652
  + the 2 trades the F-5 lead-in admitted (both losers)        −2.0881
  ────────────────────────────────────────────────────────────────────
  v3 net R                                                    +6.7151
```

Of the **+16.5652** on shared armings, **+11.1480 (67.3%) is one arming** — ETHUSDT short, 2025-10-29, the exact trade v1's F-3 finding was about. **Four of the ten shared armings changed exit reason from `stop` to `bell_12_89`**; the other six moved by 0.004–0.090 R, which is only the toll shrinking against a wider R. **This is not ten independent confirmations that the rail works. It is four survivals, one of them enormous.**

**AND THE LEAD-IN TOUCHES THE SEAL.** The corridor starts 2025-10-06 — the day *after* the sealed lockbox ends. So F-5's 30-day lead-in reaches **exactly 30 days into the sealed span** (2025-09-06 → 2025-10-05). That was not avoidable under the ruling and it is not hidden:

- An arming may be **seen** there. Reading a 12/89 cross is EMA state — the same class of act as the warm-up traversal already on the record (`LEDGER.md:121`, F4-a: *"traversal is not emission"*).
- **A trade is SCORED iff its ENTRY bar is inside the corridor.** Every scored outcome in this build is computed from post-lockbox bars only; `LEDGER.md:865` puts the seal on **scored outcome evidence**, and none is computed inside it.
- A trade that **enters** during the lead-in gets **no outcome at all** — no gross R, no net R, no prices. It appears only in `lead_in_trades.parquet` as the occupancy fact it is, because a position open across the left edge blocks in-window triggers and dropping it would invent trades the card would not have taken. **One such trade exists** (ETHUSDT long, entered 2025-09-18, released 2025-09-21). It blocked nothing.
- **But two scored trades now carry an arming timestamp inside the sealed span** (2025-10-01T20:00Z, 2025-10-02T08:00Z) and a `disp_at_arming` computed on a sealed bar. v1's F-C2-5 asserted *zero* journal rows with lockbox stamps; under the F-5 ruling that is no longer true of `arm_ms`. **It is asserted, counted and disclosed by F-C3-5 rather than quietly allowed — and it is finding F-C3-a below.**

---

## 1 · THE CARD DIFFS, VERBATIM

Everything not listed here **byte-inherits — and the inheritance is by import, not by copy.** `tierc3_rules.build_4h`, `_crosses`, `armings`, `Frame4h`, `Arming` and the program's loaders, table writer, F-KEY, headline aggregation and the entire Amendment-B1 tape are **bound to Tier-C2's own objects**. A copied function can drift; a bound one cannot. **F-C3-INHERIT asserts twelve of these identities with `is`.**

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
```

**CORRIDOR [F-1/F-2] — UNCHANGED**, `2025-10-06 → 2026-01-31`, held byte-identical to v1 so the v1↔v3 delta is a delta in the **card** and not in the corridor. Label carried on every headline row: **"YARDSTICK v3 — PROVISIONAL (one regime, n small)"**.

**UNCHANGED and re-asserted from Tier-C2's own register:** universe · lens 4h · tide 89/316 · window 12/89 with d = 0.75 (strip {0.50, 1.00} reprinted unscored) · trigger 12/26 at close · ride untouched · bell counter-12/89 or 89/316-against · one unit, one position per asset · net of 10 bps round trip (**derived** as 2 × `fee_bps_side`, never typed) + journaled funding · Amendment B1 tape captured-not-consulted.

**The four new register rows, each cited to its ruling** (`tierc3_rules.REGISTER_DIFF`, printed in full by F-C3-INHERIT):

| constant | value | source |
|---|---:|---|
| `MIN_STOP_ATR` | **1.0** | F-3 ruling. Strictly **wider** than the estate's own rail `min_stop_atr: 0.5` (`configs/tc1_B.yaml:53`, engine G-8c) — the rail v1's F-3 found absent from the card |
| `PIVOT_LOOKBACK_4H` | **200** | byte-inherited from `engine/trading.py:222` — 200 bars **in the pivot's own lens**, which was 1h there and is 4h here. See F-C3-b |
| `LEAD_IN_DAYS` | **30** | F-5 ruling; 30 is the span v1's F-5 itself measured |
| `STRIP_TRUNCATE` | **2026-07-07T23:59:59Z** | F-7 ruling; VR-1's forward edge |

**Two readings named, not left implicit.** *"REAL 4h swing pivot"* is read as the estate's own strict `(5, 5)` pivot on the 4h series (`engine/s1._pivots`) — same shape as the retired 1H one, new lens; **F-C3-PIVOT verifies the strictness on raw bars**. And **the rail does not invent a stop where structure names none**: with no eligible anchor the tranche is refused (`no_struct_anchor`), exactly as in v1, because the card rails a *distance*, it does not replace the *anchor*.

---

## 2 · THE FUNNEL v3 — where the system leaks, with the left edge counted

Per asset × direction, cumulative by construction. The three new columns are the F-5 edge bias **measured**.

| asset | dir | seen | in-window | lead-in | tide | d | trig | entered | leak tide | leak d | leak no-trig |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTCUSDT | long | 8 | 6 | 2 | 0 | 0 | 0 | 0 | **8** | 0 | 0 |
| BTCUSDT | short | 8 | 7 | 1 | 5 | 3 | 3 | 3 | 3 | 2 | 0 |
| ETHUSDT | long | 5 | 3 | 2 | 2 | 2 | 2 | **2** | 3 | 0 | 0 |
| ETHUSDT | short | 5 | 4 | 1 | 2 | 1 | 1 | 1 | 3 | 1 | 0 |
| NEARUSDT | long | 5 | 3 | 2 | 1 | 1 | 1 | **1** | 4 | 0 | 0 |
| NEARUSDT | short | 5 | 4 | 1 | 3 | 3 | 2 | 2 | 2 | 0 | 1 |
| SOLUSDT | long | 5 | 4 | 1 | 1 | 1 | 0 | 0 | 4 | 0 | 1 |
| SOLUSDT | short | 6 | 5 | 1 | 3 | 3 | 3 | 3 | 3 | 0 | 0 |
| ZECUSDT | long | 3 | 3 | 0 | 3 | 3 | 1 | 1 | 0 | 0 | 2 |
| ZECUSDT | short | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 |
| **ALL** | | **54** | **43** | **11** | **20** | **17** | **13** | **13** | **34** | **3** | **4** |

`leak_position_open = 0` · `leak_no_struct_anchor = 0` · `leak_degenerate_R = 0`. **Entered 13 = 12 scored + 1 unscored lead-in entry** (F-KEY asserts that identity).

**The tide is still the whole funnel** — 34 of 54 armings, still removed *by direction, wholesale*. **In-window armings are 43, identical to v1's 43**, which is the check that the lead-in added armings without disturbing the ones v1 counted.

### THE F-5 TRIPLE, and what the left edge was actually worth

| | |
|---|---:|
| armings **in window** | 43 |
| armings **in the lead-in** | 11 |
| of those, passed tide **and** d | **4** |
| scored trades | **12** |
| scored trades **armed in the lead-in** | **2** |
| lead-in trades, entered and **unscored** | 1 |
| in-window triggers blocked by an open position | **0** |

**v1's F-5 predicted this exactly.** Its §9 said *"in the 30 days before it, 4 armings passed tide + d and 2 of them triggered inside the scored window."* v3 measures **4** and **2**. The complete account of the four: ETHUSDT long armed 2025-09-11 → entered 2025-09-18, **unscored**; ETHUSDT long armed 2025-10-01 → entered 2025-10-08, **scored**; NEARUSDT long armed 2025-10-02 → entered 2025-10-08, **scored**; SOLUSDT long armed 2025-10-02 → **never triggered**.

**Both trades the lead-in bought are losers** (−1.0463, −1.0418). The edge correction cost 2.09 R. **It is a correction, not a gift — and it is worth saying that it went the unhelpful way**, because a lead-in that only ever added winners would deserve suspicion.

### The `d` sensitivity strip — UNSCORED, counts only, both populations

| population | d = 0.50 | **d = 0.75 (ratified)** | d = 1.00 |
|---|---:|---:|---:|
| in-window armings (v1-comparable) | 15 / 16 · 93.75% | **13 / 16 · 81.25%** | 10 / 16 · 62.50% |
| in-window + lead-in | 19 / 20 · 95.00% | **17 / 20 · 85.00%** | 14 / 20 · 70.00% |

The first row reproduces v1's strip exactly. No R is attached to any row: a swept threshold with an outcome beside it is a selection surface, and this one has *m* = 0 because nothing was selected.

---

## 3 · THE HEADLINE v3 — the yardstick, stated plainly

> **YARDSTICK v3 — PROVISIONAL (one regime, n small)**
> **SCORED 2025-10-06 → 2026-01-31 · 5 assets · both directions · 12 trades**

| | value |
|---|---:|
| **net R** | **+6.7151 R** |
| **expectancy / trade** | **+0.5596 R** |
| **win rate** | **41.67%** (5 of 12) |
| **maxDD (R)** | **4.2697 R** |
| tail concentration (top-decile share of winning mass) | 71.83% — one trade of twelve, see caveat 2 |
| gross R · fee R · funding R | +6.5788 · 0.4296 · −0.5659 |
| best trade · strip-best net R | **+10.0526** · **−3.3375** |

**The yardstick is +0.5596 R per trade, and it is positive.** Stated positive or not, as commissioned. **Strip the single best trade and it is −3.3375 R over eleven** — that is the number the operator should hold beside it.

**Per asset · per direction · per exit**

| cut | key | n | net R | expectancy | win % | maxDD R |
|---|---|---:|---:|---:|---:|---:|
| asset | BTCUSDT | 3 | −3.1606 | −1.0535 | 0.0 | 3.1606 |
| asset | ETHUSDT | 2 | **+9.0063** | +4.5032 | 50.0 | 1.0463 |
| asset | NEARUSDT | 3 | −1.1349 | −0.3783 | 33.3 | 1.1349 |
| asset | SOLUSDT | 3 | +0.1785 | +0.0595 | 66.7 | 1.0161 |
| asset | ZECUSDT | 1 | +1.8257 | +1.8257 | 100.0 | 0.0000 |
| direction | long | 3 | −0.2624 | −0.0875 | 33.3 | 2.0881 |
| direction | short | 9 | **+6.9775** | +0.7753 | 44.4 | 4.2697 |
| exit | stop | 7 | −7.2808 | −1.0401 | 0.0 | 7.2808 |
| exit | bell_12_89 | 5 | **+13.9959** | +2.7992 | 100.0 | 0.0000 |
| exit | bell_89_316 · corridor_end | 0 | — | — | — | — |

**Monthly equity (R), exit-stamped**

| month | n | net R | cumulative |
|---|---:|---:|---:|
| 2025-10 | 2 | −2.0881 | −2.0881 |
| 2025-12 | 6 | +8.7355 | +6.6474 |
| 2026-01 | 4 | +0.0677 | **+6.7151** |

*(No 2025-11 row: nothing resolved in November. The wider stop pushed v1's November resolution into December — median hold went from **6 bars to 22**, max from **84 to 210**.)*

**Three caveats, all structural, all carried forward from v1:**

1. **n = 12.** Twelve trades over 118 days across five assets; every per-asset row is n ≤ 3. **No confidence interval is printed, deliberately** — a bootstrap CI on twelve campaigns would dress an anecdote as a measurement.
2. **The tail metric is still nearly degenerate and is printed anyway.** With n = 12 the top decile is one trade; 71.83% is arithmetic about one trade, not a finding about a distribution. Named rather than suppressed, because the estate has four incompatible tail metrics.
3. **Nine of twelve trades are still shorts.** This baseline still measures **one regime**. A positive number from one regime is not a positive expectancy.

### THE DELTA TABLE — v1 vs v3, per arming

Joined on the arming itself, `(asset, direction, arm_ms)`, **outer** — because the two cards do not agree on which armings become trades. v1's side is read from the **filed** `research_outputs/tierc2/trade_journal.parquet` (content-sha `58071cf2b4d0c6e7`, the figure v1's own §7 recorded) and is **never recomputed**: this build must not be able to move v1's number while comparing itself to it. **10 rows `both`, 2 rows `v3_only`, 0 rows `v1_only` — no v1 trade was lost.**

| asset · arming | R ÷ ATR v1 → v3 | entry | stop px v1 → v3 | exit v1 → v3 | reason v1 → v3 | net R v1 → v3 | Δ |
|---|---|---:|---|---|---|---|---:|
| BTC short 12-06 | 1.594 → 2.182 | 89636.50 | 91812.40 → 92614.30 | 12-08 → 12-09 | stop → stop | −1.0373 → −1.0222 | +0.015 |
| BTC short 12-29 | 1.033 → 1.575 | 87203.30 | 88107.14 → 88581.34 | 12-30 → 12-30 | stop → stop | −1.0829 → −1.0545 | +0.028 |
| BTC short 12-31 | 0.585 → 1.197 | 87603.70 | 88057.26 → 88531.46 | 01-01 → 01-01 | stop → stop | −1.1743 → −1.0839 | +0.090 |
| **ETH short 10-29** | **0.525 → 1.000** | 3903.54 | 3944.67 → **3981.94** | 10-29 → **12-03** | **stop → bell_12_89** | **−1.0954 → +10.0526** | **+11.148** |
| ETH long 10-01 | — → 1.268 | 4523.67 | — → 4423.48 | — → 10-09 | — → stop | — → −1.0463 | *new* |
| NEAR long 10-02 | — → 1.000 | 2.964 | — → 2.886939 | — → 10-09 | — → stop | — → −1.0418 | *new* |
| NEAR short 11-16 | 2.164 → 3.191 | 1.736 | 1.841343 → 1.891343 | 12-09 → **12-28** | **stop → bell_12_89** | −1.0124 → +0.9230 | +1.935 |
| NEAR short 12-29 | 1.474 → 1.913 | 1.515 | 1.561921 → 1.575921 | 01-01 → 01-01 | stop → stop | −1.0208 → −1.0161 | +0.005 |
| SOL short 10-30 | 1.404 → 2.702 | 154.50 | 160.480 → 166.010 | 11-12 → **12-03** | **stop → bell_12_89** | −1.0310 → +0.8526 | +1.884 |
| SOL short 12-05 | 1.992 → 2.552 | 133.22 | 139.588 → 141.378 | 12-09 → 12-09 | stop → stop | −1.0204 → −1.0161 | +0.004 |
| SOL short 12-11 | 1.183 → 2.697 | 130.93 | 135.435 → 141.205 | 12-11 → **01-02** | **stop → bell_12_89** | −1.0362 → +0.3420 | +1.378 |
| ZEC long 12-24 | **1.044 → 1.000** | 448.45 | 434.499 → **435.087** | 01-07 → 01-07 | bell → bell | +1.7487 → +1.8257 | +0.077 |

**THE FLAGGED ROW is pinned by arithmetic, not by hand.** The program identifies the tightest v1 R/ATR and then **asserts** it is ETHUSDT short 2025-10-29 — if a re-run ever moved that row, the build HALTs rather than flagging a different trade.

**The F-3 row is not a new price path.** v1's own bell-only counterfactual for that trade was **+19.1618 R against R = 41.1318** = 788.161 price units. v3's realised outcome is **+10.0526 R against R = 78.4037** = 788.161 price units. **Identical path, different denominator** (|diff| = 3.97e-05, F-C3-PIVOT asserts it). v1 already knew this trade was right; the rail is what let it be *held*.

**And the rail is not the whole story.** Of the +16.5652 on shared armings, **+11.2250 came from the two trades the rail actually bound** (ETH, ZEC) and **+5.3402 from the eight it did not** — those were widened by the move to the 4h anchor alone. **ZEC is the counter-example worth keeping**: its 4h anchor sat *nearer* than v1's 1H anchor (0.651 ATR against 1.044), so on ZEC the 4h lens **narrowed** R and only the rail pushed it back to 1.000. **The 4h lens does not uniformly widen the stop.**

### Stop geometry v3 — the rail, proven

| | median | min | max |
|---|---:|---:|---:|
| **R ÷ ATR(4h) at entry — v3** | **1.744** | **1.000** | 3.191 |
| R ÷ ATR(4h) at entry — v1 | 1.293 | 0.525 | 2.164 |
| **toll as % of 1R — v3** | **3.25%** | 1.07% | **9.49%** |
| toll as % of 1R — v1 | 3.28% | 1.70% | **19.36%** |

**F-C3-RAIL asserts `R ≥ 1.0 × ATR` on every one of the twelve trades individually**, re-derives `stop = the farther of {pivot stop, rail stop}` per trade, checks `R = max(pivot distance, rail distance)` to 1e-6, and confirms `rail_binding` is arithmetic rather than a label. **The rail bound on 3 of 12** (ETH short 10-29, NEAR long 10-08, ZEC long 12-24), widening those stops by 0.214, 0.059 and 0.349 ATR. **Zero rows sit under the v3 rail; zero sit under the estate's G-8c 0.5 rail.** In v1, **2 of 10 sat under the v3 floor and 0 under G-8c**. The worst toll bite halved, from 19.36% of R to 9.49%.

### The bell-only counterfactual — UNSCORED, reprinted

Riding every trade to its bell and honouring no stop gives **−2.1634 R** against the headline's **+6.7151 R**. **In v1 that comparison ran the other way** (+14.8733 bell-only against −7.7620 stopped). **Do not read the reversal as "the stop is now worth +8.9 R."** Two things forbid it: the trade populations differ (12 vs 10, with different occupancy), and v1's bell-only figure was itself 89.5% one trade — the same ETH trade the v3 card now *realises* rather than counterfactualises. What can be said plainly: **under the v3 card the stop no longer costs the book money, and under the v1 card it cost 22.6 R.** Neither number is scored.

### The lineage row, printed beside — CENSUS RIDE-ONLY

*(Pinned + labelled historical per CONVENTIONS §6.4 leg 3 — it reproduces a filed record and must never track a live value.)*

> **Source** CENSUS-2A CEN-5, `BUILD_2026-08-12_CENSUS2A_RUN_6.md` §2.3 · **Era** 2019-10-01 → 2024-06-30 (exploration-classic) · **Ruler** gross R, **size-free, NOT net of toll**
> loss 5,829 · median −1.0415 · mean −0.9690 | win 814 · median +2.1422 · mean **+9.4458** | ALL 6,643 · median −1.0324 · mean **+0.3072**

**Not comparable, for the same four reasons v1 gave**: different corridor, different rule card, different ruler (size-free gross, not net of toll), different denominator (tranches, not campaigns). Printed for lineage, as commissioned.

---

## 4 · THREE TRADES, HAND-VERIFIED END TO END (F-C3-PIVOT)

Chosen adversarially: **the flagged F-3 row**, **the largest rail widening**, and **the largest R/ATR** (the anchor found farthest away). Every leg re-derived from raw 4h bars — including that the anchor **is** a strict `(5,5)` swing pivot by the estate's own definition, that it was **confirmed by the entry bar**, and that it is the **nearest eligible one** beyond entry. Full transcript reproduces with `~/venvs/naiad/bin/python scripts/tierc3_fixtures.py`.

| | **ETHUSDT short** (F-3 row) | **ZECUSDT long** (widest rail) | **NEARUSDT short** (widest R) |
|---|---|---|---|
| arming (12/89) | 2025-10-29T16:00Z | 2025-12-24T16:00Z | 2025-11-16T12:00Z |
| tide | e89 4016.83 **<** e316 4115.92, close 3903.54 ✓ | e89 423.13 **>** e316 416.47, close 443.54 ✓ | e89 2.448629 **<** e316 2.459515, close 2.341 ✓ |
| d at cross | 1.444952 ≥ 0.75 ✓ | 1.490507 ≥ 0.75 ✓ | 1.013086 ≥ 0.75 ✓ |
| trigger (12/26) | same bar ✓ | 2025-12-24T20:00Z ✓ | 2025-12-05T08:00Z ✓ |
| entry = that bar's close | 3903.540000 | 448.450000 | 1.736000 |
| **4h anchor, strict (5,5)** | high **3926.00** @ 2025-10-18T04:00Z | low **446.43** @ 2025-11-28T00:00Z | high **1.867** @ 2025-11-30T16:00Z |
| raw bars around it | prev5 max 3882.00 · next5 max 3907.92 | prev5 min 482.50 · next5 min 450.62 | prev5 max 1.866 · next5 max 1.866 |
| confirmed / lookback | conf ≤ entry ✓ · 64 ≤ 200 bars ✓ | conf ≤ entry ✓ · 156 ≤ 200 ✓ | conf ≤ entry ✓ · 23 ≤ 200 ✓ |
| pivot stop (±0.5 ATR) | 3965.201844 | 439.748581 | 1.891343 |
| rail stop (±1.0 ATR) | **3981.943688** | **435.087161** | 1.784686 |
| **stop taken** | **RAIL** 3981.943688 | **RAIL** 435.087161 | **PIVOT** 1.891343 |
| R · R/ATR | 78.403688 · **1.000000** | 13.362839 · **1.000000** | 0.155343 · **3.190712** |
| exit | bell 12/89 2025-12-03T16:00Z, close 3126.78 | bell 12/89 2026-01-07T20:00Z, close 469.38 | bell 12/89 2025-12-28T08:00Z, close 1.594 |
| **F-4 adverse-first** | 210-bar ride, worst excursion **3962.55** vs stop 3981.94 — never touched ✓ | 84-bar ride, worst 435.18 vs 435.087 — **never touched, by 0.09** ✓ | 138-bar ride, worst 1.885 vs 1.891343 ✓ |
| **net R** | +9.907187 − 0.044834 − (−0.190248) = **+10.052601** | +1.566284 − 0.034343 − (−0.293782) = **+1.825723** | +0.914106 − 0.010718 − (−0.019629) = **+0.923016** |

**Read the ZEC line.** Its 84-bar ride came within **0.093 price units** of the rail stop and did not touch it. On the v1 card that stop sat at 434.4986 and also held — but the point stands generally: **a rail that converts stop-outs into bell exits works by surviving excursions it barely survives.** That is a property of one regime's noise, not a law.

**All three reconcile to the journal at 1e-6. 8/8 fixtures PASS.**

---

## 5 · THE ANALYTICS TAPE (Amendment B1) — captured, never consulted

**640 rows**, one per `(asset, ts)` over the scored corridor: **43 arming · 10 trigger · 6 exit · 581 daily-00:00Z spine** (an instant that is two things collapses to the higher-priority label — F-KEY depends on it). The four RECORDED-ONLY columns are joined onto `trade_journal.parquet` by ts.

*"6 exit" is not 6 of 12 exits missing.* **All twelve exit instants are in the tape**; six are labelled `arming`, because a `bell_12_89` exit **is** a counter 12/89 cross, which is the opposite direction's arming on the very same bar. Five bells collapse that way plus one stop that landed on an arming bar. Nine spine bars collapse likewise (590 daily bars → 581 labelled `spine`).

**F-C3-6 — no consultation — remains a property, not a promise**, and is now proved over **both** modules in the decision path: AST import scan of `tierc3_rules.py` (`['__future__','dataclasses','engine.s1','numpy','tierc2_rules']` — zero analytics) **and** of the `tierc2_rules.py` it inherits from; a **240-module transitive closure** whose project members are exactly `{engine.indicators, tierc2_rules, tierc3_rules}`; `engine/`↛`analytics/` (invariant I-B), so the closure cannot reach a registry symbol by any path; and zero tape column names in either source.

**Two tape facts, stated as raw material and conditioned on nowhere:**

- **The single-wall stamp is still mostly non-identifying.** At armings: `multi` **35 of 43**. At spine instants: `multi` **425 of 581 (73.1%)**, `FAST` 108, `none` 22. Nulls appear only in `wall_dist_atr`, exactly where `wall_family = "none"` (arming 4 = 9.30%, spine 22 = 3.79%). This is v1's F-6 unchanged, and F-6 was ruled **for the next TC, not this one**.
- **Two scored trades have NULL arming-instant tape columns, by construction.** Their armings fall in the lead-in, and **the tape does not cross into the sealed span**. The nulls are disclosed here and never back-filled. Their *trigger*-instant columns are present, because their entries are in-corridor.

**Q6c is why this tape exists and why it is inert.** *Stillbirth counterfactual first — rescore all historical fills by range-position before any location gate becomes law.* This baseline is that unconditioned population of fills. Conditioning here would destroy it.

---

## 6 · DISPLAY-ONLY STRIPS — F-7 enacted

> **DISPLAY-ONLY — hypothesis generation only, never evidence**

| window | span | trades | net R | expectancy | win % | maxDD R |
|---|---|---:|---:|---:|---:|---:|
| census-scored era | exploration-classic → 2024-06-30 | 127 | +145.4539 | +1.1453 | 18.90% | 39.5073 |
| pinning window | 2026-02-01 → **2026-07-07** | 15 | +12.2566 | +0.8171 | 13.33% | 10.3163 |
| **SEALED LOCKBOX** | 2024-07-01 → 2025-10-05 | **—** | **NOT COMPUTED** | | | |

**F-7 is enacted and proved, not just declared.** The pinning window now ends at VR-1's forward edge; **F-C3-5 asserts the last exit in each strip is at or before 2026-07-07T23:59:59Z** (CENSUS_ERA last exit 2024-06-07T16:00Z; PINNING last exit **2026-06-22T12:00Z**). v1's strip ran to 2026-08-11 and its last 35 days sat past that edge — this is the ruling that closed it.

**The lead-in is applied to every window, not only the scored one** — each strip admits armings from its own start − 30d, and a trade whose entry falls in a strip's lead-in is excluded from that strip by the same rule. One code path, so the strips are computed under the identical card; stated because a strip computed under a *different* arming rule than the headline would not be a continuity strip at all.

Both strips remain positive where they were positive before, but **the census-era strip moved from +34.89 R to +145.45 R under the same card change.** Neither is scored, neither may be cited, and the size of that move is itself only a reminder that the stop change is not marginal.

---

## 7 · FIXTURE TRANSCRIPT

**8/8 PASS** — `{"F-C3-1": true, "F-C3-INHERIT": true, "F-C3-RAIL": true, "F-C3-PIVOT": true, "F-C3-4": true, "F-C3-5": true, "F-C3-6": true, "F-KEY": true}`. The multi-hundred-line transcript prints locally and is not duplicated into the box (§9).

| fixture | verdict | evidence |
|---|---|---|
| **F-C3-1** gates | PASS | HEAD `20f23a1` · remote `catpatrol/Naiad` · pwd `/Users/luis/Naiad` == `$HOME/Naiad` · no cloud-sync token · branch `v12-v1-census` · venv present. **ESTATE READY over THREE spans** — the corridor (1h 2,832 / 4h 708 per asset), the **F-5 lead-in** (1h 720 / 4h 180), and the **F-7-truncated strip** (1h 3,768 / 4h 942) — all 5 assets × {1h, 4h}, **gaps = 0**, monotonic. |
| **F-C3-INHERIT** *(added)* | PASS | **12 identities asserted with `is`** — the unchanged half of the card is Tier-C2's own objects, not a copy. 15 unchanged register values re-read and matched; toll **derived** 2 × 5.0 = 10.0 bps; corridor proved byte-identical to v1; F-7 truncation proved as a diff. Rule card v3 echoed verbatim. |
| **F-C3-RAIL** | PASS | **Every one of 12 trades asserted individually**: `R/ATR ≥ 1.0`; `stop` = the farther of {pivot, rail} to 1e-6; `R = max(pivot_dist, rail_dist)`; `rail_binding` agrees with the arithmetic. R/ATR range **1.000000 → 3.190693**. 0 rows under the v3 rail, 0 under G-8c. v1's own table read for contrast: 2 of 10 under the v3 floor. |
| **F-C3-PIVOT** | PASS | Three trades hand-verified from raw 4h bars (§4) — strict `(5,5)` pivot definition re-tested on the raw series, causal confirmation `conf ≤ entry`, lookback, nearest-eligible, rail arithmetic, exit, **F-4 adverse-first over the whole ride**, net R to 1e-6. Plus the **cross-version reconciliation** of the F-3 row to 3.97e-05 price units. |
| **F-C3-4** determinism | PASS | Full re-run into `research_outputs/tierc3_run2/`; **all 13 table content-hashes identical** (`funnel 0b98e943…`, `headline 81cb04d3…`, `journal 4440bb1f…`, `delta 1be1c225…`, `tape 685d7319…`, …) **and the counts block identical**. NORMALIZATION DISCLOSURE: normalized fields are `['elapsed_s']` and the output root path; *no computed value is normalized*. Seed 20260815 printed and **unused** — determinism is structural. |
| **F-C3-5** era exclusions | PASS | Per table, min/max ts: `trade_journal.entry_ms` 2025-10-08T20:00Z → 2026-01-01T04:00Z · `.exit_ms` 2025-10-09T00:00Z → 2026-01-07T20:00Z · `analytics_tape.ts` 2025-10-06 → 2026-01-31 · `stop_geometry`, `anchor_lookback` same — all in-scored, lockbox-free, after the census ceiling. **F-5 disclosed**: 2 of 12 scored trades armed before the corridor, both with entries inside it; their arming stamps inside the sealed span are **named**. **`lead_in_trades` is the ONE table with a pre-corridor stamp and a banned-name scan proves it carries no outcome column.** **F-7 asserted** on both strips' last exits. |
| **F-C3-6** no consultation | PASS | AST scan of **both** decision-path modules · 240-module transitive closure · `engine/`↛`analytics/` · zero tape column names (§5). |
| **F-KEY** | PASS | Asserted before every join in-program **and re-asserted against the 12 written tables** — 0 duplicates anywhere. Plus **five funnel reconciliation identities**, `entered 13 == 12 scored + 1 lead-in`, and `headline.net_r == sum(journal.net_r)`. |

**Suite:** `pytest fixtures tests -q -m "not slow"` → **314 passed, 1 skipped, 1 deselected, exit 0** — measured **with and without** the three new scripts and identical both ways. No existing test was touched.

---

## 8 · FINDINGS — NOT FIXED

Named, measured, left alone.

**F-C3-a · The F-5 lead-in reaches 30 days into the sealed lockbox, because the corridor begins the day after the seal ends.** §0. The seal holds for outcomes — every scored entry, exit, price and R is post-lockbox, and the one trade that entered inside the lead-in carries no outcome column at all. But **two scored journal rows now carry an arming timestamp inside the sealed span** and a displacement computed there, which is a property v1's F-C2-5 explicitly asserted was absent. **Ruling needed: ratify "arming is state, not outcome" as standing law for lead-ins, or move future corridors' start so the lead-in clears the seal.** The 462 sealed days remain unspent and unread for outcomes.

**F-C3-b · The lookback reading is load-bearing, and the card does not name it.** F-3 moved the anchor to the 4h lens; the inherited constant is *200 bars in the pivot's own lens*, which was 200 hours on 1h and is **800 hours** on 4h. The time-equivalent reading (50 bars) is a different card: **only 5 of 12 trades get the same anchor under it, and 7 do not.** Taken as 200 bars, byte-inheriting the constant; the alternative is counted in `anchor_lookback_disclosure.parquet` with **no R attached to either reading**, because a swept parameter with an outcome beside it is a selection surface. **Ruling needed: pin the lookback in the card, in bars or in hours.**

**F-C3-c · The sign flip rests on four survivals, one of them 67% of the move.** §0, §3. Four of ten shared armings changed `stop → bell_12_89`; the other six moved only by the toll shrinking. ETHUSDT 2025-10-29 alone is +11.1480 of +16.5652. **This is the same concentration v1 reported from the other side** — v1's bell-only gap was 89.5% that one trade. **Ruling needed: is a twelve-trade, one-regime, one-dominant-trade result an acceptable bar for a multiplier to beat, or does the yardstick wait for a longer post-lockbox corridor?** The label **PROVISIONAL** is carried on every headline row until it is answered.

**F-C3-d · The estate now holds two rails for one concept.** G-8c rails at `min_stop_atr = 0.5` (`configs/tc1_B.yaml:53`, `engine/trading.py:555-560`); the v3 card rails at **1.0**. Both are live, they are not equal, and nothing states their relationship. **Ruling needed: reconcile them, or name them as deliberately distinct objects** — the way `TC-2` and `Tier-C2` had to be.

**F-C3-e · The 4h lens does not uniformly widen the stop, and one trade proves it.** §3. ZECUSDT's 4h anchor sat *nearer* than its 1H anchor (0.651 ATR vs 1.044), so on that trade the lens **narrowed** R and only the rail restored it. **Reported, not fixed** — it means "the 4h anchor is more conservative" is false as a general statement, and any future card text should say *railed*, not *wider*.

**F-C3-f · The bell-only comparison across versions is not a like-for-like.** §3. v1 bell-only +14.8733 and v3 bell-only −2.1634 are computed over **different trade populations** (10 vs 12, different occupancy). Printed unscored, as commissioned. **Do not subtract them.**

**F-C3-g · F-6 is untouched and still standing.** The single-wall stamp is `multi` on 73.1% of spine instants and 35 of 43 armings. Ruled for the **next** TC; nothing here conditions on it. Carried.

**F-C3-h · Nothing here is a registration, and these tables must not be mined as if they were.** m = 0 holds because the replay is a complete, unranked pass over one ratified card. The moment a cut is picked out of §2 or §3 on its R, the selection surface is the number of cells that were available to pick from, and that *m* must be declared **before** the look.

---

## 9 · DISPOSITION + BOX-COST

| item | disposition |
|---|---|
| `scripts/tierc3_rules.py` | **new** — the decision path; analytics-free by import closure, Tier-C2's objects bound rather than copied |
| `scripts/tierc3_baseline.py` | **new** — the program: replay · tape · tables · delta |
| `scripts/tierc3_fixtures.py` | **new** — the transcript, 8/8 PASS, HALTs non-zero |
| `research_outputs/tierc3/` | **built** — 13 parquet tables + manifest, local, gitignored |
| `research_outputs/tierc3_run2/` | **built, hashed, DATA DISCARDED** per rule R3; its `build_manifest.json` retained per refinement D-3 |
| `.gitignore` | **modified** — `research_outputs/tierc3{,_run2}/**` added, matching the per-phase convention |
| `exchange/reports/RULES_OF_RECORD_VIZ_IRON_2026-08-15.md` | **new** — the F-1 promotion; **V-10 closes by ruling** |
| THE HEADLINE | **+0.5596 R / trade over 12 trades**, stated plainly, positive, **PROVISIONAL** |
| THE FUNNEL | **built and printed whole**, 54 → 13, leaks counted, left edge measured |
| THE DELTA | **built**, per arming, v1 read from its filed table and never recomputed |
| THE TAPE | **captured, never consulted**, 640 rows, proved over both decision modules |
| sealed lockbox | **NO OUTCOME COMPUTED** — seal intact; the lead-in's 30-day reach is disclosed as F-C3-a |
| `engine/` · `analytics/` · `scripts/tierc2_*` · `com.naiad.daily` | **UNTOUCHED** — zero diff |
| registrations | **none**, as classed |

### BOX-COST

`exchange/**` measured **2,725,668 B = 17.04%** of the 16,000,000 B box **before this paste**; the governing **tick set** (`exchange/**` + `LEDGER.md`, per the D3 closure) **2,984,966 B = 18.66%** — state **OK** (warn 40% / refuse 70%), headroom to REFUSE **8,215,034 B**.

**This paste adds ≈ 33,900 B = 0.212% of the box** — this document (≈ 24,300 B), the `LEDGER_APOLLO` append (≈ 8,500 B) and the one-line rules-of-record file (1,073 B) — taking `exchange/**` to **≈ 2,759,600 B = 17.25%** and the tick set to **≈ 3,018,900 B = 18.87%**, level **OK**. **Against the < 0.5% target (80,000 B) that is 42% of budget, with ≈ 46 KB unspent.**

That is deliberate. The full fixture transcript (259 lines), the 640-row tape, the 30-series endpoint reconciliation and the per-trade journal beyond the three verified in §4 stay **local** — §7 carries the verdicts, the evidence values and the one command that reproduces them. **What is printed whole is what a reader cannot re-derive from a pointer: the card diffs, the funnel, the headline, the delta, and the findings.**

**Constants: pin-vs-import per site, per CONVENTIONS §6.4.** `tierc3_rules.py` **defines** the four new card values and **inherits** every other by import from `tierc2_rules.REGISTER`, which itself re-reads the estate's from source at fixture time. `BOX_BYTES`/`WARN_FRACTION`/`REFUSE_FRACTION` were **read live from `publish_exchange`**, not typed. The CENSUS RIDE-ONLY row is **pinned and labelled historical**.

---

## 10 · THE LEDGER_APOLLO APPEND

Per the 2026-08-12 `append` ruling — *a report without its ledger entry is an incomplete deliverable* — this document ends by appending the session's STATUS entry to `exchange/status/LEDGER_APOLLO.md`, **in this session**. Quoted here by its spine only; the complete block lives in the ledger.

```
=== STATUS_APOLLO — 2026-08-15 (2) ===
NOW: TIER-C3 IS MEASURED. The railed baseline is +0.5596 R per trade over 12
     trades, 2025-10-06 -> 2026-01-31, against TIER-C2's -0.7762 R over 10.
     THE NUMBER CHANGED SIGN. It is PROVISIONAL and it is labelled so on every
     headline row: one regime, n = 12, and 67% of the improvement is ONE trade.
     THE SEAL HELD FOR OUTCOMES: no scored entry, exit, price or R comes from a
     lockbox bar. The F-5 lead-in DOES reach 30 days into the sealed span,
     because the corridor starts the day after the seal ends — disclosed, not
     hidden, and it is finding F-C3-a.
CLASS: measurement, not registration. m = 0. No lockbox outcome. No estate
       write. No live orders. engine/, analytics/ and scripts/tierc2_* untouched.
Q6 DECISION RULE, RE-INVOKED AGAINST v3: Q6c still governs — 'stillbirth
     counterfactual first; rescore all historical fills by range-position BEFORE
     any location gate becomes law.' v3 is a SECOND unconditioned population of
     fills over the same corridor, and its tape is the location record it must
     be rescored against. Nothing in the v3 card read a registry symbol; the
     counterfactual is still answerable, and it is now answerable TWICE — once
     per card version, over one corridor. No location gate is proposed.
PENDING: [F-C3-a..h, 8 findings; F-C3-a/b/c/d need operator rulings]
PROBE LEDGER: m = 0. EXPLORATION — ungated; promotion requires registration.
=== END STATUS ===
```

---

*End of build document. TIER-C3 · measurement, not registration · m = 0 · seal intact for outcomes, 462 sealed days unspent · no registrations · the card diffs are the seven F's and nothing else. The yardstick is positive, thin, and PROVISIONAL.*
