# BUILD — VIZ-4 · THE EMA MANTLE (payloads)

**Date** 2026-08-15 · **Branch** `v12-v1-census` · **HEAD at start** `1dbc790` · **Seed** 20260815 · **Drafted** APOLLO · **Executor** HEPHAESTUS

**CLASS — DISPLAY-ONLY / Tier-E exploration · m = 0 · no registrations.** Every number emitted is a displacement, a velocity, a correlation or a mark. **Echoes are shown, never scored.** The payloads are complete fixed-stride decimations of fixed series: nothing is ranked, nothing is selected, and no window was chosen on what it contained. Promotion requires registration (`CENSUS2A_CLOSEOUT_2026-08-12.md` §5).

**Program:** `scripts/census2b_viz4.py` (new). **Payloads:** `research_outputs/census2b/viz_payloads/`. **Ferry:** `research_outputs/census2b/DESIGN_HANDOFF_VIZ4/`.

---

## 1 · CONTRACTS — filed

| contract | state | sha256 | bytes |
|---|---|---|---:|
| `DESIGN_CONTRACT_VIZ4_EMA_MANTLE_2026-08-15.md` | **FILED** to `exchange/reports/` from the operator's attachment | `8e8b3264805c9dee92d4bd9ad79ba62e56f1f404175d9a60d82ae9d1b1cdec7c` | 3,857 |
| `DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md` | **ABSENT** | — | — |

**V-10 DOES NOT CLOSE.** The VIZ-3 contract is not in `exchange/reports/`, not in the operator's attachment folder, and not anywhere in the repo — `find` over the whole tree returns only `research_outputs/census2b/DESIGN_HANDOFF_VIZ3/` (which holds the four `v3_*.json` payloads, the ORACLE build, the CENSUS-2A design brief and a DIONYSUS lane update — **no contract**). It was **not invented**, and the ferry carries what exists.

This matters beyond bookkeeping: the VIZ-4 contract's first line binds *"Iron rules of the VIZ-3 contract apply verbatim"*, and §5 tells the design session *"§2 of the VIZ-3 iron rules binding"* — **a document the estate does not hold.** The build proceeded because VIZ-4 §Class **restates the operative rules inline**: *payload-only · no verdict language · toll bands on outcome axes · dark-mode legible · self-contained HTML, CDN deps only · provenance footer per artifact · DESIGN_NOTES.md*. Those are the rules honoured here. **Ruling needed** — see F-1.

---

## 2 · THE PAYLOADS (contract §3)

| payload | steps | source bars | stride | rows | bytes | sha256 (data block) | toll_lo / toll_hi |
|---|---:|---:|---:|---:|---:|---|---:|
| `v4_mantle_BTC_1h.json` | 7,593 | 60,737 | 8 | 115,072 | 2,459,852 | `c01bd118df16ae17…` | 0.135516 / 0.140043 |
| `v4_echo_BTC_1h.json` | 7,593 | 60,737 | 8 | 23,964 | 2,201,695 | `4fd09d4f233f077a…` | 0.135516 / 0.140043 |
| `v4_mantle_BTC_5m.json` | 7,923 | 728,833 | 92 | 328,108 | 4,151,334 | `0676e3c1c2502a0e…` | 0.553747 / 0.564108 |
| `v4_echo_BTC_5m.json` | 7,923 | 728,833 | 92 | 233,040 | 3,869,551 | `a3f683f437fee134…` | 0.553747 / 0.564108 |

*(`rows` is the emitter's array-CELL count, not a record count — read `marks.n` / `len(ts)`. `sha256` is of the payload's own `data` block, per the shared emitter; a file may never contain its own file-sha.)*

**Decimation rule, deterministic and restated in every `meta`:** fixed stride `ceil(n/8000)`, **anchored at the LAST bar** — `arange(n-1, -1, -stride)[::-1]`. Anchored at the end rather than the start so the newest bar is always present: a mantle whose right edge is a stale bar is a mantle that lies about now.

### What the numbers mean

- **Displacement** `(EMA − price)/ATR` — **note the order**: a thread *above* price reads **positive**. `null` where the EMA is not warm **or** ATR is undefined.
- **Velocity** — Δdisplacement **per bar** over that thread's SR window: `(d[t] − d[t−k])/k`. This is census-2B's own `_delta_k` shape (`census2b_program.py:686-693`, a *k-bar difference*, not a rolling mean) divided by `k` to make it the per-bar rate the contract asks for. `k` is **read from the ORACLE manifest's pins**, not retyped: `{FAST 20 · M 20 · MH 40 · H 111 · VH 327 · UH 577}`, law `k = max(20, round(median_len/8))`, pinned by R-3 on 2026-08-15.
- **Echo** — Pearson `corr` over a trailing 96-bar window between **hem-edge velocity at t** (mean of e12/e26, contract §2) and **rod-edge velocity at t+lag** (mean of e2618/e3618/e4236/e4618/e5000), lags 0…48. So **a ridge at lag L reads "the rod moved L bars *after* the hem"** — the direction the contract's question asks for, stated in each payload's `note` so a renderer cannot invert it silently.
- **Marks** — knot→fan transitions, **columnar** (`marks.n`, `marks.fields`, parallel arrays).

