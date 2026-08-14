# BUILD · 2026-08-14 · CENSUS-2B PART A + W-TB1

**Contract:** operator paste 2026-08-14, two ratified blocks — *CENSUS-2B · PART A — COMPLETION AUDIT +
SEQUENTIAL SUBSTRATE (run BEFORE W-TB1)* and *CENSUS-2B · W-TB1 — TAIL BIOGRAPHY*.
Drafted: APOLLO (W-TB1 scope credit: DIONYSUS §4). Executor: HEPHAESTUS. Seed 20260814.
**CLASS:** Tier-E substrate + Tier-E descriptive. **NO REGISTRATIONS.** F-KEY everywhere.
NaN-before-warm inherited from V-ULT-1, not re-implemented.

Part A's close supersedes W-TB1's: the two blocks land in **one** build document, this one.
`BUILD_2026-08-14_CENSUS2B_WTB1.md` is therefore not written, by contract, not by omission.

---

## 0 · GATES — every hard assertion, printed

| assertion | result |
|---|---|
| `git rev-parse --short HEAD` | `7e80d01` |
| `git remote -v` contains `catpatrol/Naiad` | yes — `https://github.com/catpatrol/Naiad.git` |
| `pwd` | `/c/Naiad` |
| IDENTITY two-sided: ends `C:/Naiad` or `/c/Naiad` **and** no `OneDrive` | PASS |
| `git branch --show-current` == `v12-v1-census` | PASS |
| DRIVE GATE `wait_for_drive('D:/Naiad')` | **PRESENT** |
| `census2b_manifest.json` exists | PASS |
| manifest pins include {feasibility, emas, ribbons, crosses} | PASS — all four, plus `firstlook` |
| spot-verify one `emas` parquet sha | PASS — `emas/BTCUSDT/12h.parquet` `8db770cc2070…` recomputed, identical |
| `ribbons/BTCUSDT/5m.parquet` loads with {width_atr, state, orientation, knot} | **PASS with a naming note** (below) |
| `scripts/census2b_program.py` exists | PASS |
| `exchange/reports/CENSUS2A_PROBE_LEDGER.md` exists | PASS |

**The one naming note, stated rather than smoothed over.** The gate names bare columns
`{width_atr, state, orientation, knot}`. The stored schema is **per-SR-prefixed**:
`FAST_width_atr`, `FAST_state`, `FAST_orient`, `FAST_knot`, and the same for `M/MH/H/VH/UH` — 56
columns, six bands. The gated geometry is all present; the orientation code is spelled `orient`, and
the columns are per-band because a ribbon file carries six ribbons. Read as a check that the ribbon
geometry exists, the gate passes. Read as a literal string match, it does not. It is recorded as
PASS with the exact schema quoted, so nobody has to guess which reading was taken.

---

## 1 · A-0 — COMPLETION AUDIT · **the census-2B completion certificate**

This is the table the reviewer could not obtain from the box. A cell counts PRESENT only if the
manifest pins it, the file is on disk, **and its recorded sha256 still matches the bytes**. A
pinned-but-changed file reports STALE, which is neither PRESENT nor ABSENT. 157 cells probed against
the 100 artifacts V-ULT-1 pinned; every sha recomputed from the bytes on D:.

```
stage        asset     lens  state                  rows         bytes  sha256[:16]
--------------------------------------------------------------------------------------------------------
feasibility  -         -     PRESENT                 630        12,402  273e4f97bf0f0eca
emas         BTCUSDT   1m    ABSENT                                     
emas         BTCUSDT   5m    PRESENT             728,833    88,690,998  46422108056fa9e0
emas         BTCUSDT   15m   PRESENT             242,945    36,937,902  d5d6c380a1227248
emas         BTCUSDT   30m   PRESENT             121,473    18,108,111  08f66d1a37b16652
emas         BTCUSDT   1h    PRESENT              60,737     8,651,685  7e5e6f9b1c20fb8d
emas         BTCUSDT   4h    PRESENT              15,184     1,719,202  1da95f770511fa77
emas         BTCUSDT   12h   PRESENT               5,061       481,180  8db770cc20704554
emas         ETHUSDT   1m    ABSENT                                     
emas         ETHUSDT   5m    PRESENT             705,915    84,421,348  1d8783cdeca2cd1c
emas         ETHUSDT   15m   PRESENT             235,305    35,045,554  c36ee7b86e839123
emas         ETHUSDT   30m   PRESENT             117,653    17,287,615  68f77b2433e8415f
emas         ETHUSDT   1h    PRESENT              58,827     8,294,646  ea7dd7571c372f6c
emas         ETHUSDT   4h    PRESENT              14,707     1,650,152  deaa005f2ac1529d
emas         ETHUSDT   12h   PRESENT               4,902       462,549  5e356d384b0bc82d
emas         SOLUSDT   1m    ABSENT                                     
emas         SOLUSDT   5m    PRESENT             621,828    73,568,885  e94312eec54afd3f
emas         SOLUSDT   15m   PRESENT             207,276    29,904,526  585ef7331449b835
emas         SOLUSDT   30m   PRESENT             103,638    14,734,659  414bb1cad25066d7
emas         SOLUSDT   1h    PRESENT              51,819     7,096,474  6e66a648bc651a47
emas         SOLUSDT   4h    PRESENT              12,955     1,412,045  7a48b21ab62b49b9
emas         SOLUSDT   12h   PRESENT               4,318       396,518  dabb74dacb895d2f
emas         NEARUSDT  1m    ABSENT                                     
emas         NEARUSDT  5m    PRESENT             612,888    71,174,963  6cd56ac4ce5a2881
emas         NEARUSDT  15m   PRESENT             204,296    28,691,733  efe19fd3c14eeb7f
emas         NEARUSDT  30m   PRESENT             102,148    14,015,738  76f1bc295e832243
emas         NEARUSDT  1h    PRESENT              51,074     6,691,521  c0cde2327280e846
emas         NEARUSDT  4h    PRESENT              12,768     1,321,754  809f1d7c683ce26b
emas         NEARUSDT  12h   PRESENT               4,256       377,593  2c9021c697a49122
emas         ZECUSDT   1m    ABSENT                                     
emas         ZECUSDT   5m    PRESENT             685,752    77,439,612  cfaebca7f715b6b2
emas         ZECUSDT   15m   PRESENT             228,584    32,072,792  5ef184aabda700e5
emas         ZECUSDT   30m   PRESENT             114,292    15,717,957  46fa8c26de0368a5
emas         ZECUSDT   1h    PRESENT              57,146     7,554,398  76cade3502299369
emas         ZECUSDT   4h    PRESENT              14,286     1,521,982  e187dff8322998f7
emas         ZECUSDT   12h   PRESENT               4,762       433,407  35c1dd2dd2e1c86d
emas         JTOUSDT   1m    ABSENT                                     
emas         JTOUSDT   5m    ABSENT                                     
emas         JTOUSDT   15m   ABSENT                                     
emas         JTOUSDT   30m   ABSENT                                     
emas         JTOUSDT   1h    ABSENT                                     
emas         JTOUSDT   4h    ABSENT                                     
emas         JTOUSDT   12h   ABSENT                                     
emas         TAOUSDT   1m    ABSENT                                     
emas         TAOUSDT   5m    ABSENT                                     
emas         TAOUSDT   15m   ABSENT                                     
emas         TAOUSDT   30m   ABSENT                                     
emas         TAOUSDT   1h    ABSENT                                     
emas         TAOUSDT   4h    ABSENT                                     
emas         TAOUSDT   12h   ABSENT                                     
ribbons      BTCUSDT   1m    ABSENT                                     
ribbons      BTCUSDT   5m    PRESENT             728,833   117,983,222  69368295e62da2c4
ribbons      BTCUSDT   15m   PRESENT             242,945    49,286,610  5e07687831ffdd17
ribbons      BTCUSDT   30m   PRESENT             121,473    23,819,096  51735bed3ddb80ff
ribbons      BTCUSDT   1h    PRESENT              60,737    11,160,643  a6166a1bf31c1b88
ribbons      BTCUSDT   4h    PRESENT              15,184     1,973,543  1d2f2ccc402d3264
ribbons      BTCUSDT   12h   PRESENT               5,061       517,349  ade5ca97b9a31875
ribbons      ETHUSDT   1m    ABSENT                                     
ribbons      ETHUSDT   5m    PRESENT             705,915   114,386,631  335558f4760d721d
ribbons      ETHUSDT   15m   PRESENT             235,305    47,500,434  efedbf729b88faf5
ribbons      ETHUSDT   30m   PRESENT             117,653    22,968,647  1f1188b94b8d9cf8
ribbons      ETHUSDT   1h    PRESENT              58,827    10,757,844  7da8b9b2220ecb7e
ribbons      ETHUSDT   4h    PRESENT              14,707     1,894,720  883b887e81ff860c
ribbons      ETHUSDT   12h   PRESENT               4,902       496,202  98f698bbe01a3d47
ribbons      SOLUSDT   1m    ABSENT                                     
ribbons      SOLUSDT   5m    PRESENT             621,828   102,564,919  a84fad680db0fe5c
ribbons      SOLUSDT   15m   PRESENT             207,276    41,560,056  e10aa2ea2a96f6f0
ribbons      SOLUSDT   30m   PRESENT             103,638    20,003,015  6ef5c42550d2c98b
ribbons      SOLUSDT   1h    PRESENT              51,819     9,314,704  e69b26bb1554e0df
ribbons      SOLUSDT   4h    PRESENT              12,955     1,605,344  b4fadbdf69695c3a
ribbons      SOLUSDT   12h   PRESENT               4,318       419,519  059dbc7ac4ec354e
ribbons      NEARUSDT  1m    ABSENT                                     
ribbons      NEARUSDT  5m    PRESENT             612,888   100,924,514  b53efed472cb7a3d
ribbons      NEARUSDT  15m   PRESENT             204,296    40,756,398  234a7039affc4c54
ribbons      NEARUSDT  30m   PRESENT             102,148    19,573,449  f924480e6b92ea7a
ribbons      NEARUSDT  1h    PRESENT              51,074     9,089,595  dd460ab23a0d2798
ribbons      NEARUSDT  4h    PRESENT              12,768     1,558,101  06e0041797bfc15a
ribbons      NEARUSDT  12h   PRESENT               4,256       409,719  9fc7832658969f4f
ribbons      ZECUSDT   1m    ABSENT                                     
ribbons      ZECUSDT   5m    PRESENT             685,752   110,413,668  d9304aa43213848d
ribbons      ZECUSDT   15m   PRESENT             228,584    45,657,121  0c796d9c7370ba91
ribbons      ZECUSDT   30m   PRESENT             114,292    22,018,743  7fe557d9531e04e2
ribbons      ZECUSDT   1h    PRESENT              57,146    10,296,756  0b750d2fa9b7b2ec
ribbons      ZECUSDT   4h    PRESENT              14,286     1,806,228  902d4a7653da09f3
ribbons      ZECUSDT   12h   PRESENT               4,762       474,478  3cab068d835c231a
ribbons      JTOUSDT   1m    ABSENT                                     
ribbons      JTOUSDT   5m    ABSENT                                     
ribbons      JTOUSDT   15m   ABSENT                                     
ribbons      JTOUSDT   30m   ABSENT                                     
ribbons      JTOUSDT   1h    ABSENT                                     
ribbons      JTOUSDT   4h    ABSENT                                     
ribbons      JTOUSDT   12h   ABSENT                                     
ribbons      TAOUSDT   1m    ABSENT                                     
ribbons      TAOUSDT   5m    ABSENT                                     
ribbons      TAOUSDT   15m   ABSENT                                     
ribbons      TAOUSDT   30m   ABSENT                                     
ribbons      TAOUSDT   1h    ABSENT                                     
ribbons      TAOUSDT   4h    ABSENT                                     
ribbons      TAOUSDT   12h   ABSENT                                     
crosses      BTCUSDT   1m    ABSENT                                     
crosses      BTCUSDT   5m    PRESENT             688,963     9,956,297  40295c2a23828501
crosses      BTCUSDT   15m   PRESENT             221,036     3,995,251  de7c14c5d4dcc276
crosses      BTCUSDT   30m   PRESENT             105,527     1,863,277  67239e41915a335c
crosses      BTCUSDT   1h    PRESENT              50,454       879,308  4a29001493ea33f9
crosses      BTCUSDT   4h    PRESENT              11,146       193,027  5eee077451c84ddb
crosses      BTCUSDT   12h   PRESENT               3,289        61,432  cb60e17aac438bce
crosses      ETHUSDT   1m    ABSENT                                     
crosses      ETHUSDT   5m    PRESENT             664,252     9,647,512  7ae70bfdbb167851
crosses      ETHUSDT   15m   PRESENT             213,073     3,802,578  1a691f5356d3867f
crosses      ETHUSDT   30m   PRESENT             103,074     1,811,994  12b2b513f8efad51
crosses      ETHUSDT   1h    PRESENT              48,801       849,670  a485ae3de5d330d3
crosses      ETHUSDT   4h    PRESENT              11,108       192,064  627dba3eca6ad9d3
crosses      ETHUSDT   12h   PRESENT               3,218        59,253  c93744a5404b97e0
crosses      SOLUSDT   1m    ABSENT                                     
crosses      SOLUSDT   5m    PRESENT             572,880     8,500,559  815932fc2b50d3ad
crosses      SOLUSDT   15m   PRESENT             184,996     3,307,517  74fd4035c263eaa2
crosses      SOLUSDT   30m   PRESENT              90,591     1,594,244  90d09276baab0020
crosses      SOLUSDT   1h    PRESENT              43,626       757,444  8b4f6b2002f8839f
crosses      SOLUSDT   4h    PRESENT              10,012       171,907  60a975c9ba199682
crosses      SOLUSDT   12h   PRESENT               2,936        54,333  78aab621723e620c
crosses      NEARUSDT  1m    ABSENT                                     
crosses      NEARUSDT  5m    PRESENT             577,967     8,503,393  68663e33b5050491
crosses      NEARUSDT  15m   PRESENT             187,894     3,326,117  be45981becfc6d2f
crosses      NEARUSDT  30m   PRESENT              90,874     1,591,857  ad536cc446ad474c
crosses      NEARUSDT  1h    PRESENT              43,533       754,278  0f5e37e86954918c
crosses      NEARUSDT  4h    PRESENT               9,535       165,488  3288281ea7ce2f57
crosses      NEARUSDT  12h   PRESENT               2,770        51,771  e31dd559a955f0fd
crosses      ZECUSDT   1m    ABSENT                                     
crosses      ZECUSDT   5m    PRESENT             649,788     9,415,439  2f8b9187294254c6
crosses      ZECUSDT   15m   PRESENT             214,150     3,776,697  390a2ece728abb73
crosses      ZECUSDT   30m   PRESENT             104,049     1,810,238  4ee934686da09a94
crosses      ZECUSDT   1h    PRESENT              50,372       862,367  7deae8923d624026
crosses      ZECUSDT   4h    PRESENT              11,380       193,719  234d03168a172ab8
crosses      ZECUSDT   12h   PRESENT               3,396        62,536  050025e1ed0c768d
crosses      JTOUSDT   1m    ABSENT                                     
crosses      JTOUSDT   5m    ABSENT                                     
crosses      JTOUSDT   15m   ABSENT                                     
crosses      JTOUSDT   30m   ABSENT                                     
crosses      JTOUSDT   1h    ABSENT                                     
crosses      JTOUSDT   4h    ABSENT                                     
crosses      JTOUSDT   12h   ABSENT                                     
crosses      TAOUSDT   1m    ABSENT                                     
crosses      TAOUSDT   5m    ABSENT                                     
crosses      TAOUSDT   15m   ABSENT                                     
crosses      TAOUSDT   30m   ABSENT                                     
crosses      TAOUSDT   1h    ABSENT                                     
crosses      TAOUSDT   4h    ABSENT                                     
crosses      TAOUSDT   12h   ABSENT                                     
first-look   5a_event_ parquet PRESENT               2,484        31,234  093a3b7cfea271eb
first-look   5b_equiva parquet PRESENT                 108         7,548  3f1a2a0530a35ef9
first-look   5b_equiva parquet PRESENT                 324         5,884  09afed019f4d090d
first-look   5c_vult_o parquet PRESENT                  30        18,994  0ab405daf96bd8e2
first-look   5d1_fast_ parquet PRESENT                 270        20,157  c5fbff3ba9ecefd6
first-look   5d2_knot_ parquet PRESENT              10,684       464,407  d19857dda05da901
first-look   5d3_campa parquet PRESENT               6,571       448,846  c16782cd8559c225
first-look   5d3_campa parquet PRESENT                  30         8,443  b3ed3072d08fa141
first-look   TIER_E    json  PRESENT                               772  54d8cd23db37c97a
--------------------------------------------------------------------------------------------------------

COMPLETION GRID  (P = present+sha-verified, . = absent)

  emas
    asset          1m    5m   15m   30m    1h    4h   12h
    BTCUSDT         .     P     P     P     P     P     P
    ETHUSDT         .     P     P     P     P     P     P
    SOLUSDT         .     P     P     P     P     P     P
    NEARUSDT        .     P     P     P     P     P     P
    ZECUSDT         .     P     P     P     P     P     P
    JTOUSDT         .     .     .     .     .     .     .
    TAOUSDT         .     .     .     .     .     .     .

  ribbons
    asset          1m    5m   15m   30m    1h    4h   12h
    BTCUSDT         .     P     P     P     P     P     P
    ETHUSDT         .     P     P     P     P     P     P
    SOLUSDT         .     P     P     P     P     P     P
    NEARUSDT        .     P     P     P     P     P     P
    ZECUSDT         .     P     P     P     P     P     P
    JTOUSDT         .     .     .     .     .     .     .
    TAOUSDT         .     .     .     .     .     .     .

  crosses
    asset          1m    5m   15m   30m    1h    4h   12h
    BTCUSDT         .     P     P     P     P     P     P
    ETHUSDT         .     P     P     P     P     P     P
    SOLUSDT         .     P     P     P     P     P     P
    NEARUSDT        .     P     P     P     P     P     P
    ZECUSDT         .     P     P     P     P     P     P
    JTOUSDT         .     .     .     .     .     .     .
    TAOUSDT         .     .     .     .     .     .     .

SUMMARY
```

