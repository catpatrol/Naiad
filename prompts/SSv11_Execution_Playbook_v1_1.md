# Secret Sauce — Cascade v11 · EXECUTION PLAYBOOK
### The discretionary trader's manual · v1.1 · 2026-07-08 · aligned to SS_Cascade_v11.0.2
Companion to `SS_Cascade_v11.pine` ≥ v11.0.2 (arming tiers, re-anchored sniper,
gated C, standing EMA colors). Grounded in the Oct 2025 → Jul 2026 BTC study and the
Dec-'25/May-'26 verification cycle. Where this document and older versions differ,
this one is current.

---

## 1. What this system is

One sentence: **the governor timeframe picks the fight, the zones pick the location,
the execution timeframe picks the moment.**

A 9/89 regime cross on the governor (default 4H) *arms* a campaign. Price returning
into a governor-EMA zone makes a trade *possible*. A 5m reclaim of its own 9 EMA with
a confirming close (PRIME) makes it *actual*. Structure (89 vs 200) no longer decides
*whether* you trade — it decides **how big and how deep**: aligned campaigns get full
zones and full grades; provisional campaigns get shallow zones, a B-cap, and half
size. Everything else on the chart is management (stops, TPW, X) or context.

### The Five Laws

1. **Never enter at the triangle.** Every cross in the study printed 30–60% into its
   impulse — buying the arrow buys the snap-back. The arrow arms; the retest pays.
2. **No zone, no trade.** If price is not inside a colored band, there is nothing
   to do.
3. **Respect the structure tier.** Solid arrow / deep tint = full campaign. Faded
   arrow / faint tint = **provisional**: Z1+Z2 only, grade ceiling B, half size. The
   tier is a throttle, not a wall — Jun 14–16 '26 returns as one half-size B loss;
   May 26 and Jul 2 '26 return as the marquee wins. That trade-off is the design.
4. **The stop lives just beyond the zone extreme, never wider.** If that stop feels
   far away, the entry came late — skip; the next zone tag is coming.
5. **Armed means patient.** Arming has no expiry. The marquee short armed May 16 and
   paid May 26 — nine days later, at the governor-89 zone, with near-zero heat for
   ~18,000 points of favorable movement. Waiting is a position.

---

## 2. Chart setup

- Default mandate: chart **5m**, Governor input **240**. Alignment TF: 1H (default).
- Other mandates: **1H governor / 1m chart** — optional intraday mandate, run at
  **half risk and only in trending regimes** (it out-harvests two-sided trends but
  pays 3–4× the chop tax; set alignment TF 15m, `snipeLookback` ≥ 89). **12H
  governor / 15m chart** — position mandate (alignment TF 4H). Instances don't
  interact; the 12H is context, never a gate.
- First-run defaults: `provisionalArming` ON, structure tiers active, sniper ON
  (pocket 0.5–0.786, re-anchored), V ON, TPW ON, `zoneMemory` 5 on the 5m.
- Style tab overrides remain available; project-standard line colors below.

## 3. Reading the chart state in five seconds

| Cue | Meaning |
|---|---|
| **Background tint** | Governor regime (green bull / red bear). **Deep shade = stage-aligned** (89 across the 200): full campaign. **Faint shade = provisional** (Stage 1): campaign live but throttled. |
| **Zone bands** | Amber **Z1** (gov 9) and purple **Z2** (gov 89) arm with **every** campaign; cyan **Z3** (gov 89–200 band) appears/arms only when stage-aligned. Bands visible ≠ armed — arming needs a live campaign (dir ≠ 0). *Provisional (Stage-1) campaigns arm **Z2**, not just Z1 — see erratum **E-1** (SSv12_SPEC_ERRATA.md); those entries are real but grade-capped at **B**.* |
| **Stop step-line** | Green below price = live long campaign with entries printed; red above = live short. No line = no entries yet (machine may still be armed and waiting). |

