# BUILD — PINE ESTATE v12.6 FILED
**ARGUS (PINE lane, folded) · date of record 2026-08-16 · filed to the repo 2026-08-21**
**Path of record: `exchange/reports/BUILD_2026-08-16_PINE_ESTATE_V12_6.md`**

---

> ## ⚠ READ THIS BEFORE THE REST
>
> **The filing succeeded.** Three Pine files verified to the byte and filed to `pine/`; shas in §6;
> no mismatch, no halt.
>
> **Three things found while filing are more urgent than the filing:**
>
> 1. **THE ORACLE DAILY HAS BEEN DOWN SINCE 2026-08-20** — four consecutive FAIL rows, both slots,
>    two days, no HTML produced. **Gate G-BR2-2 will read FAIL on 2026-08-22**, the date BR-2 was
>    parked to wake on. Nobody has seen it because `LEDGER_ARGUS.md` has been silent for five days.
>    **§5A.** Outside this filing's scope; reported because the next person to touch BR-2 will
>    otherwise act on a false assumption.
> 2. **THE ANCHOR DIVERGES FROM ITS HANDBOOK IN THREE PLACES** (§5, F-1/F-2/F-3), one of them —
>    the stop anchor, which *sets R* — **not flagged in the Anchor's own list of things it knows it
>    guessed at.** Root cause is stated once in §5, F-0: the builder had neither the handbook nor
>    the contracted base file. **Every missing number is in the handbook; nothing needs measuring.**
> 3. **NONE OF THE FIVE RULINGS IN §3 HAS A PRIOR WRITTEN RECORD**, and two of them contradict what
>    the repo currently says. This document is where all five enter the record. **§3, opening box.**
>
> Nothing above was changed. Everything is reported-not-fixed, with an owner, in **§10**.


## §0 · WHAT THIS DOCUMENT IS, TO SOMEONE WHO KNOWS NOTHING

Naiad is a crypto-futures research estate. One of its outputs is a set of **TradingView Pine v6
indicators** — chart software, not engine code. They draw what the research says, so a human can
look at a chart and see what the system sees. That family of files is "the Pine estate". None of
it executes trades and none of it feeds the analytics engine; it is an instrument for the eye.

This document files **version 12.6 of that estate**, which is **three files**, and it is the
single build document for that block of work. It records what the three files are, how the estate
arrived at this shape, which operator rulings bind it, what is still owed, and the sha256 of every
byte filed. Read it alone and you should be able to re-derive or refute the filing without asking
anyone a question.

**Two dates, on purpose.** The work, the rulings and the source files are of **2026-08-16**, and
the operator named this document for that date. The act of copying the files into the repo and
writing this record happened on **2026-08-21**. Both are stated rather than collapsed, because the
filing date is what `git` will show and the record must not appear to contradict it.

**What was NOT done here:** nothing was deleted, nothing was renamed in place, no older Pine file
was removed, and no engine code, config or threshold was touched. This is a filing, plus the
findings that filing turned up.

---

## §1 · THE THREE FILES

| file | what it is | bytes |
|---|---|---|
| `pine/SS12_MANTLE_v12_6.pine` | **the fabric, and only the fabric** — the EMA suite: 20 lines, 8 ribbons, 3 grounds. No events. | 11,274 |
| `pine/SS12_SIGNAL_v12_6.pine` | **every event, one instrument** — all cross machinery: the 12/89 MTF regime cascade over five lenses, primary regime arrows, secondary pairs, arming/trigger events. | 20,249 |
| `pine/SS_Anchor_v12_T_0.pine` | **one indicator, ONE TRADE** — the six-gate lifecycle S0–S8 drawn as chart furniture, per APOLLO's brief. | 15,828 |

Their declared titles, read from the sources:

- `indicator("SS12-MANTLE v12.6", shorttitle="SS Mantle", overlay=true)` — `SS12_MANTLE_v12_6.pine:2`
- `indicator("SS12-SIGNAL v12.6", shorttitle="SS Signal", overlay=true, max_labels_count=500)` — `SS12_SIGNAL_v12_6.pine:2`
- `indicator("Secret Sauce — ANCHOR (v12-T.0)", shorttitle="SS Anchor", overlay=true, max_labels_count=500, max_lines_count=500)` — `SS_Anchor_v12_T_0.pine:2`

**The division of labour is the point of v12.6.** MANTLE draws lines and never an event; SIGNAL
draws events and never the fabric; ANCHOR draws neither in general — it draws exactly one trade's
lifecycle. Loading all three gives the whole picture; loading one gives a clean one.

---

## §2 · (a) LINEAGE OF RECORD

The estate reached three files by six steps. Only the first and last exist as filed artifacts;
the four in between were chat-side iterations, superseded and never filed. They are recorded here
because a lineage with holes invites someone to go looking for files that do not exist.

**SS v12.1 — SINGLE FILE.** Everything in one indicator: fabric and events together. This is the
ancestor the whole estate is measured against. **It is not in the repo** (see §4, debt V-3); what
`pine/` holds from that era is `SS_v12_0_1.pine`, its immediate predecessor, 15,004 bytes, filed
2026-08-15 and untouched by this build.

**v12.2 — THE SPLIT.** The single file is cut in two along the seam that has held ever since:
**Scope** (fabric) and **Signals** (events). Chat-side, superseded, not filed.

**v12.3 — RIBBONS + CONST COLORS.** Ribbon structure introduced; colours moved to constants.
Chat-side, superseded, not filed.

**v12.4 — COLOR-INPUT RESTORE + PER-LENS LADDER.** The colour *inputs* removed by v12.3's
constants are restored, and the MTF lenses gain their own ladder. Chat-side, superseded, not filed.

**v12.5 — HTF-EVENT CROSS ENGINE + THE 12/89 REGIME RULING + SECONDARY PAIRS.** The cross engine is
rewired so crosses are **computed on the higher timeframe and ferried down as events**, deduped at
the chart lens, rather than recomputed locally — the defect class that a shared resampler tends to
produce. The regime/cascade pair moves **9/89 → 12/89** by operator ruling. Secondary pairs added.
Chat-side, superseded, not filed; but its engine and its ruling are **carried into v12.6 intact**
and are visible in `SS12_SIGNAL_v12_6.pine:11-13`.

**v12.6 — THE RENAME, AND THE ANCHOR.** Two moves in one version:

1. **Scope → SS12-MANTLE** (fabric only) and **Signals → SS12-SIGNAL** (all events). The rename is
   not cosmetic: it is accompanied by the *completion* of the split. All remaining cross machinery
   — MTF cascade, regime triangles, secondary pairs — leaves MANTLE for SIGNAL, so that after
   v12.6 the fabric file contains no event logic at all. The sources say so in their own headers:
   *"MANTLE = the EMA suite alone: 20 lines, 8 ribbons, 3 grounds. ALL cross machinery (MTF
   cascade, regime triangles, secondary pairs) moved to SS12-SIGNAL v12.6"*
   (`SS12_MANTLE_v12_6.pine:10-12`), and *"ABSORBS the cross machinery removed from MANTLE"*
   (`SS12_SIGNAL_v12_6.pine:9`).
