# D0 — v11.0.2 delta report (SSv11.3 §1a) — CLOSED

**Date opened:** 2026-07-11 · **Delta computed:** 2026-07-11 (capture received).
Builder: Claude Code · for reviewer ruling on the 2026-06-23 parity break.

---

## 0. Result — the delta is EMPTY. Deployed ≡ committed.

The operator's deployed capture `pine/SS_Cascade_v11.0.2.pine` is **byte-for-byte
identical** to the committed project copy `SS_Cascade_v11_0_2.pine`:

```
sha256  0ade9d0104fd3e45545299ff2bfea95fb2708cb0ab51c374c7c0792bdc31c4d7  SS_Cascade_v11_0_2.pine
sha256  0ade9d0104fd3e45545299ff2bfea95fb2708cb0ab51c374c7c0792bdc31c4d7  pine/SS_Cascade_v11.0.2.pine
```

`cmp` reports no differences; `diff -u` is empty; both are 57718 bytes / 933
lines / CRLF. **There is no delta of any kind — not in CONFIRM gating, not in
zone arming, not anywhere.**

## 1. H1 verdict — REFUTED at the source level

> **H1 (reviewer):** deployed v11.0.2 zone-gates the CONFIRM trigger; the engine
> implements the older *ungated* form, making the engine the deviant.

**REFUTED.** The deployed source does **not** zone-gate CONFIRM. Its trigger is
the same ungated form the engine implements. **CONFIRM trigger (deployed,
identical to committed):**

```
line 510  confirmXL = dir == 1  and ribUp and coolOK          // raw re-cross, NO zone term
line 511  confirmXS = dir == -1 and ribDn and coolOK
line 543  gradeCL  = confirmXL and not hadPrimeEp and structOKL and activeZone > 0
line 544  gradeCS  = confirmXS and not hadPrimeEp and structOKS and activeZone > 0
line 545  confirmL = (confirmXL and hadPrimeEp) or gradeCL     // <-- add branch has NO activeZone term
line 546  confirmS = (confirmXS and hadPrimeEp) or gradeCS
```

The add branch `confirmXL and hadPrimeEp` carries no `activeZone` term, so it
fires with `activeZone == 0` (zone `"-"`). The diamond draws and the stop
ratchets on those zoneless adds (deployed, identical):

```
line 744  plotshape(confirmL and not gradeCL, "Confirm Long",  shape.diamond, ..., size=size.tiny)
line 824  if confirmL
line 825      alert(f_json("CONFIRM", "long", gradeCL ? "C" : "-", rCount, zoneStr, stopLong, ...))
```

The engine is **not** the deviant. The deployed Pine, the committed Pine, and the
engine all agree: zoneless CONFIRM adds fire, draw, and ratchet.

## 2. Zone-arming lines (deployed, identical to committed) — E-1 stands

```
line 426  stageAligned = dir == 1 ? gS2B : dir == -1 ? gS2S : false
line 427  z1Armed = dir != 0
line 428  z2Armed = dir != 0 and (not campCounter or provZones == "Z1+Z2")   // arms Z2 provisional
line 429  z3Armed = dir != 0 and stageAligned                                 // Z3 needs stage
line  99  provZones = input.string("Z1+Z2", ...)                             // default
```

- **Z2** armed in provisional campaigns by default (line 428) — erratum **E-1**,
  unchanged by the capture.
- **Z3** not armed provisionally (line 429).

## 3. §1a expected-delta rule — resolved

The rule anticipated a CONFIRM zone-gate delta (H1) as EXPECTED. **That delta
does not exist.** The stop rule (STOP only for out-of-scope logic deltas) is
moot — there are zero deltas.

## 4. So what caused the 2026-06-23 parity break?

The break is real (the deployed chart's stop line stayed flat and printed no
glyphs at 17:00 / 17:45 / 20:45, while the engine ratcheted
62590.61 → 62586.80 → 62490.50). But it is **NOT a source-logic difference** —
the sources are identical. The cause is therefore **operational/environmental**,
in the deployed chart's *runtime state*, not its code. Candidate causes for the
reviewer/operator to rule out, roughly in order of likelihood:

1. **Stale chart instance** — the chart was running an older compiled copy
   (pre-addendum bytecode) and was never re-added/recompiled after the v11.0.2
   ADD §1/§2 patch. Most likely: the code on disk is current, the code *on the
   chart* was not.
2. **Non-default inputs on the deployed chart** — e.g. `provisionalArming` OFF,
   a different `provZones`, `structureGate`, `cooldownBars`, `zoneMemory`, or a
   different governor TF — any of which changes whether/when `hadPrimeEp` is set
   and thus whether the re-crosses classify as adds. (The engine ran defaults.)
3. **Chart context mismatch** — symbol (BTCUSDT.P vs BTCUSDT), exec interval
   (not 5m), or chart timezone not UTC, so the "same" bars weren't the same.
4. **Campaign-state divergence upstream** — if the deployed chart had a
   different `dir`/`hadPrimeEp`/`rCount` entering 2026-06-23 (e.g. it missed an
   earlier arming or PRIME), the 17:00/17:45/20:45 re-crosses would not satisfy
   `confirmXL and hadPrimeEp` and would correctly print nothing. The divergence
   would then trace to an *earlier* bar, not the CONFIRM logic.

**Recommended next probe (separate contract):** have the operator confirm the
deployed chart's inputs are defaults and that it was re-added after the addendum
patch, then walk the deployed chart backward from 2026-06-23 to the first bar
where its state (dir / rCount / stop / last glyph) diverges from the parity
journal. That first-divergence bar — not the CONFIRM trigger — is the true
break origin.

## 5. Engine action

**None.** H1 is refuted, so there is no engine deviance to fix; the "Engine
1.0.3 fix" contemplated by the SSv11.3 contract is **not** warranted. Any fix, if
one proves needed, targets the deployed chart's runtime/config, not engine code
and not the Pine source (which is correct and current). Per contract §6, no
engine or Pine logic change is taken here.