```
SUMMARY
  manifest artifacts pinned      100
  audit cells probed             157
    ABSENT              57
    PRESENT            100
  total pinned bytes             1,706,299,021

  PANEL core ABSENT cells: 15  -- stages ['crosses', 'emas', 'ribbons'], lenses ['1m']
  ANNEX (JTOUSDT, TAOUSDT): never built by V-ULT-1 -- the pins list them as budget-only.
    NAMED, not silently dropped; annex is out of scope for Part A and W-TB1.

  VERDICT: census-2B V-ULT-1 is COMPLETE on the panel for {5m,15m,30m,1h,4h,12h}.
           1m is the sole gap, on every core stage and every panel asset.

  wrote D:\Naiad\research_outputs\census2b\cen2b_completion_audit.parquet  rows=157  bytes=14,456
```

**COMPLETION GRID** (P = present + sha-verified, `.` = absent) — identical for `emas`, `ribbons` and
`crosses`, so it is printed once:

```
    asset          1m    5m   15m   30m    1h    4h   12h
    BTCUSDT         .     P     P     P     P     P     P
    ETHUSDT         .     P     P     P     P     P     P
    SOLUSDT         .     P     P     P     P     P     P
    NEARUSDT        .     P     P     P     P     P     P
    ZECUSDT         .     P     P     P     P     P     P
    JTOUSDT         .     .     .     .     .     .     .
    TAOUSDT         .     .     .     .     .     .     .
```

**VERDICT.** Census-2B V-ULT-1 is **COMPLETE on the panel across {5m, 15m, 30m, 1h, 4h, 12h}** —
15 cells × 3 core stages, 100 pinned artifacts, 0 STALE, 0 PINNED-MISSING, 1.71 GB, every sha
verified this session. The first-look stage is complete (9 tables). The feasibility matrix is
complete (630 cells).

**1m DEFERRED, named.** 1m is ABSENT on all three core stages for all five panel assets — 15 cells.
It is the sole panel gap. The budget did not clearly allow it after A-1..A-4: A-2 alone opens 103,153
windows across five lenses, and 1m would add ~3.65M bars per asset to a machine whose previous
V-ULT-1 run failed on 1m for RAM (LEDGER_APOLLO 2026-08-14a, fact 9). Per the contract's own
instruction — *"complete 1m ONLY if budget clearly allows after A-1..A-4; else print '1m DEFERRED,
named' and continue"* — **1m DEFERRED, named.** No table in this document reads 1m; nothing here is
affected by its absence beyond the lens list.

**ANNEX named.** JTOUSDT and TAOUSDT were never built by V-ULT-1; the manifest pins list them as
budget-only. They are out of scope for Part A and W-TB1 and are reported ABSENT rather than omitted
from the audit, so the 57 ABSENT cells reconcile exactly: 15 panel-1m + 42 annex (2 assets × 3 stages
× 7 lenses).

---

## 2 · A-1 — i-a REFUSALS ON THE NEW PAIRS

Grammar: ε=0.25, δ=0.75, k=10 — **ratified constants, unchanged**, both limbs. What changes is only
the *arguments*: census-2A and V-ULT-1 ran the grammar with `close` approaching a **band rail**; here
the approaching series is itself an EMA — the faster member of the pair — and the level is the
slower. A refusal is emitted with the side it approached **from**; the grammar forbids a sign change
of (series − level) between touch and veer, so the approach side is well defined, and an exact-zero
touch is settled by the confirm bar.

The pared within-SR set is **derived from `RIBBONS`** (middle member vs slow member of each band) and
then asserted equal to the contract's literal list, so the two statements cannot drift apart.
`9_12` is VETOed by name and is not in the set — asserted, not assumed.

| | 5m | 15m | 30m | 1h | total |
|---|---:|---:|---:|---:|---:|
| **A-1 refusals, all pairs, 5 assets** | 176,905 | 55,834 | 27,564 | 15,409 | **275,712** |

**Per-pair counts, all assets and lenses pooled** (`within_sr` = pared, `sr_median` = midline):

```
  pair         class              5m       15m       30m        1h       total
  12_26        within_sr      83,608    26,439    13,043     7,342     130,432
  89_127       within_sr          12         7         5         6          30
  316_423      within_sr           0         0         0         0           0
  889_1272     within_sr           0         0         0         0           0
  2618_3618    within_sr           0         0         0         0           0
  4618_5000    within_sr           0         0         0         0           0
  12_89        sr_median      83,703    26,077    12,584     7,001     129,365
  89_316       sr_median       9,006     3,010     1,689       984      14,689
  316_889      sr_median         557       299       242        75       1,173
  889_2618     sr_median          19         2         1         1          23
  2618_4618    sr_median           0         0         0         0           0
```

### 2.1 · FINDING, REPORTED NOT FIXED — the kiss grammar is INERT on slow line-vs-line pairs

Five pairs return **exactly zero** refusals at every lens. A zero that is not explained cannot be
told apart from a bug, and the constants that would explain it are VETO and may not be moved to find
out. So the reach was measured instead — `n_touch` = bars inside the approach limb, `max_veer` =
the largest |spread|/ATR reached within k=10 bars **of a touch**, over the entire history:

```
  pair         lens     n_touch  med_veer  max_veer  p_veer_ge   verdict
  12_26        5m       996,854    0.3990    2.6416     0.1335   fires
  12_89        5m       288,220    0.7673    5.0511     0.5154   fires
  89_316       5m       185,048    0.2974    1.8813     0.0617   fires
  316_889      5m       114,563    0.1990    1.0868     0.0017   fires, barely
  889_2618     5m        61,417    0.1729    0.9605     0.0002   fires, barely
  89_127       5m       821,494    0.1773    0.9481     0.0000   INERT
  316_423      5m       495,590    0.1523    0.6112     0.0000   INERT — max < delta
  889_1272     5m       228,923    0.1494    0.5469     0.0000   INERT — max < delta
  2618_3618    5m       130,641    0.1392    0.4183     0.0000   INERT — max < delta
  4618_5000    5m       381,820    0.1400    0.4225     0.0000   INERT — max < delta
  2618_4618    5m        68,094    0.1429    0.5143     0.0000   INERT — max < delta
```

