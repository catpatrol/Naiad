# Pre-contract findings — the Jun/May parity fork is a zoneMemory value mismatch

**2026-07-12 · read-only · v11_faithful, BTCUSDT_swing · engine reconstruction
validated bit-for-bit vs `compute_signals`; full-window fresh-tag count 1083 =
journal TAG count; break stops reproduce exactly.** No code changed.

## Verdict

The deployed chart runs **`zoneMemory = 3`** (the Pine input default); the engine
uses **`zone_memory = 5`** (hardcoded for 5m exec). Every observed divergence
follows from that single constant. It is **not** a knife-edge, **not** a band
value / EMA / governor-selection difference (those match), and **not** a
freshness-bookkeeping *logic* difference (the code is line-identical, T1).

A Pine-semantics shadow run at `zoneMemory = 3` reproduces the deployed chart
**to the decimal** across three independent operator observations.

## T1 — freshness/tag bookkeeping, engine vs Pine (verbatim, structurally identical)

**ENGINE** (`engine/signals.py`, `engine/cells.py`):
```
cells.py:66     return 5 if self.tf_exec == "5m" else 3           # zone_memory (=5)
signals.py:318  tag_now = [_tag_now(z1_armed, z1Top[i], z1Bot[i]), ...]   # high>=zBot (short)
signals.py:321  fresh = [tag_now[k] and (tag_bar[k] is None or i - tag_bar[k] > zone_memory) ...]
signals.py:323-324  if any(fresh):  had_prime_ep = False
signals.py:332  if tag_now[k]: ... tag_bar[k] = i
signals.py:358-360  rec = [... i - tag_bar[k] <= zone_memory ...] ; active_zone = 3/2/1/0
signals.py:424  if prime_l or prime_s: ... had_prime_ep = True
```

**PINE** (`pine/SS_Cascade_v11.0.2.pine`, byte-identical to deployed capture):
```
121   zoneMemory = input.int(3, "Zone memory (exec bars a tag stays recent)", minval=1,
122        tooltip="Default 3. On a 5m execution chart, 5 is recommended (ADD §8).", ...)
431-433  tag1Now = z1Armed and (dir == 1 ? low <= z1Top : high >= z1Bot)   (+ tag2Now/tag3Now)
437-439  fresh1 = tag1Now and (na(tagBar1) or bar_index - tagBar1 > zoneMemory)   (+ fresh2/3)
440-441  if fresh1 or fresh2 or fresh3 \n     hadPrimeEp := false
443-454  if tag1Now: ... tagBar1 := bar_index   (+ tag2/3)
480-483  rec1 = z1Armed and not na(tagBar1) and bar_index - tagBar1 <= zoneMemory
         activeZone = rec3 ? 3 : rec2 ? 2 : rec1 ? 1 : 0
534-536  if primeL or primeS: ... hadPrimeEp := true
```

Same `>` (fresh), same `<=` (recency/expiry), same order, same tag detection.
**The only difference is the value of the memory constant: engine 5, Pine
input default 3.** Governor-bar selection is identical too — Pine
`request.security(tfGovern, expr[1], lookahead=lookahead_on)` (last closed
governor bar) = engine `map_htf_to_exec` (`gov_close <= exec_open`).

## Root cause reproduction — shadow(mem=3) == deployed chart

| observation (operator) | engine (mem=5) | shadow (mem=3) | chart |
|---|---|---|---|
| May 23 16:20 rc-40 PRIME | fires (activeZone=1, bars_since=4); stop→75534.56 | **skipped** (activeZone=0, zone expired at 4>3); stop stays 76769.67 | skipped |
| May 20–27 stop path | freezes at 75534.56 | 76769.67 → **76731.14 → 76569.81 → 75755.80** (step 05-27 09:15) | 76,772 → 76,731 → 76,569.8 → 75,755.8 (~09:10) |
| May 27 12:45 grade-C | fires | **skipped** (activeZone=0 at 12:40) | did not print |
| Jun 23 17:00/17:45/20:45 CONFIRMs | fire (hadPrimeEp=True) | **gated off** (03:50 fresh→hadPrimeEp=False) | flat stop |

**First divergent bar per window** (activeZone/bars_since/fresh/hadPrimeEp):
- (a) 2026-05-23 15:15 — `activeZone 1 vs 0`
- (b) 2026-05-27 12:40 — `activeZone 1 vs 0`
- (c) 2026-06-23 03:50 — `fresh False vs True; hadPrimeEp True vs False`

## T5 — band values & governor-bar selection (the reviewer's pivot): CLEAN

Traced gov9 / ATR_gov / Z1-bottom and the selected governor bar per exec bar.
The governor edge steps at exactly the right exec bar (Jun 23 **04:00** rollover:
gov bar 06-22 20:00 → 06-23 00:00; Z1-bottom 64035.19 → 64003.62), and the
values are deterministic and match Q4d and the operator's 0.01-pt hover. **The
bands and governor selection are identical; the fork is not here.** This
*confirms* the reviewer's band hypothesis is negative and isolates zoneMemory.

## T4 — blast radius, engine(5) vs shadow(3), full dev window (2025-10-06 → 2026-07-07)

```
PRIME    removed  : 6
CONFIRM  removed  : 12
CONFIRM  regraded : 2      (C <-> add)
TOTAL changed entry/exit signals : 20   (18 removed, 2 regraded, 0 added)
by month (removed): 2025-10:1  11:1  12:2  2026-01:1  02:6  03:2  05:2  06:3
regraded: 2026-05: 2
stop-divergent bars: 4,360   (10:294 11:20 12:231 02:1152 03:747 05:1509 06:407)
```
Direction is one-way: the mem=3 chart **loses** entries the mem=5 engine takes
(fewer active-zone bars, more hadPrimeEp resets) — never gains. 20 signal
changes and 4,360 stop-divergent bars over ~9 months.

## Fix framing (for reviewer ruling — NOT taken here)

The engine and the Pine **logic** are correct and identical; the parity journal
(truth) uses `zoneMemory = 5`. So no engine logic change is warranted — an
"Engine 1.0.3" logic fix would be aimed at the wrong layer. The candidate
resolutions are config/doc:
1. **Operator sets `Zone memory = 5`** on the deployed 5m chart (one setting).
   This alone should restore parity — verify by re-checking May 23 16:20 /
   May 27 12:45 / Jun 23 17:00.
2. Change the **Pine input default 3 → 5** for the 5m line (a one-literal input
   change; note it alters behavior for anyone on "default inputs").
3. Fix the F6 sign-off note in `case_windows.md` ("with default inputs" →
   "with Zone memory = 5 on 5m").

## The one confirming measurement

Operator: open the deployed chart's **Inputs → Zone memory**. If it reads **3**,
this is closed. (The shadow already matches the chart at 3 to the decimal.)
