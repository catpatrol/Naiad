# ARGUS CYCLE 5 — SESSION SUMMARY

**Builder:** HEPHAESTUS · **Date:** 2026-08-06 · **Reviewer:** ARGUS
Five items, all executed. Cycle 4 was not re-run.

---

## HOW TO READ THIS

**§1 is the headline** — the last unverified quantity in the VWAP family is now
certified. **§2** is what else shipped. **§3** is where I corrected *you*, and
where I corrected myself. **§4** is the one decision I am handing back. **§5**
routes the census note.

**Nothing is adopted.** `PARITY NOT CERTIFIED` still prints on every render.

---

## §1 · THE VWAP FAMILY IS FULLY VERIFIED

For five cycles the anchored **σ on the 1h substrate** was the last quantity
nobody had checked against your chart. You supplied two 1H captures with
anchored bands enabled. **It passes.**

**42 values** — two closed bars × Week/Month/Quarter × seven levels:

| bar | anchor | bars | our σ | your implied σ | worst \|Δ\| |
|---|---|---|---|---|---|
| 2026-07-26T20:00Z | Week | 165 | 798.4663 | 798.47 | 0.0445 |
| | Month = Quarter | 621 | 1729.9887 | 1729.95 | 0.0486 |
| 2026-08-02T04:00Z | Week | 149 | 754.4595 | 754.45 | 0.0408 |
| | Month | 29 | 313.3966 | 313.37 | 0.0495 |
| | Quarter | 773 | 1608.6236 | 1608.63 | 0.0488 |

**Worst disagreement anywhere: 0.0495** — inside the 0.05 rounding half-step of
your one-decimal display, so what is left is your display precision, not our
arithmetic. **Both raw bars matched to every decimal first.** All **18 triples**
exactly symmetric at exact integer multiples of σ.

**`anchored_vwap` σ on 1h: UNVERIFIED → CERTIFIED. Nothing in the VWAP family is
now unverified.**

---

## §2 · WHAT ELSE SHIPPED

**`.gitignore` closed.** The SEQ8 gap that blocked the whole branch push on
2026-08-05 is gone — proven three ways (status count 13→12, `check-ignore`
naming lines 104/105, and a dry-run wildcard add now staging zero seq8 paths).
**You owe the SEQ8/DIONYSUS lane a note** that their bulk outputs are ignored
here and their five scripts remain untracked.

**A degeneracy note that had never fired.** In your 2026-07-26 capture, July
opens Q3, so Month and Quarter anchor on the *same bar* and their seven levels
are byte-identical — σ included. The collapse rule already merged them correctly
(14 → 7), but **only source comments said so**; nothing in the report did. A
reader seeing a 2-member cluster could not tell whether two tools agreed or one
tool was counted twice. It now prints.

**Episodes replace the bar-fraction view** (§3.1 explains why), and the
**maturity stabilisation** measurement that cycle 4 owed is delivered — with a
result I did not expect (§4).

---

## §3 · CORRECTIONS

### 3.1 Your §5.3 comparison was a category error — you were right to pull it

C4 compared time beyond ±1σ/±2σ/±3σ to a normal distribution's 31.7/4.6/0.27 and
called the tails "roughly double". Those figures describe **independent draws**.
Price relative to a VWAP is **persistent and autocorrelated** — once beyond a
band it tends to *stay* there, because trending is what carried it there. A ~50%
time-fraction measures persistence, not tail fatness. **Removed from
INTERFACE.md**, with a fixture keeping it out.

The replacement, per **episode** — one entry beyond the band until price returns
inside it, which is **one decision** however many bars it spans:

| band | episodes / asset-window / year | median length | median max \|z\| |
|---|---|---|---|
| ±2σ | **~122** | **2 bars** | ~2.2σ |
| ±3σ | **~12** | **1.5 bars** | ~3.2σ |

**8.82% of bars is ~122 events a year, not 772 opportunities. At σ3 it is about
twelve.**

### 3.2 ⚠ A correction to YOUR item-3.2 note

You wrote that σ_month 313.37 being under half σ_week 754.45 means "the monthly
band sits inside the weekly band — **structurally backwards**".

**The inequality is exact. "Backwards" is not.** At that bar your **Week anchor
was five days OLDER than your Month anchor** — 149 bars against 29. The
developing Month was the **shorter** lookback, so a smaller σ is arithmetically
**expected**. Calendar *names* invert against calendar *ages* at the start of
every month, and that is what happened.

