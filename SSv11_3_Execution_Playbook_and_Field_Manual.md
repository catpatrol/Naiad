# SECRET SAUCE — CASCADE v11.3 · EXECUTION PLAYBOOK & FIELD MANUAL
### The discretionary trader's field manual · v2.0 · 2026-07-12
### Companion to `SS_Cascade_v11.3.pine` (logic identical to deployed v11.0.2)
### Supersedes SSv11_Execution_Playbook v1.0/v1.1.

Grounded in the Oct 2025 → Jul 2026 BTC multi-timeframe study **and** the full
nine-month machine-verified parity record (six case windows, ~450 events,
engine 1.0.3 conformance). Written against the shipped, verified code — where
older documents differ, this one describes what the indicator actually does.

---

## 0. Version status: FROZEN

SSv11.3 is the terminal version of the v11 line. Its signal logic is
byte-identical to v11.0.2 (proven by diff; only glyphs, colors and docs
changed). All improvement candidates — 12H swing mode (B-1), MTF smear fix
(B-2), the provisional-zone question (E-1), zoneMemory variants — are
chartered for **SSv12**, gated on the v12 Study. No change to this script or
its inputs is expected or permitted outside that process.

**The Inputs Law (new, non-negotiable):** run this indicator at **defaults**.
In particular **Zone memory = 3** — this single constant was proven
parity-critical (a 3-vs-5 mismatch produced every divergence ever found
between chart and engine). Changing *any* input creates an unnamed variant,
desyncs your chart from the verified engine, and invalidates the manual's
claims. If a setting ever seems worth changing, that is a v12 named-variant
proposal, not a settings tweak.

---

## 1. What this system is

One sentence: **the governor timeframe picks the fight, the zones pick the
location, the execution timeframe picks the moment.**

The indicator runs a campaign state machine. A 9/89 regime cross on the
governor (default 4H) *arms* it. Price returning into one of three
governor-EMA zones makes a trade *possible*. An exec-TF reclaim of its own 9
EMA with a confirming close (PRIME) makes it *actual*. Everything else on the
chart is management (stop line, TPW, X) or context (tint, MTF triangles).
You are not looking for trades; you are waiting for the machine to hand you
one.

---

## 2. ELEMENT DICTIONARY (reference — every concept in the machine)

**Governor / Exec.** Two timeframes. The *governor* (input `tfGovern`,
default 240 = 4H) supplies regime, stage, and zones — the strategic layer.
The *exec* timeframe is whatever chart you load the script on (5m for the
swing mandate) — the timing layer. Mandates: swing = 4H gov on 5m chart ·
intraday = 1H on 1m · position = 12H on 15m. One chart layout per mandate;
instances don't interact.

**Regime.** The governor's 9 EMA vs 89 EMA. A cross flips the regime (bull /
bear), tints the background, and **arms a campaign** in that direction.
Every value comes from *confirmed* governor bars — the chart lags a cross by
up to one governor bar and never repaints.

**Stage.** The governor's 89 EMA vs 200 EMA — the structure. **Stage 2** =
89 on the regime's side of the 200 (structure aligned; deep tint). **Stage
1** = structure against the regime (faint tint).

**Tier.** The campaign's citizenship class, set at arming. **Full** = the
regime cross agreed with the stage (aligned). **Provisional** = the cross
fought the stage (counter-structure). Provisional campaigns are real and arm
by default in v11.0.2+ — but they are *throttled*: grade ceiling **B**, and
Z3 never arms for them. Tier is fixed for the campaign's life even if the
stage later flips.

**Campaign & rc.** From arming until death (X, or an opposite cross), the
machine tracks one campaign. Every PRIME increments the entry counter **rc**:
rc 1 = R1, the graded first entry; rc ≥ 2 = R2+ adds. Arming has no expiry
(Law 5); rc counts into the dozens in long grinds.

**Zones (Z1 / Z2 / Z3).** Three governor-EMA bands, widths in governor-ATR:
- **Z1 (amber)** — around the gov 9, ±0.25 ATR. The trend-rider add zone.
  Arms in every campaign, both tiers.
