# BUILD — TIER-C4 · THE MEAN CARD

**Date** 2026-08-16 · **Branch** `v12-v1-census` · **HEAD at start** `c4d7ddf` · **Seed** 20260816 · **Drafted** APOLLO · **Executor** HEPHAESTUS

**RATIFIED** operator 2026-08-16 — *"run tc4 with just the anchor 4H trade; ratchet and harvest per your lean; a mean for the average trade we can tune later."*

**CLASS — measurement, not registration. m = 0. ONE pre-named card.** No grid, no sweep, nothing promoted. The estate's selection guard is **loaded and CALLED** with the empty candidate list this build actually has; its verdict (`m = 0`, *"no usable candidate"*) is in the manifest and F-C4-1 asserts it. **A guard that is only mentioned is a guard nobody ran.** No registration. No lockbox read for outcomes. No estate write. No live orders. F-KEY on every join.

**Programs (local):** `scripts/tierc4_rules.py` (decision path) · `scripts/tierc4_baseline.py` (program) · `scripts/tierc4_fixtures.py` (transcript) · `scripts/tierc4_independent.py` (a second, independent reading of the card — §9). **Tables local** at `research_outputs/tierc4/` — 17 parquet + `build_manifest.json`.

> **THIS DOCUMENT SUPERSEDES THE VERSIONS AT COMMITS `5d4acdc` AND `49cc242`.** `exchange/**` auto-publishes, so this document was on the remote the instant it was first written — F-C3-i, carried and now demonstrated a second time. **The three states differ ONLY in §11's BOX-COST block** (estimated figures → `publish_exchange`'s own published figures → this banner). **No finding, table, fixture verdict or headline figure differs between them.** Named because the estate's rule is that an intermediate published state is part of the record, not because anything was corrected.

**I9** — `ANALYTICS_VERSION` **1.5.0**, `analytics_sha()` `ea5f02f21ca43b6b71e450b540ff09c807b305971e3eb8cff50bea84c985dc91`. Instrument: **BINANCE USDT-M perpetuals**, `{BTC,ETH,SOL,NEAR,ZEC}USDT.P`, offline cache `~/.cache/naiad/data_cache/klines`.

---

## 0 · THE ONE THING THE OPERATOR MUST READ FIRST

**The card did exactly what it was asked to do. The mean did not move — the SHAPE did. And the shape moved by spending the tail.**

| | TIER-C3 (v3) | **TIER-C4 (v4)** | |
|---|---:|---:|---|
| net R | +7.7614 | **+7.5978** | −0.1636 |
| expectancy / trade | +0.7056 | **+0.6907** | −0.0149 |
| n | 11 | **11** | — |
| win rate | 45.45% | **27.27%** | −18.18 pp |
| **maxDD (R)** | 4.2697 | **2.0348** | **halved** |
| **tail concentration** | 71.83% | **50.76%** | −21.07 pp |
| best trade | +10.0526 | +6.1794 | −3.87 |
| **net R WITHOUT the best trade** | **−2.2912** | **+1.4184** | **the sign flips** |

**That last row is the deliverable.** The operator asked for *"a mean for the average trade"*. Under v3 the yardstick was **negative once you removed one trade of eleven** — the estate has been carrying that sentence since 2026-08-15 as finding F-C3-d. **Under v4 it is positive.** The ten remaining trades pay for themselves.

**The price is printed beside it, and it is large.** On the DISPLAY-ONLY continuity strip — 127 trades over five years, hypothesis generation only, never evidence — the same two amendments take **+145.4539 R to −7.0097 R**, and the strip's best trade from **+165.79 R to +5.85 R**. The trail caps every tail it meets. **On eleven trades that is nearly free; on a hundred and twenty-seven it is the whole result.** F-C4-a.

**And the name holds, which is not something this estate assumes any more.** Tier-C3 was named for the rail and the rail was worth +0.15 R (F-C3-b). So the same test was run here before the title was allowed to stand: *is this a mean card?* maxDD halved, tail share down 21 points, and the ex-best-trade result changes sign. **It is a mean card. It is not a better card, and §3 says so in the arithmetic.**

---

## 1 · THE TWO AMENDMENTS, VERBATIM

Everything not listed here **byte-inherits — and the inheritance is by import, two generations deep.** `build_4h`, `_crosses`, `armings`, `Frame4h`, `Arming`, `build_pivots_4h`, `struct_stop_4h`, `Pivots4h`, `Stop`, `sealed_mask`, `funnel_table`, `lead_in_census`, `lead_in_table`, `anchor_lookback_disclosure`, `WINDOWS` and the whole Tier-C2 program layer are **bound to Tier-C3's and Tier-C2's own objects**. **F-C4-INHERIT asserts nineteen identities with `is`**, plus thirty-five further inherited names proved either to BE the parent's object or to be called through the parent and **not redefined here** — driven from the program's own `INHERITED_FROM_*` tuples, which until the repairs of §9 were decoration nothing read.

```
RATCHET ["ratchet"] [TC-4]: THE LPS-TRAIL. When a new FAVOURABLE 4h swing pivot
  CONFIRMS — fractal (2,2) ["pivot"], the pivot bar's low/high STRICTLY beyond
  the 2 bars each side, close-confirmed at pivot bar + 2 — the stop ADVANCES to
  beyond that pivot (0.5 x ATR_4h, the card's own 'beyond'), RAILED so it is
  never nearer than 1.0 x ATR_4h from the CONFIRMING BAR's close. Stops only
  advance, never retreat. The advanced stop governs the NEXT bar onward. The
  bell still exits everything. R is NOT re-denominated: R stays the ENTRY stop
  distance for the life of the campaign.
HARVEST ["harvest"] [TC-4]: THE CREEK/ICE TOUCH. At the FIRST touch of the
  opposing 89/316 band after entry — shorts: the bar's HIGH reaches the band's
  near edge FROM BELOW; longs: the mirror — exit 50% of the unit AT THAT BAR'S
  CLOSE. Remainder rides to ratchet or bell. ONE harvest per campaign, ever.
  "FROM BELOW" IS A PRECONDITION, NOT DECORATION: the touch counts only once
  the campaign has CLOSED on its own side of the near edge (at the entry bar,
  or any bar since). A campaign that entered INSIDE the band is not armed until
  it leaves — a position that was never outside cannot cross in. Count of
  entries inside the band is disclosed, and is 0 on this corridor.
  WITHIN A BAR: stop, then bell, then harvest. A stop takes the whole remainder
  adverse-first [F-4]; a bell exits the whole remainder at the close, which
  makes a same-bar harvest economically identical and it is not recorded.
ACCOUNTING ["accounting"]: net of 10 bps round-trip + journaled funding; R units;
  R = ENTRY stop distance; the halves BOOK THEIR OWN R contributions — entry fee
  splits 50/50, each half pays its own exit fee, funding accrues on the size
  actually held into each bar; one unit, one position per asset
SEAL FLOOR [CLASS, not a card diff]: no pivot lying on a SEALED bar may be an
  anchor — AND NONE MAY BE A RATCHET PIVOT EITHER.
```

**Both amendments are RIDE-ONLY. And because the ENTRY half of the ride loop is a HAND TRANSCRIPTION of Tier-C3's rather than a binding — the amendments live inside the loop, so the loop had to be rewritten around them — that claim is made where it can be FALSIFIED rather than where it is comfortable.** `is` cannot reach transcribed code. Five of Tier-C3's filed tables therefore come out of this build **content-hash-identical**, and F-C4-INHERIT asserts all five: `funnel` `391fae98…`, `lead_in_census` `f00105fb…`, `lead_in_trades` `01ba4719…`, `strip_d_unscored` `89943555…`, `anchor_lookback_disclosure` `62c34cea…`. **The same 54 armings, the same 43 in-window, the same 11 lead-in, the same 2 seal-refusals, the same 11 entries, the same entry stops.** A single drifted arming, gate, trigger, occupancy decision, anchor or entry stop would move one of those hashes. The delta table additionally HALTs if any shared arming's R denominator moves by more than 1e-9.

### The register — FOUR new numbers, TWO new named rules, THREE re-pointed rows

**The partition is DERIVED FROM THE REGISTER, not typed beside it** (F-C4-INHERIT: *"4 new numbers + 2 new named rules + 3 re-pointed = 9 of 9 rows"*), and **every one of the nine is asserted to be READ by the decision path or the program.** Both of those checks exist because the first draft of this document claimed *"exactly three genuinely new numbers"* from a hand-written 3-tuple, which (a) mis-counted — `HARVEST_MAX_PER_CAMPAIGN = 1` is a number — and (b) would have printed "three" whatever the register held. See §9.

