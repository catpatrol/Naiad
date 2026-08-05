# ARGUS CYCLE 4 — SESSION SUMMARY

**Builder:** HEPHAESTUS · **Date:** 2026-08-03 · **Reviewer:** ARGUS
Replacement amendment executed in full. **D.4 was withdrawn and no distance
filter exists.** The render landed, so **D.7 is complete except the reversion
archetype**, which is the one deferred item.

---

## HOW TO READ THIS

§1 is the parity result — it closes a question that has been open for three
cycles. §2 is what shipped. §3 is where I was wrong or where a number I gave you
earlier was overstated. §4 has four decisions.

**Nothing is adopted.** `PARITY NOT CERTIFIED` still prints on every render, and
§1 explains exactly why that is still correct even though everything matched.

---

## §1 · PARITY — the anchored recipe is now fully settled

You re-read the chart with **Source = hlc3** and the numbers moved to where the
addendum said they would.

| | operator | ours | delta |
|---|---|---|---|
| Anchored Month VWAP | 63,112.3 | **63,112.2671** | **−0.0329** |
| all six Month bands | — | — | max **0.0445** |
| RVWAP 365 + six bands | 83,686.7 | **83,686.7122** | max **0.0452** |

**14 of 14 values match.**

### The prediction held

Before the setting changed, the addendum computed hlc3 = **63,112.2671** against
the then-current ohlc4 reading of 63,038.9, and predicted the reading would move
there if Source were switched. It did, to within **0.005 bps**.

That matters more than the match itself: it means the earlier ohlc4/hlc3
discrepancy was **fully explained**, not merely patched over. A recipe you can
predict the behaviour of is understood; one that merely agrees today is not.

### A.6.3 — the sigma, and a small correction to the reviewer

σ = **319.8884** against your observed band-1 distance of 319.9 → **−0.004%**.
The back-solved 320.13 misses by −0.075%, so **the back-solve was slightly off,
not our arithmetic.** True volume weights on the two bars: **0.394428 / 0.605572**.

### A.6.2 — RVWAP unchanged, as it must be

Rolling VWAP was always hlc3, and its 365d values are byte-identical to the
ohlc4-era capture. **No finding.** Its 1σ is **11.44 daily ATR** — which is the
direct evidence for your D.4 withdrawal: those bands are far because a year of
business was wide.

### A.6.4 — THE THING THAT IS STILL NOT TESTED

**Every parity check across four cycles has compared a 1D chart reading to a 1D
computation.** The ruled substrate for the instrument is **1h**. On the rolling
VWAP the 1h-vs-1D gap reached **0.377 daily-ATR** on the 7-day window.

**So the path the instrument actually runs on has never been externally
verified.** That is why the banner stays up. It is the single largest open item
and it is a measurement, not a build.

---

## §2 · WHAT SHIPPED

**D.5 stretch layer.** Price's distance from every volume-weighted mean in
**sigma units**, beside bps and ATR — eleven means per asset. Your worked example
reproduces exactly (+1.28σ Month, −1.07σ RVWAP365) and is fixtured.

**D.5.1 multi-scale disagreement**, live on BTC: `anchored M` **+1.38σ** while
`prior Y` sits **−2.94σ**. Spread 4.32σ, straddling ±1σ. Overextended up against
the month and down against the year at the same instant.

**D.6 band excursions.** Which σ band price has reached, on which side, distance
back to the mean in ATR and sigma. **No "captures since last touch" counter is
stored** — it is derived at panel-build time, so the capture stays
self-describing and the panel stays rebuildable from captures alone.

**The render.** Part I and Part II, Atlas visual language, 144 KB from a stored
capture. It **recomputes nothing** — asserted by AST: no analytics import, no
call to any computation function.

**D.7.1 target bucketing** — the mirror of R-1, and the guard you asked for.
NEAR/MID/FAR by target distance, ranked **within** buckets, never globally.
**D.7.2 target clusters** at any distance, ranked by score.
**`brief_note.py`** with an outcome-language guard at the one place a human types
free text into the record.

**INTERFACE.md regenerated** (34 KB) — it was stale and APOLLO cites it.
**Census note routed** with the H-VBR deflation gauge stated in advance.

---

## §3 · WHERE I WAS WRONG, OR OVERSTATED

### 3.1 Item 6 was overstated — by 40%

Cycle 2's headline was *"a line moved on 20 of 20 sides."* Median move: **0.127
ATR**, against a cluster width of **0.15**. Re-bucketed:

| | count |
|---|---|
| **relocations** (≥ one cluster width) | **12** |
| refinements (< one cluster width) | 8 |
| line in one view only | 0 |

