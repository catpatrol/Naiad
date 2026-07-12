# Q4c / Q4d / Q4e — the hadPrimeEp fork, tag/freshness accounting

**2026-07-12 · read-only · v11_faithful, BTCUSDT_swing · engine reconstruction
validated bit-for-bit against `compute_signals` and against the parity journal
(fresh-tag count 1083 = journal TAG count; 2026-06-23 break stops reproduce
62590.61 / 62586.80 / 62490.50 exactly).**

Staged for the operator's hover/settings verdict on the deployed chart.

---

## 1. The forking surface is `hadPrimeEp`, not the ribbon (Q4c superseded)

Q4c(a) named a candidate ribbon fork at **2026-06-23 16:15** (gap `e9x−e89x`
turns +1.90550 after a 285-bar negative run). **Operator hover refuted it:**
the chart's EMAs match the engine's to 0.1 pt at all three flip bars, so the
17:00 / 17:45 / 20:45 down-crosses fire *identically* on both. The gate that
forked is `hadPrimeEp`: `confirmL = (confirmXL and hadPrimeEp) or gradeCL`. With
`hadPrimeEp = false` the identical 17:00 down-cross produces **no** CONFIRM →
flat stop. So the fork is upstream, in this episode's tag/freshness accounting.

## 2. Q4d — tag/freshness accounting, 2026-06-23 02:30→04:20 UTC

`hadPrimeEp` resets to false only on a **fresh** tag; fresh ⇔ tag AND
`bars_since_prev_tag > zoneMemory`. Engine `zoneMemory = 5`.

```
time UTC           high      Z1edge   |h-edge|%  tag  bars_since  fresh?  hadPrimeEp  flag
02:30–03:00  (7 continuous Z1 tags, bars_since=1, cont.)                        Y
03:05  64023.40  64035.19   0.0184%    .       1         -         Y   E  (near-miss −11.8pt)
03:10  63990.30  64035.19   0.0702%    .       2         -         Y
03:15  64060.00  64035.19   0.0388%    T       3       cont.       Y   E  (barely tag +24.8pt)
03:20  64023.90  64035.19   0.0176%    .       1         -         Y   E  (near-miss −11.3pt)
03:25  64076.10  64035.19   0.0638%    T       2       cont.       Y
03:30  64068.80  64035.19   0.0525%    T       1       cont.       Y
03:35  64030.80  64035.19   0.0069%    .       1         -         Y   E  (near-miss −4.4pt)
03:40  63974.80  64035.19   0.0944%    .       2         -         Y
03:45  63997.20  64035.19   0.0594%    .       3         -         Y
03:50  64056.40  64035.19   0.0331%    T       4       cont.       Y   E  (barely tag +21.2pt)
03:55  64042.80  64035.19   0.0119%    T       1       cont.       Y   E  (barely tag +7.6pt)
04:00  64068.00  64003.62   0.1005%    T       1       cont.       Y
04:05  64061.00  64003.62   0.0896%    T       1       cont.       Y
04:10  64039.10  64003.62   0.0554%    T       1       cont.       Y
04:15  64027.40  64003.62   0.0372%    T       1       cont.       Y   E  (barely tag +23.8pt)
04:20  63946.40  64003.62   0.0895%    .       1         -         Y
```

- **7 knife-edge tag-membership bars (E):** 03:05, 03:15, 03:20, 03:35, 03:50, 03:55, 04:15.
- **0 boundary-freshness bars (B):** the engine's longest no-tag run here is 3
  bars, so max `bars_since` at a tag is **4** (03:50). No fresh tag fires;
  `hadPrimeEp` stays **Y** on every bar under `zoneMemory = 5`.

### The 03:50 / 03:55 call
If the deployed chart drops the two sub-0.05% tags at **03:50 (+21.2 pt, 0.033%)**
and **03:55 (+7.6 pt, 0.012%)**, its no-tag run becomes 03:35→03:55 (5 bars) and
the **04:00 tag lands at bars_since = 6 → FRESH → `hadPrimeEp` resets to false**,
while the engine keeps it true. That is a `hadPrimeEp` fork born here.

