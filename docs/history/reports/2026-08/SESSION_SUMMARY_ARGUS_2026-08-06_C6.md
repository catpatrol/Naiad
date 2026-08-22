# ARGUS CYCLE 6 — SESSION SUMMARY

**Builder:** HEPHAESTUS · **Date:** 2026-08-06 · **Reviewer:** ARGUS
Six items. Four built, two routed.

---

## §1 · THE BANNER IS DOWN ⭐

**All 42 anchored values match at your displayed precision. Zero mismatches.**
Re-run fresh against the live estate rather than quoted from cycle 5.

| | |
|---|---|
| values compared | **42** (two closed bars × W/M/Q × 7 levels) |
| mismatches at displayed precision | **0** |
| worst absolute delta | **0.0495** |
| worst \|bps\| | **0.0083** |

`parity_certified` is set. **`PARITY NOT CERTIFIED` appears zero times in the
render.**

### What replaced it, and why something had to

Certification is not silence. With the warning gone, the recipes that were
**never chart-certified** become the ones most likely to be mistaken for
verified. So every page now carries both lists:

| | |
|---|---|
| **CERTIFIED against your charts** | rolling VWAP (both substrates) · anchored VWAP **including σ** · the σ bands · oscillators + ATR · resampling |
| **FIXTURE-VERIFIED, NOT chart-certified** ⚠ | volume profile (POC/VAH/VAL) · LVN · value-area nesting |

**The profile family was excluded from the gate deliberately.** Our profile
spreads each bar's volume uniformly across its range — a declared approximation
over klines. TradingView's is a *different* approximation over data we do not
have. Comparing them would certify nothing whichever way it came out: agreement
would be a coincidence of two approximations, disagreement uninformative about
either. They keep a **permanent approximation chip**, and the *reason* is written
into the code so a later cycle does not read the exclusion as an oversight and
"fix" it.

**Scope:** BINANCE perpetuals, 1h substrate, hlc3 source. A reading from an
index or a spot pair is still a different number.

**What certification does NOT mean:** the arithmetic matches your charts.
Nothing about whether any of it predicts anything has been established.

---

## §2 · WHAT ELSE SHIPPED

**Maturity floors ruled** — line 10→16, bands 30→60, both on the cycle-5
measurement. `ANALYTICS_VERSION` 1.5.0, because registry membership genuinely
changes.

**The de-peg layer** — your framing, and it replaces bar count as the redundancy
test. Adjacent anchored pairs and anchored↔rolling counterparts now carry a peg
state, separation in bps and ATR, σ ratio, and both ages. Redundancy **prints**
rather than being suppressed, exactly as you asked.

**The hinge** — every reversion draft now carries **two** targets: A the mean
(pullback), B the dominant POC and opposing value-area edge (rejection). Both
with distance and R:R. **No preference between them**, enforced by fixture.

---

## §3 · WHERE I CORRECTED YOU, AND WHERE I CORRECTED MYSELF

### 3.1 ⚠ Your period-relative floor argument was wrong — and the correction is worth more than the floor

You proposed scaling the floor to the period (`period/4`) because a young σ
**inflates the σ-label** and manufactures false reversion signals.

**It does not.** An anchored σ grows as √t — but **price's displacement from the
anchored mean grows as √t too**. Both accumulate the same walk from the same
anchor, so their ratio — the z-score — is approximately **scale-free in time**.

Your own captures, same asset, same Month anchor:

| bars | σ | z |
|---|---|---|
| 29 | 313.3966 | **+2.0136** |
| 114 | 583.3876 | **+1.9389** |

**σ grew 86%. The reading moved 3.7%.** A young band's **width** is
age-dependent; its **reading** is not. You withdrew the proposal before I got
here — this is the evidence for why that was right, and it is now fixtured so
the same proposal cannot quietly return.

**What survives:** the floors are justified by **sampling noise alone**, and
band **widths** are comparable only at **comparable ages** — so age in bars now
prints beside every σ width.

### 3.2 I inverted the hinge direction and caught it before committing

A SHORT reversion sits at an **upper** band: the trade is a move *down* to the
mean, so **rejection is price continuing UP** — toward the VAH. A LONG mirrors
it: rejection continues *down*, toward the VAL. My first version had it exactly
backwards. The fixture now asserts the two sides never choose the same edge,
which is the assertion the broken version fails.

### 3.3 One consequence of the new floors you should see

The W anchor reopens Monday 00:00 UTC. Under the 60-bar band floor its **bands
are withheld until Wednesday 12:00 — 35.7% of the week**, up from 17.9% under
the interim 30. Today is Wednesday and W carries 66 bars: it cleared the floor
about six hours before this capture. Nothing else on the estate is affected
(every other anchor is far past 60), but for a third of every week the weekly
bands will now be absent from scoring. **That is the cost of the ruling, and it
is worth naming before you see it in a Monday brief.**