- **Z2 (purple)** — around the gov 89, ±0.35. The campaign entry zone. Arms
  in every campaign **including provisional** (erratum E-1; the deployed
  `provZones` default is "Z1+Z2"). In provisional campaigns its entries cap
  at grade B.
- **Z3 (cyan)** — the gov 89–200 band, padded ±0.35. The deep,
  highest-quality zone (the May 26 marquee entry). **Stage-aligned full
  campaigns only** — its band is hidden in Stage 1 and it *cannot* arm
  provisionally (verified at source). Only zone where the ribbon-separation
  filter is waived.
Bands visible ≠ armed: drawing needs only a governor; arming needs a live
campaign. Priority when several are tagged: **Z3 > Z2 > Z1**.

**Zone tag / memory / episode / activeZone.** A *tag* = a bar touching a
band. A tag stays *recent* for **3 exec bars** (Zone memory — the verified
constant). A *fresh* tag is one arriving after the previous tag expired; it
opens a new *zone episode*. The *activeZone* at any moment is the innermost
recently-tagged armed zone — it is what gates PRIMEs and C-entries and what
labels each entry's zone.

**PRIME.** The entry trigger: inside an active zone, an exec candle closes
back across the exec 9, and the next candle confirms (closes beyond the 9,
at or beyond the prior close). Filters: minimum bar range (0.5× exec ATR),
exec 9/89 ribbon separation (0.5× ATR, waived in Z3), 5-bar cooldown,
structure gate, per-campaign caps. Prints the graded marker; ratchets the
stop; increments rc.

**Grades.** Quality of a PRIME (and of C-entries):
- **A+** — the zone-tag extreme landed inside the *sniper fib box* ∩ zone:
  the 0.618–0.786 retrace of the arming impulse meeting the governor zone.
  Three signals, one entry. Full size.
- **A** — PRIME in zone with the 1H MTF already aligned to the campaign.
  Full or near-full size.