| What you see | State | Your job |
|---|---|---|
| Solid arrow + deep tint flip | ARMED (full) | Nothing. Wait for a zone tag. |
| **Faded arrow + faint tint flip** | **ARMED (provisional)** | Same wait — but pre-commit to half size, Z1/Z2 only, grade ≤ B. |
| Tint flipped, no arrow visible | Armed silently (whipsaw filter hides arrows only) | Trust the tint, not the arrow. |
| "89x200" dot during a live campaign | **Stage confirm — campaign upgrades** | Z3 unlocks, grade cap lifts, size normalizes on *new* signals. |
| Price entering a band | ZONE ACTIVE | Watch the 5m 9. The only moment needing your eyes. |
| Grade circle (A+/A/B) | ENTERED (R1) | Execute §5. |
| Tiny circles / diamonds after R1 | SCALING | Add per §6, ratchet stop. |
| TPW / X / opposite arrow | DEFENSE / DEATH | §7. Never negotiate with an X. |

## 4. Glyph dictionary

**Lines & fills**

| Glyph | Look | Meaning |
|---|---|---|
| Exec 9 EMA | **yellow** line | The trigger line: PRIME = reclaim + confirming close. |
| Exec 89 EMA | **purple** line | CONFIRM = 9 re-crossing this toward the campaign. (Purple = 89-family, matching the Z2 band.) |
| Exec 200 EMA | thin **blue** line | Context on the exec chart. |
| Z1 band | amber | Gov-9 zone (±0.25 gov-ATR). Trend-rider add zone. Armed in every campaign. |
| Z2 band | purple | Gov-89 zone (±0.35). **The campaign entry zone — armed in every campaign, provisional (Stage-1) included** per erratum **E-1** (SSv12_SPEC_ERRATA.md): entries there are real, grade ceiling **B** (v11.0.2). |
| Z3 band | cyan | Gov 89–200 band (±0.35 pad). Deepest, highest-quality zone; stage-aligned campaigns only. Ribbon-compression filter waived here. |
| Stop line | green/red step | Ratcheting risk floor: signal-bar extreme ∓ 0.5 exec-ATR; only tightens. Reference, not an order. |
| Background | 4 shades | Regime × tier (see §3). |

Bands/tint step once per governor bar and lag one bar — confirmed-bar, zero-repaint
discipline. On a 4H governor expect up to 4h of acknowledgment lag; that is the
price of webhook-safe signals.

**Event glyphs**

| Glyph | Look | Meaning | Action |
|---|---|---|---|
| Solid ▲/▼, normal size | green/red | Stage-aligned governor cross → full campaign armed | Wait for zone tag |
| **Faded small ▲/▼** | pale | **Provisional campaign armed** (cross before 89×200 agrees) | Wait for Z1/Z2 tag; half size, B-cap |
| "89x200" tiny dot | dark green/red | Stage confirm; live campaign upgrades | Expect Z3 + A/A+ from here |
| **A+ / A / B circle** | bright green below (long) / bright pink above (short) | **R1 — first PRIME, graded** | The trade. §5 |
| Tiny unlabeled circle | muted green / orange | R2+ later PRIMEs | Add. §6 |
| Tiny diamond | yellow / amber | CONFIRM (exec 9/89 re-cross) | Add if positioned; late entry only with structure+zone checked |
| "C" label | yellow/amber | CONFIRM with no PRIME this episode — **now zone- and structure-gated in code; on probation** | Missed-R1 recovery only; journal it |
| "V" arrow | blue ↑ / violet ↓ | Tightened capitulation reversal (gate-exempt trend birth) | §8 |
| "TPW" flag | amber, exit side | ≥2 of {5m,1H,4H,12H} crossed against the campaign within 12 bars | Partials / tighten. §7 |
| "X" xcross | orange, **plots on the far side of the failure bar** (above a failed long, below a failed short — v11.0.2 flip) | Campaign death: 3 exec closes beyond far band edge | Flat. Immediately |
| Tiny dark ▲/▼ + TF text | 5m/1H/4H/12H | MTF telemetry (chart TF suppressed) | Context + TPW inputs; never entries |

## 5. THE IDEAL ENTRY

### 5.1 The shape
1. Governor cross (solid or faded) — armed. 2. Price pulls back into an armed zone;
the 5m is below its 9 (that *is* the pullback). 3. Inside the zone, a 5m close
reclaims the 5m 9 and the **next** close confirms — the grade circle prints there.
4. Stop just beyond the zone-tag extreme (the printed line does the arithmetic).
5. Price leaves the zone; heat, when the setup is right, is a handful of 5m bars.