The zero pairs are **not** "these lines never meet" — they meet constantly (61k–820k touches each).
For five of them the **maximum** separation reachable within ten bars, across the whole panel history,
is **below the 0.75 ATR veer threshold** — 0.61, 0.55, 0.42, 0.42, 0.51 ATR. The event is not rare; it
is **impossible**. The kiss grammar is calibrated for price-against-a-rail and for fast lines; the
separation of two slow EMAs cannot move 0.75 ATR in 10 bars, because that is what being a slow EMA
means. **The constants are VETO by name and were NOT changed.** Whether the grammar should be
scale-matched per pair is an operator ruling, not an edit. It is the same shape of defect V-ULT-1
reported for `k=20` and UH `state`, in a different place.

`89_127` is the interesting boundary case: 821,494 touches, max reach 0.948 ATR — the threshold *is*
attainable, and it is cleared 30 times in 275,712 refusals. The grammar is not quite dead there; it
is at the edge of its resolution.

**F-A1 PASS** — 3/3 hand-verified refusals (touch, veer, gap, no-sign-change, limb, all recomputed
from first principles), determinism re-run **hash-identical**.

---

## 3 · A-2 — BR ARMED-WINDOW LEDGER v2 · **the headline**

arming = close-confirmed `12_89` cross, both directions · window = `[t0, next counter-12_89)`,
half-open, **no W_max cap** · trigger = same-direction `12_26` cross in-window · fate =
{TRIGGERED, ABORTED}, disjoint and exhaustive.

**103,153 windows** across 5 assets × {5m, 15m, 30m, 1h, 4h}: 42,287 TRIGGERED, 60,866 ABORTED.
Up/down is balanced to within one window overall — 51,573 up, 51,580 down.

**Stamps AT the arming bar**, every one as-of t0: displacement |close−e89|/ATR · all six SR
states/orients/knots/widths · fan_age per SR · nearest sweep within 24h (from A-4) · refusal density
trailing 24h (from A-1) · in-window trigger-taxonomy counts for all eleven pared pairs.

**Curtain, enforced not asserted.** A sweep counts toward the 24h lookback only if its **reclaim**
bar is at or before t0; a refusal only if its **confirm** bar is. Both events are unknowable at their
opening bar — that is what makes them sweeps and refusals rather than pokes and touches — so keying
the lookback on the opening bar would be a curtain breach dressed as a lookback. Verified
independently on ETHUSDT 1h: 1,022 windows, 0 stamp mismatches, 0 stamps sourced from a future bar.

A-1 and A-4 are pinned to four lenses; A-2 runs on five. On 4h the stamp sources are therefore
computed **in memory** from the same functions rather than read from disk, so A-2's stamp is complete
on every lens it is contracted for without widening A-1's or A-4's ratified deliverable by a lens
nobody ratified.

### 3.1 · The trigger interval — the contract's reading, with the precedent printed beside it

The contract pins the window as `[t0, counter)` — **closed at t0** — and the fate on "the first 12_26
trigger in-window". So a `12_26` on the arming bar itself is in-window and counts. census-2A v1 used
`(t, close]`, strictly after, so that a trigger could never share a bar with its own arming. The
contract's words govern; the precedent is kept as a second, explicitly-named column, because the two
readings differ on **6.33% of all windows** and a reader must be able to see which one a number came
from.

```
  lens     windows  TRIG(contract)  TRIG(strict)  on-arm-bar    delta
  5m        66,137          26,944        22,660       6,175    4,284
  15m       20,914           8,695         7,389       1,897    1,306
  30m       10,102           4,135         3,552         847      583
  1h         4,884           2,032         1,736         423      296
  4h         1,116             481           420          96       61
  ALL      103,153          42,287        35,757       9,438    6,530   (6.33% of all windows)
```

A same-bar trigger makes `trg_*` an **alias** of `arm_*` for that row — the two anchors are the same
bar. That is why the strict column exists, and why the trigger-anchored H100 median below is printed
a **third** time on the strict subset.

### 3.2 · The toll line, printed first because it decides how to read everything after it

10 bps round trip in ATR units, measured on **each cell's own armings** (census-2A note m8: the toll
must be measured where the returns are normalised, and armings occur at compressed ATR):

```
  asset            5m      15m      30m       1h       4h
  BTCUSDT      0.5869   0.3060   0.2023   0.1342   0.0658
  ETHUSDT      0.4274   0.2218   0.1526   0.1029   0.0517
  NEARUSDT     0.2350   0.1260   0.0878   0.0612   0.0295
  SOLUSDT      0.2778   0.1503   0.1040   0.0724   0.0378
  ZECUSDT      0.2666   0.1448   0.1003   0.0699   0.0337
```

### 3.3 · Fate × direction, R-1 at BOTH anchors (I6), all five lenses

I6 reads *"rulers arrival/trigger-anchored … the other lens always printed"*. Both anchors are
computed and both are printed for every row. `trgH100(str)` is the trigger-anchored H100 with the
same-bar rows removed. H20 on 4h is INFEASIBLE (1h40m is shorter than one 4h bar) and emits NaN —
**never substituted with one bar**.

```
  lens  fate       dir        n  arm_termH20  arm_termH100  trg_termH20  trg_termH100  trgH100(str)  med_lag  med_disp
  5m    TRIGGERED  up    13,615       0.8626        1.8208      -0.1531       -0.1933       -0.1530      4.0     1.224
  5m    TRIGGERED  down  13,329       0.8127        1.6685      -0.2191       -0.3346       -0.3173      5.0     1.221
  5m    ABORTED    up    19,454      -0.7570       -1.2220           --            --            --       --     1.086
  5m    ABORTED    down  19,739      -0.8421       -1.3134           --            --            --       --     1.088
  15m   TRIGGERED  up     4,393       0.4280        1.1106      -0.1104       -0.1994       -0.2437      5.0     1.181
  15m   TRIGGERED  down   4,302       0.3817        1.0059      -0.1336       -0.2819       -0.2850      6.0     1.233
  15m   ABORTED    up     6,065      -0.4380       -0.8904           --            --            --       --     1.045
  15m   ABORTED    down   6,154      -0.5065       -0.9390           --            --            --       --     1.051
  30m   TRIGGERED  up     2,095       0.1813        0.8705      -0.0637        0.0071       -0.0512      7.0     1.256
  30m   TRIGGERED  down   2,040       0.2159        0.8489      -0.0626       -0.0829       -0.0934      6.0     1.237
  30m   ABORTED    up     2,957      -0.2654       -0.7485           --            --            --       --     1.057
  30m   ABORTED    down   3,010      -0.2752       -0.5659           --            --            --       --     1.032
  1h    TRIGGERED  up     1,010       0.1231        0.5170      -0.0325        0.1361        0.1628      7.5     1.264
  1h    TRIGGERED  down   1,022       0.1245        0.4395      -0.0199       -0.0024        0.0000      9.0     1.246
  1h    ABORTED    up     1,433      -0.1532       -0.3485           --            --            --       --     1.063
  1h    ABORTED    down   1,419      -0.2060       -0.3674           --            --            --       --     1.075
  4h    TRIGGERED  up       232           --        0.2357           --        0.0574        0.0714     16.5     1.396
  4h    TRIGGERED  down     249           --        0.2164           --        0.0225       -0.0282      6.0     1.240
  4h    ABORTED    up       325           --       -0.1231           --            --            --       --     1.244
  4h    ABORTED    down     310           --       -0.0873           --            --            --       --     1.067
```

### 3.4 · What this table says — and the half of it that is circular

**The arming-anchored split is spectacular and is not tradeable.** +1.82 ATR at H100 for TRIGGERED
against −1.22 for ABORTED on 5m is a **fate-conditioned** comparison: fate is decided by what happens
*inside* the window, after the arming. Sorting armings by whether they later triggered and then
measuring forward from the arming is circular by construction. It is printed because the contract
asks for it and because it is the correct description of a partition — but it is not a statement any
decision at t0 could act on, and no reading of it as one is supported here.

**The curtain-clean anchor is the trigger, and it is negative.** At the only instant a decision could
be taken — the first `12_26` trigger — the median forward R-1 is **negative at both horizons on 5m,
15m and 30m**, and within noise of zero on 1h and 4h. The strict column, which removes every row
where the trigger and the arming share a bar, says the same thing and in two places says it more
strongly (−0.153/−0.317 on 5m; −0.244/−0.285 on 15m).

**The trigger lag is bimodal, and that is the mechanism.** Under the contract's reading the median lag
is 4–9 bars, but the quartiles on BTC 5m are p25 = 1, p50 = 5, **p75 = 51**: one population of
triggers fires almost immediately with the arming, and a second fires tens of bars later. Restricted
to the strict subset the median is 30. The structural reason is that e12 crosses e26 *before* it
crosses e89, so a `12_26` that arrives after a `12_89` arming is either the same impulse (lag 0–2) or
a **re-entry after a pullback** (lag 30+). Neither is a confirmation of the arming, and by either
arrival the displacement — median 1.22–1.40 ATR **already at the arming bar** — has happened.

Then the toll is charged: 0.28 ATR median on 5m against a median trigger-anchored outcome of −0.19.

Nothing is registered. This is Tier-E, the trigger definition is the contract's own, pinned by name,
and one measurement on one ruler at two horizons is not a result about the operator's system.

**F-A2 PASS** — (a) 0 overlapping windows across 25 cells × 2 directions; (b) arming counts reconcile
to the A-0 cross artifact on every cell, with the 4 suppressed re-arms read from the run's **own**
stats table rather than derived as (crosses − windows), which would have made the identity true by
algebra and proved nothing; (c) one TRIGGERED window hand-unpacked per lens — arming cross, trigger
cross, displacement and ordering all recomputed from the EMAs.

> **The 4 suppressed re-arms are real and worth a line.** A same-direction `12_89` cross can fire
> twice with no counter-cross between when the two lines touch at exact float equality: `crossover`
> needs `a <= b` on the prior bar, and `a == b` satisfies it without a `crossunder` ever firing. Four
> such cases exist in 103,157 crosses. They are suppressed as re-arms inside a still-open window,
> counted, and named — left in, they would have made the ledger's own disjointness claim false.

---

## 4 · A-3 — TRANSITION LEDGER (KNOT episodes + FAN births)

knot episode = a contiguous run of `SR_knot == 1`; a `KN_NA` bar **breaks** a run, because cold data
is not "no knot". exit direction = the sign of the first fully-ordered bar at or after the exit. fan
birth = the onset of a full-order run; a bull→bear flip with no `mixed` bar between is **two** fans,
not one. Forward R-1 at H20/H100 from the knot **exit** bar and the fan **onset** bar; an episode
whose exit direction never resolves carries NaN rather than a zero sign, because R-1 on a zero sign
is identically zero and would read as a measured flat outcome.

**262,086 knot episodes · 318,427 fan births** across 5 assets × {5m, 15m, 30m, 1h} × 6 SRs.

```
  SR          knots       fans  med_knot_bars  med_fan_bars
  FAST      189,580    265,565           10.0          13.0
  M          39,139     37,730           27.0          93.0
  MH         16,487      9,828           42.0         363.0
  H           6,196      3,520           47.0         982.0
  VH          2,630      1,178           27.0       2,864.5
  UH          8,054        606            9.0       5,691.5
```

The monotone march across the bands is the whole content of the table and it is a fact about EMA
lengths rather than about the tape: a UH fan, once born, holds its order for a median of 5,691 bars
against FAST's 13. UH is the exception to the knot column — 8,054 episodes with a median duration of
**9 bars**, shorter than FAST's 10 — which is the `RIBBON_C`/`k=20` scale mismatch V-ULT-1 already
reported, seen from the episode side: the UH band's width crosses 0.5 ATR briefly and often rather
than settling.

**`fan_age` at each bar** is carried as `(onset, length)` and reconstituted exactly by
`fan_age_series()` wherever it is consumed — it is stamped at every A-2 arming and at every W-TB1
capture bar. It is not stored as a standalone per-bar table: that would be one int32 column per SR per
lens per asset, on the order of 10^8 rows, to carry information the two stored numbers already
determine. **Named here as a storage decision, not a measurement one.**

**F-A3 PASS** — (a) 0 overlapping episodes across 20 cells × 6 SRs × 2 episode types;
(b) 2 hand-verified transitions per lens, knot boundaries and fan onsets recomputed from the ribbon
codes.

---

## 5 · A-4 — SPRING / UPTHRUST EVENT STREAM