| constant | value | source |
|---|---:|---|
| `RATCHET_PIVOT_L` | **2** | **NEW NUMBER.** TC-4 card `["pivot"]`. Computed by `engine.s1._pivots` — the estate's pivot of record and the *same function* the (5,5) entry anchor uses. The card moved the SHAPE, not the definition |
| `RATCHET_PIVOT_R` | **2** | **NEW NUMBER.** Same row. The confirmation lag *is* R: a fractal at bar p is knowable at the CLOSE of p+2 and the advanced stop governs p+3 onward |
| `HARVEST_FRACTION` | **0.5** | **NEW NUMBER.** TC-4 card `["harvest"]`, *"exit 50% of the unit"* |
| `HARVEST_MAX_PER_CAMPAIGN` | **1** | **NEW NUMBER.** TC-4 card: *"One harvest per campaign, ever."* **The ride counts against this row**, not against a literal `harv is None` |
| `RATCHET_MONOTONE` | **True** | **NEW NAMED RULE.** *"Stops only advance, never retreat."* **`ratchet_step` reads it**; it is not a sentence the code merely happens to obey |
| `HARVEST_FILL` | **`bar_close`** | **NEW NAMED RULE.** The TOUCH is intrabar, the FILL is *"at that bar's close"* — two different instants, and the card names both. **`harvest_fill_px` dispatches on this row and HALTs on any value it cannot enact** |
| `RATCHET_BUF_ATR` | 0.5 | **RE-POINTED INHERITANCE of `STOP_BUF_ATR`.** The card says *"beyond that pivot"*; *beyond* is the v3 card's own word for its entry anchor (*"offset 0.5 x ATR_4h beyond it"*). The register row's value **is the v3 constant object**, not a literal |
| `RATCHET_RAIL_ATR` | 1.0 | **RE-POINTED INHERITANCE of `MIN_STOP_ATR`.** Same rail, same value, new measuring point: v3 rails the ENTRY stop against the ENTRY close; the ratchet rails an ADVANCED stop against the CONFIRMING BAR's close |
| `HARVEST_BAND` | (89, 316) | **RE-POINTED INHERITANCE of `(TIDE_FAST, TIDE_SLOW)`.** The harvest band **is** the tide band. **No new EMA is computed anywhere in this build** |

**`tierc4_rules` refuses to import** if any re-pointed row stops equalling the constant it claims to inherit. That assertion exists because F-C3-e recorded what happens otherwise: the estate ended up holding two rails for one concept and relating them nowhere. **A register row that governs nothing is the same defect from the other side, and F-C4-INHERIT now closes it too.**

**UNCHANGED, re-read from Tier-C3's register:** universe · lens 4h · tide 89/316 · window 12/89 with d = 0.75 (strip {0.50, 1.00} reprinted unscored) · trigger 12/26 at close · entry anchor 4h (5,5) lookback 200 bars · entry rail 1.0 ATR · F-5 lead-in 30d · F-7 strip truncation · bell · one unit, one position per asset · net of 10 bps round trip (**derived** as 2 × `fee_bps_side`, never typed) + journaled funding · Amendment B1 tape captured-not-consulted. **`PIVOT_LOOKBACK_1H` is still RETIRED**, and the 1H lens is **not reachable from the v4 program at all** — v1's number is READ from its filed headline, never recomputed.

---

## 2 · THE HEADLINE TRIPTYCH — v4 beside v3 beside v1

> **YARDSTICK v4 — PROVISIONAL (one regime, n small)**
> **SCORED 2025-10-06 → 2026-01-31 · 5 assets · both directions · 11 trades**

`headline_triptych.parquet`. **v1's and v3's rows are READ from their own filed `headline.parquet` and are never recomputed here** — a build that can move its predecessor's number while comparing itself to it is not comparing anything.

| | **v1** TIER-C2 | **v3** TIER-C3 | **v4** TIER-C4 |
|---|---:|---:|---:|
| card | 1H anchor, no rail, no lead-in | 4h anchor + 1.0 ATR rail + 30d lead-in | v3 + LPS-trail + creek/ice harvest |
| n | 10 | 11 | **11** |
| **net R** | −7.7620 | +7.7614 | **+7.5978** |
| **expectancy / trade** | −0.7762 | +0.7056 | **+0.6907** |
| win rate | 10.00% | 45.45% | **27.27%** |
| **maxDD (R)** | 9.5107 | 4.2697 | **2.0348** |
| tail concentration | 100.00% | 71.83% | **50.76%** |
| best trade | +1.7487 | +10.0526 | **+6.1794** |
| **net R minus best trade** | −9.5107 | −2.2912 | **+1.4184** |
| bell-only counterfactual | +14.8733 | −0.0919 | **−0.0919** |

**The bell-only column is the cross-check that the ride is the only thing that changed.** It is the same object in v3 and v4 by construction — ride to the bell, honour no stop, manage nothing — and it comes out **byte-identical at −0.0919 R**. Anything that had moved an entry, a stop denominator or a bell would have moved that number.

**The distribution, which is what actually changed:**

| | v3 | v4 |
|---|---:|---:|
| winners · mean winner | 5 · **+2.7992** | 3 · **+4.0583** |
| losers · mean loser | 6 · **−1.0391** | 8 · **−0.5721** |
| win/loss size ratio | 2.69 | **7.09** |
| median bars held · max | 23 · 210 | **11 · 54** |
| exits: stop / bell | 6 / 5 | **11 / 0** |

**Fewer, bigger winners; more, much smaller losers; half the holding time; and the bell never fires once.** Every loser in v3 was ≈ −1.0 R because every loser paid the full entry stop. Under v4 the trail takes most of them at a fraction of R — but it also converts two marginal winners (NEAR +0.9230, SOL +0.3420) into small losses. That is the whole trade the card makes.

**Monthly equity (R), exit-stamped:** 2025-10 · n 1 · −1.0418 · cum −1.0418 | 2025-11 · n 2 · +7.0182 · cum +5.9764 | 2025-12 · n 6 · +3.1219 · cum +9.0982 | 2026-01 · n 2 · −1.5004 · cum **+7.5978**. *(v3 had no November row; the trail resolves in November what v3 held into December.)*

**Three caveats, all structural and all carried:** **n = 11**, every per-asset row n ≤ 3, and **no confidence interval is printed, deliberately**. **Nine of eleven trades are shorts** — this still measures **one regime**. And the result now rests on **two** trades rather than one: ETH +6.1794 and ZEC +5.1566 sum to **+11.3360 against a net of +7.5978**. That is a better shape than v3's one-trade dependence and it is not independence.

---

## 3 · THE UNSCORED ABLATION — four cells, one code path

**F-C4-ABLATE.** `ablation_unscored.parquet`. Each cell is the SAME `replay_asset` with one keyword changed. **The V3 cell reproduces Tier-C3's filed net R to 2.00e-06 over the same 11 trades — and, since the repairs of §9, TRADE BY TRADE and with a HALT on any one-sided or null row** — so every marginal below is the AMENDMENT and not the fork.

| cell | ratchet | harvest | seal | n | net R | expectancy | win % | maxDD | tail % | best | **minus best** | adv | harv | stop/bell | marginal |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| **V3** | — | — | ✓ | 11 | **+7.7614** | +0.7056 | 45.45 | 4.2697 | 71.83 | 10.0526 | −2.2912 | 0 | 0 | 6/5 | *control* |
| **RATCHET** | ✓ | — | ✓ | 11 | +7.3262 | +0.6660 | 27.27 | 2.2111 | 50.76 | 6.1794 | +1.1469 | 21 | 0 | 11/0 | **−0.4352** vs V3 |
| **HARVEST** | — | ✓ | ✓ | 11 | +4.5800 | +0.4164 | 36.36 | 4.4059 | 66.88 | 6.8036 | −2.2236 | 0 | 9 | 6/5 | **−3.1814** vs V3 |
| **BOTH** | ✓ | ✓ | ✓ | 11 | **+7.5978** | +0.6907 | 27.27 | **2.0348** | **50.76** | 6.1794 | **+1.4184** | 21 | 3 | 11/0 | **−0.1636** vs V3 — **SHIPPED** |
| **BOTH_NOSEAL** | ✓ | ✓ | ✗ | **12** | +6.5515 | +0.5460 | 25.00 | 2.0881 | 50.76 | 6.1794 | +0.3721 | 21 | 3 | 12/0 | **−1.0463** vs BOTH |

**The last row is the SEAL FLOOR "PRINTED BOTH WAYS", and it is this card's own number.** The v4 card text inherits the promise that the operator can overturn the floor in one line (F-C3-a); Tier-C3 discharged it with its cell A0, and the first draft of this build **made the same promise and filed no such cell** — it would have had the reader borrow a predecessor's figure computed under a different ride. Executed literally, without the CLASS line's mask, the card takes the two refused ETHUSDT-long armings and scores **+6.5515 over 12**. *(The −1.0463 R cost is the same losing trade Tier-C3's A0 measured, which is why the two builds' seal-floor deltas agree to the fourth decimal. It removes a LOSER, so the floor is not flattering the number.)* Both figures are on the record; the ruling is still F-C3-a's and still the operator's.