**Your conclusion survives; the reasoning needs replacing.** The hazard is real
but it is a **presentation** hazard: a level labelled "Month" printed narrower
than one labelled "Week" misleads anyone whose intuition says a month contains a
week. That justifies the chip and the floor. Tested properly, σ orders with an
anchor's **actual age in 93.4% of 5,294 comparisons** — the estimator is sane.

### 3.3 Two mistakes of my own

**I nearly rewrote `.gitignore` wholesale.** My first append used Python's
default text mode, which on Windows converted the entire file LF→CRLF — a `105
insertions / 101 deletions` diff on a file I was authorised only to append to.
Caught it in the diff, rebuilt from the original bytes, amended. The committed
change is **4 insertions, 0 deletions**.

**My first degeneracy fixture asserted the wrong number.** I tested "exactly 2
members merge" against the full capture — but on that bar the **Week +2σ**
(66,787.75) sits 6.28 from Month/Quarter +2σ (66,794.03), inside the 32.57
collapse width, so three merge, not two. The fixture now tests the degeneracy in
isolation and the three-way merge as its own case. Worth knowing that genuine
near-coincidences between *different* anchors are common enough to trip a test.

---

## §4 · THE ONE DECISION — maturity floors ⭐

You asked me to measure, propose, and not apply. **The measurement did not go
the way the brief assumed**, so read this before ruling.

I tried three criteria. **Two are rejected, and the rejections are the finding.**

**1. Per-bar movement** ("how far does it move when a bar arrives") →
`line 16, bands 3`. **Rejected.** A volume-weighted population variance over few
bars is biased *low* and creeps upward, so it can be nearly motionless and badly
wrong at once. Item 3.2 of this same cycle is the counter-example: at 29 bars the
σ had "stabilised" 26 bars earlier by this test. **A 3-bar band floor would be
worse than the interim 30.**

**2. Convergence to the mature value** → `line 236, bands 231`. **Rejected as
circular** — distance to the 240-bar value is zero *at* 240 by construction. And
an anchored σ converges to nothing: as price wanders from the anchor,
dispersion-so-far genuinely grows.

**3. Fraction of the mature value** — non-circular, and the basis of what I
propose:

| bars | 10 | 30 | 60 | 120 | 180 |
|---|---|---|---|---|---|
| σ / mature | ~15% | **~33%** | **~50%** | ~77% | ~91% |

### PROPOSED, NOT APPLIED

```
line   >= 10 bars    UNCHANGED
bands  >= 60 bars    RAISED from 30
```

Sixty is where σ first carries **half** the dispersion it ends with. Thirty is
one **third** — thin enough that your 2026-08-02 Month band printed at 0.19 ATR
beside a Week band at 0.46.

**The honest caveat: no floor makes a developing anchor's σ "correct."** The
quantity keeps growing by construction. A floor only decides how misleading a
young band may be before it stops being *scored* — a judgement about
presentation, not a fact recoverable from data. That is why this is yours to
rule. **R3's 10/30 stand until you do.**

**Rolling windows need no floor at all** — every window is orders of magnitude
inside tolerance at steady state, and `warming` already refuses a short span.

---

## §5 · CENSUS — H-VBR's gauge just got harder

**H-VBR (VWAP Band Reversion)** — do fills entered at σ2/σ3 targeting the mean
differ in expectancy from the base book? Cross-scale replication required.

**Deflation gauge, stated in advance and now tightened:** a σ2 touch is *by
construction* "price is far from its recent volume-weighted mean". It must beat a
plain distance-from-mean or ATR-extension baseline or be filed as a redundant
dressing of a simpler fact.

**What cycle 5 adds:** the baseline is **per-episode**, not per-bar. Roughly
**122 σ2 events and 12 σ3 events per instrument per year** — far fewer than the
9.5%-of-bars figure suggests. **This raises the evidential bar rather than
lowering it**, and a σ3 study in particular will be sample-starved.

**H-VBT (VWAP Band Target)** unchanged: exits at confluence-scored VWAP levels
must beat riding to regime break, against the study's unsolved harvest problem
(73.67% of trades reaching +1R round-trip into loss).

**Firewall unchanged.** Counting episodes is OPS; what fraction revert is census
work under G-7. A fixture now enforces that on the **code**, including a ban on
the episode view looking past a run at all.

---

## §6 · PROVENANCE

`analytics` **1.4.0** · sha `e8a4959b…d20d66` · suite **271 passed / 1 skipped**
(was 262).

Commits `d6cf09d` (item 1) · `765db4b` (items 2+3) · `ea837eb` (items 4+5).

Paired with **`BUILDERS_REPORT_ARGUS_2026-08-06_C5.md`**.

— HEPHAESTUS, 2026-08-06