penetration of the prior-96-bar extreme **[VETO N=96]**, strictly prior (bar *i* excluded from its own
reference, or every new extreme would be its own reference and nothing could ever penetrate), then
close back inside within 3 bars **[VETO]**. Episodes are greedy and non-overlapping per side: once a
spring fires at *i* and reclaims at *j*, the scan resumes at *j*+1. Emitting every qualifying bar
would triple-count a single three-bar spring and make F-A4's disjointness assertion unprovable
because it would be false. R-1 is anchored at the **reclaim** bar — the bar the event completes and
the first bar at which it is knowable.

**227,268 events · 106,566 springs · 120,702 upthrusts.**

```
  lens       spring   upthrust      total   pen bars   absorbed  no-reclaim  sum ok
  5m         68,003     74,467    142,470    232,171     31,237      58,464    True
  15m        22,067     25,721     47,788     76,255      9,646      18,821    True
  30m        11,078     13,431     24,509     38,892      4,666       9,717    True
  1h          5,418      7,083     12,501     19,903      2,361       5,041    True
```

**The penetration census reconciles exactly, and it is printed because a greedy scan that reports
only its survivors is indistinguishable from one that drops data.** `pen bars` are all bars that
penetrated the prior-96 extreme; `absorbed` are penetration bars falling inside an already-emitted
episode, folded into it rather than discarded; `no-reclaim` never closed back inside within 3 bars.
**emitted + absorbed + no-reclaim ≡ pen bars is asserted per lens**, and holds on all four.

**A quarter of all penetrations never reclaim** — 58,464 of 232,171 on 5m (25.2%), and the share is
stable across lenses. Those are the breakouts that kept going; A-4 by construction is a census of the
ones that failed, and the failure rate is now beside it instead of implied.

Median reclaim lag is **0 bars** at every lens and asset — the overwhelming majority of sweeps poke
through the prior extreme and close back inside on the *same* bar. Median depth is 0.35–0.46 ATR.
Upthrusts outnumber springs 1.13:1 on this panel across every lens.

**No `NOMENCLATURE_MAP` exists.** The W-TB1 block cites "spring/upthrust per NOMENCLATURE_MAP row
1/2". An exhaustive search of the estate — including ignored paths, `_reviewer_box/`, and all of D: —
finds no artifact of that name, and no numbered table pairing row 1 with spring and row 2 with
upthrust. What exists is prose (`SS_SYSTEM_SYNTHESIS_2026-08-06.md` §3.6, the nomenclature *programme*,
opened and explicitly not urgent) and definitions in the knowledge base
(`Level_Selection_Deep_Dive_Wyckoff_AMT_CCL.md` §1.1/§1.5), neither of which pins a lookback or a
reclaim count. **Part A supplies the pinned definition itself** — N=96 and 3 bars, both [VETO] in this
contract — so A-4 is fully specified without the map, and the BRIDGE resolves W-TB1's citation to
A-4's definition. Recorded as a dangling citation, not repaired: writing the map is a nomenclature
ruling, not a builder's edit.

For the record, the nearest pinned cousin in committed code is census-2A's prior-extreme sweep at
`w = 60` bars on the 4h lens (`census2a_program.py:2787`). **96 ≠ 60**, both are pinned, and they are
different objects on different lenses. Neither was changed.

**F-A4 PASS** — 3/3 hand-verified sweeps (prior-96 reference, penetration, reclaim, lag, all
recomputed from raw OHLC), 0 overlapping episodes across 20 cells × 2 sides.

---

## 6 · THE RULER — F-A0R, and why it needed a fixture

Part A **restates** census-2A's `outcome_block` because a Part-A table interleaves both directions in
one call and the original takes a single scalar `up`. A restatement that drifts from the ruler it
claims to be is worse than no ruler, so it is compared against the original on a real series, element
for element, both directions, at both horizons, across `terminal`, `mfe` and `mae`:

```
  5m   n=420 (120 at the series tail, clamped path) x 2 directions x 2 horizons x 3 series  identical=True
  15m  n=420 (120 at the series tail, clamped path) x 2 directions x 2 horizons x 3 series  identical=True
  30m  n=420 (120 at the series tail, clamped path) x 2 directions x 2 horizons x 3 series  identical=True
  1h   n=420 (120 at the series tail, clamped path) x 2 directions x 2 horizons x 3 series  identical=True
  4h   n=420 (120 at the series tail, clamped path) x 2 directions x 2 horizons x 3 series  identical=True   [['H20'] INFEASIBLE]
  F-A0R PASS -- element-for-element identical on every A-2 lens, both directions,
  interior and clamped-tail anchors, including the INFEASIBLE 4h/H20 branch
```

The sample deliberately includes **120 anchors at the series tail** on every lens, because that is the
only place `r1_block`'s clamped path (`end = min(i+bars, n-1)`) is exercised at all — and the 4h lens,
because that is the only place the INFEASIBLE branch is. A first draft sampled one lens's interior and
would have passed while both branches went untested (F-25). The identity was also reproduced
independently against a naive per-anchor loop on NEARUSDT 30m: 3 tail rows at H20, 17 at H100,
all identical to the bit.

**The horizon realisation, printed before every outcome table.** H20 and H100 are DURATION-fixed —
20 and 100 *five-minute equivalents*, 1h40m and 8h20m — not bar counts. Reading them as bar counts is
the paste-1 defect R-1 exists to remove; it would make `H100` mean 8h20m on 5m and 4 days 4 hours on
1h, i.e. a different horizon per lens under one label.

```
  lens                            H20                        H100
  5m       20 bar(s) =  1.67h  r=1.00 100 bar(s) =  8.33h  r=1.00
  15m       7 bar(s) =  1.75h  r=1.05  33 bar(s) =  8.25h  r=0.99
  30m       3 bar(s) =  1.50h  r=0.90  17 bar(s) =  8.50h  r=1.02
  1h        2 bar(s) =  2.00h  r=1.20   8 bar(s) =  8.00h  r=0.96
  4h              INFEASIBLE -> NaN   2 bar(s) =  8.00h  r=0.96
```

`('4h', 'H20')` is infeasible and emits NaN. It is **never** substituted with one bar — which is why
the 4h rows of §3.2 are blank in the H20 columns rather than zero.

---

## 7 · W-TB1 — COHORT AND MATCHING TABLE

`gross_R` is the ruler declared in `census2a_program.py:2271`; its stored column is
`cen5_campaigns.ride_R`, and `outcome_sign` is literally `sign(ride_R)` — both are stated so the
cohort cannot be read as depending on a derived label. Verified this run:
`outcome_sign == (gross_R > 0)` is **True** for every panel row.

```
resolved book, panel only            6,643 campaigns
winners (gross_R > 0)                  814     <- the contract expects ~814
loser pool                           5,829
matched pairs                          814
unmatched winners                        0
match gap (days)  median 2.5  p90 11.8  max 58.4
WF1 exit rows read                   7,094
cohort rows                          1,628   with t_exit 1,628   missing 0
cen5 ts_ms == WF1 ts_open_epoch*1000  1,628 / 1,628
```

**814 exactly**, not approximately. The cohort's `gross_R` is **mean +9.4458, median +2.1422** —
byte-for-byte the winner figures in `census2a_run_log.txt:1561` and the F1 line of
`CENSUS2A_CLOSEOUT_2026-08-12.md`. 814/6,643 = **12.25%**, the 12.3% tail the commission means.
(For precision: the F1 loser figure, median −1.0415, is over the **full** 5,829-strong loser pool.
The 814 **matched** controls have a median of −1.0332 — a different, smaller population, and the two
numbers should not be quoted as if they were the same one.)

**The exit timestamp exists after all.** Every downstream census-2A and V-ULT-1 table says the exit
side cannot be computed — `cen4_book` carries `ts_open`/`ts_ms` (both the *entry*) and
`cen5_campaigns` carries no exit column (`census2b_firstlook.py:709-718`). It is a **parquet-column
gap, not a data gap**: `stage_cen5` computes `t1 = t0 + hold_s*1000` at `census2a_program.py:2332`
and simply does not persist it. W-TB1 reads `ts_close`/`hold_s` from the WF1 source JSONs
(`_reviewer_box/wf1/*USDT_*.json`) — no simulation, no inference — and gets t_exit for **all 1,628**
campaigns. The named gap is closed by reading, not by modelling.

**Matching table** — 1:1, nearest-neighbour by entry ts within an **exact** stratum of
(asset, direction, entry-quarter, size_r). Winners are processed in (ts_ms, tranche_id) order and the
nearest unused loser wins; no RNG is involved anywhere, so the control set is a function of the book
alone.

```
  asset                    dir                      size_r
  level      winners control  level   winners control  level   winners control
  BTCUSDT        172     172  long        400     400  0.25        329     329
  ETHUSDT        185     185  short       414     414  0.5         485     485
  NEARUSDT       143     143
  SOLUSDT        156     156  quarter: 19 levels, per-quarter difference max 0
  ZECUSDT        158     158
```

**F-W1 PASS** — 814 controls drawn, 814 distinct (no reuse); 0 winner/control overlap; max |share
difference| = **0.0000** on all four matched keys.

> **Honest reading of F-W1b.** Because every stratum had at least as many losers as winners, the
> match is *exact* on all four keys and the marginals are equal by construction, not by luck. The
> "within 10%" test therefore cannot fail here — it is a **vacuous pass**. It is reported as passing
> because it did, and flagged as vacuous because it is. The non-vacuous part of F-W1 is the no-reuse
> and no-overlap check, which could have failed and did not.

---

## 8 · W-TB1 — CAPTURE INVENTORY

t0 = birth, ±72h, lenses {5m, 15m, 30m, 1h}; exit side t_exit ±24h, labelled EXIT-ANATOMY.

**(a) BR STATE SERIES** — all 18 EMA values (feasible cells; NaN before warm) + their ranks + BR
dispersion in ATR + per-SR width/state/orientation/knot + per-SR `fan_age` + SR-order disorder + the
BR's own state/orientation/knot. Downsampled to **state-change points ∪ hourly spine**, with t0 and
t_exit always kept.

**(b) EVENT TAPE** — within-SR and SR-median crosses · A-1 refusals, both limbs, timestamped at
**confirm** · A-2 window arm/trigger/close · A-3 knot exits and fan births · A-4 sweeps, timestamped
at **reclaim** · range-verdict state changes. The BRIDGE is satisfied: A-1, A-2, A-3 and A-4 events
are all **first-class tape rows**, so the motif alphabet below is the full grammar rather than half
of it.

**(c) EXIT-SIDE** — the same tape and state around t_exit ±24h, carried as an `exit_anatomy` flag on
top of the BEFORE/AFTER split rather than as a separate row set, so a bar that is in both windows is
stored once and labelled twice.

```
  asset     lens  campaigns   state rows   tape rows   state MB   tape MB
  BTCUSDT   5m           344      300,495     335,664       44.4       6.1
  BTCUSDT   15m          344      123,786     108,077       18.0       1.9
  BTCUSDT   30m          344       79,324      53,633       10.7       1.0
  BTCUSDT   1h           344       55,688      27,220        6.3       0.5
  ETHUSDT   5m           370      319,603     356,284       46.1       6.3
  ETHUSDT   15m          370      131,488     115,183       18.8       2.0
  ETHUSDT   30m          370       85,355      57,301       11.2       1.0
  ETHUSDT   1h           370       60,157      28,662        6.4       0.5
  SOLUSDT   5m           312      269,144     302,760       38.9       5.4
  SOLUSDT   15m          312      112,124      97,655       15.7       1.7
  SOLUSDT   30m          312       72,415      47,977        9.5       0.8
  SOLUSDT   1h           312       50,985      25,255        5.4       0.4
  NEARUSDT  5m           286      245,469     275,859       34.0       4.9
  NEARUSDT  15m          286      101,749      89,419       13.9       1.6
  NEARUSDT  30m          286       65,622      44,260        8.4       0.8
  NEARUSDT  1h           286       46,201      22,977        4.7       0.4
  ZECUSDT   5m           316      280,254     318,574       41.1       5.8
  ZECUSDT   15m          316      115,038     104,301       16.5       1.9
  ZECUSDT   30m          316       73,986      51,361        9.9       0.9
  ZECUSDT   1h           316       51,808      26,322        5.7       0.5
  TOTAL                1,628    2,640,691   2,488,744   410,199,635 B (0.41 GB)
```

F-KEY asserted on all 20 state cells `(ckey, lens, ts_ms)` and all 20 tape cells
`(ckey, lens, ts_ms, src_ts_ms, kind, token)` — **40 assertions, dup = 0 on every one.**

