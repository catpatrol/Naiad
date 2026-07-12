# SSv12 — Spec Errata

Standing register of confirmed spec/behavior contradictions surfaced during
the SSv11 → SSv12 work. Each entry cites the source line, states the
contradiction, and records disposition. Behavior is **not** changed by an
erratum entry (that is a named-variant decision at SSv12 spec time); the
entry documents reality so the spec and playbook stop lying about it.

---

## E-1 — Provisional (Stage-1) campaigns arm Z2, not just Z1

**Status:** CONFIRMED · opened 2026-07-11 (SSv11.3 build) · disposition deferred to SSv12 spec.

**Contradiction.** The design spec §4.2 states *"Stage 1 arms Z1 only,"* and the
earlier playbook glyph row read the Z2 band as a *Stage-2-only* entry zone. The
shipped engine and the committed Pine both arm **Z1 *and* Z2** the moment any
governor cross opens a campaign — including a provisional (counter-structure,
Stage-1) campaign — whenever the `provZones` variant is at its default
`"Z1+Z2"`. A provisional campaign therefore fires **Z2-labeled entries**, capped
at grade **B**, before the 89×200 stage ever confirms.

**Source line (committed `SS_Cascade_v11_0_2.pine`):**

```
line 428:  z2Armed = dir != 0 and (not campCounter or provZones == "Z1+Z2")   // ADD §1
line  99:  provZones = input.string("Z1+Z2", "Provisional campaign zones", ...)  // default
```

When `campCounter` is true (provisional/Stage-1), `not campCounter` is false, so
`z2Armed` reduces to `provZones == "Z1+Z2"` — true by default. Z2 is armed. The
arming was introduced by the v11.0.2 verification-addendum patch (ADD §1,
"ARMING TIERS"), whose banner explicitly documents "zones per the `provZones`
variant input (default Z1+Z2)."

**Z3 status (checked, for completeness).** Z3 is **NOT** likewise armed under a
provisional campaign:

```
line 426:  stageAligned = dir == 1 ? gS2B : dir == -1 ? gS2S : false
line 429:  z3Armed = dir != 0 and stageAligned                                 // Z3 needs stage
```

In a Stage-1 campaign `stageAligned` is false, so `z3Armed` is false regardless
of `provZones`. The operator's worry — that a provisional **Z3** entry could
fire from a band hidden in Stage 1 — does **not** occur in the committed source:
Z3 entries require stage alignment, at which point the campaign is no longer
provisional and the Z3 band is shown. Only **Z2** is the provisional-arming
surprise. *(This holds for the committed Pine and the engine; the deployed
chart's Z-arming has not been independently re-verified against a captured
source — see D0.)*

**Evidence.**
- Operator tint check 2026-06-16 (faint green / provisional tint) confirmed
  deployed v11.0.2 firing Z2-labeled PRIMEs inside a Stage-1 campaign.
- Engine parity journal (`v11_faithful`, BTCUSDT_swing): provisional-stage
  campaigns carry Z2 PRIME/CONFIRM rows.

**Disposition (deferred to SSv12 spec).** Named-variant candidate
**`provisional-Z1-only`**: at spec time, decide whether the DS-literal "Z1 only"
(`provZones = "Z1 only"`) becomes the sealed default, or the current `"Z1+Z2"`
is ratified as intended. Until then behavior is **unchanged** (invariant I6 of
the SSv11.3 build): v11.3 corrects the *documents*, not the arming.

**Doc corrections applied 2026-07-11 (SSv11.3 build, D6):**
- `SSv11_Execution_Playbook_v1_1.md` §3 zone-bands cue row — E-1 pointer added.
- `SSv11_Execution_Playbook_v1_1.md` §4 Z2 glyph-dictionary row — E-1 citation +
  "grade ceiling B" made explicit.
- The design spec §4.2 ("Stage 1 arms Z1 only") remains the authoritative text
  to amend at SSv12 spec time per the disposition above.
