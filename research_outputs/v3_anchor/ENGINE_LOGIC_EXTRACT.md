# V3 Anchor — Engine Logic Extract (read-only forensics)

**Scope.** Verbatim extraction of the naiad engine's stop, ratchet, exit-journaling,
shadow, flag, and harvest logic, in plain terms with `file:line` references. No code was
changed and nothing was run — this is a static read of the source only.

## Provenance

| Item | Value |
|---|---|
| Commit | `2f260e1` — "engine 1.0.7: gate tranche-cap sibling projection (G-6, ratified)" |
| Engine version | `1.0.7` (`engine/version.py:3`) |
| Verified identity | `git diff 2f260e1 HEAD -- engine/ configs/` is **empty**, and the working tree is clean for those paths. The line numbers below (working-tree reads) are therefore exact for `2f260e1`. |
| Run configs | `configs/v12_anchor.yaml` (signal section byte-identical to `v11_faithful`; **trading + shadows** byte-identical to `naiad_v0`) and `configs/naiad_v0.yaml` for reference. |
| Config loader | `engine/config.py:17` — a single YAML file per `config_id`; **no inheritance/merge machinery**. `v12_anchor.yaml` is self-contained; the "byte-identical" relationships are maintained by hand (per its header comment) and confirmed by inspection. |

### The one architectural fact that governs Q1–Q3

**All real stop *placement* and *ratchet* logic lives in `engine/signals.py`, not `engine/trading.py`.**
The signal layer computes two per-direction ratchet series, `stop_long` / `stop_short`
(`signals.py:71–72`, `605`). The trading layer never computes, seeds, or advances a stop.
It only:

- **reads** the working stop for a bar — `stop_level(i, d)` returns `sig.stop_long[i-1]` /
  `sig.stop_short[i-1]` (`trading.py:214–218`);
- **captures** the entry value — `stop_now = sig.stop_long[i] ...` at the signal bar
  (`trading.py:461`), stored as `stop_at_signal` → `stop_at_entry`;
- **fills** against the series and **journals**.

So Q1 ("placement rule") and Q2 ("code paths that move a stop") are answered almost
entirely from `signals.py`. Two further consequences that matter downstream:

1. The real stop is a **single per-direction series shared by the whole campaign/direction
   run** — it is *not* per-tranche. Every open tranche in a direction reads the same
   `stop_level`, so a stop hit or a flatten closes **all** open tranches together
   (`trading.py:389–399`, `328–343`).
2. The real ratchet is **not** price/MFE-trailing. It advances **only when a new entry
   event fires** (PRIME / CONFIRM / V). Between entry events the live stop is static. The
   only trailing construct in the codebase (e200 trail) is a **shadow** (X-A), never the
   traded book.

---

## 1. INITIAL STOP — placement rule per entry kind

There is **one** placement formula, in the "Ratchet stop on PRIME / CONFIRM / V" block
(`signals.py:472–482`), and **all three entry kinds use it identically**:

```python
# signals.py:473–482
entry_l = ((prime_l or confirm_l) and dir_ == 1) or cap_l
entry_s = ((prime_s or confirm_s) and dir_ == -1) or cap_s
if entry_l:
    new_stop = l[i] - stop_buf * atr_x[i]
    stop_long = new_stop if isnan(stop_long) else max(stop_long, new_stop)
    last_sig_bar = i
if entry_s:
    new_stop = h[i] + stop_buf * atr_x[i]
    stop_short = new_stop if isnan(stop_short) else min(stop_short, new_stop)
    last_sig_bar = i
```

**Anchor bar.** The **signal (trigger) bar itself**, bar `i` — the closed bar on which the
PRIME / CONFIRM / V event fires. Not a prior bar.

**Extreme.** The signal bar's **own** low (`l[i]`, long) or high (`h[i]`, short).

**Buffer formula.**
- Long: `stop = l[i] − stop_buf · ATR_exec[i]`
- Short: `stop = h[i] + stop_buf · ATR_exec[i]`
- `stop_buf = p["stop_buf_atr"]` (`signals.py:172`) = **0.5** in all three configs
  (`v12_anchor.yaml:36`, `naiad_v0.yaml:34`, `v11_faithful.yaml:35`).