**THEY ARE STRONGLY NON-ADDITIVE, AND THE TABLE PRINTS THE INTERACTION RATHER THAN LEAVING IT TO BE INFERRED: BOTH − RATCHET − HARVEST + V3 = +3.4530 R.** The two amendments share one ride. **The trail pre-empts the harvest**: 9 fills when the harvest rides alone, **3** when the trail is on, because a ratchet stop ends the campaign before the band is reached. Reading either marginal on its own is wrong, and the shipped card is closer to *ratchet plus a residue* than to *ratchet plus harvest*.

### The harvest's cost is NOT in the fills it took

This is the row that would be misread without its decomposition, so the decomposition is in the table:

| cell | harvest fills | **sum of the harvested halves' own net R** | mean UNIT move at the fill (R) | adverse fills | median bars after entry |
|---|---:|---:|---:|---:|---:|
| HARVEST | 9 | **+1.7282** | +0.3935 | 6 of 9 | 15 |
| BOTH | 3 | **−0.9898** | −0.6085 | 3 of 3 | 3 |

**The two R columns are NOT the same quantity and the headings now say so.** *"Unit move at the fill"* is the price move from entry to the fill expressed in R **on a full unit**; the half's own booked contribution is roughly half of it, less its share of the toll and funding. The first draft called that column `half_move_r` and printed it beside `fraction = 0.5` and two genuine half quantities, where a reader reconciling the row would have doubled it — found by the post-build adversarial review and renamed to `unit_move_at_harvest_r`.

**Under HARVEST-only the fills MADE money — and the amendment still cost −3.1814 R.** The cost is in the half that was **not allowed to run**, which is a different quantity from the half that was taken. On the ETH campaign alone: v3 rode one full unit to +10.0526 R; the harvest took half at +3.5341 R of move and let half ride to the same bell, for **+6.8036** — a 3.25 R loss to *position size*, not to *timing*.

**And the harvest is bimodal, by geometry.** A short lives below the 89/316 band, so a touch of the band's near edge is an **adverse** move on a campaign that dies quickly (3–4 bars, unit move −0.49 to −0.81 R → it **cuts the loss**) and a **favourable** one on a campaign that has run far enough for the band to come down to it (52–89 bars, unit move +0.92 to +3.53 R → it **banks the tail**). **Under the shipped card the trail kills every campaign of the second kind before its band touch, so all three surviving fills are of the first kind.** F-C4-e.

**THIS IS NOT A SWEEP AND NOTHING HERE IS SCORED.** A sweep searches a space and reports the best cell; this decomposes ONE ratified card into its OWN ratified parts, every cell printed, the card chosen before the table existed. This table **is** the *"tune later"* substrate the operator asked for, and the sentence that rides with it is: **tuning later means declaring m first.** Picking a cell out of this table on its R is a new probe with its own m.

---

## 4 · THE PER-TRADE DELTA — v3 → v4, with the give-back accounted

`delta_v3_v4.parquet`, joined on `(asset, direction, arm_ms)`, **outer**, `validate="1:1"`. v3's side is read from the **filed** `research_outputs/tierc3/trade_journal.parquet` and never recomputed. **11 rows `both`, 0 `v3_only`, 0 `v4_only` — the population did not move.**

**THE GIVE-BACK, defined once:** `mfe_r_v3` is the campaign's best unrealised R **under the v3 ride**, counting only bars the v3 position was held through. `giveback_v3_r = mfe_r_v3 − net_r_v3`. `captured_r = net_r_v4 − net_r_v3`. `surrendered_r = mfe_r_v3 − net_r_v4`.

**TWO OF THOSE THREE ARE EASY TO OVER-READ, AND THE BUILD SAYS SO RATHER THAN LETTING A READER DO IT.** `captured + surrendered ≡ giveback` is an **ALGEBRAIC IDENTITY** — `net_r_v4` cancels — so the F-KEY leg that checks it to 2.2e-16 is catching a wiring or rounding error and is **NOT evidence about the amendments**. The only one of the three that carries information about v4 is **`captured_r`**. And `surrendered_r` is **not** "what v4 left on the table": on the campaigns the ratchet closed early, the v4 position was already flat while the v3 ride ran on, so `mfe_r_v3` reaches past v4's exit. It is a comparison against a counterfactual peak. *(ETH is the clearest case: the v3 peak lands 2025-11-21, a fortnight after v4 exited on 11-07.)*

| asset · arming | v3 exit → v4 exit | v3 net R → v4 net R | adv | harv | **captured** | v3 give-back | surrendered |
|---|---|---|---:|---|---:|---:|---:|
| NEAR long 10-02 | 10-09 stop → **same** | −1.0418 → −1.0418 | 0 | — | 0.0000 | 1.0418 | 1.0418 |
| **ETH short 10-29** | 12-03 **bell** → **11-07 stop** | **+10.0526 → +6.1794** | **4** | — | **−3.8732** | 6.3183 | **10.1915** |
| SOL short 10-30 | 12-03 bell → 11-20 stop | +0.8526 → +0.8388 | 7 | — | −0.0139 | 2.0561 | 2.0699 |
| NEAR short 11-16 | 12-28 bell → 12-07 stop | **+0.9230 → −0.2196** | 1 | — | **−1.1426** | 1.2142 | 2.3568 |
| SOL short 12-05 | 12-09 stop → 12-07 stop | −1.0161 → −0.2031 | 2 | — | **+0.8129** | 1.7110 | 0.8981 |
| BTC short 12-06 | 12-09 stop → 12-07 stop | −1.0222 → −0.3495 | 2 | — | **+0.6727** | 1.6765 | 1.0039 |
| SOL short 12-11 | 01-02 bell → 12-15 stop | **+0.3420 → −0.4644** | 2 | ✓ | **−0.8063** | 1.0420 | 1.8484 |
| **ZEC long 12-24** | 01-07 **bell** → **12-31 stop** | **+1.8257 → +5.1566** | **2** | — | **+3.3309** | 6.1890 | 2.8581 |
| BTC short 12-29 | 12-30 stop → **same** | −1.0545 → −0.7982 | 0 | ✓ | **+0.2563** | 1.3552 | 1.0988 |
| NEAR short 12-29 | 01-01 stop → **same** | −1.0161 → −0.5118 | 1 | — | **+0.5043** | 1.8040 | 1.2997 |
| BTC short 12-31 | 01-01 stop → **same** | −1.0839 → −0.9886 | 0 | ✓ | **+0.0953** | 1.0986 | 1.0034 |
| **ALL** | | **+7.7614 → +7.5978** | **21** | **3** | **−0.1636** | **25.5068** | **25.6704** |

**Read the totals.** v3's own peaks exceeded v3's own results by **25.5068 R** across eleven campaigns. The two amendments captured **−0.1636** of it — **less than nothing, net.** What they actually did was **redistribute 5.67 R onto five campaigns and take 5.84 R off four**, and the two sides very nearly cancel. **The mean is not where the card acted. The variance is.**

**Five campaigns changed exit reason `bell → stop`** — every one of v3's bell exits. **Three campaigns were untouched by the trail** (0 advances — see §6 for why each), and on those the only mover is the harvest, worth +0.2563, +0.0953 and 0.0000.

---

## 5 · THE ETH-10-29 ROW, NARRATED

**The estate's dominant trade, third card version running.** ETHUSDT short, armed and triggered on the same bar 2025-10-29T16:00Z, entry **3903.54**, entry anchor the 4h swing high **3926.00** @ 2025-10-18T04:00Z, **rail-bound** stop **3981.943688**, R = **78.403688** = exactly **1.000 ATR**. All of that is v3's, unchanged, and F-C4-SEAL re-derives the anchor's own bar and finds it unsealed.

**What the trail did.** Four advances, each from a confirmed (2,2) fractal high, each railed 1.0 ATR from its own confirming close, each strictly monotone:

| # | confirmed | pivot bar | pivot high | close | ATR | beyond (0.5) | rail (1.0) | **stop taken** | bound by | advance |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| 1 | 11-01T00:00Z | 10-31T16:00Z | 3904.90 | 3860.00 | 77.2792 | 3943.540 | 3937.279 | **3943.539579** | pivot | 0.497 ATR |
| 2 | 11-02T00:00Z | 11-01T16:00Z | 3907.61 | 3879.25 | 60.7589 | 3937.989 | 3940.009 | **3940.008913** | **rail** | 0.058 ATR |
| 3 | 11-06T04:00Z | 11-05T20:00Z | 3479.00 | 3378.90 | 102.6269 | 3530.313 | 3481.527 | **3530.313464** | pivot | **3.992 ATR** |
| 4 | 11-07T12:00Z | 11-07T04:00Z | 3370.00 | 3295.99 | 98.8466 | 3419.423 | 3394.837 | **3419.423324** | pivot | 1.122 ATR |

**The stop travelled 7.175 ATR in nine days and then was hit on the very next bar.** Advance #4 was placed at the close of 2025-11-07T12:00Z and governed from 16:00Z; that bar's high reached it. **Exit: stop at 3419.423324, bar 54 of the ride, +6.179393 R.**