**Twelve of twenty, not twenty of twenty.** Forty per cent of what I counted as
movement was the same structure re-centred inside its own cluster. You called
this and you were right; I should have split it the first time.

### 3.2 The D.7.1 bucketing does not currently bind — and that is informative

| bucket | n | median R:R |
|---|---|---|
| NEAR (<2 ATR) | **40** | 1.35 |
| MID (2–6) | 0 | — |
| FAR (>6) | 0 | — |

**Every target is under 2 ATR.** With a 148-level median registry, the next
opposing cluster scoring ≥4 is always close, so the far-target inflation the
bucketing guards against cannot currently occur.

That is not a reason to remove the guard — it is the reason **the reversion
archetype matters**. Its target is the VWAP *mean*, which for the far anchors
sits **12–21 ATR** away. MID and FAR stay empty until reversion drafts exist.

### 3.3 Fifth instance of the same fixture bug

A scan tripped on `stoch_rsi_k` — a capture *key* the render legitimately reads —
because I tested for the name rather than the call. That is the fifth time this
project has hit the identical pattern (F-F3's prohibition text, F-B29's "not
probability", F-B35's quoted `n=3`, F-B36's `claims_nothing`). **The rule is now
written into the fixtures: scan what the code DOES, never what it mentions, and
never the prose that disclaims a thing.**

---

## §4 · DECISIONS

### **D4-1 · The 1h substrate has never been parity-checked** ⭐ *the important one*

Four cycles of parity, all 1D-to-1D. The instrument runs on 1h.

| option | consequence |
|---|---|
| **(a) Read one 1h chart** | You set the chart to 1h and read 4–6 values (RVWAP 7d/30d, anchored M, RSI). Closes the gap directly and cheaply. |
| **(b) Switch the spec to the plane's bars** | D3-1's option (b). Then the 1D readings already collected ARE the verification, and 1h never needs testing because nothing computes on it. |
| **(c) Accept the gap** | The banner stays up indefinitely on a technicality nobody intends to resolve. |

**Recommendation: (a) then decide D3-1.** One 1h reading converts an open
question into a closed one for the cost of a single screenshot.

### **D4-2 · Reversion archetype — build it in cycle 5?**

Not built. §3.2 shows it is the missing half of the R:R board: continuation
drafts target *nearby* clusters, reversion drafts target the *mean*, and the mean
is where the far distance lives.

**Recommendation: build it in cycle 5**, with the σ2/σ3 entry gated on
`thin_sample=False` so a fresh anchor cannot manufacture a draft.

### **D4-3 · Minimum-sample rule for anchored bands (DA-2, still open)**

Proposed last addendum, still not implemented, and D.8 now quantifies it: **3
thin_sample flags across 102 VWAPs** today — rare, but they cluster at exactly
the moments a new anchor opens.

**Recommendation: ≥30 bars on 1h before anchored BANDS emit; the LINE prints
earlier with a chip.** Unchanged from the addendum.

### **D4-4 · Registry is 126–173 (median 148) against §5.3's 180–200**

The remaining gap is not prior anchors any more — those are in. It is that
§5.3's estimate was made before the layers existed.

**Recommendation: amend §5.3 to the measured range** rather than adding levels to
reach a forecast. Thresholds are being re-ratified against measurement anyway.

---

## §5 · WHAT REMAINS

- **Reversion archetype** (D.7 second half) — cycle 5
- **1h parity reading** — operator, D4-1
- **DA-2 minimum-sample rule** — reviewer, D4-3
- **DA-1/DA-3** — anchored source and the CONVENTIONS upgrade to VERIFIED; both
  now moot on source (hlc3 confirmed) but the CONVENTIONS text still says
  "INFERRED" and should be corrected
- **v1.1 retirement** — the render exists, so ruling D-3's condition is met

---

## §6 · PROVENANCE

`analytics` **1.3.0** · sha `da81034d…c731` · `rules_version` 2.0.0 ·
`schema_version` 2.1.0 · suite **248 passed / 1 skipped**.

Commits: `e127869` (D.5/D.6) · `4239ef7` (stage E render) · `6a758f6` (F+G).
Capture `c60eac9a…9bc2`. Paired with `BUILDERS_REPORT_ARGUS_2026-08-03_C4.md`.

**Firewall unchanged.** Confluence measures agreement between tools, not edge.
R:R measures geometry, not probability. Recording is OPS; H-VBR and H-VBT are
census work under G-7, routed to APOLLO with their deflation gauges stated in
advance.

— HEPHAESTUS, 2026-08-03