- `atr_x` = exec-TF Wilder ATR(14) (`signals.py:119`; `atr_len: 14`).

**Per-kind differences: none, for placement.** R1 PRIME, R2+ PRIME (ADD), CONFIRM add, and
V all seed/advance the *same* `stop_long`/`stop_short` variable with the *same* formula. The
"kind" (R1 / ADD / V) affects **sizing** (`trading.py:144–155`, `size_for`) and gating, **not**
the stop level. What actually differs between an R1 and a later ADD is only *which bar's*
low/high+ATR the shared ratchet last latched to — and, because the update is one-way
(below), a later same-direction entry can only tighten it, never loosen it.

**How a tranche inherits its initial stop.** At fill-queuing (`trading.py:461`) the engine
reads the series value *at the signal bar*:
`stop_now = sig.stop_long[i] if ev.dir == 1 else sig.stop_short[i]`. That becomes
`PendingEntry.stop_at_signal` (`trading.py:488`) → `Tranche.stop_at_entry` (`trading.py:377`).
So a tranche's "initial stop" is the campaign ratchet **as of its own signal bar** — which,
for the first tranche, is that bar's `low − 0.5·ATR`, and for a later add is the tightened
shared value.

**Mandate / TF dependence.** The stop uses **exec-TF** low/high and **exec-TF** ATR only.
No governor/HTF term enters the stop formula. `stop_buf_atr` is a signal-section parameter
(0.5), identical across all three configs; there is no per-mandate or per-tier variation of
the buffer.

**Minimum-distance floor: NONE.** There is no clamp that widens a too-tight stop. A grep
over `engine/` for floor/clamp/min-distance constructs finds only: funding-hour rounding,
the warm-up history floor, the LIT data-start floor, the `max(0.0, …)` that clamps *negative*
risk to zero in `open_risk_r` (`trading.py:258`), and the ratchet's own one-way `max`/`min`
(`signals.py:477`,`481`) — none of which is a minimum stop-distance. The only distance-aware
guard is a **rejection**, not a floor: at fill time, if `unit_risk = (fill_px − stop)·dir ≤ 0`
the entry is dropped as `gap_through_stop` (`trading.py:363–366`); and a NaN series value is
dropped as `no_stop` at signal time (`trading.py:462–464`). Neither adjusts the stop.

---

## 2. RATCHET — every path that moves, clears, or re-places a stop

### 2a. The only path that MOVES (tightens) a stop

`signals.py:475–482` (quoted above). One-way by construction:
`stop_long = max(stop_long, new_stop)` / `stop_short = min(stop_short, new_stop)`.

- **Triggers** (`entry_l` / `entry_s`, `signals.py:473–474`):
  - **PRIME** — `prime_l`/`prime_s`, any `r_count` (both R1 and R2+ adds).
  - **CONFIRM** — `confirm_l`/`confirm_s`, which covers both PRIME-backed confirm-adds and
    stand-alone grade-C confirms (`signals.py:428–429`).
  - **V** (capitulation) — `cap_l`/`cap_s`.
  - **Not** triggered by price, MFE, favorable excursion, time, or TPW. There is no
    price-based trailing of the real stop.
- **Step target formula:** identical to the initial placement — `low − 0.5·ATR` (long) /
  `high + 0.5·ATR` (short) at the *triggering* bar.
- **Buffer:** `stop_buf_atr` = 0.5 × exec-ATR(14).
- **Monotonicity:** enforced in-line by `max`/`min` (invariant 5, "na-safe, one-way").

### 2b. Paths that CLEAR a stop (set to NaN) or RE-SEED a direction

A stop series is set back to `NaN` **only on a direction change or death** — never on a
same-direction event:

| Path | Line | Effect |
|---|---|---|
| Arm long (`arm_bull`) | `signals.py:276` | clears **`stop_short`** (opposite side). Leaves `stop_long` intact. |
| Arm short (`arm_bear`) | `signals.py:291` | clears **`stop_long`**. Leaves `stop_short` intact. |
| V long (`cap_l`) | `signals.py:447` | clears **`stop_short`**; the V is itself an `entry_l`, so it re-seeds `stop_long` at `475–478`. |
| V short (`cap_s`) | `signals.py:462` | clears **`stop_long`**; re-seeds `stop_short`. |
| Failure-X long (`fail_l`) | `signals.py:504–506` | `dir_ = 0`, clears **`stop_long`** (campaign death). |
| Failure-X short (`fail_s`) | `signals.py:507–509` | `dir_ = 0`, clears **`stop_short`**. |

**Same-direction re-arm does NOT clear the stop.** `arm_bull` never touches `stop_long`
(only `stop_short`), and vice-versa. A same-direction governor re-cross increments
`campaign_seq` (`signals.py:271–272`, a new `campaign_id`) **but leaves the in-direction stop
in place**, where the next entry event ratchets it one-way. So the stop persists — and keeps
tightening — across same-direction campaign re-arms.

### 2c. Where is "never-loosen" enforced — per tranche, per campaign, or across re-arms?

Neither per-tranche nor per-`campaign_id`. Monotonicity holds **per direction-run**: the
`stop_long`/`stop_short` series is one-way for the entire life of a directional run — from the
first entry event after a direction change until the direction flips or dies — **including
across same-direction re-arms that mint new `campaign_id`s** (§2b). The series resets (to NaN,
then re-seeded by the next entry event) **only** when the direction changes (opposite arm,
opposite-direction V) or the campaign dies (failure-X). Within one continuous directional run
it can never loosen; a flip/death is a hard reset, not a loosening.

> Note — the trading layer holds this to account but does not create it: the
> stop-guarantee-and-repair step (`trading.py:308–318`) raises `GateViolation` if an open
> tranche ever has a `NaN` working stop with no queued flatten, and the one-bar
> death-transition is the sole exemption (G-3, `trading.py:310–312`).

---

## 3. EXIT-ROW `stop` FIELD — what value is journaled

First, how the exit price is captured. `close_tranche(tr, i, raw_px, reason)` sets
`tr.exit_raw_px = raw_px` (`trading.py:229`). It is called from exactly three sites:

| Exit site | `trading.py` | `raw_px` passed | `reason` |
|---|---|---|---|
| Flatten at open | `330` | `o[i]` (bar open) | `campaign_died` / `failure_x` / `opposite_cross` / `v_reversal` |
| Gap-through stop at open | `341` | `o[i]` (bar open) | `stop_gap` |
| Intra-bar stop | `397` | `stop` = `stop_level(i,d)` = `sig.stop_long[i-1]` | `stop` |

So `exit_raw_px` is **the price/level that actually filled**: for a clean intra-bar stop it is
the working ratchet level (`sig.stop_long[exit_i − 1]`, i.e. the stop confirmed at the prior
bar's close); for a gap or a flatten it is that bar's open.

Now the journal (`engine/replay.py`):

- **ENTRY_FILL / ADD_FILL** — `stop = f(tr.stop_at_entry)` (`replay.py:162`). **The tranche's
  original entry stop.**
- **STOP_FILL** — `stop = f(tr.exit_raw_px)` (`replay.py:178`). **The fill level** (stop level
  for `stop`; open for `stop_gap`).
- **EXIT** — `stop = f(tr.exit_raw_px if tr.exit_reason.startswith("stop") else None)`
  (`replay.py:191`).

**Answer for the EXIT row:** the value written is **the level that filled**, and only for
stop-type exits — `stop` or `stop_gap` (both pass `.startswith("stop")`). For every flatten
exit (`failure_x`, `opposite_cross`, `v_reversal`, `campaign_died`) the EXIT-row `stop` is
**null**. It is **never** the tranche's original `stop_at_entry` (that lives on the
ENTRY_FILL/ADD_FILL row), and it is **never** a post-bar-update ratchet state — for a clean
stop it is the pre-update working level `sig.stop_long[exit_i−1]` that the fill occurred at.