### Absent cloth — the inventory (contract §3: *"render the missing cloth as absent, never as zero"*)

| payload | disp cells | absent | e12 | e316 | e2618 | e5000 (rod) |
|---|---:|---:|---:|---:|---:|---:|
| mantle BTC 1h | 136,674 | 11,172 (**8.2%**) | 0.1% | 1.8% | 14.9% | **28.5%** |
| mantle BTC 5m | 142,614 | 977 (**0.7%**) | 0.0% | 0.2% | 1.2% | **2.4%** |

Echo nulls (window not full or an edge not warm): 1h **15.6%** of 372,057 cells · 5m **1.3%** of 388,227.

**The 1h mantle is a quarter unwoven at the rod and that is the honest picture** — e5000 needs 17,300 warm bars (census-2B's `WARMFACTOR 3.46`), which at 1h is ~721 days of the 60,737-bar series. F-V4 (c) proves the nulls **lead unbroken** and that **not one absent cell was written as an exact zero**.

---

## 3 · F-V4 — PASS

| leg | result |
|---|---|
| **(a) round-trip** | all four payloads `json.load` and their stored data-block sha re-hashes **OK** |
| **(b) shape** | 18 threads · 18 `disp` rows · 18 `vel` rows · steps ≤ 8,000 · 49 lags · window 96 · every array length equals `len(ts)` |
| **(c) absent, not zero** | rod thread nulls **lead unbroken**, **0 exact-zero cells** in both mantles |
| **(d) marks reconcile** | **1h: 2,710 marks = 2,710 resolving knots**, 0 not-in-knots, **2,710 inside a same-SR fan episode, 0 outside**. **5m: 37,501 = 37,501**, 0 / 37,501 / 0. Both payloads of each cell carry byte-identical mark blocks. |
| **(e) ferry** | `DESIGN_HANDOFF_VIZ4/` holds 5 files — 4 payloads + the VIZ-4 contract; the absent VIZ-3 contract is named, not silently skipped |
| **(f) provenance** | per-SR `k` from the ORACLE pins; `toll_lo/hi` per cell from that cell's own `transitions` tables; `seed 20260815`; `class DISPLAY-ONLY / Tier-E exploration` on every payload |

**F-KEY** asserted before every join and logged on success: `emas[BTCUSDT/1h]`, `ribbons[BTCUSDT/1h]`, `emas[BTCUSDT/5m]`, `ribbons[BTCUSDT/5m]` — 0 duplicates; plus an explicit equality check that the `emas` and `ribbons` timestamp grids are the *same* grid before they are read side by side.

**Suite:** `pytest fixtures tests -q -m "not slow"` → **288 passed, 1 skipped, exit 0**, unchanged. No existing test touched.

---

## 4 · FINDINGS — NOT FIXED

**F-1 · The VIZ-4 contract binds a document the estate does not hold.** §1. Its class line and §5 both make the VIZ-3 iron rules binding; no VIZ-3 contract exists anywhere. VIZ-4 restates the operative rules inline, so the build is not blocked — but the *authority* for those rules is a file nobody can read, and the standing PENDING item "re-attach `DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md`" is now **two cycles old**. **Ruling needed: re-attach it, or promote VIZ-4's inline restatement to the rules of record and stop citing VIZ-3.**

**F-2 · A knot→fan mark almost never starts a fan — measured, and it changes how M2 must be drawn.** F-V4 (d) first asserted that every mark lands on a *fan onset*. **It failed 2,568 of 2,710.** The estate never promised it: `fans` splits an ordered run at every direction change, and a ribbon can be **knotted while `orient` is already bull or bear**, so a knot commonly releases into a fan that was **already running**. Measured: only **142 of 2,710 (5.2%) at 1h** and **1,479 of 37,501 (3.9%) at 5m** begin a new fan. Every mark now carries `at_fan_onset` so the renderer can tell the two apart. **This bears directly on M2's question** — *"did an echo precede the fan?"* — because for ~95% of marks the fan predates the knot's release, and a mark drawn as "a fan started here" would assert something the data does not say. **Ruling needed for the design session's copy: does a mark mean "knot released" (what it is) or "fan began" (what it mostly is not)?** Not resolved here; both facts are in the payload.

**F-3 · The payloads are 3–6× the VIZ-1 emitter's 700 KB cap, and the contract's own spec is why.** 8,000 steps × 18 threads × 2 (displacement + velocity) is 288,000 numbers before a single mark; 49 lags × 8,000 steps is another 392,000. **No rounding fits that in 700 KB.** Reductions already taken, and stated rather than done quietly: displacement 3 dp, velocity 5 dp, **correlations 2 dp** (200 distinct levels across [−1,1] — more than any colormap resolves), and **marks emitted columnar**, which alone cut the handoff from 18.3 MB to **12.7 MB**. The cap is VIZ-1's module constant, not this contract's requirement, and the contract sets no byte limit. **Ruling needed: raise the shared cap for 3D payloads, or cap VIZ-4 by steps-per-payload instead.**

**F-4 · "12 at the hem" is 17 threads; the fabric is 18.** Contract §2 labels the y-axis *"log scale, 12 at the hem → 5000 at the rod"*, while §1 and §3 both say **eighteen** EMAs — and `RIBBONS` FAST is `(9, 12, 26)`. Read as: the axis spans **9 → 5000** (all eighteen woven), and the **hem *edge* used by the echo is 12/26 exactly as §2 defines it**. Both facts ship in every payload (`threads`, `hem_lens`) so a renderer never has to guess which it got. **Ruling needed only if the intent was to drop e9 from the cloth.**

**F-5 · Nothing here is a registration.** m = 0 holds because each payload is a complete decimation of a fixed series under one deterministic rule. The moment a window, a lag or a thread is picked out of these payloads *because of what it shows*, the selection surface is the number that were available to pick from, and that *m* must be declared **before** the look.

---

## 5 · DISPOSITION + BOX-COST

| item | disposition |
|---|---|
| `scripts/census2b_viz4.py` | **new** — payload builder + F-V4; reuses `census2a_viz.write_payload`, imports `census2b_program.RIBBONS` |
| `exchange/reports/DESIGN_CONTRACT_VIZ4_EMA_MANTLE_2026-08-15.md` | **filed**, sha printed §1 |
| `DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md` | **ABSENT — V-10 does not close** (F-1) |
| `research_outputs/census2b/viz_payloads/v4_*.json` | **built** — 4 payloads, 12.7 MB, local, gitignored |
| `research_outputs/census2b/viz_payloads/viz4_manifest.json` | **built** — shas, tolls, contract states |
| `research_outputs/census2b/DESIGN_HANDOFF_VIZ4/` | **ferried** — 4 payloads + the VIZ-4 contract |
| `census2b/` substrate · `analytics/` · `engine/` | **UNTOUCHED** — read-only throughout |
| registrations | **none**, as classed |

**Constants: pin-vs-import per site (CONVENTIONS §6.4).** Per-SR `k` — **read** from `oracle_manifest.json` `pins.state_k` (R-3 owns it; a copy here would be a second source of truth). Toll — **read** per cell from its own `transitions` tables. Ribbons and flag codes — **imported** from `census2b_program`. The meta block, the sha rule and NaN→null — **imported** from `census2a_viz`, not restated. The emitter's `TOLL_LO/TOLL_HI` are **re-pointed per payload** (VIZ-1 carries one global toll as a module constant; this contract spans two lenses whose tolls differ four-fold, 0.1355 vs 0.5537) — an extension of the same re-point pattern VIZ-2 used for `PAY`, `SEED` and `ART`, named here because it is an extension.

### BOX-COST

`exchange/**` measured **2,722,503 B = 17.02%** of the 16,000,000 B box before this document (the VIZ-4 contract's 3,857 B included); tick set (`exchange/**` + `LEDGER.md`) **2,981,801 B = 18.64%**, level **OK** (warn 40% / refuse 70%).

**This paste adds 17,772 B = 0.111% of the box** — this document plus the `LEDGER_APOLLO` append — taking `exchange/**` to **2,740,275 B = 17.13%** and the tick set to **2,999,573 B = 18.75%**, level **OK**. **Against the < 0.5% target (80,000 B) that is 22% of budget.** The 12.7 MB of payloads never touch the box: they are local and ferried by the operator, which is what the ferry is for.

---

## 6 · THE LEDGER_APOLLO APPEND

Per the 2026-08-12 `append` ruling, this document ends by appending the session's STATUS entry to `exchange/status/LEDGER_APOLLO.md`, in this session. It is not duplicated here — see the ledger.

---

*End of build document. VIZ-4 · DISPLAY-ONLY / Tier-E exploration · m = 0 · no registrations · no rule adopted. Echoes are shown, not scored; a visible ridge is a picture, and promotion requires registration.*