---

## §4 · CENSUS — ROUTED TO APOLLO, NOT IMPLEMENTED

### H-VDP — VWAP De-Peg (NEW, operator-originated)

Does the moment an anchored VWAP separates from its next-shorter neighbour mark
a regime change, or precede one?

Formulations: (i) de-peg timing vs SS governor flips against a matched
random-timing null; (ii) do fills born within N bars of a de-peg differ in
expectancy from the base book; (iii) cross-scale replication across W↔M, M↔Q,
Q↔Y.

**DEFLATION GAUGE, IN ADVANCE:** a de-peg is by construction *"the longer window
has accumulated enough distinct history to diverge"* — which is partly a
**calendar fact, not a market one**. **The null must be a calendar-matched
shuffle, not a uniform one**, or the finding will be the calendar. January 1
anchoring Y, Q and M simultaneously means de-pegs cluster at fixed dates every
year for every asset; a uniform null would score that as signal.

### H-VBR EXTENDED — the hinge dichotomy

At a σ2/σ3 touch, does price revert to the mean or reject and auction to the
opposing value? What discriminates them?

**⚠ A SAMPLE-SIZE WARNING TO ESTABLISH BEFORE REGISTERING, NOT AFTER.** Cycle 5
measured ~122 σ2 and ~12 σ3 episodes per asset-**window** per year. **Those
episodes are not independent across VWAPs** — one large move puts price beyond
σ2 on the 7d, the 30d and the weekly anchor at once. The effective sample is
closer to episodes-per-**ASSET** than per-asset-window. On a five-asset scorable
panel, **σ3 may be too thin for cross-scale replication at all.**

### H-FSU — the σ-width-in-ATR scale coordinate

Unchanged, now with item 1's caveat attached: **widths are only comparable at
comparable ages.**

---

## §5 · SCOPING NOTE — CUSTOM ANCHORS (proposed, NOT built)

You raised anchoring a VWAP at a significant high or low rather than a calendar
boundary. `analytics.confirmed_pivots` already supplies causality-disciplined
swing points, so the machinery exists.

**Which pivots would qualify.** `confirmed_pivots` on the 1d plane, 180-day
lookback, pivot(5,5) — the same feed the `structure` family already uses. They
are lag:5 by construction, so an anchor could only be *opened* five bars after
the pivot printed. That is a feature: it is the same discipline that stops an
unconfirmed pivot leaking into the registry.

**How many that adds — measured on today's capture:**

| | min | median | max |
|---|---|---|---|
| confirmed pivots per asset | 17 | **20** | 22 |
| registry now | 131 | **160** | 169 |

**Registry consequence.** Each anchor contributes 7 levels (line + 6 bands):

| policy | added levels | median registry | multiple |
|---|---|---|---|
| **all pivots** | +119 … +154 | **299** | **1.9×** |
| top-5 per side (10 anchors) | +70 | 230 | 1.44× |
| **top-3 per side (6 anchors)** | **+42** | **202** | **1.26×** |

**Doubling the registry is the wrong trade** — every threshold in the system was
calibrated against 131–169 levels, and the confluence score counts members, so
a 1.9× registry inflates scores everywhere without adding a single new *kind* of
evidence. **Recommend top-3 per side** as the opening position: +42 levels, 1.26×,
and it keeps the anchors that a human would actually name.

**Do maturity and de-peg apply unchanged?**

- **Maturity: yes, unchanged.** A pivot-anchored VWAP is an anchored VWAP; the
  16/60 floors apply as they stand. Note that a *recent* pivot anchor will spend
  its first 60 bars band-withheld, exactly as a fresh Month anchor does.
- **De-peg: NO — it needs a rethink.** The de-peg layer assumes a **nesting
  order** (W ⊂ M ⊂ Q ⊂ Y) so "the next-shorter anchor" is well defined. Pivot
  anchors have no such ordering: two pivots five days apart are not nested, they
  are simply two anchors. The de-peg question would have to be re-posed as
  "has this pivot anchor separated from the *calendar* anchor nearest its own
  age", and whether that is the same question is not obvious. **Flagging it
  rather than assuming it carries.**

**Not built. Proposed only.**

---

## §6 · PROVENANCE

`analytics` **1.5.0** · sha `ea5f02f2…c985dc91` · suite **286 passed / 1
skipped** (was 271).

Capture `briefs/brief_2026-08-05_post_ny.json` (certified), all four partitions
rebuilt, render 200 KB.

Commits `5f52b15` · `01870b6` · `8a0d8aa` · `6d11e9c`.

Paired with **`BUILDERS_REPORT_ARGUS_2026-08-06_C6.md`**.

— HEPHAESTUS, 2026-08-06