2. **SS Anchor v12-T.0 is added**, per APOLLO's brief
   `exchange/reports/BRIEF_ARGUS_PINE_SSV12T_2026-08-16.md`. It is a third instrument, not a
   replacement for either: where MANTLE and SIGNAL are general, ANCHOR strips the estate's
   generality down to the six-gate lifecycle of the handbook so a discretionary human sees exactly
   — and only — what the system sees, in order. Its header records the naming:
   *"Per BRIEF_ARGUS_PINE_SSV12T_2026-08-16 (APOLLO). Operator named it ANCHOR."*
   (`SS_Anchor_v12_T_0.pine:7`).

---

## §3 · (b) RULINGS CARRIED — operator, this session series

Five operator rulings bind this filing. **Before stating them, one thing must be said about all
five, because it changes how they should be read.**

> ### THE PROVENANCE DISCLOSURE — READ THIS BEFORE THE FIVE
>
> These five rulings were carried into this filing **on the operator's authority as given in the
> filing instruction itself.** A search of the repo made during this build found that **none of the
> five has a prior written record** — no ledger entry, no dated ruling stamp, no relay note. Where
> they appear at all before now, they appear as **comments inside the Pine sources being filed** —
> which is the builder's own attestation, not independent corroboration. A file asserting its own
> authority is the weakest form of record there is.
>
> **This build document is therefore the point at which all five enter the written record.** That
> is a legitimate thing for a build document to be — CONVENTIONS §3.1 requires it to record *"what
> was decided and on whose authority"* — but it must not be dressed up as a citation to something
> older. Nothing here is challenged; it is dated and attributed so that the next reader knows
> exactly how much weight the record itself carries.
>
> **Two of the five sit against an existing written record that says something different (R-1, R-2).
> Those conflicts are stated under their own headings rather than smoothed over.** Ruling wins over
> stale record — that is what a ruling is for — but a superseded record that is never named simply
> resurfaces later as a contradiction nobody can date.

### R-1 · THE PINE LANE IS FOLDED INTO ARGUS

**As it operates:** there is no separate PINE lane ledger and no separate PINE commissioning
authority. Pine work is ARGUS work — commissioned, recorded and closed in
`exchange/status/LEDGER_ARGUS.md`. This is why this document's entry is a `STATUS_ARGUS` block.

> **CONFLICT WITH THE STANDING RECORD, DISCLOSED.** The written record runs the other way, and
> recently:
> - **2026-08-15** — APOLLO **spun PINE out into its own chat**, with its own primer:
>   *"**PINE** spun out to its own chat (`PINE_LANE_PRIMER_2026-08-15.md` + `SS_v12_1.pine`)"*
>   (`exchange/reports/APOLLO_LANE_STATUS_2026-08-15.md:47`).
> - **2026-08-17** — the succession handoff **still lists PINE as a separate lane**:
>   *"Pine `SS_v12_1.pine` (Pine lane owns evolution; renders-never-rules)"*
>   (`exchange/reports/HANDOFF_APOLLO_NAIAD_SUCCESSION_2026-08-17.md:59`).
> - The **CONVENTIONS lane roster** has no PINE row, and assigns the Pine indicator to **APOLLO**:
>   *"| **APOLLO** | web chat | SSv12, census programme, Tier-C runs, Engine V2, SSv12 Pine
>   indicator |"* (`exchange/status/CONVENTIONS.md:536`). ARGUS's charter row is *"analytics
>   toolkit, daily brief, volume filter"*.
>
> A repo-wide search for *"folded into ARGUS" / "fold into ARGUS" / "absorbed into ARGUS"* returns
> **zero hits**. The nearest thing to a fold in the written record is a **commission, not a lane
> merge**: on 2026-08-16 APOLLO addressed the SS v12-T brief *to ARGUS* while noting the PINE
> lane's constraints ledger binds *"whoever implements"*.
>
> **R-1 supersedes all of the above.** Named consequence: **`CONVENTIONS.md:536` and the succession
> handoff now disagree with the operating truth**, and CONVENTIONS is the roster three web lanes
> read. Correcting it is a CONVENTIONS edit, outside this filing's authority — **flagged, not
> fixed.**

### R-2 · THE DISPLAY SET IS 20 EMAs, AND 26 IS IN IT

**Verified in the source, not the comment.** `SS12_MANTLE_v12_6.pine:88-92` defines exactly twenty
`ta.ema` calls, `:94-113` plots all twenty, and `:46-65` gives each its own on/off input, all
defaulting on:

    9, 12, 26, 62, 89, 162, 200, 261, 362, 500, 618, 785,
    886, 1272, 1618, 2224, 2618, 3618, 4236, 5000

Twenty lines, and **26 is present** — third in plot order, default colour `#C43C03`. Over them sit
**8 ribbons**: FAST 12–26 (hem) · M 89–162 (arming band) · MH 261–362 · GOLD 500–618 (seam) ·
H 886–1272 (creek/ice) · DEEP 1618–2224 · VH 2618–3618 (mantle) · UH 4236–5000 (rod). The file has
**20 `plot()` calls, 8 `fill()` calls, zero events, zero alerts, zero `request.security` and zero
`ta.crossover/crossunder`** — the split is complete in the code, not just in the header.

*(Small internal inconsistency, noted so a reader who counts does not think they have found a bug:
the header says "**3 grounds**" while the control offers **four** options — `["Bone","Sietch
Dusk","Noir","Custom"]` (`:25`). Both are right about different things: `f_pal()` has three palette
ladders, and "Custom" is not a ladder — it is handled in `lcol()` as a pass-through to your own
inputs. Three ladders + one pass-through = four dropdown entries.)*