---

## 4. SHADOW DEFINITIONS (verbatim)

All shadows are computed per resolved tranche in `enrich_tranche` (`engine/shadows.py:144`)
and are **never traded** (module docstring `shadows.py:1–2`). Journaled under the `shadow`
column (fields listed at `journal.py:26–32`). Per-unit-R convention: shadow exit R is
`(exit − fill)/(fill − stop_at_entry)`, sign-adjusted (`_unit_r`, `shadows.py:89–91`);
multiply by `size_r` for campaign-R (`shadows.py:6–11`).

### 4a. `stop_alt_anchor` — alternate anchor, live buffer

Built by `_alt_anchor_series(sig, tr, entry_bars, stop_buf, atr_frozen=None,
trigger_offset=True, last)` (`shadows.py:219`; helper `120–141`).

- **Same entry events** as the real ratchet — `campaign_entry_bars[(campaign, dir)]` =
  every PRIME/V/CONFIRM bar of that campaign+direction (`shadows.py:271–278`).
- **Different anchor:** `trigger_offset=True` ⇒ `anchor_bar = max(0, e − 1)` — the bar
  **before** the entry event (the trigger/reclaim bar) rather than the event bar itself
  (`shadows.py:134`).
- Extreme: `ext = l[anchor_bar]` (long) / `h[anchor_bar]` (short) (`shadows.py:135`).
- **Buffer:** `atr_frozen is None` ⇒ `buf_atr = sig.atr_x[e]` — the **live** exec-ATR at the
  entry-event bar (`shadows.py:136`).
- Candidate: `cand = ext − d · stop_buf · buf_atr`, `stop_buf` = `cfg["signal"]["stop_buf_atr"]`
  = 0.5 (`replay.py:150`, passed in at `182`). One-way ratchet, `max`/`min` (`shadows.py:138`).
- **Update cadence:** at each entry-event bar in the campaign (same cadence as the real
  ratchet), from `fill_i − 1` onward (`shadows.py:129–131`).
- **Journaled scalar** `stop_alt_anchor` = the series value **at the tranche's fill bar**,
  `alt_anchor[tr.fill_i]`, 8 dp, or null if NaN (`shadows.py:244`).
- Its simulated exit R is journaled as `stop_alt_anchor_exit_r` (`shadows.py:223`,`246`).

### 4b. `stop_alt_volbuf` — real anchor, frozen buffer

`_alt_anchor_series(..., atr_frozen = sig.atr_x[entry_bars[0]], trigger_offset=False, ...)`
(`shadows.py:220–222`).