## 3. Engine vs Pine freshness — side by side (verbatim, line numbers)

The **logic and comparison operator are identical**; the only difference is the
**value of the memory constant**.

**ENGINE** (`engine/signals.py`, `engine/cells.py`):
```
cells.py:64-66   @property
                 def zone_memory(self) -> int:
                     return 5 if self.tf_exec == "5m" else 3        # = 5 for BTCUSDT_swing
signals.py:164   zone_memory = cell.zone_memory                     # 5
signals.py:321   fresh = [tag_now[k] and (tag_bar[k] is None or i - tag_bar[k] > zone_memory)
                          for k in range(3)]
signals.py:323-324   if any(fresh):
                         had_prime_ep = False
signals.py:358   rec = [z1_armed and tag_bar[0] is not None and i - tag_bar[0] <= zone_memory, ...]
```

**PINE** (`pine/SS_Cascade_v11.0.2.pine`, byte-identical to the deployed capture):
```
121   zoneMemory = input.int(3, "Zone memory (exec bars a tag stays recent)", minval=1,
122        tooltip="Default 3. On a 5m execution chart, 5 is recommended (ADD §8).", group=G_Z)
437   fresh1 = tag1Now and (na(tagBar1) or bar_index - tagBar1 > zoneMemory)
438   fresh2 = tag2Now and (na(tagBar2) or bar_index - tagBar2 > zoneMemory)
439   fresh3 = tag3Now and (na(tagBar3) or bar_index - tagBar3 > zoneMemory)
440   if fresh1 or fresh2 or fresh3
441       hadPrimeEp := false
480   rec1 = z1Armed and not na(tagBar1) and bar_index - tagBar1 <= zoneMemory
```

**Same `>` operator, same `<=` expiry, same structure. The divergence vector is
the constant: engine `zone_memory = 5` (hardcoded for 5m); Pine `zoneMemory`
input **defaults to 3** and must be set to 5 on a 5m chart.** The F6 sign-off
note ("default inputs", `case_windows.md`) would leave the chart at **3**. A
default-3 chart is fresh at `bars_since > 3`; the engine at `bars_since > 5`.

## 4. Q4e — bars_since boundary census, full dev window (2025-10-06 → 2026-07-07)

```
total tag_now decisions (fresh+continuation, all zones) = 44,495
fresh tags (== journalled TAG rows)                     = 1,083   (journal TAG count = 1,083 ✓)
bars_since == 4 : 85 (cont)    == 5 : 51 (cont)    == 6 : 50 (fresh)    total 186
```

- **Engine's own boundary (5→6) off-by-one exposure:** the 51 continuation tags
  at `bars_since = 5` (would flip to fresh) + the 50 fresh tags at `bars_since = 6`
  (would flip to cont) = **101 tag decisions** one bar from flipping.
- **zoneMemory 3-vs-5 mismatch exposure:** if the chart runs default `zoneMemory = 3`,
  every tag at `bars_since ∈ {4, 5}` is **fresh on the chart, continuation on the
  engine** — **85 + 51 = 136** forced fresh/cont divergences across the window,
  each one a `hadPrimeEp` reset the engine does not take (or vice versa). This is
  a systematic, deterministic fork, far larger than a float knife-edge.

## 5. The one measurement that closes it

Operator: read the deployed chart's **Zone memory** input value (Inputs tab).
- If it is **5** → the zoneMemory mismatch is ruled out; the fork is the
  knife-edge tag calls at 03:50 / 03:55 (§2), pending a hover of the Z1 edge there.
- If it is **3** (the Pine default) → that is the fork, deterministically: retag
  the 5m chart with `zoneMemory = 5` and re-check the 2026-06-23 17:00/17:45/20:45
  CONFIRMs and stop ratchet. No engine or Pine logic change is implied either way
  (the Pine already exposes the input; only the operator's setting differs).
```