> **CONFLICT WITH THE STANDING RECORD, DISCLOSED.** The display set of record before this filing is
> **not 20 lines, and not these lines.** It is the **ratified TWELVE preset** — each sub-ribbon's
> median+roof `{12,26 · 89,127 · 316,423 · 889,1272 · 2618,3618 · 4618,5000}` — drawn over an
> **18-EMA Big Ribbon**: Fast 9·12·26 · Medium 62·89·127 · MediumHigh 262·316·423 · High
> 616·889·1272 · VeryHigh 1618·2618·3618 · UberHigh 4236·4618·5000. That set is the operator's own
> **back-to-basics declaration of 2026-08-13, tagged "[ratified as observation program]"**
> (`exchange/reports/LANE_UPDATE_DIONYSUS_2026-08-13_BR-momentum_winner-zoom_brief-feedback.md:9,11`;
> `exchange/reports/PINE_LANE_PRIMER_2026-08-15.md:8-10`), and `pine/SS_v12_0_1.pine` plots exactly
> those twelve.
>
> **The v12.6 set is a different set, not a re-count of the same one.** **Seven periods dropped**
> — 127, 262, 316, 423, 616, **889**, 4618 — and **nine added** — 162, 200, 261, 362, 500, 618, 785,
> **886**, 2224. The arithmetic closes: **18 − 7 + 9 = 20**.
>
> **Two of the drops are near-misses that will read as typos and are not.** The ribbon of record
> carries **889** and **262**; v12.6 carries **886** and **261**. Three apart and one apart
> respectively — deliberate different numbers, not transcription slips, and worth knowing before
> someone "corrects" one of them.
>
> **The 889 drop has a consequence beyond the fabric.** 889 is a **champion wall** (brief §7: walls
> at *"889 (12h + 1d), 3618 (4h), 4618 (1h)"*). Of those three, the v12.6 fabric plots **only 3618**:
> 889 became 886, and 4618 is gone entirely. The Anchor draws all three walls itself via
> `request.security`, so nothing breaks — but **the MANTLE fabric can no longer be used to eyeball
> two of the three champion walls.**
>
> **316 is the drop that matters, and its consequence is narrower than it first looks.** 316 is
> half of the **89/316 tide pair** and half of the **89/316 de-risk band**. It is **absent from
> MANTLE entirely** — `grep -c 316 pine/SS12_MANTLE_v12_6.pine` returns **0** — where the ancestor
> `pine/SS_v12_0_1.pine` plots it as a toggled line (`:54-57`), fills an `MH 316–423` ribbon
> (`:114`) and carries an `89/316 — the BELL` accent (`:98,119`).
>
> **Nothing is broken by this, because 316 did not leave the estate — it left the *fabric*.** SIGNAL
> still computes it (13 references; `BELL 89/316 ✖` at `:45`, ferried per lens at `:114-122`) and
> ANCHOR still computes it (17 references, for the S0 tide and the S6 de-risk band), both via
> `request.security` rather than by reading any MANTLE plot. **The single practical consequence: an
> operator who reads tide off the MANTLE fabric by eye will not find a 316 line to read it from.**
> Tide must be taken from the Anchor's chip or from SIGNAL's bell. Flagged, not fixed.
>
> **A NEARBY RULING THAT IS NOT THIS ONE.** The number 26 *does* have a dated operator ruling —
> **A2-3, operator, 2026-08-16, verbatim stamp "Rc 26"**
> (`exchange/queue/2026-08-16_BR1_brief_redesign_ARGUS.md:100-107`) — but that ruling is about the
> **trigger pair**, not the display set. It is cited here so the two are not conflated: A2-3 does
> **not** ratify a 20-line display set.

### R-3 · THE PALETTE OBEYS THE "touch-wins" COLOUR LAW

**Statement of record**, verbatim from `SS12_MANTLE_v12_6.pine:13-18`: *"COLOR OVERRIDE FIXED,
properly: **YOUR TOUCH ALWAYS WINS.** Any line whose color input differs from its shipped default is
honored under ANY ground; untouched lines follow the selected palette. Ground "Custom" still forces
all twenty to your inputs."* Restated in the user-facing control itself: *"Ground — palette preset;
**a per-line color you have changed always wins**"* (`:25`). Enforced in **one line** (`:67-69`):

    base = ground == "Custom" or cIn != defC ? cIn : f_pal(i)

Plainly: pick a ground (Bone / Sietch Dusk / Noir / Custom); every line you have **not** recoloured
follows it; every line you **have** touched keeps your colour under any ground.

*(The label "**touch-wins**" is this document's and the operator's shorthand. The phrase does not
occur in the repo; the law does, verbatim, under the wording above.)*

> **CORNER CASE, DISCLOSED IN THE SOURCE AND CARRIED HERE.** The law detects "touched" **by value**
> — `cIn != defC` — not by event. So **setting a colour back to exactly its shipped default returns
> that line to the palette**, even though you touched it deliberately. `SS12_MANTLE_v12_6.pine:16-18`
> discloses this itself. Not introduced by this filing. **Reported, not fixed.**

### R-4 · THE REGIME/CASCADE PAIR IS 12/89, NOT 9/89

**Implemented, not merely documented:** `lenFast = input.int(12, "Fast EMA (regime)")` and
`lenSlow = input.int(89, "Slow EMA (regime)")` (`SS12_SIGNAL_v12_6.pine:66-67`), with the cascade
group titled *"MTF cascade — 12/89 regime triangles"* (`:74`). The header states the doctrine:
*"Trigger pair 12/26 per ruling A2-3; regime/cascade pair 12/89 per the operator's v12.5 ruling —
one semantics everywhere."* (`:27-28`).

**The 9/89 ancestry is verifiable.** `pine/SS_Cascade_v11.3.pine:95-96` sets the same two inputs to
`input.int(9, "Fast EMA (9)")` / `input.int(89, "Slow EMA (89)")`. So the 9 → 12 move on the regime
inputs is real and can be seen by diffing two files in `pine/`.

> **PRECISION THAT THE SHORTHAND LOSES — and it matters.** "9/89 → 12/89" is **not** a change to the
> window/arming pair. **12/89 was already ratified card law** in the Tier-C lineage (*"window 12/89
> with d = 0.75"*, re-read from the register unchanged at every tier —
> `exchange/reports/BUILD_2026-08-15_TIERC3_RAILED.md:89`,
> `exchange/reports/BUILD_2026-08-16_TIERC4_MEANCARD.md:93`). What the v12.5 ruling changed is the
> pair used by the **MTF regime cascade and the primary regime arrows** — bringing the *display*
> into line with the *already-ruled* window pair. **The estate did not move its window; it stopped
> drawing a different one.** The authority named for it — *"the operator's v12.5 ruling"* — has no
> record in the repo: a search for `v12.5`/`v12_5` returns three hits, all inside the two v12.6 Pine
> headers filed here.

**Why the distinction is load-bearing: 12/89 opens the window; 12/26 is the entry inside it.** Two
pairs, two jobs, one semantics each. SIGNAL's own tooltip states the dependency: *"The census's
entry clause is measured INSIDE an open 12/89 window. ON: ◆ prints only while that lens's 12 is on
the trigger's side of its 89. OFF: every 12/26 cross prints."* (`:53`).

### R-5 · THE ANCHOR IS NAMED BY THE OPERATOR

APOLLO's brief commissioned the instrument as **"SS v12-T"**, version token `SS_v12_T_0` (brief §1,
§4). **The brief never uses the word "Anchor" as a name** — its single occurrence of "anchor" is the
stop's geometry, *"anchor = 800h 4h pivot, rail 1.0 ATR"*. The operator named the delivered
instrument **ANCHOR**, giving `SS Anchor v12-T.0`.