**Curtain discipline, mechanically.** Every state row and every tape row carries `side ∈ {BEFORE,
AFTER}` plus an independent `exit_anatomy` boolean. A row from the exit window that precedes t0
(possible when the hold is under 24h) is correctly `BEFORE` *and* `exit_anatomy`. The +72h side would
have to be read past **two** labels to be mistaken for entry evidence.

The split is on **knowability, not bar-open**: a bar's state and every close-confirmed event on it
become knowable at that bar's CLOSE, so `side = (bar_close <= t0)`. Splitting on the open stamped a
1h bar opening at 10:30 as BEFORE an 11:00 birth — a leak of up to one bar (F-18). `knowable_ts_ms`
is persisted beside `ts_ms`, and every as-of lookup, every `rel_h` and the pooled cross-lens motif
ordering read it. Verified independently on 634k tape rows: 0 label violations, 0 BEFORE rows
carrying a timestamp at or after t0.

**One reading declared rather than assumed: "SR-order entropy".** The contract names it; no
definition of that name is pinned anywhere in the estate. It is implemented as the **normalised
inversion count of the six SR medians against the bull order** — 0 = perfectly bull-ordered,
1 = perfectly bear-ordered, 0.5 = maximally scrambled — and stored as `sr_order_disorder` under that
explicit definition rather than under a borrowed word. Median across the cohort sits at 0.467–0.600
at every stage of W-A, i.e. the six medians are near-maximally scrambled essentially always.

---

## 9 · W-A — STATION OCCUPANCY · the six-stage kit, photographed

BR state at t−72h, t−24h, t−4h, t0, t+24h, t_exit, winners vs control. The state series stores every
bar at which any code changes, so an as-of lookup at an arbitrary instant is exact rather than
interpolated — and the lookup is on **knowability** (the last bar *closed* by that instant), not on
bar-open. `disp` = BR width in ATR; `disord` = SR-order disorder.

**CURTAIN: t−72h / t−24h / t−4h are the only columns that could ever be entry evidence. t+24h and
t_exit are ANATOMY.** Two of the six stages are printed here precisely so the split is visible.

Two lenses are reproduced below; the full four-lens table is in the run transcript on D:.

```
  LENS 5m   winners n=814  control n=814
    stage    coh        compr    flat  expand |    bull   mixed    bear |   knot%    disp  disord
    t-72h    winner     70.8%    1.0%   28.2% |   14.4%   74.4%   11.2% |    0.0%  19.668   0.467
    t-72h    control    71.1%    1.5%   27.4% |   16.0%   72.5%   11.6% |    0.0%  20.231   0.400
    t-24h    winner     70.2%    1.0%   28.8% |   10.7%   80.3%    9.0% |    0.0%  17.330   0.467
    t-24h    control    73.5%    0.5%   26.0% |    8.4%   83.6%    8.0% |    0.0%  18.698   0.533
    t-4h     winner     67.8%    1.3%   30.9% |    8.8%   84.7%    6.5% |    0.0%  15.983   0.467
    t-4h     control    70.2%    1.4%   28.4% |    6.4%   87.8%    5.8% |    0.0%  16.906   0.467
    t0       winner     92.0%    1.1%    6.8% |    7.0%   85.3%    7.7% |    0.0%  15.028   0.467
    t0       control    92.7%    0.8%    6.5% |    5.6%   89.0%    5.4% |    0.0%  15.399   0.467
    t+24h    winner     59.1%    1.6%   39.3% |   19.2%   63.7%   17.1% |    0.0%  20.608   0.533
    t+24h    control    70.5%    1.5%   28.0% |   14.3%   74.3%   11.4% |    0.0%  17.032   0.467
    t_exit   winner     86.3%    0.1%   13.6% |    1.1%   97.5%    1.4% |    0.0%  15.171   0.467
    t_exit   control    92.5%    1.4%    6.2% |    2.8%   95.9%    1.4% |    0.0%  14.024   0.467

  LENS 1h   winners n=814  control n=814
    stage    coh        compr    flat  expand |    bull   mixed    bear |   knot%    disp  disord
    t-72h    winner     70.6%    0.5%   28.9% |   12.4%   74.1%   13.5% |    0.0%  26.036   0.600
    t-72h    control    71.1%    1.6%   27.2% |   13.6%   70.2%   16.2% |    0.0%  26.160   0.600
    t-24h    winner     76.3%    1.2%   22.5% |   11.7%   71.8%   16.5% |    0.0%  26.212   0.600
    t-24h    control    79.3%    1.2%   19.5% |   10.2%   80.1%    9.7% |    0.0%  25.725   0.600
    t-4h     winner     79.4%    1.4%   19.2% |   10.6%   75.9%   13.4% |    0.0%  24.410   0.600
    t-4h     control    82.9%    0.7%   16.4% |    9.9%   76.0%   14.0% |    0.0%  24.199   0.600
    t0       winner     78.0%    1.2%   20.8% |   11.3%   75.5%   13.2% |    0.0%  23.625   0.600
    t0       control    80.3%    0.7%   19.0% |   11.4%   73.5%   15.1% |    0.0%  24.508   0.600
    t+24h    winner     54.2%    0.9%   44.9% |   12.1%   71.9%   16.0% |    0.0%  24.307   0.600
    t+24h    control    70.3%    3.5%   26.2% |   10.8%   75.0%   14.2% |    0.0%  25.243   0.600
    t_exit   winner     97.5%    0.0%    2.5% |   12.4%   72.3%   15.2% |    0.0%  25.418   0.600
    t_exit   control    85.0%    1.4%   13.6% |   10.6%   75.2%   14.2% |    0.0%  25.977   0.600
```

Three things the photograph shows, all descriptive:

1. **The BEFORE columns barely separate the cohorts.** At t−72h, t−24h and t−4h the winner and control
   distributions sit within a few points of each other on every axis and every lens. Whatever makes a
   winner a winner is not visible in the BR state before birth, on this ruler.
2. **Births cluster in compression, for both cohorts alike.** On 5m the compressing share jumps from
   68% at t−4h to **92%** at t0 — for winners *and* controls, to within 0.7 points. That is a property
   of the entry machinery, not of the tail.
3. **The separation is on the AFTER side, which is anatomy.** At t+24h winners are expanding 39.3% vs
   28.0% (5m) and 44.9% vs 26.2% (1h); at t_exit winners are 86–97% compressing. Winners are the
   campaigns that were still alive to be measured in expansion 24h later. **This is not entry
   evidence and is not offered as any.**

The population behind each cell is the campaigns whose BR is fully warm at that instant — 1,586 of
1,628 at t−72h on 5m, 851 on 1h, where the 1h shortfall is e4618/e5000 needing ~2 years to warm. An
unwarmed BR is `n/a` and is excluded from the percentages rather than counted as `mixed`.

> **One reading of the contract, declared.** The block reads *"BR state distribution at t-72h, t-24h,
> t-4h, t0, t+24h, t_exit (the six-stage kit, photographed)"*. The six instants are taken as the six
> stages, because the contract enumerates them in the same sentence. There is a *different* six-stage
> kit in the estate — DIONYSUS's S1 WATCHLIST → S6 GRACEFUL EXIT — and if the apposition was meant to
> invoke that, W-A answers a different question from the one asked. Flagged, not guessed at.

---

## 10 · W-B — SEQUENTIAL MOTIFS · the full selection surface

Ordered event k-grams, k ≤ 4, over the 24h before t0, **pooled across the four lenses** and ordered by
**knowability** (bar close), not bar open — the SEQ frames are about multi-timeframe sequencing, and
on a pooled tape a 1h event that opens at 10:00 is *not* knowable before a 5m event that closes at
10:05. 1,628 of 1,628 campaigns carry a non-empty pre-tape; **median 230 events per campaign**, p90
282, max 411, 378,965 events in total.