**What v3 did instead.** Held the same position through **bar 210** to the counter-12/89 bell on 2025-12-03T16:00Z at **3126.78** for **+10.0526 R**. So the trail **surrendered 292.64 price units = 3.73 R** of a move that was still coming.

**What the harvest would have done, and did not.** Under HARVEST-only the band touch on this campaign lands at **bar 68, 2025-11-10T00:00Z**, at a **unit move of +3.5341 R** — the *favourable* mode of §3 — booking the harvested half at **+1.7773 R** and letting the runner ride to the same bell for **+5.0263 R**, campaign **+6.8036 R**. **The trail ended the campaign at bar 54, fourteen bars early, so the harvest never fired on the one campaign it was built for.** That single fact is the +3.4530 R interaction term in miniature.

**And the give-back is the honest frame — including against v4's OWN peak.** v3's peak on this campaign was **+16.3709 R**, reached at 2025-11-21T12:00Z (price 2620.00) — **a fortnight after v4 had already exited.** v3 handed back 6.32 R of it. But v4 did not merely miss a peak it never saw: **inside its own 54-bar ride it was +10.8227 R at 2025-11-04T20:00Z (price 3055.00) and it exited at +6.18 R.** The trail gave back **4.64 R of its own excursion** before it fired, because the trail is a stop and a stop is behind price by construction. **Neither card captured this trade. One captured 61% of what the other did, and both left more on the table than they took.**