The brief's version token survives inside the operator's name — file `SS_Anchor_v12_T_0.pine`, title
`Secret Sauce — ANCHOR (v12-T.0)` — so brief and artifact stay matchable by anyone holding only one
of them. **The naming's only trace before this document is one comment line**
(`SS_Anchor_v12_T_0.pine:7`): *"Per BRIEF_ARGUS_PINE_SSV12T_2026-08-16 (APOLLO). Operator named it
ANCHOR."* No ledger entry records it, and no date for the naming is stated anywhere. **This document
is where it enters the record.**

## §4 · (c) OPEN DEBTS

### D-1 · PARITY SPOT-CHECKS (V-3) NOW TARGET SS12-SIGNAL v12.6

**What V-3 is.** V-3 is a disclosure filed in `exchange/reports/BUILD_2026-08-16_ORACLE_REBIRTH.md`
(§ "V-3 · PINE SS v12.1 IS NOT IN THE REPO", lines 221-227). Fixture F-BR-1 was contracted to
compare the analytics engine's markers against *"Pine SS v12.1 markers"* — but v12.1 is not in the
repo and exists only as a description in `PINE_LANE_PRIMER_2026-08-15` §2. F-BR-1 therefore did
what it could and said what it could not: it transcribed the marker logic **directly from the
v12.0.1 Pine source** as an independent second implementation, compared it to the engine
event-for-event over full history on a frozen day — **10/10 symbols, 6 marker series each,
mismatch list empty** — and printed a standing `[handoff]` that **v12.1-level parity is OWED**.
The same passage names the only thing that can close it: *"The operator's mid-week chart glance
(BR-2 gate G-BR2-3) is the only thing that can close it."*

**The ruling recorded here.** The parity target **moves to `SS12-SIGNAL v12.6`**. This is not a
convenience, and the claim underneath it was checked rather than assumed: SS12-SIGNAL's **arming
pair is 12/89** (`SS12_SIGNAL_v12_6.pine:66-67`), and 12/89 **is the posture engine's own window
pair** — `WINDOW_FAST = 12`, `WINDOW_SLOW = 89`, both `ruled: True`, sourced to the rule card
(`scripts/posture_engine.py:91-95`, values originating in `scripts/tierc2_rules.py` as
*"rule card WINDOW — 4h 12/89 cross"*). The engine executes it as `e12` vs `e89` on the 4h lens —
`"w_up": ind.crossover(f.e12, f.e89)` / `"w_dn": ind.crossunder(f.e12, f.e89)`
(`scripts/tierc2_rules.py:287-288`), which `posture_engine` **re-exports rather than
reimplements**. The shipped canon artifact agrees: `research_outputs/oracle/posture_canon.json`
carries `WINDOW_FAST 12` / `WINDOW_SLOW 89`, `ruled: true`.

**So the instrument and the engine compute the same window from the same pair**, and a chart glance
is a genuine comparison rather than an analogy. *(Caveat worth one line: same pair is not same
implementation — SIGNAL is Pine on TradingView's bars, the engine is Python on the tape. That gap
is exactly what a spot-check exists to measure, and it is why the glance is evidence rather than
ceremony.)*

**The consequence, which is the useful part.** The operator's Oracle mid-week **PARITY glance
therefore doubles as the first V-3 spot-check** — one act discharges two debts. It is already
required for its own reasons: gate **G-BR2-3 currently FAILS** because no `PARITY: OK <date>` or
`PARITY: mismatches:` line exists anywhere in the record
(`exchange/status/LEDGER_ARGUS.md`, BR-2 gate entry; the exact string to paste is held in
`exchange/reports/ORACLE_CHAIN_CLOSE_2026-08-16.md` §3.1). That gate is the operator's to
discharge, not a builder's.

> **DO NOT CONFUSE THIS WITH THE 2026-08-02 PARITY EXERCISE.** `PARITY_CAPTURE_PLAN.md` and
> `PARITY_READINGS_GUIDE.md` describe a **different and already-closed** exercise — the 2026-08-02
> ARGUS analytics-vs-TradingView indicator parity (twelve screenshots, two chart setups, BINANCE
> `.P` perpetuals, UTC, last closed candle). They do **not** describe this debt. Reading them
> expecting the V-3 procedure will mislead you.
>
> **Also worth knowing before you look:** no `PARITY: OK <date>` line has *ever* been appended to
> `LEDGER_ARGUS.md` — `grep -n "PARITY:" exchange/status/LEDGER_ARGUS.md` returns exactly one hit,
> and it is the halt record's own statement that the line is missing. And there is **no cadence,
> launchd agent or `CADENCE.md` entry** scheduling the mid-week glance: it is a one-off operator
> act with nothing in the estate that will remind him. That, more than anything else in this
> document, is the item most likely to be forgotten.

### D-2 · THE ANCHOR'S BUILDER-DEFAULT PINS AWAIT HANDBOOK NUMBERS

The Anchor ships with two values its own source marks as provisional:

| pin | shipped value | source line | status |
|---|---|---|---|
| `TRAIL_PIVOT_BARS` | `20` (4h bars) | `SS_Anchor_v12_T_0.pine:62` | `// [builder default — handbook value to be pinned]` |
| WINDOW/TRIGGER lens | the **chart's own timeframe** | `SS_Anchor_v12_T_0.pine:30` | builder default, brief inherits "grid-set lens defaults" without pinning one |

Most of the rest of the Anchor's trade furniture is **not** provisional and matches the handbook,
which is worth stating so the debt is not read as larger than it is: the 800h/4h stop anchor and
its **1.0 ATR rail** (`SS_Anchor_v12_T_0.pine:117,122` — `stopP := math.min(piv4hLo, close - 1.0 *
tATR)`), the trail's **0.5 ATR offset**, its **0.05 ATR minimum advance**, and the trail arming
**only after +1R** (`:150-168`). Those agree with handbook Steps 3-5 as written.

**But the pin above is not the whole of this debt, and §5 states why: the handbook is not in fact
silent on the trail's pivot, and where it speaks, the shipped code diverges from it twice.** Read
§5 before acting on the table above.

### D-3 · THE ANCHOR'S QUICKSTART IS NOT FILED

APOLLO's brief §4 requires the Anchor be delivered as *"pine file + one-page quickstart"*. That
quickstart **exists** — `SS_Anchor_QUICKSTART.md`, in the operator's `~/Downloads`, headed
*"SS ANCHOR (v12-T.0) — QUICKSTART · one trade, six gates · ARGUS · 2026-08-16 · companion to
SS_Anchor_v12_T_0.pine"*. It is **not in this filing's three-file manifest**, so it was **not
copied into the repo**: filing an unlisted artifact would put a file on the bus that the operator
did not authorise. **Reported, not fixed — the operator's call.** Named here so that a deliverable
the brief requires does not go missing between a Downloads folder and the record.

*(Its content is not lost detail: it pins the Anchor's intended lens — "Load it on **1H or 4H** (on
5m/30m everything drowns in its own toll)" — which is the nearest thing on record to a value for
the WINDOW/TRIGGER lens pin in D-2.)*

### D-4 · UNCHANGED, CARRIED FORWARD