**The three SEQ frames** are the ratified three (`seq8_views.py:30-35`, SEQ-2 ruling D — all three
counted, none primary): `absolute` (literal lens labels), `gov_relative` (ladder steps from the
k-gram's *first* event), `tier` (TIER_GRAMMAR labels). **The motif alphabet is the BRIDGE's full
grammar**: within-SR crosses at **pair** level (all 18 pairs, not collapsed to the family), SR-median
crosses, A-1 refusals on both limbs, A-2 window arm/trigger/close, A-3 knot **entries** and exits and
fan births, A-4 sweeps.

```
FULL MOTIF COUNT (all three frames, k=1..4)  m_full = 743,516
    absolute       distinct motifs    288,857   usable (>=8 both sides)    7,113
    gov_relative   distinct motifs    262,219   usable (>=8 both sides)    6,858
    tier           distinct motifs    192,440   usable (>=8 both sides)    7,313

I11 SELECTION GUARD -- max-statistic permutation, 2000 permutations, shared across frames
    frame            m_guard   obs max  null p95   p_sel        q/m  admissible
    absolute           7,113   0.08477   0.08722  0.0735   1.41e-05  False
    gov_relative       6,858   0.07248   0.08477  0.3213   1.46e-05  False
    tier               7,313   0.07494   0.08722  0.3063   1.37e-05  False
```

**This is a clean null, and it is the point of the guard.** The largest winners-vs-control gap any
motif achieves in the `absolute` frame is 0.08477. The gap the *largest-of-7,113* reaches when the
labels are meaningless is 0.08722 — the observed statistic sits **below** its own null 95th
percentile, in all three frames.

> **The `admissible` column is structurally False and must not be read as "tested and rejected".**
> With 2,000 permutations the smallest attainable p_sel is 1/2001 = 4.998×10⁻⁴, while the BH bar q/m
> is ≈4.0×10⁻⁷ — **the bar sits 1,239× below the permutation floor**. No motif could clear it at this
> permutation count whatever the data said. The informative comparison is obs-vs-null above, and that
> one is genuinely uninformative-of-signal: the maximum does not reach its own null p95.

```
  frame=absolute (usable m=7,113)      k   n_w   n_c  share_w  share_c     diff  motif
                                       1   610   679   0.7494   0.8342  -0.0848  5m:X62_89+
                                       1   474   413   0.5823   0.5074  +0.0749  1h:FFAST-
                                       1   266   206   0.3268   0.2531  +0.0737  5m:M316_889+
                                       1   278   220   0.3415   0.2703  +0.0713  5m:KIH
  frame=gov_relative (usable m=6,858)  1   326   267   0.4005   0.3280  +0.0725  0:M316_889+
                                       2   424   372   0.5209   0.4570  +0.0639  0:X89_127->0:FM-
                                       2   157   207   0.1929   0.2543  -0.0614  0:KFAST->-1:Sspring
  frame=tier (usable m=7,313)          1   474   413   0.5823   0.5074  +0.0749  STAIR:FFAST-
                                       1   674   731   0.8280   0.8980  -0.0700  FAST:X62_89+
                                       1   319   263   0.3919   0.3231  +0.0688  FAST:M316_889+

  k-gram survival: distinct / usable
     k        absolute          gov_relative                 tier
     1       361 /   282        95 /    90          178 /   143
     2    21,737 / 2,617    14,896 / 2,250        8,847 / 1,823
     3    91,639 / 2,707    80,769 / 2,829       53,158 / 3,069
     4   175,120 / 1,507   166,459 / 1,689      130,257 / 2,278
```

The usable column collapsing as k grows **is** a result: a 4-gram over this grammar is very nearly a
campaign fingerprint — 175,120 distinct 4-grams over 1,628 campaigns — so almost none recurs in eight
winners *and* eight controls. That is a statement about the alphabet's resolution, not about the tail.

**m for the probe ledger = 743,516.** Under the ledger's own rule (*"extraction, description, and
display are m = 0"*) this probe could have been charged nothing: no row is kept on the strength of its
value. The contract charges the whole surface instead — *"REPORT the full motif count as m"* — because
the motif table is what a future registration would be drawn **from**. The conservative number is the
one recorded.

---

## 11 · W-C — THE FAN QUESTION

### 11.1 · FINDING, REPORTED NOT FIXED — the knot constant does not survive the change of scale

```
    lens  in-knot at t0        BR width at t0
    5m      0 of 1,628    median  15.24 ATR   p10   6.70 ATR
    15m     0 of 1,628    median  17.37 ATR   p10   7.61 ATR
    30m     0 of 1,628    median  20.66 ATR   p10   8.60 ATR
    1h      0 of 1,628    median  24.17 ATR   p10   9.20 ATR
```

`RIBBON_C = 0.5 ATR` is calibrated for a **three-member** SR band. The BR spans e9…e5000 and its width
is 15–24 ATR at *every* stage of W-A, so `br_knot` is false for **every one** of the 1,628 campaigns
on every lens: the in-knot class is empty **by construction, not by measurement**. The constant is
VETO by name and was **not** changed; the fan question is answered below at SR scale, where the
constant lives. This is the third instance of the same family of defect (V-ULT-1 already reported it
for `k=20`/UH `state` and for the knot/expansion tautology at VH scale) and it is now a pattern worth
an operator ruling rather than three separate notes.

### 11.2 · The fan question at SR scale, 1h lens

```
    SR    class            w n  w share    c n  c share     diff
    FAST  in-knot          314   0.3857    385   0.4730  -0.0872
    FAST  fanning            5   0.0061      9   0.0111  -0.0049
    FAST  fan-complete     495   0.6081    420   0.5160  +0.0921
    M     in-knot          309   0.3796    275   0.3378  +0.0418
    M     fan-complete     504   0.6192    537   0.6597  -0.0405
    MH    in-knot          166   0.2039    133   0.1634  +0.0405
    MH    fan-complete     623   0.7654    657   0.8071  -0.0418
    H     in-knot           43   0.0528     47   0.0577  -0.0049
    H     fan-complete     645   0.7924    642   0.7887  +0.0037
    VH    in-knot           13   0.0160     12   0.0147  +0.0012   (n/a 265/265 — not warm)
    UH    in-knot           43   0.0528     41   0.0504  +0.0025   (n/a 386/386 — not warm)
```

The largest single split in the whole study sits here: **winners are born fan-complete on FAST more
often than controls (60.8% vs 51.6%) and born in-knot less often (38.6% vs 47.3%)** — a 9.2-point gap
on the 1h lens. Every other SR is inside 4.2 points. It is recorded, not claimed: W-B's guard has just
demonstrated that this cohort at this size produces 8.7-point gaps from label noise alone, and this is
one contrast among the many that six SRs × four lenses afford.

The `n/a` rows are honest, not empty: on 1h, e4618 and e5000 need ~17,300 bars to warm, so 265–386
campaigns predate a warm VH/UH. NaN-before-warm is inherited, and an unwarmed band is reported as
undefined rather than as "not knotted".

**Time from knot exit to t0** (hours, from the A-3 episode ledger; `never` = that SR had not unknotted
at any point before t0):

```
      lens  SR      w med   w p90   c med   c p90  w never  c never
      1h    FAST     11.7    39.8    12.1    40.8        0        0
      1h    M        83.7   272.5    86.2   249.3        3        2
      1h    MH      316.1  1091.1   336.9  1053.2       25       22
      1h    H       973.6  3015.0   971.9  3157.9      119      122
      1h    VH     2889.5  9003.7  2892.1  9250.9      389      391
      1h    UH     2240.1  8104.1  2339.2  8145.2      521      523
```

Winners and controls are indistinguishable on this axis at every SR and every lens — the medians agree
to within a few percent throughout. Recorded as a null.

---

## 12 · W-D — RECLAIM ANATOMY (feeds P-REC-1 wording)

Long-EMA loss→reclaim inside campaigns: close crosses e889 / e2618 / e4618 **against** the campaign
direction and back **in favour** before t_exit, on the 1h lens. Every event is strictly after t0 —
this is anatomy, not an entry feature.

> **EXPOSURE WARNING, and it changes the answer.** Median hold is **112.4h for winners against 2.2h
> for controls — a 50× gap.** A loss→reclaim can only happen while a campaign is open, so any raw
> winner-vs-control count here is mostly a measurement of how long each side was exposed.

```
     ema cohort     events  campaigns  ev/camp   ev/100h  med lag h  med h from t0   after->exit ATR
     889 winner        644        154     4.18     0.374        2.0           95.4            -1.683
     889 control        35         20     1.75     0.305        1.0           19.6            -2.249
    2618 winner        303         81     3.74     0.176        3.0          111.6            -1.185
    2618 control        25          8     3.12     0.218        2.0           59.8            -4.568
    4618 winner        164         35     4.69     0.095        2.0          138.1            +0.517
    4618 control        16          3     5.33     0.139        1.5           14.2            -1.219

  total open-campaign exposure: winners 172,326h   controls 11,470h

  campaigns with >=1 loss->reclaim on ANY long EMA:
    winner   221 of 814 (27.1%)     <- exposure-confounded
    control   31 of 814  (3.8%)     <- exposure-confounded

  DURATION-MATCHED BAND (campaigns held >= 24h, both cohorts):
    winner     737 campaigns   171,778h exposure   221 with an event (30.0%)   0.647 ev/100h
    control    114 campaigns     8,696h exposure    24 with an event (21.1%)   0.736 ev/100h
```

**The headline that isn't.** "27.1% of winners against 3.8% of controls experience a long-EMA
loss→reclaim" is a 7× ratio and it is **almost entirely exposure**. Normalised per 100 open hours the
two cohorts are indistinguishable (0.374 vs 0.305 on e889), and on e2618 and e4618 the *controls* are
higher. In the duration-matched band the controls are higher still (0.736 vs 0.647 ev/100h). Whatever
P-REC-1 ends up saying, it cannot be "winners reclaim more" — on this measurement they do not.

---

## 13 · W-E — THE BRUNCH TABLE

Top 20 winners by `gross_R`. The 20 of them carry **2,925 R of the winner cohort's 7,689 R — 38.0%**.
Full per-campaign ±72h event pages (BEFORE/AFTER split, 12-hour buckets, token counts) are in the run
transcript on D:; the identity card is here. `wrm` = how many of the 18 EMAs were warm at the stamp
bar; `V1h` = the range-verdict state at t0 on the 1h member.

```
 # campaign                   dir   mand       gross_R    mfe_R    gb_R  hold_h t0                BR@t0(1h)    wrm wall   disp V1h
 1 ETHUSDT_swing|c61t75       long  swing      +507.62  +685.62 +178.00  1408.7 2020-12-26 11:30Z n-a/n-a       14 multi   0.53 BROKEN
 2 ETHUSDT_intraday|c554t720  long  intraday   +402.34  +552.16 +149.82   398.1 2023-01-02 06:56Z compr/mixed   18 none    0.91 BROKEN
 3 ETHUSDT_intraday|c186t225  long  intraday   +276.28  +462.92 +186.64   209.2 2021-01-02 10:09Z n-a/n-a       14 M       0.39 BROKEN
 4 BTCUSDT_intraday|c218t290  long  intraday   +236.23  +517.76 +281.54   254.1 2020-12-24 20:14Z n-a/n-a       14 multi   0.17 BROKEN
 5 NEARUSDT_swing|c144t217    long  swing      +128.07  +185.80  +57.73  1346.0 2023-10-23 14:10Z compr/mixed   18 multi   1.37 RESPECTED
 6 BTCUSDT_intraday|c613t788  long  intraday   +124.77  +165.72  +40.96   228.6 2023-03-13 10:26Z compr/mixed   18 multi   3.11 BROKEN
 7 ETHUSDT_swing|c185t266     long  swing      +116.49  +187.26  +70.77   675.7 2023-10-21 04:30Z compr/mixed   18 multi   1.94 BROKEN
 8 BTCUSDT_intraday|c71t101   short intraday   +108.75  +167.46  +58.71   234.4 2020-03-08 10:37Z n-a/n-a       11 none    4.52 BROKEN
 9 SOLUSDT_intraday|c553t708  long  intraday   +108.43  +216.76 +108.33   163.0 2023-11-07 03:04Z compr/bull    18 M       0.41 BROKEN
10 ETHUSDT_swing|c12t6        long  swing       +93.93  +138.37  +44.44  1262.8 2020-01-04 13:20Z n-a/n-a        7 FAST    1.33 RESPECTED
11 NEARUSDT_intraday|c658t797 long  intraday    +87.71  +128.71  +41.00   212.0 2023-12-19 18:03Z expand/bull   18 FAST    0.84 RESPECTED
12 SOLUSDT_intraday|c79t82    long  intraday    +87.34  +141.75  +54.41   179.8 2021-01-30 05:15Z n-a/n-a       11 multi   0.44 BROKEN
13 BTCUSDT_position|c53t101   long  position    +85.36  +170.71  +85.35  2008.8 2023-10-27 19:45Z compr/bull    18 M       0.18 BROKEN
14 ETHUSDT_intraday|c538t707  short intraday    +83.60  +142.92  +59.32   116.0 2022-12-15 12:03Z compr/mixed   18 multi   0.42 BROKEN
15 NEARUSDT_swing|c50t57      long  swing       +82.03  +144.38  +62.34  1382.3 2021-07-25 13:50Z n-a/n-a       13 multi   1.68 RESPECTED
16 BTCUSDT_intraday|c194t253  long  intraday    +81.96  +115.44  +33.48   232.0 2020-10-19 04:04Z n-a/n-a       14 multi   0.48 BROKEN
17 ETHUSDT_swing|c26t28       long  swing       +81.74  +158.19  +76.45   423.7 2020-05-28 08:30Z n-a/n-a       11 multi   0.43 RESPECTED
18 BTCUSDT_swing|c156t219     short swing       +81.63  +167.33  +85.70   525.7 2022-08-18 13:20Z compr/mixed   18 multi   1.75 RESPECTED
19 NEARUSDT_intraday|c428t525 short intraday    +79.85   +91.19  +11.35   383.3 2022-11-07 05:46Z compr/mixed   18 MH      1.98 RESPECTED
20 SOLUSDT_swing|c39t52       long  swing       +70.92  +116.12  +45.20  1174.2 2021-07-30 09:55Z n-a/n-a       13 multi   2.19 BROKEN
```

17 of the top 20 are long; 8 are ETH. `wall = multi` on 12 of 20 — at birth, price is within 0.5 ATR
of **more than one** SR band, so the "single wall" stamp has no single identity to report on most of
the biggest winners. **10 of the top 20 show `BR@t0 = n-a`**, because fewer than 18 EMAs were warm
at their birth: every one of those is a 2020 or early-2021 campaign, and the `wrm` column says exactly
how short they fell (7 to 14 of 18). This is the warm-up law showing up precisely where the tail is
richest, reported rather than filled in — and it is the reason the BR-warmth correction in §14 F-19
mattered.

**The range verdict at t0 is a null too.** Across the full cohort on the 1h member: winners
**BROKEN 627 / RESPECTED 187**, controls **BROKEN 632 / RESPECTED 182**. Coverage is 100% — every one
of the 1,628 campaigns has an as-of verdict state at t0.

---

## 13a · ADVERSARIAL REVIEW OF THIS BUILD'S OWN PROGRAMS

Both programs were put through an eight-dimension adversarial review before publication — the R-1
ruler restatement, A-2's window logic and curtain, A-1/A-4's event definitions, A-3's episode
segmentation, the cohort and exit join, the capture and its curtain labels, the motif construction and
the I11 guard, and a literal contract-completeness audit. Each dimension's findings were then handed
to an independent skeptic instructed to **refute** them, defaulting to refuted when the failure could
not be demonstrated against the artifacts on D:.

**44 candidate findings · 38 refuted · 6 survived · all 6 fixed.** 52 agents, 1,073 tool calls.

| survivor | severity | what it was | effect |
|---|---|---|---|
| `br_state` labelled bear-fanned order as BULL | **critical** | sign inverted on `np.diff` | every bull/bear column in W-A and W-E was **backwards** |
| `tax_*` reported `0` for pairs that never existed | major | no feasibility sentinel | 26,714 cells, 6.9% of windows, absent data as a definite negative |
| trigger medians printed against the arming toll | minor | `trg_toll_atr` computed, never printed | two of four outcome columns judged against the wrong bar |
| `window_width_bars` off by one at the series edge | minor | `n-1-i` for a window spanning `n-i` bars | 25 rows, one per cell |
| `refusal_per_1k_bars_24h` fencepost | minor | numerator spanned L+1 bars, denominator L | systematic over-count, up to 27% on 4h |
| verdict rows on the BEFORE side of the curtain | minor | member state stamped at its open | up to 12h of leak into a birth stamp |

Beyond those six, this lane found and fixed **five more** that the review either did not reach or
reached only after they were gone — the exit-window mask (F-17, independently flagged CRITICAL by two
reviewers *after* it had been fixed), the knowability split (F-18), the partially-warm BR (F-19), and
two window-margin errors of the same family (F-20, F-26). **Eleven defects total, all fixed, all with
measured before/after in §14.2.**

**What the 38 refutations were worth.** They are not noise: each was a specific, plausible failure
that a skeptic had to go to the artifacts to kill. Two examples of claims that did *not* survive —
that `r1_block`'s vectorised bulk path diverges from the naive per-anchor loop (it does not; verified
element-for-element including the clamped tail), and that the greedy A-4 scan silently drops
penetrations (it does not; the census now proves emitted + absorbed + no-reclaim ≡ penetration bars,
per lens).