- **B** — PRIME in zone without 1H alignment, or *any* provisional-campaign
  entry (the tier's ceiling). Reduced size or skip early on.
- **C** — a CONFIRM-only entry: an exec 9/89 re-cross toward the campaign in
  a zone episode that produced **no PRIME**. In v11.0.2+ the C is
  **zone-gated and structure-gated at source** (this corrected an older
  manual's warning) — a printed C has location and structure. Still the
  lowest grade: consistently later and worse-priced than the PRIME it missed.

**CONFIRM (add).** The other branch of the same event: an exec 9/89 re-cross
*after* a PRIME has fired in the current zone episode. Prints a tiny diamond,
ratchets the stop, does not increment rc. **Not zone-gated** — about one in
six confirms fires with price far from any band ("zoneless adds," 17.3% of
the nine-month record). They are legitimate machine events whose main job in
practice is the stop ratchet; as *entries* they were consistently 200–900
points worse than the PRIME. Treat far-from-band diamonds as stop management,
not initiations.

**V (Capitulation).** The gate-exempt trend-birth: a climax bar (volume ≥
3.5× average, extreme ≥ 1 gov-ATR beyond the gov 89) followed within 10 exec
bars by a close across the *far* edge of the governor 89–200 band on
confirming volume. Flips the machine and births a new campaign with its own
stop, no 9/89 cross required. Ferociously strict by design: **one firing in
nine months** — a blow-off-top catch at 90,795 ahead of a multi-day decline.
When a V prints, it is the machine's loudest statement; when you *feel* a
capitulation and no V prints, the signature wasn't met — trade your judgment,
not a phantom glyph.

**TPW (Take-Profit Warning).** ≥2 of the {5m, 1H, 4H, 12H} regimes crossing
*against* your campaign within 12 exec bars. Prints an amber flag — and
re-prints **every bar** while the condition holds, so expect flag *stacks*
(31 in a row during the May campaign). Read a stack as one warning event,
not thirty-one.

**X (Failure).** Three consecutive exec closes beyond the far governor band
edge. Campaign death. Flat, immediately, no averaging — the record contains
no example where negotiating with an X was paid.

**Ratchet stop.** On every PRIME / CONFIRM / V the stop moves to the signal
bar's (or zone-tag's) extreme ∓ 0.5 exec-ATR — **and only ever tightens**.
The printed step-line is your risk floor and doubles as an event detector:
every step is a machine event, even one whose glyph you missed. A stop
frozen for days is normal (the marquee short's froze for four); it means no
later signal beat the earlier one.

**Whipsaw suppression.** A governor-cross *arrow* is hidden if the opposite
cross occurred fewer than 10 governor bars ago. **Arrows only — arming
still happens.** Trust the tint, not the arrow.

**Sniper fib box.** The single drawn box: 0.618–0.786 of the arming impulse,
refreshed per campaign. Its intersection with a zone is the A+ condition.

**MTF display layers.** Four toggles ("MTF Display" group) painting other
timeframes' regime crosses as small triangles. Context and TPW inputs only.
Known ergonomic caveat (B-2): each higher-TF cross paints a *carpet* across
every exec bar of the following HTF period — read the first triangle of a
carpet as the event. Toggle off when doing precision bar work.

---

## 3. Reading the chart in five seconds

| Cue | Meaning |
|---|---|
| **Background tint** | Regime (green bull / red bear) × stage: **deep = Stage 2** (full campaigns, Z3 available) · **faint = Stage 1** (provisional territory: entries real, grade-capped B, no Z3). |
| **Zone bands** | Amber Z1 + purple Z2 always drawn; cyan Z3 appears only when stage aligns. Visible ≠ armed. |
| **Stop step-line** | Green below = live long with entries; red above = live short. No line = armed but not yet entered. Steps = events. |

| What you see | State | Your job |
|---|---|---|
| Tint flips (arrow or not) | ARMED | Nothing. Alerts on, wait for a zone tag. Hidden arrow ≠ no arming. |
| Deep tint + price entering a band | ZONE ACTIVE (full) | Watch the exec 9. The only moment needing your eyes. |
| Faint tint + price at amber/purple | ZONE ACTIVE (provisional) | §5.5 protocol — smaller, stricter, X-vigilant. |
| Grade marker prints | ENTERED (R1) | Execute per §5. |
| Graded circles / diamonds after R1 | SCALING | Add per §6, ratchet each time. |
| TPW stack / X / opposite solid arrow | DEFENSE / DEATH | §7. Never negotiate with an X. |

---

## 4. Glyph dictionary (v11.3 — grade colors are the change)

**Lines & fills:** exec 9 = yellow (trigger line) · exec 89 = pink/purple
(confirm line) · exec 200 = thin blue (context) · Z1 amber / Z2 purple / Z3
cyan bands · stop step-line green/red (reference, not an order) · background
4 shades. Bands and tint step with a one-governor-bar lag — deliberate,
repaint-free.

**Event glyphs:**

| Glyph | Look (v11.3) | Meaning | Action |
|---|---|---|---|
| Governor cross, aligned | solid ▲/▼ | Full campaign armed (Law 1: not an entry) | Wait for a zone |
| Governor cross, counter | faded small ▲/▼ (often whipsaw-hidden) | **Provisional campaign armed** (grade cap B, Z1+Z2 only) | §5.5 protocol |
| **R1 grade marker** | **A+ = GOLD, normal size** · A = full direction color, small · B = direction color 60% faded, small — lettered | Campaign's first PRIME, graded | The trade. §5 |
| **R2+ graded circle** | **A+ = gold, small** · A = direction color, tiny · B = faded, tiny | Later PRIMEs, now grade-visible | Add per §6 — a **gold add** is a premium location; the old anonymous circles are gone |
| Tiny diamond | yellow/amber, textless | CONFIRM add (9/89 re-cross, PRIME already in episode). May print far from bands (zoneless add) | Positioned: note the ratchet. Flat: not your initiation |
| **"C" label** | gold label | Confirm-only entry — zone- and structure-gated at source | Lowest grade; honor location, size accordingly |
| "V" arrow | blue ↑ / violet ↓ | Capitulation trend-birth, gate-exempt | §8. Rare and loud |
| "TPW" flag (stacks) | amber flags | Opposite MTF cluster | One warning per stack. §7 |
| "X" cross | orange ✕ | Campaign death | Flat. Immediately |
| Small TF-labeled ▲/▼ | "5m/1H/4H/12H" | MTF regime crosses (carpets — read first of each) | Telemetry |

*Retired in v11.3:* the "89x200" stage circles — the deep tint already
carries that information.

---

## 5. THE IDEAL ENTRY

### 5.1 The shape
1. Governor crosses aligned (deep tint). Armed.
2. Price pulls back into a zone; the exec 9 is above/below price (that's the
   pullback).
3. Inside the zone: close back across the exec 9 + confirming close → PRIME;
   the grade marker prints.
4. Stop just beyond the zone-tag extreme — the printed line does the
   arithmetic (extreme ∓ 0.5 ATR). If the line feels far, the entry is late:
   skip; the next tag is coming (Law 4).
5. Right setups show near-zero heat within a handful of exec bars.

### 5.2 Grade → size
**A+** full · **A** full/near-full · **B** reduced or skip early on · **C**
smallest, only with clean location. Deeper zone beats shallower at equal
grade for *initiation* (Z3 > Z2 > Z1); Z1 is primarily the add zone.

### 5.3 Sixty-second checklist
1. Tint direction and **depth**? 2. Armed on record (tint counts even
arrow-hidden)? 3. Which band, and is it Z2/Z3? 4. Grade marker on a
*confirming* close? 5. Stop-line distance in R — size right? 6. MTF
triangles stacking against (pre-TPW)? 7. Fill within ticks of the signal
close, stop at the line. No chasing.

### 5.4 What is NOT the ideal entry
The arrow itself (Law 1) · anything with no band under it (Law 2) —
including zoneless diamonds · fresh signals after the stage de-aligns
mid-campaign (PRIMEs silently stop printing by design; manage holdings, add
nothing) · anything after an X.

### 5.5 Provisional campaigns (faint tint) — the honest protocol
The machine arms counter-structure crosses by default and will hand you real
Z1 and Z2 entries under faint tint, all capped at grade B. The record is
two-faced and the manual says so: **six provisional campaigns died in X**
across the study's case windows — *and the marquee short itself ran
provisional for its entire eleven-day life*, the structure only aligning
after the window. Until the v12 Study separates the trap from the marquee
(open hypothesis H3), the standing protocol is:
- Size at the B-ceiling or below; never full doctrine size.
- Prefer Z2 (purple) locations over Z1 grinds for provisional *initiation*.
- X-vigilance doubled: provisional campaigns die by X more often and faster.
- Expect no Z3, no A/A+, and no shame in skipping entirely — Law 3 remains
  the default posture; §5.5 governs only when you consciously engage.

---

## 6. Scaling (R2+, CONFIRM, the ratchet)

Every later PRIME prints a **graded** circle (new in v11.3 — a gold R2+ add
marks a premium re-entry, the single most requested legibility fix). Stop
ratchets on each; because it only tightens, **campaign risk stays constant
or shrinks as size grows** — the entire point of the pyramid. CONFIRM
diamonds are adds for positioned traders only. Sizing doctrine: R1 = full
planned unit; adds ≤ the initial unit, and only while each prior tranche is
at/beyond breakeven after the ratchet. In a mature Stage-2 trend, Z1 tags
are the campaign's rhythm — miss one, wait for the next; chasing between
zones is the strongest habit-breaker in the record.

---

## 7. THE IDEAL EXIT

1. **TPW stack → take partials.** Bank 25–50%, tighten to the ratchet line
   or beyond the last exec swing, stop adding. One stack is information;
   two stacks in the same leg rarely forgive.
2. **Exec-9 trail.** Extended move + close back across the yellow 9 without
   a quick reclaim = discretionary partial/trail. No glyph — read the line.
3. **X or opposite solid arrow → flat.** No negotiation, ever.

Rhythm that matched the record: partial at TPW, partial into extension
(≥ ~2 exec-ATR beyond the 9 is stretched), core runs until the structure
says stop. No fixed targets — the marquee paid ~18,000 points precisely
because nothing said "enough" until the X did.

---

## 8. The V

When it prints: it is gate-exempt, flips the machine, sets its own stop, and
in nine months fired exactly once — at the top. Treat a printed V as the
highest-conviction context the system produces. Treat an *unprinted* V —
a capitulation you can see but the machine won't name — as outside the
system: the signature demands a full far-band recross within ten exec bars
on volume, and real capitulations frequently fail it. That is a documented
design limit (the clock ticks in exec bars while the geometry scales with
the governor), on the v12 docket.

---

## 9. Alerts & journaling

Unchanged from v1.x: every event arrives as one-line JSON
(`evt/dir/grade/rc/zone/px/stop/atr/stage/t`), webhook-ready; ten named
alertconditions for phone setups. Journal every trade with the JSON fields
verbatim plus fill, heat in ATRs, exit reason, and R result — your log and
the engine share one language, and grade/zone expectancy becomes queryable.
Note the journal's semantics, now machine-verified: `tier` and campaign
labels are set at arming; REGIME alerts fire on aligned *and* counter
crosses (`stage` field distinguishes); hidden arrows still journal.

---

## 10. The Five Laws (unchanged, one annotation)

1. **Never enter at the triangle.** Every cross in the study printed 30–60%
   into its impulse — buying the arrow buys the snap-back.
2. **No zone, no trade.**
3. **Never fight the structure.** Counter-structure setups killed every
   trigger variant tested (Jun 14–16 '26). The gate stays on.
   *Annotation (2026-07-12): the machine now arms these provisionally by
   default, and the record holds one documented counterexample — the May
   16–26 marquee ran provisional throughout. Law 3 remains the default
   posture; §5.5 is the protocol for conscious exceptions; v12 H3 will
   separate trap from marquee with data.*
4. **The stop lives just beyond the zone extreme, never wider.** If the stop
   feels far away, the entry came late — skip it.
5. **Armed means patient.** Arming has no expiry. The marquee armed May 16
   and paid for eleven days. Waiting is a position.

---

## 11. Known behaviors & open questions (so nothing surprises you)

- **Zoneless diamonds** are real and common (17.3% of confirms) — stop
  ratchets far from bands are correct behavior, not glitches.
- **TPW and MTF carpets** repeat per-bar (B-2, SSv12 docket). First glyph =
  the event.
- **One-governor-bar lag** on tint/bands/arrows: the no-repaint price.
- **Stop freezes** lasting days are normal in grinding campaigns.
- **E-1** (provisional Z2) is deployed behavior, documented in
  `SSv12_SPEC_ERRATA.md`; its keep-or-revert decision is a v12 named-variant
  slot, as are "zoneMemory-5" and "zone-gated CONFIRM adds."
- **Parity**: this chart's behavior is machine-verified against the Naiad
  engine (1.0.3) across six case windows at these exact input defaults —
  which is *why* the Inputs Law exists.

## 12. Honest limits

Everything derives from one asset (BTC perp), nine months, one regime
era — now machine-verified event-by-event, but still n=1 on asset and
regime. Grades and zone widths are evidence-backed defaults, not laws of
nature. The ten-asset v12 Study exists to give these numbers error bars;
until it reports, treat any new market as unvalidated.

---

### Pocket card

**ENTER** only: campaign armed (tint!) + price in band (Z3>Z2>Z1) + grade
marker on confirming close. Stop = the line. **A+ (gold) full · A full ·
B small · C smallest · faint tint = §5.5 throttle.**
**ADD**: graded circles / diamonds — gold adds are premium; ratchet every
time; risk never grows.
**EXIT**: TPW stack → partial + tighten · exec-9 lost, not reclaimed →
trail · X or opposite solid arrow → flat, no discussion.
**NEVER**: the arrow itself · outside a band (diamonds included) · after an
X · wider stops · changed inputs. *Armed means patient.*