The live week and **BR-2 are unchanged by this filing.** BR-2 remains **BUILT: PENDING**, halted at
its three gates, per `exchange/status/LEDGER_ARGUS.md`. Nothing in this build touches BR-2's gates,
its calibration, or the Oracle. Stated so this filing is not mistaken for movement on that chain.

---

## §5 · FINDINGS — REPORTED, NOT FIXED

**Four findings.** Three (F-1, F-2, F-3) are divergences between the Anchor's shipped code and the
handbook it implements; one (F-4) is a set of binding brief constraints left unmet. All were found
by reading `SS_Anchor_v12_T_0.pine` line by line against
`exchange/reports/SSV12_LOGIC_2026-08-16.md` and `BRIEF_ARGUS_PINE_SSV12T_2026-08-16.md` during
this filing. **None was changed.** APOLLO's brief §4 is explicit — *"No new
semantics, no new thresholds: anything not in the handbook needs an APOLLO word first"* — and the
converse binds equally: where the code departs from the handbook, restoring it is a ruling, not a
builder's edit.

### F-1 · THE TRAIL PIVOT IS A 20-BAR EXTREME; THE HANDBOOK SPECIFIES A (2,2) FRACTAL

`SS_Anchor_v12_T_0.pine:62` reads `TRAIL_PIVOT_BARS = 20  // [builder default — handbook value to
be pinned]`, and `:63-64` use it as a **rolling extreme** over the 4h lens:

    trailLo = request.security(..., "240", ta.lowest(low,  TRAIL_PIVOT_BARS)[1], ...)
    trailHi = request.security(..., "240", ta.highest(high, TRAIL_PIVOT_BARS)[1], ...)

The handbook is **not silent here.** Step 5 specifies the construct outright: *"every newly
**confirmed** 4h swing pivot in your favor (**a (2,2) fractal — two bars each side**) drags the
stop behind it"* (`SSV12_LOGIC_2026-08-16.md:41`), and Part B pins it as measured and promoted:
*"**Trail = (2,2) pivots**, 0.5 offset, arms after +1R [measured then promoted]"* (`:85`).

**So the comment is wrong about its own debt.** It says a *value* awaits pinning; what actually
differs is the **mechanism**. A (2,2) fractal and a 20-bar rolling low are not the same object with
a different parameter — no integer substituted for `20` turns `ta.lowest(low, n)` into
`ta.pivotlow(2, 2)`.

**Failure scenario, concretely.** A (2,2) fractal advances the ratchet each time a new swing low
two bars clear on each side confirms — it tracks the *most recent* structure. A 20-bar rolling low
only rises as the old low ages out of the window. In a trade that runs steadily for several days
with rising swing lows, the handbook's trail ratchets up repeatedly behind each new pivot, while
the shipped trail stays pinned to a low up to 20×4h = **80 hours stale** and advances late or not
at all. The Part B evidence for the trail (*+0.032 expectancy improvement, tail-ratio 1.006*) was
measured on **(2,2) pivots**; it does not transfer to this construct.

### F-2 · THE TRAIL'S CLOSE-RAIL IS 0.5 ATR; THE HANDBOOK REQUIRES 1.0 ATR

Handbook Step 5, same sentence: the trail is *"pivot ± **0.5 ATR** offset, **never nearer than
1.0 ATR from the confirming close**"* (`SSV12_LOGIC_2026-08-16.md:42-43`). Two separate numbers —
an **offset** of 0.5 and a **floor** of 1.0.

The shipped code uses **0.5 for both** (`SS_Anchor_v12_T_0.pine:153,156,158,165`):

    cand = math.min(trailLo - 0.5 * tATR, close - 0.5 * tATR)   // pivot − 0.5 ATR, rail-checked vs price

**The entry stop gets this right and the trail does not**, which is what makes it look like a slip
rather than a decision: `:117` rails the S3 stop correctly at `close - 1.0 * tATR`, matching
handbook Step 3.

**Failure scenario, concretely.** The `math.min` takes whichever candidate sits further below
price, so the close-rail binds only when the pivot has come up close to price — precisely the
tight case the floor exists to govern. In that case the shipped trail may sit as near as **0.5 ATR
below the confirming close** where the handbook forbids anything nearer than 1.0 ATR: **a stop at
half the ruled minimum distance, in the one situation the rule was written for.** Winners dip
~0.31R against the trader before reaching +1R (handbook Step 4); a trail at 0.5 ATR is inside the
noise band that Step 4's mandated sleep exists to survive. The direction of the error is toward
being shaken out of winners — the exact cost Part B says arming-after-+1R was adopted to avoid.

### F-3 · THE STOP ANCHOR IS AN 800h EXTREME; THE HANDBOOK SPECIFIES THE NEAREST SWING PIVOT

Same class as F-1, on the entry stop rather than the trail. The handbook, Step 3: the stop sits
*"**Behind the nearest real 4h swing pivot** within the last 800 hours"*
(`SSV12_LOGIC_2026-08-16.md:32-33`). The Pine implements the **800-hour extreme**:

    piv4hLo = request.security(syminfo.tickerid, "240", ta.lowest(low, 200)[1], ...)   // 800h pivot

`ta.lowest(low, 200)` on the 4h lens is *the lowest low of the last 200 4h bars* — 800 hours, which
is why the comment says "800h pivot". But **"the lowest low in 800 hours" and "the nearest swing
pivot within 800 hours" are different points**, and usually far apart: the first is a single extreme
that may be a month old, the second is recent structure.