**Two substantial non-fixes are declared readings rather than defects**, and both are flagged for a
ruling instead of being resolved by a builder: A-3's "first ordered separation of *medians*" is read
as the SR's own three members rather than the six SR-median lines (F-16), and W-A's "six-stage kit" is
read as the six instants the contract enumerates in the same sentence rather than DIONYSUS's S1–S6
stations (§9).

---

## 14 · FINDINGS

Numbered so the operator can rule on them by number. **F-1…F-16 are NOT fixed** — each is a pinned
constant, a dangling citation, or a reading that belongs to a ruling rather than to a builder.
**F-17…F-27 WERE fixed in this build**, with their measured before/after: five found by this lane,
six by the adversarial review of §13a.

### 14.1 · NOT FIXED — for a ruling

**F-1 · The kiss grammar is INERT on slow line-vs-line pairs.** §2.1. Five of eleven pared pairs
return exactly zero refusals at every lens, and for five of them the *maximum* reach within k=10 bars
across the whole panel history is below the δ=0.75 threshold — the event is impossible, not rare.
ε/δ/k are VETO and were not changed. **Ruling wanted:** should the grammar be scale-matched per pair,
as `k=20` and `RIBBON_C` arguably should be? This is now the fourth instance of one pattern.

**F-2 · `RIBBON_C = 0.5 ATR` does not survive the change of scale to the BR.** §11.1. BR width is
15–24 ATR at every stage, so `br_knot` is false for **all 1,628 campaigns on all four lenses** and
W-C's in-knot class is empty by construction. Answered at SR scale instead. **Same ruling as F-1.**

**F-3 · `NOMENCLATURE_MAP` does not exist.** §5. The W-TB1 block cites "row 1/2" of an artifact that
is nowhere in the estate. Part A pins its own N=96 / 3-bar definitions [VETO], so nothing is blocked;
the citation is left dangling and named. **Ruling wanted:** file the map, or drop the citation.

**F-4 · A-2's arming-anchored fate table is circular.** §3.4. It is printed because the contract asks
for it. The curtain-clean anchor is the trigger, and it is negative on 5m/15m/30m under **both**
trigger readings. Not a defect in the code; a defect in any reading of the table that stops at the
first two columns.

**F-5 · W-D's raw winner-vs-control counts are an exposure artifact.** §12. Median hold is 112.4h vs
2.2h — a 50× gap. "27.1% vs 3.8%" becomes 0.374 vs 0.305 per 100 open hours, and reverses on e2618
and e4618. The per-100h and duration-matched columns are printed beside the raw ones; the raw ones are
kept because deleting them would hide the size of the trap.

**F-6 · F-W1b is a vacuous fixture.** §7. Every stratum had enough losers, so the match is exact on
all four keys and the marginals are equal by construction. "Within 10%" cannot fail here. Reported as
passing because it did; flagged as vacuous because it is. The no-reuse and no-overlap halves of F-W1
are not vacuous.

**F-7 · `fan_age` at each bar is stored as `(onset, length)`, not as a per-bar column.** §4. The two
numbers determine the series exactly, and `fan_age_series()` reconstitutes it at every consuming
stamp — including every A-2 arming and every W-TB1 capture bar. A stored per-bar table would be ~10⁸
rows. A storage decision, disclosed.

**F-8 · "SR-order entropy" had no pinned definition and now has a declared one.** §8. Implemented as
the normalised inversion count of the six SR medians against the bull order, stored as
`sr_order_disorder` under that name rather than under a borrowed word — no entropy, of any base, over
any distribution, is computed. **Ruling wanted:** ratify or replace the definition.

**F-9 · The tape excludes `price_band` events.** §8. The contract's tape enumeration names "every
cross (within-SR + SR-median pairs)"; `price_band` enter/exit/traverse/reject is a different
pair_class and is not named. It is computed and pinned by V-ULT-1 but is not on the tape and not in
the motif alphabet. Folding it in silently would have made the declared alphabet a different object
from the measured one. **Ruling wanted:** in or out.

**F-10 · "both lenses per I6" is a reading, and here is the reading taken.** §3.3. I6's lens pair
(`24h|window_chained` / `direction_consistent`) is a cascade-depth construct that A-2 does not build.
The clause taken as binding is I6's last — *"rulers arrival/trigger-anchored"* — so both **anchors**
are computed and both are always printed. If I6's window lenses were meant, A-2 does not yet answer.

**F-11 · A-2's 4h stamps are computed in memory, not read from a pinned artifact.** §3. A-1 and A-4
are pinned to four lenses; A-2 runs on five. The same functions produce the 4h sweep and refusal
streams on demand rather than widening A-1's or A-4's ratified deliverable by an unratified lens.
Consequence: the 4h stamp inputs are not independently sha-pinned.

**F-12 · The ribbons gate passes on a reading, not a string match.** §0. Stored columns are per-SR
prefixed and the orientation code is `orient`, not `orientation`.

**F-13 · 1m is deferred and the annex was never built.** §1. Both named in the audit; neither is read
by any table here.

**F-14 · `m_full` may over-charge by counting one motif three times.** §10. The same underlying event
sequence appears once per SEQ frame, so 743,516 is the count of *(frame, motif)* pairs rather than of
distinct sequences. The contract says "the full motif count"; the larger, more conservative reading is
the one charged. **Ruling wanted:** is the surface 743,516, or 288,857 (the `absolute` frame alone, of
which the other two are re-spellings)?

**F-15 · The missing fixture class, still missing.** V-ULT-1's pending item 3 said no fixture asserts
a taxonomy is *complete* over the transitions it claims to cover. Part A adds disjointness fixtures
(F-A2a, F-A3a, F-A4b), a reconciliation fixture (F-A2b) and, new this build, A-4's penetration census
(emitted + absorbed + no-reclaim ≡ penetration bars, asserted per lens). A-3's episode segmentation is
still not proved exhaustive by anything here. **F-17 and F-19 below were both invisible to every
fixture in this build**, which is the argument for the class.

**F-16 · A-3's "first ordered separation of medians" is read as the SR's own three members.** §4. The
contract's word is *medians*, plural, which could mean the six SR-median lines (12, 89, 316, 889,
2618, 4618) read globally. Since knot episodes are per-SR, the exit direction is taken from that SR's
own monotone order. **Ruling wanted:** per-SR ordering, or the global median ladder?

### 14.2 · FIXED in this build

**F-17 · The exit-window mask was assigned, not unioned.** `keep[exit_window] = state_changes[...]`
ran *after* the hourly spine had been written into `keep`. Wherever the exit window overlapped the
birth window — most of the control cohort, median hold 2.2h — it **reset the birth spine to the change
mask**, dropping every spine bar in the overlap that was not also a state change, and on some
campaigns the t0 bar itself. `=` → `|=`. **64,277 spine rows restored (2.5%).** Every W-A percentage
column was byte-identical across the fix; only the continuous columns moved, because the as-of row is
now closer to each instant. *Found by this lane; independently flagged CRITICAL by two reviewers.*

**F-18 · The curtain split used bar-OPEN, so it leaked up to one bar.** A close-confirmed event on the
bar that *contains* t0 was labelled BEFORE, though that bar had not closed at the birth instant. Every
side label, every `rel_h`, every as-of lookup and the pooled motif ordering now use **knowability =
bar close**; `knowable_ts_ms` is persisted beside `ts_ms`. On the pooled cross-lens tape this also
fixes the *order*: a 1h event opening at 10:00 no longer precedes a 5m event closing at 10:05.

**F-19 · BR geometry was taken over a MOVING set of warm EMAs.** `warm = (n_finite > 0)` meant the BR
envelope spanned e9..e26 on a 2019 bar and e9..e5000 on a 2023 one — two populations under one column
name, on **37.8% of the 1h capture**, reading 13.1 ATR against 26.4 ATR. Now **all eighteen or NaN**,
with `br_n_warm_lines` persisted so the coverage is visible. BR width on 1h: median 17.3 → **24.2 ATR**.
Nine of the top-20 winners correctly turned `n-a` (§13).

**F-20 / F-26a · The t−72h stage fell outside the capture, twice.** Once as-of lookups moved to
knowability, the first captured bar closed *after* t0−72h and the whole stage reported n/a for
**1,362 of 1,628 campaigns on 5m and 1,611 on 1h**. Fixing it took two passes and both are worth
recording, because they are the same mistake at two levels: the window's left margin was anchored on
bar-*open* (giving the last bar *opening* before t−72h, which closes after it), and so was the hourly
**spine** (marking a bar that has not finished at its own spine instant). Both are now anchored on
the close. t−72h coverage: 261 → 630 → **1,586 of 1,628** on 5m.

**F-21 · The trigger interval contradicted the contract.** `(t0, t_close)` where the contract writes
`[t0, counter)`. Changed to the contract's reading. **TRIGGERED 35,757 → 42,287, +6,530 windows =
6.33% of the whole population**; median trigger lag 30 → 5 bars. `fate_strict` and
`trigger_on_arming_bar` are persisted so the precedent reading is not lost, and §3.3 prints the
trigger-anchored H100 a third time on the strict subset. **The finding survives both readings.**

**F-22 · `window_width_bars` undercounted every right-censored window by one bar.** `n - 1 - i` where
`[t0, t_close)` spans `n - i` bars.

**F-23 · The tape's key was not unique, and the motif alphabet was lossy.** All three within-SR pairs
of a family collapsed onto one token (`XFAST+` meant 9_12, 9_26 *or* 12_26), which made 37,389 tape
rows collide on BTC 5m alone. Tokens are now **pair-level**; and because several distinct refusals
genuinely share one confirm bar, the originating bar rides along as `src_ts_ms` and is part of the
key. F-KEY now runs on the tape as well as the state series — **40 assertions, dup = 0 on every one.**

**F-24 · The BRIDGE was half-satisfied: knot ENTRIES were never tape rows.** A knot episode has two
transitions; only the exit was emitted, so "the ribbon just knotted" was unrepresentable in the motif
alphabet the contract calls the *full* grammar. `KI<SR>` added, along with a neutral `K<SR>?` token so
the 48 exits whose direction never resolves are counted instead of dropped.

**F-26 · `br_state` labelled every bear fan `bull`.** `S` is stacked fast-to-slow, so
`np.diff(S, axis=0)` is *slower minus faster* and `(dif > 0).all()` means e12 < e89 < … < e4618 — a
bear fan. It was assigned `OR_BULL`, with an inline comment asserting the opposite of what the
expression tested. **Every bull/bear column in W-A and every `BR@t0` label in W-E was backwards.**
The same function's `sr_order_disorder` had the convention right, so one function emitted two
contradictory outputs: 273,883 rows carried `br_orient = BULL` with disorder 1.000, which on its own
ruler is *perfectly bear-ordered*. Verified after the fix: BULL rows now have disorder 0.000, and a
BULL row reads e12 = 48,653.6 > e89 = 48,449.1 > … > e4618 = 40,519.8. *Found by the review, severity
critical, and it is the one defect in this build that was making a printed table say the opposite of
the truth.*

**F-27 · Three A-2 columns and one stamp were quietly wrong.** (a) `tax_*` reported integer `0` for
pairs whose EMAs are `NEVER` warm on that lens — 26,714 cells across 6.9% of windows, including
`tax_4618_5000` on all 1,116 4h windows for a pair that does not exist on 4h. Infeasible pairs now
carry **−1**; the row's own `UH_state` already carried the −9 sentinel, so the ledger had been
internally inconsistent. (b) `refusal_per_1k_bars_24h` counted over a **closed** 24h interval spanning
L+1 bars against a denominator of L, on 100% of armings — a systematic over-count reaching 27% on 4h;
the interval is now half-open. (c) `trg_term_*` are ATR-normalised at the **trigger** bar but the only
toll printed was the arming population's; `trg_toll_atr` was computed, stored and never surfaced. It
is now printed as its own block. (d) Range-verdict states were stamped at their member bar's **open**,
leaking up to 12h into a birth stamp on the 12h member; the as-of now uses the member's own close.