*(The cross-version reconciliation of this row is Tier-C3's and is not re-litigated: v1's bell-only counterfactual and v3's realised outcome are the identical price path against different denominators, asserted to 3.97e-05 by F-C3-PIVOT. v4's `net_r_bellonly` for this row is +10.052601 — Tier-C3's realised number, which is what "the bell-only object did not change" means.)*

---

## 6 · THE RATCHET AND THE HARVEST, MEASURED

### The ratchet — `ratchet_ledger.parquet`, one row per advance

**21 advances over 8 of 11 campaigns. 8 campaigns exited on an advanced stop; 3 on the entry stop; 0 on a bell.** Of the three campaigns with no advance, **two had no favourable fractal confirm at all** during their (1-bar and 4-bar) rides, and **the third had one confirm — BTCUSDT 2026-01-01T08:00Z — that did not improve on the standing stop, and `RATCHET_MONOTONE` refused it.** The rule is doing work, not just describing an absence.

| | |
|---|---:|
| advances · campaigns carrying one | **21** · 8 |
| advances per campaign | 1 (×2) · 2 (×4) · 4 (×1) · 7 (×1) |
| bound by the **rail** / by the **pivot buffer** | **7** / **14** |
| advance size (ATR) — min · median · max | **0.002053** · 0.9437 · 3.9921 |
| bars after entry — min · median · max | 5 · 19 · 53 |
| distance from the confirming close at placement | **min 1.000000 × ATR** — the floor, met by every advance |
| total stop travel per campaign (ATR, favourable) | 0.964 · 1.478 · 1.704 · 2.077 · 2.527 · 4.991 · 6.176 · **7.175** |

**F-C4-RAIL asserts seven legs on every one of the 21 advances individually** — the rail floor at placement, the buffer arithmetic, the rail arithmetic, that the stop taken is the farther of the two, strict monotonicity, that `rail_binding` is arithmetic and not a label, and that the stop is on the correct side of price. It also asserts monotonicity **across whole campaigns**, not only per advance.

**Two facts from this table are findings, not colour.** The pivot buffer — not the rail — set the stop on **14 of 21** advances, which makes the unruled 0.5-ATR reading load-bearing (**F-C4-b**). And the smallest advance was **0.002053 ATR**, on the SOL 10-30 campaign, and it was **the advance that was paid out** (**F-C4-d**).

### The harvest — `harvest_ledger.parquet`, one row per fill

**3 fills of 11 campaigns**, and the other eight are accounted rather than absent: **3** campaigns whose first band touch fell on their own **stop bar** (adverse-first [F-4] takes the whole remainder), **0** on a bell bar, and **5** that **never touched the band at all**. 3 + 3 + 5 = 11.

| asset | entry | fill | bars | band edge | fill px | unit move (R) | **harvest half** | **runner half** | **campaign** |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| BTC short | 12-29T20:00Z | 12-30T08:00Z | 3 | 88145.033 | 87875.20 | −0.4876 | −0.270922 | −0.527262 | **−0.798185** |
| BTC short | 01-01T04:00Z | 01-01T16:00Z | 3 | 88145.095 | 88354.80 | −0.8096 | −0.446676 | −0.541930 | **−0.988606** |
| SOL short | 12-11T04:00Z | 12-11T20:00Z | 4 | 136.167 | 136.36 | −0.5285 | −0.272204 | −0.192175 | **−0.464379** |

*(**"Unit move" is a FULL-unit quantity**; the two half columns beside it are the halves' own booked R. They differ by the fraction plus each half's share of the toll and funding.)*

**THE HALVES BOOK THEIR OWN R AND THE SUM IS AN IDENTITY, NOT A CONVENTION.** The entry fee splits 50/50, each half pays its own exit fee, funding accrues on the size actually held into each bar. `net_r_harvest_half + net_r_runner_half == net_r` is asserted **at full float precision inside the program, where it HALTs at 1e-9**, and re-asserted against the written record at 2e-6 — the arithmetic bound of three independently 6-dp-rounded columns, one of which sits at exactly 1.0e-6. **The fixture tests the written record at the precision it was written at; the arithmetic is tested where the arithmetic happens.** An unharvested campaign carries NULL half columns — **a half that did not happen is not booked as zero.**

F-C4-HARV additionally hand-reconciles one fill end to end from raw 4h bars and raw EMAs: the band edge, the intrabar touch, that it is the FIRST touch after entry (rescanned bar by bar), that the fill is that bar's close, and both halves' net R from raw prices + the register's toll + journaled funding.

---

## 7 · DISPLAY-ONLY STRIPS — and the number that should worry the operator

> **DISPLAY-ONLY — hypothesis generation only, never evidence**

| window | span | | v1 | v3 | **v4** |
|---|---|---|---:|---:|---:|
| census-scored era | 2019-09-08 → 2024-06-30 | n | 128 | 127 | 127 |
| | | **net R** | +34.8898 | **+145.4539** | **−7.0097** |
| | | expectancy | +0.2726 | +1.1453 | **−0.0552** |
| | | win % | 14.84 | 18.90 | **29.13** |
| | | maxDD R | 39.0462 | 39.5073 | **21.4799** |
| | | **best trade** | +65.5226 | **+165.7890** | **+5.8468** |
| | | tail share | 94.76% | 94.45% | **68.34%** |
| pinning window | 2026-02-01 → **2026-07-07** | n | 16 | 15 | 15 |
| | | **net R** | +37.4521 | +12.2566 | **+27.2038** |
| | | expectancy | +2.3408 | +0.8171 | **+1.8136** |
| | | maxDD R | 9.7721 | 10.3163 | **6.2327** |
| **SEALED LOCKBOX** | 2024-07-01 → 2025-10-05 | | **—** | **NOT COMPUTED** | **NOT COMPUTED** |

**F-7 is enacted and proved, not declared** — F-C4-SEAL asserts each strip's last exit is at or before 2026-07-07T23:59:59Z. Both strips ride the identical card through one code path.

**The two strips disagree, and that is the first reason not to read either as evidence.** The census era says the amendments cost **152 R**; the pinning window says they are worth **+15 R**. The scored corridor says **−0.16 R**.

**The second reason is that the census strip is the only one large enough to show a tail, and what it shows is that the trail eats it.** On that strip the same code path takes **36 bell exits down to 1** and **91 stop exits up to 126**; it fires **174 advances and 24 harvests**; the win rate rises 10 points, maxDD falls 18 R, tail concentration falls 26 points — **and expectancy goes negative.** That is the same shape change §0 reports on eleven trades, run out over a hundred and twenty-seven, and at that size the shape change is not free. **It is display-only, it registers nothing, and it is the most informative thing in this document.** F-C4-a.

*(The census-era lineage row is Tier-C2's, pinned and labelled historical, and is not restated: CENSUS-2A CEN-5, ride-only, gross R, different corridor / card / ruler / denominator. It was never comparable and is not made comparable by a third card.)*

---

## 8 · THE ANALYTICS TAPE (Amendment B1) — captured, never consulted

**649 rows**, one per `(asset, ts)`: **43 arming · 10 trigger · 11 exit · 3 harvest · 582 daily-00:00Z spine**. The harvest fill is a new instant class in the location record and is captured as one; v3's tape was 640 rows over the same corridor, and the 9-row difference is exactly the 6 extra exit instants the trail created plus the 3 harvests.

**F-C4-6 — no consultation — remains a property, not a promise**, and is now proved over **three** modules in the decision path: AST import scan of `tierc4_rules.py`, `tierc3_rules.py` and `tierc2_rules.py` (zero analytics members in any); an import-closure walk over 241 modules whose project members are exactly `{engine.indicators, tierc2_rules, tierc3_rules, tierc4_rules}`; `engine/`↛`analytics/` (invariant I-B), so the closure cannot reach a registry symbol by any path; and zero tape column names in any of the three sources.

**That last leg was strengthened by this build, because it fired.** Tier-C3 hardened the *import* leg to an AST walk precisely because *"a line-grep gives false positives on this module's own prose"* — and left the *column* leg on raw text. It duly false-positived on a **comment in `tierc4_rules.py` explaining why a field had been renamed away from a tape-column name.** The column leg now scans **code, not text**: comments and docstrings are stripped by AST round-trip, ordinary string literals are **kept** (a `tape["wall_family"]` subscript is a real consultation and a scan that dropped it would be weaker, not cleaner). The transcript prints what the raw-text scan would still say, beside what the code scan says. **F-C4-h.**

**Two tape facts, raw material, conditioned on nowhere:** the single-wall stamp is `multi` on **35 of 43** armings and **426 of 582 (73.2%)** spine instants — v1's F-6, unchanged and ruled for a later TC — and the one lead-in-armed scored trade still has NULL arming-instant tape columns by construction, because the tape does not cross into the sealed span. Disclosed, never back-filled.

**Q6c is why this tape exists and why it is inert.** This is now a **third** unconditioned population of fills over one corridor, and the counterfactual is answerable three times, once per card version, without a conditioning having been paid for. **No location gate is proposed, and none may be until the rescore is done.**

---

## 9 · FIXTURE TRANSCRIPT

**10/10 PASS** — `{"F-C4-1", "F-C4-INHERIT", "F-C4-RAIL", "F-C4-PIVOT", "F-C4-HARV", "F-C4-SEAL", "F-C4-ABLATE", "F-C4-DET", "F-C4-6", "F-KEY"}` all `true`, exit 0. Reproduce: `~/venvs/naiad/bin/python scripts/tierc4_fixtures.py` (496 lines of transcript, local).

| fixture | verdict | evidence |
|---|---|---|
| **F-C4-1** gates | PASS | HEAD · remote `catpatrol/Naiad` · pwd == `$HOME/Naiad` · no cloud-sync token · branch · venv. **ESTATE READY over THREE spans** — corridor, F-5 lead-in, F-7 strip — all 5 assets × {1h, 4h}, **gaps = 0**, monotonic. **SELECTION GUARD loaded, called with 0 candidates, verdict m = 0 — IDLE, as classed.** |
| **F-C4-INHERIT** | PASS | **19 identities asserted with `is`**, two generations deep, plus **35 inherited names** proved to be the parent's object or not redefined here (driven from the program's own `INHERITED_*` tuples). **`REGISTER_DIFF` partitioned FROM THE REGISTER — 4 new numbers + 2 new named rules + 3 re-pointed = 9 of 9 — and every one of the nine proved to be READ by the decision path or the program.** 20 unchanged register values matched; toll **derived**; corridor identical across v1/v3/v4; `PIVOT_LOOKBACK_1H` still retired; the 1H lens unreachable from the v4 program; anchor shape (5,5) ≠ trail shape (2,2) with **one** pivot definition behind both. **And the transcribed entry half proved as an OUTCOME: five Tier-C3 tables content-hash-identical.** Card v4 echoed verbatim. |
| **F-C4-RAIL** | PASS | **Leg 1** — all 11 entry stops asserted individually, R/ATR range 1.000000 → 3.190712, 0 under the v3 rail, 0 under G-8c. **Leg 2 — all 21 advances asserted individually** on seven legs at placement; min distance from the confirming close **1.000000 × ATR**; monotonicity re-asserted across whole campaigns (0 retreats). |
| **F-C4-PIVOT** | PASS | Three advances end to end from raw 4h bars, **one per selection criterion** so two of the three are SUPERSEDED advances that were never paid out. Strict (2,2) flanks printed; the p+2 lag **plus the leg that carries it** — at every earlier as-of bar the right flank is incomplete, so the fractal does not yet exist; the pivot bar's position relative to entry printed (F-C4-k); **CAUSALITY RE-DERIVED** — the campaign's whole stop schedule replayed from the ledger over raw bars, advances applied from conf+1, reproducing the filed exit bar and price, with the ACAUSAL counterfactual replayed beside it; the buffer; the rail; monotonicity; and for a paid-out stop that the exit bar reached it **and that no earlier bar reached it first**. |
| **F-C4-HARV** | PASS | **The harvest rule RE-DERIVED from raw bars and raw EMAs on EVERY one of the 11 campaigns** — first touch of the armed band inside the ride → harvested there once; first touch on the exit bar → `blocked_by`; no armed touch → neither — with the partition asserted **exhaustive and disjoint** (3 + 3 + 0 + 5 = 11). **EVERY fill hand-reconciled** from raw prices, the register's toll and journaled funding, both halves. Halves-sum-to-campaign checked and **labelled as the algebraic tautology it is**. NULL halves on unharvested campaigns. |
| **F-C4-SEAL** | PASS | **Leg 1** every entry anchor re-derived from raw bars, **0 of 11 sealed**, 2 armings refused. **Leg 2 (new)** every one of the 21 ratchet pivots resolved back to its own raw bar and asserted unsealed — **0 sealed**, earliest pivot bar 2025-10-18, seal closes 2025-10-05. **Leg 3** every `_ms`/`ts` column of every filed table **discovered, not curated**. **Leg 4** lead-in table outcome-free. **Leg 5** F-7 on both strips. **Leg 6 (new) THE ONE DELIBERATE SEAL READ, NAMED** — the four masked ablation cells assert `anchors_in_lockbox = 0`, **exactly one** cell is unmasked (`BOTH_NOSEAL`), and it is asserted to **actually read the seal** (1 anchor, 12 campaigns). Leg 3 could never have seen it: the ablation table has no timestamp column. |
| **F-C4-ABLATE** | PASS | **The V3 cell reproduces Tier-C3's filed net R to 2.00e-06** over the same 11 trades — and, in the program, **trade by trade on an OUTER join that HALTs on any one-sided or null row** — so every marginal is the amendment and not the fork. **Five** cells printed with the **interaction term** and the seal floor **printed both ways**. The **BOTH cell asserted to BE the shipped run** (+7.5978 / 11 == headline). UNSCORED. |
| **F-C4-DET** | PASS | Full re-run into `research_outputs/tierc4_run2/`; **all 17 content-hashes identical, the counts block identical, and the selection-guard verdict identical**. Normalized: `['elapsed_s']` and the output root path; *no computed value is normalized*. Seed 20260816 printed and **unused** — determinism is structural. |
| **F-C4-6** | PASS | AST import scan of **three** decision modules · 241-module import closure · `engine/`↛`analytics/` · tape column names scanned over **CODE, not text** (§8), with the raw-text result printed beside it. |
| **F-KEY** | PASS | Asserted in-program **and re-asserted against the 16 written tables** — 0 duplicates. Plus six funnel reconciliation identities, `entered == journal + lead-in`, `headline.net_r == sum(journal.net_r)`, **`ratchet_ledger` rows == Σ`journal.n_advances`**, **`harvest_ledger` rows == `journal.harvested`**, **`journal.final_stop_px` == the campaign's last advance (or its entry stop)**, **the give-back decomposition as an identity to 2.2e-16**, and the triptych's v4 row == this build's own headline. |

### THE REPAIRS — what a six-lens adversarial review found, and what it cost

Tier-C3's own seal breach was found by an audit run **after** the draft was published. This build ran the audit **before**: six independent lenses over the three scripts (the ratchet path, the harvest path, the accounting, the fixtures, the seal-and-inheritance claims, the ablation and delta), each raising at most three findings, each finding then handed to an adversarial verifier instructed to refute it. **Eighteen findings were raised across the six lenses; seven survived the adversarial verification pass. Twelve were acted on**, every one checked by hand against the real data first. **The verification pass ran against a moving target** — repairs were landing while it worked, and at least two verdicts of *refuted* say so in their own reasoning (*"the build itself has since conceded it in code"*). So the 7-of-18 survival rate is **not** a clean signal and the repairs below were decided by checking each finding by hand against the real data, not by the vote.

**Nothing in the headline moved. Every repair was to a claim, a fixture, or a rule the code obeyed by accident rather than by reading.**

| # | what was wrong | what changed |
|---|---|---|
| 1 | **MFE credited the stop bar's favourable extreme**, contradicting F-4's own adverse-first rule — the same loop refused to record a harvest on a stop bar on exactly those grounds | the extreme is credited only for bars the position was held THROUGH. Moved one campaign's give-back (a 1-bar NEAR long whose entire MFE was its own stop bar); **no headline figure** |
| 2 | **the card promised the seal floor "printed both ways" and the build filed no such cell** — the reader would have had to borrow Tier-C3's A0, computed under a different ride | a fifth ablation cell, `BOTH_NOSEAL`: **+6.5515 / 12, −1.0463 R vs BOTH** |
| 3 | **`F-C4-HARV`'s once-only leg was a tautology of the writer's shape** (the ledger emits ≤ 1 row per trade), and only ONE of three fills was reconciled | the harvest rule re-derived from raw bars on **all 11** campaigns with the partition asserted exhaustive; **every** fill hand-reconciled |
| 4 | **`F-C4-PIVOT`'s causality leg compared a value with itself** — `governs_from_ts` vs how `governs_from_ts` is written — and the one falsifiable quantity beside it was computed and never asserted | the campaign's whole stop schedule replayed from raw bars, with the acausal counterfactual replayed beside it (see F-C4-m) |
| 5 | **`F-C4-PIVOT`'s three "adversarial" picks were three draws from one bucket** — every paid-out advance was queued before the second criterion, so the largest advance in the book was never verified | one pick per criterion; two of the three are now SUPERSEDED advances |
| 6 | **two `is` identities compared an object with itself**, and the `INHERITED_*` tuples were decoration nothing read | self-identities removed; the tuples now drive a real leg, plus an AST check that the program redefines none of the names |
| 7 | **the V3-cell reproduction guard was aggregate-only, NaN-permissive and one-sided** — the one thing separating the ablation from a silent fork | outer join, per-trade equality, HALT on any one-sided or null row |
| 8 | **three register rows governed nothing** (`RATCHET_MONOTONE`, `HARVEST_MAX_PER_CAMPAIGN`, `HARVEST_FILL`) and the "exactly three new numbers" claim was a hand-written tuple that mis-counted | all three wired into the decision path; the partition derived from the register and asserted exhaustive; **every row asserted to be read** |
| 9 | **the harvest had no "from below" precondition** — a short entering INSIDE the band would book a phantom first touch on the next bar | the touch arms only once the campaign has closed on its own side of the near edge. **0 entries inside the band across all 153 campaigns in the three windows**, so no number moved |
| 10 | **`BOTH_NOSEAL` files an outcome descended from a SEALED bar** while F-C4-SEAL printed a blanket *"no outcome anywhere in this build"* — and leg 3 is **structurally blind** to it, because the ablation table has no timestamp column. Exactly the class F-C3-a was found by, in a table a timestamp test can never reach | the exception **named, counted and bounded**: `anchors_in_lockbox` per cell, a `seal_read` block in the manifest, and F-C4-SEAL asserting that **exactly one** cell is unmasked and that it **does** read the seal (1 anchor, 12 campaigns vs 11) |
| 11 | **F-C4-ABLATE claimed the V3 cell reproduces Tier-C3 "trade by trade" and checked only the SUM** with a 1e-3 tolerance — offsetting per-trade drift would pass while the sentence beneath it went false | per-trade join re-asserted against the written delta table: **11 of 11 joined 1:1, 0 null, max per-trade diff 0.00e+00** |
| 12 | **`half_move_r` reported a FULL-unit move under a half name**, beside `fraction = 0.5` and two genuine half quantities — a reader reconciling the row would have doubled it | renamed `unit_move_at_harvest_r` / `harvest_unit_move_r_mean`; §3, §5 and §6 corrected (the ETH figure was mis-stated as *"+3.53 R on the half"*; the half booked **+1.7773 R**) |
| — | **the give-back "identity" and the halves-sum HALT were presented as guarantees** when both are algebraic tautologies | both labelled as tautologies wherever printed; the substantive claims moved to the raw-bar reconciliations that actually establish them |
| — | **`HARVEST_MAX_PER_CAMPAIGN` became readable but not enactable** at any value but 1 — the accounting models exactly one reduction, so a 2 would have overwritten the first fill | the row HALTs at import unless it is 1. **A constant that is read but cannot be honoured is worse than one that is ignored, because it looks wired** |

**Two findings were raised, checked and NOT acted on, and they are findings rather than repairs: F-C4-i** (the ratchet's "new pivot" gate is on the confirmation bar) and **F-C4-k** (the causality leg is not falsifiable on this corridor's data). Both are in §10.

### The independent re-derivation — a builder's check, OUTSIDE the ten-fixture contract

Every fixture above re-derives its evidence from raw bars, but it re-derives it **by calling the same functions the program called** — that is what makes a fixture cheap and it is also its limit. Tier-C3's seal breach was found by an adversarial audit that had no fixture at all.

So `scripts/tierc4_independent.py` **re-implements the whole v4 card from the card text**, sharing with the build **only** `engine.indicators.ema/.atr` (the estate's primitives of record, which Stage B must ride identically anyway), the cache location, and the raw bars. It imports neither `tierc4_rules` nor `tierc4_baseline` nor their parents. The (5,5) anchor scan, the (2,2) fractal scan, the cross detector, the arming loop, the seal mask, the ride, the ratchet, the harvest and the accounting are all written again, in a different shape — a naive O(n) python scan instead of `engine.s1._pivots`' rolling/shift form, an inline cross instead of `crossover`, one flat loop instead of the program's layered closures.

**It agrees on all eleven trades** — same population, same R to 6 dp, same advance count, same harvest flag, same net R to 6 dp; the worst gap between its unrounded value and the filed 6-dp column is 4.96e-07, which is **below the 5e-7 floor rounding alone imposes**. Exit 0; it HALTs non-zero on any disagreement.

**What that rules out, and only that:** the shipped numbers are not an artefact of how the program is factored. It does **not** say the card is right, that the corridor is representative, or that either reading matches the operator's intent — those are §10 and the operator's rulings.

**Suite:** `pytest fixtures tests -m "not slow"` → **333 passed, 1 skipped, 1 deselected, exit 0**. **Nothing here touched an existing test, and that is checkable rather than asserted:** `grep -rl "tierc4\|tierc3" tests fixtures` returns nothing, so no collected test imports this build or its predecessor and the suite cannot have been moved by either. *(The count is 333 rather than Tier-C3's 323 because other lanes landed tests between the two builds.)*

---

## 10 · FINDINGS — NOT FIXED

**F-C4-a · THE MEAN WAS BOUGHT WITH THE TAIL, AND THE BILL IS ONLY VISIBLE AT SCALE.** §0, §7. On the scored corridor the amendments cost **−0.1636 R** and halve maxDD, cut tail concentration by 21 points and flip the ex-best-trade result from **−2.2912 to +1.4184**. On the DISPLAY-ONLY 127-trade census strip the same code path takes **+145.4539 R to −7.0097 R** and the best trade from **+165.79 to +5.85**. The corridor is too small to see a tail; the strip is not evidence. **Ruling needed: is a mean bought with the tail the object the estate wants — and if the answer is yes, the trail needs a rule that lets a runner run (a wider trail once N R is banked, or a trail that only arms after a threshold), which is a NEW card and a new probe, not a tune of this one.** Related: CENSUS-2A CEN-5 already recorded that *"any exit study on this book is a study of tail preservation"* — this build is the first to measure the cost of failing that test.

**F-C4-b · THE TRAIL'S "BEYOND" IS AN UNRULED READING, AND IT IS LOAD-BEARING ON TWO-THIRDS OF THE ADVANCES.** The card says *"advance the stop to beyond that pivot"*. `RATCHET_BUF_ATR` is re-pointed from the v3 card's own `STOP_BUF_ATR = 0.5` because *beyond* is that card's word for exactly this offset. The alternative reading — **0.0, the stop exactly AT the pivot** — is a different card, and **the pivot buffer (not the rail) set the stop on 14 of 21 advances**, so the two readings disagree on most of them. **Counts only; no R is attached to either reading, deliberately** — a swept parameter with an outcome beside it is a selection surface. **Ruling needed: pin the trail's offset in the card.** Same shape as the still-open F-C3-c.

**F-C4-c · THE RATCHET RETIRES THE BELL.** **11 of 11 scored campaigns exit on a stop; zero on a bell.** On the display-only census strip, **126 of 127**. The bell — counter-12/89 or 89/316-against — has been the card's exit since Tier-C2 and the amendment has made it very nearly unreachable without anyone voting to remove it. **Ruling needed: is the bell now a backstop that is expected never to fire, or is it dead law that should be struck from the card?** A rule that never fires is not free: it is still in the card text, still in the fixtures, and still shapes how the card is read.

**F-C4-d · MONOTONICITY ADMITS ARBITRARILY SMALL ADVANCES, AND ONE OF THEM WAS PAID OUT.** The rule is *"stops only advance, never retreat"*, enforced as a strict inequality. The smallest advance in the book is **0.002053 ATR** (SOLUSDT 2025-11-11, advance #7 of 7) — and it is **the advance that took the campaign**. A 0.002-ATR advance is not a decision, it is arithmetic noise that happened to clear zero. **Ruling needed: a minimum advance increment (in ATR), or ratify that any strict improvement counts.** Not fixed, because inventing a threshold here would be pinning a [VETO] by inspection.

**F-C4-e · THE HARVEST IS A DE-RISK, NOT A PROFIT-TAKE, AND ITS COST IS NOT WHERE IT LOOKS.** §3. The band sits on the ADVERSE side of a short, so the touch fires early-and-negative on campaigns that die (cutting the loss) and late-and-positive on campaigns that run (banking the tail). Under HARVEST-only **the fills themselves net +1.7282 R** and the amendment still costs **−3.1814 R** — the entire cost is the half that was not allowed to run. Under the shipped card the trail pre-empts every favourable fill, so all three survivors are of the loss-cutting kind. **Ruling needed: is halving the runner the intent? The natural alternatives — harvest only when the half is in profit, or harvest only above a threshold in R — are different cards.**

**F-C4-f · THE TWO AMENDMENTS ARE NOT SEPARABLE AND MUST NOT BE QUOTED SEPARATELY.** Interaction **+3.4530 R** on eleven trades. Harvest fills fall from **9 to 3** when the trail is on. **Any sentence of the form "the harvest is worth −3.18 R" is false about the shipped card**, and the ablation table carries the interaction column so that sentence cannot be written from it by accident. This is the same class of error as F-C3-b — crediting a result to the wrong half of a two-part change — caught before publication this time rather than after.

**F-C4-g · n = 11, ONE REGIME, AND THE RESULT NOW RESTS ON TWO TRADES.** ETH +6.1794 and ZEC +5.1566 sum to **+11.3360 against a net of +7.5978**. That is materially better than v3's one-trade dependence — the top-decile share falls 71.83% → 50.76% and the ex-best result changes sign — and it is not independence. Nine of eleven trades are still shorts. **PROVISIONAL is carried on every headline row.** F-C3-d's question is unchanged and still unanswered: **is an 11-trade, one-regime result an acceptable bar for anything to beat?**

**F-C4-h · THE FIXTURES WERE THE WEAKEST PART OF THE BUILD, AND A SIX-LENS REVIEW SAID SO IN NINE PLACES.** §9's repair table. The pattern across every one of them is the same and is worth naming above the instances: **a check that re-derives a value the way the program derived it, and then compares it to itself, prints PASS and tests nothing.** Four legs of the first draft were of that shape — the once-only harvest, the causality assertion, the halves-sum HALT, the give-back "identity" — and two more (`x is x`, a hand-written 3-tuple of "new numbers") were the same defect wearing different clothes. **All are repaired and all are labelled where they remain structural.** The estate has now met this shape in three consecutive builds: Tier-C3's `arm_ms` dropped from a curated column list, Tier-C3's own note that *"a hand-written tuple is a scan that passes by construction"*, and these. **Recommendation, not a ruling: a standing fixture convention that every leg must name what would have to be true for it to FAIL, and that a leg with no such answer is not a leg.** Related and unfixed: F-C3-6's `engine/` grep for `import analytics` is still a raw text scan and is still wrong in the same way — it is Tier-C3's file and this build does not edit a predecessor's code.

**F-C4-i · THE RATCHET'S "NEW PIVOT" GATE IS ON THE CONFIRMATION BAR, WHICH IS A READING.** The card says *"when a new FAVOURABLE 4h swing pivot CONFIRMS"*, and `ratchet_step` gates on `conf > entry bar`. Because a fractal's confirmation trails its pivot bar by `RATCHET_PIVOT_R = 2`, that gate **would admit a pivot BAR at entry − 1 or entry** — structure that formed before the trade existed. **It did not bind: the earliest advance in this book confirms 5 bars after its entry, so the nearest pivot bar sits at entry + 3.** The alternative reading — gate on the pivot BAR being after entry — is a different card and is NOT taken. **Ruling needed: pin "new" to the confirmation or to the pivot bar.** Counts only, no R attached to either reading. Same shape as the still-open F-C3-c. *(The loose version of this argument also underwrote the seal claim in the first draft — "every ratchet pivot confirms after an entry that is after the seal" does not place the PIVOT BAR after the seal. The prose is fixed; the proof never depended on it, because F-C4-SEAL checks every pivot bar directly.)*

**F-C4-j · THE HARVEST'S "FROM BELOW" WAS A PRECONDITION THE FIRST DRAFT LEFT UNGUARDED.** The card says *"price into the band from below"*; the first implementation tested only that the bar's extreme reached the near edge, with no state saying the campaign had ever been outside the band. A short whose trigger close sat between e89 and e316 would have booked 50% out on the very next bar, recorded as a band touch that crossed nothing — and F-C4-HARV would have certified it, because both of its legs were true of that case. **Fixed: the touch arms only once the campaign has closed on its own side of the near edge. It changes no number — 0 of the 153 campaigns across all three windows entered inside the band — and it is in the card text now because "it did not happen to bind" is not a rule.** Named because the tide gate only constrains price against e316, never against e89, so nothing structural prevents it on another corridor.

**F-C4-k · THE CAUSALITY LEG IS SOUND AND NOT FALSIFIABLE ON THIS DATA, AND THAT IS SAID RATHER THAN GLOSSED.** F-C4-PIVOT now replays each picked campaign's whole stop schedule from raw bars with advances applied from `conf + 1`, reproducing the filed exit bar and price — and replays the ACAUSAL version, advances applied one bar early, beside it. **On all three picks the two are IDENTICAL**, because no confirming bar in this book has its own adverse extreme reaching the stop it created. So the leg reproduces the ride but does not, on this corridor, distinguish a causal implementation from an acausal one. **The guarantee therefore still rests on reading the code, and the fixture prints that sentence rather than letting a PASS imply more.** **Not fixed: manufacturing a synthetic bar to force the discrimination would be a fixture testing a fabricated tape, which is a different and larger decision than this build is authorised to make.**

**F-C4-l · THE LIVE PAPER LINE IS NOW TWO FULL CARD VERSIONS BEHIND.** F-C3-g recorded that `configs/tierc2_paper.yaml` and `research_outputs/tierc2/heartbeat.json` still enact the **v1** card. They still do. **The gap is now v1 → v4.** No Stage B was commissioned for Tier-C4 and none was built. Named again, and more loudly, because a forward paper line quietly running a card three generations old is exactly the drift the estate's conventions exist to catch.

**F-C4-m · CARRIED, UNCHANGED, FROM TIER-C3.** **F-C3-a** the seal floor (still taken, still enacted in code, still overturnable in one line; the ratchet now takes the same mask and F-C4-SEAL proves it never binds on this corridor) · **F-C3-b** the Tier-C3 name and its attribution · **F-C3-c** the anchor lookback, bars vs hours · **F-C3-d** the acceptance bar · **F-C3-e** two rails for one concept, G-8c 0.5 vs the card's 1.0 — **and note the ratchet re-points the card's rail to a THIRD site (an advanced stop against the confirming close) without adding a fourth constant, which is the discipline F-C3-e asked for** · **F-C3-i** `exchange/**` auto-publishes, so a draft build document is published the instant it is written. **And m = 0 holds**: this is a complete, unranked replay of one pre-named card. The moment a cell is picked out of §3 on its R, the selection surface is the number of cells that were available to pick from, and that *m* must be declared **before** the look.

---

## 11 · DISPOSITION + BOX-COST

| item | disposition |
|---|---|
| `scripts/tierc4_rules.py` | **new** — decision path; analytics-free by import closure; Tier-C3's and Tier-C2's objects bound, not copied |
| `scripts/tierc4_baseline.py` | **new** — replay · ratchet · harvest · tape · tables · delta · ablation · triptych |
| `scripts/tierc4_fixtures.py` | **new** — 10/10 PASS, HALTs non-zero |
| `scripts/tierc4_independent.py` | **new** — a second reading of the card, sharing only the engine's EMA/ATR primitives and the raw bars; agrees on all 11 trades; HALTs non-zero. **Filed so the strongest check in the build is reproducible rather than asserted. NOT part of the ten-fixture contract** |
| `research_outputs/tierc4/` | **built** — 17 parquet + manifest, local, gitignored |
| `research_outputs/tierc4_run2/` | **built, hashed, DATA DISCARDED** per rule R3; `build_manifest.json` retained per refinement D-3 |
| `.gitignore` | **modified** — `research_outputs/tierc4{,_run2}/**` |
| THE HEADLINE | **+0.6907 R / trade over 11 trades**, positive, **PROVISIONAL** — and **+1.4184 R over ten without the best trade**, which is the point |
| THE ABLATION | **built** — ratchet −0.4352, harvest −3.1814, both −0.1636, **interaction +3.4530**; and the seal floor **printed both ways** (BOTH_NOSEAL +6.5515 / 12) |
| THE SEAL | **held, and extended to the second published price** — 0 of 11 anchors and 0 of 21 ratchet pivots sealed, proved per row by F-C4-SEAL. **Printed both ways, with the one deliberate read named, counted and bounded** in the manifest's `seal_read` block |
| THE REVIEW | **run BEFORE publication** — six lenses, 16 findings, **9 repaired**, 2 carried as findings (F-C4-i, F-C4-k), headline unmoved |
| THE SELECTION GUARD | **loaded, called, IDLE at m = 0** — recorded in the manifest, asserted by F-C4-1 |
| `engine/` · `analytics/` · `scripts/tierc2_*` · `scripts/tierc3_*` · `com.naiad.daily` | **UNTOUCHED** — zero diff |
| registrations | **none**, as classed |

### BOX-COST

**Figures below are `publish_exchange`'s own, read from the publish that filed this document — not estimated.** `BOX_BYTES` / `WARN_FRACTION` / `REFUSE_FRACTION` were read live from the module, never typed.

| | before this paste | **after** |
|---|---:|---:|
| `exchange/**` | 2,973,220 B · 18.58% | **3,044,451 B · 19.03%** (167 files) |
| **tick set** (`exchange/**` + `LEDGER.md`) — *governs* | 3,232,518 B · 20.20% | **3,303,749 B · 20.65%** |
| level | OK | **OK** (warn 40% / refuse 70%) · headroom to REFUSE ≈ **7.90 MB** |

**This paste's own two files: ≈ 68.8 KB (this document) + 4,635 B (the `LEDGER_APOLLO` append) ≈ 73.4 KB ≈ 0.46% of the box.** *(The document's own size is quoted approximately on purpose: a byte-exact self-measurement inside the file it measures cannot converge.)*

**AGAINST THE < 0.5% TARGET (80,000 B) THAT IS 92% OF BUDGET, WITH ≈ 6.6 KB UNSPENT — and it is a bigger document than Tier-C3's 50,439 B.** The card said LEAN and this is not lean. Where the extra went, so the operator can rule on it: the five card deliverables cost what they cost, and **§9's repair table plus five new findings are the post-review overhead**. **Named rather than trimmed, because the alternative was to cut the record of what the review found, which is the one part of a build document that cannot be re-derived from the tables.**

**THE NAMING TRIP-WIRE FIRED ON THIS DOCUMENT AND IT IS ANSWERED HERE, NOT IGNORED.** `publish_exchange` names every box-bound file over the absolute 64,000 B wire and requires each to have an intended home in the disposition table (CONVENTIONS §3.2). This paste puts two files over it: **`BUILD_2026-08-16_TIERC4_MEANCARD.md` at ≈ 68,700 B** — intended home: **`exchange/reports/`, permanent, the build's only document, per the card's "ONE build doc"**; and **`exchange/status/LEDGER_APOLLO.md` at 122,526 B**, which was already over the wire before this paste and is **append-only by ruling** — its home is `exchange/status/` and its growth is structural, not this build's to fix. *(The wire is a naming rule; it never refuses a publish. It is answered because an unanswered trip-wire is how a soft rule becomes decoration.)*

The full fixture transcript (496 lines), the 649-row tape, the 21-row ratchet ledger beyond the four narrated in §5, and the per-trade journal stay **local**. **What is printed whole is what a reader cannot re-derive from a pointer: the two amendments, the triptych, the ablation with its interaction, the per-trade delta with its give-back, the ETH narration, and the findings.**

**Constants: pin-vs-import per site, per CONVENTIONS §6.4.** `tierc4_rules.py` **defines** four new values and two new named rules, **re-points** three by binding the v3 constant object itself into the register row, and **inherits** every other by import from `tierc3_rules.REGISTER`. **Every one of the nine is asserted to be read by the code it governs.** **Ledger citations in this build are by QUOTE, not by line.**

---

## 12 · THE LEDGER_APOLLO APPEND

Per the 2026-08-12 `append` ruling — *a report without its ledger entry is an incomplete deliverable* — this document ends by appending the session's STATUS entry to `exchange/status/LEDGER_APOLLO.md`, **in this session**. Quoted by its spine only.

```
=== STATUS_APOLLO — 2026-08-16b ===
NOW: TIER-C4 IS MEASURED. THE MEAN CARD — the v3 card plus the LPS-trail ratchet
     and the creek/ice harvest — is +0.6907 R per trade over 11 trades against
     TIER-C3's +0.7056 over 11. THE MEAN DID NOT MOVE. THE SHAPE DID:
         maxDD 4.2697 -> 2.0348 · tail share 71.83% -> 50.76% ·
         net R WITHOUT the best trade -2.2912 -> +1.4184, WHICH CHANGES SIGN.
     The operator asked for "a mean for the average trade" and got one.
     THE PRICE IS THE TAIL, and it is only visible at scale: on the DISPLAY-ONLY
     127-trade census strip the same code path takes +145.4539 R -> -7.0097 R and
     the best trade +165.79 -> +5.85. Display-only, hypothesis generation only,
     and the most informative number in the build. F-C4-a.
     ABLATION (unscored, one code path, five cells): V3 +7.7614 | RATCHET-only
     +7.3262 | HARVEST-only +4.5800 | BOTH +7.5978 | BOTH_NOSEAL +6.5515/12.
     INTERACTION +3.4530 — the two amendments are NOT separable and must not be
     quoted apart. The trail pre-empts the harvest: 9 fills alone, 3 together.
CLASS: measurement, not registration. m = 0. ONE pre-named card, no grid, no
     sweep; the selection guard is LOADED, CALLED and IDLE at m = 0, in the
     manifest. NO lockbox read. No estate write. No live orders. engine/,
     analytics/, scripts/tierc2_* and scripts/tierc3_* byte-untouched.
RIDE-ONLY, PROVED AS AN OUTCOME: the ENTRY half of the ride loop is a hand
     TRANSCRIPTION, not an import, so `is` cannot reach it — and five Tier-C3
     tables therefore come out CONTENT-HASH-IDENTICAL (funnel, lead_in_census,
     lead_in_trades, strip_d_unscored, anchor_lookback_disclosure). Same
     armings, same entries, same entry stops. The bell-only counterfactual is
     byte-identical at -0.0919 R. An INDEPENDENT re-implementation written from
     the card text (scripts/tierc4_independent.py, sharing only the engine's
     EMA/ATR and the raw bars) agrees on all 11 trades.
THE REVIEW RAN BEFORE PUBLICATION, NOT AFTER: six adversarial lenses over the
     three scripts, 18 findings raised, TWELVE REPAIRED. Nothing in the headline
     moved; every repair was to a claim, a fixture, or a rule the code obeyed by
     accident rather than by reading. The recurring shape — a check that
     re-derives a value the way the program derived it and compares it to itself
     — accounted for six of them. The sharpest catch: BOTH_NOSEAL files an
     outcome descended from a SEALED bar while F-C4-SEAL printed a blanket "no
     outcome anywhere in this build", and leg 3 was structurally blind to it
     because the ablation table has no timestamp column — the F-C3-a class
     again, in a table a timestamp test can never reach. Now named, counted and
     bounded (manifest `seal_read`). Recommendation in F-C4-h: a standing
     convention that every fixture leg must name what would have to be true for
     it to FAIL.
PENDING (operator): 5 rulings, all in section 10 --
     F-C4-a  IS A MEAN BOUGHT WITH THE TAIL THE OBJECT THE ESTATE WANTS? If yes,
             the trail needs a rule that lets a runner run, which is a NEW card
             and a new probe, not a tune of this one
     F-C4-b  PIN THE TRAIL'S "BEYOND" in the card. 0.5 ATR (taken, re-pointed
             from the entry anchor's own word) vs 0.0 (the stop at the pivot).
             The pivot buffer, not the rail, set the stop on 14 of 21 advances
     F-C4-c  THE RATCHET RETIRES THE BELL: 11 of 11 scored campaigns exit on a
             stop, 126 of 127 on the display strip. Backstop, or dead law?
     F-C4-d  A MINIMUM ADVANCE INCREMENT, or ratify that any strict improvement
             counts. The smallest advance in the book is 0.002053 ATR and it is
             the one that was PAID OUT
     F-C4-e  IS HALVING THE RUNNER THE INTENT? The harvest's fills NET +1.7282 R
             and the amendment still costs -3.1814 R — the cost is the half that
             was not allowed to run
     -- also filed, not blocking: F-C4-f (not separable), F-C4-g (n = 11, two
     trades), F-C4-h (the fixture-hygiene pattern, three builds running),
     F-C4-i (the "new pivot" gate is on the CONFIRMATION bar — a reading that
     did not bind), F-C4-j (the harvest's "from below" precondition, now in the
     card, 0 of 153 campaigns affected), F-C4-k (the causality leg is sound and
     NOT falsifiable on this corridor's data), F-C4-l (the live paper line is
     now TWO card versions behind), F-C4-m (F-C3-a..e and F-C3-i carried).
PROBE LEDGER: m = 0. EXPLORATION — ungated; promotion requires registration.
=== END STATUS ===
```

---

*End of build document. TIER-C4 · measurement, not registration · m = 0 · one pre-named card · no outcome, price or anchor drawn from a sealed bar · no registrations. The mean is there, the tail paid for it, and both numbers are on the record.*