### 5.2 Grades (v11.0.2 definitions)
- **A+** — stage-aligned campaign; the zone-tag extreme landed inside the
  **re-anchored sniper pocket (0.5–0.786 of the impulse leg, terminus frozen at the
  first Z2/Z3 tag) ∩ the zone**. Three signals, one entry. Full size.
  *(Old-anchor A+ prints like Dec 30 '25 — shallow chop snap-backs — no longer
  qualify; that was the point of the re-anchor.)*
- **A** — stage-aligned campaign, PRIME in zone, **alignment TF** (one step below
  the governor: 4H→1H, 1H→15m, 12H→4H) agreeing. Full / near-full size.
- **B** — PRIME in zone on a **provisional** campaign (hard ceiling), or aligned
  campaign without alignment-TF agreement. **Half size.**
- **C** — gated CONFIRM-only late entry. Smallest size or skip; probation until
  30–50 journaled events prove it.
- Zone quality at equal grade: **Z3 > Z2 > Z1** for initiation; Z1 is the add zone.

### 5.3 Entry checklist (60 seconds)
1. Tint: direction and **depth** (full or provisional? → size decision made now).
2. Arming on record (arrow or tint flip)? 3. Which band, ideally Z2/Z3?
4. Grade circle on a confirming close? 5. Stop distance in R — size accordingly
(B/provisional = half). 6. MTF triangles stacking against? 7. Fill near the signal
close; never chase — the next tag is the trade.

### 5.4 Not the ideal entry
- The arrow itself (Law 1). Anything outside a band (Law 2).
- **Full size on a faded-arrow campaign** — the Jun 14–16 archetype now costs half
  a unit by design; don't make it cost a full one.
- A "C" without checking location and tint yourself, gate notwithstanding.
- Fresh entries after stage *de-aligns* mid-campaign (PRIMEs go silent by design;
  manage holdings, add nothing).

## 6. Scaling (R2+, CONFIRM, ratchet)
Unchanged mechanics: each later zone-tag PRIME prints a tiny circle, the stop
ratchets to the new signal bar's extreme ∓ buffer, campaign risk stays constant or
shrinks as size grows. New in v11.0.2: a mid-campaign **89×200 stage confirm
upgrades the live campaign** — Z3 tags become valid adds and new PRIMEs can grade
A/A+; bring subsequent adds up from half to full unit. CONFIRM diamonds remain
adds-for-the-positioned, never the preferred initiation. R1 = full planned risk
unit (halved when provisional); adds ≤ the initial unit, each only while prior
tranches sit at/beyond breakeven after the ratchet.

## 7. THE IDEAL EXIT (unchanged ladder)
1. **TPW → take partials** (25–50%), pull stop to the ratchet or tighter, stop
   adding. One TPW is information; two in a leg rarely forgive.
2. **Exec-9 trail** — extended trend + close back through the 5m 9 without a
   quick reclaim = discretionary partial/trail. (Still no glyph; read the yellow
   line. Candidate glyph in v11.1.)
3. **X or opposite solid arrow → flat on the close.** No averaging, no negotiation.
Profit rhythm: partial at TPW, partial into extension (≥ ~2 exec-ATR beyond the 9),
core runs until structure says done. The stop line is disaster insurance, not the
exit tool; the one sanctioned upgrade under evaluation is a breakeven jump at +1.5R.

## 8. Capitulation V
Mechanics unchanged (≥3.5× volume climax, ≥1 gov-ATR beyond the gov 89, far-band
reclaim ≤10 bars on ≥1.2× volume). Clarified: **V births a provisional campaign
unless stage is already aligned** — size like a B until the first ordinary PRIME or
a stage confirm upgrades it. Two true positives in nine months (Feb 6, Jun 22);
expect it to feel terrible to click — that's the trade.

## 9. Anti-patterns

| Window | What the chart showed | The lesson as now encoded |
|---|---|---|
| Dec 4–13 '25 | Arrow clusters, flat 89, price straddling the 200 | Faint tint + whipsaw filter + ribbon filter: provisional Bs at half size and mostly Z1 — expect scratch trading; sitting out remains correct |
| Jun 14–16 '26 | Faded bull arrow → tag into the overhead band → collapse | **Provisional campaign, capped**: one half-size B loss is the budgeted cost of catching every May-16/Jul-2-type birth |
| Any markdown | Green LTF triangles mid-crash | Counter-regime LTF signals bought 1–3 bars, every time. Telemetry, never entries |