**Failure scenario.** In a market that sold off hard three weeks ago and has since based and turned
up, the 800h low is that old capitulation wick. The handbook would put the stop behind the *nearest*
4h swing pivot — close, giving a small R. The shipped code puts it behind the old wick — far, giving
a large R. **Since R is the unit every result is measured in** (handbook Step 3: *"That distance is
your R"*), position size computed from this stop is wrong by the same ratio, and every R-denominated
number downstream inherits it.

**This one is worse than F-1 and F-2 in one specific way:** the Anchor's header lists the pins it
knows are provisional, and this is **not among them** — `:31-32` claims *"Everything else quotes the
brief verbatim: … 800h/4h stop anchor"*. It does not. **An unflagged divergence is more dangerous
than a flagged one**, because the flagged ones will be revisited by definition.

### F-4 · THREE OF THE BRIEF'S FIVE BINDING CONSTRAINTS ARE UNMET IN THE ANCHOR

The brief's opening block is a **constraints ledger that "binds whoever implements"**, five items
verbatim: *"plain-text tooltips · 500-label cap + capless history dots · lookahead_on parity on
closed HTF bars · evidence class on every label · PARITY NOT CERTIFIED banner until operator
spot-checks"* (`BRIEF_ARGUS_PINE_SSV12T_2026-08-16.md:4-5`). Two hold. **Three do not.**

| constraint | state | evidence |
|---|---|---|
| plain-text tooltips | **met** | tooltips are plain strings throughout |
| `lookahead_on` parity on closed HTF bars | **met** | every `request.security` uses `gaps=barmerge.gaps_off, lookahead=barmerge.lookahead_on` |
| PARITY NOT CERTIFIED banner | **met** | `SS_Anchor_v12_T_0.pine:9` |
| **evidence class on every label** | **UNMET** | 7 `label.new` sites; only **2** carry a class — S1 window `[provisional]` (`:89`) and the S2 trigger tooltip (`:130`). The LPS label (`:146`), both trail-advance labels (`:161`, `:168`), the ½-OFF de-risk label (`:185`) and the bell label (`:206`) carry none. *(The 11 `alertcondition` messages do carry `[verified]`/`[provisional]` — the alerts comply, the labels do not.)* |
| **500-label cap + capless history dots** | **UNMET** | The cap is declared (`max_labels_count=500`, `:2-3`); the **capless dots do not exist** — `plotshape` count **0**, `plotchar` count **0**. Beyond 500 labels, deep history is simply lost. **SS12-SIGNAL does implement this** (12 `plotshape`, 6 `plotchar`), which is what makes the omission visible as an omission rather than a house style. |

Additionally, brief §4's *"Grid-set lens defaults inherited (5m/30m marks OFF — toll)"* is **not
implemented** in the Anchor: it has **no lens toggles and no `input.timeframe` at all** (its entire
input surface is 7 inputs, `:39-46`). The discipline survives only as advisory header prose
(`:35-36`). Nothing enforces it; load the Anchor on a 5m chart and it will draw.

**All of F-4 is reported, not fixed.** Adding plotchar dots or evidence classes is new rendering
code, which is builder work the operator has not commissioned in this filing.

---

### F-0 · SCOPE NOTE ON THESE FINDINGS

**All four (F-1 … F-4) bear on the Anchor.** MANTLE and SIGNAL were read for the same class of
defect. MANTLE is clean: 20 EMAs, 20 plots, 8 fills, zero events, zero alerts — it does exactly what
its header says. SIGNAL is clean on its rulings — the 12/89 pair appears in four independent places
with no 9/89 anywhere, and the 12/26 trigger matches A2-3 — with **one inconsistency worth a line**:
its **event** 5m lens defaults **OFF** with the tooltip *"ORACLE GRID: every class NET-negative at
5m … Default OFF by data"* (`:55`), while its **MTF cascade** 5m lens defaults **ON** (`:76`). The
same toll evidence argues for both; only one of them acts on it. Reported, not fixed.

**None of these findings affects the shas filed.** The files are filed exactly as delivered,
divergences included, because the record must hold what was delivered, not what should have been.

**Root cause of F-1, F-2 and F-3, stated once.** The Anchor was built **without either of its two
reference documents.** Its own header admits one: *"the handbook file was not attached this
session"* (`:27`). The other is in the brief itself — *"Base: **SS_v12_1.pine** (attach it)"* (§1) —
and **that file has never existed in `pine/`**; its absence *is* debt V-3 (§4, D-1), still live.
So the builder implemented a handbook it could not read, from a base file it could not open,
flagged what it knew it was guessing at, and got three constructs wrong. **The fix is to re-read
`SSV12_LOGIC_2026-08-16.md`, which does contain every one of the missing numbers** — not to
measure anything new.

---

---

## §5A · FOUND WHILE FILING, OUTSIDE THIS FILING'S SCOPE — AND TIME-CRITICAL

**THE ORACLE DAILY HAS BEEN FAILING FOR TWO DAYS AND NOTHING HAS REPORTED IT.**

This has nothing to do with the Pine estate. It was found because verifying debt D-4 ("BR-2
unchanged") meant reading BR-2's gate evidence. It is stated here, prominently, because the next
person to act on BR-2 will act on a false assumption otherwise.

`research_outputs/oracle/calibration/selfcheck_log.jsonl` holds 12 rows. The last four are **all
FAIL**:

| date | slot | verdict | detail | html_sha | seconds |
|---|---|---|---|---|---|
| 2026-08-20 | full | **FAIL** | `run failed` | `null` | 3.0 |
| 2026-08-20 | refresh | **FAIL** | `run failed` | `null` | 3.3 |
| 2026-08-21 | full | **FAIL** | `run failed` | `null` | 3.0 |
| 2026-08-21 | refresh | **FAIL** | `run failed` | `null` | 3.1 |

**Both slots, both days, no HTML produced, failing in ~3 seconds** — that is a crash on startup, not
a timeout or a slow run.

**The consequence for BR-2, stated as arithmetic.** Gate **G-BR2-2** requires PASS rows on **5 of the
last 7 days**. Distinct PASS dates are **2026-08-16, 08-17, 08-18, 08-19 — four**. 08-20 and 08-21
are FAIL on both slots. **BR-2 was parked to wake on 2026-08-22. On that date G-BR2-2 will read
FAIL, not PASS, unless the daily is repaired first — and repairing it on the 22nd does not
retroactively supply the two missing days.** The lane is waiting on a date that will not deliver.

**Why nobody has seen it:** `LEDGER_ARGUS.md` has not been appended since 2026-08-16, so the estate's
own reporting surface has been silent for five days. This document's ledger append is the first
entry since.

**Reported, not fixed** — repairing `oracle_daily` is outside a Pine filing's authority, and the
failure detail (`run failed`) is a wrapper-level message that needs the actual traceback read from
the launchd log before anyone guesses at a cause. **Owner: operator. This is the most time-critical
item in this document.**

---

## §6 · (d) SHAS AND BYTES — THE FILING OF RECORD

Verified twice: once at the source before copying, once in `pine/` after. `cmp` reported the pairs
byte-identical.

| file | sha256 (full) | bytes |
|---|---|---|
| `pine/SS12_MANTLE_v12_6.pine` | `f3b1a1262d233db34a981585ab29ff2aa5723ce25ca8d36382ac2575b714f558` | 11,274 |
| `pine/SS12_SIGNAL_v12_6.pine` | `9a4a97d3772d0c50d8d0c8528229a499ceb09b56e942999653b1ae2648ff4eca` | 20,249 |
| `pine/SS_Anchor_v12_T_0.pine` | `464cad81cf2a21d927e2a00f590ffdb13164ab58298f2d64f9b4de4bfd50d7a7` | 15,828 |

All three matched their expected sha256 prefixes (`f3b1a1262d233db3`, `9a4a97d3772d0c50`,
`464cad81cf2a21d9`) and expected byte counts exactly. No mismatch, no halt.

> **INTAKE DEVIATION, DISCLOSED.** The three files were expected in `~/Naiad/incoming/`. **That
> directory does not exist.** The files were found instead in **`~/Downloads/`**, under the exact
> expected names. Because a sha256 identifies content and not location, and all three matched to
> the full digest, this is a **provenance deviation, not a content mismatch** — the halt condition
> (*"ANY mismatch"*) was not met and the filing proceeded. `incoming/` was deliberately **not**
> created after the fact: manufacturing the staging directory the files never passed through would
> make this record say something untrue about where they came from.

**Not touched, by instruction — the historical files of record in `pine/`:**

| file | bytes | status |
|---|---|---|
| `pine/SS_v12_0_1.pine` | 15,004 | STAYS — historical file of record, the v12.1-era ancestor actually present (see §2) |
| `pine/SS_Cascade_v11.0.2.pine` | 57,718 | STAYS — prior estate |
| `pine/SS_Cascade_v11.3.pine` | 59,988 | STAYS — prior estate |

No `git rm` was issued, and no file in `pine/` was modified or removed.

---

## §7 · WHAT ELSE THE READING TURNED UP — observations, no action implied

These are not defects. They are properties an operator would otherwise discover by surprise.

**O-1 · THE ALERT SURFACE IS THE ANCHOR, ALONE.** MANTLE has zero `alertcondition()` calls; SIGNAL
has zero; ANCHOR has **eleven**. Despite SIGNAL's header claim *"every event, one instrument"*, it
renders events **visually only** — it will never fire a TradingView alert. If you want alerts, the
Anchor is the file to load. This appears deliberate (the brief commissioned the R1 alert set for
the Anchor and for nothing else), and it is recorded so nobody waits on a SIGNAL alert that cannot
come.

**O-2 · THE R1 ALERT SET IS COMPLETE.** APOLLO's brief §3 names ten alerts. The Anchor delivers all
ten as eleven `alertcondition()` calls: `window-open` and `TRIGGER` are each split by direction
(LONG/SHORT), and `window-close` and `counter-arming` are delivered as **one** alert —
`"window-close (counter-arming)"` — because they are the same event, a counter 12/89 cross.

**O-3 · touch-wins IS MANTLE'S ALONE.** The colour law of R-3 exists in MANTLE and in neither of the
other two. SIGNAL and ANCHOR have no palette preset and no per-line colour inputs; ANCHOR's eight
style colours are constants and are not user-editable at all. Reason it matters: recolouring your
fabric will not recolour your events, and there is no setting that makes it.

**O-4 · THE touch-wins IMPLEMENTATION IS ONE LINE.** For anyone auditing R-3:
`base = ground == "Custom" or cIn != defC ? cIn : f_pal(i)`, inside `lcol(i, cIn, defC, onX, dX)`.
The `cIn != defC` comparison **is** the corner case disclosed in R-3 — the law detects your touch
by value, so restoring a colour to its shipped default reads as "untouched".

**O-5 · THE ROOT CAUSE OF §5 IS STATED IN THE SOURCE.** The Anchor's own header explains why F-1 and
F-2 exist: *"BUILDER-DEFAULT PINS (**the handbook file was not attached this session**; each is
named, tooltip-flagged, awaiting the handbook's own number)"* (`SS_Anchor_v12_T_0.pine:27-28`). The
builder was working from the brief without the handbook, flagged every value it could not source,
and shipped honestly. **The handbook does contain the numbers** — so both findings close by
re-reading `SSV12_LOGIC_2026-08-16.md`, not by new measurement.

**O-6 · `C_WIN` IS DEAD.** `C_WIN = #B0BEC5` is declared in the Anchor (`:49`) and never referenced
anywhere else in the file. Cosmetic.

**O-8 · "SIX GATES" IS A COUNT THAT IS WRONG EVERYWHERE, IDENTICALLY.** The brief says *"six-gate
lifecycle"* (§1) and signs off *"one trade, six gates, zero ambiguity"* — while its own §2 enumerates
**nine** render blocks, S0 through S8. The Anchor's header inherits the error verbatim: *"THE SIX
GATES, IN RENDER ORDER:"* followed by nine rows. The handbook's Part A likewise runs STEP 0 through
STEP 8. **There are nine stages.** "Six gates" is inherited prose, not a count, and this document
uses it only in quotation.

**O-9 · THE TRIO IS A ONE-WAY DECLARATION, NOT A MUTUALLY AWARE SUITE.** MANTLE and SIGNAL each name
`SS Anchor v12-T.0` as a companion of record. **The Anchor names neither** — the strings `MANTLE`,
`SIGNAL` and `v12.6` return **zero hits** inside `SS_Anchor_v12_T_0.pine`. That is chronology, not
carelessness: the Anchor is dated 2026-08-17 and the other two 2026-08-21, four days later. Nothing
depends on the Anchor knowing about them; recorded so the asymmetry is not read as a missing edit.

**O-10 · THE ANCHOR'S SEVEN INPUTS ARE THE BUILDER'S OWN.** The brief specifies **no** user inputs of
any kind and no ATR length; the handbook specifies none either. All seven (`:39-46`) are the
builder's additions: six section toggles plus `atrLen = input.int(14)`. The 14 does match the
engine's register independently (`ATR_LEN` value 14, `ruled: true`, in `posture_canon.json`) — a
correct number, but arrived at without brief or handbook provenance. There is **no `input.timeframe`,
no `input.color` and no `input.string`** in the file.

**O-7 · THE PARITY BANNER IS STILL UP.** All three files carry *"PARITY NOT CERTIFIED until operator
spot-checks"* — consistent with debt D-1 being open, and correct as shipped.

---
---

## §8 · THE LEDGER ENTRY AND THE PUBLISH

Per CONVENTIONS §3.1, a build document that does not append its ledger line is an incomplete
deliverable. This document's entry was appended, append-only, to
**`exchange/status/LEDGER_ARGUS.md`** — the ARGUS ledger, because ruling R-1 folds the PINE lane
into ARGUS and there is no separate Pine ledger. The entry as appended:

    === STATUS_ARGUS — 2026-08-16 (PINE ESTATE FILED) ===
    NOW: Pine estate v12.6 filed: MANTLE (fabric) · SIGNAL (events) · ANCHOR (v12-T).
         PINE lane operates inside ARGUS by operator ruling.
    FACTS: three files, shas per build doc [verified] · 12/89 regime ruling recorded
           [ratified] · parity target = SS12-SIGNAL v12.6 [standing]
    PENDING: 1. operator parity spot-check (doubles as Oracle PARITY line) 2. Anchor
             pins await handbook 3. live week + BR-2 unchanged
    NEXT: iterate on operator screenshots. Owner: operator.
    === END STATUS ===

Publishing used the §3.4 invocation verbatim — `publish()` stages `exchange/**` only, guard-checks
the whole index, commits and pushes. **No `git add` and no `git commit` was issued by hand**, in
either direction, for any path. The commit hash and push result are stated on screen at the close
of the session that filed this, and in the run log; they are not written into this file, because a
file cannot contain the identity of the commit that first contains it.

**Box health at filing**, measured on the governing tick set (`exchange/**` + `LEDGER.md`) before
this document was added: **3,739,652 B — 23.37% of the 16,000,000 B box — level OK**, against warn
0.40 and refuse 0.70. Headroom to the warn line: **2,660,348 B**. This document is a few tens of
kilobytes and does not move the level. No file created by this session is over the absolute
64,000 B trip-wire.

---

## §9 · HOW TO CHECK THIS FILING YOURSELF

Four commands, no context required:

    cd ~/Naiad
    shasum -a 256 pine/SS12_MANTLE_v12_6.pine pine/SS12_SIGNAL_v12_6.pine pine/SS_Anchor_v12_T_0.pine
    grep -n 'TRAIL_PIVOT_BARS' pine/SS_Anchor_v12_T_0.pine
    sed -n '41p;42p;43p' exchange/reports/SSV12_LOGIC_2026-08-16.md

The first reproduces §6. The second shows F-1's `20` and its own "handbook value to be pinned"
comment. The third shows the handbook sentence that F-1 and F-2 say it should have been read
against — `(2,2) fractal`, `0.5 ATR` offset, `1.0 ATR` floor.

---

## §10 · WHAT IS OWED, AND BY WHOM — the short version

| # | item | owner | closes when |
|---|---|---|---|
| 1 | **Parity spot-check** — the Oracle mid-week PARITY glance, which doubles as the first V-3 spot-check against SS12-SIGNAL v12.6 | **operator** | a `PARITY: OK <date>` or `PARITY: mismatches:` line exists; also discharges gate G-BR2-3 |
| 2 | **F-1 · trail pivot** — 20-bar rolling extreme vs the handbook's `(2,2)` fractal | **APOLLO / operator** (a ruling, not a builder edit) | the construct is ruled, then implemented |
| 3 | **F-2 · trail close-rail** — 0.5 ATR vs the handbook's 1.0 ATR | **APOLLO / operator** | as above |
| 4 | **WINDOW/TRIGGER lens pin** — currently the chart's own timeframe | **APOLLO / operator** | a lens is pinned (the quickstart's "1H or 4H" is the nearest thing on record) |
| 5 | **The Anchor quickstart** — required by brief §4, exists, unfiled | **operator** | one instruction to file it |
| 6 | **`pine/` is uncommitted** — the three files live on one Mac | **operator** | one authorised commit of `pine/` |
| 7 | **`CONVENTIONS.md:536` contradicts R-1** — the lane roster still assigns the Pine indicator to APOLLO and has no PINE→ARGUS fold | **operator / HEPHAESTUS** (CONVENTIONS custody) | the roster row is corrected |
| 8 | **316 is not in the v12.6 display set** — it is half the tide pair and half the de-risk band (§3 R-2) | **operator** | ruled: either restore 316 to MANTLE, or record that tide is read off the Anchor only |
| 9 | **F-3 · stop anchor** — 800h extreme vs the handbook's *nearest* 4h swing pivot; **unflagged** in the Anchor's own pin list, and it sets R | **APOLLO / operator** | the construct is ruled, then implemented |
| 10 | **F-4 · three unmet brief constraints** — evidence class on every label · capless history dots · grid lens defaults | **operator** (commissions builder work) | the three are implemented or waived |
| 11 | **⚠ THE ORACLE DAILY IS DOWN** — four consecutive FAIL rows, both slots, 08-20 and 08-21; **G-BR2-2 will read FAIL on 2026-08-22** (§5A) | **operator** | the daily runs green again; the two lost days cannot be recovered retroactively |
| 12 | Live week + BR-2 | unchanged by this filing | per the BR-2 gates |

**If only one of these is done, do #11 — then #1.** #11 is a live outage with a deadline the estate
is already inside: BR-2 wakes 2026-08-22 onto a gate that will fail, and every day the daily stays
down pushes the earliest possible BR-2 execution further out. #1 is the next most urgent: it is
time-bound, discharges two debts at once, and nothing in the estate will remind the operator to do
it. **Items 2-10 can all wait; those two cannot.**


---

## §11 · FILE-DISPOSITION TABLE

Every file this session created, modified or moved. Box constants read live from
`scripts/publish_exchange.py`: `BOX_BYTES = 16,000,000` · `FLAG_BYTES = 64,000` (absolute) ·
warn 0.40 / refuse 0.70, governing the **tick set** (`exchange/**` + `LEDGER.md`).

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `pine/SS12_MANTLE_v12_6.pine` | yes | untracked (not ignored — `git check-ignore` exit 1) | **not committed** | **no** | **NOT PROTECTED** — GitHub does not hold it | n/a — `pine/` is outside `exchange/` and outside the tick set; unsynced |
| `pine/SS12_SIGNAL_v12_6.pine` | yes | untracked (not ignored) | **not committed** | **no** | **NOT PROTECTED** | n/a — outside the tick set; unsynced |
| `pine/SS_Anchor_v12_T_0.pine` | yes | untracked (not ignored) | **not committed** | **no** | **NOT PROTECTED** | n/a — outside the tick set; unsynced |
| `exchange/reports/BUILD_2026-08-16_PINE_ESTATE_V12_6.md` | yes | tracked by `publish()` | see §9 | see §9 | GitHub + project-knowledge box | counted in §9; **under** the 64,000 B wire |
| `exchange/status/LEDGER_ARGUS.md` | yes | tracked, **modified** (append-only) | see §9 | see §9 | GitHub + box | ~21 KB → grows by this append; under the wire |
| `exchange/status/daily/DAILY_2026-08-21.md` | yes | tracked, modified **before this session** | see §9 | see §9 | GitHub + box | pre-existing edit; rides along, see the note below |

> **WHY THE THREE PINE FILES ARE UNCOMMITTED, AND THIS IS THE CORRECT OUTCOME, NOT AN OMISSION.**
> CONVENTIONS §3.4 is explicit: *"`publish()` stages `exchange/**` only … Do NOT `git add` or `git
> commit` exchange files separately"*, and *"A `git add` of any file OUTSIDE `exchange/**` in the
> same paste goes nowhere and leaves it stranded as an uncommitted change. Commit non-exchange
> paths explicitly, in their own authorized commit."* (CL-13). `pine/` is outside `exchange/`.
> Committing it inside this paste is forbidden by the guard's path scope; committing it in a second
> commit needs an authorisation this session's instructions do not contain — STEP 5 authorised a
> publish per §3.4 and nothing wider.
> **CONSEQUENCE, STATED PLAINLY: the three files exist on this Mac's disk and nowhere else. Losing
> the machine loses them.** They are reproducible from `~/Downloads` only for as long as that
> folder is untouched. **One instruction — "commit pine/" — closes this.**

> **NOTE ON `DAILY_2026-08-21.md`.** This file was already modified before this session began (21
> insertions, unrelated to the Pine estate). Because `publish()` stages all of `exchange/**`, it
> **will be committed by the publish in §9** alongside this build document. That is the guard
> behaving as designed, not scope creep by this build, and it is disclosed rather than left for the
> operator to find in a diff.

**Nothing was deleted, renamed or moved.** `~/Downloads` was read, never modified.