- **Same anchor as the real stop:** `trigger_offset=False` ⇒ `anchor_bar = e` (the entry
  bar's own extreme).
- **Frozen buffer:** `buf_atr = atr_frozen = sig.atr_x[entry_bars[0]]` — the exec-ATR at the
  **first entry bar of the campaign**, reused for every subsequent step (`shadows.py:136`).
- Candidate/ratchet identical otherwise; `cand = ext − d · 0.5 · atr_frozen`.
- **Journaled scalar** `stop_alt_volbuf` = `alt_volbuf[tr.fill_i]`, 8 dp, or null
  (`shadows.py:245`); exit R as `stop_alt_volbuf_exit_r` (`shadows.py:224`,`247`).

> Contrast in one line: **real** = entry-bar extreme + live entry-bar ATR;
> **alt_anchor** = *prior*-bar extreme + live ATR; **alt_volbuf** = entry-bar extreme +
> *campaign-frozen* ATR.

### 4c. `entry_alt` — first rib cross in campaign direction

`rib_cross[(campaign, dir)]` = the **first** exec-TF 9/89 EMA ribbon crossover in the
campaign direction: `crossover(e9x, e89x)` (long) / `crossunder(e9x, e89x)` (short), earliest
bar per campaign+dir (`build_shadow_context`, `shadows.py:280–291`). It models entering at the
ribbon cross instead of the PRIME/zone-reclaim trigger. Journaled (`shadows.py:229–233`):

- `entry_alt_px` = close at the rib-cross bar (`sig.c[alt]`, 8 dp).
- `entry_alt_t` = ISO-8601 UTC timestamp of that bar's exec open.
- `entry_alt_stop` = `ext − d · stop_buf · atr_x[alt]`, `ext = l[alt]`/`h[alt]` — the same
  `0.5·ATR` stop formula applied at the rib-cross bar.

### 4d. `exit_XA / XB / XC / XD` — candidate exit variants (per-unit R)

All four are **per-unit R** floats on the `shadow` column (`shadows.py:252–255`; docstring
`17–27`). Partials bank at the **open of the bar after** the trigger event, and are voided
(fall back to the X-A number) if that open would land after the X-A trail already exited
(`partial_r`, `shadows.py:198–201`).

- **`exit_XA`** (`shadows.py:181–185`,`252`; series `_xa_series`, `94–117`). Pure two-phase
  survival→trail: keep the native ratchet until a **closed** bar closes beyond the exec-200 on
  the trade side (`(c[j] − e200x[j])·d > 0`, engagement, `shadows.py:104`); from engagement,
  `trail = e200x[j] − d · buf · atr_x[j]` with `buf = xa_trail_buf_atr = 0.5`
  (`v12_anchor.yaml:64`), one-way, **closed bars only**, and never looser than the real
  ratchet (`shadows.py:113–115`). Exit found by `_sim_stop_exit` (`67–86`). `exit_XA = xa_r`,
  the per-unit R of that exit.
- **`exit_XB`** (`shadows.py:205–206`,`253`). X-A **+ bank 50% at the next open after the
  first TPW**: `xb_tpw_partial·tpw_r + (1 − xb_tpw_partial)·xa_r`, `xb_tpw_partial = 0.5`. No
  TPW ⇒ `= xa_r`.
- **`exit_XC`** (`shadows.py:207–208`,`254`). X-A **+ bank 50% at the next open after the
  first extension** (a close `≥ xc_ext_atr · ATR = 2.0·ATR` beyond exec-9 on the trade side,
  `shadows.py:190–193`): `xc_partial·ext_r + (1 − xc_partial)·xa_r`, `xc_partial = 0.5`. No
  extension ⇒ `= xa_r`.
- **`exit_XD`** (`shadows.py:209–215`,`255`). Mechanized Playbook stack: **25% at first TPW**
  (`xd_tpw_partial = 0.25`), **25% at first extension** (`xd_ext_partial = 0.25`), **remainder
  on the X-A trail / campaign death**. `xd_r = Σ fraction·R` over whichever legs occurred plus
  the residual on `xa_r`.

Config values (`v12_anchor.yaml:61–72`, identical in `naiad_v0.yaml:61–72`): `xa_trail_buf_atr
0.5`, `xb_tpw_partial 0.5`, `xc_ext_atr 2.0`, `xc_partial 0.5`, `xd_tpw_partial 0.25`,
`xd_ext_partial 0.25`.

---

## 5. FLAGS — `engagement_flags`

The tranche-enrichment `engagement_flags` dict has **exactly three** members
(`shadows.py:257–261`):

```python
flags = {
    "xa_engaged_before_exit": bool(engaged_at is not None and engaged_at < xa[1]),
    "tpw_before_exit":        bool(tpw_i is not None),
    "ext_before_exit":        bool(ext_i is not None),
}
```

- **`xa_engaged_before_exit`** — True iff the X-A trail **engaged** (some closed bar closed
  beyond the exec-200 on the trade side; `engaged_at` from `_xa_series`, `shadows.py:104`)
  **before** the X-A exit bar (`engaged_at < xa[1]`). I.e., did the survival→trail transition
  occur before X-A closed the trade.
- **`tpw_before_exit`** — True iff a first TPW occurred in-campaign after fill (`tpw_i is not
  None`, where `tpw_i = tr.first_tpw_i` if `≤ campaign end`, `shadows.py:188`). `first_tpw_i`
  is stamped in the trading layer on the first TPW event matching the tranche's direction
  while it is open (`trading.py:411–415`).
- **`ext_before_exit`** — True iff a first extension bar existed in-campaign (`ext_i is not
  None`) — a closed bar `≥ 2·exec-ATR` beyond exec-9 on the trade side (`shadows.py:190–193`).

**No other flags exist in the enrichment set.** One namesake to avoid confusing with these:
**REGIME** signal rows carry a *separate* `engagement_flags = {"arrow_visible": …}`
(`replay.py:141–142`) recording the whipsaw arrow filter (`signals.py:242–247`); it is a
REGIME-row field, unrelated to tranche engagement, and arrows of other event types are `None`
there unless enriched.

---

## 6. HARVEST — is there any partial-exit / take-profit path in `trading.py`?

**Refuted. No partial-exit or take-profit path exists anywhere in `engine/trading.py`.**

- The sole exit routine, `close_tranche` (`trading.py:220–237`), always closes the **full**
  tranche: it prices `tr.qty` in full, sets `tr.exited = True`, and records a single
  `exit_px`/`exit_reason`. There is no quantity reduction — `tr.qty` is written once at entry
  (`trading.py:369`,`376`) and never decremented, scaled, or split. A grep of `trading.py`
  for `partial | take-profit | tp | bank | scale | harvest | qty -= | qty *= | .qty =` returns
  **no matches**.
- Every one of the three `close_tranche` call sites is immediately followed by
  `open_tranches.clear()` (`trading.py:331`, `342`, `398`) — so any exit trigger flattens the
  **entire** open set, not a fraction of one tranche.
- The complete set of exit reasons is: `campaign_died`, `failure_x`, `opposite_cross`,
  `v_reversal` (full-campaign flattens), `stop_gap`, and `stop`. None is a take-profit.
- The **TPW** event in the trading layer only stamps `first_tpw_i` and `continue`s
  (`trading.py:410–415`) — it triggers **no** exit. TPW/extension "banking" exists **only** as
  non-traded shadow arithmetic in `exit_XB / XC / XD` (`shadows.py`, §4d).

The real book is strictly all-or-nothing per tranche, and in practice all tranches in a
direction exit together on one shared stop or one flatten.

---

## Appendix A — parameter values used (v12_anchor / naiad_v0)

| Parameter | Value | Source | Used at |
|---|---|---|---|
| `stop_buf_atr` | 0.5 | `v12_anchor.yaml:36` | real stop, `signals.py:476/480`; alt-shadows & entry_alt via `replay.py:150` |
| `atr_len` | 14 | `:11` | `signals.py:119` |
| `xa_trail_buf_atr` | 0.5 | `:64` | X-A trail, `shadows.py:181`→`_xa_series:109` |
| `xb_tpw_partial` | 0.5 | `:66` | `shadows.py:205` |
| `xc_ext_atr` | 2.0 | `:68` | extension test, `shadows.py:191` |
| `xc_partial` | 0.5 | `:69` | `shadows.py:207` |
| `xd_tpw_partial` | 0.25 | `:71` | `shadows.py:211` |
| `xd_ext_partial` | 0.25 | `:72` | `shadows.py:213` |
| `max_tranches` | 3 | `:51` | cap, `trading.py:268/458` |
| `max_open_campaign_risk_r` | 1.0 | `:52` | risk rail, `trading.py:287/482` |

**Signal divergence in v12_anchor:** `v_births_provisional: false` (`v12_anchor.yaml:39`,
inherited from Pine v11.0.2 / `v11_faithful`) vs `naiad_v0`'s `true`. This changes only the
**tier** a V campaign is born at (`camp_counter` at `signals.py:446/461`), i.e. V sizing/zone
classification — **not** any stop-placement or ratchet formula.

## Appendix B — read-only attestation

No files under `engine/` or `configs/` were modified and the engine was not executed. The
only write performed for this task is this document. Evidence base: static reads of
`engine/{trading,signals,shadows,journal,replay,config,version}.py` and
`configs/{v12_anchor,naiad_v0,v11_faithful}.yaml` at commit `2f260e1`, confirmed
byte-identical to the working tree for those paths.