Also: full size on provisional campaigns; stops wider than the ratchet; re-entry
after X before a fresh arming; judging C before its post-gate probation data exists.

## 10. Alerts, webhooks, journaling
One "Any alert() function call" alert = full JSON stream; or ten named
alertconditions for notifications. Schema now includes **`"retr"`** on PRIME —
the tag-extreme's retracement fraction of the corrected sniper leg. Journal it on
every entry: after 30–50 trades the winning-depth distribution per mandate sets the
pocket empirically. Bot-side rules (write them into any automation now): act only
on `stage==2` REGIME events or explicitly handle provisional; ignore
`evt=="CLUSTER"` unless a campaign is live. Journal fields = JSON fields verbatim,
plus fill, heat in ATRs, exit reason, R.

## 11. First two weeks
Days 1–3 observation; days 4–7 Bar Replay the four canon cases — May 16→26 short
(now prints: Z1 Bs May 17–18, **Z2 B on May 26 08:00**, upgrades A after the June
stage confirm), Jul 2→6 provisional longs, Jun 14–16 (execute the half-size B,
honor the stop, feel why the cap exists), Jun 22 V. Week 2 live at ¼ size, A+/A in
Z2/Z3 only, hard 1R daily stop. Graduate on a clean two-week journal.

## 12. Honest limits
One asset, nine months, screenshot-derived measurements, 5m evidence from Apr 26 '26.
The v11.0.2 arming tiers were validated by replaying the study, not yet by forward
trades — the five acceptance signatures (Addendum §4) are the go/no-go, and the
`retr` log is the tuning instrument. Confirmed-bar lag is a feature. Parameter
review after the first 30–50 journaled trades stands.

---

## APPENDIX A — Gating & signal-print evolution, v9.3 → v11

**v9.3 / v9.4 (LTF):** every 9/89 cross printed a regime triangle on the chart TF —
*signal = the cross itself*. Tiered pullback marks existed but ungated; MTF panel
included 30m; HTF values read live (repainted intrabar); no zones, no stops, no
grades, no exits. Gating: essentially none — the trader was the filter.

**v10 (Pyramid):** first campaign logic on the chart TF: R1/R2 reclaim entries
(A/B), band-retest marks, capitulation V, failure X, ratcheting stop, whipsaw
filter, MTF cluster. Gating: a **boolean HTF bias gate** — counter-HTF signals
suppressed outright. Still chart-TF-centric, still live HTF values, still 30m.

**v11.0 (Cascade):** the engine inverted — a selectable **governor TF** owns regime,
structure and three EMA **zones**; the chart TF only times entries. New machinery:
no-expiry armed state, two-close PRIME gated by zone + structure, grades A+/A/B/C,
sniper fib pocket, TPW as a first-class exit, tightened V, confirmed-bar
(zero-repaint) HTF discipline, webhook JSON, 30m removed, stop as pure risk floor.
Gating: **binary structure gate** — only stage-aligned crosses armed. Verification
exposed the flaw: it silenced the Jun-14 trap *and* the Mar-9/May-16/Jul-2 marquee
births.

**v11.0.2 (current):** binary gate → **tiered arming**. Every governor cross arms;
alignment with the 200 sets the *tier*: aligned = solid arrow, deep tint, Z1/Z2/Z3,
grades to A+; provisional = faded arrow, faint tint, Z1/Z2 only, grade ceiling B,
half-size doctrine; a mid-campaign 89×200 confirm upgrades the live campaign. Plus:
C gated by zone+structure, A-grade alignment TF de-tautologized (one step below
governor), sniper re-anchored (terminus at first Z2/Z3 tag, pocket 0.5–0.786,
`retr` telemetry), X glyphs flipped to the visible side, standing EMA colors
(9 yellow / 89 purple / 200 blue).

**Signal-print translation for v9.3 veterans:** your old triangles are now the
*arming arrows* — context, never entries; the trade you used to take at the
triangle now waits for the grade circle inside a band; the eyeball 89-retest you
hunted manually is Z2 doing it for you; and the exits you improvised are the
TPW → 9-trail → X ladder.