**F-25 · Two fixtures could not fail.** F-A0R drew its sample from one lens's interior, never touching
`r1_block`'s clamped-tail path or the INFEASIBLE 4h/H20 branch — it now runs on **every A-2 lens, both
directions, with 120 anchors at the series tail**. And the I11 `admissible` flag was compared against
a BH bar of q/m ≈ 4×10⁻⁷ while 2,000 permutations can produce no p-value below 1/2001 ≈ 5×10⁻⁴: the
bar sat **1,239× below the resolution floor**, so the flag was structurally False whatever the data
said. It is still printed, now with that limitation stated beside it, and the informative obs-vs-null
comparison is the one the text leans on.

---

## 15 · PROBE-LEDGER APPEND — all m declared

Appended to `exchange/reports/CENSUS2A_PROBE_LEDGER.md` as **ENTRY 3** (summary row + prose block +
the rewritten running-sum line, which is how that file appends):

| stage | what it is | m | why |
|---|---|---:|---|
| A-0 completion audit | manifest × disk × sha reconciliation | **0** | a census of what exists; nothing compared |
| A-1 refusals | ratified grammar on a fixed pair list | **0** | complete partition; constants VETO, none swept |
| A-2 armed-window ledger v2 | fixed arming/window/trigger/fate definitions | **0** | every definition pinned by the contract; no arm ranked |
| A-3 transitions | episode extraction | **0** | extraction |
| A-4 sweeps | fixed N=96 / 3-bar definitions, both VETO | **0** | extraction |
| W-A station occupancy | six fixed stages × fixed partition | **0** | complete partition printed whole |
| W-B sequential motifs | every k-gram, k ≤ 4, three frames, pair-level alphabet | **743,516** | the contract charges the full surface |
| W-C fan question | fixed three-class partition | **0** | complete partition |
| W-D reclaim anatomy | fixed three long EMAs, fixed event definition | **0** | extraction; no threshold swept |
| W-E brunch table | top-20 by `gross_R`, display | **0** | sorted to be looked at, nothing kept |
| **TOTAL for ENTRY 3** | | **743,516** | |

**RUNNING SELECTION SURFACE after this entry: 743,516** (it was 0).

That number is the honest price of the motif probe and it is why the probe registers nothing. The
I11 guard is printed beside the top table in all three frames and returns `admissible = False`
everywhere — with the caveat of F-25 attached: at 2,000 permutations the flag could not have been
True whatever the data said, because the BH bar sits 1,239× below the p-value floor. The comparison
that IS informative is obs-vs-null, and there the observed maximum separation does not reach its own
null 95th percentile in any frame.

---

## 16 · DISPOSITION

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `scripts/census2b_parta.py` | yes | tracked | this session | yes | GitHub + estate zip | n/a — `scripts/` is not in the box |
| `scripts/census2b_wtb1.py` | yes | tracked | this session | yes | GitHub + estate zip | n/a — `scripts/` is not in the box |
| `exchange/reports/BUILD_2026-08-14_CENSUS2B_PARTA_WTB1.md` | yes | tracked | this session | yes | GitHub + estate zip | see below |
| `exchange/reports/CENSUS2A_PROBE_LEDGER.md` | yes | tracked | this session | yes | GitHub + estate zip | +6,421 B |
| `exchange/status/LEDGER_APOLLO.md` | yes | tracked | this session | yes | GitHub + estate zip | +8,529 B |
| `D:/Naiad/research_outputs/census2b/refusals/**` | yes | untracked | no | no | D: only — **NOT PROTECTED** | n/a — D:, unsynced |
| `D:/Naiad/research_outputs/census2b/windows/**` | yes | untracked | no | no | D: only — **NOT PROTECTED** | n/a — D:, unsynced |
| `D:/Naiad/research_outputs/census2b/transitions/**` | yes | untracked | no | no | D: only — **NOT PROTECTED** | n/a — D:, unsynced |
| `D:/Naiad/research_outputs/census2b/springs/**` | yes | untracked | no | no | D: only — **NOT PROTECTED** | n/a — D:, unsynced |
| `D:/Naiad/research_outputs/census2b/wtb1/**` | yes | untracked | no | no | D: only — **NOT PROTECTED** | n/a — D:, unsynced |
| `D:/Naiad/research_outputs/census2b/cen2b_completion_audit.parquet` | yes | untracked | no | no | D: only — **NOT PROTECTED** | n/a — D:, unsynced |
| `D:/Naiad/research_outputs/census2b/census2b_manifest.json` | yes | untracked | no | no | D: only — **NOT PROTECTED** | n/a — D:, unsynced |

**Data on D:, not one byte of it committed.** Part A adds ~93 MB (A-1 refusals + grammar reach, A-2
windows, A-3 transitions, A-4 sweeps, the audit); W-TB1 adds ~417 MB (capture 410 + aggregates 7).
The manifest now pins **260 artifacts, 2,223,134,462 B = 2.22 GB**, up from 100 artifacts and 1.71 GB — I12 pin-merge, and the
V-ULT-1 `pins` block survived untouched and was verified so (`ribbons.UH == [4236, 4618, 5000]`
re-read after the merge). Artifact classes were corrected by prefix after the merge, so a Tier-E
capture is never stamped SUBSTRATE: 91 V-ULT-1 substrate · 86 Part-A substrate · 43 W-TB1 descriptive
capture · 9 W-TB1 Tier-E aggregate · 9 first-look Tier-E · 1 audit · 1 Tier-E JSON.

### BOX-COST

`exchange/**` was **2,256,225 B = 35.31%** of the 6.39 MB box. **This build adds 112,319 B** — the
document 97,369 + the probe-ledger entry 6,421 + the LEDGER_APOLLO entry 8,529 — taking it to
**2,368,544 B = 37.06%**. Above the contract's `<1%` target; far below the 40% REFUSE line.

**The publish will carry 15,571 B that are not this build's.** `exchange/` currently holds two
uncommitted DIONYSUS artifacts — the untracked
`LANE_UPDATE_DIONYSUS_2026-08-13_BR-momentum_winner-zoom_brief-feedback.md` (15,571 B) and a modified
`LEDGER_DIONYSUS.md`. `publish_exchange` is path-scoped to `exchange/**` and stages the whole bus, so
those go with it. That is how the bus is designed to work and they are not touched here, but it means
the box lands at **2,384,115 B = 37.31%** rather than 37.06%, and the difference is another lane's
work rather than this one's. Named so the arithmetic reconciles for whoever reads the next
BOX-COST line.

**The overage is stated rather than rounded off, and it has one cause.** `<1%` is ≈63,900 B. This
document alone exceeds that, because of a single contract-required block: **A-0's verbatim 157-row
completion audit table is 14,859 B**, and the instruction is *"print FIRST, verbatim table"*. Dropping
it to hit the budget would have deleted the census-2B completion certificate — the one artifact the
reviewer could not obtain from the box, which is the entire reason A-0 exists. It is kept. The rest of
the overage is the second contract-required verbatim block: the A-2 outcome table at five lenses × two
fates × two directions × three anchors.

Everything compressible was compressed: W-A prints two of four lenses, W-C one of four, W-E the
identity card rather than 20 full event pages, the A-1 grammar-reach diagnostic 5m only, and §17
quotes the ledger entry by its spine rather than in full. Those five decisions cut roughly 35 KB; the
full versions are all in the run transcripts on D:.

Flagged to the operator by name, at the moment of creation, per the BOX COST ruling: this document is
**the largest single artifact this lane has added to the box**, it is prose not data, and if the
operator prefers the 1% figure to the verbatim audit table, the fix is one line —
`cen2b_completion_audit.parquet` on D: already carries all 157 rows, and §1's table can be replaced by
the grid plus a pointer, recovering ~15 KB.

---

## 17 · THE LEDGER_APOLLO APPEND

Per the 2026-08-12 ruling 'append' — *a report without its ledger entry is an incomplete
deliverable* — this document ends by appending the session's STATUS entry to
`exchange/status/LEDGER_APOLLO.md`, in this session. The entry is quoted here by its spine rather
than in full: the complete block lives in the ledger, and duplicating ~5 KB of it into the box for a
second time would be paying twice for one piece of prose (see §16 on the budget).

```
=== STATUS_APOLLO — 2026-08-14b ===
NOW: CENSUS-2B PART A AND W-TB1 ARE BUILT, IN THAT ORDER, AS THE CONTRACT REQUIRED. The completion
certificate A-0 could not obtain from the box now exists and is printed first; the sequential
substrate A-1..A-4 is on D:; and the 12.3% tail has its ±72h biography against a 1:1 matched control.
CLASS: Tier-E substrate + Tier-E descriptive. NO REGISTRATIONS. Selection surface m = 743,516, all of
it W-B's motif surface — and the I11 guard returns a clean null in all three SEQ frames. Tail Bio nomenclature is
NOT ratified; it remains [proposed] as W-TB1 · TAIL BIOGRAPHY, DIONYSUS 2026-08-13, routed to APOLLO.
LAST EVENT: 2026-08-14 — census-2B Part A (A-0..A-4) + W-TB1 tail biography, one build document
FACTS:  [11 facts — completion certificate · the negative trigger · the motif null · the 44-finding
        adversarial review and the inverted bull/bear it caught · the exact 814 cohort · the exit
        side was never a data gap · W-D's exposure artifact · four constants that do not scale ·
        all fixtures pass · duration-fixed horizons and the infeasible one · BOX-COST]
PENDING (none blocks this contract):  [8 items, all operator rulings — see §14.1]
NEXT: the operator reads §3.3 (the trigger is negative), §10 (the motif null), §12 (the exposure
artifact), and rules on the four scale-mismatched constants as one question rather than four.
Owner: operator.
METRICS: operator actions this session = 1 (the CENSUS-2B PART A + W-TB1 paste) — files re-ingested = 0
=== END STATUS ===
```

**Three status items the contract asked to be named explicitly:**

- **Tail Bio nomenclature: NOT ratified.** "TAIL BIOGRAPHY" appears four times in the estate, all
  from DIONYSUS on 2026-08-13, all as the probe name `W-TB1 · TAIL BIOGRAPHY`, tagged `[proposed]`
  in that file's own legend, with design and registrations routed to APOLLO. The abbreviation "Tail
  Bio" appears nowhere. This build does not ratify it and does not use it as if ratified.
- **Census-2B completion certificate: PRINTED.** §1. 157 cells, 100 PRESENT and sha-verified,
  0 STALE, the panel complete across six lenses, and the two gaps (1m, annex) named.
- **1m: DEFERRED, named.** §1. **PO3-mirror: STILL UNEXECUTED, and not commissioned here.** It is a
  specific object, not a vague frame: **CEN-5 arm (b), the PO3-mirror exit v0**, whose band is pinned
  by **A3-BAND [VETO]** to the CEN-6 boundary object — the prior completed week's extremes
  (`CENSUS2A_CONTRACT_v0.3_RESOLVED_2026-08-12.md:102`, `…APOLLO.md:238`). It was **deliberately not
  captured** in census-2A and said so on the record (`CENSUS2A_CLOSEOUT_2026-08-12.md:120`), was
  still `[unexecuted arm]` in the DIONYSUS lane update of 2026-08-13, and **neither block of this
  contract commissions it**. What this build adds toward it is substrate, not study: W-TB1 §(c)
  EXIT-ANATOMY captures the exit side as data for all 1,628 campaigns, and A-4 supplies a pinned
  sweep grammar. No mirrored exit grammar is defined, computed or claimed here.
  Status: **substrate present, arm still unexecuted.**
- **W-D is the P-REC-1 feed, and it comes back null.** DIONYSUS commissioned P-REC-1 `[proposed]` on
  the operator's observation that *trailed-out on a long EMA, then the reclaim is the signal*. §12
  measures exactly that shape and, once exposure is divided out, winners and controls reclaim at
  indistinguishable rates — with controls higher in the duration-matched band. P-REC-1 remains
  unregistered; this is the descriptive wording it now has to be written against.

---

*End of build document. Class: Tier-E substrate + Tier-E descriptive. No registrations. Selection
surface m = 743,516, declared in the probe ledger. Nothing in this document is a finding.*
